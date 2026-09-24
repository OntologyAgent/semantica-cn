---
title: 流水线构建器
description: 用 PipelineBuilder DSL 构建端到端数据处理工作流——在一条声明式流水线中完成摄取、抽取、规范化、嵌入与存储。
source: guides/pipeline.md
source_version: dbd478bfe99b9a7b30a9d0c405a5d44894319eba
---

`PipelineBuilder` 解决的是处理步骤之间的"粘合"问题。你只需声明步骤、注册处理函数、连好依赖关系，然后把控制权交给 `ExecutionEngine`——它会做拓扑排序、在步骤之间传递输出、失败时按可配置的退避策略重试，最后返回一个结构化的 `ExecutionResult`，方便你记录日志或触发告警。

## 为什么使用流水线？

流水线(Pipeline)解决的是多步数据处理中的协调问题。你不再编写"上一个函数调用下一个函数"的单体脚本，而是定义相互独立的步骤、声明它们之间的依赖；执行顺序由流水线引擎推算，相互独立的步骤并行运行，数据在步骤之间自动传递。

以下场景里它尤为关键：
- 多个数据源需要不同的处理逻辑
- 部分步骤可以并发执行
- 有复杂的重试或错误恢复需求
- 工作流频繁变动
- 团队协作中不同步骤由不同人负责

一条带两条并行分支的五步流水线，比线性脚本跑得更快；要加第六步，只需声明它在有向无环图(DAG)中的位置。

## 适用与不适用场景

**适合用流水线：**
- 包含 3 个以上处理阶段的多步 ETL 工作流
- 每天或每小时运行的生产定时任务
- 部分步骤可以并行的工作流
- 模块化设计能带来收益的复杂数据变换
- 不同步骤由不同人维护的团队环境

**不适合用流水线：**
- 一次性脚本或原型（用普通函数就够了）
- 只有 1-2 步的线性工作流
- Jupyter notebook 里的探索性数据分析
- 定义步骤的开销超过工作流本身复杂度的场合

## 典型流水线工作流

不论什么领域，多数数据流水线都遵循四段式模式：

1. **摄取(Ingest)** — 从文件、API、数据库或数据流拉取数据
2. **变换(Transform)** — 清洗、校验、规范化并增强原始数据
3. **抽取(Extract)** — 运行命名实体识别(NER)、关系抽取(Relationship Extraction)或其他 NLP 任务
4. **存储(Store)** — 把结果写入向量库(Vector Store)、知识图谱(Knowledge Graph)或输出文件

每个阶段都可以有多个并行步骤。举个例子：摄取阶段同时从三个不同的 REST API 拉数据，而变换阶段对每个来源套用不同的清洗规则。

<Info>
  `PipelineBuilder` 和 `ExecutionEngine` 位于 `semantica.pipeline`。失败处理、重试策略和并行度管理是独立的类，需要细粒度控制时可以单独导入。自定义步骤处理函数就是普通的 Python 函数——不需要继承任何基类。
</Info>

## 第一个流水线

最小可用的流水线只有三步：摄取、抽取、存储。定义步骤、连接依赖、构建、执行。

每个步骤都是一个函数：第一个位置参数是 `data`，步骤配置以关键字参数传入。引擎调用处理函数时，把上游数据（来自依赖步骤）作为 `data`，把步骤配置经 `**kwargs` 传入：

```python
def handler(data, **config):
    # data contains outputs from all upstream dependencies
    # config contains any parameters passed to add_step()
    processed_data = transform_logic(data, config.get("param1", "default"))
    return processed_data  # Always return data for downstream steps
```

根步骤（没有依赖）收到的 `data` 是 `None`——它们从零生成数据，而不是变换上游输出。

把处理函数通过 `handler` 关键字参数直接传给 `add_step()`，同时附上步骤配置：

```python
builder.add_step("extract_step", "ner_extract", handler=extract_entities_handler)
builder.connect_steps("ingest_step", "extract_step")
```

```python
from semantica.pipeline import PipelineBuilder, ExecutionEngine
from semantica.ingest import ingest_file
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore

# --- Define handler functions ---
# The engine calls handler(data, **step_config), so the first positional
# argument is always the upstream data; step config arrives as kwargs.

def ingest_stix_bundles(data, **config):
    # Root step — data is None, generate data from config
    files = ingest_file(config["path"], method="directory")
    return [f.text for f in files if f.file_type == "json"]

def extract_entities(data, **config):
    # data is the output from the previous step
    threshold = config.get("confidence_threshold", 0.7)
    results = []
    for text in data:
        # Your NER logic here — simplified for illustration
        results.append({"text": text, "entities": [], "threshold": threshold})
    return results

def build_graph(data, **config):
    graph   = ContextGraph(advanced_analytics=True)
    context = AgentContext(
        vector_store    = VectorStore(backend="faiss", dimension=768),
        knowledge_graph = graph,
    )
    texts = [d["text"] for d in data]
    context.store(texts, extract_entities=True, extract_relationships=True)
    context.save(config["output_path"])
    return {"node_count": graph.stats()["node_count"],
            "edge_count": graph.stats()["edge_count"]}

# --- Build the pipeline ---
# Pass handler= directly in add_step() so each PipelineStep carries its callable.

builder = PipelineBuilder()

builder.add_step("ingest",  "stix_ingest",  handler=ingest_stix_bundles, path="./stix_bundles/")
builder.add_step("extract", "ner_extract",  handler=extract_entities,    confidence_threshold=0.75)
builder.add_step("store",   "kg_build",     handler=build_graph,         output_path="./cti_output/")

builder.connect_steps("ingest",  "extract")
builder.connect_steps("extract", "store")

pipeline = builder.build("cti_pipeline")

# --- Execute ---

engine = ExecutionEngine(max_workers=4, retry_on_failure=True)
result = engine.execute_pipeline(pipeline)

print(f"Success:  {result.success}")
print(f"Output:   {result.output}")   # the final step's return value, e.g. {"node_count": ..., "edge_count": ...}
print(f"Duration: {result.metrics['execution_time']:.2f}s")
print(f"Steps completed: {result.metrics['steps_executed']}")
```

`ExecutionEngine` 在执行前会对步骤图做拓扑排序，所以即使你声明步骤的顺序不对，实际执行顺序也一定正确。每个步骤都会拿到上一步的返回值，作为自己的 `data` 参数。

## 读取 ExecutionResult

每次 `engine.execute_pipeline()` 调用都会返回一个 `ExecutionResult` dataclass。在假定成功之前，先检查它：

```python
result = engine.execute_pipeline(pipeline)

if not result.success:
    print("Pipeline failed. Errors:")
    for err in result.errors:
        print(f"  {err}")
else:
    print(f"Pipeline completed in {result.metrics['execution_time']:.1f}s")
    print(f"Steps run:    {result.metrics['steps_executed']}")
    print(f"Steps failed: {result.metrics['steps_failed']}")
    # result.output  — the return value of the final step
    # result.metadata — {"pipeline_id": "...", "execution_time": float}
```

`result.errors` 是一个 `List[str]`——每个失败步骤一条，内容是对应的异常信息。设置 `retry_on_failure=True` 后，流水线会对失败步骤重试至多 `max_retries` 次（默认 3 次），重试仍失败才记为失败并继续往下走。

## 处理失败与配置重试策略

默认情况下，`ExecutionEngine(retry_on_failure=True)` 使用指数退避策略：重试 3 次，起始间隔 1 秒，每次翻倍，上限 60 秒。对于调用外部 API 或数据库的步骤——瞬时失败在所难免——可以通过 `FailureHandler` 为每类步骤设置独立的策略：

```python
from semantica.pipeline import ExecutionEngine, FailureHandler, RetryPolicy, RetryStrategy

# Build a custom failure handler
handler = FailureHandler()

# Web/API steps: retry up to 5 times with exponential backoff
handler.set_retry_policy(
    "misp_fetch",
    RetryPolicy(
        max_retries    = 5,
        strategy       = RetryStrategy.EXPONENTIAL,
        backoff_factor = 2.0,
        initial_delay  = 2.0,
        max_delay      = 120.0,
    ),
)

# Database steps: fixed delay, fewer retries (connection pool usually recovers fast)
handler.set_retry_policy(
    "db_ingest",
    RetryPolicy(
        max_retries   = 3,
        strategy      = RetryStrategy.FIXED,
        initial_delay = 5.0,
    ),
)

# NER steps: don't retry — if the model crashes it needs human intervention
handler.set_retry_policy(
    "ner_extract",
    RetryPolicy(max_retries=0),
)

engine = ExecutionEngine(
    max_workers      = 4,
    retry_on_failure = True,
)
# ExecutionEngine builds its own FailureHandler; replace it with the configured one
engine.failure_handler = handler
# The engine now calls engine.failure_handler.get_retry_policy(step.step_type) on failure
```

`handler.classify_error()` 区分 `ValidationError`（低严重度，通常不重试）、`ProcessingError`（高严重度）和超时/连接错误（中严重度，总是重试）。查看分类结果：

```python
try:
    result = engine.execute_pipeline(pipeline)
except Exception as e:
    classification = handler.classify_error(e)
    print(f"Severity: {classification['severity'].value}")   # "high" / "medium" / "low"
    print(f"Message: {classification['message']}")
```

## 并行执行步骤

当两个步骤互不依赖——例如 NER 抽取和三元组(Triplet)抽取都在读同一份摄取输出——把二者都连接到同一个上游步骤，即可声明为并行分支：

```python
builder = PipelineBuilder()
builder.register_step_handler("file_ingest",     ingest_stix_bundles)
builder.register_step_handler("ner_extract",     run_ner)
builder.register_step_handler("triplet_extract", run_triplets)
builder.register_step_handler("kg_merge",        merge_into_graph)

builder.add_step("ingest",   "file_ingest",     path="./stix_bundles/")
builder.add_step("ner",      "ner_extract",     confidence_threshold=0.75)
builder.add_step("triplets", "triplet_extract", include_temporal=True)
builder.add_step("store",    "kg_merge",        output_path="./cti_output/")

# ingest feeds both ner and triplets in parallel
builder.connect_steps("ingest",   "ner")
builder.connect_steps("ingest",   "triplets")
# both converge into store
builder.connect_steps("ner",      "store")
builder.connect_steps("triplets", "store")

builder.set_parallelism(2)   # run ner and triplets concurrently

pipeline = builder.build("parallel_extraction")
engine   = ExecutionEngine(max_workers=2, retry_on_failure=True)
result   = engine.execute_pipeline(pipeline)
```

`set_parallelism(n)` 告诉引擎最多可以同时运行多少个步骤；`n` 必须是正整数。拓扑排序保证只有依赖全部完成的步骤才有资格并发执行——不可能在输入未就绪时误跑某个步骤。实际并发度取 `min(n, max_workers)`，因此引擎的 `max_workers` 设置始终是硬性资源上限。

并发是按步骤显式开启的。只有当一层依赖中的每个步骤都标记了 `parallel_safe`、该层步骤数超过一个、且流入该层的数据是 dict 时，这一层才会并行执行：

```python
builder.add_step("ner",      "ner_extract",     parallel_safe=True, confidence_threshold=0.75)
builder.add_step("triplets", "triplet_extract", parallel_safe=True, include_temporal=True)
```

如果层内任何一个步骤没有标记 `parallel_safe`，或某个步骤以增量模式运行，整层都会回退为顺序执行——并行永远不会悄悄绕过一个未声明安全的步骤。`parallel_safe` 是控制字段：和 `dependencies` 一样由构建器消费，不会进入处理函数的 config。

标记为 parallel-safe 的处理函数必须返回 dict。并行层中的每个步骤都会收到该层输入的一份隔离深拷贝，因此步骤之间看不到彼此的修改。各步骤的结果按键逐步合并，顺序按步骤声明顺序：某一步写入的键会加入合并结果；多个步骤写入相同值的键予以保留；两个步骤对同一个键写入不同的值，流水线即告失败，抛出的 `ProcessingError` 会指明冲突的键和涉事的两个步骤。触及共享可变资源的处理函数——数据库连接、内存存储、全局缓存——不应标记 `parallel_safe`。

## 常见陷阱

**忘记返回数据。** 如果处理函数不返回任何内容，下游步骤的 `data` 参数就是 `None`，通常导致崩溃或静默失败。除最后一步外，每个步骤都应为下一阶段返回数据。

**并行度过高。** 在 8 核机器上设 `max_workers=50`，开销比提速还多。从 `max_workers=4` 起步，边监控资源占用边逐步上调。多数 I/O 密集型步骤在中等并行度下就工作得很好。

**有状态的处理函数。** 处理函数应当是纯函数——相同的输入数据和配置应产出相同的输出。避免使用跨调用存活的全局变量、文件句柄或数据库连接。每次步骤执行都应相互独立。

**调试大型流水线。** 当 10 步流水线在第 7 步失败时，不要重跑整条流水线来调试。把失败步骤抽到独立脚本里，用真实的中间数据作输入，单独修复。

## 开发与调试

先从小处着手，逐个验证每个步骤，再组装完整流水线：

```python
# Add debug output in handlers during development
def extract_entities(data, **config):
    print(f"Processing {len(data)} items with threshold {config.get('confidence_threshold')}")
    results = []
    for item in data:
        # Your processing logic
        results.append({"text": item["text"], "entities": []})
    print(f"Generated {len(results)} results")
    return results

# Test individual handlers with known data
test_data = [{"text": "sample data", "entities": []}]
result = extract_entities(test_data, confidence_threshold=0.5)
print(f"Processed {len(result)} items")
```

对复杂流水线，可以加检查点来保存中间输出：

```python
def save_checkpoint(data, **config):
    # Save intermediate data for debugging
    checkpoint_path = config.get("checkpoint_path", "checkpoint.json")
    with open(checkpoint_path, "w") as f:
        json.dump(data, f)
    return data  # Pass data through unchanged

builder.add_step(
    "checkpoint_after_transform", "checkpoint",
    handler=save_checkpoint,
    checkpoint_path="transform_output.json"
)
builder.connect_steps("transform", "checkpoint_after_transform")
```

## 增量处理

增量(delta)流水线只处理两个数据版本之间的变化，而不是从头重跑所有数据。当数据集大到全量重跑太慢或太贵时，这是必备能力。

假设你的 STIX bundle 目录每晚新增 20-30 个文件。每天早上重跑全部 4,000 个历史文件，既浪费时间又浪费算力。在摄取步骤上设 `delta_mode=True`，流水线就只处理自上一个版本快照以来有变化的文件：

```python
builder = PipelineBuilder()
builder.register_step_handler("stix_ingest", ingest_stix_bundles)
builder.register_step_handler("ner_extract", run_ner)
builder.register_step_handler("kg_append",   append_to_graph)

builder.add_step(
    "ingest", "stix_ingest",
    handler           = ingest_stix_bundles,
    path              = "./stix_bundles/",
    delta_mode        = True,
    base_version_id   = "2024-11-30",   # last successful run
    target_version_id = "2024-12-01",   # today's snapshot
)
builder.add_step("extract", "ner_extract", handler=run_ner)
builder.add_step("store",   "kg_append",   handler=append_to_graph, output_path="./cti_output/")

builder.connect_steps("ingest",  "extract")
builder.connect_steps("extract", "store")

pipeline = builder.build("delta_pipeline")
result   = ExecutionEngine(max_workers=4, retry_on_failure=True).execute_pipeline(pipeline)

print(f"Delta run: {result.output}")
```

`base_version_id` 和 `target_version_id` 保存在 `PipelineStep` dataclass 上，并经 `config` 传给你的处理函数——由处理函数负责用它们过滤输入。常见做法是用文件修改时间与基准版本日期做比较。

## 从配置字典构建

流水线也可以定义在配置文件里——当开发、预发布、生产等不同环境要用不同路径和阈值运行同一条流水线时，这特别有用。此时不必逐个调用 `add_step()`，而是把 dict 传给 `build_pipeline()`：

```python
from semantica.pipeline import PipelineBuilder, ExecutionEngine

pipeline_config = {
    "name": "cti_pipeline",
    "parallelism": 4,
    "steps": [
        {
            "name": "ingest",
            "type": "stix_ingest",
            "config": {"path": "./stix_bundles/"},
        },
        {
            "name": "extract",
            "type": "ner_extract",
            "config": {"confidence_threshold": 0.8},
        },
        {
            "name": "store",
            "type": "kg_build",
            "config": {"output_path": "./cti_output/"},
        },
    ],
}

builder = PipelineBuilder()
# Register handlers as before, then:
pipeline = builder.build_pipeline(pipeline_config)

engine = ExecutionEngine(max_workers=4, retry_on_failure=True)
result = engine.execute_pipeline(pipeline)
```

注意：`build_pipeline()` 从每个步骤 config dict 内部的 `"dependencies"` 键读取步骤连接（而不是从 `connect_steps()` 调用读取）。走这条路时要显式声明依赖：

```python
{
    "name": "extract",
    "type": "ner_extract",
    "config": {"confidence_threshold": 0.8, "dependencies": ["ingest"]},
},
```

## 监控进度

`ExecutionEngine` 自动接入 Semantica 的进度追踪器——每个步骤的开始、更新和完成都有记录。要观察长时间运行流水线的进展，可在执行后检查 `Pipeline` 对象上的步骤状态：

```python
from semantica.pipeline import StepStatus

result   = engine.execute_pipeline(pipeline)
for step in pipeline.steps:
    status_str = step.status.value   # "completed" / "failed" / "skipped"
    print(f"  {step.name:20s}  {status_str}")
    if step.status == StepStatus.FAILED and step.error:
        print(f"    Error: {step.error}")
```

`result.metrics` 给出聚合视图：

```python
print(f"Total time:      {result.metrics['execution_time']:.2f}s")
print(f"Steps completed: {result.metrics['steps_executed']}")
print(f"Steps failed:    {result.metrics['steps_failed']}")
```

## 领域示例

<Tabs>
  <Tab title="国防 — CTI/威胁情报">
    安全运营中心(SOC)的威胁情报团队需要一条端到端流水线：从涉密目录摄取 STIX bundle，用自定义威胁行为者标签做实体抽取，构建出可供分析师查询的 `ContextGraph`。流水线每六小时运行一次，失败步骤自动重试，瞬时文件系统错误不会丢掉一轮摄取。

```python
from semantica.pipeline import PipelineBuilder, ExecutionEngine, RetryPolicy, RetryStrategy
from semantica.ingest import ingest_file
from semantica.semantic_extract import NamedEntityRecognizer
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore

def ingest_classified_stix(data, **config):
    files = ingest_file(config["path"], method="directory")
    return [
        {"text": f.text, "source": f.name, "classification": config["classification"]}
        for f in files if f.file_type == "json"
    ]

def extract_cti_entities(data, **config):
    ner = NamedEntityRecognizer(
        methods=["pattern", "ml"],
        custom_labels=["THREAT_ACTOR", "MALWARE", "CVE", "C2_DOMAIN", "CAMPAIGN"],
        confidence_threshold=config.get("confidence_threshold", 0.80),
    )
    results = []
    for doc in data:
        entities = ner.extract_entities(doc["text"])
        results.append({**doc, "entities": [e.__dict__ for e in entities]})
    return results

def build_cti_graph(data, **config):
    graph   = ContextGraph(advanced_analytics=True, community_detection=True)
    context = AgentContext(
        vector_store    = VectorStore(backend="faiss", dimension=768),
        knowledge_graph = graph,
        graph_expansion = True,
    )
    texts = [d["text"] for d in data]
    context.store(texts, extract_entities=True, extract_relationships=True)
    context.save(config["output_path"])
    return graph.stats()

builder = PipelineBuilder()
builder.register_step_handler("classified_ingest", ingest_classified_stix)
builder.register_step_handler("cti_ner",           extract_cti_entities)
builder.register_step_handler("cti_graph",         build_cti_graph)

builder.add_step("ingest",  "classified_ingest",
                 handler=ingest_classified_stix,
                 path="./classified/stix/",
                 classification="SECRET//REL TO USA FVEY")
builder.add_step("extract", "cti_ner", handler=extract_cti_entities, confidence_threshold=0.85)
builder.add_step("store",   "cti_graph", handler=build_cti_graph, output_path="./cti_state/")

builder.connect_steps("ingest",  "extract")
builder.connect_steps("extract", "store")
builder.set_parallelism(2)

pipeline = builder.build("cti_pipeline")
engine   = ExecutionEngine(max_workers=2, retry_on_failure=True)
result   = engine.execute_pipeline(pipeline)

print(f"CTI pipeline: success={result.success}, "
      f"nodes={result.output.get('node_count')}, "
      f"time={result.metrics['execution_time']:.1f}s")
```

  </Tab>

  <Tab title="安全 — SOC/事件响应">
    P1 事件处置进行中，SOC 需要一条 15 分钟的流水线：拉取最新的 SIEM 告警 CSV，与内部数据库交叉比对 CVE，然后更新事件知识图谱。流水线运行周期很紧——NER 失败不能阻塞图谱更新，因此步骤配置为 NER 出错不重试、数据库超时则激进重试。

```python
from semantica.pipeline import (
    PipelineBuilder, ExecutionEngine, FailureHandler,
    RetryPolicy, RetryStrategy,
)
from semantica.ingest import ingest_file, DBIngestor
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore

def ingest_siem_alerts(data, **config):
    files = ingest_file(config["path"], method="directory")
    return [{"text": f.text, "source": f.name}
            for f in files if f.file_type == "csv"]

def enrich_with_cves(data, **config):
    db = DBIngestor()
    cve_rows = db.execute_query(config["db_url"], config["query"])
    cve_lookup = {r["cve_id"]: r for r in cve_rows}
    for doc in data:
        doc["cve_enrichment"] = cve_lookup
    return data

def update_incident_graph(data, **config):
    graph   = ContextGraph(advanced_analytics=True)
    context = AgentContext(
        vector_store    = VectorStore(backend="faiss", dimension=768),
        knowledge_graph = graph,
    )
    texts = [d["text"] for d in data]
    context.store(texts, extract_entities=True, extract_relationships=True)
    context.save(config["output_path"])
    return graph.stats()

handler = FailureHandler()
handler.set_retry_policy("db_enrich",
    RetryPolicy(max_retries=5, strategy=RetryStrategy.EXPONENTIAL,
                initial_delay=2.0, max_delay=30.0))
handler.set_retry_policy("cti_ner", RetryPolicy(max_retries=0))

builder = PipelineBuilder()
builder.register_step_handler("siem_ingest",  ingest_siem_alerts)
builder.register_step_handler("db_enrich",    enrich_with_cves)
builder.register_step_handler("graph_update", update_incident_graph)

builder.add_step("ingest",  "siem_ingest",  handler=ingest_siem_alerts, path="./siem_exports/")
builder.add_step("enrich",  "db_enrich",
                 handler=enrich_with_cves,
                 db_url="postgresql://ro:pass@cvedb:5432/nvd",
                 query="SELECT cve_id, description, cvss_v3_score FROM cve_records "
                       "WHERE cve_id = ANY(ARRAY['CVE-2024-3400','CVE-2024-21762'])")
builder.add_step("store",   "graph_update", handler=update_incident_graph, output_path="./incident_state/")

builder.connect_steps("ingest",  "enrich")
builder.connect_steps("enrich",  "store")

pipeline = builder.build("incident_pipeline")
engine   = ExecutionEngine(max_workers=4, retry_on_failure=True)
result   = engine.execute_pipeline(pipeline)

print(f"Incident update: {result.success}, "
      f"nodes={result.output.get('node_count')}, "
      f"errors={result.errors}")
```

  </Tab>

  <Tab title="生命科学 — 临床/制药">
    临床 NLP 流水线在每个试验月度结账后处理电子健康记录(EHR)导出：从共享目录摄取患者笔记，用 HuggingFace 模型跑生物医学 NER，抽取药物/疾病/剂量实体，记录符合 ICH E6(R2) 的溯源(Provenance)，再追加到试验图谱。流水线采用增量模式，只处理自上次运行以来新增的笔记。

```python
from semantica.pipeline import PipelineBuilder, ExecutionEngine
from semantica.ingest import ingest_file
from semantica.semantic_extract import NamedEntityRecognizer
from semantica.provenance import ProvenanceManager, SourceReference
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore

def ingest_ehr_notes(data, **config):
    files = ingest_file(config["path"], method="directory")
    return [
        {"text": f.text, "patient_id": f.name.split("_")[0], "source": f.name}
        for f in files
    ]

def run_biomedical_ner(data, **config):
    ner = NamedEntityRecognizer(
        methods=["huggingface"],
        huggingface_model="d4data/biomedical-ner-all",
        confidence_threshold=config.get("confidence_threshold", 0.80),
        custom_labels=["DRUG", "DISEASE", "DOSAGE", "GENE", "BIOMARKER"],
    )
    results = []
    for doc in data:
        entities = ner.extract_entities(doc["text"])
        results.append({**doc, "entities": entities})
    return results

def track_provenance_and_store(data, **config):
    manager = ProvenanceManager(storage_path=config["provenance_db"])
    graph   = ContextGraph(advanced_analytics=True)
    context = AgentContext(
        vector_store    = VectorStore(backend="faiss", dimension=768),
        knowledge_graph = graph,
        retention_days  = None,
    )
    for doc in data:
        for entity in doc.get("entities", []):
            source = SourceReference(
                document=doc["patient_id"],
                section="clinical_note",
                confidence=getattr(entity, "confidence", 1.0),
            )
            manager.track_entity(
                entity_id=f"{doc['patient_id']}_{getattr(entity, 'text', '')}",
                source=source.document,
                metadata={"entity_type": getattr(entity, "label", ""),
                           "confidence": getattr(entity, "confidence", 1.0)},
            )
    context.store([d["text"] for d in data], extract_entities=True)
    context.save(config["output_path"])
    return graph.stats()

builder = PipelineBuilder()
builder.register_step_handler("ehr_ingest",    ingest_ehr_notes)
builder.register_step_handler("bio_ner",       run_biomedical_ner)
builder.register_step_handler("prov_store",    track_provenance_and_store)

builder.add_step("ingest",  "ehr_ingest",
                 handler=ingest_ehr_notes,
                 path="./ehr_exports/month_12/",
                 delta_mode=True,
                 base_version_id="2024-11",
                 target_version_id="2024-12")
builder.add_step("extract", "bio_ner", handler=run_biomedical_ner, confidence_threshold=0.82)
builder.add_step("store",   "prov_store",
                 handler=track_provenance_and_store,
                 provenance_db="./provenance/trial_Q4.db",
                 output_path="./trial_state/")

builder.connect_steps("ingest",  "extract")
builder.connect_steps("extract", "store")
builder.set_parallelism(4)

pipeline = builder.build("clinical_nlp_pipeline")
engine   = ExecutionEngine(max_workers=4, retry_on_failure=True)
result   = engine.execute_pipeline(pipeline)

print(f"Clinical pipeline: {result.success}, "
      f"nodes={result.output.get('node_count')}")
```

  </Tab>

  <Tab title="银行业 — 风险/合规">
    合规团队运行一条月度增量流水线：从 sitemap 摄取国际清算银行(BIS)新发布的文件，抽取资本比率和阈值相关实体，追加到已积累三年监管历史的合规知识图谱。增量模式确保只处理自上次运行以来发布的页面。

```python
from semantica.pipeline import PipelineBuilder, ExecutionEngine
from semantica.ingest import ingest_web
from semantica.semantic_extract import NamedEntityRecognizer, TripletExtractor
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore

def ingest_bis_pages(data, **config):
    pages = ingest_web(config["sitemap"], method="sitemap")
    return [
        {"text": p.text, "url": p.url}
        for p in pages
        if p.text.strip() and any(
            kw in p.url.lower() for kw in ["bcbs", "capital", "liquidity"]
        )
    ]

def extract_regulatory_entities(data, **config):
    ner = NamedEntityRecognizer(
        methods=["pattern", "ml"],
        custom_labels=["REGULATION", "CAPITAL_RATIO", "RISK_WEIGHT", "THRESHOLD"],
        confidence_threshold=config.get("confidence_threshold", 0.75),
    )
    extractor = TripletExtractor(
        method="pattern", include_temporal=True, include_provenance=True,
    )
    results = []
    for doc in data:
        entities = ner.extract_entities(doc["text"])
        triplets = extractor.extract_triplets(doc["text"], entities=entities)
        results.append({**doc, "entities": entities, "triplets": triplets})
    return results

def append_to_compliance_graph(data, **config):
    graph = ContextGraph(advanced_analytics=True)
    graph.load_from_file(config["existing_graph"])
    context = AgentContext(
        vector_store    = VectorStore(backend="faiss", dimension=768),
        knowledge_graph = graph,
        retention_days  = 2555,   # 7-year regulatory requirement
    )
    context.store([d["text"] for d in data],
                  extract_entities=True, extract_relationships=True)
    context.save(config["output_path"])
    return {"added_docs": len(data), "graph": graph.stats()}

builder = PipelineBuilder()
builder.register_step_handler("bis_ingest",   ingest_bis_pages)
builder.register_step_handler("rule_extract", extract_regulatory_entities)
builder.register_step_handler("graph_append", append_to_compliance_graph)

builder.add_step("ingest",  "bis_ingest",
                 handler=ingest_bis_pages,
                 sitemap="https://www.bis.org/sitemap.xml",
                 delta_mode=True,
                 base_version_id="2024-11",
                 target_version_id="2024-12")
builder.add_step("extract", "rule_extract", handler=extract_regulatory_entities, confidence_threshold=0.75)
builder.add_step("store",   "graph_append",
                 handler=append_to_compliance_graph,
                 existing_graph="./compliance_graph/knowledge_graph.json",
                 output_path="./compliance_graph/")

builder.connect_steps("ingest",  "extract")
builder.connect_steps("extract", "store")
builder.set_parallelism(4)

pipeline = builder.build("regulatory_pipeline")
engine   = ExecutionEngine(max_workers=4, retry_on_failure=True)
result   = engine.execute_pipeline(pipeline)

print(f"Compliance delta update: {result.output}")
```

  </Tab>
</Tabs>

## 延伸阅读

- [摄取](./ingest.md) — 摄取步骤的全部来源类型：PDF、API、数据库、RSS 订阅源、STIX 目录与数据流
- [语义抽取](./semantic-extraction.md) — 抽取步骤的 NER、关系抽取、三元组抽取与事件检测
- [上下文图](./context-graphs.md) — 构建和查询由存储步骤填充的 `ContextGraph`
- [溯源](./provenance.md) — 为每个抽取出的实体追踪来源文档、置信度分数和流水线运行 ID
