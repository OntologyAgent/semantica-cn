---
title: "Parse Module"
description: "Document parsing and text extraction: DocumentParser for standard formats, DoclingParser for complex layouts, and MinerUParser for scanned, formula-heavy PDFs."
icon: "file-lines"
---

**`semantica.parse`** extracts **structured text, layout, tables, and metadata** from unstructured documents:

- `DocumentParser`: broad format support (PDF, DOCX, HTML, JSON, CSV, PPTX, XLSX), no extra dependencies
- `DoclingParser`: complex layouts, merged-cell tables, multi-column PDFs, OCR (`pip install docling`)
- `MinerUParser`: layout analysis, formula recognition, and strong OCR for scanned PDFs (`pip install "mineru[core]"`)
- All return a consistent `dict` with `full_text`, `metadata`, `pages`, and `tables` keys
- `parse_batch()` processes multiple files in parallel with configurable error handling


## Getting Started

### Installation

The parse module works out of the box for standard formats:

```python
from semantica.parse import DocumentParser

parser = DocumentParser()
result = parser.parse("document.pdf")
print(result["full_text"])  # Extracted text content
```

For enhanced table extraction and complex layouts, install the Docling dependency:

```bash
pip install docling
```

```python
from semantica.parse import DoclingParser

parser = DoclingParser(export_format="markdown")
result = parser.parse("document.pdf", extract_tables=True)
print(result["tables"])  # Enhanced table extraction
```

For scanned, formula-heavy, or CJK-language PDFs, install MinerU instead:

```bash
pip install "mineru[core]"
```

```python
from semantica.parse import MinerUParser

parser = MinerUParser(parse_method="auto")
result = parser.parse("scanned_report.pdf")
print(result["full_text"])  # Layout-aware markdown with OCR
```

### First Document Parsing

```python
from semantica.parse import DocumentParser

# Parse any supported format
parser = DocumentParser()
result = parser.parse("annual_report.pdf")

# Access extracted content
text = result["full_text"]           # Complete document text
metadata = result["metadata"]        # Document properties
pages = result.get("pages", [])      # Page-level content

print(f"Extracted {len(text)} characters from {metadata.get('page_count', 0)} pages")
```

## Parser Selection Guide

<Tabs>
  <Tab title="DocumentParser: Standard">
    Zero extra dependencies. Use for clean PDFs, Word docs, HTML, and structured formats.

    | | |
    | :-- | :-- |
    | **Formats** | PDF, DOCX, HTML, TXT, JSON, CSV, PPTX, XLSX |
    | **Speed** | Fast |
    | **Setup** | None: included in base install |
    | **Best for** | Clean documents, broad format support, production pipelines |

    ```python
    from semantica.parse import DocumentParser

    parser = DocumentParser()
    result = parser.parse("contract.pdf")

    print(result["full_text"])        # Extracted text
    print(result["metadata"])         # Title, author, page count, ...
    print(len(result.get("pages", [])))  # Per-page breakdown
    ```
  </Tab>
  <Tab title="DoclingParser: Complex Layouts">
    Superior table extraction, OCR, multi-column PDFs. Requires `pip install docling`.

    | | |
    | :-- | :-- |
    | **Formats** | PDF, DOCX, PPTX, XLSX, HTML, images |
    | **Speed** | Slower (deep layout analysis) |
    | **Setup** | `pip install docling` |
    | **Best for** | Merged-cell tables, scanned documents, multi-column layouts |

    ```python
    from semantica.parse import DoclingParser

    parser = DoclingParser(export_format="markdown")
    result = parser.parse(
        "financial_report.pdf",
        extract_tables=True,
        extract_text=True,
    )

    for i, table in enumerate(result["tables"]):
        print(f"Table {i+1}: {table['row_count']} rows × {table['col_count']} columns")
        print(f"  Page: {table['page_number']}")
        for row in table["rows"][:3]:
            print(" | ".join(row))
    ```

    <Tip>
      Start with `DocumentParser`. Switch to `DoclingParser` only when you need better table extraction or encounter complex PDF layouts.
    </Tip>
  </Tab>
  <Tab title="MinerUParser: Scanned & Formula-heavy PDFs">
    Layout analysis, LaTeX formula recognition, and strong OCR (incl. CJK). Requires `pip install "mineru[core]"`; models download on first run.

    | | |
    | :-- | :-- |
    | **Formats** | PDF, images |
    | **Speed** | Slower (deep learning models; GPU recommended) |
    | **Setup** | `pip install "mineru[core]"` |
    | **Best for** | Scanned documents, formulas, complex tables, Chinese/Japanese/Korean PDFs |

    ```python
    from semantica.parse import MinerUParser

    parser = MinerUParser(parse_method="auto", language="ch")
    result = parser.parse("scanned_report.pdf", extract_tables=True)

    for i, table in enumerate(result["tables"]):
        print(f"Table {i+1}: {table['row_count']} rows (page {table['page_number']})")
        for row in table["rows"][:3]:
            print(" | ".join(row))
    ```

    <Tip>
      Start with `DocumentParser`. Switch to `DoclingParser` for better table extraction, or to `MinerUParser` when documents are scanned, formula-heavy, or CJK-language.
    </Tip>
  </Tab>
  <Tab title="Batch Processing">
    Process multiple files in parallel with per-file error isolation.

    ```python
    from semantica.parse import DocumentParser

    parser  = DocumentParser()
    results = parser.parse_batch(
        ["doc1.pdf", "doc2.docx", "doc3.html"],
        continue_on_error=True,   # skip failed files instead of raising
    )

    print(f"Parsed: {results['success_count']}/{results['total']}")

    for item in results["successful"]:
        print(f"{item['file_path']}: {len(item['result']['full_text'])} chars")

    for item in results["failed"]:
        print(f"FAILED: {item['file_path']}: {item['error']}")
    ```

    <Note>
      `continue_on_error=True` is recommended for production batch jobs where individual files may be corrupted or unsupported.
    </Note>
  </Tab>
</Tabs>

## Exported Classes

| Class | Role |
| :--- | :--- |
| `DocumentParser` | Auto-detects format: delegates to format-specific parser (PDF, DOCX, HTML, JSON, CSV, ...) |
| `DoclingParser` | Complex layouts, merged-cell tables, multi-column PDFs, and OCR (`pip install docling`) |
| `DoclingMetadata` | Document metadata from Docling parsing |
| `MinerUParser` | Layout analysis, formulas, and OCR for scanned PDFs (`pip install "mineru[core]"`) |
| `MinerUMetadata` | Document metadata from MinerU parsing |
| `PDFParser` | PDF text and metadata extraction |
| `WebParser` | URL fetch + HTML parsing |
| `EmailParser` | `.eml` / `.msg` email files with attachment extraction |
| `CodeParser` | Source code files with syntax-aware block detection |

## DocumentParser

Standard parser for clean, machine-readable documents:

```python
from semantica.parse import DocumentParser

parser = DocumentParser()
result = parser.parse("data/report.pdf")

print(result["full_text"])      # Complete extracted text
print(result["metadata"])       # Document properties (title, author, page_count, etc.)
if "pages" in result:           # Page-level content (when available)
    print(f"Pages: {len(result['pages'])}")
```

Supported formats: PDF, DOCX, HTML, TXT, JSON, CSV, PPTX, XLSX.

## DoclingParser

Advanced parser using the Docling backend: handles layouts that `DocumentParser` cannot:

```bash
pip install docling
```

```python
from semantica.parse import DoclingParser

parser = DoclingParser(
    export_format="markdown",      # Export format: "markdown" | "html" | "json"
    enable_ocr=False               # Enable OCR for scanned documents
)

result = parser.parse(
    "data/annual_report.pdf",
    extract_tables=True,           # Extract structured tables
    extract_images=False,          # Extract image regions
    extract_text=True              # Extract text content
)

print(result["full_text"])    # Complete extracted text
print(result["tables"])       # Structured table data
if "pages" in result:         # Page-level content
    print(f"Pages: {len(result['pages'])}")
```

Use `DoclingParser` for:

- Multi-column PDF layouts
- Tables with merged cells or complex headers
- PPTX slides with embedded charts
- XLSX spreadsheets with formulas
- Scanned documents with OCR
- Academic papers and technical reports

## MinerUParser

Advanced parser using the MinerU backend: built for documents that defeat both text-layer extraction and lighter layout tools:

```bash
pip install "mineru[core]"
```

```python
from semantica.parse import MinerUParser

parser = MinerUParser(
    backend="pipeline",            # "pipeline" | "vlm-transformers" | "vlm-sglang-engine"
    parse_method="auto",           # "auto" | "txt" | "ocr"
    language="ch",                 # OCR language hint (None = auto)
    export_format="markdown"       # "markdown" | "html"
)

result = parser.parse(
    "data/scanned_paper.pdf",
    extract_tables=True,
    extract_images=False,
    extract_text=True
)

print(result["full_text"])    # Layout-aware markdown (formulas as LaTeX)
print(result["tables"])       # Structured table data
print(result["total_pages"])
```

Use `MinerUParser` for:

- Scanned or image-only PDFs needing OCR
- Scientific papers with formulas (exported as LaTeX)
- Complex table structures and merged cells
- Chinese, Japanese, and Korean documents
- Multi-column layouts and reading-order reconstruction

<Note>
  MinerU downloads its models on first run (~1-2 GB). Set `MINERU_MODEL_SOURCE=modelscope` to download from ModelScope instead of HuggingFace. Pass `output_dir="..."` to keep the generated markdown, JSON, and extracted images instead of a temporary directory.
</Note>

## OCR Support

```python
parser = DoclingParser(
    enable_ocr=True,           # Enable OCR via PdfPipelineOptions
    export_format="markdown"
)

result = parser.parse("data/scanned_contract.pdf")
print(result["full_text"])     # OCR-extracted text
```

MinerU applies OCR through its `ocr` parse method, which also handles CJK text:

```python
parser = MinerUParser(parse_method="ocr", language="ch")
result = parser.parse("data/scanned_contract.pdf")
print(result["full_text"])     # OCR-extracted text
```

## Supported Formats

| Format | Extension | Parser Used | Notes |
| :------ | :--------- | :----------- | :----- |
| PDF | `.pdf` | `PDFParser` / `DoclingParser` / `MinerUParser` | Text, tables, metadata; Docling adds OCR; MinerU adds formulas and CJK OCR |
| Word | `.docx` | Built-in | Text, headings, tables, metadata |
| HTML | `.html`, `.htm` | `HTMLParser` / `WebParser` | `WebParser` fetches remote URLs |
| Markdown | `.md` | Built-in | Preserves heading hierarchy |
| Plain text | `.txt` | `TXTParser` | Minimal metadata |
| JSON | `.json` | `JSONParser` | One object per line or array |
| CSV / TSV | `.csv`, `.tsv` | `CSVParser` | Header auto-detected |
| Excel | `.xlsx`, `.xls` | Built-in | Sheet selection supported |
| PowerPoint | `.pptx` | Built-in | `DoclingParser` for embedded charts |
| Email | `.eml`, `.msg` | `EmailParser` | Attachments extracted |
| XML | `.xml` | `XMLIngestor` | XXE-safe, optional XSD validation |
| Archive | `.zip`, `.tar` | `FileIngestor` | Recursive extraction |
| Source code | `.py`, `.js`, `.java`, ... | `CodeParser` | AST-aware block detection |

## Parser Output Structure

Both parsers return dictionaries with the following structure:

```python
result = {
    "full_text": str,              # Complete extracted text
    "metadata": dict,              # Document properties and statistics
    "pages": List[dict],           # Page-level content (when available)
    "tables": List[dict],          # Structured table data (DoclingParser)
    "images": List[dict],          # Image regions (DoclingParser)
    "total_pages": int,            # Total page count
    "export_format": str           # Format used for text extraction (DoclingParser)
}
```

### Metadata Structure

```python
metadata = {
    "file_path": str,              # Source file path
    "page_count": int,             # Number of pages
    "format": str,                 # File format ("pdf", "docx", etc.)
    # Additional fields vary by parser and document type
}
```

## DocumentParser Methods

| Method | Returns | Description |
| :------ | :------- | :----------- |
| `parse(source)` | `dict` | Auto-detect format and extract text, metadata, tables |
| `parse_batch(sources)` | `dict` | Process multiple sources in parallel |
| `extract_text(path)` | `str` | Extract only text content from document |
| `extract_metadata(path)` | `dict` | Extract only metadata from document |

## Integration with FileIngestor

The most common pattern: ingest a directory then parse each source:

```python
from semantica.ingest import FileIngestor
from semantica.parse import DoclingParser

ingestor = FileIngestor()
parser   = DoclingParser(export_format="markdown")

sources = ingestor.ingest("data/reports/")
for source in sources:
    result = parser.parse(source)
    # Access extracted content
    text = result["full_text"]
    tables = result["tables"] 
    metadata = result["metadata"]
```

<Note>
  Docling and MinerU are optional dependencies. If `docling` is not installed, `DoclingParser` raises an `ImportError` with installation instructions: `pip install docling`; the same applies to `MinerUParser` (`pip install "mineru[core]"`). `DocumentParser` is always available and requires no extras.
</Note>

- [Ingest](/reference/ingest) — Load files before parsing.
- [Split](/reference/split) — Chunk parsed text for embedding and extraction.
- [Docling Integration](../integrations/docling) — Full Docling integration setup guide.
- [MinerU Integration](../integrations/mineru) — Full MinerU integration setup guide.
- [Semantic Extract](/reference/semantic_extract) — Extract entities and relations from parsed text.
