---
title: 深入学习
description: 结构化学习路径、配置参考、故障排查与性能优化指南。
source: learning-more.md
source_version: ab49bad34a55ab0ef531966840981dc8d1011dd9
icon: "graduation-cap"
---

无论你是在跑第一条流水线，还是在生产环境中部署 Semantica，本页都为你提供一条清晰的前进路径：从入门一路走到企业级用法。


## 学习路径

- **入门(1–2 小时)**：刚接触 Semantica 和知识图谱(Knowledge Graph)。[从安装开始 →](./installation.md)
- **进阶(4–6 小时)**：已掌握基础，正在构建真实应用。[从模块开始 →](./modules.md)
- **高级(8+ 小时)**：企业级部署、定制与扩展。[从架构开始 →](./architecture.md)

<Tabs>
  <Tab title="入门(1–2 小时)">
    刚接触 Semantica 和知识图谱。不需要任何图数据库经验。

    <Steps>
      <Step title="搭建环境">
        [安装指南](./installation.md)：虚拟环境、可选附加依赖，以及各平台的常见问题修复。
      </Step>
      <Step title="理解核心思想">
        [核心概念](./concepts.md)：什么是知识图谱、嵌入(Embedding)如何工作、抽取到底在做什么。
      </Step>
      <Step title="运行第一个示例">
        [入门指南](./getting-started.md)：5 分钟代码走查，使用基于模式的抽取（无需 API key）。
      </Step>
      <Step title="构建第一个知识图谱">
        [快速开始教程](./quickstart.md)：从摄取到可视化的完整 6 步流水线。
      </Step>
      <Step title="交互式探索">
        [Welcome to Semantica 笔记本](https://github.com/semantica-agi/semantica/blob/main/cookbook/introduction/01_Welcome_to_Semantica.ipynb)：逐一走过每个模块的 Jupyter 笔记本。
      </Step>
    </Steps>
  </Tab>
  <Tab title="进阶(4–6 小时)">
    已掌握基础，正在构建真实应用。默认你已完成入门路径。

    <Steps>
      <Step title="了解所有模块">
        [模块指南](./modules.md)：全部 27 个模块，附代码示例与常见的流水线组合。
      </Step>
      <Step title="构建生产级知识图谱">
        [Building Knowledge Graphs 笔记本](https://github.com/semantica-agi/semantica/blob/main/cookbook/introduction/07_Building_Knowledge_Graphs.ipynb)：多源接入、去重(Deduplication)与冲突消解(Conflict Resolution)。
      </Step>
      <Step title="添加语义检索">
        [Embedding Generation 笔记本](https://github.com/semantica-agi/semantica/blob/main/cookbook/introduction/12_Embedding_Generation.ipynb)：生成嵌入、切换提供商与模型、设置维度。再配合 [Vector Store 笔记本](https://github.com/semantica-agi/semantica/blob/main/cookbook/introduction/13_Vector_Store.ipynb)：存储向量并进行相似度检索。
      </Step>
      <Step title="多源数据整合">
        [Multi-Source Data Integration 笔记本](https://github.com/semantica-agi/semantica/blob/main/cookbook/advanced/06_Multi_Source_Data_Integration.ipynb)讲解多源数据的常用整合模式。
      </Step>
    </Steps>
  </Tab>
  <Tab title="高级(8+ 小时)">
    企业级部署、定制与扩展。默认你已有生产环境使用经验。

    <Steps>
      <Step title="理解架构">
        [架构指南](./architecture.md)：四层设计、扩展点与关键设计决策。
      </Step>
      <Step title="时态智能">
        [Temporal Graphs 笔记本](https://github.com/semantica-agi/semantica/blob/main/cookbook/advanced/10_Temporal_Knowledge_Graphs.ipynb)：`valid_from`/`valid_until`、Allen 区间代数与时点查询。
      </Step>
      <Step title="本体驱动的知识库">
        [Ontology 笔记本](https://github.com/semantica-agi/semantica/blob/main/cookbook/introduction/14_Ontology.ipynb)：本体(Ontology)自动生成、SHACL 校验与本体中心。
      </Step>
      <Step title="高级可视化">
        [Complete Visualization Suite 笔记本](https://github.com/semantica-agi/semantica/blob/main/cookbook/advanced/03_Complete_Visualization_Suite.ipynb)：UMAP、t-SNE、社区布局与嵌入投影。
      </Step>
      <Step title="企业级导出">
        [Multi-Format Export 笔记本](https://github.com/semantica-agi/semantica/blob/main/cookbook/advanced/05_Multi_Format_Export.ipynb)：带 W3C PROV-O 溯源的资源描述框架(RDF)、Parquet、Neo4j Cypher、Arrow 与网络本体语言(OWL)。
      </Step>
    </Steps>
  </Tab>
</Tabs>


## 配置参考

所有设置都能用环境变量覆盖，无需改动任何代码。

| 设置项 | 环境变量 | 默认值 |
| :------- | :-------------------- | :------- |
| OpenAI API 密钥 | `OPENAI_API_KEY` | `None` |
| Groq API 密钥 | `GROQ_API_KEY` | `None` |
| Anthropic API 密钥 | `ANTHROPIC_API_KEY` | `None` |
| 图存储后端 | `GRAPH_STORE_DEFAULT_BACKEND` | `"neo4j"` |
| 向量库后端 | `VECTOR_STORE_DEFAULT_BACKEND` | `"faiss"` |
| 服务器主机 | `SEMANTICA_HOST` | `"127.0.0.1"` |
| 服务器 API 密钥 | `SEMANTICA_API_KEY` | `None` |


## 故障排查

<AccordionGroup>

<Accordion title="ModuleNotFoundError: No module named 'semantica'" icon="circle-xmark">

请确认安装无误、且处于正确的 Python 环境：

```bash
pip list | grep semantica
pip install --upgrade semantica
```

如需可选功能，安装对应的附加依赖：

```bash
pip install "semantica[llm-openai]"   # OpenAI provider
pip install "semantica[gpu]"          # GPU acceleration
```

</Accordion>

<Accordion title="AuthenticationError" icon="lock">

把 API key 设为环境变量（切勿把密钥硬编码在源码里）：

```bash
export OPENAI_API_KEY="sk-..."
export GROQ_API_KEY="gsk_..."
```

</Accordion>

<Accordion title="MemoryError 或 OOM 崩溃" icon="memory">

把默认基于内存的 NetworkX 后端换成持久化图数据库：

```python
from semantica.graph_store import FalkorDBStore
from semantica.kg import GraphBuilder

store   = FalkorDBStore(host="localhost", port=6379)
builder = GraphBuilder(merge_entities=True, graph_store=store)
```

处理大规模语料时，还应减小批大小，并启用流式摄取。

</Accordion>

<Accordion title="大数据集上处理缓慢" icon="gauge">

启用并行执行与 GPU 加速：

```python
from semantica.pipeline import ParallelismManager, Task

# Run pipeline tasks concurrently across worker threads
manager = ParallelismManager(max_workers=8)
tasks = [
    Task("task_1", lambda: "process part 1"),
    Task("task_2", lambda: "process part 2"),
]
results = manager.execute_parallel(tasks)
```

```bash
pip install "semantica[gpu]"  # CUDA-backed embeddings
```

</Accordion>

<Accordion title="Windows 上 [all] 安装失败" icon="windows">

升级到最新版本：

```bash
pip install --upgrade semantica
```

或者逐项安装附加依赖：先执行 `pip install semantica`，再按需加上 `[llm-openai]`、`[gpu]` 等。

</Accordion>

<Accordion title="Windows 上的 cp1252 编码崩溃" icon="windows">

设置编码环境变量：

```bash
set PYTHONIOENCODING=utf-8
```

</Accordion>

</AccordionGroup>


## 性能优化

<AccordionGroup>

<Accordion title="后端选型：开发环境与生产环境" icon="server">

| 操作 | NetworkX(默认) | Neo4j / FalkorDB |
| :--------- | :------------------ | :---------------- |
| 图构建 | 快 | 中等 |
| 查询性能 | 中等 | 快 |
| 可扩展性 | 仅限内存 | 持久化、生产级规模 |
| 推荐用途 | 开发、小规模图 | 生产、大规模语料 |

本地开发与原型验证用 NetworkX 即可；上线生产之前，切换到持久化后端。

</Accordion>

<Accordion title="大规模语料的批处理" icon="layer-group">

批量处理文档，而不是一篇一篇来。把长文本分块，再分批抽取实体：

```python
from semantica.split import TextSplitter
from semantica.semantic_extract import NERExtractor

document_text = "Acme Corp announced record revenue in Seattle. CEO Jane Doe presented results."
splitter = TextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = splitter.split(document_text)

extractor = NERExtractor()
batch_entities = extractor.extract_entities_batch([c.text for c in chunks])
```

</Accordion>

<Accordion title="去重 v2：最高提速 7 倍" icon="bolt">

如果去重成为瓶颈，可以在相似度打分之前先用候选筛选(candidate blocking)，减少 O(n²) 量级的两两比较：

```python
from semantica.deduplication import DuplicateDetector, EntityMerger

entities = [
    {"id": "1", "name": "Acme Corp", "type": "Company"},
    {"id": "2", "name": "Acme Corporation", "type": "Company"},
    {"id": "3", "name": "Globex", "type": "Company"},
]

# Fast candidate blocking for large entity sets
detector = DuplicateDetector(similarity_threshold=0.8)
duplicates = detector.detect_duplicates(entities, candidate_strategy="blocking_v2")

merger = EntityMerger()
merged = merger.merge_duplicates(entities, strategy="keep_most_complete")
```

`blocking_v2` 与 `hybrid_v2` 两种候选策略会在计算细粒度相似度之前，先过滤掉候选对。

</Accordion>

</AccordionGroup>


## 安全最佳实践

- **API 密钥**：存放在环境变量或密钥管理服务中，绝不提交到版本控制，并按周期轮换
- **敏感数据**：涉及个人身份信息(PII)或涉密内容时，使用本地嵌入模型（Ollama、HuggingFace）；尚未签订数据处理协议时，避免把敏感数据发往外部 API
- **图导出**：对敏感的导出数据做静态加密；配置自定义大语言模型(LLM)网关时，启用可防服务端请求伪造(SSRF)的 `base_url` 校验
- **XML 摄取**：始终使用 `XMLIngestor`，它基于可防 XML 外部实体注入(XXE)的 lxml 后端；绝不要用标准库解析器处理不可信的 XML

- [Cookbook](./cookbook.md)：从入门到高级的交互式 Jupyter 笔记本。
- [常见问题](./faq.md)：解答高频疑问。
- [API 参考](./reference/core.md)：完整的技术文档。
