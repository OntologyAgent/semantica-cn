---
title: "流水线模块（Pipeline）"
description: "流水线 DSL：并行 worker、重试策略、失败处理与进度跟踪。"
source: reference/pipeline.md
source_version: 9fe33aab39d6b36ef0ac17fbcddf90f1733672b3
icon: "gear"
---

**`semantica.pipeline`** 把 Semantica 组件串联成**可复现、容错的工作流**：

- 逐步骤失败策略：`skip`、`retry`、`abort` 或 `fallback`
- 经 `ParallelismManager` 并行执行：线程池或进程池
- `PipelineValidator` 在运行前捕获依赖环、缺失 handler 和配置错误
- 预置模板：`"document_processing"`、`"rag_pipeline"`、`"kg_construction"`、`"ontology_generation"`
- 流水线可序列化为 YAML：任意环境保存和重载


## 导出的类

| 类 | 职责 |
| :--- | :--- |
| `PipelineBuilder` | 步骤接线 DSL：`add_step`、`connect_steps`、`set_parallel`、`build` |
| `ExecutionEngine` | 运行已构建的流水线：`execute_pipeline(pipeline, data)` → `ExecutionResult` |
| `ExecutionResult` | `{success, output, metadata, metrics, errors}`：完整的运行摘要 |
| `FailureHandler` | 逐步骤策略：失败时 `skip`、`retry`、`abort` 或 `fallback` |
| `ParallelismManager` | 线程池或进程池并发执行步骤，worker 数可配置 |
| `PipelineValidator` | 运行前捕获依赖环、缺失 handler 和配置错误 |
| `PipelineTemplateManager` | 预置模板：`"document_processing"`、`"rag_pipeline"`、`"kg_construction"`、`"ontology_generation"` |

## 为什么用流水线？

用普通 Python 代码也能把 Semantica 模块串起来。流水线额外提供：

- **重试与失败处理** — 一篇坏文档不会搞垮 10000 篇的批次。
- **并行** — 一个参数即可让抽取跑在多个 worker 上。
- **进度跟踪** — tqdm 控制台进度条，或经 WebSocket 推送到 Explorer。
- **可复现** — 把精确的流水线配置存成 YAML，任何机器都能重放。
- **增量模式(Delta mode)** — 重跑时只处理上次之后有变化的文档。
- **校验** — 在配错的步骤和依赖环导致运行中断之前就捕获它们。

<Note>
  快速脚本和 notebook 用普通模块调用即可。凡是反复运行、大规模运行或生产环境的任务，用流水线。
</Note>

<img src="/assets/img/diagrams/pipeline-flow.svg" alt="Pipeline step sequence: Ingest → Parse → Normalize → Extract → Build KG → QA → Store → Deliver" style={{ width: '100%', borderRadius: '10px', margin: '0 0 24px' }} />

## 快速开始

<Steps>
  <Step title="搭建流水线">
    ```python
    from semantica.pipeline import PipelineBuilder
    from semantica.ingest import FileIngestor
    from semantica.parse import DocumentParser
    from semantica.semantic_extract import NERExtractor
    from semantica.kg import GraphBuilder

    ingestor   = FileIngestor()
    parser     = DocumentParser()
    extractor  = NERExtractor(method="ml")
    kg_builder = GraphBuilder(merge_entities=True)

    builder = PipelineBuilder()
    builder.add_step("ingest",   "file_ingest",    handler=ingestor.ingest_file)
    builder.add_step("parse",    "document_parse", handler=parser.parse)
    builder.add_step("extract",  "ner_extract",    handler=extractor.extract)
    builder.add_step("build_kg", "graph_build",    handler=kg_builder.build)
    builder.connect_steps("ingest", "parse")
    builder.connect_steps("parse",  "extract")
    builder.connect_steps("extract","build_kg")

    pipeline = builder.build("my_pipeline")
    ```
  </Step>
  <Step title="运行前先校验">
    ```python
    from semantica.pipeline import PipelineValidator

    validator = PipelineValidator()
    result = validator.validate_pipeline(pipeline)

    if not result.valid:
        for error in result.errors:   # errors is List[str]
            print(f"Error: {error}")
        for warning in result.warnings:
            print(f"Warning: {warning}")
    ```

    <Tip>
      **生产运行前用 `PipelineValidator`。**它能捕获依赖环、缺失的步骤名和配错的连接——这些问题否则只会在运行中途才暴露。校验是瞬时完成的；等 30 分钟的抽取作业跑完才发现就晚了。
    </Tip>
  </Step>
  <Step title="执行并检查结果">
    ```python
    from semantica.pipeline import ExecutionEngine

    engine = ExecutionEngine()
    result = engine.execute_pipeline(pipeline, data="data/")

    kg = result.output
    print(f"Success:        {result.success}")
    print(f"Steps executed: {result.metrics['steps_executed']}")
    print(f"Steps failed:   {result.metrics['steps_failed']}")
    print(f"Duration:       {result.metrics['execution_time']:.1f}s")
    ```

    <Tip>
      **检查 `result.metrics` 定位瓶颈。**`result.metrics['steps_executed']` 和 `result.metrics['execution_time']` 能快速反映流水线整体健康状况。要看逐步耗时，运行后检查每个 `PipelineStep` 的 `step.result`。
    </Tip>
  </Step>
</Steps>

## 并行处理

在 builder 上设置并行度，并给 `ExecutionEngine` 传 `max_workers`：

```python
from semantica.pipeline import PipelineBuilder, ExecutionEngine

builder = PipelineBuilder()
builder.add_step("ingest",  "file_ingest",    handler=ingestor.ingest_file)
builder.add_step("parse",   "document_parse", handler=parser.parse)
builder.add_step("extract", "ner_extract",    handler=extractor.extract)
builder.add_step("build",   "graph_build",    handler=kg_builder.build)
builder.set_parallelism(4)

pipeline = builder.build("parallel_pipeline")
engine   = ExecutionEngine(max_workers=4)
result   = engine.execute_pipeline(pipeline, data="data/")
```

<Tip>
  **按负载类型设置 `workers=`。**I/O 密集步骤（网页抓取、数据库查询）用线程 worker，CPU 密集步骤（嵌入、OCR、大批量 NER）用进程 worker。池类型与步骤类型错配只会浪费资源，不会提速。
</Tip>

## 重试与错误处理

<Tabs>
  <Tab title="指数退避（推荐）">
    ```python
    from semantica.pipeline import RetryPolicy, RetryStrategy, FailureHandler, ExecutionEngine

    policy = RetryPolicy(
        max_retries=3,
        strategy=RetryStrategy.EXPONENTIAL,
        initial_delay=1.0,    # 1s → 2s → 4s
        backoff_factor=2.0
    )

    handler = FailureHandler()
    handler.set_retry_policy("ner_extract", policy)   # keyed by step_type

    engine = ExecutionEngine(default_max_retries=3, default_backoff_factor=2.0)
    result = engine.execute_pipeline(pipeline, data="data/")
    ```

    最适合瞬态 API 错误和限流：每次重试等得更久，给上游服务恢复的时间。
  </Tab>
  <Tab title="线性退避">
    ```python
    from semantica.pipeline import RetryPolicy, RetryStrategy

    policy = RetryPolicy(
        max_retries=3,
        strategy=RetryStrategy.LINEAR,
        initial_delay=2.0    # 2s → 4s → 6s
    )
    ```

    适用于重试间隔需要可预测增长的场景：例如等待数据库锁释放。
  </Tab>
  <Tab title="固定间隔退避">
    ```python
    from semantica.pipeline import RetryPolicy, RetryStrategy

    policy = RetryPolicy(
        max_retries=5,
        strategy=RetryStrategy.FIXED,
        initial_delay=1.0    # 1s every attempt
    )
    ```

    适用于对固定冷却窗口的服务做重试。
  </Tab>
</Tabs>

### 失败策略

| 策略 | 行为 | 适用场景 |
| :-------- | :--------- | :----------- |
| `"skip"` | 记录失败，继续处理下一篇文档 | 生产环境：一篇坏文档不应拦下 1 万篇 |
| `"stop"` | 立即抛出异常 | 开发环境：尽快暴露错误 |
| `"retry"` | 按 `RetryPolicy` 重试，之后跳过 | 失败大概率是瞬态的时候 |

<Warning>
  生产环境请配置带有限重试次数的 `RetryPolicy`，避免单个失败步骤中断整个运行。执行结束后检查 `result.errors`，找出并重跑失败的文档。
</Warning>

<Warning>
  **生产环境配置重试策略来兜住失败。**用 `handler.set_retry_policy("step_type", RetryPolicy(max_retries=3))` 让瞬态错误被重试而不是中断流水线。运行结束后检查 `result.errors`，找出并重跑重试耗尽的文档。
</Warning>

## 进度跟踪

<Tabs>
  <Tab title="控制台（tqdm）">
    ```python
    from semantica.pipeline import ExecutionEngine

    engine = ExecutionEngine()
    result = engine.execute_pipeline(pipeline, data="data/")
    # The progress tracker outputs tqdm bars to the console during execution
    ```

    Semantica 内置的进度跟踪器会在终端渲染实时进度条。最适合脚本和 CLI 工具。
  </Tab>
  <Tab title="实时状态查询">
    ```python
    from semantica.pipeline import ExecutionEngine
    import threading, time

    engine = ExecutionEngine()

    # Run in a background thread, poll progress from main thread
    def run():
        engine.execute_pipeline(pipeline, data="data/")

    t = threading.Thread(target=run, daemon=True)
    t.start()

    while t.is_alive():
        progress = engine.get_progress(pipeline.name)
        if progress:
            print(f"  {progress['completed_steps']}/{progress['total_steps']} steps: {progress['status']}")
        time.sleep(2)
    ```

    执行期间轮询 `get_progress()` 获取实时状态。
  </Tab>
</Tabs>

## 流水线 DSL

`PipelineBuilder` 用 `add_step(name, type, **config)` 和 `connect_steps(from, to)` 定义 DAG：

```python
from semantica.pipeline import PipelineBuilder, ExecutionEngine

builder = PipelineBuilder()

# Add steps: step_type is a string label, handler is the callable invoked at runtime
builder.add_step("ingest",      "file_ingest",    handler=ingestor.ingest_file)
builder.add_step("parse",       "document_parse", handler=parser.parse)
builder.add_step("normalize",   "text_normalize", handler=normalizer.normalize)
builder.add_step("extract",     "ner_extract",    handler=extractor.extract)
builder.add_step("rel_extract", "rel_extract",    handler=rel_extractor.extract)
builder.add_step("build_kg",    "graph_build",    handler=kg_builder.build)
builder.add_step("deduplicate", "dedup",          handler=deduplicator.deduplicate)
builder.add_step("export",      "rdf_export",     handler=exporter.export, format="turtle", path="output.ttl")

# Wire the data flow
builder.connect_steps("ingest",      "parse")
builder.connect_steps("parse",       "normalize")
builder.connect_steps("normalize",   "extract")
builder.connect_steps("extract",     "rel_extract")
builder.connect_steps("rel_extract", "build_kg")
builder.connect_steps("build_kg",    "deduplicate")
builder.connect_steps("deduplicate", "export")

pipeline = builder.build("full_pipeline")
result   = ExecutionEngine().execute_pipeline(pipeline, data="data/")
```

## 序列化与恢复流水线

`PipelineSerializer` 把流水线转成 JSON 或 dict 存储，之后再重新加载：

```python
from semantica.pipeline import PipelineSerializer

serializer = PipelineSerializer()

# Serialize to JSON string
json_str = serializer.serialize_pipeline(pipeline, format="json")

# Save to file
with open("pipeline_config.json", "w") as f:
    f.write(json_str)

# Restore on any machine and execute
with open("pipeline_config.json") as f:
    restored = serializer.deserialize_pipeline(f.read())

result = ExecutionEngine().execute_pipeline(restored, data="data/")
```

<Tip>
  序列化的流水线会保存步骤名、类型和配置：但不保存 handler 函数（可调用对象无法序列化）。执行前要在恢复出的步骤上重新注册 handler。
</Tip>

## 预置模板

`PipelineTemplateManager` 以正确的步骤顺序接好常见工作流：无需手工连线：

```python
from semantica.pipeline import PipelineTemplateManager

manager = PipelineTemplateManager()
```

`create_pipeline_from_template(name)` 方法返回配置好的 `PipelineBuilder`。对它调用 `.build(pipeline_name)` 即可得到可运行的 `Pipeline`。

- **document_processing** — **摄取 → 解析 → 规范化 → 抽取 → 嵌入 → 构建 KG** — 从摄取到知识图谱的完整文档处理。

  ```python
  builder  = manager.create_pipeline_from_template("document_processing")
  pipeline = builder.build("doc_pipeline")
  ```

- **rag_pipeline** — **摄取 → 分块 → 嵌入 → 存向量** — 面向问答的 RAG 流水线：构建带向量索引的存储。

  ```python
  builder  = manager.create_pipeline_from_template("rag_pipeline")
  pipeline = builder.build("rag_pipeline")
  ```

- **kg_construction** — **摄取 → 抽取实体 → 抽取关系 → 去重 → 消歧 → 建图** — 从多个来源构建知识图谱。

  ```python
  builder  = manager.create_pipeline_from_template("kg_construction")
  pipeline = builder.build("kg_pipeline")
  ```

- **ontology_generation** — **抽取概念 → 推断类 → 推断属性 → 生成 OWL → 校验** — 从抽取数据生成本体。

  ```python
  builder  = manager.create_pipeline_from_template("ontology_generation")
  pipeline = builder.build("ontology_pipeline")
  ```

<Tip>
  **常见模式直接用 `PipelineTemplateManager` 的模板。**`create_pipeline_from_template("kg_construction")` 会按正确顺序接好规范化、去重、冲突检测和建图：避免"先去重后规范化"这类常见错误。
</Tip>

## ExecutionEngine

细粒度控制流水线执行：暂停、恢复、取消和查看实时进度：

```python
from semantica.pipeline import ExecutionEngine

engine = ExecutionEngine(max_workers=4)

# pipeline.name is the pipeline ID used for all control operations
result = engine.execute_pipeline(pipeline, data="data/")

pipeline_id = pipeline.name   # e.g. "my_pipeline"

# Pause after the current step finishes
engine.pause_pipeline(pipeline_id)

progress = engine.get_progress(pipeline_id)
print(f"Completed: {progress['completed_steps']}/{progress['total_steps']}")
print(f"Status: {progress['status']}")

engine.resume_pipeline(pipeline_id)
engine.stop_pipeline(pipeline_id)
```

| 方法 | 返回 | 说明 |
| :------ | :------- | :----------- |
| `execute_pipeline(pipeline, data)` | `ExecutionResult` | 从头到尾执行流水线 |
| `get_pipeline_status(pipeline_id)` | `PipelineStatus` | 当前状态（RUNNING、PAUSED、STOPPED） |
| `get_progress(pipeline_id)` | `Dict` | `completed_steps`、`total_steps`、`progress_percentage`、`status` |
| `pause_pipeline(pipeline_id)` | `None` | 当前步骤完成后挂起 |
| `resume_pipeline(pipeline_id)` | `None` | 从暂停状态恢复 |
| `stop_pipeline(pipeline_id)` | `None` | 立即取消并清理 |

## PipelineValidator

在问题演变成运行中途的失败之前捕获它们：

```python
from semantica.pipeline import PipelineValidator

validator = PipelineValidator()
result    = validator.validate_pipeline(pipeline)

if result.valid:
    print("Pipeline is valid: safe to run")
else:
    for error in result.errors:     # errors is List[str]
        print(f"Error: {error}")
    for warning in result.warnings: # warnings is List[str]
        print(f"Warning: {warning}")
```

检查项：
- **依赖环检测**：A 依赖 B，B 又依赖 A
- **步骤类型校验**：每个步骤类型必须已注册
- **连接完整性**：引用的步骤名必须存在
- **配置完整性**：必填参数必须齐备

## ParallelismManager

<Tabs>
  <Tab title="线程池（I/O 密集）">
    ```python
    from semantica.pipeline import ParallelismManager, Task

    # use_processes=False (default) → thread pool for I/O-bound tasks
    manager = ParallelismManager(max_workers=8, use_processes=False)

    tasks   = [Task(task_id=f"t{i}", handler=ner.extract, args=(text,)) for i, text in enumerate(texts)]
    results = manager.execute_parallel(tasks)
    # returns List[ParallelExecutionResult]

    successes = [r for r in results if r.success]
    failures  = [r for r in results if not r.success]
    ```

    **I/O 密集**步骤用线程池：网页抓取、数据库查询、API 调用。
  </Tab>
  <Tab title="进程池（CPU 密集）">
    ```python
    from semantica.pipeline import ParallelismManager, Task

    # use_processes=True → process pool, bypasses Python GIL
    manager = ParallelismManager(max_workers=4, use_processes=True)

    tasks   = [Task(task_id=f"t{i}", handler=embedder.generate_embeddings, args=(chunk,)) for i, chunk in enumerate(chunks)]
    results = manager.execute_parallel(tasks)
    ```

    **CPU 密集**步骤用进程池：嵌入、OCR、大批量 NER。
  </Tab>
</Tabs>

## ResourceScheduler

防止大规模运行时的内存超额占用：

```python
from semantica.pipeline import ResourceScheduler, ExecutionEngine

scheduler = ResourceScheduler()
engine    = ExecutionEngine()

resources = scheduler.allocate_resources(pipeline)

try:
    result = engine.execute_pipeline(pipeline, data="data/")
finally:
    scheduler.release_resources(resources)
```

## 增量模式

只重跑上次之后有变化的数据：

```python
from semantica.pipeline import PipelineBuilder, ExecutionEngine

builder = PipelineBuilder()

# delta_mode=True tells ExecutionEngine to compute the diff between two snapshots
# and pass only changed triples to this step's handler
builder.add_step(
    "ingest",  "file_ingest",
    handler=ingestor.ingest_file,
    delta_mode=True, base_version_id="v1", target_version_id="v2"
)
builder.add_step(
    "extract", "ner_extract",
    handler=extractor.extract,
    delta_mode=True, base_version_id="v1", target_version_id="v2"
)
builder.add_step(
    "build", "graph_build",
    handler=kg_builder.build,
    delta_mode=False  # always rebuild the merged graph
)
builder.connect_steps("ingest", "extract")
builder.connect_steps("extract", "build")

pipeline = builder.build("delta_pipeline")
engine   = ExecutionEngine()
result   = engine.execute_pipeline(
    pipeline,
    data="data/",
    version_manager=version_manager,   # required for delta mode
    triplet_store=triplet_store        # required for delta mode
)
```

<Note>
  增量检测对源内容做 SHA-256 校验和。只有校验和与 `base_version_id` 不同的源才会传给下游步骤。对每小时或每天对着增长的语料跑一遍的流水线，增量模式免去了冗余的重新嵌入和重新抽取。
</Note>

## SPARQL CONSTRUCT 模板步骤

使用 `"construct_template"` 步骤类型，把 [SPARQL CONSTRUCT 模板](./triplet_store.md#sparql-construct-templates)的渲染和执行纳入流水线。`store_backend` 和 `construct_template_registry` 是执行期资源，不是步骤配置——把它们传给 `execute_pipeline()`，与 `delta_mode` 步骤接收 `version_manager` 和 `triplet_store` 的方式相同：

```python
from semantica.pipeline import PipelineBuilder, ExecutionEngine
from semantica.triplet_store.construct_templates import construct_template_step_handler

builder = PipelineBuilder()
builder.add_step(
    "apply_person_template",
    "construct_template",
    handler=construct_template_step_handler,
    template_name="person_to_foaf",
    params={"subject": "http://ex.org/p1", "name": "Alice", "age": 30},
    target_graph="http://ex.org/graphs/people",
)
pipeline = builder.build("person_pipeline")

engine = ExecutionEngine()
result = engine.execute_pipeline(
    pipeline,
    data=None,
    store_backend=store,                   # required: a BlazegraphStore instance
    construct_template_registry=registry,  # required: holds the registered template
)

triplets = result.output   # List[Triplet], already persisted via store.add_triplets
```

<Note>
  `execute_pipeline()` 的选项里缺 `store_backend` 或 `construct_template_registry` 时，`construct_template` 步骤抛 `ProcessingError`；`template_name` 未注册时抛 `ValidationError`。
</Note>

## 数据结构

<AccordionGroup>
  <Accordion title="ExecutionResult 数据结构">

```python
@dataclass
class ExecutionResult:
    success:  bool            # True if all steps completed without failure
    output:   Any             # output from the final pipeline step
    metadata: Dict[str, Any]  # {"pipeline_id": "...", "execution_time": 1.23}
    metrics:  Dict[str, Any]  # {"steps_executed": 4, "steps_failed": 0, "execution_time": 1.23}
    errors:   List[str]       # error messages from failed steps (empty on full success)

# Access pattern
result.success                       # bool
result.output                        # final step output
result.metadata["pipeline_id"]       # pipeline name used as ID
result.metadata["execution_time"]    # total wall-clock seconds
result.metrics["steps_executed"]     # count of successfully completed steps
result.metrics["steps_failed"]       # count of failed steps
result.errors                        # List[str] of error messages
```

  </Accordion>
  <Accordion title="PipelineStep 数据结构">

```python
@dataclass
class PipelineStep:
    name:              str
    step_type:         str
    config:            Dict[str, Any]
    dependencies:      List[str]          # names of steps this step waits for
    handler:           Optional[Callable]
    status:            StepStatus
    result:            Any
    error:             Optional[Exception]
    delta_mode:        bool               # True = process only changed data
    base_version_id:   Optional[str]     # snapshot ID to diff against
    target_version_id: Optional[str]     # snapshot ID being produced
```

  </Accordion>
  <Accordion title="StepStatus 枚举">

```python
from semantica.pipeline import StepStatus

StepStatus.PENDING    # Not yet started
StepStatus.RUNNING    # Currently executing
StepStatus.COMPLETED  # Finished successfully
StepStatus.FAILED     # Error occurred: check step.error
StepStatus.SKIPPED    # Skipped due to FailureHandler "skip" strategy
```

  </Accordion>
</AccordionGroup>

- [Ingest](./ingest.md) — 大多数流水线的第一步。
- [Semantic Extract](./semantic_extract.md) — 核心抽取步骤。
- [Knowledge Graph](./kg.md) — 建图步骤。
- [Export](./export.md) — 最终输出步骤。
