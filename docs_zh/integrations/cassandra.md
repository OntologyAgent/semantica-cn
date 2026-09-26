---
title: Apache Cassandra 集成
description: 将 Apache Cassandra 表中的结构化数据摄取进 Semantica 知识图谱流水线。
source: integrations/cassandra.md
source_version: 83ceff1d7aee803c91ba6b9232c938ebcc2cbdfe
icon: "database"
---

> 使用官方 `cassandra-driver` 把 Apache Cassandra 表中的数据抽取进 Semantica。

## 安装

```bash
# Install with Cassandra support
pip install "semantica[db-cassandra]"

# Or install the connector separately
pip install "cassandra-driver>=3.29.0"
```

`cassandra-driver` 是可选依赖。直接 `pip install semantica` 不会把它装进来；Cassandra 连接器采用懒加载，首次使用时才真正导入。

## 基本用法

```python
import os
from semantica.ingest import CassandraIngestor

ingestor = CassandraIngestor(
    hosts=os.getenv("CASSANDRA_HOSTS", "127.0.0.1").split(","),
    port=int(os.getenv("CASSANDRA_PORT", "9042")),
    username=os.getenv("CASSANDRA_USERNAME"),
    password=os.getenv("CASSANDRA_PASSWORD"),
    keyspace=os.getenv("CASSANDRA_KEYSPACE"),
)

data = ingestor.ingest_table("users")

print(f"Retrieved {data.row_count} rows")
print(f"Columns: {data.columns}")
```

<Tip>
用环境变量把 Cassandra 凭据挡在源代码之外。
</Tip>

## 认证方式

对于启用了认证的 Cassandra 集群：

```python
from semantica.ingest import CassandraIngestor

ingestor = CassandraIngestor(
    hosts=["127.0.0.1"],
    port=9042,
    username="cassandra",
    password="your-password",
    keyspace="my_keyspace",
)
```

对于未启用认证的集群：

```python
from semantica.ingest import CassandraIngestor

ingestor = CassandraIngestor(
    hosts=["127.0.0.1"],
    port=9042,
    keyspace="my_keyspace",
)
```

## 查询

### 摄取一张表

```python
data = ingestor.ingest_table("orders")
print(f"{data.row_count} rows, columns: {data.columns}")
```

### 限制行数

```python
data = ingestor.ingest_table(
    "orders",
    limit=1000,
)
```

`limit` 参数最终会转换成 CQL 的 `LIMIT` 子句。

## 表结构探查

```python
schema = ingestor.get_table_schema("users")

for column in schema["columns"]:
    print(
        f"{column['name']}: "
        f"{column['type']} "
        f"(nullable={column['nullable']})"
    )

print("Primary keys:", schema["primary_keys"])
```

每个列条目是一个字典，包含以下键：

| 键 | 类型 | 说明 |
|---|---|---|
| `name` | `str` | 列名 |
| `type` | `str` | Cassandra CQL 类型 |
| `nullable` | `bool` | 该列是否可为空 |
| `primary_key` | `bool` | 该列是否属于主键 |
| `static` | `bool` | 该列是否为静态列 |

`primary_keys` 按 Cassandra 定义的顺序给出该表主键列的名称。

## 导出为 Semantica 文档

```python
documents = ingestor.export_as_documents(
    data,
    id_field="id",
    text_fields=["name", "city"],
)

print(f"Created {len(documents)} documents")
```

每个文档的结构如下：

```python
{
    "id": "123",
    "text": "Alice Delhi",
    "metadata": {
        "source": "cassandra",
        "keyspace": "my_keyspace",
        "table": "users",
        "row_data": {}
    }
}
```

**ID 解析**：配置的 `id_field` 统一转成字符串；该字段缺失时，改用行号作为确定性的兜底值。

**提供 `text_fields` 时的文本**：非 `None` 的值转成字符串，再用单个空格拼接。

**`text_fields=None` 时的文本**：只有字符串值会进入文档文本。

## 连接测试

```python
from semantica.ingest import CassandraConnector

connector = CassandraConnector(
    hosts=["127.0.0.1"],
    port=9042,
    keyspace="my_keyspace",
)

if connector.test_connection():
    print("Connection OK")
else:
    print("Connection failed")
```

## 延伸阅读

- [摄取模块](../reference/ingest.md)
- [Redshift 集成](./redshift.md)
- [Databricks 集成](./databricks.md)
- [安装](../installation.md)
- [知识图谱](../reference/kg.md)
