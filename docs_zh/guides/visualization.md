---
title: 可视化
description: 把知识图谱、本体层级、嵌入投影、图分析结果和时态时间线渲染为交互式 HTML 或静态图片文件。
source: guides/visualization.md
source_version: 2efc2df168faeb0bdc605f0966a8eb31bde01cba
icon: "chart-network"
---

`KGVisualizer`、`AnalyticsVisualizer`、`TemporalVisualizer` 和 `OntologyVisualizer` 只需一次方法调用，就能把图字典、分析结果和本体(Ontology)变成交互式 HTML 仪表盘或静态图片。用它们向干系人展示中心性(Centrality)排名、社区聚类、事件时间线和快照前后对比，完全不用自己写渲染代码。

## 什么是可视化？

可视化把图数据转换成人能看懂的交互式图表、网络图、时间线等视觉形式，把抽象的图结构和分析结果变成能揭示模式、关系与洞察的视觉呈现。

**可视化与分析的分工**：分析负责计算中心性得分、社区归属这类数值指标；可视化则把这些指标画出来——节点按重要性定大小、按社区着色分组。

**可视化与推理的分工**：推理从既有数据推出新的逻辑事实；可视化把已有事实和分析结果以视觉形式呈现，帮助人解读和决策。

有了可视化，人才能看懂那些单凭原始数据很难解读的图结构、分析结果和时序模式。

## 为什么要用可视化？

**可视化探索**：交互式图支持平移、缩放、悬停和过滤，让你探索那些用文本或表格根本没法看的大规模网络。

**调查支撑**：高亮实体之间的路径、按实体类型着色、按重要性定节点大小，帮助分析师发现模式、聚焦调查方向。

**沟通表达**：可视化让不直接碰数据的干系人也能理解复杂的图关系。

**报告输出**：静态可视化能为书面报告、演示材料和监管申报提供证据支撑。

## 适用与不适用场景

**适合用可视化的场景：**
- 向人展示图结构和分析结果
- 在中等规模图（10-1000 个节点）中探索关系与模式
- 为干系人制作报告和演示材料
- 调查图中的特定路径或邻域
- 传达分析或推理工作流的结论

**图遍历可能就够了：**
- 以编程方式探索关系
- 查询特定路径或连接的简单问题
- 不需要人解读的自动化工作流

**分析可能更合适：**
- 计算数值指标和排名
- 以编程方式发现社区或计算中心性得分
- 不需要可视化的定量比较

**推理可能更合适：**
- 通过逻辑推断派生新事实
- 基于规则的决策
- 自动化策略执行

**以下情况可视化就不实用了：**
- 图超过约 1000 个节点（浏览器性能下降）
- 网络太密，视觉上无法解读
- 你需要的是程序化分析，而不是人的解读

## 典型可视化工作流

**图 → 过滤 → 可视化 → 解读 → 调查**

大多数有效的可视化都遵循这个流程：
1. **从你的知识图谱(Knowledge Graph)出发**——来自 `ContextGraph` 或分析结果
2. **过滤出有意义的子图**——别把整张企业级图直接画出来
3. **选合适的可视化形式**——网络图、时间线、热力图或排名图
4. **解读视觉模式**——聚类、中心节点、时序趋势
5. **追查有意思的发现**——深挖意外的模式或离群点

先过滤、再画图，这条原则永远成立。一张 10000 节点的企业图，过滤到中心性最高的 50 个节点、或围绕某个关注实体的子图之后，才有可读性。

<Info>
  **性能警告**：大图（超过 1000 个节点）会拖垮浏览器性能，视觉上也无从下手。交互式网络图最适合 10-1000 个节点。更大的图先用分析找出最重要的子图，再对过滤结果做可视化。
</Info>

<Info>
  所有可视化器都接受 `output="interactive"`（Plotly/pyvis 的 HTML，可在 Jupyter 中显示或存成文件）或 `output="static"`（经 Matplotlib 输出 PNG/SVG）。省略 `file_path` 则返回图形对象，方便继续加工。
</Info>

## 渲染完整知识图谱

最先摆在干系人面前的，是完整的网络——节点按实体类型着色、按度中心性(degree centrality)定大小，悬停时提示框显示内容。

```python
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore
from semantica.visualization import KGVisualizer

graph = ContextGraph(advanced_analytics=True)
ctx   = AgentContext(
    vector_store=VectorStore(backend="faiss", dimension=768),
    knowledge_graph=graph,
    graph_expansion=True,
)
ctx.store([
    "APT29 exploited CVE-2024-3400 targeting NATO defense contractors.",
    "CVE-2024-3400 is a critical vulnerability in PAN-OS by Palo Alto Networks.",
    "HAMMERTOSS is APT29's C2 backdoor operating over Twitter and GitHub.",
    "APT29 conducted the SUNBURST supply chain attack against SolarWinds in 2020.",
], extract_entities=True, extract_relationships=True)

viz = KGVisualizer()

# Interactive network — saved to HTML, opens in any browser
viz.visualize_network(
    graph         = graph.to_dict(),
    output        = "interactive",
    file_path     = "reports/threat_graph.html",
    node_color_by = "type",      # colour each node by its entity type
    node_size_by  = "degree",    # larger nodes = more connections
    hover_data    = ["type", "content"],
)
```

生成的 HTML 完全自包含——不需要任何服务器。当作文件附件发出去，任何浏览器打开就能平移、缩放、悬停。

要一张适合放进 PDF 报告或幻灯片的静态 PNG：

```python
viz.visualize_network(
    graph     = graph.to_dict(),
    output    = "static",
    file_path = "reports/threat_graph.png",
    node_color_by = "type",
)
```

要高亮图中某条归因(attribution)路径——比如从 APT29 经 SUNBURST 到 SolarWinds 的链条——把节点 ID 传给 `highlight_path`：

```python
viz.visualize_network(
    graph          = graph.to_dict(),
    output         = "static",
    file_path      = "reports/apt29_path.png",
    highlight_path = ["APT29", "SUNBURST", "SolarWinds"],
)
```

## 展示社区结构

社区发现(Community Detection)跑完之后，你会拿到一个把社区标签映射到节点 ID 列表的字典。`KGVisualizer` 的 `visualize_communities` 把这些聚类叠加到网络上；`AnalyticsVisualizer.visualize_community_structure` 转发的也是同一个社区图视图。

```python
from semantica.visualization import AnalyticsVisualizer

# The community dict you get from graph analytics
communities = {
    "node_assignments": {
        "apt29": 0,
        "hammertoss": 0,
        "nobelium": 0,
        "sunburst": 0,
        "cve-2024-3400": 1,
        "pan-os": 1,
        "globalprotect": 1,
        "solarwinds": 2,
        "orion-platform": 2,
        "cve-2020-10148": 2,
    },
    "num_communities": 3,
}

# Network view with community colouring
viz.visualize_communities(
    graph       = graph.to_dict(),
    communities = communities,
    output      = "interactive",
    file_path   = "reports/communities_network.html",
)

# Standalone breakdown chart — for a slide on "what are the 12 clusters?"
av = AnalyticsVisualizer()
av.visualize_community_structure(
    graph      = graph.to_dict(),
    communities = communities,
    output     = "interactive",
    file_path  = "reports/communities_breakdown.html",
)
```

## 绘制中心性排名

中心性字典把节点 ID 映射到得分。两次调用覆盖两个用例：一是节点大小反映中心性的网络视图，二是给"连接最多的前 10 个节点"幻灯片用的独立排名条形图。

```python
centrality = {
    "centrality": {
        "apt29": 0.14,
        "cve-2024-3400": 0.11,
        "pan-os": 0.07,
        "hammertoss": 0.06,
        "nobelium": 0.05,
    }
}

# Network coloured and sized by centrality score
viz.visualize_centrality(
    graph          = graph.to_dict(),
    centrality     = centrality,
    centrality_type= "pagerank",
    output         = "interactive",
    file_path      = "reports/centrality_network.html",
)

# Standalone ranked bar chart — most impactful nodes at a glance
av.visualize_centrality_rankings(
    centrality      = centrality,
    centrality_type = "pagerank",
    output          = "interactive",
    file_path       = "reports/centrality_rankings.html",
)
```

## 分析图表：连通性与度分布

跑完图分析(Graph Analytics)之后，再加两张图表，画面就完整了。连通性图表显示图中有多少个互不连通的分量、各有多大；度分布(degree distribution)则展示图的幂律(power-law)形态——可以用来确认你的图是不是无标度(scale-free)的（少数高度连接的中心节点，大量叶子节点）。

```python
# Connectivity — pass the analysis result dict directly
# Keys the visualizer reads: "is_connected", "num_components", "component_sizes"
connectivity = {
    "is_connected":    False,
    "num_components":  3,
    "component_sizes": [42, 8, 2],
}

av.visualize_connectivity(
    connectivity = connectivity,
    output       = "interactive",
    file_path    = "reports/connectivity.html",
)

# Degree distribution — pass the graph dict directly
av.visualize_degree_distribution(
    graph     = graph.to_dict(),
    output    = "interactive",
    file_path = "reports/degree_distribution.html",
)
```

<Info>
  `visualize_connectivity` 接收的是连通性分析的结果字典，不是 `graph.to_dict()`。字典必须包含 `"is_connected"`、`"num_components"` 和 `"component_sizes"`。请先从图分析输出中算出这个结果再传入。
</Info>

## 绘制事件时间线

当你要讲的故事与时间相关——CVE 生命周期、事件处置时间线、攻击战役的推进——`TemporalVisualizer.visualize_timeline` 能把一串带时间戳的事件变成可滚动的交互式图表。

```python
from semantica.visualization import TemporalVisualizer

tv = TemporalVisualizer()

# Events are passed inside a dict under the "events" key
tv.visualize_timeline(
    temporal_data = {"events": [
        {"id": "pub",   "label": "CVE-2024-3400 published",      "timestamp": "2024-03-14T00:00:00"},
        {"id": "exp",   "label": "Zero-day exploitation begins",  "timestamp": "2024-03-26T00:00:00"},
        {"id": "patch", "label": "PAN-OS hotfix released",        "timestamp": "2024-04-14T00:00:00"},
        {"id": "rem",   "label": "Contractor remediation confirmed","timestamp": "2024-04-30T00:00:00"},
    ]},
    output    = "interactive",
    file_path = "reports/cve_timeline.html",
)
```

## 并排对比两张图快照

当问题是"3 月 14 日到 4 月 14 日之间变了什么"，`visualize_snapshot_comparison` 接收 `TemporalVersionManager` 里的两个命名快照，渲染出一张折线图，对比所给快照之间的图指标（实体数、关系数、密度）。

```python
from semantica.change_management import TemporalVersionManager

vm    = TemporalVersionManager(storage_path="versions.db")
snap1 = vm.get_version("pre_patch_march_14")
snap2 = vm.get_version("post_patch_april_14")

# Pass snapshots as a dict mapping label → snapshot dict
tv.visualize_snapshot_comparison(
    snapshots = {
        "pre_patch_march_14":   snap1,
        "post_patch_april_14":  snap2,
    },
    output    = "interactive",
    file_path = "reports/snapshot_diff.html",
)
```

## 追踪图随时间的增长

汇报材料的最后一张图是增长曲线——过去一年图积累了多少节点和边？`visualize_metrics_evolution` 接收一个历史字典和一份与之对应的时间戳列表。

```python
# Build from TemporalVersionManager snapshots
versions = vm.list_versions()
versions.sort(key=lambda v: v["timestamp"])

timestamps      = [v["timestamp"][:10] for v in versions]
metrics_history = {
    "node_count": [len(v.get("nodes", [])) for v in versions],
    "edge_count": [len(v.get("edges", [])) for v in versions],
}

tv.visualize_metrics_evolution(
    metrics_history = metrics_history,
    timestamps      = timestamps,
    output          = "interactive",
    file_path       = "reports/graph_growth.html",
)
```

也可以直接用已知的季度里程碑手工填这个历史字典：

```python
tv.visualize_metrics_evolution(
    metrics_history = {
        "node_count": [50, 142, 309, 481],
        "edge_count": [88, 387, 821, 1340],
    },
    timestamps = ["2025-01-01", "2025-04-01", "2025-07-01", "2025-10-01"],
    output     = "interactive",
    file_path  = "reports/graph_growth.html",
)
```

## 领域示例

<Tabs>

<Tab title="国防——CTI/威胁情报">

一整套分析师简报：交互式威胁网络、社区分布、CVE 时间线和图增长曲线——全部在晨会之前从实时 CTI 图生成。

```python
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore
from semantica.visualization import KGVisualizer, AnalyticsVisualizer, TemporalVisualizer
import os

graph = ContextGraph(advanced_analytics=True)
ctx   = AgentContext(
    vector_store=VectorStore(backend="faiss", dimension=768),
    knowledge_graph=graph,
    graph_expansion=True,
)
ctx.store([
    "APT29 used HAMMERTOSS for C2 via Twitter and GitHub in 2020.",
    "APT29 infrastructure cluster: 185.220.101.0/24, AS200651.",
    "SolarWinds supply chain compromise attributed to APT29, campaign SUNBURST.",
    "APT29 leveraged OAuth token theft against cloud workloads in 2023.",
], extract_entities=True, extract_relationships=True)

os.makedirs("reports", exist_ok=True)

kg_viz = KGVisualizer()

# Full network — interactive for the analyst portal
kg_viz.visualize_network(
    graph         = graph.to_dict(),
    output        = "interactive",
    file_path     = "reports/cti_network.html",
    node_color_by = "type",
    node_size_by  = "degree",
    hover_data    = ["type", "content"],
)

# Attribution path PNG for the slide deck
kg_viz.visualize_network(
    graph          = graph.to_dict(),
    output         = "static",
    file_path      = "reports/apt29_sunburst_path.png",
    highlight_path = ["APT29", "SUNBURST", "SolarWinds"],
)

# Connectivity overview
av = AnalyticsVisualizer()
av.visualize_connectivity(
    connectivity = {"is_connected": True, "num_components": 1, "component_sizes": [24]},
    output       = "interactive",
    file_path    = "reports/connectivity.html",
)

# CVE-2024-3400 incident timeline
tv = TemporalVisualizer()
tv.visualize_timeline(
    temporal_data = {"events": [
        {"id": "pub",   "label": "CVE-2024-3400 published",     "timestamp": "2024-03-14"},
        {"id": "exp",   "label": "Zero-day exploitation",        "timestamp": "2024-03-26"},
        {"id": "patch", "label": "PAN-OS hotfix released",       "timestamp": "2024-04-14"},
        {"id": "rem",   "label": "Remediation confirmed",        "timestamp": "2024-04-30"},
    ]},
    output    = "interactive",
    file_path = "reports/cve_timeline.html",
)
```

</Tab>

<Tab title="安全——SOC/事件响应">

事件处置进行时，SOC 生成一张高亮了攻击路径的横向移动(lateral movement)网络图、一份用来判断哪些主机最关键的中心性排名，以及一张展示"谁连着谁"的关系矩阵。

```python
from semantica.context import ContextGraph
from semantica.visualization import KGVisualizer, AnalyticsVisualizer

graph = ContextGraph(advanced_analytics=True)

for node_id, ntype, content in [
    ("wkstn-047",  "Host",   "Compromised workstation WKSTN-047"),
    ("dc01",       "Host",   "Domain controller DC01"),
    ("jsmith",     "User",   "Compromised user jsmith"),
    ("psexec",     "Tool",   "PsExec lateral movement tool"),
    ("t1021",      "MITRE",  "T1021.002 SMB/Admin Shares"),
]:
    graph.add_node(node_id, ntype, content)

graph.add_edge("wkstn-047", "dc01",    "lateral_movement", weight=1.0)
graph.add_edge("jsmith",    "wkstn-047","session_on",      weight=0.9)
graph.add_edge("psexec",    "wkstn-047","executed_on",     weight=1.0)
graph.add_edge("psexec",    "t1021",   "implements",       weight=0.95)

viz = KGVisualizer()

# Incident network with lateral movement path highlighted
viz.visualize_network(
    graph          = graph.to_dict(),
    output         = "interactive",
    file_path      = "soc/incident_graph.html",
    node_color_by  = "type",
    highlight_path = ["wkstn-047", "dc01"],
    hover_data     = ["type", "content"],
)

# Relationship matrix — who connects to what
viz.visualize_relationship_matrix(
    graph     = graph.to_dict(),
    output    = "interactive",
    file_path = "soc/rel_matrix.html",
)

# Centrality rankings — which host is most pivotal?
av = AnalyticsVisualizer()
av.visualize_centrality_rankings(
    centrality      = {"wkstn-047": 0.35, "dc01": 0.28, "psexec": 0.22, "jsmith": 0.15},
    centrality_type = "degree",
    output          = "interactive",
    file_path       = "soc/centrality.html",
)
```

</Tab>

<Tab title="生命科学——临床/制药">

一次药物重定位(drug repurposing)探索：交互式"药物—靶点—疾病"网络、OWL 类层级、UMAP 嵌入(Embedding)投影，以及一张用于发现结构等价化合物的相似度热力图。

```python
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore
from semantica.visualization import KGVisualizer, EmbeddingVisualizer, OntologyVisualizer
from semantica.ontology import OntologyGenerator
import numpy as np

graph = ContextGraph(advanced_analytics=True)
ctx   = AgentContext(
    vector_store=VectorStore(backend="faiss", dimension=768),
    knowledge_graph=graph,
    graph_expansion=True,
)
ctx.store([
    "Metformin activates AMPK and reduces hepatic glucose production in Type 2 Diabetes.",
    "Dapagliflozin inhibits SGLT2 and reduces cardiovascular mortality in HFrEF.",
    "Semaglutide agonises GLP-1R and reduces HbA1c in obesity and Type 2 Diabetes.",
], extract_entities=True, extract_relationships=True)

kg_viz = KGVisualizer()
kg_viz.visualize_network(
    graph         = graph.to_dict(),
    output        = "interactive",
    file_path     = "drug_kg.html",
    node_color_by = "type",
    node_size_by  = "degree",
)

# OWL class hierarchy
ontology = OntologyGenerator(
    base_uri="https://purl.obolibrary.org/obo/DRUG_",
    min_occurrences=1,
).generate_from_graph(graph.to_dict())

ov = OntologyVisualizer()
ov.visualize_hierarchy(ontology, output="interactive", file_path="drug_hierarchy.html")
ov.visualize_structure(ontology, output="interactive", file_path="drug_ontology.html")

# UMAP projection and similarity heatmap for drug embeddings
embeddings = np.array([[0.1, 0.2, 0.3], [0.15, 0.22, 0.31], [0.8, 0.7, 0.6]])
labels     = ["Metformin", "Dapagliflozin", "Semaglutide"]

ev = EmbeddingVisualizer()
# UMAP (Uniform Manifold Approximation and Projection) reduces high-dimensional 
# embeddings to 2D while preserving local neighborhood structure
ev.visualize_2d_projection(
    embeddings, labels, method="umap",
    output="interactive", file_path="drug_embeddings.html",
)
ev.visualize_similarity_heatmap(
    embeddings, labels,
    output="interactive", file_path="drug_similarity.html",
)
```

</Tab>

<Tab title="银行——风险/合规">

面向模型治理的监管知识图谱：实体网络、用于文档的 OWL 类层级，以及跨越多个季度巴塞尔协议 III 更新的图增长曲线——全部输出为静态 PNG，装进模型治理委员会材料包。

```python
from semantica.context import ContextGraph
from semantica.change_management import TemporalVersionManager
from semantica.visualization import KGVisualizer, TemporalVisualizer, OntologyVisualizer
from semantica.ontology import OntologyGenerator

graph = ContextGraph(advanced_analytics=True)
vm    = TemporalVersionManager(storage_path="regulatory_versions.db")

for node, ntype, content in [
    ("bcbs-cre20",  "Regulation", "Basel III CRE20 — CRE capital requirements"),
    ("metric-ltv",  "Metric",     "Loan-to-Value Ratio"),
    ("metric-dscr", "Metric",     "Debt Service Coverage Ratio"),
    ("metric-pd",   "Metric",     "Probability of Default"),
    ("metric-lgd",  "Metric",     "Loss Given Default"),
]:
    graph.add_node(node, ntype, content)

graph.add_edge("bcbs-cre20", "metric-ltv",  "requires", weight=1.0)
graph.add_edge("bcbs-cre20", "metric-dscr", "requires", weight=1.0)
graph.add_edge("bcbs-cre20", "metric-pd",   "requires", weight=0.9)
graph.add_edge("bcbs-cre20", "metric-lgd",  "requires", weight=0.9)

kg_viz = KGVisualizer()
kg_viz.visualize_network(
    graph         = graph.to_dict(),
    output        = "static",
    file_path     = "regulatory/regulatory_kg.png",
    node_color_by = "type",
    node_size_by  = "degree",
)

# OWL hierarchy — static PNG for the documentation appendix
ontology = OntologyGenerator(
    base_uri="https://basel.eba.eu/ontology/",
    min_occurrences=1,
).generate_from_graph(graph.to_dict())

ov = OntologyVisualizer()
ov.visualize_hierarchy(ontology, output="static", file_path="regulatory/class_hierarchy.png")

# Graph growth curve across quarterly snapshots
tv = TemporalVisualizer()
tv.visualize_metrics_evolution(
    metrics_history = {
        "node_count": [12, 18, 25, 31],
        "edge_count": [8,  15, 24, 32],
    },
    timestamps = ["2025-01-01", "2025-04-01", "2025-07-01", "2025-10-01"],
    output     = "interactive",
    file_path  = "regulatory/graph_growth.html",
)

# Snapshot comparison — what changed between Q2 and Q3 Basel update?
snap1 = vm.get_version("basel_q2_2025")
snap2 = vm.get_version("basel_q3_2025")
if snap1 and snap2:
    tv.visualize_snapshot_comparison(
        snapshots = {"basel_q2_2025": snap1, "basel_q3_2025": snap2},
        output    = "interactive",
        file_path = "regulatory/snapshot_diff.html",
    )
```

</Tab>

</Tabs>

## 常见陷阱

**渲染超大图。** 上千节点的图直接可视化，浏览器会崩，画面也会变成无从解读的毛线团。大图一定要先过滤出有意义的子集再画。

**把视觉上的靠近当成关系存在的证据。** 画得近的两个节点，在图结构里未必关系紧密。布局算法优化的是可读性，不是语义准确性。

**可视化重复或不干净的数据。** 重复实体、命名不一致等数据质量问题会在可视化中被放大。给干系人做视觉呈现之前，先把图数据清理干净。

**提示框塞进超长文本。** 悬停节点时不应展示整篇文档内容。提示框里只放关键元数据——实体类型、名称和核心属性。

**图还没清理就先出图。** 可视化会如实反映数据质量问题。命名混乱、节点重复、关系缺失，画出来的东西只会让人困惑甚至误导。

## 输出模式

每个可视化器方法都接受同样的两种输出模式：

| `output` 取值 | 格式 | 适用场景 |
| :------------- | :----- | :------- |
| `"interactive"` | 自包含 HTML（Plotly / pyvis） | Jupyter notebook、分析师门户、邮件附件 |
| `"static"` | PNG / SVG（Matplotlib） | PDF 报告、幻灯片、监管申报 |

想拿到图形对象而不是写盘，省略 `file_path` 即可：

```python
fig = viz.visualize_network(graph.to_dict(), output="interactive")
fig.show()              # renders inline in Jupyter
fig.write_html("out.html")   # manual export
```

## 相关指南

- [上下文图](./context-graphs.md) — `graph.to_dict()` 是 `KGVisualizer` 的主要输入
- [本体管理](./ontology.md) — `OntologyVisualizer` 渲染 `OntologyGenerator` 生成的本体
- [变更管理](./change-management.md) — `TemporalVersionManager` 的快照供 `visualize_metrics_evolution()` 和 `visualize_snapshot_comparison()` 使用
- [图分析](./graph-analytics.md) — 为 `AnalyticsVisualizer` 供数的中心性得分、社区字典和连通性结果
- [导出与序列化](./export.md) — 把同一张图导出为 GraphML、GEXF 或 DOT，供 Gephi 和 Graphviz 使用
