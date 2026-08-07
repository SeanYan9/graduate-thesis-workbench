from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from docx_style_profile import profile
from omml import Parser
from template_writer import write
from validate_docx_math import validate


class DocxTemplateToolsTest(unittest.TestCase):
    def test_common_unicode_scripts_are_parsed(self) -> None:
        parsed = Parser("xᵢ²").parse()
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0].subscript.text, "i")
        self.assertEqual(parsed[0].superscript.text, "2")

    def test_template_styles_are_reused_and_formulas_are_native(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            template = root / "template.docx"
            content = root / "content.json"
            output = root / "output.docx"

            document = Document()
            body_style = document.styles.add_style("ThesisBody", WD_STYLE_TYPE.PARAGRAPH)
            body_style.font.name = "SimSun"
            body_style.font.size = Pt(12)
            heading_style = document.styles.add_style("ThesisHeading", WD_STYLE_TYPE.PARAGRAPH)
            heading_style.font.name = "SimHei"
            heading_style.font.size = Pt(14)
            formula_style = document.styles.add_style("ThesisFormula", WD_STYLE_TYPE.PARAGRAPH)
            formula_style.font.name = "Cambria Math"
            formula_style.font.size = Pt(12)
            document.add_paragraph("ANCHOR", style="ThesisHeading")
            document.save(template)

            content.write_text(
                json.dumps(
                    {
                        "anchor": "ANCHOR",
                        "blocks": [
                            {
                                "type": "heading",
                                "style": "ThesisHeading",
                                "text": "2.1 参数定义",
                            },
                            {
                                "type": "paragraph",
                                "style": "ThesisBody",
                                "runs": [
                                    {"text": "饱和度由式 "},
                                    {"latex": "X_p = \\frac{v_p}{c_p}"},
                                    {"text": " 计算。"},
                                ],
                            },
                            {
                                "type": "formula",
                                "style": "ThesisFormula",
                                "latex": "C = \\frac{1}{1-Y}",
                                "number": "(2-1)",
                            },
                        ],
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            before_styles = _zip_member(template, "word/styles.xml")
            summary = write(template, content, output)
            after_styles = _zip_member(output, "word/styles.xml")

            self.assertEqual(summary["blocks_written"], 3)
            self.assertEqual(before_styles, after_styles)
            self.assertEqual(validate(output)["status"], "PASS")

            profile_data = profile(output)
            self.assertGreaterEqual(profile_data["used_paragraph_styles"]["ThesisBody"], 1)
            self.assertGreaterEqual(profile_data["used_paragraph_styles"]["ThesisHeading"], 2)
            self.assertGreaterEqual(profile_data["used_paragraph_styles"]["ThesisFormula"], 1)

            with zipfile.ZipFile(output) as archive:
                document_xml = archive.read("word/document.xml").decode("utf-8")
            self.assertIn("oMath", document_xml)
            self.assertIn("fPr", document_xml)
            self.assertNotIn("\\frac", document_xml)


def _zip_member(path: Path, member: str) -> bytes:
    with zipfile.ZipFile(path) as archive:
        return archive.read(member)


if __name__ == "__main__":
    unittest.main()
