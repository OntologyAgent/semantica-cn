---
title: "知识图谱模块（KG）"
description: "图构建、时态模型、图分析、相似度打分与结构化嵌入。"
source: reference/kg.md
source_version: 22789d3a9ca042bcabe9f7f1acb7b1bccb148c9c
icon: "diagram-project"
---

`semantica.kg` 把抽取出的实体和关系变成结构化、可查询的知识图谱(Knowledge Graph，KG)：

- 时态节点和边带 `valid_from` / `valid_until` 窗口，支持全部 13 种 Allen 区间关系
- 完整图分析套件：中心性、社区检测、路径查找、链路预测
- Node2Vec 结构化嵌入，服务下游机器学习和相似度打分
- OWL-Time 导出和带版本的快照（`TemporalVersionManager`）
- 持久化之前先做模式和约束校验


## 导出的类

| 类 | 职责 |
| :--- | :--- |
| `KnowledgeGraph` | 核心图数据结构：节点、边、属性、时态有效期 |
| `GraphBuilder` | 从实体 + 关系构建图；传 `merge_entities=True` 启用去重 |
| `RelationalSchemaMapper` | 把关系型/表格数据源的行映射为 `GraphBuilder` 和 `OntologyGenerator` 可直接消费的 `{"entities", "relationships"}` |
| `GraphBuilderWithProvenance` | 包装 `GraphBuilder`，可选溯源跟踪；传 `provenance=True` 启用 |
| `EntityResolver` | 图构建过程中的实体去重与合并 |
| `GraphAnalyzer` | 统一分析入口：一次调用跑完中心性、社区检测和连通性 |
| `ConnectivityAnalyzer` | 连通分量检测、桥识别、密度与度统计 |
| `TemporalGraphQuery` | 时间点快照、区间查询、演化分析、时态路径查找 |
| `TemporalPatternDetector` | 时态边上的序列与循环模式检测 |
| `TemporalReasoningEngine` | 对 `TemporalInterval` 对象施加全部 13 种 Allen 区间代数关系 |
| `TemporalInterval` | 不可变 dataclass `(start: datetime, end: datetime \| TemporalBound, label?)` |
| `IntervalRelation` | 全部 13 种 Allen 关系标签的枚举（`BEFORE`、`AFTER`、`MEETS` 等） |
| `BiTemporalFact` | 包装 `valid_from`、`valid_until`、`recorded_at`、`superseded_at` 的 dataclass。工厂方法：`BiTemporalFact.from_relationship(rel_dict)` |
| `TemporalBound` | 开放区间的哨兵枚举——单值：`TemporalBound.OPEN` |
| `TemporalNormalizer` | 把自然语言时间表达式解析为 `(datetime, datetime)` 元组，全程不调用大语言模型(LLM) |
| `TemporalQueryRewriter` | 从自由文本查询中抽取时态意图；返回 `TemporalQueryResult` |
| `TemporalQueryResult` | `TemporalQueryRewriter.rewrite()` 的 dataclass 输出 |
| `TemporalVersionManager` | 带版本的快照：SHA-256 完整性校验、SQLite 持久化存储 |
| `CentralityCalculator` | PageRank、度、中介、接近、特征向量中心性 |
| `CommunityDetector` | Louvain、Leiden、标签传播、K-派系社区检测 |
| `PathFinder` | Dijkstra、A*、BFS、K 短路径算法 |
| `LinkPredictor` | 优先连接、Jaccard、Adamic-Adar 链路预测 |
| `NodeEmbedder` | Node2Vec 结构化嵌入，服务下游机器学习 |
| `SimilarityCalculator` | 余弦、欧氏、曼哈顿、相关系数相似度打分 |
| `GraphValidator` | 持久化前的模式与约束校验 |
| `AlgorithmTrackerWithProvenance` | 带溯源元数据的算法执行跟踪 |
| `AlgorithmRegistry` / `algorithm_registry` | 已注册算法的注册表；`algorithm_registry` 是共享单例 |
| `ProvenanceTracker` | 图操作的 W3C PROV-O 溯源跟踪 |
| `SeedManager` | 跨算法的可复现随机种子管理 |
| `KGConfig` / `kg_config` | 模块级配置；`kg_config` 是共享单例 |


<Tip>
  冲突检测(Conflict Detection)和高级实体消解(Entity Resolution)请配合 `semantica.conflicts` 和 `semantica.deduplication` 使用。
</Tip>

<img src="../../docs/assets/img/diagrams/kg-structure.svg" alt="Knowledge graph entity and relation structure: Person, Organization, Location, Date nodes with typed labeled edges" style={{ width: '100%', borderRadius: '12px', margin: '0 0 24px' }} />

## GraphBuilder

**`GraphBuilder`** 从抽取出的实体和关系构建知识图谱。`merge_entities` 默认 `False`：传 **`True`** 在构建过程中启用实体去重：

```python
from semantica.kg import GraphBuilder

# Pass a dict with "entities" and "relationships" keys
builder = GraphBuilder(merge_entities=True)
kg = builder.build({"entities": entities, "relationships": relationships})
```

| 方法 | 返回 | 说明 |
| :------ | :------- | :----------- |
| `build(sources)` | `dict` | 从 dict、dict 列表或实体/关系对象列表构建图 |
| `build_single_source(data)` | `dict` | 从单个数据源 dict 构建图 |

## RelationalSchemaMapper

**`RelationalSchemaMapper`** 把关系型或表格数据源的行，加上一份简短的模式说明，转换成 `GraphBuilder` 和 `OntologyGenerator` 消费的 `{"entities": [...], "relationships": [...]}` 结构。数据已经以行和列的形式存在（业务数据库、数据仓库、DataFrame）时使用它：无需把行拼成文本再交给大语言模型抽取，主键和外键直接决定图的结构。

映射规则：

- 实体表的每一行变成一个实体。实体 ID 为 `"<Type>:<pk>"`，其余列成为实体属性。同一行从两个记录系统摄取时得到相同的 ID，便于冲突检测。
- 每个外键变成一条带类型的关系，从当前行的实体指向被引用的实体。
- 联结表(junction table)不在 `entity_tables` 中、由恰好两个外键组成，只生成关系，不生成实体。关系从第一个外键指向第二个外键，联结表的其余列成为关系属性。
- 每个实体和关系都记录来源：实体带扁平的 `source` 字段（`ConflictDetector` 读取它），实体和关系都带 `metadata: {"source", "table"}`，供溯源使用。

```python
from semantica.kg import GraphBuilder, RelationalSchemaMapper

mapper = RelationalSchemaMapper(
    entity_tables={
        "CUSTOMERS": {"pk": "CUSTOMER_ID", "type": "Customer", "name": "NAME"},
        "ORDERS":    {"pk": "ORDER_ID", "type": "Order"},
        "PRODUCTS":  {"pk": "PRODUCT_ID", "type": "Product", "name": "TITLE"},
    },
    foreign_keys=[
        {"table": "ORDERS", "column": "CUSTOMER_ID",
         "references": ("CUSTOMERS", "CUSTOMER_ID"), "predicate": "placedBy"},
        # ORDER_ITEMS is a junction table: two foreign keys, no entity
        {"table": "ORDER_ITEMS", "column": "ORDER_ID",
         "references": ("ORDERS", "ORDER_ID")},
        {"table": "ORDER_ITEMS", "column": "PRODUCT_ID",
         "references": ("PRODUCTS", "PRODUCT_ID"), "predicate": "contains"},
    ],
)

mapped = mapper.map(
    {"CUSTOMERS": customers, "ORDERS": orders,
     "PRODUCTS": products, "ORDER_ITEMS": order_items},
    source="snowflake_crm",
)
# mapped["entities"][0] -> {"id": "Customer:42", "type": "Customer", "name": "Acme",
#                           ..., "source": "snowflake_crm",
#                           "metadata": {"source": "snowflake_crm", "table": "CUSTOMERS"}}
# Order -> Customer edges are typed "placedBy"; ORDER_ITEMS rows become Order -> Product "contains" edges

kg = GraphBuilder().build(sources=[mapped])
```

### 构造参数

| 参数 | 说明 |
| :--- | :--- |
| `entity_tables` | `{table: {"pk": 列名或列名列表, "type": 类名, "name": 列名（可选）}}`。`pk` 和 `type` 必填。`name` 指定用作实体显示名的列，默认使用主键值。 |
| `foreign_keys` | 显式外键列表：`[{"table", "column", "references": (table, column), "predicate"（可选）}]`。`predicate` 默认为被引用表的表名。数据仓库中约束仅作参考或缺失时，用它补齐。 |
| `schema` | 带 `foreign_keys` 键的模式 dict，例如 `DBIngestor.analyze_schema()` 的返回值（SQLAlchemy inspector 格式的外键）。只有没被显式外键覆盖的列才会使用这里的外键。约束未记录所属表时，按哪张已映射表包含该列来推断。 |

外键必须引用目标实体表的完整主键，因为实体 ID 来自主键：

- 显式外键引用非主键列、引用复合主键，或引用不在 `entity_tables` 中的表时，构造函数抛出 `ValueError`。
- 来自 `schema` 的此类外键会被跳过并记录一条警告。

### `map(tables, source)`

`tables` 是 `{表名: 行}`，返回 `{"entities": [...], "relationships": [...]}`。每张表的行可以是：

- 行 dict 列表，例如 `DBIngestor.execute_query()` 的返回值
- 带 `.data` 或 `.rows` 的摄取结果（`SnowflakeIngestor`、`DatabricksIngestor`、`DBIngestor`）
- 带 `.dataframe` 的结果（`PandasIngestor`）或 pandas `DataFrame`
- `DBIngestor.ingest_database()["tables"]` 中的 `{"columns", "row_count", "rows"}` dict

`source` 是写入每个实体和关系的来源标签。

以下情况会抛出 `ValueError`：

- 某张表不在 `entity_tables` 中，且外键数量不是两个。
- 某列名与映射器自己设置的键冲突，例如实体表中的 `id`、`type`、`source`、`target`、`subject`、`object`、`metadata`。请在查询中给这些列起别名。

主键为空的行会被跳过。外键值为空时不生成对应的关系。


## 时态知识图谱（v0.4.0+）

<Info>
  `BiTemporalFact`、`TemporalReasoningEngine`、Allen 区间代数(Allen Interval Algebra)和 `TemporalNormalizer` 的完整时态参考，见专门的[时态智能](./temporal.md)页面。本节只记录 KG 层的时态 API。
</Info>

时态技术栈总览见[时态智能](./temporal.md)页面。

### 构建时态图

```python
from semantica.kg import GraphBuilder, TemporalGraphQuery, TemporalVersionManager

builder = GraphBuilder()
kg = builder.build(sources=[
    {
        "entities": [
            {"id": "alice",     "type": "Person"},
            {"id": "acme_corp", "type": "Organization"},
            {"id": "beta_ltd",  "type": "Organization"},
        ],
        "relationships": [
            {
                "source": "alice", "target": "acme_corp", "type": "ceo_of",
                "valid_from":  "2018-01-01",
                "valid_until": "2022-06-01",
            },
            {
                "source": "alice", "target": "beta_ltd", "type": "ceo_of",
                "valid_from":  "2022-06-01",
                # No valid_until → open-ended (TemporalBound.OPEN)
            },
        ],
    }
])
```

### 时间点查询

`TemporalGraphQuery` 的构造参数是可选的；每次调用查询方法时把图传进去：

```python
from semantica.kg import TemporalGraphQuery

query = TemporalGraphQuery(
    temporal_granularity="day",        # second|minute|hour|day|week|month|year
    enable_temporal_reasoning=True,
)

# Primary API: query_at_time returns counts + filtered data
result_2020 = query.query_at_time(kg, "", at_time="2020-06-15")
result_2023 = query.query_at_time(kg, "", at_time="2023-01-01")
print(f"Rels in 2020: {result_2020['num_relationships']}")

# Low-level: reconstruct_at_time returns a deep-copied subgraph dict
snapshot = query.reconstruct_at_time(kg, "2020-06-15")

# Range query: all relationships active during any part of 2021
range_result = query.query_time_range(kg, "", "2021-01-01", "2021-12-31")

# Compare two snapshots: use TemporalVersionManager.compare_versions()
# (temporal_diff() does not exist — see TemporalVersionManager below)
```

### 双时态事实(Bi-Temporal Facts)

`BiTemporalFact` 是 **dataclass**——用 `from_relationship()` 工厂方法，不要用位置参数构造。也就是说，每条事实带两条时间线：它何时在现实中成立，以及这条记录何时录入、何时被取代：

```python
from semantica.kg import BiTemporalFact, TemporalBound

rel = {
    "source": "alice", "target": "acme_corp", "type": "ceo_of",
    "valid_from":    "2018-01-01",
    "valid_until":   "2022-06-01",
    "recorded_at":   "2018-01-05T09:32:00Z",
    "superseded_at": None,   # None → TemporalBound.OPEN (still current)
}
fact = BiTemporalFact.from_relationship(rel)

print(fact.valid_from)      # datetime(2018, 1, 1, tzinfo=utc)
print(fact.valid_until)     # datetime(2022, 6, 1, tzinfo=utc)
print(fact.superseded_at)   # TemporalBound.OPEN

# Open-ended fact (no valid_until → TemporalBound.OPEN)
open_rel = {"source": "alice", "target": "beta_ltd", "type": "ceo_of",
            "valid_from": "2022-06-01"}
open_fact = BiTemporalFact.from_relationship(open_rel)
print(open_fact.valid_until)   # TemporalBound.OPEN

# Serialize back to dict fields for storage
fields = fact.to_relationship_fields()
```

### Allen 区间代数

`TemporalReasoningEngine` 确定性地实现**全部 13 种 Allen 关系**——无 LLM、无概率。说白了，它回答一个问题：任意两个时间段之间是哪种关系——先后、相接、重叠还是包含。具体来说，它只作用于 `TemporalInterval` 对象（不是普通 dict）：

```python
from semantica.kg import (
    TemporalReasoningEngine, TemporalInterval, IntervalRelation
)
from datetime import datetime, timezone

def dt(y, m, d): return datetime(y, m, d, tzinfo=timezone.utc)

engine = TemporalReasoningEngine()

h1_2020 = TemporalInterval(start=dt(2020, 1, 1), end=dt(2020, 6, 30))
q2_q4   = TemporalInterval(start=dt(2020, 4, 1), end=dt(2020, 12, 31))

relation = engine.relation(h1_2020, q2_q4)   # primary method
print(relation)          # IntervalRelation.OVERLAPS
print(relation.value)    # "overlaps"

print(engine.overlaps(h1_2020, q2_q4))  # True
print(engine.contains(q2_q4, h1_2020))  # False
print(engine.active_at(h1_2020, dt(2020, 3, 15)))  # True
```

| `IntervalRelation` | `.value` | 说明 |
| :--- | :--- | :--- |
| `BEFORE` | `"before"` | A 严格结束于 B 开始之前 |
| `MEETS` | `"meets"` | A 结束的时刻恰好是 B 开始的时刻 |
| `OVERLAPS` | `"overlaps"` | A 和 B 有一段重叠；A 先开始也先结束 |
| `STARTS` | `"starts"` | 同时开始；A 先结束 |
| `DURING` | `"during"` | A 完全位于 B 之内 |
| `FINISHES` | `"finishes"` | 同时结束；B 更早开始 |
| `EQUALS` | `"equals"` | 区间完全相同 |
| `AFTER`、`MET_BY`、`OVERLAPPED_BY`、`STARTED_BY`、`CONTAINS`、`FINISHED_BY` | *（逆关系）* | 镜像关系 |

### 自然语言时间解析

```python
from semantica.kg import TemporalNormalizer, TemporalQueryRewriter
from datetime import datetime, timezone

# reference_date set at construction time (required for relative phrases)
norm = TemporalNormalizer(reference_date=datetime(2024, 6, 15, tzinfo=timezone.utc))

# Returns Optional[Tuple[datetime, datetime]] — not a dict
result = norm.normalize("last quarter")
start, end = result
print(start)   # datetime(2024, 1, 1, tzinfo=utc)
print(end)     # datetime(2024, 3, 31, tzinfo=utc)

result = norm.normalize("2022")
# (datetime(2022, 1, 1, tzinfo=utc), datetime(2022, 12, 31, tzinfo=utc))

result = norm.normalize("unparseable phrase")
print(result)  # None

# TemporalQueryRewriter: primary method is rewrite(), returns TemporalQueryResult
rewriter = TemporalQueryRewriter()
result = rewriter.rewrite("Who was CEO before the 2022 restructuring?")
print(result.temporal_intent)    # "before"
print(result.at_time.year)       # 2022
print(result.rewritten_query)    # "Who was CEO"
print(result.confidence)         # 0.85
print(result.has_temporal_context())  # True
```

### 带版本的快照

```python
from semantica.kg import TemporalVersionManager

# In-memory (default); pass storage_path="versions.db" for SQLite persistence
versioner = TemporalVersionManager()

# author and description are required for create_snapshot
versioner.create_snapshot(kg, version_label="2024-Q1",
                          author="user@example.com",
                          description="Q1 2024 baseline")

# List versions (not list_snapshots)
for v in versioner.list_versions():
    print(f"{v['label']:12s}  {v['author']}")

# Compare two versions (not diff_versions)
diff = versioner.compare_versions("2023-Q4", "2024-Q1")
print(f"Entities added:      {diff['summary']['entities_added']}")
print(f"Relationships added: {diff['summary']['relationships_added']}")

# Retrieve a version (not restore_snapshot)
past_kg = versioner.get_version("2023-Q4")

# SHA-256 integrity check
versioner.verify_checksum(past_kg)
```

<Tip>
  完整的类 API、领域示例（人事变动、政策演化、财务时间线）和配置选项，见[时态智能](./temporal.md)参考。
</Tip>


## 相似度打分

`SimilarityCalculator` 计算节点嵌入之间的余弦、欧氏、曼哈顿和相关系数相似度：

```python
from semantica.kg import SimilarityCalculator, NodeEmbedder

# First compute structural embeddings
embedder   = NodeEmbedder(method="node2vec", embedding_dimension=128)
embeddings = embedder.compute_embeddings(kg, ["Person", "Organization"], ["RELATED_TO"])

# Then compare nodes by embedding similarity
calc  = SimilarityCalculator()
score = calc.cosine_similarity(embeddings["Apple Inc."], embeddings["Google"])
print(f"Apple–Google structural similarity: {score:.3f}")

# Find structurally similar nodes: returns List[str] of node IDs
similar = embedder.find_similar_nodes(kg, "Apple Inc.", top_k=5)
for node_id in similar:
    print(node_id)
```


## 图分析

<Tabs>
  <Tab title="中心性">
    用五种算法度量节点重要性。`calculate_all_centrality()` 可以一次全部跑完。

    ```python
    from semantica.kg import CentralityCalculator

    calculator = CentralityCalculator()

    # Run all centrality measures at once
    all_metrics = calculator.calculate_all_centrality(graph)

    # Or run individually
    pagerank    = calculator.calculate_pagerank(graph, damping_factor=0.85)
    betweenness = calculator.calculate_betweenness_centrality(graph)
    closeness   = calculator.calculate_closeness_centrality(graph)

    # Get the top 10 most important nodes
    top_nodes = calculator.get_top_nodes(pagerank, top_k=10)
    ```

    | 方法 | 最适合 |
    | :------ | :-------- |
    | `calculate_degree_centrality()` | 连接数最多的节点 |
    | `calculate_pagerank()` | 基于链接的影响力（类似 Google PageRank） |
    | `calculate_betweenness_centrality()` | 瓶颈/桥接节点 |
    | `calculate_closeness_centrality()` | 离所有其他节点最近的节点 |
    | `calculate_eigenvector_centrality()` | 与其他高影响力节点相连的节点 |
  </Tab>
  <Tab title="社区检测">
    发现图中的簇和社区。Louvain 最快；Leiden 划分质量更高。

    ```python
    from semantica.kg import CommunityDetector

    detector = CommunityDetector()

    # Louvain: fast, high quality (default)
    communities = detector.detect_communities(graph, algorithm="louvain")

    # Leiden: higher quality, slower
    communities = detector.detect_communities_leiden(graph, resolution=1.2)

    # Evaluate community quality
    metrics = detector.calculate_community_metrics(graph, communities)
    print(f"Modularity: {metrics['modularity']:.3f}")
    print(f"Communities found: {metrics['num_communities']}")
    ```

    | 算法 | 强项 |
    | :--------- | :-------- |
    | Louvain | 快，模块度良好：大图用 |
    | Leiden | 模块度最佳：质量优先于速度时用 |
    | 标签传播 | 接近线性时间：超大图用 |
    | K-派系 | 重叠社区：节点可属多个组 |
  </Tab>
  <Tab title="路径查找">
    求任意两节点间的最短路径和备选路径。

    ```python
    from semantica.kg import PathFinder

    finder = PathFinder()

    # Dijkstra shortest path
    path = finder.dijkstra_shortest_path(graph, "Alice", "Bob")
    print(" → ".join(path["path"]))

    # All shortest paths between two nodes
    paths = finder.all_shortest_paths(graph, "source", "target")

    # K-Shortest paths (alternative routes)
    k_paths = finder.find_k_shortest_paths(graph, "source", "target", k=3)
    ```

    | 算法 | 用途 |
    | :--------- | :-------- |
    | Dijkstra | 带权最短路径：标准寻路 |
    | A\* | 启发式引导搜索：大稀疏图上更快 |
    | BFS | 无权最短路径：只数跳数 |
    | K 短路径 | 多条备选路径 |
  </Tab>
  <Tab title="链路预测">
    预测缺失或未来的边。用于补全知识图谱或发现隐含关系。

    ```python
    from semantica.kg import LinkPredictor

    predictor = LinkPredictor(method="preferential_attachment")

    # Predict the top 20 most likely missing edges
    predicted = predictor.predict_links(graph, top_k=20)
    for link in predicted:
        print(f"{link['source']} → {link['target']}  (score: {link['score']:.3f})")

    # Score a specific pair
    score = predictor.score_link(graph, "Alice", "CompanyX")
    ```

    | 算法 | 最适合 |
    | :--------- | :-------- |
    | 优先连接 | 高连接度节点的连边预测 |
    | 共同邻居 | 有共享连接的节点 |
    | Jaccard | 归一化的共同邻居重叠 |
    | Adamic-Adar | 加权共同邻居（惩罚枢纽节点） |
    | 资源分配 | 保守：忽略高度数中介节点 |
  </Tab>
  <Tab title="节点嵌入">
    用 Node2Vec 计算结构化嵌入，然后找相似节点或喂给下游机器学习。

    ```python
    from semantica.kg import NodeEmbedder, SimilarityCalculator

    # Compute Node2Vec embeddings
    embedder = NodeEmbedder(method="node2vec", embedding_dimension=128)
    embeddings = embedder.compute_embeddings(
        graph, ["Person", "Organization"], ["RELATED_TO"]
    )

    # Find structurally similar nodes
    similar = embedder.find_similar_nodes(graph, "Apple Inc.", top_k=5)
    for node_id in similar:
        print(node_id)

    # Compare two specific nodes by embedding similarity
    calc  = SimilarityCalculator()
    score = calc.cosine_similarity(embeddings["Apple Inc."], embeddings["Google"])
    print(f"Structural similarity: {score:.3f}")
    ```

    <Note>
      `find_similar_nodes` 返回 `List[str]`：节点 ID 列表，不是节点对象。完整节点数据要通过 `graph["nodes"]` 查。
    </Note>
  </Tab>
</Tabs>


## 算法总览

| 类别 | 算法 | 用途 |
| :-------- | :---------- | :--------- |
| 节点嵌入 | Node2Vec | 结构相似度、节点表示 |
| 相似度 | 余弦、欧氏、曼哈顿、相关系数 | 节点匹配、推荐 |
| 路径查找 | Dijkstra、A*、BFS、K 短路径 | 路线规划、网络分析 |
| 链路预测 | 优先连接、Jaccard、Adamic-Adar | 网络补全 |
| 中心性 | 度、中介、接近、PageRank | 影响力分析 |
| 社区检测 | Louvain、Leiden、标签传播 | 社群聚类 |
| 连通性 | 分量、桥、密度 | 网络健壮性 |


## GraphValidator

校验图结构：检查必填字段、重复 ID、悬空边，并可选检测环和孤岛节点：

```python
from semantica.kg import GraphValidator

validator = GraphValidator()
result    = validator.validate(kg)   # accepts the dict returned by GraphBuilder.build()

if result.is_valid:
    print("Graph is valid")
else:
    for issue in result.issues:
        print(f"{issue.severity.value}: {issue.message}")
```

传 `strict=True` 把警告当错误。传带 `"entity_types"` 和 `"relationship_types"` 键的 `schema` dict，可按已知类型词表校验。

## 配置

```yaml
kg:
  resolution:
    threshold: 0.9
    strategy: semantic

  temporal:
    enabled: true
    default_validity: infinite
```

- [Graph Store](./graph_store.md) — 把图持久化到 Neo4j、FalkorDB 或 Apache AGE。
- [Semantic Extract](./semantic_extract.md) — GraphBuilder 的实体与关系来源。
- [Visualization](./visualization.md) — 交互式可视化知识图谱。
- [Conflicts](./conflicts.md) — 冲突检测与消解。

### Cookbooks

- [Building Knowledge Graphs](https://github.com/semantica-agi/semantica/blob/main/cookbook/introduction/07_Building_Knowledge_Graphs.ipynb): KG 构建基础 · 入门
- [Your First Knowledge Graph](https://github.com/semantica-agi/semantica/blob/main/cookbook/introduction/08_Your_First_Knowledge_Graph.ipynb): 从实体抽取到可视化 · 入门
- [Graph Analytics](https://github.com/semantica-agi/semantica/blob/main/cookbook/introduction/10_Graph_Analytics.ipynb): 中心性与社区检测 · 进阶
- [Advanced Graph Analytics](https://github.com/semantica-agi/semantica/blob/main/cookbook/advanced/02_Advanced_Graph_Analytics.ipynb): PageRank、Louvain、最短路径 · 高级
- [Temporal Knowledge Graphs](https://github.com/semantica-agi/semantica/blob/main/cookbook/advanced/10_Temporal_Knowledge_Graphs.ipynb): 时态逻辑与图演化 · 高级
