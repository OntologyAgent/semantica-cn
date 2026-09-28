---
title: 摄取任意数据源
description: 从文件、网站、Git 仓库、数据库、Kafka 流、RSS 订阅源等来源装载数据——统一的摄取 API。
source: guides/ingest.md
source_version: dda9c31ef652dedf2ff2b6cf20fce95ae46daf05
---

Semantica 的摄取(Ingestion)模块为每类来源都提供一个统一一致的函数调用。文件、网页和订阅源来源返回带 `.text` 属性的对象；API 与数据库来源返回结构化对象（`APIData.data`、`List[Dict]`），你需要先把它转换成文本再存储；Git 仓库来源返回带 `code_files` 和 `commits` 键的字典；流来源返回带 `.content` 字段的 `StreamMessage` 对象。它们都能干净地组装进同一个图谱摄取脚本——每种来源的确切访问模式见下文对应小节。

<Info>
  所有摄取函数都在 `semantica.ingest` 中。可选依赖采用懒加载——网页/订阅源摄取只需要 `pip install beautifulsoup4`，仓库摄取需要 `pip install gitpython`，Parquet 需要 `pip install pyarrow`。缺依赖时会抛出明确的 `ImportError`，指明具体缺哪个包。
</Info>

## 为什么摄取很重要

Semantica 要对数据做分析、检索、推理或关联，前提是先够得着数据。摄取就是这第一步——把内容从它所在的地方拉过来，转换成 `AgentContext` 能存储并建立索引的形式。

摄取完成后，内容会流向两处：一个用于语义检索的向量索引，以及一个可选的 `ContextGraph`（承载实体关系）。此后，每个下游模块——语义抽取(Semantic Extraction)、推理、GraphRAG、决策智能(Decision Intelligence)——处理的都是同一份统一数据，无论它最初来自 PDF、数据库行、API 响应还是实时流。

## 典型工作流

无论来源是什么类型，大多数摄取流水线都遵循同样的四步：

1. **连接来源** —— 携带连接信息调用相应的摄取函数。
2. **取回数据** —— 函数要么返回带文本的对象（文件、网页、订阅源），要么返回还需加工一步的结构化数据（API、数据库）。
3. **必要时做转换** —— 对结构化来源，把每条记录拼成纯文本字符串，`AgentContext.store()` 才能对其生成嵌入(Embedding)并建立索引。
4. **存入 AgentContext** —— 把字符串、字符串列表或字典列表传给 `context.store()`。可选开启实体与关系抽取，在同一时间填充 `ContextGraph`。

```python
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore

# AgentContext is the entry point for storage.
# ContextGraph is optional — attach it to build a searchable entity graph.
graph   = ContextGraph()
context = AgentContext(
    vector_store    = VectorStore(backend="faiss", dimension=768),
    knowledge_graph = graph,   # omit if you only need vector search
)

# store() accepts a string, a list of strings, or a list of dicts
context.store("A single observation or document text.")
context.store(["Doc one text.", "Doc two text."])
context.store([{"content": "Doc text.", "metadata": {"source": "wiki"}}])
```

## 何时使用摄取

当你的数据在 Semantica 之外、需要把它拿进来时，就用摄取模块：

- **文件与文档** —— 磁盘或云存储上的 PDF、Word 文档、CSV、JSON、XML 以及整个目录。
- **网页内容** —— 公开文档站、监管发布页、新闻订阅源，或任何你能爬取的 URL。
- **REST API** —— 内部平台（SIEM、EDR、ITSM、CRM）、威胁情报(Threat Intelligence)订阅源，或任何分页的 HTTP 端点。
- **数据库** —— 已有的 SQL 数据库，可用一条有针对性的查询取出相关记录。
- **企业数据平台** —— 已经落在 Databricks lakehouse（Unity Catalog + Delta Lake）或 Snowflake 仓库里的表，无需先导出成 CSV。
- **实时流** —— Kafka 或其他消息代理，需要在事件到达时即刻处理。
- **Git 仓库** —— 由版本控制管理的源码、文档或配置文件。

如果你的数据已经在内存里、就是一个 Python 字符串或字典，那就跳过摄取，直接调用 `context.store()`。

## 数据源 1 — PDF 供应商报告与内部文档

把文件路径或目录传给 `ingest_file()`，即可从 PDF 及其他文档格式中提取纯文本。它同样适用于供应商威胁报告、内部制度文档、产品手册，或磁盘上任何含文本的文件：

```python
from semantica.ingest import ingest_file

# Single file
report = ingest_file("apt29_q4_2024.pdf", method="file")
print(report.text[:500])       # extracted plain text
print(report.metadata)         # {"file_type": "pdf", "size": 1843200, ...}
print(report.name)             # "apt29_q4_2024.pdf"
print(report.file_type)        # "pdf"

# Whole directory at once — recursive by default
reports = ingest_file("./vendor_reports/", method="directory", recursive=True)
for r in reports:
    print(f"{r.name}: {len(r.text)} chars extracted")

# apt29_q4_2024.pdf:    42317 chars extracted
# lazarus_group_h2.pdf: 38901 chars extracted
# fin7_campaign.pdf:    51204 chars extracted
# cozy_bear_ttps.pdf:   29876 chars extracted
```

`ingest_file()` 返回一个 `FileObject`（单文件）或 `List[FileObject]`（目录）。`.text` 属性永远是解码后的字符串——你完全不用手动处理字节或编码。DOCX、XLSX、CSV、TXT、JSON 和 XML 文件走的是同一个调用；文件类型会根据扩展名和 MIME 类型自动识别。

同样的方法也适用于内部知识库。如果你的团队把运维手册、产品文档或面向客户的指南存成 PDF 或 Word 文档：

```python
from semantica.ingest import ingest_file
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore

graph   = ContextGraph(advanced_analytics=True)
context = AgentContext(
    vector_store    = VectorStore(backend="faiss"),
    knowledge_graph = graph,
)

# Internal documentation — same API as vendor reports
docs = ingest_file("./internal_docs/", method="directory", recursive=True)
doc_texts = [d.text for d in docs]
context.store(doc_texts, extract_entities=True)
```

如果供应商还会把报告丢进 S3 存储桶，可以切换到云端摄取，流水线其余部分原封不动：

```python
s3_reports = ingest_file(
    "s3://intel-vendor-bucket/weekly-reports/",
    method="cloud",
    provider="s3",
    aws_access_key_id="AKIA...",
    aws_secret_access_key="...",
)
# Returns List[FileObject] — same shape as the local directory call
```

## 数据源 2 — REST API

`RESTIngestor` 负责处理鉴权、重试逻辑和分页。与文件来源不同，REST API 返回的是结构化 JSON——`APIData.data` 是 `List[Dict]`，而不是文本字符串。在传给 `AgentContext.store()` 之前，你需要把每条记录组织成文本形式。

```python
from semantica.ingest import RESTIngestor

ingestor = RESTIngestor()

# Single paginated endpoint — returns APIData
# APIData.data is List[Dict] — one dict per record, not a .text string
api_data = ingestor.ingest_endpoint(
    "https://misp.internal/events/restSearch",
    headers={"Authorization": "YOUR_MISP_API_KEY"},
    params={"limit": 100, "page": 1, "threat_level_id": "1"},
)

# api_data.data is List[Dict] — one dict per event
events = api_data.data
print(f"Retrieved {len(events)} MISP events")
print(f"Endpoint: {api_data.endpoint}")
print(f"Status:   {api_data.response_status}")

# Convert to text blobs for the knowledge graph
event_texts = []
for event in events:
    attrs = ", ".join(
        a.get("value", "") for a in event.get("Event", {}).get("Attribute", [])
    )
    text = (
        f"MISP Event {event['Event']['id']}: "
        f"{event['Event'].get('info', '')} "
        f"[TLP: {event['Event'].get('distribution', '')}] "
        f"Attributes: {attrs[:300]}"
    )
    event_texts.append(text)
```

同样的模式适用于任何 REST API——工单系统、CRM 或内部服务目录。先取回结构化记录，再为每条记录拼出一两句能抓住关键事实的话，供检索和抽取使用。

对于跨多页返回成千上万条记录的端点，`paginated_fetch()` 会自动遍历所有页，每页返回一个 `APIData` 对象：

```python
all_events = ingestor.paginated_fetch(
    "https://misp.internal/events/restSearch",
    headers={"Authorization": "YOUR_MISP_API_KEY"},
    page_size=100,
)
# all_events is List[APIData] across all pages
total_events = sum(len(page.data) for page in all_events if isinstance(page.data, list))
print(f"Pages fetched: {len(all_events)}")
print(f"Total events fetched: {total_events}")
```

## 数据源 3 — SQL 数据库

`DBIngestor.execute_query()` 返回 `List[Dict]`——每行一个字典。和 REST API 一样，数据库结果是结构化数据，存入 `AgentContext` 前需要一步文本转换。查询要保持克制：只取真正需要的行和列，别把整张表倒进来。

即席 SQL 查询用 `DBIngestor.execute_query()`：

```python
from semantica.ingest import DBIngestor

db = DBIngestor()

# Returns List[Dict] — one dict per row
cves = db.execute_query(
    "postgresql://readonly:pass@cvedb.internal:5432/nvd",
    """
        SELECT
            cve_id,
            description,
            cvss_v3_score,
            affected_products,
            published_date,
            last_modified
        FROM cve_records
        WHERE cvss_v3_score >= 7.0
          AND published_date >= NOW() - INTERVAL '30 days'
        ORDER BY cvss_v3_score DESC
    """,
)

print(f"High-severity CVEs (last 30 days): {len(cves)}")

# Convert rows to text for the knowledge graph
cve_texts = [
    f"{r['cve_id']} (CVSS {r['cvss_v3_score']}): "
    f"{r['description']} "
    f"Affects: {r['affected_products']}"
    for r in cves
]
```

同一个 `DBIngestor.execute_query()` 模式也覆盖 MySQL、SQLite、Oracle 和 SQL Server——只需换连接字符串。写查询前想先摸清表结构：

```python
schema = db.execute_query(
    "postgresql://readonly:pass@cvedb.internal:5432/nvd",
    """
        SELECT table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position
    """,
)
for col in schema[:10]:
    print(f"{col['table_name']}.{col['column_name']} ({col['data_type']})")
```

表之间已有主键和外键时，也可以跳过文本转换，用 [`RelationalSchemaMapper`](../reference/kg.md#relationalschemamapper) 把行直接映射成实体和关系，再交给 `GraphBuilder`。这同样适用于 `SnowflakeIngestor`、`DatabricksIngestor` 和 `PandasIngestor` 的结果：

```python
from semantica.kg import GraphBuilder, RelationalSchemaMapper

conn = "postgresql://readonly:pass@cvedb.internal:5432/nvd"

mapper = RelationalSchemaMapper(
    entity_tables={
        "cve_records": {"pk": "cve_id", "type": "Vulnerability"},
        "products":    {"pk": "product_id", "type": "Product", "name": "product_name"},
    },
    foreign_keys=[
        # cve_products is a junction table: rows become Vulnerability -> Product edges
        {"table": "cve_products", "column": "cve_id",
         "references": ("cve_records", "cve_id")},
        {"table": "cve_products", "column": "product_id",
         "references": ("products", "product_id"), "predicate": "affects"},
    ],
)

mapped = mapper.map(
    {
        "cve_records":  db.execute_query(conn, "SELECT cve_id, description, cvss_v3_score FROM cve_records"),
        "products":     db.execute_query(conn, "SELECT product_id, product_name, vendor FROM products"),
        "cve_products": db.execute_query(conn, "SELECT cve_id, product_id FROM cve_products"),
    },
    source="nvd_postgres",
)
kg = GraphBuilder().build(sources=[mapped])
```

## 数据源 4 — RSS 与 Atom 订阅源

`ingest_feed()` 拉取 RSS 和 Atom 订阅源，返回一个携带 `FeedItem` 对象列表的 `FeedData` 对象。每个条目都以字符串形式暴露 `.title`、`.description` 和 `.published`——可以直接拼进文本，无需再转换：

```python
from semantica.ingest import ingest_feed

# RSS feed — returns FeedData; iterate .items for FeedItem objects
feed = ingest_feed(
    "https://github.com/advisories.atom",
    method="atom",
)

print(f"Feed title:   {feed.title}")
print(f"Total items:  {len(feed.items)}")

# Convert feed items to text blobs
advisory_texts = []
for item in feed.items:
    text = f"Advisory: {item.title}\n{item.description}"
    advisory_texts.append(text)
    print(f"  {item.title[:80]}  [{item.published}]")

# For NVD's own RSS feed of new CVEs:
nvd_feed = ingest_feed(
    "https://nvd.nist.gov/feeds/xml/cve/misc/nvd-rss.xml",
    method="rss",
)
nvd_texts = [
    f"{item.title}: {item.description}"
    for item in nvd_feed.items
]
```

如果不确定某个站用的是 RSS 还是 Atom，`method="discover"` 会从页面的 HTML link 标签里找出所有可用的订阅源 URL：

```python
feeds = ingest_feed("https://github.com/advisories", method="discover")
# feeds is a list of validated feed URLs
for f in feeds:
    print(f)
```

## 数据源 5 — 文件系统中的 STIX 包

对某个目录使用 `ingest_file()`，从守护进程过夜投递的每个 STIX JSON 文件中提取文本：

```python
from semantica.ingest import ingest_file

# Ingest all STIX JSON files from the directory
stix_files = ingest_file("./stix_bundles/", method="directory", recursive=True)

stix_texts = []
for f in stix_files:
    if f.file_type == "json":
        stix_texts.append(f.text)
        print(f"{f.name}: {f.size:,} bytes")

# apt29_stix_bundle_2024-12-01.json:  184,320 bytes
# lazarus_stix_bundle_2024-12-01.json: 97,408 bytes
# fin7_stix_bundle_2024-12-01.json:   211,968 bytes
```

对于大体量的 XML 格式 STIX 1.x 包，用 `ingest_xml()` 可以拿到结构化的解析结果，而不是原始文本：

```python
from semantica.ingest import ingest_xml

stix_xml_files = ingest_xml("./stix_xml_bundles/", method="directory")
for bundle in stix_xml_files:
    print(f"{bundle.source_path}: {len(bundle.elements)} elements parsed")
```

## 数据源 6 — 企业数据平台（Databricks 与 Snowflake）

`DatabricksIngestor` 和 `SnowflakeIngestor` 返回包装对象（`DatabricksData` / `SnowflakeData`），其 `.data` 字段是 `List[Dict]`——和 `DBIngestor.execute_query()` 直接返回的"字典列表"行结构完全相同，只是多了一层包装。数据源 3 的"先转文本、再存储"模式在这里同样适用：用有针对性的查询只取需要的表和列，再为每条记录拼出一句话，交给 `AgentContext.store()`。

```python
from semantica.ingest import DatabricksIngestor

# Unity Catalog + Delta Lake — PAT or OAuth M2M auth
databricks = DatabricksIngestor(
    host="https://adb-xxx.azuredatabricks.net",
    token="dapi-xxxxxxxx",
    http_path="/sql/1.0/warehouses/xxxxxxxx",
    catalog="main",
)

# .data is List[Dict] — one dict per row, same shape as DBIngestor.execute_query()
customers = databricks.ingest_query(
    "SELECT customer_id, name, industry, arr FROM main.default.customers "
    "WHERE churn_risk_score > 0.7"
)
customer_texts = [
    f"Customer {r['customer_id']} ({r['name']}, {r['industry']}): "
    f"ARR ${r['arr']:,}, flagged high churn risk"
    for r in customers.data
]

# Unity Catalog lineage — build Table --DEPENDS_ON--> Table edges directly from
# Unity Catalog's own lineage tracking, instead of re-deriving them from query logs
lineage = databricks.get_table_lineage("customers", catalog="main", schema="default")
lineage_texts = [
    f"Table main.default.customers depends on {upstream}"
    for upstream in lineage["upstream"]
]
```

```python
from semantica.ingest import SnowflakeIngestor

snowflake = SnowflakeIngestor(
    account="myaccount",
    user="myuser",
    password="mypassword",         # or private_key=... for key-pair; use authenticator="oauth", token=... for OAuth
    warehouse="COMPUTE_WH",
    database="ANALYTICS",
    schema="PUBLIC",
)

# Snowflake uppercases unquoted identifiers, so unquoted columns come back
# as ORDER_ID, PRODUCT, etc. unless the source table quotes them lowercase
orders = snowflake.ingest_query(
    "SELECT order_id, product, region, amount FROM orders "
    "WHERE order_date >= DATEADD(day, -30, CURRENT_DATE())"
)
order_texts = [
    f"Order {r['ORDER_ID']}: {r['PRODUCT']} in {r['REGION']}, ${r['AMOUNT']}"
    for r in orders.data
]
```

把得到的文本列表喂给 `AgentContext.store()`，做法和其他结构化来源完全一致：

```python
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore

graph   = ContextGraph(advanced_analytics=True)
context = AgentContext(
    vector_store    = VectorStore(backend="faiss"),
    knowledge_graph = graph,
)

context.store(
    customer_texts + lineage_texts + order_texts,
    extract_entities=True,
    extract_relationships=True,
)
print(f"Enterprise data graph: {graph.stats()['node_count']} nodes")
```

鉴权细节（Databricks 的 PAT 与 OAuth M2M 之别；Snowflake 的密码、密钥对与 OAuth 之别）、schema/catalog 内省和故障排查，见专门的 [Databricks 集成](../integrations/databricks.md)与 [Snowflake 集成](../integrations/snowflake.md)指南。

> **安全提示：** 生产代码里绝不硬编码凭证（`token`、`password`、`private_key`）；请通过环境变量（如 `DATABRICKS_TOKEN`、`SNOWFLAKE_PASSWORD`）或密钥管理服务传入。

## 数据源 7 — SAP OData

`SAPIngestor` 从 SAP OData 服务（S/4HANA Cloud、SuccessFactors，或经 REST 接入的本地 NetWeaver Gateway）摄取实体集(Entity Set)。它同时支持 OData v2 和 v4，自动跟随服务端驱动的分页，并通过 `export_as_documents()` 把每条记录摊平成文档字典——和其他来源一样，走"先转文本、再存储"的结构化模式。

```python
from semantica.ingest import SAPIngestor

ing = SAPIngestor(
    base_url="https://my-sap.example.com/sap/opu/odata/sap/API_BUSINESS_PARTNER",
    client_id="...", client_secret="...",
    token_url="https://my-sap.example.com/oauth/token",  # OAuth2 client-credentials (BTP/S/4HANA Cloud)
    # On-prem NetWeaver often uses Basic auth instead — swap the block above for:
    # username="erp_user", password="...",
)

# 1. Discover an unfamiliar service: entity sets + field types from $metadata
sets = ing.discover_service()          # [{"name": "A_BusinessPartnerSet", "fields": [...]}, ...]

# 2. Pull a page-walked Entity Set (v2/v4 next links handled for you)
partners = ing.ingest_entity_set(
    entity_set="A_BusinessPartnerSet",
    select="BusinessPartner,BusinessPartnerFullName",   # $select
    top=1000,                                           # cap on total rows
)

# 3. Flatten to document dicts, then build text for the graph
docs = ing.export_as_documents(partners)
partner_texts = [
    f"Business Partner {d['BusinessPartner']}: {d['BusinessPartnerFullName']}"
    for d in docs
]
```

- 用 `expand="to_Item"`（比如用在销售订单头实体集上）可以在一次请求里拉出嵌套的行项目——建模"订单 → 行项目 → 物料"关系时特别顺手。
- 每个出站请求（包括 OAuth2 令牌交换）都经过服务端请求伪造(SSRF)防护，因此用户提供的 SAP URL 永远到不了私有/回环/链路本地地址段。
- 安装：`pip install 'semantica[ingest-sap]'`。

> **安全提示：** 绝不在代码里硬编码凭证（`client_secret`、`password`）；请通过环境变量（如 `SAP_CLIENT_SECRET`、`SAP_PASSWORD`）或密钥管理服务传入。

## 整合全部五类数据源

各来源的文本到手后，`AgentContext.store()` 接受一个扁平的字符串列表。Semantica 会把它们一起生成嵌入并建立索引——除非你显式补充元数据，否则上下文图(Context Graph)并不知道哪个字符串来自哪个来源。

各来源都返回文本后，把所有内容一次性批量传给 `AgentContext.store()`：

```python
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore
from semantica.ingest import ingest_file, ingest_feed, RESTIngestor, DBIngestor

# --- Infrastructure ---
graph   = ContextGraph(advanced_analytics=True)
context = AgentContext(
    vector_store    = VectorStore(backend="faiss", dimension=768),
    knowledge_graph = graph,
    graph_expansion = True,
)

# --- Source 1: PDF reports ---
reports      = ingest_file("./vendor_reports/", method="directory")
report_texts = [r.text for r in reports]

# --- Source 2: MISP API ---
ingestor   = RESTIngestor()
api_data   = ingestor.paginated_fetch(
    "https://misp.internal/events/restSearch",
    headers={"Authorization": "YOUR_MISP_API_KEY"},
    page_size=100,
)
misp_texts = [
    f"MISP {e['Event']['id']}: {e['Event'].get('info', '')} "
    f"attrs={len(e['Event'].get('Attribute', []))}"
    for page in api_data
    for e in page.data
]

# --- Source 3: PostgreSQL CVEs ---
db        = DBIngestor()
cves      = db.execute_query(
    "postgresql://readonly:pass@cvedb.internal:5432/nvd",
    "SELECT cve_id, description, cvss_v3_score FROM cve_records "
    "WHERE cvss_v3_score >= 7.0 AND published_date >= NOW() - INTERVAL '30 days'",
)
cve_texts = [f"{r['cve_id']} (CVSS {r['cvss_v3_score']}): {r['description']}" for r in cves]

# --- Source 4: GitHub Advisory feed ---
feed           = ingest_feed("https://github.com/advisories.atom", method="atom")
advisory_texts = [f"{item.title}: {item.description}" for item in feed.items]

# --- Source 5: STIX bundles ---
stix_files = ingest_file("./stix_bundles/", method="directory")
stix_texts = [f.text for f in stix_files if f.file_type == "json"]

# --- Combine and store ---
all_texts = report_texts + misp_texts + cve_texts + advisory_texts + stix_texts

context.store(
    all_texts,
    extract_entities      = True,
    extract_relationships = True,
)

s = graph.stats()
print(f"Graph: {s['node_count']} nodes, {s['edge_count']} edges")
print(f"Total documents ingested: {len(all_texts)}")
```

## 常见陷阱

**摄取的数据超出所需。** 整表抓取或无限制翻页会让向量索引塞满噪声，拖慢检索。用 `WHERE` 子句、日期过滤和 `page_size` 限制，只取与你的用例相关的记录。

**结构化数据转出的文本质量差。** 数据库行或 API 响应里是字段名、ID 和原始值——不是句子。形如 `"2025-06-21|CVE-2024-3400|10.0"` 的字符串嵌入效果很差，检索结果也弱。把每条记录格式化成自然的句子：`"CVE-2024-3400 (CVSS 10.0): critical RCE in PAN-OS, published 2025-06-21."` 这点额外功夫会在检索质量上回报你。

**没有处理分页。** `RESTIngestor.ingest_endpoint()` 只取一页。如果端点有几千条记录，用 `paginated_fetch()`——否则你只悄悄摄取了第一页。

**API 限速。** `RESTIngestor` 会对 HTTP 429 响应以指数退避自动重试（由 `RESTIngestor(config={"backoff_factor": 2})` 中的 `backoff_factor` 控制）。这是被动应对突发限速，但不会在成功调用之间主动控制节奏。对有严格每秒配额的 API，可以调小 `page_size` 降低请求频率，或在你自己的循环里给 `paginated_fetch()` 调用之间加延时。

**大规模数据库导出。** 把几十万行导进 `AgentContext` 很少是正确做法。写一条只选与你领域相关记录的查询，按日期范围过滤，只投影格式化文本所需的列。

## 优雅地处理错误

把每个来源都包进 try/except，让流水线继续跑、最后统一上报失败，而不是在第一个出错的来源上就崩掉。在定时任务里这一点尤其重要——有部分数据总比没有强：

```python
from semantica.ingest import ingest_file, ingest_feed, RESTIngestor, DBIngestor

all_texts = []
errors    = []

# Source 1: PDFs
try:
    reports = ingest_file("./vendor_reports/", method="directory")
    all_texts.extend(r.text for r in reports)
    print(f"PDFs:       {len(reports)} files ingested")
except Exception as e:
    errors.append(f"PDF ingest failed: {e}")

# Source 2: MISP
try:
    ingestor = RESTIngestor()
    events   = ingestor.paginated_fetch(
        "https://misp.internal/events/restSearch",
        headers={"Authorization": "YOUR_MISP_API_KEY"},
        page_size=100,
    )
    all_texts.extend(
        f"MISP {e['Event']['id']}: {e['Event'].get('info', '')}"
        for page in events
        for e in page.data
    )
    print(f"MISP:       {sum(len(page.data) for page in events if isinstance(page.data, list))} events ingested")
except Exception as e:
    errors.append(f"MISP API failed: {e}")

# Source 3: PostgreSQL
try:
    db = DBIngestor()
    cves = db.execute_query(
        "postgresql://readonly:pass@cvedb.internal:5432/nvd",
        "SELECT cve_id, description, cvss_v3_score FROM cve_records "
        "WHERE cvss_v3_score >= 7.0 AND published_date >= NOW() - INTERVAL '30 days'",
    )
    all_texts.extend(f"{r['cve_id']}: {r['description']}" for r in cves)
    print(f"CVEs:       {len(cves)} records ingested")
except Exception as e:
    errors.append(f"PostgreSQL failed: {e}")

# Source 4: GitHub feed
try:
    feed = ingest_feed("https://github.com/advisories.atom", method="atom")
    all_texts.extend(f"{item.title}: {item.description}" for item in feed.items)
    print(f"Advisories: {len(feed.items)} items ingested")
except Exception as e:
    errors.append(f"GitHub feed failed: {e}")

# Source 5: STIX files
try:
    stix_files = ingest_file("./stix_bundles/", method="directory")
    stix_texts = [f.text for f in stix_files if f.file_type == "json"]
    all_texts.extend(stix_texts)
    print(f"STIX:       {len(stix_texts)} bundles ingested")
except Exception as e:
    errors.append(f"STIX directory failed: {e}")

# Report any failures — don't silently swallow them
if errors:
    print(f"\n{len(errors)} source(s) failed:")
    for err in errors:
        print(f"  - {err}")

print(f"\nTotal documents for graph: {len(all_texts)}")
```

## 调度周期性摄取

把整合后的摄取包成一个函数，交给你选的调度器（cron、Airflow、云调度器）调用：

```python
from datetime import datetime, timedelta
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore
from semantica.ingest import ingest_file, ingest_feed, RESTIngestor, DBIngestor

def run_daily_ingest(since: datetime = None):
    """Run the full five-source ingest pipeline. Returns graph stats dict."""
    since = since or datetime.now() - timedelta(days=1)

    graph   = ContextGraph(advanced_analytics=True)
    context = AgentContext(
        vector_store    = VectorStore(backend="faiss", dimension=768),
        knowledge_graph = graph,
        graph_expansion = True,
    )

    all_texts = []
    errors    = []

    # PDFs deposited since last run
    try:
        reports = ingest_file("./vendor_reports/", method="directory")
        # Filter by modification time in production — simplified here
        all_texts.extend(r.text for r in reports)
    except Exception as e:
        errors.append(f"PDF: {e}")

    # MISP events since last run
    try:
        ingestor = RESTIngestor()
        events   = ingestor.paginated_fetch(
            "https://misp.internal/events/restSearch",
            headers={"Authorization": "YOUR_MISP_API_KEY"},
            params={"timestamp": int(since.timestamp())},
            page_size=100,
        )
        all_texts.extend(
            f"MISP {e['Event']['id']}: {e['Event'].get('info', '')}"
            for page in events
            for e in page.data
        )
    except Exception as e:
        errors.append(f"MISP: {e}")

    # CVEs published since last run
    try:
        db = DBIngestor()
        cves = db.execute_query(
            "postgresql://readonly:pass@cvedb.internal:5432/nvd",
            f"SELECT cve_id, description, cvss_v3_score FROM cve_records "
            f"WHERE published_date >= '{since.isoformat()}' AND cvss_v3_score >= 7.0",
        )
        all_texts.extend(f"{r['cve_id']}: {r['description']}" for r in cves)
    except Exception as e:
        errors.append(f"PostgreSQL: {e}")

    # GitHub advisory feed (always latest)
    try:
        feed = ingest_feed("https://github.com/advisories.atom", method="atom")
        all_texts.extend(f"{item.title}: {item.description}" for item in feed.items)
    except Exception as e:
        errors.append(f"GitHub feed: {e}")

    # STIX bundles deposited since last run
    try:
        stix_files = ingest_file("./stix_bundles/", method="directory")
        all_texts.extend(f.text for f in stix_files if f.file_type == "json")
    except Exception as e:
        errors.append(f"STIX: {e}")

    if all_texts:
        context.store(all_texts, extract_entities=True, extract_relationships=True)
        context.save("./cti_state/")

    return {
        "run_at":     datetime.now().isoformat(),
        "documents":  len(all_texts),
        "errors":     errors,
        "graph":      graph.stats(),
    }

if __name__ == "__main__":
    result = run_daily_ingest()
    print(f"Ingested {result['documents']} documents")
    print(f"Graph: {result['graph']['node_count']} nodes, {result['graph']['edge_count']} edges")
    if result["errors"]:
        print("Errors:", result["errors"])
```

## 业务示例

这两种模式在安全与研究领域之外也很常见。

**内部产品文档。** 如果团队把产品文档、运维手册或入职指南以 Markdown 或 PDF 文件存在共享盘里，摄取一次，之后智能体就能基于完整语料回答问题，而不是只靠关键词搜索。

```python
from semantica.ingest import ingest_file
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore

graph   = ContextGraph(advanced_analytics=True)
context = AgentContext(
    vector_store    = VectorStore(backend="faiss"),
    knowledge_graph = graph,
)

docs = ingest_file("./product_docs/", method="directory", recursive=True)
context.store(
    [d.text for d in docs],
    extract_entities=True,
)
print(f"Indexed {len(docs)} documentation pages")
```

**数据库里的客服工单。** SQL 数据库中的客服工单以自然语言记录了真实世界的产品问题。把它们摄取进来，你就能浮现共性模式、找到相似的历史问题，并构建检索增强的支持工具。

```python
from semantica.ingest import DBIngestor
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore

graph   = ContextGraph(advanced_analytics=True)
context = AgentContext(
    vector_store    = VectorStore(backend="faiss"),
    knowledge_graph = graph,
)

db = DBIngestor()
# Fetch only resolved tickets from the last 90 days — avoid full table dumps
tickets = db.execute_query(
    "postgresql://readonly:YOUR_DB_PASSWORD@support-db:5432/helpdesk",
    """
        SELECT ticket_id, subject, description, resolution, product_area
        FROM support_tickets
        WHERE status = 'resolved'
          AND created_at >= NOW() - INTERVAL '90 days'
        ORDER BY created_at DESC
        LIMIT 5000
    """,
)

# Transform each row into a readable text string
# Guard against NULL description/resolution — common in real helpdesk schemas
ticket_texts = [
    f"Ticket {r['ticket_id']} [{r['product_area']}]: {r['subject']}. "
    f"Description: {(r['description'] or '')[:300]}. "
    f"Resolution: {(r['resolution'] or '')[:200]}"
    for r in tickets
]

context.store(ticket_texts, extract_entities=True)
print(f"Indexed {len(ticket_texts)} support tickets")
```

## 行业示例

以下示例展示常见部署场景下的完整多来源流水线。它们遵循同一个工作流：从多个来源摄取，把结构化数据转成文本，再存入共享的上下文。

<Tabs>
  <Tab title="国防 — CTI/威胁情报">
    某联合情报小组每六小时融合三个实时来源：NVD CVE RSS、合作机构投递的涉密 PDF，以及内部 MISP 实例。

```python
from semantica.ingest import ingest_file, ingest_feed, RESTIngestor
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore

graph   = ContextGraph(advanced_analytics=True, community_detection=True)
context = AgentContext(
    vector_store    = VectorStore(backend="faiss", dimension=768),
    knowledge_graph = graph,
    graph_expansion = True,
)

# NVD CVE feed — new CVEs in last 6 hours
nvd_feed  = ingest_feed(
    "https://nvd.nist.gov/feeds/xml/cve/misc/nvd-rss.xml",
    method="rss",
)
nvd_texts = [f"{item.title}: {item.description}" for item in nvd_feed.items]

# Classified PDF drop from partner agency
partner_docs  = ingest_file("//partner-share/intel-drops/", method="directory")
partner_texts = [doc.text for doc in partner_docs]

# MISP events tagged TLP:AMBER or higher
ingestor   = RESTIngestor()
misp_data  = ingestor.paginated_fetch(
    "https://misp.internal/events/restSearch",
    headers={"Authorization": "YOUR_MISP_API_KEY"},
    params={"tags": "tlp:amber||tlp:red", "threat_level_id": "1"},
    page_size=100,
)
misp_texts = [
    f"MISP {e['Event']['id']}: {e['Event'].get('info', '')}"
    for page in misp_data
    for e in page.data
]

# Fuse all three into the graph
context.store(
    nvd_texts + partner_texts + misp_texts,
    extract_entities=True, extract_relationships=True,
)
print(f"Fused graph: {graph.stats()['node_count']} nodes")
```

  </Tab>

  <Tab title="安全 — SOC/事件响应">
    事件处置期间，SOC 以 15 分钟为周期从三个来源充实时间线：SIEM 告警 CSV 导出、EDR REST API，以及内部 CVE 数据库。

```python
from semantica.ingest import ingest_file, RESTIngestor, DBIngestor
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore

graph   = ContextGraph(advanced_analytics=True)
context = AgentContext(
    vector_store    = VectorStore(backend="faiss", dimension=768),
    knowledge_graph = graph,
)

# SIEM alert CSV exports (written by SIEM every 15 minutes)
alert_files  = ingest_file("./siem_exports/", method="directory")
alert_texts  = [
    f.text for f in alert_files if f.file_type == "csv"
]

# EDR platform REST API — host telemetry for the affected segment
ingestor  = RESTIngestor()
edr_data  = ingestor.ingest_endpoint(
    "https://edr.internal/api/v1/telemetry",
    headers={"X-API-Key": "EDR_KEY"},
    params={"segment": "finance", "severity": "high", "limit": 500},
)
edr_texts = [
    f"Host {e.get('hostname')}: {e.get('event_type')} — {e.get('description')}"
    for e in edr_data.data
]

# CVE cross-reference for any CVE IDs observed in alerts
db = DBIngestor()
exploited_cves = db.execute_query(
    "postgresql://readonly:pass@cvedb.internal:5432/nvd",
    "SELECT cve_id, description, cvss_v3_score FROM cve_records "
    "WHERE cve_id = ANY(ARRAY['CVE-2024-3400', 'CVE-2024-21762'])",
)
cve_texts = [f"{r['cve_id']} (CVSS {r['cvss_v3_score']}): {r['description']}"
             for r in exploited_cves]

context.store(
    alert_texts + edr_texts + cve_texts,
    extract_entities=True, extract_relationships=True,
)
print(f"Incident graph: {graph.stats()['node_count']} nodes enriched")
```

  </Tab>

  <Tab title="生命科学 — 临床/制药">
    某药物警戒平台在每个试验阶段结束后摄取三个数据源：FDA 申报 PDF、PostgreSQL 临床试验数据库，以及通过网络抓取获得的 PubMed 文献。

```python
from semantica.ingest import ingest_file, ingest_web, DBIngestor
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore

graph   = ContextGraph(advanced_analytics=True)
context = AgentContext(
    vector_store    = VectorStore(backend="faiss", dimension=768),
    knowledge_graph = graph,
    retention_days  = None,   # regulatory data — unlimited retention
)

# FDA submissions for Phase III oncology trials
submissions  = ingest_file("./fda_submissions/phase3_oncology/", method="directory")
sub_texts    = [s.text for s in submissions]

# Clinical trials database — protocol and AE records
db = DBIngestor()
trial_records = db.execute_query(
    "postgresql://readonly:pass@clindb.internal:5432/trials",
    """
        SELECT t.protocol_id, t.title, t.primary_endpoint,
               ae.event_type, ae.severity, ae.frequency_pct
        FROM clinical_trials t
        JOIN adverse_events ae ON t.protocol_id = ae.protocol_id
        WHERE t.phase = 'III' AND t.therapeutic_area = 'oncology'
        ORDER BY ae.severity DESC
    """,
)
trial_texts = [
    f"Protocol {r['protocol_id']}: {r['title']} "
    f"AE: {r['event_type']} (severity={r['severity']}, freq={r['frequency_pct']}%)"
    for r in trial_records
]

# PubMed literature for the drug compound
pubmed_pages = ingest_web(
    "https://pubmed.ncbi.nlm.nih.gov/?term=dapagliflozin+cardiovascular",
    method="url",
)
pub_texts = [pubmed_pages.text]

context.store(
    sub_texts + trial_texts + pub_texts,
    extract_entities=True, extract_relationships=True,
)
print(f"Pharmacovigilance graph: {graph.stats()['node_count']} nodes")
```

  </Tab>

  <Tab title="银行 — 风险/合规">
    某合规团队每季度从三个来源取数：BIS 与巴塞尔出版物（网站 sitemap 爬取）、内部制度 PDF，以及监管规则数据库。

```python
from semantica.ingest import ingest_file, ingest_web, DBIngestor
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore

graph   = ContextGraph(advanced_analytics=True)
context = AgentContext(
    vector_store    = VectorStore(backend="faiss", dimension=768),
    knowledge_graph = graph,
    retention_days  = 2555,   # 7-year regulatory retention requirement
)

# BIS/Basel publications via sitemap crawl — filter to capital/liquidity pages
bis_pages    = ingest_web("https://www.bis.org/sitemap.xml", method="sitemap")
basel_pages  = [p for p in bis_pages if any(
    kw in p.url.lower() for kw in ["bcbs", "capital", "liquidity", "leverage"]
)]
bis_texts    = [p.text for p in basel_pages]
print(f"BIS pages matched: {len(bis_texts)}")

# Internal policy library
policies     = ingest_file("./regulatory_library/", method="directory", recursive=True)
policy_texts = [p.text for p in policies]

# Regulatory rules database — active rules only
db = DBIngestor()
rules = db.execute_query(
    "postgresql://compliance_ro:pass@regdb.internal:5432/compliance",
    """
        SELECT rule_id, title, requirement_text, effective_date, jurisdiction
        FROM regulations
        WHERE active = true AND jurisdiction IN ('EU', 'US', 'UK')
        ORDER BY effective_date DESC
    """,
)
rule_texts = [
    f"{r['rule_id']} [{r['jurisdiction']}] {r['title']}: {r['requirement_text']}"
    for r in rules
]

context.store(
    bis_texts + policy_texts + rule_texts,
    extract_entities=True, extract_relationships=True,
)
print(f"Compliance graph: {graph.stats()['node_count']} nodes, "
      f"{graph.stats()['edge_count']} edges")
```

  </Tab>
</Tabs>

## 相关指南

- [流水线](./pipeline.md) — 用 `PipelineBuilder` 把摄取步骤串成自动化、可重试、可并行的流水线
- [上下文图](./context-graphs.md) — 把摄取到的实体存为带类型的属性图并进行查询
- [语义抽取](./semantic-extraction.md) — 从摄取文本中做命名实体识别(NER)、关系抽取与三元组(Triplet)抽取
- [溯源](./provenance.md) — 为每个抽取出的实体追踪来源文档、置信度分数与摄取时间戳
- [Databricks 集成](../integrations/databricks.md) — Unity Catalog 配置、PAT/OAuth M2M 鉴权与血缘内省
- [Snowflake 集成](../integrations/snowflake.md) — 数据仓库配置与密码/密钥对/OAuth 鉴权
