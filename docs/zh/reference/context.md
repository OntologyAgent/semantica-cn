---
title: "上下文模块（Context）"
description: "智能体上下文图、决策跟踪、因果链、先例搜索、政策执行与多跳 GraphRAG。"
source: reference/context.md
source_version: 24f0993584fb160848b2c35510a23b65dc342ae3
icon: "brain"
---

`semantica.context` 是 AI 智能体的记忆与决策层：

- 存储事实，带溯源和基于嵌入的检索
- 把决策记录为一等图对象，保留完整因果链
- 让智能体检索自己的历史，跨运行保持一致
- 经多跳 GraphRAG 遍历回答复杂查询
- 执行带版本的政策并跟踪合规例外


## 导出的类

| 类 | 职责 |
| :--- | :--- |
| `AgentContext` | 主入口：记忆、检索、决策、图遍历、检查点 |
| `ContextGraph` | 内存知识图谱：中心性、社区检测和决策跟踪 |
| `AgentMemory` | 向量驱动的持久记忆：`store(text)`、`retrieve(query, max_results)` |
| `EntityLinker` | 把实体提及链接到 URI；在实体 ID 之间创建类型化边 |
| `ContextRetriever` | 混合向量 + 图检索，支持最低分数和图扩展选项 |
| `DecisionRecorder` | 记录决策，带嵌入、因果链和元数据 |
| `PolicyEngine` | 政策管理：`add_policy()`、`check_compliance()`、`get_applicable_policies()` |
| `CausalChainAnalyzer` | 追溯决策之间的相互影响：`get_causal_chain(decision_id)` |


## 你能得到什么

- **AgentContext** — 记忆、决策跟踪和图检索收进一个 API
  - 对话历史与检查点差异对比
  - 完整上下文状态持久化到磁盘并恢复
- **ContextGraph** — 线程安全的内存知识图谱
  - PageRank、中心性、社区检测、时态有效性
  - 跨图导航和链接遍历
- **AgentMemory** — 带保留策略的嵌入记忆
  - 可配置 `max_memory_size` 的 LRU 淘汰
  - 按对话隔离历史
- **DecisionRecorder** — 记录决策，带因果链和置信度得分
  - 时态有效窗口（`valid_from` / `valid_until`）
  - 每条决策都捕获跨系统上下文
- **PolicyEngine** — 存在知识图谱里的带版本政策
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
    最快搭建：不需要知识图谱。适合只需要对事实做语义搜索、不想承担图遍历开销的智能体。

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
      调大 `max_expansion_hops` 遍历更深，代价是延迟。从 2 起步往上调。
    </Tip>
  </Tab>
  <Tab title="政策执行">
    添加带版本的合规政策，每条决策记录前先过一遍。

    ```python
    from semantica.context import AgentContext, ContextGraph, PolicyEngine
    from semantica.vector_store import VectorStore

    context = AgentContext(
        vector_store=VectorStore(backend="faiss", dimension=768),
        knowledge_graph=ContextGraph(),
        decision_tracking=True,
    )

    engine = PolicyEngine(knowledge_graph=context.knowledge_graph)

    engine.add_policy(
        name="data_privacy",
        description="No PII stored without user consent flag",
        version="1.2",
        effective_date="2024-01-01",
        category="privacy",
        rules={"requires_consent": True, "max_retention_days": 90},
    )

    decision_data = {"action": "store_user_email", "user_consent": True}
    result = engine.check_compliance(decision_data, policy_names=["data_privacy"])

    if result["compliant"]:
        context.record_decision(
            category="data_storage",
            scenario="Store user profile",
            outcome="stored",
            confidence=1.0,
        )
    else:
        print("Blocked by policy:", result["violations"])
    ```
  </Tab>
</Tabs>


## AgentContext

**`AgentContext`** 是主入口。把记忆、图和决策跟踪包在**单一统一 API** 后面。

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
  **设 `retention_days` 防止记忆膨胀。**默认 `30` 会自动修剪。合规攸关的智能体可能需要 `retention_days=None`，再用 `export()` 显式归档。
</Tip>

<Tip>
  **跨运行持久化你的上下文。**`VectorStore` 不会自动持久化——给它的构造函数传 `index_path=` 是无效操作。调 `context.save("agent_state/")` 把记忆、向量索引和图写到磁盘，下一个进程用 `context.load("agent_state/")` 恢复。见下文[实战模式](#real-world-patterns)的"持久化与恢复"标签页。
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
  **`retrieve()` 用的是 `max_results=`，不是 `top_k=`。**参数名是 `max_results`（默认 `5`）。传 `use_graph=True` 强制 GraphRAG、`use_graph=False` 强制纯向量检索：不管有没有配置 `knowledge_graph`。
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

**要求构造时设置 `knowledge_graph`**：启用 `query_with_reasoning()` 做 LLM 支撑的多跳遍历：

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
  **每个重要决策之前都用 `find_precedents()`。**上下文模块就是这样防止智能体跨运行做出矛盾选择的。把先例作为上下文呈现给 LLM："基于类似理由我们之前选过 X。"
</Tip>

### 检查点方法

**审计推理循环的理想工具**：一轮前后各拍一个快照，看清到底改了什么：

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

**`ContextGraph`** 是 `AgentContext` 背后的知识图谱。也可以**独立使用**，只做关系建模，不要整个上下文层。

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

必需的 frontmatter 字段是 `id`、`created_at`、`updated_at`，以及 `type` 或 `kind` 二选一。可选元数据可在顶层编辑。导入会在改动记忆之前拒绝格式错误或重复的字段，重新导入未变化的文件是幂等的。记忆本地的 `entities` 和 `relationships` 会作为溯源保留，但 Markdown 导入不会把它们应用到 `ContextGraph`。请使用专用的导出目录：同名文件会被覆盖，但无关或过期的 Markdown 文件不会被自动删除。导出拒绝覆盖文件系统链接，使用原子文件替换；导入同样拒绝符号链接、Windows 目录联接和其他 Windows 重解析点。
时间戳偏移量在 Markdown 里原样保留，只在比较时归一化为 UTC，因此带时区和不带时区的记录可以安全地一起查询。向量存储写入会推迟到内存导入提交之后；适配器同步尽力而为，失败会记日志。


## PolicyEngine

`PolicyEngine` 管理存放在知识图谱中的带版本政策。政策存为节点，可以链接到决策：

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
  **`EntityLinker.link_entities()` 链接的是两个实体 ID，不是列表。**调 `link_entities(entity1_id, entity2_id, link_type)` 在两个已知 ID 之间创建类型化边。要链接从文本抽取的实体，改用 `link(text, entities=[...])`。
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
