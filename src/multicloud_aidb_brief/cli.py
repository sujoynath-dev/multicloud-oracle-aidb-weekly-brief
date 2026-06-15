from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

from .brief_data import DEFAULT_RECIPIENT, DEFAULT_TIMEZONE, source_ledger
from .deck import build_deck, find_repo_root, output_name, parse_date
from .verify import verify_pptx


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="multicloud-aidb-brief",
        description="Generate, verify, and send the weekly Oracle AI Database multicloud brief.",
    )
    parser.add_argument("--repo-root", default=None, help="Path to a cloned repository. Defaults to the current directory or nearest repo root.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build = subparsers.add_parser("build", help="Build a portable Redwood-themed PPTX.")
    build.add_argument("--week-ending", default=None, help="Week-ending date in YYYY-MM-DD format. Defaults to today in Australia/Melbourne.")
    build.add_argument("--timezone", default=DEFAULT_TIMEZONE, help=f"Timezone for default dates. Default: {DEFAULT_TIMEZONE}.")
    build.add_argument("--output", default=None, help="Output PPTX path. Default: dist/<dated filename>.")
    build.add_argument("--sync-workspace-output", action="store_true", help="Also copy the PPTX into the checked-in PowerPoint output workspace.")
    build.add_argument("--verify", action="store_true", help="Verify the generated PPTX package and appendix hyperlinks.")
    build.add_argument("--json", action="store_true", help="Print machine-readable JSON.")

    verify = subparsers.add_parser("verify", help="Verify a generated PPTX.")
    verify.add_argument("pptx", help="PPTX path to verify.")
    verify.add_argument("--expected-slides", type=int, default=10)
    verify.add_argument("--min-hyperlinks", type=int, default=15)
    verify.add_argument("--json", action="store_true", help="Print machine-readable JSON.")

    sources = subparsers.add_parser("sources", help="Print the official source ledger.")
    sources.add_argument("--json", action="store_true", help="Print machine-readable JSON.")

    send = subparsers.add_parser("send", help="Send a PPTX using the local mail connector.")
    send.add_argument("--attachment", required=True, help="PPTX attachment path.")
    send.add_argument("--to", action="append", default=[], help="Recipient email address. May be repeated or comma-separated.")
    send.add_argument("--subject", default=None, help="Email subject.")
    send.add_argument("--body", default="Attached is the weekly Oracle Database multicloud announcements and innovations brief.")
    send.add_argument("--mode", choices=["auto", "outlook", "smtp"], default="auto")
    send.add_argument("--timeout-seconds", type=int, default=180)
    send.add_argument("--dry-run", action="store_true")
    send.add_argument("--draft", action="store_true")

    doctor = subparsers.add_parser("doctor", help="Check local tool availability.")
    doctor.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    return parser


def repo_root_from_args(args: argparse.Namespace) -> Path:
    return Path(args.repo_root).resolve() if args.repo_root else find_repo_root()


def command_build(args: argparse.Namespace) -> int:
    repo_root = repo_root_from_args(args)
    week_ending = parse_date(args.week_ending, args.timezone)
    output = Path(args.output).resolve() if args.output else (repo_root / "dist" / output_name(week_ending)).resolve()
    manifest = build_deck(repo_root, week_ending, output, sync_workspace=args.sync_workspace_output)
    result: dict[str, object] = {"build": manifest}
    if args.verify:
        result["verify"] = verify_pptx(output)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Built {output}")
        print(f"Manifest {output.with_suffix('.manifest.json')}")
        if args.verify:
            verify = result["verify"]
            assert isinstance(verify, dict)
            print(f"Verified {verify['slideCount']} slides and {verify['hyperlinkCount']} hyperlinks")
    return 0


def command_verify(args: argparse.Namespace) -> int:
    result = verify_pptx(Path(args.pptx).resolve(), expected_slides=args.expected_slides, min_hyperlinks=args.min_hyperlinks)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"OK: {result['slideCount']} slides, {result['hyperlinkCount']} hyperlinks, {result['bytes']} bytes")
    return 0


def command_sources(args: argparse.Namespace) -> int:
    rows = [source.__dict__ for source in source_ledger()]
    if args.json:
        print(json.dumps(rows, indent=2))
    else:
        for row in rows:
            print(f"{row['provider']}: {row['topic']} - {row['url']}")
    return 0


def command_send(args: argparse.Namespace) -> int:
    repo_root = repo_root_from_args(args)
    connector = repo_root / "tools" / "send_weekly_brief_email.py"
    if not connector.exists():
        raise FileNotFoundError(f"Mail connector not found: {connector}")
    recipients = args.to or [DEFAULT_RECIPIENT]
    subject = args.subject or "Weekly Multicloud Announcements and Innovations"
    command = [
        sys.executable,
        str(connector),
        "--mode",
        args.mode,
        "--timeout-seconds",
        str(args.timeout_seconds),
        "--subject",
        subject,
        "--body",
        args.body,
        "--attachment",
        str(Path(args.attachment).resolve()),
    ]
    for recipient in recipients:
        command.extend(["--to", recipient])
    if args.dry_run:
        command.append("--dry-run")
    if args.draft:
        command.append("--draft")
    result = subprocess.run(command, text=True, capture_output=False, check=False)
    return result.returncode


def command_doctor(args: argparse.Namespace) -> int:
    repo_root = repo_root_from_args(args)
    checks = {
        "repoRoot": str(repo_root),
        "python": sys.executable,
        "mailConnector": str(repo_root / "tools" / "send_weekly_brief_email.py"),
        "mailConnectorExists": (repo_root / "tools" / "send_weekly_brief_email.py").exists(),
        "workspaceExists": (repo_root / "outputs/manual-20260612-redwood-ppt/presentations/multicloud-announcements").exists(),
        "osascript": shutil.which("osascript"),
    }
    if args.json:
        print(json.dumps(checks, indent=2))
    else:
        for key, value in checks.items():
            print(f"{key}: {value}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "build":
            return command_build(args)
        if args.command == "verify":
            return command_verify(args)
        if args.command == "sources":
            return command_sources(args)
        if args.command == "send":
            return command_send(args)
        if args.command == "doctor":
            return command_doctor(args)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
