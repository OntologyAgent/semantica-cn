---
title: "MinerU 集成"
description: "MinerU 原生集成：高保真 PDF 解析——版面分析、公式识别、复杂表格，以及面向扫描件和中日韩文档的强 OCR。"
source: integrations/mineru.md
source_version: 423819c56a17be9b4a8515dab67e8882cf40edd2
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

## 实测基准

两个解析器处理了同一份真实语料：中文维基百科《傅里叶变换》条目的 PDF 导出——13 页，行内与行间公式密集（以非文本对象渲染），含 9-10 个表格（内有一张大型变换对照表）和若干插图。耗时为 Apple 芯片 Mac 上的首次运行（`pipeline` 后端，CPU）。

| | DoclingParser | MinerUParser |
| :-- | :-- | :-- |
| 耗时（首次，含模型下载/加载） | 224 秒 | 445 秒（热跑 264 秒） |
| 抽取正文字符数 | 19,871 | 28,248 |
| 行内公式 | **全部丢失**（句中留空白） | **还原为 LaTeX**（如 `$\hat{\pmb f}$`） |
| 表格内的数学单元格 | **为空**（公式列空白） | **有内容**（逐格 OCR，带噪声） |
| 表格数量 | 9 | 9 |
| 图片 | 0（抽取报错） | 21（1 块级 + 20 行内，含路径和 bbox） |

实际含义：

- **公式是决定性差距。** 同一句话，Docling 返回「生成的函数 称作原函数 的傅里叶变换」——符号缺失、语义受损；MinerU 返回「生成的函数 $\hat{\pmb f}$ 称作原函数 $\pmb f$ 的傅里叶变换」。对数学、物理和量化研报类 PDF，这一项就足以定选型。
- **MinerU 的数学 OCR 有噪声但在场。** 积分号 `∫` 被读成 `8`，小数编号 `10.1` 误读为 `101`。对下游建知识图谱而言，「有噪声但在场」好过「干净地缺失」；`vlm-*` 后端还能进一步改善 `pipeline` 的结果。
- **面对干净、机器可读的多格式文档，Docling 仍是对的**——出首结果更快、安装更轻；本例中的公式丢失只在含公式的 PDF 上出现。

<Note>
  基准环境：MinerU 2.x `pipeline` 后端 + docling 2.129，macOS。绝对耗时因硬件而异；定性差距（公式、表格数学单元格）是结构性的。
</Note>


## 与直接使用官方 MinerU 的差异

`MinerUParser` 是包在 `mineru.cli.common.do_parse`（与官方 CLI 相同的入口）外面的一层薄而防御性的封装。相对官方包本身，Semantica 增加了：

- **统一结果结构**——与 `DocumentParser`、`DoclingParser` 共享同一套 `dict` 形状（`full_text`/`pages`/`tables`/`images`/`metadata`），流水线里解析器可互换。
- **零额外依赖的结构化表格**——用标准库 `HTMLParser` 把 MinerU 的表格 HTML 解析成行数组（不需要 pandas）；行数组和原始 HTML 同时返回。
- **跨 MinerU 小版本的签名过滤**——kwargs 按已安装 `do_parse` 的签名过滤，输出文件递归定位，抹平 2.x 的参数与目录布局变化。
- **进度跟踪与流水线集成**——解析各阶段接入 `semantica` 进度跟踪；可通过方法注册表（`method="mineru"`）和 `parse_document_mineru()` 调用。
- **可选依赖的优雅降级**——未安装 `mineru` 时导入 `semantica.parse` 永不失败；placeholder 类抛出带安装指引的错误。
- **图片元数据规范化**——块级图片与行内图片（维基式 PDF 把公式和插图以行内图片 span 嵌在正文里）统一给出路径和 bbox。

与官方行为保持一致的部分：模型选择与下载（`MINERU_MODEL_SOURCE`）、后端、`parse_method`、OCR 语言和输出文件格式。


## 延伸阅读

- [Parse 模块](../reference/parse.md) — DocumentParser、DoclingParser 与 MinerUParser 完整参考。
- [Docling 集成](../integrations/docling.md) — 多格式解析的替代方案。
- [Ingest 模块](../reference/ingest.md) — 解析前先加载文档。
- [Semantic Extract](../reference/semantic_extract.md) — 在解析出的文本上做实体与关系抽取。
- [Pipeline](../reference/pipeline.md) — 在完整流水线中使用 MinerUParser。
