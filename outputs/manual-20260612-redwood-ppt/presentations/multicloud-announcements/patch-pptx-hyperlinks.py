from __future__ import annotations

import html
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
HYPERLINK_TYPE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink"

ET.register_namespace("p", P_NS)
ET.register_namespace("a", A_NS)
ET.register_namespace("r", R_NS)


URL_RE = re.compile(r"^https?://")
TOPIC_URLS = {
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


def patch_slide(slide_xml: bytes, rels_xml: bytes) -> tuple[bytes, bytes, int]:
    slide_root = ET.fromstring(slide_xml)
    rels_root = ET.fromstring(rels_xml)
    existing_ids = {rel.attrib.get("Id", "") for rel in rels_root}

    def next_id(index: int) -> str:
        while True:
            rel_id = f"rIdSrc{index}"
            if rel_id not in existing_ids:
                existing_ids.add(rel_id)
                return rel_id
            index += 1

    count = 0
    for run in slide_root.findall(f".//{{{A_NS}}}r"):
        text_node = run.find(f"{{{A_NS}}}t")
        if text_node is None or not text_node.text:
            continue
        text = html.unescape(text_node.text.strip())
        url = TOPIC_URLS.get(text)
        if url is None and URL_RE.match(text):
            url = text
        if url is None:
            continue
        rpr = run.find(f"{{{A_NS}}}rPr")
        if rpr is None:
            rpr = ET.Element(f"{{{A_NS}}}rPr")
            run.insert(0, rpr)
        for existing in list(rpr.findall(f"{{{A_NS}}}hlinkClick")):
            rpr.remove(existing)
        rel_id = next_id(count + 1)
        hlink = ET.Element(f"{{{A_NS}}}hlinkClick", {f"{{{R_NS}}}id": rel_id})
        rpr.append(hlink)
        rel = ET.Element(
            f"{{{REL_NS}}}Relationship",
            {
                "Id": rel_id,
                "Type": HYPERLINK_TYPE,
                "Target": url,
                "TargetMode": "External",
            },
        )
        rels_root.append(rel)
        count += 1

    return (
      b'<?xml version="1.0" encoding="utf-8"?>' + ET.tostring(slide_root, encoding="utf-8"),
      b'<?xml version="1.0" encoding="utf-8"?>' + ET.tostring(rels_root, encoding="utf-8"),
      count,
    )


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: patch-pptx-hyperlinks.py input.pptx output.pptx", file=sys.stderr)
        return 2

    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])
    patches: dict[str, bytes] = {}
    total = 0

    with zipfile.ZipFile(src, "r") as zin:
        for slide_no in (10,):
            slide_name = f"ppt/slides/slide{slide_no}.xml"
            rels_name = f"ppt/slides/_rels/slide{slide_no}.xml.rels"
            slide_xml, rels_xml, count = patch_slide(zin.read(slide_name), zin.read(rels_name))
            patches[slide_name] = slide_xml
            patches[rels_name] = rels_xml
            total += count

        with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = patches.get(item.filename, zin.read(item.filename))
                zout.writestr(item, data)

    print(f"Patched {total} hyperlink(s) into {dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
