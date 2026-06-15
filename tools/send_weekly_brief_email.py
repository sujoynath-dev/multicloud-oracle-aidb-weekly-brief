#!/usr/bin/env python3
"""
Send the weekly multicloud Oracle Database brief as an email attachment.

Primary mode: Microsoft Outlook for macOS via AppleScript.
Fallback mode: SMTP using MAIL_* environment variables.
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import shutil
import smtplib
import subprocess
import sys
from email.message import EmailMessage
from pathlib import Path


OUTLOOK_APP = Path("/Applications/Microsoft Outlook.app")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["auto", "outlook", "smtp"], default="auto")
    parser.add_argument("--to", action="append", required=True, help="Recipient email address. May be repeated.")
    parser.add_argument("--subject", required=True)
    parser.add_argument("--body", required=True)
    parser.add_argument("--attachment", required=True)
    parser.add_argument("--from-address", default=os.environ.get("MAIL_FROM"))
    parser.add_argument("--timeout-seconds", type=int, default=180, help="Timeout for Outlook automation.")
    parser.add_argument("--dry-run", action="store_true", help="Validate inputs without sending.")
    parser.add_argument("--draft", action="store_true", help="Outlook only: open a draft instead of sending.")
    return parser.parse_args()


def normalize_recipients(values: list[str]) -> list[str]:
    recipients: list[str] = []
    for value in values:
        for part in value.split(","):
            address = part.strip()
            if address:
                recipients.append(address)
    if not recipients:
        raise ValueError("At least one recipient is required.")
    return recipients


def validate_attachment(path_text: str) -> Path:
    path = Path(path_text).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"Attachment not found: {path}")
    if not path.is_file():
        raise ValueError(f"Attachment is not a file: {path}")
    if path.stat().st_size <= 0:
        raise ValueError(f"Attachment is empty: {path}")
    return path


def choose_mode(requested: str) -> str:
    if requested != "auto":
        return requested
    if OUTLOOK_APP.exists() and shutil.which("osascript"):
        return "outlook"
    if os.environ.get("MAIL_SMTP_HOST"):
        return "smtp"
    raise RuntimeError("No mail connector available: Outlook is unavailable and MAIL_SMTP_HOST is not set.")


def send_with_outlook(
    recipients: list[str],
    subject: str,
    body: str,
    attachment: Path,
    *,
    dry_run: bool,
    draft: bool,
    timeout_seconds: int,
) -> None:
    if not OUTLOOK_APP.exists():
        raise RuntimeError("Microsoft Outlook is not installed at /Applications/Microsoft Outlook.app.")
    if not shutil.which("osascript"):
        raise RuntimeError("osascript is not available.")

    if dry_run:
        print(json.dumps({
            "mode": "outlook",
            "action": "draft" if draft else "send",
            "to": recipients,
            "subject": subject,
            "attachment": str(attachment),
            "attachmentBytes": attachment.stat().st_size,
        }, indent=2))
        return

    script = r'''
on run argv
  set recipientString to item 1 of argv
  set messageSubject to item 2 of argv
  set messageBody to item 3 of argv
  set attachmentPath to item 4 of argv
  set sendNow to item 5 of argv

  set oldDelimiters to AppleScript's text item delimiters
  set AppleScript's text item delimiters to ","
  set recipientList to text items of recipientString
  set AppleScript's text item delimiters to oldDelimiters

  tell application "Microsoft Outlook"
    set newMessage to make new outgoing message with properties {subject:messageSubject, content:messageBody}
    repeat with recipientAddress in recipientList
      set cleanAddress to recipientAddress as text
      if cleanAddress is not "" then
        make new recipient at newMessage with properties {email address:{address:cleanAddress}}
      end if
    end repeat
    make new attachment at newMessage with properties {file:(POSIX file attachmentPath)}
    if sendNow is "true" then
      send newMessage
    else
      open newMessage
    end if
  end tell
end run
'''
    try:
        result = subprocess.run(
            [
                "osascript",
                "-e",
                script,
                "--",
                ",".join(recipients),
                subject,
                body,
                str(attachment),
                "false" if draft else "true",
            ],
            text=True,
            capture_output=True,
            check=False,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(
            "Outlook automation timed out. Open Outlook once and approve any macOS "
            "Automation permission prompt for the terminal/Codex process, then retry."
        ) from exc
    if result.returncode != 0:
        raise RuntimeError(
            "Outlook send failed.\n"
            f"stdout: {result.stdout.strip()}\n"
            f"stderr: {result.stderr.strip()}"
        )
    print(json.dumps({"mode": "outlook", "sent": not draft, "draft": draft, "to": recipients}, indent=2))


def send_with_smtp(
    recipients: list[str],
    subject: str,
    body: str,
    attachment: Path,
    *,
    from_address: str | None,
    dry_run: bool,
) -> None:
    host = os.environ.get("MAIL_SMTP_HOST")
    if not host:
        raise RuntimeError("MAIL_SMTP_HOST is required for SMTP mode.")
    port = int(os.environ.get("MAIL_SMTP_PORT", "587"))
    username = os.environ.get("MAIL_SMTP_USERNAME")
    password = os.environ.get("MAIL_SMTP_PASSWORD")
    use_ssl = os.environ.get("MAIL_SMTP_SSL", "false").lower() in {"1", "true", "yes"}
    use_starttls = os.environ.get("MAIL_SMTP_STARTTLS", "true").lower() in {"1", "true", "yes"}
    sender = from_address or username
    if not sender:
        raise RuntimeError("MAIL_FROM or MAIL_SMTP_USERNAME is required for SMTP mode.")

    if dry_run:
        print(json.dumps({
            "mode": "smtp",
            "host": host,
            "port": port,
            "from": sender,
            "to": recipients,
            "subject": subject,
            "attachment": str(attachment),
            "attachmentBytes": attachment.stat().st_size,
        }, indent=2))
        return

    message = EmailMessage()
    message["From"] = sender
    message["To"] = ", ".join(recipients)
    message["Subject"] = subject
    message.set_content(body)

    content_type, _ = mimetypes.guess_type(str(attachment))
    maintype, subtype = (content_type or "application/octet-stream").split("/", 1)
    message.add_attachment(
        attachment.read_bytes(),
        maintype=maintype,
        subtype=subtype,
        filename=attachment.name,
    )

    smtp_class = smtplib.SMTP_SSL if use_ssl else smtplib.SMTP
    with smtp_class(host, port, timeout=60) as smtp:
        if use_starttls and not use_ssl:
            smtp.starttls()
        if username and password:
            smtp.login(username, password)
        smtp.send_message(message)

    print(json.dumps({"mode": "smtp", "sent": True, "to": recipients}, indent=2))


def main() -> int:
    args = parse_args()
    try:
        recipients = normalize_recipients(args.to)
        attachment = validate_attachment(args.attachment)
        mode = choose_mode(args.mode)
        if mode == "outlook":
            send_with_outlook(
                recipients,
                args.subject,
                args.body,
                attachment,
                dry_run=args.dry_run,
                draft=args.draft,
                timeout_seconds=args.timeout_seconds,
            )
        elif mode == "smtp":
            send_with_smtp(
                recipients,
                args.subject,
                args.body,
                attachment,
                from_address=args.from_address,
                dry_run=args.dry_run,
            )
        else:
            raise RuntimeError(f"Unsupported mode: {mode}")
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
