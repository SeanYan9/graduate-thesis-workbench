#!/usr/bin/env python3
"""Fail-closed smoke checks for native OMML and unresolved formula text."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import zipfile

from lxml import etree

M_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"m": M_NS, "w": W_NS}


def validate(path: Path) -> dict[str, object]:
    with zipfile.ZipFile(path) as archive:
        xml = archive.read("word/document.xml")
    root = etree.fromstring(xml)
    paragraphs = root.xpath(".//w:p", namespaces=NS)
    formulas = root.xpath(".//m:oMath | .//m:oMathPara", namespaces=NS)
    unresolved: list[str] = []
    duplicates: list[str] = []
    for paragraph in paragraphs:
        plain = "".join(paragraph.xpath(".//w:t/text()", namespaces=NS))
        if re.search(r"@@MATH_|\\frac|\\sqrt|\$\$?", plain):
            unresolved.append(plain)
        for math in paragraph.xpath(".//m:oMath", namespaces=NS):
            visible = "".join(math.xpath(".//m:t/text()", namespaces=NS)).strip()
            if len(visible) >= 3 and visible in plain:
                duplicates.append(visible)
    return {
        "path": str(path.resolve()),
        "omml_elements": len(formulas),
        "unresolved_formula_text": unresolved,
        "duplicate_math_text": duplicates,
        "status": "PASS" if formulas and not unresolved and not duplicates else "FAIL",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate native OMML and unresolved formula text in a DOCX.")
    parser.add_argument("docx", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = validate(args.docx)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"STATUS: {result['status']}")
        print(f"OMML_ELEMENTS: {result['omml_elements']}")
        print(f"UNRESOLVED: {len(result['unresolved_formula_text'])}")
        print(f"DUPLICATES: {len(result['duplicate_math_text'])}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
