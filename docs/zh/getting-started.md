---
title: 入门指南
description: AI 的上下文与智能层：把原始数据变成可解释、可审计的知识图谱。
source: getting-started.md
source_version: fd00501e08262d0677b543051a82198e594c833a
icon: "rocket"
---

<Tip>
  已经装好了？直接跳到[快速开始](./quickstart.md)。需要先配置环境？见[安装指南](./installation.md)。
</Tip>

## 你能构建什么

- **GraphRAG 系统** — 让大语言模型(LLM)的回答落在可追溯的结构化知识上。每条断言都链回一个源节点。
- **可问责的 AI 智能体** — 具备结构化决策历史、因果链和先例检索的智能体(Agent)。每个选择都有记录、可审计。
- **生产级知识图谱** — 从多源数据构建、校验并维护企业级语义知识库。
- **合规就绪的 AI** — 每个事实都带 W3C PROV-O 溯源(Provenance)。内置 HIPAA、SOX、GDPR、FDA 21 CFR Part 11 基础设施。


## 三步完成配置

<Steps>
  <Step title="安装 Semantica">
    <CodeGroup>

    ```bash pip (recommended)
    pip install semantica
    ```

    ```bash With all extras
    pip install semantica[all]
    ```

    ```bash From source
    git clone https://github.com/semantica-agi/semantica.git
    cd semantica
    pip install -e ".[dev]"
    ```

    </CodeGroup>

    <Check>
      验证安装：
      ```python
      import semantica
      print(semantica.__version__)  # 0.6.8
      ```
    </Check>
  </Step>

  <Step title="选一条路线">
    挑一条和你目标匹配的路线：每条都从一个 5 分钟的聚焦示例开始。

    | 路线 | 你想…… | 从这里开始 |
    | :----- | :-------------- | :--------- |
    | **知识图谱** | 把文档变成结构化、可查询的图 | [快速开始 · 第一步](./quickstart.md) |
    | **智能体上下文** | 给 AI 智能体持久记忆和决策追踪 | [Context 参考](../reference/context.md) |
    | **GraphRAG** | 让 LLM 的回答扎根于结构化知识 | [核心概念 · GraphRAG](../concepts.md#graphrag) |
    | **MCP 集成** | 从 Claude Desktop 或 VS Code 使用 Semantica | [MCP 服务器](../reference/mcp_server.md) |

  </Step>

  <Step title="跑通流水线">
    完整的 6 步流水线——摄取、解析、抽取、构建、可视化、导出——都在[快速开始](./quickstart.md)里。用基于模式的抽取 5 分钟内即可跑完（无需 API key）。

    <Note>
      API key 对快速开始是**可选**的。基于模式的抽取开箱即用；准备好后随时升级到 LLM 抽取，获得更高准确率。
    </Note>
  </Step>
</Steps>


## 选你的路线

<Tabs>
  <Tab title="知识图谱">
    从任意文档或数据源构建结构化知识图谱。

    ```python
    from semantica.ingest import FileIngestor
    from semantica.parse import DocumentParser
    from semantica.semantic_extract import NERExtractor, RelationExtractor
    from semantica.kg import GraphBuilder

    # 1. Ingest
    sources = FileIngestor().ingest("data/report.pdf")

    # 2. Parse (extract_text returns a plain string for any supported format)
    text = DocumentParser().extract_text(sources[0].path)

    # 3. Extract (extractors take text, return Entity / Relation objects)
    ner           = NERExtractor(method="pattern")  # no API key needed
    entities      = ner.extract(text)
    relationships = RelationExtractor(method="pattern").extract(text, entities=entities)

    # 4. Build
    graph = GraphBuilder(merge_entities=True).build(
        {"entities": entities, "relationships": relationships}
    )
    print(f"{len(graph['entities'])} nodes, {len(graph['relationships'])} edges")
    ```

    **下一步：**[完整流水线走查 →](./quickstart.md)
  </Tab>

  <Tab title="智能体上下文">
    给智能体持久记忆、决策追踪和先例检索。

    ```python
    from semantica.context import AgentContext, ContextGraph
    from semantica.vector_store import VectorStore

    context = AgentContext(
        vector_store=VectorStore(backend="faiss", dimension=768),
        knowledge_graph=ContextGraph(advanced_analytics=True),
        decision_tracking=True,
    )

    # Store a fact with provenance
    context.store("GPT-4 outperforms GPT-3.5 on reasoning by 40%")

    # Record a decision with full causal chain
    decision_id = context.record_decision(
        category="model_selection",
        scenario="Choose LLM for production pipeline",
        reasoning="GPT-4 benchmark advantage justifies cost",
        outcome="selected_gpt4",
        confidence=0.91,
    )

    # Search past decisions before making a new one
    precedents = context.find_precedents("model selection", limit=5)
    ```

    **下一步：**[Context 模块参考 →](../reference/context.md)
  </Tab>

  <Tab title="GraphRAG">
    让 LLM 的每条回答都扎根于你的知识图谱——没有无根据的断言。

    ```python
    from semantica.context import AgentContext, ContextGraph
    from semantica.vector_store import VectorStore

    context = AgentContext(
        vector_store=VectorStore(backend="faiss", dimension=768),
        knowledge_graph=ContextGraph(advanced_analytics=True),
        graph_expansion=True,       # blend graph traversal into retrieval
        max_expansion_hops=3,       # how far to walk from the seed nodes
    )

    # store() runs extraction and populates both the vector index and the graph
    context.store([
        {"content": "Steve Wozniak co-founded Apple with Steve Jobs in 1976."},
        {"content": "Tony Fadell led the iPod team at Apple, then founded Nest."},
    ])

    # GraphRAG retrieval: seed from vector matches, expand along graph edges
    results = context.retrieve(
        "What companies were founded by people who worked at Apple?",
        use_graph=True,
        expand_graph=True,
    )
    for r in results:
        print(f"[{r['score']:.3f}]  {r['content'][:70]}  (source: {r['source']})")
    ```

    每条结果携带 `content`、`score`、`source` 和 `metadata`。要有扎根的自然语言回答加可审计的遍历路径，用 `context.query_with_reasoning(query, llm_provider=...)`——它返回 `response`、`reasoning_path`、`sources` 和 `confidence`。

    **下一步：**[GraphRAG 概念 →](../concepts.md#graphrag)
  </Tab>

  <Tab title="MCP 集成">
    从 Claude Desktop、VS Code、Cursor 或任意 MCP 客户端使用 Semantica——配置完成后无需写 Python 代码。

    ```bash
    pip install semantica
    ```

    添加到你的 MCP 客户端配置：

    ```json
    {
      "mcpServers": {
        "semantica": {
          "command": "semantica-mcp"
        }
      }
    }
    ```

    立即可用 15 个工具：抽取实体、查询图谱、记录决策、运行推理、导出结果。

    **下一步：**[MCP 服务器参考 →](../reference/mcp_server.md)
  </Tab>
</Tabs>


## 核心架构

Semantica 采用模块化分层架构：只导入你需要的部分。

- **[输入层](../reference/ingest.md)** — 从任意来源加载并准备数据。模块：`ingest`、`parse`、`split`、`normalize`
- **[语义层](../reference/semantic_extract.md)** — 从原始文本提取语义。模块：`semantic_extract`、`kg`、`ontology`、`reasoning`
- **[存储层](../reference/vector_store.md)** — 持久化知识供检索。模块：`embeddings`、`vector_store`、`graph_store`、`triplet_store`
- **[质量层](../reference/deduplication.md)** — 校验与去重。模块：`deduplication`、`conflicts`
- **[上下文层](../reference/context.md)** — 追踪决策与血缘。模块：`context`、`provenance`、`change_management`
- **[输出层](../reference/export.md)** — 向下游交付结果。模块：`export`、`visualization`、`pipeline`、`explorer`


## 我需要哪个模块？

见[选对模块](../choose-your-module.md)指南——它把 35+ 个开发目标映射到 27 个模块的正确起点，常见路径都附可运行代码。


## 下一步

- [核心概念](../concepts.md) — 深入讲解知识图谱、本体与推理。
- [快速开始教程](./quickstart.md) — 带完整代码的 6 步流水线走查。
- [模块参考](../modules.md) — 每个模块、类和常见组合的讲解。
- [API 参考](../reference/context.md) — 每个类和方法的完整模块文档。


## 帮助

- [Discord](https://discord.gg/sV34vps5hH) — 提问、分享项目、获取社区支持。
- [GitHub Issues](https://github.com/semantica-agi/semantica/issues) — 报告缺陷或提功能建议。
- [常见问题](../faq.md) — 常见问题解答。
