---
title: "分块模块（Split）"
description: "文本分块：递归、语义、实体感知、关系感知、结构化与滑动窗口等切分策略。"
source: reference/split.md
source_version: 2a6484505037f206c1c91b1ceab9c4dab49f3ec7
icon: "scissors"
---

**`semantica.split`** 把文档切成**保留语义上下文**的块：

- 六种分块策略：递归、语义、实体感知、关系感知、滑动窗口、结构化
- `SemanticChunker` 用基于嵌入的主题偏移检测，只在内容真正变化处切分
- `EntityAwareChunker` 保证实体提及不跨块边界
- `RelationAwareChunker` 把"主-谓-宾"三元组留在同一个块内
- 分块质量直接决定下游嵌入准确率和实体抽取质量


## 为什么分块很重要

大多数大语言模型(LLM)和嵌入模型的上下文窗口是固定的。超过窗口的文档必须切分。但朴素切分（每 500 字符一刀切，不管结构）会破坏语义上下文：

- "Apple Inc." 这样的实体提及被切到两个块里，两边都丢了上下文
- "Steve Jobs founded Apple" 这样的关系三元组在 "Steve Jobs" 处切开，主语就悬空了
- 把两个不相关主题混在一个块里做嵌入，得到的质心向量跟谁都匹配不上

Semantica 的分块方法就是为避免这些失败模式设计的。

## 导出的类

| 类 | 职责 |
| :--- | :--- |
| `TextSplitter` | 统一入口：换 `method=` 不用改下游代码 |
| `Chunk` | `{text, start_index, end_index, metadata, id}` |
| `SemanticChunker` | 基于嵌入的主题偏移检测：只在内容真正变化处切分 |
| `StructuralChunker` | 基于标题/章节的结构化文本分析切分 |
| `EntityAwareChunker` | 防止命名实体提及被切到块边界两侧 |
| `RelationAwareChunker` | 把"主-谓-宾"三元组完整保留在单个块内 |
| `HierarchicalChunker` | 多级分块，产出父/子块关系 |

**`TextSplitter` 可用的 `method=` 取值：**

| 方法 | 适用场景 |
| :--- | :--- |
| `recursive` | 常规文本：按段落、句子、单词依次切分 |
| `sentence` | 会话文本、问答 |
| `paragraph` | 段落完整性重要的长文 |
| `token` | LLM 上下文窗口控制 |
| `semantic_transformer` | 有主题偏移的长文档 |
| `entity_aware` | 知识图谱抽取流水线 |
| `relation_aware` | 三元组完整性重要的 KG 流水线 |
| `structural` | 有标题/段落结构的文本 |
| `sliding_window` | 面向双编码器检索的稠密重叠 |

## 你能得到什么

- **TextSplitter** — 11 种分块策略的统一接口：换方法不用改下游代码。
- **语义分块** — 基于嵌入的主题偏移检测：只在主题真正变化处切分。
- **实体感知分块** — 实体跨度绝不跨块边界：由边界调整保证。
- **关系感知分块** — "主-谓-宾"三元组保留在单个块内，服务 KG 流水线。
- **Chunk 对象** — 输出 dataclass，含文本、字符偏移、可选 id 和方法专属元数据。

## 快速开始

<Steps>
  <Step title="选择切分方法">
    ```python
    from semantica.split import TextSplitter

    splitter = TextSplitter(
        method="recursive",   # see Splitting Methods table
        chunk_size=1000,
        chunk_overlap=200,
    )
    ```
  </Step>
  <Step title="切分原始文本">
    ```python
    chunks = splitter.split(text)

    for chunk in chunks:
        print(f"  Start: {chunk.start_index}, End: {chunk.end_index}")
        print(f"  Method: {chunk.metadata.get('method')}")
        print(f"  Preview: {chunk.text[:80]}...")
    ```
  </Step>
  <Step title="或者切分文档对象">
    ```python
    # split_documents() accepts any object with a .text attribute,
    # or a plain string: no specific document class required.
    class Doc:
        def __init__(self, text, metadata=None):
            self.text = text
            self.metadata = metadata or {}

    doc = Doc(text="Annual report content...", metadata={"source": "annual_report.pdf"})

    splitter = TextSplitter(method="structural")
    chunks   = splitter.split_documents([doc])

    for chunk in chunks:
        print(f"  {chunk.text[:80]}...")
    ```
  </Step>
  <Step title="批量切分文档列表">
    ```python
    # split_documents() returns a flat List[Chunk] across all inputs
    all_chunks = splitter.split_documents(docs)

    for chunk in all_chunks:
        print(chunk.text[:80])
    ```
  </Step>
</Steps>

## 切分方法

| 方法 | 切分方式 | 适用场景 |
| :------ | :------------- | :-------- |
| `recursive` | 段落 → 句子 → 单词（级联回退） | 通用默认选择 |
| `semantic_transformer` | 嵌入句子，在余弦相似度下降处切分 | 检索增强生成(RAG)：主题连贯性重要时 |
| `entity_aware` | 调整边界，保证实体跨度不被切断 | 命名实体识别(NER)流水线 |
| `relation_aware` | 把"主-谓-宾"三元组留在同一块内 | 知识图谱构建 |
| `sentence` | 句子边界检测（regex、NLTK、spaCy） | 短文档、问答 |
| `paragraph` | 段落边界切分 | 长文章、报告 |
| `token` | 用 tiktoken 或 transformers 数 token；硬截断 | LLM 上下文窗口准备 |
| `word` | 按词数带重叠 | 简单的近似 token 切分 |
| `character` | 固定字符数带重叠；最快，无 NLP | 简单批处理 |
| `sliding_window` | 固定大小窗口按步长推进；重叠可配置 | 稠密检索（ColBERT、DPR） |
| `structural` | 标题/段落结构检测 | 有明确标题层级的文本 |
| `embedding_semantic` | 嵌入相似度边界（`semantic_transformer` 的别名） | 基于嵌入连贯性的 RAG |
| `hierarchical` | 多级章节 → 段落 → 句子分块 | 多粒度检索 |

## 策略选择

选方法前先过一遍这棵决策树：

- **构建知识图谱(KG)？** → `relation_aware`（保持三元组完整）；纯 NER 用 `entity_aware`
- **检索质量至上的 RAG 系统？** → `semantic_transformer`
- **双编码器检索的稠密重叠（ColBERT、DPR）？** → `sliding_window`
- **给固定窗口 LLM 准备提示词？** → `token`
- **带标题的结构化文本？** → `structural`
- **段落级连贯性？** → `paragraph` 或 `sentence`
- **不要 NLP 开销的快速切分？** → `recursive` 或 `character`

## TextSplitter 构造参数

```python
from semantica.split import TextSplitter

splitter = TextSplitter(
    method="semantic_transformer",   # chunking strategy: see Splitting Methods table
    chunk_size=1000,                 # target size in characters
    chunk_overlap=200,               # character overlap between adjacent chunks
    similarity_threshold=0.7,        # cosine similarity cutoff (semantic_transformer only)
    model="all-MiniLM-L6-v2",        # sentence-transformers model name (semantic_transformer only)
    ner_method="ml",                 # NER method (entity_aware only)
    relation_method="ml",            # relation extraction method (relation_aware only)
)
```

| 参数 | 类型 | 默认值 | 说明 |
| :--------- | :---- | :------- | :----------- |
| `method` | `str \| list[str]` | `"recursive"` | 分块策略，或作为回退链的方法列表 |
| `chunk_size` | `int` | `1000` | 目标大小，单位为**字符**（不是 token：若你之前用 token 计尺寸，乘以约 4 可近似同样的边界） |
| `chunk_overlap` | `int` | `200` | 相邻块之间的字符重叠 |
| `similarity_threshold` | `float` | `0.7` | `semantic_transformer` 的余弦相似度阈值：越低切得越多 |
| `model` | `str` | `"all-MiniLM-L6-v2"` | `semantic_transformer` 用的 sentence-transformers 模型名 |
| `ner_method` | `str` | `"ml"` | `entity_aware` 的 NER 方法：`"pattern"` \| `"regex"` \| `"ml"` \| `"huggingface"` \| `"llm"` |
| `relation_method` | `str` | `"ml"` | `relation_aware` 的关系抽取方法：`"ml"` \| `"llm"` \| `"huggingface"` |
| `tokenizer` | `str` | `"gpt-4"` | `token` 方法的 tiktoken 模型名：无法识别的名字回退到 `cl100k_base` |

<Warning>
  **`chunk_overlap` 不能太小。** 没有重叠的话，跨块边界的事实会在两个块里都不可见。相对 `chunk_size` 10–20% 的重叠是安全下限：`chunk_size=1000` 时，`chunk_overlap` 设 100 到 200。
</Warning>

## 切分方法详解

<Tabs>
  <Tab title="Recursive（默认）">
    先尝试段落断点，再句子边界，再单词边界：只有块超过 `chunk_size` 时才回退：

    ```python
    splitter = TextSplitter(method="recursive", chunk_size=1000, chunk_overlap=200)
    chunks   = splitter.split(text)
    ```

    **关键行为：**
    - 尽可能保留段落和句子结构
    - 优雅回退：产出的块不会超过 `chunk_size`
    - 重叠保证块边界两侧的上下文连续
    - 不确定用哪种方法时的良好起点
  </Tab>
  <Tab title="Semantic（语义）">
    用 sentence-transformers 模型嵌入每个句子，当相邻句子的余弦相似度低于 `similarity_threshold` 时切分。每个块覆盖一个连贯主题：

    ```python
    from semantica.split import TextSplitter

    splitter = TextSplitter(
        method="semantic_transformer",
        model="all-MiniLM-L6-v2",      # any sentence-transformers model name
        similarity_threshold=0.7,       # 0.6 = more splits, 0.8 = fewer splits
        chunk_size=800,
        chunk_overlap=0,                # not needed: chunks are already coherent
    )
    chunks = splitter.split(text)
    ```

    **关键行为：**
    - 需要 `sentence-transformers` 包：默认用 `all-MiniLM-L6-v2`，可通过 `model=` 配置
    - 产出变长块：有的主题短，有的主题长
    - 未安装 `sentence-transformers` 时回退为句子切分
    - 因嵌入计算而比 `recursive` 慢；重复切分请缓存嵌入

    <Tip>
      **语义切分需要足够的句子。** `semantic_transformer` 需要多个句子才能检测主题偏移。短于约 300 词的文档上，它的表现退化为 `sentence` 切分：改用 `recursive`。
    </Tip>
  </Tab>
  <Tab title="Entity-Aware（实体感知）">
    内部先跑 NER，再调整块边界，保证没有任何实体提及被切到两个块里：

    ```python
    from semantica.split import TextSplitter
    import os

    # ner_method is passed through to the internal NERExtractor.
    # Use "llm" for highest accuracy, "ml" (default) for speed.
    splitter = TextSplitter(
        method="entity_aware",
        chunk_size=512,
        chunk_overlap=50,
        ner_method="ml",   # "pattern" | "regex" | "ml" | "huggingface" | "llm"
    )
    chunks = splitter.split(text)

    for chunk in chunks:
        print(f"  entities in chunk: {chunk.metadata.get('entity_count', 0)}")
        print(f"  preview: {chunk.text[:80]}...")
    ```

    **关键行为：**
    - NER 在内部运行：实体抽取在切分器里自动完成
    - 每个块的 `chunk.metadata["entities"]` 里有实体对象
    - 块大小与 `chunk_size` 略有出入：边界调整不超过一个句子
    - 支持所有实体类型：PERSON、ORGANIZATION、LOCATION、DATE 及自定义类型
  </Tab>
  <Tab title="Relation-Aware（关系感知）">
    把"主-谓-宾"三元组保留在同一个块内：KG 流水线的关键能力：

    ```python
    from semantica.split import TextSplitter

    # relation_method is passed through to the internal RelationExtractor.
    # Use "llm" for highest accuracy, "ml" (default) for speed.
    splitter = TextSplitter(
        method="relation_aware",
        chunk_size=512,
        relation_method="ml",   # "ml" | "llm" | "huggingface"
    )
    chunks = splitter.split(text)

    for chunk in chunks:
        print(f"  relations in chunk: {chunk.metadata.get('relation_count', 0)}")
        for rel in chunk.metadata.get("relationships", []):
            print(f"  {rel}")
    ```

    **关键行为：**
    - 关系抽取在内部运行：无需预先算好的实体或三元组
    - 每个块的 `chunk.metadata["relationships"]` 里有关系对象
    - 隐含实体感知行为：三元组中的两个实体也会保持完整
    - 最适合作为 `Parse → Split → Extract → Build KG` 流水线中的切分步骤
  </Tab>
  <Tab title="Structural（结构化）">
    基于标题和段落边界的结构分析切分文本。每个标题或段落组成为一个块边界：

    ```python
    from semantica.split import TextSplitter

    splitter = TextSplitter(method="structural")
    chunks   = splitter.split(text)

    for chunk in chunks:
        print(f"  {chunk.text[:80]}...")
        print(f"  start: {chunk.start_index}, end: {chunk.end_index}")
    ```

    **关键行为：**
    - 作用于纯文本：不要求特定的结构化文档格式
    - 尊重标题层级（`#` 开头的行或全大写标题）和段落断点
    - 用 `max_chunk_size=` 参数（而非标准的 `chunk_size=`）控制最大尺寸
    - `StructuralChunker` 不可用时回退为 `recursive`
  </Tab>
</Tabs>

## Chunk 模式

<AccordionGroup>
  <Accordion title="Chunk dataclass">

```python
@dataclass
class Chunk:
    text:        str                    # the chunk's text content
    start_index: int                    # character offset of start in source text
    end_index:   int                    # character offset of end in source text
    metadata:    Dict[str, Any]         # method-specific fields: see table below
    id:          Optional[str] = None   # optional chunk identifier
```

  </Accordion>
  <Accordion title="Chunk 元数据字段">

元数据键因方法而异。只列出实现实际会设置的键。

| 字段 | 类型 | 设置者 | 说明 |
| :----- | :---- | :------ | :----------- |
| `method` | `str` | 所有方法 | 产出该块的切分方法 |
| `chunk_size` | `int` | 大多数方法 | 该块的字符长度 |
| `sentence_count` | `int` | `sentence`、`semantic_transformer`、spaCy 路径 | 该块的句子数 |
| `paragraph_count` | `int` | `paragraph` | 该块的段落数 |
| `word_count` | `int` | `word` | 该块的词数 |
| `token_count` | `int` | `token`；spaCy 可用时的 `sentence`/`semantic_transformer` | Token 数：不一定存在 |
| `entity_count` | `int` | `entity_aware` | 边界落在该块内的实体数 |
| `entities` | `list` | `entity_aware` | 边界落在该块内的实体对象 |
| `relation_count` | `int` | `relation_aware` | 该块内的关系三元组数 |
| `relationships` | `list` | `relation_aware` | 该块内的关系对象 |
| `element_count` | `int` | `structural` | 归入该块的结构元素数 |
| `element_types` | `list[str]` | `structural` | 元素类型：`"heading"`、`"paragraph"`、`"list"` 等 |

  </Accordion>
</AccordionGroup>

## Tokenizer 选项

`token` 方法接受 `tokenizer=` 关键字参数，传给 `tiktoken.encoding_for_model()`。值应为 tiktoken 模型名。无法识别的名字自动回退到 `cl100k_base`。

| 取值 | 使用的编码 |
| :----- | :------------- |
| `"gpt-4"`（默认） | `cl100k_base` |
| `"gpt-3.5-turbo"` | `cl100k_base` |
| `"text-embedding-ada-002"` | `cl100k_base` |
| 任何无法识别的字符串 | 回退到 `cl100k_base` |

未安装 `tiktoken` 时，`token` 方法回退为按空白分词切分。

<Warning>
  **Tokenizer 别传错。** `token` 方法把 `tokenizer=` 的值传给 `tiktoken.encoding_for_model()`。模型名不被 tiktoken 识别时会静默回退到 `cl100k_base`。传有效的 tiktoken 模型名（如 `"gpt-4"`、`"gpt-3.5-turbo"`）才能获得确定性行为。
</Warning>

## 流水线集成

`TextSplitter` 可以独立使用，也可以手动与其他 Semantica 模块组合。下面的例子展示顺序模式：解析文件、切分文本、再从每个块抽取实体：

```python
from semantica.parse import DocumentParser
from semantica.split import TextSplitter
from semantica.semantic_extract import NERExtractor

# Parse
parser = DocumentParser()
parsed = parser.parse("data/report.pdf")   # returns a dict with "full_text" key

# Split
splitter = TextSplitter(method="semantic_transformer", chunk_size=512)
chunks   = splitter.split(parsed["full_text"])

# Extract from each chunk
ner = NERExtractor(method="ml")

for chunk in chunks:
    entities = ner.extract(chunk.text)
    print(f"  {len(entities)} entities in chunk starting at {chunk.start_index}")
```

完整的流水线编排 API 见 [Pipeline 参考](./pipeline.md)。

- [Parse](./parse.md) — 分块前先解析文档：产出章节和元数据。
- [Embeddings](../../reference/embeddings.md) — 为向量检索和语义分块生成块嵌入。
- [Semantic Extract](../../reference/semantic_extract.md) — 从单个块抽取实体和关系。
- [Pipeline](./pipeline.md) — 把切分集成为具名流水线步骤。
