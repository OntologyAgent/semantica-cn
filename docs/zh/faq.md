---
title: 常见问题
description: Semantica 常见问题：安装、功能、集成与故障排查。
source: faq.md
source_version: c98fdf1cfda14c4e8b648f884e05f14cf765c7d7
icon: "circle-question"
---

<Info>
  用 **Ctrl+F** / **Cmd+F** 搜索本页。常见跳转：[安装](#安装) · [数据与功能](#数据与功能) · [故障排查](#故障排查)
</Info>

## 快速解答

| 问题 | 回答 |
| :-------- | :------ |
| 许可证？ | MIT：永久免费，没有付费墙功能 |
| Python 版本？ | 3.8+（推荐 3.11+） |
| 需要 API key 吗？ | 可选：模式抽取无需任何 key |
| 兼容 LangChain / LlamaIndex 吗？ | 兼容：Semantica 是叠加层，不是替代品 |
| 生产可用吗？ | 可以：1000+ 项测试，每个版本都随附安全修复（见 [CHANGELOG](https://github.com/semantica-agi/semantica/blob/main/CHANGELOG.md)） |
| 最新版本？ | **v0.6.8**（2026 年 9 月） |
| 支持本地 LLM 吗？ | 支持：经 LiteLLM 接 Ollama，气隙环境用 HuggingFaceLLM |


## 常规问题

<AccordionGroup>

<Accordion title="Semantica 是什么？" icon="info-circle">

Semantica 是一个开源框架，用于为 AI 构建上下文图(Context Graph)和决策智能(Decision Intelligence)层。它把非结构化数据——文档、API、数据库——变成带完整溯源(Provenance)追踪的结构化知识图谱(Knowledge Graph)，让 AI 系统可解释、可审计。

它不是 LangChain 或 LlamaIndex 的替代品。它是叠加在其上的**问责层**：记录决策、把事实追溯到来源、让推理过程透明可见。

</Accordion>

<Accordion title="用 Semantica 能构建什么？" icon="hammer">

- 从文档和多源数据构建知识图谱
- 带图谱增强检索和来源标注的 GraphRAG 系统
- 有结构化决策历史和语义记忆的 AI 智能体
- 兼容 W3C PROV-O 血缘的合规流水线（HIPAA、SOX、GDPR、FDA 21 CFR Part 11）
- 追踪事实随时间变化的时态图
- 带 SHACL 校验的本体驱动知识库

</Accordion>

<Accordion title="Semantica 和 LangChain、LlamaIndex 有什么不同？" icon="scale-balanced">

多数框架止步于检索或生成。Semantica 加了一层**问责层**：每个决策都被记录，每条事实都链向来源，每个推理步骤都可解释。它面向这样的环境：你不仅要知道 AI 说了什么，还要能审计 AI *为什么*得出这个结论。

Semantica 与这些框架协同工作，而不是对抗。

</Accordion>

<Accordion title="Semantica 能解释 LLM 的内部推理或思维链吗？" icon="triangle-exclamation">

不能。这是**系统级可解释性，不是基础模型可解释性**。Semantica 不暴露、不重建、不解释 LLM/基础模型*内部*发生了什么——其内部推理或思维链对外部系统始终是不透明的。

Semantica 解释的是模型*之外*的部分：用了什么上下文和数据、产生了什么决策、背后的溯源、相关的关系、适用的策略，以及由此形成的决策轨迹。

一句话：Semantica 解释和审计的是 *AI 系统做了什么*，而不是基础模型私有的内部推理。

</Accordion>

<Accordion title="Semantica 免费吗？" icon="tag">

免费：MIT 许可，无厂商锁定，没有付费墙功能。部分能力需要第三方 API key（如 OpenAI 嵌入、Groq 推理），但 Semantica 本身永远免费开源。

</Accordion>

<Accordion title="最新版本是多少？" icon="star">

**v0.6.8**：2026 年 9 月发布。

亮点：每个版本现已带密码学签名（SLSA 构建溯源 + Sigstore，补上 OpenSSF Scorecard 的 Signed-Releases 缺口）；FAISS/SQLiteVec/PgVector/Qdrant/Weaviate/Milvus 全线真实的向量枚举（`scan_vectors()`/`iter_vectors()`），让 `store migrate` 真正可用；Anthropic/Gemini/Ollama/DeepSeek/Novita 一等 LLM 提供商包装器；面向 CI 的本体质量门(quality gate)；以及 35 项正确性修复。0.6.x 系列还加入了一等 LangChain 与 CrewAI 支持、带确定性 IRI 的 Semantica RDF 词表。完整历史见 [CHANGELOG](https://github.com/semantica-agi/semantica/blob/main/CHANGELOG.md)。

```bash
pip install --upgrade semantica
```

</Accordion>

</AccordionGroup>


## 安装

<AccordionGroup>

<Accordion title="怎么安装 Semantica？" icon="download">

```bash
pip install semantica
```

虚拟环境配置、可选 extra（`[gpu]`、`[all]`、各提供商专用）和平台相关故障排查见[安装](./installation.md)。

</Accordion>

<Accordion title="需要什么 Python 版本？" icon="python">

Python **3.8 或更高**。推荐 Python 3.11+，性能和兼容性最好。

</Accordion>

<Accordion title="Windows 上 [all] extra 安装失败" icon="windows">

这是一个已知缺陷：**v0.5.0** 已修复。升级：

```bash
pip install --upgrade semantica
```

如果还在用旧版本，可以逐个装 extra：先 `pip install "semantica[core]"`，再加 `[llm-openai]`、`[gpu]` 等。

</Accordion>

<Accordion title="系统要求是什么？" icon="server">

| 要求 | 最低 | 推荐 |
| :----------- | :------- | :----------- |
| Python | 3.8 | 3.11+ |
| 内存 | 4 GB | 16 GB+ |
| 存储 | 2 GB | 20 GB+ |
| GPU | 可选 | 嵌入和 ML 模型用 CUDA |

</Accordion>

</AccordionGroup>


## 数据与功能

<AccordionGroup>

<Accordion title="Semantica 支持哪些数据来源？" icon="database">

| 类别 | 来源 |
| :-------- | :------- |
| **文件** | PDF、DOCX、HTML、JSON、CSV、Excel、PPTX、Parquet（v0.5.0）、XML（v0.5.0）、压缩包 |
| **网页** | `WebIngestor` 爬取、RSS 订阅源、站点地图 |
| **数据库** | PostgreSQL、MySQL、Snowflake、Databricks，经 `DBIngestor` / `SnowflakeIngestor` / `DatabricksIngestor` |
| **NoSQL** | MongoDB 经 `MongoIngestor`，DuckDB 经 `DuckDBIngestor` |
| **流** | Kafka、`StreamIngestor` 实时摄取 |
| **协议** | MCP（Model Context Protocol）经 `MCPIngestor` |
| **云** | Google Drive 经 `GDriveIngestor`、HuggingFace 数据集 |

</Accordion>

<Accordion title="能用我自己的模型吗？" icon="robot">

可以。Semantica 支持：

- **自定义 NER 和抽取模型**：经 `method_registry` 注册
- **自定义嵌入模型**：任何带 `.encode()` 接口的模型
- **自定义 LLM 提供商**：经 LiteLLM（100+ 模型）或直接对接提供商
- **自定义流水线处理器**：经 `PluginRegistry` 注册

</Accordion>

<Accordion title="Semantica 支持 GPU 吗？" icon="bolt">

支持。检测到 GPU 时会自动用于嵌入生成、ML 模型推理和向量运算。安装 GPU 支持：

```bash
pip install "semantica[gpu]"
```

包含带 CUDA 的 PyTorch、FAISS GPU 和 CuPy。

</Accordion>

<Accordion title="Semantica 怎么处理大规模数据集？" icon="layer-group">

- **分批**：按可配置的块处理文档，控制内存占用
- **并行处理**：`Pipeline(workers=N)` 并发跑抽取步骤
- **增量处理**：图增量更新，新数据无需全量重算
- **持久化后端**：大规模生产图可把内存版 NetworkX 换成 Neo4j、FalkorDB 或 Apache AGE

</Accordion>

<Accordion title="什么是时态智能？" icon="clock">

`TemporalKnowledgeGraph` 给节点和边挂上 `valid_from` / `valid_until` 窗口，支持时间点查询和历史分析。支持全部 13 种 Allen 区间代数关系和 OWL-Time 导出。

```python
from semantica.kg import TemporalKnowledgeGraph

tkg = TemporalKnowledgeGraph()
tkg.add_temporal_triple("A", "caused", "B", valid_from="2024-01", valid_until="2024-06")
snapshot = tkg.query_at_time("2024-03")
```

v0.4.0 起可用。

</Accordion>

<Accordion title="什么是本体中心？" icon="sitemap">

覆盖本体全生命周期的可视化浏览器界面：经 `semantica.explorer` 启动。包含：

- **可视化编辑器**：创建和编辑类、属性、关系
- **SHACL Studio**：编写、校验、导出 SHACL 形状
- **对齐编写**：跨本体映射概念
- **健康看板**：覆盖率、一致性、约束违规指标
- **版本控制**：本体变更的差异对比与历史

v0.5.0 起可用。

</Accordion>

<Accordion title="什么是距离智能？" icon="compass">

对图中任意实体做语义邻域探索，返回带距离带分类的结构化邻近数据。

- 一组实体的 N×N 距离矩阵
- 以单个节点为中心的 ego 模式可视化
- 距离带：按嵌入阈值分为 `near` / `mid` / `far`
- 面向重复查询的嵌入缓存优化

v0.5.0 起可用。

</Accordion>

<Accordion title="自定义网关上我的 NER 抽取器静默回退到模式模式" icon="triangle-exclamation">

**v0.5.0** 已修复。现在 `response_format=json_object` 参数会对不兼容的网关按条件省略，并自动回退到普通 `generate()` 加 JSON 解析。升级修复：

```bash
pip install --upgrade semantica
```

</Accordion>

</AccordionGroup>


## 技术问题

<AccordionGroup>

<Accordion title="支持哪些图数据库？" icon="diagram-project">

- **Neo4j**：行业标准，Cypher 查询语言
- **FalkorDB**：Redis 协议，超低延迟
- **Apache AGE**：PostgreSQL 扩展，OpenCypher
- **Amazon Neptune**：AWS 托管，SPARQL 和 Gremlin
- **NetworkX**：内存版，适合开发和小图

</Accordion>

<Accordion title="有哪些导出格式？" icon="file-export">

RDF（Turtle、JSON-LD、N-Triples、XML）、Apache Parquet、ArangoDB AQL、Apache Arrow、LPG、CSV、YAML、OWL 本体，以及距离矩阵。

</Accordion>

<Accordion title="支持哪些向量库？" icon="server">

FAISS、Pinecone、Weaviate、Qdrant、Milvus、PgVector 和内存版。所有后端共用同一套 `VectorStore` API：改一行代码即可切换。

</Accordion>

<Accordion title="支持哪些 LLM 提供商？" icon="microchip">

Groq、OpenAI、Anthropic、Google Gemini、Ollama（完全本地）、DeepSeek、Novita AI、LiteLLM（一个接口接入 100+ 模型），以及任何 OpenAI 兼容网关。

</Accordion>

<Accordion title="Semantica 生产可用吗？" icon="shield-check">

可以。每个版本都带有：

- 1000+ 项通过测试，覆盖 Python 3.8–3.12
- `PipelineValidator` 和 `FailureHandler`，带指数退避和可配置重试策略
- 覆盖所有模块的 W3C PROV-O 溯源追踪
- 带 SHA-256 校验和与完整审计轨迹的变更管理
- 12 项安全漏洞修复：eval 注入、pickle 反序列化、SQL 注入、XXE、SSRF、ReDoS、路径穿越等

</Accordion>

</AccordionGroup>


## 故障排查

<AccordionGroup>

<Accordion title="ModuleNotFoundError: No module named 'semantica'" icon="xmark-circle">

确认激活了正确的 Python 环境：

```bash
pip list | grep semantica
pip install --upgrade semantica
```

</Accordion>

<Accordion title="安装时依赖报错" icon="xmark-circle">

```bash
pip install --upgrade pip wheel
pip install semantica
```

Windows 上 `[all]` 失败时，改为逐个安装 extra。

</Accordion>

<Accordion title="处理过程中内存报错" icon="memory">

减小批量、开启流式摄取，或换用持久化图后端：

```python
from semantica.graph_store import FalkorDBStore
store   = FalkorDBStore(host="localhost", port=6379)
builder = GraphBuilder(merge_entities=True, graph_store=store)
```

</Accordion>

<Accordion title="嵌入或推理很慢" icon="gauge-high">

安装 GPU 支持并确认 CUDA 可用：

```bash
pip install "semantica[gpu]"
nvidia-smi  # 确认 GPU 可见
```

</Accordion>

<Accordion title="Windows 上 Unicode / cp1252 崩溃" icon="windows">

**v0.5.0** 已修复。升级，或给旧版本设置编码环境变量：

```bash
pip install --upgrade semantica
# 或旧版本：
set PYTHONIOENCODING=utf-8
```

</Accordion>

</AccordionGroup>


## 支持

- [Discord](https://discord.gg/sV34vps5hH) — 社区聊天与实时支持。
- [GitHub Issues](https://github.com/semantica-agi/semantica/issues) — 缺陷报告与功能建议。
- [参与贡献](../contributing-guide.md) — 帮助改进 Semantica。
