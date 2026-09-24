---
title: 社区项目
description: Semantica 社区构建的项目、扩展与集成。
source: community-projects.md
source_version: e2af5e4626e15ea62e0da7dab7ca18925a3edb04
icon: "people-group"
---

<Tip>
  正在用 Semantica 构建东西？欢迎[在 GitHub 上提交](https://github.com/semantica-agi/semantica/issues/new?template=community_project.md)：我们很乐意在这里展示你的作品。
</Tip>

Semantica 的用户遍布学术界、企业界和独立研究圈。下面是社区正在构建的生态一瞥。


## 使用 Semantica 的项目

### 科研与学术界

学术界团队正用 Semantica 从非结构化的科学文献中构建结构化、可审计的知识。

- **学术文献图谱**：在跨年语料上构建引文图，并附带时态溯源(Provenance)
- **生物医学知识图谱(Knowledge Graph)**：从 PubMed 和预印本源流中关联基因、蛋白质、药物与疾病
- **社交网络分析**：在实体关联的交互图上做社区发现(Community Detection)与影响力分析
- **计算语言学**：指代消解(Coreference Resolution)流水线，输出实体关联结果，供下游 NLP 任务使用

### 企业与产业界

生产级部署遍布受监管、高风险的行业——在这些行业里，AI 的可问责性不是可选项。

- **商业智能**：用申报文件、报告和内部文档构建企业知识库
- **网络安全与威胁情报**：攻击者归因图、关联 CVE 的威胁情报源、事件时间线
- **医疗与临床 AI**：患者安全图、药物相互作用知识库、符合 HIPAA 的审计轨迹
- **金融服务**：反欺诈图、监管合规流水线（SOX/GDPR/MiFID II）、风险血缘
- **法律与合规**：合同分析流水线、法规变动追踪、有证据支撑的研究图谱
- **关键基础设施**：供应链风险图、电网事件图、物流溯源

### 独立开发者与开源

- **GraphRAG 工具包**：基于 Semantica 的 `context` 与 `vector_store` 模块搭建的自定义检索层
- **领域专用抽取器**：面向临床、法律和科学文本的命名实体识别(NER)与关系抽取器
- **时态图看板**：用 Semantica 的 `TemporalKnowledgeGraph` 加自定义可视化适配器搭建的可视化时间线


## 支持的集成

<Tabs>
  <Tab title="向量数据库">
    | 存储 | 说明 |
    | :---- | :---- |
    | **FAISS** | 进程内运行，支持 CPU/GPU |
    | **Pinecone** | 托管向量云服务 |
    | **Weaviate** | 模式优先的混合检索(Hybrid Search) |
    | **Qdrant** | Rust 原生，高性能 |
    | **Milvus** | 企业级分布式 |
    | **PgVector** | Postgres 原生，贴合 SQL 技术栈 |
  </Tab>
  <Tab title="图数据库">
    | 存储 | 说明 |
    | :---- | :---- |
    | **Neo4j** | 行业标准，支持 Cypher 查询 |
    | **FalkorDB** | Redis 协议，低延迟 |
    | **Apache AGE** | PostgreSQL 扩展，支持 OpenCypher |
    | **Amazon Neptune** | AWS 托管，支持 SPARQL + Gremlin |
  </Tab>
  <Tab title="LLM 提供商">
    | 提供商 | 说明 |
    | :-------- | :---- |
    | **OpenAI** | GPT-4o、GPT-4、GPT-3.5 |
    | **Anthropic** | Claude Opus、Sonnet、Haiku |
    | **Google Gemini** | Gemini Pro 及其他 Gemini 模型 |
    | **Groq** | LLaMA、Mixtral（高速推理） |
    | **Ollama** | 完全本地，可物理隔离部署 |
    | **HuggingFace** | 基于 Transformers 的本地 LLM 模型 |
    | **DeepSeek** | deepseek-chat 与推理模型 |
    | **Novita AI** | OpenAI 兼容网关，默认 DeepSeek-V3.2 |
    | **LiteLLM** | 100 多个模型的统一网关 |
  </Tab>
  <Tab title="NLP 库">
    | 库 | 说明 |
    | :------- | :---- |
    | **spaCy** | 生产级 NER 与依存句法分析 |
    | **NLTK** | 分词与特征抽取 |
    | **Sentence Transformers** | 语义嵌入(Embedding) |
    | **FastEmbed** | 轻量、推理快 |
  </Tab>
</Tabs>


## 社区扩展

插件系统（`PluginRegistry`）让你无需改动核心代码就能添加新能力。社区已经构建了：

- **自定义实体抽取器**：面向临床实体、法律条款类型和金融工具的领域专用 NER
- **导出适配器**：为专有行业系统提供专用的序列化格式
- **摄取(Ingestion)插件**：SharePoint、Notion、Confluence 和自定义数据库的适配器
- **可视化插件**：基于 Plotly、D3.js 和自定义图渲染器的增强看板
- **评测工具**：用 `semantica.evals` 搭建的领域专用精确率/召回率基准


## 构建你自己的扩展

任何 Semantica 组件都能通过注册表(registry)模式来扩展：

```python
from semantica.ingest.registry import method_registry

def my_ingestor(source):
    return [{"text": "...", "metadata": {}, "source": source}]

method_registry.register("file", "my_format", my_ingestor)
```

完整的扩展指南见[架构](./architecture.md#扩展点)。


## 如何贡献

- [贡献指南](./contributing-guide.md)：提交代码、文档、测试或 cookbook notebook。
- [GitHub Issues](https://github.com/semantica-agi/semantica/issues)：报告缺陷、提出功能需求或建议新的集成。
- [Discord](https://discord.gg/sV34vps5hH)：与社区分享你正在构建的东西。
- [GitHub Discussions](https://github.com/semantica-agi/semantica/discussions)：长文提问、设计讨论和想法交流。
