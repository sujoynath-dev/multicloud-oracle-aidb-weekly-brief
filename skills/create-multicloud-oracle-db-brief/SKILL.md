---
name: create-multicloud-oracle-db-brief
description: Create, update, or schedule official-source weekly PowerPoint/PDF briefs about Oracle Database multicloud announcements and innovations across OCI, Google Cloud, AWS, and Azure. Use when Codex is asked to build a Redwood-themed weekly Oracle Database on Exadata or Autonomous AI Database deck, summarize hyperscaler announcements, add clickable source appendices, fix PowerPoint arrows or links, or automate emailing the brief on a weekly Melbourne-time schedule.
---

# Create Multicloud Oracle DB Brief

## Overview

Create a polished, official-source weekly executive brief for Oracle Database multicloud activity. Default to an editable PowerPoint deck unless the user explicitly asks for PDF, and use the official Oracle Redwood visual language: quiet near-white surfaces, charcoal typography, restrained Oracle red and teal accents, provider logos from official pages, and clean enterprise architecture diagrams.

When creating an automation prompt or when the user asks for a detailed reusable prompt, load [references/weekly-brief-prompt.md](references/weekly-brief-prompt.md).

## Workflow

1. Establish the week and output.
   - Use the user's locale and timezone; for this workflow default to Australia/Melbourne when the user mentions Melbourne time.
   - Title the deck `Weekly Multicloud Announcements and Innovations`.
   - Save the final file with a clear week-ending date when generating a recurring output.

2. Gather only trusted official sources.
   - Use official Oracle, AWS, Google Cloud, and Microsoft sources only.
   - Prefer docs and release notes over marketing pages.
   - Browse or otherwise verify sources for each weekly run; do not rely on stale memory for current announcements.
   - Keep a source ledger with title, provider, URL, and observed update/release date when available.

3. Build the story.
   - Cover Oracle Database on Exadata and Autonomous AI Database across OCI, Google Cloud, AWS, and Azure.
   - Separate current-week announcements from watchlist/recent changes.
   - Include architecture ideas that combine Oracle Autonomous AI Database or Exadata with AI offerings such as Gemini Enterprise, Amazon Bedrock, Microsoft Foundry, and OCI Generative AI.
   - Make every architecture claim traceable to official product behavior or documentation.

4. Create the PowerPoint.
   - Use the Presentations skill and artifact-tool PowerPoint workflow.
   - Include authentic provider logo/header assets from official pages where possible; do not draw approximate logos.
   - Use native PowerPoint arrow shapes or robust shape-based connectors. Avoid fragile glyph arrows or detached line fragments.
   - Keep diagrams editable and executive-readable.

5. Add the appendix.
   - Fit the source appendix into one slide when possible.
   - Group sources in this order: OCI, GCP, AWS, Azure.
   - Link each visible topic label directly to its official URL.
   - Do not show raw URLs unless the user explicitly asks.

6. Verify before delivery.
   - Render the deck preview/contact sheet and inspect the appendix at readable size.
   - Confirm the exported PPTX opens as a PowerPoint package.
   - Confirm slide count and hyperlink relationships for appendix source links.
   - Check that arrows/connectors render cleanly.

7. Schedule when requested.
   - Use the Codex app `automation_update` tool for recurring automations.
   - Prefer updating an existing matching automation over creating a duplicate.
   - For the weekly email request, schedule Monday 9:00 AM Australia/Melbourne and email the PPTX to `sujoy.nath@oracle.com`.
   - Use the workspace mail connector script when present: `tools/send_weekly_brief_email.py --mode outlook --timeout-seconds 180 --to sujoy.nath@oracle.com --subject "<subject>" --body "<body>" --attachment "<pptx>"`.
   - Treat email delivery as successful only when the mail connector exits with code 0 and reports `"sent": true` for Outlook mode. If it fails, times out, or does not report sent, preserve the failure log and do not say the email was sent.
   - For a manual resend, use the same connector against the latest verified PPTX or the user-specified attachment, then report the recipient, subject, and attachment path.
   - Put task requirements in the automation prompt, not in raw RRULE text shown to the user.

## Official Source Starting Points

Use these as starting points, then verify current links and dates during the run:

- Oracle/OCI: OCI release notes, Oracle Database@AWS, Oracle Database@Google Cloud, Oracle AI Database@Azure, Oracle AI Vector Search, Oracle Redwood.
- AWS: AWS Oracle Database@AWS User Guide and document history, Amazon Bedrock User Guide.
- GCP: Google Cloud Oracle Database documentation and release notes, Gemini Enterprise documentation.
- Azure: Oracle AI Database@Azure documentation and regional availability, Microsoft Foundry documentation.

## Output Standard

The final deck should feel like an Oracle executive brief, not a generic cloud news digest. It should have a clear weekly signal, provider-by-provider evidence, architecture implications, and a source appendix that makes every cited topic clickable.
