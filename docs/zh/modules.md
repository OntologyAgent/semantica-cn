---
title: 模块
description: Semantica 的每个模块都独立可用：只导入你需要的部分。
source: modules.md
source_version: 9c47f1cc335e7f9f001b70e2edba71003a3908cf
icon: "puzzle-piece"
---

<Info>
  想要速查表？直接跳到文末的[模块索引](#模块索引)。
</Info>

<Tip>
  不确定该用哪个模块？[选对模块](./choose-your-module.md)指南把 35+ 个开发目标映射到对应模块并附代码示例——初次上手建议从这里开始。
</Tip>

Semantica 按六个逻辑层组织成 **27 个模块**。每个模块都可独立导入：用不上的部分一分钱成本也不用付。

## 架构总览

- **输入层** — 数据摄取与准备。模块：`ingest`、`parse`、`split`、`normalize`
- **核心处理** — 智能与理解。模块：`semantic_extract`、`kg`、`ontology`、`reasoning`
- **存储** — 持久化数据存储。模块：`embeddings`、`vector_store`、`graph_store`、`triplet_store`
- **质量保障** — 数据质量与一致性。模块：`deduplication`、`conflicts`
- **上下文与记忆** — 智能体记忆与决策追踪。模块：`context`、`provenance`、`change_management`
- **输出与编排** — 导出、可视化与工作流。模块：`export`、`visualization`、`pipeline`、`explorer`


## 输入层

### 摄取

从文件、网页、数据库和数据流加载数据，统一为 `SourceDocument` 格式。

```python
from semantica.ingest import FileIngestor, WebIngestor, ParquetIngestor, XMLIngestor, DatabricksIngestor

# 文件：PDF、DOCX、CSV、Excel、PPTX、JSON、HTML、压缩包
ingestor = FileIngestor()
documents = ingestor.ingest_directory("data/")

# 网页爬取
web_ingestor = WebIngestor()
page = web_ingestor.ingest_url("https://example.com")

# Parquet：单文件、分区目录、Hive 风格（v0.5.0）
parquet = ParquetIngestor()
sources = parquet.ingest("data/events.parquet")

# XML，支持 XSD/DTD 校验、命名空间处理（v0.5.0）
xml = XMLIngestor()
sources = xml.ingest("data/records/", schema_path="schema.xsd")

# 企业级湖仓/数仓——Unity Catalog + Delta Lake，或 Snowflake 仓库
databricks = DatabricksIngestor(host="...", token="...", http_path="...")
customers   = databricks.ingest_table("customers")
```

**可用摄取器：** `FileIngestor`, `WebIngestor`, `ParquetIngestor`, `XMLIngestor`, `RESTIngestor`, `PublicAPIIngestor`, `DBIngestor`, `DatabricksIngestor`, `SnowflakeIngestor`, `EmailIngestor`, `FeedIngestor`, `MCPIngestor`, `OntologyIngestor`, `RepoIngestor`, `StreamIngestor`, `ArrowIngestor`, `CloudStorageIngestor`

<Note>
  `DuckDBIngestor`、`ElasticIngestor`、`GDriveIngestor`、`HuggingFaceIngestor`、`MongoIngestor` 和 `PandasIngestor` 也在包内，但尚未从顶层 `semantica.ingest` 命名空间再导出——请直接导入，例如 `from semantica.ingest.duckdb_ingestor import DuckDBIngestor`。
</Note>

### 解析

从原始文档中抽取结构化文本和版面元数据。

```python
from semantica.parse import DocumentParser, DoclingParser

# 标准解析器：覆盖所有常见格式
parser = DocumentParser()
parsed = parser.parse_document("document.pdf")

# 高级解析器：多栏 PDF、合并单元格表格、OCR
parser = DoclingParser(extract_tables=True, extract_images=True, output_format="markdown")
parsed = parser.parse("data/annual_report.pdf")
```

**可用解析器：** `DocumentParser`, `DoclingParser`, `CodeParser`, `CSVParser`, `DocxParser`, `EmailParser`, `ExcelParser`, `HTMLParser`, `ImageParser`, `JSONParser`, `MCPParser`, `MediaParser`, `PDFParser`, `PPTXParser`, `StructuredDataParser`, `WebParser`, `XMLParser`

### 分块

为嵌入和 RAG 流水线切分文本，感知语义边界。

```python
from semantica.split import TextSplitter

splitter = TextSplitter(method="semantic_transformer")
chunks = splitter.split(text, chunk_size=1000, chunk_overlap=200)
```

**分块策略：** `recursive`, `semantic_transformer`, `entity_aware`, `relation_aware`, `sliding_window`, `structural`

### 规范化

在语义处理前清洗并标准化文本。

```python
from semantica.normalize import TextNormalizer, normalize_text, normalize_date

normalizer = TextNormalizer()
clean_text        = normalizer.normalize_text(text)
standardized_date = normalize_date("Jan 1st, 2020")
```

**可用规范化器：** 文本清洗、实体规范化、日期规范化、数字规范化、编码处理、语言检测


## 核心处理

### 语义抽取

命名实体识别、关系抽取和三元组生成。

```python
from semantica.semantic_extract import NERExtractor, RelationExtractor, TripletExtractor

ner = NERExtractor(method="llm", llm_provider=llm)
entities = ner.extract("Apple Inc. was founded by Steve Jobs.")

rel = RelationExtractor(method="llm", llm_provider=llm)
relationships = rel.extract(text, entities=entities)

trip = TripletExtractor(method="pattern")
triplets = trip.extract(text)                                     # list[Triplet]
```

**抽取方法：** `"pattern"`（无需 API key）、`"ml"`（本地 spaCy 模型）、`"llm"`（9 家受支持提供商任选）

**其他抽取器：** `CoreferenceResolver`, `EventDetector`, `SemanticAnalyzer`, `SemanticNetworkExtractor`

### 知识图谱

图构建、图算法、时态模型和距离智能。

```python
from semantica.kg import GraphBuilder, GraphAnalyzer, TemporalGraphQuery, SimilarityCalculator
from datetime import datetime

# 构建: build() takes a {"entities": ..., "relationships": ...} dict
builder = GraphBuilder(merge_entities=True)
kg = builder.build({"entities": entities, "relationships": relationships})

# 时态图（v0.4.0）
query_engine = TemporalGraphQuery(enable_temporal_reasoning=True)
snapshot = query_engine.query_at_time(kg, query="", at_time=datetime(2021, 6, 15))

# 语义相似度（v0.5.0）: operates on embedding vectors
calc = SimilarityCalculator(method="cosine")
score = calc.cosine_similarity(vec_a, vec_b)
```

**可用图算法：** 中心度计算、社区检测、连通性分析、实体消解、链路预测、路径查找、相似度计算

### 本体

模式管理：SHACL、SKOS、本体对齐、差异/迁移、自动生成，以及可视化的本体中心（v0.5.0）。

```python
from semantica.ontology import OntologyGenerator, SHACLGenerator

generator = OntologyGenerator()
ontology  = generator.generate_from_graph(kg)

shacl  = SHACLGenerator()
shapes = shacl.generate(ontology)
```

**组件：** `OntologyGenerator`, `SHACLGenerator`, `OntologyValidator`, `OntologyEvaluator`, `LLMOntologyGenerator`, `OWLGenerator`, `PropertyGenerator`, `DomainOntologies`, `NamespaceManager`

### 推理

用多种推断策略从已有知识推导新事实。

```python
from semantica.reasoning import Reasoner, DatalogReasoner

# 前向链接: facts and rules as predicate(args) / IF-THEN strings
engine = Reasoner()
engine.add_fact("Manager(Alice)")
engine.add_rule("IF Manager(?x) THEN HasAuthority(?x)")
results = engine.forward_chain()          # list[InferenceResult] with .conclusion, .rule_used

# Datalog：递归 Horn 子句规则（v0.4.0）
datalog = DatalogReasoner()
datalog.add_fact("parent(tom, bob)")
datalog.add_fact("parent(bob, ann)")
datalog.add_rule("ancestor(X, Y) :- parent(X, Y).")
datalog.derive_all()
results = datalog.query("ancestor(tom, ?Z)")   # [{"Z": "bob"}, {"Z": "ann"}], order not guaranteed
```

**引擎：** `Reasoner`（前向/后向链）、`ReteEngine`、`SPARQLReasoner`、`DatalogReasoner`、`TemporalReasoningEngine`、`GraphReasoner`（LLM）——全部产出可解释的推理路径


## 存储

### 嵌入

生成并管理用于语义相似度的向量嵌入。

```python
from semantica.embeddings import EmbeddingGenerator

generator  = EmbeddingGenerator()
embeddings = generator.generate_embeddings(["text1", "text2"])   # np.ndarray
similarity = generator.compare_embeddings(embeddings[0], embeddings[1])
```

**支持的模型：** Sentence-Transformers、FastEmbed、OpenAI、BGE

**组件：** `EmbeddingGenerator`, `TextEmbedder`, `VectorEmbeddingManager`, `GraphEmbeddingManager`, `PoolingStrategies`

### 向量库

多后端向量数据库，支持混合检索。

```python
from semantica.vector_store import VectorStore

store = VectorStore(backend="faiss", dimension=768)
# Raw vectors
ids     = store.store_vectors(embeddings)                 # returns generated ids
hits    = store.search_vectors(query_vector, k=10)
# Or store text and let the store embed it
store.add_documents(["Apple was founded in 1976.", "Google was founded in 1998."])
results = store.search("tech company founding dates", limit=10)
```

**后端：** FAISS、Pinecone、Weaviate、Qdrant、Milvus、PgVector、SQLite、内存版

**检索模式：** 语义 top-k、混合（向量 + 关键词）、元数据过滤

### 图库

连接图数据库，提供可持久化、可查询的存储。

```python
from semantica.graph_store import GraphStore

store = GraphStore(backend="neo4j")
store.add_nodes([{"id": "acme", "type": "Organization", "properties": {"name": "Acme"}}])
store.add_edges([{"source": "alice", "target": "acme", "type": "works_for"}])
results = store.query("MATCH (n)-[r]->(m) RETURN n, r, m")
```

**后端：** Neo4j、FalkorDB、Apache AGE、Amazon Neptune

### 三元组库

基于 RDF 三元组的存储，支持 SPARQL 查询。

```python
from semantica.triplet_store import TripletStore

store = TripletStore(backend="oxigraph")
store.add_triplets(triplets)                 # list of Triplet objects (or add_triplet for one)
results = store.execute_query("SELECT ?s ?p ?o WHERE { ?s ?p ?o }")
```

**后端：** Oxigraph（嵌入式）、Blazegraph、Apache Jena、RDF4J


## 质量保障

### 去重

检测、评分并合并跨来源的重复实体。

```python
from semantica.deduplication import DuplicateDetector, EntityMerger

detector   = DuplicateDetector(similarity_threshold=0.85)
candidates = detector.detect_duplicates(entities)
merger     = EntityMerger()
operations = merger.merge_duplicates(entities, strategy="keep_most_complete")
```

**v2 策略**（`blocking_v2`, `hybrid_v2`, `semantic_v2`）比 v1 快至 7 倍。

**组件：** `DuplicateDetector`, `EntityMerger`, `ClusterBuilder`, `MergeStrategyManager`

**`DuplicateDetector` 选项：** `max_results`, `top_k_per_entity`, `min_similarity`, `sort_by`

### 冲突

检测并消解重叠知识来源之间的事实冲突。

```python
from semantica.conflicts import ConflictDetector, ConflictResolver

conflicts = ConflictDetector().detect_conflicts(entities)   # list of entity dicts
resolved  = ConflictResolver().resolve_conflicts(conflicts, strategy="most_recent")
```

**检测类型：** 值冲突、类型冲突、关系冲突、时态冲突、逻辑冲突

**消解策略：** 新近优先、可信来源优先、多数表决、标记人工复核


## 上下文与记忆

### 上下文

智能体上下文图、决策追踪、因果链和先例检索。

```python
from semantica.context import AgentContext, ContextGraph

context = AgentContext(
    vector_store=VectorStore(backend="faiss", dimension=768),
    knowledge_graph=ContextGraph(advanced_analytics=True),
    decision_tracking=True,
)

context.store("GPT-4 outperforms GPT-3.5 on reasoning benchmarks by 40%")

decision_id = context.record_decision(
    category="model_selection",
    scenario="...",
    reasoning="...",
    outcome="...",
    confidence=0.9,
)

precedents = context.find_precedents("model selection", limit=5)
```

**组件：** `AgentContext`, `ContextGraph`, `AgentMemory`, `DecisionRecorder`, `CausalAnalyzer`, `EntityLinker`, `PolicyEngine`

### 溯源

兼容 W3C PROV-O 的血缘追踪，覆盖所有模块。

```python
from semantica.provenance import ProvenanceManager

manager = ProvenanceManager()
manager.track_entity("entity_1", source="document.pdf", metadata={"type": "person"})
lineage = manager.get_lineage("entity_1")
```

**组件：** `ProvenanceManager`, `IntegrityChecker`, `BridgeAxiom`, `ProvenanceStorage`

### 变更管理

带 SHA-256 校验和、差异对比和回滚的版本控制。

```python
from semantica.change_management import TemporalVersionManager

manager  = TemporalVersionManager(storage_path="versions.db")
snapshot = manager.create_snapshot(kg, "v1.0", "user@example.com", "Initial version")
diff     = manager.diff("v1.0", "v1.1")
```

**组件：** `TemporalVersionManager`, `ChangeLog`, `OntologyVersionManager`, `VersionStorage`


## 输出与编排

### 导出

把图序列化为下游格式，用于分析平台、语义网或图数据库。

```python
from semantica.export import RDFExporter, ParquetExporter, ArangoAQLExporter

# RDF 格式
RDFExporter().export(graph, file_path="graph.ttl", format="turtle")

# 分析平台
ParquetExporter().export(graph, file_path="output/graph.parquet")

# ArangoDB: writes AQL INSERT statements to the given path
ArangoAQLExporter().export(graph, file_path="graph.aql")
```

**导出格式：** RDF（Turtle、JSON-LD、N-Triples、XML）、Parquet、ArangoDB AQL、CSV、OWL、Arrow、LPG、YAML、距离矩阵

### 可视化

渲染交互式和静态知识图谱可视化。

```python
from semantica.visualization import KGVisualizer

viz = KGVisualizer()
viz.visualize_network(graph, output="html", file_path="graph.html")
```

**可视化器：** `KGVisualizer`, `OntologyVisualizer`, `EmbeddingVisualizer`, `SemanticNetworkVisualizer`, `TemporalVisualizer`, `AnalyticsVisualizer`

**布局算法：** 力导向、层次、环形

### 流水线

流水线 DSL，带并行 worker、重试策略和失败处理。

```python
from semantica.pipeline import Pipeline

pipeline = Pipeline()
pipeline.add_step("ingest",   FileIngestor())
pipeline.add_step("extract",  NERExtractor())
pipeline.add_step("build",    GraphBuilder())
result = pipeline.run("data/")
```

**组件：** `Pipeline`, `PipelineBuilder`, `ExecutionEngine`, `FailureHandler`, `PipelineValidator`, `ParallelismManager`, `ResourceScheduler`

### Explorer

基于 FastAPI 的知识探索面板：本体中心、WebSocket 进度、双向路径查找和索引搜索（11.8 万节点上 0.004ms）。

```bash
semantica-explorer --graph my_graph.json
```

**路由：** graph、ontology、provenance、decisions、analytics、SPARQL、temporal、annotations、导出/导入、vocabulary


## 工具

### LLM 提供商

所有受支持 LLM 提供商的统一接口。

```python
from semantica.llms import Groq, OpenAI, LiteLLM
import os

llm = Groq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))
llm = OpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))
# 经 LiteLLM 使用 Anthropic、Gemini、Ollama、DeepSeek：
llm = LiteLLM(model="anthropic/claude-opus-4-7", api_key=os.getenv("ANTHROPIC_API_KEY"))
```

**支持的提供商：** OpenAI、Anthropic、Google Gemini、Groq、Ollama、DeepSeek、Novita AI、HuggingFace，外加 LiteLLM（一个接口接入 100+ 模型）

### MCP 服务器

把 Semantica 暴露为 MCP stdio 服务器，供 IDE 和智能体集成。

```bash
python -m semantica.mcp_server
```

**集成：** Claude Desktop、VS Code、Cursor、Windsurf、Cline。暴露 15 个 MCP 工具。

### 种子数据

从经过验证的结构化来源引导知识图谱：定点参考数据、受控词表和领域锚点。

```python
from semantica.seed import SeedDataManager

seed = SeedDataManager()
# Load trusted reference data from CSV / JSON / a database / an API
seed_data = seed.load_from_csv("seed_data/industries.csv", entity_type="Industry")

# Merge seed data with extraction output (seed values win on conflict by default)
combined = seed.integrate_with_extracted(
    {"entities": seed_data, "relationships": []},
    {"entities": extracted_entities, "relationships": extracted_relationships},
    merge_strategy="seed_first",
)
```

**用例：** 用已知实体锚定抽取、预填充本体类、生成确定性的测试图。

### 评估

为决策智能产出（决策记录、审计轨迹、推理文本）打分：一组确定性评估器与模型支撑的评估器，加一个小型运行框架。

```python
from semantica.evals import evaluate, list_evaluators

list_evaluators()
# ['decision_scores', 'exact_match', 'keyword_check', 'length_range',
#  'levenshtein', 'llm_as_judge', 'numeric_range', 'regex_match', 'rouge',
#  'temporal_range']

cases = [("apple", "aple"), ("night", "nacht")]
summary = evaluate(cases, evaluators=["levenshtein"])
print(summary.total, summary.passed, summary.pass_rate)
```

**公开 API：** `evaluate(cases, evaluators, config=None)`、`list_evaluators()`、`get_evaluator(name)`，以及 `EvalMetric` / `CaseResult` / `EvalSummary` 结果类型。详见[评估模块参考](../reference/evals.md)。

### Core

所有模块共用的基类、共享数据模型和插件注册表。

```python
from semantica.core import Semantica, PluginRegistry, ConfigManager

# ConfigManager loads a Config; Config.get() does dotted lookups
sem.initialize()

# 插件注册表：注册自定义组件
registry = PluginRegistry()
registry.register("my_ingestor", MyCustomIngestor)

# 配置管理
config  = ConfigManager(config_path="config.yaml")
batch   = config.get("processing.batch_size", default=32)
```

**组件：** `Semantica`, `PluginRegistry`, `ConfigManager`, `LifecycleManager`, `HealthMonitor`, `Config`

### Utils

共享工具：ID 生成、日期解析、校验和日志。

```python
from semantica.utils import helpers, validators, logging
```

**组件：** `helpers`, `validators`, `constants`, `types`, `exceptions`, `logging`, `ProgressTracker`


## 常见模块组合

<Tabs>
  <Tab title="文档 → KG">
    从任意来源加载文档，变成可查询的知识图谱。

    **流水线：** `Ingest` → `Parse` → `Normalize` → `Semantic Extract` → `GraphBuilder` → `KG`

```python
from semantica.ingest import FileIngestor
from semantica.parse import DocumentParser
from semantica.semantic_extract import NERExtractor, RelationExtractor
from semantica.kg import GraphBuilder

sources       = FileIngestor().ingest("data/")
parsed        = DocumentParser().parse(sources[0])
entities      = NERExtractor(method="llm", llm_provider=llm).extract(parsed)
relationships = RelationExtractor(method="llm", llm_provider=llm).extract(parsed, entities=entities)
graph         = GraphBuilder(merge_entities=True).build(
                    entities=entities, relationships=relationships
                )
```

    **适用：** 研究流水线、企业数据抽取、文档智能
  </Tab>

  <Tab title="GraphRAG">
    让 LLM 的每条回答都扎根于知识图谱：结构化检索，带来源标注。

    **流水线：** `KG` + `VectorStore` → `AgentContext` → GraphRAG 查询 → 有根据的回答

```python
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore

context = AgentContext(
    vector_store=VectorStore(backend="faiss", dimension=768),
    knowledge_graph=ContextGraph(advanced_analytics=True),
)
context.load_graph("company_kg.json")

result = context.query(
    "What companies did Apple alumni found?",
    mode="graphrag",
    reasoning=True,
)
for claim in result.claims:
    print(f"{claim.text}  →  {claim.source_node}")
```

    **适用：** 问答系统、带来源标注的 RAG、研究助手
  </Tab>

  <Tab title="AI 智能体">
    给智能体持久记忆、决策追踪和策略执行。

    **流水线：** `AgentContext` → 决策记录 → 先例检索 → 策略检查 → 因果分析

```python
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore

context = AgentContext(
    vector_store=VectorStore(backend="faiss", dimension=768),
    knowledge_graph=ContextGraph(advanced_analytics=True),
    decision_tracking=True,
)
context.store("GPT-4 outperforms GPT-3.5 on reasoning by 40%")

decision_id = context.record_decision(
    category="model_selection",
    scenario="Choose LLM for production",
    reasoning="Benchmark advantage justifies cost",
    outcome="selected_gpt4",
    confidence=0.91,
)
precedents = context.find_precedents("model selection", limit=5)
```

    **适用：** 自主智能体、AI 副驾、决策支持系统
  </Tab>

  <Tab title="合规流水线">
    从原始数据到最终推断的完整溯源：W3C PROV-O、SHA-256 校验和、审计轨迹。

    **流水线：** `Ingest` → `Parse` → `Extract` → `KG` → `Provenance` → `ChangeManagement` → `Export`

```python
from semantica.ingest import FileIngestor
from semantica.semantic_extract import NERExtractor
from semantica.kg import GraphBuilder
from semantica.provenance import ProvenanceManager
from semantica.export import RDFExporter

sources  = FileIngestor().ingest("records/")
entities = NERExtractor(method="llm", llm_provider=llm).extract(sources)
graph    = GraphBuilder(merge_entities=True).build(entities=entities, relationships=[])
prov     = ProvenanceManager()
lineage  = prov.get_entity_lineage("entity_id")

RDFExporter(include_provenance=True).export(graph, file_path="audit.ttl", format="turtle")
```

    **适用：** HIPAA、SOX、GDPR、FDA 21 CFR Part 11 部署
  </Tab>

  <Tab title="网页抓取 → 图">
    爬取网站、规范化文本，直接从网页抽取知识。

    **流水线：** `WebIngestor` → `Normalize` → `Semantic Extract` → `GraphStore`

```python
from semantica.ingest import WebIngestor
from semantica.normalize import TextNormalizer
from semantica.semantic_extract import NERExtractor, RelationExtractor
from semantica.graph_store import Neo4jStore

pages      = WebIngestor(max_depth=2).ingest("https://example.com")
normalizer = TextNormalizer()
store      = Neo4jStore(uri="bolt://localhost:7687", user="neo4j", password="password")

for page in pages:
    text          = normalizer.normalize_text(page.text)
    entities      = NERExtractor().extract(text)
    relationships = RelationExtractor().extract(text, entities=entities)
    store.add_nodes(entities)
    store.add_edges(relationships)
```

    **适用：** 竞争情报、新闻监控、研究聚合
  </Tab>

  <Tab title="时态分析">
    追踪事实随时间的变化：时间点查询、快照和版本控制。

    **流水线：** `KG (Temporal)` → `TemporalGraphQuery` → `VersionManager` → `ChangeManagement`

```python
from semantica.kg import GraphBuilder, TemporalGraphQuery, TemporalVersionManager

builder = GraphBuilder()
kg      = builder.build(sources=[{
    "entities": [{"id": "alice", "type": "Person"}],
    "relationships": [{"source": "alice", "target": "acme", "type": "ceo_of",
                       "valid_from": "2020-01-01", "valid_until": "2023-06-01"}]
}])

query         = TemporalGraphQuery()
snapshot_2021 = query.reconstruct_at_time(kg, "2021-06-15")

versioner = TemporalVersionManager()
versioner.create_snapshot(kg, "2024-Q1", author="user@example.com", description="Q1 snapshot")
```

    **适用：** 金融历史、监管时间线、组织变动追踪
  </Tab>
</Tabs>


## 模块索引

| 模块 | 用途 | 关键类 |
| :------ | :------- | :----------- |
| [ingest](../reference/ingest.md) | 数据摄取 | `FileIngestor`, `WebIngestor`, `ParquetIngestor`, `XMLIngestor` |
| [parse](../reference/parse.md) | 文档解析 | `DocumentParser`, `DoclingParser` |
| [split](../reference/split.md) | 文本分块 | `TextSplitter` |
| [normalize](../reference/normalize.md) | 数据清洗 | `TextNormalizer`, `EntityNormalizer`, `LanguageDetector` |
| [semantic_extract](../reference/semantic_extract.md) | NER 与关系抽取 | `NERExtractor`, `RelationExtractor`, `TripletExtractor`, `SemanticAnalyzer`, `SemanticNetworkExtractor`, `ExtractionValidator` |
| [kg](../reference/kg.md) | 图构建 | `GraphBuilder`, `TemporalGraphQuery`, `SimilarityCalculator` |
| [ontology](../reference/ontology.md) | 模式管理 | `OntologyGenerator`, `SHACLGenerator` |
| [reasoning](../reference/reasoning.md) | 逻辑推断 | `Reasoner`, `DatalogReasoner` |
| [embeddings](../reference/embeddings.md) | 向量嵌入 | `EmbeddingGenerator` |
| [vector_store](../reference/vector_store.md) | 向量数据库 | `VectorStore` |
| [graph_store](../reference/graph_store.md) | 图数据库 | `GraphStore` |
| [triplet_store](../reference/triplet_store.md) | RDF 三元组库 | `TripletStore` |
| [deduplication](../reference/deduplication.md) | 实体消解 | `EntityResolver`, `DuplicateDetector`, `ClusterBuilder`, `MergeStrategyManager` |
| [conflicts](../reference/conflicts.md) | 冲突消解 | `ConflictDetector` |
| [context](../reference/context.md) | 智能体上下文与决策 | `AgentContext`, `ContextGraph` |
| [provenance](../reference/provenance.md) | W3C PROV-O 血缘 | `ProvenanceManager` |
| [change_management](../reference/change_management.md) | 版本控制 | `TemporalVersionManager` |
| [export](../reference/export.md) | 数据导出 | `RDFExporter`, `ParquetExporter` |
| [visualization](../reference/visualization.md) | 图可视化 | `KGVisualizer` |
| [pipeline](../reference/pipeline.md) | 工作流编排 | `Pipeline`, `PipelineBuilder` |
| [explorer](../reference/explorer.md) | 知识探索界面 | `semantica-explorer --graph <file>` |
| [llms](../reference/llms.md) | LLM 提供商 | `Groq`, `OpenAI`, `create_provider` |
| [mcp_server](../reference/mcp_server.md) | MCP stdio 服务器 | `python -m semantica.mcp_server` |
| [seed](../reference/seed.md) | 从结构化来源引导 KG | `SeedDataManager` |
| [evals](../reference/evals.md) | 质量评估 | `evaluate`, `list_evaluators`, `EvalSummary` |
| [core](../reference/core.md) | 基类与注册表 | `Semantica`, `ConfigManager`, `PluginRegistry`, `LifecycleManager` |
| [utils](../reference/utils.md) | 共享工具 | `helpers`, `validators` |

- [入门指南](./getting-started.md) — 5 分钟建好你的第一张知识图谱。
- [示例手册](../cookbook.md) — 40+ 个带真实示例的领域笔记本。
- [API 参考](../reference/context.md) — 完整技术文档。
