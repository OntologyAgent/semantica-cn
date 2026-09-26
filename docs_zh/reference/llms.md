---
title: "LLM 模块（LLMs）"
description: "生成式大语言模型(LLM)提供商，外加 TypeSafe Jev 类型化决策。"
source: reference/llms.md
source_version: acf7d04c7de58c432d5b86f18f8a95c0e0dd9ee3
icon: "microchip"
---

**`semantica.llms`** 为各大主流大语言模型(LLM)提供商提供统一的生成式 API，并为 TypeSafe Jev 提供一套独立的类型化决策(typed decision) API：

- 生成式提供商都是抽取器、推理器和智能体中 `llm_provider=` 参数的直接替代品
- `LiteLLM` 用一个类加模型字符串前缀，路由到 100+ 提供商
- `HuggingFaceLLM` 完全本地运行：无需 API key、无需网络请求
- 经 `generate_typed()` 输出结构化结果，按 schema 校验抽取内容
- `Jev` 与 `AsyncJev` 返回 Choice、Noul 或 Score 决策，不会伪装成文本生成
- 支持流式输出、工具调用和批量推理的 `generate_batch()`


## 导出的类

```python
from semantica.llms import (
    AsyncJev,
    Groq,
    HuggingFaceLLM,
    Jev,
    JevDecisionResult,
    LiteLLM,
    OpenAI,
)
```

| 类 | 提供商 | 需要 API Key |
| :----- | :-------- | :---------------- |
| `Groq` | Groq Cloud | `GROQ_API_KEY` |
| `OpenAI` | OpenAI / 任意 OpenAI 兼容网关 | `OPENAI_API_KEY` |
| `LiteLLM` | 经 LiteLLM 路由的 100+ 提供商 | 取决于模型 |
| `HuggingFaceLLM` | 本地 HuggingFace Transformers | 无（本地） |
| `Jev` | TypeSafe System One，同步 | `TYPESAFE_API_KEY` |
| `AsyncJev` | TypeSafe System One，异步 | `TYPESAFE_API_KEY` |

<Tip>
  **Anthropic、Gemini、Ollama、DeepSeek、Azure、Bedrock、Cohere 以及 90+ 其他提供商**都可以经 `LiteLLM` 用各自模型字符串前缀访问。见下文 [LiteLLM 一节](#litellm-100+-providers)。
</Tip>

## 你能得到什么

- **统一的 `LLMProvider` 接口**：一行代码切换提供商，不改应用代码
- **`LiteLLM`**：一个类经模型字符串路由到 100+ 提供商
- **本地模型**：`HuggingFaceLLM` 完全本地运行，无需 API key
- **类型化决策**：`Jev` 支持有界的 Choice、Noul、Score 决策，附带概率元数据
- **流式输出**：逐 token 输出，低延迟体验
- **自定义网关**：用 `base_url` 把 `OpenAI` 指向任意 OpenAI 兼容端点

## 选择提供商

<Tabs>
  <Tab title="Groq：快速上手">
    有免费额度，推理速度最快，几乎零配置。最适合开发和高吞吐抽取流水线。

    | | |
    | :-- | :-- |
    | **速度** | 非常快：100+ tok/s |
    | **成本** | 有免费额度 |
    | **上下文** | 128k |
    | **最适合** | 开发、高吞吐抽取 |

    ```python
    import os
    from semantica.llms import Groq

    llm = Groq(
        model="llama-3.1-8b-instant",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.0,
    )
    ```

    在 [console.groq.com](https://console.groq.com) 免费领取 key。
  </Tab>
  <Tab title="OpenAI：生产环境">
    准确率最高，JSON 模式和函数调用最稳。抽取质量攸关的生产流水线用它。

    | | |
    | :-- | :-- |
    | **速度** | 快 |
    | **成本** | 中 |
    | **上下文** | 128k |
    | **最适合** | 生产级质量、JSON 抽取、函数调用 |

    ```python
    import os
    from semantica.llms import OpenAI

    llm = OpenAI(
        model="gpt-4o",
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.0,
        max_tokens=4096,
    )
    ```
  </Tab>
  <Tab title="Ollama：本地/隔离环境">
    完全本地部署：无需 API key，数据不出你的基础设施。气隙(air-gapped)部署必选。

    | | |
    | :-- | :-- |
    | **速度** | 中（取决于硬件） |
    | **成本** | 免费（只有本地算力） |
    | **上下文** | 因模型而异 |
    | **最适合** | 隐私、隔离环境、自定义微调模型 |

    ```bash
    # Install Ollama and pull a model first
    ollama pull llama3.2:3b
    ```

    ```python
    from semantica.llms import LiteLLM

    llm = LiteLLM(
        model="ollama/llama3.2:3b",
        api_base="http://localhost:11434",  # Ollama default port
    )
    ```

    <Note>
      无需 API key。创建 `LiteLLM` 实例前先确认 Ollama 服务已启动（`ollama serve`）。
    </Note>
  </Tab>
  <Tab title="Claude：复杂推理">
    最大上下文窗口，最强的多跳推理，最高的安全底线。复杂分析和长文档抽取用它。

    | | |
    | :-- | :-- |
    | **速度** | 快 |
    | **成本** | 中 |
    | **上下文** | 200k |
    | **最适合** | 复杂推理、长文档、安全攸关的输出 |

    ```python
    import os
    from semantica.llms import LiteLLM

    llm = LiteLLM(
        model="anthropic/claude-sonnet-5",
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        temperature=0.0,
    )
    ```
  </Tab>
  <Tab title="DeepSeek：成本优化">
    大批量负载下单 token 成本最低。编码和结构化数据抽取能力扎实。

    | | |
    | :-- | :-- |
    | **速度** | 快 |
    | **成本** | 极低 |
    | **上下文** | 64k |
    | **最适合** | 高吞吐流水线、编码任务、预算敏感负载 |

    ```python
    import os
    from semantica.llms import LiteLLM

    llm = LiteLLM(
        model="deepseek/deepseek-chat",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        temperature=0.0,
    )
    ```
  </Tab>
  <Tab title="Jev：类型化决策">
    只做决策的推理，适用于有界的路由、分类、二元判断和打分。需要生成文本或多步推理时，请改用生成式提供商。

    | | |
    | :-- | :-- |
    | **速度** | 非常快 |
    | **输出** | Choice、Noul 或 Score |
    | **接口** | `decide()`；不是 `generate()` |
    | **最适合** | 带置信度门控的应用决策 |

    ```python
    from semantica.llms import Jev

    decider = Jev()  # reads TYPESAFE_API_KEY
    result = decider.decide(
        state={"risk_score": 0.62},
        question="How should this case be routed?",
        kind="choice",
        choices=["approve", "escalate"],
    )
    ```
  </Tab>
</Tabs>

## API Key 配置

### 环境变量（推荐）

```bash
# Add to your shell profile (.bashrc, .zshrc, etc.)
export GROQ_API_KEY="your_groq_api_key_here"
export OPENAI_API_KEY="your_openai_api_key_here"
export ANTHROPIC_API_KEY="your_anthropic_api_key_here"
export TYPESAFE_API_KEY="your_typesafe_api_key_here"

# Reload your shell
source ~/.bashrc
```

### 配置文件方式

```yaml
# config.yaml
llm_provider:
  name: groq
  model: llama-3.1-8b-instant
  temperature: 0.0
# Set GROQ_API_KEY environment variable and pass to constructor
```

### 代码方式配置

```python
import os
from semantica.llms import Groq, LiteLLM

# Method 1: Direct API key
llm = Groq(api_key="your-api-key-here", model="llama-3.1-8b-instant")

# Method 2: Environment variable (preferred)
llm = Groq(api_key=os.getenv("GROQ_API_KEY"), model="llama-3.1-8b-instant")

# Method 3: Multiple providers via LiteLLM
providers = {
    "fast": LiteLLM(model="groq/llama-3.1-8b-instant", api_key=os.getenv("GROQ_API_KEY")),
    "smart": LiteLLM(model="anthropic/claude-sonnet-5", api_key=os.getenv("ANTHROPIC_API_KEY"))
}
```

### 安全最佳实践

<Warning>
不要把 API key 提交进版本控制。用环境变量或安全的密钥管理服务。
</Warning>

```python
# ❌ Bad - API key in code
llm = Groq(api_key="gsk_abc123...", model="llama-3.1-8b-instant")

# ✅ Good - Environment variable
llm = Groq(api_key=os.getenv("GROQ_API_KEY"), model="llama-3.1-8b-instant")
```

## TypeSafe Jev

`Jev` 与 `AsyncJev` 封装官方 `typesafe-sdk` 的 System One 客户端，是仅决策(decision-only)的提供商：两个类都不实现 `generate()`、`generate_structured()` 或 `generate_typed()`，也都不能作为 `llm_provider=` 参数传给生成式抽取器或推理器。

<Warning>
  Jev 目前处于实验性的抢先体验阶段。`llm-typesafe` extra 当前支持经过审阅的 TypeSafe SDK 0.7 API，要求 Python 3.10 或更高版本。由于该 SDK 是可选依赖且带保护性导入，Semantica 基础安装仍然兼容 Python 3.9。
</Warning>

<Warning>
  TypeSafe SDK 0.7 会在 `DEBUG` 级别经 `typesafe_sdk` logger 输出完整的请求与响应体；授权头会做脱敏，但应用传入的 `state` 不会。当 `state` 可能包含敏感信息时，即使根 logger 用的是 `DEBUG`，也要把这个 logger 保持在 `INFO` 或更高级别。
</Warning>

```python
import logging

logging.getLogger("typesafe_sdk").setLevel(logging.INFO)
```

```bash
pip install "semantica[llm-typesafe]"
```

### 构造参数

```python
Jev(
    model="jev-latest",
    api_key=None,
    client=None,
    **client_options,
)

AsyncJev(
    model="jev-latest",
    api_key=None,
    client=None,
    **client_options,
)
```

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `model` | `str` | TypeSafe 模型名或别名，默认 `jev-latest`。结果中保留的是服务实际返回的具体模型。 |
| `api_key` | `Optional[str]` | API key。省略时 SDK 读取 `TYPESAFE_API_KEY`。 |
| `client` | 兼容客户端或 `None` | 可选注入的 `TypeSafeClient`/`AsyncTypeSafeClient`，便于自定义传输层和测试。注入的客户端仍归调用方所有。 |
| `**client_options` | `Any` | 透传给 SDK 客户端构造函数，例如 `retry`、`timeout`、`headers`、`transport`、`base_url`。 |

### 方法

| 方法 | 返回 | 说明 |
| :--- | :--- | :--- |
| `decide(state, question, kind, *, choices=None, criteria=None, **request_options)` | `JevDecisionResult` | 做一次 Choice、Noul 或 Score 决策。`AsyncJev.decide()` 需要 await。 |
| `is_available()` | `bool` | 在本地检查是否存在注入的客户端，或 SDK 与已配置的 API key 是否齐备。它不校验 key，也不发起网络请求。 |
| `close()` | `None` | 关闭 `Jev` 自建的同步客户端；注入的客户端不会被关闭。 |
| `aclose()` | `None` | `AsyncJev` 的异步等价方法。 |

`state` 接受字符串、映射或列表。`question` 是针对该状态求值的指令。按 `kind` 的输入要求：

- `kind="choice"`：`choices` 传标签序列，或“标签 → 描述”的映射。`criteria=` 可作为等价的显式写法传入；两者不要同时传。
- `kind="noul"`：可选传入 `criteria={"true": ..., "false": ...}`。
- `kind="score"`：`criteria` 传按序排列的评分量规等级，从 0 分开始。

其余请求选项会转发给 `system_one()`，例如单次调用的 `model`、`retry`、`timeout`、`extra_headers` 或 `extra_body`。

```python
from semantica.llms import Jev

jev = Jev()  # TYPESAFE_API_KEY
result = jev.decide(
    state={"ticket": "Charged twice; please refund this today."},
    question="Which queue should handle this ticket?",
    kind="choice",
    choices={
        "billing": "Charges, invoices, or refunds",
        "technical": "Product or integration failures",
        "other": None,
    },
)
```

### `JevDecisionResult`

| 字段 | 类型 | 说明 |
| :--- | :--- | :--- |
| `kind` | `Literal["choice", "noul", "score"]` | 本次决策使用的原语。 |
| `value` | `Union[str, bool, float]` | 选中的标签、Noul 在 0.5 边界上的布尔值，或期望得分。 |
| `probability` | `Optional[float]` | Choice 为选中标签的概率，Noul 为 yes 的原始概率，Score 为 `None`。 |
| `confidence` | `float` | Choice/Score 取 SDK 置信度；Noul 取 `abs(2p - 1)` 的路由确定性。 |
| `probabilities` | `dict` | 完整的 Choice 或 Score 概率分布；Noul 为空。 |
| `model` | `str` | TypeSafe 上报的具体模型。 |
| `request_id` | `Optional[str]` | API 返回时的请求 ID。 |
| `usage` | `dict` | 上报的输入/输出 token 用量。 |
| `legend` | `dict[int, Any]` | 评分等级量规；Choice 与 Noul 为空。 |

`result.to_dict()` 返回可序列化的副本，适合放进 Semantica 的决策元数据或 `cross_system_context`。它特意把 Noul 的原始概率与派生的置信度分开保留。

```python
from semantica.llms import AsyncJev

async with AsyncJev() as jev:
    result = await jev.decide(
        state="The message asks for an immediate duplicate-charge refund.",
        question="Does the message explicitly communicate urgency?",
        kind="noul",
    )
```

## 提供商

<CodeGroup>

```python Groq
import os
from semantica.llms import Groq

llm = Groq(
    model="llama-3.3-70b-versatile",   # recommended; implementation default: llama-3.1-8b-instant
    api_key=os.getenv("GROQ_API_KEY"),
    max_tokens=64000,
    temperature=0.0,
)
# **Best for:** high-throughput extraction, fast inference at low cost
```

```python OpenAI
import os
from semantica.llms import OpenAI

llm = OpenAI(
    model="gpt-4o",                     # recommended; implementation default: gpt-3.5-turbo
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.0,
)
# **Best for:** general purpose, function calling, JSON mode
```

```python LiteLLM (100+ providers)
import os
from semantica.llms import LiteLLM

# pip install "semantica[llm-litellm]"

# Anthropic Claude
llm = LiteLLM(model="anthropic/claude-opus-4-7",         api_key=os.getenv("ANTHROPIC_API_KEY"))

# Google Gemini
llm = LiteLLM(model="gemini/gemini-1.5-pro",             api_key=os.getenv("GOOGLE_API_KEY"))

# Ollama (local: no API key)
llm = LiteLLM(model="ollama/llama3.2:3b",                api_base="http://localhost:11434")

# DeepSeek
llm = LiteLLM(model="deepseek/deepseek-chat",            api_key=os.getenv("DEEPSEEK_API_KEY"))

# Azure OpenAI
llm = LiteLLM(model="azure/gpt-4o",                      api_key=os.getenv("AZURE_API_KEY"))

# AWS Bedrock
llm = LiteLLM(model="bedrock/anthropic.claude-sonnet-4-5-20250929-v1:0")

# Novita AI
llm = LiteLLM(model="novita/deepseek/deepseek-v3.2",     api_key=os.getenv("NOVITA_API_KEY"))
```

```python HuggingFaceLLM (Local)
from semantica.llms import HuggingFaceLLM

llm = HuggingFaceLLM(
    model="mistralai/Mistral-7B-Instruct-v0.3",
    device="cuda",           # "cpu" | "cuda" | "mps"
    max_new_tokens=512,
    temperature=0.1,
)
# Bring your own model: full local control, no API key
```

```python TypeSafe Jev (Decision-only)
from semantica.llms import Jev

decider = Jev(model="jev-latest")  # reads TYPESAFE_API_KEY
result = decider.decide(
    state={"risk_score": 0.62},
    question="How should this case be routed?",
    kind="choice",
    choices=["approve", "escalate"],
)
# Best for typed, confidence-gated application decisions; no text generation
```

</CodeGroup>

## LiteLLM：100+ 提供商

对 `semantica.llms` 没有直接导出的提供商，推荐经 `LiteLLM` 访问。也就是说，只要给出 `provider/model` 格式的模型字符串，`LiteLLM` 就会把它路由到对应服务商：

```python
import os
from semantica.llms import LiteLLM

# Pattern: LiteLLM(model="<provider>/<model-name>")
providers = {
    "Anthropic":  LiteLLM(model="anthropic/claude-opus-4-7",       api_key=os.getenv("ANTHROPIC_API_KEY")),
    "Gemini":     LiteLLM(model="gemini/gemini-1.5-pro",            api_key=os.getenv("GOOGLE_API_KEY")),
    "Ollama":     LiteLLM(model="ollama/llama3.2:3b",               api_base="http://localhost:11434"),
    "DeepSeek":   LiteLLM(model="deepseek/deepseek-chat",           api_key=os.getenv("DEEPSEEK_API_KEY")),
    "Azure":      LiteLLM(model="azure/gpt-4o",                     api_key=os.getenv("AZURE_API_KEY")),
    "Bedrock":    LiteLLM(model="bedrock/anthropic.claude-sonnet-4-5-20250929-v1:0"),
    "Cohere":     LiteLLM(model="cohere/command-r-plus",            api_key=os.getenv("COHERE_API_KEY")),
    "Novita AI":  LiteLLM(model="novita/deepseek/deepseek-v3.2",    api_key=os.getenv("NOVITA_API_KEY")),
}

# Every LiteLLM instance implements the same .generate() interface
response = providers["Anthropic"].generate("Explain GraphRAG in one paragraph.")
```

<Note>
  LiteLLM 支持的完整模型字符串列表见 [docs.litellm.ai/docs/providers](https://docs.litellm.ai/docs/providers)。使用上面展示的 `provider/model` 格式。
</Note>

## 自定义/企业网关

任意 OpenAI 兼容端点：内部路由层、Qwen 代理或私有 LLaMA 部署：

```python
import os
from semantica.llms import OpenAI

llm = OpenAI(
    model="qwen2.5-72b",
    api_key=os.getenv("GATEWAY_API_KEY"),
    base_url="https://my-internal-gateway.company.com/v1",
)
```

<Note>
  `base_url` 在构造时校验。非 HTTP(S) 协议会抛 `ValueError`，以防服务端请求伪造(SSRF)攻击（v0.5.0 修复）。
</Note>

## 在抽取器中使用生成式提供商

抽取器接受生成式提供商作为 `llm_provider=`。Jev 返回的是决策而非生成的文本，因此在这里不被接受：

```python
import os
from semantica.semantic_extract import NERExtractor, RelationExtractor, TripletExtractor
from semantica.llms import Groq

llm = Groq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

ner  = NERExtractor(method="llm",      llm_provider=llm, max_retries=3)
rel  = RelationExtractor(method="llm", llm_provider=llm)
trip = TripletExtractor(method="llm",  llm_provider=llm)
```

## 提供商对比

| 提供商 | 导入方式 | 速度 | 成本 | 本地 | 上下文 | 最适合 |
| :-------- | :------ | :----- | :---- | :----- | :------- | :-------- |
| Groq | `Groq` | 非常快 | 低 | 否 | 128k | 高吞吐抽取 |
| OpenAI | `OpenAI` | 快 | 中 | 否 | 128k | 通用、函数调用 |
| Anthropic | `LiteLLM(model="anthropic/...")` | 快 | 中 | 否 | 200k | 复杂推理、安全 |
| Gemini | `LiteLLM(model="gemini/...")` | 快 | 低 | 否 | 1M | 长上下文、多模态 |
| Ollama | `LiteLLM(model="ollama/...")` | 中 | 免费 | 是 | 因模型而异 | 隐私、隔离环境 |
| DeepSeek | `LiteLLM(model="deepseek/...")` | 快 | 极低 | 否 | 64k | 编码、分析 |
| Azure OpenAI | `LiteLLM(model="azure/...")` | 快 | 中 | 否 | 128k | 企业、合规 |
| AWS Bedrock | `LiteLLM(model="bedrock/...")` | 快 | 不等 | 否 | 因模型而异 | AWS 原生负载 |
| HuggingFace | `HuggingFaceLLM` | 慢 | 免费 | 是 | 因模型而异 | 自定义模型、BYOM |
| TypeSafe Jev | `Jev` / `AsyncJev` | 非常快 | 按提供商定价 | 否 | 应用状态 | 类型化路由、分类与打分 |

<Tip>
  生产抽取流水线用 Groq，吞吐与成本的平衡最好。复杂多跳推理用 Claude Opus 或 GPT-4o，准确率最高。
</Tip>

## 默认值与可复现性

文档示例为了更好的开发者体验，可能展示更强的模型；而实现默认值优先考虑可靠性和成本效率。因此，了解真实的默认值有助于复现结果、保持基准测试一致。

**经核实的实现默认值：**

| 提供商 | 默认模型 | 说明 |
| :---------- | :--------------- | :------- |
| `Groq` | `llama-3.1-8b-instant` | 实现默认值；示例用 `llama-3.3-70b-versatile` 做展示 |
| `OpenAI` | `gpt-3.5-turbo` | 实现默认值；示例用 `gpt-4o` 做展示 |
| `HuggingFaceLLM` | `gpt2` | 轻量、兼容性广 |
| `Jev` / `AsyncJev` | `jev-latest` | 抢先体验别名；生产环境对可复现性有要求时，请显式传入具体模型 |

构造提供商时不传 `model=` 就会用这些模型。本文档各处示例用的是更强的展示模型。生产环境要结果可复现，请始终显式传 `model=`。

**为什么这很重要：**
- 抽取结果跨环境可复现
- 基准测试有一致的基线性能
- 生产负载扩容时成本可预期

## 性能与可靠性建议

### 带重试的抽取

```python
import os
from semantica.semantic_extract import NERExtractor
from semantica.llms import Groq

llm = Groq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))
ner = NERExtractor(method="llm", llm_provider=llm, max_retries=3)

# Process multiple texts with automatic retries
texts = ["Document 1 text...", "Document 2 text...", "Document 3 text..."]
all_entities = []

for text in texts:
    entities = ner.extract(text)
    all_entities.extend(entities)

# Rate limiting handled automatically by provider
```

### 按用例选模型

| 用例 | 推荐提供商/模型 | 理由 |
| :---------- | :--------------------------- | :----------- |
| **实体抽取** | `Groq("llama-3.3-70b-versatile")` | 快，结构化任务准确率不错 |
| **关系抽取** | `OpenAI("gpt-4o")` | 复杂关系推理最强 |
| **复杂分析** | `LiteLLM("anthropic/claude-sonnet-5")` | 推理能力最高 |
| **高吞吐/低成本** | `LiteLLM("deepseek/deepseek-chat")` | 单 token 成本最低 |

### 错误处理

```python
import os
from semantica.llms import Groq
from semantica.semantic_extract import NERExtractor

llm = Groq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

# Automatic retries for rate limits and transient errors
extractor = NERExtractor(
    method="llm",
    llm_provider=llm,
    max_retries=3      # Retry failed requests automatically
)
```

- [Semantic Extract](./semantic_extract.md) — 用 LLM 做实体和关系抽取。
- [Agno Integration](../integrations/agno.md) — Agno 多智能体团队中的 LLM 提供商。
- [Reasoning](./reasoning.md) — 基于 LLM 的演绎与溯因推理。
- [Context](./context.md) — GraphRAG 用 LLM 对知识图谱(Knowledge Graph)做推理。
