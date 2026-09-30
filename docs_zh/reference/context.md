---
title: "上下文模块（Context）"
description: "智能体上下文图、决策跟踪、因果链、先例搜索、政策执行与多跳 GraphRAG。"
source: reference/context.md
source_version: 164a4128875aa1b01ca0dfccadbbff8a07627658
icon: "brain"
---

`semantica.context` 是 AI 智能体的记忆与决策层：

- 存储事实，带溯源(Provenance)和基于嵌入(Embedding)的检索
- 把决策记录为一等图对象，保留完整因果链
- 让智能体检索自己的历史，跨运行保持一致
- 经多跳 GraphRAG 遍历回答复杂查询
- 执行带版本的政策并跟踪合规例外


## 导出的类

| 类 | 职责 |
| :--- | :--- |
| `AgentContext` | 主入口：记忆、检索、决策、图遍历、检查点 |
| `ContextGraph` | 内存知识图谱(Knowledge Graph)：中心性、社区发现和决策跟踪 |
| `AgentMemory` | 向量驱动的持久记忆：`store(text)`、`retrieve(query, max_results)` |
| `EntityLinker` | 把实体提及链接到 URI；在实体 ID 之间创建类型化边 |
| `ContextRetriever` | 混合向量 + 图检索，支持最低分数和图扩展选项 |
| `DecisionRecorder` | 记录决策，带嵌入、因果链和元数据 |
| `PolicyEngine` | 政策管理：`add_policy()`、`check_compliance()`、`get_applicable_policies()` |
| `CausalChainAnalyzer` | 追溯决策之间的相互影响：`get_causal_chain(decision_id)` |
| `ErasureCoordinator` | 跨图、记忆和向量库擦除一个实体，返回可审计的 `ErasureReceipt` |


## 你能得到什么

- **AgentContext** — 记忆、决策跟踪和图检索收进一个 API
  - 对话历史与检查点差异对比
  - 完整上下文状态持久化到磁盘并恢复
- **ContextGraph** — 线程安全的内存知识图谱
  - PageRank、中心性、社区发现、时态有效性
  - 跨图导航和链接遍历
- **AgentMemory** — 带保留策略的嵌入记忆
  - 可配置 `max_memory_size` 的 LRU 淘汰
  - 按对话隔离历史
- **DecisionRecorder** — 记录决策，带因果链和置信度得分
  - 时态有效窗口（`valid_from` / `valid_until`）
  - 每条决策都捕获跨系统上下文
- **PolicyEngine** — 存放在知识图谱里的带版本政策
  - 对已记录决策做合规检查
  - 政策例外跟踪，带审批人审计轨迹
- **EntityLinker** — 把实体文本映射到稳定 URI
  - 在实体 ID 之间创建类型化链接
  - 避免 "Apple"、"Apple Inc."、"AAPL" 变成三个节点
- **ContextRetriever** — 融合向量相似度、图遍历和智能体记忆
  - 比纯向量搜索的上下文更丰富
  - `hybrid_alpha` 和扩展跳数可配置
- **CausalChainAnalyzer** — 追溯任意决策的上游原因和下游影响
  - 带关系类型的可解释路径
  - 深度和方向可配置


## 快速开始

<Steps>
  <Step title="初始化智能体上下文">
    ```python
    from semantica.context import AgentContext, ContextGraph
    from semantica.vector_store import VectorStore

    context = AgentContext(
        vector_store=VectorStore(backend="faiss", dimension=768),
        knowledge_graph=ContextGraph(advanced_analytics=True),
        decision_tracking=True,
        retention_days=90,
        max_memories=50000,
    )
    ```
  </Step>
  <Step title="存储事实并按语义相似度检索">
    ```python
    memory_id = context.store(
        "GPT-4 outperforms GPT-3.5 on reasoning benchmarks by 40%",
        metadata={"source": "openai_blog", "date": "2024-01"}
    )

    results = context.retrieve("LLM benchmark comparisons", max_results=5)
    for r in results:
        print("{} (score: {:.3f})".format(r["content"], r["score"]))
    ```
  </Step>
  <Step title="带完整溯源记录决策">
    ```python
    decision_id = context.record_decision(
        category="model_selection",
        scenario="Choose LLM for production reasoning pipeline",
        reasoning="GPT-4 benchmark advantage justifies 3x cost increase",
        outcome="selected_gpt4",
        confidence=0.91,
        entities=["gpt-4", "gpt-3.5"],
        decision_maker="pipeline_agent",
    )
    ```
  </Step>
  <Step title="查找先例并追溯因果链">
    ```python
    # Search past decisions: prevents contradictory choices across runs
    precedents = context.find_precedents("model selection reasoning", limit=5)
    for p in precedents:
        print("[{}] {}  (confidence: {:.2f})".format(p.category, p.outcome, p.confidence))
        print("  Reasoning: {}".format(p.reasoning))

    # Trace downstream decisions influenced by this one
    chain = context.get_causal_chain(decision_id, direction="downstream", max_depth=5)
    print("Downstream decisions: {}".format(len(chain)))

    # Full explainability
    explanation = context.trace_decision_explainability(decision_id)
    print("Total connections: {}".format(explanation["total_connections"]))
    ```
  </Step>
</Steps>


## 使用模式

<Tabs>
  <Tab title="纯向量记忆">
    最快搭建：不需要知识图谱。适合这类智能体：只需要对事实做语义搜索，不想承担图遍历的开销。

    ```python
    from semantica.context import AgentContext
    from semantica.vector_store import VectorStore

    # Zero-graph setup: vector memory only
    context = AgentContext(
        vector_store=VectorStore(backend="faiss", dimension=768),
    )

    context.store("User prefers concise responses with code examples")
    context.store("Project uses Python 3.11 with FastAPI and PostgreSQL")

    results = context.retrieve("user coding preferences", max_results=5)
    for r in results:
        print("{:.3f}  {}".format(r["score"], r["content"]))
    ```

    <Check>
      本地零依赖开发把 `backend="faiss"` 换成 `backend="inmemory"` 即可。
    </Check>
  </Tab>
  <Tab title="完整智能体上下文">
    生产配置：图 + 决策 + 分析。需要可解释性和无矛盾决策历史时用它。

    ```python
    from semantica.context import AgentContext, ContextGraph
    from semantica.vector_store import VectorStore

    context = AgentContext(
        vector_store=VectorStore(backend="faiss", dimension=768),
        knowledge_graph=ContextGraph(
            advanced_analytics=True,  # PageRank, centrality, community detection
            kg_algorithms=True,       # path-finding, link prediction
        ),
        decision_tracking=True,       # requires knowledge_graph
        retention_days=90,
        max_memories=50000,
    )

    decision_id = context.record_decision(
        category="model_selection",
        scenario="Choose LLM for production reasoning pipeline",
        reasoning="GPT-4 benchmark advantage justifies 3x cost",
        outcome="selected_gpt4",
        confidence=0.91,
        entities=["gpt-4", "gpt-3.5"],
    )

    # Prevent contradictions across runs
    precedents = context.find_precedents("model selection", limit=5)
    ```

  </Tab>
  <Tab title="GraphRAG 查询">
    加载预构建的知识图谱，用多跳图遍历回答复杂问题。

    ```python
    from semantica.context import AgentContext, ContextGraph
    from semantica.vector_store import VectorStore

    context = AgentContext(
        vector_store=VectorStore(backend="faiss", dimension=768),
        knowledge_graph=ContextGraph(advanced_analytics=True),
        hybrid_alpha=0.4,        # 0.0 = pure vector  →  1.0 = pure graph
        max_expansion_hops=3,
    )

    # Load a pre-built knowledge graph
    context.load_graph("company_kg.json")

    # Multi-hop GraphRAG retrieval
    results = context.retrieve(
        "companies founded by Apple alumni",
        use_graph=True,
        max_results=10,
    )
    for r in results:
        print("[{:.3f}] {}".format(r["score"], r["content"]))
    ```

    <Tip>
      调大 `max_expansion_hops` 可以遍历得更深，代价是延迟。建议从 2 起步往上调。
    </Tip>
  </Tab>
  <Tab title="政策执行">
    添加带版本的合规政策，每条决策在记录前都要先过一遍。

    ```python
    from datetime import datetime

    from semantica.context import AgentContext, ContextGraph, PolicyEngine
    from semantica.context.decision_models import Decision, Policy
    from semantica.vector_store import VectorStore

    context = AgentContext(
        vector_store=VectorStore(backend="faiss", dimension=768),
        knowledge_graph=ContextGraph(),
        decision_tracking=True,
    )

    engine = PolicyEngine(graph_store=context.knowledge_graph)

    engine.add_policy(Policy(
        policy_id="data_privacy",
        name="Data Privacy",
        description="No PII stored without user consent flag",
        rules={"required_user_consent": True, "max_retention_days": 90},
        category="privacy",
        version="1.2",
        created_at=datetime(2024, 1, 1),
        updated_at=datetime(2024, 1, 1),
    ))

    decision = Decision(
        decision_id="dec_store_email",
        category="data_storage",
        scenario="Store user profile",
        reasoning="User opted in to profile storage",
        outcome="stored",
        confidence=1.0,
        timestamp=datetime.now(),
        decision_maker="profile_agent",
        metadata={"user_consent": True, "retention_days": 30},
    )

    if engine.check_compliance(decision, "data_privacy"):
        context.record_decision(
            category=decision.category,
            scenario=decision.scenario,
            reasoning=decision.reasoning,
            outcome=decision.outcome,
            confidence=decision.confidence,
        )
    else:
        print("Blocked by policy: data_privacy")
    ```
  </Tab>
</Tabs>


## AgentContext

**`AgentContext`** 是主入口。它把记忆、图和决策跟踪包在**单一统一 API** 后面。

### 构造参数

| 参数 | 类型 | 默认值 | 说明 |
| :--------- | :---- | :------- | :----------- |
| `vector_store` | `VectorStore` | **必填** | 基于嵌入的记忆检索后端 |
| `knowledge_graph` | `ContextGraph` | `None` | 启用图关系和 GraphRAG |
| `decision_tracking` | `bool` | `False` | 激活 `DecisionRecorder`：要求同时设置 `knowledge_graph` |
| `retention_days` | `Optional[int]` | `30` | 自动过期超过 N 天的记忆；`None` = 永久保留 |
| `max_memories` | `int` | `10000` | LRU 淘汰前的硬上限 |
| `graph_expansion` | `bool` | `True` | 从存储的记忆自动扩展图 |
| `max_expansion_hops` | `int` | `2` | 检索时图扩展的最大跳数 |
| `hybrid_alpha` | `float` | `0.5` | 向量（`0.0`）与图（`1.0`）检索之间的平衡 |
| `advanced_analytics` | `bool` | `True` | 启用 PageRank、中心性和社区分析 |
| `kg_algorithms` | `bool` | `True` | 增加路径查找和链接预测 |

<Tip>
  **设 `retention_days` 防止记忆膨胀。** 默认 `30` 会自动修剪。合规攸关的智能体可能需要设 `retention_days=None`，再用 `export()` 显式归档。
</Tip>

<Tip>
  **跨运行持久化你的上下文。**`VectorStore` 不会自动持久化——给它的构造函数传 `index_path=` 是无效操作。调 `context.save("agent_state/")` 把记忆、向量索引和图写到磁盘；下一个进程再用 `context.load("agent_state/")` 恢复。见下文[实战模式](#real-world-patterns)的"持久化与恢复"标签页。
</Tip>

### 记忆方法

| 方法 | 返回 | 说明 |
| :------ | :------- | :----------- |
| `store(content, metadata, conversation_id, user_id)` | `str` 或 `Dict` | 存一条事实（str → 记忆 ID）或一批文档（list → 统计 dict） |
| `batch_store(items)` | `List[str]` | 一次存多项：返回记忆 ID 列表 |
| `retrieve(query, max_results, min_score, use_graph, conversation_id)` | `List[Dict]` | 语义检索；设置了 `knowledge_graph` 时自动选择 GraphRAG |
| `forget(memory_id, conversation_id, days_old)` | `int` | 按 ID、对话或年龄删除记忆 |
| `update(memory_id, content, metadata)` | `bool` | 更新已存记忆的内容或元数据 |
| `get_memory(memory_id)` | `Optional[Dict]` | 按 ID 取一条具体记忆 |
| `stats()` | `Dict` | 记忆计数、向量存储状态、图统计 |
| `health()` | `Dict` | 系统健康：全部后端、状态标志 |
| `save(path)` | `None` | 把完整上下文状态（记忆 + 图）持久化到磁盘 |
| `load(path)` | `None` | 从磁盘恢复上下文状态 |
| `export(conversation_id, format)` | `str \| Dict` | 把记忆导出为 JSON 或 dict |
| `import_data(data, format)` | `int` | 从 JSON 或 dict 导入记忆 |

<Tip>
  **`retrieve()` 用的是 `max_results=`，不是 `top_k=`。** 参数名是 `max_results`（默认 `5`）。传 `use_graph=True` 强制走 GraphRAG，传 `use_graph=False` 强制纯向量检索——无论有没有配置 `knowledge_graph`。
</Tip>

### 对话方法

```python
# Store turns in a conversation thread
context.store("User asked about deployment options", conversation_id="conv_001")
context.store("Agent recommended Docker + Kubernetes", conversation_id="conv_001")

# Retrieve full conversation history
history = context.conversation("conv_001", max_items=50)
for turn in history:
    print("[{}] {}".format(turn["timestamp"], turn["content"]))

# Retrieve across all conversations with a query
results = context.retrieve(
    "deployment recommendations",
    conversation_id="conv_001",
    max_results=10,
)
```

### 多跳 GraphRAG

**要求构造时设置 `knowledge_graph`**：有了它才能启用 `query_with_reasoning()`，做大语言模型(LLM)支撑的多跳遍历：

```python
import os
from semantica.llms import Groq

llm    = Groq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))
result = context.query_with_reasoning(
    query="What technologies have we chosen and why?",
    llm_provider=llm,
    max_hops=2,
    max_results=10,
)

print(result["response"])
print("Confidence: {:.2f}".format(result["confidence"]))
print("Sources used: {}".format(result["num_sources"]))
```

### 决策方法

| 方法 | 返回 | 说明 |
| :------ | :------- | :----------- |
| `record_decision(category, scenario, reasoning, outcome, confidence, entities, decision_maker, valid_from, valid_until)` | `str` | 记录一条决策；`decision_tracking=False` 或没有 `knowledge_graph` 时抛 `RuntimeError` |
| `find_precedents(scenario, category, limit, use_hybrid_search, max_hops, as_of)` | `List[Decision]` | 按语义 + 结构相似度找相似的历史决策 |
| `query_decisions(query, max_hops, use_hybrid_search)` | `List[Decision]` | 宽泛的上下文感知决策搜索 |
| `get_causal_chain(decision_id, direction, max_depth)` | `List[Decision]` | 追溯 `"upstream"` 原因或 `"downstream"` 影响 |
| `trace_decision_explainability(decision_id)` | `Dict` | 完整可解释性：原因、影响、关系路径 |
| `get_policy_engine()` | `PolicyEngine` | 访问活动的 `PolicyEngine` 实例 |

<Warning>
  `decision_tracking=True` 要求同时设置 `knowledge_graph`。否则 `record_decision()` 抛 `RuntimeError`。
</Warning>

<Tip>
  **每个重要决策之前都用 `find_precedents()`。** 上下文模块就是这样防止智能体跨运行做出矛盾选择的。具体做法是把先例作为上下文呈现给 LLM："基于类似理由，我们之前选过 X。"
</Tip>

### 检查点方法

**审计推理循环的理想工具**：在一轮推理前后各拍一个快照，看清到底改了什么：

```python
# Take a named snapshot of the current graph state
context.checkpoint("before_inference")

# ... run reasoning, record decisions ...

context.checkpoint("after_inference")

# See exactly what was added/removed
diff = context.diff_checkpoints("before_inference", "after_inference")
print("Decisions added: {}".format(len(diff["decisions_added"])))
print("Relationships added: {}".format(len(diff["relationships_added"])))

# Persist a checkpoint to disk via TemporalVersionManager
context.flush_checkpoint("after_inference")
```


## ContextGraph

**`ContextGraph`** 是 `AgentContext` 背后的知识图谱。一句话点破：它就是智能体的"脑内地图"——实体是节点，关系是边，决策也作为节点挂在这张网上。它也可以**独立使用**：只做关系建模，不必引入整个上下文层。

```python
from semantica.context import ContextGraph

graph = ContextGraph(advanced_analytics=True)

# Build the graph
graph.add_node("Python",  "language",  properties={"paradigm": "multi-paradigm"})
graph.add_node("FastAPI", "framework", properties={"language": "Python"})
graph.add_edge("Python", "FastAPI", "enables")

# Record and query decisions directly on the graph
decision_id = graph.record_decision(
    category="technology_choice",
    scenario="Web API framework selection",
    reasoning="FastAPI's async support and auto-docs match our requirements",
    outcome="selected_fastapi",
    confidence=0.92,
    entities=["Python", "FastAPI"],
)

similar = graph.find_precedents_by_scenario("web framework", limit=3)
stats   = graph.stats()
print("Nodes: {}, Edges: {}".format(stats["node_count"], stats["edge_count"]))
```

### 构造选项

| 参数 | 类型 | 默认值 | 说明 |
| :--------- | :---- | :------- | :----------- |
| `advanced_analytics` | `bool` | `True` | PageRank、介数中心性 |
| `centrality_analysis` | `bool` | `True` | 完整中心性套件 |
| `community_detection` | `bool` | `True` | Louvain 社区聚类 |
| `node_embeddings` | `bool` | `True` | Node2Vec 嵌入，用于结构相似度 |

### ContextGraph：完整方法参考

| 方法 | 返回 | 说明 |
| :------ | :------- | :----------- |
| `add_node(node_id, node_type, properties, valid_from, valid_until)` | `None` | 添加节点；支持时态有效窗口 |
| `add_edge(source_id, target_id, edge_type, weight, properties)` | `None` | 添加有向边，可带权重 |
| `add_nodes(nodes)` | `int` | 从 dict 列表批量添加；返回添加数 |
| `add_edges(edges)` | `int` | 批量添加边；返回添加数 |
| `get_neighbors(node_id, hops)` | `List[Dict]` | 给定深度内的 BFS 邻居 |
| `get_neighbor_distances(node_id, hops)` | `List[Dict]` | 带置信度衰减得分的邻居 |
| `find_node(node_id)` | `Optional[Dict]` | 按 ID 查单个节点 |
| `find_nodes(node_type, skip, limit)` | `List[Dict]` | 按类型过滤节点，带分页 |
| `find_active_nodes(node_type, at_time)` | `List[Dict]` | 在给定时间戳有效的节点 |
| `find_edges(edge_type, skip, limit)` | `List[Dict]` | 按类型过滤边，带分页 |
| `record_decision(category, scenario, reasoning, outcome, confidence, entities, decision_maker)` | `str` | 添加决策节点，带因果边 |
| `find_precedents_by_scenario(scenario, category, limit, use_semantic_search, as_of)` | `List[Dict]` | 语义相似的历史场景 |
| `query(query, skip, limit)` | `List[Dict]` | 节点内容全文搜索 |
| `stats()` | `Dict` | 节点/边计数、类型分布、图密度 |
| `density()` | `float` | 图密度得分 |
| `save_to_file(path, format="json")` | `None` | 把图持久化为 JSON 或 Markdown 目录 |
| `load_from_file(path, format="json")` | `None` | 从 JSON 或 Markdown 目录替换图状态 |
| `build_from_conversations(conversations, link_entities)` | `Dict` | 从对话数据构建图 |
| `link_graph(other_graph, source_node_id, target_node_id, link_type)` | `str` | 创建跨图导航链接；返回 `link_id` |
| `navigate_to(link_id)` | `Tuple` | 沿跨图链接到达 `(target_graph, target_node_id)` |
| `cross_graph_path(source_node_id, target_graph, target_node_id, max_hops)` | `Dict` | 跨链接图的最短路径 |
| `clear()` | `None` | 重置图状态和全部索引 |

### 距离智能（v0.5.0）

`ContextGraph` 提供完整的距离智能 API，用于探索语义邻域并把邻近度混入检索。

<Info>
  完整的距离智能参考——距离矩阵、API 端点、嵌入缓存、Explorer 界面——见专门的[距离智能](./distance.md)页面。本节只记录上下文层的 API。
</Info>

### 带距离元数据的邻居

给 `get_neighbors()` 传 `include_distance_metadata=True`，每个邻居都会附带距离带、置信度衰减和路径信息：

```python
graph = ContextGraph(advanced_analytics=True)

# ... populate graph ...

neighbors = graph.get_neighbors(
    "python",
    hops=3,
    include_distance_metadata=True,
    min_weight=0.3,   # exclude low-confidence edges
)

for n in neighbors:
    print(
        f"{n['node_id']:15s}  "
        f"band={n['distance_band']:10s}  "
        f"decay={n['confidence_decay']:.3f}  "
        f"hops={n['hop_count']}"
    )
```

| 新增字段 | 类型 | 说明 |
| :---------- | :---- | :----------- |
| `distance_band` | `str` | `"direct"`（1 跳）/ `"near"`（2）/ `"mid-range"`（3–4）/ `"distant"`（5+） |
| `confidence_decay` | `float` | `edge_weight ^ hop_count`——每跳衰减一次 |
| `path_to_anchor` | `List[str]` | 从锚节点到该邻居的最短路径 |
| `hop_count` | `int` | 距锚点的 BFS 深度 |

### 邻近度混合检索

在 `AgentContext` 上设 `proximity_weight`，把图邻近度混进每次 `retrieve()` 和 `find_precedents()` 调用：

```python
context = AgentContext(
    vector_store=VectorStore(backend="faiss", dimension=768),
    knowledge_graph=ContextGraph(advanced_analytics=True),
    proximity_weight=0.3,   # 0.7×semantic + 0.3×proximity
)

# combined_score is returned alongside semantic_score and proximity_score
results = context.retrieve("web API frameworks", max_results=10)
for r in results:
    print(
        f"[{r['combined_score']:.3f}]  "
        f"semantic={r['semantic_score']:.3f}  "
        f"proximity={r['proximity_score']:.3f}  "
        f"{r['content'][:60]}"
    )

# Override weight per-call
precedents = context.find_precedents(
    "infrastructure scaling decisions",
    proximity_weight=0.5,
    limit=5,
)
```

<Tip>
  `proximity_weight=0.0` 完全关闭邻近度混合（纯语义）。`proximity_weight=1.0` 纯按到查询锚点的图邻近度排序。多数生产场景 `0.2`–`0.4` 效果不错。
</Tip>


## 跨图导航

把多个独立的 `ContextGraph` 实例链接起来，智能体就能跨问题空间遍历：

```python
domain_graph    = ContextGraph()
decision_graph  = ContextGraph()

domain_graph.add_node("microservices", "architecture", properties={"style": "distributed"})
decision_graph.add_node("deploy_k8s",  "decision",     properties={"outcome": "approved"})

link_id = domain_graph.link_graph(
    other_graph=decision_graph,
    source_node_id="microservices",
    target_node_id="deploy_k8s",
    link_type="INFORMED_BY",
)

# Follow the link at traversal time
target_graph, entry_node = domain_graph.navigate_to(link_id)

# Cross-graph pathfinding
path = domain_graph.cross_graph_path(
    source_node_id="microservices",
    target_graph=decision_graph,
    target_node_id="deploy_k8s",
    max_hops=5,
)
print("Reachable: {}, hops: {}".format(path["reachable"], path["hop_count"]))
```


## AgentMemory

需要对记忆存储和检索做细粒度控制时：

```python
from semantica.context import AgentMemory
from semantica.vector_store import VectorStore

memory = AgentMemory(
    vector_store=VectorStore(backend="faiss", dimension=768),
    max_memory_size=10000,
    retention_policy="90_days",   # or "unlimited"
)

memory_id = memory.store(
    "Critical compliance rule: all trades must be pre-approved",
    metadata={"type": "compliance"},
)

results = memory.retrieve(
    query="trade approval requirements",
    max_results=5,
    min_score=0.0,
)

memory.delete_memory(memory_id)
memory.clear_memory(conversation_id="conv_001")

history = memory.get_conversation_history(conversation_id="conv_001", max_items=100)
```

| 参数 | 类型 | 默认值 | 说明 |
| :--------- | :---- | :------- | :----------- |
| `vector_store` | `VectorStore` | **必填** | 语义检索的嵌入后端 |
| `max_memory_size` | `int` | `10000` | LRU 淘汰前的最大条目数 |
| `retention_policy` | `str` | `"unlimited"` | `"N_days"`（如 `"30_days"`）或 `"unlimited"` |

### Markdown 往返

`AgentMemory` 可以导出人类可编辑的 Markdown，并把编辑后的文件再导入回来。
每个文件对应一条记忆：必需元数据放在 YAML frontmatter，记忆内容放在 Markdown 正文：

```markdown
---
id: mem_compliance_rule
created_at: '2026-07-22T09:00:00+00:00'
updated_at: '2026-07-22T10:30:00+00:00'
type: compliance
tags:
- trading
- approval
---

All trades must be pre-approved.
```

```python
from pathlib import Path

# A single selected memory can be returned as Markdown text.
document = memory.export(format="markdown", type="compliance")

# Export a memory set as one stable Markdown file per item.
memory.export(format="markdown", destination="memory_export/")

# New IDs create memories; existing IDs are updated in place.
count = memory.import_data(Path("memory_export/"), format="markdown")
```

必需的 frontmatter 字段是 `id`、`created_at`、`updated_at`，以及 `type` 或 `kind` 二选一；可选元数据可在顶层编辑。导入会在改动记忆之前拒绝格式错误或重复的字段；重新导入未变化的文件则是幂等的，多导一次结果不变。记忆本地的 `entities` 和 `relationships` 会作为溯源保留，但 Markdown 导入不会把它们应用到 `ContextGraph`。请使用专用的导出目录：导入会覆盖同名文件，但不会自动删除无关或过期的 Markdown 文件。导出拒绝覆盖文件系统链接，改用原子文件替换；导入同样拒绝符号链接、Windows 目录联接和其他 Windows 重解析点。
时间戳偏移量在 Markdown 里原样保留，只在比较时归一化为 UTC，因此带时区和不带时区的记录可以安全地一起查询。向量存储的写入会推迟到内存导入提交之后才执行；适配器同步是尽力而为，失败会记入日志。


## ErasureCoordinator

`ContextGraph.purge_node()` 的作用范围只有一张图：它移除节点、写入一条墓碑标记(tombstone)，但同样的内容可能仍以 `AgentMemory` 条目和向量库嵌入的形式存活。`ErasureCoordinator` 驱动跨所有已绑定存储的级联擦除，并返回一份擦除回执(`ErasureReceipt`)，逐项记录每个存储的报告结果。

```python
from semantica.context import AgentMemory, ContextGraph, ErasureCoordinator

coordinator = ErasureCoordinator(graph=graph, memory=memory)

receipt = coordinator.erase_entity(
    "customer-4471",
    reason="GDPR Art. 17 request #882",
)

if not receipt.complete:
    # These stores may still hold the entity; handle them out of band.
    print(receipt.incomplete_stores)
```

<Warning>
务必检查回执——调用返回并不代表数据已经删除。FAISS、Milvus 和 Weaviate 没有提供删除方法，因此这些后端目前无法完成擦除；回执会如实报告 `unsupported`，而不会谎报一次并未取得的成功。
</Warning>

### 构造参数

| 参数 | 类型 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- |
| `graph` | `ContextGraph` | `None` | 任何暴露 `purge_node()` 的对象 |
| `memory` | `AgentMemory` | `None` | 任何暴露 `find_by_entity()` 和 `batch_delete()` 的对象 |
| `vector_store` | `VectorStore` | `memory.vector_store` | 持有按实体索引的嵌入的存储；传 `False` 可禁用该环节 |

至少要绑定一个存储；未提供的存储会报告 `not_configured`，而不是静默跳过。

### 方法

| 方法 | 返回 | 说明 |
| :--- | :--- | :--- |
| `erase_entity(entity_id, reason, at, vector_ids)` | `ErasureReceipt` | 从所有已绑定存储中擦除一个实体 |
| `erase_entities(entity_ids, reason, at)` | `List[ErasureReceipt]` | 每个实体一份回执，按序返回；单个失败不会中断其余擦除 |

### 存储状态

| 状态 | 含义 |
| :--- | :--- |
| `erased` | 已触达，数据已移除。在向量环节，它表示存储接受了针对给定 ID 的删除——各后端没有可移植的存在性检查，因此它并不代表那里实际存在过多少嵌入 |
| `not_found` | 已触达，但没有该实体的数据 |
| `not_configured` | 未绑定该存储——属正常情况，不算失败 |
| `unsupported` | 该存储完全不支持删除；重试也不会有结果 |
| `failed` | 已触达存储，但删除没有成功 |

### ErasureReceipt

| 成员 | 类型 | 说明 |
| :--- | :--- | :--- |
| `entity_id` | `str` | 请求擦除的实体 |
| `reason` | `Optional[str]` | 记录在回执和图墓碑标记中 |
| `erased_at` | `str` | ISO-8601 格式；与墓碑标记的 `purged_at` 一致 |
| `stores` | `Dict[str, Dict]` | 各存储的结果，键为 `vectors`、`memory`、`graph` |
| `complete` | `bool` | 任一存储报告 `unsupported` 或 `failed` 时为 `False` |
| `incomplete_stores` | `List[str]` | 可能仍持有该实体数据的存储 |
| `to_dict()` | `Dict` | 序列化后的回执，可安全持久化为审计记录 |

```python
receipt.to_dict()
# {
#   "entity_id": "customer-4471",
#   "reason": "GDPR Art. 17 request #882",
#   "erased_at": "2026-08-16T09:03:36.813220",
#   "complete": False,
#   "stores": {
#     "vectors": {"status": "unsupported", "backend": "faiss",
#                 "detail": "backend exposes no delete()/delete_vectors(); ..."},
#     "memory":  {"status": "erased", "items": 14},
#     "graph":   {"status": "erased", "nodes": 1, "edges": 3},
#   },
# }
```

擦除按由外向内的顺序执行——先向量、再记忆、最后是图。墓碑标记是"擦除确实发生过"的持久凭证，因此放在最后写入：级联中途崩溃，留下的会是尚存的节点和一份不完整的回执，而不是一条言过其实的墓碑标记。某个存储抛出异常时，回执会把它记录为 `failed`，其余存储仍会照常擦除。对同一实体重复擦除，返回的回执会说明已无可删除的内容，而不会抛出异常。


## PolicyEngine

`PolicyEngine` 管理存放在知识图谱中的带版本政策。政策以节点形式存放，可以链接到决策：

```python
from semantica.context import PolicyEngine
from semantica.context import ContextGraph
from semantica.context.decision_models import Policy, Decision
from datetime import datetime

graph  = ContextGraph()
policy = PolicyEngine(graph_store=graph)

# Create and store a policy
p = Policy(
    policy_id="policy_001",
    name="Confidence Threshold Policy",
    description="All decisions must have confidence >= 0.7",
    rules={"min_confidence": 0.7, "requires_reasoning": True},
    category="decision_quality",
    version="1.0",
    created_at=datetime.now(),
    updated_at=datetime.now(),
)
policy.add_policy(p)

# Check compliance of a specific decision
decision = Decision(
    decision_id="dec_001",
    category="loan_approval",
    scenario="First-time homebuyer",
    reasoning="Good credit score and stable employment",
    outcome="approved",
    confidence=0.94,
    timestamp=datetime.now(),
    decision_maker="loan_agent",
)
compliant = policy.check_compliance(decision, "policy_001")
print("Compliant:", compliant)

# Get applicable policies for a category
policies = policy.get_applicable_policies(category="decision_quality")
for p in policies:
    print("{} v{}".format(p.name, p.version))
```


## EntityLinker

把实体文本映射到 URI，并在实体 ID 之间创建类型化链接：

```python
from semantica.context import EntityLinker

linker = EntityLinker(similarity_threshold=0.8)

# Assign a URI to an entity
uri = linker.assign_uri("apple_inc", "Apple Inc.", "ORGANIZATION")
print(uri)  # "https://semantica.dev/entity/apple_inc.#organization"

# Link entities from extracted text
entities = [
    {"id": "e1", "text": "Apple Inc.", "type": "ORGANIZATION"},
    {"id": "e2", "text": "Apple",      "type": "ORGANIZATION"},
]
linked = linker.link(text="Apple Inc. was founded by Steve Jobs.", entities=entities)
for e in linked:
    print("{} → {}  (confidence: {:.2f})".format(e.text, e.uri, e.confidence))

# Explicitly link two entity IDs (not a list: takes two IDs)
linker.link_entities(
    entity1_id="apple_inc",
    entity2_id="aapl",
    link_type="same_as",
    confidence=0.99,
)

# Build the full entity web
web = linker.build_entity_web()
print("Entities:", web["statistics"]["total_entities"])
print("Links:   ", web["statistics"]["total_links"])
```

<Warning>
  **`EntityLinker.link_entities()` 链接的是两个实体 ID，不是列表。** 调 `link_entities(entity1_id, entity2_id, link_type)` 在两个已知 ID 之间创建类型化边。要链接从文本抽取的实体，改用 `link(text, entities=[...])`。
</Warning>

`link()` 返回的 `LinkedEntity` 字段：

| 字段 | 类型 | 说明 |
| :----- | :---- | :----------- |
| `entity_id` | `str` | 实体标识符 |
| `uri` | `str` | 生成的 URI（如 `"https://semantica.dev/entity/apple_inc."`） |
| `text` | `str` | 表层文本 |
| `type` | `str` | 实体类型 |
| `linked_entities` | `List[EntityLink]` | 相关实体链接，含 `source_entity_id`、`target_entity_id`、`link_type`、`confidence` |
| `context` | `Dict` | 实体元数据 |
| `confidence` | `float` | 总体置信度得分 |


## ContextRetriever

混合检索：向量相似度 + 图遍历 + 记忆：

```python
from semantica.context import ContextRetriever

retriever = ContextRetriever(
    memory_store=memory,
    knowledge_graph=context_graph,
    vector_store=vector_store,
    use_graph_expansion=True,
    max_expansion_hops=2,
    hybrid_alpha=0.5,
)

results = retriever.retrieve(
    query="What decisions were made about cloud infrastructure?",
    max_results=10,
    use_graph_expansion=True,
    min_relevance_score=0.3,
)

for r in results:
    print("[{}] score={:.3f}: {}".format(r.source, r.score, r.content[:80]))
```


## 支持感知检索（`truth_filter`）

缓存中的向量或记忆内容，可能比当初支撑它的证据活得更久。一句话点破：记录照常留在库里，但检索只放行证据仍然站得住的结果。具体来说，`ContextRetriever.retrieve(..., truth_filter=...)` 接受一个按需启用的 `TruthMaintenanceContextFilter`，它在**排序之前**就做一次筛查，把声明的依赖已失去支持的候选结果剔除掉；存储中的记录本身绝不会被改动。

下面的示例可独立运行：不需要模型、数据库或网络，只依赖 `semantica` 本身：

```python
from semantica.context import ContextRetriever, TruthMaintenanceContextFilter
from semantica.reasoning import FactSupport, Rule, TruthMaintenanceSession

# A tiny read-only store standing in for any real vector backend.
class StaticVectorStore:
    def __init__(self, rows):
        self.rows = [dict(row) for row in rows]

    def search(self, *, query, limit):
        return self.rows[:limit]

def annotated_row(identifier, fact, score, text):
    """One record whose content depends on one live fact."""
    return {
        "id": identifier,
        "score": score,
        "content": text,
        "metadata": {
            "truth_maintenance": {
                "schema_version": 1,
                "session_id": "employment-session-1",
                "required_facts": [fact],
                "required_support_ids": [],
            }
        },
    }

rules = [
    Rule(
        rule_id="employment",
        name="employment",
        conditions=["Employed(?x)"],
        conclusion="Eligible(?x)",
    ),
]
session = TruthMaintenanceSession(rules=rules)
session.apply(assertions=[FactSupport("v1", "Employed(Alice)")])

store = StaticVectorStore([
    annotated_row("cached", "Eligible(Alice)", 0.9, "Alice is eligible"),
])
retriever = ContextRetriever(vector_store=store, use_graph_expansion=False)
gate = TruthMaintenanceContextFilter(session, session_id="employment-session-1")

checked = retriever.retrieve("eligibility", truth_filter=gate)
assert [result.content for result in checked] == ["Alice is eligible"]
assert (
    checked[0].metadata["truth_maintenance_validation"]["version"]
    == session.version
)

# The supporting evidence is withdrawn. The vector record stays stored,
# but it no longer reaches the caller through the checked retrieval.
session.apply(retractions=["v1"])
checked = retriever.retrieve("eligibility", truth_filter=gate)
assert checked == []
assert store.rows[0]["content"] == "Alice is eligible"  # record untouched
```

### 手工标注的语义

过滤器只校验应用显式写进存储元数据的标注；它既不推断依赖，也不替你给任何记录打标：

- 每个候选结果都必须携带 `metadata["truth_maintenance"]`，且恰好含四个键：`schema_version`（当前为 `1`）、`session_id`（必须与过滤器的 `session_id` 一致）、`required_facts` 和 `required_support_ids`。至少要声明一个事实或一个支持 ID。
- 候选结果要保留，必须同时满足两个条件：`required_facts` 的每一项都在快照的 `facts` 中，**且** `required_support_ids` 的每一项都在快照的激活支持中。未标注或标注畸形的候选结果都会被整条剔除——记录 ID 或节点 ID 从来不是信任信号。

### 来源级引用

两条记录可能断言同一个结论，却引用不同的来源。`required_support_ids` 把每条记录绑定到它实际使用的证据：撤回一条支持，只会让引用它的记录失效；由其他推导或显式支持兜底的记录则原样保留。

### 图结果包

从 `ContextGraph` 取回的候选结果，要求根记录**和** `related_entities` / `related_relationships` 里的每个成员都在各自的 `metadata` 上携带同样形状的标注。只要根记录或任一附属成员失去支持，整个候选结果都会被排除——结果绝不会保留正文，却悄悄丢掉一个过期的附属成员。

### 行为细节

- 过滤发生在排序之前，也发生在旧版合并逻辑之前：高分的过期记录挤不掉低分的有效记录，依赖元数据也能在合并后保留下来。
- 幸存的候选结果以深拷贝形式返回，并打上 `metadata["truth_maintenance_validation"]` 标记（含 `session_id` 和 `version`）。原始候选结果与存储记录绝不会被修改。
- 每次调用只针对一个不可变快照做校验；若检索进行途中会话提交了新版本，`retrieve` 会抛出 `ProcessingError`，而不是返回混合版本的结果。
- 向量、记忆和图三类来源在同一次过滤中处理：构造检索器时传入 `memory_store=` 或 `knowledge_graph=`，再把 `truth_filter=` 传给 `retrieve`，或传给 `search`、`vector_search`、`graph_search` 这几个委托方法（它们都转发到 `retrieve`）。`memory_search` 绕过 `retrieve`，**不会**应用过滤器——需要记忆结果有证据支撑时，请改用 `retrieve`。

### 不支持的调用入口

只有 `ContextRetriever.retrieve(mode="local", ...)`（默认模式）以及走这条路径的委托方法支持过滤器。给 `retrieve` 传 `truth_filter` 而 `mode` 为 `"global"`、`"drift"` 或 `"hybrid"` 时，检索开始前就会抛出 `ValidationError`。这些模式以及直接调用 `retrieve_global` / `retrieve_drift` 都不在依赖校验的保证范围内。

`AgentContext.retrieve`、`AgentContext.query_with_reasoning` 和 `ContextRetriever.query_with_reasoning` 有意**不**接受 `truth_filter`——在这些入口传入会立即抛出 `ValidationError`。请自己用 `ContextRetriever.retrieve(..., truth_filter=...)` 组装出已校验的上下文，再交给模型。

过滤器背后的会话模型见 [真值维护(Truth Maintenance)](./truth_maintenance.md)。


## 数据结构

<AccordionGroup>
  <Accordion title="Decision">

```python
@dataclass
class Decision:
    decision_id:          str
    category:             str
    scenario:             str
    reasoning:            str
    outcome:              str
    confidence:           float               # 0.0 - 1.0
    timestamp:            datetime
    decision_maker:       str
    reasoning_embedding:  Optional[List[float]]  # generated embedding
    node2vec_embedding:   Optional[List[float]]  # structural embedding
    valid_from:           Optional[str]       # ISO datetime
    valid_until:          Optional[str]       # ISO datetime
    metadata:             Dict[str, Any]
```

  </Accordion>
  <Accordion title="Precedent">

```python
@dataclass
class Precedent:
    precedent_id:        str
    source_decision_id:  str
    similarity_score:    float               # 0-1 match score
    relationship_type:   str                 # "similar_scenario" | "same_policy" | "exception_precedent"
    metadata:            Dict[str, Any]
```

  </Accordion>
  <Accordion title="Policy">

```python
@dataclass
class Policy:
    policy_id:    str
    name:         str
    description:  str
    rules:        Dict[str, Any]    # rule definitions
    category:     str
    version:      str               # e.g. "1.0", "2.1"
    created_at:   datetime
    updated_at:   datetime
    metadata:     Dict[str, Any]
```

  </Accordion>
  <Accordion title="PolicyException">

```python
@dataclass
class PolicyException:
    exception_id:        str
    decision_id:         str
    policy_id:           str
    reason:              str
    approver:            str
    approval_timestamp:  datetime
    justification:       str
    metadata:            Dict[str, Any]
```

  </Accordion>
  <Accordion title="ApprovalChain">

```python
@dataclass
class ApprovalChain:
    approval_id:       str
    decision_id:       str
    approver:          str
    approval_method:   str          # "slack_dm" | "zoom_call" | "email" | "system"
    approval_context:  str
    timestamp:         datetime
    metadata:          Dict[str, Any]
```

  </Accordion>
  <Accordion title="LinkedEntity">

```python
@dataclass
class LinkedEntity:
    entity_id:       str
    uri:             str
    text:            str
    type:            str
    linked_entities: List[EntityLink]
    context:         Dict[str, Any]
    confidence:      float

@dataclass
class EntityLink:
    source_entity_id:  str
    target_entity_id:  str
    link_type:         str          # "same_as" | "related_to" | "part_of"
    confidence:        float
    source:            Optional[str]
    metadata:          Dict[str, Any]
```

  </Accordion>
</AccordionGroup>


## 实战模式

<Tabs>
  <Tab title="医疗：治疗决策">
    ```python
    from semantica.context import AgentContext, ContextGraph
    from semantica.vector_store import VectorStore

    health_agent = AgentContext(
        vector_store=VectorStore(backend="faiss", dimension=768),
        knowledge_graph=ContextGraph(),
        decision_tracking=True,
    )

    health_agent.store("Patient has hypertension, type 2 diabetes")
    health_agent.store("Patient allergic to penicillin: verified 2024-01")

    decision_id = health_agent.record_decision(
        category="treatment_plan",
        scenario="Hypertension with comorbid diabetes",
        reasoning="ACE inhibitors are renoprotective in diabetic patients",
        outcome="prescribed_lisinopril",
        confidence=0.91,
    )

    precedents = health_agent.find_precedents("hypertension diabetes", limit=5)
    for p in precedents:
        print("Past: {}  (confidence: {:.2f})".format(p.outcome, p.confidence))

    chain = health_agent.get_causal_chain(decision_id, direction="downstream")
    print("Follow-up decisions triggered: {}".format(len(chain)))
    ```
  </Tab>
  <Tab title="金融：贷款决策">
    ```python
    from semantica.context import AgentContext, ContextGraph, PolicyEngine
    from semantica.context.decision_models import Policy, Decision
    from semantica.vector_store import VectorStore
    from datetime import datetime

    graph  = ContextGraph()
    policy = PolicyEngine(graph_store=graph)

    # Add compliance policy
    p = Policy(
        policy_id="lending_policy",
        name="Lending Policy",
        description="Min confidence 0.8 for loan decisions",
        rules={"min_confidence": 0.8},
        category="loan_approval",
        version="1.0",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    policy.add_policy(p)

    loan_agent = AgentContext(
        vector_store=VectorStore(backend="faiss", dimension=768),
        knowledge_graph=graph,
        decision_tracking=True,
    )
    loan_agent.store("Applicant: credit score 750, DTI 28%, stable employment 4yr")

    # Check compliance before recording
    d = Decision(
        decision_id="dec_loan_001",
        category="loan_approval",
        scenario="First-time homebuyer: 30yr fixed, 20% down",
        reasoning="Credit score above threshold, DTI within limits",
        outcome="approved_300k",
        confidence=0.94,
        timestamp=datetime.now(),
        decision_maker="loan_agent",
    )
    compliant = policy.check_compliance(d, "lending_policy")
    if compliant:
        loan_agent.record_decision(
            category=d.category,
            scenario=d.scenario,
            reasoning=d.reasoning,
            outcome=d.outcome,
            confidence=d.confidence,
        )
    ```
  </Tab>
  <Tab title="持久化与恢复">
    ```python
    from semantica.context import AgentContext, ContextGraph
    from semantica.vector_store import VectorStore

    context = AgentContext(
        vector_store=VectorStore(backend="faiss", dimension=768),
        knowledge_graph=ContextGraph(),
        decision_tracking=True,
    )

    context.store("Important fact learned during session")
    context.record_decision(
        category="ops", scenario="Scale up", reasoning="Load > 80%",
        outcome="scaled_to_10_replicas", confidence=0.97,
    )

    # Persist everything
    context.save("agent_state/")

    # Later: restore and continue
    restored = AgentContext(
        vector_store=VectorStore(backend="faiss", dimension=768),
        knowledge_graph=ContextGraph(),
        decision_tracking=True,
    )
    restored.load("agent_state/")

    results = restored.retrieve("load scaling decisions", max_results=3)
    ```
  </Tab>
</Tabs>

- [Vector Store](./vector_store.md) — 记忆检索的嵌入存储后端。
- [Knowledge Graph](./kg.md) — ContextGraph 内部使用的图算法与分析。
- [Reasoning](./reasoning.md) — 叠加在上下文之上的逻辑推理。
- [Provenance](./provenance.md) — 每条存储事实的 W3C PROV-O 血缘。

- [Context Module](https://github.com/semantica-agi/semantica/blob/main/cookbook/introduction/19_Context_Module.ipynb) — 记忆与决策跟踪 · Intermediate
- [Advanced Context Engineering](https://github.com/semantica-agi/semantica/blob/main/cookbook/advanced/11_Advanced_Context_Engineering.ipynb) — 生产级 FAISS + Neo4j 配置 · Advanced
