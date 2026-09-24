---
title: "上下文图"
description: "Semantica 如何把知识存进线程安全的内存属性图——节点与边带时态有效期，支持跨图导航、邻近度混合检索，以及从对话构建图谱。"
source: guides/context-graphs.md
source_version: 3f6e35a2127bb12b126d51ad69ce4f0edcb7e930
icon: "diagram-project"
---

`ContextGraph` 是一个线程安全的内存属性图(Property Graph)：每个节点和边都带时态有效期(temporal validity)窗口，内置广度优先搜索(BFS)遍历，配有用于语义检索的 FAISS 向量索引，还能经 `AgentContext` 做邻近度混合检索(proximity-blended retrieval)。多个智能体(Agent)或线程往共享知识库写入、同时分析师实时查询的场景，就该用它。

## 什么是上下文图？

上下文图(Context Graph)把实体存成**节点**、把关系存成**边**，再辅以元数据和时态有效期。

**节点**表示领域中的实体——威胁行为者、漏洞、公司、人物，或任何你想追踪的概念。每个节点有 ID、类型、可选的内容文本和元数据属性。

**边**表示实体之间的关系——"APT29 uses SUNBURST"、"Alice works_for Acme Corp"，或"CVE-2024-3400 affects SolarWinds"。每条边有类型、权重和可选元数据。

**元数据**以键值对的形式在节点和边上存放附加属性——地理来源、置信度分数、时间戳，或任何领域专属属性。

像 ContextGraph 这样的**属性图**与简单网络的区别在于：节点和边都能挂丰富的元数据，因此适合关系需要上下文和属性支撑的复杂真实场景。

## 为什么要用上下文图？

**关系分析。**图结构揭示实体之间如何连接——谁攻击谁、什么漏洞利用什么、哪个决策导致了哪个结果。单看每份文档看不出的关系，一旦连起来就一目了然。

**多跳推理。**遍历图（而不是做关键词匹配）就能回答"APT29 三步之内能触及哪些目标？"或"哪些漏洞影响我们的关键系统？"这类问题。

**上下文保留。**单纯向量检索做不到这一点：图保留了实体之间的关系。找到相关的威胁行为者后，可以立即看到它的工具、目标和基础设施。

**时态状态追踪。**记录关系何时有效、基础设施何时活跃、决策何时做出。既可以查询历史状态，也可以只筛选当前信息。

## 适用与不适用场景

**上下文图适用于：**
- 实体之间关系丰富的复杂领域
- 多跳推理与遍历查询
- 对实体关系和状态做时态追踪
- 与具有明确实体关系的结构化数据集成
- 多个来源贡献关联数据的协作环境

**以下场景用简单向量检索可能就够了：**
- 关系无关紧要的纯文档检索
- 单跳相似度搜索
- 结构尚不清晰的探索性研究
- 不涉及实体关系的非结构化文本只读分析

**以下场景可能用不上图：**
- 简单的关键词或语义搜索任务
- 关系不再演化的静态文档集合
- 单人、短期的分析项目
- 搭建复杂度超过关系本身复杂度的情况

<Info>
  ContextGraph 是一个**内存数据结构**。所有节点、边和元数据都存在 Python 字典和列表里。独立使用的图用 `save_to_file()` 持久化状态；用 `AgentContext` 时则改调 `AgentContext.save()`——它会一步保存图、FAISS 向量索引和记忆。在已成形的图上做分析运算（中心性排名、社区发现、节点嵌入、链接预测），见[图分析指南](./graph-analytics.md)；要把决策记录成节点并查询，见[决策智能指南](./decision-intelligence.md)。
</Info>

## 构建图

构建 ContextGraph 有两种方式：

**手工构建** — 用 `add_node()` 和 `add_edge()` 以编程方式添加节点和边。这种方式完全掌控图结构，适合已有结构化数据、或想构建特定关系模式的场合。

**自动抽取工作流** — 把文档列表传给 `AgentContext.store()`，并设置 `extract_entities=True` 或 `extract_relationships=True`。这要求在 `AgentContext` 构造函数里设置 `knowledge_graph=`；抽取过程随后会为检测到的实体创建节点、为发现的关系创建边。传给 `store()` 的单个字符串只会存为记忆条目，不会触发图构建。

最简单的图不需要任何参数：

```python
from semantica.context import ContextGraph

graph = ContextGraph()
```

要让图谱既服务威胁情报工作负载又跑分析，就在构造时启用子组件——它们是惰性初始化的，但必须预先声明：

```python
graph = ContextGraph(
    advanced_analytics  = True,
    centrality_analysis = True,
    community_detection = True,
    node_embeddings     = True,
)
```

整张图完全由 Python 字典和一个可重入锁（`threading.RLock`）支撑：不需要外部服务、不需要数据库连接、也没有网络调用。一次 import，就能在单元测试里立起一个功能完备的情报图谱。

## 添加第一批实体

每个实体作为一个节点加入，带类型、可选内容字符串和任意多个元数据关键字参数：

```python
# add_node(node_id, node_type, content=None, **properties) -> None
# 所有额外的关键字参数都会存入 ContextNode.metadata

graph.add_node(
    "APT29",
    "ThreatActor",
    "Russian state-sponsored group, also known as COZY BEAR",
    origin="Russia",
    motivation="espionage",
    first_seen="2008",
)

graph.add_node(
    "SUNBURST",
    "Malware",
    "Supply-chain backdoor embedded in SolarWinds Orion updates",
    family="backdoor",
    first_seen="2019-10",
    platforms=["Windows"],
)

graph.add_node(
    "CVE-2020-10148",
    "Vulnerability",
    "SolarWinds Orion API authentication bypass",
    cvss=10.0,
    affected_product="SolarWinds Orion",
)

graph.add_node(
    "45.142.212.100",
    "C2Domain",
    "Command-and-control server observed in SUNBURST campaign",
    asn="AS29550",
    country="Netherlands",
)

graph.add_node(
    "SolarWinds",
    "Victim",
    "SolarWinds Corporation — software supply chain victim",
    sector="Technology",
)
```

<Info>
  没有 `properties={}` 这样的参数。所有元数据字段都要作为直接关键字参数传入。调用 `add_node("x", "t", properties={"k": "v"})` 会把这个字典存到 metadata 里一个字面名为 `properties` 的键下——这不是你想要的效果。
</Info>

现在用带类型、带权重的边把它们连起来：

```python
# add_edge(source_id, target_id, edge_type="related_to", weight=1.0, **properties) -> None

graph.add_edge("APT29",          "SUNBURST",         "uses",       weight=1.0)
graph.add_edge("SUNBURST",       "CVE-2020-10148",   "exploits",   weight=0.95)
graph.add_edge("SUNBURST",       "SolarWinds",       "targets",    weight=1.0)
graph.add_edge("APT29",          "45.142.212.100",   "operates",   weight=0.9)
graph.add_edge("SUNBURST",       "45.142.212.100",   "beacons_to", weight=0.85)
graph.add_edge("CVE-2020-10148", "SolarWinds",       "affects",    weight=1.0)
```

看看目前有什么：

```python
s = graph.stats()
print(f"Nodes: {s['node_count']}, Edges: {s['edge_count']}, Density: {s['density']:.4f}")
# Nodes: 5, Edges: 6, Density: 0.3000

print("Node types:", s["node_types"])   # {"ThreatActor": 1, "Malware": 1, ...}
print("Edge types:", s["edge_types"])   # {"uses": 1, "exploits": 1, ...}
```

## 时态有效期——情报有保质期

用 `valid_from` 和 `valid_until` 给节点和边标记活跃窗口，时态查询就会自动排除过期数据：

```python
# 该 C2 域名只在战役窗口内活跃
graph.add_node(
    "45.142.212.100",
    "C2Domain",
    "SUNBURST C2 — active during campaign",
    asn="AS29550",
    valid_from="2019-10-01T00:00:00",
    valid_until="2020-12-17T00:00:00",   # DarkHalo C2 关停日期
)

# 一条有效期有限的检测规则
graph.add_node(
    "SIGMA-SUNBURST-001",
    "DetectionRule",
    "Sigma rule: SUNBURST beacon pattern",
    rule_type="sigma",
    valid_from="2020-12-13T00:00:00",
    valid_until="2021-06-30T23:59:59",   # 观察到更新 TTP 后弃用
)

# 时态边同理
graph.add_edge(
    "APT29", "45.142.212.100", "operates",
    weight=0.9,
    valid_from="2019-10-01T00:00:00",
    valid_until="2020-12-17T00:00:00",
)
```

现在问一个问题：2020 年 12 月 1 日（战役期间）哪些节点处于活跃状态？

```python
from datetime import datetime

# at_time 必须是 datetime 对象——不能传 ISO 字符串
active = graph.find_active_nodes(
    node_type="C2Domain",
    at_time=datetime(2020, 12, 1, 0, 0, 0),
)
print(f"Active C2 domains on 2020-12-01: {len(active)}")
# Active C2 domains on 2020-12-01: 1  (45.142.212.100 is still in its window)

# 对比今天——该 C2 已过期
active_now = graph.find_active_nodes(node_type="C2Domain")  # 默认取 datetime.now()
print(f"Active C2 domains today: {len(active_now)}")
# Active C2 domains today: 0

# 完整时态快照——只含给定时刻有效的节点和边
snapshot = graph.state_at(datetime(2020, 12, 1, 0, 0, 0))
print(f"Active nodes: {len(snapshot['nodes'])}")
print(f"Active edges: {len(snapshot['edges'])}")
```

这样一来，今天的查询就不会再返回"APT29 目前运营着 45.142.212.100"——这条边已超出有效期，不会出现在时态查询结果里。

## 查找节点

`find_node()` 按 ID 取节点，`find_nodes()` 按类型或元数据过滤：

```python
# find_node(node_id) -> Optional[Dict]
# 返回的键是 "id"、"type"、"content"、"metadata"——不是 "node_id" 或 "node_type"

actor = graph.find_node("APT29")
if actor:
    print(actor["id"])       # "APT29"
    print(actor["type"])     # "ThreatActor"
    print(actor["content"])  # "Russian state-sponsored group..."
    print(actor["metadata"]) # {"origin": "Russia", "motivation": "espionage", ...}

# find_nodes(node_type=None, skip=0, limit=None) -> List[Dict]
all_actors = graph.find_nodes(node_type="ThreatActor")
all_vulns  = graph.find_nodes(node_type="Vulnerability")
```

## 遍历图

BFS 遍历直接回答可达性问题：

```python
# get_neighbors(node_id, hops=1, relationship_types=None,
#               min_weight=0.0, include_distance_metadata=False) -> List[Dict]
# 每条结果包含 {"id", "type", "content", "relationship", "weight", "hop"}

neighbors = graph.get_neighbors("APT29", hops=2)
for n in neighbors:
    print(f"  hop={n['hop']}  [{n['relationship']}]  {n['id']}  ({n['type']})")

# hop=1  [uses]       SUNBURST         (Malware)
# hop=1  [operates]   45.142.212.100   (C2Domain)
# hop=2  [exploits]   CVE-2020-10148   (Vulnerability)
# hop=2  [targets]    SolarWinds       (Victim)
# hop=2  [beacons_to] 45.142.212.100   (C2Domain)  — also reachable via hop-1
```

只沿特定边类型遍历——比如想只追踪漏洞利用链、不受其他关系类型干扰时很有用：

```python
exploit_chain = graph.get_neighbors(
    "APT29",
    hops=3,
    relationship_types=["uses", "exploits", "affects"],
)
```

当你需要依据图上距离判断连接的可信度时，启用距离元数据(distance metadata)。每条结果会多出一个 `confidence_decay` 置信衰减乘数——距离越远的节点，权重越低：

```python
neighbors = graph.get_neighbors(
    "APT29",
    hops=3,
    include_distance_metadata=True,
)
for n in neighbors:
    print(f"  {n['id']:30s}  band={n['distance_band']:8s}  decay={n['confidence_decay']:.3f}")

# APT29's direct SUNBURST edge:   band=direct   decay=1.000
# CVE reached via SUNBURST:       band=near     decay=0.850
# SolarWinds reached via CVE:     band=mid      decay=0.700
```

要追踪从起始节点到特定目标的路径，用 `get_neighbors()` 加 `include_distance_metadata=True`。每条结果带一个 `path_to_anchor` 列表，给出从源节点到该邻居的完整节点 ID 序列：

```python
# include_distance_metadata=True 时 get_neighbors 会返回 path_to_anchor
neighbors = graph.get_neighbors("APT29", hops=3, include_distance_metadata=True)
for n in neighbors:
    if n["id"] == "SolarWinds":
        print(" → ".join(n["path_to_anchor"]))
        # APT29 → SUNBURST → SolarWinds
```

## 处理并发写入

`ContextGraph` 用一个可重入锁（`threading.RLock`）包裹每一次变更操作来处理并发写入——你不需要自己加同步：

```python
import threading
from semantica.context import ContextGraph

graph = ContextGraph()

def misp_ingest_worker(events):
    for event in events:
        graph.add_node(event["id"], event["type"], event["value"])
        for attr in event.get("attributes", []):
            graph.add_edge(event["id"], attr["value"], "has_attribute")

def nvd_ingest_worker(cves):
    for cve in cves:
        graph.add_node(cve["id"], "Vulnerability", cve["description"], cvss=cve["cvss"])
        graph.add_edge(cve["id"], cve["product"], "affects")

# 两个线程安全地写同一张图
t1 = threading.Thread(target=misp_ingest_worker, args=(misp_events,))
t2 = threading.Thread(target=nvd_ingest_worker, args=(nvd_batch,))
t1.start(); t2.start()
t1.join(); t2.join()

print(graph.stats())
```

锁是可重入的，所以内部会再次获取锁的调用（例如 `add_edge()` 内部调用 `find_node()`）不会死锁。

## 经 AgentContext 做语义检索

`AgentContext` 在图外面包了一层 FAISS 向量索引，可以按语义相似度检索，还可以选择混入图上的邻近度：

```python
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore

graph = ContextGraph()
# ...（已按上文填入 CTI 节点）

context = AgentContext(
    vector_store    = VectorStore(backend="faiss", dimension=768),
    knowledge_graph = graph,
    hybrid_alpha    = 0.5,       # 语义 50% / 结构 50% 加权
    decision_tracking = True,
)

# 存入情报摘要——之后即可被检索
context.store("APT29 operated SUNBURST backdoor via SolarWinds supply chain compromise")
context.store("45.142.212.100 is a C2 server associated with the SUNBURST campaign")
context.store("CVE-2020-10148 allows unauthenticated API access in SolarWinds Orion")

# 混入图邻近度检索
# anchor_node="APT29" 表示图上离 APT29 近的节点得分更高
results = context.retrieve(
    "APT29 infrastructure and C2 servers",
    max_results      = 10,
    anchor_node      = "APT29",
    max_hops         = 2,
    proximity_weight = 0.3,    # 图邻近度 30%，语义得分 70%
    use_graph        = True,
)

for r in results:
    # "score"          —— 基础语义相似度（始终存在）
    # "combined_score" —— 混合得分（proximity_weight > 0 时存在）
    # "distance_band"  —— "direct" / "near" / "mid" / "far"
    score = r.get("combined_score", r.get("score", 0))
    print(f"[{score:.3f}]  {r.get('content', '')[:70]}")
```

`proximity_weight` 是 `retrieve()` 的**逐次调用参数**，不是构造函数设置。也就是说，同一个 context 对象上的不同查询可以用不同的混合比例——宽泛的语义检索用 `proximity_weight=0.0`，聚焦邻域的遍历用 `proximity_weight=0.5`。

## 跨图导航

`link_graph()` 连接两张独立的图，`cross_graph_path()` 查找跨越边界的路径：

```python
from semantica.context import ContextGraph

actor_graph  = ContextGraph()
victim_graph = ContextGraph()

actor_graph.add_node("APT29",    "ThreatActor", "APT29")
actor_graph.add_node("SUNBURST", "Malware",     "SUNBURST backdoor")
actor_graph.add_edge("APT29", "SUNBURST", "uses")

victim_graph.add_node("SolarWinds", "Victim", "SolarWinds Corporation")
victim_graph.add_node("Treasury",   "Victim", "US Department of Treasury")
victim_graph.add_edge("SolarWinds", "Treasury", "supply_chain_compromised")

link_id = actor_graph.link_graph(
    victim_graph,
    "APT29",
    "SolarWinds",
    link_type="targets",
)

other_graph, target_node_id = actor_graph.navigate_to(link_id)

sw = other_graph.find_node(target_node_id)
if sw:
    print("Reached:", sw["id"])

result = actor_graph.cross_graph_path(
    "APT29",
    victim_graph,
    "Treasury",
)

if result.get("reachable"):
    print(f"Reached in {result['hop_count']} hops")
# APT29 → SUNBURST → SolarWinds → Treasury
```

## 序列化与持久化

每轮摄取结束后，把图存到磁盘。重启后恢复——节点和边完整保留：

```python
# 保存
graph.save_to_file("cti_graph.json")

# 恢复
restored = ContextGraph(advanced_analytics=True)
restored.load_from_file("cti_graph.json")

print(restored.stats())

# to_dict() 返回可直接序列化的原始字典
d = graph.to_dict()
# d["nodes"]      → 节点字典列表
# d["edges"]      → 边字典列表
# d["statistics"] → {"node_count": int, "edge_count": int}
```

如果想要人类可编辑、对版本控制友好的表示形式，改存 Markdown 目录：

```python
graph.save_to_file("context_graph/", format="markdown")

restored = ContextGraph(advanced_analytics=True)
restored.load_from_file("context_graph/", format="markdown")
```

该目录包含一个带版本号的 `graph.md` 清单，记录图的标识、关系和跨图链接描述符；`nodes/` 下每个节点一个文件。节点的内容就是 Markdown 正文，而它的 ID、类型、属性、元数据和时态有效期写在 YAML frontmatter 里。节点、边、family、图和跨图链接的 ID 在多次导出导入往返后保持不变。

Markdown 加载采用替换语义，与 `from_dict()` 相同：先解析并校验整个目录，校验通过后才替换当前图。无效 YAML、重复 ID、不支持的版本、不安全的文件系统链接都会让加载失败，且不会对图做任何部分改动。与 JSON 加载一样，边的端点缺少节点文件时会创建 `entity` 占位节点。符号链接、Windows 目录联接（junction）及其他 Windows reparse point 一律拒绝。

向已有的受管目录重新导出时会原子性地整体替换，并删除过期的节点文件。替换之前，Semantica 会校验完整的规范导出布局，而不只看清单头部。因此，未跟踪的文件、资源文件、多余目录或改名后的节点文件都会让导出直接失败，而不是被顺手删掉。附件和手工维护的索引请放在受管导出目录之外。

如果图曾用 `link_graph()` 建过跨图链接，加载后要调用 `resolve_links()` 恢复实时导航——对象引用无法序列化，必须手工重新接线：

```python
g1b, g2b = ContextGraph(), ContextGraph()
g1b.load_from_file("actor_graph.json")
g2b.load_from_file("victim_graph.json")
g1b.resolve_links({g2b.graph_id: g2b})
```

要完整持久化会话（图 + FAISS 向量索引 + 记忆），用 `AgentContext.save()` / `AgentContext.load()`：

```python
context.save("agent_state/")

# 之后重启时：
context2 = AgentContext(
    vector_store    = VectorStore(backend="faiss", dimension=768),
    knowledge_graph = ContextGraph(),
)
context2.load("agent_state/")
```

## 常见陷阱

**实体重复。**把 "APT-29"、"APT29"、"Cozy Bear" 当成三个节点加入，本该是一个实体的东西会把图割裂。提前统一命名规范，或在摄取后用[去重](./deduplication.md)指南里的 `detect_duplicates()` 和 `EntityMerger` 把它们合并。

**命名规范不一致。**"ThreatActor"、"threat_actor"、"Threat-Actor" 混用作节点类型，会破坏按类型过滤的查询。选定一种规范，并在所有数据源上强制执行。

**过度连接节点。**给同一篇文档里提到的所有实体两两建边只会添噪。聚焦有意义的关系——直接因果、成员关系或功能依赖，而不是共同出现。

**存储不必要的信息。**把源数据的每个字段都塞进元数据会撑大内存占用。只保留查询、过滤或下游分析需要的属性。

**忘记持久化重要图状态。**ContextGraph 存在内存里，应用一关，没调 `save_to_file()` 或 `AgentContext.save()` 的话，所有节点和边都会丢失。长时间摄取过程中要定期持久化。

## 图结构与向量检索的关系

ContextGraph 的图结构和向量检索各司其职：

- **图结构**捕捉显式关系，支持遍历、可达性分析和多跳推理
- **向量检索**支持基于内容的语义相似度查询和模糊匹配

两者经 `AgentContext` 配合使用时可以混合：找出语义相似的内容，同时让图上离起点结构更近的结果排名更靠前。

## 领域示例

<Tabs>
  <Tab title="国防 — 威胁情报">
    三个独立的摄取 worker 同时写一张共享的 `ContextGraph`（MISP、NVD、涉密 STIX）。时态有效期保证过期的战役数据不会出现在当前威胁查询里。

```python
from semantica.context import ContextGraph, AgentContext
from semantica.vector_store import VectorStore
from datetime import datetime

graph = ContextGraph(advanced_analytics=True, community_detection=True)

# 核心 CTI 实体
graph.add_node("APT29", "ThreatActor", "Russian GRU unit, COZY BEAR",
               origin="Russia", motivation="espionage")
graph.add_node("SUNBURST", "Malware", "SolarWinds supply chain backdoor",
               family="backdoor", platforms=["Windows"])
graph.add_node("CVE-2020-10148", "Vulnerability",
               "SolarWinds Orion API auth bypass", cvss=10.0)

# 有时限的 C2 基础设施
graph.add_node("avsvmcloud.com", "C2Domain",
               "SUNBURST DNS C2 domain",
               valid_from="2019-10-01T00:00:00",
               valid_until="2020-12-18T00:00:00")

graph.add_edge("APT29",    "SUNBURST",        "deploys",    weight=1.0)
graph.add_edge("SUNBURST", "CVE-2020-10148",  "exploits",   weight=0.95)
graph.add_edge("SUNBURST", "avsvmcloud.com",  "beacons_to", weight=0.9,
               valid_from="2019-10-01T00:00:00",
               valid_until="2020-12-18T00:00:00")

# 此刻有哪些 C2 基础设施仍然活跃？
active_c2 = graph.find_active_nodes(node_type="C2Domain")
print(f"Currently active C2 domains: {len(active_c2)}")
# Currently active C2 domains: 0  — avsvmcloud.com expired in 2020

# 历史查询：战役期间什么在活跃？
campaign_c2 = graph.find_active_nodes(
    node_type="C2Domain",
    at_time=datetime(2020, 6, 1),
)
print(f"C2 domains active June 2020: {len(campaign_c2)}")
# C2 domains active June 2020: 1  — avsvmcloud.com was active

# 遍历：从 APT29 出发的完整影响范围
blast_radius = graph.get_neighbors("APT29", hops=3,
                                   include_distance_metadata=True)
for n in blast_radius:
    print(f"  hop={n['hop']}  decay={n['confidence_decay']:.2f}  {n['id']}")
```

  </Tab>

  <Tab title="安全 — SOC/事件响应">
    事件处置进行中时，主机是节点、观测到的横向连接是边。图会回答哪些主机处在关键路径上，以及从初始立足点出发，攻击者的可达网络长什么样。

```python
from semantica.context import ContextGraph

graph = ContextGraph(advanced_analytics=True)

# 受影响主机
for host in ["ws-finance-04", "srv-dc-01", "srv-file-02",
             "ws-hr-11", "srv-backup-01"]:
    graph.add_node(host, "Host", f"Windows host: {host}")

# 观测到的植入体
graph.add_node("COBALT-STRIKE-BEACON-01", "Implant",
               "Cobalt Strike beacon, staged from ws-finance-04")
graph.add_node("MIMIKATZ-DUMP-01", "Tool",
               "Credential dump observed on srv-dc-01")

# 横向移动边
graph.add_edge("ws-finance-04", "srv-dc-01",               "lateral_move", weight=0.9)
graph.add_edge("srv-dc-01",     "srv-file-02",             "lateral_move", weight=0.85)
graph.add_edge("srv-dc-01",     "srv-backup-01",           "lateral_move", weight=0.8)
graph.add_edge("ws-finance-04", "COBALT-STRIKE-BEACON-01", "hosts",        weight=1.0)
graph.add_edge("srv-dc-01",     "MIMIKATZ-DUMP-01",        "executes",     weight=1.0)

# 从初始立足点出发的影响范围
reachable = graph.get_neighbors("ws-finance-04", hops=3,
                                 relationship_types=["lateral_move"])
print("Reachable via lateral movement:")
for n in reachable:
    print(f"  hop={n['hop']}  {n['id']}")

# 用 path_to_anchor 追溯从初始立足点到备份服务器的路径
all_paths = graph.get_neighbors("ws-finance-04", hops=3,
                                relationship_types=["lateral_move"],
                                include_distance_metadata=True)
for n in all_paths:
    if n["id"] == "srv-backup-01":
        print(" → ".join(n["path_to_anchor"]))
        # ws-finance-04 → srv-dc-01 → srv-backup-01
```

  </Tab>

  <Tab title="生命科学 — 临床/制药">
    临床试验知识图谱追踪药物、生物标志物、患者人群、不良事件和监管里程碑。每个监管里程碑都有有效期——查询必须尊重这些窗口，防止过期的疗效数据与当前安全性结论混在一起被引用。

```python
from semantica.context import ContextGraph
from datetime import datetime

graph = ContextGraph(advanced_analytics=True)

# 实体
graph.add_node("dapagliflozin",     "Drug",        "SGLT2 inhibitor, AstraZeneca")
graph.add_node("HbA1c-reduction",   "Biomarker",   "Primary endpoint: HbA1c change from baseline")
graph.add_node("T2D-adults-65plus", "Population",  "Type 2 diabetes, adults 65+, DECLARE-TIMI 58")
graph.add_node("DKA",               "AdverseEvent","Diabetic ketoacidosis, known SGLT2 risk")

# III 期数据节点——申报受理后生效
graph.add_node("DECLARE-TIMI58-results", "ClinicalData",
               "Phase III CVOT results: dapagliflozin vs placebo",
               phase="III",
               primary_endpoint_met=True,
               valid_from="2019-01-11T00:00:00")   # NEJM 发表日期

graph.add_edge("dapagliflozin",          "HbA1c-reduction",    "primary_endpoint", weight=1.0)
graph.add_edge("dapagliflozin",          "T2D-adults-65plus",  "studied_in",       weight=1.0)
graph.add_edge("dapagliflozin",          "DKA",                "risk_of",          weight=0.7)
graph.add_edge("DECLARE-TIMI58-results", "dapagliflozin",      "evaluates",        weight=1.0)

# 只取截至某一监管评审日期已可用的试验数据
active_data = graph.find_active_nodes(
    node_type="ClinicalData",
    at_time=datetime(2019, 6, 1),
)
print(f"Published trial data available June 2019: {len(active_data)}")
# Published trial data available June 2019: 1

# 遍历：2 跳之内关于 dapagliflozin 已知什么？
drug_neighbors = graph.get_neighbors("dapagliflozin", hops=2)
for n in drug_neighbors:
    print(f"  [{n['relationship']}]  {n['id']}  ({n['type']})")
```

  </Tab>

  <Tab title="银行 — 风控/合规">
    交易对手风险图谱连接银行、SPV、敞口工具、担保人和监管实体。实体带报告期有效期——交易对手的 CDS 敞口节点只在它申报的那个季度内有效。

```python
from semantica.context import ContextGraph
from datetime import datetime

graph = ContextGraph(advanced_analytics=True, community_detection=True)

# 实体
graph.add_node("BankA",      "Counterparty", "Tier-1 bank, EUR exposure 4.2B")
graph.add_node("SPV-EUR-01", "SPV",          "Structured vehicle, BankA sponsored")
graph.add_node("BankB",      "Counterparty", "Tier-2 bank, USD exposure 0.8B")
graph.add_node("CCP-LME",    "CCP",          "Central counterparty — LME metals")

# 2024 年四季度敞口节点——仅在申报季度内有效
graph.add_node("BankA-BankB-CDS-Q42024", "Exposure",
               "CDS notional 400M, BankA writes protection on BankB",
               notional_eur=400_000_000,
               valid_from="2024-10-01T00:00:00",
               valid_until="2024-12-31T23:59:59")

graph.add_edge("BankA",      "SPV-EUR-01",             "sponsors",   weight=1.0)
graph.add_edge("BankA",      "BankB",                  "exposed_to", weight=0.8)
graph.add_edge("BankA",      "BankA-BankB-CDS-Q42024", "holds",      weight=1.0)
graph.add_edge("SPV-EUR-01", "CCP-LME",                "clears_via", weight=0.9)
graph.add_edge("BankB",      "CCP-LME",                "member_of",  weight=1.0)

# 传染路径：如果 BankA 违约，下游是谁？
downstream = graph.get_neighbors("BankA", hops=3, include_distance_metadata=True)
print("Contagion reach from BankA:")
for n in downstream:
    print(f"  hop={n['hop']}  decay={n['confidence_decay']:.2f}  {n['id']}")

# 四季度敞口全貌——只计入 2024 年四季度有效的节点
q4_exposures = graph.find_active_nodes(
    node_type="Exposure",
    at_time=datetime(2024, 11, 15),
)
print(f"\nActive Q4 2024 exposures: {len(q4_exposures)}")

# 从 BankA 出发的可达性：找出压力测试范围内的所有实体
stress_reach = graph.get_neighbors("BankA", hops=2)
print(f"Stress-test reachable entities: {len(stress_reach)}")
for n in stress_reach:
    print(f"  hop={n['hop']}  {n['id']}")
```

  </Tab>
</Tabs>

## 相关指南

- [图分析](./graph-analytics.md) — 在建好的 `ContextGraph` 上做中心性排名、社区发现、节点嵌入和链接预测
- [决策智能](./decision-intelligence.md) — 把决策记录成带类型的节点，做因果链分析、先例检索与策略执行
- [摄取](./ingest.md) — 把 PDF、API、数据库、STIX 包和 RSS 源的数据装入图
- [去重](./deduplication.md) — 插入前检测并合并近似重复节点，防止图碎片化
- [推理](./reasoning.md) — 时态区间代数（Allen 关系）、前向/后向链推理，以及在知识图谱上跑 SPARQL
- [本体管理](./ontology.md) — 从 `graph.to_dict()` 推导形式化 OWL 本体，供下游推理引擎使用
- [Context 模块参考](../reference/context.md) — `AgentContext`、`ContextGraph`、`ContextNode`、`ContextEdge` 的完整 API
