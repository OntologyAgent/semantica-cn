---
title: BigQuery 集成
description: 把 Google BigQuery 表和查询中的结构化数据摄取进 Semantica 的知识图谱流水线。
source: integrations/bigquery.md
source_version: b5890034896dd2a8fc3a56c8dcbfb87dae6189ad
icon: "google"
---

> 通过应用默认凭据(Application Default Credentials)或服务账号密钥文件认证，从 BigQuery 的表、查询和表结构(schema)中把数据抽取进 Semantica。


## 安装

```bash
# Install with BigQuery support
pip install "semantica[db-bigquery]"

# Or install the connector separately
pip install google-cloud-bigquery>=3.0.0
```


## 基本用法

```python
import os
from semantica.ingest import BigQueryIngestor

ingestor = BigQueryIngestor(
    project=os.getenv("BIGQUERY_PROJECT"),
    dataset=os.getenv("BIGQUERY_DATASET"),
)

data = ingestor.ingest_table("orders", limit=1000)
print(f"Retrieved {data.row_count} rows, columns: {data.columns}")
```

<Tip>
用环境变量（或配合 `python-dotenv` 使用 `.env` 文件）存放配置，别把它们写死在源代码里。只要设置了 `BIGQUERY_PROJECT`，不带参数的 `BigQueryIngestor()` 就会自动读取 `BIGQUERY_*` 环境变量。
</Tip>


## 认证

<Tabs>
  <Tab title="应用默认凭据（推荐）">
    ```python
    import os
    from semantica.ingest import BigQueryIngestor

    ingestor = BigQueryIngestor(
        project=os.getenv("BIGQUERY_PROJECT"),
        dataset=os.getenv("BIGQUERY_DATASET"),
    )
    ```

    在环境中设置 `BIGQUERY_PROJECT`，可选设置 `BIGQUERY_DATASET`：

    ```bash
    export BIGQUERY_PROJECT="my-gcp-project"
    export BIGQUERY_DATASET="my_dataset"
    ```

    ADC 会按以下顺序自动从环境中解析凭据：
    1. `GOOGLE_APPLICATION_CREDENTIALS` 环境变量（密钥文件的路径）
    2. gcloud 默认凭据（`gcloud auth application-default login`）
    3. 挂载的服务账号（GKE、Cloud Run、Vertex AI、Compute Engine）

    本地开发时执行：

    ```bash
    gcloud auth application-default login
    ```

    生产环境中，如果工作负载身份已绑定服务账号，就不需要任何凭据文件。
  </Tab>
  <Tab title="服务账号密钥文件">
    ```python
    import os
    from semantica.ingest import BigQueryIngestor

    ingestor = BigQueryIngestor(
        project=os.getenv("BIGQUERY_PROJECT"),
        dataset=os.getenv("BIGQUERY_DATASET"),
        credentials_file=os.getenv("BIGQUERY_CREDENTIALS_FILE"),
    )
    ```

    ```bash
    export BIGQUERY_PROJECT="my-gcp-project"
    export BIGQUERY_DATASET="my_dataset"
    export BIGQUERY_CREDENTIALS_FILE="/run/secrets/sa-key.json"
    ```

    在 GCP 控制台的 **IAM & Admin → Service Accounts → [你的服务账号] → Keys** 页面下载 JSON 密钥文件。不要把它提交进版本控制，改用密钥管理服务或挂载卷注入。

    服务账号至少需要在项目上拥有 **BigQuery Data Viewer**（`roles/bigquery.dataViewer`）和 **BigQuery Job User**（`roles/bigquery.jobUser`）两个角色。
  </Tab>
</Tabs>


## 环境变量

所有构造函数参数都支持环境变量兜底：

| 变量 | 参数 | 默认值 |
|---|---|---|
| `BIGQUERY_PROJECT` | `project` | —（必填） |
| `BIGQUERY_DATASET` | `dataset` | — |
| `BIGQUERY_LOCATION` | `location` | 项目默认值 |
| `BIGQUERY_CREDENTIALS_FILE` | `credentials_file` | ADC |


## 表摄取

### 带过滤条件摄取表

```python
data = ingestor.ingest_table(
    "orders",
    where="status = 'shipped' AND created_date >= '2024-01-01'",
    order_by="created_date DESC",
    limit=50000,
)
print(f"Fetched {data.row_count} rows from {data.table_name}")
```

<Warning>
`where` 和 `order_by` 接受原始 SQL 片段。它们会经过一份黑名单校验（语句分隔符、UNION、DML/DDL 关键字、注释序列），但设计初衷是面向可信的、由运维人员控制的输入。不要把最终用户的原始文本直接传给这两个参数。
</Warning>

### 在单次调用中覆盖 project 与 dataset

```python
data = ingestor.ingest_table(
    "transactions",
    project="analytics-project-456",
    dataset="finance",
    limit=10000,
)
```

### 从全限定表名摄取

```python
# project and dataset on the ingestor default to the connector's values;
# you can override them at the call site for cross-project queries.
data = ingestor.ingest_table(
    "daily_sales",
    project="reporting-project",
    dataset="warehouse",
)
```


## 自定义 SQL 查询

```python
data = ingestor.ingest_query("""
    SELECT
        customer_id,
        SUM(amount) AS total_amount,
        COUNT(*) AS order_count
    FROM `my-project`.`sales`.`orders`
    WHERE DATE(created_at) >= '2024-01-01'
    GROUP BY customer_id
    ORDER BY total_amount DESC
    LIMIT 1000
""")
print(f"Query returned {data.row_count} rows")
```

查询字符串会原样传给 BigQuery，SQL 的正确性与安全性由调用方负责。

### 参数化查询

```python
from google.cloud import bigquery

job_config = bigquery.QueryJobConfig(
    query_parameters=[
        bigquery.ScalarQueryParameter("min_amount", "FLOAT64", 100.0),
    ]
)

data = ingestor.ingest_query(
    "SELECT id, amount FROM `my-project`.`sales`.`orders` WHERE amount >= @min_amount",
    job_config=job_config,
)
```


## 表结构检查

```python
# Inspect columns for a table
schema = ingestor.get_table_schema("orders")

print(f"Row count: {schema['num_rows']}")
print(f"Clustering fields: {schema['clustering_fields']}")
for col in schema["columns"]:
    nullable = "NULLABLE" if col["nullable"] else "REQUIRED"
    print(f"  {col['name']}: {col['type']} ({nullable})")
```

### 列出数据集中的表

```python
tables = ingestor.list_tables()
print(f"Tables in dataset: {tables}")
# ['customers', 'orders', 'products', 'returns']

# Or specify a different dataset
tables = ingestor.list_tables(dataset="analytics", project="my-other-project")
```


## 导出为 Semantica 文档

把摄取到的行转换成 Semantica 文档格式，供 `GraphBuilder` 使用：

```python
documents = ingestor.export_as_documents(
    data,
    id_field="order_id",              # field to use as document ID
    text_fields=["customer_name", "product_name", "notes"],
)

print(f"Created {len(documents)} documents")
# Each document:
# {
#   "id": "ORD-12345",
#   "text": "Alice Smith Widget Pro Shipped on time",
#   "metadata": {
#     "source": "bigquery",
#     "table": "orders",
#     "project": "my-gcp-project",
#     "dataset": "sales",
#     "location": "US",
#     "row_data": { ... full original row ... }
#   }
# }
```

把文档直接交给 `GraphBuilder`：

```python
from semantica.kg import GraphBuilder

builder = GraphBuilder()
kg = builder.build(documents)
```

省略 `text_fields` 时，每行中所有 `str` 类型的列值会拼接成文档文本；整数、浮点数、Decimal 与 `None` 值不参与默认文本的拼装。


## 上下文管理器

批量执行查询时建议用上下文管理器——进入时打开一个客户端、退出时关闭，`with` 块内的每次调用都复用同一个已完成认证的会话：

```python
import os
from semantica.ingest import BigQueryIngestor

with BigQueryIngestor(
    project=os.getenv("BIGQUERY_PROJECT"),
    dataset=os.getenv("BIGQUERY_DATASET"),
) as bq:
    orders = bq.ingest_table("orders", limit=10000)
    customers = bq.ingest_table("customers", limit=5000)
    tables = bq.list_tables()
    schema = bq.get_table_schema("orders")
```

不使用上下文管理器时，每次方法调用都会各自打开并关闭一个临时客户端。


## 连接测试

```python
import os
from semantica.ingest import BigQueryConnector

connector = BigQueryConnector(
    project=os.getenv("BIGQUERY_PROJECT"),
)
if connector.test_connection():
    print("Connected to BigQuery successfully.")
else:
    print("Connection failed — check project ID and credentials.")
```


## 故障排查

**`ImportError: BigQuery ingestion requires optional dependency 'google-cloud-bigquery'`**

安装对应的可选 extra：

```bash
pip install "semantica[db-bigquery]"
```

**`google.auth.exceptions.DefaultCredentialsError`**

环境中没有找到任何凭据。可以任选其一：

- 本地开发运行 `gcloud auth application-default login`；或
- 把 `GOOGLE_APPLICATION_CREDENTIALS` 指向服务账号 JSON 密钥文件的路径；或
- 把 `BIGQUERY_CREDENTIALS_FILE` 指向服务账号 JSON 密钥文件的路径。

**`google.api_core.exceptions.Forbidden`**

服务账号或用户账号没有访问该数据集或表的权限。请确保账号至少拥有：

- 数据集或项目上的 `roles/bigquery.dataViewer`
- 项目上的 `roles/bigquery.jobUser`

**`ValidationError: Invalid BigQuery project ID`**

项目 ID 可以包含字母、数字、连字符和下划线，且必须以字母开头。纯数字或以连字符开头的项目 ID 一律拒绝。

**`ValidationError: Invalid table_name`**

表名和数据集名必须以字母或下划线开头，且只能包含字母、数字和下划线。表名和数据集名不允许使用连字符（请改用下划线）。

**查询缓慢**

用 `limit` 和 `where` 限制取回的行数。面对大型分析查询，考虑改用 `ingest_query()` 配合预聚合的 SQL 语句，而不是直接摄取原始表行。


## 延伸阅读

- [摄取模块](../reference/ingest.md) — `BigQueryIngestor` 的完整 API 与所有其他摄取器。
- [Snowflake 集成](./snowflake.md) — 设计类似的数仓连接器。
- [Redshift 集成](./redshift.md) — AWS Redshift 连接器。
- [Databricks 集成](./databricks.md) — 湖仓一体(Lakehouse)连接器。
- [安装](../installation.md) — 全部可选依赖 extra。
- [知识图谱](../reference/kg.md) — 用摄取的 BigQuery 数据构建知识图谱。
