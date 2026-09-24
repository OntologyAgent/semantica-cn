---
title: 选对模块
description: 30 秒内把你的目标映射到正确的 Semantica 模块。
source: choose-your-module.md
source_version: 86ad3da1b0e618549fae5fa69ac7374d520e2d51
icon: "compass"
---

<Info>
  每个模块都独立可用——只导入你需要的部分。本页把开发目标映射到起点模块。[模块参考](./modules.md)深入讲解每个模块。
</Info>

## 速查表

在下表找到你的目标。**模块**列是导入路径；**关键类**是你首先要实例化的类。

| 我想…… | 模块 | 关键类 |
| :------------ | :------ | :--------- |
| 加载 PDF、DOCX、HTML、CSV 或压缩包 | `ingest` | `FileIngestor` |
| 爬取网站 | `ingest` | `WebIngestor` |
| 加载 Parquet 文件或分区数据集 | `ingest` | `ParquetIngestor` |
| 摄取 XML 并做 schema 校验 | `ingest` | `XMLIngestor` |
| 从 SQL、Snowflake、Databricks、Kafka 或邮件摄取 | `ingest` | `DBIngestor`, `SnowflakeIngestor`, `DatabricksIngestor`, `StreamIngestor` |
| 从文档抽取干净的文本和表格 | `parse` | `DocumentParser` |
| 解析需要 OCR 或多栏版面的复杂 PDF | `parse` | `DoclingParser` |
| 解析扫描件、公式密集或中文 PDF | `parse` | `MinerUParser` |
| 为嵌入(Embedding)或检索增强生成(RAG)切分文本 | `split` | `TextSplitter` |
| 规范化文本、日期、实体或编码 | `normalize` | `TextNormalizer`, `EntityNormalizer` |
| 在文本中识别人名、机构、地名等命名实体 | `semantic_extract` | `NERExtractor` |
| 从文本抽取带类型的关系 | `semantic_extract` | `RelationExtractor` |
| 抽取资源描述框架(RDF)主谓宾三元组(Triplet) | `semantic_extract` | `TripletExtractor` |
| 构建可查询的知识图谱(Knowledge Graph) | `kg` | `GraphBuilder` |
| 给事实加上时间有效期（`valid_from` / `valid_until`） | `kg` | `TemporalGraphQuery` |
| 跑图算法（中心度、社区、路径） | `kg` | `GraphAnalyzer`, `CentralityCalculator` |
| 生成向量嵌入 | `embeddings` | `EmbeddingGenerator` |
| 存储和检索向量 | `vector_store` | `VectorStore` |
| 把图持久化到 Neo4j 或 FalkorDB | `graph_store` | `Neo4jStore`, `FalkorDBStore` |
| 存储 RDF 三元组并用 SPARQL 查询 | `triplet_store` | `TripletStore` |
| 跨来源去重实体 | `deduplication` | `DuplicateDetector`, `EntityMerger` |
| 检测并消解矛盾事实 | `conflicts` | `ConflictDetector`, `ConflictResolver` |
| 给 AI 智能体持久记忆 | `context` | `AgentContext` |
| 让大语言模型(LLM)回答扎根于知识图谱（GraphRAG） | `context` | `AgentContext.query_with_reasoning()` |
| 记录 AI 决策，带完整审计轨迹 | `context` | `AgentContext.record_decision()` |
| 做新决策前检索历史决策 | `context` | `AgentContext.find_precedents()` |
| 追踪决策的因果链 | `context` | `AgentContext.get_causal_chain()` |
| 追踪每条事实的来源（W3C PROV-O） | `provenance` | `ProvenanceManager` |
| 用校验和与回滚做图版本控制 | `change_management` | `TemporalVersionManager` |
| 从图自动生成 OWL 模式 | `ontology` | `OntologyGenerator` |
| 用 SHACL 约束校验图 | `ontology` | `SHACLGenerator`, `OntologyValidator` |
| 从已有知识推导新事实 | `reasoning` | `Reasoner`, `GraphReasoner` |
| 导出为 RDF Turtle、JSON-LD 或 N-Triples | `export` | `RDFExporter` |
| 导出 Parquet 供 Spark / BigQuery 使用 | `export` | `ParquetExporter` |
| 为 ArangoDB 导出 | `export` | `ArangoAQLExporter` |
| 经 Cypher 写入 Neo4j 或 Memgraph | `export` | `LPGExporter` |
| 交互式可视化知识图谱 | `visualization` | `KGVisualizer` |
| 跑可复现的多步流水线 | `pipeline` | `PipelineBuilder` |
| 在 Claude Desktop 或 Cursor 里使用 Semantica | `mcp_server` | `semantica-mcp` |
| 用可信种子数据引导图 | `seed` | `SeedDataManager` |
| 用自定义组件扩展 Semantica | `core` | `PluginRegistry` |


## 逐目标起步指南

选一个目标，查看最少导入和可运行的骨架代码。

<Tabs>
  <Tab title="构建知识图谱">
    把文档、网页或数据库变成结构化、可查询的图。

    **流水线：** `ingest` → `parse` → `semantic_extract` → `kg`

    ```python
    from semantica.ingest import FileIngestor
    from semantica.parse import DocumentParser
    from semantica.semantic_extract import NERExtractor, RelationExtractor
    from semantica.kg import GraphBuilder

    sources       = FileIngestor().ingest("report.pdf")
    parsed        = DocumentParser().parse_document("report.pdf")

    # 无需 API key——基于模式的抽取
    entities      = NERExtractor(method="pattern").extract(parsed)
    relationships = RelationExtractor(method="rule").extract(parsed, entities=entities)

    graph = GraphBuilder(merge_entities=True).build(
        sources=[{"entities": entities, "relationships": relationships}]
    )
    print(f"{len(graph.nodes)} nodes, {len(graph.edges)} edges")
    ```

    <Tip>
      给 `NERExtractor` 传 `method="pattern"`，零成本、零 API key 即可抽取。想要更高召回率，换成 `method="llm"`，任选受支持的提供商。
    </Tip>

    **下一步：** [快速开始 →](./quickstart.md)——带可视化和导出的完整流水线。
  </Tab>

  <Tab title="构建 GraphRAG">
    让 LLM 的每条回答都扎根于结构化知识图谱。每条断言都链回一个源节点。

    **模块：** `context`

    ```python
    from semantica.context import AgentContext, ContextGraph
    from semantica.vector_store import VectorStore
    from semantica.llms import Groq

    llm = Groq(model="llama-3.3-70b-versatile")

    context = AgentContext(
        vector_store=VectorStore(backend="faiss", dimension=768),
        knowledge_graph=ContextGraph(advanced_analytics=True),
    )

    # 存事实——检索同时用向量和图结构
    context.store("Apple Inc. was co-founded by Steve Jobs in 1976 in Cupertino.")

    # GraphRAG 查询，带多跳推理轨迹
    result = context.query_with_reasoning(
        "Who co-founded Apple?",
        llm_provider=llm,
        max_hops=2,
    )
    print(result["response"])        # 有根据的回答
    print(result["reasoning_path"])  # 多跳推理轨迹
    ```

    **下一步：** [Context 模块参考 →](reference/context.md)
  </Tab>

  <Tab title="添加智能体记忆">
    给 AI 智能体跨会话的持久记忆、决策追踪和先例检索。

    **模块：** `context`

    ```python
    from semantica.context import AgentContext, ContextGraph
    from semantica.vector_store import VectorStore

    context = AgentContext(
        vector_store=VectorStore(backend="faiss", dimension=768),
        knowledge_graph=ContextGraph(advanced_analytics=True),
        decision_tracking=True,   # 使用 record_decision() 必须开启
    )

    # 存一条记忆
    context.store("GPT-4 outperforms GPT-3.5 on reasoning benchmarks by 40%.")

    # 记录决策，带完整因果上下文
    decision_id = context.record_decision(
        category="model_selection",
        scenario="Choose LLM for production reasoning pipeline",
        reasoning="GPT-4 benchmark advantage justifies cost increase",
        outcome="selected_gpt4",
        confidence=0.91,
    )

    # 做新决策前先检索历史决策
    precedents = context.find_precedents("model selection", limit=5)

    # 追踪该决策下游发生了什么
    chain = context.get_causal_chain(decision_id, direction="downstream")
    ```

    <Note>
      必须设置 `decision_tracking=True`。否则 `record_decision()` 会抛 `RuntimeError`。
    </Note>

    **下一步：** [Context 模块参考 →](reference/context.md)
  </Tab>

  <Tab title="追踪溯源">
    每条事实都有 W3C PROV-O 血缘：来源文档、抽取方法、时间戳和校验和。

    **模块：** `provenance`、`change_management`

    ```python
    from semantica.provenance import ProvenanceManager

    prov = ProvenanceManager()

    # 追踪实体，带完整来源信息
    prov.track_entity(
        entity_id="entity_1",
        source="DOI:10.1371/journal.pone.0023601",
        source_location="Figure 2",
        confidence=0.92,
    )

    # 取回该实体的完整血缘
    lineage = prov.get_lineage("entity_1")

    # 用 SHA-256 校验和给图做版本控制
    from semantica.change_management import TemporalVersionManager

    manager  = TemporalVersionManager()
    snapshot = manager.create_snapshot(kg, "v1.0", "user@example.com", "Initial build")
    diff     = manager.diff("v1.0", "v1.1")
    ```

    **下一步：** [溯源参考 →](reference/provenance.md) · [变更管理参考 →](reference/change_management.md)
  </Tab>

  <Tab title="导出">
    把知识图谱序列化，供语义网、分析平台或图数据库使用。

    **模块：** `export`

    ```python
    from semantica.export import RDFExporter, ParquetExporter, LPGExporter, ArangoAQLExporter

    # RDF——多种序列化格式
    RDFExporter().export(graph, "graph.ttl",    format="turtle")
    RDFExporter().export(graph, "graph.jsonld", format="jsonld")

    # Parquet——供 Spark、BigQuery、Databricks、Snowflake 使用
    ParquetExporter().export(graph, "output/graph.parquet")

    # 经 Cypher 写入 Neo4j / Memgraph
    LPGExporter().export(graph, "graph.cypher")

    # ArangoDB AQL 插入语句
    ArangoAQLExporter().export(graph, "graph.aql")
    ```

    **格式：** Turtle · JSON-LD · N-Triples · RDF/XML · Parquet · Cypher · Arrow · OWL · CSV · ArangoDB AQL

    **下一步：** [Export 模块参考 →](reference/export.md)
  </Tab>

  <Tab title="MCP——Claude / Cursor">
    在 Claude Desktop、Cursor、VS Code 或任何支持模型上下文协议(MCP)的工具里使用 Semantica——配置完成后无需写 Python 代码。可用工具共 15 个。

    **第 1 步——安装：**
    ```bash
    pip install semantica
    ```

    **第 2 步——加进 MCP 客户端配置：**

    <CodeGroup>

    ```json Claude Desktop / Windsurf / Cline
    {
      "mcpServers": {
        "semantica": {
          "command": "semantica-mcp"
        }
      }
    }
    ```

    ```json Cursor / VS Code / Continue
    {
      "mcpServers": {
        "semantica": {
          "command": "semantica-mcp",
          "env": {
            "SEMANTICA_KG_PATH": "/path/to/my_graph.json"
          }
        }
      }
    }
    ```

    </CodeGroup>

    **可用工具：** `extract_entities` · `extract_relations` · `add_entity` · `add_relationship` · `record_decision` · `query_decisions` · `find_precedents` · `get_causal_chain` · `run_reasoning` · `get_graph_analytics` · `export_graph` · `get_graph_summary`

    <Warning>
      设置 `SEMANTICA_KG_PATH` 让图在重启后仍然保留。不设置的话，服务器进程退出时所有数据都会丢失。
    </Warning>

    **下一步：** [MCP 服务器参考 →](reference/mcp_server.md)
  </Tab>
</Tabs>


## 还拿不准？

<AccordionGroup>
  <Accordion title="知识图谱还是向量库——我需要哪个？" icon="scale-balanced">
    需要结构化推理、多跳遍历、溯源或合规审计轨迹时，用**知识图谱**（`kg`）。

    需要在大规模文本语料上做快速模糊相似度检索、且条目之间的关系不重要时，用**向量库**（`vector_store`）。

    也可以通过 `AgentContext`（GraphRAG）**把两者结合起来**：让 LLM 的回答有根据，每条断言都能追溯到源节点。

    另见：[核心概念](./concepts.md)
  </Accordion>

  <Accordion title="我只想先快速跑起来。" icon="rocket">
    从[快速开始](./quickstart.md)入手。它搭建一条完整流水线（摄取 → 解析 → 抽取 → 图 → 可视化 → 导出），无需 API key。
  </Accordion>

  <Accordion title="把 Semantica 接进已有智能体——最小改动是什么？" icon="plug">
    加上 `AgentContext` 即可。它为现有智能体补上记忆、决策追踪和先例检索，而 LLM 提供商和智能体框架都不用改。

    ```python
    from semantica.context import AgentContext, ContextGraph
    from semantica.vector_store import VectorStore

    context = AgentContext(
        vector_store=VectorStore(backend="faiss", dimension=768),
        knowledge_graph=ContextGraph(advanced_analytics=True),
        decision_tracking=True,
    )
    ```

    [Context 模块参考 →](reference/context.md)
  </Accordion>

  <Accordion title="我要合规就绪的流水线——最小技术栈是什么？" icon="shield-check">
    | 层 | 模块 | 关键类 |
    | :---- | :------ | :--------- |
    | 摄取 | `ingest` | `FileIngestor` |
    | 抽取 | `semantic_extract` | `NERExtractor` |
    | 图 | `kg` | `GraphBuilder` |
    | 血缘 | `provenance` | `ProvenanceManager` |
    | 版本 | `change_management` | `TemporalVersionManager` |
    | 审计导出 | `export` | `RDFExporter` |

    支持 HIPAA、SOX、GDPR 和 FDA 21 CFR Part 11 审计要求。
  </Accordion>
</AccordionGroup>

---

- [快速开始](./quickstart.md) — 5 分钟跑通完整流水线。
- [模块参考](./modules.md) — 每个模块的示例与常见组合。
- [API 参考](reference/context.md) — 完整的类与方法文档。
