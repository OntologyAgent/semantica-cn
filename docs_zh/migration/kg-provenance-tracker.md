---
title: 从 kg.ProvenanceTracker 迁移
description: 如何从已废弃的 semantica.kg.ProvenanceTracker 迁移到统一的 semantica.provenance.ProvenanceManager。
source: migration/kg-provenance-tracker.md
source_version: 496f5b136b97167c0974bd31f1884fa8ec65d22b
---

## 为什么要迁移

`semantica.kg.ProvenanceTracker` 已废弃，将在未来的主版本中移除。它是一个独立的纯内存实现，从未把工作委托给统一的溯源后端——`semantica.provenance.ProvenanceManager` 正是这个后端，如今是在所有 Semantica 模块中追踪实体与关系溯源的受支持方式（见[溯源与审计轨迹指南](../guides/provenance.md)）。

现在 `kg.ProvenanceTracker` 的每个方法在调用时都会发出 `DeprecationWarning`，但在这个类移除之前，现有代码无需任何改动即可继续运行——目前还没有强制的迁移截止日期。

## 方法对照

| `kg.ProvenanceTracker` | `ProvenanceManager` 对应方法 | 说明 |
| --- | --- | --- |
| `ProvenanceTracker()` | `ProvenanceManager()` | `ProvenanceManager` 还接受 `storage_path=`，用 SQLite 持久化，而不是只有内存。 |
| `track_entity(entity_id, source, metadata)` | `track_entity(entity_id, source, metadata)` | 调用形式相同。`ProvenanceManager` 还会通过 `parent_entity_id` 自动把每次更新与它的上一版关联起来。 |
| `get_all_sources(entity_id)` | `get_all_sources(entity_id)` | 字段名不同：`kg` 追踪器把每条记录的时间放在 `"recorded_at"` 里；`ProvenanceManager` 返回的是 `"timestamp"`。 |
| `clear(entity_id=None)` | `clear()` | `ProvenanceManager.clear()` 会清空全部溯源数据；目前还不支持按实体清空。 |
| `query_recorded_between(start, end)` | `query_recorded_between(start, end)` | 调用形式相同；按 `timestamp`（ISO 8601 字符串比较）过滤，作用于所有被追踪的条目，而非单个实体。 |
| `revision_history(fact_id)` | `revision_history(fact_id)` | 调用形式与返回结构都相同（`version`、`valid_from`、`valid_until`、`recorded_at`、`author`，以及可选的 `revision_type`/`supersedes`）——但它沿实体的 `previous_version_id` 链遍历，而不是查扁平的按实体字典。 |
| `export_audit_log(fact_ids, format)` | *暂无直接对应方法* | 基于 `get_lineage()` 的输出自行组装导出，或序列化 `get_statistics()` 得到汇总视图。 |

没有直接对应方法的功能，不计划在 `kg.ProvenanceTracker` 上重新实现——你需要在调用方代码里写个小适配器，或者（如果重度依赖）向 `ProvenanceManager` 提功能请求。

## 示例

```python
# Before
from semantica.kg import ProvenanceTracker

tracker = ProvenanceTracker()
tracker.track_entity("entity_1", source="doc_1", metadata={"confidence": 0.9})
sources = tracker.get_all_sources("entity_1")  # [{"source": ..., "recorded_at": ..., "confidence": 0.9}]

# After
from semantica.provenance import ProvenanceManager

prov = ProvenanceManager()
prov.track_entity("entity_1", source="doc_1", metadata={"confidence": 0.9})
sources = prov.get_all_sources("entity_1")  # [{"source": ..., "timestamp": ..., "metadata": {...}, ...}]
```

## 迁移期间抑制告警

如果迁移规划期间还需要临时使用 `kg.ProvenanceTracker`，又想压掉这条告警：

```python
import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore", DeprecationWarning)
    tracker = ProvenanceTracker()
```

这只是权宜之计，不是解决办法——务必赶在 `kg.ProvenanceTracker` 移除之前完成向 `ProvenanceManager` 的迁移。
