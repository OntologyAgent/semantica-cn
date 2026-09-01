---
title: "导出模块（Export）"
description: "把知识图谱导出为 RDF、Parquet、LPG、ArangoDB AQL、CSV、GraphML、OWL、JSON-LD、Arrow 和向量格式。"
source: reference/export.md
source_version: eef19e941a4eaed063e00d49d55d8e870c81d11e
icon: "file-export"
---

**`semantica.export`** 把知识图谱序列化成**所有下游格式**：

- RDF：Turtle、JSON-LD、N-Triples、RDF/XML：可选内联 W3C PROV-O 溯源
- 分析：Apache Parquet 和 Arrow，面向 Spark、BigQuery、Databricks
- 图数据库：Neo4j 的 Cypher `CREATE` 语句；ArangoDB 的 AQL `INSERT`
- 标准格式：GraphML、GEXF、Graphviz DOT、CSV、OWL 2.0
- 向量导出：NumPy `.npz`、FAISS 索引、二进制，服务嵌入流水线


## 导出的类

| 类 | 输出格式 | 说明 |
| :--- | :--- | :--- |
| `RDFExporter` | Turtle、JSON-LD、N-Triples、RDF/XML | `export_to_rdf()` → 字符串；`export()` → 文件 |
| `ParquetExporter` | `.parquet` | 需要 `pyarrow`；显式类型化模式 |
| `LPGExporter` | Cypher `CREATE` | 兼容 Neo4j 和 Memgraph |
| `ArangoAQLExporter` | AQL `INSERT` | 顶点和边集合 |
| `GraphExporter` | GraphML、GEXF、Graphviz DOT | 标准图交换格式 |
| `OWLExporter` | Turtle/XML 的 OWL 2.0 | 本体序列化 |
| `CSVExporter` | `.csv` | `export_entities()` 和 `export_relationships()` |
| `VectorExporter` | JSON、NumPy `.npz`、FAISS 索引、二进制 | 嵌入向量导出 |
| `ArrowExporter` | Apache Arrow IPC | 需要 `pyarrow`；零拷贝传输 |
| `DistanceExporter` | CSV、JSONL | 成对距离指标；构造时收 `graph` 参数 |
| `ReportGenerator` | HTML、Markdown、JSON、纯文本 | 分析报告 |
| `NamespaceManager` |: | RDF 命名空间抽取与声明生成 |

## 快速上手

```python
from semantica.export import RDFExporter

# Export a knowledge graph dict to Turtle
exporter = RDFExporter()
rdf_str = exporter.export_to_rdf(graph, format="turtle")
with open("output.ttl", "w") as f:
    f.write(rdf_str)
```

或用一行式便捷函数：

```python
from semantica.export import export_rdf, export_csv, export_lpg

export_rdf(graph,  "output.ttl",    format="turtle")
export_csv(graph,  "output_base")   # writes entities and relationships as CSV
export_lpg(graph,  "import.cypher", method="cypher")
```

## 快速导出

<Steps>
  <Step title="导出为 RDF 字符串">
    ```python
    from semantica.export import RDFExporter

    exporter = RDFExporter()
    rdf_str = exporter.export_to_rdf(graph, format="turtle")
    ```
  </Step>
  <Step title="把 RDF 直接写入文件">
    ```python
    exporter.export(graph, "output.ttl", format="turtle")
    ```
  </Step>
  <Step title="面向分析的列式导出">
    ```python
    from semantica.export import ParquetExporter

    exporter = ParquetExporter(compression="snappy")
    exporter.export_entities(entities, "nodes.parquet")
    exporter.export_relationships(relationships, "edges.parquet")
    ```
  </Step>
  <Step title="图数据库导入">
    ```python
    from semantica.export import LPGExporter

    exporter = LPGExporter()
    exporter.export(graph, "import.cypher")   # Cypher CREATE statements
    ```
  </Step>
</Steps>

## 导出器

<Tabs>
  <Tab title="RDF">
    导出到 W3C RDF 格式：Turtle、JSON-LD、N-Triples 和 RDF/XML。

    **`export_to_rdf()` 返回字符串；`export()` 写文件：**

    ```python
    from semantica.export import RDFExporter

    exporter = RDFExporter()

    # Returns RDF string
    turtle_str  = exporter.export_to_rdf(graph, format="turtle")   # Turtle
    jsonld_str  = exporter.export_to_rdf(graph, format="jsonld")   # JSON-LD
    nt_str      = exporter.export_to_rdf(graph, format="ntriples") # N-Triples
    xml_str     = exporter.export_to_rdf(graph, format="rdfxml")   # RDF/XML

    # Accepted format aliases: "ttl" -> turtle, "nt" -> ntriples, "xml" -> rdfxml,
    # "json-ld" -> jsonld, "rdf" -> rdfxml

    # Write directly to file
    exporter.export(graph, "output.ttl", format="turtle")

    # Also available
    exporter.export_knowledge_graph(graph, "output.ttl", format="turtle")
    ```

    <Warning>
      **`export_to_rdf()` 返回字符串：不写文件。**要直接写盘，调用 `export()` 或 `export_knowledge_graph()`。
    </Warning>

    <Tip>
      **检查用 `export_to_rdf()` + 字符串，生产用 `export()`。**notebook 或调试时，`export_to_rdf()` 方便快速查看。CI 流程和写文件的流水线用 `export()`，一次调用搞定。
    </Tip>

    <Tip>
      **人类可读用 `turtle`，流式处理用 `ntriples`。**Turtle 紧凑可读，适合调试和分享。N-Triples（`.nt`）按行组织：一行一个三元组，可以放心地流式处理、拼接，用标准 Unix 工具加工。
    </Tip>

    **命名空间管理：**

    ```python
    from semantica.export import NamespaceManager, RDFExporter

    ns_manager = NamespaceManager()
    # ns_manager.namespaces contains the built-in prefix dict (rdf, rdfs, owl, xsd, semantica)
    # Add custom namespaces by updating the dict directly
    ns_manager.namespaces["ex"]     = "http://example.org/"
    ns_manager.namespaces["schema"] = "https://schema.org/"

    # Generate Turtle prefix declarations
    decls = ns_manager.generate_namespace_declarations(
        ns_manager.namespaces, format="turtle"
    )
    print(decls)   # @prefix ex: <http://example.org/> .   etc.
    ```

    **时态导出（OWL-Time）：**

    ```python
    # Pass include_temporal=True to embed OWL-Time interval triples
    turtle_str = exporter.export_to_rdf(
        graph,
        format="turtle",
        include_temporal=True,
        time_axis="valid",  # "valid" | "transaction" | "both"
    )
    ```
  </Tab>
  <Tab title="列式与分析">
    ```python
    from semantica.export import ParquetExporter

    exporter = ParquetExporter(compression="snappy")
    # compression: snappy | gzip | brotli | zstd | lz4 | none

    # Export entities and relationships as separate Parquet files
    exporter.export_entities(entities,           "nodes.parquet")
    exporter.export_relationships(relationships, "edges.parquet")

    # Export full knowledge graph (writes entities.parquet and relationships.parquet)
    exporter.export_knowledge_graph(graph, "output_base")
    # → output_base_entities.parquet, output_base_relationships.parquet

    # Generic export from list or dict
    exporter.export(entities, "entities.parquet")
    exporter.export(graph,    "output_base")
    ```

    <Warning>
      **`ParquetExporter` 和 `ArrowExporter` 需要 `pyarrow`。**`pyarrow` 未安装时，两者都退化为 no-op 桩类。使用这些导出器前先 `pip install pyarrow`。
    </Warning>

    <Tip>
      **下游分析用 `ParquetExporter`。**Parquet 保留列类型（int、float、datetime），CSV 会丢失；Spark、BigQuery、Databricks 和 Snowflake 原生支持。`compression="snappy"` 在速度和压缩率之间平衡最好。
    </Tip>

    需要 `pyarrow`：`pip install pyarrow`。模式显式类型化。

    ```python
    from semantica.export import CSVExporter

    exporter = CSVExporter(delimiter=",")
    exporter.export_entities(entities,           "nodes.csv")
    exporter.export_relationships(relationships, "edges.csv")
    exporter.export_knowledge_graph(graph,       "output_base")
    ```

    ```python
    from semantica.export import SemanticNetworkYAMLExporter

    exporter = SemanticNetworkYAMLExporter()
    exporter.export(graph, "graph.yaml")
    ```

    YAML 导出器读取 `entities`/`relationships`/`triplets`（`nodes`/`edges` 作为别名接受，所以 `ContextGraph.to_dict()` 的结果可以直接导出）。非空 mapping 若这些键一个都没有，会抛 `ValidationError`，而不是写出所有集合都为空的文件；集合值不是记录列表（如 `{"entities": "abc"}`）同样如此。
  </Tab>
  <Tab title="图数据库导入">
    **LPGExporter** 为 Neo4j 和 Memgraph 写出 Cypher `CREATE` 语句：

    ```python
    from semantica.export import LPGExporter

    exporter = LPGExporter()

    # Write Cypher CREATE statements to file
    exporter.export(graph, "import.cypher")

    # Also available
    exporter.export_knowledge_graph(graph, "import.cypher")
    ```

    **ArangoAQLExporter** 为 ArangoDB 写出 `INSERT` 语句：

    ```python
    from semantica.export import ArangoAQLExporter

    exporter = ArangoAQLExporter(
        vertex_collection="entities",
        edge_collection="relationships"
    )

    # Write AQL INSERT statements to file
    exporter.export(graph, "import.aql")
    exporter.export_knowledge_graph(graph, "import.aql")
    ```

    两个导出器都写文件并返回 `None`。

    `LPGExporter`、`ArangoAQLExporter` 和 `Neo4jCSVExporter` 按上文 YAML 导出器同样的规则解析 mapping 载荷：无法识别或格式不对的 mapping 会被拒绝，不会导出成一张空图。`Neo4jCSVExporter` 仍从图*对象*的 `nodes`/`entities` 和 `edges`/`relationships` 属性读取数据。

    <Warning>
      **`ArangoAQLExporter.export()` 和 `LPGExporter.export()` 写文件并返回 `None`。**它们不返回 AQL/Cypher 字符串。需要字符串时，先写文件再读回来。
    </Warning>
  </Tab>
  <Tab title="可视化与 OWL">
    ```python
    from semantica.export import GraphExporter

    exporter = GraphExporter()
    exporter.export(graph, "graph.graphml", format="graphml")  # Gephi, yEd
    exporter.export(graph, "graph.gexf",    format="gexf")     # Gephi streaming
    exporter.export(graph, "graph.dot",     format="dot")      # Graphviz
    ```

    ```python
    from semantica.export import OWLExporter

    exporter = OWLExporter()
    exporter.export(ontology, path="ontology.owl", format="owl-xml")
    exporter.export(ontology, path="ontology.ttl", format="turtle")
    ```
  </Tab>
  <Tab title="向量、Arrow 与报告">
    **VectorExporter**：收 `(vectors, file_path, format=)`：

    ```python
    from semantica.export import VectorExporter

    exporter = VectorExporter()
    # vectors: list of dicts with 'id', 'vector', 'text', 'metadata' keys
    exporter.export(vectors, "vectors.json",  format="json")
    exporter.export(vectors, "vectors.npz",   format="numpy")   # NumPy .npz
    exporter.export(vectors, "vectors.bin",   format="binary")
    exporter.export(vectors, "vectors.faiss", format="faiss")
    ```

    **ArrowExporter**：需要 `pyarrow`：

    ```python
    from semantica.export import ArrowExporter

    exporter = ArrowExporter()
    exporter.export(graph, "graph.arrow")
    ```

    **DistanceExporter**：构造时收 `graph` 参数：

    ```python
    from semantica.export import DistanceExporter

    exporter = DistanceExporter(graph)   # graph is required

    # Compute all pairwise distances and write to file
    exporter.to_csv("distances.csv")
    exporter.to_jsonl("distances.jsonl")

    # Compute with column selection and optional node subset
    exporter.to_csv(
        "distances.csv",
        include=["source_id", "target_id", "hop_count", "distance_band"],
        node_subset=["node_a", "node_b", "node_c"],
    )

    # Return as pandas DataFrame (requires pandas)
    df = exporter.to_dataframe(include=["hop_count", "semantic_similarity"])

    # Return as string (for API responses)
    csv_str  = exporter.to_csv_string(node_subset=["node_a", "node_b"])
    jsonl_str = exporter.to_jsonl_string()
    ```

    可用的 `include` 列：`source_id`、`source_type`、`target_id`、`target_type`、`hop_count`、`weighted_distance`、`semantic_similarity`、`distance_band`、`source_betweenness`、`target_betweenness`。

    <Warning>
      **`DistanceExporter` 构造时必须传图。**实例化用 `DistanceExporter(graph)`，不是 `DistanceExporter()`。语义相似度列（`semantic_similarity`）要求图节点的 properties 里有嵌入(embedding)。
    </Warning>

    **ReportGenerator：**

    ```python
    from semantica.export import ReportGenerator

    generator = ReportGenerator()
    generator.generate_report(data, "report.html",  format="html")
    generator.generate_report(data, "report.md",    format="markdown")
    generator.generate_report(data, "report.json",  format="json")
    generator.generate_report(data, "report.txt",   format="text")
    ```
  </Tab>
</Tabs>

## 便捷函数

```python
from semantica.export import (
    export_rdf, export_json, export_parquet, export_csv,
    export_lpg, export_arango, export_graph, export_owl,
    export_vector, export_arrow, export_yaml, generate_report,
)

export_rdf(graph,     "output.ttl",    format="turtle")
export_rdf(graph,     "output.nt",     format="ntriples")
export_json(graph,    "output.json",   format="json")
export_parquet(graph, "output_base",   compression="snappy")
export_csv(graph,     "output_base")   # uses CSVExporter.export()
export_lpg(graph,     "import.cypher", method="cypher")
export_arango(graph,  "import.aql")
export_graph(graph,   "graph.graphml", format="graphml")
export_owl(ontology,  "ontology.owl",  format="owl-xml")
export_vector(vectors,"vectors.json",  format="json")
export_arrow(graph,   "graph.arrow")
export_yaml(graph,    "graph.yaml",    method="semantic_network")
generate_report(data, "report.html",   format="html")
```

`export_csv` 便捷函数委托给 `CSVExporter.export()`。按类型分别导出请直接用类（`exporter.export_entities()`、`exporter.export_relationships()`）。

## 格式参考

| 格式字符串 | 规范名 | 导出器 | 扩展名 | 最适合 |
| :--- | :--- | :--- | :--- | :--- |
| `"turtle"` / `"ttl"` | `turtle` | `RDFExporter` | `.ttl` | 可读 RDF、本体分享 |
| `"jsonld"` / `"json-ld"` | `jsonld` | `RDFExporter` | `.jsonld` | API、关联数据(Linked Data)、JSON 流水线 |
| `"ntriples"` / `"nt"` | `ntriples` | `RDFExporter` | `.nt` | 流式 RDF、逐行处理 |
| `"rdfxml"` / `"xml"` / `"rdf"` | `rdfxml` | `RDFExporter` | `.rdf` | W3C RDF/XML，兼容性最广 |
| `"parquet"` | `parquet` | `ParquetExporter` | `.parquet` | Spark、BigQuery、Databricks、Snowflake |
| `"cypher"` | `cypher` | `LPGExporter` | `.cypher` | Neo4j、Memgraph 导入 |
| `"aql"` | `aql` | `ArangoAQLExporter` | `.aql` | ArangoDB 顶点 + 边集合 |
| `"graphml"` | `graphml` | `GraphExporter` | `.graphml` | Gephi、yEd 可视化 |
| `"gexf"` | `gexf` | `GraphExporter` | `.gexf` | Gephi 流式格式 |
| `"dot"` | `dot` | `GraphExporter` | `.dot` | Graphviz 渲染 |
| `"owl-xml"` | `owl-xml` | `OWLExporter` | `.owl` | OWL 2.0 本体分发 |
| `"csv"` | `csv` | `CSVExporter` | `.csv` | 电子表格、简单流水线 |
| `"yaml"` | `yaml` | `SemanticNetworkYAMLExporter` | `.yaml` | 人类可读的配置驱动场景 |
| `"arrow"` | `arrow` | `ArrowExporter` | `.arrow` | 零拷贝进程间传输 |
| `"json"` | `json` | `VectorExporter` | `.json` | 向量嵌入 |
| `"numpy"` | `numpy` | `VectorExporter` | `.npz` | 嵌入转 NumPy 数组 |
| `"binary"` | `binary` | `VectorExporter` | `.bin` | 原始 float32 二进制 |
| `"faiss"` | `faiss` | `VectorExporter` | `.faiss` | 直接生成 FAISS 索引文件 |
| `"html"` / `"markdown"` / `"json"` / `"text"` |: | `ReportGenerator` | `.html` / `.md` / `.json` / `.txt` | 分析报告 |

<Tip>
  **按消费方选导出格式。**Neo4j → `cypher`；ArangoDB → `aql`；Gephi/yEd → `graphml` 或 `gexf`；语义网工具 → `turtle` 或 `json-ld`；分析流水线 → `parquet`；零拷贝 IPC → `arrow`。
</Tip>

- [Triplet Store](./triplet_store.md) — 把 RDF 导出存进可 SPARQL 查询的后端。
- [Ontology](./ontology.md) — 导出 OWL 本体。
- [Provenance](./provenance.md) — 在 RDF 导出里带上溯源元数据。
- [Pipeline](../../reference/pipeline.md) — 把导出作为流水线最后一步。
