---
title: 快速开始
description: 5 分钟搭好你的第一个知识图谱，无需任何配置。
source: quickstart.md
source_version: d802dc5ef05d7f4ccfed8eb17e1521450eba4c64
icon: "rocket"
---

<Info>
  **v0.5.0** — 本体中心、距离智能、Parquet 与 XML 摄取、12 项安全修复。<a href="https://github.com/semantica-agi/semantica/releases" style={{color:"#10B981",fontWeight:600,textDecoration:"none"}}>看看有什么新东西 →</a>
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
# 0.5.0
```


## 完整流水线

<img src="/assets/img/diagrams/pipeline-flow.svg" alt="Semantica 端到端流水线：摄取 → 解析 → 规范化 → 抽取 → 构建知识图谱 → 质检 → 存储 → 交付" style={{ width: '100%', borderRadius: '10px', margin: '0 0 24px' }} />

<Steps>

<Step title="摄取(Ingest)">

从文件、目录、URL 或数据库加载文档。

<CodeGroup>

```python File
from semantica.ingest import FileIngestor

ingestor = FileIngestor()
sources  = ingestor.ingest("data/report.pdf")
# Also accepts: .docx, .html, .json, .csv, .xlsx, .pptx, .parquet, .xml
```

```python Web
from semantica.ingest import WebIngestor

ingestor = WebIngestor(max_depth=2)
sources  = ingestor.ingest("https://example.com/article")
```

```python Parquet / XML (v0.5.0)
from semantica.ingest import ParquetIngestor, XMLIngestor

# Single file or Hive-partitioned directory
sources = ParquetIngestor().ingest("data/events.parquet")

# XML with XSD schema validation
sources = XMLIngestor(validate_xsd="schema.xsd").ingest("data/records/")
```

</CodeGroup>

</Step>

<Step title="解析(Parse)">

从原始文档提取结构化文本和版面信息。

```python
from semantica.parse import DocumentParser

parser = DocumentParser()
parsed = parser.parse(sources[0])

print(parsed.text[:200])  # 提取出的文本
print(parsed.metadata)    # 标题、作者、日期、来源
```

<Tip>
  处理带表格、图表或多栏版面的 PDF 时，用 `DoclingParser`：它会做高级版面分析，在文本之外还返回结构化的表格数据。
</Tip>

```python
from semantica.parse import DoclingParser

parser = DoclingParser()
parsed = parser.parse(sources[0])
print(parsed.tables)  # 结构化表格对象
```

</Step>

<Step title="抽取实体与关系">

识别命名实体，抽取实体之间带类型的语义关系。

<CodeGroup>

```python Pattern-based (fast, no API key)
from semantica.semantic_extract import NERExtractor, RelationExtractor

ner      = NERExtractor(method="pattern")
entities = ner.extract(parsed)
# Returns: [{"text": "Apple Inc.", "type": "ORGANIZATION", "confidence": 0.98}, ...]

rel           = RelationExtractor(method="rule")
relationships = rel.extract(parsed, entities=entities)
# Returns: [{"subject": "Steve Jobs", "predicate": "founded", "object": "Apple Inc."}, ...]
```

```python LLM-powered (higher accuracy)
from semantica.semantic_extract import NERExtractor, RelationExtractor
from semantica.llms import Groq

llm = Groq(model="llama-3.3-70b-versatile")

ner           = NERExtractor(method="llm", llm_provider=llm)
entities      = ner.extract(parsed)

rel           = RelationExtractor(method="llm", llm_provider=llm)
relationships = rel.extract(parsed, entities=entities)
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
exporter.export(graph, file_path="output/graph.parquet")
# Writes nodes.parquet + edges.parquet: ready for Spark, BigQuery, Databricks
```

```python ArangoDB
from semantica.export import ArangoAQLExporter

exporter = ArangoAQLExporter()
aql      = exporter.export(graph)
# Returns ready-to-run AQL INSERT statements
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
# {"source": "data/report.pdf", "location": None, "timestamp": "...", "confidence": 0.98}
```

</Accordion>

</AccordionGroup>


## 故障排查

<AccordionGroup>

<Accordion title="抽取不到任何实体" icon="magnifying-glass">

文档很可能是扫描图像，不是机器可读文本。启用 OCR：

```python
from semantica.parse import DocumentParser

parser = DocumentParser(ocr=True)  # enables Tesseract OCR
parsed = parser.parse(sources[0])
```

</Accordion>

<Accordion title="大规模语料处理缓慢" icon="gauge">

开启并行处理和 GPU 加速：

```bash
pip install semantica[gpu]
```

```python
from semantica.pipeline import Pipeline

pipeline = Pipeline(workers=8, batch_size=32)
pipeline.run(sources)
```

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
