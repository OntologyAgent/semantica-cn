---
title: Databricks 集成
description: 把 Unity Catalog 元数据与 Delta Lake 表从 Databricks 摄取到 Semantica 的知识图谱流水线。
source: integrations/databricks.md
source_version: 1b26eb0f716c0da18696177687d5732360f5835e
icon: "cloud"
---

> 借助个人访问令牌(Personal Access Token)或 OAuth M2M 鉴权，从 Databricks 摄取(Ingestion) Delta Lake 表与 Unity Catalog 元数据（schema、血缘(Lineage)），送入 Semantica。


## 安装

```bash
# Install with Databricks support
pip install "semantica[db-databricks]"

# Or install the connectors separately
pip install databricks-sdk databricks-sql-connector
```


## 基本用法

```python
from semantica.ingest import DatabricksIngestor
import os

ingestor = DatabricksIngestor(
    host=os.getenv("DATABRICKS_HOST"),           # e.g. https://adb-xxx.azuredatabricks.net
    token=os.getenv("DATABRICKS_TOKEN"),
    http_path=os.getenv("DATABRICKS_HTTP_PATH"),  # SQL warehouse or cluster HTTP path
    catalog=os.getenv("DATABRICKS_CATALOG", "main"),
    schema=os.getenv("DATABRICKS_SCHEMA", "default"),
)

data = ingestor.ingest_table("customers")
print(f"Retrieved {data.row_count} rows: columns: {data.columns}")
```

<Tip>
用环境变量（或配合 `python-dotenv` 的 `.env` 文件）保管凭据，避免写进源代码。不带任何参数的 `DatabricksIngestor()` 会自动读取 `DATABRICKS_*` 环境变量。
</Tip>


## 鉴权方式

<Tabs>
  <Tab title="个人访问令牌">
    ```python
    ingestor = DatabricksIngestor(
        host="https://adb-xxx.azuredatabricks.net",
        token="dapi-xxxxxxxx",
        http_path="/sql/1.0/warehouses/xxxxxxxx",
    )
    ```
  </Tab>
  <Tab title="OAuth M2M（推荐）">
    ```python
    ingestor = DatabricksIngestor(
        host="https://adb-xxx.azuredatabricks.net",
        client_id="your_service_principal_client_id",
        client_secret="your_service_principal_client_secret",
        http_path="/sql/1.0/warehouses/xxxxxxxx",
    )
    ```
    生产环境优先选择这种方式：配置文件里不必长期保存个人访问令牌。
  </Tab>
</Tabs>

<Note>
`http_path` 标识执行查询所用的 SQL 仓库(SQL warehouse)或通用集群。在 Databricks 控制台的 **SQL Warehouses → Connection details** 下可以找到它。Unity Catalog 元数据调用（`list_catalogs`、`get_table_schema`、`get_table_lineage` 等）只需要 `host` 和凭据——这类调用用不到 `http_path`。
</Note>


## 查询

### 按条件摄取表

```python
data = ingestor.ingest_table(
    "customers",
    catalog="main",
    schema="default",
    where="country = 'USA' AND created_date > '2024-01-01'",
    order_by="created_date DESC",
    limit=10000,
)
```

### 自定义 SQL

```python
data = ingestor.ingest_query("""
    SELECT customer_id, SUM(amount) AS total_amount
    FROM main.default.sales
    WHERE date >= '2024-01-01'
    GROUP BY customer_id
""")
```


## Unity Catalog 元数据

### Schema 内省

```python
schema = ingestor.get_table_schema("customers")
for column in schema["columns"]:
    print(f"{column['name']}: {column['type']}")
```

### 目录(Catalog)、Schema 与表

```python
catalogs = ingestor.list_catalogs()
schemas = ingestor.list_schemas(catalog="main")
tables = ingestor.list_tables(catalog="main", schema="default")
```

### 表级与列级血缘

```python
lineage = ingestor.get_table_lineage("customers", catalog="main", schema="default")
print(lineage["upstream"])    # tables that feed into `customers`
print(lineage["downstream"])  # tables derived from `customers`
```

借助 Unity Catalog 自带的血缘追踪，`get_table_lineage` 可以直接在知识图谱(Knowledge Graph)里生成 `Table --DEPENDS_ON--> Table` 边，不必再从查询日志重新推导血缘。

<Tip>
传入 `include_column_lineage=True` 还能进一步解析列级的上下游引用（每列要多发一次 Unity Catalog 请求，因此默认关闭）：

```python
lineage = ingestor.get_table_lineage(
    "customers", catalog="main", schema="default", include_column_lineage=True,
)
print(lineage["columns"]["email"])
# {"upstream": ["main.default.raw_customers.email_address"], "downstream": []}
```

</Tip>


## 导出为 Semantica 文档

```python
documents = ingestor.export_as_documents(
    data,
    id_field="customer_id",
    text_fields=["name", "email", "notes"],
)
print(f"Created {len(documents)} documents for processing")
```


## 批量处理大表

```python
PAGE_SIZE = 5000
for page in range(total_pages):
    data = ingestor.ingest_table(
        "large_table",
        limit=PAGE_SIZE,
        offset=page * PAGE_SIZE,
    )
    process_batch(data)
```

也可以改用内置的 `batch_size` 参数：

```python
data = ingestor.ingest_query(
    "SELECT * FROM main.default.large_table",
    batch_size=5000,
)
```


## 故障排查

```python
from semantica.ingest import DatabricksConnector

connector = DatabricksConnector(
    host="https://adb-xxx.azuredatabricks.net",
    token="dapi-xxxxxxxx",
    http_path="/sql/1.0/warehouses/xxxxxxxx",
)
if not connector.test_connection():
    print("Connection failed: check host, http_path, and credentials")
```


## 延伸阅读

- [摄取模块](../reference/ingest.md) — `DatabricksIngestor` 与全部其他摄取器的完整参考。
- [Snowflake 集成](./snowflake.md) — 面向 Snowflake + Databricks 混合数据体系的配套连接器。
- [流水线](../reference/pipeline.md) — 把 Databricks 摄取作为流水线的一个步骤。
- [安装](../installation.md) — 全部可选依赖 extras。
- [知识图谱](../reference/kg.md) — 用摄取到的 Databricks 数据构建知识图谱。
