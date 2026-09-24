"""
MinerU Document Parser Module

This module provides a standalone document parser that uses MinerU as its core
dependency. MinerUParser is completely independent from DocumentParser and uses only:
    - mineru: Core document parsing library (mineru.cli.common.do_parse)
    - semantica utilities: Logging, progress tracking, exceptions

Key Features:
    - High-fidelity PDF parsing with layout analysis (MinerU 2.x)
    - Strong OCR for scanned and image-only PDFs (multilingual, incl. CJK)
    - Formula (LaTeX) and complex table structure recognition
    - Markdown export, per-page structure, table and image extraction
    - Local execution; models are downloaded automatically on first run
    - Standalone parser - no dependency on DocumentParser

Core Dependency:
    - mineru: Required for all parsing functionality
      (install with `pip install "semantica[parse-mineru]"` or `pip install "mineru[core]"`)

Main Classes:
    - MinerUParser: Standalone MinerU-based document parser

Example Usage:
    >>> from semantica.parse import MinerUParser
    >>> parser = MinerUParser()
    >>> result = parser.parse("document.pdf")
    >>> text = parser.extract_text("document.pdf")
    >>> tables = parser.extract_tables("document.pdf")

Author: Semantica Contributors
License: MIT
"""

import inspect
import json
import tempfile
import time
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from ..utils.exceptions import ProcessingError, ValidationError
from ..utils.logging import get_logger
from ..utils.progress_tracker import get_progress_tracker

# Try to import mineru, handle gracefully if not available
MINERU_AVAILABLE = False
MINERU_IMPORT_ERROR = None
do_parse = None

try:
    from mineru.cli.common import do_parse

    MINERU_AVAILABLE = True
    MINERU_IMPORT_ERROR = None
except (ImportError, OSError) as e:
    MINERU_AVAILABLE = False
    MINERU_IMPORT_ERROR = str(e)


class _HTMLTableParser(HTMLParser):
    """Minimal stdlib HTML table parser: collects rows of cell text."""

    def __init__(self):
        super().__init__()
        self.rows: List[List[str]] = []
        self._row: Optional[List[str]] = None
        self._cell: Optional[List[str]] = None

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self._row = []
        elif tag in ("td", "th"):
            self._cell = []

    def handle_endtag(self, tag):
        if tag == "tr" and self._row is not None:
            self.rows.append(self._row)
            self._row = None
        elif tag in ("td", "th") and self._cell is not None:
            text = "".join(self._cell).strip()
            if self._row is not None:
                self._row.append(text)
            self._cell = None

    def handle_data(self, data):
        if self._cell is not None:
            self._cell.append(data)

    def close(self):
        super().close()
        # Flush a cell/row left unterminated by malformed HTML
        if self._cell is not None and self._row is not None:
            self._row.append("".join(self._cell).strip())
            self._cell = None
        if self._row is not None:
            self.rows.append(self._row)
            self._row = None


def _html_table_to_rows(html_body: str) -> List[List[str]]:
    """Parse an HTML <table> fragment into a list of string rows."""
    if not html_body:
        return []
    parser = _HTMLTableParser()
    try:
        parser.feed(html_body)
        parser.close()
    except Exception:
        return []
    return [row for row in parser.rows if any(cell for cell in row)]


@dataclass
class MinerUMetadata:
    """Document metadata representation from MinerU."""

    title: Optional[str] = None
    page_count: int = 0
    format: Optional[str] = None
    backend: Optional[str] = None


class MinerUParser:
    """MinerU-based document parser for complex PDFs, OCR, tables, and formulas."""

    def __init__(self, **config):
        """
        Initialize MinerU parser.

        Args:
            **config: Parser configuration:
                - backend: MinerU backend ("pipeline", "vlm-transformers",
                  "vlm-sglang-engine", ...) (default: "pipeline")
                - parse_method: "auto", "txt", or "ocr" (default: "auto")
                - language: OCR language hint, e.g. "ch", "en" (default: None)
                - export_format: Export format ("markdown", "html") (default: "markdown")
                - output_dir: Directory to keep MinerU outputs (markdown, JSON,
                  extracted images). Defaults to a temporary directory that is
                  removed after parsing.
        """
        self.logger = get_logger("mineru_parser")
        self.config = config
        self.progress_tracker = get_progress_tracker()
        # Ensure progress tracker is enabled
        if not self.progress_tracker.enabled:
            self.progress_tracker.enabled = True

        self.backend = config.get("backend", "pipeline")
        self.parse_method = config.get("parse_method", "auto")
        self.language = config.get("language", None)
        self.export_format = config.get("export_format", "markdown")
        self.output_dir = config.get("output_dir", None)

    def parse(self, file_path: Union[str, Path], **options) -> Dict[str, Any]:
        """
        Parse document using MinerU.

        Args:
            file_path: Path to document file (PDF, or image)
            **options: Parsing options:
                - extract_text: Whether to extract text (default: True)
                - extract_tables: Whether to extract tables (default: True)
                - extract_images: Whether to collect image metadata (default: False)
                - export_format: Export format ("markdown", "html") (default: from config)
                - output_dir: Directory to keep MinerU outputs (default: from config)

        Returns:
            dict: Parsed document data matching Semantica format
        """
        file_path = Path(file_path)

        # Get pipeline_id from options if provided
        pipeline_id = options.get("pipeline_id", None)

        tracking_id = self.progress_tracker.start_tracking(
            file=str(file_path),
            module="parse",
            submodule="MinerUParser",
            message=f"MinerU: {file_path.name}",
            pipeline_id=pipeline_id,
        )

        try:
            if not file_path.exists():
                raise ValidationError(f"Document file not found: {file_path}")

            if not MINERU_AVAILABLE:
                if MINERU_IMPORT_ERROR:
                    raise ImportError(MINERU_IMPORT_ERROR)
                else:
                    raise ImportError("MinerU is not installed")

            # Stage 1: Initialization (0-10%)
            self.progress_tracker.update_progress(
                tracking_id,
                processed=1,
                total=10,
                message="Preparing MinerU pipeline (first run downloads models)..."
            )

            export_format = options.get("export_format", self.export_format)
            output_dir = Path(options.get("output_dir", self.output_dir) or tempfile.mkdtemp(prefix="semantica_mineru_"))
            output_dir.mkdir(parents=True, exist_ok=True)
            persistent_output = options.get("output_dir", self.output_dir) is not None

            # Stage 2: Document conversion (10-70%) - blocking; models may download
            self.progress_tracker.update_progress(
                tracking_id,
                processed=2,
                total=10,
                message=f"Converting document with MinerU ({self.backend} backend; this may take a while)..."
            )

            conversion_start = time.time()
            self._run_do_parse(file_path, output_dir)
            conversion_elapsed = time.time() - conversion_start

            # Stage 3: Locate outputs (70%)
            self.progress_tracker.update_progress(
                tracking_id,
                processed=7,
                total=10,
                message=f"Document conversion complete ({conversion_elapsed:.1f}s), extracting content..."
            )

            md_path = self._find_output(output_dir, (".md",), "markdown")
            middle_path = self._find_output(output_dir, ("_middle.json",), "middle.json")
            html_path = self._find_output(output_dir, (".html",), "html") if export_format == "html" else None

            # Stage 4: Text extraction (70-80%)
            extract_text = options.get("extract_text", True)
            extract_tables = options.get("extract_tables", True)
            extract_images = options.get("extract_images", False)

            full_text = ""
            if extract_text:
                self.progress_tracker.update_progress(
                    tracking_id,
                    processed=8,
                    total=10,
                    message=f"Extracting text content ({export_format} format)..."
                )
                source_path = html_path or md_path
                if source_path is not None:
                    full_text = source_path.read_text(encoding="utf-8")

            # Stage 5-7: Structure extraction from middle.json
            pages: List[Dict[str, Any]] = []
            tables: List[Dict[str, Any]] = []
            images: List[Dict[str, Any]] = []
            page_count = 0

            if middle_path is not None:
                try:
                    middle = json.loads(middle_path.read_text(encoding="utf-8"))
                    pages, tables, images, page_count = self._extract_from_middle(
                        middle, extract_tables, extract_images, output_dir, persistent_output
                    )
                except Exception as e:
                    self.logger.warning(f"Could not extract structure from middle.json: {e}")

            # Fallback: single page from full text when no middle.json was produced
            if not pages:
                pages.append({
                    "page_number": 1,
                    "text": full_text,
                    "width": 0,
                    "height": 0,
                    "tables": [],
                    "images": [],
                })
                page_count = max(page_count, 1)

            metadata = MinerUMetadata(
                title=file_path.stem,
                page_count=page_count,
                format=file_path.suffix.lower().lstrip(".") or "pdf",
                backend=self.backend,
            )

            extraction_counts = {
                "tables": len(tables),
                "images": len(images),
                "pages": page_count,
            }

            count_parts = []
            if extraction_counts["tables"] > 0:
                count_parts.append(f"{extraction_counts['tables']} tables")
            if extraction_counts["images"] > 0:
                count_parts.append(f"{extraction_counts['images']} images")
            if extraction_counts["pages"] > 0:
                count_parts.append(f"{extraction_counts['pages']} pages")

            if count_parts:
                completion_message = f"Parsed document (MinerU): {', '.join(count_parts)} extracted"
            else:
                completion_message = f"Parsed document (MinerU): 0 tables, 0 images, {extraction_counts['pages']} pages extracted"

            self.progress_tracker.stop_tracking(
                tracking_id,
                status="completed",
                message=completion_message,
                metadata={
                    "extraction_counts": extraction_counts,
                    "core_dependency": "mineru",
                },
            )

            return {
                "metadata": metadata.__dict__,
                "pages": pages,
                "full_text": full_text,
                "tables": tables,
                "images": images,
                "total_pages": page_count,
                "export_format": export_format,
                "output_dir": str(output_dir) if persistent_output else None,
            }

        except (ImportError, OSError):
            self.progress_tracker.stop_tracking(
                tracking_id, status="failed", message="MinerU not installed"
            )
            raise
        except Exception as e:
            self.progress_tracker.stop_tracking(
                tracking_id, status="failed", message=str(e)
            )
            self.logger.error(f"Failed to parse document with MinerU {file_path}: {e}")
            raise ProcessingError(f"Failed to parse document with MinerU: {e}")

    def extract_text(
        self, file_path: Union[str, Path], export_format: str = "markdown"
    ) -> str:
        """
        Extract text from document.

        Args:
            file_path: Path to document file
            export_format: Export format ("markdown", "html")

        Returns:
            str: Extracted text
        """
        result = self.parse(
            file_path,
            extract_tables=False,
            extract_images=False,
            export_format=export_format,
        )
        return result["full_text"]

    def extract_tables(
        self, file_path: Union[str, Path]
    ) -> List[Dict[str, Any]]:
        """
        Extract tables from document.

        Args:
            file_path: Path to document file

        Returns:
            list: Extracted tables
        """
        result = self.parse(
            file_path,
            extract_text=False,
            extract_images=False,
        )
        return result["tables"]

    def _run_do_parse(self, file_path: Path, output_dir: Path) -> None:
        """Invoke MinerU's do_parse, filtering kwargs to the supported signature."""
        pdf_bytes = file_path.read_bytes()
        stem = file_path.stem

        candidate_kwargs = {
            "backend": self.backend,
            "parse_method": self.parse_method,
            "f_dump_md": True,
            "f_dump_middle_json": True,
            "f_dump_content_list": True,
            "f_write_html": False,
            "f_draw_layout_bbox": False,
            "f_draw_span_bbox": False,
        }

        try:
            supported = set(inspect.signature(do_parse).parameters.keys())
        except (TypeError, ValueError):
            supported = None

        if supported:
            # Core arguments are shared across MinerU 2.x; extras vary by version.
            kwargs = {k: v for k, v in candidate_kwargs.items() if k in supported}
            do_parse(
                str(output_dir),
                [stem],
                [pdf_bytes],
                [self.language or ""],
                **kwargs,
            )
        else:
            # Signature introspection unavailable: call with core args only.
            do_parse(str(output_dir), [stem], [pdf_bytes], [self.language or ""])

    def _find_output(
        self, output_dir: Path, suffixes: Tuple[str, ...], label: str
    ) -> Optional[Path]:
        """Locate a MinerU output file anywhere below output_dir."""
        matches: List[Path] = []
        for suffix in suffixes:
            matches.extend(p for p in sorted(output_dir.rglob(f"*{suffix}")) if p.is_file())
        if not matches:
            return None
        if len(matches) > 1:
            self.logger.debug(f"Multiple {label} outputs found, using {matches[0]}")
        return matches[0]

    def _extract_from_middle(
        self,
        middle: Dict[str, Any],
        extract_tables: bool,
        extract_images: bool,
        output_dir: Path,
        persistent_output: bool,
    ) -> tuple:
        """Extract pages, tables, and images from MinerU middle.json."""
        pages: List[Dict[str, Any]] = []
        tables: List[Dict[str, Any]] = []
        images: List[Dict[str, Any]] = []

        pdf_info = middle.get("pdf_info") or []

        for page_index, page in enumerate(pdf_info):
            page_number = page.get("page_idx", page_index) + 1
            page_size = page.get("page_size") or [0, 0]
            blocks = page.get("para_blocks") or page.get("preproc_blocks") or page.get("blocks") or []

            page_text_parts: List[str] = []
            page_tables: List[Dict[str, Any]] = []
            page_images: List[Dict[str, Any]] = []

            for block in blocks:
                block_type = block.get("type", "")
                sub_blocks = block.get("blocks") or []
                bbox = block.get("bbox") or [0, 0, 0, 0]

                if block_type == "table":
                    if extract_tables:
                        table_data = self._extract_table_block(
                            block, sub_blocks, page_number, bbox
                        )
                        if table_data:
                            tables.append(table_data)
                            page_tables.append(table_data)

                elif block_type == "image":
                    if extract_images:
                        image_data = self._extract_image_block(
                            sub_blocks, page_number, bbox, output_dir, persistent_output
                        )
                        if image_data:
                            images.append(image_data)
                            page_images.append(image_data)

                else:
                    text = self._extract_block_text(block)
                    if text:
                        page_text_parts.append(text)
                    if extract_images:
                        for image_data in self._extract_inline_images(
                            block, page_number, output_dir, persistent_output
                        ):
                            images.append(image_data)
                            page_images.append(image_data)

            pages.append({
                "page_number": page_number,
                "text": "\n".join(page_text_parts).strip(),
                "width": page_size[0] if len(page_size) > 0 else 0,
                "height": page_size[1] if len(page_size) > 1 else 0,
                "tables": page_tables,
                "images": page_images,
            })

        return pages, tables, images, len(pdf_info)

    def _extract_block_text(self, block: Dict[str, Any]) -> str:
        """Collect text content from a MinerU block's lines/spans."""
        parts: List[str] = []
        for line in block.get("lines") or []:
            for span in line.get("spans") or []:
                content = span.get("content")
                if content:
                    parts.append(content)
                elif span.get("latex"):
                    parts.append(f"$${span['latex']}$$")
        return " ".join(parts).strip()

    @staticmethod
    def _find_table_html(node: Dict[str, Any]) -> str:
        """Locate table HTML on any level (block, sub-block, line, or span)."""
        if node.get("html"):
            return node["html"]
        for line in node.get("lines") or []:
            for span in line.get("spans") or []:
                if span.get("html"):
                    return span["html"]
        return ""

    def _extract_table_block(
        self,
        block: Dict[str, Any],
        sub_blocks: List[Dict[str, Any]],
        page_number: int,
        bbox: List[float],
    ) -> Optional[Dict[str, Any]]:
        """Extract one table block (HTML body parsed into rows)."""
        html_body = self._find_table_html(block)
        if not html_body:
            for sub in sub_blocks:
                html_body = self._find_table_html(sub)
                if html_body:
                    break

        rows = _html_table_to_rows(html_body or "")

        if not rows:
            # Fall back to data lines if no HTML body was produced
            for sub in sub_blocks:
                for line in sub.get("lines") or []:
                    row = [span.get("content", "") for span in line.get("spans") or []]
                    row = [cell for cell in row if cell]
                    if row:
                        rows.append(row)

        return {
            "rows": rows,
            "row_count": len(rows),
            "col_count": max(len(row) for row in rows) if rows else 0,
            "data": rows,
            "page_number": page_number,
            "html": html_body,
            "bbox": list(bbox),
        }

    def _extract_image_block(
        self,
        sub_blocks: List[Dict[str, Any]],
        page_number: int,
        bbox: List[float],
        output_dir: Path,
        persistent_output: bool,
    ) -> Optional[Dict[str, Any]]:
        """Extract one image block's path metadata."""
        image_path = None
        for sub in sub_blocks:
            if sub.get("image_path"):
                image_path = sub["image_path"]
                break
            for line in sub.get("lines") or []:
                for span in line.get("spans") or []:
                    if span.get("image_path"):
                        image_path = span["image_path"]
                        break

        if not image_path:
            return None

        resolved = output_dir / image_path
        return {
            "page_number": page_number,
            "image_path": str(resolved) if persistent_output and resolved.exists() else image_path,
            "x0": bbox[0] if len(bbox) > 0 else 0,
            "y0": bbox[1] if len(bbox) > 1 else 0,
            "x1": bbox[2] if len(bbox) > 2 else 0,
            "y1": bbox[3] if len(bbox) > 3 else 0,
            "width": (bbox[2] - bbox[0]) if len(bbox) > 2 else 0,
            "height": (bbox[3] - bbox[1]) if len(bbox) > 3 else 0,
        }

    def _extract_inline_images(
        self,
        block: Dict[str, Any],
        page_number: int,
        output_dir: Path,
        persistent_output: bool,
    ) -> List[Dict[str, Any]]:
        """Collect inline images embedded in text/title/list blocks.

        Wikipedia-style PDFs render inline formulas and small figures as
        image spans inside ordinary text blocks, not as image blocks.
        """
        found: List[Dict[str, Any]] = []
        for line in block.get("lines") or []:
            for span in line.get("spans") or []:
                image_path = span.get("image_path")
                if not image_path:
                    continue
                sbbox = span.get("bbox") or [0, 0, 0, 0]
                resolved = output_dir / image_path
                found.append({
                    "page_number": page_number,
                    "image_path": str(resolved) if persistent_output and resolved.exists() else image_path,
                    "inline": True,
                    "x0": sbbox[0] if len(sbbox) > 0 else 0,
                    "y0": sbbox[1] if len(sbbox) > 1 else 0,
                    "x1": sbbox[2] if len(sbbox) > 2 else 0,
                    "y1": sbbox[3] if len(sbbox) > 3 else 0,
                    "width": (sbbox[2] - sbbox[0]) if len(sbbox) > 2 else 0,
                    "height": (sbbox[3] - sbbox[1]) if len(sbbox) > 3 else 0,
                })
        return found
