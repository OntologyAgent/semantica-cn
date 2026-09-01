---
title: "语义抽取模块（Semantic Extract）"
description: "命名实体识别(NER)、关系抽取、事件检测与三元组生成。"
source: reference/semantic_extract.md
source_version: 8f5a58dfbeac2c4f48748dff556394c9a2db63e1
icon: "magnifying-glass-chart"
---

`semantica.semantic_extract` 从非结构化文本中抽取结构化信息：Semantica 里每张知识图谱的地基：

- `NERExtractor`：命名实体识别(NER)，带置信度得分和来源归属
- `RelationExtractor`：带类型的关系抽取（`founded_by`、`located_in` 及自定义类型）
- `TripletExtractor`：直接生成 `(subject, predicate, object)` 三元组，供 RDF 输出
- `EventDetector`：事件检测，带参与者、时间上下文和置信度
- 每个抽取器都有三种抽取模式：`"pattern"`（无需 API key）、`"huggingface"`、`"llm"`


## 快速开始

### 前置准备与安装

**第 1 步：安装依赖**

```bash
# Basic extraction (pattern methods only)
pip install semantica

# HuggingFace models for advanced NER
pip install semantica[models-huggingface]

# LLM-based extraction (highest accuracy)
pip install semantica[llm-groq]    # or llm-openai
```

**第 2 步：设置 API Key**（仅 LLM 方法需要）

```bash
export GROQ_API_KEY="your_groq_key_here"
export OPENAI_API_KEY="your_openai_key_here"
```

**第 3 步：第一次抽取**

```python
from semantica.semantic_extract import NERExtractor

# Start with pattern method (no setup required)
ner = NERExtractor(method="pattern")
entities = ner.extract("Apple Inc. was founded by Steve Jobs.")
print(f"Found {len(entities)} entities")
# Output: Found 2 entities

# Upgrade to LLM for better accuracy
from semantica.llms import Groq
import os

llm = Groq(api_key=os.getenv("GROQ_API_KEY"))
ner = NERExtractor(method="llm", llm_provider=llm)
entities = ner.extract("Apple Inc. was founded by Steve Jobs.")
```


## 导出的类

<Tip>
  **`NamedEntityRecognizer`** 是高层协调器，带置信度阈值过滤和重叠合并。**`NERExtractor`** 是底层实现。多数场景用 `NERExtractor` 求简单，要细粒度控制就用 `NamedEntityRecognizer`。
</Tip>

| 类 | 职责 |
| :--- | :--- |
| `NamedEntityRecognizer` | 高层 NER：带置信度阈值过滤和重叠合并 |
| `NERExtractor` | 核心 NER 实现：图简单可直接用 |
| `RelationExtractor` | 带类型的关系抽取（`founded_by`、`located_in` 等） |
| `TripletExtractor` | 直接生成 `(subject, predicate, object)` 三元组，供 RDF 输出 |
| `EventDetector` | 事件检测：带参与者、时间上下文和置信度得分 |
| `CoreferenceResolver` | 把 "Apple" 和 "the company" 消解为同一个规范实体 |
| `Entity` | `{id, text, type, confidence, start, end}` |
| `Relation` | `{subject, predicate, object, confidence}` |
| `Event` | `{type, participants, temporal, location, confidence}` |

## 方法选择指南

<Tabs>
  <Tab title="Pattern：零配置">
    零依赖，无需 API key。用 spaCy 规则和正则匹配标准实体类型。

    | | |
    | :-- | :-- |
    | **安装** | 无：开箱即用 |
    | **成本** | 免费 |
    | **准确率** | 标准实体类型表现良好 |
    | **最适合** | 快速原型、批处理、离线隔离系统 |

    ```python
    from semantica.semantic_extract import NERExtractor, RelationExtractor

    ner = NERExtractor(method="pattern")
    entities = ner.extract("Apple Inc. was founded by Steve Jobs in Cupertino.")

    rel = RelationExtractor(method="pattern")
    relationships = rel.extract(text, entities=entities)
    ```
  </Tab>
  <Tab title="HuggingFace：自定义模型">
    任何预训练或微调过的 transformer 模型都行。本地推理，免费。

    | | |
    | :-- | :-- |
    | **安装** | `pip install semantica[models-huggingface]` |
    | **成本** | 免费（本地算力） |
    | **准确率** | 领域专属 NER 表现优秀 |
    | **最适合** | 医学 NER、自定义微调模型、零 API 成本 |

    ```python
    from semantica.semantic_extract import NERExtractor

    ner = NERExtractor(method="huggingface")

    # Pass model per-call
    entities = ner.extract(text, model="dslim/bert-base-NER", device="cpu")

    # Biomedical NER
    entities = ner.extract(text, model="d4data/biomedical-ner-all")
    ```
  </Tab>
  <Tab title="LLM：准确率最高">
    复杂模式和自定义实体类型上准确率最高。需要 LLM API key。

    | | |
    | :-- | :-- |
    | **安装** | `pip install semantica[llm-groq]` + API key |
    | **成本** | 取决于提供商 |
    | **准确率** | 最高：能处理复杂类型和上下文 |
    | **最适合** | 生产环境、自定义实体类型、复杂关系模式 |

    ```python
    import os
    from semantica.llms import Groq
    from semantica.semantic_extract import NERExtractor, RelationExtractor, TripletExtractor

    llm = Groq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

    ner  = NERExtractor(method="llm",  llm_provider=llm, max_retries=3)
    rel  = RelationExtractor(method="llm", llm_provider=llm)
    trip = TripletExtractor(method="llm", llm_provider=llm)

    entities      = ner.extract(text)
    relationships = rel.extract(text, entities=entities)
    triplets      = trip.extract(text)
    ```
  </Tab>
  <Tab title="回退链">
    按优先级依次尝试各方法：首选方法不可用时也能保证产出非空结果。

    ```python
    from semantica.semantic_extract import NERExtractor, RelationExtractor

    # Try LLM first, fall back to pattern on error
    ner = NERExtractor(method=["llm", "pattern"])
    rel = RelationExtractor(method=["llm", "pattern"])

    # Always returns results: safe for production pipelines
    entities      = ner.extract(text)
    relationships = rel.extract(text, entities=entities)
    ```

    <Tip>
      在 API 可用性没有保障的流水线里（限流、网络问题）用回退链。列表中的第一个方法总是先被尝试。
    </Tip>
  </Tab>
</Tabs>

### 各抽取器的方法可用性

| 抽取器 | `pattern` | `huggingface` | `llm` | 备注 |
| :----------- | :----------- | :--------------- | :------- | :------- |
| `NERExtractor` | ✅ | ✅ | ✅ | 支持全部方法 |
| `RelationExtractor` | ✅ | ✅ | ✅ | 另支持 `dependency`、`cooccurrence` |
| `TripletExtractor` | ✅ | ✅ | ✅ | 另支持 `rules` 方法 |
| `EventDetector` | ✅ | ❌ | ✅ | 仅 pattern 和 LLM |

### 方法回退链

为了可靠性，抽取器支持回退链：按顺序尝试各方法直到某个成功：

```python
# Try LLM first, fall back to pattern if it fails
ner = NERExtractor(method=["llm", "pattern"])
rel = RelationExtractor(method=["llm", "pattern"]) 
trip = TripletExtractor(method=["llm", "pattern"])

# Always returns results - guarantees non-empty extraction
entities = ner.extract(text)
```


## 极简上手

```python
from semantica.semantic_extract import NERExtractor, RelationExtractor, TripletExtractor
from semantica.llms import Groq
import os

text = "Apple Inc. was founded by Steve Jobs in Cupertino in 1976."
llm  = Groq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

entities      = NERExtractor(method="llm", llm_provider=llm).extract(text)
relationships = RelationExtractor(method="llm", llm_provider=llm).extract(text, entities=entities)
triplets      = TripletExtractor(method="llm", llm_provider=llm).extract(text)
```

<img src="/assets/img/diagrams/extraction-pipeline.svg" alt="Semantic extraction pipeline: raw text fans into NER, Relation, and Coreference extractors, then merges into a Triplet Generator" style={{ width: '100%', borderRadius: '12px', margin: '0 0 24px' }} />


## 抽取器方法

| 方法 | 返回 | 说明 |
| :------ | :------- | :----------- |
| `extract(text)` | `List[Entity]` / `List[Relation]` / `List[Triplet]` / `List[Event]` | 从单个文本输入抽取 |
| `extract(texts)` | `List[List[...]]` | 处理多个文本（自动识别批输入） |


## NERExtractor

```python
from semantica.semantic_extract import NERExtractor
from semantica.llms import Groq
import os

# Pattern-based: fast, no API key, good for standard entity types
ner = NERExtractor(method="pattern")
entities = ner.extract("Apple Inc. was founded by Steve Jobs in Cupertino.")

# HuggingFace-based: custom models, no API cost
ner = NERExtractor(method="huggingface")
entities = ner.extract(text, model="dslim/bert-base-NER", device="cpu")

# LLM-based: best accuracy, handles complex schemas and custom types
llm = Groq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))
ner = NERExtractor(method="llm", llm_provider=llm, max_retries=3)
entities = ner.extract(text)
```

输出格式：

```python
[
    {"text": "Apple Inc.",  "type": "ORGANIZATION", "confidence": 0.98, "start": 0,  "end": 10},
    {"text": "Steve Jobs",  "type": "PERSON",       "confidence": 0.99, "start": 27, "end": 37},
    {"text": "Cupertino",   "type": "LOCATION",     "confidence": 0.97, "start": 41, "end": 50}
]
```

### 自定义实体类型

```python
ner = NERExtractor(
    method="pattern",
    custom_entities={
        "DRUG": ["aspirin", "ibuprofen", "metformin"],
        "GENE": ["BRCA1", "TP53", "EGFR"]
    }
)
```

<Note>
  **v0.5.0 修复：** `NERExtractor(method="llm")` 遇到自定义网关时不再静默回退到 pattern 抽取。对不兼容的网关，现在会有条件地省略 `response_format=json_object` 参数，并自动应用普通 `generate()` + JSON 解析的回退路径。
</Note>

## RelationExtractor

```python
from semantica.semantic_extract import RelationExtractor

rel = RelationExtractor(method="llm", llm_provider=llm, max_retries=3)
relationships = rel.extract(text, entities=entities)
```

输出格式：

```python
[
    {"subject": "Steve Jobs", "predicate": "founded",    "object": "Apple Inc.", "confidence": 0.92},
    {"subject": "Apple Inc.", "predicate": "located_in", "object": "Cupertino",  "confidence": 0.89}
]
```

可用方法：

- `"pattern"`：基于规则的模式匹配
- `"dependency"`：spaCy 依存句法分析
- `"cooccurrence"`：基于邻近度的共现
- `"huggingface"`：自定义模型
- `"llm"`：准确率最高，需要 API key


## TripletExtractor

直接从文本生成 RDF 可用的 `(subject, predicate, object)` 三元组：

```python
from semantica.semantic_extract import TripletExtractor

trip = TripletExtractor(method="llm", llm_provider=llm)
triplets = trip.extract(text)
# → [{"subject": "Steve Jobs", "predicate": "founded", "object": "Apple Inc.", ...}]
```

三元组可以直接灌入三元组存储或知识图谱。


## EventDetector

检测带参与者和时间上下文的事件：

```python
from typing import List
from semantica.semantic_extract import EventDetector, Event

extractor = EventDetector(method="llm", llm_provider=llm)
events: List[Event] = extractor.extract(text)

for event in events:
    print(f"Event type:   {event.type}")
    print(f"Participants: {event.participants}")
    print(f"Temporal:     {event.temporal}")
    print(f"Confidence:   {event.confidence:.2f}")
```

每个事件的输出字段：

- `type`：事件类别（如 `"founding"`、`"acquisition"`）
- `participants`：带角色的实体列表
- `temporal`：日期或时间参照
- `location`：位置实体（如有）
- `confidence`：抽取置信度得分


## CoreferenceResolver

抽取前把代词和别名引用消解为规范实体：

```python
from semantica.semantic_extract import CoreferenceResolver

resolver = CoreferenceResolver()
resolved_text = resolver.resolve(
    "Apple Inc. was founded in 1976. The company is headquartered in Cupertino."
)
# "Apple Inc." replaces "The company" for consistent downstream extraction
```


## 批处理

所有抽取器都会自动识别批输入，并高效处理多个文本：

```python
# Batch processing with list input
texts = ["Apple Inc. was founded by Steve Jobs.", "Google was founded by Larry Page.", "Microsoft was founded by Bill Gates."]

ner = NERExtractor(method="llm", llm_provider=llm)
batch_results = ner.extract(texts)  # Returns List[List[Entity]]

# Process results
for i, doc_entities in enumerate(batch_results):
    print(f"Document {i}: {len(doc_entities)} entities")
    for entity in doc_entities:
        print(f"  - {entity.text} ({entity.label})")
```

**批输入选项：**

```python
# Option 1: List of strings
texts = ["Text 1...", "Text 2...", "Text 3..."]
results = ner.extract(texts)

# Option 2: List of documents with IDs (adds provenance metadata)
documents = [
    {"id": "doc_1", "content": "Apple Inc. was founded by Steve Jobs."},
    {"id": "doc_2", "content": "Google was founded by Larry Page."}
]
results = ner.extract(documents)  # Entities include document_id in metadata
```

## 组合使用全部抽取器

标准抽取流水线：实体 → 关系 → 三元组：

```python
from semantica.semantic_extract import NERExtractor, RelationExtractor, TripletExtractor
from semantica.llms import Groq
import os

llm = Groq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

ner  = NERExtractor(method="llm",      llm_provider=llm, max_retries=3)
rel  = RelationExtractor(method="llm", llm_provider=llm, max_retries=3)
trip = TripletExtractor(method="llm",  llm_provider=llm, max_retries=3)

entities      = ner.extract(text)
relationships = rel.extract(text, entities=entities)
triplets      = trip.extract(text)
```

## 抽取方法对比

| 方法 | 速度 | 成本 | 准确率 | 自定义类型 |
| :------ | :----- | :---- | :-------- | :------------ |
| `pattern` | 非常快 | 免费 | 中 | 支持（词典） |
| `ml` | 快 | 免费 | 高 | 有限 |
| `llm` | 中 | API 计费 | 最高 | 支持（schema） |

- [LLM 提供商](./llms.md) — 配置抽取用哪个 LLM。
- [Knowledge Graph](../../reference/kg.md) — 用抽取出的实体和关系构建图。
- [Parse](./parse.md) — 抽取前先解析文档。
- [Deduplication](./deduplication.md) — 抽取后消解重复实体。
