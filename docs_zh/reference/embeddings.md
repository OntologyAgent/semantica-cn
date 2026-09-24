---
title: "嵌入模块（Embeddings）"
description: "文本与图嵌入生成：FastEmbed、Sentence-Transformers、OpenAI、BGE，带池化策略与提供商无关的 API。"
source: reference/embeddings.md
source_version: 5658be565695e8e98cdf3361027725657e4f2dac
icon: "vector-square"
---

**`semantica.embeddings`** 把文本和图结构转成**稠密向量表示**：

- 提供商无关的 API：FastEmbed（默认，ONNX，无需 GPU）、Sentence-Transformers、OpenAI、BGE
- 驱动语义检索、实体消解、GraphRAG 检索和去重
- `GraphEmbeddingManager` 为图数据库后端嵌入 KG 节点和边
- 五种池化策略：Mean（默认）、Max、CLS、Attention、Hierarchical
- `check_available_providers()` 显示环境中已安装哪些后端


## 为什么嵌入很重要

原始文本无法做数学比较。嵌入(Embedding)把语义翻译成几何：两句话语义相近，向量在高维空间就彼此靠近，哪怕它们不共享任何词。

Semantica 用嵌入做：

- **语义检索**：按含义找知识图谱节点，而不只是关键词
- **实体消解**：识别"Apple Inc."和"Apple Computer"指向同一实体
- **去重**：`semantic_v2` 策略用嵌入距离度量实体相似度
- **GraphRAG 检索**：向量 + 图遍历混合，给 LLM 有依据的回答
- **语义分块**：`TextSplitter(method="semantic_transformer")` 里检测话题切换边界

## 导出的类

| 类 | 职责 |
| :--- | :--- |
| `EmbeddingGenerator` | 提供商无关的主入口：负责分批与提供商选择 |
| `TextEmbedder` | 文本嵌入，自动批处理；默认用 FastEmbed |
| `GraphEmbeddingManager` | 为 GraphRAG 和图数据库嵌入 KG 节点和边 |
| `VectorEmbeddingManager` | 为向量数据库后端准备和格式化嵌入 |
| `OpenAIStore` | OpenAI `text-embedding-3-small` / `text-embedding-3-large` 提供商 |
| `BGEStore` | 经 `sentence-transformers` 使用 BAAI/bge 模型 |
| `FastEmbedStore` | ONNX 加速的本地嵌入：**不要求** CUDA |
| `LlamaStore` | 占位实现：不可用于生产，不要用它做嵌入 |
| `MeanPooling` | 默认池化策略：检索和聚类最佳 |

## 你能得到什么

- **EmbeddingGenerator** — 主入口：提供商无关，自动跨所有后端分批。
- **TextEmbedder** — 文本专用，自动分批并带进度跟踪。默认方法是 FastEmbed。
- **GraphEmbeddingManager** — 图数据库的节点和边嵌入：Neo4j、NetworkX、FalkorDB。
- **VectorEmbeddingManager** — 为 FAISS、Weaviate、Qdrant、Milvus 准备、归一化、格式化嵌入。
- **提供商 Store** — `OpenAIStore`、`BGEStore`、`FastEmbedStore` 和 `ProviderStoreFactory`。
- **池化策略** — Mean、Max、CLS、Attention、Hierarchical：控制 token 到向量的聚合方式。

## 提供商配置

<Tabs>
  <Tab title="FastEmbed（默认）">
    ONNX 加速的本地嵌入。无需 GPU，无需 API key。最佳起点。

    ```bash
    pip install "semantica[fastembed]"
    ```

    ```python
    from semantica.embeddings import EmbeddingGenerator

    # FastEmbed is the default: no config needed
    generator = EmbeddingGenerator()
    embedding = generator.generate_embeddings("Text about AI")
    ```

    <Check>
      默认模型是 `BAAI/bge-small-en-v1.5`。零成本、零 GPU，任何机器都能跑。
    </Check>

    <Warning>
      **FastEmbed 忽略 `device` 参数。**FastEmbed 走 ONNX Runtime，自己管理执行 provider：传 `device="cuda"` 无效。需要显式 GPU 控制时换 `method="sentence_transformers"`。
    </Warning>
  </Tab>
  <Tab title="Sentence-Transformers">
    经 HuggingFace 选择海量模型。本地运行，无需 API key。

    ```bash
    pip install semantica  # sentence-transformers included
    ```

    ```python
    from semantica.embeddings import EmbeddingGenerator

    generator = EmbeddingGenerator(config={
        "text": {
            "method": "sentence_transformers",
            "model_name": "all-MiniLM-L6-v2",
        }
    })
    ```

    常用模型：`all-MiniLM-L6-v2`（快、小）、`all-mpnet-base-v2`（均衡）、`BAAI/bge-large-en-v1.5`（高精度）。

    <Warning>
      **序列长度上限。**多数 sentence-transformers 模型上限 512 token，模型会静默截断超长部分。长文档用 `TextSplitter(method="hierarchical")` + `HierarchicalPooling`。
    </Warning>
  </Tab>
  <Tab title="BGE">
    经 sentence-transformers 使用 BAAI/bge 模型。检索性能业界领先，本地运行。

    ```bash
    pip install semantica
    ```

    ```python
    from semantica.embeddings import BGEStore, EmbeddingGenerator

    store     = BGEStore(model="BAAI/bge-large-en-v1.5")
    embedding = store.embed("Text about AI")

    # Or switch model on an existing EmbeddingGenerator
    generator = EmbeddingGenerator()
    generator.set_text_model("sentence_transformers", "BAAI/bge-large-en-v1.5")
    ```
  </Tab>
  <Tab title="OpenAI">
    经 OpenAI API 的云端嵌入。质量最高，需要 API key。

    ```bash
    pip install "semantica[llm-openai]"
    export OPENAI_API_KEY="sk-..."
    ```

    ```python
    import os
    from semantica.embeddings import OpenAIStore

    store = OpenAIStore(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="text-embedding-3-small",   # or text-embedding-3-large
    )
    embedding = store.embed("Text about AI")
    ```

    | 模型 | 维度 | 最适合 |
    | :---- | :--------- | :-------- |
    | `text-embedding-3-small` | 1536 | 高性价比检索 |
    | `text-embedding-3-large` | 3072 | 最高精度负载 |
  </Tab>
</Tabs>

检查环境中已安装哪些提供商：

```python
from semantica.embeddings import check_available_providers

providers = check_available_providers()
# → {"sentence_transformers": True, "fastembed": True, "openai": False}
```

## 快速开始

`EmbeddingGenerator` 是生成嵌入最快的路径：默认方法是 FastEmbed（ONNX，无需 GPU）：

```python
from semantica.embeddings import EmbeddingGenerator

# Default: FastEmbed with BAAI/bge-small-en-v1.5
generator = EmbeddingGenerator()

# Embed a single text
embedding = generator.generate_embeddings("Text about AI")

# Embed a batch
embeddings = generator.generate_embeddings(["Text about AI", "Machine learning concepts"])

# Compare two embeddings (cosine similarity: 0.0 to 1.0)
score = generator.compare_embeddings(embeddings[0], embeddings[1], method="cosine")
print(f"Similarity: {score:.3f}")
```

<Tip>
  **索引和查询务必用同一个模型。**不同模型的向量不可比——它们处在不同的向量空间。因此换模型就要对整个语料重新嵌入。
</Tip>

构造后切换提供商：

```python
# Switch to a sentence-transformers model
generator.set_text_model("sentence_transformers", "all-MiniLM-L6-v2")

# Switch to BGE large
generator.set_text_model("sentence_transformers", "BAAI/bge-large-en-v1.5")
```

## 上手步骤

<Steps>
  <Step title="安装并初始化提供商">
    ```python
    from semantica.embeddings import EmbeddingGenerator

    # Default: FastEmbed, free, runs locally with no GPU
    generator = EmbeddingGenerator()

    # Use sentence-transformers instead
    generator = EmbeddingGenerator(config={"text": {"method": "sentence_transformers", "model_name": "all-MiniLM-L6-v2"}})
    ```
  </Step>
  <Step title="生成嵌入">
    ```python
    # Single text → 1D array
    embedding = generator.generate_embeddings("Text about AI")

    # Batch → 2D array (n_texts, dim)
    embeddings = generator.generate_embeddings(["Text about AI", "Machine learning concepts"])
    ```
  </Step>
  <Step title="计算相似度">
    ```python
    # Cosine similarity: 0.0 (unrelated) to 1.0 (identical meaning)
    score = generator.compare_embeddings(embeddings[0], embeddings[1], method="cosine")
    print(f"Similarity: {score:.3f}")
    ```
  </Step>
  <Step title="为向量数据库做准备">
    ```python
    from semantica.embeddings import VectorEmbeddingManager
    import numpy as np

    manager = VectorEmbeddingManager()

    embeddings = np.array([...], dtype=np.float32)
    metadata   = [{"text": "doc 1"}, {"text": "doc 2"}]

    result = manager.prepare_for_vector_db(embeddings, metadata=metadata, backend="faiss")
    # result["vectors"]  → normalized float32 array
    # result["ids"]      → ["vec_0", "vec_1", ...]
    # result["metadata"] → formatted metadata list
    ```
  </Step>
</Steps>

## 支持的模型

| 提供商 | 模型 | 维度 | 速度 | 最适合 |
| :-------- | :----- | :--------- | :----- | :-------- |
| `fastembed` | `BAAI/bge-small-en-v1.5` | 384 | 很快 | **默认**：针对 CPU 优化，**不要求** GPU |
| `sentence_transformers` | `all-MiniLM-L6-v2` | 384 | 快 | 速度与质量的均衡 |
| `sentence_transformers` | `all-mpnet-base-v2` | 768 | 中 | 更高检索质量 |
| `sentence_transformers` | `BAAI/bge-large-en-v1.5` | 1024 | 中 | 业界领先的检索精度 |
| `openai` | `text-embedding-3-small` | 1536 | API | 高性价比的 OpenAI 嵌入 |
| `openai` | `text-embedding-3-large` | 3072 | API | OpenAI API 的最高质量 |

## EmbeddingGenerator

<Tabs>
  <Tab title="FastEmbed（默认）">
    ```python
    from semantica.embeddings import EmbeddingGenerator

    # Default: FastEmbed with BAAI/bge-small-en-v1.5
    generator = EmbeddingGenerator()
    embeddings = generator.generate_embeddings(texts)
    similarity = generator.compare_embeddings(embeddings[0], embeddings[1])
    ```

    **最适合：** 纯 CPU 生产环境、无 GPU 时延迟最低。默认即开即用。
  </Tab>
  <Tab title="Sentence-Transformers">
    ```python
    from semantica.embeddings import EmbeddingGenerator

    generator = EmbeddingGenerator()
    generator.set_text_model("sentence_transformers", "all-MiniLM-L6-v2")
    embeddings = generator.generate_embeddings(texts)
    ```

    **最适合：** 有 GPU 时的更高检索质量，或需要微调模型。
  </Tab>
  <Tab title="OpenAI">
    ```python
    from semantica.embeddings import OpenAIStore
    import os

    store     = OpenAIStore(api_key=os.getenv("OPENAI_API_KEY"), model="text-embedding-3-small")
    embedding = store.embed("Hello world")
    ```

    **最适合：** 最高质量（`text-embedding-3-large`），或对齐既有 OpenAI 流水线。
  </Tab>
  <Tab title="GPU 加速">
    ```python
    from semantica.embeddings import EmbeddingGenerator

    # Use CUDA via sentence-transformers
    generator = EmbeddingGenerator(config={"text": {"method": "sentence_transformers", "device": "cuda"}})

    # Apple Silicon (M1/M2/M3)
    generator = EmbeddingGenerator(config={"text": {"method": "sentence_transformers", "device": "mps"}})
    ```

    GPU 只对 sentence-transformers 生效。FastEmbed 走 ONNX，不使用 `device`。
  </Tab>
</Tabs>

### 构造参数

| 参数 | 类型 | 默认值 | 说明 |
| :--------- | :---- | :------- | :----------- |
| `config` | `dict` | `None` | 配置 dict；`config["text"]` 传给 `TextEmbedder` |
| `**kwargs` | | | 其余键值配置，合并进 `config` |

构造后用 `generator.set_text_model(method, model_name)` 切换嵌入模型。

## TextEmbedder

直接做文本嵌入，带批处理：

```python
from semantica.embeddings import TextEmbedder

# Default: FastEmbed with BAAI/bge-small-en-v1.5
embedder = TextEmbedder()

# Single text → 1D array
embedding = embedder.embed_text("A knowledge graph connects entities with typed relationships.")

# Batch → 2D array (n_texts, dim)
embeddings = embedder.embed_batch(["First text", "Second text", "Third text"])

# Per-sentence embeddings
sentence_embeddings = embedder.embed_sentences("First sentence. Second sentence.")

# Get embedding dimension
dim = embedder.get_embedding_dimension()
```

### TextEmbedder 构造参数

| 参数 | 类型 | 默认值 | 说明 |
| :--------- | :---- | :------- | :----------- |
| `model_name` | `str` | `"BAAI/bge-small-en-v1.5"` | 要加载的模型名 |
| `method` | `str` | `"fastembed"` | 嵌入方法：`"fastembed"` 或 `"sentence_transformers"` |
| `device` | `str` | `"cpu"` | sentence-transformers 的设备：`"cpu"`、`"cuda"`、`"mps"`。FastEmbed 忽略此项。 |
| `normalize` | `bool` | `True` | 对输出向量做 L2 归一化 |

**关键行为：**
- FastEmbed 或 sentence-transformers 不可用时，回退到 128 维的基于哈希的嵌入。哈希嵌入是确定性的但没有语义：不要用于生产。
- 大批次会在底层库内部先分块再处理，避免内存溢出(OOM)。

<Warning>
  **维度不匹配。**传给向量存储的维度必须与嵌入模型的输出完全一致。`BAAI/bge-small-en-v1.5` → 384、`all-MiniLM-L6-v2` → 384、`all-mpnet-base-v2` → 768、`BAAI/bge-large-en-v1.5` → 1024。建 store 前先用 `embedder.get_embedding_dimension()` 确认。
</Warning>

<Tip>
  **回退嵌入没有语义。**FastEmbed 和 sentence-transformers 都加载失败时，TextEmbedder 会静默回退到 128 维 SHA-256 哈希嵌入。它确定性但不含语义。检查 `embedder.get_method()`：返回 `"fallback"` 就安装你想要的提供商。
</Tip>

## 提供商 Store

需要对单个后端做细粒度控制时，直接用提供商 store：

```python
from semantica.embeddings import (
    OpenAIStore, BGEStore, FastEmbedStore,
    ProviderStoreFactory,
)
import os

# OpenAI
store     = OpenAIStore(api_key=os.getenv("OPENAI_API_KEY"), model="text-embedding-3-small")
embedding = store.embed("Hello world")

# BGE (Sentence-Transformers wrapper): pass model_name= not model=
store     = BGEStore(model_name="BAAI/bge-large-en-v1.5")
embedding = store.embed("Hello world")

# FastEmbed: ONNX runtime, no CUDA required
store     = FastEmbedStore(model_name="BAAI/bge-small-en-v1.5")
embedding = store.embed("Hello world")
# FastEmbedStore also has an efficient batch method
embeddings = store.embed_batch(["text1", "text2", "text3"])

# Auto-select from a name string: useful in config-driven pipelines
# Supported providers: "openai", "bge", "fastembed"
store = ProviderStoreFactory.create(provider="bge", model_name="BAAI/bge-large-en-v1.5")
```

<Note>
  `LlamaStore` 存在于模块中但只是占位：不连接 Ollama，嵌入时总是抛 `ProcessingError`。不要用于生产。
</Note>

<Warning>
  **LlamaStore 不可用。**`LlamaStore` 存在于模块中但不连接 Ollama，嵌入时总是抛 `ProcessingError`。本地 ONNX 嵌入用 `FastEmbedStore`，本地 sentence-transformers 嵌入用 `BGEStore`。
</Warning>

## 池化策略

池化(Pooling)做的事很直观：把一组向量压成一个能代表全体的向量。因此需要合并多个分块的嵌入时，就会用到它：

<Tabs>
  <Tab title="MeanPooling（默认）">
    ```python
    from semantica.embeddings import MeanPooling

    pooler = MeanPooling()
    pooled = pooler.pool(token_embeddings)   # shape: (hidden_dim,)
    ```

    **最适合：** 检索、语义检索和聚类——对所有贡献取平均。
  </Tab>
  <Tab title="MaxPooling">
    ```python
    from semantica.embeddings import MaxPooling

    pooler = MaxPooling()
    pooled = pooler.pool(token_embeddings)
    ```

    **最适合：** 捕捉任一特征的存在——每个维度取最大激活。
  </Tab>
  <Tab title="CLSPooling">
    ```python
    from semantica.embeddings import CLSPooling

    pooler = CLSPooling()
    pooled = pooler.pool(token_embeddings)
    ```

    **最适合：** 分类类任务；显式以 CLS 池化训练的模型（BERT）。
  </Tab>
  <Tab title="HierarchicalPooling">
    ```python
    from semantica.embeddings import HierarchicalPooling

    pooler = HierarchicalPooling()
    # chunk_size is passed at pool time, not at construction
    pooled = pooler.pool(token_embeddings, chunk_size=10)
    ```

    **最适合：** 长文档——先分块平均池化，再跨块全局平均池化。
  </Tab>
  <Tab title="策略对比">

    | 策略 | 适用场景 |
    | :-------- | :----------- |
    | `mean` | 检索、语义检索和聚类的默认选择 |
    | `max` | 想捕捉任一特征的存在，而非平均存在度 |
    | `cls` | 分类类任务；显式以 CLS 池化训练的模型（BERT） |
    | `attention` | token 重要性差异显著时；更慢但更准 |
    | `hierarchical` | 多分块的长文档；先分块池化再全局池化 |

    ```python
    from semantica.embeddings import PoolingStrategyFactory

    pooler = PoolingStrategyFactory.create(strategy="mean")
    ```

  </Tab>
</Tabs>

## GraphEmbeddingManager

嵌入图节点和边，存入图数据库：

```python
from semantica.embeddings import GraphEmbeddingManager

manager = GraphEmbeddingManager()

entities = [
    {"id": "e1", "text": "Apple Inc.", "type": "Organization"},
    {"id": "e2", "text": "Tim Cook",   "type": "Person"},
]
relationships = [
    {"source": "e2", "target": "e1", "type": "CEO_OF"}
]

# Embed entities → dict of {id: np.ndarray}
node_embeddings = manager.embed_entities(entities)

# Embed relationships → dict of {id: np.ndarray}
edge_embeddings = manager.embed_relationships(relationships)

# Or prepare everything at once for a graph DB backend
result = manager.prepare_for_graph_db(entities, relationships, backend="neo4j")
# result["node_embeddings"] → {id: np.ndarray}
# result["edge_embeddings"] → {id: np.ndarray}
# result["nodes"]           → entities with "embedding" field added
# result["edges"]           → relationships with "embedding" field added
```

**支持的后端：** `"neo4j"`、`"networkx"`、`"falkordb"`

## VectorEmbeddingManager

为向量数据库存储准备并校验嵌入：

```python
from semantica.embeddings import VectorEmbeddingManager
import numpy as np

manager    = VectorEmbeddingManager()
embeddings = np.random.rand(5, 384).astype(np.float32)
metadata   = [{"text": f"doc_{i}", "category": "science"} for i in range(5)]

# Prepare for FAISS
result = manager.prepare_for_vector_db(embeddings, metadata=metadata, backend="faiss")
# result["vectors"]  → L2-normalized float32 array
# result["ids"]      → ["vec_0", "vec_1", ...]
# result["metadata"] → formatted metadata list

# Validate dimensions before insertion
is_valid = manager.validate_dimensions(embeddings, backend="milvus")

# Prepare multiple batches at once
combined = manager.batch_prepare([embeddings_a, embeddings_b], backend="qdrant")
```

**支持的后端：** `"faiss"`、`"weaviate"`、`"qdrant"`、`"milvus"`

## 常见工作流

<Tabs>
  <Tab title="批量文本嵌入">
    ```python
    from semantica.embeddings import TextEmbedder

    embedder = TextEmbedder()   # default: FastEmbed

    texts = [
        "Apple Inc. was founded by Steve Jobs.",
        "Microsoft was co-founded by Bill Gates.",
        "Amazon was started by Jeff Bezos.",
    ]

    # All at once: more efficient than calling embed_text() per item
    embeddings = embedder.embed_batch(texts)
    print(f"Shape: {embeddings.shape}")   # (3, 384)
    ```
  </Tab>
  <Tab title="提供商对比">
    ```python
    from semantica.embeddings import check_available_providers, EmbeddingGenerator

    # Check what's installed
    available = check_available_providers()
    # → {"sentence_transformers": True, "fastembed": True, "openai": False}

    # Use the fastest available provider
    generator = EmbeddingGenerator()
    if available["fastembed"]:
        generator.set_text_model("fastembed", "BAAI/bge-small-en-v1.5")
    elif available["sentence_transformers"]:
        generator.set_text_model("sentence_transformers", "all-MiniLM-L6-v2")

    embeddings = generator.generate_embeddings(texts)
    ```
  </Tab>
  <Tab title="图节点嵌入">
    ```python
    from semantica.embeddings import GraphEmbeddingManager

    manager  = GraphEmbeddingManager()
    entities = [{"id": "n1", "text": "Python"}, {"id": "n2", "text": "Django"}]

    node_embeddings = manager.embed_entities(entities)
    # {"n1": array([...]), "n2": array([...])}
    ```
  </Tab>
  <Tab title="相似度检索">
    ```python
    from semantica.embeddings import EmbeddingGenerator, calculate_similarity
    import numpy as np

    generator = EmbeddingGenerator()
    query     = generator.generate_embeddings("knowledge graph databases")
    corpus    = generator.generate_embeddings([
        "graph databases store relationships",
        "relational databases use tables",
        "knowledge graphs model entity relationships",
    ])

    scores = [calculate_similarity(query, doc, method="cosine") for doc in corpus]
    ranked = sorted(zip(scores, range(len(scores))), reverse=True)

    for score, idx in ranked:
        print(f"{score:.3f}  {['graph databases store...', 'relational databases...', 'knowledge graphs...'][idx]}")
    ```
  </Tab>
</Tabs>

## 相似度计算

```python
from semantica.embeddings import calculate_similarity

# Cosine similarity: direction only, not magnitude; most common for text
score = calculate_similarity(embedding_a, embedding_b, method="cosine")
# → 0.0 (orthogonal / unrelated) to 1.0 (identical direction)

# Euclidean distance converted to similarity
score = calculate_similarity(embedding_a, embedding_b, method="euclidean")
```

## 便捷函数

```python
from semantica.embeddings import (
    embed_text, generate_embeddings, calculate_similarity,
    pool_embeddings, check_available_providers,
)

# Single text: fastest path
emb = embed_text("Hello world", method="sentence_transformers")

# Batch
embs = generate_embeddings(["text1", "text2"], method="default")

# Pool multiple embeddings into one
pooled = pool_embeddings(embs, method="mean")

# Check which providers are installed
providers = check_available_providers()
# → {"sentence_transformers": True, "fastembed": True, "openai": False}
```

- [Vector Store](./vector_store.md) — 存储并检索生成的嵌入。
- [Split](./split.md) — 嵌入前先分块，检索质量更好。
- [KG Module](./kg.md) — 距离智能用图嵌入定义语义邻域。
- [Deduplication](./deduplication.md) — 语义去重用嵌入距离做实体消解。
