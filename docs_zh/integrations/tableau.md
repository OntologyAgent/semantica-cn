---
title: Tableau 集成
description: 把 Tableau Server 或 Tableau Cloud 的工作簿与数据源元数据摄取到 Semantica 的知识图谱流水线。
source: integrations/tableau.md
source_version: cdff1c3a519cc2ae114093fec71318f1781466e3
icon: "chart-bar"
---

> 使用个人访问令牌（PAT）或用户名/密码身份验证，把工作簿元数据、已发布数据源清单和字段模式（Schema）从 Tableau 提取到 Semantica。

## 安装

```bash
# Install with Tableau support
pip install "semantica[ingest-tableau]"

# Or install the connector separately
pip install "tableauserverclient>=0.25"
```

## 基本用法

```python
import os
from semantica.ingest import TableauIngestor

ingestor = TableauIngestor(
    server_url=os.getenv("TABLEAU_SERVER_URL"),
    token_name=os.getenv("TABLEAU_TOKEN_NAME"),
    token_value=os.getenv("TABLEAU_TOKEN_VALUE"),
    site_name=os.getenv("TABLEAU_SITE_NAME", ""),  # empty = default site
)

# Ingest all workbooks
data = ingestor.ingest_workbooks()
print(f"Retrieved {data.row_count} workbook(s)")

# Export to Semantica document format for GraphBuilder
docs = ingestor.export_as_documents(data)
```

<Tip>
使用环境变量（或配合 `python-dotenv` 的 `.env` 文件）让凭据远离源代码。无参调用 `TableauIngestor()` 会自动读取 `TABLEAU_*` 环境变量。
</Tip>

## 身份验证

### 个人访问令牌（PAT）——推荐

```python
ingestor = TableauIngestor(
    server_url="https://your-server.tableau.example.com",
    site_name="your-site",          # empty string = default site
    token_name="my-pat-name",
    token_value=os.getenv("TABLEAU_TOKEN_VALUE"),
)
```

### 用户名 / 密码

```python
ingestor = TableauIngestor(
    server_url="https://your-server.tableau.example.com",
    username=os.getenv("TABLEAU_USERNAME"),
    password=os.getenv("TABLEAU_PASSWORD"),
)
```

## 环境变量

| 变量 | 说明 |
|---|---|
| `TABLEAU_SERVER_URL` | Tableau Server 或 Cloud 实例的基础 URL |
| `TABLEAU_SITE_NAME` | 站点名（默认站点用空字符串） |
| `TABLEAU_TOKEN_NAME` | 个人访问令牌名称 |
| `TABLEAU_TOKEN_VALUE` | 个人访问令牌值 |
| `TABLEAU_USERNAME` | Tableau 用户名（PAT 的替代方案） |
| `TABLEAU_PASSWORD` | Tableau 密码（PAT 的替代方案） |

## 摄取方法

### 工作簿

```python
# All workbooks
data = ingestor.ingest_workbooks()

# Filter by project
data = ingestor.ingest_workbooks(project_name="Finance")
```

### 数据源

```python
data = ingestor.ingest_datasources()
# or filter:
data = ingestor.ingest_datasources(project_name="Finance")
```

### 字段（来自指定数据源）

```python
data = ingestor.ingest_fields(datasource_id="<luid>")
```

## 导出为文档

```python
docs = ingestor.export_as_documents(data)
# Each doc: {"id": str, "text": str, "metadata": {"source": "tableau", "type": ..., ...}}
```

## 上下文管理器

```python
with TableauIngestor(
    server_url=os.getenv("TABLEAU_SERVER_URL"),
    token_name=os.getenv("TABLEAU_TOKEN_NAME"),
    token_value=os.getenv("TABLEAU_TOKEN_VALUE"),
) as t:
    workbooks = t.ingest_workbooks()
    datasources = t.ingest_datasources()
```

## TableauData 参考

| 字段 | 类型 | 说明 |
|---|---|---|
| `workbooks` | `list[dict]` | 工作簿元数据（id、name、project_name 等） |
| `datasources` | `list[dict]` | 数据源元数据（id、name、type 等） |
| `fields` | `list[dict]` | 使用 `ingest_fields()` 时的字段元数据 |
| `server_url` | `str` | Tableau Server 基础 URL |
| `site_name` | `str` | 摄取所用的站点名 |
| `row_count` | `int` | 结果集中的条目总数 |
| `ingested_at` | `datetime` | 摄取时间戳 |
