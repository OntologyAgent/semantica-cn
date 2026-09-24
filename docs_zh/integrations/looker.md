---
title: Looker 集成
description: 把 Looker 的 Look、Dashboard、LookML 模型、文件夹与项目元数据摄取到 Semantica 的知识图谱流水线。
source: integrations/looker.md
source_version: 64fbb504168f4c79d0df48b13d914c401d72f431
icon: "chart-line"
---

> 使用 API 客户端凭据与经过校验的实例端点，通过官方 `looker-sdk` 把 Looker 元数据提取到 Semantica。


## 安装

```bash
# Install with Looker support
pip install "semantica[ingest-looker]"

# Or install the connector separately
pip install looker-sdk>=24.0.0
```

`looker-sdk` 是可选依赖：普通的 `pip install semantica` 永远不会安装它，`import semantica.ingest` 也不会急切加载——只有在你第一次使用 `LookerConnector` 或 `LookerIngestor` 时才会导入该 SDK。`LookerData` 无需 SDK 即可导入，因此在没有 SDK 的环境中，类型标注和数据类照常可用。

<Note>
本连接器只摄取 Looker 元数据——Look、Dashboard、LookML 模型（含各自的 Explore）、文件夹(Folder)与项目(Project)。查询结果行、定时计划(Scheduled Plan)、用户和群组不在当前集成范围内。
</Note>


## 基本用法

```python
import os
from semantica.ingest import LookerIngestor

with LookerIngestor(
    base_url=os.getenv("LOOKERSDK_BASE_URL"),          # e.g. https://looker.example.com
    client_id=os.getenv("LOOKERSDK_CLIENT_ID"),
    client_secret=os.getenv("LOOKERSDK_CLIENT_SECRET"),
) as ingestor:
    looks = ingestor.ingest_looks()
    print(f"Retrieved {looks.row_count} looks — columns: {looks.columns}")

    documents = ingestor.export_as_documents(looks)
```

<Note>
`LookerIngestor` 进入 `with` 块时建立一条已鉴权会话，退出时关闭，因此块内的每次调用都复用这条经过校验的连接。不经过 `with` 的独立调用，每次都会建立并关闭一条临时连接。
</Note>

<Tip>
用环境变量（或配合 `python-dotenv` 的 `.env` 文件）保管凭据，避免写进源代码。不带任何参数的 `LookerIngestor()` 会自动读取 `LOOKERSDK_*` 环境变量。
</Tip>


## 鉴权

<Tabs>
  <Tab title="Client ID / Client Secret">
    Looker API 凭据是 Looker 为 API3 访问签发的 `client_id` 与 `client_secret` 组合（在 Admin → Users → API Keys 页面创建）。可以显式传入这两个值，也可以让连接器读取 `LOOKERSDK_CLIENT_ID` 和 `LOOKERSDK_CLIENT_SECRET` 环境变量：

    ```python
    import os
    from semantica.ingest import LookerIngestor

    ingestor = LookerIngestor(
        base_url=os.getenv("LOOKERSDK_BASE_URL"),   # must be https
        client_id=os.getenv("LOOKERSDK_CLIENT_ID"),
        client_secret=os.getenv("LOOKERSDK_CLIENT_SECRET"),
    )
    ```

    所需的环境变量：

    ```bash
    export LOOKERSDK_BASE_URL="https://looker.example.com"
    export LOOKERSDK_CLIENT_ID="your-client-id"
    export LOOKERSDK_CLIENT_SECRET="your-client-secret"
    ```

    端点必须使用 `https`。遇到非 `https` 协议（例如 `http://looker.internal`），连接器会在构造任何客户端之前抛出 `ValidationError`。
  </Tab>
  <Tab title="现有 looker.ini">
    连接器也接受 Looker SDK 配置文件：把 `config_file` 指向该文件，并可选地指定其中的 `section`：

    ```python
    from semantica.ingest import LookerIngestor

    ingestor = LookerIngestor(
        config_file="looker.ini",
        section="Looker",
    )
    ```

    `config_file` 默认取 `"looker.ini"`。只要对应的构造参数与环境变量都未提供，就采用文件中已有的值。
  </Tab>
</Tabs>

<Warning>
连接私有、回环(loopback)或链路本地(link-local)端点时需要设置 `allow_private_ips=True`；该选项同时放宽了 `https` 要求，允许非 `https` 协议。除非你明确要连内部实例，否则不要开启。
</Warning>

如果显式传入的 `base_url` 与 `LOOKERSDK_BASE_URL` 或配置文件中的值冲突，连接器会抛出 `ValidationError`，而不是连到一个你并未校验过的主机。


## 环境变量

所有连接参数都有 `LOOKERSDK_*` 环境变量回落值，经 SDK 自身的 `ApiSettings` 解析；显式传入的构造参数始终优先。

| 变量 | 参数 | 默认值 |
|---|---|---|
| `LOOKERSDK_BASE_URL` | `base_url` | — |
| `LOOKERSDK_CLIENT_ID` | `client_id` | — |
| `LOOKERSDK_CLIENT_SECRET` | `client_secret` | — |

`config_file` 与 `section` 是构造参数，而非环境变量：

| 参数 | 说明 | 默认值 |
|---|---|---|
| `config_file` | 现有 `looker.ini` 文件的路径 | `"looker.ini"` |
| `section` | `config_file` 中的节名 | — |
| `allow_private_ips` | 允许私有端点与非 `https` 协议 | `False` |


## 元数据摄取

每次读取都会返回一个 `LookerData` 对象，其中包含 `data`（规范化后的元数据字典）、`row_count`、`columns`、`content_type`、`base_url`、`metadata` 与 `ingested_at`。

| 方法 | SDK 读取 | `content_type` |
|---|---|---|
| `ingest_looks()` | `all_looks` | `"look"` |
| `ingest_dashboards()` | `all_dashboards` | `"dashboard"` |
| `ingest_lookml_models()` | `all_lookml_models` | `"lookml_model"` |
| `ingest_folders()` | `all_folders` | `"folder"` |
| `ingest_projects()` | `all_projects` | `"project"` |

读取操作使用 SDK 的 `all_*` 集合方法。每个方法都接受可选的关键字参数并原样转发给 SDK 调用——多数读取支持 `transport_options` 与 `fields`，`ingest_lookml_models()` 还额外支持 `limit`/`offset`：

```python
looks = ingestor.ingest_looks(fields="id,title,description,model")
models = ingestor.ingest_lookml_models(limit=100)
```

<Note>
这是仅针对元数据的连接器。Dashboard 以不带磁贴(tile)的 `DashboardBase` 记录读取，因此不会拉取或存储任何查询结果行。
</Note>

### LookML 模型与 Explore

返回的 LookML 模型把各自的 Explore 嵌套在父模型记录内。Explore 自身不携带父级引用，因此每个嵌套标识符里都拼入了父模型的 `project_name`/`name` 组合：

```python
models = ingestor.ingest_lookml_models()

for model in models.data:
    print(f"{model['project_name']}.{model['name']}")
    for explore in model["explores"]:
        print(f"  {explore['name']}")
```


## 导出为 Semantica 文档

`export_as_documents(data)` 把 `LookerData` 结果转换成 `GraphBuilder` 可直接消费的 `{"id", "text", "metadata"}` 文档结构：

```python
documents = ingestor.export_as_documents(looks)

print(f"Created {len(documents)} documents")
# Each document:
# {
#   "id": "looker:look:42",
#   "text": "Monthly Revenue Revenue by region orders jdoe",
#   "metadata": {
#     "source": "looker",
#     "content_type": "look",
#     "row_data": { ... allowlisted Look metadata ... },
#     "look_id": 42
#   }
# }
```

文档 `id` 按内容类型划分命名空间，跨集合保持唯一：`looker:look:<id>`、`looker:dashboard:<id>`、`looker:folder:<id>`、`looker:project:<id>`，模型则为 `looker:lookml_model:<project>.<name>`。每个文档的 `metadata["source"]` 均为 `"looker"`，`metadata["content_type"]` 记录该文档来自哪个集合。完整的规范化记录保存在 `metadata["row_data"]` 下。

LookML 模型文档还会进一步嵌套各自的 Explore，每个 Explore 都有自己的命名空间 id 与父模型引用：

```python
# {
#   "id": "looker:lookml_model:ecommerce.orders",
#   "text": "Orders orders ecommerce Order Items order_items",
#   "metadata": {
#     "source": "looker",
#     "content_type": "lookml_model",
#     "row_data": { ... allowlisted LookML model metadata ... },
#     "project_name": "ecommerce",
#     "model_name": "orders",
#     "explores": [
#       {
#         "id": "looker:lookml_model:ecommerce.orders:explore:order_items",
#         "name": "order_items",
#         "label": "Order Items",
#         "group_label": "Order Items",
#         "description": None,
#         "hidden": False,
#         "parent_model": "ecommerce.orders"
#       }
#     ],
#     "explore_count": 1
#   }
# }
```

把文档直接交给 `GraphBuilder`：

```python
from semantica.kg import GraphBuilder

builder = GraphBuilder()
graph = builder.build(documents)
print(f"Entities: {graph['metadata']['num_entities']}")
```

导出的文档均可 JSON 序列化：嵌套的 SDK 模型对象转为普通字典或列表，`datetime` 值转为 ISO 8601 字符串。


## 安全

连接器在构造任何客户端之前先校验用户提供的端点，然后把客户端绑定到这个已校验的 `base_url`——如果 SDK 从环境变量或配置文件解析出另一个主机，就会直接失败(fail closed)而拒绝连接。

每个出站请求都经过与本仓库其他连接器相同的服务端请求伪造(SSRF)校验：OAuth 登录和每次元数据读取都单独检查，而不是只在构造时检查一次。连接固定在校验阶段解析出的地址上，因此校验与实际拨号之间发生的 DNS 重绑定(DNS rebinding)无法把连接重定向走。除非显式开启 `allow_private_ips`，请求必须使用 `https`；TLS 证书校验强制开启（`LOOKERSDK_VERIFY_SSL` 或 `looker.ini` 都无法将其降级）；不跟随重定向；也不信任代理环境变量。SDK 的错误文档查询（它在收到非 2xx 响应时会额外发起一次无防护的 `requests.get`）已禁用，失败的请求因此无法打开第二条出网通道。

记录规范化会把每个 SDK 对象投影到一份显式的保留字段清单上。`Project.git_password`、`Project.deploy_secret`、`Dashboard.password`、`Dashboard.pdt_password`、`LookmlModel.device_token` 这类涉密字段一律丢弃；`Project.git_remote_url` 中任何 `user:password@` 用户信息均予以清除（无法安全改写的 URL 整体脱敏）。导出的文档不携带 `base_url` 或任何凭据。


## 延伸阅读

- [摄取模块](../reference/ingest.md) — `LookerIngestor` 与全部其他摄取器的完整参考。
- [Snowflake 集成](./snowflake.md) — 提供类似元数据摄取能力的 SQL 数据仓库连接器。
- [Redshift 集成](./redshift.md) — 支持表级与查询摄取的数据仓库连接器。
- [安装](../installation.md) — 全部可选依赖 extras。
- [知识图谱](../reference/kg.md) — 用摄取到的 Looker 元数据构建知识图谱。
