# Detailed Weekly Brief Prompt

Use this prompt when creating the recurring automation or when the user asks for a reusable detailed prompt.

```text
Create a fresh weekly PowerPoint deck titled "Weekly Multicloud Announcements and Innovations" covering official multicloud announcements and enhancements from Oracle, AWS, Google Cloud, and Microsoft Azure related to Oracle Database on Exadata and Autonomous AI Database.

Use only trusted official hyperscaler or Oracle sources. Prioritize official release notes, product documentation, service user guides, and regional availability documentation. Do not use blogs, news articles, community posts, or third-party analysis unless the user explicitly asks for a non-official watchlist, and never mix unofficial sources into the official brief.

Verify the current week using Australia/Melbourne time. Clearly distinguish current-week announcements from recent watchlist items. For each provider, capture the source title, provider, URL, and update or release date when available.

Follow the official Oracle Redwood visual style: warm near-white background, charcoal typography, quiet enterprise spacing, restrained borders, sparse Oracle red and teal accents, and polished but understated architecture diagrams. Include verified provider logo/header assets for Oracle Cloud, Google Cloud, AWS, and Microsoft Azure where available from official provider pages; do not draw approximate logos.

Create an executive-ready story with:
1. A cover slide with the week range and concise weekly signal.
2. A provider-by-provider announcement matrix for OCI, GCP, AWS, and Azure.
3. Deeper slides for material updates or watchlist items.
4. Architecture design ideas that combine Oracle Autonomous AI Database or Exadata with AI offerings from other hyperscalers, including Gemini Enterprise, Amazon Bedrock, Microsoft Foundry, and OCI Generative AI where relevant.
5. A governance/security/DR slide covering data movement, identity, model routing, auditability, and operational ownership.
6. A one-slide appendix grouped by OCI, GCP, AWS, and Azure.

For the appendix, link each visible source topic label directly to its official source URL. Do not show raw URLs unless space is abundant and the user asks for visible URLs.

Use native PowerPoint arrow shapes or robust shape-based arrows so all connectors render cleanly in PowerPoint. Avoid fragile glyph arrows or detached line fragments.

Render and inspect a contact sheet before delivery. Verify that the exported PPTX has the expected slide count, that the appendix links are present as hyperlink relationships, that provider logos render properly, and that arrows/connectors are not broken.

Save the PPTX in the workspace with the week-ending date in the filename. If this is a scheduled run, send the generated PPTX using the workspace mail connector script:

python3 "/Users/sujoynath/Documents/Multicloud Research/tools/send_weekly_brief_email.py" --mode outlook --timeout-seconds 180 --to sujoy.nath@oracle.com --subject "Weekly Multicloud Announcements and Innovations - week ending <week-ending-date>" --body "Attached is the weekly Oracle Database multicloud announcements and innovations brief." --attachment "<absolute-path-to-generated-pptx>"

Treat email delivery as successful only if the connector exits with code 0 and the Outlook connector output includes `"sent": true`. If it fails, times out, or does not report sent, save the failure output to an `email-send-failure-<date>.log` file in the workspace and do not claim that the email was sent.

For a manual resend, use the same connector command against the latest verified PPTX or the user-specified attachment, then report the recipient, subject, and attachment path after the connector returns `"sent": true`.
```
