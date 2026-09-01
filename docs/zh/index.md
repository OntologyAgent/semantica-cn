---
title: "Semantica"
description: "AI 的问责与上下文层：上下文图 · 决策智能 · 全程溯源"
source: index.md
source_version: a16d01076b5586fcda2c47184f450a4503fbe29f
---

```bash
pip install semantica
```

你的 AI 智能体(Agent)刚做了一个决策。现在需要有人解释它。

*它当时知道什么？哪些事实影响了结果？这些事实从哪来？它以前做过同样的判断吗——结果如何？*

如果你的技术栈无法用可追溯的记录回答这些问题，你就有一个缺口。不是能力缺口，而是**问责缺口**。AI 至今没能在医疗、金融、法律和政府领域规模化落地，原因就在这里。面向这些市场的团队之所以反复重造同一套护栏，也是因为这个。

**Semantica 补上了这个缺口。**它是位于现有智能体框架之下的上下文与问责层——不替代 LangChain 或 LlamaIndex，而是让它们的输出变得可信的基础设施。


## 每个生产级 AI 团队都会遇到的问题

强大的智能体不会自动变得可信。五个结构性盲区，让现代 AI 系统无法在受监管的环境中部署：

**没有记忆结构** — 智能体存的是嵌入(Embedding)，不是语义
- 无法追问一个事实当初为何被召回
- 召回的事实无法回链到源文档
- 上下文是个黑盒，每次运行都清零

**没有决策轨迹** — 智能体持续行动，却什么也不记录
- 拿不出历史记录给监管者或审计师
- 无法重放或复现过去的决策
- 调试靠重跑，而不是回看记录

**没有溯源** — 输出无法追溯到源事实
- 在医疗、金融和法律领域，这是硬性合规障碍
- 推理结果与原始文档之间没有血缘链路
- 根本说不出智能体当时依据了什么

**没有推理透明度** — 黑盒输出，没有解释
- 无法验证推理路径
- 无法对某个具体结论提出异议
- 改进或纠正后续行为缺乏依据

**没有冲突检测** — 相互矛盾的事实静默共存于向量库
- 两个来源不一致时毫无察觉
- 输出随时间变得前后矛盾、不可预测
- 知识库越大，静默失败越多

<Note>
  这些不是极端个例。它们正是企业 AI 试点停滞的原因，也是你的合规团队总说"再等等"的原因。
</Note>


## Semantica 为你的技术栈补上什么

Semantica 给每个智能体补齐可问责所需的基础设施。几分钟即可接入现有环境：

**上下文图(Context Graph)** — 一个结构化、可查询的图，记录智能体知道、决策和推理的一切
- 跨运行持久化：会话之间不丢上下文
- 支持 SPARQL 查询和完整的图算法
- 时态模型：节点和边带 `valid_from` / `valid_until`
- 可对完整知识状态做时间点快照

**决策智能(Decision Intelligence)** — 每个决策都是系统中的一等对象
- `record_decision()` 记录完整生命周期和因果链
- 基于历史决策的混合先例检索，保持决策一致
- `analyze_decision_impact()` 展示下游影响
- 从触发到结果的因果链可视化

**全程溯源** — 每个事实都链到源文档和摄取(Ingestion)事件
- 全模块兼容 W3C PROV-O 的血缘追踪
- 从原始输入到最终推理全程可追溯
- `recorded_at` 时间戳，支持 OWL-Time 导出
- 开箱满足 HIPAA、SOX、GDPR、FDA 21 CFR Part 11 审计要求

**推理引擎(Reasoning Engine)** — 可解释的推理路径，而非黑盒
- 前向链、Rete、演绎、溯因
- 基于 SPARQL 查询的 RDF 图推理
- 支持递归 Horn 子句的 Datalog
- 每个结论都有可追溯的推导路径

**时态智能** — 图不仅知道"是什么"，还知道"什么时候"
- Allen 区间代数：覆盖全部 13 种时态关系
- 对历史图状态做时间点查询
- 每个事实都带时态溯源戳
- OWL-Time 导出，符合标准归档要求

**本体中心(Ontology Hub)** — 浏览器内的本体(Ontology)全生命周期管理
- 可视化编辑器，设计和修改模式
- SHACL Studio 编写和校验约束
- 跨多个本体对齐编排
- 内置健康看板与版本控制

<Tip>
  可与任意大语言模型(LLM)提供商、任意智能体框架配合使用：不改变现有架构，直接叠加。
</Tip>

<img src="/assets/img/diagrams/architecture-overview.svg" alt="Semantica 四层架构：摄取 → 处理 → 智能 → 应用" style={{ width: '100%', borderRadius: '12px', margin: '24px 0' }} />


## 看它跑起来

一条 pip 命令安装。几行代码接入你的智能体。其余一切都变得可追溯。

```bash
pip install semantica
```

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

- [完整快速开始](./quickstart.md) — 逐步走完整条流水线
- [Cookbook](../cookbook.md) — 40 多个实战 Jupyter 笔记本
- [加入 Discord](https://discord.gg/sV34vps5hH) — 社区交流与技术支持


## 为出错的代价高昂的领域而生

Semantica 为这样的领域设计：每个决策必须可解释，每个事实必须可追溯。

<Warning>
  **这是系统级可解释性，不是基础模型可解释性。**Semantica 不暴露、不重建、不解释 LLM/基础模型*内部*发生了什么——其内部推理或思维链对外部系统始终是不透明的。Semantica 解释的是模型*之外*的部分：输入的上下文和数据、产生的决策、它的溯源、相关的关系、适用的策略，以及完整的执行轨迹。完整边界说明见[核心概念](../concepts.md)。
</Warning>

**医疗与生命科学**
- 带完整审计轨迹的临床决策支持
- 药物相互作用与禁忌图谱
- 患者安全事件追踪与根因分析
- 开箱即用的 HIPAA 合规溯源链

**金融与风控**
- 欺诈检测知识图谱(Knowledge Graph)
- 经得起审计的风险评估轨迹
- SOX、GDPR 与 MiFID II 合规基础设施
- 面向监管报告的模型决策血缘

**法律与合规**
- 循证研究，每条引用事实都带溯源链接
- 条款抽取可追溯的合同分析
- 跨辖区的法规变化追踪
- 可用于法庭文书的完整推理路径

**网络安全**
- 关联攻击者、TTP 和指标的威胁归因图谱
- 带完整事件溯源的应急响应时间线
- 覆盖完整杀伤链的安全审计轨迹
- 对齐 MITRE ATT&CK 的知识图谱集成

**政府与国防**
- 从简报到结果的决策轨迹
- 带溯源链的涉密信息处理
- 情报报告的证据链审查
- 支持本地 LLM 的物理隔离部署

**关键基础设施**
- 基于时态智能的电网状态追踪
- 交通安全事件图谱
- 带决策审计轨迹的应急响应协同
- 高风险运营决策的后果建模


## 从这里开始

<Steps>
  <Step title="安装 Semantica">
    ```bash
    pip install semantica
    ```
    可选 extras（`[all]`、`[neo4j]`、`[pinecone]`）和环境配置见[安装指南](./installation.md)。
  </Step>
  <Step title="跑通快速开始">
    用 [5 分钟](./quickstart.md)搭一条完整的知识图谱流水线：
    - 从任意来源摄取文档
    - 抽取实体和关系
    - 构建并查询图
    - 记录并追溯一个决策
  </Step>
  <Step title="建立心智模型">
    [核心概念](../concepts.md)涵盖：
    - 知识图谱与向量库：各自适用场景
    - GraphRAG 是什么，Semantica 如何实现它
    - 溯源与决策追踪如何协同
    - 问责层架构
  </Step>
  <Step title="深入任意模块">
    每个模块都有专门的[参考页](../reference/context.md)：
    - 完整的类和方法文档
    - 带类型和默认值的参数表
    - 每个功能的可运行代码示例
  </Step>
</Steps>

- [安装](./installation.md) — 一分钟内装好 Semantica
- [快速开始](./quickstart.md) — 5 分钟搭一条完整的知识图谱流水线
- [核心概念](../concepts.md) — API 背后的心智模型
- [API 参考](../reference/context.md) — 模块、类、方法的精确说明
- [Cookbook](../cookbook.md) — 面向真实场景的领域笔记本
- [更新日志](https://github.com/semantica-agi/semantica/releases) — 发布历史


## 全部能力

<AccordionGroup>

<Accordion title="上下文与决策智能" icon="brain">

### 上下文图

- 实体、关系、决策的结构化持久图
- 时态模型：每个节点和边带 `valid_from` / `valid_until`
- 跨历史图状态的时间点查询
- 距离智能：语义邻域与 N×N 距离矩阵

### 决策追踪

- `record_decision()` 全生命周期管理与因果链
- 基于历史决策的混合相似度检索，保证决策一致
- `analyze_decision_impact()` 与 `analyze_decision_influence()` 建模下游后果
- Ego 模式探索，聚焦目标邻域调查

</Accordion>

<Accordion title="知识工程" icon="diagram-project">

### 实体与关系抽取

- 命名实体识别(NER)：模式、机器学习或 LLM 三种方法
- 基于 LLM 或规则流水线的类型化三元组(Triplet)抽取
- 带时态与因果链接的事件抽取

### 本体与模式

- 本体中心：可视化编辑器、SHACL Studio、对齐、健康看板
- 去重 v2：`blocking_v2`、`hybrid_v2`、`semantic_v2`，最快提升 7 倍
- Datalog 推理：递归 Horn 子句规则与不动点语义
- SPARQL 推理：基于查询的 RDF 图推理

</Accordion>

<Accordion title="溯源与可审计性" icon="shield-check">

### 血缘追踪

- 全模块 W3C PROV-O 血缘：每个事实都有出处
- `recorded_at` 时间戳与完整的 OWL-Time 导出
- 带 SHA-256 校验和的变更管理与版本控制
- 从摄取事件到最终推理的完整审计轨迹

### 合规基础设施

- HIPAA：带审计级溯源链的患者数据处理
- SOX / MiFID II：全程可追溯的金融决策记录
- GDPR：支撑主体访问权与被遗忘权工作流的数据血缘
- FDA 21 CFR Part 11：电子记录与电子签名合规

</Accordion>

<Accordion title="数据摄取与导出" icon="database">

### 摄取格式

- 文档：PDF、DOCX、HTML、PPTX、Docling 版面分析
- 结构化数据：JSON、CSV、Excel、Parquet、XML
- 来源：网页爬取、SQL、Snowflake、订阅源、邮件、代码仓库、MCP

### 向量库

- FAISS、Pinecone、Weaviate、Qdrant、Milvus、PgVector、内存模式

### 图库

- Neo4j、FalkorDB、Apache AGE、Amazon Neptune

### 导出格式

- RDF：Turtle、JSON-LD、N-Triples、RDF/XML
- 表格：Parquet、CSV、Arrow
- 图：GraphML、GEXF、DOT、ArangoDB AQL
- 本体：OWL、SKOS、SHACL

</Accordion>

</AccordionGroup>


## 模块参考

| 模块 | 提供的能力 |
| :-------- | :----------------- |
| `semantica.context` | 上下文图、智能体记忆、决策追踪、因果分析、先例检索 |
| `semantica.kg` | 知识图谱构建、图算法、时态模型、Allen 区间代数 |
| `semantica.semantic_extract` | NER、关系抽取、事件抽取、三元组生成 |
| `semantica.reasoning` | 前向链、Rete、演绎、溯因、SPARQL、Datalog |
| `semantica.ontology` | SHACL、SKOS、对齐、diff/迁移、自动生成、OWL/RDF |
| `semantica.explorer` | FastAPI 知识探索器、本体中心、距离智能、SHACL Studio |
| `semantica.mcp_server` | MCP stdio 服务器：面向 Claude Desktop、VS Code、Cursor、Windsurf、Cline 的 12 个工具 |
| `semantica.vector_store` | FAISS、Pinecone、Weaviate、Qdrant、Milvus、PgVector |
| `semantica.graph_store` | Neo4j、FalkorDB、Apache AGE、Amazon Neptune |
| `semantica.triplet_store` | 内存与持久化 RDF 三元组存储，带 SPARQL |
| `semantica.ingest` | 文件、网页、订阅源、数据库、Snowflake、Parquet、XML、MCP |
| `semantica.parse` | 文档解析：PDF、DOCX、HTML、PPTX、Docling 版面分析 |
| `semantica.split` | 文本分块：句子、段落、token、语义边界等策略 |
| `semantica.normalize` | 文本规范化、实体名规范化、空白与编码清理 |
| `semantica.embeddings` | Sentence-Transformers、FastEmbed、OpenAI、BGE、Ollama 本地嵌入 |
| `semantica.pipeline` | 流水线 DSL、并行 worker、重试策略、失败处理 |
| `semantica.export` | RDF、Parquet、ArangoDB AQL、CSV、OWL、Arrow、GraphML、GEXF、DOT |
| `semantica.visualization` | 程序化图渲染：force、hierarchical、circular、spring 布局 |
| `semantica.deduplication` | 实体去重 v1/v2、相似度评分、分块阻塞、合并 |
| `semantica.conflicts` | 跨重叠知识源的冲突检测与消解 |
| `semantica.provenance` | W3C PROV-O 血缘追踪、来源标注、审计轨迹 |
| `semantica.change_management` | 带 SHA-256 校验和的版本控制、diff、回滚 |
| `semantica.llms` | Groq、OpenAI、Anthropic、Gemini、Ollama、DeepSeek、Novita AI、LiteLLM、HuggingFace |
| `semantica.seed` | 从 CSV、JSON、SQL、API、RDF 源播种基础图谱 |
| `semantica.evals` | 评测框架：KG 质量、抽取 F1、流水线基准、回归追踪 |
| `semantica.core` | 编排、ConfigManager、LifecycleManager、PluginRegistry、MethodRegistry |
| `semantica.utils` | 日志、校验、进度追踪、哈希工具、嵌套字典辅助 |


## 为什么选 Semantica？

**开源，MIT 协议** — 没有厂商锁定，没有付费墙功能。
- 源码全部托管在 GitHub
- 每一行都可被你的安全团队审计
- 无限制地 fork、扩展、自托管
- 无遥测，无使用上报

**生产可用** — 为容不下意外的团队打造。
- 1000+ 通过的测试，完整回归覆盖
- `PipelineValidator` 在启动时就拦住配置错误
- `FailureHandler` 支持指数退避和死信队列
- v0.5.0 修复了 12 个安全漏洞

**模块化设计** — 只导入需要的部分。
- 不接图库也能用 `NERExtractor`
- 不接向量存储也能用 `ContextGraph`
- 每个组件都可独立替换、独立测试
- 不绑定框架：适配任意智能体技术栈
