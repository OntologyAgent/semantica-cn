---
title: "变更管理模块（Change Management）"
description: "面向知识图谱与本体的版本控制、SHA-256 校验和、差异分析、回滚与审计轨迹。"
source: reference/change_management.md
source_version: 4268fe34a779313982224ba8bae716d46dfd140d
icon: "clock-rotate-left"
---

说白了，这个模块给图加了一套"存档 + 防篡改"机制：随时拍快照，每个快照带指纹，需要时回滚到任意时点。**`semantica.change_management`** 为知识图谱(Knowledge Graph)和本体(Ontology)提供**版本控制与审计轨迹(Audit Trail)**：

- 每个快照都带 SHA-256 校验和：无需外部基础设施即可检测篡改
- 任意两个版本之间的结构化差异：节点的新增、删除和修改
- 完整回滚到任意命名快照
- 按实体的变更历史，支撑审计轨迹查询
- 支持的合规框架：HIPAA、SOX、GDPR、FDA 21 CFR Part 11

<Note>
  开箱即用的合规框架：**HIPAA**、**SOX**、**GDPR** 和 **FDA 21 CFR Part 11**。
</Note>


## 导出的类

| 类 | 职责 |
| :--- | :--- |
| `TemporalVersionManager` | KG 的快照、差异、回滚与按节点变更历史 |
| `OntologyVersionManager` | 本体 schema 版本控制，支持结构化差异 |
| `InMemoryVersionStorage` | 开发测试用的内存存储：不持久化 |
| `SQLiteVersionStorage` | 生产存储：持久化到本地 SQLite 文件 |
| `compute_checksum()` | 返回任意 dict（图快照、本体快照）的 SHA-256 指纹 |
| `verify_checksum()` | 重算并比对快照 dict 内存储的校验和，检测篡改 |

## 你能得到什么

- **TemporalVersionManager**：知识图谱的快照、差异、回滚与按实体审计轨迹。
- **OntologyVersionManager**：OWL 本体的版本控制，带差异与 schema 迁移支持。
- **VersionStorage**：可插拔后端，测试用 `InMemoryVersionStorage`，生产用 `SQLiteVersionStorage`。
- **完整性校验**：每个快照都带 SHA-256 校验和，检测任何未经授权的修改。
- **ChangeLogEntry**：快照内部元数据，带 ISO 8601 时间戳、邮箱作者与描述校验（最长 500 字符）。
- **版本历史**：经 `list_versions()` 与 `diff()` 提供完整防篡改版本历史，供监管审查。

## 典型工作流

<Steps>
  <Step title="初始化版本管理器">
    ```python
    from semantica.change_management import TemporalVersionManager

    manager = TemporalVersionManager(storage_path="versions.db")
    ```
  </Step>
  <Step title="破坏性操作前先打快照">
    ```python
    snapshot = manager.create_snapshot(
        graph=kg,
        version_label="v1.0",
        author="user@example.com",
        description="Before deduplication run"
    )
    print("Snapshot label:", snapshot["label"])
    print("Checksum:", snapshot["checksum"])
    ```
  </Step>
  <Step title="执行你的变更">
    运行去重、冲突消解、合并或任何图修改。不过要注意，版本管理器不会自动跟踪任何东西：何时打快照完全由你决定。
  </Step>
  <Step title="给结果打快照">
    ```python
    snapshot_v2 = manager.create_snapshot(
        graph=kg,
        version_label="v2.0",
        author="user@example.com",
        description="After deduplication: 1 342 duplicates merged"
    )
    ```
  </Step>
  <Step title="diff 审查变更内容">
    ```python
    diff = manager.diff("v1.0", "v2.0")
    summary = diff["summary"]
    print("Entities added:   ", summary["entities_added"])
    print("Entities removed: ", summary["entities_removed"])
    print("Entities modified:", summary["entities_modified"])
    ```
  </Step>
</Steps>

<Warning>
  **破坏性操作前先打快照。**运行去重、冲突消解或合并操作前，先调 `manager.create_snapshot()`。也就是说，变更前必须有快照，`restore_snapshot()` 才有得回。
</Warning>

## TemporalVersionManager

知识图谱的版本控制：快照、差异与回滚。

### 构造参数

| 参数 | 类型 | 默认值 | 说明 |
| :--------- | :---- | :------- | :----------- |
| `storage_path` | `str` | `None` | SQLite 数据库路径；省略时用内存存储 |

### 列出与取回

```python
# List all versions: returns List[Dict] with label, author, timestamp, checksum, entity_count
versions = manager.list_versions()
for v in versions:
    print(v["label"], "|", v["author"], "|", v["timestamp"], "|", v["checksum"][:8], "...")

# Retrieve a specific version (returns full snapshot dict)
snapshot = manager.get_version("v1.0")
```

### TemporalVersionManager 方法

| 方法 | 返回 | 说明 |
| :------ | :------- | :----------- |
| `create_snapshot(graph, version_label, author, description)` | `Dict[str, Any]` | 创建版本快照；返回含 `checksum` 的完整快照 dict |
| `get_version(label)` | `Optional[Dict[str, Any]]` | 按版本标签取回快照 dict |
| `list_versions()` | `List[Dict[str, Any]]` | 列出全部版本元数据 dict |
| `diff(version_a, version_b)` | `Dict[str, Any]` | 对比两个快照；`compare_versions` 的别名 |
| `compare_versions(v1, v2)` | `Dict[str, Any]` | 两个快照之间实体/关系的详细差异 |
| `restore_snapshot(graph, target_version, require_confirmation=True)` | `bool` | 把活动图恢复到之前的版本；默认直接抛错，除非 `require_confirmation=False` |
| `get_node_history(node_id)` | `List[Dict[str, Any]]` | 返回指定节点按时间排序的变更历史 |
| `tag_version(version_label, tag_name)` | `None` | 创建指向某版本标签的命名 tag |
| `list_tags()` | `Dict[str, str]` | 返回 tag 名 → 版本标签的映射 |
| `prune_versions(keep_last_n)` | `Dict[str, Any]` | 删除旧快照，保留最近 N 个 |
| `verify_checksum(snapshot)` | `bool` | 对照存储的校验和验证快照完整性 |

## 差异分析

对比任意两个快照，看清到底改了什么。结果可用于代码评审、事故调查和监管审计：

```python
diff = manager.diff("v1.0", "v2.0")

summary = diff["summary"]
print("Entities added:      ", summary["entities_added"])
print("Entities removed:    ", summary["entities_removed"])
print("Entities modified:   ", summary["entities_modified"])
print("Relationships added: ", summary["relationships_added"])
print("Relationships removed:", summary["relationships_removed"])

# Inspect individual modified entities
for item in diff["entities_modified"]:
    print("Modified:", item["id"])
    for field, change in item["changes"].items():
        print("  %s: %s -> %s" % (field, change["from"], change["to"]))
```

<Tip>
  **代码评审和事故调查用 `diff()`。**`manager.diff("v1.0", "v2.0")` 返回普通 dict，含 `"summary"`、`"entities_added"`、`"entities_removed"` 和 `"entities_modified"` 几个键。具体来说：用 `"summary"` 子 dict 拿计数，用 `"entities_modified"` 查看属性级变更。
</Tip>

<Accordion title="diff() 返回结构">

```python
# diff() / compare_versions() returns a plain dict:
{
    "version1": str,                  # first version label
    "version2": str,                  # second version label
    "summary": {
        "entities_added":          int,
        "entities_removed":        int,
        "entities_modified":       int,
        "relationships_added":     int,
        "relationships_removed":   int,
        "relationships_modified":  int,
        # also present as nodes_*/edges_* aliases
    },
    "entities_added":    List[Dict],  # full entity dicts
    "entities_removed":  List[Dict],
    "entities_modified": List[Dict],  # {id, before, after, changes}
    "relationships_added":    List[Dict],
    "relationships_removed":  List[Dict],
    "relationships_modified": List[Dict],  # {key, before, after, changes}
    # node_*/edge_* aliases point to the same lists
}
```

</Accordion>

## OntologyVersionManager

本体版本控制支持保存、差异对比与 schema 变更追踪：

```python
from semantica.change_management import OntologyVersionManager

manager = OntologyVersionManager()

# Save a version
snapshot = manager.create_snapshot(
    ontology_data=ontology,
    version_label="1.2.0",
    author="ontology-team@example.com",
    description="Added FHIR alignment mappings"
)

# Diff two ontology versions: returns a plain dict
diff = manager.compare_versions("1.1.0", "1.2.0")
print("Classes added:    ", diff["classes_added"])
print("Classes removed:  ", diff["classes_removed"])
print("Properties added: ", diff["properties_added"])
```

## VersionStorage 后端

<Tabs>
  <Tab title="SQLite（生产）">
    ```python
    from semantica.change_management import SQLiteVersionStorage, TemporalVersionManager

    # Pass path directly to the manager (recommended)
    manager = TemporalVersionManager(storage_path="versions.db")
    ```

    全部版本历史持久化到磁盘，进程重启后仍在。因此，任何需要保留审计轨迹的环境都推荐使用它。
  </Tab>
  <Tab title="内存（测试）">
    ```python
    from semantica.change_management import InMemoryVersionStorage, TemporalVersionManager

    # Default (no storage_path) uses in-memory storage automatically
    manager = TemporalVersionManager()
    ```

    快且零配置。数据**不持久化**：进程退出即丢失全部版本历史。只用于单元测试和开发。
  </Tab>
</Tabs>

<Warning>
  不带参数的 `TemporalVersionManager()` 默认用内存存储。生产环境务必传 `storage_path="versions.db"` 或显式的 `SQLiteVersionStorage`：否则重启后整个版本历史都会消失。
</Warning>

<Tip>
  **生产环境用 `SQLiteVersionStorage`。**默认的内存存储在进程退出时丢失全部版本历史。给 `TemporalVersionManager` 传 `storage_path="versions.db"`，或显式创建 `SQLiteVersionStorage(db_path="versions.db")`。
</Tip>

## 完整性校验

用大白话讲，校验和就是快照的"指纹"：快照一旦落盘，谁动过图，重算指纹就对不上。因此，SHA-256 校验和能检测出图在两次快照之间发生的任何未授权修改：

```python
from semantica.change_management import compute_checksum, verify_checksum

# Compute a checksum for any dict
checksum = compute_checksum({"nodes": [], "edges": []})

# verify_checksum takes the snapshot dict directly.
# It reads the "checksum" key from the snapshot and recomputes to compare.
snapshot = manager.get_version("v1.0")
is_valid = verify_checksum(snapshot)

if not is_valid:
    raise RuntimeError("Snapshot has been tampered with")
```

<Tip>
  `verify_checksum` 接收完整快照 dict（其中含存储的 `"checksum"` 键）。直接传 `create_snapshot` 或 `get_version` 返回的 dict 即可：无需单独的 `expected_checksum` 参数。
</Tip>

## ChangeLogEntry

`ChangeLogEntry` 是 `create_snapshot` 在内部创建的元数据对象。快照存储前，它会先校验作者（必须是合法邮箱地址）和描述（非空，最长 500 字符）。

```python
from semantica.change_management.change_log import ChangeLogEntry

# Create using current timestamp
entry = ChangeLogEntry.create_now(
    author="user@example.com",     # must be a valid email
    description="Initial snapshot" # max 500 chars, non-empty
)
print(entry.timestamp)   # ISO 8601 timestamp
print(entry.author)      # "user@example.com"
print(entry.description) # "Initial snapshot"
```

<Accordion title="ChangeLogEntry 数据结构">

```python
@dataclass
class ChangeLogEntry:
    timestamp:       str            # ISO 8601 timestamp
    author:          str            # valid email address (validated on init)
    description:     str            # change description, max 500 chars
    change_id:       Optional[str]  # optional unique identifier
    related_changes: List[str]      # optional list of related change IDs
```

</Accordion>

## 合规与版本历史

全部版本快照构成一条防篡改的审计轨迹。用 `list_versions()` 和 `diff()` 重建并审查变更，满足监管要求：

```python
from semantica.change_management import TemporalVersionManager

manager = TemporalVersionManager(storage_path="versions.db")

# Enumerate the full version history
for v in manager.list_versions():
    print(v["timestamp"], "|", v["author"], "|", v["label"], "|", v["description"])

# Diff any two snapshots for a change report
diff = manager.diff("v1.0", "v2.0")
s = diff["summary"]
print("Added: %d | Removed: %d | Modified: %d" % (
    s["entities_added"], s["entities_removed"], s["entities_modified"]))
```

<Tip>
  **合规审查用 `list_versions()` 和 `diff()`。**`manager.list_versions()` 返回元数据 dict 列表（含 `label`、`author`、`timestamp`、`checksum`）。导出前对 `get_version()` 返回的 dict 跑 `verify_checksum(snapshot)` 确认完整性。
</Tip>

任何合规导出前先用 `verify_checksum()` 确认快照完整性：

```python
from semantica.change_management import verify_checksum

snapshot = manager.get_version("v1.0")
is_valid = verify_checksum(snapshot)
if not is_valid:
    raise RuntimeError("Snapshot has been modified since it was recorded")
```

按节点的变更历史可用于 HIPAA 主题访问和 SOX 审计工作流：

```python
# Get full mutation history for a specific node
history = manager.get_node_history("patient_001")
for record in history:
    print(record["timestamp"], record["operation"], record["version_label"])
```

### 合规场景覆盖

<AccordionGroup>
  <Accordion title="HIPAA：主题访问请求">
    用 `manager.get_node_history("patient_001")` 取回患者实体上的每一条变更记录。每条 `MutationRecord` 含 `timestamp`、`operation`、`entity_id`、`payload` 和 `version_label`。每个快照上的 SHA-256 校验和证明记录未被篡改。
  </Accordion>
  <Accordion title="SOX：季度审查">
    用 `manager.list_versions()` 枚举全部快照，用 `manager.diff(v1, v2)` 把变更报告限定到相关季度。不可变的快照链提供了 SOX Section 404 要求的监管链(chain of custody)。
  </Accordion>
  <Accordion title="GDPR：删除权验证">
    删除数据主体的实体后，对图打快照并与删除前的快照做 diff。`diff["entities_removed"]` 以机器可读的形式记录了删了什么、何时删的，因此满足 Article 17 的文档化要求。
  </Accordion>
  <Accordion title="FDA 21 CFR Part 11：电子记录">
    每个快照 dict 都含 `author`、`timestamp` 和 `checksum`：合规电子记录要求的三个字段。`verify_checksum(snapshot)` 提供 21 CFR § 11.10(e) 要求的防篡改证明。
  </Accordion>
</AccordionGroup>

- [Provenance](./provenance.md)：W3C PROV-O 血缘追踪。
- [Knowledge Graph](./kg.md)：接受版本管理的图。
- [Export](./export.md)：导出版本化快照。
- [Conflicts](./conflicts.md)：检测版本之间引入的冲突。
