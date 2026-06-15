# Weekly Multicloud Oracle AI Database Brief

Reusable source, generated artifacts, automation helpers, and a portable local CLI for a weekly official-source executive brief covering Oracle Database multicloud announcements and innovations across OCI, Google Cloud, AWS, and Azure.

The current brief is titled **Weekly Multicloud Announcements and Innovations**. It focuses on Oracle Database on Exadata and Autonomous AI Database, then turns those announcements into architecture ideas that combine Oracle data platforms with AI offerings such as Gemini Enterprise, Amazon Bedrock, Microsoft Foundry, and OCI Generative AI.

## Current Deliverables

- `weekly-multicloud-announcements-and-innovations-2026-06-15-redwood.pptx`: latest shareable Redwood-themed PowerPoint deck at the repository root.
- `outputs/manual-20260612-redwood-ppt/presentations/multicloud-announcements/output/weekly-multicloud-announcements-and-innovations-2026-06-15-redwood.pptx`: generated deck copy inside the PowerPoint source workspace.
- `outputs/manual-20260612-redwood-ppt/presentations/multicloud-announcements/preview/contact-sheet.png`: rendered contact sheet used for visual QA.
- `outputs/manual-20260612-redwood-ppt/presentations/multicloud-announcements/`: editable deck workspace with slide modules, theme helpers, layout JSON, official provider assets, previews, build manifest, and source notes.

The older root-level HTML/PDF brief artifacts and the undated root PPTX have been removed. The PowerPoint deck is now the primary output format.

## Repository Layout

- `pyproject.toml`: installable Python package metadata for the reusable local CLI.
- `src/multicloud_aidb_brief/`: portable CLI source for building, verifying, listing sources, and sending the deck.
- `docs/local-cli.md`: local setup and command reference for users who fork or clone the repository.
- `outputs/manual-20260612-redwood-ppt/presentations/multicloud-announcements/slides/`: slide source modules for the 10-slide deck.
- `outputs/manual-20260612-redwood-ppt/presentations/multicloud-announcements/assets/`: official provider logo/header captures and Redwood visual references.
- `outputs/manual-20260612-redwood-ppt/presentations/multicloud-announcements/build-deck.mjs`: local Codex Presentations build helper for regenerating previews, layout files, manifest, and PPTX output.
- `outputs/manual-20260612-redwood-ppt/presentations/multicloud-announcements/patch-pptx-hyperlinks.py`: post-build hyperlink patcher for the one-slide source appendix.
- `tools/send_weekly_brief_email.py`: real mail connector. It supports Microsoft Outlook for macOS via AppleScript and SMTP fallback.
- `tools/mail_config.example.env`: SMTP fallback configuration template. Do not commit real credentials.
- `skills/create-multicloud-oracle-aidb-brief/`: reusable Codex skill and detailed prompt for recreating, updating, scheduling, or emailing the weekly brief.

## Workflow Summary

1. Research only official Oracle, AWS, Google Cloud, and Microsoft sources.
2. Separate current-week announcements from recent watchlist items.
3. Build an editable Oracle Redwood-style PowerPoint deck.
4. Use provider logos and visual references captured from official pages.
5. Keep diagrams and arrows as robust editable PowerPoint shapes.
6. Add a one-slide appendix grouped by OCI, GCP, AWS, and Azure.
7. Link each appendix topic label directly to its official source URL.
8. Render and inspect previews before publishing.
9. Send the verified PPTX through the local mail connector.

## Local CLI

Install the reusable CLI from a cloned repository:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Build and verify the current brief locally:

```bash
multicloud-aidb-brief build \
  --week-ending 2026-06-15 \
  --verify
```

Useful commands:

```bash
multicloud-aidb-brief doctor
multicloud-aidb-brief sources
multicloud-aidb-brief verify weekly-multicloud-announcements-and-innovations-2026-06-15-redwood.pptx
```

See `docs/local-cli.md` for the full command reference, including mail delivery.

## Advanced Codex Rebuild

The portable CLI is the recommended local path for forks. The original presentation workspace is still available for Codex-based visual iteration. From the repository root, regenerate the current deck with:

```bash
PYTHON=/path/to/python3 node \
  outputs/manual-20260612-redwood-ppt/presentations/multicloud-announcements/build-deck.mjs \
  outputs/manual-20260612-redwood-ppt/presentations/multicloud-announcements/output/weekly-multicloud-announcements-and-innovations-2026-06-15-redwood.pptx
```

Then patch appendix hyperlinks and copy the verified deck to the root shareable artifact:

```bash
python3 outputs/manual-20260612-redwood-ppt/presentations/multicloud-announcements/patch-pptx-hyperlinks.py \
  outputs/manual-20260612-redwood-ppt/presentations/multicloud-announcements/output/weekly-multicloud-announcements-and-innovations-2026-06-15-redwood.pptx \
  weekly-multicloud-announcements-and-innovations-2026-06-15-redwood.pptx
```

Before publishing, verify that the PPTX is a valid PowerPoint package, has 10 slides, and that the appendix hyperlinks are present.

## Reusing The Codex Skill

The reusable skill is stored at:

```text
skills/create-multicloud-oracle-aidb-brief/
```

To install it into a Codex environment, copy that folder into:

```text
~/.codex/skills/create-multicloud-oracle-aidb-brief
```

Then invoke it with:

```text
Use $create-multicloud-oracle-aidb-brief to create this week's official Redwood PowerPoint brief.
```

## Sending The Brief

The current manual Outlook send pattern is:

```bash
python3 tools/send_weekly_brief_email.py \
  --mode outlook \
  --timeout-seconds 180 \
  --to sujoy.nath@oracle.com \
  --subject "Weekly Multicloud Announcements and Innovations - week ending 2026-06-15" \
  --body "Attached is the weekly Oracle Database multicloud announcements and innovations brief." \
  --attachment weekly-multicloud-announcements-and-innovations-2026-06-15-redwood.pptx
```

Delivery should only be considered successful when the script exits with code `0` and returns `"sent": true`.

For non-Outlook environments, configure SMTP variables based on `tools/mail_config.example.env` and run the connector with `--mode smtp`.

## Automation

The weekly schedule is managed in Codex automation, not in this repository. The intended schedule is:

- Every Monday at 9:00 AM Australia/Melbourne time.
- Recipient: `sujoy.nath@oracle.com`.
- Attachment: the latest verified Redwood PowerPoint deck.
- Mail path: `tools/send_weekly_brief_email.py`, preferably in Outlook mode on macOS.

If delivery fails, preserve the failure output and treat the email as unsent until the connector returns `"sent": true`.

## Notes For Forks

- Do not commit SMTP passwords, app passwords, tokens, private `.env` files, or generated failure logs.
- Update source links each week from official pages rather than relying on stale memory.
- Keep transient inspection files such as `*.inspect.ndjson` out of Git.
- If you change the deck structure, rerender and inspect the contact sheet before publishing.
- If you run the advanced Codex builder outside this workspace, set `PRESENTATIONS_SKILL_DIR`, `PRESENTATIONS_SKILL_SCRIPTS_DIR`, `ARTIFACT_TOOL_UTILS_PATH`, or `MAKE_CONTACT_SHEET_PATH` for your local presentation runtime.
