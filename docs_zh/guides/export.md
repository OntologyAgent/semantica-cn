---
title: 导出与序列化
description: "把知识图谱导出为 RDF（Turtle、JSON-LD、N-Triples）、GraphML、Cypher（Neo4j）、ArangoDB AQL、CSV、Parquet、OWL 等格式。"
source: guides/export.md
source_version: 125c70f89d8a2917b4d7265339c33a8f549dc886
---

## 什么是导出？

导出把 Semantica 的图数据转换成外部工具和系统使用的格式。让数据留在 Semantica 内部的是内部持久化机制；导出则专门面向外部消费方的互操作。

**导出与内部持久化的区别：**
- **`AgentContext.store()`** 和图持久化把数据留在 Semantica 内部，供后续处理、检索和推理
- **导出函数**把图数据序列化成外部系统可直接消费的标准化格式

借助导出，你可以对接分析平台、图数据库、RDF 三元组库、语义网系统、数据仓库、商业智能工具，以及任何需要以原生格式访问知识图谱(Knowledge Graph)数据的下游消费方。

## 为什么要用导出？

**一次构建，多次导出。**通过 Semantica 的抽取与推理工作流构建知识图谱，然后把同一份图数据导出成多种格式交给不同消费方，无需重建或重新处理。

**与既有生态互通。**把 Semantica 图接入组织里现成的工具和工作流——从 Neo4j 图数据库、Gephi 可视化到 pandas 数据分析流水线。

**分析与报表工作流。**把图数据喂给商业智能工具、统计分析平台和机器学习流水线——这些系统往往要求 CSV、Parquet 或 RDF 等特定数据格式。

**图数据库迁移与部署。**把图从 Semantica 的内存表示迁移到 Neo4j、ArangoDB 等生产级图数据库或三元组库，获得可扩展的查询性能。

**RDF 与语义网集成。**导出为语义网标准格式（Turtle、JSON-LD、N-Triples），对接本体工具、SPARQL 端点和语义推理系统。

**数据湖与数据仓库集成。**导出为 Parquet 等列式格式，对接 DuckDB、Apache Spark 和云端数据仓库等现代数据栈工具。

**合规与归档工作流。**为监管报送、长期归档和强制特定数据格式的审计轨迹需求生成标准化导出。

## 适用与不适用场景

**适合用导出的场景：**
- 将 Semantica 图与外部系统和工具集成
- 与使用不同技术栈的团队共享图数据
- 构建在下游处理中消费图数据的分析流水线
- 对接要求语义网标准的 RDF 与本体工作流
- 制作报表、可视化和商业智能仪表盘
- 把图迁移到生产数据库以获得可扩展的查询性能
- 满足特定数据格式报送的合规要求

**不适合用导出的场景：**
- 只是想保存并重新加载 Semantica 状态——请改用内置持久化机制
- 首要目标是智能体持久化与记忆连续性
- 内部检索、推理和图操作已经满足需求
- 工作流完全在 Semantica 内部运转，导出只会徒增复杂度
- 需要实时访问不断演化的图数据——导出生成的是静态快照

**以下场景请改用内部持久化：**
- 工作流涉及在 Semantica 内反复建图、查询和推理
- 需要维护智能体记忆、对话历史和决策追踪
- 图数据还会在 Semantica 工作流中继续处理和充实

`export_rdf`、`export_graph`、`export_lpg` 及相关函数一次调用即可把 `ContextGraph` 序列化为十种格式中的任意一种，忠实保留节点类型、边权重和元数据。当下游消费方——三元组库、图数据库、可视化工具、机器学习流水线或用电子表格做审计的人——各自期待不同格式时，就用它们处理同一份内存图。

<Info>
  所有导出函数的第一个参数都是 `graph.to_dict()`——即 `ContextGraph.to_dict()` 生成的那个 dict。图只需构建一次，想导出多少种格式都行，无需重复序列化。注意 `graph.to_dict()` 会把整张图物化到内存，超大图谱需要额外做内存规划。
</Info>

## 构建待导出的图

第一次导出前，先填充一张图。下面所有示例都从这段公共配置开始：

```python
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore

vs    = VectorStore(backend="faiss", dimension=768)
graph = ContextGraph()
ctx   = AgentContext(vector_store=vs, knowledge_graph=graph, graph_expansion=True)

ctx.store(
    [
        "APT29 exploits CVE-2024-3400 in PAN-OS to target NATO defense contractors.",
        "CVE-2024-3400 is a critical remote code execution vulnerability in GlobalProtect.",
        "HAMMERTOSS is APT29's C2 backdoor using Twitter and GitHub as covert channels.",
    ],
    extract_entities=True,
    extract_relationships=True,
)

graph_data = graph.to_dict()   # 单个 dict，下面所有导出复用它
```

## RDF 格式——面向三元组库与语义推理器

**RDF（资源描述框架，Resource Description Framework）**是语义网的基础数据模型，把信息表示为主语-谓语-宾语三元组(Triplet)。要对接语义网技术、本体工具以及任何需要形式化知识表示的系统，RDF 格式必不可少。

当消费方是三元组库（GraphDB、Stardog、Apache Jena）或 OWL 推理器（HermiT、Pellet）时，就该用 RDF。一次 `export_rdf` 调用即可导出全部五种标准 RDF 序列化格式。

```python
from semantica.export import export_rdf

# Turtle —— 人类可读的默认选择；最适合人工审阅和 Git 存储
export_rdf(graph_data, "threat_graph.ttl", format="turtle")

# N-Triples —— 每行一个三元组、无缩进；向任何三元组库批量加载最快
export_rdf(graph_data, "threat_graph.nt", format="ntriples")

# JSON-LD —— 内嵌 @context；下游系统原生讲 JSON 时最佳
export_rdf(graph_data, "threat_graph.jsonld", format="jsonld")

# RDF/XML —— 遗留系统兼容性最强；部分老 OWL 工具只认它
export_rdf(graph_data, "threat_graph.rdf", format="rdfxml")
```

选哪种格式取决于消费方。Turtle 紧凑易读，最适合人工审阅和提交进 Git。N-Triples 向 SPARQL 端点批量加载最快，因为解析器可以逐行流式读取，不必缓存整个文件。下游系统本来就讲 JSON、又想把语义上下文嵌在同一份数据里时，JSON-LD 是正解。RDF/XML 的存在纯粹是为了兼容早于其他格式的老工具。

## 图格式——面向 Gephi、Maltego 与网络分析

**标签属性图(LPG, Labeled Property Graph)**格式用带类型的节点和边表示网络，节点与边可携带属性和元数据。这类格式为图可视化工具和网络分析平台优化，聚焦于关系与结构模式的探索。

GraphML、GEXF 和 DOT 是图分析与可视化工具的原生格式。它们保留节点属性、边权重和类型标签，因此在 Semantica 里构建的图导入 Gephi 或 NetworkX 后立刻就能渲染，属性数据一个不少。

```python
from semantica.export import export_graph

# GraphML —— 工具支持最广：Gephi、yEd、NetworkX、Maltego
export_graph(graph_data, "threat_graph.graphml", format="graphml")

# GEXF —— Gephi 中属性支持更丰富；更适合大型带属性图
export_graph(graph_data, "threat_graph.gexf", format="gexf")

# DOT（Graphviz）—— 自动布局渲染，用于报告配图
export_graph(graph_data, "threat_graph.dot", format="dot")
```

如果你用 Gephi 做分析师简报，GEXF 值得了解——它支持 GraphML 无法表达的动态属性和时态数据。需要 Graphviz 自动排版一张图、嵌入 PDF 报告或文档站时，DOT 是正确选择。

## Neo4j Cypher——面向图模式威胁狩猎

**Cypher** 是 Neo4j 的声明式图查询语言，用模式匹配查找和操作图数据。导出为 Cypher 后，团队可以借助 Neo4j 优化过的查询引擎运行复杂图查询、模式检测和图分析。

当 SOC 团队想对图跑 Cypher 查询——找出共享基础设施的威胁行为者，或追踪多跳攻击路径——你只需导出为 Cypher，再用一条命令把结果载入 Neo4j Desktop 或 Memgraph。

```python
from semantica.export import export_lpg

export_lpg(graph_data, "threat_graph.cypher", method="cypher")
```

输出文件里是可直接执行的 `CREATE` 和 `MATCH` 语句：

```text
CREATE (:ThreatActor {id: "apt29", name: "APT29", nation_state: "RU"})
CREATE (:Vulnerability {id: "cve-2024-3400", cvss_score: 10.0})
MATCH (a {id: "apt29"}), (b {id: "cve-2024-3400"}) CREATE (a)-[:EXPLOITS {confidence: 0.97}]->(b)
```

用 `cypher-shell < threat_graph.cypher` 载入 Neo4j，或把文件拖进 Neo4j Desktop 的导入向导。从此 SOC 团队写 Cypher 查询，完全不必碰 Python。

## ArangoDB AQL——面向多模型查询

ArangoDB 用一种查询语言同时覆盖图遍历、文档查询和全文检索。合规团队需要把图与结构化监管文档做关联查询时，ArangoDB 是合适的后端。

```python
from semantica.export import export_arango

export_arango(
    graph_data,
    "regulatory.aql",
    vertex_collection         = "regulatory_nodes",
    edge_collection           = "regulatory_edges",
    include_collection_creation = True,    # 生成 CREATE COLLECTION 语句
    batch_size                = 200,       # INSERT 语句分批执行，避免内存尖峰
)
```

`include_collection_creation=True` 意味着这个 AQL 文件自包含——先创建集合再插入数据，因此对一个全新的 ArangoDB 实例可以直接运行，无需任何前置配置。

## CSV——面向电子表格审计与统计分析

**CSV（逗号分隔值）**是一种简单的表格格式，电子表格应用、统计工具和数据分析平台全都支持。CSV 导出把图数据摊平成行与列，服务以表格数据为主的团队。

合规团队泡在 Excel 里，数据科学团队泡在 pandas 里，两边都要 CSV。`export_csv` 把图写成扁平的行——传入基础路径时，实体和关系分别写成两个文件。

```python
from semantica.export import export_csv

# 单个 CSV —— 节点和边交织在一起，用 "record_type" 列区分
export_csv(graph_data, "threat_graph.csv")

# 拆分 CSV —— 分别写出 threat_graph_entities.csv 和 threat_graph_relationships.csv
export_csv(
    {"entities": graph_data.get("nodes", []),
     "relationships": graph_data.get("edges", [])},
    "threat_graph",
)
```

拆分形式对下游工具更实用：实体 CSV 可以喂给实体类型透视表，关系 CSV 可以喂给 pandas 或 R 里的网络分析。

## Parquet——面向数据湖与机器学习流水线

**Parquet** 是为分析型负载优化的列式存储格式，压缩高效、查询快。Parquet 文件与现代数据栈工具和机器学习框架无缝衔接。

数据科学团队在 DuckDB、Spark 或湖仓里对图属性做特征工程时，要的就是 Parquet：列式、压缩，主流机器学习框架都能读。

```python
from semantica.export import export_parquet

export_parquet(graph_data, "threat_graph_entities.parquet")
```

变成 Parquet 之后，图实体就是一个 DataFrame，可以与遥测数据做连接、用外部特征充实、再喂给分类模型——数据科学一侧不用写任何自定义序列化代码。

## OWL——面向基于本体的推理

**OWL（网络本体语言，Web Ontology Language）**是表示富本体的语义网标准，涵盖类、属性和逻辑约束。OWL 支持对形式化知识模型做自动推理、一致性检查和推断。

**OntologyGenerator** 通过分析实体类型、关系和模式，从图数据生成类层次、属性定义和逻辑约束，产出形式化本体。由此可以获得模式校验、自动推理以及与语义网工具集成的能力。

用 `OntologyGenerator` 从图生成 OWL 本体后，可以把它导出给 Protégé、HermiT 推理或监管报送使用。

```python
from semantica.export import export_owl
from semantica.ontology import OntologyGenerator

ontology = OntologyGenerator(base_uri="https://example.org/cti/") \
               .generate_from_graph(graph_data)

export_owl(ontology, "cti_ontology.owl", format="owl-xml")
```

## 常见误区

**把导出与持久化混为一谈。**导出为互操作生成外部快照；持久化维护的是 Semantica 的内部状态。需要保存并重新加载智能体记忆、或继续基于图的工作流时，别用导出——改用内置持久化机制。

**图已变更还导出过期数据。**务必在最后一次修改图之后再调用 `graph.to_dict()`。如果工作流早期就存下 `graph_data`，之后又改了图，导出的将是过时状态，而非最新变更。

**放着现成图数据不用，重跑昂贵的抽取。**通过实体抽取和关系推断把图构建一次，然后用同一个 `graph_data` dict 导出多种格式。别为每种导出格式重建一遍图。

**CSV 就够时选了过于复杂的格式。**如果下游消费方只处理表格数据、不需要保留图结构，CSV 比 RDF 或 GraphML 更简单、更快、支持面更广。

**以为溯源和历史会自动出现在导出里。**标准导出格式只捕捉当前图状态，不包含溯源链、版本历史或审计轨迹。需要完整血缘信息时，请使用专门的溯源导出机制。

**忽视下游的 schema 要求。**不同系统对标识符格式、属性 schema 和关系表示各有期待。上生产工作流之前，先验证导出数据是否符合消费系统的预期。

**不做内存规划就导出超大图。**`graph.to_dict()` 会把整张图物化进内存。图特别大时请监控内存占用；资源受限的环境里考虑分块或流式方案。

## 领域示例

<Tabs>

<Tab title="国防——CTI/威胁情报">

CTI 团队要同时把同一张威胁图用在四处：跨团队查询的 SPARQL 端点、分析师简报用的 Gephi、图模式威胁狩猎用的 Neo4j，以及 SIEM 摄取管道的 JSON-LD 数据流。四次导出，一份图 dict。

```python
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore
from semantica.ingest import ingest_file
from semantica.export import export_rdf, export_graph, export_lpg
import os

vs    = VectorStore(backend="faiss", dimension=768)
graph = ContextGraph()
ctx   = AgentContext(vector_store=vs, knowledge_graph=graph, graph_expansion=True)

apt_report = ingest_file("apt29_2024_campaign.pdf", method="file")
ctx.store(apt_report.text, extract_entities=True, extract_relationships=True)

graph_data = graph.to_dict()
os.makedirs("./exports/", exist_ok=True)

# 1. Turtle → SPARQL 端点（Apache Jena、Stardog、GraphDB）
export_rdf(graph_data, "./exports/threat_graph.ttl", format="turtle")

# 2. JSON-LD → SIEM 摄取（Splunk、Elastic）—— 原生 JSON 管道
export_rdf(graph_data, "./exports/threat_graph.jsonld", format="jsonld")

# 3. GraphML → Gephi，用于分析师简报可视化
export_graph(graph_data, "./exports/threat_graph.graphml", format="graphml")

# 4. Cypher → Neo4j，用于图模式威胁狩猎
export_lpg(graph_data, "./exports/threat_graph.cypher", method="cypher")

print("Threat graph exported to 4 formats.")
```

</Tab>

<Tab title="安全——SOC/事件响应">

事件处置进行中，SOC 需要同一张图的三种形态：Neo4j 用于狩猎，GEXF 用于 Gephi 时间线可视化，GraphML 用于导入 Maltego。三者都出自同一份内存图。

```python
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore
from semantica.export import export_lpg, export_graph
import os

vs    = VectorStore(backend="faiss", dimension=768)
graph = ContextGraph()
ctx   = AgentContext(
    vector_store=vs,
    knowledge_graph=graph,
    graph_expansion=True,
    decision_tracking=True,
)

incidents = [
    "Host ws-finance-03 (10.10.1.5): scheduled task created via wmiprvse.exe — T1053.005",
    "User jsmith logged in from anomalous IP 185.220.101.7 (Tor exit node)",
    "EDR alert on dc01: LSASS memory access by procdump.exe — T1003.001",
]
ctx.store(incidents, extract_entities=True, extract_relationships=True)

graph_data = graph.to_dict()
os.makedirs("./soc_exports/", exist_ok=True)

# Cypher → Neo4j，用于基于 Cypher 的威胁狩猎
export_lpg(graph_data, "./soc_exports/incident_graph.cypher", method="cypher")

# GEXF → Gephi，用于时间线可视化
export_graph(graph_data, "./soc_exports/incident_graph.gexf", format="gexf")

# GraphML → Maltego，用于关联分析
export_graph(graph_data, "./soc_exports/incident_graph.graphml", format="graphml")

print("SOC graph exported — load incident_graph.cypher into Neo4j Desktop.")
```

</Tab>

<Tab title="生命科学——临床/制药">

临床试验数据要送到三处：SPARQL 端点做跨试验联合查询、CSV 供 R 做统计分析、Turtle 文件用于监管报送。图里编码的是从试验方案中抽取的化合物-靶点-疾病关系。

```python
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore
from semantica.ingest import DBIngestor
from semantica.export import export_rdf, export_csv

vs    = VectorStore(backend="faiss", dimension=768)
graph = ContextGraph(advanced_analytics=True)
ctx   = AgentContext(
    vector_store=vs,
    knowledge_graph=graph,
    graph_expansion=True,
    retention_days=None,
)

db = DBIngestor()
trial_rows = db.execute_query(
    "postgresql://readonly@clindb:5432/trials",
    "SELECT compound, target_protein, disease, mechanism FROM trial_protocols",
)
trial_texts = [
    "{} targets {} in {} via {}.".format(
        r["compound"], r["target_protein"], r["disease"], r["mechanism"]
    )
    for r in trial_rows
]
ctx.store(trial_texts, extract_entities=True, extract_relationships=True)

graph_data = graph.to_dict()

# N-Triples，快速批量加载进 GraphDB 或 Stardog
export_rdf(graph_data, "./exports/clinical_graph.nt",  format="ntriples")

# Turtle，供人工审阅并附入监管卷宗
export_rdf(graph_data, "./exports/clinical_graph.ttl", format="turtle")

# 拆分 CSV，供 R / SAS 做统计分析
export_csv(
    {"entities": graph_data.get("nodes", []),
     "relationships": graph_data.get("edges", [])},
    "./exports/clinical_graph",
)

print("Clinical graph exported — ready for SPARQL endpoint and statistical review.")
```

</Tab>

<Tab title="银行——风险/合规">

监管知识图谱要送到三处：ArangoDB 做多模型合规查询、RDF/XML 进长期监管归档、JSON-LD 供合规仪表盘 API 使用。巴塞尔 III 监管条款、风险参数及其关系全部以图节点的形式捕获。

```python
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore
from semantica.ingest import ingest_file
from semantica.export import export_arango, export_rdf
import os

vs    = VectorStore(backend="faiss", dimension=768)
graph = ContextGraph()
ctx   = AgentContext(
    vector_store=vs,
    knowledge_graph=graph,
    graph_expansion=True,
    retention_days=2555,    # 7 年监管留存
)

regs = [
    ingest_file("basel3_cre20.pdf",       method="file"),
    ingest_file("sr_11_7_model_risk.pdf", method="file"),
    ingest_file("bcbs239.pdf",            method="file"),
]
ctx.store(
    [r.text for r in regs],
    extract_entities=True,
    extract_relationships=True,
)

graph_data = graph.to_dict()
os.makedirs("./compliance_exports/", exist_ok=True)

# ArangoDB AQL，多模型监管查询（图 + 文档关联）
export_arango(
    graph_data,
    "./compliance_exports/regulatory.aql",
    vertex_collection           = "regulatory_nodes",
    edge_collection             = "regulatory_edges",
    include_collection_creation = True,
    batch_size                  = 200,
)

# RDF/XML，长期监管归档（遗留系统兼容性最强）
export_rdf(graph_data, "./compliance_exports/regulatory_audit.rdf", format="rdfxml")

# JSON-LD，合规仪表盘 REST API
export_rdf(graph_data, "./compliance_exports/regulatory.jsonld", format="jsonld")

print("Compliance graph exported in 3 formats.")
```

</Tab>

</Tabs>

## 选对格式

格式选择归根结底取决于两件事：谁来消费输出，以及他们手上已经用什么工具。

消费方讲 SPARQL 或用三元组库，就选 Turtle（人工审阅）、N-Triples（批量加载）或 JSON-LD（原生 JSON 管道）。消费方用属性图数据库，Cypher 对应 Neo4j 或 Memgraph；如果还想在同一系统里做文档与搜索查询，AQL 对应 ArangoDB。消费方用图可视化工具，GraphML 是工具支持最广的保底之选，GEXF 在 Gephi 里属性处理更丰富，需要 Graphviz 自动渲染静态示意图时选 DOT。消费方泡在电子表格或统计工具里，CSV 最省事。消费方在 DuckDB、Spark 或湖仓里跑机器学习流水线，Parquet 正中下怀。

做语义推理和本体工作，OWL/XML 是唯一之选——只有它能在 Protégé 和 HermiT 里保留完整的类层次。

## 相关指南

- [上下文图](./context-graphs.md) — `ContextGraph` 对象，其 `to_dict()` 是所有导出的输入
- [本体管理](./ontology.md) — 导出从图生成的 OWL 本体
- [推理与规则](./reasoning.md) — 推理结果可导出为 RDF 三元组
- [变更管理](./change-management.md) — 导出前给图做快照，证明导出来自经验证的状态
- [流水线](./pipeline.md) — 用一个 `PipelineBuilder` 串联摄取、抽取与导出
