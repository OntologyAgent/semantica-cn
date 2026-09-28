---
title: "向量存储模块（Vector Store）"
description: "FAISS、Pinecone、Weaviate、Qdrant、Milvus、PgVector 的统一接口，支持混合检索。"
source: reference/vector_store.md
source_version: d5f9928e79e3fed064371789f4fcfbe22ed3d68e
icon: "database"
---

`semantica.vector_store` 为所有主流后端提供统一的向量存储与检索 API：

- 一行代码切换后端：无需改动应用代码
- `HybridSearch` 把稠密向量相似度与元数据过滤融合：RRF 或加权平均
- `NamespaceManager` 做多租户的结构化隔离
- `FAISSStore` 支持 flat、ivf、hnsw、pq 四种索引类型
- 并行 worker 批量生成嵌入（Embedding）并存储；更新元数据无需重新嵌入


## 导出的类

| 类 | 职责 |
| :--- | :--- |
| `VectorStore` | 统一接口：`store_vectors`、`search_vectors`、`update_vectors`、`delete_vectors` |
| `HybridSearch` | 把稠密向量相似度与元数据过滤融合：RRF 或加权平均 |
| `MetadataFilter` | 可链式调用的过滤器构造器：`.eq("type", "person").gt("year", 2020).in_list("tag", [...])` |
| `NamespaceManager` | 多租户隔离：按项目或用户划分独立索引命名空间 |
| `FAISSStore` | 本地磁盘或内存：flat、ivf、hnsw、pq 索引类型 |
| `WeaviateStore` | 云端或自托管，感知 schema |
| `QdrantStore` | 云端或自托管，基于 payload 的过滤 |
| `PineconeStore` | 托管云向量数据库：serverless 和 pod 两种模式 |
| `MilvusStore` | 可扩展的向量数据库，支持 Milvus Lite、自托管服务器和 Zilliz Cloud |
| `PgVectorStore` | PostgreSQL + `pgvector` 扩展：无需额外基础设施 |
| `MetadataStore` | 独立的元数据索引与查询 |
| `SearchRanker` | RRF 与加权平均的结果融合 |

## 你能得到什么

- **VectorStore** — 跨 FAISS、Pinecone、Weaviate、Qdrant、Milvus、PgVector 的统一接口
  - 一行切换后端：不改应用代码
  - `add_documents()` 自动嵌入；预计算嵌入用 `store_vectors()`
- **HybridSearch** — 稠密向量相似度 + 元数据过滤
  - RRF 或加权平均两种融合策略
  - 跨独立集合的多源融合
- **MetadataStore** — 按字段值建富元数据索引
  - 更新元数据字段无需重新嵌入
  - OR 与 AND 查询运算符
- **NamespaceManager** — 每租户的结构化命名空间隔离
  - 查询更快（每租户搜索空间更小）
  - 比仅靠元数据过滤的隔离更安全
- **批量操作** — 批量添加、删除、元数据更新
  - `batch_size` 和 `workers` 可配置的并行嵌入
  - 向量就地更新，无需全量重建索引
- **FAISS 索引类型** — flat、ivf、hnsw、pq
  - `FAISSStore.create_index()` 提供完整配置控制
  - `save()` / `load()` 落盘持久化


## 快速开始

**`VectorStore`** 是主入口。开发用 `"inmemory"`，**本地生产**用 `"faiss"`：

```python
from semantica.vector_store import VectorStore

# In-memory (development / testing: no persistence)
store = VectorStore(backend="inmemory", dimension=384)

# FAISS (local, persists to disk via save/load)
store = VectorStore(backend="faiss", dimension=384)

# Add plain text documents (auto-embedded)
ids = store.add_documents(
    documents=["Apple was founded by Steve Jobs.", "Microsoft was co-founded by Bill Gates."],
    metadata=[{"source": "wiki"}, {"source": "wiki"}]
)

# Search by text query (auto-embedded)
results = store.search("technology company founders", limit=5)
for r in results:
    print(f"{r['id']}: score: {r['score']:.3f}")
```

<Warning>
  **向量维度必须与嵌入模型匹配。**`dimension` 参数必须与嵌入模型的输出维度完全一致：`BAAI/bge-small-en-v1.5` = 384、`all-MiniLM-L6-v2` = 384、`all-mpnet-base-v2` = 768、`bge-large-en-v1.5` = 1024。不匹配会在插入时报错。
</Warning>

<Tip>
  **文本用 `add_documents()`，预计算嵌入用 `store_vectors()`。**`add_documents()` 会并行分批自动嵌入。嵌入已经算好（比如来自微调模型）时，直接用 `store_vectors()` 跳过重复嵌入。
</Tip>

## 上手步骤

<Steps>
  <Step title="创建向量存储">
    ```python
    from semantica.vector_store import VectorStore

    # In-memory (development)
    store = VectorStore(backend="inmemory", dimension=384)

    # FAISS (local production)
    store = VectorStore(backend="faiss", dimension=384)
    ```
  </Step>
  <Step title="添加向量">
    ```python
    # Add text documents (auto-embedded in batches)
    ids = store.add_documents(
        documents=["text one", "text two"],
        metadata=[{"title": "Document 1"}, {"title": "Document 2"}]
    )

    # Add pre-computed vectors directly
    ids = store.store_vectors(
        vectors=[embedding1, embedding2],
        metadata=[{"title": "Document 1"}, {"title": "Document 2"}]
    )
    ```
  </Step>
  <Step title="按语义相似度检索">
    ```python
    # Search by text query (auto-embeds the query)
    results = store.search("machine learning", limit=10)

    # Search by pre-computed vector
    results = store.search_vectors(query_vector, k=10)

    for r in results:
        print(f"{r['id']}: score: {r['score']:.3f}")
    ```
  </Step>
  <Step title="按元数据过滤">
    ```python
    from semantica.vector_store import HybridSearch, MetadataFilter

    mf = MetadataFilter().eq("category", "research").gt("year", 2022)

    # Pass vector_store to the constructor: search() resolves vectors automatically
    search  = HybridSearch(vector_store=store)
    results = search.search(query=query_vector, k=10, metadata_filter=mf)
    ```
  </Step>
</Steps>

## 后端

<Tabs>
  <Tab title="In-memory / FAISS">

```python
# In-memory: no persistence, for development and testing
store = VectorStore(backend="inmemory", dimension=384)

# FAISS: local disk persistence via save() / load()
store = VectorStore(backend="faiss", dimension=384)
store.save("./my_store")   # save to directory
store.load("./my_store")   # restore from directory
```

无需安装，无需 API key。FAISS 需要 `pip install faiss-cpu`。

  </Tab>
  <Tab title="Pinecone">

```bash
pip install "semantica[vectorstore-pinecone]"
```

```python
import os
store = VectorStore(
    backend="pinecone",
    dimension=768,
    api_key=os.getenv("PINECONE_API_KEY"),
    index_name="semantica-index",
    environment="us-east-1-aws"
)
```

  </Tab>
  <Tab title="Weaviate">

```bash
pip install "semantica[vectorstore-weaviate]"
```

```python
store = VectorStore(
    backend="weaviate",
    dimension=768,
    url="http://localhost:8080",
    class_name="Document"
)
```

  </Tab>
  <Tab title="Qdrant">

```bash
pip install "semantica[vectorstore-qdrant]"
```

```python
store = VectorStore(
    backend="qdrant",
    dimension=768,
    url="http://localhost:6333",
    collection_name="semantica"
)
```

  </Tab>
  <Tab title="PgVector">

```bash
pip install "semantica[vectorstore-pgvector]"
```

```python
store = VectorStore(
    backend="pgvector",
    dimension=768,
    connection_string="postgresql://user:pass@localhost/db",
    table_name="embeddings"
)
```

`connection_string` 必填：缺失时 store 会在构造时抛 `ValueError`。

  </Tab>
  <Tab title="Milvus">

```bash
pip install pymilvus
```

你可以通过 `host`/`port` 连接自托管 Milvus 服务器，也可以通过 `uri`/`token` 连接 Milvus Lite、远程服务器或 Zilliz Cloud。

```python
import os

# 自托管服务器：host/port
store = VectorStore(
    backend="milvus",
    dimension=768,
    host="localhost",
    port=19530,
    collection_name="semantica"
)

# Milvus Lite：uri 为本地文件路径，无需运行服务器
store = VectorStore(
    backend="milvus",
    dimension=768,
    uri="./milvus.db",
    collection_name="semantica"
)

# 远程服务器：uri 为服务器地址，可搭配 RBAC 的 user/password
store = VectorStore(
    backend="milvus",
    dimension=768,
    uri="http://milvus.example.com:19530",
    user="root",
    password=os.getenv("MILVUS_PASSWORD"),
    collection_name="semantica"
)

# Zilliz Cloud：uri 为集群 endpoint，token 为 API key
store = VectorStore(
    backend="milvus",
    dimension=768,
    uri="https://<cluster>.zillizcloud.com",
    token=os.getenv("ZILLIZ_API_KEY"),
    collection_name="semantica"
)
```

| 参数 | 说明 |
| :--- | :--- |
| `host` / `port` | Milvus 服务器地址，默认 `localhost` / `19530`。设置 `uri` 时忽略。 |
| `uri` | Milvus Lite 文件路径（如 `"./milvus.db"`）、服务器地址（如 `"http://localhost:19530"`）或 Zilliz Cloud endpoint。设置后优先于 `host`/`port`。 |
| `token` | `uri` 连接使用的认证 token，例如 Zilliz Cloud API key。 |
| `user` / `password` | RBAC 用户名和密码。`host`/`port` 和 `uri` 两种方式均会传递。 |

Semantica 在记录连接日志前会移除 `uri` 中的凭据（userinfo 和查询参数），只保留 scheme、host、port 和路径。

  </Tab>
</Tabs>

## 后端选择指南

| 后端 | 部署方式 | API Key | 持久化 | 最适合 |
| :------- | :---------- | :------- | :----------- | :-------- |
| `inmemory` | 进程内 | 否 | 否 | 开发、单元测试 |
| `faiss` | 本地 | 否 | 经 `save()`/`load()` | 本地部署、离线生产 |
| `pinecone` | 云端 | 是 | 托管 | 托管云、serverless |
| `weaviate` | 自托管 / 云端 | 可选 | 托管 | 富元数据过滤 |
| `qdrant` | 自托管 / 云端 | 可选 | 托管 | 高性能过滤 |
| `milvus` | 本地（Milvus Lite）/ 自托管 / 云端（Zilliz Cloud） | 可选 | 托管 | 大规模生产 |
| `pgvector` | PostgreSQL | 否 | 托管 | Postgres 原生集成 |

## HybridSearch

`HybridSearch` 实现混合检索（Hybrid Search）。说白了，向量相似度管“语义上像不像”，元数据过滤管“业务上符不符合”，两者结合就是一次完整的混合检索。构造时传 `vector_store`，后续调用就不必每次传原始向量：

```python
from semantica.vector_store import HybridSearch, MetadataFilter

# With vector_store: search() pulls vectors from the store automatically
search = HybridSearch(vector_store=store)
mf     = MetadataFilter().eq("category", "research").gt("year", 2022)

results = search.search(
    query=query_vector,   # np.ndarray or query string (auto-embedded)
    k=10,
    metadata_filter=mf
)

for r in results:
    print(f"{r['id']}: score: {r['score']:.3f}  metadata: {r['metadata']}")
```

不传 `vector_store` 时，就要显式传入向量：

```python
search = HybridSearch()
results = search.search(
    query=query_vector,
    vectors=my_vectors,
    metadata=my_metadata,
    vector_ids=my_ids,
    k=10,
    metadata_filter=mf,
)
```

跨独立集合的多源融合：

```python
sources = [
    {"vectors": v1, "metadata": m1, "ids": ids1},
    {"vectors": v2, "metadata": m2, "ids": ids2},
]
fused = search.multi_source_search(query_vector, sources, k=10)
```

<Tip>
  **用 `HybridSearch(vector_store=store)` 避免每次传原始向量。** 设了 `vector_store` 后，`search()` 自动从 store 拉取向量和元数据：你只需传 query 和过滤器。
</Tip>

## 元数据过滤

`MetadataFilter` 支持链式条件：所有条件之间是 AND：

```python
from semantica.vector_store import MetadataFilter

mf = MetadataFilter().eq("author", "John Smith")          # equality
mf = MetadataFilter().ne("status", "archived")            # not equal
mf = MetadataFilter().gt("year", 2022).lte("year", 2024)  # range
mf = MetadataFilter().in_list("tag", ["ai", "ml"])        # set membership
mf = MetadataFilter().contains("title", "neural")         # substring / list contains

# Multiple conditions: all must match (AND)
mf = (
    MetadataFilter()
    .eq("category", "research")
    .gt("year", 2022)
    .contains("title", "language model")
)
```

### MetadataFilter 方法

| 方法 | 运算符 | 说明 |
| :------ | :-------- | :----------- |
| `.eq(field, value)` | `==` | 精确相等 |
| `.ne(field, value)` | `!=` | 不等 |
| `.gt(field, value)` | `>` | 大于 |
| `.gte(field, value)` | `>=` | 大于等于 |
| `.lt(field, value)` | `<` | 小于 |
| `.lte(field, value)` | `<=` | 小于等于 |
| `.in_list(field, values)` | `in` | 字段值在列表中 |
| `.contains(field, value)` | substring | 字符串包含或列表包含 |

## SearchRanker

`SearchRanker` 融合多个排序列表的结果：

```python
from semantica.vector_store import SearchRanker

# Reciprocal Rank Fusion: robust to score scale differences
ranker  = SearchRanker(strategy="reciprocal_rank_fusion")
fused   = ranker.rank([results_list_1, results_list_2])

# Weighted average: requires normalised scores on the same scale
ranker  = SearchRanker(strategy="weighted_average")
fused   = ranker.rank([results_list_1, results_list_2], weights=[0.7, 0.3])
```

| 融合策略 | 说明 |
| :--------------- | :----------- |
| `reciprocal_rank_fusion` | 基于排名的 RRF 组合：对分数量纲差异稳健（默认） |
| `weighted_average` | 分数加权求和：`rank()` 传 `weights=[...]` |

## 命名空间隔离

多租户隔离用 `NamespaceManager` 把向量分配到命名空间：

```python
from semantica.vector_store import NamespaceManager, VectorStore

store      = VectorStore(backend="inmemory", dimension=384)
ns_manager = NamespaceManager()

ns_manager.create_namespace("tenant_a", description="Customer A data")
ns_manager.create_namespace("tenant_b", description="Customer B data")

# Store vectors, then assign them to a namespace
ids_a = store.store_vectors(embeddings_a, metadata=metadata_a)
for vid in ids_a:
    ns_manager.add_vector_to_namespace(vid, "tenant_a")

# List all namespace names
for name in ns_manager.list_namespaces():     # returns List[str]
    print(name)

# Get all vectors in a namespace
vectors_in_a = ns_manager.get_namespace_vectors("tenant_a")

# Look up which namespace a vector belongs to
ns = ns_manager.get_vector_namespace("vec_0")

ns_manager.delete_namespace("tenant_a")
```

<Tip>
  **多租户应用用 `NamespaceManager`。** 如果把所有租户的向量存进同一集合，查询时再靠元数据过滤，那么既慢，又可能因漏写过滤器而泄露数据。命名空间隔离既快（搜索空间更小）又安全（结构上彼此隔离）。
</Tip>

## 批量操作

```python
# Batch add text documents: parallel embedding with configurable workers
ids = store.add_documents(
    documents=large_doc_list,
    metadata=large_meta_list,
    batch_size=32,     # texts per embedding batch
    parallel=True,     # use ThreadPoolExecutor
)

# Batch add pre-computed vectors
ids = store.store_vectors(vectors=embeddings_list, metadata=meta_list)

# Delete by vector ID list
store.delete_vectors(vector_ids=["vec_0", "vec_1", "vec_2"])

# Update vectors in-place (rebuilds index for inmemory backend)
store.update_vectors(
    vector_ids=["vec_0"],
    new_vectors=[new_embedding]
)
```

## 持久化（FAISS 与 in-memory）

```python
store = VectorStore(backend="faiss", dimension=384)
store.add_documents(documents=docs, metadata=meta)

# Save to a directory: creates index.bin and store_data.pkl
store.save("./vector_store_backup")

# Restore in a new process
store2 = VectorStore(backend="faiss", dimension=384)
store2.load("./vector_store_backup")
```

<Note>
  云后端（Pinecone、Weaviate、Qdrant、Milvus、PgVector）自行管理持久化。`save()`/`load()` 仅适用于 in-memory 和 FAISS 后端。
</Note>

<Warning>
  **inmemory 和 faiss 后端若不 `save()`，进程退出即丢数据。** 添加向量后请调用 `store.save(path)`。云后端（Pinecone、Qdrant、Weaviate、Milvus、PgVector）会自动持久化。
</Warning>

## MetadataStore

`MetadataStore` 索引结构化元数据，无需向量即可按字段值查询。说白了，它就是挂在向量旁边的元数据索引表，专供按字段过滤，不参与相似度计算：

```python
from semantica.vector_store import MetadataStore

meta_store = MetadataStore()

# Store and retrieve metadata
meta_store.store_metadata("doc1", {"author": "Alice", "year": 2024, "category": "research"})
meta_store.store_metadata("doc2", {"author": "Bob",   "year": 2023, "category": "review"})

# Query: returns List[str] of matching vector IDs
ids = meta_store.query_metadata({"category": "research", "year": 2024})

# OR query
ids = meta_store.query_metadata({"category": "research"}, operator="OR")

# Get and update metadata for a specific vector
meta = meta_store.get_metadata("doc1")
meta_store.update_metadata("doc1", {"score": 0.92})

# Get all unique values for a field
years = meta_store.get_field_values("year")

# Statistics
stats = meta_store.get_stats()
# {"total_vectors": 2, "indexed_fields": 3, "field_counts": {...}}
```

<Tip>
  **更新元数据不必重新嵌入。**`MetadataStore.update_metadata(id, {...})` 只改挂载的字段（状态、标签、审阅日期），不重跑嵌入模型。凡是不影响语义内容的状态变更，都可以用它。
</Tip>

## FAISS 索引类型参考

要配置 FAISS 索引类型，需直接构造 `FAISSStore` 并调用 `create_index()`。类型名用小写：

```python
from semantica.vector_store import FAISSStore

store = FAISSStore(dimension=384)

# flat: brute-force exact search
store.create_index(index_type="flat", metric="L2")

# ivf: inverted file index
store.create_index(index_type="ivf", metric="L2", nlist=100)

# hnsw: hierarchical navigable small world graph
store.create_index(index_type="hnsw", metric="L2", M=32)

# pq: product quantization for memory efficiency
store.create_index(index_type="pq", metric="L2", m=8)
```

| 索引 | 内存 | 速度 | 精度 | 适用场景 |
| :----- | :------ | :----- | :-------- | :----------- |
| `flat` | 高 | 慢 | 精确（100%） | 少于 10 万向量，正确性优先 |
| `ivf` | 中 | 快 | ~95–98% | 10 万–1000 万向量，均衡之选 |
| `hnsw` | 中高 | 很快 | ~97–99% | 低延迟、生产检索 |
| `pq` | 低 | 快 | ~90–95% | 千万级向量、内存受限 |

<Warning>
  **FAISS 索引类型名是小写。**`FAISSStore.create_index()` 接受 `"flat"`、`"ivf"`、`"hnsw"`、`"pq"`：不是 `"Flat"`、`"IVF"`、`"HNSW"`、`"PQ"`。大写值会抛 `ValidationError`。
</Warning>

<Note>
  `VectorStore(backend="faiss")` 底层的 `FAISSStore` 默认初始化为 flat 索引。要用 ivf/hnsw/pq，须直接构造 `FAISSStore` 并以目标类型调用 `create_index()`。
</Note>

## 常见工作流

<Tabs>
  <Tab title="语义检索流水线">
    ```python
    from semantica.vector_store import VectorStore

    store = VectorStore(backend="faiss", dimension=384)

    # Index documents
    store.add_documents(
        documents=corpus_texts,
        metadata=[{"source": src} for src in sources],
        batch_size=64,
    )

    # Persist
    store.save("./corpus_index")

    # Query
    results = store.search("What is knowledge graph construction?", limit=5)
    for r in results:
        print(f"[{r['score']:.3f}] {r['metadata']['source']}")
    ```
  </Tab>
  <Tab title="过滤检索">
    ```python
    from semantica.vector_store import VectorStore, HybridSearch, MetadataFilter

    store  = VectorStore(backend="inmemory", dimension=384)
    search = HybridSearch(vector_store=store)

    # Only return results from 2023+ with category "research"
    mf = MetadataFilter().gte("year", 2023).eq("category", "research")
    results = search.search(query=query_vector, k=10, metadata_filter=mf)
    ```
  </Tab>
  <Tab title="多源融合">
    ```python
    from semantica.vector_store import HybridSearch, SearchRanker

    search = HybridSearch()
    sources = [
        {"vectors": v1, "metadata": m1, "ids": ids1},
        {"vectors": v2, "metadata": m2, "ids": ids2},
    ]
    fused = search.multi_source_search(query_vector, sources, k=10)

    # Custom fusion weights
    ranker = SearchRanker(strategy="weighted_average")
    fused  = ranker.rank([results_a, results_b], weights=[0.7, 0.3])
    ```
  </Tab>
  <Tab title="多租户命名空间">
    ```python
    from semantica.vector_store import VectorStore, NamespaceManager

    store = VectorStore(backend="inmemory", dimension=384)
    ns    = NamespaceManager()

    ns.create_namespace("project_a")
    ns.create_namespace("project_b")

    ids = store.add_documents(docs_a, metadata=meta_a)
    for vid in ids:
        ns.add_vector_to_namespace(vid, "project_a")

    # Check ownership
    print(ns.get_vector_namespace(ids[0]))  # "project_a"
    print(ns.get_namespace_stats("project_a"))
    ```
  </Tab>
</Tabs>

- [Embeddings](./embeddings.md) — 生成存入这里的向量。
- [Context](./context.md) — AgentContext 用 VectorStore 做记忆检索。
- [Split](./split.md) — 嵌入和入库前先分块。
- [Ingest](./ingest.md) — 嵌入和入库前先摄取文档。
