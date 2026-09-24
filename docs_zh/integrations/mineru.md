---
title: "MinerU 集成"
description: "MinerU 原生集成：高保真 PDF 解析——版面分析、公式识别、复杂表格，以及面向扫描件和中日韩文档的强 OCR。"
source: integrations/mineru.md
source_version: 71fbf34eae12371d68b3c4de60970a2185369704
icon: "file-pdf"
---

> 解析扫描件、公式密集和中日韩 PDF：输出版面感知的 markdown，公式转 LaTeX，表格返回结构化数据。


## 概述

MinerU 通过 **`MinerUParser`** 接入 Semantica 的 `parse` 模块。文档先经过 MinerU 的**深度学习版面流水线**，再直接进入 Semantica 的抽取和知识图谱流水线。

- **版面分析**——多栏和复杂页面的阅读顺序重建。
- **公式识别**——公式导出为 LaTeX，可直接进入下游处理。
- **复杂表格**——表格结构（含合并单元格）以行数组加 HTML 两种形式返回。
- **强 OCR**——扫描件和纯图像 PDF，中日韩文本是一等公民。
- **Markdown 导出**——干净的 Markdown 输出，为 LLM 消费优化。

<Info>
  MinerU 专注于 PDF 和图片。DOCX、PPTX、XLSX 和 HTML 请用 `DocumentParser` 或 `DoclingParser`。
</Info>


## 安装

```bash
pip install semantica[parse-mineru]
# 或单独安装：
pip install "mineru[core]"
```

<Note>
  MinerU 首次运行会自动下载模型（约 1-2 GB）。设置 `MINERU_MODEL_SOURCE=modelscope` 可改从 ModelScope 下载——国内环境更稳。`pipeline` 后端 CPU 可跑；`vlm-*` 后端质量更高，建议配 GPU。
</Note>

<Note>
  macOS：`pipeline` 后端用进程池渲染 PDF 页面。如果解析报 `BrokenProcessPool`，在入口脚本最上方、调用 `MinerUParser` 之前执行 `multiprocessing.set_start_method("spawn", force=True)`。
</Note>


## 基本用法

```python
from semantica.parse import MinerUParser

parser = MinerUParser()
result = parser.parse("financial_report.pdf")

print(result["full_text"][:200])
print(f"Found {len(result['tables'])} tables")
```


## 完整示例

```python
from semantica.parse import MinerUParser

parser = MinerUParser(
    backend="pipeline",        # "pipeline" | "vlm-transformers" | "vlm-sglang-engine"
    parse_method="auto",       # "auto" | "txt" | "ocr"
    language="ch",             # OCR 语言提示（None = 自动）
    export_format="markdown",
)

result = parser.parse("scanned_annual_report.pdf")

# 全文内容（版面感知的 markdown，公式为 LaTeX）
print(result["full_text"])

# 抽取出的表格
for i, table in enumerate(result["tables"]):
    print(f"Table {i+1}: {table['row_count']} rows (page {table['page_number']})")
    for row in table.get("rows", [])[:3]:
        print(f"  Row: {row}")

# 逐页结构
for page in result["pages"]:
    print(f"Page {page['page_number']}: {len(page['text'])} chars, {len(page['tables'])} tables")

# 元数据
print(f"Pages: {result['total_pages']}, backend: {result['metadata']['backend']}")
```


## 保留 MinerU 的输出

默认情况下，MinerU 写入一个临时目录，解析完成后即删除。传入 `output_dir` 可以保留生成的 markdown、`middle.json`、`content_list.json` 和抽取出的图片：

```python
parser = MinerUParser(output_dir="out/mineru/")
result = parser.parse("scanned_annual_report.pdf")
# out/mineru/scanned_annual_report/ 下会保留 .md、JSON 和 images/
```


## MinerUParser 参数

| 参数 | 默认值 | 说明 |
| :----------- | :--------- | :------------- |
| `backend` | `"pipeline"` | MinerU 后端：`"pipeline"`、`"vlm-transformers"`、`"vlm-sglang-engine"` |
| `parse_method` | `"auto"` | `"auto"`、`"txt"` 或 `"ocr"` |
| `language` | `None` | OCR 语言提示，如 `"ch"`、`"en"` |
| `export_format` | `"markdown"` | 输出格式：`"markdown"` 或 `"html"` |
| `output_dir` | `None` | 把 MinerU 输出保留在该目录（默认临时目录） |


## 解析结果结构

```python
{
    "full_text":    str,         # 版面感知的 markdown 文本
    "tables":       List[dict],  # rows、row_count、col_count、html、page_number
    "pages":        List[dict],  # 逐页文本、表格与页面尺寸
    "images":       List[dict],  # image_path、page_number、bbox
    "metadata":     dict,        # title、page_count、format、backend
    "total_pages":  int,
    "output_dir":   str | None,  # 传入 output_dir 时返回该路径
}
```


## DoclingParser 与 MinerUParser 怎么选

| | `DoclingParser` | `MinerUParser` |
| :-- | :-- | :-- |
| **格式** | PDF、DOCX、PPTX、XLSX、HTML、图片 | PDF、图片 |
| **公式** | 有限支持 | LaTeX 识别 |
| **中日韩文档** | 可用 OCR | 一等支持（专为 CJK 训练） |
| **表格** | 高保真 | 高保真 + HTML 表体 |
| **安装重量** | 较轻 | 较重（torch + 模型） |

两者返回相同的 Semantica 结果结构，切换解析器只需改一行代码。


## 延伸阅读

- [Parse 模块](../reference/parse.md) — DocumentParser、DoclingParser 与 MinerUParser 完整参考。
- [Docling 集成](../integrations/docling.md) — 多格式解析的替代方案。
- [Ingest 模块](../reference/ingest.md) — 解析前先加载文档。
- [Semantic Extract](../reference/semantic_extract.md) — 在解析出的文本上做实体与关系抽取。
- [Pipeline](../reference/pipeline.md) — 在完整流水线中使用 MinerUParser。
