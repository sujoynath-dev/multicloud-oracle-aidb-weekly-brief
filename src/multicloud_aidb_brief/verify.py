from __future__ import annotations

import json
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
HYPERLINK_TYPE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink"


def verify_pptx(path: Path, *, expected_slides: int = 10, min_hyperlinks: int = 15) -> dict[str, object]:
    if not path.exists():
        raise FileNotFoundError(path)
    if path.stat().st_size <= 0:
        raise ValueError(f"File is empty: {path}")

    with zipfile.ZipFile(path, "r") as zf:
        names = set(zf.namelist())
        slide_names = sorted(
            name
            for name in names
            if name.startswith("ppt/slides/slide") and name.endswith(".xml") and "/_rels/" not in name
        )
        if "[Content_Types].xml" not in names or "ppt/presentation.xml" not in names:
            raise ValueError(f"Not a valid PowerPoint package: {path}")
        if len(slide_names) != expected_slides:
            raise ValueError(f"Expected {expected_slides} slides, found {len(slide_names)}")

        hyperlink_count = 0
        external_targets: list[str] = []
        for rel_name in sorted(name for name in names if name.startswith("ppt/slides/_rels/") and name.endswith(".rels")):
            rels = ET.fromstring(zf.read(rel_name))
            for rel in rels.findall(f"{{{REL_NS}}}Relationship"):
                if rel.attrib.get("Type") == HYPERLINK_TYPE:
                    hyperlink_count += 1
                    external_targets.append(rel.attrib.get("Target", ""))
        if hyperlink_count < min_hyperlinks:
            raise ValueError(f"Expected at least {min_hyperlinks} hyperlinks, found {hyperlink_count}")

        appendix_xml = zf.read("ppt/slides/slide10.xml")
        appendix_root = ET.fromstring(appendix_xml)
        linked_runs = appendix_root.findall(f".//{{{A_NS}}}hlinkClick")

    return {
        "path": str(path),
        "bytes": path.stat().st_size,
        "slideCount": len(slide_names),
        "hyperlinkCount": hyperlink_count,
        "appendixLinkedRuns": len(linked_runs),
        "externalTargets": external_targets,
        "ok": True,
    }


def verify_json(path: Path, *, expected_slides: int = 10, min_hyperlinks: int = 15) -> str:
    return json.dumps(verify_pptx(path, expected_slides=expected_slides, min_hyperlinks=min_hyperlinks), indent=2)
