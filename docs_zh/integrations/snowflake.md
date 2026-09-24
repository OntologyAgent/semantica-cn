---
title: Snowflake 集成
description: 将 Snowflake 表和查询中的结构化数据摄取进 Semantica 知识图谱流水线。
source: integrations/snowflake.md
source_version: 11f2cd9da8dc58b2315de98cdb6c1c26a6bd50c3
icon: "snowflake"
---

> 通过密码、密钥对、OAuth 与 SSO(单点登录)认证，把 Snowflake 的数据抽取进 Semantica。


## 安装

```bash
# Install with Snowflake support
pip install "semantica[db-snowflake]"

# Or install the connector separately
pip install snowflake-connector-python
```


## 基本用法

```python
from semantica.ingest import SnowflakeIngestor
import os

ingestor = SnowflakeIngestor(
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA"),
)

data = ingestor.ingest_table("CUSTOMERS")
print(f"Retrieved {data.row_count} rows: columns: {data.columns}")
```

<Tip>
用环境变量（或配合 `python-dotenv` 的 `.env` 文件）把凭据挡在源代码之外。不带参数的 `SnowflakeIngestor()` 会自动读取 `SNOWFLAKE_*` 环境变量。
</Tip>


## 认证方式

<Tabs>
  <Tab title="密码">
    ```python
    ingestor = SnowflakeIngestor(
        account="myaccount",
        user="myuser",
        password="mypassword",
        warehouse="COMPUTE_WH",
    )
    ```
  </Tab>
  <Tab title="密钥对（推荐）">
    ```python
    ingestor = SnowflakeIngestor(
        account="myaccount",
        user="myuser",
        private_key_path="/path/to/rsa_key.p8",
        warehouse="COMPUTE_WH",
    )
    ```
    生产环境首选：配置中不存放密码。
  </Tab>
  <Tab title="OAuth">
    ```python
    ingestor = SnowflakeIngestor(
        account="myaccount",
        user="myuser",
        authenticator="oauth",
        token="your_oauth_token",
        warehouse="COMPUTE_WH",
    )
    ```
  </Tab>
  <Tab title="SSO">
    ```python
    ingestor = SnowflakeIngestor(
        account="myaccount",
        user="myuser",
        authenticator="externalbrowser",
        warehouse="COMPUTE_WH",
    )
    ```
  </Tab>
</Tabs>


## 查询

### 带过滤条件摄取表

```python
data = ingestor.ingest_table(
    "CUSTOMERS",
    where="COUNTRY = 'USA' AND CREATED_DATE > '2024-01-01'",
    order_by="CREATED_DATE DESC",
    limit=10000,
)
```

### 自定义 SQL

```python
data = ingestor.ingest_query("""
    SELECT CUSTOMER_ID, SUM(AMOUNT) AS TOTAL_AMOUNT
    FROM SALES
    WHERE DATE >= '2024-01-01'
    GROUP BY CUSTOMER_ID
""")
```

### 查看表结构

```python
schema = ingestor.get_table_schema("CUSTOMERS")
for column in schema["columns"]:
    print(f"{column['name']}: {column['type']}")
```


## 导出为 Semantica 文档

```python
documents = ingestor.export_as_documents(
    data,
    id_field="CUSTOMER_ID",
    text_fields=["NAME", "EMAIL", "NOTES"],
)
print(f"Created {len(documents)} documents for processing")
```


## 大表分批处理

```python
PAGE_SIZE = 5000
for page in range(total_pages):
    data = ingestor.ingest_table(
        "LARGE_TABLE",
        limit=PAGE_SIZE,
        offset=page * PAGE_SIZE,
    )
    process_batch(data)
```

或使用内置的 `batch_size` 参数：

```python
data = ingestor.ingest_query(
    "SELECT * FROM LARGE_TABLE",
    batch_size=5000,
)
```


## 故障排查

```python
from semantica.ingest import SnowflakeConnector

connector = SnowflakeConnector(account="myaccount", user="myuser", password="mypassword")
if not connector.test_connection():
    print("Connection failed: check credentials and account identifier")
```


## 延伸阅读

- [摄取模块](../reference/ingest.md) — SnowflakeIngestor 及所有其他摄取器的完整参考。
- [Databricks 集成](./databricks.md) — Snowflake + Databricks 混合架构的配套连接器。
- [流水线](../reference/pipeline.md) — 把 Snowflake 摄取用作流水线步骤。
- [安装](../installation.md) — 全部可选依赖 extras。
- [知识图谱](../reference/kg.md) — 用摄取来的 Snowflake 数据构建知识图谱。
