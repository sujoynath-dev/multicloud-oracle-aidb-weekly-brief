from __future__ import annotations

from dataclasses import dataclass


TITLE = "Weekly Multicloud Announcements and Innovations"
DEFAULT_TIMEZONE = "Australia/Melbourne"
DEFAULT_RECIPIENT = "sujoy.nath@oracle.com"


@dataclass(frozen=True)
class Source:
    provider: str
    topic: str
    url: str


SOURCE_URLS: dict[str, str] = {
    "Oracle Cloud Infrastructure release notes": "https://docs.oracle.com/en-us/iaas/releasenotes/index.htm",
    "Oracle AI Vector Search overview": "https://docs.oracle.com/en/database/oracle/oracle-database/26/vecse/overview-ai-vector-search.html",
    "Official Design for Oracle Redwood": "https://redwood.oracle.com/?pageId=CORE17B41D21FF4244A3BBB82A4D99AE610C&shell=getting-started",
    "AWS Oracle Database@AWS document history": "https://docs.aws.amazon.com/odb/latest/UserGuide/doc-history.html",
    "AWS Oracle Database@AWS overview": "https://docs.aws.amazon.com/odb/latest/UserGuide/what-is-odb.html",
    "AWS Oracle Database@AWS how it works": "https://docs.aws.amazon.com/odb/latest/UserGuide/how-it-works.html",
    "AWS Amazon Bedrock User Guide": "https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html",
    "Oracle AI Database@AWS": "https://docs.oracle.com/en-us/iaas/Content/database-at-aws/oaaws.htm",
    "Google Cloud Oracle Database release notes": "https://docs.cloud.google.com/oracle/database/docs/release-notes",
    "Google Cloud Oracle Database docs": "https://docs.cloud.google.com/oracle/database/docs",
    "Google Cloud Gemini Enterprise docs": "https://docs.cloud.google.com/gemini/enterprise/docs",
    "Oracle Database@Google Cloud": "https://docs.oracle.com/en-us/iaas/Content/database-at-gcp/home.htm",
    "Oracle AI Database@Azure overview": "https://docs.oracle.com/en-us/iaas/Content/database-at-azure/overview.htm",
    "Oracle AI Database@Azure regional availability": "https://docs.oracle.com/en-us/iaas/Content/database-at-azure/oaa_regions.htm",
    "Microsoft Foundry overview": "https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry",
}


SOURCE_GROUPS: list[tuple[str, str, list[str]]] = [
    (
        "OCI",
        "#c74634",
        [
            "Oracle Cloud Infrastructure release notes",
            "Oracle AI Vector Search overview",
            "Official Design for Oracle Redwood",
        ],
    ),
    (
        "GCP",
        "#4285f4",
        [
            "Google Cloud Oracle Database release notes",
            "Google Cloud Oracle Database docs",
            "Google Cloud Gemini Enterprise docs",
            "Oracle Database@Google Cloud",
        ],
    ),
    (
        "AWS",
        "#ff9900",
        [
            "AWS Oracle Database@AWS document history",
            "AWS Oracle Database@AWS overview",
            "AWS Oracle Database@AWS how it works",
            "AWS Amazon Bedrock User Guide",
            "Oracle AI Database@AWS",
        ],
    ),
    (
        "Azure",
        "#0078d4",
        [
            "Oracle AI Database@Azure overview",
            "Oracle AI Database@Azure regional availability",
            "Microsoft Foundry overview",
        ],
    ),
]


def source_ledger() -> list[Source]:
    rows: list[Source] = []
    for provider, _accent, topics in SOURCE_GROUPS:
        for topic in topics:
            rows.append(Source(provider=provider, topic=topic, url=SOURCE_URLS[topic]))
    return rows
