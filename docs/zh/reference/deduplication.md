---
title: "去重模块（Deduplication）"
description: "实体去重：相似度打分、分块(blocking)、合并与基于聚类的批处理。"
source: reference/deduplication.md
source_version: bb514abd19ac1a76ab1b24216be522dde0ded674
icon: "copy"
---

**`semantica.deduplication`** 跨数据源检测并合并重复实体，产出**干净的单一事实来源**知识图谱：

- 四个 v2 策略最高比 v1 快 7 倍：`blocking_v2`、`hybrid_v2`、`semantic_v2`
- `ClusterBuilder` 用 Union-Find 和层次聚类做大规模批量去重
- `EntityMerger` 在每个合并后的实体上保留原始来源溯源
- `MergeStrategyManager` 支持按属性配置规则和冲突消解
- 所有工作流都作用于纯 Python dict：不需要 ORM 或 schema


## 导出的类

| 类 | 职责 |
| :--- | :--- |
| `DuplicateDetector` | 成对与批量检测：返回 `DuplicateCandidate` 或 `DuplicateGroup` 列表 |
| `EntityMerger` | 合并重复组：返回 `List[MergeOperation]` |
| `SimilarityCalculator` | 多因子相似度：字符串、属性、关系与嵌入 |
| `ClusterBuilder` | Union-Find 与层次聚类，支撑大规模批量去重 |
| `MergeStrategy` | 合并策略枚举：`KEEP_FIRST`、`KEEP_LAST`、`KEEP_MOST_COMPLETE`、`KEEP_HIGHEST_CONFIDENCE`、`MERGE_ALL` |
| `PropertyMergeRule` | 保存单属性合并规则的 dataclass：`{property_name, strategy, conflict_resolution, priority}` |
| `MergeStrategyManager` | 管理并应用具名合并策略；接受按属性规则 |
| `detect_duplicates()` | 便捷函数：`detect_duplicates(entities, method="pairwise", similarity_threshold=0.7)` |
| `merge_entities()` | 便捷函数：`merge_entities(entities, method="keep_most_complete")` |
| `calculate_similarity()` | 便捷函数：`calculate_similarity(entity_a, entity_b, method="multi_factor")` |

## 你能得到什么

- **DuplicateDetector** — 成对、批量、增量与分组四种检测模式。返回带原因的打分候选。
- **EntityMerger** — 五种合并策略：保留首个、末个、最完整、置信度最高，或合并全部字段。
- **SimilarityCalculator** — 跨字符串编辑距离、属性重叠、关系重叠与嵌入的多因子打分。
- **ClusterBuilder** — Union-Find 与层次聚类，支撑大规模批量去重：可处理 10 万+ 实体集。
- **MergeStrategyManager** — 按属性配置合并规则，带冲突消解优先级。不同字段可用不同策略。
- **v2 策略** — `blocking_v2`、`hybrid_v2`、`semantic_v2`：大实体集上最高比 v1 快 7 倍。


## 快速开始

```python
from semantica.deduplication import DuplicateDetector, EntityMerger

entities = [
    {"id": "1", "name": "Apple Inc.",   "type": "Company"},
    {"id": "2", "name": "Apple",        "type": "Company"},
    {"id": "3", "name": "Microsoft",    "type": "Company"},
]

# 1. Detect duplicates: returns List[DuplicateCandidate]
detector   = DuplicateDetector(similarity_threshold=0.7)
candidates = detector.detect_duplicates(entities)

for dup in candidates:
    print(
        "{} vs {}: sim: {:.2f}, confidence: {:.2f}".format(
            dup.entity1.get("name"),
            dup.entity2.get("name"),
            dup.similarity_score,
            dup.confidence,
        )
    )

# 2. Merge duplicates: returns List[MergeOperation]
merger     = EntityMerger()
operations = merger.merge_duplicates(entities, strategy="keep_most_complete")

for op in operations:
    print("Merged {} entities → {}".format(
        len(op.source_entities), op.merged_entity.get("name")
    ))
```

<Tip>
  **去重前先规范实体名。** `"Apple Inc."` 与 `"apple inc"` 这样的规范形式，可能仅因大小写差异就低于阈值。先跑 `EntityNormalizer` 或 `TextNormalizer`，匹配才可靠。
</Tip>

## DuplicateDetector

找出重复实体对：

```python
from semantica.deduplication import DuplicateDetector

detector = DuplicateDetector(
    similarity_threshold=0.7,    # default 0.7: minimum score to include a candidate
    confidence_threshold=0.6,    # default 0.6: minimum confidence to include a candidate
    max_results=100,             # optional: hard cap on total candidates returned
    top_k_per_entity=3,          # optional: max candidates per entity
    min_similarity=0.75,         # optional: additional floor applied after sorting
    sort_by="confidence",        # "confidence" (default) | "similarity_score"
)

# Returns List[DuplicateCandidate]
candidates = detector.detect_duplicates(entities)

for c in candidates:
    print(c.entity1.get("name"), "vs", c.entity2.get("name"))
    print("  similarity_score:", c.similarity_score)
    print("  confidence:      ", c.confidence)
    print("  reasons:         ", c.reasons)

# Detect duplicate groups with union-find (returns List[DuplicateGroup])
groups = detector.detect_duplicate_groups(entities)
for g in groups:
    print("Group of {}: confidence: {:.2f}: representative: {}".format(
        len(g.entities), g.confidence, g.representative and g.representative.get("name")
    ))

# Incremental: compare new entities against existing (returns List[DuplicateCandidate])
new_entities = [{"id": "4", "name": "Apple Corp.", "type": "Company"}]
candidates   = detector.incremental_detect(new_entities, entities)
```

<Tip>
  **先调 `similarity_threshold`，再调 `confidence_threshold`。** 相似度阈值决定哪些实体对会被纳入考量，置信度阈值再按多因子打分过滤这些对。从 `similarity_threshold=0.7` 起步，调高它可减少误报。
</Tip>

<Tip>
  **要合并就用 `detect_duplicate_groups()`。** `"group"` 检测策略用 union-find 构成传递闭包簇：A≈B 且 B≈C，三者进同一组。普通 `detect_duplicates()` 只返回单独的对，没有传递性。
</Tip>

### `detect_duplicates()` 的检测方法

`detect_duplicates()` 便捷函数的 `method=` 参数控制比较方式。它与内部使用的 `SimilarityCalculator` 字符串方法相互独立：

| `method=` | 算法 | 返回 |
| :--------- | :--------- | :------- |
| `"pairwise"`（默认） | O(n²) 全对比较 | `List[DuplicateCandidate]` |
| `"batch"` | 批量相似度计算 | `List[DuplicateCandidate]` |
| `"incremental"` | 新实体 vs 已有实体 | `List[DuplicateCandidate]` |
| `"group"` | union-find 分组 | `List[DuplicateGroup]` |

### DuplicateCandidate 字段

| 字段 | 类型 | 说明 |
| :----- | :---- | :----------- |
| `entity1` | `Dict` | 第一个实体 |
| `entity2` | `Dict` | 第二个实体 |
| `similarity_score` | `float` | 相似度得分（0–1） |
| `confidence` | `float` | 置信度得分（0–1） |
| `reasons` | `List[str]` | 判定为重复的原因 |
| `metadata` | `Dict` | 附加元数据 |

<Warning>
  **`DuplicateCandidate` 的字段是 `entity1`、`entity2`、`similarity_score`：不是 `entity_a`、`entity_b`、`similarity`。** 访问错误的字段名会抛 `AttributeError`。
</Warning>

### DuplicateGroup 字段

| 字段 | 类型 | 说明 |
| :----- | :---- | :----------- |
| `entities` | `List[Dict]` | 组内全部实体 |
| `similarity_scores` | `Dict` | 实体对 → 得分映射 |
| `representative` | `Optional[Dict]` | 组内最完整的实体 |
| `confidence` | `float` | 组置信度得分 |
| `metadata` | `Dict` | 附加元数据 |

## EntityMerger

把检测出的重复组合并为规范实体：

```python
from semantica.deduplication import EntityMerger, MergeStrategy

# Basic usage
merger     = EntityMerger(preserve_provenance=True)
operations = merger.merge_duplicates(entities, strategy="keep_most_complete")

# operations is List[MergeOperation]
for op in operations:
    merged = op.merged_entity         # the resulting merged entity dict
    sources = op.source_entities      # list of original entities that were merged
    conflicts = op.merge_result.conflicts  # unresolved conflicts, if any

# Merge a known group directly (no duplicate detection)
pair = [
    {"id": "1", "name": "Apple Inc.", "type": "Company"},
    {"id": "2", "name": "Apple",      "type": "Company"},
]
op = merger.merge_entity_group(pair, strategy="keep_most_complete")
print(op.merged_entity)

# Retrieve full merge history
history = merger.get_merge_history()
print("Total merges performed:", len(history))
```

<Warning>
  **`merge_entities()` 和 `EntityMerger.merge_duplicates()` 返回 `List[MergeOperation]`，不是实体 dict 列表。** 在每个 operation 上访问 `.merged_entity` 才能拿到合并后的 dict。
</Warning>

### 合并策略

作为字符串传给 `merge_duplicates()` 或 `merge_entity_group()` 的 `strategy=`：

| 策略 | 行为 |
| :-------- | :-------- |
| `"keep_first"` | 保留每个重复组中的第一个实体 |
| `"keep_last"` | 保留最近出现的实体 |
| `"keep_most_complete"` | 保留非空属性 + 关系最多的实体 |
| `"keep_highest_confidence"` | 保留 `.confidence` 值最高的实体 |
| `"merge_all"` | 合并全部属性：冲突消解为列表 |

### 按属性的合并规则

按属性规则通过 `add_property_rule()` 设在 `EntityMerger.merge_strategy_manager` 上。规则接受 `MergeStrategy` 枚举值：

```python
from semantica.deduplication import EntityMerger, MergeStrategy

merger = EntityMerger()

# Add per-property rules
merger.merge_strategy_manager.add_property_rule(
    "name", MergeStrategy.KEEP_FIRST
)
merger.merge_strategy_manager.add_property_rule(
    "aliases", MergeStrategy.MERGE_ALL
)

# Custom conflict resolution function
def keep_longest(val1, val2):
    return val1 if len(str(val1)) >= len(str(val2)) else val2

merger.merge_strategy_manager.add_property_rule(
    "description", MergeStrategy.KEEP_FIRST, conflict_resolution=keep_longest
)

operations = merger.merge_duplicates(entities)
```

<Warning>
  **`PropertyMergeRule` 是 dataclass，不是 Enum。** 合并策略枚举是 `MergeStrategy`（`KEEP_FIRST`、`KEEP_LAST`、`KEEP_MOST_COMPLETE`、`KEEP_HIGHEST_CONFIDENCE`、`MERGE_ALL`）。按属性规则要通过 `merger.merge_strategy_manager.add_property_rule(name, strategy)` 添加。
</Warning>

### MergeOperation 字段

| 字段 | 类型 | 说明 |
| :----- | :---- | :----------- |
| `source_entities` | `List[Dict]` | 被合并的原始实体 |
| `merged_entity` | `Dict` | 合并产生的实体 |
| `merge_result` | `MergeResult` | 含冲突的详细结果 |
| `metadata` | `Dict` | 组置信度、相似度得分、所用策略 |

## SimilarityCalculator

计算实体对的多因子相似度得分：

```python
from semantica.deduplication import SimilarityCalculator

calc = SimilarityCalculator(
    string_weight=0.6,        # default 0.6
    property_weight=0.2,      # default 0.2
    relationship_weight=0.2,  # default 0.2
    embedding_weight=0.0,     # default 0.0 (used only when "embedding" key is present)
    similarity_threshold=0.7,
)

result = calc.calculate_similarity(entity_a, entity_b)
# result is a SimilarityResult
print(result.score)                         # overall score 0.0–1.0
print(result.method)                        # e.g. "multi_factor"
print(result.components["string"])          # string similarity component
print(result.components["property"])        # property overlap component
print(result.components["relationship"])    # relationship jaccard component
# result.components["embedding"] is present only when embeddings are supplied

# String similarity methods: method= accepts "levenshtein", "jaro_winkler", "cosine"
lev  = calc.calculate_string_similarity("Apple Inc.", "Apple Inc",  method="levenshtein")
jaro = calc.calculate_string_similarity("Steve Jobs", "Steven Jobs", method="jaro_winkler")
cos  = calc.calculate_string_similarity("apple",     "apples",      method="cosine")

# Embedding cosine similarity (vector inputs)
emb_score = calc.calculate_embedding_similarity(embedding_a, embedding_b)

# Property and relationship similarity (entity dict inputs)
prop_score = calc.calculate_property_similarity(entity_a, entity_b)
rel_score  = calc.calculate_relationship_similarity(entity_a, entity_b)
```

### SimilarityResult 字段

| 字段 | 类型 | 说明 |
| :----- | :---- | :----------- |
| `score` | `float` | 加权总相似度得分（0–1） |
| `method` | `str` | 所用方法（如 `"multi_factor"`、`"levenshtein"`） |
| `components` | `Dict[str, float]` | 分项得分：`"string"`、`"property"`、`"relationship"`、`"embedding"` |
| `metadata` | `Dict` | 所用权重与可选的得分明细 |

## ClusterBuilder

为大规模批量去重构建实体簇：

```python
from semantica.deduplication import ClusterBuilder

builder = ClusterBuilder(
    similarity_threshold=0.8,  # minimum similarity to be in same cluster
    min_cluster_size=2,         # minimum entities per valid cluster
    max_cluster_size=100,       # maximum entities per cluster
    use_hierarchical=False,     # True for hierarchical, False (default) for union-find
)
result = builder.build_clusters(entities)

print("Clusters found:", len(result.clusters))
for cluster in result.clusters:
    print("  [{}] {} entities: quality: {:.2f}".format(
        cluster.cluster_id,
        len(cluster.entities),
        cluster.quality_score,
    ))

print("Unclustered:   ", len(result.unclustered))
print("Quality metrics:", result.quality_metrics)
# {"average_size": ..., "average_quality": ..., "total_clusters": ..., "high_quality_clusters": ...}
```

### Cluster 字段

| 字段 | 类型 | 说明 |
| :----- | :---- | :----------- |
| `cluster_id` | `str` | 簇的唯一标识 |
| `entities` | `List[Dict]` | 簇内实体 |
| `centroid` | `Optional[Dict]` | 代表实体（可选） |
| `quality_score` | `float` | 簇内平均相似度 |
| `metadata` | `Dict` | 相似度得分等元数据 |

## 便捷函数

```python
from semantica.deduplication import detect_duplicates, merge_entities, calculate_similarity

# Detect: method= accepts "pairwise" (default), "batch", "incremental", "group"
candidates = detect_duplicates(
    entities,
    method="pairwise",
    similarity_threshold=0.8,
    confidence_threshold=0.6,
)

# Merge: method= accepts the strategy strings, same as EntityMerger
operations = merge_entities(entities, method="keep_most_complete", preserve_provenance=True)
# Returns List[MergeOperation]; access .merged_entity on each

# Similarity: method= accepts "exact", "levenshtein", "jaro_winkler", "cosine",
#              "property", "relationship", "embedding", "multi_factor" (default)
result = calculate_similarity(entity_a, entity_b, method="multi_factor")
print(result.score)
```

## 自定义相似度函数

注册领域专属的相似度逻辑，经方法注册表调用：

```python
from semantica.deduplication import method_registry, SimilarityResult

def drug_name_similarity(entity_a, entity_b, **kwargs):
    """Match drug names by active compound prefix."""
    name_a = entity_a.get("name", "").lower()
    name_b = entity_b.get("name", "").lower()
    score = 1.0 if name_a[:5] == name_b[:5] else 0.0
    return SimilarityResult(score=score, method="drug_name")

method_registry.register("similarity", "drug_name", drug_name_similarity)

# Now callable via calculate_similarity
from semantica.deduplication import calculate_similarity
result = calculate_similarity(entity_a, entity_b, method="drug_name")
```

## 常见工作流

<Tabs>
  <Tab title="基础去重">
    ```python
    from semantica.deduplication import DuplicateDetector, EntityMerger

    detector   = DuplicateDetector(similarity_threshold=0.8)
    candidates = detector.detect_duplicates(entities)

    print("Duplicate pairs found:", len(candidates))

    merger     = EntityMerger(preserve_provenance=True)
    operations = merger.merge_duplicates(entities, strategy="keep_most_complete")

    merged_entities = [op.merged_entity for op in operations]
    ```
  </Tab>
  <Tab title="基于分组的批量处理">
    ```python
    from semantica.deduplication import DuplicateDetector, EntityMerger

    detector = DuplicateDetector(similarity_threshold=0.75)
    # detect_duplicate_groups uses union-find internally
    groups   = detector.detect_duplicate_groups(entities)

    merger = EntityMerger()
    for group in groups:
        op = merger.merge_entity_group(group.entities, strategy="keep_most_complete")
        print("Merged into:", op.merged_entity.get("name"))
    ```
  </Tab>
  <Tab title="大规模聚类">
    ```python
    from semantica.deduplication import ClusterBuilder, EntityMerger

    # Build clusters first: more efficient for large entity sets
    builder = ClusterBuilder(similarity_threshold=0.8, min_cluster_size=2)
    result  = builder.build_clusters(entities)

    merger = EntityMerger()
    for cluster in result.clusters:
        op = merger.merge_entity_group(cluster.entities, strategy="keep_most_complete")
        print("Cluster merged into:", op.merged_entity.get("name"))
    ```
  </Tab>
  <Tab title="增量去重">
    ```python
    from semantica.deduplication import EntityMerger

    existing_entities = [...]  # already in the graph
    new_entities      = [...]  # arriving in a batch

    merger     = EntityMerger()
    operations = merger.incremental_merge(new_entities, existing_entities)

    print("New merges performed:", len(operations))
    ```
  </Tab>
</Tabs>

- [Conflicts](./conflicts.md) — 检测非重复实体之间的值冲突。
- [Knowledge Graph](../../reference/kg.md) — GraphBuilder 构建过程中会使用去重。
- [Normalize](./normalize.md) — 去重前先规范实体名。
- [Provenance](../../reference/provenance.md) — 追踪合并实体的谱系。
