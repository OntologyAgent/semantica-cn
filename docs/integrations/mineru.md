---
title: "MinerU Integration"
description: "Native MinerU integration for high-fidelity PDF parsing: layout analysis, formula recognition, complex tables, and strong OCR for scanned and CJK documents."
icon: "file-pdf"
---

> Parse scanned, formula-heavy, and CJK PDFs: with layout-aware markdown output, LaTeX formulas, and structured table extraction.


## Overview

MinerU is integrated into Semantica's `parse` module via the **`MinerUParser`**. Documents pass through MinerU's **deep learning layout pipeline**, then feed directly into Semantica's extraction and KG pipeline.

- **Layout Analysis** — Reading-order reconstruction for multi-column and complex pages.
- **Formula Recognition** — Equations are exported as LaTeX, ready for downstream processing.
- **Complex Tables** — Table structures (including merged cells) come back as row arrays plus HTML.
- **Strong OCR** — Scanned and image-only PDFs, with first-class Chinese/Japanese/Korean support.
- **Markdown Export** — Clean Markdown output optimized for LLM consumption.

<Info>
  MinerU focuses on PDFs and images. For DOCX, PPTX, XLSX, and HTML, use `DocumentParser` or `DoclingParser`.
</Info>


## Installation

```bash
pip install semantica[parse-mineru]
# or install separately:
pip install "mineru[core]"
```

<Note>
  MinerU downloads its models on first run (~1-2 GB). Set `MINERU_MODEL_SOURCE=modelscope` to download from ModelScope instead of HuggingFace — useful in mainland China. The `pipeline` backend runs on CPU; the `vlm-*` backends are higher quality and benefit from a GPU.
</Note>


## Basic Usage

```python
from semantica.parse import MinerUParser

parser = MinerUParser()
result = parser.parse("financial_report.pdf")

print(result["full_text"][:200])
print(f"Found {len(result['tables'])} tables")
```


## Full Example

```python
from semantica.parse import MinerUParser

parser = MinerUParser(
    backend="pipeline",        # "pipeline" | "vlm-transformers" | "vlm-sglang-engine"
    parse_method="auto",       # "auto" | "txt" | "ocr"
    language="ch",             # OCR language hint (None = auto)
    export_format="markdown",
)

result = parser.parse("scanned_annual_report.pdf")

# Full text content (layout-aware markdown, formulas as LaTeX)
print(result["full_text"])

# Extracted tables
for i, table in enumerate(result["tables"]):
    print(f"Table {i+1}: {table['row_count']} rows (page {table['page_number']})")
    for row in table.get("rows", [])[:3]:
        print(f"  Row: {row}")

# Per-page structure
for page in result["pages"]:
    print(f"Page {page['page_number']}: {len(page['text'])} chars, {len(page['tables'])} tables")

# Metadata
print(f"Pages: {result['total_pages']}, backend: {result['metadata']['backend']}")
```


## Keeping MinerU Outputs

By default MinerU writes into a temporary directory that is removed after parsing. Pass `output_dir` to keep the generated markdown, `middle.json`, `content_list.json`, and extracted images:

```python
parser = MinerUParser(output_dir="out/mineru/")
result = parser.parse("scanned_annual_report.pdf")
# out/mineru/scanned_annual_report/ now holds .md, JSONs, and images/
```


## MinerUParser Parameters

| Parameter | Default | Description |
| :----------- | :--------- | :------------- |
| `backend` | `"pipeline"` | MinerU backend: `"pipeline"`, `"vlm-transformers"`, `"vlm-sglang-engine"` |
| `parse_method` | `"auto"` | `"auto"`, `"txt"`, or `"ocr"` |
| `language` | `None` | OCR language hint, e.g. `"ch"`, `"en"` |
| `export_format` | `"markdown"` | Output format: `"markdown"` or `"html"` |
| `output_dir` | `None` | Keep MinerU outputs in this directory (default: temp dir) |


## Parsed Result Structure

```python
{
    "full_text":    str,         # Layout-aware markdown text
    "tables":       List[dict],  # rows, row_count, col_count, html, page_number
    "pages":        List[dict],  # Per-page text, tables, and dimensions
    "images":       List[dict],  # image_path, page_number, bbox
    "metadata":     dict,        # title, page_count, format, backend
    "total_pages":  int,
    "output_dir":   str | None,  # Set when output_dir was provided
}
```


## Choosing Between DoclingParser and MinerUParser

| | `DoclingParser` | `MinerUParser` |
| :-- | :-- | :-- |
| **Formats** | PDF, DOCX, PPTX, XLSX, HTML, images | PDF, images |
| **Formulas** | Limited | LaTeX recognition |
| **CJK documents** | OCR available | First-class (trained for CJK) |
| **Tables** | High-fidelity | High-fidelity + HTML body |
| **Weight** | Lighter install | Heavier install (torch + models) |

Both return the same Semantica result structure, so switching between them is a one-line change.


## See Also

- [Parse Module](../reference/parse) — Full DocumentParser, DoclingParser, and MinerUParser reference.
- [Docling Integration](../integrations/docling) — Multi-format parsing alternative.
- [Ingest Module](../reference/ingest) — Loading documents before parsing.
- [Semantic Extract](../reference/semantic_extract) — NER and relation extraction on parsed text.
- [Pipeline](../reference/pipeline) — Using MinerUParser in a full pipeline.
