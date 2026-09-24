---
title: Apache Airflow 集成
description: 把 Apache Airflow 的 DAG、任务与依赖元数据摄取进 Semantica。
source: integrations/airflow.md
source_version: 9c58cd9438d6c3c52b3193b94127bb7f0349eacd
icon: 'wind'
---

> 通过稳定的 Airflow REST API 摄取 Apache Airflow 的 DAG(有向无环图)、任务与任务依赖，用于 Semantica 中的流水线与血缘(lineage)分析。

## 安装

```bash
pip install "semantica[ingest-airflow]"
```

## 基本用法

```python
from semantica.ingest import AirflowIngestor

ingestor = AirflowIngestor(
    base_url="https://airflow.example.com",
    token="your-access-token",
)

data = ingestor.ingest()
documents = ingestor.export_as_documents(data)

print(f"DAGs: {len(data.dags)}")
print(f"Tasks: {len(data.tasks)}")
print(f"Dependencies: {len(data.dependencies)}")

ingestor.close()
```

`base_url` 必须指向 Airflow webserver 的根地址。

不要在 `base_url` 里带上 `/api/v1`；连接器会自动补上稳定的 REST API 路径。

## 认证

### Bearer Token

```python
from semantica.ingest import AirflowIngestor

ingestor = AirflowIngestor(
    base_url="https://airflow.example.com",
    token="your-access-token",
)
```

### 用户名与密码

```python
from semantica.ingest import AirflowIngestor

ingestor = AirflowIngestor(
    base_url="https://airflow.example.com",
    username="airflow-user",
    password="your-password",
)
```

用户名和密码必须成对提供。

## 过滤 DAG

把摄取范围限制在指定的 DAG ID：

```python
data = ingestor.ingest(
    dag_ids=["daily_etl", "warehouse_sync"],
)
```

排除已暂停的 DAG：

```python
data = ingestor.ingest(
    include_paused=False,
)
```

两个选项可以同时使用：

```python
data = ingestor.ingest(
    dag_ids=["daily_etl", "warehouse_sync"],
    include_paused=False,
)
```

## 流水线血缘

连接器从每个 Airflow 任务的 `downstream_task_ids` 推导出任务级依赖。

举个例子：

```python
[
    {
        "dag_id": "daily_etl",
        "upstream_task_id": "extract",
        "downstream_task_id": "transform",
    },
    {
        "dag_id": "daily_etl",
        "upstream_task_id": "transform",
        "downstream_task_id": "load",
    },
]
```

重复的依赖边会自动去除。

## 导出文档

`export_as_documents()` 把摄取到的 Airflow 元数据转换成 GraphBuilder 友好的字典。

连接器导出三种文档类型：

- `airflow_dag`
- `airflow_task`
- `airflow_dependency`

生成的标识符采用如下形式：

```text
airflow:dag:<dag_id>
airflow:task:<dag_id>:<task_id>
airflow:dependency:<dag_id>:<upstream_task_id>:<downstream_task_id>
```

## 私有化部署的 Airflow

发往用户所提供 Airflow 端点的所有请求，都会经过 Semantica 的服务端请求伪造(SSRF)防护。

默认拦截私有 IP 地址。

如果 Airflow 部署在私有网络中且可信：

```python
from semantica.ingest import AirflowIngestor

ingestor = AirflowIngestor(
    base_url="http://10.0.0.20:8080",
    username="airflow-user",
    password="your-password",
    allow_private_ips=True,
)
```

只对你信任的端点启用 `allow_private_ips=True`。

## 分页

DAG 结果通过 Airflow 的 `limit` 与 `offset` 分页机制获取。

默认页大小为 100。

```python
data = ingestor.ingest(
    page_limit=100,
)
```

需要时可以传入其他正整数页大小。

## 错误处理

连接器针对常见失败抛出 Semantica 错误，包括：

- 连接配置缺失或无效
- Airflow API 请求失败
- JSON 响应无效
- API 响应结构不符合预期
- 分页 limit 参数无效

## API 覆盖范围

连接器目前使用以下稳定的 Airflow REST API 端点：

```text
GET /api/v1/dags
GET /api/v1/dags/{dag_id}/tasks
```

任务依赖从每个任务的 `downstream_task_ids` 推导得出。

## 只读行为

Airflow 连接器只执行元数据摄取。

它不会：

- 创建 DAG
- 修改 DAG
- 触发 DAG 运行
- 暂停或恢复 DAG
- 修改任务
- 删除 DAG 或任务

## 关闭连接

摄取完成后，关闭底层的 HTTP 会话：

```python
ingestor.close()
```
