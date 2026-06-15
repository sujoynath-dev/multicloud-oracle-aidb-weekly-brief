from __future__ import annotations

import json
import shutil
from dataclasses import asdict
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from .brief_data import DEFAULT_TIMEZONE, SOURCE_GROUPS, SOURCE_URLS, TITLE, source_ledger
from .pptx_writer import PptxDeck, Slide


C = {
    "paper": "#fbf9f8",
    "warm": "#efebe6",
    "warm2": "#f6f2ee",
    "ink": "#161513",
    "charcoal": "#312d2a",
    "muted": "#6f625b",
    "line": "#d7d0c8",
    "red": "#c74634",
    "redDark": "#8f3328",
    "teal": "#4e7c78",
    "tealDark": "#315f5b",
    "blue": "#d8eaf0",
    "azure": "#0078d4",
    "aws": "#ff9900",
    "google": "#4285f4",
    "green": "#6f7f63",
    "amber": "#f3b15b",
    "white": "#ffffff",
}


WORKSPACE = Path("outputs/manual-20260612-redwood-ppt/presentations/multicloud-announcements")


def today_in_timezone(timezone_name: str = DEFAULT_TIMEZONE) -> date:
    return datetime.now(ZoneInfo(timezone_name)).date()


def parse_date(value: str | None, timezone_name: str = DEFAULT_TIMEZONE) -> date:
    if value:
        return date.fromisoformat(value)
    return today_in_timezone(timezone_name)


def coverage_label(week_ending: date) -> str:
    start = week_ending - timedelta(days=6)
    if start.month == week_ending.month:
        return f"{start.day}-{week_ending.day} {week_ending:%b}"
    return f"{start.day} {start:%b}-{week_ending.day} {week_ending:%b}"


def output_name(week_ending: date) -> str:
    return f"weekly-multicloud-announcements-and-innovations-{week_ending.isoformat()}-redwood.pptx"


def find_repo_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "README.md").exists() and (candidate / "outputs").exists():
            return candidate
    return current


def setup(slide: Slide, *, page: int | None = None, source: str = "Official sources only", no_footer: bool = False) -> None:
    slide.add_shape(0, 0, 1280, 720, fill=C["paper"])
    slide.add_shape(0, 0, 1280, 6, fill="#4b4540")
    if not no_footer:
        footer(slide, source, page)


def footer(slide: Slide, source: str, page: int | None) -> None:
    slide.add_shape(64, 674, 1040, 1, fill=C["line"])
    slide.add_text(64, 686, 820, 16, source, font_size_pt=10, color=C["muted"])
    slide.add_text(1140, 686, 76, 16, f"{page:02d}" if page else "", font_size_pt=10, color=C["muted"], align="r")


def kicker(slide: Slide, text: str, y: float = 52) -> None:
    slide.add_shape(64, y + 2, 8, 8, fill=C["redDark"])
    slide.add_text(82, y, 520, 16, text.upper(), font_size_pt=11, color=C["muted"], bold=True)


def claim(slide: Slide, text: str, y: float = 82, w: float = 950) -> None:
    slide.add_text(64, y, w, 104, text, font_size_pt=32, color=C["ink"], bold=True)


def subline(slide: Slide, text: str, x: float, y: float, w: float, color: str = C["muted"]) -> None:
    slide.add_text(x, y, w, 44, text, font_size_pt=17, color=color)


def panel(slide: Slide, x: float, y: float, w: float, h: float, *, fill: str = C["warm2"], line: str = C["line"]) -> None:
    slide.add_shape(x, y, w, h, fill=fill, line=line)


def pill(slide: Slide, x: float, y: float, text: str, *, w: float | None = None, fill: str = C["warm"], color: str = C["charcoal"]) -> None:
    width = w or max(72, len(text) * 7.5 + 24)
    panel(slide, x, y, width, 24, fill=fill)
    slide.add_text(x + 10, y + 5, width - 20, 14, text, font_size_pt=10, color=color, bold=True, align="ctr")


def bullet(slide: Slide, x: float, y: float, text: str, *, w: float = 480, dot: str = C["red"], size: float = 15) -> None:
    slide.add_shape(x, y + 7, 5, 5, fill=dot, geometry="ellipse")
    slide.add_text(x + 16, y, w, 54, text, font_size_pt=size, color=C["charcoal"])


def metric(slide: Slide, x: float, y: float, value: str, label: str, *, w: float = 180, color: str = C["redDark"]) -> None:
    panel(slide, x, y, w, 96, fill=C["white"])
    slide.add_text(x + 18, y + 14, w - 36, 30, value, font_size_pt=27, color=color, bold=True)
    slide.add_text(x + 18, y + 50, w - 36, 34, label, font_size_pt=12, color=C["muted"])


def node(
    slide: Slide,
    x: float,
    y: float,
    w: float,
    h: float,
    title: str,
    body: str,
    *,
    fill: str = C["white"],
    bar: str | None = None,
    title_size: float = 15,
    body_size: float = 12,
    title_color: str = C["ink"],
    body_color: str = C["muted"],
) -> None:
    panel(slide, x, y, w, h, fill=fill)
    if bar:
        slide.add_shape(x, y, w, 5, fill=bar)
    slide.add_text(x + 14, y + 14, w - 28, 32, title, font_size_pt=title_size, color=title_color, bold=True)
    if body:
        slide.add_text(x + 14, y + 48, w - 28, max(12, h - 64), body, font_size_pt=body_size, color=body_color)


def arrow(slide: Slide, x1: float, y1: float, x2: float, y2: float, *, color: str = C["muted"], width: float = 2) -> None:
    horizontal = abs(x2 - x1) >= abs(y2 - y1)
    if horizontal:
        left = min(x1, x2)
        shape_w = max(24, abs(x2 - x1))
        slide.add_shape(
            left,
            y1 - max(4, width * 2),
            shape_w,
            max(10, width * 5),
            fill=color,
            geometry="rightArrow" if x2 >= x1 else "leftArrow",
        )
    else:
        top = min(y1, y2)
        shape_h = max(24, abs(y2 - y1))
        slide.add_shape(
            x1 - max(4, width * 2),
            top,
            max(10, width * 5),
            shape_h,
            fill=color,
            geometry="downArrow" if y2 >= y1 else "upArrow",
        )


def logo_strip(deck: PptxDeck, slide: Slide, asset_dir: Path, x: float = 64, y: float = 360) -> None:
    logos = [
        ("oracle-wordmark-official.png", "Oracle"),
        ("google-cloud-official.png", "Google Cloud"),
        ("aws-official.png", "AWS"),
        ("azure-official.png", "Microsoft Azure"),
    ]
    cell_w = 184
    gap = 14
    for index, (file_name, label) in enumerate(logos):
        cell_x = x + index * (cell_w + gap)
        panel(slide, cell_x, y, cell_w, 74, fill=C["white"])
        logo_path = asset_dir / file_name
        if logo_path.exists():
            package_path = deck.add_media(logo_path)
            slide.add_image(logo_path, package_path, cell_x + 18, y + 20, cell_w - 36, 34, alt=label)
        else:
            slide.add_text(cell_x + 18, y + 27, cell_w - 36, 18, label, font_size_pt=13, color=C["charcoal"], bold=True, align="ctr")


def add_source_group(slide: Slide, x: float, y: float, title: str, accent: str, topics: list[str]) -> None:
    panel(slide, x, y, 535, 178, fill=C["white"])
    slide.add_shape(x, y, 535, 5, fill=accent)
    slide.add_text(x + 18, y + 18, 120, 28, title, font_size_pt=18, color=C["ink"], bold=True)
    slide.add_text(x + 142, y + 22, 340, 18, "Click topic names to open official sources", font_size_pt=10, color=C["muted"])
    for index, topic in enumerate(topics):
        yy = y + 60 + index * 23
        slide.add_shape(x + 20, yy + 6, 4, 4, fill=accent, geometry="ellipse")
        slide.add_text(
            x + 34,
            yy,
            470,
            18,
            topic,
            font_size_pt=10.8,
            color=C["redDark"],
            bold=True,
            hyperlink=SOURCE_URLS[topic],
        )


def build_deck(repo_root: Path, week_ending: date, output: Path, *, sync_workspace: bool = False) -> dict[str, object]:
    workspace = repo_root / WORKSPACE
    asset_dir = workspace / "assets"
    deck = PptxDeck()
    coverage = coverage_label(week_ending)

    slide = deck.add_slide()
    setup(slide, no_footer=True)
    kicker(slide, "Official-source weekly brief", 54)
    claim(slide, TITLE, 92, 760)
    subline(
        slide,
        "Oracle Database on Exadata and Autonomous AI Database across Oracle Cloud, AWS, Google Cloud, and Azure",
        64,
        250,
        720,
    )
    logo_strip(deck, slide, asset_dir, 64, 336)
    metric(slide, 920, 92, coverage, "coverage window, Australia/Melbourne", w=230, color=C["charcoal"])
    metric(slide, 920, 210, "AWS", "strongest weekly signal: ADB-S in Oracle Database@AWS", w=230)
    bullet(slide, 920, 352, "OCI had adjacent data and AI platform updates: GoldenGate Veridata and Generative AI model import.", w=245)
    bullet(slide, 920, 450, "Google Cloud and Azure had no new dated Oracle Database items inside the week.", w=245, dot=C["teal"])
    bullet(slide, 920, 548, "Deck theme follows the official Redwood reference page supplied by the user.", w=245, dot=C["amber"])

    slide = deck.add_slide()
    setup(slide, page=2, source="AWS doc history; Google release notes; Oracle Azure docs; OCI release notes")
    kicker(slide, "Weekly signal")
    claim(slide, "The weekly signal is narrow, but the AWS change is strategically important.", 82, 920)
    rows = [
        ("AWS", "10 Jun 2026", "Oracle Database@AWS supports Autonomous Database Serverless.", "High", C["red"]),
        ("OCI", "9-10 Jun 2026", "OCI GoldenGate adds Veridata; OCI Generative AI adds Whisper model import.", "Adjacent", C["amber"]),
        ("Google Cloud", coverage, "No new dated Oracle Database@Google Cloud item found; latest release note remains 27 May.", "Watch", C["teal"]),
        ("Azure", coverage, "No new official Oracle Database@Azure item found; availability page still shows 33 live regions.", "Steady", C["blue"]),
    ]
    x = 72
    y = 220
    widths = [150, 145, 610, 145]
    offset = 0
    for index, header in enumerate(["Provider", "Date", "Official update", "Signal"]):
        node(slide, x + offset, y, widths[index], 48, header, "", fill=C["warm"], title_size=13)
        offset += widths[index]
    for idx, row in enumerate(rows):
        yy = y + 54 + idx * 78
        node(slide, x, yy, widths[0], 68, row[0], "", bar=row[4], title_size=15)
        node(slide, x + widths[0], yy, widths[1], 68, row[1], "", title_size=14)
        node(slide, x + widths[0] + widths[1], yy, widths[2], 68, row[2], "", title_size=13.5)
        pill(slide, x + widths[0] + widths[1] + widths[2] + 24, yy + 22, row[3], w=86, fill="#f6ded8" if idx == 0 else C["warm2"], color=C["redDark"] if idx == 0 else C["charcoal"])

    slide = deck.add_slide()
    setup(slide, page=3, source="AWS Oracle Database@AWS document history and overview")
    kicker(slide, "AWS update")
    claim(slide, "Autonomous Database Serverless lowers the entry path for Oracle data on AWS.", 82, 950)
    node(slide, 78, 238, 260, 120, "Before", "Most serious Oracle Database@AWS designs centered on dedicated Exadata infrastructure and VM cluster planning.", fill=C["warm2"])
    arrow(slide, 356, 298, 454, 298, color=C["red"])
    node(slide, 470, 218, 318, 160, "Now", "AWS documentation says Oracle Database@AWS supports Autonomous Database Serverless with create and manage flows and a public AWS Marketplace offer.", bar=C["red"], title_size=18)
    arrow(slide, 804, 298, 902, 298, color=C["red"])
    node(slide, 918, 238, 260, 120, "Impact", "Elastic AI and app workloads can start without provisioning Exadata infrastructure or VM clusters.", fill="#fff7f2")
    metric(slide, 98, 452, "ADB-S", "serverless Autonomous Database path", w=210)
    metric(slide, 340, 452, "Bedrock", "agent and generative AI adjacency", w=210, color=C["charcoal"])
    metric(slide, 582, 452, "Redshift", "zero-ETL analytics watch pattern", w=210, color=C["tealDark"])
    metric(slide, 824, 452, "S3", "backup and data integration surface", w=210, color=C["aws"])
    bullet(slide, 98, 584, "Best pilot lane: AI-enabled apps that need Oracle transactional integrity with AWS-native model and analytics services.", w=930)

    slide = deck.add_slide()
    setup(slide, page=4, source="Google Cloud Oracle Database@Google Cloud release notes")
    kicker(slide, "Google Cloud watchlist")
    claim(slide, "Google Cloud shows a recent expansion pattern, not a current-week spike.", 82, 940)
    timeline = [
        ("20 Apr", "Database Center integration GA", "Fleet insights, alerts, and recommendations for Exadata and Autonomous Database."),
        ("19 May", "Autonomous Data Guard local peers GA", "Improves local continuity for Autonomous Database in Google Cloud."),
        ("20 May", "OCI GoldenGate support GA", "Strengthens migration, replication, and data-product feeds."),
        ("27 May", "Melbourne and Milan zones", "Adds placement options for Exascale, Base Database, and GoldenGate."),
        (f"{week_ending.day} {week_ending:%b}", "Release notes checked", f"No new dated Oracle Database enhancement inside {coverage}."),
    ]
    slide.add_shape(118, 275, 986, 2, fill=C["line"])
    for index, item in enumerate(timeline):
        item_x = 118 + index * 246
        is_check = index == 4
        slide.add_shape(item_x - 9, 266, 20, 20, fill=C["warm"] if is_check else C["teal"], geometry="ellipse")
        pill(slide, item_x - 35, 214, item[0], w=70, fill=C["warm2"] if is_check else "#e4efed")
        node(slide, item_x - 88, 322, 176, 158, item[1], item[2], fill=C["warm2"] if is_check else C["white"], bar=C["line"] if is_check else C["teal"], title_size=13.2, body_size=11)

    slide = deck.add_slide()
    setup(slide, page=5, source="Oracle AI Database@Azure docs; Microsoft Foundry docs")
    kicker(slide, "Azure platform stance")
    claim(slide, "Azure remains a broad landing zone for Oracle AI Database plus Microsoft Foundry.", 82, 970)
    node(slide, 72, 230, 210, 128, "Azure apps", "AKS, App Service, Functions, VM workloads, and enterprise network controls.", bar=C["azure"])
    arrow(slide, 292, 292, 370, 292, color=C["azure"])
    node(slide, 386, 218, 250, 152, "Delegated subnet", "Oracle docs describe Azure VNet plus delegated subnet for direct, secure, low-latency connectivity.", fill=C["warm2"], bar=C["line"])
    arrow(slide, 648, 292, 726, 292, color=C["azure"])
    node(slide, 742, 218, 250, 152, "Oracle AI Database@Azure", "Exadata Database Service and Autonomous AI Database provisioned from the Azure console.", fill="#eef5f5", bar=C["teal"])
    arrow(slide, 870, 380, 870, 452)
    node(slide, 704, 468, 334, 112, "Microsoft Foundry", "Agents, model routing, evaluations, monitoring, policies, and enterprise AI operations.", bar=C["azure"])
    metric(slide, 1060, 230, "33", "live Oracle AI Database@Azure regions in official availability page", w=150, color=C["azure"])

    slide = deck.add_slide()
    setup(slide, page=6, source="Oracle Database@AWS, @Google Cloud, @Azure official docs")
    kicker(slide, "Placement model")
    claim(slide, "The architecture choice is increasingly data-plane plus AI-control-plane placement.", 82, 980)
    lanes = [
        ("AWS", C["aws"], "EC2/EKS/Lambda", "Oracle Database@AWS", "Bedrock, Redshift, S3, EventBridge"),
        ("Google Cloud", C["google"], "Cloud Run/GKE/Compute", "Oracle Database@Google Cloud", "Gemini Enterprise, GoldenGate, Database Center"),
        ("Azure", C["azure"], "AKS/App Service/Functions", "Oracle AI Database@Azure", "Microsoft Foundry, policy, identity"),
    ]
    for index, lane in enumerate(lanes):
        lane_y = 222 + index * 118
        pill(slide, 72, lane_y + 37, lane[0], w=120, fill=C["white"])
        node(slide, 220, lane_y, 220, 90, "Application tier", lane[2], bar=lane[1])
        arrow(slide, 448, lane_y + 45, 516, lane_y + 45)
        node(slide, 532, lane_y, 244, 90, "Oracle data plane", lane[3], fill="#eef5f5", bar=C["teal"])
        arrow(slide, 784, lane_y + 45, 852, lane_y + 45)
        node(slide, 868, lane_y, 300, 90, "AI and analytics plane", lane[4], fill=C["warm2"], bar=lane[1])

    slide = deck.add_slide()
    setup(slide, page=7, source="Oracle AI Vector Search; Bedrock; Gemini Enterprise; Microsoft Foundry docs")
    kicker(slide, "Governed RAG")
    claim(slide, "Autonomous AI Database can anchor RAG while hyperscaler AI handles reasoning and workflow.", 82, 980)
    node(slide, 82, 228, 220, 120, "Oracle operational data", "Transactions, documents, metadata, policies, lineage, and entitlements stay governed in Oracle.", bar=C["teal"])
    arrow(slide, 312, 288, 384, 288, color=C["teal"])
    node(slide, 400, 228, 220, 120, "AI Vector Search", "Embeddings stored beside business data; semantic search runs close to the governed records.", fill="#eef5f5", bar=C["teal"])
    arrow(slide, 630, 288, 702, 288)
    node(slide, 718, 228, 220, 120, "Model platform", "Bedrock, Gemini Enterprise, Microsoft Foundry, or OCI Generative AI selected by use case.", fill=C["warm2"], bar=C["red"])
    arrow(slide, 948, 288, 1020, 288)
    node(slide, 1036, 228, 160, 120, "Agent action", "Answer, summarize, route, write back, or escalate with controls.", bar=C["amber"])
    bullet(slide, 112, 420, "Use Oracle as the governed retrieval and data-quality boundary.", w=470, dot=C["teal"])
    bullet(slide, 112, 482, "Expose only approved views, APIs, summaries, or vector search results to the model layer.", w=470)
    bullet(slide, 664, 420, "Choose the AI platform by domain fit, model governance, latency, cost, and enterprise channel.", w=470, dot=C["amber"])
    bullet(slide, 664, 502, "Log prompts, retrieval context, output, and user action for auditability.", w=470, dot=C["blue"])

    slide = deck.add_slide()
    setup(slide, page=8, source="Architecture ideas synthesized from official service docs")
    kicker(slide, "Architecture moves")
    claim(slide, "Four multicloud moves are ready to evaluate.", 82, 880)
    cards = [
        ("AWS operational AI", "Use Oracle Database@AWS ADB-S or Exadata with Bedrock agents, Redshift analytics, S3 integration, and CloudWatch/EventBridge operations.", C["aws"]),
        ("Gemini enterprise knowledge", "Ground Gemini Enterprise assistants on governed Oracle data, selected replicated views, GoldenGate feeds, and access-controlled search.", C["google"]),
        ("Azure regulated copilot", "Pair Oracle AI Database@Azure with Microsoft Foundry agents, model routing, evaluations, policy, identity, and Teams/M365 channels.", C["azure"]),
        ("Cross-cloud governed fabric", "Keep Oracle as system of record, replicate only selected data products, and route AI work to the best provider by risk and domain.", C["teal"]),
    ]
    for index, card in enumerate(cards):
        card_x = 82 + (index % 2) * 555
        card_y = 230 + (index // 2) * 170
        node(slide, card_x, card_y, 500, 130, card[0], card[1], bar=card[2], title_size=18, body_size=13.2)

    slide = deck.add_slide()
    setup(slide, page=9, source="OCI release notes; AWS KMS/Data Guard release note; provider service docs")
    kicker(slide, "Controls before models")
    claim(slide, "Governance, security, and DR should be designed before model routing.", 82, 980)
    controls = [
        ("Key control", "Validate AWS KMS CMK support for Autonomous AI Database on Oracle Database@AWS cross-region Data Guard.", "Regulated AWS-resident DR"),
        ("Data movement", "Classify whether each dataset stays in Oracle, is replicated, summarized, embedded, or exposed through an API.", "Prevents uncontrolled AI data drift"),
        ("Identity", "Keep Oracle database entitlements authoritative; map provider IAM/RBAC to app and tool access.", "Consistent least privilege"),
        ("Operations", "Use provider observability for cloud-side services and Oracle controls for database health, backups, and patching.", "Clear ownership boundary"),
    ]
    x = 82
    y = 226
    widths = [180, 620, 250]
    offset = 0
    for index, header in enumerate(["Control", "Required design decision", "Why it matters"]):
        node(slide, x + offset, y, widths[index], 48, header, "", fill=C["warm"], title_size=13)
        offset += widths[index]
    for index, row in enumerate(controls):
        yy = y + 56 + index * 78
        node(slide, x, yy, widths[0], 66, row[0], "", bar=C["red"] if index == 0 else C["teal"], title_size=14.5)
        node(slide, x + widths[0], yy, widths[1], 66, row[1], "", title_size=13)
        node(slide, x + widths[0] + widths[1], yy, widths[2], 66, row[2], "", fill=C["warm2"], title_size=13)
    pill(slide, 82, 604, "Design principle: move models to governed context, not governed data to every model.", w=650, fill="#e4efed", color=C["tealDark"])

    slide = deck.add_slide()
    setup(slide, page=10, source="Appendix: grouped clickable official source topics")
    kicker(slide, "Appendix")
    claim(slide, "Official source topics grouped by cloud.", 82, 820)
    for index, group in enumerate(SOURCE_GROUPS):
        col = index % 2
        row = index // 2
        add_source_group(slide, 64 + col * 580, 214 + row * 200, group[0], group[1], group[2])

    deck.save(output)
    manifest = {
        "title": TITLE,
        "weekEnding": week_ending.isoformat(),
        "coverageWindow": coverage,
        "output": str(output),
        "slideCount": len(deck.slides),
        "sourceCount": len(source_ledger()),
        "sources": [asdict(source) for source in source_ledger()],
    }
    manifest_path = output.with_suffix(".manifest.json")
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    if sync_workspace:
        workspace_output = workspace / "output" / output.name
        workspace_output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(output, workspace_output)
    return manifest
