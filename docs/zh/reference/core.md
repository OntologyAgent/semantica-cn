---
title: "核心模块（Core）"
description: "框架编排、生命周期管理、配置与插件系统。"
source: reference/core.md
source_version: f2cbd864bfa6493680a1740f28976e0bf2217a93
icon: "gear"
---

**`semantica.core`** 是框架的**协调层**：

- `Semantica` 编排器从一份 YAML 配置协调完整的知识图谱(KG)构建流水线
- `ConfigManager` 加载 YAML 配置，支持深度合并、校验和环境变量覆盖
- `PluginRegistry` 支持在运行时动态注册和加载组件
- `LifecycleManager` 管理启动/关闭，带健康监测和生命周期钩子

<Tip>
  绝大多数用例直接用各个模块即可。只有需要应用级生命周期管理、集中式配置或插件系统时，才用到 `semantica.core`。
</Tip>


## 你能得到什么

- **Semantica** — 高层编排器：从单个 `config.yaml` 协调完整的 KG 构建流水线。应用级部署的入口。
- **ConfigManager** — YAML 配置支持深度合并、`SEMANTICA_` 环境变量覆盖和点号嵌套键访问。让密钥远离源码文件。
- **LifecycleManager** — 有序的启动/关闭钩子、健康监测和 6 状态机。FastAPI 应用这类长运行服务的必备品。
- **PluginRegistry** — 注册自定义摄取器、解析器、导出器或任意组件。运行时按名称加载：无需 import。

## 导出的类

| 类 | 职责 |
| :--- | :--- |
| `Semantica` | 编排入口：协调完整的 KG 构建流水线 |
| `ConfigManager` | YAML 配置加载、深度合并、校验与环境变量覆盖 |
| `LifecycleManager` | 启动/关闭状态机，带健康监测与生命周期钩子 |
| `PluginRegistry` | 插件的动态发现、注册与加载 |
| `method_registry` | 全局 `MethodRegistry` 实例：注册并分发自定义编排方法 |


## Semantica（编排）

**`Semantica`** 是协调**完整 KG 构建流水线**的高层入口：

```python
from semantica.core import Semantica, ConfigManager

config_manager = ConfigManager()
config = config_manager.load_from_file("config.yaml")

framework = Semantica(config=config)
framework.initialize()

try:
    result = framework.build_knowledge_base(
        sources=["doc1.pdf", "doc2.docx"],
        embeddings=True,
        graph=True,
    )
    status = framework.get_status()
    print(f"State: {status['state']}")
finally:
    framework.shutdown(graceful=True)
```

### 核心方法

| 方法 | 说明 |
| :------ | :----------- |
| `initialize()` | 初始化所有框架组件 |
| `build_knowledge_base(sources, **kwargs)` | 协调完整的 KG 构建流水线 |
| `run_pipeline(pipeline, data)` | 执行已有的 `Pipeline` 实例 |
| `get_status()` | 返回系统健康状态与当前状态 |
| `shutdown(graceful=True)` | 优雅关闭：等待进行中的操作完成 |

## ConfigManager

集中式配置加载，带深度合并和环境变量覆盖：

```python
from semantica.core import ConfigManager

manager = ConfigManager()
config = manager.load_from_file("config.yaml")

# Merge base config with environment-specific overrides
merged = manager.merge_configs(
    manager.load_from_file("base.yaml"),
    manager.load_from_file("prod.yaml"),
)

# Nested key access with dot notation
batch_size = config.get("processing.batch_size", default=16)
config.set("processing.batch_size", 64)
config.validate()
```

### YAML 配置

```yaml
llm_provider:
  name: openai
  model: gpt-4o
  # Do not put API keys in YAML: use environment variables instead.
  # ConfigManager loads YAML with yaml.safe_load(), which does not
  # interpolate ${...} expressions. Set secrets via env vars (see below).

processing:
  batch_size: 32
  max_workers: 4

quality:
  min_confidence: 0.7

logging:
  level: INFO
```

环境变量覆盖（前缀 `SEMANTICA_`）：

用双下划线（`__`）生成嵌套键访问所需的点分隔符。实现会去掉 `SEMANTICA_` 前缀、把结果转为小写，再把 `__` 替换成 `.`，最后对配置 dict 调用 `set_nested_value()`。

```bash
# Double underscores map to nested keys:
export SEMANTICA_LLM_PROVIDER__MODEL=gpt-4o
export SEMANTICA_LLM_PROVIDER__NAME=openai
export SEMANTICA_PROCESSING__BATCH_SIZE=64
export SEMANTICA_QUALITY__MIN_CONFIDENCE=0.8
export SEMANTICA_LOGGING__LEVEL=DEBUG
```

## LifecycleManager

用确定的状态机和有序的启动/关闭钩子管理框架状态：

**状态机：** `UNINITIALIZED` → `INITIALIZING` → `READY` → `RUNNING` → `STOPPING` → `STOPPED`

```python
from semantica.core import LifecycleManager

manager = LifecycleManager()

def init_db():
    print("Initializing database...")

def cleanup_db():
    print("Closing database connections...")

# Lower priority values run first during startup
# Higher priority values run first during shutdown
manager.register_startup_hook(init_db,     priority=10)
manager.register_shutdown_hook(cleanup_db, priority=10)

manager.startup()

# Component health monitoring
class DatabaseComponent:
    def health_check(self):
        return {"healthy": True, "message": "Connected"}

manager.register_component("database", DatabaseComponent())
summary = manager.get_health_summary()
# → {
#     "state": "ready",
#     "is_healthy": True,
#     "total_components": 1,
#     "healthy_components": 1,
#     "unhealthy_components": 0,
#     "last_check": 1234567890.0,
#     "components": {
#         "database": {"healthy": True, "message": "Connected", "timestamp": ...}
#     }
#   }

manager.shutdown(graceful=True)
```

## PluginRegistry

注册参与完整流水线的自定义组件：自动获得溯源跟踪、重试策略和并行执行：

```python
from semantica.core import PluginRegistry

class MyPlugin:
    def initialize(self):
        print("Plugin initialized")

    def execute(self, data):
        return {"processed": True}

registry = PluginRegistry(plugin_paths=["./plugins"])
registry.register_plugin("my_plugin", MyPlugin, version="1.0.0")

plugin = registry.load_plugin("my_plugin", api_key="xxx")
result = plugin.execute("sample data")

for info in registry.list_plugins():
    print(f"{info['name']}: {info['version']}")
```

## MethodRegistry

注册自定义编排方法，按名称分发：

```python
from semantica.core import method_registry
from semantica.core.methods import build_knowledge_base

def fast_kb_builder(sources, **kwargs):
    # Custom logic: skip embeddings for speed
    ...

method_registry.register("knowledge_base", "fast", fast_kb_builder)

result = build_knowledge_base(sources=["doc.pdf"], method="fast")
```

## 何时用 Core、何时用单个模块

| 场景 | 推荐做法 |
| :-------- | :-------------------- |
| 单次抽取任务 | `from semantica.semantic_extract import NERExtractor` |
| 构建知识图谱 | `from semantica.kg import GraphBuilder` |
| 多步骤流水线 | `from semantica.pipeline import Pipeline` |
| 应用级生命周期 + 配置 | `from semantica.core import Semantica, ConfigManager` |
| 自定义分发 / 插件 | `from semantica.core import method_registry, PluginRegistry` |

<Tip>
  只有在构建长运行应用（如 FastAPI 服务）——需要有序启动、健康检查和优雅关闭——时才用 `Semantica` 和 `LifecycleManager`。脚本和 notebook 直接用各个模块即可。
</Tip>

- [Pipeline](../../reference/pipeline.md) — 流水线执行与步骤编排。
- [Utils](./utils.md) — Core 内部使用的共享工具集。
- [入门指南](../getting-started.md) — 使用 Core 前先了解基础。
- [LLMs](../../reference/llms.md) — 通过 ConfigManager 配置大语言模型(LLM)提供商。
