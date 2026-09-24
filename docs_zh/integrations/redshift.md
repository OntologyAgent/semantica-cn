---
title: Amazon Redshift 集成
description: 将 Amazon Redshift 表和查询中的结构化数据摄取进 Semantica 知识图谱流水线。
source: integrations/redshift.md
source_version: 1112970cbde65cf4aa02b6e5f89d8e52efa9889b
icon: "database"
---

> 借助密码/原生或 IAM 角色认证，通过 PostgreSQL 兼容的传输协议，把 Amazon Redshift 的数据抽取进 Semantica。


## 安装

```bash
# Install with Redshift support
pip install "semantica[db-redshift]"

# Or install the connector separately
pip install redshift-connector>=2.0.0
```

`redshift-connector` 是可选依赖。普通的 `pip install semantica` 不会把它装进来，`import semantica.ingest` 也不会急切加载它——只有在你第一次使用 `RedshiftConnector` 或 `RedshiftIngestor` 时才会导入该 SDK。

<Note>
此连接器通过 Redshift 数据库传输协议做只读摄取。COPY、UNLOAD、S3 集成、Spectrum 外部表以及 Redshift Data API 都不在本次集成的范围内。
</Note>


## 基本用法

```python
from semantica.ingest import RedshiftIngestor
import os

ingestor = RedshiftIngestor(
    host=os.getenv("REDSHIFT_HOST"),
    database=os.getenv("REDSHIFT_DATABASE"),
    user=os.getenv("REDSHIFT_USER"),
    password=os.getenv("REDSHIFT_PASSWORD"),
)

data = ingestor.ingest_table("customers")
print(f"Retrieved {data.row_count} rows — columns: {data.columns}")
```

<Tip>
用环境变量（或配合 `python-dotenv` 的 `.env` 文件）把凭据挡在源代码之外。不带参数的 `RedshiftIngestor()` 会自动读取 `REDSHIFT_*` 环境变量。
</Tip>


## 认证

<Tabs>
  <Tab title="密码 / 原生">
    标准 Redshift 数据库用户名加密码：

    ```python
    import os
    from semantica.ingest import RedshiftIngestor

    ingestor = RedshiftIngestor(
        host=os.getenv("REDSHIFT_HOST"),       # e.g. cluster.abc.us-east-1.redshift.amazonaws.com
        database=os.getenv("REDSHIFT_DATABASE"),
        user=os.getenv("REDSHIFT_USER"),
        password=os.getenv("REDSHIFT_PASSWORD"),
        port=5439,    # default; omit to use the default
        ssl=True,     # default
    )
    ```

    所需环境变量：

    ```bash
    export REDSHIFT_HOST="cluster.abc.us-east-1.redshift.amazonaws.com"
    export REDSHIFT_DATABASE="dev"
    export REDSHIFT_USER="awsuser"
    export REDSHIFT_PASSWORD="your-password"
    ```
  </Tab>
  <Tab title="IAM 角色（AWS 推荐）">
    设 `iam=True` 即可通过 `GetClusterCredentials` 获取临时凭证。连接器把凭证解析完全交给 `redshift-connector` / boto3——Semantica 从不直接调用 AWS API。

    **基于配置文件**(读取 `~/.aws/credentials`)：

    ```python
    import os
    from semantica.ingest import RedshiftIngestor

    ingestor = RedshiftIngestor(
        host=os.getenv("REDSHIFT_HOST"),
        database=os.getenv("REDSHIFT_DATABASE"),
        iam=True,
        db_user=os.getenv("REDSHIFT_DB_USER"),
        cluster_identifier=os.getenv("REDSHIFT_CLUSTER_IDENTIFIER"),
        profile="default",   # AWS credentials-file profile
    )
    ```

    **显式 AWS 凭证**(例如用于 CI/CD，或持有短期密钥的 IAM 角色)：

    ```python
    ingestor = RedshiftIngestor(
        host=os.getenv("REDSHIFT_HOST"),
        database=os.getenv("REDSHIFT_DATABASE"),
        iam=True,
        db_user=os.getenv("REDSHIFT_DB_USER"),
        cluster_identifier=os.getenv("REDSHIFT_CLUSTER_IDENTIFIER"),
        region=os.getenv("REDSHIFT_REGION"),
        access_key_id=os.getenv("REDSHIFT_ACCESS_KEY_ID"),
        secret_access_key=os.getenv("REDSHIFT_SECRET_ACCESS_KEY"),
        session_token=os.getenv("REDSHIFT_SESSION_TOKEN"),  # only for temporary creds
    )
    ```

    `profile` 与显式密钥都未提供时，`redshift-connector` 会回落到标准 AWS 凭证链：`AWS_*` 环境变量、实例配置文件元数据等。

    IAM 模式必需：`host`、`database`、`db_user`、`cluster_identifier`。若能从凭证链或集群端点推断出 `region`，则该参数可省略。
  </Tab>
</Tabs>


## 环境变量

所有构造参数都有 `REDSHIFT_*` 环境变量兜底；显式传入的构造参数始终优先。

| 环境变量 | 参数 | 默认值 |
|---|---|---|
| `REDSHIFT_HOST` | `host` | — |
| `REDSHIFT_DATABASE` | `database` | — |
| `REDSHIFT_USER` | `user` | — |
| `REDSHIFT_PASSWORD` | `password` | — |
| `REDSHIFT_PORT` | `port` | `5439` |
| `REDSHIFT_SCHEMA` | `schema` | `"public"` |
| `REDSHIFT_DB_USER` | `db_user` | — |
| `REDSHIFT_CLUSTER_IDENTIFIER` | `cluster_identifier` | — |
| `REDSHIFT_REGION` | `region` | — |
| `REDSHIFT_PROFILE` | `profile` | — |
| `REDSHIFT_ACCESS_KEY_ID` | `access_key_id` | — |
| `REDSHIFT_SECRET_ACCESS_KEY` | `secret_access_key` | — |
| `REDSHIFT_SESSION_TOKEN` | `session_token` | — |


## 查询

### 摄取一张表

```python
data = ingestor.ingest_table("orders")
print(f"{data.row_count} rows, columns: {data.columns}")
```

### Schema、过滤与分页

```python
data = ingestor.ingest_table(
    "orders",
    schema="sales",          # defaults to the ingestor's schema attribute ("public")
    database="analytics",    # defaults to the connector's database
    where="status = 'shipped' AND total > 100",
    order_by="created_at DESC",
    limit=5000,
    offset=0,
)
```

<Warning>
`where` 与 `order_by` 接受原始 SQL 片段，必须来自可信的、由运维方控制的输入。不要把最终用户的原始字符串传进来。二者会对照一份阻止列表做校验，拒绝语句分隔符、`UNION`、DML/DDL 关键字以及基于时间的注入模式——但这不是完整的解析器。
</Warning>

### 自定义 SQL

```python
data = ingestor.ingest_query("""
    SELECT customer_id, SUM(total) AS lifetime_value
    FROM sales.orders
    WHERE status = 'completed'
    GROUP BY customer_id
    ORDER BY lifetime_value DESC
    LIMIT 1000
""")
print(f"{data.row_count} rows")
```

### 参数化查询

使用 `%s` 占位符（DB-API 2.0 的 `format` 参数风格，也是 `redshift-connector` 的默认风格）：

```python
data = ingestor.ingest_query(
    "SELECT id, name FROM users WHERE region = %s AND active = %s",
    params=("us-east-1", True),
)
```

### 大结果集的分批抓取

用 `batch_size` 控制驱动一次抓取的行数——行数据按该大小分块从服务器拉回，而不是一次性全部取回，且每块都会在请求下一块之前立即完成转换：

```python
data = ingestor.ingest_query(
    "SELECT * FROM large_events_table",
    batch_size=10000,
)
```

`batch_size` 决定驱动每次往返从 Redshift 读取多少行。返回的 `RedshiftData.data` 列表仍然包含全部匹配行；若要限制结果总量，请直接在查询里使用 `LIMIT`/`OFFSET`。


## Schema 探查

### 列出某个 Schema 下的基表

```python
tables = ingestor.list_tables(schema="public")
print(tables)  # ["customers", "orders", "products", ...]
```

视图不包含在内，只返回基表。

### 查看列元数据

```python
schema = ingestor.get_table_schema("customers", schema="public")

for col in schema["columns"]:
    print(f"{col['name']}: {col['type']} (nullable={col['nullable']})")

print("Primary keys:", schema["primary_keys"])
```

每个列字典包含：

| 键 | 类型 | 说明 |
|---|---|---|
| `name` | `str` | 列名 |
| `type` | `str` | Redshift 数据类型（如 `"integer"`、`"character varying"`） |
| `nullable` | `bool` | 该列是否接受 `NULL` |

`primary_keys` 是列名字符串组成的列表（未定义主键时为空列表）。


## 导出为 Semantica 文档

把摄取到的行转换成 `GraphBuilder` 消费的文档格式：

```python
documents = ingestor.export_as_documents(
    data,
    id_field="customer_id",        # column used as document ID; defaults to "id"
    text_fields=["name", "notes"], # columns joined as document text; omit to auto-select
)

print(f"Created {len(documents)} documents")
# Each document:
# {
#   "id": "12345",
#   "text": "Alice Acme customer notes here",
#   "metadata": {
#     "source": "redshift",
#     "table": "customers",
#     "database": "analytics",
#     "schema": "public",
#     "row_data": { ... full cleaned row ... }
#   }
# }
```

**ID 解析**：`str(row.get(id_field, row_index))`——当 `id_field` 列缺失时，用整数行号作为确定性的兜底值。

**提供 `text_fields` 时的文本**：每个非 `None` 的字段值转为字符串，再用单个空格拼接。

**`text_fields=None` 时的文本**：只拼接取值本身就是 `str` 类型的列；整数、浮点、布尔与 `None` 值一律排除——与 Snowflake、Databricks 连接器的行为一致。

把文档直接交给 `GraphBuilder`：

```python
from semantica.kg import GraphBuilder

builder = GraphBuilder()
graph = builder.build(documents)
print(f"Entities: {graph['metadata']['num_entities']}")
```


## 上下文管理器

需要执行多条查询的作业建议用上下文管理器：进入时建立一条连接、退出时关闭，`with` 块内的每次调用都复用同一个已认证的会话：

```python
with RedshiftIngestor(
    host=os.getenv("REDSHIFT_HOST"),
    database=os.getenv("REDSHIFT_DATABASE"),
    user=os.getenv("REDSHIFT_USER"),
    password=os.getenv("REDSHIFT_PASSWORD"),
) as ingestor:
    customers = ingestor.ingest_table("customers", limit=50000)
    orders    = ingestor.ingest_table("orders",    limit=50000)
    schema    = ingestor.get_table_schema("customers")
    tables    = ingestor.list_tables()
# Connection closed automatically on exit, even if an exception is raised.
```

不用 `with` 的独立调用，每次都会新建再关闭一条临时连接。


## 连接测试

```python
from semantica.ingest import RedshiftConnector

connector = RedshiftConnector(
    host="cluster.abc.us-east-1.redshift.amazonaws.com",
    database="dev",
    user="awsuser",
    password="your-password",
)
if connector.test_connection():
    print("Connection OK")
else:
    print("Connection failed — check host, credentials, and network access")
```


## 延伸阅读

- [摄取模块](../reference/ingest.md) — `RedshiftIngestor` 及所有其他摄取器的完整参考。
- [Snowflake 集成](./snowflake.md) — SQL 数据仓库连接器，表/查询摄取方式类似。
- [Databricks 集成](./databricks.md) — Delta Lake / Unity Catalog 连接器。
- [流水线](../reference/pipeline.md) — 把 Redshift 摄取用作流水线步骤。
- [安装](../installation.md) — 全部可选依赖 extras。
- [知识图谱](../reference/kg.md) — 用摄取来的 Redshift 数据构建知识图谱。
