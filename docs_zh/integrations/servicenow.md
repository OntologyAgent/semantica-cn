---
title: ServiceNow 集成
description: 通过 Table API 把 CMDB 配置项、事件、变更以及任意 ServiceNow 表摄取进 Semantica 知识图谱流水线。
source: integrations/servicenow.md
source_version: 679bf8abbb90baadb26da25e7679c837dc00363d
icon: "server"
---

> 通过 Table API，以 Basic 或 OAuth2 认证把 ServiceNow 表记录拉取进 Semantica。


## 安装

```bash
pip install "semantica[ingest-servicenow]"
```

这个连接器只需要 `requests`，而 `requests` 已随 Semantica 核心一起安装，所以这个 extra 目前装了也不会多装任何包；保留它只是为了让依赖声明显式化。该模块是懒导出的：`import semantica.ingest` 不会立刻加载它，直到你第一次用到 `ServiceNowIngestor` 才会真正导入。


## 基本用法

```python
import os
from semantica.ingest import ServiceNowIngestor

ingestor = ServiceNowIngestor(
    instance_url=os.getenv("SERVICENOW_INSTANCE_URL"),
    username=os.getenv("SERVICENOW_USERNAME"),
    password=os.getenv("SERVICENOW_PASSWORD"),
)

data = ingestor.ingest_table("cmdb_ci_server", query="operational_status=1")
documents = ingestor.export_as_documents(data)

print(f"{data.count} record(s) from {data.table}")
```

<Tip>
用环境变量（或配合 `python-dotenv` 的 `.env` 文件）把凭据挡在源代码之外。不带参数的 `ServiceNowIngestor()` 会自动读取 `SERVICENOW_*` 环境变量。
</Tip>


## 认证方式

| 配置项 | 参数 | 环境变量 |
| --- | --- | --- |
| 实例 URL（`https://<instance>.service-now.com`） | `instance_url` | `SERVICENOW_INSTANCE_URL` |
| 认证方式（`basic` 或 `oauth2`，可选） | `auth` | `SERVICENOW_AUTH` |
| 用户名 | `username` | `SERVICENOW_USERNAME` |
| 密码 | `password` | `SERVICENOW_PASSWORD` |
| OAuth2 客户端 ID | `client_id` | `SERVICENOW_CLIENT_ID` |
| OAuth2 客户端密钥 | `client_secret` | `SERVICENOW_CLIENT_SECRET` |

- **Basic**：只设置 `username`/`password` 时的默认方式。
- **OAuth2**：设置了 `client_id` 时自动选用。若同时提供 `username`/`password`，会以 `password` 授权模式从 `<instance_url>/oauth_token.do` 获取令牌；否则使用 `client_credentials` 模式。

配置缺失时，连接器会在发起任何网络请求之前抛出 `ValidationError`。


## 查询表

`ingest_table` 的参数与 Table API 的查询参数一一对应：

```python
data = ingestor.ingest_table(
    "incident",
    query="active=true^priority=1",       # sysparm_query (encoded query)
    fields=["sys_id", "number", "short_description", "cmdb_ci"],
    limit=500,                            # stop after 500 rows
    batch_size=200,                       # sysparm_limit per request
    display_value="all",                  # raw + display values per field
)
```

分页基于偏移量（`sysparm_limit` / `sysparm_offset`），连接器会一直翻页，直到取完整张表或攒够 `limit` 行。引用字段的 `link` 对象默认丢弃（对应 `sysparm_exclude_reference_link=true`）；想保留它们，传入 `exclude_reference_link=False`。

CMDB 配置项之间的关系存放在 `cmdb_rel_ci` 表中：

```python
rels = ingestor.ingest_table("cmdb_rel_ci", fields=["parent", "child", "type"])
```


## 文档输出

`export_as_documents` 把每条记录压平成一个字典，包含 `id`（记录的 `sys_id`）、`name`（依次从 `name`、`number` 或 `short_description` 解析得出）、`source`（实例 URL）与 `table`，外加 API 返回的全部字段，因此输出可以直接喂给 `GraphBuilder`：

```python
from semantica.kg import GraphBuilder

documents = ingestor.export_as_documents(data)
graph = GraphBuilder().build(documents)
```


## 安全

每一个对外发出的 HTTP 请求——包括 OAuth2 令牌请求——都要经过 Semantica 统一的服务端请求伪造(SSRF)防护，因此用户提供的实例 URL 无法触达私有、回环或链路本地地址段。只对确实有此需要的自托管部署设置 `allow_private_ips=True`。
