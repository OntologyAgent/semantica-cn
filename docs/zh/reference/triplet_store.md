---
title: "三元组存储模块（Triplet Store）"
description: "内嵌与服务器形态的 RDF 存储，支持 SPARQL 查询和批量加载。"
source: reference/triplet_store.md
source_version: ee5c24e6f96867ead1f80ec11f31aa186fc62107
icon: "table"
---

`semantica.triplet_store` 提供 **W3C 标准 RDF 存储**，支持 **SPARQL 1.1** 查询。需要**语义网兼容**、OWL 风格推理、基于 SPARQL 的查询或符合标准的 RDF 序列化时用它。

## 导出的类

| 类 | 职责 |
| :---- | :--- |
| `TripletStore` | 统一接口：`add_triplet`、`add_triplets`、`get_triplets`、`delete_triplet`、`execute_query` |
| `QueryEngine` | **SPARQL 1.1** 执行，带查询优化和结果缓存 |
| `BulkLoader` | 大批量 RDF 加载：分批、重试、进度跟踪 |
| `BlazegraphStore` | Blazegraph REST API：SPARQL 1.1 Update、命名空间管理 |
| `JenaStore` | Apache Jena：rdflib 实现，经远程端点支持 SPARQL 读 |
| `RDF4JStore` | Eclipse RDF4J：REST API、事务支持 |
| `OxigraphStore` | 内嵌 SPARQL 1.1 存储：内存和落盘两种模式 |

## 你能得到什么

- **TripletStore** — 跨内嵌 Oxigraph、Blazegraph、Apache Jena、RDF4J 的统一接口：换一个参数即可切换后端。
- **SPARQL** — 经 `execute_query()` 完整支持 SPARQL SELECT、ASK、CONSTRUCT、UPDATE。
- **批量加载** — `add_triplets()` 分批写入，批量大小、重试逻辑、进度跟踪均可配置。
- **SKOS 词表** — 内置辅助方法：`add_skos_concept()` 和 `get_skos_concepts()`，管理受控词表。
- **命名图(Named Graphs)** — Oxigraph、Blazegraph、RDF4J 支持经 `execute_query()` 的 `graph=` 参数做命名图作用域。
- **差量计算** — `compute_delta(old_graph_uri, new_graph_uri)` 返回两个命名图快照之间新增和删除的三元组。

## 快速开始

**`TripletStore`** 包装你选择的后端。构造 `Triplet` 对象（来自 `semantica.semantic_extract.types`）然后调 `add_triplet()`：

```python
from semantica.triplet_store import TripletStore
from semantica.semantic_extract.types import Triplet

store = TripletStore(
    backend="blazegraph",
    endpoint="http://localhost:9999/blazegraph/sparql"
)

# Create and store a single triplet
t = Triplet(
    subject="http://example.org/apple_inc",
    predicate="http://example.org/founded_by",
    object="http://example.org/steve_jobs",
)
store.add_triplet(t)

# Query with SPARQL: returns a QueryResult with a .bindings list
result = store.execute_query("""
    PREFIX ex: <http://example.org/>
    SELECT ?person ?company WHERE {
        ?person ex:founded ?company .
    }
""")

for row in result.bindings:
    person  = row.get("person",  {}).get("value")
    company = row.get("company", {}).get("value")
    print(person, company)
```

## 上手步骤

<Steps>
  <Step title="连接后端">
    ```python
    from semantica.triplet_store import TripletStore

    store = TripletStore(
        backend="blazegraph",
        endpoint="http://localhost:9999/blazegraph/sparql"
    )
    ```
  </Step>
  <Step title="添加三元组">
    ```python
    from semantica.semantic_extract.types import Triplet

    # Add a single triplet
    store.add_triplet(Triplet(
        subject="http://example.org/apple_inc",
        predicate="http://example.org/founded_by",
        object="http://example.org/steve_jobs",
    ))

    # Bulk-add a list of Triplet objects
    store.add_triplets(triplets, batch_size=500)
    ```
  </Step>
  <Step title="用 SPARQL 查询">
    ```python
    # execute_query returns a QueryResult: iterate result.bindings
    result = store.execute_query("""
        PREFIX ex: <http://example.org/>
        SELECT ?person ?company WHERE {
            ?person ex:founded ?company .
            ?company ex:located_in ex:SiliconValley .
        }
    """)

    for row in result.bindings:
        print(row.get("person",  {}).get("value"))
        print(row.get("company", {}).get("value"))
    ```
  </Step>
  <Step title="存入整张知识图谱">
    ```python
    # store(knowledge_graph, ontology) converts entities/relationships
    # to RDF triples and bulk-loads them in one call
    store.store(knowledge_graph=kg_dict, ontology=ontology_dict)
    ```
  </Step>
</Steps>

## 后端

<Tabs>
  <Tab title="Oxigraph">
    ```bash
    pip install "semantica[tripletstore-oxigraph]"
    ```

    ```python
    # In-memory: no server process or files required
    store = TripletStore(backend="oxigraph")

    # Persistent: reopen the same directory to reuse the data
    persistent_store = TripletStore(
        backend="oxigraph",
        path="./data/knowledge-graph",
    )
    ```

    **最适合：** 本地开发、CI、桌面应用，以及不依赖外部基础设施的持久单进程负载。
  </Tab>
  <Tab title="Blazegraph">
    ```bash
    pip install requests
    ```

    ```python
    from semantica.triplet_store import TripletStore

    store = TripletStore(
        backend="blazegraph",
        endpoint="http://localhost:9999/blazegraph/sparql",
        namespace="kb",      # default: "kb"
        timeout=30,          # request timeout in seconds
    )
    ```

    **最适合：** Wikidata 风格的负载、海量三元组、命名图支持、SPARQL 1.1 Update。
  </Tab>
  <Tab title="Apache Jena">
    ```bash
    pip install rdflib
    ```

    ```python
    store = TripletStore(
        backend="jena",
        endpoint="http://localhost:3030/ds",   # SPARQL read endpoint for rdflib SPARQLStore
    )
    ```

    **最适合：** 基于 rdflib 的本地开发，对 Fuseki 端点做 SPARQL 读查询。

    <Warning>
      **`backend="jena"` 的 OWL 推理是占位实现。** `enable_inference=True` 能传入，但推理调用返回 0 条推断三元组。生产环境 OWL 推理请直接用 Jena Fuseki 及其内置 reasoner 配置。
    </Warning>
  </Tab>
  <Tab title="RDF4J">
    ```bash
    pip install requests
    ```

    ```python
    store = TripletStore(
        backend="rdf4j",
        endpoint="http://localhost:8080/rdf4j-server",
        repository_id="semantica",   # selects the remote repository
    )
    ```

    **最适合：** Eclipse Foundation 系部署，经 REST API 做事务化加载。
  </Tab>
  <Tab title="后端对比">

    | 后端 | 许可证 | 命名图 | 写入方式 | 最适合 |
    | :------- | :------- | :------------ | :--------- | :-------- |
    | Oxigraph | Apache 2.0 / MIT | 支持 | 内嵌原生 API | 本地、CI、落盘 |
    | Blazegraph | 开源 | 支持 | SPARQL Update REST | 海量三元组、SPARQL 1.1 |
    | Apache Jena | Apache 2.0 | 不支持（rdflib 后端） | rdflib 进程内 | 本地开发、读查询 |
    | RDF4J | Eclipse 1.0 | 支持 | REST API N-Triples | 企业 Java、事务 |

  </Tab>
</Tabs>

<Tip>
  **零基础设施的开发和本地持久化用 Oxigraph。**分布式生产部署换 `backend=` 即可切到服务器形态的存储。
</Tip>

## Triplet 对象

所有 store 操作都用 `semantica.semantic_extract.types` 里的 `Triplet` dataclass：

```python
from semantica.semantic_extract.types import Triplet

t = Triplet(
    subject="http://example.org/apple_inc",     # required: full URI string
    predicate="http://example.org/founded_by",  # required: full URI string
    object="http://example.org/steve_jobs",     # required: URI or literal string
    confidence=0.95,                            # optional: float 0.0–1.0, default 1.0
    metadata={"source": "wikipedia"},           # optional: dict
)
```

| 字段 | 类型 | 默认值 | 说明 |
| :----- | :---- | :------- | :----------- |
| `subject` | `str` | **必填** | 主语 URI |
| `predicate` | `str` | **必填** | 谓语 URI |
| `object` | `str` | **必填** | 宾语 URI 或字面量 |
| `confidence` | `float` | `1.0` | 置信度得分（0–1） |
| `metadata` | `dict` | `{}` | 任意元数据 |

<Warning>
  **`add_triplet()` 接受 `Triplet` 对象，不接受关键字参数。**用 `semantica.semantic_extract.types` 的 `Triplet(subject=..., predicate=..., object=...)` 构造后传对象：不要给 `add_triplet` 传 `subject=`、`predicate=`、`obj=`。
</Warning>

## TripletStore 方法

| 方法 | 返回 | 说明 |
| :------ | :------- | :----------- |
| `add_triplet(triplet)` | `dict` | 添加单个 `Triplet` 对象 |
| `add_triplets(triplets, batch_size)` | `dict` | 批量添加 `Triplet` 列表；返回 `{"success", "total", "processed", "failed", "batches"}` |
| `get_triplets(subject, predicate, object)` | `List[Triplet]` | 按主语/谓语/宾语过滤检索三元组 |
| `delete_triplet(triplet)` | `dict` | 从存储中删除一个 `Triplet` |
| `update_triplet(old_triplet, new_triplet)` | `dict` | 原子化的删 + 加 |
| `execute_query(query, parameters, graph, graphs)` | `QueryResult` | 执行 SPARQL 查询：返回带 `.bindings`、`.variables`、`.execution_time` 的 `QueryResult` |
| `store(knowledge_graph, ontology)` | `dict` | 把 KG + 本体 dict 转成 RDF 三元组并批量加载 |
| `add_skos_concept(concept_uri, scheme_uri, pref_label, ...)` | `dict` | 添加 SKOS 概念，可选别名、上下位及相关概念 |
| `get_skos_concepts(scheme_uri)` | `List[dict]` | 检索全部 SKOS 概念，可按 scheme URI 过滤 |
| `compute_delta(old_graph_uri, new_graph_uri)` | `dict` | 返回两个命名图快照间的 `{"added_triples", "removed_triples", "added_count", "removed_count"}` |
| `get_stats()` | `dict` | 取后端统计信息 |

## SPARQL 查询

`execute_query()` 是所有 SPARQL 操作的唯一入口。返回 `QueryResult`：经 `.bindings` 访问结果：

```python
from semantica.triplet_store import TripletStore

store = TripletStore(backend="blazegraph", endpoint="http://localhost:9999/blazegraph/sparql")

# SELECT: iterate result.bindings
result = store.execute_query("""
    PREFIX ex: <http://example.org/>
    SELECT ?person ?company WHERE {
        ?person ex:founded ?company .
    }
""")

for row in result.bindings:
    print(row.get("person",  {}).get("value"))
    print(row.get("company", {}).get("value"))

# ASK, CONSTRUCT, UPDATE: same method, different SPARQL form
result = store.execute_query("""
    PREFIX ex: <http://example.org/>
    ASK { ex:apple_inc ex:founded_by ex:steve_jobs . }
""")
print(result.bindings)   # ASK returns boolean result in bindings

# SPARQL UPDATE (INSERT/DELETE)
store.execute_query("""
    PREFIX ex: <http://example.org/>
    INSERT DATA {
        ex:apple_inc ex:listed_on ex:NASDAQ .
    }
""")
```

### QueryResult 字段

| 字段 | 类型 | 说明 |
| :----- | :---- | :----------- |
| `bindings` | `List[dict]` | 每个 dict 把变量名映射到 `{"value": ..., "type": ...}` |
| `variables` | `List[str]` | SPARQL 结果变量名 |
| `execution_time` | `float` | 耗时（秒） |
| `metadata` | `dict` | 查询、图作用域、缓存命中标志 |

<Warning>
  **`execute_query()` 返回 `QueryResult`，不是列表。**遍历 `result.bindings`，不要直接遍历 `result`。每个 binding 是变量名 → `{"value": ..., "type": ...}` 的 dict。
</Warning>

## SPARQL CONSTRUCT 模板

`semantica.triplet_store.construct_templates` 提供参数化的 SPARQL `CONSTRUCT` 查询模板：可复用的查询定义一次，安全地代入类型化参数，一次调用把产出的三元组持久化。**仅 Blazegraph 后端可用**（见上文[后端](#backends)）——`BlazegraphStore.execute_sparql()` 是唯一具备 CONSTRUCT 感知 RDF 解析的后端。

```python
from semantica.triplet_store.construct_templates import (
    ConstructTemplate,
    ParameterDescriptor,
    ConstructTemplateRegistry,
    render_construct_template,
    execute_construct_template,
)
from semantica.triplet_store import BlazegraphStore

# Define and register a template
template = ConstructTemplate(
    name="person_to_foaf",
    description="Maps a person record subject to a foaf:name triple",
    construct_query="""
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        CONSTRUCT { {{subject}} foaf:name {{name}} ; foaf:age {{age}} }
        WHERE { {{subject}} a <http://ex.org/Person> }
    """,
    parameters=[
        ParameterDescriptor(name="subject", type="uri", required=True),
        ParameterDescriptor(name="name", type="literal", required=True),
        ParameterDescriptor(
            name="age", type="typed-literal", required=False, default=0,
            datatype="xsd:integer",
        ),
    ],
)

registry = ConstructTemplateRegistry()
registry.register(template)

# Render only: inspect the substituted SPARQL string, no network call
sparql = render_construct_template(
    registry.get("person_to_foaf"),
    params={"subject": "http://ex.org/p1", "name": "Alice", "age": 30},
)

# Render + execute + persist in one call
store = BlazegraphStore(endpoint="http://localhost:9999/blazegraph", namespace="kb")
triplets = execute_construct_template(
    template=registry.get("person_to_foaf"),
    params={"subject": "http://ex.org/p1", "name": "Alice", "age": 30},
    store_backend=store,
    target_graph="http://ex.org/graphs/people",
)
# triplets: List[Triplet], already persisted via store.add_triplets
```

每个 `ParameterDescriptor.type` 控制值的渲染方式：`"uri"` 值经白名单校验后包在 `<...>` 里；`"literal"` 值转义并加引号；`"typed-literal"` 值要求给 `datatype`（如 `"xsd:integer"`），数值/布尔 XSD 类型渲染时不加引号。占位符用 `{{param}}` 而不是 SPARQL 自己的 `?param` 语法，模板占位符就不会与查询体里的真实 SPARQL 变量混淆。

<Note>
  CONSTRUCT 模板仅支持 Blazegraph。`store_backend` 不同时实现 `execute_sparql()` 和 `add_triplets()` 时，`execute_construct_template()` 抛 `ProcessingError`。
</Note>

## SPARQL 结果分页

大结果集用 LIMIT 和 OFFSET 分页：

```python
page_size = 1000
offset    = 0

while True:
    result = store.execute_query(f"""
        SELECT ?s ?p ?o WHERE {{
            ?s ?p ?o .
        }}
        ORDER BY ?s
        LIMIT {page_size} OFFSET {offset}
    """)
    if not result.bindings:
        break
    process_batch(result.bindings)
    offset += page_size
```

<Warning>
  **大 SPARQL 结果集务必分页。**对大存储跑 `SELECT * WHERE { ?s ?p ?o }` 会返回全部三元组。探索性查询一律带 `LIMIT` 和 `OFFSET`。不显式指定时，`QueryEngine` 会自动加 `LIMIT 1000`。
</Warning>

## 命名图作用域

Oxigraph、Blazegraph、RDF4J 支持命名图。用 `graph=` 参数把 `execute_query()` 限定到某个命名图：

```python
# Add a triplet to a named graph
from semantica.semantic_extract.types import Triplet

t = Triplet(
    subject="http://example.org/a",
    predicate="http://example.org/p",
    object="http://example.org/b",
)
store.add_triplet(t, graph="http://example.org/graph1")

# Query a named graph via FROM clause in SPARQL
result = store.execute_query("""
    SELECT ?s ?p ?o WHERE {
        ?s ?p ?o .
    }
""", graph="http://example.org/graph1")   # injects FROM <graph> before WHERE

# Or scope inline using FROM in the query string
result = store.execute_query("""
    SELECT ?s ?p ?o FROM <http://example.org/graph1> WHERE {
        ?s ?p ?o .
    }
""")
```

<Note>
  命名图查询作用域适用于 Oxigraph、Blazegraph、RDF4J。
  Jena 后端会静默忽略 `graph=` 查询参数。
</Note>

<Tip>
  **用命名图隔离来源。**写入和 `execute_query()` 都传 `graph="http://example.org/source_A"`，存储和检索就都在同一作用域内。Oxigraph、Blazegraph、RDF4J 支持命名图查询作用域。
</Tip>

## 批量加载

`add_triplets()` 经内部 `BulkLoader` 分批写入。经 `store.bulk_loader` 访问并配置：

```python
from semantica.triplet_store import TripletStore
from semantica.semantic_extract.types import Triplet

store = TripletStore(backend="blazegraph", endpoint="http://localhost:9999/blazegraph/sparql")

# Default: batch_size=1000, max_retries=3
result = store.add_triplets(triplets)
# Returns: {"success": True, "total": N, "processed": N, "failed": 0, "batches": B}

# Custom batch size for this call
result = store.add_triplets(triplets, batch_size=500)

# Validate before loading
validation = store.bulk_loader.validate_before_load(triplets)
if not validation["valid"]:
    print(validation["errors"])
```

`BulkLoader` 也可以直接用，带 `progress_callback`：

```python
from semantica.triplet_store import BulkLoader

loader = BulkLoader(batch_size=2000, max_retries=5, retry_delay=2.0)

def on_progress(p):
    print(f"{p.progress_percentage:.1f}%  ({p.loaded_triplets}/{p.total_triplets})")

progress = loader.load_triplets(triplets, store._store_backend, progress_callback=on_progress)
print(f"Loaded {progress.loaded_triplets} in {progress.elapsed_time:.2f}s")
```

## 存储知识图谱

`store(knowledge_graph, ontology)` 把 KG + 本体 dict 结构转成 RDF，一次调用全部批量加载：

```python
kg = {
    "entities": [
        {"id": "apple_inc",  "type": "Organization", "properties": {"name": "Apple Inc."}},
        {"id": "steve_jobs", "type": "Person",        "properties": {"name": "Steve Jobs"}},
    ],
    "relationships": [
        {"source": "steve_jobs", "target": "apple_inc", "type": "founded"}
    ],
}
ontology = {
    "uri": "https://example.org/ontology/",
    "classes": [
        {"name": "Organization"},
        {"name": "Person"},
    ],
    "properties": [
        {"name": "founded", "type": "object", "domain": ["Person"], "range": ["Organization"]},
    ],
}

result = store.store(knowledge_graph=kg, ontology=ontology)
# Returns add_triplets result dict
```

## SKOS 词表管理

```python
store.add_skos_concept(
    concept_uri="http://example.org/skos/MachineLearning",
    scheme_uri="http://example.org/skos/AIScheme",
    pref_label="Machine Learning",
    alt_labels=["ML", "Statistical Learning"],
    broader=["http://example.org/skos/AI"],
    definition="A field of artificial intelligence...",
)

# Retrieve all concepts in a scheme
concepts = store.get_skos_concepts(scheme_uri="http://example.org/skos/AIScheme")
for c in concepts:
    print(c["uri"], c["pref_label"], c["alt_labels"])
```

## 差量计算

```python
# Compare two named graph snapshots and return added/removed triples
delta = store.compute_delta(
    old_graph_uri="http://example.org/graph/v1",
    new_graph_uri="http://example.org/graph/v2",
)

print(f"Added:   {delta['added_count']} triples")
print(f"Removed: {delta['removed_count']} triples")

for t in delta["added_triples"]:
    print(f"+  {t.subject}  {t.predicate}  {t.object}")
for t in delta["removed_triples"]:
    print(f"-  {t.subject}  {t.predicate}  {t.object}")
```

## 与 Export 模块集成

Export 模块写出 RDF，三元组存储随后经 `add_triplets()` 接收：

```python
from semantica.export import RDFExporter
from semantica.triplet_store import TripletStore
from semantica.semantic_extract.types import Triplet

# Export KG to Turtle
exporter = RDFExporter()
exporter.export_to_file(kg, "output.ttl", format="turtle")

# Parse the file and load triplets into the store
# (TripletStore does not have a built-in import_file() method —
#  parse with rdflib and convert to Triplet objects)
import rdflib
g = rdflib.Graph()
g.parse("output.ttl", format="turtle")

store = TripletStore(backend="jena", endpoint="http://localhost:3030/ds")
triplets = [
    Triplet(subject=str(s), predicate=str(p), object=str(o))
    for s, p, o in g
]
store.add_triplets(triplets)

# Query with SPARQL
result = store.execute_query("SELECT * WHERE { ?s ?p ?o } LIMIT 10")
for row in result.bindings:
    print(row)
```

- [Export](./export.md) — 把知识图谱导出为 RDF 格式。
- [Ontology](./ontology.md) — 加载 OWL 本体并存为 RDF 三元组。
- [Reasoning](./reasoning.md) — 基于 SPARQL 的属性链推理。
- [Graph Store](./graph_store.md) — 面向 Cypher 查询的属性图替代方案。
