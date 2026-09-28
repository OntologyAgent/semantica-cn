---
title: "欢迎来到 Semantica"
description: "面向高风险领域的 AI 上下文与语义层：上下文图 · 决策智能 · 全程溯源"
source: index.md
source_version: 615cc722c3afe7b6d17d44b89795378e0f30a07a
---

<Note>
  **关于中文版**：本站是社区 fork [OntologyAgent/semantica-cn](https://github.com/OntologyAgent/semantica-cn) 维护的 Semantica 中文文档。该 fork 同时在 PyPI 发布同源包 **`semantica-cn`**（`pip install semantica-cn`，与官方 `semantica` 包二选一安装）。官方仓库 [semantica-agi/semantica](https://github.com/semantica-agi/semantica) 保持不变，本站内容与其保持同步翻译。
</Note>

```bash
pip install semantica
```

大多数 AI 智能体(Agent)跑在嵌入(Embedding)上，而不是语义上。相似度分数没有结构、没有关系，也解释不了为什么返回了这个结果。

Semantica 是垫在你的大语言模型(LLM)、向量库(Vector Store)和智能体框架底下的语义与上下文层：它是确定性基础设施，不是模型。打个比方：模型负责生成答案，Semantica 负责让答案背后的事实、关系和出处有账可查。图构建、推理和溯源全程无需 LLM 参与。它把碎片化的企业数据变成结构化、可查询的上下文图(Context Graph)与知识图谱(Knowledge Graph)。这些图由本体(Ontology)、分类体系和受控词表（OWL、SHACL、SKOS）治理，数据的含义是显式声明的，而不是靠嵌入近似出来的。

溯源(Provenance)和审计轨迹不是外挂的。数据一旦有了这层结构，它们就自然长出来：支撑检索和推理的同一张图，在监管者问「为什么」时也能给出直接答案。

## 你能得到什么

- **[上下文图](guides/context-graphs.md)**：一张持久、可查询的图，记录智能体知道的一切、做过的每个决策和每步推理
- **决策智能(Decision Intelligence)**：`record_decision()` 捕捉每个决策的完整生命周期和因果链
- **[全程溯源](guides/provenance.md)**：每条事实都链回来源，兼容 W3C PROV-O，满足 HIPAA、SOX、GDPR 审计
- **[可解释推理](guides/reasoning.md)**：前向链(Forward Chaining)、Datalog、SPARQL，每种都带可检视的推导路径
- **时态智能**：Allen 区间代数(Allen Interval Algebra)和时间点快照——图不仅知道「什么」，还知道「什么时候」

<Tip>
  Semantica 能与任何 LLM 提供商、任何智能体框架协同工作，也能直接从 Databricks、SAP、Salesforce、Snowflake 等企业数据平台摄取数据。加进现有技术栈，无需改动架构。
</Tip>

## 试一试

<CodeGroup>

```python OpenAI
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore
from semantica.llms import OpenAI

context = AgentContext(
    vector_store=VectorStore(backend="faiss", dimension=1536),
    knowledge_graph=ContextGraph(advanced_analytics=True),
    decision_tracking=True,
    llm=OpenAI(model="gpt-4o"),
)

context.store("GPT-4 outperforms GPT-3.5 on reasoning benchmarks by 40%")

decision_id = context.record_decision(
    category="model_selection",
    scenario="Choose LLM for production reasoning pipeline",
    reasoning="GPT-4 benchmark advantage justifies 3x cost increase",
    outcome="selected_gpt4",
    confidence=0.91,
)

precedents = context.find_precedents("model selection reasoning", limit=5)
influence  = context.analyze_decision_influence(decision_id)
```

```python Anthropic
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore
from semantica.llms import LiteLLM
import os

context = AgentContext(
    vector_store=VectorStore(backend="faiss", dimension=1024),
    knowledge_graph=ContextGraph(advanced_analytics=True),
    decision_tracking=True,
    llm=LiteLLM(model="anthropic/claude-opus-4-7", api_key=os.getenv("ANTHROPIC_API_KEY")),
)

context.store("Claude excels at long-context reasoning and code generation")

decision_id = context.record_decision(
    category="model_selection",
    scenario="Choose LLM for document analysis pipeline",
    reasoning="Claude's 200k context window eliminates chunking overhead",
    outcome="selected_claude",
    confidence=0.94,
)

precedents = context.find_precedents("document analysis model", limit=5)
```

```python Ollama (Local)
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore
from semantica.llms import LiteLLM

context = AgentContext(
    vector_store=VectorStore(backend="faiss", dimension=768),
    knowledge_graph=ContextGraph(advanced_analytics=True),
    decision_tracking=True,
    llm=LiteLLM(model="ollama/llama3.2", base_url="http://localhost:11434"),
)

# Fully local: no data leaves your infrastructure
context.store("Local LLMs enable air-gapped compliance deployments")

decision_id = context.record_decision(
    category="deployment_model",
    scenario="Choose inference strategy for on-prem environment",
    reasoning="Air-gap requirement eliminates cloud API options",
    outcome="local_inference",
    confidence=0.99,
)
```

</CodeGroup>

## 从这里开始

<Steps>
  <Step title="安装">
    ```bash
    pip install semantica
    ```
    可选 extras：`[all]`、`[neo4j]`、`[pinecone]`。见[安装指南](./installation.md)。
  </Step>
  <Step title="跑通流水线">
    跟着[快速开始](./quickstart.md)，5 分钟内摄取文档、抽取实体、构建图谱并记录一条决策。
  </Step>
  <Step title="理解模型">
    [核心概念](./concepts.md)讲清知识图谱与向量库的分野、GraphRAG，以及溯源与决策如何咬合。
  </Step>
  <Step title="深入">
    每个模块都有[参考页](reference/context.md)，附完整 API 文档和可运行示例。
  </Step>
</Steps>

更多：[Cookbook](cookbook.md) 里有实战 notebook；[Discord](https://discord.gg/sV34vps5hH) 可以提问。

<Accordion title="完整模块列表">
  `semantica.ingest`, `semantica.parse`, `semantica.split`, `semantica.normalize`, `semantica.semantic_extract`, `semantica.kg`, `semantica.ontology`, `semantica.reasoning`, `semantica.embeddings`, `semantica.vector_store`, `semantica.graph_store`, `semantica.triplet_store`, `semantica.context`, `semantica.provenance`, `semantica.change_management`, `semantica.deduplication`, `semantica.conflicts`, `semantica.export`, `semantica.visualization`, `semantica.pipeline`, `semantica.seed`, `semantica.llms`, `semantica.mcp_server`, `semantica.explorer`, `semantica.evals`, `semantica.utils`, `semantica.core`。各模块完整文档见 [API 参考](reference/context.md)。
</Accordion>
