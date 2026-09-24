---
title: Salesforce 集成
description: 将 Salesforce sObject 与 SOQL 查询中的 CRM 记录摄取进 Semantica 知识图谱流水线。
source: integrations/salesforce.md
source_version: 4a27e1cbb644f3f97db0db5878c81926e86ad9d3
icon: "cloud"
---

> 通过用户名/密码/安全令牌、JWT Bearer 或基于会话的认证，把 Salesforce 的客户(Account)、联系人(Contact)、商机(Opportunity)与自定义对象抽取进 Semantica。


## 安装

```bash
# Install with Salesforce support
pip install "semantica[db-salesforce]"

# Or install the connector separately
pip install simple-salesforce>=1.12.0
```


## 基本用法

```python
from semantica.ingest import SalesforceIngestor
import os

ingestor = SalesforceIngestor(
    username=os.getenv("SALESFORCE_USERNAME"),
    password=os.getenv("SALESFORCE_PASSWORD"),
    security_token=os.getenv("SALESFORCE_SECURITY_TOKEN"),
    domain=os.getenv("SALESFORCE_DOMAIN", "login"),   # "test" for sandbox
)

data = ingestor.ingest_sobject("Account", fields=["Id", "Name", "Industry"], limit=1000)
print(f"Retrieved {data.row_count} of {data.total_size} matching records")
print(f"Columns: {data.columns}")
```

<Tip>
用环境变量（或配合 `python-dotenv` 的 `.env` 文件）把凭据挡在源代码之外。不带参数的 `SalesforceIngestor()` 会自动读取 `SALESFORCE_*` 环境变量。
</Tip>


## 认证方式

<Tabs>
  <Tab title="用户名 / 密码 / 安全令牌">
    ```python
    import os
    from semantica.ingest import SalesforceIngestor

    ingestor = SalesforceIngestor(
        username=os.getenv("SALESFORCE_USERNAME"),
        password=os.getenv("SALESFORCE_PASSWORD"),
        security_token=os.getenv("SALESFORCE_SECURITY_TOKEN"),
        domain="login",   # production; use "test" for sandbox
    )
    ```
    运行前先设置所需的环境变量：
    ```bash
    export SALESFORCE_USERNAME="your-username@example.com"
    export SALESFORCE_PASSWORD="your-password"
    export SALESFORCE_SECURITY_TOKEN="your-security-token"
    ```
    标准的服务端流程。Salesforce SOAP 登录时，安全令牌会拼接在密码后面。可在 **Settings → My Personal Information → Reset My Security Token** 下生成或重置令牌。
  </Tab>
  <Tab title="JWT Bearer（CI/CD 推荐）">
    ```python
    import os
    from semantica.ingest import SalesforceIngestor

    ingestor = SalesforceIngestor(
        username=os.getenv("SALESFORCE_USERNAME"),
        consumer_key=os.getenv("SALESFORCE_CONSUMER_KEY"),
        privatekey_file=os.getenv("SALESFORCE_PRIVATE_KEY_FILE"),
        domain="login",   # or "test" for sandbox
    )
    ```
    ```bash
    export SALESFORCE_USERNAME="your-username@example.com"
    export SALESFORCE_CONSUMER_KEY="your-connected-app-consumer-key"
    export SALESFORCE_PRIVATE_KEY_FILE="/path/to/server.key"
    ```
    JWT Bearer 流程用签名的令牌完成认证——不传输密码，非常适合服务器到服务器集成与 CI/CD 流水线。前提是配置了一个启用 **Use digital signatures** 的 Salesforce 连接应用程序，并在 **Manage → Profiles / Permission Sets** 下列出预授权用户。

    如果想以字符串而不是文件路径的方式传入密钥材料，可用 `SALESFORCE_PRIVATE_KEY`(PEM 内容)代替 `SALESFORCE_PRIVATE_KEY_FILE`。
  </Tab>
  <Tab title="Session ID + 实例 URL">
    ```python
    ingestor = SalesforceIngestor(
        session_id=os.getenv("SALESFORCE_SESSION_ID"),
        instance_url=os.getenv("SALESFORCE_INSTANCE_URL"),
    )
    ```
    当你的环境已经统一管理 OAuth 令牌生命周期时（例如连接应用程序通过 web-server 或 device flow 获取令牌），就用这种方式。把访问令牌作为 `session_id`，把完整的实例 URL(如 `https://myorg.my.salesforce.com`)作为 `instance_url` 传入。
  </Tab>
  <Tab title="沙盒">
    ```python
    import os
    from semantica.ingest import SalesforceIngestor

    ingestor = SalesforceIngestor(
        username=os.getenv("SALESFORCE_USERNAME"),
        password=os.getenv("SALESFORCE_PASSWORD"),
        security_token=os.getenv("SALESFORCE_SECURITY_TOKEN"),
        domain="test",   # routes to test.salesforce.com
    )
    ```
    ```bash
    export SALESFORCE_USERNAME="your-sandbox-username@example.com.sandbox"
    export SALESFORCE_PASSWORD="your-password"
    export SALESFORCE_SECURITY_TOKEN="your-security-token"
    export SALESFORCE_DOMAIN="test"
    ```
    把 `domain="login"` 换成 `domain="test"`（或在环境里设 `SALESFORCE_DOMAIN=test`），即可连接开发者沙盒或完整沙盒。
  </Tab>
</Tabs>

### 环境变量

所有构造参数都有对应的环境变量兜底：

| 环境变量 | 参数 | 默认值 |
|---|---|---|
| `SALESFORCE_USERNAME` | `username` | — |
| `SALESFORCE_PASSWORD` | `password` | — |
| `SALESFORCE_SECURITY_TOKEN` | `security_token` | — |
| `SALESFORCE_DOMAIN` | `domain` | `"login"` |
| `SALESFORCE_INSTANCE_URL` | `instance_url` | — |
| `SALESFORCE_SESSION_ID` | `session_id` | — |
| `SALESFORCE_CONSUMER_KEY` | `consumer_key` | — |
| `SALESFORCE_PRIVATE_KEY_FILE` | `privatekey_file` | — |
| `SALESFORCE_PRIVATE_KEY` | `privatekey` | — |
| `SALESFORCE_API_VERSION` | `api_version` | 库默认值（`59.0`） |


## 对象摄取

### 摄取标准对象

```python
data = ingestor.ingest_sobject(
    "Account",
    fields=["Id", "Name", "Industry", "AnnualRevenue", "BillingCity"],
    where="Type = 'Customer' AND AnnualRevenue > 1000000",
    order_by="Name ASC",
    limit=5000,
)
print(f"Retrieved {data.row_count} of {data.total_size} matching records")
```

<Note>
`data.row_count` 是 `data.data` 里的记录数（即应用 `limit` 之后实际返回的内容）。`data.total_size` 对应 Salesforce 的 `totalSize`——查询匹配到的记录总数，也就是 `limit` 生效之前的数量。对比两者即可知道结果是否取全。
</Note>

### 摄取自定义对象

自定义对象的 API 名称以 `__c` 结尾：

```python
data = ingestor.ingest_sobject(
    "My_Custom_Object__c",
    fields=["Id", "Name", "Custom_Field__c"],
)
```

也支持关系穿越字段（如 `Owner.Name`）：

```python
data = ingestor.ingest_sobject(
    "Contact",
    fields=["Id", "Name", "Email", "Account.Name", "Owner.Name"],
    limit=10000,
)
```

### 让 Semantica 自选字段

省略 `fields` 时，会通过 `describe()` 拉取全部可选字段（多花一次 API 调用）。复合地址与地理位置字段（`type=address`、`type=location`）会被自动排除——需要的话请单独选取它们的组成字段（`BillingStreet`、`BillingCity`、`Location__Latitude__s` 等）。

```python
data = ingestor.ingest_sobject("Opportunity")
```


## 原始 SOQL 摄取

传入任意合法的 SOQL 查询，原样执行——分页自动处理：

```python
data = ingestor.ingest_query("""
    SELECT Id, Name, StageName, Amount, CloseDate,
           Account.Name, Owner.Name
    FROM Opportunity
    WHERE IsClosed = false
    ORDER BY CloseDate ASC
""")
print(f"Open opportunities: {data.row_count}")
```

查询会原样传给 Salesforce REST API，SOQL 的正确性与安全性由调用方负责。

<Warning>
`ingest_query` 不对 SOQL 字符串做任何校验或清洗。当查询由应用程序控制的输入拼装而成时，请改用 `ingest_sobject`（它会校验 sObject 名称、字段名以及 WHERE/ORDER BY 片段）。
</Warning>


## 文档导出

把摄取到的记录转换成 Semantica 文档格式，供 `GraphBuilder` 使用：

```python
documents = ingestor.export_as_documents(
    data,
    id_field="Id",                            # default; Salesforce 18-char record Id
    text_fields=["Name", "Description"],      # omit to join all string fields
)

print(f"Created {len(documents)} documents")
# Each document:
# {
#   "id": "001xx000003GYk2AAG",
#   "text": "Acme Corp Enterprise software company",
#   "metadata": {
#     "source": "salesforce",
#     "sobject": "Account",
#     "instance_url": "https://myorg.my.salesforce.com",
#     "row_data": { ... full cleaned record ... }
#   }
# }
```

把文档直接喂给 `GraphBuilder`：

```python
from semantica.kg import GraphBuilder

builder = GraphBuilder()
kg = builder.build(documents)
```


## 对象与 Schema 探查

```python
# List all accessible sObjects
sobject_names = ingestor.list_sobjects()
print(sobject_names[:10])   # ["Account", "Case", "Contact", ...]

# Inspect fields for a specific sObject
schema = ingestor.get_sobject_schema("Account")
for field in schema["fields"]:
    print(f"{field['name']}: {field['type']} (nillable={field['nillable']})")
```


## 上下文管理器

长时间运行的作业建议用上下文管理器：进入时建立一条连接、退出时关闭，`with` 块内的每次摄取调用都复用同一个已认证的会话：

```python
with SalesforceIngestor(
    username=os.getenv("SALESFORCE_USERNAME"),
    password=os.getenv("SALESFORCE_PASSWORD"),
    security_token=os.getenv("SALESFORCE_SECURITY_TOKEN"),
) as sf:
    accounts = sf.ingest_sobject("Account", limit=10000)
    contacts = sf.ingest_sobject("Contact", limit=10000)
    sobjects = sf.list_sobjects()
```


## 便捷函数

一行式摄取可用 `ingest_salesforce()`：

```python
from semantica.ingest import ingest_salesforce

# Fetch records
data = ingest_salesforce(
    method="sobject",
    sobject_name="Account",
    fields=["Id", "Name", "Industry"],
    limit=500,
)

# Execute raw SOQL (credentials from environment variables)
data = ingest_salesforce(
    method="query",
    soql="SELECT Id, Name FROM Contact WHERE IsActive = true",
)

# Ingest + export to documents in one step
docs = ingest_salesforce(
    method="documents",
    sobject_name="Account",
    text_fields=["Name", "Description"],
    limit=1000,
)

# List accessible sObjects
sobject_names = ingest_salesforce(method="list_sobjects")
```

或者使用统一的 `ingest()` 分发器：

```python
from semantica.ingest import ingest

result = ingest(
    None,
    source_type="salesforce",
    method="sobject",
    sobject_name="Account",
    fields=["Id", "Name"],
    limit=500,
)
data = result["data"]   # SalesforceData
```


## 故障排查

```python
import os
from semantica.ingest import SalesforceConnector

connector = SalesforceConnector(
    username=os.getenv("SALESFORCE_USERNAME"),
    password=os.getenv("SALESFORCE_PASSWORD"),
    security_token=os.getenv("SALESFORCE_SECURITY_TOKEN"),
)
if not connector.test_connection():
    print("Connection failed: check username, password, security token, and domain")
```

认证失败的常见原因：

- **域名不对**：生产组织用 `domain="login"`，沙盒用 `domain="test"`。
- **安全令牌失效**：在 **Settings → Reset My Security Token** 下重置，新令牌会通过邮件发给你。
- **IP 限制**：组织的可信 IP 段可能拦截了来源 IP。检查 **Setup → Network Access**。
- **API 访问未启用**：确认所用 profile 具有 **API Enabled** 权限。


## 延伸阅读

- [摄取模块](../reference/ingest.md) — `SalesforceIngestor` 完整 API 与所有其他摄取器。
- [Snowflake 集成](./snowflake.md) — 设计类似的关系型数仓连接器。
- [Databricks 集成](./databricks.md) — Lakehouse 连接器。
- [安装](../installation.md) — 全部可选依赖 extras。
- [知识图谱](../reference/kg.md) — 用摄取来的 Salesforce 数据构建知识图谱。
