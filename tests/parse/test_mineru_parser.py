"""Tests for the MinerU document parser.

These tests mock MinerU's ``do_parse`` so they run without the (heavy)
``mineru`` package installed. The package-level integration point
(placeholder classes when MinerU is missing) is exercised conditionally.
"""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from semantica.parse.mineru_parser import (
    MINERU_AVAILABLE,
    MinerUParser,
    _html_table_to_rows,
)

SAMPLE_MIDDLE = {
    "pdf_info": [
        {
            "page_idx": 0,
            "page_size": [595.0, 842.0],
            "para_blocks": [
                {
                    "type": "title",
                    "lines": [{"spans": [{"content": "Quarterly Report"}]}],
                },
                {
                    "type": "text",
                    "lines": [{"spans": [{"content": "Revenue grew 20%."}]}],
                },
                {
                    "type": "table",
                    "bbox": [1.0, 2.0, 3.0, 4.0],
                    "blocks": [
                        {
                            "type": "table_body",
                            "html": "<table><tr><th>Item</th><th>Qty</th></tr>"
                            "<tr><td>Widget</td><td>3</td></tr></table>",
                        }
                    ],
                },
                {
                    "type": "image",
                    "bbox": [5.0, 6.0, 7.0, 8.0],
                    "blocks": [{"type": "image_body", "image_path": "images/hash.jpg"}],
                },
                {
                    "type": "equation",
                    "lines": [{"spans": [{"latex": "E=mc^2"}]}],
                },
            ],
        },
        {"page_idx": 1, "page_size": [595.0, 842.0], "para_blocks": []},
    ]
}


def _fake_do_parse_factory(markdown="# Report\n\ncontent"):
    """Build a do_parse stub that writes MinerU-style outputs under output_dir."""

    def fake_do_parse(output_dir, pdf_file_names, pdf_bytes_list, language_list, **kwargs):
        name = pdf_file_names[0]
        out = Path(output_dir) / name
        out.mkdir(parents=True, exist_ok=True)
        (out / f"{name}.md").write_text(markdown, encoding="utf-8")
        (out / f"{name}_middle.json").write_text(
            json.dumps(SAMPLE_MIDDLE), encoding="utf-8"
        )
        (out / name / "images").mkdir(parents=True, exist_ok=True)

    return fake_do_parse


class TestHTMLTableToRows(unittest.TestCase):
    def test_parses_simple_table(self):
        html = "<table><tr><th>A</th><th>B</th></tr><tr><td>1</td><td>2</td></tr></table>"
        self.assertEqual(_html_table_to_rows(html), [["A", "B"], ["1", "2"]])

    def test_handles_empty_and_malformed(self):
        self.assertEqual(_html_table_to_rows(""), [])
        self.assertEqual(_html_table_to_rows("<table><tr><td>x"), [["x"]])


class TestMinerUParser(unittest.TestCase):
    def setUp(self):
        self.available_patcher = patch(
            "semantica.parse.mineru_parser.MINERU_AVAILABLE", True
        )
        self.available_patcher.start()

        self.tempdir = tempfile.TemporaryDirectory()
        self.dummy_pdf = Path(self.tempdir.name) / "test.pdf"
        self.dummy_pdf.write_bytes(b"%PDF-1.4 fake")

        self.parser = MinerUParser()

    def tearDown(self):
        patch.stopall()
        self.tempdir.cleanup()

    def test_parse_returns_semantica_dict(self):
        with patch(
            "semantica.parse.mineru_parser.do_parse",
            side_effect=_fake_do_parse_factory(),
        ):
            result = self.parser.parse(str(self.dummy_pdf))

        self.assertIsInstance(result, dict)
        for key in ("full_text", "tables", "images", "pages", "metadata", "total_pages"):
            self.assertIn(key, result)
        self.assertEqual(result["full_text"], "# Report\n\ncontent")
        self.assertEqual(result["total_pages"], 2)
        self.assertEqual(result["metadata"]["page_count"], 2)
        self.assertEqual(result["metadata"]["backend"], "pipeline")

    def test_tables_extracted_from_middle_json(self):
        with patch(
            "semantica.parse.mineru_parser.do_parse",
            side_effect=_fake_do_parse_factory(),
        ):
            tables = self.parser.extract_tables(str(self.dummy_pdf))

        self.assertEqual(len(tables), 1)
        table = tables[0]
        self.assertEqual(table["rows"], [["Item", "Qty"], ["Widget", "3"]])
        self.assertEqual(table["row_count"], 2)
        self.assertEqual(table["col_count"], 2)
        self.assertEqual(table["page_number"], 1)
        self.assertIn("<table>", table["html"])

    def test_page_structure_and_equations(self):
        with patch(
            "semantica.parse.mineru_parser.do_parse",
            side_effect=_fake_do_parse_factory(),
        ):
            result = self.parser.parse(str(self.dummy_pdf), extract_images=True)

        page1 = result["pages"][0]
        self.assertIn("Quarterly Report", page1["text"])
        self.assertIn("Revenue grew 20%.", page1["text"])
        self.assertIn("$$E=mc^2$$", page1["text"])
        self.assertEqual(page1["width"], 595.0)
        self.assertEqual(len(page1["tables"]), 1)
        self.assertEqual(len(result["images"]), 1)
        self.assertEqual(result["images"][0]["page_number"], 1)

    def test_missing_file_raises_processing_error(self):
        # Matching DoclingParser semantics: parse() wraps any failure
        # (including missing files) in ProcessingError.
        from semantica.utils.exceptions import ProcessingError

        with patch(
            "semantica.parse.mineru_parser.do_parse",
            side_effect=_fake_do_parse_factory(),
        ):
            with self.assertRaises(ProcessingError) as ctx:
                self.parser.parse(str(Path(self.tempdir.name) / "nope.pdf"))
        self.assertIn("not found", str(ctx.exception))

    def test_unavailable_mineru_raises_import_error(self):
        with patch("semantica.parse.mineru_parser.MINERU_AVAILABLE", False):
            with patch("semantica.parse.mineru_parser.MINERU_IMPORT_ERROR", None):
                with self.assertRaises(ImportError):
                    self.parser.parse(str(self.dummy_pdf))


class TestPackageIntegrationPoint(unittest.TestCase):
    def test_export_matches_availability(self):
        """The package export must be a placeholder iff mineru is missing."""
        from semantica.parse import MINERU_AVAILABLE as PKG_AVAILABLE
        from semantica.parse import MinerUParser as ExportedParser

        if PKG_AVAILABLE or MINERU_AVAILABLE:
            self.assertTrue(callable(ExportedParser))
        else:
            with self.assertRaises(ImportError):
                ExportedParser()


class TestMethodRegistration(unittest.TestCase):
    def test_parse_document_mineru_registered(self):
        from semantica.parse.methods import parse_document_mineru
        from semantica.parse.registry import method_registry

        self.assertTrue(callable(parse_document_mineru))
        method = method_registry.get("document", "mineru")
        self.assertEqual(method, parse_document_mineru)


if __name__ == "__main__":
    unittest.main()


class _V4Span:
    def __init__(self, content):
        self.content = content


class _V4TextBlock:
    def __init__(self, btype, text, bbox=None):
        self.type = btype
        self.bbox = bbox
        if isinstance(text, list):
            self.content = [_V4Span(t) for t in text]
        else:
            self.content = text


class _V4TableBlock:
    def __init__(self, html, bbox=None):
        self.type = "table"
        self.bbox = bbox
        self.content = [_V4TextBlock("table_body", html)]


class _V4ImageBlock:
    def __init__(self, image_path, bbox=None):
        self.type = "image"
        self.bbox = bbox
        self.content = [_V4TextBlock("image_body", "") ]
        self.content[0].image_path = image_path


class _V4Page:
    def __init__(self, page_idx, blocks):
        self.page_idx = page_idx
        self.blocks = blocks


class _V4Result:
    def __init__(self, pages, markdown="# Report\n\ncontent"):
        self.pages = pages
        self._markdown = markdown

    def markdown(self):
        return self._markdown


def _fake_v4_result():
    return _V4Result(pages=[
        _V4Page(0, [
            _V4TextBlock("doc_title", ["Quarterly Report"]),
            _V4TextBlock("text", ["Revenue grew 20%."]),
            _V4TableBlock("<table><tr><th>Item</th><th>Qty</th></tr>"
                          "<tr><td>Widget</td><td>3</td></tr></table>"),
            _V4ImageBlock("images/hash.jpg"),
            _V4TextBlock("equation", "E=mc^2"),
        ]),
        _V4Page(1, []),
    ])


class TestMinerUParserV4(unittest.TestCase):
    """MinerU >= 4 path: the public SDK parse() replaces do_parse."""

    def setUp(self):
        self.dummy_pdf = Path(tempfile.mkstemp(suffix=".pdf")[1])
        self.dummy_pdf.write_bytes(b"%PDF-1.4 minimal")
        self.available_patcher = patch(
            "semantica.parse.mineru_parser.MINERU_AVAILABLE", True
        )
        self.version_patcher = patch(
            "semantica.parse.mineru_parser.MINERU_API_VERSION", "v4"
        )
        self.available_patcher.start()
        self.version_patcher.start()
        self.parser = MinerUParser()

    def tearDown(self):
        patch.stopall()
        self.dummy_pdf.unlink(missing_ok=True)

    def test_parse_returns_semantica_dict(self):
        captured = {}

        def fake_parse(path, **kwargs):
            captured.update(kwargs)
            return _fake_v4_result()

        with patch(
            "semantica.parse.mineru_parser.mineru_parse", side_effect=fake_parse
        ):
            result = self.parser.parse(str(self.dummy_pdf))

        # backend "pipeline" maps to the v4 "basic" tier; parse_method -> ocr_mode
        self.assertEqual(captured.get("tier"), "basic")
        self.assertEqual(captured.get("ocr_mode"), "auto")
        self.assertEqual(result["full_text"], "# Report\n\ncontent")
        self.assertEqual(result["total_pages"], 2)
        self.assertEqual(result["metadata"]["page_count"], 2)

    def test_vlm_backend_maps_to_standard_tier(self):
        parser = MinerUParser(backend="vlm-transformers")
        captured = {}

        def fake_parse(path, **kwargs):
            captured.update(kwargs)
            return _fake_v4_result()

        with patch(
            "semantica.parse.mineru_parser.mineru_parse", side_effect=fake_parse
        ):
            parser.parse(str(self.dummy_pdf))

        self.assertEqual(captured.get("tier"), "standard")

    def test_tables_and_pages_extracted_from_v4_result(self):
        with patch(
            "semantica.parse.mineru_parser.mineru_parse",
            return_value=_fake_v4_result(),
        ):
            tables = self.parser.extract_tables(str(self.dummy_pdf))

        self.assertEqual(len(tables), 1)
        self.assertEqual(tables[0]["rows"], [["Item", "Qty"], ["Widget", "3"]])
        self.assertEqual(tables[0]["page_number"], 1)

    def test_titles_and_equations_reach_page_structure(self):
        with patch(
            "semantica.parse.mineru_parser.mineru_parse",
            return_value=_fake_v4_result(),
        ):
            result = self.parser.parse(str(self.dummy_pdf))

        page_one = result["pages"][0]
        self.assertIn("Quarterly Report", page_one["text"])
        self.assertIn("Revenue grew 20%.", page_one["text"])
        self.assertIn("$$E=mc^2$$", page_one["text"])
