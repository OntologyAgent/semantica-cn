---
title: "距离智能（Distance Intelligence）"
description: "语义邻域、N×N 距离矩阵、自我模式探索、邻近度混合检索与嵌入缓存优化。"
source: reference/distance.md
source_version: 1366e0fd6e8217ad7b18b409f41673b31b9347e5
icon: "radar"
---

距离智能给知识图谱里每个节点一个**语义邻域**——不仅能回答"A 和 B 连通吗？"，还能回答"A 和 B 语义上有多近？中间有什么？"

距离智能在 **v0.5.0** 引入，横跨三层：

<div style={{display:"flex",flexWrap:"wrap",gap:"1.5rem",margin:"1.5rem 0"}}>
  <div style={{flex:"1 1 200px",padding:"1.25rem 1.5rem",borderRadius:"10px",border:"1px solid rgba(16,185,129,0.25)",background:"rgba(16,185,129,0.04)"}}>
    <div style={{fontSize:"1.1rem",fontWeight:700,color:"#10B981",marginBottom:"6px"}}>距离矩阵</div>
    <div style={{fontSize:"0.82rem",color:"rgba(255,255,255,0.6)",lineHeight:1.5}}>任意节点集的 N×N 上三角语义距离</div>
  </div>
  <div style={{flex:"1 1 200px",padding:"1.25rem 1.5rem",borderRadius:"10px",border:"1px solid rgba(16,185,129,0.25)",background:"rgba(16,185,129,0.04)"}}>
    <div style={{fontSize:"1.1rem",fontWeight:700,color:"#10B981",marginBottom:"6px"}}>语义邻域</div>
    <div style={{fontSize:"0.82rem",color:"rgba(255,255,255,0.6)",lineHeight:1.5}}>带置信度衰减与距离分带分类的 BFS 自我图(ego-graph)</div>
  </div>
  <div style={{flex:"1 1 200px",padding:"1.25rem 1.5rem",borderRadius:"10px",border:"1px solid rgba(16,185,129,0.25)",background:"rgba(16,185,129,0.04)"}}>
    <div style={{fontSize:"1.1rem",fontWeight:700,color:"#10B981",marginBottom:"6px"}}>邻近度混合</div>
    <div style={{fontSize:"0.82rem",color:"rgba(255,255,255,0.6)",lineHeight:1.5}}>检索时把语义相似度与图邻近度结合</div>
  </div>
  <div style={{flex:"1 1 200px",padding:"1.25rem 1.5rem",borderRadius:"10px",border:"1px solid rgba(16,185,129,0.25)",background:"rgba(16,185,129,0.04)"}}>
    <div style={{fontSize:"1.1rem",fontWeight:700,color:"#10B981",marginBottom:"6px"}}>10× 缓存</div>
    <div style={{fontSize:"0.82rem",color:"rgba(255,255,255,0.6)",lineHeight:1.5}}>基于图修订号的嵌入缓存，避免重复计算</div>
  </div>
</div>


## 距离分带

每个邻居结果都按跳数和语义相似度归入四个距离分带之一：

| 分带 | 跳数 | 含义 | Explorer 颜色 |
| :---- | :-------- | :------- | :------------- |
| `direct` | 1 | 直接邻居——语义重叠强 | 绿色 |
| `near` | 2 | 一跳之外——概念密切相关 | 青色 |
| `mid-range` | 3–4 | 概念相关但有一定间隔 | 黄色 |
| `distant` | 5+ | 结构连接弱 | 红色 |

距离分带贯穿整个系统：检索结果、路径响应、API 端点、Explorer 自我模式(Ego Mode)可视化，用的都是同一套四级分类。


## 快速开始

<Steps>
  <Step title="带距离元数据获取邻居">
    最简单的入口：调用 `get_neighbors()` 并传 `include_distance_metadata=True`：

    ```python
    from semantica.context import ContextGraph

    graph = ContextGraph(advanced_analytics=True)

    graph.add_node("python",   "language",   properties={"paradigm": "multi"})
    graph.add_node("fastapi",  "framework",  properties={"language": "Python"})
    graph.add_node("django",   "framework",  properties={"language": "Python"})
    graph.add_node("sqlmodel", "library",    properties={"orm": True})

    graph.add_edge("python",   "fastapi",  "enables")
    graph.add_edge("python",   "django",   "enables")
    graph.add_edge("fastapi",  "sqlmodel", "uses")

    neighbors = graph.get_neighbors(
        "python",
        hops=3,
        include_distance_metadata=True,
    )

    for n in neighbors:
        print(f"{n['node_id']:12s}  band={n['distance_band']:10s}  "
              f"decay={n['confidence_decay']:.3f}  "
              f"path={n['path_to_anchor']}")
    ```
    ```
    fastapi       band=direct     decay=1.000  path=['python', 'fastapi']
    django        band=direct     decay=1.000  path=['python', 'django']
    sqlmodel      band=near       decay=0.750  path=['python', 'fastapi', 'sqlmodel']
    ```
  </Step>
  <Step title="计算语义距离矩阵">
    ```python
    from semantica.kg import SimilarityCalculator, NodeEmbedder

    # Generate structural embeddings first
    embedder   = NodeEmbedder(method="node2vec", embedding_dimension=128)
    embeddings = embedder.compute_embeddings(kg, ["language", "framework", "library"], ["enables", "uses"])

    # N×N upper-triangle distance matrix
    calc   = SimilarityCalculator()
    matrix = calc.compute_distance_matrix(embeddings)

    # matrix["distances"] is an upper-triangle dict: {(node_a, node_b): distance}
    for (a, b), dist in sorted(matrix["distances"].items(), key=lambda x: x[1]):
        print(f"{a:15s} ↔ {b:15s}  distance={dist:.4f}")
    ```
  </Step>
  <Step title="把邻近度混入检索">
    在 `AgentContext` 上设 `proximity_weight`，把图邻近度混进每次语义检索调用：

    ```python
    from semantica.context import AgentContext, ContextGraph
    from semantica.vector_store import VectorStore

    context = AgentContext(
        vector_store=VectorStore(backend="faiss", dimension=768),
        knowledge_graph=ContextGraph(advanced_analytics=True),
        decision_tracking=True,
        proximity_weight=0.3,   # combined = 0.7×semantic + 0.3×proximity
    )

    # retrieve() and find_precedents() both use the blended score
    results = context.retrieve("web API frameworks", max_results=10)
    for r in results:
        print(f"[{r['combined_score']:.3f}]  semantic={r['semantic_score']:.3f}  "
              f"proximity={r['proximity_score']:.3f}  {r['content'][:60]}")
    ```
  </Step>
</Steps>


## ContextGraph 距离 API

### `get_neighbors()`

`include_distance_metadata=True` 时返回带距离元数据的 BFS 邻居：

```python
neighbors = graph.get_neighbors(
    node_id="python",
    hops=4,
    include_distance_metadata=True,
    min_weight=0.3,               # exclude low-confidence edges
)
```

| 字段 | 类型 | 说明 |
| :---- | :---- | :----------- |
| `node_id` | `str` | 节点标识符 |
| `node_type` | `str` | 节点类型标签 |
| `properties` | `Dict` | 节点属性 dict |
| `hop_count` | `int` | 距锚点的 BFS 跳数 |
| `distance_band` | `str` | `"direct"` / `"near"` / `"mid-range"` / `"distant"` |
| `confidence_decay` | `float` | 按跳数衰减后的置信度：`weight^hop_count` |
| `path_to_anchor` | `List[str]` | 锚点到该节点的最短路径 |
| `edge_weight` | `float` | 直接边的权重（hop=1 时） |

### `get_neighbor_distances()`

返回按置信度衰减距离综合得分排序的邻居列表：

```python
distances = graph.get_neighbor_distances("fastapi", hops=3)

for d in distances:
    print(f"{d['node_id']:15s}  score={d['combined_distance_score']:.4f}  "
          f"band={d['distance_band']}")
```


## SimilarityCalculator — 成对相似度

`SimilarityCalculator` 用四种度量计算节点嵌入间的相似度。

```python
from semantica.kg import SimilarityCalculator

calc = SimilarityCalculator(method="cosine", normalize=True)
# method: "cosine" | "euclidean" | "manhattan" | "correlation"
```

### 构造参数

| 参数 | 类型 | 默认值 | 说明 |
| :--------- | :---- | :------- | :----------- |
| `method` | `str` | `"cosine"` | 默认度量：`"cosine"`、`"euclidean"`、`"manhattan"`、`"correlation"` |
| `normalize` | `bool` | `True` | 计算前先归一化向量 |

### 方法

| 方法 | 返回 | 说明 |
| :------ | :------- | :----------- |
| `cosine_similarity(vector1, vector2)` | `float` | 两向量的余弦相似度 `[-1, 1]` |
| `euclidean_distance(embedding1, embedding2)` | `float` | 两向量的 L2 距离（非负） |
| `manhattan_distance(embedding1, embedding2)` | `float` | 两向量的 L1 距离（非负） |
| `correlation_similarity(embedding1, embedding2)` | `float` | 两向量的 Pearson 相关系数 `[-1, 1]` |
| `batch_similarity(embeddings, query_embedding, method=None, top_k=None, chunk_size=1000)` | `Dict[str, float]` | 全部节点对某查询向量的相似度。返回 `{node_id: score}` |
| `pairwise_similarity(embeddings, method=None)` | `Dict[Tuple[str,str], float]` | 全部节点对的上三角 N×N 成对相似度矩阵 |
| `find_most_similar(embeddings, query_embedding, top_k=10, method=None)` | `List[Tuple[str, float]]` | 按相似度排序的 top-k `(node_id, score)` 对 |

### 成对相似度矩阵

`pairwise_similarity()` 返回 N×N 矩阵的上三角——每个键是 `(node_id_a, node_id_b)` 元组：

```python
from semantica.kg import NodeEmbedder, SimilarityCalculator

embedder   = NodeEmbedder(method="node2vec", embedding_dimension=128)
embeddings = embedder.compute_embeddings(kg, ["language", "framework"], ["enables", "uses"])

calc = SimilarityCalculator(method="cosine")

# N×N upper-triangle: Dict[(node_a, node_b), similarity_score]
matrix = calc.pairwise_similarity(embeddings)

# Sort by similarity (most similar first)
for (a, b), score in sorted(matrix.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"{a:15s} ↔ {b:15s}  similarity={score:.4f}")

# Find most similar pair
best_pair = max(matrix.items(), key=lambda x: x[1])
print(f"Most similar: {best_pair[0]}  score={best_pair[1]:.4f}")

# Find most dissimilar pair
worst_pair = min(matrix.items(), key=lambda x: x[1])
print(f"Most distant:  {worst_pair[0]}  score={worst_pair[1]:.4f}")
```

<Note>
  矩阵只有上三角——存 `(a, b)` 不存 `(b, a)`。任一方向查询：`matrix.get((a, b)) or matrix.get((b, a))`。
</Note>

### 批量相似度

用分块向量化运算高效比较查询向量与全部节点：

```python
# Query vector against all nodes
scores = calc.batch_similarity(
    embeddings,
    query_embedding=my_query_vec,
    method="cosine",    # override default
    top_k=10,           # return only top 10 (None = all)
    chunk_size=1000,    # chunk size for memory efficiency
)

for node_id, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
    print(f"{node_id:15s}  {score:.4f}")
```

### 找最相似

```python
# Top-k (node_id, score) tuples sorted descending
similar = calc.find_most_similar(
    embeddings,
    query_embedding=embeddings["python"],
    top_k=5,
    method="cosine",
)

for node_id, score in similar:
    print(f"{node_id:15s}  similarity={score:.4f}")
```

### 单项度量

```python
vec_a = embeddings["fastapi"]
vec_b = embeddings["django"]

cosine  = calc.cosine_similarity(vec_a, vec_b)
l2      = calc.euclidean_distance(vec_a, vec_b)
l1      = calc.manhattan_distance(vec_a, vec_b)
pearson = calc.correlation_similarity(vec_a, vec_b)

print(f"Cosine:      {cosine:.4f}")
print(f"Euclidean:   {l2:.4f}")
print(f"Manhattan:   {l1:.4f}")
print(f"Correlation: {pearson:.4f}")
```


## 邻近度混合检索

`AgentContext.retrieve()` 和 `find_precedents()` 都支持 `proximity_weight` 参数，把图邻近度混入语义相似度得分：

```
combined_score = (1 − proximity_weight) × semantic_score
              + proximity_weight × proximity_score
```

其中 `proximity_score` 由查询锚点节点的跳数和边权重导出。

```python
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore

context = AgentContext(
    vector_store=VectorStore(backend="faiss", dimension=768),
    knowledge_graph=ContextGraph(advanced_analytics=True),
    proximity_weight=0.3,
)

# Standard retrieval — proximity blended automatically
results = context.retrieve("model deployment strategies", max_results=10)

# Override weight per-call
results = context.retrieve(
    "model deployment strategies",
    max_results=10,
    proximity_weight=0.5,   # stronger proximity weight for this query
)

# find_precedents also blends proximity
precedents = context.find_precedents(
    "infrastructure scaling decisions",
    proximity_weight=0.4,
    limit=5,
)

for p in precedents:
    print(f"[{p.combined_score:.3f}]  {p.outcome}  (confidence: {p.confidence:.2f})")
```


## 嵌入缓存

嵌入缓存避免为上次调用以来未变化的节点重复计算嵌入——大图上吞吐量最高提升 **10 倍**。

### 工作原理

每个 `GraphSession` 维护一个由当前节点和边状态导出的**图修订哈希**。距离矩阵或邻域请求到达时：

1. 修订哈希与缓存哈希比较
2. 未变：直接返回缓存的嵌入
3. 已变（增改了节点/边）：缓存失效，重新计算嵌入

```python
from semantica.explorer import GraphSession

session = GraphSession(graph=kg)

# First call: computes embeddings, stores in cache
embeddings = session.get_cached_embeddings()

# Second call (graph unchanged): returns cache instantly
embeddings = session.get_cached_embeddings()

# After graph modification: cache is automatically invalidated
session.graph.add_node("new_node", "concept", properties={})
embeddings = session.get_cached_embeddings()  # recomputes
```

| 参数 | 类型 | 默认值 | 说明 |
| :--------- | :---- | :------- | :----------- |
| `force_refresh` | `bool` | `False` | 图未变也强制缓存失效 |
| 缓存失效 | 自动 | — | `add_nodes()`、`add_edges()` 或任何变更都会触发 |
| 缓存范围 | 每会话 | — | 每个 `GraphSession` 维护自己独立的缓存 |

<Tip>
  缓存在 Explorer 部署中最有效：同一张图被反复查询距离矩阵和自我模式邻域。批量流水线场景设 `force_refresh=True`，确保始终用最新图状态。
</Tip>


## REST API 端点

v0.5.0 新增五个端点，供程序化访问距离智能：

### `POST /api/graph/distance-matrix`

为一组节点 ID 计算 N×N 语义距离矩阵：

```bash
curl -X POST http://localhost:8000/api/graph/distance-matrix \
  -H "Content-Type: application/json" \
  -d '{
    "node_ids": ["alice", "bob", "acme_corp", "beta_ltd"],
    "embedding_model": "all-MiniLM-L6-v2",
    "include_band_classification": true
  }'
```

```json
{
  "matrix": {
    "alice,bob": 0.312,
    "alice,acme_corp": 0.087,
    "alice,beta_ltd": 0.154,
    "bob,acme_corp": 0.401,
    "bob,beta_ltd": 0.233,
    "acme_corp,beta_ltd": 0.198
  },
  "most_similar": ["alice", "acme_corp"],
  "most_distant": ["bob", "acme_corp"],
  "mean_distance": 0.231
}
```

### `GET /api/graph/node/{id}/semantic-neighborhood`

取节点的自我图（BFS 邻域），带距离元数据：

```bash
curl "http://localhost:8000/api/graph/node/alice/semantic-neighborhood?depth=3&include_distance_metadata=true"
```

```json
{
  "anchor_node": "alice",
  "neighbors": [
    {"node_id": "acme_corp", "distance_band": "direct",   "confidence_decay": 1.0,  "hop_count": 1},
    {"node_id": "ceo_role",  "distance_band": "direct",   "confidence_decay": 1.0,  "hop_count": 1},
    {"node_id": "beta_ltd",  "distance_band": "near",     "confidence_decay": 0.75, "hop_count": 2},
    {"node_id": "london_hq", "distance_band": "mid-range","confidence_decay": 0.56, "hop_count": 3}
  ],
  "total_neighbors": 4,
  "depth": 3
}
```

### `GET /api/decisions/causal-distance`

返回两个决策节点间的因果距离（经因果边的跳数）：

```bash
curl "http://localhost:8000/api/decisions/causal-distance?source=dec_001&target=dec_005"
```

```json
{
  "source": "dec_001",
  "target": "dec_005",
  "causal_hops": 3,
  "causal_path": ["dec_001", "dec_002", "dec_004", "dec_005"],
  "distance_band": "near"
}
```

### `GET /api/temporal/distance-history`

追踪两节点语义距离随时间的演化：

```bash
curl "http://localhost:8000/api/temporal/distance-history?node_a=alice&node_b=acme_corp&snapshots=2021-01-01,2022-01-01,2023-01-01"
```

```json
{
  "node_a": "alice",
  "node_b": "acme_corp",
  "history": [
    {"timestamp": "2021-01-01", "distance": 0.08, "band": "direct"},
    {"timestamp": "2022-01-01", "distance": 0.09, "band": "direct"},
    {"timestamp": "2023-01-01", "distance": 0.54, "band": "mid-range"}
  ]
}
```

### `POST /api/export/distance-enriched`

导出带距离元数据的图数据（CSV 或 JSONL，上限 200 节点）：

```bash
curl -X POST http://localhost:8000/api/export/distance-enriched \
  -H "Content-Type: application/json" \
  -d '{"anchor_node": "alice", "depth": 4, "format": "csv"}'
```


## Explorer 距离智能界面

Knowledge Explorer 把距离智能直接嵌进浏览器面板：

<AccordionGroup>

<Accordion title="自我模式（Ego Mode）" icon="circle-nodes">
  自我模式把可视化聚焦到选定节点，用 **BFS 景深渐隐**渲染其语义邻域——离锚点越远的节点越暗，呈现概念邻近度的"形状"。

  - **深度滑块（1–8）**：控制邻域的 BFS 半径
  - **置信度衰减可视化**：边的不透明度映射 `confidence_decay` 得分
  - **距离分带配色**：绿（direct）→ 青（near）→ 黄（mid-range）→ 红（distant）
  - **瓶颈高亮**：连接原本分离簇的桥节点在路径检查器中高亮

  经 Explorer 工具栏启用：**View → Ego Mode**，然后点任意节点设为锚点。
</Accordion>

<Accordion title="距离热力图" icon="table-cells">
  热力图把 N×N 距离矩阵渲染成配色网格——一眼看出哪些节点簇语义内聚、哪些孤立。

  - **色标**：绿（近，距离 → 0）经黄到红（远，距离 → 1）
  - **悬停**：显示每格的精确距离值与距离分带
  - **排序选项**：按节点类型、社区归属或字母序排行列

  经 Explorer 侧边栏的 **View → Distance Heatmap** 进入。
</Accordion>

<Accordion title="语义叠加层" icon="layer-group">
  不切换模式，把语义相似度叠加到标准力导向图布局上：

  - **语义叠加层**：边粗细按语义相似度得分缩放
  - **结构叠加层**：边粗细按图中心性缩放
  - 两个叠加层可独立开关

  经 Explorer 工具栏的 **Overlay** 开关进入。
</Accordion>

<Accordion title="路径检查器" icon="route">
  点任意两个节点，检查它们之间的最短路径。路径检查器显示：

  - **距离分带徽章**：把整条路径归为 direct / near / mid-range / distant
  - **指标卡片**：跳数、平均边权重、路径置信度衰减
  - **瓶颈节点高亮**：移除即断路的唯一节点
  - **距离历史**：两节点距离跨图快照的时间线

  经任意两个选中节点**右键 → Inspect Path** 进入。
</Accordion>

</AccordionGroup>


## 实战模式

<Tabs>
  <Tab title="知识簇发现">
    不跑社区检测，直接在大知识图谱里找语义内聚的话题簇：

    ```python
    from semantica.kg import NodeEmbedder, SimilarityCalculator

    embedder = NodeEmbedder(method="node2vec", embedding_dimension=128)
    embeddings = embedder.compute_embeddings(kg, node_types=["Concept", "Topic"])

    calc = SimilarityCalculator()

    # Cluster nodes where pairwise distance < 0.2
    clusters = calc.cluster_by_distance(embeddings, threshold=0.2)

    for i, cluster in enumerate(clusters):
        print(f"Cluster {i+1} ({len(cluster)} nodes): {cluster[:5]}")
    ```
  </Tab>
  <Tab title="异常检测">
    标记与其结构邻居意外疏远的节点——可能是数据质量问题，也可能是真异常：

    ```python
    from semantica.context import ContextGraph
    from semantica.kg import NodeEmbedder, SimilarityCalculator

    graph   = ContextGraph(advanced_analytics=True)
    # ... build graph ...

    embedder = NodeEmbedder(method="node2vec", embedding_dimension=128)
    embeddings = embedder.compute_embeddings(graph._graph, ["entity"], ["RELATED_TO"])

    calc = SimilarityCalculator()

    for node_id in graph._graph.nodes():
        neighbors = graph.get_neighbors(node_id, hops=1, include_distance_metadata=True)
        for n in neighbors:
            # Node connected by edge but semantically very distant → anomaly candidate
            structural_dist = 1.0 - n["edge_weight"]
            semantic_dist   = calc.euclidean_distance(
                embeddings[node_id], embeddings[n["node_id"]]
            )
            if semantic_dist > 0.7 and structural_dist < 0.3:
                print(f"Anomaly: {node_id} → {n['node_id']}  "
                      f"(structural={structural_dist:.2f}, semantic={semantic_dist:.2f})")
    ```
  </Tab>
  <Tab title="决策一致性审计">
    验证相似决策（语义距离小）是否得到相似结果——标记不一致项供人工复核：

    ```python
    from semantica.context import AgentContext, ContextGraph
    from semantica.vector_store import VectorStore

    context = AgentContext(
        vector_store=VectorStore(backend="faiss", dimension=768),
        knowledge_graph=ContextGraph(advanced_analytics=True),
        decision_tracking=True,
        proximity_weight=0.4,
    )

    # ... populate with historical decisions ...

    # Find pairs of semantically close decisions with different outcomes
    all_decisions = context.query_decisions("", max_hops=0)
    for i, d1 in enumerate(all_decisions):
        for d2 in all_decisions[i+1:]:
            precedents = context.find_precedents(
                d1.scenario, limit=5, proximity_weight=0.4
            )
            for p in precedents:
                if p.source_decision_id == d2.decision_id:
                    if p.similarity_score > 0.85 and d1.outcome != d2.outcome:
                        print(f"INCONSISTENCY: {d1.scenario}")
                        print(f"  Decision A: {d1.outcome}  (confidence {d1.confidence:.2f})")
                        print(f"  Decision B: {d2.outcome}  (confidence {d2.confidence:.2f})")
                        print(f"  Similarity: {p.similarity_score:.3f}")
    ```
  </Tab>
</Tabs>


## 性能

| 操作 | 无缓存 | 有缓存 | 提升 |
| :--------- | :------------ | :--------- | :---------- |
| 距离矩阵（11.8 万节点） | ~48s | ~4.8s | **10×** |
| 语义邻域（深度 4） | ~2.1s | ~0.21s | **10×** |
| 节点检索（有索引） | 24 ms | 0.004 ms | **6,000×** |
| 语义去重 | 基线 | — | **6.98×**（v2 算法） |

<Note>
  10× 缓存提升的前提是两次请求之间图未变化。节点持续写入的写重流水线里，缓存命中率会更低。读重的 Explorer 用 `force_refresh=False`（默认），批量流水线场景用 `force_refresh=True`。
</Note>

- [Context Module](./context.md) — `ContextGraph.get_neighbors()` 与邻近度混合检索。
- [Knowledge Graph Module](./kg.md) — `NodeEmbedder`、`SimilarityCalculator` 与图分析。
- [Visualization](./visualization.md) — 程序化距离热力图与自我模式图渲染。
- [Explorer](./explorer.md) — 内置距离智能面板的 Knowledge Explorer。

- [Distance Intelligence](https://github.com/semantica-agi/semantica/blob/main/cookbook/advanced/12_Distance_Intelligence.ipynb) — 语义邻域与距离矩阵 · 高级
