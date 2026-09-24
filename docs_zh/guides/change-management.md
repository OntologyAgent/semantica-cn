---
title: 变更管理与版本控制
description: 对知识图谱与本体进行快照、版本管理、差异比较与迁移——支持 SQLite 持久化、校验和验证与结构化变更日志。
source: guides/change-management.md
source_version: 76ee7e8ddc585bec71cc0decd622a9ff1bc8bffa
icon: "clock-rotate-left"
---

## 什么是变更管理与版本控制？

知识图谱时刻在变。一句话概括这套机制：先拍照存证，再放心改动，出了问题随时翻回上一张。`TemporalVersionManager` 通过在特定时间点捕获完整的状态快照(Snapshot)，为你的图谱提供一份可验证的历史。你可以在重大变更前打命名快照，在任意两个状态之间生成详细差异(diff)，一次调用回滚(Rollback)到旧版本，并在向下游发布数据前校验 SHA-256 校验和。

## 存储行为

传入 `storage_path`，例如 `TemporalVersionManager(storage_path="versions.db")`，快照就会持久化到磁盘上的 SQLite 数据库。省略 `storage_path` 则默认使用内存存储，脚本结束即消失。

## 为什么要用变更管理？

变更管理(Change Management)是你的安全网和审计轨迹。用途包括：
- **保障摄取安全**：大批量摄取前先打快照，数据一旦损坏可立即回滚。
- **审计轨迹**：维护一份可验证的日志，记录变更何时发生、由谁批准、具体改了哪些节点/边。
- **发布门禁**：比较预发布与生产图谱，核验校验和后再签发发布。

## 我需要哪个工具？

Semantica 提供多种追踪能力，选对工具至关重要：
- **变更管理**（本指南）：用于**整图快照**、状态差异比较和完整回滚。
- **溯源(Provenance)**：用于细粒度的**来源与数据血缘(Lineage)追踪**。它回答的是*"这个节点具体来自哪份文档？"*
- **智能体记忆**：用于**对话与上下文状态**。它回答的是*"AI 智能体在本次会话中做了哪些决策？"*

## 适用与不适用场景

- **适用**：存在关键检查点（如每日数据源、合作伙伴合并、监管报送），需要冻结图谱的完整状态，且可能需要回滚。
- **不适用**：图谱有数百万节点，却想追踪每一次细小编辑。由于 `TemporalVersionManager` 快照的是整个图字典，对超大图频繁打快照会导致严重的存储膨胀。细粒度追踪请改用溯源。

<Info>
  `TemporalVersionManager` 与 `AgentContext.flush_checkpoint()` 直接集成——智能体检查点与手工快照共用同一存储格式，因此可以在自动化与手工两类工作流之间做差异比较。
</Info>

---

## 典型工作流

标准的变更管理循环按以下步骤推进：

1. **快照**：捕获基线图谱状态。
2. **修改**：执行摄取、变更或分析。
3. **比较**：生成差异，看清改了什么。
4. **验证**：检查 SHA-256 哈希，确认数据完整性。
5. **打标**：应用人类可读的标签（如 `approved`）。
6. **回滚**：修改有误时恢复图谱状态。

---

## 通用示例：员工档案变更

来看一个谁都看得懂的例子：追踪员工的部门调动。

```python
from semantica.change_management import TemporalVersionManager
from semantica.context import ContextGraph

# 1. 搭建图与版本管理器
graph = ContextGraph()
graph.add_node("emp-101", "Employee", "Alice")
graph.add_node("dept-hr", "Department", "Human Resources")
graph.add_edge("emp-101", "dept-hr", "works_in")

# 传入了 storage_path，因此启用 SQLite 持久化
vm = TemporalVersionManager(storage_path="hr_versions.db")

# 2. 给基线打快照
snap_v1 = vm.create_snapshot(
    graph         = graph.to_dict(),
    version_label = "v1_baseline",
    author        = "hr_system@example.com",
    description   = "Initial employee graph",
)

# 3. 修改图（把 Alice 调到工程部）
graph.add_node("dept-eng", "Department", "Engineering")
graph.add_edge("emp-101", "dept-eng", "works_in")

# 4. 给变更后的状态打快照
snap_v2 = vm.create_snapshot(
    graph         = graph.to_dict(),
    version_label = "v2_transfer",
    author        = "hr_admin@example.com",
    description   = "Alice transferred to Engineering",
)

# 5. 比较版本
diff = vm.compare_versions("v1_baseline", "v2_transfer")
print("Nodes added:", diff["summary"]["nodes_added"])  # 1（工程部）
print("Edges added:", diff["summary"]["edges_added"])  # 1（works_in → 工程部）
```

接下来用领域场景深入了解这些能力。

---

## 创建快照

在任何有影响的变更之前先打快照：一次摄取扫描、一次合作伙伴数据源合并，或一次自动富集运行。

```python
from semantica.change_management import TemporalVersionManager
from semantica.context import ContextGraph

graph = ContextGraph()
graph.add_node("apt29",         "ThreatActor",   "APT29 / NOBELIUM")
graph.add_node("cve-2024-3400", "Vulnerability", "CVE-2024-3400 PAN-OS RCE")
graph.add_edge("apt29", "cve-2024-3400", "exploits", weight=0.97)

vm = TemporalVersionManager(storage_path="cti_versions.db")

snap_pre = vm.create_snapshot(
    graph         = graph.to_dict(),
    version_label = "q3_2025_baseline",
    author        = "analyst_zhang@example.com",
    description   = "CTI baseline before Q3 OSINT sweep",
)

print(snap_pre["label"])        # "q3_2025_baseline"
print(snap_pre["checksum"])     # 序列化图的 SHA-256
print(snap_pre["timestamp"])    # ISO 日期时间
print(snap_pre["author"])       # "analyst_zhang"
print(len(snap_pre["nodes"]))   # 快照时的节点数
print(len(snap_pre["edges"]))   # 快照时的边数
```

摄取运行完成后，再打一次快照来标记变更后的状态：

```python
graph.add_node("cve-2024-21412", "Vulnerability", "CVE-2024-21412 Windows SmartScreen bypass")
graph.add_node("apt40",          "ThreatActor",   "APT40 / BRONZE MOHAWK")
graph.add_edge("apt40", "cve-2024-21412", "exploits", weight=0.88)

snap_post = vm.create_snapshot(
    graph         = graph.to_dict(),
    version_label = "q3_2025_post_nvd_sweep",
    author        = "osint_pipeline@example.com",
    description   = "After NVD weekly sweep — 2025-07-14",
)
```

## 比较两个快照

`compare_versions` 返回任意两个命名快照之间的精确差异——新增、删除或修改的节点和边。

```python
diff = vm.compare_versions("q3_2025_baseline", "q3_2025_post_nvd_sweep")

s = diff["summary"]
print("Nodes added   :", s["nodes_added"])    # 2
print("Nodes removed :", s["nodes_removed"])  # 0
print("Edges added   :", s["edges_added"])    # 1

for node in diff["nodes_added"]:
    print(" +", node.get("id"), "/", node.get("content"))

for edge in diff["edges_added"]:
    print(" +", edge.get("source"), "→", edge.get("target"), "[" + edge.get("type", "") + "]")
```

你也可以直接传快照字典，而不必传标签：

```python
diff = vm.compare_versions(snap_pre, snap_post)
```

## 验证完整性

把快照发布给下游系统之前——SIEM、合作伙伴数据源、监管报送——先校验 SHA-256 校验和(Checksum)，确认快照写入后没有任何改动。

```python
snap = vm.get_version("q3_2025_post_nvd_sweep")

if not vm.verify_checksum(snap):
    raise RuntimeError("Checksum mismatch on q3_2025_post_nvd_sweep — aborting publish.")

print("Integrity verified — safe to publish.")
```

## 回滚

传入目标标签和 `require_confirmation=False`（一道显式的安全闸），即可把图恢复到任意历史快照。

```python
vm.restore_snapshot(
    graph                = graph,
    target_version       = "q3_2025_baseline",
    require_confirmation = False,
)

# 把回滚事件记录为一份新快照
vm.create_snapshot(
    graph         = graph.to_dict(),
    version_label = "q3_2025_rollback",
    author        = "analyst_zhang@example.com",
    description   = "Rolled back to baseline after corrupted OSINT batch",
)
```

<Info>
  若 `require_confirmation` 未显式设为 `False`，`restore_snapshot` 会抛出 `ProcessingError`，以防自动化脚本误触发回滚。
</Info>

## 构建审计变更日志

按时间顺序列出全部快照，并逐一与前一份做差异比较，得到一份人类可读的变更日志。

```python
versions = sorted(vm.list_versions(), key=lambda v: v["timestamp"])

print("Graph Change Log")
print("=" * 60)

for i, v in enumerate(versions):
    print("\n[{}] {}  (by {})".format(v["timestamp"][:10], v["label"], v["author"]))
    print("  " + v["description"])

    if i > 0:
        diff = vm.compare_versions(versions[i - 1]["label"], v["label"])
        s    = diff["summary"]
        print("  Changes: +{} nodes  -{} nodes  +{} edges  -{} edges".format(
            s["nodes_added"], s["nodes_removed"],
            s["edges_added"], s["edges_removed"],
        ))
```

示例输出：

```text
Graph Change Log
============================================================

[2025-07-01] q3_2025_baseline  (by analyst_zhang@example.com)
  CTI baseline before Q3 OSINT sweep

[2025-07-14] q3_2025_post_nvd_sweep  (by osint_pipeline@example.com)
  After NVD weekly sweep — 2025-07-14
  Changes: +2 nodes  -0 nodes  +1 edges  -0 edges

[2025-07-14] q3_2025_rollback  (by analyst_zhang@example.com)
  Rolled back to baseline after corrupted OSINT batch
  Changes: -2 nodes  +0 nodes  -1 edges  +0 edges
```

## 为里程碑打标签

给任意快照挂上命名标签，用来标记评审门禁、已批准状态或监管报送节点。

```python
vm.tag_version("q3_2025_post_nvd_sweep", "q3-approved")

for tag_name, version_label in vm.list_tags().items():
    print(f"{tag_name:20s} → {version_label}")
# q3-approved          → q3_2025_post_nvd_sweep
```

## 节点历史

把 `TemporalVersionManager` 挂载到运行中的 `ContextGraph` 上，即可自动记录每一次单独的变更操作——每次 `add_node`、`add_edge` 和更新调用——而不只是快照级别的差异。

```python
vm.attach_to_graph(graph)

graph.add_node("apt29-alias", "ThreatActor", "NOBELIUM (rebranding 2021)")
graph.add_edge("apt29", "apt29-alias", "alias_of", weight=1.0)

for record in vm.get_node_history("apt29"):
    print("[{}] {} on {}  payload={}".format(
        record["timestamp"], record["operation"], record["entity_id"],
        str(record["payload"])[:60],
    ))
```

## 与 AgentContext 集成

在构造 `AgentContext` 时传入版本管理器。智能体检查点与手工快照共用同一存储，给你一份统一的历史。

```python
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore
from semantica.change_management import TemporalVersionManager

graph = ContextGraph()
vm    = TemporalVersionManager(storage_path="agent_versions.db")

context = AgentContext(
    vector_store             = VectorStore(backend="faiss", dimension=768),
    knowledge_graph          = graph,
    temporal_version_manager = vm,
)

context.store("APT29 targeting NATO infrastructure in Q3 2025")
context.checkpoint("pre_analysis")

# ... 智能体推理循环 ...

context.checkpoint("post_analysis")
context.flush_checkpoint("post_analysis")   # 经 vm 持久化

diff = context.diff_checkpoints("pre_analysis", "post_analysis")
print("Decisions added    :", len(diff["decisions_added"]))
print("Relationships added:", len(diff["relationships_added"]))
```

---

## 常见陷阱

- **对超大图过于频繁地打快照**：`TemporalVersionManager` 快照的是整个图结构。对大规模图在每次细小编辑后都这么做，会造成严重的存储膨胀。它适用于里程碑门禁，不适合做事件溯源(Event Sourcing)。
- **变更追踪前忘记 `attach_to_graph`**：想用 `get_node_history()`，就必须在任何变更发生*之前*调用 `vm.attach_to_graph(graph)`。否则这些事件不会被捕获。
- **混淆溯源与版本控制**：不要用版本快照回答"这个节点的数据具体来自哪里？"。那是溯源模块的职责。版本控制追踪的是*整个*图在某一时间点的状态。
- **忽略回滚确认要求**：在自动化脚本里直接调用 `restore_snapshot` 会抛出 `ProcessingError` 并中断流水线，除非你显式传入 `require_confirmation=False`。
- **快照过多导致存储增长**：长期不清理旧快照、或不必要地打快照，SQLite 数据库会越积越大。

---

## 领域示例

<Tabs>
  <Tab title="国防——CTI 流水线">
    每日摄取 NVD 与 ISAC 数据源，做前后快照、出一份 SOC 变更通报，并在发布到 SIEM 前设一道完整性门禁。

```python
from semantica.change_management import TemporalVersionManager
from semantica.context import ContextGraph
import datetime

graph = ContextGraph()
vm    = TemporalVersionManager(storage_path="cti_versions.db")
today = datetime.date.today().isoformat()

snap_pre = vm.create_snapshot(
    graph         = graph.to_dict(),
    version_label = f"pre_nvd_{today}",
    author        = "osint_pipeline@example.com",
    description   = "CTI baseline before NVD sweep",
)

# 摄取
graph.add_node("cve-2025-1337",    "Vulnerability", "CVE-2025-1337 critical RCE")
graph.add_node("apt29-q3-cluster", "ThreatActor",   "APT29 Q3 2025 campaign cluster")
graph.add_edge("apt29-q3-cluster", "cve-2025-1337", "weaponizes", weight=0.91)

snap_post = vm.create_snapshot(
    graph         = graph.to_dict(),
    version_label = f"post_nvd_{today}",
    author        = "osint_pipeline@example.com",
    description   = "After NVD sweep",
)

diff = vm.compare_versions(snap_pre["label"], snap_post["label"])
s    = diff["summary"]
print(f"SOC Bulletin: +{s['nodes_added']} threat nodes, +{s['edges_added']} relationships")
for n in diff["nodes_added"]:
    print(f"  + [{n.get('type')}] {n.get('content')}")

if not vm.verify_checksum(snap_post):
    raise RuntimeError("Checksum mismatch — aborting SIEM publish")
print("Snapshot verified — publishing to SIEM feed.")
```

  </Tab>

  <Tab title="安全——事件响应">
    现场应急响应过程中，每有重大发现就给事件图打一次快照，事后复盘时就能精确重放调查的演进过程。

```python
from semantica.change_management import TemporalVersionManager
from semantica.context import ContextGraph

graph = ContextGraph()
vm    = TemporalVersionManager(storage_path="incident_ir042.db")

# T+0：初始分诊
graph.add_node("wkstn-047",   "Host",    "Compromised workstation WKSTN-047")
graph.add_node("attacker-ip", "Network", "Attacker ingress 185.220.101.47")
graph.add_edge("attacker-ip", "wkstn-047", "initial_access", weight=0.95)

vm.create_snapshot(
    graph         = graph.to_dict(),
    version_label = "ir042_t0_triage",
    author        = "analyst_chen@example.com",
    description   = "T+0 — one compromised host identified",
)

# T+2h：确认横向移动
graph.add_node("dc01",       "Host",    "Domain controller DC01")
graph.add_node("svc-backup", "Account", "Stolen service account SVC-BACKUP")
graph.add_edge("wkstn-047",  "svc-backup", "credential_theft", weight=0.88)
graph.add_edge("svc-backup", "dc01",       "lateral_move",     weight=0.82)

vm.create_snapshot(
    graph         = graph.to_dict(),
    version_label = "ir042_t2h_lateral",
    author        = "analyst_chen@example.com",
    description   = "T+2h — lateral movement to DC01 via stolen SVC-BACKUP",
)

diff = vm.compare_versions("ir042_t0_triage", "ir042_t2h_lateral")
s    = diff["summary"]
print(f"Post-mortem T+0→T+2h: +{s['nodes_added']} hosts/accounts, +{s['edges_added']} attack paths")
for edge in diff["edges_added"]:
    print(f"  + {edge.get('source')} → {edge.get('target')} [{edge.get('type')}]")
```

  </Tab>

  <Tab title="生命科学——临床试验">
    按试验阶段为试验知识图谱做版本管理，在 II 期与 III 期申报之间生成机器可验证的差异，供监管审查。

```python
from semantica.change_management import TemporalVersionManager
from semantica.context import ContextGraph

graph_ph2 = ContextGraph()
graph_ph2.add_node("compound-xr401", "Compound", "XR-401")
graph_ph2.add_node("endpoint-orr",   "Endpoint", "Overall Response Rate")
graph_ph2.add_node("disease-nsclc",  "Disease",  "NSCLC")

graph_ph3 = ContextGraph()
graph_ph3.add_node("compound-xr401",  "Compound",   "XR-401")
graph_ph3.add_node("endpoint-orr",    "Endpoint",   "Overall Response Rate")
graph_ph3.add_node("endpoint-pfs",    "Endpoint",   "Progression-Free Survival")
graph_ph3.add_node("disease-nsclc",   "Disease",    "NSCLC")
graph_ph3.add_node("comparator-doce", "Comparator", "Docetaxel")

vm = TemporalVersionManager(storage_path="trial_xr401.db")

vm.create_snapshot(
    graph=graph_ph2.to_dict(), version_label="phase_ii_v1.0",
    author="clinical_data_team@example.com", description="Phase II — ORR primary, NSCLC",
)
vm.create_snapshot(
    graph=graph_ph3.to_dict(), version_label="phase_iii_v2.0",
    author="clinical_data_team@example.com", description="Phase III — PFS co-primary, Docetaxel added",
)

diff = vm.compare_versions("phase_ii_v1.0", "phase_iii_v2.0")
print("Regulatory diff Phase II → Phase III:")
for n in diff["nodes_added"]:
    print(f"  + [{n.get('type')}] {n.get('content')}")

snap = vm.get_version("phase_iii_v2.0")
assert vm.verify_checksum(snap), "Checksum failed — cannot attach to dossier"
print("Phase III snapshot verified — safe for regulatory submission.")
```

  </Tab>

  <Tab title="银行——模型治理">
    每次监管更新都为 Basel III 信用风险模型图做版本管理，并在生产部署前为模型治理委员会生成机器可验证的差异。

```python
from semantica.change_management import TemporalVersionManager
from semantica.context import ContextGraph

graph = ContextGraph()
graph.add_node("metric-cet1",      "CapitalMetric", "CET1 Capital Ratio")
graph.add_node("metric-ltv",       "RiskParameter", "LTV Ratio")
graph.add_node("metric-pd",        "RiskParameter", "Probability of Default")
graph.add_node("metric-lgd",       "RiskParameter", "Loss Given Default")
graph.add_node("regulation-cre20", "Regulation",    "Basel III CRE20")

vm = TemporalVersionManager(storage_path="credit_risk_versions.db")

vm.create_snapshot(
    graph=graph.to_dict(), version_label="basel_v1.0",
    author="risk_model_team@example.com", description="Basel III CRE20 initial graph",
)

# 监管更新——DSCR 成为强制指标
graph.add_node("metric-dscr", "RiskParameter", "Debt Service Coverage Ratio")
graph.add_edge("regulation-cre20", "metric-dscr", "requires", weight=1.0)

vm.create_snapshot(
    graph=graph.to_dict(), version_label="basel_v1.1",
    author="risk_model_team@example.com", description="DSCR added per EBA GL 2020/06",
)

diff = vm.compare_versions("basel_v1.0", "basel_v1.1")
s    = diff["summary"]
print(f"Model governance diff v1.0→v1.1: +{s['nodes_added']} params, +{s['edges_added']} rules")
for n in diff["nodes_added"]:
    print(f"  + [{n.get('type')}] {n.get('content')}")

snap = vm.get_version("basel_v1.1")
assert vm.verify_checksum(snap), "Checksum failed — aborting model deployment"
print("Model v1.1 verified and approved for production.")
```

  </Tab>
</Tabs>

## 相关指南

- [上下文图](./context-graphs.md) — `ContextGraph.to_dict()` 为 `create_snapshot()` 供数
- [本体管理](./ontology.md) — 本体版本管理与图版本管理配套，构成完整的模式 + 数据审计轨迹
- [SHACL 校验](./shacl-validation.md) — 在每个版本门禁上先校验图谱数据，再打快照
- [溯源](./provenance.md) — 变更管理结合 W3C PROV-O 血缘，形成完整的审计轨迹
- [可视化](./visualization.md) — `TemporalVisualizer.visualize_snapshot_comparison()` 与 `visualize_metrics_evolution()` 把版本差异渲染成交互式图表
