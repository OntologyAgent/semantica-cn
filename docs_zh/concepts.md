---
title: 核心概念
description: Semantica 背后的基本理念：知识图谱、推理、溯源与时态智能。
source: concepts.md
source_version: d2ead7fa52cafd647ca5d8a0f6c8964483d4f825
icon: "book-open"
---

<Info>
  第一次接触？先读[入门指南](./getting-started.md)跑通示例，再回来深入理解。
</Info>

Semantica 把非结构化数据——文档、网页、报告、数据库——变成**知识图谱(Knowledge Graph)**：一种结构化表示，AI 系统可以在上面查询、推理，还能回溯到源头。

Semantica 的核心，是在你现有的 AI 技术栈之上加一层**上下文与问责层**。它不替代 LangChain、LlamaIndex 或你的 LLM 提供商——它让它们的输出**有根据**、**可追溯**、**可审计**。

- **上下文层** — 知识图谱、GraphRAG 检索、语义嵌入(Embedding)与时态智能，让大语言模型(LLM)的每条回答都扎根于结构化、可查询的事实。
- **问责层** — 溯源(Provenance)追踪、决策智能(Decision Intelligence)、冲突检测与 W3C PROV-O 合规，让 AI 技术栈里的每条断言都可审计、可解释。
- **扩展层** — `PluginRegistry` 和 `MethodRegistry` 让你替换或增强任意组件——摄取器、抽取器、推理引擎、后端——而无需改动框架代码。

<Warning>
  **这是系统级可解释性，不是基础模型可解释性。** Semantica 不暴露、不重建、不解释 LLM/基础模型*内部*发生了什么——其内部推理或思维链对外部系统始终是不透明的。Semantica 解释的是模型*之外*的部分：输入的上下文和数据、产生的决策、它的溯源、相关的关系、适用的策略，以及完整的执行轨迹。一句话：Semantica 解释和审计的是 *AI 系统做了什么*，而不是基础模型私有的内部推理。
</Warning>

## 知识图谱

<img src="../docs/assets/img/diagrams/kg-structure.svg" alt="知识图谱的节点与边结构：实体（Person、Organization、Location、Date）及其类型化关系" style={{ width: '100%', borderRadius: '12px', margin: '0 0 20px' }} />

先用一句大白话点破：知识图谱就是把散落的事实连成一张关系网——节点是人、公司、事件，边是它们之间的关系。它是 Semantica 一切能力的基石，具体用三种积木存储信息：

- **节点（实体）**：人物、公司、地点、事件、概念
- **边（关系）**：`works_for`、`located_in`、`founded_by`
- **属性**：名称、日期、置信度、来源 URL

这种结构让知识**可搜索**、**可关联**、**可查询**，也——最关键的——**可解释**：每个答案都能回溯到产生它的事实和关系。


## 实体抽取（NER）

扫描文本，找出并分类现实世界中的实体：

```python
# "Apple Inc. was founded by Steve Jobs in 1976 in Cupertino."
[
    Entity(text="Apple Inc.", label="ORG",    start_char=0,  end_char=10, confidence=0.98),
    Entity(text="Steve Jobs", label="PERSON", start_char=25, end_char=35, confidence=0.99),
    Entity(text="1976",       label="DATE",   start_char=39, end_char=43, confidence=0.95),
    Entity(text="Cupertino",  label="GPE",    start_char=47, end_char=56, confidence=0.97),
]
```

`NERExtractor(method=...).extract(text)` 返回一组 `Entity` 对象，每个都带 `label`、字符偏移（`start_char` / `end_char`）、`confidence` 分数，以及记录抽取方式的 `metadata` 字典。三种方法可选：

| 方法 | 速度 | 准确率 | 要求 |
| :------ | :----- | :-------- | :------------ |
| `"pattern"` | ⚡ 非常快 | 中等 | 无需 API key：基于正则 |
| `"ml"` | 快 | 高 | 本地 ML 模型 |
| `"llm"` | 中等 | 最高 | LLM 提供商：支持全部 9 家 |

## 关系抽取

找出实体之间如何关联：

```python
jobs  = Entity(text="Steve Jobs", label="PERSON", start_char=25, end_char=35)
apple = Entity(text="Apple Inc.", label="ORG",    start_char=0,  end_char=10)

[
    Relation(subject=jobs,  predicate="founded",     object=apple, confidence=0.92),
    Relation(subject=apple, predicate="located_in",  object=Entity(text="Cupertino", label="GPE", start_char=47, end_char=56), confidence=0.89),
]
```

`RelationExtractor(method=...).extract(text, entities=entities)` 返回一组 `Relation` 对象：类型化的「主语-谓语-宾语」三元组(Triplet)，端点是 `Entity` 对象，并带置信度分数与来源标注。具体抽取方式有三种：模式规则、ML 模型或 LLM。


## 知识图谱与向量库

两者都为 AI 检索存储信息，不过设计目标不同。

<Tabs>
  <Tab title="知识图谱">
    它以类型化节点和带标签的边存储**结构化事实**，适合回答那些需要理解实体之间关系的问题。

    | 优势 | 为什么重要 |
    | :-------- | :------------- |
    | **图遍历** | 多跳查询："在 Apple 工作过的人后来创办了哪些公司？" |
    | **可解释性** | 每个答案都回溯到具体的节点和边——没有黑盒检索 |
    | **时态推理** | 时间点查询、`valid_from`/`valid_until` 窗口、历史快照 |
    | **冲突检测** | 两个来源对同一事实不一致时，Semantica 会把冲突标出来，并可进一步消解 |
    | **模式校验** | SHACL 校验会在违规数据污染结果之前把问题拦下 |

    **适用场景：** 需要结构化推理、溯源、合规或可解释性时。

    ```python
    from semantica.kg import GraphBuilder, PathFinder

    graph = GraphBuilder(merge_entities=True).build(
        {"entities": entities, "relationships": rels}
    )
    path  = PathFinder().dijkstra_shortest_path(graph, "Steve Jobs", "Tim Cook")
    ```
  </Tab>

  <Tab title="向量库">
    它存储文本分块(Chunking)的**稠密嵌入(Embedding)**，通过寻找语义相近的段落来回答问题——答案结构事先未知时很有用。

    | 优势 | 为什么重要 |
    | :-------- | :------------- |
    | **模糊相似** | 措辞不同也能找到相关内容 |
    | **速度** | 规模化场景下亚毫秒级的近似最近邻搜索 |
    | **非结构化文本** | 直接作用于段落、句子和原始文档 |
    | **简单** | 无需设计模式：嵌入、建索引即可 |

    **适用场景：** 需要在大规模文本语料上做快速语义检索时。

    ```python
    from semantica.vector_store import VectorStore

    store   = VectorStore(backend="faiss", dimension=768)
    store.add_documents(["Apple was founded in 1976.", "Google was founded in 1998."])
    results = store.search("tech company founding dates", limit=5)
    ```
  </Tab>

  <Tab title="GraphRAG（两者结合）">
    Semantica 把两者结合起来：向量检索为图遍历提供种子，图谱则提供向量库给不了的结构与溯源。

    | 步骤 | 发生什么 |
    | :---- | :----------- |
    | **查询嵌入** | 先把用户查询向量化，再用向量相似度找到锚点节点 |
    | **图遍历** | 从锚点节点出发多跳遍历，取回相关实体和关系 |
    | **上下文组装** | 把事实和关系组装起来，每条断言都带来源标注 |
    | **LLM 生成** | LLM 在取回的结构化上下文之上生成回答 |

    **结果：** 回答中的每条断言都链回具体的图节点——没有来自训练数据的幻觉，全程可审计。

    ```python
    from semantica.context import AgentContext, ContextGraph
    from semantica.vector_store import VectorStore

    context = AgentContext(
        vector_store=VectorStore(backend="faiss", dimension=768),
        knowledge_graph=ContextGraph(advanced_analytics=True),
        graph_expansion=True,
    )
    # store() extracts entities and populates the graph + vector index
    context.store([{"content": "Steve Jobs co-founded Apple Inc. in 1976."}])
    # retrieve() blends vector similarity with graph traversal
    results = context.retrieve("Who founded Apple?", use_graph=True, expand_graph=True)
    for r in results:
        print(r["score"], r["content"], r["source"])
    ```
  </Tab>
</Tabs>


## 嵌入(Embedding)

嵌入把文本转成数值向量，让 AI 系统能度量语义相似度——措辞不同也能找到相关概念。

Semantica 在这些场景使用嵌入：

- **语义检索**：按含义检索，而不只是关键词
- **实体消解(Entity Resolution)**：跨来源匹配同一实体
- **先例检索**：找到相似的历史决策
- **GraphRAG 检索**：向量 + 图遍历的混合检索(Hybrid Search)
- **距离智能**：任意节点集之间的 N×N 语义距离矩阵

**支持的模型：** Sentence-Transformers、FastEmbed、OpenAI、BGE、Ollama 本地嵌入。


## GraphRAG

GraphRAG 是图增强的检索增强生成(RAG)：它让 LLM 的回答扎根于结构化知识图谱，而不只是原始文本块，从而提升回答质量。

<img src="../docs/assets/img/diagrams/graphrag-flow.svg" alt="GraphRAG 流程：用户查询 → 向量检索 + 图遍历 → 上下文构建 → LLM → 有根据的回答" style={{ width: '100%', borderRadius: '12px', margin: '16px 0 20px' }} />

<Steps>
  <Step title="用户提交查询">
    系统先把查询向量化，再用它同时启动向量检索和图遍历。
  </Step>
  <Step title="混合上下文检索">
    Semantica 会取回相关的图谱上下文——实体、类型化关系、多跳推理路径——同时也取回向量相似的文本块。
  </Step>
  <Step title="上下文构建">
    Semantica 把取回的事实和推理路径组装成结构化的提示上下文，每条事实都标注源节点和置信度。
  </Step>
  <Step title="LLM 生成有根据的回答">
    LLM 产出的回答中，每条断言都链回图中的源节点——没有无根据的断言，没有来自训练数据的幻觉。
  </Step>
</Steps>

<Tip>
  **GraphRAG 消除了标准 RAG 的幻觉与可追溯性问题。** 标准 RAG 检索文本块；GraphRAG 检索带类型化关系的结构化事实。图谱里从来没有的结构，LLM 编不出来。
</Tip>


## 本体(Ontology)

打个比方：如果知识图谱是一座图书馆，本体就是它的编目规则——什么书算一类、哪些书互相关联、上架要满足什么条件。具体来说，本体定义你的知识的模式与规则：存在哪些实体类型、哪些关系合法、适用什么约束。

```python
ontology = {
    "classes": ["Person", "Organization", "Location"],
    "relationships": ["works_for", "located_in", "founded_by"],
    "rules": {
        "Person":       ["must_have_name"],
        "Organization": ["must_have_name", "can_have_founding_date"]
    }
}
```

Semantica 可以从你的知识图谱自动生成本体，或导入现有的 OWL/RDF/Turtle 本体。**本体中心(Ontology Hub)**（v0.5.0）提供可视化编辑器、SHACL Studio、对齐编排和实时健康看板。完整的 6 阶段生成流水线见[本体参考](reference/ontology.md)。


## 推理与推断

说穿了，推理引擎就是把「顺藤摸瓜」交给机器：从已知事实出发，按规则一步步推出新事实。Semantica 内置多种推理引擎(Reasoning Engine)，从已有事实推导新知识。

```text
Known:    Steve Jobs founded Apple Inc.
Known:    Apple Inc. is headquartered in Cupertino
Inferred: Steve Jobs has a connection to Cupertino
```

<Tabs>
  <Tab title="前向链(Forward Chaining)">
    反复套用 IF/THEN 规则，直到推不出新事实。最适合告警系统、合规检查和触发式工作流。

    ```python
    from semantica.reasoning import Reasoner

    engine = Reasoner()
    engine.add_fact("Manager(Alice)")
    engine.add_rule("IF Manager(?x) THEN HasAuthority(?x)")
    results = engine.forward_chain()   # list of InferenceResult
    for r in results:
        print(r.conclusion)           # "HasAuthority(Alice)"
    ```
  </Tab>
  <Tab title="Rete 网络">
    Rete 算法的思路是：前置条件没变的规则不再重复求值，因此大规则集也能高效做模式匹配。最适合在百万级事实上跑数千条规则。

    ```python
    from semantica.reasoning import ReteEngine, Rule, Fact

    engine = ReteEngine()
    engine.build_network([
        Rule(rule_id="r1", name="manager_authority",
             conditions=["Manager(?x)"], conclusion="HasAuthority(?x)"),
    ])
    engine.add_fact(Fact(fact_id="f1", predicate="Manager", arguments=["Alice"]))
    matches = engine.match_patterns()
    results = engine.execute_matches(matches)   # ["HasAuthority(?x)"]
    ```
  </Tab>
  <Tab title="LLM 推理">
    `GraphReasoner` 用 LLM 回答对知识图谱的开放式问题，返回扎根于图事实的自然语言回答。最适合固定规则预判不了的探索性、调查性问题。

    ```python
    from semantica.reasoning import GraphReasoner

    reasoner = GraphReasoner(provider="openai", model="gpt-4o-mini")
    answer = reasoner.reason(kg, "Which suppliers are indirectly exposed to the Acme outage?")
    ```
  </Tab>
  <Tab title="Datalog (v0.4.0)">
    带不动点语义的递归 Horn 子句规则：能处理前向链表达不了的传递闭包和递归关系。

    ```python
    from semantica.reasoning import DatalogReasoner

    reasoner = DatalogReasoner()
    reasoner.add_fact("parent(alice, bob)")
    reasoner.add_fact("parent(bob, charlie)")
    reasoner.add_rule("ancestor(X, Y) :- parent(X, Y).")
    reasoner.add_rule("ancestor(X, Z) :- parent(X, Y), ancestor(Y, Z).")
    reasoner.derive_all()
    results = reasoner.query("ancestor(alice, ?Z)")   # {"Z": "bob"} and {"Z": "charlie"}, order not guaranteed
    ```
  </Tab>
  <Tab title="引擎对比">

    | 引擎 | 类 | 最适合 |
    | :------ | :----- | :-------- |
    | 前向链 | `Reasoner` | 告警系统、合规检查 |
    | Rete 网络 | `ReteEngine` | 大规则集、高事实吞吐 |
    | SPARQL 扩展 | `SPARQLReasoner` | RDF 上的语义网、本体推理 |
    | Datalog (v0.4.0) | `DatalogReasoner` | 传递闭包、图可达性 |
    | 时态 | `TemporalReasoningEngine` | Allen 区间代数、时间感知推理 |
    | 图上 LLM | `GraphReasoner` | 开放式、调查性问题 |

  </Tab>
</Tabs>

`Reasoner.forward_chain()` 返回的 `InferenceResult` 携带所用规则（`rule_used`）和触发前提，`ExplanationGenerator` 能把一条结果转成逐步的自然语言论证——这里的推理**不是**黑盒。


## 时态智能

知识随时间变化。时态图给节点和边挂上 `valid_from` / `valid_until` 窗口，支持时间点查询和历史分析。

```python
from semantica.kg import TemporalGraphQuery
from datetime import datetime

query_engine = TemporalGraphQuery(enable_temporal_reasoning=True)

# Query the graph as it existed on a specific date
snapshot = query_engine.query_at_time(kg, query="", at_time=datetime(2021, 6, 15))
```

**支持特性：** Allen 区间代数（全部 13 种时态关系）、OWL-Time 导出、`recorded_at` 时间戳、时态溯源。

**常见用途：** 追踪公司高管变动、政策演变、研究时间线、金融工具历史、监管合规窗口。


## 距离智能

探索图中任意实体的语义邻域——有助于理解概念上的远近、发现簇、可视化知识拓扑。

```python
from semantica.kg import SimilarityCalculator

calc = SimilarityCalculator(method="cosine")   # "cosine" | "euclidean" | "manhattan" | "correlation"
# Similarity for every unique pair of node embeddings: {(node_a, node_b): score}
pairs = calc.pairwise_similarity({"apple": vec_apple, "google": vec_google, "nest": vec_nest})
# Or rank a set of embeddings by closeness to one query vector
nearest = calc.find_most_similar(embeddings, query_embedding, top_k=10)
```

**特性：** N×N 语义距离矩阵、ego 模式可视化、距离带分类（`direct` / `near` / `mid-range` / `distant`）、面向大图谱的嵌入缓存优化。

[可视化模块](reference/visualization.md)把距离矩阵渲染成交互式热力图和 ego 模式邻域图。[Explorer](reference/explorer.md) 则把距离智能直接嵌进浏览器看板。


## 去重与实体消解

真实数据里，同一实体会以许多名字出现："Apple"、"Apple Inc."、"Apple Computer Inc."。Semantica 的去重流水线识别它们、合并属性、消解冲突，并保留原始来源溯源。

<Tabs>
  <Tab title="策略">

    | 策略 | 算法 | 最适合 |
    | :-------- | :--------- | :-------- |
    | `v1` | Jaro-Winkler 字符串相似度 | 小数据集、快速基线 |
    | `blocking_v2` | 候选分块阻塞 + 相似度 | 大语料：减少 O(n²) 比较 |
    | `hybrid_v2` | 分块阻塞 + 语义嵌入匹配 | 结构化/非结构化混合的实体名 |
    | `semantic_v2` | 纯嵌入消解 | 比 v1 快至 7 倍；能处理缩写和别名 |

  </Tab>
  <Tab title="配置">
    ```python
    from semantica.deduplication import DuplicateDetector, EntityMerger

    detector   = DuplicateDetector(similarity_threshold=0.85)
    candidates = detector.detect_duplicates(entities)

    merger = EntityMerger()
    operations = merger.merge_duplicates(entities, strategy="keep_most_complete")
    ```
  </Tab>
</Tabs>


## 溯源与可审计性

Semantica 里的每个事实都能回溯到：

- 它来自的**源文档**
- 所用的**抽取方法**（模式 / ML / LLM）
- 图构建时应用的**本体规则**
- 产生任何推断事实的**推理步骤**

<Note>
  这是兼容 W3C PROV-O 的血缘：适合要求审计轨迹的受监管行业（HIPAA、SOX、GDPR、FDA 21 CFR Part 11）。`ProvenanceManager.export_prov(format="turtle")` 把记录的血缘序列化为 PROV-O RDF。
</Note>

```python
from semantica.provenance import ProvenanceManager

prov = ProvenanceManager()
prov.track_entity("apple_inc", source="report.pdf",
                  metadata={"extractor": "NamedEntityRecognizer", "confidence": 0.98})

record = prov.get_provenance("apple_inc")   # dict; use get_lineage() for the full chain
print(record["source_document"])
print(record["timestamp"])
print(record["checksum"])
print(record["metadata"])          # extractor, confidence, and any custom keys
```


## 决策智能

在 Semantica 里，智能体(Agent)的每一个决策都是一等对象：有记录、有因果链接、可按先例检索。这也就是前面说的**问责层**：决策不再是转瞬即逝的日志，而是可查询的知识图谱节点。

```python
decision_id = context.record_decision(
    category="model_selection",
    scenario="Choose LLM for production pipeline",
    reasoning="GPT-4 benchmark advantage justifies 3x cost increase",
    outcome="selected_gpt4",
    confidence=0.91,
)

# Find similar past decisions before making a new one
precedents = context.find_precedents("model selection reasoning", limit=5)

# Trace downstream impact of a past decision
influence  = context.analyze_decision_influence(decision_id)
```

<Tip>
  **每个高风险决策之前，先用 `find_precedents()`。** 对全部已记录决策做混合相似度检索，能浮出可能适用的历史推理——减少智能体各次运行之间的不一致，让组织真正从 AI 决策历史中学习。
</Tip>


## 冲突检测

多个来源对同一事实不一致时，Semantica 不会静默挑一个值了事，而是先把冲突标记出来，再按策略消解(Conflict Resolution)。

**消解策略：**

- **新近优先**：偏向最新的来源
- **来源可信度**：偏向最可靠的来源（可信度分数可配置）
- **多数表决**：≥ 2 个来源一致时聚合采纳
- **人工复核**：打上人工仲裁的标记，流水线不阻塞、继续往下走

`ConflictResolver`、`SourceTracker` 和 `InvestigationGuideGenerator` 见[冲突参考](reference/conflicts.md)。


## 自定义插件开发

Semantica 从一开始就为扩展而设计。任何组件——摄取器、抽取器、图构建器、推理引擎——都允许你用运行时注册的自定义实现来替换或增强。

<AccordionGroup>
  <Accordion title="PluginRegistry：按名字替换任意组件">

    `PluginRegistry` 提供跨所有模块的动态插件发现、注册和加载。把你的类注册到一个字符串键下；此后凡是在配置或流水线步骤里引用该键的地方，Semantica 都会改用你的实现。

    ```python
    from semantica.core import PluginRegistry

    registry = PluginRegistry()

    # Register a custom ingestor
    registry.register_plugin(
        "my_sql_ingestor", MySQLIngestor,
        version="1.0.0",
        description="PostgreSQL ingestor for internal warehouse",
        capabilities=["ingest"],
    )

    # Load and use
    plugin = registry.load_plugin("my_sql_ingestor", connection_string="postgresql://...")
    result = plugin.execute("SELECT * FROM documents")

    # Reference by name in pipeline YAML: no code changes needed
    ```

    ```yaml
    steps:
      - name: ingest
        plugin: my_sql_ingestor
        config:
          connection_string: "${DB_URL}"
    ```

    **可用扩展点：** 摄取器、解析器、规范化器、抽取器、推理引擎、导出格式、向量库后端、图库后端、可视化渲染器。

  </Accordion>
  <Accordion title="MethodRegistry：添加领域专属的图操作">

    `method_registry` 让你为知识图谱任务（`build`、`analyze`、`centrality`、`resolve` 等）按名字注册一套替代实现；之后凡是跑到该任务的地方，都可以选用这个名字。

    ```python
    from semantica.kg import method_registry
    from semantica.kg.methods import calculate_centrality

    def fast_centrality(graph, **kwargs):
        """Custom centrality implementation."""
        ...

    # register(task, name, func)
    method_registry.register("centrality", "fast_centrality", fast_centrality)

    # The task wrappers consult method_registry, so the name is now selectable:
    scores = calculate_centrality(kg, method="fast_centrality")

    print(method_registry.list_all("centrality"))   # {"centrality": ["fast_centrality", ...]}
    ```

  </Accordion>
</AccordionGroup>

- [快速开始教程](./quickstart.md) — 带代码搭一条完整流水线。
- [模块指南](./modules.md) — 逐模块配示例讲解。
- [API 参考](reference/context.md) — 完整技术参考。
