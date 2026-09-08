---
title: 架构
description: 四层模块化架构，各组件可独立使用、职责清晰分离，且完全可扩展。
source: architecture.md
source_version: e0f70fc52f2986197e337aa38033d948a7e19984
icon: "building"
---

Semantica 围绕四层模块化架构构建。只导入你需要的部分：框架从不强制引入整套技术栈。每个组件都可独立替换，层与层之间通过清晰的接口通信，没有隐藏耦合。


## 四层架构

<img src="/assets/img/diagrams/architecture-overview.svg" alt="Semantica 四层架构" style={{ width: '100%', borderRadius: '12px', margin: '16px 0 24px' }} />

<Tabs>

<Tab title="第 1 层：摄取">

把任意来源的数据加载进流水线，统一为 `SourceDocument` 格式。

| 来源 | 模块 | 说明 |
| :------ | :------ | :----- |
| PDF、DOCX、PPTX、HTML、JSON、CSV | `ingest.FileIngestor` | 支持压缩包、递归目录扫描 |
| Parquet | `ingest.ParquetIngestor` | PyArrow，Hive 风格分区（v0.5.0） |
| XML | `ingest.XMLIngestor` | XXE 安全的 lxml，XSD/DTD 校验（v0.5.0） |
| 网页 | `ingest.WebIngestor` | 可配置深度、链接过滤 |
| SQL / Snowflake / Databricks | `ingest.DBIngestor` / `ingest.SnowflakeIngestor` / `ingest.DatabricksIngestor` | 自定义 SQL、schema 内省、Unity Catalog 血缘 |
| Kafka / 流 | `ingest.StreamIngestor` | 实时数据流摄取 |
| 邮件 | `ingest.EmailIngestor` | IMAP/SMTP，含附件抽取 |
| 代码仓库 | `ingest.RepoIngestor` | Git 仓库、代码结构 |
| MCP | `ingest.MCPIngestor` | Model Context Protocol 数据源 |

</Tab>

<Tab title="第 2 层：处理">

把原始文本转换成结构化、增广后的文档，为知识库摄取做好准备。

| 步骤 | 模块 | 作用 |
| :---- | :------ | :------------ |
| 解析 | `parse.DocumentParser` / `parse.DoclingParser` | 文本与版面抽取、表格检测 |
| 规范化 | `normalize` | 规范形式、日期/名称标准化、编码修复 |
| 抽取 | `semantic_extract` | NER、关系抽取、事件检测、三元组 |
| 构建 | `kg.GraphBuilder` | 实体合并、边构建、图组装 |
| 质检 | `deduplication`, `conflicts` | 重复检测、冲突消解、校验 |

</Tab>

<Tab title="第 3 层：智能">

支撑检索与推理的持久化知识存储和嵌入基础设施。

| 组件 | 模块 | 说明 |
| :--------- | :------ | :----------- |
| 知识图谱 | `kg` | 图构建、时态模型、分析、距离智能 |
| 向量库 | `vector_store` | pgvector、Qdrant、Weaviate、Pinecone：语义相似度搜索 |
| 本体 | `ontology` | OWL/RDFS 建模、SHACL 校验、本体对齐 |
| 三元组库 | `triplet_store` | RDF 三元组存储与 SPARQL 查询 |
| 嵌入 | `embeddings` | Sentence-Transformers、FastEmbed、OpenAI、BGE |
| 时态 | `kg.TemporalKnowledgeGraph` | `valid_from` / `valid_until`、Allen 区间代数（v0.4.0） |

</Tab>

<Tab title="第 4 层：应用">

消费知识图谱和向量库，服务下游用例。

| 用例 | 模块 | 说明 |
| :-------- | :------ | :----------- |
| GraphRAG | `context.AgentContext` | 面向 LLM 的图谱增强检索 |
| 智能体记忆 | `context.ContextGraph` | 跨智能体运行的持久语义记忆 |
| 决策追踪 | `context.AgentContext` | 记录、追踪并审计每个智能体决策 |
| 本体中心 | `explorer` | 可视化编辑器、SHACL Studio、对齐界面（v0.5.0） |
| 多智能体 | `integrations.agno` | 共享上下文、团队级记忆、KG 工具包 |
| 可视化 | `visualization` | 交互式 HTML 图、嵌入图、时态视图 |
| 导出 | `export` | RDF、Parquet、ArangoDB AQL、OWL、CSV、Arrow |
| 推理 | `reasoning` | 前向链、Rete、Datalog、SPARQL、溯因 |

</Tab>

</Tabs>


## 数据流

每条流水线都走同一条线性路径：从原始数据到最终交付。

<img src="/assets/img/diagrams/pipeline-flow.svg" alt="Semantica 8 步流水线：摄取 → 解析 → 规范化 → 抽取 → 构建 KG → 质检 → 存储 → 交付" style={{ width: '100%', borderRadius: '10px', margin: '16px 0 24px' }} />


## 模块地图

| 层 | 类别 | 模块 |
| :----- | :-------- | :------- |
| **第 1 层：摄取** | 来源 | `ingest`, `split` |
| **第 2 层：处理** | 转换 | `parse`, `normalize`, `semantic_extract`, `deduplication`, `conflicts` |
| **第 3 层：智能** | 存储 | `kg`, `vector_store`, `graph_store`, `triplet_store`, `embeddings`, `ontology` |
| **第 4 层：应用** | 交付 | `context`, `reasoning`, `export`, `visualization`, `explorer`, `pipeline` |
|: | 横切 | `provenance`, `change_management`, `llms`, `mcp_server`, `seed`, `evals`, `core`, `utils` |


## 扩展点

每一层都提供基于注册表(Registry)的扩展点。注册自定义实现后，它们就能参与完整流水线，核心代码零改动。

<CodeGroup>

```python 自定义摄取器
from semantica.ingest.registry import method_registry

def custom_file_ingestor(source):
    # 返回文档字典列表，包含 'text'、'metadata'、'source' 字段
    return [{"text": "...", "metadata": {}, "source": source}]

# 以唯一名称注册到 "file" 任务类别下
method_registry.register("file", "my_custom_format", custom_file_ingestor)

available = method_registry.list_all("file")
```

```python 自定义抽取器
from semantica.semantic_extract.registry import method_registry

def custom_entity_extractor(text, config=None):
    # 返回实体字典列表，包含 'text'、'type'、'confidence' 字段
    return [{"text": "...", "type": "CUSTOM_TYPE", "confidence": 0.9}]

# 注册到 "entity" 抽取任务下
method_registry.register("entity", "my_extractor", custom_entity_extractor)
```

```python 自定义插件
from semantica.core import PluginRegistry

class MyPlugin:
    def process(self, graph, config):
        # 原地修改图并返回
        return graph

registry = PluginRegistry()
registry.register_plugin("my_plugin", MyPlugin, version="1.0.0")
```

</CodeGroup>


## 设计决策

<AccordionGroup>

<Accordion title="模块化：只用你需要的" icon="puzzle-piece">

每个组件都能独立运行。`NERExtractor` 不需要图库，`VectorStore` 不需要决策追踪。框架从不强制实例化整套技术栈：导入什么，才付出什么的成本。

</Accordion>

<Accordion title="可插拔：不改核心即可扩展" icon="plug">

自定义摄取器、抽取器、校验器和导出器都遵循同一套基类模式。通过 `PluginRegistry` 注册后，它们就能参与完整流水线——溯源追踪、重试策略、并行执行一应俱全——核心代码零改动。

</Accordion>

<Accordion title="默认开启溯源" icon="link">

血缘追踪内建在图构建的最底层。每个节点和边都带 `source_id`，指向来源文档、抽取方法和时间戳。无需主动开启：溯源始终在线。

</Accordion>

<Accordion title="显式配置优于隐式约定" icon="sliders">

集中式 `ConfigManager`，支持环境变量覆盖。没有魔法默认值：所有行为都显式、可覆盖。适合开发、预发布、生产环境需要不同后端的多环境部署。

</Accordion>

</AccordionGroup>


## 性能特性

| 特性 | 机制 |
| :-------------- | :--------- |
| **并行执行** | `Pipeline(workers=N)`，每个阶段可配置 worker 数 |
| **增量处理** | 图增量更新：新数据无需全量重算 |
| **流式摄取** | 处理大规模语料而无需全部载入内存 |
| **后端灵活** | 内存版 NetworkX 与 Neo4j / FalkorDB 可互换，API 不变 |
| **去重 v2** | `blocking_v2`, `hybrid_v2`, `semantic_v2`：比 v1 快至 7 倍 |
| **索引搜索** | Explorer 搜索在 11.8 万节点上仅 0.004ms（v0.5.0） |

- [模块](./modules.md) — 逐模块配代码示例的完整文档。
- [进阶学习](../learning-more.md) — 配置参考、性能指南与故障排查。
- [Pipeline 参考](../reference/pipeline.md) — 流水线编排、worker 与重试策略。
- [Core 参考](../reference/core.md) — 框架生命周期、插件注册表与配置。
