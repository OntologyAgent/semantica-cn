---
title: CrewAI 集成
description: 通过三个即插即用组件，为 CrewAI 团队(Crew)提供共享的语义知识图谱、决策智能与基于图的检索。
source: integrations/crewai.md
source_version: 3c67f1eca734e71da2ebbfd7f2ac91971b8e4720
icon: "users"
---

> 三个即插即用组件，把 Semantica 的知识图谱(Knowledge Graph)与决策智能(Decision Intelligence)带进任意 CrewAI 团队(Crew)。

## 安装

```bash
pip install "crewai>=0.80.0"
```

`crewai` 需要单独安装——semantica 不提供 `[crewai]` extra，因为 crewai 硬性锁定 `chromadb~=1.1.0` 依赖，而该版本带有关键级、至今尚未修复的安全公告（CVE-2026-45829/45830/45831/45833）。确有需要时，请自行安装 `crewai` 并接受这一风险。未安装 `crewai` 时，本集成依然可以导入——每个类都携带完整的 Semantica API 并会优雅降级，只是无法传给 `Crew` 使用。

## 组件一览

- **SemanticaKGTool** — `Agent(tools=[…])`: 5 个知识图谱构建/查询动作：抽取实体、抽取关系、加入图谱、查询图谱、查找关联。
- **SemanticaDecisionTool** — `Agent(tools=[…])`: 5 个决策智能动作：记录决策、查找先例、追踪因果链、分析影响、检查策略。
- **SemanticaKnowledgeSource** — `Crew(knowledge_sources=[…])`: 把 `ContextGraph` 序列化进 CrewAI 的知识存储，让每个智能体都能检索这张图。

## 组件详解

<Tabs>
  <Tab title="SemanticaKGTool">
    让智能体在推理过程中主动**构建和查询**共享的 `ContextGraph`。

    ```python
    from crewai import Agent, Crew, Task
    from semantica.context import ContextGraph
    from integrations.crewai import SemanticaKGTool

    graph = ContextGraph()

    analyst = Agent(
        role="Knowledge Analyst",
        goal="Build and explore a knowledge graph from documents",
        backstory="You map entities and relationships into a shared graph.",
        tools=[SemanticaKGTool(graph=graph)],
    )

    crew = Crew(
        agents=[analyst],
        tasks=[Task(
            description="Extract and link key entities from the brief",
            expected_output="JSON",
            agent=analyst,
        )],
    )
    crew.kickoff()
    ```

    | 工具 | 说明 |
    | :------ | :------------- |
    | `extract_entities` | 从 `text` 中抽取命名实体 |
    | `extract_relations` | 抽取 `text` 中实体之间的关系 |
    | `add_to_graph` | 从 `text` 抽取实体/关系并加入共享图谱 |
    | `query_graph` | 用 `query` 按节点 id、类型与内容做关键词检索 |
    | `find_related` | 在 `hops` 跳范围内查找与 `entity` 相关的概念 |

    所有动作都返回 JSON，智能体拿到的结果是可解析的。

    **共享图谱：** 工具读写的正是你传入的那个 `graph`。不给 `graph` 时，会新建一个内存态的 `ContextGraph()`（并记录一条警告）——两个各自自动建图的工具实例之间**不会**共享知识。需要共享状态的每个智能体，都请传入同一个 `ContextGraph`。
  </Tab>
  <Tab title="SemanticaDecisionTool">
    把 Semantica 的决策智能封装为原生 CrewAI 工具，底层由 `AgentContext` 提供支撑。

    ```python
    from crewai import Agent, Crew, Task
    from integrations.crewai import SemanticaDecisionTool

    planner = Agent(
        role="Decision Planner",
        goal="Make grounded, precedented decisions",
        backstory="You record decisions and validate them against policy.",
        tools=[SemanticaDecisionTool()],
    )

    crew = Crew(agents=[planner], tasks=[...])
    ```

    不传 `AgentContext` 时，会自动创建一个内存态实例，开启 `decision_tracking=True` 并自带一个 `ContextGraph`，因此决策动作开箱即用（会记录一条警告——要让多个智能体共享决策状态，就把同一个 `AgentContext` 传给它们）。`record_decision` 中缺失的可选字段会回落为 `category="general"`、`reasoning="agent decision"`、`outcome="recorded"`。`find_precedents` 最多返回 `max_precedents` 条结果。如果知识图谱无法追踪因果，`trace_causal_chain` 会返回显式错误，而不是拿基于相似度的结果来顶替。

    | 工具 | 说明 |
    | :------ | :------------- |
    | `record_decision` | 记录一条决策，附推理过程、结果与置信度 |
    | `find_precedents` | 检索相似的历史决策 |
    | `trace_causal_chain` | 追踪一条决策的因果链 |
    | `analyze_impact` | 评估一条决策的下游影响 |
    | `check_policy` | 用策略规则校验拟议的决策 |
  </Tab>
  <Tab title="SemanticaKnowledgeSource">
    让 **crew 中的每个智能体**都能检索 `ContextGraph`。

    ```python
    from crewai import Agent, Crew, Task
    from semantica.context import ContextGraph
    from integrations.crewai import SemanticaKnowledgeSource

    graph = ContextGraph()
    graph.add_node(node_id="privacy", node_type="policy", content="...")

    researcher = Agent(
        role="Policy Researcher",
        goal="Answer questions from the knowledge base",
        backstory="You retrieve from graph knowledge to answer accurately.",
    )

    crew = Crew(
        agents=[researcher],
        tasks=[...],
        knowledge_sources=[SemanticaKnowledgeSource(graph=graph)],
    )
    ```

    kickoff 时，图的节点与边会经过序列化、分块(Chunking)，再存入 CrewAI 的知识流水线。

    > **必须配置嵌入器(Embedder)：** 分块的存储要经过 CrewAI 的知识流水线，而这条流水线需要配置好嵌入器。请设置 `Crew(embedder=...)`（或提供 CrewAI 回落使用的默认凭据，例如 `OPENAI_API_KEY`）。若没有可用的嵌入器，存储会失败并记录 ERROR 日志，智能体将**检索不到任何内容**——crew 照样运行，但知识查询返回空。

    **兼容性：** CrewAI 的 `BaseKnowledgeSource` 接口在 `0.80.x` 与当前版本之间发生过变化（`load_content()` → `validate_content()`/`aadd()`）。`SemanticaKnowledgeSource` 同时实现了新旧两套方法，因此在 `crewai>=0.80.0` 上都能工作。
  </Tab>
</Tabs>

## 检查点与序列化

CrewAI 会把工具和知识源(Knowledge Source)序列化成 JSON，用于检查点保存与恢复。Semantica 的活动状态（`ContextGraph`、`AgentContext`、抽取器）**不在这次序列化范围内**——恢复出来的工具/知识源会带着一个全新的内存态 `ContextGraph` 回来，并记录一条警告。在你重新接上活动的图/上下文之前，恢复出的对象都是在对着一张**空**图回答查询，因此恢复运行后要先重新接线（例如 `restored_tool.graph = live_graph`），再让智能体继续工作。

## API 参考

```python
from integrations.crewai import (
    SemanticaKGTool,          # BaseTool: KG construction/query actions
    SemanticaDecisionTool,    # BaseTool: decision intelligence actions
    SemanticaKnowledgeSource, # BaseKnowledgeSource: graph → crew knowledge
    CREWAI_AVAILABLE,         # bool: True if crewai is installed
)
```

三个类在未安装 `crewai` 时同样可用：它们自带完整的 Semantica API，并会优雅降级。

## 延伸阅读

- [上下文模块](../reference/context.md) — 支撑本集成的 `AgentContext` 与 `ContextGraph`。
- [语义抽取](../reference/semantic_extract.md) — `SemanticaKGTool` 所用的 `NERExtractor` / `RelationExtractor`。
- [LLM](../reference/llms.md) — 为 crew 中的智能体配置大语言模型(LLM)提供商。
- [向量库](../reference/vector_store.md) — `SemanticaDecisionTool` 所用的向量后端。
