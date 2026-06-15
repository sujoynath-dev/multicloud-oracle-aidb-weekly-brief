# Local CLI Quickstart

This repository now includes a portable Python CLI called `multicloud-aidb-brief`. It can generate, verify, and send the weekly Oracle AI Database multicloud brief without requiring Codex-specific presentation runtime paths.

## Install

From a cloned repository:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

The package has no required third-party runtime dependencies.

## Check The Local Environment

```bash
multicloud-aidb-brief doctor
```

This reports the repository root, Python executable, mail connector path, workspace presence, and Outlook automation availability on macOS.

## Build A Deck

```bash
multicloud-aidb-brief build \
  --week-ending 2026-06-15 \
  --verify
```

By default, the generated deck is written to:

```text
dist/weekly-multicloud-announcements-and-innovations-2026-06-15-redwood.pptx
```

The CLI also writes a sibling `.manifest.json` file with the title, week-ending date, coverage window, slide count, source count, and source ledger.

To write to a custom path:

```bash
multicloud-aidb-brief build \
  --week-ending 2026-06-15 \
  --output ./weekly-multicloud-announcements-and-innovations-2026-06-15-redwood.pptx \
  --verify
```

To also copy the generated PPTX into the checked-in PowerPoint workspace output folder:

```bash
multicloud-aidb-brief build \
  --week-ending 2026-06-15 \
  --sync-workspace-output \
  --verify
```

## Verify An Existing Deck

```bash
multicloud-aidb-brief verify \
  weekly-multicloud-announcements-and-innovations-2026-06-15-redwood.pptx
```

The verifier checks that the file is a valid PPTX package, contains the expected 10 slides, and has at least 15 appendix hyperlink relationships.

## Print Official Sources

```bash
multicloud-aidb-brief sources
```

For automation:

```bash
multicloud-aidb-brief sources --json
```

## Send A Deck

Dry-run first:

```bash
multicloud-aidb-brief send \
  --mode outlook \
  --dry-run \
  --to sujoy.nath@oracle.com \
  --subject "Weekly Multicloud Announcements and Innovations - week ending 2026-06-15" \
  --attachment weekly-multicloud-announcements-and-innovations-2026-06-15-redwood.pptx
```

Send for real:

```bash
multicloud-aidb-brief send \
  --mode outlook \
  --to sujoy.nath@oracle.com \
  --subject "Weekly Multicloud Announcements and Innovations - week ending 2026-06-15" \
  --attachment weekly-multicloud-announcements-and-innovations-2026-06-15-redwood.pptx
```

For SMTP, configure the variables in `tools/mail_config.example.env` and pass `--mode smtp`.

## Notes

- The portable CLI builds a Redwood-themed deck from the checked-in evidence and slide model.
- The original Codex Presentations workspace remains in `outputs/manual-20260612-redwood-ppt/presentations/multicloud-announcements/` for richer visual iteration.
- Weekly source research still needs to be refreshed from official Oracle, AWS, Google Cloud, and Microsoft pages before publishing a new dated brief.
