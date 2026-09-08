---
title: "工具模块（Utils）"
description: "日志、校验、错误处理、进度跟踪与常用操作的共享工具集。"
source: reference/utils.md
source_version: 2386a956155b938905f718f68a1735b7cbd2fc8d
icon: "wrench"
---

**`semantica.utils`** 提供整个 Semantica 使用的**共享基础设施**：

- 结构化日志：`setup_logging()`、`get_logger()`、`log_execution_time` 装饰器
- 校验辅助：`validate_entity()` 与 `validate_config()` 返回 `(bool, Optional[str])`，不抛异常
- 进度跟踪：`ProgressTracker` 类和带 ETA 的 `track_progress()` 可迭代包装器
- 类型化异常：`SemanticaError`、`ValidationError`、`ProcessingError`、`ConfigurationError`、`QualityError`

大多数用户不会直接调用 utils：它是所有模块的**共享地基**。


## 导出的类与函数

| 名称 | 类型 | 职责 |
| :--- | :--- | :--- |
| `setup_logging` | function | 配置 `semantica` 根 logger：接受 `level`、`file`、`console`、`rotation` 关键字参数 |
| `get_logger` | function | 获取具名 logger 实例（`semantica.<name>`） |
| `log_execution_time` | decorator | 包装函数：记录函数名、执行时间与成功/失败 |
| `log_performance` | function | 记录已采集的性能指标：`log_performance(func_name, execution_time, **metrics)` |
| `validate_entity` | function | 校验实体 dict：返回 `(bool, Optional[str])`；不抛异常 |
| `validate_config` | function | 校验配置 dict：返回 `(bool, Optional[str])`；不抛异常 |
| `ProgressTracker` | class | 类形式的进度跟踪器，带 ETA 与步骤回调 |
| `track_progress` | function | 给任意可迭代对象包一层实时进度条 |
| `clean_text` | function | 规范化空白字符并去除零宽控制字符 |
| `hash_data` | function | 对 `str`、`bytes` 或 `dict` 计算确定性 SHA-256 哈希 |
| `SemanticaError` | exception | 所有 Semantica 错误的基类异常 |
| `ValidationError` | exception | 输入未通过校验时抛出；带 `.field`、`.value`、`.message` |
| `ProcessingError` | exception | 抽取、建图或流水线步骤中抛出；带 `.stage` |
| `ConfigurationError` | exception | 配置校验失败时抛出 |
| `QualityError` | exception | 数据质量低于阈值时抛出 |

## 你能得到什么

- **日志** — 通过 `@log_execution_time` 装饰器做结构化日志，用环境变量控制质量指标。
- **校验** — `validate_entity` 与 `validate_config` 配合携带字段和值上下文的类型化 `ValidationError`。
- **进度跟踪** — `track_progress` 包装任意可迭代对象：自动探测控制台与 Jupyter，选择合适的渲染器。
- **辅助函数** — `clean_text`、`hash_data`、`safe_filename` 以及全框架使用的嵌套 dict 工具。
- **异常层次** — `SemanticaError` → `ValidationError`、`ProcessingError`：类型化异常支持针对性恢复。
- **文件工具** — `read_json_file` 失败时抛 `FileNotFoundError` 或 `json.JSONDecodeError`：JSON 读写不用再包样板 try/except。

## 日志

<Steps>
  <Step title="应用启动时初始化日志">
    ```python
    from semantica.utils import setup_logging, get_logger

    setup_logging(level="INFO")   # "DEBUG" | "INFO" | "WARNING" | "ERROR"
    logger = get_logger(__name__)
    ```

    <Warning>
      **应用启动时调用一次 `setup_logging(level="INFO")`。** 不调用的话，Semantica 会退回到 Python 根 logger，可能是静默的或配置不当的。在导入其他 Semantica 模块之前调用它，才能捕获初始化日志。
    </Warning>
  </Step>
  <Step title="用性能装饰器测量耗时函数">
    ```python
    from semantica.utils import log_execution_time

    @log_execution_time
    def expensive_step(data):
        ...
    # Logs: "expensive_step completed in 2.34s"
    ```

    <Tip>
      **`@log_execution_time` 是性能装饰器。** 加到任意函数上即可自动记录函数名、执行时间与成功/失败。`log_performance` 是更底层的函数，用于记录你已经采集好的指标：它不是装饰器。
    </Tip>
  </Step>
  <Step title="通过环境变量配置">
    ```bash
    export SEMANTICA_LOG_LEVEL=DEBUG
    export SEMANTICA_LOG_FORMAT=json     # "json" | "text"
    export SEMANTICA_DISABLE_PROGRESS=true
    export SEMANTICA_FORCE_PROGRESS=true
    ```

    <Tip>
      **进度条跟随终端。** 只有 stdout 是交互式终端（或 Jupyter notebook）时才渲染控制台进度，
      因此管道或重定向输出不会再把日志填满进度条和转义序列。设置 `SEMANTICA_DISABLE_PROGRESS`
      可以即使在终端里也关闭进度显示；设置 `SEMANTICA_FORCE_PROGRESS` 可以在 stdout 被重定向时保留进度条。
      两者同时设置时 `SEMANTICA_DISABLE_PROGRESS` 优先。
    </Tip>
  </Step>
</Steps>

## 校验

```python
from semantica.utils import validate_entity, validate_config, ValidationError

# validate_entity returns (is_valid, error_message)
is_valid, error = validate_entity({"id": "1", "type": "PERSON", "text": "Alice"})
if not is_valid:
    raise ValidationError(error)

# validate_config returns (is_valid, error_message)
is_valid, error = validate_config(config, required_keys=["model", "provider"])
if not is_valid:
    print(f"Invalid config: {error}")
```

| 函数 | 说明 | 返回 |
| :-------- | :----------- | :------- |
| `validate_entity(data)` | 检查实体 dict 是否含**必需**字段（`id`、`text`、`type`）且类型正确 | `Tuple[bool, Optional[str]]` |
| `validate_config(cfg, required_keys=None)` | 检查配置 dict；可选地强制**必需**键 | `Tuple[bool, Optional[str]]` |

## 进度跟踪

```python
from semantica.utils import track_progress

# Wraps any iterable: auto-detects console vs Jupyter
for item in track_progress(items, desc="Processing documents"):
    process(item)
```

支持：

- **控制台**：带 ETA 的 tqdm 进度条
- **Jupyter**：notebook 兼容组件（自动探测）
- **文件**：把进度写入日志文件

<Tip>
  **`track_progress` 自动探测 Jupyter。** 在终端里渲染 tqdm 进度条；在 Jupyter notebook 里渲染交互组件。你不需要探测环境：同一个调用在两边都能用。
</Tip>

## 辅助函数

```python
from semantica.utils import clean_text, hash_data, safe_filename

# Normalize whitespace and strip control characters
clean = clean_text("  Hello   World  ")     # -> "Hello World"

# Deterministic SHA-256 hash of a string, bytes, or dict
uid   = hash_data({"key": "value"})         # -> hex digest string

# Sanitize a string for use as a filename
fname = safe_filename("My File?.txt")       # -> "My_File.txt"
```

<Tip>
  **`hash_data()` 跨运行确定。** 相同的输入 dict（任何可 JSON 序列化的对象），`hash_data()` 总是返回相同的 SHA-256 十六进制串：适合在流水线步骤中作为缓存键或幂等令牌。
</Tip>

## 嵌套 Dict 工具

用于深层配置读写的辅助函数：在 `Config` 与 `ConfigManager` 内部大量使用：

```python
from semantica.utils import get_nested_value, set_nested_value, merge_dicts

config = {
    "processing": {"batch_size": 32, "max_workers": 4},
    "llm":        {"provider": "groq", "model": "llama-3.3-70b-versatile"},
}

# Dot-notation read: returns default if key path is absent
batch = get_nested_value(config, "processing.batch_size", default=16)
# -> 32

# Dot-notation write
set_nested_value(config, "processing.batch_size", 64)

# Deep merge: nested keys are merged recursively (deep=True by default)
base      = {"a": {"x": 1, "y": 2}, "b": 3}
overrides = {"a": {"y": 99, "z": 4}, "c": 5}
merged    = merge_dicts(base, overrides)
# -> {"a": {"x": 1, "y": 99, "z": 4}, "b": 3, "c": 5}
```

## 异常层次

<AccordionGroup>
  <Accordion title="异常类型及其抛出时机">

```python
from semantica.utils import SemanticaError, ValidationError, ProcessingError

try:
    run_pipeline(data)
except ValidationError as e:
    # Input data did not pass schema validation
    logger.error("Validation failed: %s", e.message)
except ProcessingError as e:
    # Failure during extraction or graph construction
    logger.error("Processing failed at stage %s: %s", e.stage, e)
except SemanticaError as e:
    # Catch-all for all Semantica framework errors
    logger.error("Framework error: %s", e)
```

| 异常 | 抛出时机 | 关键属性 |
| :--------- | :----------- | :-------------- |
| `SemanticaError` | 基类：所有框架错误都继承自它 | `.message`、`.context`、`.error_code` |
| `ValidationError` | 输入数据未通过模式或类型校验 | `.field`、`.value`、`.constraint` |
| `ProcessingError` | 抽取、建图或流水线步骤中失败 | `.stage`、`.input_data`、`.output_data` |
| `ConfigurationError` | 配置键缺失或类型错误 | `.config_key`、`.config_value`、`.expected_type` |
| `QualityError` | 数据质量分低于阈值 | `.quality_score`、`.threshold`、`.metrics` |

  </Accordion>
</AccordionGroup>

<Tip>
  **把 `SemanticaError` 当作最宽的异常网。** 所有框架错误都继承自 `SemanticaError`，所以 `except SemanticaError` 能捕获校验失败、处理错误以及中间的一切。需要针对性恢复逻辑时再用具体子类。
</Tip>

## 文件工具

```python
from semantica.utils import read_json_file

# Read and parse a JSON file: raises FileNotFoundError or json.JSONDecodeError on failure
config = read_json_file("config.json")
```

- [Core](./core.md) — 内部使用 Utils 的框架编排层。
- [Pipeline](./pipeline.md) — 用 ProgressTracker 做每步跟踪。
