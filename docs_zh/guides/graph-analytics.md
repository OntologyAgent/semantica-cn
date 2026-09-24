---
title: 图分析
description: "如何找出知识图谱中最重要的节点、发现隐藏社区、度量结构相似度并预测缺失的连接——附真实场景示例。"
source: guides/graph-analytics.md
source_version: bbbcf5803bd95cab2fdb61f67e2b8117f014097a
icon: "chart-network"
---

`ContextGraph` 的图分析(Graph Analytics)——中心性(Centrality)、社区发现(Community Detection)、Node2Vec 嵌入、链路预测(Link Prediction)与结构相似度——回答的是图*意味着*什么，而不只是图里装了什么。用 `advanced_analytics=True` 一次性开启，即可给结构上最重要的节点排序、让隐藏的行动集群现形，并在隐含连接被正式观测到之前提前标记。

## 什么是图分析？

图分析用数学算法发现知识图谱(Knowledge Graph)结构中的模式与性质。它超越了存取数据，直接分析关系本身。

**图分析与图遍历的区别**：遍历沿着已有的边找连通节点；图分析审视整张图的结构来发现模式——哪些节点最有影响力、哪些节点群构成社区、哪些连接缺失。

**图分析与推理的区别**：推理应用逻辑规则推导新事实；图分析应用统计与拓扑算法，度量中心性、聚类、相似度等结构性质。

图分析帮你理解数据内部的*形态*和*重要性分布*，揭示单个节点或边看不出的洞见。

## 为什么要用图分析？

**找出有影响力的实体。** 节点的重要性并不均等。图分析能识别哪些实体在网络结构中最居中心、连接最多或占据最有利的战略位置。

**社区发现。** 图分析通过连接密度模式揭示隐藏的集群和行动组织。聚在一起的实体往往共享仅凭元数据看不出的目的、来源或行为。

**关系发现。** 链路预测识别尚未被明确观测到的高概率连接，帮助调查者把精力集中在最可能缺失的关系上。

**调查支持。** 图分析提供重要性与关联度的客观度量，帮助分析师排定调查优先级：先查哪些实体，哪些关系值得深挖。

**风险识别。** 中心性度量能找出一旦移除就会最大程度瓦解网络的实体——理解单点故障、关键基础设施或高影响目标时非常有用。

## 适用与不适用场景

**适合用图分析的场景：**
- 人工检视看不出模式的大型图（100+ 节点）
- 依据结构重要性排定调查优先级
- 发现隐藏社区与行动集群
- 理解网络韧性与脆弱点
- 用链路预测识别缺失关系

**图遍历可能就够用的场景：**
- 追踪特定实体之间的已知关系
- 探索特定节点周围的邻域
- 已知实体之间的寻路

**推理可能就够用的场景：**
- 应用已知逻辑规则推导新事实
- 策略执行与基于规则的决策
- 关系遵循清晰逻辑模式的情形

**简单查询可能就够用的场景：**
- 模式一眼可见的小图
- 直接查找特定实体或关系
- 明确知道自己在找什么的情形

**图分析能创造价值的情形：**
- 需要理解整体结构与模式
- 人工检视会漏掉重要结构性质
- 想发现意料之外的关系或社区
- 需要重要度或相似度的客观度量辅助决策

## 核心分析概念

**模块度(Modularity)**衡量图中社区的定义清晰程度。高模块度（>0.4）表示检测出的社区内部连接密集、对外连接稀少——说明存在真实的组织结构。

**Louvain 社区发现**找出彼此之间的连接比与图其余部分的连接更紧密的节点群。发现行动集群、组织单元或功能群体时很好用。

**Node2Vec** 在图上模拟随机游走(Random Walk)，为节点生成向量嵌入。游走中出现在相似上下文里的节点最终会得到相似的向量，哪怕它们并不直接相连。

**中心性指标**从不同角度度量节点重要性：
- 度(Degree)：有多少直接连接
- 介数(Betweenness)：多少次出现在其他节点的最短路径上
- 特征向量(Eigenvector)：因邻居重要而重要
- PageRank：在图的随机游走中的重要性

<Info>
  所有分析功能都要求在构造时传入 `advanced_analytics=True`。缺了它，本指南中的每个方法都会抛出 `RuntimeError: advanced_analytics not enabled`。该标志会惰性初始化五个子组件：`CentralityCalculator`、`CommunityDetector`、`NodeEmbedder`、`LinkPredictor` 和 `SimilarityCalculator`。
</Info>

## 搭建分析用图

```python
from semantica.context import ContextGraph

graph = ContextGraph(
    advanced_analytics  = True,
    community_detection = True,
    node_embeddings     = True,
)
```

如果从存储加载已有图，也要传同样的标志——子组件会从加载后的图状态初始化，而不是从一张新的空图开始。

## 一次调用拿全景

逐项深入分析之前，先摸清全局。`analyze_graph_with_kg()` 按顺序跑完每一项分析，返回一份统一报告：

```python
report = graph.analyze_graph_with_kg()

print(f"Nodes:       {report['graph_metrics']['node_count']}")
print(f"Edges:       {report['graph_metrics']['edge_count']}")
print(f"Density:     {report['graph_metrics']['density']:.4f}")
print(f"Communities: {len(report['community_analysis'])}")
```

对一张 2,400 节点、8,700 条边的图来说，密度 0.003 完全正常——知识图谱天然稀疏，多数节点只连接一小片邻域，而不是连向所有节点。若密度超过 0.1，大概率是出现了过度连接的枢纽节点，把所有东西都拉到一起，这会扭曲中心性得分。

每个摄取批次结束时跑一次。这次结果就是与下一轮对比的基线——如果两次摄取之间社区数从 12 掉到 4，说明新数据里有东西把原本分开的集群桥接起来了。下一次分析师简报之前，值得把这个信号查清楚。

完整的报告结构：

```text
report
├── "graph_metrics"         → node_count, edge_count, density
├── "centrality_analysis"   → all five measures + per-node rankings
├── "community_analysis"    → detected communities + modularity score
├── "connectivity_analysis" → connected components, diameter, avg path length
├── "node_embeddings"       → node_id → List[float] (Node2Vec vectors)
└── "timestamp"             → ISO datetime of this analysis run
```

## 找出关键节点——中心性分析

节点并非生而平等。中心性分析给每个节点五个不同的分数，各自度量一种重要性。

关键直觉：一个节点可以*度*很低（直接连接很少）但*介数*极高（所有东西都从它过）。这就是**中介节点(broker)**——一旦移除就会把图打碎成互不连通的碎片的节点。在威胁情报里，中介节点往往是基础设施：抗封禁托管(bulletproof hosting)服务商、共享 C2 框架，或每场攻击活动都要经过的中转加载器。

### 给单个节点打分

怀疑某个实体举足轻重时，先直接打分：

```python
scores = graph.get_node_centrality("APT29")

# degree      → 0.0420  (4.2% of nodes are direct neighbors)
# betweenness → 0.1837  (APT29 sits on 18% of all shortest paths)
# closeness   → 0.6123  (average 1.6 hops to any other node)
# eigenvector → 0.8941  (most of APT29's neighbors are themselves well-connected)
# pagerank    → 0.0089  (0.89% of random-walk probability mass lands here)

for measure, score in scores.items():
    print(f"{measure:12s}: {score:.4f}")
```

这里 0.18 的介数得分相当惊人——意味着图中近五分之一的信息流都要 APT29 充当中介。分析师想搞清楚"我们观测到的 TTP 与已知基础设施之间靠什么相连"时，绕不开 APT29。这不只是名气，而是结构性权力。

### 全图批量排名

一次给全部节点按五种度量排名：

```python
from semantica.kg import CentralityCalculator

calc       = CentralityCalculator()
graph_dict = graph.to_dict()

all_measures = calc.calculate_all_centrality(graph_dict)

# 取介数前 5——这些就是你的中介节点
betweenness_rankings = all_measures["centrality_measures"]["betweenness"]["rankings"]
print("Top brokers (betweenness):")
for entry in betweenness_rankings[:5]:
    print(f"  [{entry['score']:.4f}]  {entry['node']}")
```

只关心其中两种度量时，传入子集即可，不必算全五种：

```python
focused = calc.calculate_all_centrality(
    graph_dict,
    centrality_types = ["degree", "pagerank"],
)
```

### 该信哪个指标？

| 想知道什么 | 用哪个指标 |
| :--- | :--- |
| 谁的直接连接最多？ | `degree` |
| 谁被移除后对网络破坏最大？ | `betweenness` |
| 谁能最快触及网络其余部分？ | `closeness` |
| 谁因邻居有影响力而有影响力？ | `eigenvector` |
| 谁在图的随机遍历中重要？ | `pagerank` |

做归因分析时，**特征向量**中心性往往能浮出最有意义的节点——特征向量高意味着你连接着其他特征向量高的节点，在威胁情报里这对应"公认重要"的实体彼此抱团。

## 绘制威胁行为者集群——社区发现

中心性告诉你单个节点的情况；社区发现告诉你*群体*的情况——哪些节点抱成内部连接多于外部连接的紧凑集群。

假设图上有二十个各不相同的威胁行为者(Threat Actor)节点。中心性可以给他们逐一排名，却看不出其中十二个实际上共享基础设施、工具模式和目标行业——俨然一个行动集群——而剩下八个分成另外两拨。社区发现能自动把这些找出来。

```python
from semantica.kg import CommunityDetector

detector   = CommunityDetector()
result     = detector.detect_communities(graph.to_dict(), algorithm="louvain")

communities = result["communities"]       # List[List[str]] — 节点分组
assignments = result["node_assignments"]  # node_id → 社区索引
modularity  = result["modularity"]        # 0.0–1.0 — 划分质量

print(f"Found {len(communities)} communities  (modularity: {modularity:.3f})")

for i, members in enumerate(communities):
    print(f"\n  Community {i} — {len(members)} members")
    print(f"  Sample: {', '.join(members[:4])}")
```

**模块度高于 0.4** 通常即视为有意义——找到的社区并非随机产物。如果图算出 0.71，这是聚类真实存在的强烈信号：你的威胁行为者确实结成了行动集群，而不只是随机关联。

当某个社区把你原以为毫不相干的威胁行为者混在一起时，这就是值得调查的假设。`COZY BEAR`、`VENOMOUS BEAR` 和 `FANCY BEAR` 之所以出现在同一个社区，也许是因为共享 C2 基础设施——尽管传统上它们被归因于不同的 GRU 单位。

立即可视化：

```python
from semantica.visualization import KGVisualizer

viz = KGVisualizer()
viz.visualize_communities(
    graph       = graph,
    communities = communities,
    output      = "interactive",
    file_path   = "threat_clusters.html",
)
```

## 教会图度量距离——Node2Vec 嵌入

中心性和社区发现都是拓扑层面的——它们把边当作二值连接处理。Node2Vec 嵌入走得更深：它在图上模拟数千次随机游走，为每个节点生成稠密向量，学出哪些节点倾向出现在相似的邻域里。

实际效果是：扮演相似*结构角色*的节点在嵌入(Embedding)空间里彼此靠近——即使两者之间没有直接的边。同样处在威胁行为者与受害基础设施之间的两个 C2 域名，即使位于图中完全不同的角落，嵌入也会相似。

```python
from semantica.kg import NodeEmbedder
import numpy as np

embedder   = NodeEmbedder()     # 需要先执行：pip install semantica[embeddings]
embeddings = embedder.compute_embeddings(
    graph_store        = graph,   # ContextGraph 实例——不是 dict
    node_labels        = None,    # None = 嵌入所有节点类型
    relationship_types = None,    # None = 遍历所有边类型
)
# 返回：Dict[str, List[float]] — node_id → 嵌入向量

for node_id, vec in list(embeddings.items())[:3]:
    print(f"{node_id}: dim={len(vec)}, norm={np.linalg.norm(vec):.4f}")
```

这些向量在 Semantica 里是一等公民——它们以 `node2vec_embedding` 的形式存在 `Decision` 节点上，并被 `find_precedents_by_scenario()` 自动用作结构相似度组件。

## 这个攻击模式让我想起了什么？

有了嵌入之后，就可以问："图上哪些节点与 APT29 结构上最相似？"这无关共享的边，而关乎共享的*角色*：还有哪些节点在图中扮演 APT29 的位置？

```python
from semantica.kg import SimilarityCalculator

calc = SimilarityCalculator()

top5 = calc.find_most_similar(
    embeddings      = embeddings,
    query_embedding = embeddings["APT29"],
    top_k           = 5,
)

print("Nodes most similar to APT29 (by structural role):")
for node_id, score in top5:
    print(f"  [{score:.4f}]  {node_id}")
```

如果 `LAZARUS` 和 `APT38` 都以大于 0.85 的相似度排在前列，值得写进分析师报告：这些组织在图中扮演着结构上完全相同的角色，即便传统归因把它们分开，也值得建立统一追踪假设。

直接比较两个节点：

```python
score = calc.cosine_similarity(embeddings["APT29"], embeddings["LAZARUS"])
print(f"Structural similarity APT29 ↔ LAZARUS: {score:.4f}")
```

想要不必预先计算全部嵌入的快捷路径：

```python
similar = graph.find_similar_nodes(
    "APT29",
    similarity_type = "structural",
    top_k           = 5,
)
for r in similar:
    print(f"  [{r['score']:.4f}]  {r['type']:20s}  {r['id']}")
```

## 预判下一步——链路预测

链路预测回答另一个问题：不是"哪些节点相似"，而是"哪些边*缺失*了"？图上两个节点之间没有直接连接，可能不是连接不存在，而是你还没观测到它。

实际场景：你有 `APT29 → uses → SUNBURST` 和 `SUNBURST → targets → Windows Server 2019`。链路预测可能以高分浮出 `APT29 → targets → Windows Server 2019`——这条连接由传递性隐含，只是还没被显式画出。

```python
from semantica.kg import LinkPredictor

predictor   = LinkPredictor()
predictions = predictor.predict_links(graph.to_dict(), top_k=10)

print("Predicted missing links:")
for node1, node2, score in predictions:
    print(f"  [{score:.4f}]  {node1}  →  {node2}")
```

高于 0.8 的分数值得分析师复核——这些不是随机结果，而是现有图拓扑强烈暗示的边。低于 0.5 的属于噪声。人工复核的黄金区间是 0.6–0.8：看起来可信，但尚未证实。

<Info>
  `Decision` 节点上同样可以做链路预测，方法是 `DecisionQuery.predict_decision_relationships(decision_id, top_k)`。如何浮现历史决策之间的因果关系，见[决策智能指南](./decision-intelligence.md)。
</Info>

## 看懂你的决策历史

决策以节点形式存进图后，`get_decision_insights()` 为你提供横跨全部决策的分析视图：

```python
insights = graph.get_decision_insights()

print(f"Total decisions: {insights['total_decisions']}")
print(f"Mean confidence: {insights['confidence_stats']['mean']:.2f}")

print("\nBy category:")
for category, count in sorted(insights["categories"].items(), key=lambda x: -x[1]):
    print(f"  {category:<30} {count}")

print("\nBy outcome:")
for outcome, count in sorted(insights["outcomes"].items(), key=lambda x: -x[1]):
    print(f"  {outcome:<20} {count}")
```

置信度统计最能说明问题：如果均值 0.91 而最小值只有 0.34，说明有人在低置信度下做决策，却仍按最终结论记录在案。治理评审时值得把这个落差标出来。

`insights` 里的 `"advanced_analytics"` 键包含完整的 `analyze_graph_with_kg()` 结果——调用一次 `get_decision_insights()` 就能顺带拿到完整分析全景，无需额外调用。

## 领域示例

<Tabs>

<Tab title="国防——CTI 威胁网络">

你的 SOC 刚把三路威胁情报源汇入同一张 CTI 图。本周分析师简报之前，你需要给最危险的威胁行为者排名、识别隐藏的行动集群，并标记尚未正式追踪的隐含连接。

```python
from semantica.context import ContextGraph
from semantica.kg import CentralityCalculator, CommunityDetector, LinkPredictor
from semantica.visualization import AnalyticsVisualizer

graph = ContextGraph(
    advanced_analytics  = True,
    community_detection = True,
    node_embeddings     = True,
)
# （数据来自 MISP/OTX/OSINT 摄取）

# 全景快照
report = graph.analyze_graph_with_kg()
print(f"Graph: {report['graph_metrics']['node_count']} nodes, "
      f"{report['graph_metrics']['edge_count']} edges")

# 给中介节点排名——打掉谁会让网络四分五裂？
calc     = CentralityCalculator()
measures = calc.calculate_all_centrality(graph.to_dict())
brokers  = measures["centrality_measures"]["betweenness"]["rankings"][:5]

print("\nTop 5 broker nodes (betweenness):")
for entry in brokers:
    print(f"  [{entry['score']:.4f}]  {entry['node']}")

# 找行动集群
detector = CommunityDetector()
result   = detector.detect_communities(graph.to_dict(), algorithm="louvain")
print(f"\n{len(result['communities'])} clusters  "
      f"(modularity {result['modularity']:.3f})")

# 标记隐含连接
predictor   = LinkPredictor()
predictions = predictor.predict_links(graph.to_dict(), top_k=5)
print("\nHigh-confidence implied connections:")
for n1, n2, score in predictions:
    if score > 0.7:
        print(f"  [{score:.3f}]  {n1}  →  {n2}")
```

</Tab>

<Tab title="安全——事件处置进行时">

事件处置进行中，图已长出告警节点、受影响主机、横向移动边和已识别恶意软件。你需要搞清楚影响范围：哪些主机是横向移动链上的结构中介？哪些连接还没有正式记录在案？

```python
from semantica.context import ContextGraph
from semantica.kg import CentralityCalculator, LinkPredictor

graph = ContextGraph(advanced_analytics=True)
# （数据来自 SIEM 告警关联与 EDR 遥测）

calc     = CentralityCalculator()
measures = calc.calculate_all_centrality(graph.to_dict())

# 介数找出支点主机——横向移动的必经之路
pivot_hosts = measures["centrality_measures"]["betweenness"]["rankings"][:5]
print("Pivot hosts (lateral movement brokers):")
for entry in pivot_hosts:
    print(f"  [{entry['score']:.4f}]  {entry['node']}")

# 找出攻击者可能的下一个目标
predictor   = LinkPredictor()
predictions = predictor.predict_links(graph.to_dict(), top_k=10)

print("\nLikely next lateral moves (predicted):")
for src, dst, score in predictions:
    if score > 0.65:
        print(f"  [{score:.3f}]  {src}  →  {dst}")

# 给特定高价值目标打分
dc_scores = graph.get_node_centrality("DC-PROD-01")
print(f"\nDomain Controller centrality:")
print(f"  Betweenness: {dc_scores['betweenness']:.4f}")
print(f"  PageRank:    {dc_scores['pagerank']:.4f}")
# 域控制器上高介数 + 高 PageRank = 确认的支点
```

</Tab>

<Tab title="生命科学——临床试验图">

你的临床试验平台维护着一张图：药物、生物标志物、患者人群、不良事件类型和监管决策。每个试验阶段结束时，你要确认代谢综合征药物集群是否真的与心血管集群相互隔离——这种隔离关系直接影响联合用药风险评估。

```python
from semantica.context import ContextGraph
from semantica.kg import CommunityDetector, NodeEmbedder, SimilarityCalculator

graph = ContextGraph(
    advanced_analytics  = True,
    community_detection = True,
    node_embeddings     = True,
)
# （数据来自试验记录、PubMed 与 FDA 不良事件数据库）

# 找药物-疾病集群
detector = CommunityDetector()
result   = detector.detect_communities(graph.to_dict(), algorithm="louvain")
print(f"Clinical clusters: {len(result['communities'])}  "
      f"(modularity {result['modularity']:.3f})")

# 检查包含达格列净的集群
drug_cluster_idx = result["node_assignments"].get("dapagliflozin")
if drug_cluster_idx is not None:
    cluster_members = result["communities"][drug_cluster_idx]
    print(f"\nCluster containing dapagliflozin ({len(cluster_members)} members):")
    for m in cluster_members[:8]:
        print(f"  {m}")

# 找与达格列净扮演相同结构角色的药物
embedder   = NodeEmbedder()
embeddings = embedder.compute_embeddings(graph_store=graph)
calc       = SimilarityCalculator()

similar_drugs = calc.find_most_similar(
    embeddings      = embeddings,
    query_embedding = embeddings["dapagliflozin"],
    top_k           = 5,
)
print("\nStructurally similar to dapagliflozin:")
for drug, score in similar_drugs:
    print(f"  [{score:.4f}]  {drug}")
```

</Tab>

<Tab title="银行——交易对手风险">

风险管理团队把交易对手关系建模成图：银行、SPV、风险暴露工具和监管实体，通过风险暴露、担保和持股边相连。季度压力测试之前，你要找出哪些实体具有系统重要性——一旦倒下，传染面最广。

```python
from semantica.context import ContextGraph
from semantica.kg import CentralityCalculator, CommunityDetector

graph = ContextGraph(advanced_analytics=True, community_detection=True)
# （数据来自监管申报、交易数据库与内部风险暴露数据）

calc     = CentralityCalculator()
measures = calc.calculate_all_centrality(graph.to_dict())

# 特征向量找出"大到不能倒"——与其他
# 高中心性实体相连的实体
systemic = measures["centrality_measures"]["eigenvector"]["rankings"][:5]
print("Systemically connected entities:")
for entry in systemic:
    print(f"  [{entry['score']:.4f}]  {entry['node']}")

# 介数找出传染中介——一旦违约，就会把风险暴露图
# 原本分开的部分断开的实体
brokers = measures["centrality_measures"]["betweenness"]["rankings"][:5]
print("\nContagion brokers:")
for entry in brokers:
    print(f"  [{entry['score']:.4f}]  {entry['node']}")

# 找风险暴露集群——相互暴露密集的群体
detector = CommunityDetector()
result   = detector.detect_communities(graph.to_dict(), algorithm="louvain")
print(f"\n{len(result['communities'])} exposure clusters  "
      f"(modularity {result['modularity']:.3f})")
```

</Tab>

</Tabs>

## 常见误区

**把预测当事实。** 链路预测和相似度分数是概率估计，不是已证实的关系。高分只说明连接大概率存在，采取行动前仍需人工核实。

**实体重复。**"APT-29"、"APT29" 和 "Cozy Bear" 各立节点，会人为压低它们的中心性得分、割裂社区。跑分析之前先做实体去重，结果才准确。

**命名不一致。**"ThreatActor"、"threat_actor" 和 "Actor" 混用作节点类型，会让按类型分组的分析失效。各数据源之间保持一致的命名约定。

**过度解读分析结果。** 高介数节点只是在当前图中结构上重要，未必在现实中重要。图分析揭示的是数据中的模式，不是领域里的普遍真理。

**在过小的图上跑分析。** 社区发现和中心性度量在 100+ 节点、连接密度足够的图上才最有意义。低于这个阈值的结果未必可靠。

**图质量差。** 实体重复、命名不一致、关系缺失都直接影响分析准确性。跑分析之前先去重、做规范化——算法会放大图中已有的任何结构，噪声也不例外。

## 数字怎么读

| 分数 | 说明 |
| :--- | :--- |
| 介数 > 0.15 | 关键中介——任何归因或根因分析都先查这个节点 |
| 模块度 > 0.4 | 社区是真实的，不是统计噪声——可以相信聚类结果 |
| 模块度 < 0.2 | 图过于稠密，在此层级上难以形成有意义的社区结构 |
| 嵌入余弦相似度 > 0.85 | 两个节点结构上近乎相同——统一追踪假设的有力依据 |
| 链路预测分数 > 0.7 | 这条边几乎必然存在——排入分析师确认队列 |
| 链路预测分数 0.5–0.7 | 可信但不确定——当作假设而非事实 |

## 相关指南

- [上下文图](./context-graphs.md) — 构建与查询底层的 `ContextGraph`
- [可视化](./visualization.md) — 把中心性排名和社区集群渲染成交互式仪表盘
- [决策智能](./decision-intelligence.md) — 链路预测与结构相似度在决策节点上的应用
- [GraphRAG](./graphrag.md) — 用分析结果让 LLM 生成扎根于上下文最相关的子图
