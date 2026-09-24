---
title: "解析模块（Parse）"
description: "文档解析与文本抽取：标准格式用 DocumentParser，复杂版面用 DoclingParser。"
source: reference/parse.md
source_version: 166c207207c2e564fac79b66e8887a078f4ed3ba
icon: "file-lines"
---

**`semantica.parse`** 从非结构化文档中抽取**结构化文本、版面、表格和元数据**：

- `DocumentParser`：广泛的格式支持（PDF、DOCX、HTML、JSON、CSV、PPTX、XLSX），零额外依赖
- `DoclingParser`：复杂版面、合并单元格表格、多栏 PDF、OCR（`pip install docling`）
- 两者都返回结构一致的 `dict`，含 `full_text`、`metadata`、`pages`、`tables` 键
- `parse_batch()` 并行处理多个文件，错误处理策略可配置


## 快速开始

### 安装

解析模块对标准格式开箱即用：

```python
from semantica.parse import DocumentParser

parser = DocumentParser()
result = parser.parse("document.pdf")
print(result["full_text"])  # Extracted text content
```

需要更强的表格抽取和复杂版面支持时，安装 Docling 依赖：

```bash
pip install docling
```

```python
from semantica.parse import DoclingParser

parser = DoclingParser(export_format="markdown")
result = parser.parse("document.pdf", extract_tables=True)
print(result["tables"])  # Enhanced table extraction
```

### 解析第一个文档

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

## 解析器选择指南

<Tabs>
  <Tab title="DocumentParser：标准格式">
    零额外依赖。适合干净的 PDF、Word 文档、HTML 和结构化格式。

    | | |
    | :-- | :-- |
    | **格式** | PDF、DOCX、HTML、TXT、JSON、CSV、PPTX、XLSX |
    | **速度** | 快 |
    | **安装** | 无：基础安装已包含 |
    | **最适合** | 干净文档、广泛格式支持、生产流水线 |

    ```python
    from semantica.parse import DocumentParser

    parser = DocumentParser()
    result = parser.parse("contract.pdf")

    print(result["full_text"])        # Extracted text
    print(result["metadata"])         # Title, author, page count, ...
    print(len(result.get("pages", [])))  # Per-page breakdown
    ```
  </Tab>
  <Tab title="DoclingParser：复杂版面">
    更强的表格抽取、OCR、多栏 PDF。需要 `pip install docling`。

    | | |
    | :-- | :-- |
    | **格式** | PDF、DOCX、PPTX、XLSX、HTML、图片 |
    | **速度** | 较慢（深层版面分析） |
    | **安装** | `pip install docling` |
    | **最适合** | 合并单元格表格、扫描件、多栏版面 |

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
      先用 `DocumentParser`。只有需要更好的表格抽取、或遇到复杂 PDF 版面时再换 `DoclingParser`。
    </Tip>
  </Tab>
  <Tab title="批量处理">
    并行处理多个文件，单文件错误相互隔离。

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
      生产批量作业建议用 `continue_on_error=True`：个别文件可能损坏或格式不支持，但它们不应该拖垮整个批次。
    </Note>
  </Tab>
</Tabs>

## 导出的类

| 类 | 职责 |
| :--- | :--- |
| `DocumentParser` | 自动探测格式：分发给格式专属解析器（PDF、DOCX、HTML、JSON、CSV 等） |
| `DoclingParser` | 复杂版面、合并单元格表格、多栏 PDF 与 OCR（`pip install docling`） |
| `DoclingMetadata` | Docling 解析产出的文档元数据 |
| `PDFParser` | PDF 文本与元数据抽取 |
| `WebParser` | URL 抓取 + HTML 解析 |
| `EmailParser` | `.eml` / `.msg` 邮件文件，含附件抽取 |
| `CodeParser` | 源代码文件，带语法感知的块检测 |

## DocumentParser

可以把 `DocumentParser` 理解成一个调度员：先认出文件格式，再把解析工作分派给对应的格式专属解析器。具体来说，它是面向干净、机器可读文档的标准解析器：

```python
from semantica.parse import DocumentParser

parser = DocumentParser()
result = parser.parse("data/report.pdf")

print(result["full_text"])      # Complete extracted text
print(result["metadata"])       # Document properties (title, author, page_count, etc.)
if "pages" in result:           # Page-level content (when available)
    print(f"Pages: {len(result['pages'])}")
```

支持的格式：PDF、DOCX、HTML、TXT、JSON、CSV、PPTX、XLSX。

## DoclingParser

基于 Docling 后端的高级解析器，接管 `DocumentParser` 处理不了的版面：

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

以下场景用 `DoclingParser`：

- 多栏 PDF 版面
- 合并单元格或复杂表头的表格
- 带内嵌图表的 PPTX 幻灯片
- 含公式的 XLSX 电子表格
- 需要 OCR 的扫描件
- 学术论文和技术报告

## OCR 支持

```python
parser = DoclingParser(
    enable_ocr=True,           # Enable OCR via PdfPipelineOptions
    export_format="markdown"
)

result = parser.parse("data/scanned_contract.pdf")
print(result["full_text"])     # OCR-extracted text
```

## 支持的格式

| 格式 | 扩展名 | 使用的解析器 | 说明 |
| :------ | :--------- | :----------- | :----- |
| PDF | `.pdf` | `PDFParser` / `DoclingParser` | 文本、表格、元数据；Docling 加持 OCR |
| Word | `.docx` | 内置 | 文本、标题、表格、元数据 |
| HTML | `.html`、`.htm` | `HTMLParser` / `WebParser` | `WebParser` 可抓取远程 URL |
| Markdown | `.md` | 内置 | 保留标题层级 |
| 纯文本 | `.txt` | `TXTParser` | 元数据极少 |
| JSON | `.json` | `JSONParser` | 每行一个对象或数组 |
| CSV / TSV | `.csv`、`.tsv` | `CSVParser` | 自动探测表头 |
| Excel | `.xlsx`、`.xls` | 内置 | 支持工作表选择 |
| PowerPoint | `.pptx` | 内置 | 内嵌图表用 `DoclingParser` |
| 邮件 | `.eml`、`.msg` | `EmailParser` | 抽取附件 |
| XML | `.xml` | `XMLIngestor` | XML 外部实体注入(XXE)安全，可选 XSD 校验 |
| 压缩包 | `.zip`、`.tar` | `FileIngestor` | 递归解压 |
| 源代码 | `.py`、`.js`、`.java` 等 | `CodeParser` | AST 感知的块检测 |

## 解析器输出结构

两个解析器都返回如下结构的字典：

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

### Metadata 结构

```python
metadata = {
    "file_path": str,              # Source file path
    "page_count": int,             # Number of pages
    "format": str,                 # File format ("pdf", "docx", etc.)
    # Additional fields vary by parser and document type
}
```

## DocumentParser 方法

| 方法 | 返回 | 说明 |
| :------ | :------- | :----------- |
| `parse(source)` | `dict` | 自动探测格式，抽取文本、元数据、表格 |
| `parse_batch(sources)` | `dict` | 并行处理多个数据源 |
| `extract_text(path)` | `str` | 只抽取文档的文本内容 |
| `extract_metadata(path)` | `dict` | 只抽取文档的元数据 |

## 与 FileIngestor 集成

最常见模式：先摄取目录，再逐个解析数据源：

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
  Docling 是可选依赖。未安装 `docling` 时，`DoclingParser` 抛 `ImportError` 并附安装说明：`pip install docling`。`DocumentParser` 始终可用，无需任何 extra。
</Note>

- [Ingest](./ingest.md) — 解析前先加载文件。
- [Split](./split.md) — 把解析出的文本分块供嵌入与抽取。
- [Docling 集成](../integrations/docling.md) — Docling 完整集成设置指南。
- [Semantic Extract](./semantic_extract.md) — 从解析文本中抽取实体和关系。
