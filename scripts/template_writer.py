#!/usr/bin/env python3
"""Insert structured thesis content while inheriting styles from a DOCX template.

The writer never creates or rewrites styles. Every requested style must already
exist in the input template. This makes the user's Word file the formatting
authority.
"""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.text.paragraph import Paragraph
from docx.shared import Inches

from omml import latex_to_omml


def insert_after(paragraph: Paragraph, style_name: str | None = None) -> Paragraph:
    element = OxmlElement("w:p")
    paragraph._p.addnext(element)
    inserted = Paragraph(element, paragraph._parent)
    if style_name:
        inserted.style = style_name
    return inserted


def find_anchor(document: Document, anchor: str) -> Paragraph:
    for paragraph in document.paragraphs:
        if paragraph.text.strip() == anchor.strip():
            return paragraph
    raise ValueError(f"anchor paragraph not found: {anchor!r}")


def style_half_points(document: Document, style_name: str | None, default: int = 24) -> int:
    if not style_name:
        return default
    size = document.styles[style_name].font.size
    return int(round(size.pt * 2)) if size else default


def add_inline(paragraph: Paragraph, item: dict[str, object], size: int) -> None:
    if "text" in item:
        paragraph.add_run(str(item["text"]))
        return
    latex = item.get("latex")
    if latex is None:
        raise ValueError("inline item must contain either 'text' or 'latex'")
    paragraph._p.append(latex_to_omml(str(latex), size=int(item.get("size", size))))


def add_display_formula(
    paragraph: Paragraph,
    latex: str,
    number: str | None,
    size: int,
    document: Document,
) -> None:
    paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
    section = document.sections[0]
    width = section.page_width - section.left_margin - section.right_margin
    width_in = width.inches if hasattr(width, "inches") else float(width) / 914400
    paragraph.paragraph_format.tab_stops.add_tab_stop(
        Inches(width_in / 2), WD_TAB_ALIGNMENT.CENTER
    )
    paragraph.paragraph_format.tab_stops.add_tab_stop(
        Inches(width_in), WD_TAB_ALIGNMENT.RIGHT
    )
    paragraph.add_run("\t")
    paragraph._p.append(latex_to_omml(latex, display=False, size=size))
    if number:
        paragraph.add_run("\t" + number)


def add_block(document: Document, previous: Paragraph, block: dict[str, object]) -> Paragraph:
    kind = str(block.get("type", "paragraph"))
    style_name = block.get("style")
    if style_name:
        style_name = str(style_name)
        document.styles[style_name]
    paragraph = insert_after(previous, style_name)
    if kind in {"heading", "paragraph"}:
        runs = block.get("runs")
        if runs is None:
            runs = [{"text": str(block.get("text", ""))}]
        for item in runs:
            add_inline(paragraph, dict(item), style_half_points(document, style_name))
    elif kind == "formula":
        add_display_formula(
            paragraph,
            str(block["latex"]),
            str(block["number"]) if block.get("number") is not None else None,
            int(block.get("size", style_half_points(document, style_name))),
            document,
        )
    else:
        raise ValueError(f"unsupported block type: {kind!r}")
    return paragraph


def write(template: Path, content_path: Path, output: Path) -> dict[str, object]:
    spec = json.loads(content_path.read_text(encoding="utf-8"))
    document = Document(template)
    anchor = find_anchor(document, str(spec["anchor"]))
    previous = anchor
    blocks = spec.get("blocks", [])
    for block in blocks:
        previous = add_block(document, previous, dict(block))
    output.parent.mkdir(parents=True, exist_ok=True)
    document.save(output)
    return {
        "template": str(template.resolve()),
        "output": str(output.resolve()),
        "anchor": str(spec["anchor"]),
        "blocks_written": len(blocks),
        "style_policy": "template styles only; no style definitions changed",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Write content using styles already present in a DOCX template.")
    parser.add_argument("template", type=Path)
    parser.add_argument("content", type=Path, help="JSON content specification")
    parser.add_argument("-o", "--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        summary = write(args.template, args.content, args.output)
    except (KeyError, ValueError, TypeError) as exc:
        print(f"ERROR: {exc}")
        return 2
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
