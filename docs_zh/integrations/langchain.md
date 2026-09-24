---
title: LangChain 集成
description: 通过 GraphRAG 检索器、VectorStore 适配器与智能体工具，把 Semantica 接入 LangChain / LangGraph 流水线。
source: integrations/langchain.md
source_version: 10b1796cad3c266ca2a13f8ed82e8be5281cac90
icon: "link"
---

> 三个即插即用(drop-in)适配器(Adapter)，把 Semantica 的上下文图(Context Graph)与混合检索(Hybrid Search)能力带进 LangChain 链和 LangGraph 智能体(Agent)。

## 安装

```bash
pip install "semantica[langchain]"
```

要求 `langchain-core >= 0.3`。未安装 langchain-core 时，集成模块照样可以导入：每个类都携带完整的 Semantica API，并优雅降级（`build()` 返回 `None`；可依据 `LANGCHAIN_AVAILABLE` 编写分支逻辑）。

## 组件一览

- **SemanticaRetriever**（`BaseRetriever`）：先用混合检索取回种子结果，再沿图边游走 `hops` 步（默认 2 步），得到 GraphRAG 风格的结果。
- **SemanticaVectorStore**（`VectorStore`）：在 `HybridSearch` 之上提供 `add_texts` / `similarity_search` / `similarity_search_with_score` / `from_texts`。
- **SemanticaKGTool** / **SemanticaDecisionTool**（`BaseTool` 子类）：提供 `semantica_query_graph` 与 `semantica_query_decisions` 两个工具，供 LangGraph / 工具调用型智能体使用。

## 组件详解

<Tabs>
  <Tab title="SemanticaRetriever">
    先用混合检索确定种子结果，再沿图边游走 `hops` 步，让结果突破扁平向量相似度的局限。如果未提供混合检索，或者混合检索执行失败，检索器会回落到 `ContextGraph.query` 的关键词扫描。

    ```python
    from integrations.langchain import SemanticaRetriever
    from semantica.context import ContextGraph
    from semantica.vector_store import HybridSearch

    graph = ContextGraph()
    hybrid = HybridSearch()

    retriever = SemanticaRetriever(graph=graph, hybrid=hybrid, hops=2, top_k=10)

    from langchain.chains import RetrievalQA

    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    ```
  </Tab>
  <Tab title="SemanticaVectorStore">
    可直接接入 RetrievalQA / LCEL 链的 `VectorStore`。`from_texts` 需要一个预先配置好的 `hybrid` 实例。

    ```python
    from integrations.langchain import SemanticaVectorStore

    store = SemanticaVectorStore(hybrid=hybrid)
    store.add_texts(
        ["document one", "document two"],
        metadatas=[{"source": "a"}, {"source": "b"}],
    )
    docs = store.similarity_search("document", k=2)
    docs, scores = store.similarity_search_with_score("document", k=2)
    ```

    `add_texts` 会转交给带 `add_documents` 的 Semantica 向量库(Vector Store)执行（把 `vector_store=` 传给 `HybridSearch` 或 `SemanticaVectorStore` 即可）。
  </Tab>
  <Tab title="智能体工具">
    实例都是 LangChain 的 `BaseTool`，可以直接交给智能体使用。
    `.build()` 返回工具实例；缺少 langchain-core 时返回 `None`。

    ```python
    from integrations.langchain import SemanticaKGTool, SemanticaDecisionTool
    from langgraph.prebuilt import create_react_agent

    tools = [
        SemanticaKGTool(graph),
        SemanticaDecisionTool(graph),
    ]
    agent = create_react_agent(model, tools)
    ```

    | 工具 | 说明 |
    | :------ | :------------- |
    | `semantica_query_graph` | 对共享上下文图执行关键词 / 自然语言查询 |
    | `semantica_query_decisions` | 检索已记录的决策日志 |
  </Tab>
</Tabs>
