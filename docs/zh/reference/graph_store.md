---
title: "图存储模块（Graph Store）"
description: "Neo4j、FalkorDB、Apache AGE、Amazon Neptune 图数据库的统一接口。"
source: reference/graph_store.md
source_version: e14da6f64251b6d9c7947b961d34c45a0890b8c6
icon: "server"
---

**`semantica.graph_store`** 提供**单一统一 API**，把知识图谱持久化和查询落到生产级图数据库：

- 一行代码切换后端：Neo4j、FalkorDB、Apache AGE、Amazon Neptune
- 参数化 Cypher 执行，`QueryEngine` 可选结果缓存
- 节点和边批量加载：比逐条写入快
- `GraphAnalytics` 提供度中心性、连通分量、最短路径、邻居遍历
- 支持上下文管理器：`with GraphStore(...) as store:` 自动关闭连接


## 导出的类

| 类 | 职责 |
| :--- | :--- |
| `GraphStore` | 统一接口：`create_node`、`create_relationship`、`query`、`get_neighbors`、`shortest_path` |
| `QueryEngine` | 参数化 Cypher 执行，带结果缓存 |
| `GraphAnalytics` | `degree_centrality`、`connected_components`、`shortest_path`、`get_neighbors` |
| `Neo4jStore` | 经 Bolt 协议的生产负载：支持 APOC 和 GDS 插件 |
| `ApacheAgeStore` | PostgreSQL + AGE 扩展：无需独立图服务器 |
| `AmazonNeptuneStore` | AWS Neptune：经 Bolt 协议跑 OpenCypher |
| `FalkorDBStore` | 基于 Redis：亚毫秒延迟，适合实时应用 |


## 你能得到什么

- **GraphStore** — 跨 Neo4j、FalkorDB、Apache AGE、Amazon Neptune 的统一 API
  - 支持上下文管理器，自动清理连接
  - `create_nodes()` 批量加载：比逐个调用快
- **QueryEngine** — 参数化 Cypher 构造，防注入攻击
  - `use_cache=True` 可选进程内结果缓存
  - 写入时 `clear_cache()`，用 `enable_cache()` / `disable_cache()` 切换
- **GraphAnalytics** — 度中心性按度数降序排列
  - 连通分量标记
  - 节点间最短路径，邻居遍历最多 N 跳
- **批量操作** — `create_nodes(list)`：一次往返写入多个节点
  - `create_relationship()` 带类型化属性
  - `delete_node(detach=True)` 连带删除所有关联关系
- **Schema 管理** — `create_index(label, property_name=)`：让 MATCH 查询快几个数量级
  - `get_stats()`：节点数、边数、类型分布
  - 批量加载之前先建索引，性能最好
- **路径遍历** — `shortest_path()` 返回 `length`、`nodes`、`relationships`
  - `get_neighbors()` 可控方向和深度
  - 统一 API 下跨后端路径遍历


## 快速开始

`GraphStore` 把你选择的后端包在单一 API 后面。跑任何查询前先调用 `connect()`（或用作上下文管理器）：

```python
from semantica.graph_store import GraphStore

store = GraphStore(
    backend="neo4j",
    uri="bolt://localhost:7687",
    user="neo4j",
    password="password",
)
store.connect()

# Create a node
node = store.create_node(
    labels=["Person"],
    properties={"name": "Alice", "role": "Engineer"},
)
print(node["id"])   # Neo4j internal integer ID

# Create a relationship
store.create_relationship(
    start_node_id=node1_id,
    end_node_id=node2_id,
    rel_type="WORKS_FOR",
    properties={"since": 2022},
)

# Execute a Cypher query
results = store.query(
    "MATCH (p:Person)-[:WORKS_FOR]->(o:Organization) WHERE o.name = $org RETURN p",
    parameters={"org": "Acme Corp"},
)

store.close()
```

用作上下文管理器可自动关闭连接：

```python
with GraphStore(backend="neo4j", uri="bolt://localhost:7687", user="neo4j", password="password") as store:
    store.create_node(labels=["Person"], properties={"name": "Bob"})
```

<Warning>
  **任何操作前先调用 `connect()`。** `GraphStore` 构造时不会自动连接。要么显式调用 `store.connect()`，要么用上下文管理器写法 `with GraphStore(...) as store:`。
</Warning>

## 上手步骤

<Steps>
  <Step title="连接图数据库">
    ```python
    from semantica.graph_store import GraphStore

    store = GraphStore(
        backend="neo4j",
        uri="bolt://localhost:7687",
        user="neo4j",
        password="password",
    )
    store.connect()
    ```
  </Step>
  <Step title="装数据前先建索引">
    ```python
    store.create_index(label="Person",       property_name="name")
    store.create_index(label="Organization", property_name="name")
    ```
  </Step>
  <Step title="加载节点和关系">
    ```python
    # Batch creation: list of dicts with "labels" and "properties" keys
    store.create_nodes([
        {"labels": ["Person"],       "properties": {"name": "Alice"}},
        {"labels": ["Organization"], "properties": {"name": "Acme Corp"}},
    ])
    ```
  </Step>
  <Step title="查询图">
    ```python
    results = store.query(
        "MATCH (p:Person)-[:WORKS_FOR]->(o:Organization) WHERE o.name = $org RETURN p",
        parameters={"org": "Acme Corp"},
    )
    ```
  </Step>
</Steps>


## GraphStore 方法

| 方法 | 返回 | 说明 |
| :------ | :------- | :----------- |
| `create_node(labels, properties)` | `dict` | 创建单个节点，返回带 `"id"` 的节点 dict |
| `create_nodes(nodes)` | `List[dict]` | 从 `{"labels", "properties"}` dict 列表批量创建节点 |
| `get_node(node_id)` | `dict \| None` | 按后端 ID 检索节点 |
| `get_nodes(labels, properties, limit)` | `List[dict]` | 按标签/属性条件查询节点 |
| `update_node(node_id, properties, merge)` | `dict` | 更新节点属性；`merge=True`（默认）合并，`merge=False` 替换 |
| `delete_node(node_id, detach)` | `bool` | 删除节点；`detach=True`（默认）连带删除关系 |
| `create_relationship(start_node_id, end_node_id, rel_type, properties)` | `dict` | 创建有向关系 |
| `get_relationships(node_id, rel_type, direction, limit)` | `List[dict]` | 取某节点的关系 |
| `delete_relationship(rel_id)` | `bool` | 按 ID 删除关系 |
| `execute_query(query, parameters)` | `dict` | 执行原生 Cypher，返回 `{"success", "records", "keys", "metadata"}` |
| `query(query, parameters)` | `List[dict]` | 执行 Cypher，直接返回 records 列表 |
| `create_index(label, property_name)` | `bool` | 建索引加速查找 |
| `get_neighbors(node_id, rel_type, direction, depth)` | `List[dict]` | 取邻居节点 |
| `shortest_path(start_node_id, end_node_id, rel_type, max_depth)` | `dict \| None` | 求两节点间最短路径 |
| `get_stats()` | `dict` | 从后端取图统计信息 |


## 后端

<Tabs>
  <Tab title="Neo4j（推荐）">
    ```bash
    pip install neo4j
    ```

    ```python
    from semantica.graph_store import GraphStore

    store = GraphStore(
        backend="neo4j",
        uri="bolt://localhost:7687",
        user="neo4j",
        password="password",
        database="neo4j",    # optional: targets default database
    )
    store.connect()
    ```

    **最适合：** 生产负载、复杂 Cypher 查询、Bloom 可视化。
  </Tab>
  <Tab title="FalkorDB">
    ```bash
    pip install falkordb
    ```

    ```python
    store = GraphStore(
        backend="falkordb",
        host="localhost",
        port=6379,
        graph_name="semantica",
    )
    store.connect()
    ```

    **最适合：** Redis 协议上的超低延迟查询、边缘部署。
  </Tab>
  <Tab title="Apache AGE">
    ```bash
    pip install psycopg2-binary
    ```

    ```python
    store = GraphStore(
        backend="age",   # or "apache_age"
        connection_string="host=localhost dbname=agedb user=postgres password=secret",
        graph_name="semantica",
    )
    store.connect()
    ```

    **最适合：** 已在跑 PostgreSQL 的团队，想加图查询又不想多一个服务。

    <Warning>
      **Apache AGE 需要先装 PostgreSQL 扩展。** `backend="age"` 会调用 AGE 扩展函数。PostgreSQL 实例里没装 AGE 会报 `ProgrammingError`。安装步骤见 [Apache AGE 文档](https://age.apache.org/age-manual/master/intro/setup.html)。
    </Warning>
  </Tab>
  <Tab title="Amazon Neptune">
    ```bash
    pip install neo4j boto3
    ```

    ```python
    store = GraphStore(
        backend="neptune",   # or "amazon_neptune"
        endpoint="your-cluster.cluster-xxxx.us-east-1.neptune.amazonaws.com",
        port=8182,
        region="us-east-1",
        iam_auth=True,    # uses boto3 default credential chain
    )
    store.connect()

    # OpenCypher queries via Bolt protocol
    results = store.query(
        "MATCH (p:Person)-[:WORKS_FOR]->(o:Organization) RETURN p, o"
    )
    ```

    **最适合：** AWS 托管部署。Neptune 经 Bolt 协议跑 OpenCypher 查询：与 Neo4j 用同一套查询 API。

    <Warning>
      **Amazon Neptune 用 `iam_auth=`，不是 `use_iam_auth=`。** `AmazonNeptuneStore` 和 `GraphStore` 的 Neptune 后端参数名都是 `iam_auth: bool = True`。
    </Warning>
  </Tab>
  <Tab title="后端对比">

    | 后端 | 查询语言 | 部署方式 | IAM 认证 | 最适合 |
    | :------- | :-------------- | :---------- | :-------- | :-------- |
    | Neo4j | Cypher | 自托管 / Aura | 否 | 生产、复杂遍历、Bloom UI |
    | FalkorDB | OpenCypher | 基于 Redis | 否 | 超低延迟、边缘部署 |
    | Apache AGE | OpenCypher | PostgreSQL 扩展 | 否 | 已在用 Postgres 的团队 |
    | Amazon Neptune | OpenCypher | AWS 托管 | 是 | 云原生、托管、合规 |

  </Tab>
</Tabs>

## 图操作

```python
# Create a single node
node = store.create_node(
    labels=["Organization"],
    properties={"name": "Apple Inc.", "founded": 1976},
)

# Create a directed relationship (both node IDs required)
rel = store.create_relationship(
    start_node_id=jobs_id,
    end_node_id=node["id"],
    rel_type="FOUNDED",
    properties={"year": 1976},
)

# Batch-create nodes
store.create_nodes([
    {"labels": ["Person"],       "properties": {"name": "Steve Jobs"}},
    {"labels": ["Organization"], "properties": {"name": "NeXT"}},
])

# Update node properties (merge=True merges, merge=False replaces)
store.update_node(node["id"], {"employees": 164000}, merge=True)

# Delete (detach=True also removes connected relationships)
store.delete_node(node["id"], detach=True)
store.delete_relationship(rel["id"])

# Get neighbors
neighbors = store.get_neighbors(
    node["id"],
    rel_type="HAS_EMPLOYEE",
    direction="in",    # "in" | "out" | "both"
    depth=1,
)

# Shortest path: returns {"length", "nodes", "relationships"} or None
path = store.shortest_path(
    start_node_id=jobs_id,
    end_node_id=cook_id,
    rel_type="WORKS_WITH",
    max_depth=5,
)
if path:
    print(f"Hops: {path['length']}")
```

<Tip>
  **批量加载用 `create_nodes()`。** 逐个 `create_node()` 每次都发一轮网络往返。初始建图时 `create_nodes(list)` 更快。
</Tip>

## QueryEngine

`QueryEngine` 负责查询执行和可选缓存。经 `store.query_engine` 访问：

```python
from semantica.graph_store import GraphStore

store  = GraphStore(backend="neo4j", uri="bolt://localhost:7687", user="neo4j", password="password")
store.connect()

# Get the query engine from the store
engine = store.query_engine

# Execute a parameterized query
result = engine.execute(
    "MATCH (p:Person) WHERE p.department = $dept RETURN p",
    parameters={"dept": "Engineering"},
)
# result is {"success": True, "records": [...], "keys": [...], "metadata": {...}}

# Execute with caching: repeated identical calls return cached result
result = engine.execute(
    "MATCH (p:Person) RETURN count(p) as total",
    use_cache=True,
)

# Clear cached results
engine.clear_cache()

# Toggle caching
engine.disable_cache()
engine.enable_cache()
```

### QueryEngine 方法

| 方法 | 返回 | 说明 |
| :------ | :------- | :----------- |
| `execute(query, parameters, use_cache)` | `dict` | 执行 Cypher，返回 `{success, records, keys, metadata}` |
| `clear_cache()` | `None` | 清空全部缓存查询结果 |
| `enable_cache()` | `None` | 开启缓存（默认开） |
| `disable_cache()` | `None` | 关闭缓存 |

<Tip>
  **读多写少的负载用 `QueryEngine` 缓存。** 经 `store.query_engine` 拿到引擎，调 `engine.execute(query, use_cache=True)` 把相同查询缓存在进程内。写入使结果失效后调 `engine.clear_cache()`。
</Tip>

<Warning>
  **用参数化查询，别用字符串拼接。** `store.query("WHERE n.name = $name", parameters={"name": user_input})` 可防 Cypher 注入攻击。绝不要写 `f"WHERE n.name = '{user_input}'"`。
</Warning>


## GraphAnalytics

经 `store._manager.analytics` 访问，或直接用后端 store 实例构造：

```python
from semantica.graph_store import GraphStore, GraphAnalytics

store = GraphStore(backend="neo4j", uri="bolt://localhost:7687", user="neo4j", password="password")
store.connect()

# GraphAnalytics takes the backend store, not the GraphStore facade
analytics = GraphAnalytics(store._store_backend)

# Degree centrality: returns list of {"id", "degree"} dicts ordered by degree DESC
scores = analytics.degree_centrality(
    labels=["Person"],
    rel_type="KNOWS",
    direction="both",    # "in" | "out" | "both"
)
for entry in scores[:5]:
    print(f"Node {entry['id']}: degree {entry['degree']}")

# Connected components (requires GDS for Neo4j, NetworkX for in-process)
components = analytics.connected_components(labels=["Person"])

# Shortest path: returns {"length", "nodes", "relationships"} or None
path = analytics.shortest_path(
    start_node_id=alice_id,
    end_node_id=charlie_id,
    rel_type="KNOWS",
    max_depth=4,
)

# Neighbor traversal
neighbors = analytics.get_neighbors(
    node_id=alice_id,
    rel_type="KNOWS",
    direction="out",
    depth=2,
)
```

### GraphAnalytics 方法

| 方法 | 返回 | 说明 |
| :------ | :------- | :----------- |
| `degree_centrality(labels, rel_type, direction)` | `List[dict]` | 基于度的节点重要性：按度数降序排列 |
| `connected_components(labels)` | `List[dict]` | 连通分量标记（Neo4j 上需 GDS） |
| `shortest_path(start_node_id, end_node_id, rel_type, max_depth)` | `dict \| None` | 带 `length`、`nodes`、`relationships` 的路径，或 `None` |
| `get_neighbors(node_id, rel_type, direction, depth)` | `List[dict]` | `depth` 跳以内的邻居节点 |

<Note>
  `betweenness_centrality()`、`pagerank()`、`detect_communities()` 和 `all_paths()` 未实现。这些算法直接经 `store.execute_query()` 用 Neo4j GDS 过程。
</Note>


## Schema 管理

```python
# Index for fast label-property lookups: use property_name= not property=
store.create_index(label="Person",       property_name="name")
store.create_index(label="Organization", property_name="id")

# Graph statistics
stats = store.get_stats()
```

<Warning>
  **批量加载前先建索引。** `store.create_index(label="Person", property_name="name")` 让按 `name` 的 `MATCH` 查询快几个数量级。没有索引时每次查询都全表扫描。先建索引，再装数据。
</Warning>

<Warning>
  **`create_index` 的参数是 `property_name=`，不是 `property=`。** `store.create_index(label="Person", property_name="name")`：写成 `property=` 会被静默忽略。
</Warning>

## 常见工作流

<Tabs>
  <Tab title="从 KG 数据建图">
    ```python
    from semantica.graph_store import GraphStore

    store = GraphStore(backend="neo4j", uri="bolt://localhost:7687", user="neo4j", password="password")
    store.connect()

    # Create indexes first for speed
    store.create_index("Person",       property_name="name")
    store.create_index("Organization", property_name="name")

    # Load entities as nodes
    created = store.create_nodes([
        {"labels": [e["type"]], "properties": {"name": e["text"], "id": e["id"]}}
        for e in entities
    ])

    # Map entity IDs to backend node IDs
    id_map = {e["id"]: node["id"] for e, node in zip(entities, created)}

    # Load relationships
    for rel in relationships:
        if rel["source_id"] in id_map and rel["target_id"] in id_map:
            store.create_relationship(
                start_node_id=id_map[rel["source_id"]],
                end_node_id=id_map[rel["target_id"]],
                rel_type=rel["type"],
            )

    store.close()
    ```
  </Tab>
  <Tab title="参数化查询">
    ```python
    # Always use parameters, never string interpolation
    results = store.query(
        "MATCH (p:Person)-[:WORKS_FOR]->(o:Organization) "
        "WHERE o.name = $org AND p.role = $role RETURN p.name",
        parameters={"org": user_input_org, "role": user_input_role},
    )
    ```
  </Tab>
  <Tab title="邻居遍历">
    ```python
    # Walk 2 hops of KNOWS relationships
    neighbors = store.get_neighbors(
        node_id=alice_id,
        rel_type="KNOWS",
        direction="out",
        depth=2,
    )
    for n in neighbors:
        print(n["properties"]["name"])
    ```
  </Tab>
  <Tab title="Apache AGE 注意事项">
    AGE 每个顶点只支持一个主标签。传多个标签时，第一个用作 AGE 标签，其余存进 `labels` 属性数组。参数化查询内部走字面量内联（AGE 不支持 `cypher()` 调用里的 `$param` 绑定）：转义由 store 自动处理。
  </Tab>
</Tabs>

- [KG Module](./kg.md) — 先建图，再持久化。
- [Triplet Store](./triplet_store.md) — 支撑语义网和 SPARQL 查询的 RDF 三元组存储。
- [Visualization](./visualization.md) — 可视化任意后端存储的图。
- [Context](../../reference/context.md) — AgentContext 用 GraphStore 做记忆检索。
