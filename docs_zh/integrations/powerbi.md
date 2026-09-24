---
title: Power BI 集成
description: 通过 Power BI REST API 摄取工作区、数据集、报表与数据流的元数据，接入 Semantica 知识图谱流水线。
source: integrations/powerbi.md
source_version: 813d7d72fa130c9e06af08a5e2f5ff425b550c7e
icon: "chart-simple"
---

> 使用 REST API 与 Azure AD OAuth2 客户端凭据(client-credentials)认证，把 Power BI 的元数据拉进 Semantica。


## 安装

```bash
pip install semantica
```

`requests` 是 Semantica 的核心依赖，随包自带，因此这个连接器装好即用，无需再装任何东西。该模块采用惰性导出：在你第一次用到 `PowerBIIngestor` 之前，`import semantica.ingest` 不会真正加载它。

<Note>
此连接器读取的是**元数据**——工作区、数据集、报表与数据流。它不会执行 DAX 查询，也不会导出数据集的行数据；Power BI REST API 暴露的是目录信息，而不是表数据。
</Note>


## 基本用法

```python
import os
from semantica.ingest import PowerBIIngestor

ingestor = PowerBIIngestor(
    tenant_id=os.getenv("POWERBI_TENANT_ID"),
    client_id=os.getenv("POWERBI_CLIENT_ID"),
    client_secret=os.getenv("POWERBI_CLIENT_SECRET"),
)

data = ingestor.ingest_workspace_metadata()
documents = ingestor.export_as_documents(data)

print(f"{len(documents)} documents — {data.metadata['dataset_count']} dataset(s)")
```

<Tip>
用环境变量（或配合 `python-dotenv` 的 `.env` 文件）把凭据挡在源代码之外。不带参数的 `PowerBIIngestor()` 会自动读取 `POWERBI_*` 环境变量。
</Tip>


## 认证

连接器采用 Azure AD OAuth2 的**客户端凭据**模式。先在 Azure AD 注册一个应用程序，授予它访问 Power BI 服务的权限，再提供它的租户 ID、客户端 ID 和客户端密钥。

所需配置：

| 配置项 | 参数 | 环境变量 |
| --- | --- | --- |
| Azure AD 租户 ID | `tenant_id` | `POWERBI_TENANT_ID` |
| 应用程序(客户端) ID | `client_id` | `POWERBI_CLIENT_ID` |
| 客户端密钥 | `client_secret` | `POWERBI_CLIENT_SECRET` |
| 工作区/组 ID（可选） | `workspace_id` | `POWERBI_WORKSPACE_ID` |

前三项缺少任何一项，都会在发出任何网络请求之前抛出 `ValidationError`。令牌会自动缓存，并在临近过期时自动刷新。客户端密钥绝不会写入日志。


## 限定单个工作区

传入工作区(组)ID 即可只读取一个工作区；省略它则会遍历该服务主体可见的每一个工作区，收集其中的数据集、报表与数据流，并给每条记录打上来源 `workspace_id` 标签。这个逐工作区遍历是有意为之：不带范围的 `myorg` 端点只覆盖“我的工作区”，而且数据流根本没有不带范围的端点。

```python
data = ingestor.ingest_workspace_metadata(workspace_id="00000000-0000-0000-0000-000000000000")
```

用 `include` 只挑出你需要的资源（空列表什么都取不到）：

```python
data = ingestor.ingest_workspace_metadata(include=["datasets", "reports"])
```


## 文档输出

`export_as_documents` 返回标准的 `{"id", "text", "metadata"}` 结构，因此输出可以直接喂给 `GraphBuilder`：

```python
from semantica.kg import GraphBuilder

documents = ingestor.export_as_documents(data)
graph = GraphBuilder().build(documents)
```

每篇文档的 `metadata` 都带有 `source: "powerbi"`、取值为 `workspace`、`dataset`、`report` 或 `dataflow` 的 `resource_type`，外加原始 API 字段。


## 安全

每一次出站 HTTP 调用——包括请求令牌在内——都会经过 Semantica 的共享 SSRF(服务端请求伪造)防护，用户提供的端点因此无法触达私有、回环或链路本地地址段。只有确实需要的自托管部署才设置 `allow_private_ips=True`。
