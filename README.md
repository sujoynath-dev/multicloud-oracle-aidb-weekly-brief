# Weekly Multicloud Oracle Database Brief

Reusable source and artifacts for a weekly official-source brief covering Oracle Database multicloud announcements and innovations across OCI, Google Cloud, AWS, and Azure.

The current generated brief is titled **Weekly Multicloud Announcements and Innovations** and focuses on Oracle Database on Exadata and Autonomous AI Database, plus architecture ideas that combine Oracle data platforms with AI services such as Gemini Enterprise, Amazon Bedrock, Microsoft Foundry, and OCI Generative AI.

## Repository Contents

- `weekly-multicloud-announcements-and-innovations-redwood.pptx`  
  Final editable Redwood-themed PowerPoint deck.
- `weekly_multicloud_oracle_db_ai_brief_2026-06-12.pdf`  
  Earlier PDF brief artifact.
- `weekly_multicloud_oracle_db_ai_brief_2026-06-12.html`  
  HTML source for the earlier PDF brief.
- `outputs/manual-20260612-redwood-ppt/presentations/multicloud-announcements/`  
  PowerPoint source workspace with slide modules, design notes, official provider logo assets, rendered previews, and build manifest.
- `tools/send_weekly_brief_email.py`  
  Local Outlook/SMTP mail connector used by the weekly automation.
- `tools/mail_config.example.env`  
  Optional SMTP fallback configuration template.
- `skills/create-multicloud-oracle-aidb-brief/`  
  Reusable Codex skill and detailed prompt for recreating or scheduling the brief workflow.

## Workflow Summary

The workflow is designed to:

1. Research only official Oracle, AWS, Google Cloud, and Microsoft sources.
2. Separate current-week announcements from recent watchlist items.
3. Build an Oracle Redwood-style PowerPoint deck.
4. Include provider logos sourced from official provider pages.
5. Use robust editable PowerPoint shapes for diagrams and arrows.
6. Add a one-slide appendix grouped by OCI, GCP, AWS, and Azure.
7. Link each appendix topic label directly to its official source URL.
8. Send the generated PPTX through the local Outlook connector.

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

The working Outlook connector command pattern is:

```bash
python3 tools/send_weekly_brief_email.py \
  --mode outlook \
  --timeout-seconds 180 \
  --to sujoy.nath@oracle.com \
  --subject "Weekly Multicloud Announcements and Innovations - week ending 2026-06-12" \
  --body "Attached is the weekly Oracle Database multicloud announcements and innovations brief." \
  --attachment weekly-multicloud-announcements-and-innovations-redwood.pptx
```

Delivery should only be considered successful when the script exits with code `0` and returns `"sent": true`.

For non-Outlook environments, configure SMTP variables based on `tools/mail_config.example.env` and run the connector with `--mode smtp`.

## Notes For Forks

- Do not commit real SMTP passwords, app passwords, tokens, or private `.env` files.
- Update source links each week from official pages rather than relying on stale memory.
- Keep generated failure logs out of Git unless they are intentionally redacted and useful for troubleshooting.
- If you change the deck structure, rerender and inspect the contact sheet before publishing.
