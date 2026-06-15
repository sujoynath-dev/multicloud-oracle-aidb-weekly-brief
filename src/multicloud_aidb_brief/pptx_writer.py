from __future__ import annotations

import mimetypes
import posixpath
import zipfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal
from xml.sax.saxutils import escape


EMU_PER_UNIT = 9525
SLIDE_W = 1280
SLIDE_H = 720
SLIDE_CX = SLIDE_W * EMU_PER_UNIT
SLIDE_CY = SLIDE_H * EMU_PER_UNIT

REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
OFFICE_REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def emu(value: float) -> int:
    return int(round(value * EMU_PER_UNIT))


def clean_color(value: str | None) -> str:
    if not value:
        return "000000"
    return value.strip().lstrip("#").upper()


def xml_text(value: object) -> str:
    return escape(str(value), {'"': "&quot;"})


def font_size(size: float) -> int:
    return int(round(size * 100))


@dataclass
class Relationship:
    rel_id: str
    rel_type: str
    target: str
    target_mode: str | None = None


@dataclass
class Media:
    source: Path
    package_path: str


@dataclass
class Slide:
    index: int
    elements: list[str] = field(default_factory=list)
    relationships: list[Relationship] = field(default_factory=list)
    _shape_id: int = 2
    _rel_id: int = 2

    def __post_init__(self) -> None:
        self.relationships.append(
            Relationship(
                rel_id="rId1",
                rel_type=f"{OFFICE_REL_NS}/slideLayout",
                target="../slideLayouts/slideLayout1.xml",
            )
        )

    def next_shape_id(self) -> int:
        value = self._shape_id
        self._shape_id += 1
        return value

    def next_rel_id(self) -> str:
        value = f"rId{self._rel_id}"
        self._rel_id += 1
        return value

    def add_shape(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        *,
        fill: str | None = None,
        line: str | None = None,
        line_width: float = 0.75,
        geometry: str = "rect",
    ) -> None:
        shape_id = self.next_shape_id()
        fill_xml = (
            f'<a:solidFill><a:srgbClr val="{clean_color(fill)}"/></a:solidFill>'
            if fill
            else "<a:noFill/>"
        )
        if line:
            line_xml = (
                f'<a:ln w="{emu(line_width)}"><a:solidFill><a:srgbClr val="{clean_color(line)}"/>'
                "</a:solidFill></a:ln>"
            )
        else:
            line_xml = '<a:ln><a:noFill/></a:ln>'
        self.elements.append(
            f"""
            <p:sp>
              <p:nvSpPr>
                <p:cNvPr id="{shape_id}" name="Shape {shape_id}"/>
                <p:cNvSpPr/>
                <p:nvPr/>
              </p:nvSpPr>
              <p:spPr>
                <a:xfrm>
                  <a:off x="{emu(x)}" y="{emu(y)}"/>
                  <a:ext cx="{emu(w)}" cy="{emu(h)}"/>
                </a:xfrm>
                <a:prstGeom prst="{xml_text(geometry)}"><a:avLst/></a:prstGeom>
                {fill_xml}
                {line_xml}
              </p:spPr>
            </p:sp>
            """
        )

    def add_text(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        text: str,
        *,
        font_size_pt: float = 14,
        color: str = "#161513",
        bold: bool = False,
        align: Literal["l", "ctr", "r"] = "l",
        font_face: str = "Arial",
        hyperlink: str | None = None,
    ) -> None:
        shape_id = self.next_shape_id()
        rel_xml = ""
        if hyperlink:
            rel_id = self.next_rel_id()
            self.relationships.append(
                Relationship(
                    rel_id=rel_id,
                    rel_type=f"{OFFICE_REL_NS}/hyperlink",
                    target=hyperlink,
                    target_mode="External",
                )
            )
            rel_xml = f'<a:hlinkClick r:id="{rel_id}"/>'
        run_bold = ' b="1"' if bold else ""
        paragraphs = []
        for line in str(text).splitlines() or [""]:
            paragraphs.append(
                f"""
                <a:p>
                  <a:pPr algn="{align}"/>
                  <a:r>
                    <a:rPr lang="en-US" sz="{font_size(font_size_pt)}"{run_bold}>
                      <a:solidFill><a:srgbClr val="{clean_color(color)}"/></a:solidFill>
                      <a:latin typeface="{xml_text(font_face)}"/>
                      {rel_xml}
                    </a:rPr>
                    <a:t>{xml_text(line)}</a:t>
                  </a:r>
                  <a:endParaRPr lang="en-US" sz="{font_size(font_size_pt)}"/>
                </a:p>
                """
            )
        self.elements.append(
            f"""
            <p:sp>
              <p:nvSpPr>
                <p:cNvPr id="{shape_id}" name="Text {shape_id}"/>
                <p:cNvSpPr txBox="1"/>
                <p:nvPr/>
              </p:nvSpPr>
              <p:spPr>
                <a:xfrm>
                  <a:off x="{emu(x)}" y="{emu(y)}"/>
                  <a:ext cx="{emu(w)}" cy="{emu(h)}"/>
                </a:xfrm>
                <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
                <a:noFill/>
                <a:ln><a:noFill/></a:ln>
              </p:spPr>
              <p:txBody>
                <a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0"/>
                <a:lstStyle/>
                {''.join(paragraphs)}
              </p:txBody>
            </p:sp>
            """
        )

    def add_image(
        self,
        image_path: Path,
        package_path: str,
        x: float,
        y: float,
        w: float,
        h: float,
        *,
        alt: str = "Image",
    ) -> None:
        shape_id = self.next_shape_id()
        rel_id = self.next_rel_id()
        target = posixpath.relpath(package_path, start="ppt/slides")
        self.relationships.append(
            Relationship(
                rel_id=rel_id,
                rel_type=f"{OFFICE_REL_NS}/image",
                target=target,
            )
        )
        self.elements.append(
            f"""
            <p:pic>
              <p:nvPicPr>
                <p:cNvPr id="{shape_id}" name="{xml_text(alt)}"/>
                <p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr>
                <p:nvPr/>
              </p:nvPicPr>
              <p:blipFill>
                <a:blip r:embed="{rel_id}"/>
                <a:stretch><a:fillRect/></a:stretch>
              </p:blipFill>
              <p:spPr>
                <a:xfrm>
                  <a:off x="{emu(x)}" y="{emu(y)}"/>
                  <a:ext cx="{emu(w)}" cy="{emu(h)}"/>
                </a:xfrm>
                <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
              </p:spPr>
            </p:pic>
            """
        )

    def xml(self) -> str:
        return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
       xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
       xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr>
        <p:cNvPr id="1" name=""/>
        <p:cNvGrpSpPr/>
        <p:nvPr/>
      </p:nvGrpSpPr>
      <p:grpSpPr>
        <a:xfrm>
          <a:off x="0" y="0"/>
          <a:ext cx="0" cy="0"/>
          <a:chOff x="0" y="0"/>
          <a:chExt cx="0" cy="0"/>
        </a:xfrm>
      </p:grpSpPr>
      {''.join(self.elements)}
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sld>
"""

    def rels_xml(self) -> str:
        rels = []
        for rel in self.relationships:
            mode = f' TargetMode="{rel.target_mode}"' if rel.target_mode else ""
            rels.append(
                f'<Relationship Id="{rel.rel_id}" Type="{rel.rel_type}" Target="{xml_text(rel.target)}"{mode}/>'
            )
        return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="{REL_NS}">
  {''.join(rels)}
</Relationships>
"""


class PptxDeck:
    def __init__(self) -> None:
        self.slides: list[Slide] = []
        self.media: list[Media] = []
        self._media_by_source: dict[Path, str] = {}

    def add_slide(self) -> Slide:
        slide = Slide(index=len(self.slides) + 1)
        self.slides.append(slide)
        return slide

    def add_media(self, image_path: Path) -> str:
        source = image_path.resolve()
        if source in self._media_by_source:
            return self._media_by_source[source]
        suffix = source.suffix.lower() or ".png"
        package_path = f"ppt/media/image{len(self.media) + 1}{suffix}"
        self.media.append(Media(source=source, package_path=package_path))
        self._media_by_source[source] = package_path
        return package_path

    def save(self, output: Path) -> None:
        output.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as zf:
            self._write_static_parts(zf)
            for slide in self.slides:
                zf.writestr(f"ppt/slides/slide{slide.index}.xml", slide.xml())
                zf.writestr(f"ppt/slides/_rels/slide{slide.index}.xml.rels", slide.rels_xml())
            for media in self.media:
                zf.write(media.source, media.package_path)

    def _write_static_parts(self, zf: zipfile.ZipFile) -> None:
        zf.writestr("[Content_Types].xml", self._content_types())
        zf.writestr("_rels/.rels", ROOT_RELS)
        zf.writestr("docProps/core.xml", core_props())
        zf.writestr("docProps/app.xml", app_props(len(self.slides)))
        zf.writestr("ppt/presentation.xml", presentation_xml(len(self.slides)))
        zf.writestr("ppt/_rels/presentation.xml.rels", presentation_rels_xml(len(self.slides)))
        zf.writestr("ppt/slideMasters/slideMaster1.xml", SLIDE_MASTER)
        zf.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", SLIDE_MASTER_RELS)
        zf.writestr("ppt/slideLayouts/slideLayout1.xml", SLIDE_LAYOUT)
        zf.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels", SLIDE_LAYOUT_RELS)
        zf.writestr("ppt/theme/theme1.xml", THEME_XML)

    def _content_types(self) -> str:
        defaults = [
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
            '<Default Extension="xml" ContentType="application/xml"/>',
        ]
        for media in self.media:
            suffix = media.source.suffix.lower().lstrip(".") or "png"
            content_type = mimetypes.types_map.get(f".{suffix}", "image/png")
            default = f'<Default Extension="{suffix}" ContentType="{content_type}"/>'
            if default not in defaults:
                defaults.append(default)
        overrides = [
            '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>',
            '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>',
            '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>',
            '<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>',
            '<Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>',
            '<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>',
        ]
        for slide in self.slides:
            overrides.append(
                f'<Override PartName="/ppt/slides/slide{slide.index}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
            )
        return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  {''.join(defaults)}
  {''.join(overrides)}
</Types>
"""


def core_props() -> str:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
                   xmlns:dc="http://purl.org/dc/elements/1.1/"
                   xmlns:dcterms="http://purl.org/dc/terms/"
                   xmlns:dcmitype="http://purl.org/dc/dcmitype/"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>Weekly Multicloud Announcements and Innovations</dc:title>
  <dc:creator>multicloud-aidb-brief CLI</dc:creator>
  <cp:lastModifiedBy>multicloud-aidb-brief CLI</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>
"""


def app_props(slide_count: int) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
            xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>multicloud-aidb-brief</Application>
  <PresentationFormat>Widescreen</PresentationFormat>
  <Slides>{slide_count}</Slides>
</Properties>
"""


def presentation_xml(slide_count: int) -> str:
    slide_ids = []
    for i in range(1, slide_count + 1):
        slide_ids.append(f'<p:sldId id="{255 + i}" r:id="rId{i + 1}"/>')
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
                xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
                xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:sldMasterIdLst>
    <p:sldMasterId id="2147483648" r:id="rId1"/>
  </p:sldMasterIdLst>
  <p:sldIdLst>
    {''.join(slide_ids)}
  </p:sldIdLst>
  <p:sldSz cx="{SLIDE_CX}" cy="{SLIDE_CY}" type="wide"/>
  <p:notesSz cx="6858000" cy="9144000"/>
  <p:defaultTextStyle>
    <a:defPPr><a:defRPr lang="en-US"/></a:defPPr>
  </p:defaultTextStyle>
</p:presentation>
"""


def presentation_rels_xml(slide_count: int) -> str:
    rels = [
        f'<Relationship Id="rId1" Type="{OFFICE_REL_NS}/slideMaster" Target="slideMasters/slideMaster1.xml"/>'
    ]
    for i in range(1, slide_count + 1):
        rels.append(
            f'<Relationship Id="rId{i + 1}" Type="{OFFICE_REL_NS}/slide" Target="slides/slide{i}.xml"/>'
        )
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="{REL_NS}">
  {''.join(rels)}
</Relationships>
"""


ROOT_RELS = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="{REL_NS}">
  <Relationship Id="rId1" Type="{OFFICE_REL_NS}/officeDocument" Target="ppt/presentation.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="{OFFICE_REL_NS}/extended-properties" Target="docProps/app.xml"/>
</Relationships>
"""


SLIDE_MASTER = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
             xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
             xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
    </p:spTree>
  </p:cSld>
  <p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
  <p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst>
  <p:txStyles>
    <p:titleStyle><a:lvl1pPr><a:defRPr sz="4400"/></a:lvl1pPr></p:titleStyle>
    <p:bodyStyle><a:lvl1pPr><a:defRPr sz="2400"/></a:lvl1pPr></p:bodyStyle>
    <p:otherStyle><a:lvl1pPr><a:defRPr sz="1800"/></a:lvl1pPr></p:otherStyle>
  </p:txStyles>
</p:sldMaster>
"""


SLIDE_MASTER_RELS = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="{REL_NS}">
  <Relationship Id="rId1" Type="{OFFICE_REL_NS}/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
  <Relationship Id="rId2" Type="{OFFICE_REL_NS}/theme" Target="../theme/theme1.xml"/>
</Relationships>
"""


SLIDE_LAYOUT = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
             xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
             xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
             type="blank" preserve="1">
  <p:cSld name="Blank">
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sldLayout>
"""


SLIDE_LAYOUT_RELS = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="{REL_NS}">
  <Relationship Id="rId1" Type="{OFFICE_REL_NS}/slideMaster" Target="../slideMasters/slideMaster1.xml"/>
</Relationships>
"""


THEME_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Oracle Redwood Portable">
  <a:themeElements>
    <a:clrScheme name="Redwood">
      <a:dk1><a:srgbClr val="161513"/></a:dk1>
      <a:lt1><a:srgbClr val="FBF9F8"/></a:lt1>
      <a:dk2><a:srgbClr val="312D2A"/></a:dk2>
      <a:lt2><a:srgbClr val="EFE9E2"/></a:lt2>
      <a:accent1><a:srgbClr val="C74634"/></a:accent1>
      <a:accent2><a:srgbClr val="4E7C78"/></a:accent2>
      <a:accent3><a:srgbClr val="0078D4"/></a:accent3>
      <a:accent4><a:srgbClr val="4285F4"/></a:accent4>
      <a:accent5><a:srgbClr val="FF9900"/></a:accent5>
      <a:accent6><a:srgbClr val="6F7F63"/></a:accent6>
      <a:hlink><a:srgbClr val="8F3328"/></a:hlink>
      <a:folHlink><a:srgbClr val="315F5B"/></a:folHlink>
    </a:clrScheme>
    <a:fontScheme name="Arial">
      <a:majorFont><a:latin typeface="Arial"/></a:majorFont>
      <a:minorFont><a:latin typeface="Arial"/></a:minorFont>
    </a:fontScheme>
    <a:fmtScheme name="Redwood">
      <a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst>
      <a:lnStyleLst><a:ln w="9525"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst>
      <a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst>
      <a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst>
    </a:fmtScheme>
  </a:themeElements>
  <a:objectDefaults/>
  <a:extraClrSchemeLst/>
</a:theme>
"""
