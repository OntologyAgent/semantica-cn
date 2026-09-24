---
title: Cookbook
description: 交互式 Jupyter notebook，覆盖从你的第一个知识图谱到生产级 GraphRAG 系统的全过程。
source: cookbook.md
source_version: 7445c9d638dad612e736bab10b00aed71da5e32c
icon: "flask"
---

<Tip>
  **从哪里开始：**
  - **初次接触 Semantica**：从[核心教程](#核心教程)开始
  - **正在构建应用**：参见[进阶概念](#进阶概念)
  - **安装遇到问题**：参见[安装指南](./installation.md)
</Tip>

<Note>
  前置要求：Python 3.10+、Jupyter，以及你所用大语言模型(LLM)提供商的 API key。
</Note>


## 精选食谱

- **[Your First Knowledge Graph](https://github.com/semantica-agi/semantica/blob/main/cookbook/introduction/08_Your_First_Knowledge_Graph.ipynb)**：20 分钟内从原始文本得到可查询的知识图谱(Knowledge Graph)。主题：抽取、图构建、可视化 · *入门*


## 核心教程

掌握 Semantica 框架的必备教程。

- **[Welcome to Semantica](https://github.com/semantica-agi/semantica/blob/main/cookbook/introduction/01_Welcome_to_Semantica.ipynb)**：框架核心理念与全部模块的交互式导览。主题：框架概览、架构 · *入门*
- **[Data Ingestion](https://github.com/semantica-agi/semantica/blob/main/cookbook/introduction/02_Data_Ingestion.ipynb)**：从文件、网页、数据库、流、订阅源、代码仓库、邮件和 MCP 加载数据。主题：FileIngestor、WebIngestor、DBIngestor · *入门*
- **[Document Parsing](https://github.com/semantica-agi/semantica/blob/main/cookbook/introduction/03_Document_Parsing.ipynb)**：从 PDF、DOCX、HTML 等复杂格式中提取干净的文本。主题：OCR、PDF 解析、文本抽取 · *入门*
- **[Data Normalization](https://github.com/semantica-agi/semantica/blob/main/cookbook/introduction/04_Data_Normalization.ipynb)**：清洗、规范化(Normalization)、备好文本的流水线。主题：文本清洗、Unicode、格式化 · *入门*
- **[Entity Extraction](https://github.com/semantica-agi/semantica/blob/main/cookbook/introduction/05_Entity_Extraction.ipynb)**：用命名实体识别(NER)识别人物、组织和自定义实体。主题：NER、spaCy、LLM 抽取 · *入门*
- **[Relation Extraction](https://github.com/semantica-agi/semantica/blob/main/cookbook/introduction/06_Relation_Extraction.ipynb)**：发现并归类实体之间的关系。主题：关系分类、依存句法分析 · *入门*
- **[Embedding Generation](https://github.com/semantica-agi/semantica/blob/main/cookbook/introduction/12_Embedding_Generation.ipynb)**：创建并管理用于语义检索的向量嵌入(Embedding)。主题：嵌入、OpenAI、HuggingFace · *进阶*
- **[Vector Store](https://github.com/semantica-agi/semantica/blob/main/cookbook/introduction/13_Vector_Store.ipynb)**：搭建向量库(Vector Store)，支撑相似度检索。*进阶*
- **[Graph Store](https://github.com/semantica-agi/semantica/blob/main/cookbook/introduction/09_Graph_Store.ipynb)**：把知识图谱持久化到 Neo4j 或 FalkorDB。主题：Neo4j、Cypher、持久化 · *进阶*
- **[Ontology](https://github.com/semantica-agi/semantica/blob/main/cookbook/introduction/14_Ontology.ipynb)**：定义领域模式与本体(Ontology)，为数据赋予结构。主题：OWL、RDF、模式设计 · *进阶*
- **[Seed Data](https://github.com/semantica-agi/semantica/blob/main/cookbook/introduction/25_Seed_Data.ipynb)**：在抽取运行之前，用可信的 CSV、JSON、数据库和 API 数据源预置知识图谱。主题：SeedDataManager、基础图谱 · *进阶*
- **[Semantic Layer Basics](https://github.com/semantica-agi/semantica/blob/main/cookbook/introduction/26_Semantic_Layer_Basics.ipynb)**：收官教程，综合运用知识图谱、生成的本体、显式映射、与本体对齐的 RDF 和一条 SPARQL 查询。主题：语义层(Semantic Layer)、本体映射、Oxigraph、SPARQL · *进阶*


## 进阶概念

深入高级特性、自定义与复杂工作流。

- **[Advanced Extraction](https://github.com/semantica-agi/semantica/blob/main/cookbook/advanced/01_Advanced_Extraction.ipynb)**：自定义抽取器、基于 LLM 的抽取和复杂模式匹配。主题：自定义模型、正则表达式、LLM · *高级*
- **[Advanced Graph Analytics](https://github.com/semantica-agi/semantica/blob/main/cookbook/advanced/02_Advanced_Graph_Analytics.ipynb)**：中心性(Centrality)、社区发现(Community Detection)与寻路算法。主题：PageRank、Louvain、最短路径 · *高级*
- **[Advanced Context Engineering](https://github.com/semantica-agi/semantica/blob/main/cookbook/advanced/11_Advanced_Context_Engineering.ipynb)**：用 FAISS 和 Neo4j 为 AI 智能体(Agent)搭建持久记忆系统。主题：智能体记忆(Agent Memory)、GraphRAG、实体注入 · *高级*
- **[Complete Visualization Suite](https://github.com/semantica-agi/semantica/blob/main/cookbook/advanced/03_Complete_Visualization_Suite.ipynb)**：面向图的交互式网络、分析与时态可视化。主题：PyVis、NetworkX、D3.js · *进阶*
- **[Conflict Resolution](https://github.com/semantica-agi/semantica/blob/main/cookbook/introduction/17_Conflict_Detection_and_Resolution.ipynb)**：处理多来源矛盾信息的策略。主题：真值发现、投票、置信度 · *高级*
- **[Multi-Format Export](https://github.com/semantica-agi/semantica/blob/main/cookbook/advanced/05_Multi_Format_Export.ipynb)**：导出为 RDF、OWL、JSON-LD 和 NetworkX 格式。主题：序列化、互操作性 · *进阶*
- **[Multi-Source Integration](https://github.com/semantica-agi/semantica/blob/main/cookbook/advanced/06_Multi_Source_Data_Integration.ipynb)**：把来自不同来源的数据合并成一张统一的图。主题：实体消解(Entity Resolution)、合并、融合 · *高级*
- **[Reasoning and Inference](https://github.com/semantica-agi/semantica/blob/main/cookbook/advanced/08_Reasoning_and_Inference.ipynb)**：用逻辑推理从既有事实推断新知识。主题：逻辑规则、推理引擎(Reasoning Engine) · *高级*
- **[Temporal Knowledge Graphs](https://github.com/semantica-agi/semantica/blob/main/cookbook/advanced/10_Temporal_Knowledge_Graphs.ipynb)**：为随时间变化的数据建模并查询。主题：时间序列、时态逻辑、Allen 区间代数 · *高级*
- **[Provenance Tracking](https://github.com/semantica-agi/semantica/blob/main/cookbook/introduction/22_Provenance_Tracking.ipynb)**：与 W3C PROV-O 对齐的溯源(Provenance)追踪和校验和验证，覆盖实体、关系与分块。主题：PROV-O、血缘、校验和、失效处理 · *高级*
- **[Reasoning Module](https://github.com/semantica-agi/semantica/blob/main/cookbook/introduction/23_Reasoning.ipynb)**：以前向链、后向链和 Datalog 策略从既有事实推导新知识。主题：Reasoner、Datalog、解释 · *高级*
- **[Change Management](https://github.com/semantica-agi/semantica/blob/main/cookbook/introduction/24_Change_Management.ipynb)**：为知识图谱和本体提供版本管理、审计轨迹与数据完整性检查。主题：ChangeLogEntry、版本存储、数据完整性 · *高级*


## 如何运行

<Steps>
  <Step title="安装 Semantica">
    ```bash
    pip install semantica[all]
    pip install jupyter
    ```
  </Step>
  <Step title="克隆仓库（可选，源码安装）">
    ```bash
    git clone https://github.com/semantica-agi/semantica.git
    cd semantica
    pip install -e ".[all]"
    pip install jupyter
    ```
  </Step>
  <Step title="启动 Jupyter">
    ```bash
    jupyter notebook
    ```
  </Step>
</Steps>

<Tip>
  也可以用 Docker 运行 cookbook：

  ```bash
  docker run -p 8888:8888 semantica/semantica-cookbook
  ```
</Tip>
