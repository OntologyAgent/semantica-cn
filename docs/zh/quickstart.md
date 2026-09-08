---
title: 快速开始
description: 5 分钟搭好你的第一个知识图谱，无需任何配置。
source: quickstart.md
source_version: 541f29613c1e382dc9f061596742e2dcd59a04c6
icon: "rocket"
---

<Info>
  **v0.6.8**：带密码学签名的发布（SLSA 溯源 + Sigstore）、FAISS/Qdrant/Weaviate/Milvus 全线真实的向量枚举，以及 Anthropic/Gemini/Ollama/DeepSeek/Novita 一等 LLM 提供商包装器。<a href="https://github.com/semantica-agi/semantica/releases" style={{color:"#10B981",fontWeight:600,textDecoration:"none"}}>看看有什么新东西 →</a>
</Info>

本指南带你走通构建第一个知识图谱(Knowledge Graph)的端到端流水线。装好之后从这里开始。大语言模型(LLM)的 API key 是可选的：基于模式的抽取开箱即用。


## 安装

<CodeGroup>

```bash pip (recommended)
pip install semantica
```

```bash With all extras
pip install semantica[all]
```

```bash From source
git clone https://github.com/semantica-agi/semantica.git
cd semantica
pip install -e ".[dev]"
```

</CodeGroup>

验证安装：

```bash
python -c "import semantica; print(semantica.__version__)"
# 0.6.8
```


## 完整流水线

<img src="/assets/img/diagrams/pipeline-flow.svg" alt="Semantica 端到端流水线：摄取 → 解析 → 规范化 → 抽取 → 构建知识图谱 → 质检 → 存储 → 交付" style={{ width: '100%', borderRadius: '10px', margin: '0 0 24px' }} />

<Steps>

<Step title="摄取(Ingest)">

从文件或目录加载文档。本走查其余部分沿文件路径展开；其他来源在后面附上。

```python
from semantica.ingest import FileIngestor

ingestor = FileIngestor()
sources  = ingestor.ingest("data/report.pdf")
# Also accepts a directory, .docx, .html, .json, .csv, .xlsx, .pptx, .parquet, .xml
```

<Tip>
  **其他来源。** `WebIngestor().ingest_url(url)` 返回 `WebContent`，其 `.text` 可以直接喂给抽取(Extract)步骤（无需解析）。`ParquetIngestor().ingest(path)` 和 `XMLIngestor().ingest(path, schema_path=...)` 返回的是结构化记录而非文档——用 `GraphBuilder().build({"entities": [...], "relationships": [...]})` 直接建图即可。
</Tip>

</Step>

<Step title="解析(Parse)">

从原始文档提取结构化文本和版面信息。

```python
from semantica.parse import DocumentParser

parser = DocumentParser()
parsed = parser.parse(sources[0].path)   # parse() takes a path string

print(parsed["full_text"][:200])   # 提取出的文本
print(parsed["metadata"])          # 文档属性（字段随格式而异）
```

`parse()` 返回 `dict`。每种格式都有 `full_text` 和 `metadata`；其余键取决于解析器（PDF 有 `pages`，DOCX 有 `tables` 和 `paragraphs`，`DoclingParser` 有 `tables`）。

<Tip>
  处理带表格、图表或多栏版面的 PDF 时，用 `DoclingParser`（`pip install semantica[parse-docling]`）：它会做高级版面分析，在文本之外还返回结构化的表格数据。
</Tip>

```python
from semantica.parse import DoclingParser

parser = DoclingParser()
parsed = parser.parse(sources[0].path)
print(parsed["tables"])   # 结构化表格数据
```

</Step>

<Step title="抽取实体与关系">

识别命名实体，抽取实体之间带类型的语义关系。

<CodeGroup>

```python Pattern-based (fast, no API key)
from semantica.semantic_extract import NERExtractor, RelationExtractor

text = parsed["full_text"]

ner      = NERExtractor(method="pattern")
entities = ner.extract(text)
# Returns: [Entity(text="Apple Inc.", label="ORG", start_char=0, end_char=10, confidence=0.7), ...]

rel           = RelationExtractor(method="pattern")
relationships = rel.extract(text, entities=entities)
# Returns: [Relation(subject=Entity(...), predicate="founded_by", object=Entity(...), confidence=0.7), ...]
```

```python LLM-powered (higher accuracy)
from semantica.semantic_extract import NERExtractor, RelationExtractor

# Reads GROQ_API_KEY from the environment; provider/llm_model select the backend
text = parsed["full_text"]

ner           = NERExtractor(method="llm", provider="groq", llm_model="llama-3.3-70b-versatile")
entities      = ner.extract(text)

rel           = RelationExtractor(method="llm", provider="groq", llm_model="llama-3.3-70b-versatile")
relationships = rel.extract(text, entities=entities)
```

</CodeGroup>

</Step>

<Step title="构建知识图谱">

把抽取出的实体和关系组装成可查询的知识图谱。

```python
from semantica.kg import GraphBuilder

builder = GraphBuilder(merge_entities=True)
graph   = builder.build({"entities": entities, "relationships": relationships})

print(f"Graph: {len(graph['entities'])} nodes, {len(graph['relationships'])} edges")
```

<Note>
  `merge_entities=True` 自动消解重复的实体指称——"Apple"、"Apple Inc."、"AAPL" 会依据语义相似度合并，无需手工去重。
</Note>

</Step>

<Step title="可视化">

在浏览器里渲染可交互、可缩放的知识图谱。

```python
from semantica.visualization import KGVisualizer

viz = KGVisualizer(
    layout="force",        # "force" | "hierarchical" | "circular"
)
viz.visualize_network(graph, output="html", file_path="graph.html", node_color_by="type")
```

用任意浏览器打开 `graph.html`：平移、缩放、点击节点看详情、按实体类型过滤。

</Step>

<Step title="导出">

导出为任意下游格式。

<CodeGroup>

```python RDF / Semantic Web
from semantica.export import RDFExporter

exporter = RDFExporter()
exporter.export(graph, file_path="graph.ttl",    format="turtle")
exporter.export(graph, file_path="graph.jsonld", format="json-ld")
exporter.export(graph, file_path="graph.nt",     format="nt")
```

```python Parquet / Analytics
from semantica.export import ParquetExporter

exporter = ParquetExporter()
exporter.export(graph, file_path="output/graph")
# Dict input writes one file per key: output/graph_entities.parquet and
# output/graph_relationships.parquet: ready for Spark, BigQuery, Databricks
```

```python ArangoDB
from semantica.export import ArangoAQLExporter

exporter = ArangoAQLExporter()
exporter.export(graph, file_path="graph.aql")
# Writes ready-to-run AQL INSERT statements to graph.aql
```

</CodeGroup>

</Step>

</Steps>


## 加入决策智能(Decision Intelligence)

用完整的因果链和溯源(Provenance)追踪每个智能体(Agent)决策——只需多写一行导入：

```python
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore

context = AgentContext(
    vector_store=VectorStore(backend="faiss", dimension=768),
    knowledge_graph=ContextGraph(advanced_analytics=True),
    decision_tracking=True,
)

# Store a fact with provenance
context.store("GPT-4 outperforms GPT-3.5 on reasoning benchmarks by 40%")

# Record a decision
decision_id = context.record_decision(
    category="model_selection",
    scenario="Choose LLM for production reasoning pipeline",
    reasoning="GPT-4 benchmark advantage justifies 3x cost increase",
    outcome="selected_gpt4",
    confidence=0.91,
)

# Retrieve similar past decisions: prevents inconsistent choices
precedents = context.find_precedents("model selection reasoning", limit=5)
influence  = context.analyze_decision_influence(decision_id)
```


## 常见模式

<AccordionGroup>

<Accordion title="直接处理原始文本：不需要文件" icon="text">

```python
from semantica.semantic_extract import NERExtractor, RelationExtractor

text = "Apple Inc. was founded by Steve Jobs, Steve Wozniak, and Ronald Wayne in 1976 in Cupertino, California."

ner           = NERExtractor()
entities      = ner.extract(text)

rel           = RelationExtractor()
relationships = rel.extract(text, entities=entities)
```

</Accordion>

<Accordion title="多来源增量构建图谱" icon="layer-group">

```python
from semantica.kg import GraphBuilder

builder     = GraphBuilder(merge_entities=True)
all_entities, all_rels = [], []

for doc in parsed_docs:
    entities = ner.extract(doc)
    rels     = rel.extract(doc, entities=entities)
    all_entities.extend(entities)
    all_rels.extend(rels)

graph = builder.build({"entities": all_entities, "relationships": all_rels})
```

</Accordion>

<Accordion title="时态知识图谱与时间点查询" icon="clock">

```python
from semantica.kg import GraphBuilder, TemporalGraphQuery

builder = GraphBuilder()
kg = builder.build({
    "entities": [
        {"id": "alice",     "type": "Person"},
        {"id": "acme_corp", "type": "Organization"},
        {"id": "beta_ltd",  "type": "Organization"},
    ],
    "relationships": [
        {
            "source": "alice", "target": "acme_corp", "type": "ceo_of",
            "valid_from": "2018-01-01", "valid_until": "2022-06-01",
        },
        {
            "source": "alice", "target": "beta_ltd", "type": "ceo_of",
            "valid_from": "2022-06-01",
        },
    ],
})

tq = TemporalGraphQuery(temporal_granularity="day")

result_2020 = tq.query_at_time(kg, query="",  # query reserved for future use
                               at_time="2020-06-15")
result_2023 = tq.query_at_time(kg, query="", at_time="2023-01-01")

print(f"Relationships active in 2020: {result_2020['num_relationships']}")
print(f"Relationships active in 2023: {result_2023['num_relationships']}")
```

</Accordion>

<Accordion title="持久化图存储：Neo4j、FalkorDB、Apache AGE" icon="database">

```python
from semantica.graph_store import GraphStore
from semantica.kg import GraphBuilder

store = GraphStore(
    backend="neo4j",
    uri="bolt://localhost:7687",
    user="neo4j",
    password="password",
)

builder = GraphBuilder(merge_entities=True, graph_store=store)
graph   = builder.build({"entities": entities, "relationships": relationships})
# Graph persisted to Neo4j: survives process restarts
```

</Accordion>

<Accordion title="完整溯源流水线：W3C PROV-O" icon="link">

```python
from semantica.provenance import ProvenanceManager
from semantica.kg import GraphBuilder

prov    = ProvenanceManager()
prov.track_entity("Apple Inc.", "data/report.pdf", metadata={"confidence": 0.98})

builder = GraphBuilder(merge_entities=True)
graph   = builder.build({"entities": entities, "relationships": relationships})

# Retrieve full lineage for any entity
sources = prov.get_all_sources("Apple Inc.")
print(sources[0])
# {"source": "data/report.pdf", "location": None, "timestamp": "...",
#  "confidence": 1.0, "metadata": {"confidence": 0.98}}
```

</Accordion>

</AccordionGroup>


## 故障排查

<AccordionGroup>

<Accordion title="抽取不到任何实体" icon="magnifying-glass">

文档很可能是扫描图像，不是机器可读文本。`DocumentParser` 在 PDF 没有文本层时会告警；改用启用 OCR 的 `DoclingParser`：

```python
from semantica.parse import DoclingParser   # pip install semantica[parse-docling]

parser = DoclingParser(enable_ocr=True)
parsed = parser.parse(sources[0].path)
```

</Accordion>

<Accordion title="大规模语料处理缓慢" icon="gauge">

安装 GPU extras，让嵌入和 ML 推理跑在 CUDA 上：

```bash
pip install semantica[gpu]
```

先扫描目录拿到路径（不读文件内容），再逐个处理文档，写入持久化图后端而不是内存图：

```python
from semantica.ingest import FileIngestor
from semantica.parse import DocumentParser
from semantica.semantic_extract import NERExtractor, RelationExtractor
from semantica.graph_store import GraphStore
from semantica.kg import GraphBuilder

ingestor = FileIngestor()
parser   = DocumentParser()
ner      = NERExtractor(method="pattern")
rel      = RelationExtractor(method="pattern")
store    = GraphStore(backend="neo4j", uri="bolt://localhost:7687",
                      user="neo4j", password="password")
builder  = GraphBuilder(merge_entities=True, graph_store=store)
for info in ingestor.scan_directory("data/reports/", recursive=True):
    text     = parser.parse(info["path"])["full_text"]   # one document loaded at a time
    entities = ner.extract(text)
    rels     = rel.extract(text, entities=entities)
    builder.build({"entities": entities, "relationships": rels})
```

要多步编排与可配置并行度，见 [Pipeline 指南](../guides/pipeline.md)。

</Accordion>

<Accordion title="大图谱内存不足" icon="memory">

从内存态 NetworkX 切换到持久化后端：

```python
from semantica.graph_store import FalkorDBStore

store   = FalkorDBStore(host="localhost", port=6379)
builder = GraphBuilder(merge_entities=True, graph_store=store)
```

</Accordion>

<Accordion title="企业网关下 NER 回落到模式模式" icon="triangle-exclamation">

**v0.5.0** 已修复。升级即可：

```bash
pip install --upgrade semantica
```

</Accordion>

</AccordionGroup>


## 下一步

- [核心概念](../concepts.md) — 知识图谱、本体、推理引擎：Semantica 背后的心智模型。
- [模块参考](../modules.md) — 逐模块讲解关键类和常见流水线组合。
- [API 参考](../reference/context.md) — 每个模块、类、参数的完整文档。
- [Cookbook](../cookbook.md) — 40 多个基于真实数据集的交互式 Jupyter 笔记本。
