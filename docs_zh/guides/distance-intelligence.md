---
title: 距离智能
description: "把图上的邻近程度划入距离带，沿路径计算置信衰减，运行多算法寻路，并在检索中把语义相似度与结构邻近度融合起来。"
source: guides/distance-intelligence.md
source_version: 132909c183bfaeea472094e1293e3275d2228a1c
icon: "route"
---

`ContextGraph` 的距离智能(Distance Intelligence)回答纯语义相似度答不了的结构问题：给定两个节点，它们在图拓扑、路径权重与推理置信度上到底是什么关系？你可以用它为归因链标注跳数与置信衰减，按结果与锚点节点的结构邻近度为检索排序，并把隐含的连接浮出水面供分析师复核。

## 什么是距离智能？

距离智能量化并分析知识图谱(Knowledge Graph)中节点之间的结构关系。它为图路径提供详细的元数据，包括跳数、距离带、置信衰减与路径分析。

**距离元数据**包括跳数（节点之间的边数）、距离带(Distance Band)（如 "direct"、"near"、"distant" 这样的语义类别）、置信衰减（沿路径累积的信任度）以及路径分析（寻找节点之间的最优路线）。

**跳数**统计从一个节点到另一个节点要经过多少条边。跳数为 1 表示直接相连；跳数为 3 表示中间隔着 2 个节点。

**距离带**把原始跳数换算成有含义的类别："direct"（0–1 跳）、"near"（2–3 跳）、"mid-range"（4–6 跳）和 "distant"（7 跳及以上）。这些类别帮助解读图距离的语义含义。

**置信衰减(Confidence Decay)**把路径上各条边的权重连乘，得到累积信任度。假设每条边权重为 0.8，一条 3 跳路径的置信衰减就是 0.8³ = 0.512，表示这条连接的可信程度中等。

**路径分析**用 Dijkstra 最短路径、Yen k 最短路径等算法找出节点之间的最优路线。

**距离智能与图分析(Graph Analytics)的区别**：图分析在整个图上计算中心性(Centrality)、社区等统计指标；距离智能关注的是特定节点之间的具体路径和关系。

**距离智能与图遍历的区别**：简单遍历沿着边找邻居；距离智能则用权重、路径和衰减指标量化这些连接的质量与置信度。

## 为什么要用距离智能？

**置信度感知检索。**距离智能不会对图上所有连接一视同仁，而是按路径置信度给结果加权——经由更强、更直接的关系连到的节点排名更靠前。

**关系发现。**不仅回答两个实体是否相连，还回答它们怎样相连、经过哪些中介节点、整条路径的置信度有多高。

**因果分析。**在知识图谱中追溯因果链，每一步都有量化的置信度——这对决策追踪和审计轨迹至关重要。

**先例检索。**通过分析结构相似度和路径模式寻找相似的历史案例，而不只是比对内容相似度。

**图感知排序。**把语义相似度与图邻近度融合，让纯向量检索会漏掉的相关结果浮上来。

## 适用与不适用场景

**适合用距离智能的场景：**
- 路径质量至关重要的多跳推理
- 需要置信度评估的归因分析
- 因果链分析与决策追溯
- 从特定锚点节点出发的邻近度加权检索
- 为核实寻找替代连接路线
- 同时按内容相关性与结构邻近度给结果排序

**简单图遍历可能就够用的场景：**
- 找节点的直接邻居
- 不需要置信度加权的基础图探索
- 所有边同等重要的情形
- 简单的可达性查询（A 能否到达 B？）

**可能用不上距离智能的场景：**
- 单跳邻居查询
- 边权重不含有效置信信息的图
- 只问存在性、不评估质量的简单查询
- 路径分析只会徒增复杂度的情形

<Info>
  距离智能为邻近混合检索（`retrieve()` 的 `proximity_weight` 参数）、因果链分析（`trace_decision_causality()`）和进阶先例检索（`find_precedents_hybrid()`）提供支撑。在邻居查询中传入 `include_distance_metadata=True`，或在检索调用中设 `proximity_weight > 0`，即可启用。
</Info>

## 距离带：把跳数变成含义

距离智能的第一个工具是 `classify_path_distance`——它把任意广度优先搜索(BFS)深度映射成人类可读、带有语义的距离带。

```python
from semantica.utils.helpers import classify_path_distance

print(classify_path_distance(0))   # "direct"  — 同一节点
print(classify_path_distance(1))   # "direct"  — 单条边
print(classify_path_distance(2))   # "near"    — 两跳邻域
print(classify_path_distance(3))   # "near"
print(classify_path_distance(5))   # "mid-range"
print(classify_path_distance(9))   # "distant" — 谨慎对待
```

| 距离带 | 跳数范围 | 实际含义 |
| :--- | :-------- | :------------------------ |
| `"direct"` | 0–1 | 直接关系——可作高置信度推理 |
| `"near"` | 2–3 | 两跳邻域——关系紧密，可靠 |
| `"mid-range"` | 4–6 | 可达，但语义上已有距离 |
| `"distant"` | 7+ | 弱耦合——推理结论需谨慎对待 |

凡是使用 `include_distance_metadata=True`、`proximity_weight > 0` 或 `trace_decision_causality()` 的结果都会自动附带这些距离带。无需手工计算——它们直接挂在结果上。

## 置信衰减：信任如何沿路径递减

路径上每经过一跳，累积置信度就乘以一次这条边的权重。这个连乘积——`confidence_decay`——是判断多跳推理是否可信最有用的单一信号。

<Info>
  **置信衰减与边权重：**置信衰减直接取决于图中的边权重。权重应表示置信度、信任度、相关度或类似的领域信号，数值越高关系越强。无权重图（所有边权重均为 1.0）做不出有意义的衰减分析。
</Info>

<Info>
  **稠密图警告：**过于稠密的图会让路径分析的计算开销变高、结果也更难解读。密集的连接产生大量权重相近的路径，使基于距离的排序区分度下降。
</Info>

```python
from semantica.context import ContextGraph

graph = ContextGraph()
graph.add_node("apt29",       "ThreatActor",   "APT29 / NOBELIUM")
graph.add_node("hammertoss",  "Malware",       "HAMMERTOSS C2 tool")
graph.add_node("twitter_c2",  "Infrastructure","APT29 Twitter C2 channel")
graph.add_node("nato_target", "Target",        "NATO defense contractor")

graph.add_edge("apt29",      "hammertoss",  "deploys", weight=0.95)
graph.add_edge("hammertoss", "twitter_c2",  "uses",    weight=0.88)
graph.add_edge("twitter_c2", "nato_target", "reaches", weight=0.80)

# 请求邻居并附带完整距离元数据
neighbors = graph.get_neighbors(
    "apt29",
    hops=3,
    include_distance_metadata=True,
)

for n in neighbors:
    print("{:20s}  band={:10s}  decay={:.3f}  hop={}".format(
        n["id"],
        n["distance_band"],
        n["confidence_decay"],
        n["hop"],
    ))
```

输出：

```text
hammertoss            band=direct     decay=0.950  hop=1
twitter_c2            band=near       decay=0.836  hop=2
nato_target           band=near       decay=0.669  hop=3
```

`nato_target` 节点可达——但置信衰减只有 0.669。也就是说，从 APT29 与这家北约承包商的连接推出的任何结论，都带着在三跳中累积起来的 33% 不确定性。在 "near" 距离带上，这个推论尚可使用；若是在衰减相近的 "distant" 距离带上，就应标记出来交人工复核。

## 获取附带距离元数据的全部邻居

`get_neighbor_distances` 返回给定跳数深度内的所有可达节点，先按最低置信度阈值过滤，再按跳数由近到远排序；同一跳内衰减最强者排前。

```python
neighbors = graph.get_neighbor_distances(
    "apt29",
    hops=4,
    relationship_types=["deploys", "uses", "reaches"],
    min_confidence=0.60,   # 丢弃 confidence_decay < 0.60 的节点
)

# 每个结果 dict 包含：
# "id", "type", "content"    — 节点标识
# "relationship"             — 最后一跳的边类型
# "weight"                   — 最后一跳的边权重
# "hop"                      — 距锚点的 BFS 深度
# "distance_band"            — "direct" / "near" / "mid-range" / "distant"
# "confidence_decay"         — 路径上所有边权重的乘积
# "path_to_anchor"           — 从锚点到该节点的完整节点 ID 列表

for n in neighbors:
    print("[{:10s}] {:20s}  decay={:.3f}  path={}".format(
        n["distance_band"],
        n["id"],
        n["confidence_decay"],
        " → ".join(n["path_to_anchor"]),
    ))
```

## 求两节点之间的最短路径

`PathFinder` 提供五种路径算法。选哪种取决于你需要的是唯一一条最低成本路径、多条备选路径，还是从某个源点出发的全部路径。

```python
from semantica.kg import PathFinder

pf = PathFinder()
```

**Dijkstra——加权最短路径。**默认选它。它找出边权重之和最小的路径。

```python
path = pf.dijkstra_shortest_path(
    graph  = graph,
    source = "apt29",
    target = "nato_target",
)
length = pf.path_length(graph, path)
print("Shortest path:", " → ".join(path))
print("Path length  :", round(length, 3))
```

**BFS——无权最短路径。**只想看跳数最少、不管边权重时用它。

```python
path = pf.bfs_shortest_path(graph, "apt29", "nato_target")
print("Hop count:", len(path) - 1)
```

**k 最短路径——Yen 算法。**Yen 算法找出两节点之间的多条备选路径，按总路径成本排序。需要备选归因链、冗余分析或旁证路线时用它。找出三条最短路径并证明它们都汇聚到同一目标，比单条路径更有说服力。

```python
k_paths = pf.find_k_shortest_paths(graph, "apt29", "nato_target", k=3)

for i, path in enumerate(k_paths, 1):
    length = pf.path_length(graph, path)
    band   = classify_path_distance(len(path) - 1)
    print("Path {} [{}] length={:.3f}: {}".format(
        i, band, length, " → ".join(path)
    ))
```

**从源点出发的全部最短路径。**想摸清从锚点节点出发能到达什么、理解整体结构布局时用它。

```python
all_paths = pf.all_shortest_paths(graph, source="apt29")

for target, paths in all_paths.items():
    path = paths[0]
    print("{:20s}  hops={}  path={}".format(
        target, len(path) - 1, " → ".join(path)
    ))
```

## 邻近混合检索

标准语义检索按结果与查询的文本相似度排序。邻近混合检索(Proximity-Blended Retrieval)引入第二个信号：每个结果在图上与锚点节点的结构距离有多近？`proximity_weight` 参数控制两者的配比。

```python
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore

graph   = ContextGraph(advanced_analytics=True)
context = AgentContext(
    vector_store=VectorStore(backend="faiss", dimension=768),
    knowledge_graph=graph,
    hybrid_alpha=0.5,
)

context.store([
    "APT29 exploited CVE-2024-3400 in PAN-OS targeting NATO governments.",
    "HAMMERTOSS is APT29's C2 tool using Twitter as a covert channel.",
    "SUNBURST was a supply chain implant targeting SolarWinds Orion.",
], extract_entities=True, extract_relationships=True)

# 70% 语义 + 30% 图邻近度，锚定在 APT29
results = context.retrieve(
    "nation-state C2 infrastructure",
    max_results      = 8,
    use_graph        = True,
    anchor_node      = "APT29",
    max_hops         = 3,
    proximity_weight = 0.30,
    min_score        = 0.20,
)

for r in results:
    print("[{:.3f}]  band={:10s}  hop={}  decay={:.3f}  {}".format(
        r.get("combined_score", r["score"]),
        r.get("distance_band",   "-"),
        r.get("hop_distance",    "-"),
        r.get("confidence_decay", 0),
        r["content"][:70],
    ))
```

当 `proximity_weight > 0` 时，每个结果都会多出 `proximity_score`、`combined_score`、`hop_distance`、`distance_band`、`confidence_decay` 和 `path_to_anchor`——每条结果为什么排在这个位置，一目了然。

## 寻找结构相似的节点

想知道图上还有哪些节点的行为与给定节点相似——连通模式相同或文本相近——`find_similar_nodes` 提供了 `ContextGraph` 当前实现的几种模式。

```python
# 内容相似——基于节点内容字段的文本重叠
content_similar = graph.find_similar_nodes(
    "CVE-2024-3400",
    similarity_type = "content",
    top_k           = 5,
)

# 结构相似——邻域拓扑相似的节点
struct_similar = graph.find_similar_nodes(
    "CVE-2024-3400",
    similarity_type = "structural",
    top_k           = 5,
)

for n in content_similar:
    print("[{:.3f}] {}  {}".format(n["score"], n["type"], n["id"]))
```

`similarity_type="content"` 比较节点文本与内容，`similarity_type="structural"` 比较邻域拓扑。其他取值目前会回落到内容相似度，所以 `"embedding"` 请留给更底层的 KG API，别用在 `ContextGraph.find_similar_nodes()` 上。

## 领域示例

<Tabs>

<Tab title="国防——CTI/威胁情报">

找出从 C2 IP 到威胁行为者(Threat Actor)的主归因路径，再找出所有备选旁证路径，在结论进入情报产品之前夯实归因依据。

```python
from semantica.context import ContextGraph
from semantica.kg import PathFinder
from semantica.utils.helpers import classify_path_distance

graph = ContextGraph(advanced_analytics=True)

for node_id, ntype, content in [
    ("apt29",       "ThreatActor",   "APT29 / NOBELIUM / Cozy Bear"),
    ("hammertoss",  "Malware",       "HAMMERTOSS C2 backdoor"),
    ("twitter_c2",  "Infrastructure","APT29 Twitter C2 (steganography)"),
    ("github_c2",   "Infrastructure","APT29 GitHub dead-drop resolver"),
    ("as200651",    "Network",       "APT29 hosting cluster AS200651"),
    ("nato_gov",    "Target",        "NATO government agency"),
]:
    graph.add_node(node_id, ntype, content)

graph.add_edge("apt29",     "hammertoss",  "deploys",   weight=0.95)
graph.add_edge("hammertoss","twitter_c2",  "c2_via",    weight=0.88)
graph.add_edge("hammertoss","github_c2",   "c2_via",    weight=0.82)
graph.add_edge("twitter_c2","as200651",    "hosted_on", weight=0.90)
graph.add_edge("github_c2", "as200651",    "resolves",  weight=0.76)
graph.add_edge("as200651",  "nato_gov",    "targets",   weight=0.85)

pf = PathFinder()

# 主归因路径
primary = pf.dijkstra_shortest_path(graph, "apt29", "nato_gov")
length  = pf.path_length(graph, primary)
band    = classify_path_distance(len(primary) - 1)
print("Primary [{}] length={:.3f}: {}".format(band, length, " → ".join(primary)))

# 三条旁证路径
k_paths = pf.find_k_shortest_paths(graph, "apt29", "nato_gov", k=3)
for i, path in enumerate(k_paths, 1):
    l = pf.path_length(graph, path)
    b = classify_path_distance(len(path) - 1)
    print("Alt {}: {} [{}, length={:.3f}]".format(i, " → ".join(path), b, l))

# APT29 可达且置信度 >= 60% 的全部节点
neighbors = graph.get_neighbor_distances("apt29", hops=4, min_confidence=0.60)
print("\nReachable from APT29 (confidence >= 60%):")
for n in neighbors:
    print("  [{:10s}]  decay={:.3f}  {}".format(
        n["distance_band"], n["confidence_decay"], n["id"]
    ))
```

</Tab>

<Tab title="安全——SOC/事件响应">

绘制横向移动(Lateral Movement)攻击图，找出攻击者通往域控制器的所有备选路线，并按置信衰减给每条路线打分，据此决定先封堵哪条。

```python
from semantica.context import ContextGraph
from semantica.kg import PathFinder

graph = ContextGraph()

for node_id, ntype, content in [
    ("attacker_ip", "ExternalHost", "Attacker 185.220.101.47"),
    ("wkstn047",    "Host",         "Compromised workstation WKSTN-047"),
    ("svc_backup",  "Account",      "Stolen service account SVC-BACKUP"),
    ("jump_server", "Host",         "Jump server JUMP-01"),
    ("dc01",        "Host",         "Domain controller DC01"),
    ("ad_forest",   "Asset",        "Active Directory forest root"),
]:
    graph.add_node(node_id, ntype, content)

graph.add_edge("attacker_ip","wkstn047",    "initial_access",   weight=0.90)
graph.add_edge("wkstn047",   "svc_backup",  "credential_theft", weight=0.85)
graph.add_edge("svc_backup", "jump_server", "lateral_move",     weight=0.78)
graph.add_edge("jump_server","dc01",        "lateral_move",     weight=0.88)
graph.add_edge("wkstn047",   "dc01",        "direct_smb",       weight=0.60)
graph.add_edge("dc01",       "ad_forest",   "controls",         weight=0.98)

pf = PathFinder()

# 通往 DC01 的全部路线——先封堵哪条？
routes = pf.find_k_shortest_paths(graph, "attacker_ip", "dc01", k=3)
for i, route in enumerate(routes, 1):
    length = pf.path_length(graph, route)
    print("Route {} (length={:.3f}): {}".format(i, length, " → ".join(route)))

# DC01 一旦失陷会暴露什么？
exposed = graph.get_neighbor_distances("dc01", hops=2, min_confidence=0.70)
for n in exposed:
    print("Exposed: {:15s}  [{:8s}]  decay={:.3f}".format(
        n["id"], n["distance_band"], n["confidence_decay"]
    ))
```

</Tab>

<Tab title="生命科学——临床/制药">

绘制药物-酶抑制链，计算多步代谢通路的置信衰减，并用邻近混合检索找出结构上最相关的药物相互作用证据。

```python
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore
from semantica.kg import PathFinder

graph   = ContextGraph(advanced_analytics=True)
context = AgentContext(
    vector_store=VectorStore(backend="faiss", dimension=768),
    knowledge_graph=graph,
    graph_expansion=True,
)

for node_id, ntype, content in [
    ("warfarin",    "Drug",   "Warfarin — anticoagulant, narrow therapeutic window"),
    ("amiodarone",  "Drug",   "Amiodarone — antiarrhythmic"),
    ("cyp2c9",      "Enzyme", "CYP2C9 — hepatic cytochrome P450"),
    ("bleeding",    "ADE",    "Major bleeding adverse event"),
    ("cyp3a4",      "Enzyme", "CYP3A4 — major metabolising enzyme"),
    ("simvastatin", "Drug",   "Simvastatin — HMG-CoA reductase inhibitor"),
]:
    graph.add_node(node_id, ntype, content)

graph.add_edge("amiodarone", "cyp2c9",     "inhibits",    weight=0.92)
graph.add_edge("cyp2c9",     "warfarin",   "metabolises", weight=0.95)
graph.add_edge("warfarin",   "bleeding",   "risk_of",     weight=0.88)
graph.add_edge("amiodarone", "cyp3a4",     "inhibits",    weight=0.80)
graph.add_edge("cyp3a4",     "simvastatin","metabolises", weight=0.90)

pf = PathFinder()

# 相互作用链：胺碘酮 → 出血（3 跳，decay = 0.92 × 0.95 × 0.88 = 0.769）
path   = pf.dijkstra_shortest_path(graph, "amiodarone", "bleeding")
length = pf.path_length(graph, path)
print("Interaction chain: {} (length: {:.3f})".format(" → ".join(path), length))

# 从胺碘酮出发的所有路径——它能到达什么？
all_paths = pf.all_shortest_paths(graph, "amiodarone")
for target, paths in all_paths.items():
    p = paths[0]
    print("  {:15s}  hops={} path={}".format(target, len(p)-1, " → ".join(p)))

# 锚定在胺碘酮上的邻近混合检索
context.store([
    "CYP2C9 inhibition by amiodarone reduces warfarin metabolism, raising INR.",
    "Patients on warfarin and amiodarone have 4-fold increased major bleeding risk.",
], extract_entities=True, extract_relationships=True)

results = context.retrieve(
    "anticoagulant enzyme inhibition",
    anchor_node      = "amiodarone",
    max_hops         = 3,
    proximity_weight = 0.35,
    max_results      = 5,
)
for r in results:
    print("[{:.3f}]  {:10s}  {}".format(
        r.get("combined_score", r["score"]),
        r.get("distance_band", "-"),
        r["content"][:80],
    ))
```

</Tab>

<Tab title="银行——风险/合规">

量化从宏观冲击到具体贷款组合的因果距离，找出全部风险暴露路线，并把压力测试决策连同完整因果链标注一起记录在案。

```python
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore
from semantica.kg import PathFinder
from semantica.utils.helpers import classify_path_distance

graph   = ContextGraph(advanced_analytics=True)
context = AgentContext(
    vector_store=VectorStore(backend="faiss", dimension=768),
    knowledge_graph=graph,
    graph_expansion=True,
    decision_tracking=True,
)

for node_id, ntype, content in [
    ("rate_hike",      "MacroEvent", "Central bank +300bps rate cycle"),
    ("real_estate",    "Sector",     "UK residential real estate"),
    ("cre_sector",     "Sector",     "UK commercial real estate"),
    ("ltv_stress",     "RiskFactor", "LTV ratios deteriorate under higher rates"),
    ("dscr_stress",    "RiskFactor", "DSCR falls below 1.0 at +300bps"),
    ("resi_portfolio", "Portfolio",  "Retail mortgage book £4.2bn"),
    ("cre_portfolio",  "Portfolio",  "CRE lending book £1.8bn"),
    ("provision",      "Impact",     "Expected credit loss provision increase"),
]:
    graph.add_node(node_id, ntype, content)

graph.add_edge("rate_hike",    "real_estate",    "depresses", weight=0.88)
graph.add_edge("rate_hike",    "cre_sector",     "depresses", weight=0.85)
graph.add_edge("real_estate",  "ltv_stress",     "causes",    weight=0.78)
graph.add_edge("cre_sector",   "dscr_stress",    "causes",    weight=0.82)
graph.add_edge("ltv_stress",   "resi_portfolio", "exposes",   weight=0.90)
graph.add_edge("dscr_stress",  "cre_portfolio",  "exposes",   weight=0.88)
graph.add_edge("resi_portfolio","provision",      "increases", weight=0.75)
graph.add_edge("cre_portfolio", "provision",      "increases", weight=0.80)

pf = PathFinder()

# 加息如何传导到 ECL 拨备？
k_routes = pf.find_k_shortest_paths(graph, "rate_hike", "provision", k=3)
for i, route in enumerate(k_routes, 1):
    length = pf.path_length(graph, route)
    hops   = len(route) - 1
    band   = classify_path_distance(hops)
    print("Route {} [{:10s}] length={:.3f}: {}".format(
        i, band, length, " → ".join(route)
    ))

# 完整的风险暴露地图
exposed = graph.get_neighbor_distances("rate_hike", hops=5, min_confidence=0.65)
print("\nRisk exposure map from rate hike:")
for n in exposed:
    print("  [{:10s}]  decay={:.3f}  {}".format(
        n["distance_band"], n["confidence_decay"], n["id"]
    ))

# 记录并追溯压力测试决策
dec_id = context.record_decision(
    category       = "stress_test",
    scenario       = "+300bps rate shock — portfolio stress test Q3 2025",
    reasoning      = "LTV deterioration on resi book within tolerance; CRE DSCR breach requires provisioning",
    outcome        = "increase_provision_cre_book",
    confidence     = 0.87,
    decision_maker = "risk_model_v3",
)

chains = graph.trace_decision_causality(dec_id, max_depth=5)
for chain in chains:
    print("\nCausal chain ({} hops, {}, decay={:.3f}):".format(
        chain["hop_count"], chain["distance_band"], chain["confidence_decay"]
    ))
    print("  Interpretation:", chain["interpretation"])
```

</Tab>

</Tabs>

## 常见误区

**把置信衰减当统计概率。**置信衰减是基于边权重的启发式度量，不是统计概率。0.6 的衰减值不代表"60% 的概率"——它表示的是按你领域内权重设定得出的路径强度。

**用无权图还指望有意义的衰减。**如果所有边权重都是 1.0，无论路径多长，置信衰减永远是 1.0，路径之间毫无区分度。请赋予能反映关系强度的有效权重。

**在稠密图上做过度的路径探索。**节点高度互联的稠密图会生成指数级数量的路径。请限制 `max_hops`、设置 `min_confidence` 阈值，并考虑简单邻居查询是否已经够用。

**简单邻居查询就够时过度使用距离分析。**如果只需要直接邻居或单跳连接，基础图遍历比完整的距离智能分析更简单、更快。

**拉取过大的图邻域。**`max_hops` 取值过大会检索出海量子图，压垮下游处理。从 2–3 跳起步，仅在具体场景确有需要时再调大。

## 相关指南

- [上下文图](./context-graphs.md) — `ContextGraph` 的节点与边模型；`add_edge(weight=...)` 为置信衰减提供输入
- [图分析](./graph-analytics.md) — 中心性、社区发现、Node2Vec 嵌入、链路预测
- [智能体记忆](./agent-memory.md) — 邻近混合检索（`proximity_weight`）把距离智能融入记忆搜索
- [决策智能](./decision-intelligence.md) — 用 `trace_decision_causality()` 获得带距离标注的因果链
- [推理与规则](./reasoning.md) — 用 `TemporalReasoningEngine` 对带时间边界的图节点做 Allen 区间代数运算
