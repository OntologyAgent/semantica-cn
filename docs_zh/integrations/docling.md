---
title: Docling 集成
description: 原生 Docling 集成：高保真解析 PDF、DOCX 与 PPTX，支持表格抽取与 OCR。
source: integrations/docling.md
source_version: f246be0aa16d70cf892f39488aa272f97c033014
icon: "file-lines"
---

> 解析复杂文档——PDF、DOCX、PPTX、HTML——提供高保真的表格抽取，并内置 OCR。


## 概览

Docling 通过 `DoclingParser` 集成到 Semantica 的 `parse` 模块：文档先经过 Docling 的版面分析引擎(layout engine)，再直接进入 Semantica 的抽取与知识图谱(Knowledge Graph)流水线。

- **多格式** — PDF、DOCX、PPTX、HTML 等。
- **表格抽取** — 高保真表格解析，自动识别表头。
- **OCR 支持** — 内置光学字符识别(OCR)，可直接处理扫描文档。
- **Markdown 导出** — 输出整洁的 Markdown，为大语言模型(LLM)消费场景优化。


## 安装

```bash
pip install semantica
# Docling is included as an optional dependency
# or install separately:
pip install docling
```


## 基本用法

```python
from semantica.parse import DoclingParser

parser = DoclingParser(enable_ocr=True)
result = parser.parse("financial_report.pdf")

print(result["full_text"][:200])
print(f"Found {len(result['tables'])} tables")
```


## 完整示例

```python
from semantica.parse import DoclingParser

parser = DoclingParser(
    enable_ocr=True,
    export_format="markdown",
)

result = parser.parse("complex_invoice.pdf")

# Full text content
print(result["full_text"])

# Extracted tables
for i, table in enumerate(result["tables"]):
    print(f"Table {i+1} headers: {table.get('headers', [])}")
    for row in table.get("rows", [])[:3]:
        print(f"  Row: {row}")

# Metadata
metadata = result["metadata"]
print(f"Title: {metadata.get('title')}")
print(f"Pages: {result.get('total_pages')}")
```


## DoclingParser 参数

| 参数 | 默认值 | 说明 |
| :----------- | :--------- | :------------- |
| `enable_ocr` | `False` | 为扫描页面启用 OCR |
| `export_format` | `"markdown"` | 输出格式：`"markdown"` 或 `"text"` |


## 解析结果结构

```python
{
    "full_text":    str,         # Clean document text
    "tables":       List[dict],  # Extracted tables (headers + rows)
    "metadata":     dict,        # Title, author, creation date, etc.
    "total_pages":  int,
}
```


## 延伸阅读

- [解析模块](../reference/parse.md) — `DocumentParser` 与 `DoclingParser` 的完整参考。
- [摄取模块](../reference/ingest.md) — 解析之前先加载文档。
- [语义抽取](../reference/semantic_extract.md) — 在解析后的文本上执行命名实体识别(NER)与关系抽取。
- [流水线](../reference/pipeline.md) — 在完整流水线中使用 `DoclingParser`。
