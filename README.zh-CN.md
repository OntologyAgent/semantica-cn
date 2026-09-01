> 本文档翻译自英文版 [README.md](./README.md)（commit 97def3f7），如有出入以英文版为准。[English](./README.md) | **中文**

<div align="center">

<img src="Semantica Logo.png" alt="Semantica" width="420"/>

<div style="display:flex; gap:10px; align-items:center; flex-wrap:wrap;">
  <a href="https://trendshift.io/repositories/18986?utm_source=repository-badge&amp;utm_medium=badge&amp;utm_campaign=badge-repository-18986" target="_blank" rel="noopener noreferrer">
    <img src="https://trendshift.io/api/badge/repositories/18986" alt="semantica-agi/semantica | Trendshift" width="250" height="55"/>
  </a>

  <a href="https://trendshift.io/repositories/18986?utm_source=trendshift-badge&amp;utm_medium=badge&amp;utm_campaign=badge-trendshift-18986" target="_blank" rel="noopener noreferrer">
    <img src="https://trendshift.io/api/badge/trendshift/repositories/18986/weekly?language=Python" alt="semantica-agi/semantica | Trendshift" width="250" height="55"/>
  </a>
</div>

### 面向上下文与可问责 AI 系统的图原生基础设施

#### *AI 智能体的开源版 Palantir*

> 摄取你的企业数据，抽取关键信息，构建上下文图(Context Graph)与知识图谱(KG)，并在其上运行图分析与因果推理，决策溯源全程内建。可解释、可追溯、天然可信。

**上下文管理 &nbsp;·&nbsp; 知识建模 &nbsp;·&nbsp; 确定性推理 &nbsp;·&nbsp; 本体管理 &nbsp;·&nbsp; 决策智能 &nbsp;·&nbsp; 端到端可追溯**

**开源 &nbsp;·&nbsp; 可自托管 &nbsp;·&nbsp; 可审计 &nbsp;·&nbsp; 可治理 &nbsp;·&nbsp; 零供应商锁定**

**多模态图存储 &nbsp;·&nbsp; 支持 RDF 与 LPG &nbsp;·&nbsp; W3C 标准 &nbsp;·&nbsp; 可互操作**

#### 为高风险、强监管领域而生

[![GitHub Stars](https://img.shields.io/github/stars/semantica-agi/semantica?style=flat-square&color=FFD700&logo=github&logoColor=white&label=Stars)](https://github.com/semantica-agi/semantica) [![GitHub Forks](https://img.shields.io/github/forks/semantica-agi/semantica?style=flat-square&color=6E40C9&logo=github&logoColor=white&label=Forks)](https://github.com/semantica-agi/semantica/network/members) [![Contributors](https://img.shields.io/github/contributors/semantica-agi/semantica?style=flat-square&color=2EA043&logo=github&logoColor=white)](https://github.com/semantica-agi/semantica/graphs/contributors) [![PyPI](https://img.shields.io/pypi/v/semantica.svg?style=flat-square&color=0066CC&logo=pypi&logoColor=white)](https://pypi.org/project/semantica/) [![Total Downloads](https://static.pepy.tech/badge/semantica?style=flat-square)](https://pepy.tech/project/semantica) [![Python 3.8+](https://img.shields.io/badge/python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT) [![CI](https://img.shields.io/github/actions/workflow/status/semantica-agi/semantica/ci.yml?style=flat-square&label=CI)](https://github.com/semantica-agi/semantica/actions) [![Install Matrix](https://img.shields.io/github/actions/workflow/status/semantica-agi/semantica/install-matrix.yml?style=flat-square&label=pip%20install)](https://github.com/semantica-agi/semantica/actions/workflows/install-matrix.yml) [![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/semantica-agi/semantica/badge?style=flat-square)](https://scorecard.dev/viewer/?uri=github.com/semantica-agi/semantica) [![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/semantica-agi/semantica)

[![Website](https://img.shields.io/badge/Website-getsemantica.ai-000000?style=flat-square&logo=googlechrome&logoColor=white)](https://getsemantica.ai/) [![Docs](https://img.shields.io/badge/Docs-docs.getsemantica.ai-0099FF?style=flat-square&logo=readthedocs&logoColor=white)](https://docs.getsemantica.ai/) [![Discord](https://img.shields.io/badge/Discord-Join%20Community-5865F2?style=flat-square&logo=discord&logoColor=white)](https://discord.gg/sV34vps5hH) [![Twitter/X](https://img.shields.io/badge/Follow-%40BuildSemantica-000000?style=flat-square&logo=x&logoColor=white)](https://x.com/BuildSemantica) [![YouTube](https://img.shields.io/badge/YouTube-Watch%20Demos-FF0000?style=flat-square&logo=youtube&logoColor=white)](https://www.youtube.com/watch?v=QfnNZg4-dZA) [![Changelog](https://img.shields.io/badge/Changelog-View-6E40C9?style=flat-square&logo=keepachangelog&logoColor=white)](CHANGELOG.md)

```bash
pip install semantica
```

</div>

---

<div align="center">

<a href="https://www.youtube.com/watch?v=QfnNZg4-dZA" target="_blank">
<img
  src="docs/assets/img/semantica-knowledge-explorer-demo.gif"
  alt="Semantica Knowledge Explorer: live graph, decisions, entity resolution, ontology hub"
  width="900"
/>
</a>

*知识探索器 · 上下文图 · 推理引擎 · 决策智能 · 本体中心*

**[▶ 观看完整平台演示](https://www.youtube.com/watch?v=QfnNZg4-dZA)**

</div>

---

大多数 AI 智能体运行在嵌入向量之上，而不是意义之上：只有相似度分数，没有结构、没有关系，也无法解释结果为什么被返回。Semantica 是位于你的 LLM、向量存储和智能体框架之下的语义/上下文层：一个确定性的基础设施层（构建图谱、推理、溯源均不需要 LLM），把碎片化的企业数据变成结构化、可查询的上下文图和知识图谱(Knowledge Graph)，并由本体(Ontology)与受控词表（OWL、SHACL、SKOS）治理，让数据的含义显式可见，而不只是它的嵌入向量。决策溯源与审计追踪是这套结构自然带出的属性，而不是产品本身；在监管者可能质疑的领域，同一套结构恰好就是对"为什么"的直接回答。

> ⚠️ **这是系统级可解释性，不是基础模型可解释性。** Semantica 不暴露、也不重建 LLM *内部*发生的事情——模型的内部推理或思维链对任何外部系统都同样不透明。Semantica 解释的是模型*之外*的部分：输入的上下文与数据、产生的决策、决策的溯源、相关的关系、应用的策略，以及完整的执行轨迹。

**适用人群：**

- **AI/ML 平台团队**：交付会做出重大决策的智能体，需要从碎片化的原始数据构建结构化、可查询的上下文，而不只是一个向量索引
- **使用 Databricks 或 Snowflake 的数据平台团队**：需要把已经躺在 Unity Catalog 或 Snowflake 数仓里的表，变成受治理、带血缘追踪的知识图谱，而不用先把数据导出到第三方 SaaS
- **合规、风险与审计团队**：需要以监管者真正能接受的格式，直接回答"AI 为什么这样做？"
- **受监管企业**（金融、医疗、法律、政府、国防）：不能交付黑盒，也不能为了得到答案而把数据送进别人的 SaaS
- **平台与基础设施工程师**：希望知识图谱、推理和溯源栈自托管、可替换，而不是锁定在某一家厂商的后端
- **数据与知识工程师**：从混乱的多源数据构建知识图谱：实体和关系被抽取出来，冲突或矛盾的事实被标记而不是被静默覆盖，重复项在变成噪音之前就被合并

**[快速开始](#quick-start)** &nbsp;·&nbsp; **[架构](#architecture)** &nbsp;·&nbsp; **[功能概览](#what-semantica-gives-you)** &nbsp;·&nbsp; **[为什么选择 Semantica](#why-semantica)** &nbsp;·&nbsp; **[决策智能](#decision-intelligence)** &nbsp;·&nbsp; **[上下文图](#context-graphs)** &nbsp;·&nbsp; **[实战教程：审计追踪](#recipe-audit-trail-for-a-regulated-decision)** &nbsp;·&nbsp; **[模块参考](#module-reference)** &nbsp;·&nbsp; **[集成](#integrations)** &nbsp;·&nbsp; **[CLI](#cli)** &nbsp;·&nbsp; **[性能](#performance)** &nbsp;·&nbsp; **[安装](#installation)**

---

## Semantica 能为你带来什么
<a id="what-semantica-gives-you"></a>

- **上下文图：** 一张结构化、可查询的图，承载你的智能体所知道、所决策、所推理的一切
- **决策智能：** 每个决策都是一等对象：可追溯、可按先例检索、带因果链接
- **AI 治理与本体：** SHACL 约束、冲突检测、合规规则、OWL 生成、SKOS 词表管理，并配有可视化编辑器
- **完整可审计性：** 每条事实都带 W3C PROV-O 溯源(Provenance)，审计追踪可导出为 JSON、CSV 或 RDF
- **确定性推理：** 前向链、Rete 网络、Datalog 与 SPARQL，推理路径完全可解释，不是黑盒
- **知识流水线：** 多源摄取、实体感知分块、命名实体识别(NER)/关系/事件抽取、知识图谱构建，全程带语义去重与保留溯源的合并
- **企业数据平台：** Databricks（Unity Catalog + Delta Lake，PAT/OAuth M2M 认证，目录/模式/表/血缘内省）与 Snowflake（数仓/数据库/模式，密钥对与 OAuth 认证）原生连接器，让已在湖仓或数仓中的表直接变成带溯源的图节点，而不是又多一次导出/导入
- **图分析：** 在你刚建好的图上运行中心性、社区检测、链接预测与最短路径查询
- **多模态图存储：** 原生 RDF（内嵌 Oxigraph，以及通过 SPARQL 接入 Blazegraph、Apache Jena、Eclipse RDF4J）与带标签属性图(LPG)（通过 Cypher 接入 Neo4j、FalkorDB、Apache AGE、AWS Neptune），外加向量存储，全部可替换且无需改动你的代码
- **可视化：** 在交互式浏览器工作台中探索任意图、本体或时间线
- **开箱即用的集成：** 原生支持 Agno、CrewAI 与 LangChain，功能完整的 MCP 服务器、全面的 CLI、REST API，以及覆盖主流编辑器的插件

---

## 为什么选择 Semantica
<a id="why-semantica"></a>

| | 向量数据库 + RAG | 普通 LLM 记忆 | **Semantica** |
| --- | --- | --- | --- |
| **召回方式** | 嵌入相似度 | Token 窗口 | 图遍历 + 语义搜索 |
| **决策历史** | 不存储 | 不存储 | 一等可查询对象 |
| **溯源** | 无 | 无 | W3C PROV-O，关联来源 |
| **推理** | 无 | 黑盒 | 前向链、Rete、Datalog、SPARQL |
| **冲突检测** | 静默覆盖 | 静默覆盖 | 检测、标记、解决 |
| **时间回溯** | 不支持 | 不支持 | 时间点图快照 |
| **合规导出** | 无 | 无 | PROV-O、SHACL、OWL、RDF |
| **策略执行** | 无 | 无 | 内建规则引擎 + SHACL |
| **实体解析** | 不支持 | 不支持 | 分块(Blocking) + 语义去重 |
| **多智能体上下文** | 每个智能体各自独立 | 每个智能体各自独立 | 单一共享智能层 |

Semantica 是对你现有技术栈的补充，而不是替代。你的 LLM、向量存储和智能体框架保持原样；Semantica 在其之上叠加决策记录、因果推理、溯源、本体治理、冲突检测与审计追踪。推理引擎、知识图谱构建和溯源层是完全确定性的，使用它们不需要任何 LLM。

---

## 快速开始
<a id="quick-start"></a>

```bash
pip install semantica
```

```python
from semantica.context import ContextGraph

graph = ContextGraph(advanced_analytics=True)

# Every agent decision becomes a queryable, auditable knowledge node
decision_id = graph.record_decision(
    category="vendor_selection",
    scenario="Choose cloud provider for HIPAA workload",
    reasoning="AWS offers BAA, mature HIPAA tooling, and existing team expertise",
    outcome="selected_aws",
    confidence=0.93,
)

# Ask "why did this happen?" and get a real, structured answer
chain     = graph.trace_decision_chain(decision_id)       # full causal ancestry
similar   = graph.find_similar_decisions("cloud vendor", max_results=5)  # precedents
impact    = graph.analyze_decision_impact(decision_id)    # downstream influence map
compliant = graph.check_decision_rules({"category": "vendor_selection"})  # policy gate
```

**5 秒验证安装：**

```bash
semantica doctor
# Python 3.11.9         pass
# semantica 0.6.7       pass
# faiss vector store    pass
# Config file           pass    ~/.semantica/config.yaml
```

**在脚本或 CI 中运行？** 进度条只在 stdout 是交互式终端（或 Jupyter notebook）时才输出，因此默认情况下管道和重定向保持干净。设置 `SEMANTICA_DISABLE_PROGRESS=1` 可在任何环境关闭进度条，设置 `SEMANTICA_FORCE_PROGRESS=1` 可在 stdout 被重定向时保留进度条。`SEMANTICA_DISABLE_PROGRESS` 优先。

<div align="center">

如果 Semantica 解决了你的实际问题，一颗 star 能帮助更多人发现它。

**[⭐ 在 GitHub 上 Star](https://github.com/semantica-agi/semantica)** &nbsp;·&nbsp; **[加入 Discord](https://discord.gg/sV34vps5hH)**

</div>

---

## 架构
<a id="architecture"></a>

Semantica 是一条真正的端到端流水线，而不是一个只有营销名字的单一库。下面每个阶段都是已发布的模块，可独立导入：

```
Sources → Ingest → Parse → Normalize → Split → Extract → Conflict Detection → Deduplication
   → Knowledge Graph → [ Ontology · Reasoning · Provenance · Decisions ] → Enriched KG
   → Vector Store + Polyglot Graph Store (RDF & LPG) → Export / Visualize / REST · MCP · CLI
```

- **摄取(Ingest)：** 文件、Web、数据库、企业数据平台（Databricks、Snowflake）、云（Google Drive、Elasticsearch）、流（Kafka、Kinesis）、Git、邮件、MCP
- **解析 → 规范化 → 切分：** 文档解析，文本/实体/日期规范化，GraphRAG 原生的实体感知分块
- **抽取 → 冲突检测 → 去重：** NER、关系、事件、三元组；冲突事实在合并前被标记并解决
- **知识图谱：** `GraphBuilder` 构建图；双时态事实与完整图分析（中心性、社区、链接预测）在其上运行
- **本体 · 推理 · 溯源 · 决策：** 位于知识图谱之上的智能层，具备 SHACL/OWL 治理、Rete/Datalog/SPARQL 推理、W3C PROV-O 血缘和一等决策记录
- **存储：** 多模态设计，涵盖 RDF 三元组存储（内嵌 Oxigraph、Blazegraph、Apache Jena、Eclipse RDF4J）、带标签属性图（Neo4j、FalkorDB、Apache AGE、AWS Neptune）与向量存储，全部可替换且无需改动你的代码
- **输出：** 导出（RDF、OWL、Parquet、Cypher、JSON-LD）、交互式可视化，以及通过 REST API、MCP 服务器或 CLI 访问

**→ [流水线与决策智能生命周期的完整 Mermaid 图](ARCHITECTURE.md)**

---

## 决策智能
<a id="decision-intelligence"></a>

决策智能把 AI 的每一次选择，从一次转瞬即逝的推理，变成永久、可审计、可查询的记录。它回答的是监管者与企业风险团队日益迫切追问的那个问题：*"你的 AI 决定了什么、为什么这样决定、之后又发生了什么？"*

在 Semantica 中，决策不是一行日志，而是拥有完整生命周期的一等图节点。在受监管领域，每个 AI 决策都必须可追溯到来源、能向审计师自证：`record_decision()` 创建一条永久的结构化记录，可导出为 W3C PROV-O——这是多数合规框架接受用于监管提交的格式。

```
record_decision()             → stored as a graph node with full structured context
add_causal_relationship()     → linked to upstream causes and downstream effects
find_similar_decisions()      → semantic precedent search across all past decisions
trace_decision_chain()        → full causal ancestry back to root causes
analyze_decision_impact()     → downstream influence map - everything this decision affected
check_decision_rules()        → policy compliance gate against configurable rule sets
export / audit trail          → W3C PROV-O, CSV, or JSON for regulator submission
```

```python
from semantica.context import ContextGraph

graph = ContextGraph(advanced_analytics=True)

# Record decisions with full structured context
app_id = graph.record_decision(
    category="credit_application",
    scenario="Personal loan, $85k income, 31% DTI, 3yr employment",
    reasoning="Income meets threshold; employment stable; no adverse credit events",
    outcome="proceed_to_underwriting",
    confidence=0.88,
    metadata={"applicant_id": "A-7291"},
)
uw_id = graph.record_decision(
    category="loan_underwriting",
    scenario="Underwriting review for A-7291",
    reasoning="DTI within policy; clean 36-month credit history",
    outcome="approved",
    confidence=0.94,
)
rate_id = graph.record_decision(
    category="interest_rate",
    scenario="Rate assignment for approved loan A-7291",
    outcome="rate_set_8.9pct",
    reasoning="Prime + 2.4% based on risk tier B2",
    confidence=0.99,
)

# Build the auditable causal chain - relationship_type must be one of
# CAUSED, INFLUENCED, or PRECEDENT_FOR
graph.add_causal_relationship(app_id, uw_id,   relationship_type="CAUSED")
graph.add_causal_relationship(uw_id,  rate_id, relationship_type="INFLUENCED")

# Query the intelligence
chain     = graph.trace_decision_chain(rate_id)
similar   = graph.find_similar_decisions("personal loan approval, 31% DTI", max_results=5)
impact    = graph.analyze_decision_impact(uw_id)
compliant = graph.check_decision_rules({"category": "loan_underwriting", "confidence": 0.94})
insights  = graph.get_decision_insights()
```

---

## 上下文图
<a id="context-graphs"></a>

上下文图是传统检索增强生成(RAG)所缺失的结构化记忆层。扁平的嵌入向量只能回答*"什么相似？"*，而上下文图回答的是*"什么与什么相连、为什么、如何相连？"*。每个实体、关系、决策和事实都是一等节点，可通过图遍历查询。实体链接到源文档，决策链接到证据与后果，事实携带完整溯源，冲突会被检测出来，而不是被静默覆盖。

```python
from semantica.context import ContextGraph, AgentContext
from semantica.vector_store import VectorStore

graph = ContextGraph(advanced_analytics=True)

# Add nodes with typed properties
graph.add_node("acme_corp",    "Organization", name="Acme Corp", industry="SaaS")
graph.add_node("alice_chen",   "Person",       name="Alice Chen", role="CTO")
graph.add_node("contract_001", "Contract",     value=2_400_000, currency="USD")

# Add typed, weighted edges (extra kwargs become edge metadata)
graph.add_edge("alice_chen", "acme_corp",    edge_type="works_for",  since="2019-03-01")
graph.add_edge("acme_corp",  "contract_001", edge_type="party_to",   signed="2024-01-15")

# BFS traversal - hop through the graph from any node
neighbors = graph.get_neighbors("acme_corp", hops=2)

# Point-in-time snapshot - the graph as it existed on any past date
snapshot  = graph.state_at("2024-01-01")

# AgentContext - high-level API for agent memory workflows
vs  = VectorStore(backend="faiss")
ctx = AgentContext(vector_store=vs, knowledge_graph=graph)
ctx.store("Alice approved the Acme renewal in Q1 2024", conversation_id="conv_001")
retrieved = ctx.retrieve("who approved the Acme contract?")
```

**为什么用图而不是嵌入向量：** 遍历能找到嵌入向量漏掉的关联（比如与一份合同相隔 3 跳的人）；每个节点都带溯源，你随时可以问*"这是从哪来的？"*；冲突在污染你的知识库之前就被标记；时间点快照让你无需重新处理即可回放历史。

---

## 实战教程：为受监管决策生成审计追踪
<a id="recipe-audit-trail-for-a-regulated-decision"></a>

这是构建在同一个上下文图之上的一种典型模式：记录一条因果相连的决策链，为每个实体挂上溯源，导出一份可直接提交监管机构的审计追踪。

```python
from semantica.context import ContextGraph
from semantica.provenance import ProvenanceManager
from semantica.export import RDFExporter

graph = ContextGraph(advanced_analytics=True)
prov  = ProvenanceManager(storage_path="./audit.db")

# Record the decision chain
d1 = graph.record_decision(
    category="drug_interaction_check", scenario="Patient P-4821: warfarin + amiodarone co-prescribed",
    reasoning="Amiodarone potentiates warfarin's anticoagulant effect", outcome="flag_for_review", confidence=0.91,
)
d2 = graph.record_decision(
    category="dosage_adjustment", scenario="INR monitoring plan for P-4821",
    reasoning="Reduce warfarin dose per interaction severity; recheck INR in 5 days", outcome="dose_reduced_30pct", confidence=0.87,
)
# relationship_type must be one of CAUSED, INFLUENCED, or PRECEDENT_FOR
graph.add_causal_relationship(d1, d2, relationship_type="CAUSED")

# Track provenance for every entity
prov.track_entity("patient_P4821", source="ehr/medication_orders_2024.json",
                  metadata={"extractor": "NamedEntityRecognizer"})

# Export W3C PROV-O for regulator submission - to_kg_dict() is the official
# adapter that emits the {"entities": [...], "relationships": [...]} /
# source_id shape RDFExporter expects, so no manual field mapping is needed
kg = graph.to_kg_dict()
RDFExporter().export(kg, "audit_trail.ttl", format="turtle")
```

更多实战教程（GraphRAG 流水线、AML 规则引擎、一趟完成本体到知识图谱）见下文 **[更多实战教程](#more-recipes)**。

---

## 探索平台

下面每个模块都可独立导入，示例代码均已对照当前源码树验证可运行；可以单用一个，也可以全部都用。

| 模块 | 功能 |
| --- | --- |
| [`semantica.ingest`](#semanticaingest-multi-source-ingestion) | 文件、Web、数据库、API、流、邮件、Git、Parquet、Databricks、Snowflake、MCP |
| [`semantica.semantic_extract`](#semanticasemantic_extract-ner-relations-events-triplets) | NER、关系抽取、事件检测、三元组生成 |
| [`semantica.kg`](#semanticakg-knowledge-graph-construction--analysis) | 图构建、中心性、社区、链接预测 |
| [`semantica.reasoning`](#semanticareasoning-forward-chaining-rete-datalog-sparql) | 前向链、Rete、Datalog、SPARQL，完全可解释 |
| [`semantica.vector_store`](#semanticavector_store-hybrid--filtered-semantic-search) | FAISS、Qdrant、Weaviate、Milvus、Pinecone、PgVector、混合检索 |
| [`semantica.split`](#semanticasplit-graphrag-native-document-chunking) | 面向 GraphRAG 的实体感知、关系感知、本体感知分块 |
| [`semantica.provenance`](#semanticaprovenance-w3c-prov-o-lineage) | 每条事实的 W3C PROV-O 血缘 |
| [`semantica.ontology`](#semanticaontology-owl-generation-shacl-validation) | OWL 生成、SHACL 校验、SKOS 词表 |
| [`semantica.conflicts`](#semanticaconflicts-conflict-detection--resolution) | 检测并解决跨来源的冲突事实 |
| [`semantica.deduplication`](#semanticadeduplication-entity-resolution-at-scale) | 大规模实体解析 |
| [`semantica.normalize`](#semanticanormalize-data-normalization--cleaning) | 文本、实体、日期与数字规范化；数据集清洗 |
| [`semantica.pipeline`](#semanticapipeline-pipeline-dsl) | 声明式并行流水线 DSL：摄取 → 抽取 → 建图 → 导出 |
| [`semantica.export`](#semanticaexport-rdf-owl-parquet-cypher-json-ld) | RDF、OWL、Parquet、Cypher、JSON-LD |
| [`semantica.visualization`](#semanticavisualization-interactive-graph-workbench) | 力导向图、本体层级、时态仪表盘 |
| [时态智能](#temporal-intelligence-bi-temporal-graphs--time-travel) | 双时态事实、Allen 区间代数、时间回溯 |
| [多智能体（Agno）](#multi-agent-shared-context-with-agno) | 团队所有智能体共享同一张上下文图 |

**↓ 展开下方 [模块参考](#module-reference)** 查看每个模块的可运行示例，或跳转到 [更多实战教程](#more-recipes)、完整 [集成](#integrations) 矩阵、[MCP 工具列表](#mcp-server) 和 [REST 端点](#rest-api)。

---

## 模块参考
<a id="module-reference"></a>

展开下面任意模块，查看其可运行示例。

<details>
<summary><b><code>semantica.ingest</code></b>：多源摄取</summary>
<a id="semanticaingest-multi-source-ingestion"></a>

通过统一接口，从文件、Web、数据库、API、流、邮件、Git 仓库、Parquet、Databricks、Snowflake 或 MCP 服务器摄取数据。

```python
from semantica.ingest import FileIngestor, WebIngestor, ParquetIngestor, DBIngestor

# Ingest an entire directory of contracts (PDF, DOCX, HTML, TXT)
docs = FileIngestor().ingest_directory("./contracts/", recursive=True)

# Ingest live web content with robots.txt compliance
pages = WebIngestor().ingest_url("https://example.com/reports/annual-2024.html")

# Ingest structured data from Parquet with Snappy compression
records = ParquetIngestor().ingest("./data/transactions.parquet")

# Ingest from a SQL database - specify which tables to pull
rows = DBIngestor().ingest_database(
    connection_string="postgresql://user:pass@localhost/mydb",
    include_tables=["customer_events"],
    max_rows_per_table=50_000,
)
```

```python
# Enterprise data platforms - pull tables straight out of your lakehouse
# or warehouse, with lineage, instead of exporting to CSV first
from semantica.ingest import DatabricksIngestor, SnowflakeIngestor

# pip install "semantica[db-databricks]"
databricks = DatabricksIngestor(
    host="https://adb-xxx.azuredatabricks.net",
    token="dapi-xxxxxxxx",              # or client_id/client_secret for OAuth M2M
    http_path="/sql/1.0/warehouses/xxxxxxxx",
    catalog="main",
)
customers    = databricks.ingest_table("customers", limit=10_000)
sales        = databricks.ingest_query("SELECT * FROM sales WHERE region = 'EMEA'")
table_lineage = databricks.get_table_lineage("customers", catalog="main", schema="default")  # Unity Catalog lineage

# pip install semantica[db-snowflake]
snowflake = SnowflakeIngestor(
    account="myaccount",
    user="myuser",
    password="mypassword",              # or private_key=... for key-pair; use authenticator="oauth", token=... for OAuth
    warehouse="COMPUTE_WH",
    database="MYDB",
)
orders = snowflake.ingest_table("ORDERS", limit=10_000)
```

> **安全提示：** 切勿在生产代码中硬编码凭证（`token`、`password`、`private_key`）；请通过环境变量（如 `DATABRICKS_TOKEN`、`SNOWFLAKE_PASSWORD`）或密钥管理器传入。

**支持的数据源：** 本地文件（PDF、DOCX、PPTX、HTML、TXT、CSV、JSON、YAML、Excel、XML）· 网页 · RSS/Atom 订阅 · REST API · 数据库（PostgreSQL、MySQL、SQLite、Oracle、SQL Server）· Parquet 数据集 · Databricks（Unity Catalog + Delta Lake）· Snowflake · Git 仓库 · 邮件（IMAP/POP3）· 消息流（Kafka、RabbitMQ、Kinesis、Pulsar）· MCP 资源 · Apache Arrow/Feather/IPC（`ArrowIngestor`）

DuckDB、Elasticsearch、Google Drive、HuggingFace、MongoDB 和 Pandas 摄取器也随包发布（`DuckDBIngestor`、`ElasticIngestor`、`GDriveIngestor`、`HuggingFaceIngestor`、`MongoIngestor`、`PandasIngestor`），但尚未从顶层 `semantica.ingest` 命名空间再导出——请直接导入：`from semantica.ingest.duckdb_ingestor import DuckDBIngestor`。

</details>

<details>
<summary><b><code>semantica.semantic_extract</code></b>：NER、关系、事件、三元组</summary>
<a id="semanticasemantic_extract-ner-relations-events-triplets"></a>

一趟从原始文本中抽取结构化知识。

```python
from semantica.semantic_extract import (
    NamedEntityRecognizer,
    RelationExtractor,
    EventDetector,
    TripletExtractor,
)

text = """
Anthropic CEO Dario Amodei announced a $7.3B Series E funding round in partnership
with Google and Spark Capital, valuing the company at $61.5B as of Q4 2024.
"""

# Named entity recognition with confidence thresholding
ner = NamedEntityRecognizer(confidence_threshold=0.7)
entities = ner.extract_entities(text)
# → [Entity(name="Dario Amodei", type="PERSON"), Entity(name="Anthropic", type="ORG"),
#    Entity(name="Google", type="ORG"), Entity(name="$7.3B", type="MONEY"), ...]

# Relationship extraction - bidirectional support
rel_extractor = RelationExtractor(confidence_threshold=0.6, bidirectional=True)
relations = rel_extractor.extract_relations(text, entities=entities)
# → [Relation(subject="Dario Amodei", predicate="ceo_of", object="Anthropic"),
#    Relation(subject="Anthropic", predicate="raised", object="$7.3B Series E"), ...]

# Event detection with temporal processing
events = EventDetector(extract_participants=True, extract_time=True).detect_events(text)
# → [Event(type="FUNDING", participants=["Anthropic","Google","Spark Capital"],
#          amount="$7.3B", date="Q4 2024")]

# RDF triplets with optional provenance metadata
triplets = TripletExtractor(include_temporal=True, include_provenance=True).extract_triplets(text)
# → [("Anthropic", "valuation", "$61.5B"), ("Dario Amodei", "is_ceo_of", "Anthropic"), ...]
```

跨多个文档的批处理使用 `ner.process_batch([...])`，而不是在门面类上逐次调用 `extract_entities_batch`。

</details>

<details>
<summary><b><code>semantica.kg</code></b>：知识图谱构建与分析</summary>
<a id="semanticakg-knowledge-graph-construction--analysis"></a>

从文档构建生产级知识图谱，并在其上运行图算法。

```python
from semantica.ingest import FileIngestor
from semantica.kg import (
    GraphBuilder,
    GraphAnalyzer,
    CentralityCalculator,
    CommunityDetector,
    PathFinder,
    LinkPredictor,
    BiTemporalFact,
)
from datetime import datetime

# Build KG - merge duplicate entities, track temporal edges
sources = FileIngestor().ingest_directory("./contracts/", recursive=True)
kg = GraphBuilder(merge_entities=True, enable_temporal=True).build(sources)

# Graph analytics
analyzer    = GraphAnalyzer()
analysis    = analyzer.analyze_graph(kg)             # full graph metrics

centrality  = CentralityCalculator()
degree      = centrality.calculate_degree_centrality(kg)    # most-connected entities
betweenness = centrality.calculate_betweenness_centrality(kg)

communities = CommunityDetector().detect_communities(kg, method="louvain")  # natural clusters
path        = PathFinder().find_shortest_path(kg, "alice_chen", "contract_001")
predictions = LinkPredictor().predict_links(kg, top_k=10)   # relationship predictions

# Bi-temporal facts - track valid time vs. recorded time independently
fact = BiTemporalFact(
    valid_from=datetime(2024, 3, 1),
    valid_until=datetime(2025, 1, 1),
    recorded_at=datetime(2024, 3, 5),
)
```

</details>

<details>
<summary><b><code>semantica.reasoning</code></b>：前向链、Rete、Datalog、SPARQL</summary>
<a id="semanticareasoning-forward-chaining-rete-datalog-sparql"></a>

运行可解释的规则推理，而不是黑盒。

```python
from semantica.reasoning import ReteEngine, Rule, Fact, RuleType

rete = ReteEngine()
rete.build_network([
    Rule(
        rule_id="aml_flag",
        name="Flag high-risk transactions",
        conditions=[
            {"field": "amount",  "operator": ">",  "value": 10_000},
            {"field": "country", "operator": "in", "value": ["IR", "KP", "SY"]},
        ],
        conclusion="flag_for_compliance_review",
        rule_type=RuleType.IMPLICATION,
    ),
    Rule(
        rule_id="velocity_check",
        name="Flag rapid sequential transfers",
        conditions=[
            {"field": "transfers_in_1h", "operator": ">", "value": 5},
            {"field": "total_amount",    "operator": ">", "value": 50_000},
        ],
        conclusion="flag_velocity_breach",
        rule_type=RuleType.IMPLICATION,
    ),
])

rete.add_fact(Fact("tx_001", "transaction", [{"amount": 15_000, "country": "IR"}]))
flagged = rete.match_patterns()
# → [{"rule": "aml_flag", "matched_facts": ["tx_001"], "conclusion": "flag_for_compliance_review"}]
```

> **当前限制：** 本版本中 `ReteEngine` 的 alpha 节点条件匹配器是有意保持简单的——在把它接入生产合规闸门之前，请用你实际的规则集验证 `match_patterns()` 的输出；更具选择性的条件求值已在路线图上。

```python
# Recursive Datalog - natural language for graph queries
from semantica.reasoning import DatalogReasoner

engine = DatalogReasoner()
engine.add_fact("parent(tom, bob)")
engine.add_fact("parent(bob, ann)")
engine.add_fact("parent(ann, pat)")
engine.add_rule("ancestor(X, Y) :- parent(X, Y).")
engine.add_rule("ancestor(X, Z) :- parent(X, Y), ancestor(Y, Z).")
ancestors = engine.query("ancestor(tom, ?X)")
# → [{"X": "bob"}, {"X": "ann"}, {"X": "pat"}]
```

```python
# Explainable reasoning - trace the path, not just the answer
from semantica.reasoning import ExplanationGenerator, Reasoner

reasoner = Reasoner()
reasoner.add_fact("parent(tom, bob)")
reasoner.add_rule("ancestor(X, Y) :- parent(X, Y)")
result = reasoner.forward_chain()

explainer = ExplanationGenerator()
explanation = explainer.generate_explanation(result)
# → Explanation(conclusion="...", steps=[ReasoningStep(...)], justification=Justification(...))
```

</details>

<details>
<summary><b><code>semantica.vector_store</code></b>：混合与过滤语义搜索</summary>
<a id="semanticavector_store-hybrid--filtered-semantic-search"></a>

开箱即用的向量存储，支持多种后端、混合检索与决策感知检索。

```python
from semantica.vector_store import VectorStore, HybridSearch

# In-memory backend shown here: HybridSearch and explain_decision() work out of the box.
# Swap backend="qdrant" / "weaviate" / "milvus" / "pinecone" / "pgvector" / "faiss" once you
# scale past a single process — search() and store_decision() work identically on all of them.
vs = VectorStore(backend="inmemory", dimension=1536)

# Store a decision with scenario description and outcome
vs.store_decision(
    scenario="Personal loan A-7291, $85k income, 31% DTI, 3yr employment",
    outcome="approved",
    confidence=0.94,
    category="loan_underwriting",
)

# Semantic similarity search
results = vs.search(
    query="personal loan approval with low DTI",
    limit=10,
)

# Hybrid search - dense + sparse retrieval in one pass with RRF fusion
hs   = HybridSearch(vector_store=vs)
hits = hs.search("high-risk transactions 2024")

# Explain why a decision was retrieved
explanation = vs.explain_decision(results[0]["id"])
```

**后端：** `faiss` · `qdrant` · `weaviate` · `milvus` · `pinecone` · `pgvector` · `sqlite` · `inmemory`

</details>

<details>
<summary><b><code>semantica.split</code></b>：GraphRAG 原生文档分块</summary>
<a id="semanticasplit-graphrag-native-document-chunking"></a>

保留实体边界、关系三元组与本体概念的知识图谱感知切分，是 GraphRAG 流水线的关键。

```python
from semantica.split import TextSplitter, EntityAwareChunker, RelationAwareChunker

text = open("contracts/master_agreement.txt").read()

# Standard recursive chunking
chunks = TextSplitter(method="recursive", chunk_size=1000, chunk_overlap=200).split(text)

# Entity-aware chunking - never splits a named entity across chunks (GraphRAG)
chunks = TextSplitter(method="entity_aware", ner_method="llm", chunk_size=1000).split(text)

# Relation-aware chunking - preserves (subject, predicate, object) triplets intact
chunks = RelationAwareChunker(chunk_size=1000, preserve_triplets=True).chunk(text)

# Graph-based chunking - uses centrality to find natural community boundaries
chunks = TextSplitter(method="graph_based", chunk_size=1000).split(text)

# Hierarchical chunking - multi-level (section → paragraph → sentence)
chunks = TextSplitter(method="hierarchical", levels=["section", "paragraph"]).split(text)
```

**支持的方法：** `recursive` · `token` · `sentence` · `paragraph` · `semantic_transformer` · `entity_aware` · `relation_aware` · `graph_based` · `ontology_aware` · `hierarchical` · `community_detection` · `centrality_based` · `llm`

</details>

<details>
<summary><b><code>semantica.provenance</code></b>：W3C PROV-O 血缘</summary>
<a id="semanticaprovenance-w3c-prov-o-lineage"></a>

每条事实都链接到它的来源。没有黑盒，没有来历不明的输出。

```python
from semantica.provenance import ProvenanceManager

prov = ProvenanceManager(storage_path="./provenance.db")

# Track where every entity came from
prov.track_entity(
    entity_id="acme_corp",
    source="contracts/acme_master_agreement_2024.pdf",
    metadata={"page": 1, "confidence": 0.97, "extractor": "NamedEntityRecognizer"},
)

# Track a relationship's provenance - entity linkage travels in metadata
prov.track_relationship(
    relationship_id="alice_works_for_acme",
    source="hr_records/employees_q1_2024.csv",
    metadata={"source_entity_id": "alice_chen", "target_entity_id": "acme_corp"},
)

# Answer "where did this come from?"
lineage = prov.get_lineage("acme_corp")
trail   = prov.trace_lineage("alice_chen")   # full ancestor chain
entry   = prov.get_provenance("acme_corp")
```

</details>

<details>
<summary><b><code>semantica.ontology</code></b>：OWL 生成、SHACL 校验</summary>
<a id="semanticaontology-owl-generation-shacl-validation"></a>

从数据生成本体、校验形状(Shape)、管理你的词表。

```python
from semantica.ontology import OntologyGenerator, OntologyValidator

data = {
    "entities": [
        {"id": "acme_corp",  "type": "Organization", "industry": "SaaS", "founded": 2012},
        {"id": "alice_chen", "type": "Person",        "role": "CTO",     "since": 2019},
    ],
    "relationships": [
        {"source": "alice_chen", "target": "acme_corp", "type": "works_for"},
    ],
}

gen       = OntologyGenerator(base_uri="https://semantica.dev/ontology/")
ontology  = gen.generate_ontology(data)
classes   = gen.infer_classes(data)
props     = gen.infer_properties(data, classes)
optimized = gen.optimize_ontology(ontology)

# Validate against SHACL shapes
validator = OntologyValidator()
report    = validator.validate(ontology)
# → ValidationResult(valid=True, consistent=True, satisfiable=True, errors=[], warnings=[])
```

</details>

<details>
<summary><b><code>semantica.conflicts</code></b>：冲突检测与解决</summary>
<a id="semanticaconflicts-conflict-detection--resolution"></a>

在来自多个来源的冲突事实污染你的知识库之前，检测并解决它们。

```python
from semantica.conflicts import ConflictDetector, ConflictResolver, SourceTracker

entities_from_source_a = [
    {"id": "alice_chen", "role": "CTO",   "salary": 250_000, "start_date": "2019-03-01"},
]
entities_from_source_b = [
    {"id": "alice_chen", "role": "VP Eng", "salary": 275_000, "start_date": "2019-03-01"},
]

# Detect all conflict types: value, type, relationship, temporal, logical
detector   = ConflictDetector()
conflicts  = detector.detect_conflicts(entities_from_source_a + entities_from_source_b)
# → [Conflict(entity="alice_chen", field="role",   values=["CTO","VP Eng"], severity="HIGH"),
#    Conflict(entity="alice_chen", field="salary",  values=[250000,275000],   severity="MEDIUM")]

# Resolve using multiple strategies
resolver = ConflictResolver()
resolved = resolver.resolve_conflicts(conflicts, strategy="credibility_weighted")  # weighted by source trust
resolved = resolver.resolve_conflicts(conflicts, strategy="most_recent")          # prefer most recent
resolved = resolver.resolve_conflicts(conflicts, strategy="voting")               # majority wins

# Track source credibility over time
tracker = SourceTracker()
tracker.register_source("source_a", source_type="document", credibility_score=0.85)
tracker.register_source("source_b", source_type="document", credibility_score=0.72)
```

</details>

<details>
<summary><b><code>semantica.deduplication</code></b>：大规模实体解析</summary>
<a id="semanticadeduplication-entity-resolution-at-scale"></a>

用语义相似度进行分块、聚类并合并重复项。

```python
from semantica.deduplication import DuplicateDetector, EntityMerger

entities = [
    {"id": "e1", "name": "Acme Corporation",  "domain": "acme.com"},
    {"id": "e2", "name": "Acme Corp.",         "domain": "acme.com"},
    {"id": "e3", "name": "ACME Corp",          "domain": "acme.co"},
    {"id": "e4", "name": "Globex Industries",  "domain": "globex.com"},
]

detector   = DuplicateDetector(similarity_threshold=0.75, use_clustering=True)
candidates = detector.detect_duplicates(entities)
groups     = detector.detect_duplicate_groups(entities)
# → DuplicateGroup(entities=["e1","e2","e3"], confidence=0.91, strategy="semantic+blocking")

merger  = EntityMerger(preserve_provenance=True)
ops     = merger.merge_duplicates(entities, strategy="keep_most_complete")
history = merger.get_merge_history()
```

</details>

<details>
<summary><b><code>semantica.normalize</code></b>：数据规范化与清洗</summary>
<a id="semanticanormalize-data-normalization--cleaning"></a>

在构建知识图谱之前，标准化文本、实体、日期、数字与编码。

```python
from semantica.normalize import (
    TextNormalizer,
    EntityNormalizer,
    DateNormalizer,
    NumberNormalizer,
    DataCleaner,
)

# Unicode, whitespace, casing, HTML tags, smart quotes
text  = TextNormalizer().normalize("  Acme Corp.'s Q4 report...  ")
# → "Acme Corp.'s Q4 report..."

# Alias resolution + entity disambiguation with confidence scores
canonical = EntityNormalizer().normalize_entity("ACME Corp.")
# → NormalizedEntity(canonical="Acme Corporation", type="Organization", confidence=0.91)

# Natural language date parsing with timezone conversion
dt    = DateNormalizer().normalize_date("3 weeks ago")
# → datetime(2026, 7, 1, tzinfo=UTC)

# Unit conversion and currency normalization
price = NumberNormalizer().normalize_number("$1.25M USD")
# → NormalizedNumber(value=1_250_000, currency="USD")

# Deduplicate, validate, and impute missing values across a dataset
clean = DataCleaner().clean_data(records, remove_duplicates=True, handle_missing=True)
```

</details>

<details>
<summary><b><code>semantica.pipeline</code></b>：流水线 DSL</summary>
<a id="semanticapipeline-pipeline-dsl"></a>

把摄取、抽取和建图组合成声明式的并行流水线。

```python
from semantica.pipeline import PipelineBuilder, ExecutionEngine

builder = PipelineBuilder()

# add_step() returns the created PipelineStep, not the builder, so these don't chain
builder.add_step("ingest",      step_type="ingest",           source="./contracts/", recursive=True)
builder.add_step("extract",     step_type="ner_extract")
builder.add_step("relations",   step_type="relation_extract")
builder.add_step("build_kg",    step_type="kg_build",         merge_entities=True)
builder.add_step("deduplicate", step_type="deduplicate",      threshold=0.75)
builder.add_step("export",      step_type="export",           format="turtle", output="kg.ttl")

# connect_steps() and set_parallelism() return the builder, so these do chain
pipeline = (
    builder
    .connect_steps("ingest",      "extract")
    .connect_steps("extract",     "relations")
    .connect_steps("relations",   "build_kg")
    .connect_steps("build_kg",    "deduplicate")
    .connect_steps("deduplicate", "export")
    .set_parallelism(4)
    .build(name="contracts_pipeline")
)

engine   = ExecutionEngine()
result   = engine.execute_pipeline(pipeline)
status   = engine.get_pipeline_status(pipeline.name)
progress = engine.get_progress(pipeline.name)
```

</details>

<details>
<summary><b>时态智能</b>：双时态图与时间回溯</summary>
<a id="temporal-intelligence-bi-temporal-graphs--time-travel"></a>

追踪事实*在现实世界中*何时成立，与*何时被记录*，并可沿任一轴查询。

```python
from semantica.context import ContextGraph
from semantica.kg import (
    BiTemporalFact,
    TemporalGraphQuery,
    TemporalNormalizer,
)
from datetime import datetime

graph = ContextGraph(advanced_analytics=True)
graph.add_node("alice_chen", "Person",       role="VP Engineering")
graph.add_node("acme_corp",  "Organization", valuation=1_200_000_000)

# A temporally-bounded edge - valid_from/valid_until define when it held true
graph.add_edge(
    "alice_chen", "acme_corp", edge_type="works_for",
    valid_from="2024-03-01T00:00:00", valid_until="2025-01-01T00:00:00",
)

# Point-in-time snapshots - replay history without reprocessing
snapshot_2023 = graph.state_at("2023-06-01")
snapshot_2024 = graph.state_at("2024-01-01")

# Bi-temporal facts - valid_time is when true in the world;
# recorded_at is when you learned about it
fact = BiTemporalFact(
    valid_from=datetime(2024, 3, 1),
    valid_until=datetime(2025, 1, 1),
    recorded_at=datetime(2024, 3, 5),
)

# Query facts valid within a time window - to_kg_dict() is the official
# adapter that emits {"entities", "relationships"} with source_id/target_id
# keys, the shape query_time_range() expects (no manual mapping required)
kg = graph.to_kg_dict()

tq = TemporalGraphQuery()
facts_in_window = tq.query_time_range(
    kg, query="valid_facts", start_time="2024-01-01", end_time="2024-12-31"
)

# Normalize natural language temporal expressions - returns a (start, end) range
norm = TemporalNormalizer()
start, end = norm.normalize("last quarter")
```

</details>

<details>
<summary><b><code>semantica.export</code></b>：RDF、OWL、Parquet、Cypher、JSON-LD</summary>
<a id="semanticaexport-rdf-owl-parquet-cypher-json-ld"></a>

导出为监管机构、图数据库或下游系统要求的任何格式。

```python
from semantica.export import (
    RDFExporter,
    JSONExporter,
    ParquetExporter,
    LPGExporter,
    ReportGenerator,
)

kg = {"entities": [...], "relationships": [...]}

rdf = RDFExporter()
turtle_str = rdf.export_to_rdf(kg, format="turtle")     # returns string
jsonld_str = rdf.export_to_rdf(kg, format="json-ld")

rdf.export(kg, "kg_audit.ttl",    format="turtle")
rdf.export(kg, "kg_audit.jsonld", format="json-ld")
rdf.export(kg, "kg_audit.nt",     format="n-triples")

# Columnar analytics - Snappy-compressed Parquet (writes kg_snapshot_entities.parquet
# and kg_snapshot_relationships.parquet)
ParquetExporter(compression="snappy").export_knowledge_graph(kg, "kg_snapshot")

# JSON knowledge graph
JSONExporter().export_knowledge_graph(kg, "kg.json")

# Neo4j / Memgraph Cypher statements for graph database import
LPGExporter().export(kg, "kg_import.cypher")

# Human-readable HTML report
ReportGenerator().generate_report(
    {"title": "KG Audit Report", "summary": "Weekly ingestion summary", "metrics": {"entities": len(kg["entities"])}},
    file_path="audit_report.html",
    format="html",
)
```

</details>

<details>
<summary><b><code>semantica.visualization</code></b>：交互式图工作台</summary>
<a id="semanticavisualization-interactive-graph-workbench"></a>

渲染力导向图、社区图、本体层级与时态仪表盘。

```python
from semantica.visualization import (
    KGVisualizer,
    OntologyVisualizer,
    EmbeddingVisualizer,
    TemporalVisualizer,
)
import numpy as np

kg = {"entities": [...], "relationships": [...]}

# Interactive force-directed graph (opens in browser)
viz = KGVisualizer(layout="force", color_scheme="default")
viz.visualize_network(kg, output="interactive", file_path="kg.html")
viz.visualize_communities(kg, communities, output="interactive")
viz.visualize_centrality(kg, centrality, centrality_type="degree")
viz.visualize_entity_types(kg, output="html", file_path="entity_types.html")

# Ontology class hierarchy
OntologyVisualizer().visualize_hierarchy(ontology, output="interactive")

# 2D embedding projection (UMAP / t-SNE / PCA)
EmbeddingVisualizer().visualize_2d_projection(
    embeddings=np.array([...]),
    labels=["entity_a", "entity_b"],
    method="umap",
)

# Timeline scrubber - watch the graph evolve
TemporalVisualizer().visualize_timeline(kg, output="interactive")
```

</details>

<details>
<summary><b>基于 Agno 的多智能体(Multi-Agent)共享上下文</b></summary>
<a id="multi-agent-shared-context-with-agno"></a>

一个共享智能层。所有智能体读写同一张上下文图。

```python
# pip install semantica[agno]
from agno.agent import Agent
from agno.team import Team
from agno.models.anthropic import Claude
from semantica.context import ContextGraph
from semantica.vector_store import VectorStore
from integrations.agno import AgnoSharedContext, AgnoDecisionKit, AgnoKGToolkit

shared = AgnoSharedContext(
    vector_store=VectorStore(backend="faiss"),
    knowledge_graph=ContextGraph(advanced_analytics=True),
    decision_tracking=True,
)

researcher = Agent(
    name="Researcher",
    model=Claude(id="claude-sonnet-4-5"),
    memory=shared.bind_agent("researcher"),
    tools=[AgnoKGToolkit(context=shared)],
)
analyst = Agent(
    name="Analyst",
    model=Claude(id="claude-sonnet-4-5"),
    memory=shared.bind_agent("analyst"),
    tools=[AgnoDecisionKit(context=shared)],
)

team = Team(agents=[researcher, analyst], mode="coordinate")
# Researcher's findings are instantly available to the Analyst - no copy, no sync
```

→ [cookbook 中可运行的 notebook](https://github.com/semantica-agi/semantica/tree/main/cookbook)，每个都自成一体，5 分钟内可跑完

</details>

---

## 更多实战教程
<a id="more-recipes"></a>

审计追踪教程见[上文](#recipe-audit-trail-for-a-regulated-decision)。这里再给出三个常见模式。

<details>
<summary><b>端到端 GraphRAG 流水线</b></summary>

```python
from semantica.ingest import FileIngestor
from semantica.split import TextSplitter
from semantica.semantic_extract import NamedEntityRecognizer, RelationExtractor
from semantica.kg import GraphBuilder
from semantica.vector_store import VectorStore, HybridSearch
from semantica.context import AgentContext

# 1. Ingest
docs = FileIngestor().ingest_directory("./docs/", recursive=True)

# 2. Entity-aware chunking - never splits an entity across a chunk boundary
splitter = TextSplitter(method="entity_aware", chunk_size=1000)
chunks   = [splitter.split(doc["text"]) for doc in docs]

# 3. Extract entities and relations
ner      = NamedEntityRecognizer(confidence_threshold=0.7)
rel_ext  = RelationExtractor(confidence_threshold=0.6)
entities = [ner.extract_entities(chunk) for chunk_group in chunks for chunk in chunk_group]

# 4. Build KG
kg = GraphBuilder(merge_entities=True, enable_temporal=True).build(docs)

# 5. Hybrid retrieval
vs  = VectorStore(backend="inmemory")
ctx = AgentContext(vector_store=vs, knowledge_graph=kg)
ctx.store("Alice approved the Acme renewal in Q1 2024", conversation_id="c1")

results = HybridSearch(vector_store=vs).search("who approved the renewal?")
```

</details>

<details>
<summary><b>反洗钱(AML)规则引擎</b></summary>

```python
from semantica.reasoning import ReteEngine, Rule, Fact, RuleType

rete = ReteEngine()
rete.build_network([
    Rule(
        rule_id="sanctions_check",
        name="Flag sanctioned-country transactions",
        conditions=[
            {"field": "amount",  "operator": ">",  "value": 10_000},
            {"field": "country", "operator": "in", "value": ["IR", "KP", "SY", "CU"]},
        ],
        conclusion="flag_for_compliance_review",
        rule_type=RuleType.IMPLICATION,
    ),
])

# Run the rule across a batch of incoming transactions, not just one
for tx in [
    Fact("tx_101", "transaction", [{"amount": 25_000, "country": "IR"}]),
    Fact("tx_102", "transaction", [{"amount": 4_500,  "country": "DE"}]),
    Fact("tx_103", "transaction", [{"amount": 60_000, "country": "KP"}]),
]:
    rete.add_fact(tx)

flagged = rete.match_patterns()
```

与[上文](#semanticareasoning-forward-chaining-rete-datalog-sparql)相同的条件匹配器注意事项在此同样适用——生产使用前请对照你的规则集验证。

</details>

<details>
<summary><b>一趟完成本体到知识图谱</b></summary>

```python
from semantica.ingest import FileIngestor
from semantica.semantic_extract import NamedEntityRecognizer, RelationExtractor
from semantica.kg import GraphBuilder
from semantica.ontology import OntologyGenerator, OntologyValidator
from semantica.export import RDFExporter

sources   = FileIngestor().ingest_directory("./contracts/")
ner       = NamedEntityRecognizer(confidence_threshold=0.7)
entities  = ner.process_batch([s["text"] for s in sources])

kg  = GraphBuilder(merge_entities=True).build(sources)
gen = OntologyGenerator(base_uri="https://myco.dev/ontology/")
ont = gen.generate_ontology({"entities": entities[0], "relationships": []})

report = OntologyValidator().validate(ont)
if report.valid:
    RDFExporter().export({"entities": entities[0]}, "ontology.ttl", format="turtle")
```

</details>

---

## 功能一览

| 能力 | 亮点 |
| --- | --- |
| **上下文图** | 实体、决策、关系的可查询图；因果链接；跨图导航 |
| **决策智能** | `record_decision` · `trace_decision_chain` · `find_similar_decisions` · `analyze_decision_impact` · `check_decision_rules` |
| **时态智能** | 时间点快照 · Allen 区间代数（13 种关系）· `TemporalNormalizer` · 双时态溯源 |
| **距离智能** | N×N 语义距离矩阵 · 自我中心(Ego)模式可视化 · 距离带 · 嵌入缓存 |
| **语义抽取** | NER · 关系抽取 · 事件检测 · 三元组生成 · 共指消解 |
| **推理引擎** | 前向链 · Rete · 演绎 · 溯因 · SPARQL · Datalog，输出可解释 |
| **GraphRAG 分块** | 实体感知 · 关系感知 · 基于图 · 本体感知 · 社区检测分块 |
| **冲突检测** | 值 / 类型 / 关系 / 时态 / 逻辑冲突 · 多种解决策略 |
| **溯源** | W3C PROV-O · 每条事实追溯到来源 · 审计日志导出 JSON/CSV/RDF |
| **本体中心** | SHACL Studio · 可视化编辑器 · 跨本体对齐 · 健康仪表盘 |
| **向量存储** | FAISS · Pinecone · Weaviate · Qdrant · Milvus · PgVector · 混合 + 过滤检索 |
| **图数据库（LPG）** | Neo4j · FalkorDB · Apache AGE · AWS Neptune |
| **三元组存储（RDF）** | Oxigraph（内嵌）· Blazegraph · Apache Jena · Eclipse RDF4J · 统一 `TripletStore` 接口 · SPARQL 查询与批量加载 |
| **企业数据平台** | Databricks（`DatabricksIngestor`：Unity Catalog + Delta Lake，PAT/OAuth M2M，表/查询摄取，目录/模式/表/血缘内省）· Snowflake（`SnowflakeIngestor`：数仓/数据库/模式，密码/密钥对/OAuth 认证） |
| **LLM 提供商** | **目前全部已支持：** OpenAI（GPT-4o、o1、o3）· Anthropic（Claude）· Google Gemini · Mistral · Meta Llama · Groq · Cohere · Azure OpenAI · AWS Bedrock · Ollama · DeepSeek · Perplexity · Together AI · Fireworks AI · Replicate · HuggingFace · 通过 `semantica.llms` 与 LiteLLM |

---

## 性能
<a id="performance"></a>

基于 v0.5.0、在 118,000 节点生产图上测得的基准数据：

| 操作 | 优化前 | 优化后 | 提升 |
| --- | --- | --- | --- |
| 节点搜索（11.8 万节点） | 24 ms | 0.004 ms | **快 6,000 倍** |
| 嵌入缓存命中 | 冷加载 | 基于修订的缓存 | **吞吐量提升 10 倍** |
| 语义去重 | 基线 | 优化候选生成 | **快 6.98 倍** |
| 候选生成 | 基线 | 分块(Blocking)策略 | **快 63.6%** |

*在 118,000 节点生产图（AMD EPYC，64 GB 内存）上测得；去重/候选生成数字是记录在 [CHANGELOG.md](CHANGELOG.md) 中的历史测量值，而非 `tests/` 中的自动化断言。结果会因硬件、数据集拓扑和后端选择而异——运行 `pytest tests/vector_store/test_performance_benchmarks.py -s` 可在你自己的数据上测量。*

---

## CLI
<a id="cli"></a>

每一项能力都可以在终端中使用。CLI 随包发布，无需单独安装。

```bash
pip install semantica
semantica        # startup dashboard
semantica doctor # health check
semantica --help # full grouped command reference
```

从 `semantica` 开始，用 `doctor` 验证，构建一张图，在一个终端里探索各命令组。

**命令组：** `ingest` · `parse` · `extract` · `kg` · `reason` · `decision` · `temporal` · `provenance` · `ontology` · `embed` · `deduplicate` · `validate` · `export` · `visualize` · `pipeline` · `server` · `explorer` · `mcp` · `doctor` · `shell` · `init` · `watch`

→ [完整 CLI 参考](https://docs.getsemantica.ai/)

---

## 集成
<a id="integrations"></a>

为 Claude Code、Cursor、Codex、Windsurf、Cline、Continue、VS Code 和 OpenClaw 提供原生插件包；为任何 MCP 兼容客户端提供功能完整的 MCP 服务器；全面的 REST API；以及对智能体框架 Agno、CrewAI、LangChain 的一流支持。所有主流 LLM 提供商均已通过 `semantica.llms` 和 LiteLLM 获得支持：OpenAI、Anthropic、Gemini、Mistral、Llama、Groq、Cohere、Azure、Bedrock、Ollama、DeepSeek、HuggingFace 等。

MCP 配置只需 30 秒——见下文 [MCP 服务器](#mcp-server)。

<details>
<summary><b>完整集成矩阵</b>（编辑器、MCP 客户端、REST 客户端、智能体框架）</summary>

<table>
<tr>
<th colspan="3" align="left">原生插件包</th>
<th colspan="5" align="left">MCP 服务器 + 插件</th>
</tr>
<tr>
<td align="center" width="12.5%">
<a href="https://claude.com/product/claude-code"><img src="https://github.com/anthropics.png?size=120" alt="Claude Code" width="48" height="48" /></a><br/>
<strong>Claude Code</strong><br/>
<sub>技能 · 智能体 · 钩子</sub>
</td>
<td align="center" width="12.5%">
<a href="https://cursor.com"><img src="https://www.freelogovectors.net/wp-content/uploads/2025/06/cursor-logo-freelogovectors.net_.png" alt="Cursor" width="48" height="48" /></a><br/>
<strong>Cursor</strong><br/>
<sub>技能 · 智能体</sub>
</td>
<td align="center" width="12.5%">
<a href="https://github.com/openai/codex"><img src="https://github.com/openai.png?size=120" alt="Codex CLI" width="48" height="48" /></a><br/>
<strong>Codex CLI</strong><br/>
<sub>技能 · 智能体</sub>
</td>
<td align="center" width="12.5%">
<a href="https://windsurf.com"><img src="https://exafunction.github.io/public/brand/windsurf-black-symbol.svg" alt="Windsurf" width="48" height="48" /></a><br/>
<strong>Windsurf</strong><br/>
<sub><a href="plugins/.windsurf-plugin/">插件</a></sub>
</td>
<td align="center" width="12.5%">
<a href="https://github.com/cline/cline"><img src="https://github.com/cline.png?size=120" alt="Cline" width="48" height="48" /></a><br/>
<strong>Cline</strong><br/>
<sub><a href="plugins/.cline-plugin/">插件</a></sub>
</td>
<td align="center" width="12.5%">
<a href="https://github.com/continuedev/continue"><img src="https://github.com/continuedev.png?size=120" alt="Continue" width="48" height="48" /></a><br/>
<strong>Continue</strong><br/>
<sub><a href="plugins/.continue-plugin/">插件</a></sub>
</td>
<td align="center" width="12.5%">
<a href="https://github.com/microsoft/vscode"><img src="https://github.com/microsoft.png?size=120" alt="VS Code" width="48" height="48" /></a><br/>
<strong>VS Code</strong><br/>
<sub><a href="plugins/.vscode-plugin/">插件</a></sub>
</td>
<td align="center" width="12.5%">
<a href="integrations/openclaw/"><img src="https://github.com/openclaw.png?size=120" alt="OpenClaw" width="48" height="48" /></a><br/>
<strong>OpenClaw</strong><br/>
<sub>MCP + <a href="integrations/openclaw/">插件</a></sub>
</td>
</tr>
<tr>
<th colspan="1" align="left">MCP 服务器</th>
<th colspan="7" align="left">REST API</th>
</tr>
<tr>
<td align="center" width="12.5%">
<a href="https://claude.ai/download"><img src="https://github.com/anthropics.png?size=120" alt="Claude Desktop" width="48" height="48" /></a><br/>
<strong>Claude Desktop</strong><br/>
<sub>MCP 服务器</sub>
</td>
<td align="center" width="12.5%">
<a href="https://github.com/features/copilot"><img src="https://github.com/github.png?size=120" alt="GitHub Copilot" width="48" height="48" /></a><br/>
<strong>GitHub Copilot</strong><br/>
<sub>REST API</sub>
</td>
<td align="center" width="12.5%">
<a href="https://github.com/RooCodeInc/Roo-Code"><img src="https://github.com/RooCodeInc.png?size=120" alt="Roo Code" width="48" height="48" /></a><br/>
<strong>Roo Code</strong><br/>
<sub>REST API</sub>
</td>
<td align="center" width="12.5%">
<a href="https://github.com/block/goose"><img src="https://github.com/block.png?size=120" alt="Goose" width="48" height="48" /></a><br/>
<strong>Goose</strong><br/>
<sub>REST API</sub>
</td>
<td align="center" width="12.5%">
<a href="https://github.com/Kilo-Org/kilocode"><img src="https://github.com/Kilo-Org.png?size=120" alt="Kilo Code" width="48" height="48" /></a><br/>
<strong>Kilo Code</strong><br/>
<sub>REST API</sub>
</td>
<td align="center" width="12.5%">
<a href="https://github.com/Aider-AI/aider"><img src="https://github.com/Aider-AI.png?size=120" alt="Aider" width="48" height="48" /></a><br/>
<strong>Aider</strong><br/>
<sub>REST API</sub>
</td>
<td align="center" width="12.5%">
<a href="https://github.com/aws/amazon-q-developer-cli"><img src="https://github.com/aws.png?size=120" alt="Amazon Q" width="48" height="48" /></a><br/>
<strong>Amazon Q</strong><br/>
<sub>REST API</sub>
</td>
<td align="center" width="12.5%">
<a href="https://zed.dev"><img src="https://github.com/zed-industries.png?size=120" alt="Zed" width="48" height="48" /></a><br/>
<strong>Zed</strong><br/>
<sub>REST API</sub>
</td>
</tr>
</table>

### 智能体框架

<table>
<tr>
<th colspan="8" align="left">原生集成</th>
</tr>
<tr>
<td align="center" width="12.5%">
<a href="https://github.com/agno-agi/agno"><img src="https://github.com/agno-agi.png?size=120" alt="Agno" width="48" height="48" /></a><br/>
<strong>Agno</strong><br/>
<sub>一流支持 · <code>pip install semantica[agno]</code></sub>
</td>
<td align="center" width="12.5%">
<a href="https://github.com/crewAIInc/crewAI"><img src="https://github.com/crewAIInc.png?size=120" alt="CrewAI" width="48" height="48" /></a><br/>
<strong>CrewAI</strong><br/>
<sub>一流支持 · <code>pip install semantica[crewai]</code></sub>
</td>
<td align="center" width="12.5%">
<a href="https://github.com/langchain-ai/langchain"><img src="https://github.com/langchain-ai.png?size=120" alt="LangChain" width="48" height="48" /></a><br/>
<strong>LangChain</strong><br/>
<sub>一流支持 · <code>pip install semantica[langchain]</code></sub>
</td>
</tr>
<tr>
<th colspan="8" align="left">已通过 REST API 与 MCP 支持</th>
</tr>
<tr>
<td align="center" width="12.5%">
<a href="https://github.com/langchain-ai/langgraph"><img src="https://github.com/langchain-ai.png?size=120" alt="LangGraph" width="48" height="48" /></a><br/>
<strong>LangGraph</strong><br/>
<sub>REST API · MCP</sub>
</td>
<td align="center" width="12.5%">
<a href="https://github.com/run-llama/llama_index"><img src="https://github.com/run-llama.png?size=120" alt="LlamaIndex" width="48" height="48" /></a><br/>
<strong>LlamaIndex</strong><br/>
<sub>REST API · MCP</sub>
</td>
<td align="center" width="12.5%">
<a href="https://github.com/microsoft/autogen"><img src="https://github.com/microsoft.png?size=120" alt="AutoGen" width="48" height="48" /></a><br/>
<strong>AutoGen</strong><br/>
<sub>REST API · MCP</sub>
</td>
<td align="center" width="12.5%">
<a href="https://github.com/openai/openai-agents-python"><img src="https://github.com/openai.png?size=120" alt="OpenAI Agents SDK" width="48" height="48" /></a><br/>
<strong>OpenAI Agents</strong><br/>
<sub>REST API · MCP</sub>
</td>
<td align="center" width="12.5%">
<a href="https://github.com/google/adk-python"><img src="https://github.com/google.png?size=120" alt="Google ADK" width="48" height="48" /></a><br/>
<strong>Google ADK</strong><br/>
<sub>REST API · MCP</sub>
</td>
</tr>
<tr>
<th colspan="8" align="left">原生 SDK 集成（即将推出）</th>
</tr>
<tr>
<td align="center" width="12.5%">
<a href="https://github.com/run-llama/llama_index"><img src="https://github.com/run-llama.png?size=120" alt="LlamaIndex" width="48" height="48" /></a><br/>
<strong>LlamaIndex</strong><br/>
<sub>专用工具包</sub>
</td>
<td align="center" width="12.5%">
<a href="https://github.com/microsoft/autogen"><img src="https://github.com/microsoft.png?size=120" alt="AutoGen" width="48" height="48" /></a><br/>
<strong>AutoGen</strong><br/>
<sub>专用工具包</sub>
</td>
<td align="center" width="12.5%">
<a href="https://github.com/openai/openai-agents-python"><img src="https://github.com/openai.png?size=120" alt="OpenAI Agents SDK" width="48" height="48" /></a><br/>
<strong>OpenAI Agents</strong><br/>
<sub>专用工具包</sub>
</td>
<td align="center" width="12.5%">
<a href="https://github.com/google/adk-python"><img src="https://github.com/google.png?size=120" alt="Google ADK" width="48" height="48" /></a><br/>
<strong>Google ADK</strong><br/>
<sub>专用工具包</sub>
</td>
</tr>
</table>

</details>

### MCP 服务器
<a id="mcp-server"></a>

30 秒内接入任何 MCP 兼容客户端（Claude Desktop、Windsurf、Cline、VS Code）：

```bash
python -m semantica.mcp_server
# or via the installed entry point
semantica-mcp
```

```json
{
  "mcpServers": {
    "semantica": { "command": "python", "args": ["-m", "semantica.mcp_server"] }
  }
}
```

**通过 MCP 暴露的工具：**

| 工具 | 功能 |
| --- | --- |
| `extract_entities` | 对任意文本做 NER |
| `extract_relations` | 关系抽取 |
| `record_decision` | 持久化决策节点 |
| `query_decisions` | 检索决策历史 |
| `find_precedents` | 语义先例查找 |
| `get_causal_chain` | 完整因果祖先链 |
| `add_entity` | 添加知识图谱节点 |
| `add_relationship` | 添加知识图谱边 |
| `run_reasoning` | 执行规则集 |
| `get_graph_analytics` | 中心性、社区 |
| `export_graph` | 导出为 RDF/JSON/Parquet |
| `get_graph_summary` | 图统计信息 |

### REST API
<a id="rest-api"></a>

```bash
# Start the backend
python -m semantica.server   # port 8000

# Extract entities & relations via REST
curl -X POST http://localhost:8000/api/enrich/extract \
  -H "Content-Type: application/json" \
  -d '{"text": "Apple CEO Tim Cook announced record earnings."}'

# List recorded decisions
curl "http://localhost:8000/api/decisions?category=vendor_selection"

# Query the knowledge graph
curl "http://localhost:8000/api/graph/node/acme_corp/neighbors?depth=2"
```

**REST 端点覆盖：** `enrich`（抽取）· `graph` · `decisions` · `reasoning` · `provenance` · `ontology` · `embeddings` · `search` · `export` · `pipeline` · `temporal` · `deduplication`

### 插件包

**领域技能：** `extract` · `ingest` · `query` · `ontology` · `validate` · `deduplicate` · `embed` · `reason` · `decision` · `causal` · `temporal` · `provenance` · `policy` · `explain` · `export` · `change` · `visualize`

**专用智能体：** `kg-assistant` · `decision-advisor` · `explainability`

适用于 Claude Code、Cursor、Codex、Windsurf、Cline、Continue、VS Code 和 OpenClaw 的插件包位于 [`plugins/`](plugins/)。

---

## 知识探索器

基于浏览器的图工作台。平移缩放实时图、拖动时间线、审查每个决策的因果链、解决重复项、以可视化方式编写本体。基于 React 19 + Sigma.js 构建。

| 工作区 | 功能 |
| --- | --- |
| **Knowledge Graph** | 实时 Sigma.js 画布，ForceAtlas2 布局、自我中心(Ego)模式、语义距离热力图 |
| **Timeline** | 拖动时态事件，观察图的演化 |
| **Decisions** | 浏览每个已记录决策背后的因果链 |
| **Registry** | 每次图变更的实时审计日志 |
| **Entity Resolution** | 审查并合并重复项 |
| **Ontology Hub** | SHACL Studio、可视化编辑器、跨本体对齐、SKOS 浏览器 |
| **Lineage** | 任意实体的 W3C PROV-O 溯源可视化 |

最快上手方式（无需 Node.js）：

```bash
pip install "semantica[explorer]"
semantica-explorer --graph my_graph.json
# Dashboard opens at http://127.0.0.1:8000
```

贡献者 / 开发服务器配置见：**[explorer/README.md：本地搭建指南](explorer/README.md)**

---

## v0.6.7 新特性

**功能版本**，另含一处 SSRF 加固修复，以及 RDF/本体导出流水线上的一批正确性修复：

- **一流 LangChain 集成**（`semantica[langchain]`）：基于 `HybridSearch` 的 `BaseRetriever` 与 `VectorStore`，外加图/决策查询工具
- **SAP OData 摄取器**（`semantica[ingest-sap]`）：遵循现有 Snowflake/Databricks 连接器模式，为 Business Partners 和 Sales Orders 提供 OAuth2/Basic 认证、带 SSRF 防护的摄取
- **`ContextGraph` 新增确定性的、可人工编辑的 Markdown 往返持久化**，与现有 JSON API 并存；Explorer 图检查器新增只读 Markdown 内容查看器
- **`reasoning` 新增结构化 Action 层**：规则驱动的 `Assert`/`Retract`/`Call`/`EmitEvent` 动作，可选溯源，把推理器变成生产规则系统
- **`run_shacl_validation` 现为公开的文档化 API**，并修复了十余处本体/RDF 导出正确性问题：OWL 属性/类导出、SHACL 目标命名空间解析、四种 RDF 格式统一的置信度数据类型、可达的 OWL-Time 具体化(reification)、JSON-LD 默认图与内容派生的文档标识，以及每个 RDF 序列化器的完整元数据透传
- **安全**：Agno 的 `AgnoKnowledgeGraph.load_urls()` 与 OpenClaw 的 MCP 工具现在将出站请求路由经过共享的 SSRF 防护

其他修复：`PipelineBuilder.set_parallelism()` 现在真正并行执行独立的流水线步骤；`flatten_dict()` 不再在键冲突时静默丢数据；`Config.get()` 正确处理布尔型环境变量覆盖；MCP 服务器的 `export_graph` 工具在所有格式上恢复可用。

→ [完整发布说明](RELEASE_NOTES.md) · [更新日志](CHANGELOG.md)

---

## 为高风险领域而生

Semantica 专为这样的环境设计：AI 输出必须可解释、可审计、可自证，且数据本身不能离开你的基础设施。它可自托管、零供应商锁定，既为处理机密或涉密数据的组织而建，也为需要审计追踪的受监管行业而建：

- **金融：** 贷款核保审计追踪、欺诈检测、AML 合规、监管风险知识图谱
- **医疗：** 临床决策支持、药物相互作用图谱、患者安全审计追踪
- **法律：** 有据可查的研究、合同分析、判例法推理、保密特权追踪
- **政府与国防：** 政策决策记录、涉密信息治理、监管报送，完全自托管，数据不出边界
- **执法：** 案件关联、证据溯源链、经得起法律审查的侦查知识图谱
- **网络安全：** 威胁归因、事件响应时间线、IOC 溯源追踪
- **自主系统：** 决策日志、安全验证、面向认证的可解释 AI

> ⚠️ **这是系统级可解释性，不是基础模型可解释性。** Semantica 不暴露、不重建、也不解释 LLM/基础模型*内部*发生的事情——模型的内部推理或思维链对任何外部系统都同样不透明。Semantica 解释的是模型*之外*的部分：输入的上下文与数据、产生的决策、决策的溯源、相关的关系、应用的策略，以及完整的执行轨迹。简言之，Semantica 解释和审计的是 AI 系统做了什么，而不是 LLM 私有的内部推理。

---

## 安装
<a id="installation"></a>

```bash
pip install semantica           # core
pip install semantica[all]      # everything
```

```bash
pip install semantica[agno]                 # Agno multi-agent integration
pip install semantica[crewai]               # CrewAI integration
pip install semantica[langchain]            # LangChain / LangGraph integration
pip install semantica[llm-litellm]          # OpenAI, Anthropic, Gemini, Mistral, Llama, Groq, Cohere, Bedrock, Ollama, DeepSeek, and more
pip install semantica[graph-neo4j]          # Neo4j graph store (LPG)
pip install semantica[graph-falkordb]       # FalkorDB graph store (LPG)
pip install semantica[graph-apache-age]     # Apache AGE graph store (LPG)
pip install semantica[graph-amazon-neptune] # AWS Neptune graph store (LPG)
pip install semantica[tripletstore-oxigraph] # Embedded in-memory/on-disk RDF store
# RDF triple stores (Blazegraph, Apache Jena, Eclipse RDF4J) need no extra:
# semantica.triplet_store talks SPARQL over HTTP using the core `requests` dependency
pip install semantica[vectorstore-qdrant]   # Qdrant vector store
pip install semantica[vectorstore-pinecone] # Pinecone vector store
pip install semantica[db-snowflake]         # Snowflake
pip install semantica[db-databricks]        # Databricks (SDK + SQL connector)
pip install semantica[ingest-parquet]       # Parquet / PyArrow
pip install semantica[ingest-arrow]        # Apache Arrow, Feather, IPC
pip install semantica[viz]                  # HTML interactive visualization
pip install semantica[watch]                # Directory file watcher
pip install semantica[explorer]             # Knowledge Explorer dashboard
```

生产部署请使用 Docker 或 Kubernetes，而不是本地 `pip install`。设置 `SEMANTICA_SECRET_KEY`，配置持久化的 LPG 图存储（Neo4j / FalkorDB / Apache AGE / AWS Neptune）和/或 RDF 三元组存储（Blazegraph / Apache Jena / Eclipse RDF4J），并将向量存储指向托管后端（Qdrant / Pinecone）。完整部署拓扑见 [ARCHITECTURE.md](ARCHITECTURE.md)。

```bash
# From source
git clone https://github.com/semantica-agi/semantica.git
cd semantica && pip install -e ".[dev]" && pytest tests/
```

### CI 与部署

把 `semantica` 接入你自己的 CI 只需两分钟。在 GitHub Actions 上使用可复用的 composite action：

```yaml
- uses: semantica-agi/semantica/.github/actions/setup-semantica@main
  with:
    python-version: '3.11'
```

GitHub Actions、GitLab CI 和 CircleCI 可直接复制的起始模板在 [examples/ci/](examples/ci/)。发布的包本身由 [Install Matrix 工作流](.github/workflows/install-matrix.yml) 每周在 Ubuntu/macOS/Windows 与 Python 3.9-3.12 上验证可安装。

AWS、GCP、Azure、Fly.io、Railway、Render、Kubernetes 和 Helm 的现成部署配置在 [deploy/](deploy/)。

---

## 企业版

本地部署 · 私有云 · 定制领域实施 · SLA 保障支持 · 面向受监管行业（金融、医疗、法律、政府）的专业服务。

企业方案与定价见 **[getsemantica.ai](https://getsemantica.ai/)**。

---

## 社区与支持

| | |
| --- | --- |
| **Discord** | [discord.gg/sV34vps5hH](https://discord.gg/sV34vps5hH)：实时帮助、案例展示与公告 |
| **GitHub Discussions** | [问答与功能请求](https://github.com/semantica-agi/semantica/discussions) |
| **GitHub Issues** | [Bug 报告](https://github.com/semantica-agi/semantica/issues) |
| **文档** | [docs.getsemantica.ai](https://docs.getsemantica.ai/) |
| **Cookbook** | [可运行的 Jupyter notebook](https://github.com/semantica-agi/semantica/tree/main/cookbook) |
| **更新日志** | [CHANGELOG.md](CHANGELOG.md) · [发布说明](RELEASE_NOTES.md) |

---

## Star 历史

<a href="https://star-history.dera.page/#semantica-agi/semantica&amp;type=date&amp;legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://star-history.dera.page/svg?repos=semantica-agi/semantica&amp;type=date&amp;theme=dark&amp;legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://star-history.dera.page/svg?repos=semantica-agi/semantica&amp;type=date&amp;legend=top-left" />
   <img alt="Star History Chart" src="https://star-history.dera.page/svg?repos=semantica-agi/semantica&amp;type=date&amp;legend=top-left" />
 </picture>
</a>

---

## 贡献者

<div align="center">

[![Contributors](https://contrib.rocks/image?repo=semantica-agi/semantica&max=500)](https://github.com/semantica-agi/semantica/graphs/contributors)

</div>

---

## 参与贡献

欢迎所有形式的贡献：bug 修复、功能、测试与文档。

1. Fork 本仓库并创建分支
2. `pip install -e ".[dev]"`
3. 随改动一起编写测试（`pytest tests/`）
4. 提交 PR 并标记 `@KaifAhmad1` 评审

完整指南见 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## 引用我们

如果你在研究或生产系统中使用了 Semantica，请按如下格式引用：

```bibtex
@software{semantica2026,
  title  = {Semantica: Graph-Native Infrastructure for Context and Accountable AI Systems},
  author = {Semantica},
  year   = {2026},
  url    = {https://github.com/semantica-agi/semantica}
}
```

所有引用格式（APA、MLA、Chicago、IEEE）都在 [Citation](https://docs.getsemantica.ai/citation) 页面——每种格式都将作者署名归于 **Semantica**，而非个人贡献者。

---

<div align="center">

MIT 许可证 · 由 [Semantica](https://github.com/semantica-agi) 构建

[GitHub](https://github.com/semantica-agi/semantica) &nbsp;·&nbsp;
[Discord](https://discord.gg/sV34vps5hH) &nbsp;·&nbsp;
[Twitter/X](https://x.com/BuildSemantica) &nbsp;·&nbsp;
[Website](https://getsemantica.ai/) &nbsp;·&nbsp;
[Docs](https://docs.getsemantica.ai/) &nbsp;·&nbsp;
[PyPI](https://pypi.org/project/semantica/)

如果这个项目能帮你构建更好的 AI，一颗 star 意义重大。

**[⭐ 在 GitHub 上 Star →](https://github.com/semantica-agi/semantica)**

[English](https://readme-i18n.com/semantica-agi/semantica?lang=en) · [Deutsch](https://readme-i18n.com/semantica-agi/semantica?lang=de) · [Français](https://readme-i18n.com/semantica-agi/semantica?lang=fr) · [Español](https://readme-i18n.com/semantica-agi/semantica?lang=es) · [Italiano](https://readme-i18n.com/semantica-agi/semantica?lang=it) · [Português](https://readme-i18n.com/semantica-agi/semantica?lang=pt) · [العربية](https://readme-i18n.com/semantica-agi/semantica?lang=ar) · [اردو](https://readme-i18n.com/semantica-agi/semantica?lang=ur) · [हिन्दी](https://readme-i18n.com/semantica-agi/semantica?lang=hi) · [中文](https://readme-i18n.com/semantica-agi/semantica?lang=zh) · [日本語](https://readme-i18n.com/semantica-agi/semantica?lang=ja) · [한국어](https://readme-i18n.com/semantica-agi/semantica?lang=ko)

</div>
