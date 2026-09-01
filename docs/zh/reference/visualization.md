---
title: "可视化模块（Visualization）"
description: "知识图谱、本体、嵌入空间与时态数据的交互式及静态可视化。"
source: reference/visualization.md
source_version: a5d2f2c8ed1b1fa8353ccc1c5d9eb47f071874d9
icon: "chart-bar"
---

**`semantica.visualization`** 把知识图谱、本体、嵌入空间和时态数据渲染为**交互式 HTML 或静态图片**：无需启动完整的 Explorer 服务器：

- `KGVisualizer`：交互式网络图，支持力导向、层级和环形布局
- `EmbeddingVisualizer`：2D/3D UMAP 或 t-SNE 投影，带聚类标签
- `TemporalVisualizer`：时间线视图与跨快照的图演化
- `AnalyticsVisualizer`：中心性得分、社区结构、度分布图表

需要 `plotly`：`pip install plotly`。部分导出器还需要 `matplotlib` 或 `graphviz`。


## 导出的类

| 类 | 职责 |
| :--- | :--- |
| `KGVisualizer` | 交互式网络、社区与子图渲染，支持力导向/层级/环形布局 |
| `OntologyVisualizer` | 从任意本体生成类层级与属性关系图 |
| `EmbeddingVisualizer` | 嵌入空间的 2D/3D UMAP 或 t-SNE 投影，带聚类标签 |
| `SemanticNetworkVisualizer` | 加权语义网络渲染 |
| `AnalyticsVisualizer` | 中心性得分、社区结构、连通性与度分布图表 |
| `TemporalVisualizer` | 时间线视图与跨快照的图演化 |

## 快速开始

<Steps>
  <Step title="渲染一张知识图谱">
    ```python
    from semantica.visualization import KGVisualizer

    viz = KGVisualizer(layout="force", color_scheme="default")

    # Interactive: opens in browser, supports hover and click
    viz.visualize_network(graph, output="interactive")
    ```
  </Step>
  <Step title="应用布局与配色选项">
    ```python
    viz = KGVisualizer(layout="force", color_scheme="vibrant")

    viz.visualize_network(
        graph,
        output="html",
        file_path="graph.html",
        node_color_by="type",      # color nodes by entity type attribute
    )
    ```
  </Step>
  <Step title="导出为静态格式">
    ```python
    # Static PNG: for reports and embedding in documents
    viz.visualize_network(graph, output="png", file_path="graph.png")

    # Vector SVG: for publications and scalable diagrams
    viz.visualize_network(graph, output="svg", file_path="graph.svg")
    ```
  </Step>
</Steps>

<Warning>
  **所有可视化器都需要 `plotly`。** 使用前先安装：`pip install plotly`。未安装 Plotly 时，所有可视化器方法都会抛 `ProcessingError`。
</Warning>

## 可视化器

<Tabs>
  <Tab title="KGVisualizer">
    交互式与静态知识图谱渲染：

    ```python
    from semantica.visualization import KGVisualizer

    viz = KGVisualizer(layout="force", color_scheme="default")

    # Interactive: opens in browser
    viz.visualize_network(graph, output="interactive")

    # Save as HTML file
    viz.visualize_network(graph, output="html", file_path="graph.html")

    # Static PNG
    viz.visualize_network(graph, output="png", file_path="graph.png")

    # Community-colored graph
    viz.visualize_communities(graph, communities, file_path="communities.html")

    # Centrality-sized nodes
    viz.visualize_centrality(graph, centrality, centrality_type="degree")

    # Entity type distribution bar chart
    viz.visualize_entity_types(graph, output="interactive")

    # Relationship frequency heatmap
    viz.visualize_relationship_matrix(graph, output="interactive")
    ```

    <Warning>
      **大图请用 `max_nodes`。** 节点超过约 1,000 个后，力导向布局会变得难以辨认且缓慢。可视化大图前先过滤出子图。
    </Warning>

    <Tip>
      **HTML 输出永远是最佳起点。** 交互式 HTML 支持缩放、平移和悬停查看详情。只有要嵌入报告时才导出 PNG/SVG/PDF。
    </Tip>

    <Tip>
      **要交互式面板，请用 Explorer。** `KGVisualizer.visualize_network()` 生成的是自包含 HTML 文件。Explorer CLI（`semantica-explorer`）提供完整的实时 Web 应用：搜索、过滤、路径查找和 REST API。
    </Tip>

    **布局选项（`layout=`）：**

    | 布局 | 说明 | 适用场景 |
    | :------ | :----------- | :-------- |
    | `force` | 物理模拟：簇自然涌现 | 常规图 |
    | `hierarchical` | 自顶向下的树布局 | 分类体系、组织架构 |
    | `circular` | 节点排成圆环，边呈弦状 | 小型稠密图 |
  </Tab>
  <Tab title="OntologyVisualizer">
    可视化类层级与属性关系：

    ```python
    from semantica.visualization import OntologyVisualizer

    viz = OntologyVisualizer()

    # Class hierarchy tree
    viz.visualize_hierarchy(ontology, output="interactive")

    # Property domain/range graph
    viz.visualize_properties(ontology, output="html", file_path="properties.html")

    # Full structure network (classes + properties)
    viz.visualize_structure(ontology, output="interactive")

    # Class-property matrix heatmap
    viz.visualize_class_property_matrix(ontology, output="html", file_path="matrix.html")

    # Ontology metrics dashboard
    viz.visualize_metrics(ontology, output="interactive")
    ```
  </Tab>
  <Tab title="EmbeddingVisualizer">
    把高维嵌入投影到 2D 做聚类分析：

    ```python
    from semantica.visualization import EmbeddingVisualizer

    viz = EmbeddingVisualizer()

    viz.visualize_2d_projection(
        embeddings=embeddings,
        labels=labels,
        output="interactive",
        file_path="embeddings.html",
        method="umap",    # "umap" | "tsne" | "pca"
    )
    ```

    | 方法 | 速度 | 保留的结构 | 适用场景 |
    | :------ | :----- | :--------- | :-------- |
    | `umap` | 快 | 全局 + 局部结构 | 大数据集、聚类发现 |
    | `tsne` | 中等 | 局部结构 | 紧凑簇的分离 |
    | `pca` | 非常快 | 方差 | 快速总览、线性结构 |

    <Tip>
      **规模大时 UMAP 比 t-SNE 快。** 超过 5,000 个点的嵌入空间，UMAP 几秒完成；t-SNE 可能要几分钟。两者的聚类分离效果都不错。
    </Tip>
  </Tab>
  <Tab title="TemporalVisualizer">
    可视化知识图谱随时间的变化：

    ```python
    from semantica.visualization import TemporalVisualizer

    viz = TemporalVisualizer()

    # Timeline of entity/relationship changes
    viz.visualize_timeline(temporal_data, output="interactive")

    # Animated network evolution: one frame per time step
    viz.visualize_network_evolution(temporal_kg, output="html", file_path="evolution.html")

    # Side-by-side snapshot comparison
    # snapshots: dict mapping timestamp strings to graph dicts
    snapshots = {
        "2023-01": graph_v1,
        "2024-01": graph_v2,
    }
    viz.visualize_snapshot_comparison(snapshots, output="html", file_path="diff.html")

    # Temporal patterns: pass a list of pattern dicts
    viz.visualize_temporal_patterns(patterns, output="html", file_path="patterns.html")

    # Metrics evolution over time
    viz.visualize_metrics_evolution(metrics_history, timestamps, output="interactive")
    ```
  </Tab>
  <Tab title="AnalyticsVisualizer">
    可视化图分析结果：中心性、社区与度分布：

    ```python
    from semantica.visualization import AnalyticsVisualizer

    viz = AnalyticsVisualizer()

    # Bar chart of top-N nodes by centrality measure
    # param is centrality_type= (not metric=) and top_n= (not top_k=)
    viz.visualize_centrality_rankings(
        centrality,
        centrality_type="pagerank",
        top_n=20,
        output="html",
        file_path="centrality.html",
    )

    # Community-colored network graph
    viz.visualize_community_structure(kg, communities, output="html", file_path="communities.html")

    # Degree distribution histogram
    viz.visualize_degree_distribution(kg, output="html", file_path="degree_dist.html")

    # Connectivity analysis (connected/disconnected, component sizes)
    viz.visualize_connectivity(connectivity, output="interactive")

    # Full metrics dashboard (nodes, edges, density, diameter)
    viz.visualize_metrics_dashboard(metrics, output="interactive")

    # Compare multiple centrality measures side-by-side
    viz.visualize_centrality_comparison(centrality_results, top_n=10)
    ```
  </Tab>
</Tabs>

## 配色方案

所有可视化器都接受 `color_scheme=` 构造参数：

```python
viz = KGVisualizer(color_scheme="vibrant")
```

| 方案 | 说明 | 适用场景 |
| :------ | :----------- | :-------- |
| `default` | 蓝灰色系 | 通用 |
| `vibrant` | 高对比、高饱和 | 演示 |
| `pastel` | 柔和、低饱和 | 浅色背景 |
| `dark` | 深色背景配亮色节点 | 暗色模式面板 |
| `light` | 白色背景、细边 | 出版、打印 |
| `colorblind` | Okabe-Ito 安全色板 | 无障碍 |

<Tip>
  **出版物和面板用 `color_scheme="colorblind"`。** Okabe-Ito 色板对所有人都可读，包括约 8% 红绿色盲读者。
</Tip>

## 导出格式

| 格式 | 交互式 | 可缩放 | 适用场景 |
| :------ | :----------- | :-------- | :-------- |
| `.html` | 是 | 不适用 | Web 面板、探索性分析 |
| `.png` | 否 | 否 | 报告、Jupyter notebook |
| `.svg` | 否 | 是 | 出版、幻灯片 |
| `.pdf` | 否 | 是 | 打印、合规导出 |

## 便捷函数

```python
from semantica.visualization import (
    visualize_kg, visualize_ontology, visualize_embeddings,
    visualize_semantic_network, visualize_analytics, visualize_temporal,
)

# Returns Plotly figure or None
fig = visualize_kg(graph, output="interactive", method="default")
fig = visualize_ontology(ontology, output="interactive", method="hierarchy")
fig = visualize_embeddings(embeddings, labels, output="interactive", method="2d_projection")
fig = visualize_analytics(analytics_data, output="interactive", method="centrality")
fig = visualize_temporal(temporal_data, output="interactive", method="timeline")
```

## Graph Explorer（完整面板）

要获得带搜索、路径查找和本体中心(Ontology Hub)的完整浏览器界面，启动 Explorer CLI：

```bash
semantica-explorer --graph my_graph.json
```

完整功能集与 REST API 见 [Explorer 参考](../../reference/explorer.md)。

- [Knowledge Graph](../../reference/kg.md) — 被可视化的图。
- [Ontology](./ontology.md) — 可视化本体的类结构。
- [Embeddings](../../reference/embeddings.md) — 生成此处可视化的嵌入。
- [Explorer](../../reference/explorer.md) — 完整的交互式知识探索界面。
