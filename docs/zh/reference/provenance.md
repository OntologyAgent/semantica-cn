---
title: "溯源模块（Provenance）"
description: "W3C PROV-O 谱系追踪、来源归属、防篡改校验和与跨模块审计轨迹。"
source: reference/provenance.md
source_version: edbc8026255b147c6ef2f26e88f97e081bbf2463
icon: "link"
---

`semantica.provenance` 追踪每条事实的完整谱系(lineage)：从原始摄取，到抽取、分块、关系构建：

- 符合 W3C PROV-O：可用于 HIPAA、SOX、GDPR、FDA 21 CFR Part 11 审计轨迹
- 每条存储的 `ProvenanceEntry` 都带 SHA-256 校验和(checksum)，可检测篡改
- `SQLiteStorage` 持久化、跨重启保留；`InMemoryStorage` 适合开发
- `ProvenanceManager` 提供 `track_entity`、`track_relationship`、`track_chunk` 和 `get_lineage`
- 经 `BridgeAxiom` 桥接 W3C PROV-O 本体，支持语义网导出


## 导出的类

| 类 | 职责 |
| :--- | :--- |
| `ProvenanceManager` | 中央追踪器：`track_entity`、`track_relationship`、`track_chunk`、`get_lineage`、`get_statistics` |
| `ProvenanceEntry` | 单条谱系记录：`{entity_id, entity_type, activity_id, source_document, confidence, checksum, ...}` |
| `SourceReference` | 富来源指针：`{document, page, section, line, confidence, metadata}` |
| `ProvenanceStorage` | 抽象存储接口 |
| `InMemoryStorage` | 默认后端：快，但重启后不保留 |
| `SQLiteStorage` | 持久后端：写入本地 SQLite 文件 |
| `compute_checksum` | 返回 `ProvenanceEntry` 的 SHA-256 指纹 |
| `verify_checksum` | 比较存储哈希与重算哈希，检测篡改 |

## 快速开始

<Tabs>
  <Tab title="In-Memory（默认）">
    零配置：快，不写磁盘。适合笔记本环境、测试和单次运行脚本。

    ```python
    from semantica.provenance import ProvenanceManager, compute_checksum, verify_checksum

    manager = ProvenanceManager()   # InMemoryStorage by default

    entry = manager.track_entity(
        entity_id="apple_inc",
        source="annual_report_2023.pdf",
        source_location="Page 12, Section 3.1",
        source_quote="Apple Inc. was incorporated on January 3, 1977.",
        confidence=0.98,
    )

    print(entry.checksum)        # SHA-256 hex auto-computed
    print(verify_checksum(entry))  # True: tamper detection
    ```

    <Note>
      进程退出后内存存储即丢失。需要跨重启保留的数据用 `SQLiteStorage`。
    </Note>
  </Tab>
  <Tab title="SQLite（持久）">
    溯源持久化到本地 SQLite 文件。适合生产流水线和审计轨迹。

    ```python
    from semantica.provenance import ProvenanceManager, SQLiteStorage

    # Option 1: explicit storage instance
    manager = ProvenanceManager(storage=SQLiteStorage("provenance.db"))

    # Option 2: shorthand: equivalent to above
    manager = ProvenanceManager(storage_path="provenance.db")

    entry = manager.track_entity(
        entity_id="apple_inc",
        source="annual_report_2023.pdf",
        source_location="Page 12, Section 3.1",
        confidence=0.98,
    )

    # Retrieve lineage after restart: entries persist in provenance.db
    lineage = manager.get_lineage("apple_inc")
    print(f"{len(lineage)} provenance entries for apple_inc")
    ```

    <Check>
      SQLite 文件在首次写入时自动创建，无需任何 schema 设置。
    </Check>
  </Tab>
</Tabs>

## ProvenanceManager

**`ProvenanceManager`** 是所有谱系数据的中央追踪器。每次调用 `track_entity`、`track_relationship` 或 `track_chunk` 都会自动计算并存储**SHA-256 校验和**用于防篡改。

### 构造参数

```python
ProvenanceManager(
    storage=None,        # ProvenanceStorage instance; defaults to InMemoryStorage
    storage_path=None,   # str path: creates SQLiteStorage if provided
)
```

`storage` 和 `storage_path` 都不传时，使用 `InMemoryStorage`。

<Warning>
  **`InMemoryStorage` 重启后不保留。** 任何要求审计轨迹跨进程退出存活的场景，都要传 `storage_path="provenance.db"` 或显式的 `SQLiteStorage` 实例。
</Warning>

### 追踪方法

```python
from semantica.provenance import ProvenanceManager, SourceReference

manager = ProvenanceManager()

# Track an entity
entry = manager.track_entity(
    entity_id="apple_inc",        # required
    source="annual_report.pdf",   # required: document ID, DOI, file path
    source_location="Page 12",    # optional kwarg
    source_quote="Incorporated on January 3, 1977.",  # optional kwarg
    confidence=0.98,              # optional kwarg, default 1.0
    entity_type="organization",   # optional kwarg, default "entity"
    metadata={"sector": "tech"},  # optional metadata dict
)

# Track a relationship
rel_entry = manager.track_relationship(
    relationship_id="jobs_founded_apple",
    source="annual_report.pdf",
    confidence=0.95,
    metadata={"type": "founded"},
)

# Track a document chunk (after splitting)
chunk_entry = manager.track_chunk(
    chunk_id="chunk_001",
    source_document="report.pdf",
    source_path="/docs/report.pdf",
    start_index=0,
    end_index=500,
    parent_chunk_id=None,
)

# Track a property with a SourceReference
source_ref = SourceReference(
    document="DOI:10.1038/s41586-021-03371-z",
    page=4,
    section="Table S4",
    confidence=0.92,
)
prop_entry = manager.track_property_source(
    entity_id="cabo_pulmo",
    property_name="biomass_increase",
    value="463%",
    source=source_ref,
)
```

### 批量追踪

批量追踪方法按块处理条目（默认 `batch_size=1000`），每块共用一个事务。只有成功提交到存储的实体或分块才计入返回数量，回滚的条目不会虚增成功计数。

```python
entities = [
    {"id": "entity_1", "confidence": 0.9},
    {"id": "entity_2", "confidence": 0.85},
]
count = manager.track_entities_batch(entities, source="doc_1")
# Returns the number of entities successfully tracked and committed

chunks = [
    {"id": "chunk_0", "start_index": 0, "end_index": 500},
    {"id": "chunk_1", "start_index": 500, "end_index": 1000},
]
count = manager.track_chunks_batch(chunks, source_document="doc_1")
```

### 检索谱系

```python
# get_lineage returns a dict: not a ProvenanceEntry
lineage = manager.get_lineage("apple_inc")

print(lineage["entity_id"])        # "apple_inc"
print(lineage["source_documents"]) # ["annual_report.pdf"]
print(lineage["first_seen"])       # ISO timestamp string
print(lineage["last_updated"])     # ISO timestamp string
print(lineage["entity_count"])     # number of entries in chain
print(lineage["lineage_chain"])    # list of entry dicts (full history)
print(lineage["metadata"])         # merged metadata dict

# trace_lineage returns the raw ProvenanceEntry objects
entries = manager.trace_lineage("apple_inc")
for entry in entries:
    print(entry.entity_id, entry.source_document, entry.confidence)

# get_all_sources returns a list of source dicts
sources = manager.get_all_sources("apple_inc")
for s in sources:
    print(s["source"], s["location"], s["confidence"])

# get_provenance returns the most recent entry as a dict (or None)
prov = manager.get_provenance("apple_inc")
if prov:
    print(prov["source_document"])
```

<Note>
  `get_lineage()` 返回聚合后的 **dict**，不是 `ProvenanceEntry`。需要字段级访问（如 `entry.checksum`）时，用 `trace_lineage()` 拿原始 `ProvenanceEntry` 对象。
</Note>

### 工具方法

```python
# Statistics about all tracked entries
stats = manager.get_statistics()
# {"total_entries": 42, "entity_types": {"entity": 30, "chunk": 12}, "unique_sources": 5}

# Clear all provenance data; returns count of cleared entries
cleared = manager.clear()
```

### ProvenanceManager 方法参考

| 方法 | 返回 | 说明 |
| :------ | :------- | :----------- |
| `track_entity(entity_id, source, metadata, **kwargs)` | `Optional[ProvenanceEntry]` | 原子化记录实体溯源；成功返回 `ProvenanceEntry`，存储失败返回 `None` 或已有条目 |
| `track_relationship(relationship_id, source, metadata, **kwargs)` | `Optional[ProvenanceEntry]` | 记录关系溯源；成功返回 `ProvenanceEntry`，存储失败返回 `None` |
| `track_chunk(chunk_id, source_document, ...)` | `Optional[ProvenanceEntry]` | 记录带字符偏移的分块溯源；成功返回 `ProvenanceEntry`，存储失败返回 `None` |
| `track_property_source(entity_id, property_name, value, source)` | `Optional[ProvenanceEntry]` | 记录属性级来源归属；成功返回 `ProvenanceEntry`，存储失败返回 `None` |
| `track_entities_batch(entities, source)` | `int` | 批量追踪实体，返回成功计数 |
| `track_chunks_batch(chunks, source_document)` | `int` | 批量追踪分块，返回成功计数 |
| `get_lineage(entity_id)` | `Dict[str, Any]` | 以聚合 dict 返回完整谱系 |
| `trace_lineage(entity_id)` | `List[ProvenanceEntry]` | 以原始 `ProvenanceEntry` 对象返回完整谱系 |
| `get_all_sources(entity_id)` | `List[Dict]` | 实体的全部来源文档 |
| `get_provenance(entity_id)` | `Dict \| None` | 以 dict 返回最近一条溯源条目 |
| `get_statistics()` | `Dict[str, Any]` | 按类型统计条目数和唯一来源数 |
| `clear()` | `int` | 清空全部记录，返回清除数量 |

## ProvenanceEntry 字段

`ProvenanceEntry` 是核心 dataclass。所有追踪方法成功时都返回它（存储失败返回 `None`）：

```python
from semantica.provenance import ProvenanceEntry

# All fields with their types and defaults
entry = ProvenanceEntry(
    entity_id="entity_001",           # str: required
    entity_type="entity",             # str: required (entity, chunk, relationship, property)
    activity_id="ner_extraction",     # str: required
    agent_id="semantica",             # str: default "semantica"
    source_document="report.pdf",     # str: default ""
    source_location="Page 4",         # Optional[str]: default None
    source_quote="Relevant text...",  # Optional[str]: default None
    timestamp="2024-01-01T12:00:00+00:00",  # str: auto-set to utc_now_iso()
    first_seen=None,                  # Optional[str]: ISO timestamp
    last_updated=None,                # Optional[str]: ISO timestamp
    confidence=0.9,                   # float: default 1.0
    checksum=None,                    # Optional[str]: set by compute_checksum()
    parent_entity_id=None,            # Optional[str]: prov:wasDerivedFrom
    used_entities=[],                 # List[str]: prov:used
    start_index=None,                 # Optional[int]: for chunks
    end_index=None,                   # Optional[int]: for chunks
    credibility=None,                 # Optional[float]: source credibility
    metadata={},                      # Dict[str, Any]
    version="1.0",                    # str
)

# Convert to dict
d = entry.to_dict()

# Reconstruct from dict
entry2 = ProvenanceEntry.from_dict(d)
```

## SourceReference 字段

`SourceReference` 提供指向源文档内某处位置的可引用指针：

```python
from semantica.provenance import SourceReference

ref = SourceReference(
    document="DOI:10.1038/s41586-021-03371-z",  # str: required (DOI, URL, file path)
    page=4,                                       # Optional[int]
    section="Table S4",                           # Optional[str]
    line=None,                                    # Optional[int]
    timestamp=None,                               # Optional[datetime]
    confidence=0.92,                              # float: default 1.0
    metadata={"credibility": "peer-reviewed"},    # Dict[str, Any]
)

# Use with track_property_source
manager.track_property_source(
    entity_id="cabo_pulmo",
    property_name="biomass_increase",
    value="463%",
    source=ref,
)
```

## 存储后端

### InMemoryStorage

快，不持久化。适合开发、测试和短生命周期进程：

```python
from semantica.provenance import InMemoryStorage, ProvenanceManager

manager = ProvenanceManager(storage=InMemoryStorage())
```

### SQLiteStorage

持久化到磁盘。适合生产、审计轨迹和监管合规：

```python
from semantica.provenance import SQLiteStorage, ProvenanceManager

manager = ProvenanceManager(storage=SQLiteStorage("provenance.db"))

# Or use the shorthand
manager = ProvenanceManager(storage_path="provenance.db")
```

`SQLiteStorage` 在首次使用时自动建库建索引。

- **原子性与并发**：配置预写日志(`PRAGMA journal_mode=WAL`)、`PRAGMA busy_timeout=5000` 和 `PRAGMA synchronous=NORMAL`。读-改-写方法（`track_entity()`、`store()`）打开单个连接，在立即写事务(`BEGIN IMMEDIATE`)内执行，保证这些序列在并发连接间串行化，且调用之间不留打开的文件句柄。普通读取（`retrieve()`、`trace_lineage()`）使用独立连接、不加显式写锁，并发读不会排在写入者或彼此之后。
- **向后兼容**：覆写 `trace_lineage(self, entity_id)` 的自定义存储子类保持兼容；`ProvenanceManager` 检查覆写签名，若不支持 `max_depth` 就自动按单参数调用。

## 防篡改校验和

`compute_checksum` 和 `verify_checksum` 被 `track_entity` 等全部追踪方法自动使用。也可以直接调用：

```python
from semantica.provenance import compute_checksum, verify_checksum

entry = manager.trace_lineage("apple_inc")[0]

# Recompute checksum from entry fields
checksum = compute_checksum(entry)

# Verify using stored checksum (entry.checksum)
is_valid = verify_checksum(entry)

# Or verify against a separately stored expected checksum
is_valid = verify_checksum(entry, expected_checksum=checksum)

if not is_valid:
    raise RuntimeError("Provenance record has been tampered with.")
```

校验和覆盖 `entity_id`、`entity_type`、`activity_id`、`source_document`、`timestamp` 和 `confidence`。

<Tip>
  **任何合规导出前先跑 `verify_checksum(entry)`。** 直接传 `trace_lineage()` 返回的 `ProvenanceEntry` 对象。存储的校验和若已对不上，导出进行前先抛错。
</Tip>

## Bridge Axiom 翻译链

`BridgeAxiom` 和 `TranslationChain` 位于 `semantica.provenance.bridge_axiom`，用于带完整系数归属的多层领域翻译追踪：

```python
from semantica.provenance.bridge_axiom import BridgeAxiom, create_translation_chain
from semantica.provenance import ProvenanceManager

manager = ProvenanceManager()

# Define a bridge axiom with DOI-backed coefficient
axiom = BridgeAxiom(
    axiom_id="BA-001",
    name="biomass_tourism_elasticity",
    rule="1% biomass increase -> 0.346% tourism revenue increase",
    coefficient=0.346,
    source_doi="10.1038/s41586-021-03371-z",
    source_page="Table S4",
    confidence=0.92,
    input_domain="ecological",
    output_domain="financial",
)

# Apply to a value with provenance tracking
result = axiom.apply(
    input_entity="cabo_pulmo_biomass",
    input_value=463.0,
    prov_manager=manager,
)
print(result["output_value"])  # 463.0 * 0.346 = 160.098

# Build a multi-step translation chain
input_data = {"entity_id": "cabo_pulmo", "value": 463.0, "source": "DOI:10.1371/..."}
chain = create_translation_chain(input_data, [axiom], prov_manager=manager)
print(chain.confidence)  # 0.92
```

## 与 GraphBuilder 集成

`GraphBuilderWithProvenance`（来自 `semantica.kg`）自动为每个节点和边记录溯源：

```python
from semantica.kg import GraphBuilderWithProvenance
from semantica.provenance import ProvenanceManager, SQLiteStorage

prov_manager = ProvenanceManager(storage=SQLiteStorage("provenance.db"))
builder = GraphBuilderWithProvenance(provenance_manager=prov_manager)
kg = builder.build_single_source(graph_data)

# Retrieve lineage: get_lineage returns a dict
lineage = prov_manager.get_lineage("apple_inc")
print(lineage["source_documents"])  # list of source document IDs
print(lineage["first_seen"])        # ISO timestamp
```

## 与 NERExtractor 集成

`NERExtractor` 和其他抽取器接受 `provenance=True`，把溯源元数据嵌入每个抽取出的实体。结果需要你用 `ProvenanceManager` 手动追踪：

```python
from semantica.semantic_extract import NERExtractor
from semantica.provenance import ProvenanceManager

manager = ProvenanceManager()

ner = NERExtractor(method="ml", provenance=True)
entities = ner.extract("Steve Jobs founded Apple Inc.")

# Track each extracted entity manually
for entity in entities:
    manager.track_entity(
        entity_id=entity.id,
        source="source_document.txt",
        confidence=entity.confidence,
        entity_type=entity.type,
    )

# Now retrieve lineage
lineage = manager.get_lineage(entities[0].id)
print(lineage["source_documents"])
```

<Note>
  给 `NERExtractor` 设 `provenance=True` 只是把元数据嵌到抽取出的实体对象上——不会自动调用 `ProvenanceManager.track_entity()`。抽取后必须自己调用 `track_entity()`。
</Note>

## 常见工作流

<Tabs>
  <Tab title="Entity Tracking">
    ```python
    from semantica.provenance import ProvenanceManager

    manager = ProvenanceManager(storage_path="provenance.db")

    # Track an entity extracted from a document
    entry = manager.track_entity(
        entity_id="entity_001",
        source="report_2024.pdf",
        source_location="Page 5",
        source_quote="Revenue grew 12% year-over-year.",
        confidence=0.95,
    )
    # entry.checksum is set automatically

    # Retrieve full lineage
    lineage = manager.get_lineage("entity_001")
    print(lineage["source_documents"])
    ```
  </Tab>
  <Tab title="Chunk Tracking">
    ```python
    from semantica.provenance import ProvenanceManager

    manager = ProvenanceManager()

    # Track chunks produced by the split module
    manager.track_chunk(
        chunk_id="chunk_0001",
        source_document="report.pdf",
        start_index=0,
        end_index=512,
    )

    # Batch-track all chunks at once
    chunks = [
        {"id": "c0", "start_index": 0,   "end_index": 512},
        {"id": "c1", "start_index": 512, "end_index": 1024},
    ]
    count = manager.track_chunks_batch(chunks, source_document="report.pdf")
    ```
  </Tab>
  <Tab title="Integrity Check">
    ```python
    from semantica.provenance import (
        ProvenanceManager, compute_checksum, verify_checksum
    )

    manager = ProvenanceManager(storage_path="provenance.db")
    manager.track_entity("e1", source="doc.pdf", confidence=0.9)

    entries = manager.trace_lineage("e1")
    entry = entries[0]

    # Verify the stored checksum is still valid
    if not verify_checksum(entry):
        raise RuntimeError("Provenance tampered: " + entry.entity_id)
    ```
  </Tab>
</Tabs>

## 合规说明

Semantica 的溯源追踪产出以下审计工件：

| 标准 | 提供能力 |
| :-------- | :--------- |
| **W3C PROV-O** | 合规数据模型；`to_dict()` 与 `from_dict()` 用于序列化 |
| **HIPAA** | 审计轨迹：实体 → 来源文档 → 时间戳 → 置信度 |
| **SOX** | 防篡改校验和；每条条目带时间戳 |
| **GDPR** | 谱系图支持数据删除影响分析 |
| **FDA 21 CFR Part 11** | 带 `timestamp`、`agent_id`、`activity_id`、`checksum` 的电子记录 |

<Note>
  `ProvenanceManager` 不内置 Turtle 或 JSON-LD 序列化。需要 W3C PROV-O RDF 输出时，用 `entry.to_dict()` 和 `get_lineage()` 取回溯源数据，再用你偏好的 RDF 库序列化。
</Note>

- [Change Management](./change_management.md) — 版本控制与快照审计轨迹。
- [Ingest](./ingest.md) — 溯源从摄取阶段就开始。
- [Export](./export.md) — RDF 导出中携带溯源元数据。
- [Context](./context.md) — 经 AgentContext 记录决策溯源。
