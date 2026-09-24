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

<Note>
  macOS: the `pipeline` backend renders PDF pages in a process pool. If parsing fails with `BrokenProcessPool`, call `multiprocessing.set_start_method("spawn", force=True)` at the top of your entry script, before using `MinerUParser`.
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


## Measured Benchmark

Both parsers processed the same real-world corpus: a 13-page Chinese Wikipedia export of the *Fourier transform* article — dense inline and interline formulas (rendered as non-text objects), 9–10 tables including a large transform reference table, and embedded figures. Timings are first-run on an Apple-silicon Mac (`pipeline` backend, CPU).

| | DoclingParser | MinerUParser |
| :-- | :-- | :-- |
| Time (first run, incl. model download/load) | 224 s | 445 s (264 s warm) |
| Text characters extracted | 19,871 | 28,248 |
| Inline formulas | **lost entirely** (blank gaps mid-sentence) | **recovered as LaTeX** (e.g. `$\hat{\pmb f}$`) |
| Math cells inside tables | **empty** (formula columns blank) | **populated** via cell OCR (with noise) |
| Table count | 9 | 9 |
| Images | 0 (extraction error) | 21 (1 block + 20 inline, with paths and bboxes) |

What this means in practice:

- **Formulas are the decisive gap.** The same sentence came back from Docling as "生成的函数 称作原函数 的傅里叶变换" — symbols missing, semantics damaged — while MinerU returned "生成的函数 $\hat{\pmb f}$ 称作原函数 $\pmb f$ 的傅里叶变换". For math, physics, and quant-research PDFs this alone decides the choice.
- **MinerU's math OCR is imperfect but present.** Integral signs came back garbled (`∫` read as `8`) and decimal numbering was misread (`10.1` → `101`). Noisy-but-present beats cleanly-absent for downstream KG use; the `vlm-*` backends improve on the `pipeline` results.
- **Docling remains the right tool for clean, machine-readable, multi-format documents** — it is faster to a first result and lighter to install; its formula loss here is specific to formula-bearing PDFs.

<Note>
  Benchmark run with MinerU 2.x `pipeline` backend and docling 2.129 on macOS. Absolute timings vary by hardware; the qualitative gaps (formulas, table math cells) are structural.
</Note>


## Differences from Using MinerU Directly

`MinerUParser` is a thin, defensive wrapper around `mineru.cli.common.do_parse` — the same entry point as the official CLI. What Semantica adds on top of the official package:

- **Unified result schema** — one `dict` shape (`full_text`/`pages`/`tables`/`images`/`metadata`) shared with `DocumentParser` and `DoclingParser`, so parsers are interchangeable in pipelines.
- **Structured tables without extra dependencies** — MinerU's table HTML is parsed into row arrays with the stdlib `HTMLParser` (pandas not required); both the rows and the raw HTML are returned.
- **Signature filtering across MinerU point releases** — kwargs are filtered against the installed `do_parse` signature, and output files are located recursively, smoothing over 2.x layout/argument changes.
- **Progress tracking and pipeline integration** — parsing stages report through `semantica`'s progress tracker, and the parser is reachable via the method registry (`method="mineru"`) and `parse_document_mineru()`.
- **Optional-dependency ergonomics** — importing `semantica.parse` never fails when `mineru` is absent; placeholders raise actionable errors instead.
- **Image metadata normalization** — block-level and inline images (Wikipedia-style PDFs embed formulas/figures as inline image spans) are surfaced with paths and bounding boxes.

What stays identical to the official behavior: model selection and download (`MINERU_MODEL_SOURCE`), backends, `parse_method`, OCR languages, and output file formats.


## See Also

- [Parse Module](../reference/parse) — Full DocumentParser, DoclingParser, and MinerUParser reference.
- [Docling Integration](../integrations/docling) — Multi-format parsing alternative.
- [Ingest Module](../reference/ingest) — Loading documents before parsing.
- [Semantic Extract](../reference/semantic_extract) — NER and relation extraction on parsed text.
- [Pipeline](../reference/pipeline) — Using MinerUParser in a full pipeline.
