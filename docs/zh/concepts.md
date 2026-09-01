---
title: 核心概念
description: Semantica 背后的基本理念：知识图谱、推理、溯源与时态智能。
source: concepts.md
source_version: e05564f56af87d57a4db982c7fd121fcdc4bda18
icon: "book-open"
---

<Info>
  第一次接触？先读[入门指南](./getting-started.md)跑通示例，再回来深入理解。
</Info>

Semantica 把非结构化数据——文档、网页、报告、数据库——变成**知识图谱(Knowledge Graph)**：AI 系统可以查询、推理、并回溯到源头的结构化表示。

Semantica 的核心，是在你现有的 AI 技术栈之上加一层**上下文与问责层**。它不替代 LangChain、LlamaIndex 或你的 LLM 提供商——它让它们的输出**有根据**、**可追溯**、**可审计**。

- **上下文层** — 知识图谱、GraphRAG 检索、语义嵌入与时态智能，让 LLM 的每条回答都扎根于结构化、可查询的事实。
- **问责层** — 溯源(Provenance)追踪、决策智能、冲突检测与 W3C PROV-O 合规，让 AI 技术栈里的每条断言都可审计、可解释。
- **扩展层** — `PluginRegistry` 和 `MethodRegistry` 让你替换或增强任意组件——摄取器、抽取器、推理引擎、后端——而无需改动框架代码。

<Warning>
  **这是系统级可解释性，不是基础模型可解释性。**Semantica 不暴露、不重建、不解释 LLM/基础模型*内部*发生了什么——其内部推理或思维链对外部系统始终是不透明的。Semantica 解释的是模型*之外*的部分：输入的上下文和数据、产生的决策、它的溯源、相关的关系、适用的策略，以及完整的执行轨迹。一句话：Semantica 解释和审计的是 *AI 系统做了什么*，而不是基础模型私有的内部推理。
</Warning>

## 知识图谱

<img src="/assets/img/diagrams/kg-structure.svg" alt="知识图谱的节点与边结构：实体（Person、Organization、Location、Date）及其类型化关系" style={{ width: '100%', borderRadius: '12px', margin: '0 0 20px' }} />

Semantica 一切能力的基石。知识图谱用三种积木存储信息：

- **节点（实体）**：人物、公司、地点、事件、概念
- **边（关系）**：`works_for`、`located_in`、`founded_by`
- **属性**：名称、日期、置信度、来源 URL

这种结构让知识**可搜索**、**可关联**、**可查询**，也——最关键的——**可解释**：每个答案都能回溯到产生它的事实和关系。


## 实体抽取（NER）

扫描文本，找出并分类现实世界中的实体：

```python
# Input: "Apple Inc. was founded by Steve Jobs in 1976 in Cupertino."
{
    "entities": [
        {"text": "Apple Inc.",  "type": "ORGANIZATION", "confidence": 0.98},
        {"text": "Steve Jobs",  "type": "PERSON",       "confidence": 0.99},
        {"text": "1976",        "type": "DATE",         "confidence": 0.95},
        {"text": "Cupertino",   "type": "LOCATION",     "confidence": 0.97}
    ]
}
```

每个实体都带类型、置信度和指向源文档的链接。三种抽取方法可选：

| 方法 | 速度 | 准确率 | 要求 |
| :------ | :----- | :-------- | :------------ |
| `"pattern"` | ⚡ 非常快 | 中等 | 无需 API key：基于正则 |
| `"ml"` | 快 | 高 | 本地 ML 模型 |
| `"llm"` | 中等 | 最高 | LLM 提供商：支持全部 9 家 |

## 关系抽取

找出实体之间如何关联：

```python
{
    "relationships": [
        {"subject": "Steve Jobs", "predicate": "founded",    "object": "Apple Inc.", "confidence": 0.92},
        {"subject": "Apple Inc.", "predicate": "located_in", "object": "Cupertino",  "confidence": 0.89}
    ]
}
```

关系可以通过规则、机器学习模型或 LLM 抽取——每种方式都产出带置信度和来源标注的类型化三元组(Triplet)。


## 知识图谱与向量库

两者都为 AI 检索存储信息，但设计目标不同。

<Tabs>
  <Tab title="知识图谱">
    以类型化节点和带标签的边存储**结构化事实**。回答需要理解实体之间关系的问题。

    | 优势 | 为什么重要 |
    | :-------- | :------------- |
    | **图遍历** | 多跳查询："在 Apple 工作过的人后来创办了哪些公司？" |
    | **可解释性** | 每个答案都回溯到具体的节点和边——没有黑盒检索 |
    | **时态推理** | 时间点查询、`valid_from`/`valid_until` 窗口、历史快照 |
    | **冲突检测** | 两个来源对同一事实不一致时会被标出，并可消解 |
    | **模式校验** | SHACL 校验在约束违规污染结果之前就拦住它 |

    **适用场景：**需要结构化推理、溯源、合规或可解释性时。

    ```python
    from semantica.kg import GraphBuilder, PathFinder

    graph   = GraphBuilder(merge_entities=True).build(entities=entities, relationships=rels)
    finder  = PathFinder()
    path    = finder.dijkstra_shortest_path(graph, "Steve Jobs", "Tim Cook")
    ```
  </Tab>

  <Tab title="向量库">
    存储文本分块(Chunking)的**稠密嵌入(Embedding)**。通过寻找语义相近的段落来回答问题——答案结构事先未知时很有用。

    | 优势 | 为什么重要 |
    | :-------- | :------------- |
    | **模糊相似** | 措辞不同也能找到相关内容 |
    | **速度** | 规模化场景下亚毫秒级的近似最近邻搜索 |
    | **非结构化文本** | 直接作用于段落、句子和原始文档 |
    | **简单** | 无需设计模式：嵌入、建索引即可 |

    **适用场景：**需要在大规模文本语料上做快速语义检索时。

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
    | **查询嵌入** | 用户查询被向量化，用于经向量相似度找到锚点节点 |
    | **图遍历** | 从锚点节点出发多跳遍历，取回相关实体和关系 |
    | **上下文组装** | 事实 + 关系被组装起来，每条断言都带来源标注 |
    | **LLM 生成** | LLM 在取回的结构化上下文之上生成回答 |

    **结果：**回答中的每条断言都链回具体的图节点——没有来自训练数据的幻觉，全程可审计。

    ```python
    from semantica.context import AgentContext, ContextGraph
    from semantica.vector_store import VectorStore

    context = AgentContext(
        vector_store=VectorStore(backend="faiss", dimension=768),
        knowledge_graph=ContextGraph(advanced_analytics=True),
    )
    result = context.query("Who founded Apple?", mode="graphrag")
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

**支持的模型：**Sentence-Transformers、FastEmbed、OpenAI、BGE、Ollama 本地嵌入。


## GraphRAG

GraphRAG（图增强检索增强生成(RAG)）让 LLM 的回答扎根于结构化知识图谱，而不只是原始文本块，从而提升回答质量。

<img src="/assets/img/diagrams/graphrag-flow.svg" alt="GraphRAG 流程：用户查询 → 向量检索 + 图遍历 → 上下文构建 → LLM → 有根据的回答" style={{ width: '100%', borderRadius: '12px', margin: '16px 0 20px' }} />

<Steps>
  <Step title="用户提交查询">
    查询被向量化，同时用于种子向量检索和图遍历。
  </Step>
  <Step title="混合上下文检索">
    Semantica 取回相关的图谱上下文——实体、类型化关系、多跳推理路径——连同向量相似的文本块。
  </Step>
  <Step title="上下文构建">
    取回的事实和推理路径被组装成结构化的提示上下文，每条事实都标注源节点和置信度。
  </Step>
  <Step title="LLM 生成有根据的回答">
    LLM 产出的回答中，每条断言都链回图中的源节点——没有无根据的断言，没有来自训练数据的幻觉。
  </Step>
</Steps>

<Tip>
  **GraphRAG 消除了标准 RAG 的幻觉与可追溯性问题。**标准 RAG 检索文本块；GraphRAG 检索带类型化关系的结构化事实。图谱里从来没有的结构，LLM 编不出来。
</Tip>


## 本体(Ontology)

本体定义你的知识的模式与规则：存在哪些实体类型、哪些关系合法、适用什么约束。

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

Semantica 可以从你的知识图谱自动生成本体，或导入现有的 OWL/RDF/Turtle 本体。**本体中心(Ontology Hub)**（v0.5.0）提供可视化编辑器、SHACL Studio、对齐编排和实时健康看板。完整的 6 阶段生成流水线见[本体参考](../reference/ontology.md)。


## 推理与推断

Semantica 内置多种推理引擎(Reasoning Engine)，从已有事实推导新知识。

```text
Known:    Steve Jobs founded Apple Inc.
Known:    Apple Inc. is headquartered in Cupertino
Inferred: Steve Jobs has a connection to Cupertino
```

<Tabs>
  <Tab title="前向链(Forward Chaining)">
    反复套用 IF/THEN 规则，直到推不出新事实。最适合告警系统、合规检查和触发式工作流。

    ```python
    from semantica.reasoning import Reasoner, Rule, Fact, RuleType

    engine = Reasoner()
    engine.add_fact(Fact(subject="Alice", predicate="is_a", obj="Manager"))
    engine.add_rule(Rule(
        rule_type=RuleType.FORWARD_CHAIN,
        conditions=[{"subject": "?x", "predicate": "is_a", "object": "Manager"}],
        conclusion={"subject": "?x", "predicate": "has_authority", "object": "true"}
    ))
    result = engine.infer()
    ```
  </Tab>
  <Tab title="Rete 网络">
    大规则集的高效模式匹配：Rete 算法避免重复求值前置条件未变化的规则。最适合百万级事实上跑数千条规则。

    ```python
    from semantica.reasoning import ReteEngine

    engine = ReteEngine()
    engine.load_rules("rules/domain_rules.json")
    results = engine.run(kg)
    ```
  </Tab>
  <Tab title="演绎与溯因">
    **演绎(Deductive)**：从前提推出必然结论的经典三段论推理。

    **溯因(Abductive)**：为观察到的证据推断最可能的解释。最适合诊断和调查类场景。

    ```python
    from semantica.reasoning import GraphReasoner

    graph_reasoner = GraphReasoner(kg)
    graph_reasoner.add_rule({"if": [{"subject": "?a", "predicate": "parent_of", "object": "?b"}], "then": {"subject": "?a", "predicate": "ancestor_of", "object": "?b"}})
    inferences = graph_reasoner.infer(kg)
    ```
  </Tab>
  <Tab title="Datalog (v0.4.0)">
    带不动点语义的递归 Horn 子句规则：能处理前向链表达不了的传递闭包和递归关系。

    ```python
    from semantica.reasoning import DatalogReasoner, DatalogFact, DatalogRule

    reasoner = DatalogReasoner()
    reasoner.add_fact(DatalogFact("parent", ("alice", "bob")))
    reasoner.add_rule(DatalogRule("ancestor(?X, ?Y) :- parent(?X, ?Y)."))
    reasoner.evaluate()
    results = reasoner.query("ancestor(alice, ?Z)")
    ```
  </Tab>
  <Tab title="引擎对比">

    | 引擎 | 说明 | 最适合 |
    | :------ | :----------- | :-------- |
    | 前向链 | 反复套用规则直到不动点 | 告警系统、合规检查 |
    | Rete 网络 | 高效模式匹配 | 大规则集、高事实吞吐 |
    | 演绎 | 经典三段论推理 | 数理与逻辑推断 |
    | 溯因 | 最可能的解释 | 诊断、调查 |
    | SPARQL | 基于查询的 RDF 推理 | 语义网、本体推理 |
    | Datalog (v0.4.0) | 递归 Horn 子句规则 | 传递闭包、图可达性 |

  </Tab>
</Tabs>

所有引擎都产出**可解释的推理路径**，而不是黑盒结论。每个推导事实都包含产生它的规则和前提。


## 时态智能

知识随时间变化。时态图给节点和边挂上 `valid_from` / `valid_until` 窗口，支持时间点查询和历史分析。

```python
from semantica.kg import TemporalGraphQuery
from datetime import datetime

query_engine = TemporalGraphQuery(enable_temporal_reasoning=True)

# Query the graph as it existed on a specific date
snapshot = query_engine.query_at_time(kg, query="", at_time=datetime(2021, 6, 15))
```

**支持特性：**Allen 区间代数（全部 13 种时态关系）、OWL-Time 导出、`recorded_at` 时间戳、时态溯源。

**常见用途：**追踪公司高管变动、政策演变、研究时间线、金融工具历史、监管合规窗口。


## 距离智能

探索图中任意实体的语义邻域——有助于理解概念上的远近、发现簇、可视化知识拓扑。

```python
from semantica.kg import SimilarityCalculator

calc   = SimilarityCalculator()
scores = calc.calculate_similarity(entity_a, entity_b)
```

**特性：**N×N 语义距离矩阵、ego 模式可视化、距离带分类（`near` / `mid` / `far`）、面向大图谱的嵌入缓存优化。

[可视化模块](../reference/visualization.md)把距离矩阵渲染成交互式热力图和 ego 模式邻域图。[Explorer](../reference/explorer.md) 则把距离智能直接嵌进浏览器看板。


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

    detector = DuplicateDetector(similarity_threshold=0.85)
    duplicates = detector.detect_duplicates(entities)

    merger = EntityMerger()
    deduplicated_entities = merger.merge_duplicates(entities)
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
  这是兼容 W3C PROV-O 的血缘：适合要求审计轨迹的受监管行业（HIPAA、SOX、GDPR、FDA 21 CFR Part 11）。用 `RDFExporter(include_provenance=True)` 可把溯源内嵌进任意 RDF 导出。
</Note>

```python
from semantica.provenance import ProvenanceManager

prov    = ProvenanceManager()
lineage = prov.get_entity_lineage("apple_inc")

print(f"Source:    {lineage.source_document}")
print(f"Method:    {lineage.extraction_method}")
print(f"Extracted: {lineage.timestamp}")
print(f"Checksum:  {lineage.checksum}")
```


## 决策智能

每个智能体(Agent)决策在 Semantica 里都是一等对象：有记录、有因果链接、可按先例检索。这是 AI 流水线的**问责层**：决策不再是转瞬即逝的日志，而是可查询的知识图谱节点。

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
  **每个高风险决策之前，先用 `find_precedents()`。**对全部已记录决策做混合相似度检索，能浮出可能适用的历史推理——减少智能体各次运行之间的不一致，让组织真正从 AI 决策历史中学习。
</Tip>


## 冲突检测

多个来源对同一事实不一致时，Semantica 会标记并消解(Conflict Resolution)冲突，而不是静默挑一个值。

**消解策略：**

- **新近优先**：偏向最新的来源
- **来源可信度**：偏向最可靠的来源（可信度分数可配置）
- **多数表决**：≥ 2 个来源一致时聚合采纳
- **人工复核**：标记待人工仲裁；流水线不阻塞继续

`ConflictResolver`、`SourceTracker` 和 `InvestigationGuideGenerator` 见[冲突参考](../reference/conflicts.md)。


## 自定义插件开发

Semantica 为扩展而设计。任何组件——摄取器、抽取器、图构建器、推理引擎——都可以用运行时注册的自定义实现替换或增强。

<AccordionGroup>
  <Accordion title="PluginRegistry：按名字替换任意组件">

    `PluginRegistry` 提供跨所有模块的动态插件发现、注册和加载。把你的类注册到一个字符串键下；凡是在配置或流水线步骤里引用该键的地方，Semantica 都会使用它。

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

    **可用扩展点：**摄取器、解析器、规范化器、抽取器、推理引擎、导出格式、向量库后端、图库后端、可视化渲染器。

  </Accordion>
  <Accordion title="MethodRegistry：添加领域专属的图操作">

    `MethodRegistry` 让你按名字把自定义方法注册到知识图谱对象上——无需子类化就能添加领域专属的图操作。

    ```python
    from semantica.kg import MethodRegistry

    registry = MethodRegistry()

    def find_supply_chain_hops(graph, source_node, max_hops=3):
        """Custom BFS traversal for supply chain graphs."""
        ...

    # Register under a string key
    registry.register("supply_chain_hops", find_supply_chain_hops)

    # Call by name on any graph object
    result = registry.call("supply_chain_hops", kg, source_node="Supplier_A", max_hops=5)

    # List all registered methods
    print(registry.list_methods())   # ["supply_chain_hops", ...]
    ```

  </Accordion>
</AccordionGroup>

- [快速开始教程](./quickstart.md) — 带代码搭一条完整流水线。
- [模块指南](./modules.md) — 逐模块配示例讲解。
- [API 参考](../reference/context.md) — 完整技术参考。
