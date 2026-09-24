---
title: 大语言模型(LLM)集成
description: 通过统一接口将 Semantica 连接到 Groq、OpenAI、Anthropic、HuggingFace、Novita AI 等 100 多家 LLM 提供商。
source: guides/llm-integrations.md
source_version: 8b6fd62d565ade6c9c0ad75da0f755d44cba02a9
---

Semantica 提供统一的提供商(Provider)接口——无论是 Groq、OpenAI、Anthropic Claude、HuggingFace、Novita AI，还是经 LiteLLM 接入的另外 100 多家大语言模型(LLM)提供商，用的都是同一套 `.generate()`、`.generate_structured()` 和 `.generate_typed()` 方法。当你出于延迟、准确率、成本或数据驻留(Data Residency)的考虑需要更换提供商、又不想动应用代码时，就用它。

## 什么是 LLM 集成？

`semantica.llms` 模块为对接大语言模型提供商提供了统一接口。你不必逐一学习各家 API——无论调用的是 Groq、OpenAI、Anthropic 还是本地 HuggingFace 模型，用的都是同一组方法（`.generate()`、`.generate_structured()`、`.generate_typed()`）。

**提供商之间接口统一：** Semantica 中所有 LLM 提供商暴露的方法完全一致，因此从 OpenAI 换到 Anthropic，只需要改提供商的构造函数，应用代码一行不用动。

**提供商包装类与语义抽取的提供商字符串：**`semantica.llms` 里的类（`Groq`、`OpenAI`、`LiteLLM`、`HuggingFaceLLM`）是用于文本生成的 Python 对象；`semantica.semantic_extract` 模块则接受提供商名字符串来做实体与关系抽取。本指南对两种方式都有覆盖。

## 为什么使用 LLM 集成？

**提供商可移植。** 用一家测试，用另一家上线。原型阶段用 Groq，生产阶段换 Anthropic，代码不用改。

**降低供应商锁定(Vendor Lock-In)。** 别把应用绑死在某一家 LLM 提供商的 API 上。价格变了、服务出问题了，换一家也很省事。

**API 一致。** 所有提供商都用同一组 `.generate()`、`.generate_structured()`、`.generate_typed()` 方法，不用再去学各家专属接口。

**多提供商工作流。** 同一条流水线里，初始分类跑快模型，复杂推理交给昂贵的前沿模型(Frontier Model)。

**本地与云端部署的灵活性。** 开发阶段用云提供商，生产环境需要物理隔离时切换到本地 HuggingFace 模型。

## 何时该用、何时不该用

**LLM 集成适合：**

- 文本生成、摘要与问答任务
- 需要自然语言理解的复杂推理
- 从非结构化文本中抽取结构化数据
- 需要解读与综合的多步分析
- 上下文、歧义或领域知识会影响结果的场景

**确定性工具可能更合适：**

- 正则表达式就能搞定的模式匹配
- 标准清晰的简单规则分类
- 数学计算或统计分析
- 图遍历与关系查询
- 逻辑已知的确定性数据转换

**以下场景可能用不上完整 LLM：**

- 简单关键词搜索或精确字符串匹配
- 决策树早已定好的确定性流程
- 高频低延迟、推理开销敏感的操作
- 可解释性要求逻辑透明、可按规则复现的任务

<Info>
  `semantica.llms` 中的提供商（`Groq`、`OpenAI`、`LiteLLM`、`HuggingFaceLLM`）用于文本生成和 `query_with_reasoning()`。要做结构化的实体与关系抽取，`semantica.semantic_extract` 接受提供商名字符串。两种模式这里都会讲到。
</Info>

## 选择提供商

提供商的选择由四个因素驱动，各有各的适用场景：

**延迟** 在实时 SOC 分诊回路里最要紧——分析师正等着分诊结论。Groq 的推理基础设施通常能在 300 毫秒内返回 8B 模型的响应，交互式工作流非它莫属。

**准确率** 在高风险决策里最要紧：临床禁忌核查、信贷委员会推理、法律文书分析。经 `LiteLLM` 调用的 Claude、GPT-4 等前沿模型推理能力最强。

**数据驻留** 约束会直接排除云提供商——涉密或受 HIPAA 监管的工作负载就是如此。`HuggingFaceLLM` 加本地模型路径，或 `Ollama` 指向本地服务，都能实现完全无网络的气隙隔离(Air-Gapped)部署。

**规模化成本** 更适合 Novita AI 这类高吞吐提供商——批量抽取流水线每小时处理成千上万份文档，按 token 计费的成本会迅速累积。

统一接口意味着：你可以先用 Groq 追速度做原型，再用 Claude 验证准确率，最后为合规部署到 Azure OpenAI——应用代码一行不改。

## 共享接口

每个提供商都暴露同样的方法：

```python
provider.generate(prompt: str, **kwargs) -> str
provider.generate_structured(prompt: str, **kwargs) -> dict | list
provider.generate_typed(prompt: str, schema: Type[BaseModel], max_retries: int = 3, **kwargs) -> BaseModel
provider.is_available() -> bool
```

`generate()` 返回纯字符串。`generate_structured()` 要求模型以 JSON 应答并返回解析结果——顶层是 JSON 对象时返回 `dict`，模型返回顶层 JSON 数组时返回 `list`。`generate_typed()` 接收一个 Pydantic 模型，用它校验模型输出，校验失败会把错误信息回填进提示词并重试，最多 `max_retries` 次——当下游代码需要保证结构形状、而不是碰运气的 JSON 时，就用它。`is_available()` 让你在正式调用前先做一次健康检查——重试逻辑和预热检查里很有用。

也就是说，Semantica 中任何接受 LLM 的地方——`query_with_reasoning()`、语义抽取、自定义推理循环——都可以互换使用这些提供商。

## Groq — 面向实时智能体的快速推理

**Groq** 是一家专攻超高速语言模型推理的云提供商，使用名为语言处理单元(Language Processing Unit, LPU)的自定义硬件。其基础设施对较小模型能做到 300 毫秒以内的响应时间，适合速度比极限推理能力更重要的实时应用。

Groq Cloud 在专建的 LPU 上运行开源模型，8B 参数模型延迟不到 300 毫秒。只要 LLM 处于智能体循环的热路径上——SOC 分诊、实时告警分类、对话智能体——Groq 都是合理的默认选择。

```python
from semantica.llms import Groq

# api_key falls back to the GROQ_API_KEY environment variable
groq = Groq(model="llama-3.1-8b-instant", api_key="YOUR_GROQ_KEY")

# Always health-check before the first call in a long-running process
if not groq.is_available():
    raise RuntimeError("Groq provider unreachable — check GROQ_API_KEY")

# Plain generation
verdict = groq.generate(
    "Alert: 4200 LDAP objects enumerated in 8s from ws-finance-03. "
    "True positive or false positive? One sentence.",
    temperature=0.1,    # low temperature for deterministic triage verdicts
)
print(verdict)
# "True positive — volume and speed are consistent with T1087.002 domain enumeration."

# Structured extraction — returns a parsed dict
entities = groq.generate_structured(
    "Extract threat actors and CVEs from: "
    "APT29 exploited CVE-2024-3400 in PAN-OS GlobalProtect."
)
# {"threat_actors": ["APT29"], "cves": ["CVE-2024-3400"], "products": ["PAN-OS GlobalProtect"]}
```

Groq 的模型选择归结为速度与能力的权衡：热路径上的活交给 `llama-3.1-8b-instant`；需要更强推理、又能容忍稍高延迟时用 `llama-3.3-70b-versatile`；长上下文摘要任务用 `mixtral-8x7b-32768`。

## OpenAI — 函数调用与视觉

**OpenAI** 提供 GPT 模型家族的访问入口，其中包括 GPT-4o——它具备函数调用(Function Calling，即结构化工具使用)和图像/文档视觉处理等高级能力。需要强语言理解与生成能力的复杂推理任务，OpenAI 模型都能胜任。

`OpenAI` 提供商包装了 OpenAI API。需要 GPT-4o 精准的函数调用、文档截图的视觉能力，或者团队本来就有 OpenAI 合同且打算继续用时，就选它。

```python
from semantica.llms import OpenAI

oai = OpenAI(model="gpt-4o", api_key="YOUR_OAI_KEY")
# api_key falls back to OPENAI_API_KEY environment variable

response = oai.generate(
    "Under CRR2 Article 92, what is the minimum total capital ratio "
    "for a G-SIB subject to a 2% GSIB buffer surcharge?"
)
print(response)

# Structured output — useful for deterministic data extraction
risk_data = oai.generate_structured(
    "Extract all counterparty names and exposure amounts from: "
    "Counterparty A: 45M EUR notional, Counterparty B: 12M EUR notional, "
    "Counterparty C: 89M EUR notional."
)
# {"counterparties": [{"name": "Counterparty A", "exposure_eur": 45000000}, ...]}
```

默认模型 `gpt-3.5-turbo` 做分类和轻量抽取够用了。复杂的多步监管推理或文档理解，换 `gpt-4o`。

## Anthropic — 复杂推理与结构化抽取

**Anthropic** 提供 Claude 模型家族，设计上强调严谨的指令遵循，在多步推理、长文档分析和代码相关任务上表现出色。面对含糊的指令，Claude 模型通常比其他提供商的更谨慎。当"自信满满地答错"代价很高时，这一点很关键。

`Anthropic` 提供商包装了 Claude API。任务需要贯穿多个相互依赖的步骤做推理（而非单轮抽取）、要处理必须整体留在上下文里的长文档，或者需要经 schema 校验的结构化输出而非尽力而为的 JSON 时，找它。

使用前先安装：`pip install "semantica[llm-anthropic]"`（或直接 `pip install anthropic`）。

```python
from semantica.llms import Anthropic

claude = Anthropic(model="claude-sonnet-4-6", api_key="YOUR_ANTHROPIC_KEY")
# api_key falls back to the ANTHROPIC_API_KEY environment variable

# is_available() only confirms a client was constructed from some key.
# It does not validate the key or check network reachability - an
# invalid or expired key still passes this check and fails at generate().
if not claude.is_available():
    raise RuntimeError("Anthropic provider not configured - set ANTHROPIC_API_KEY")

# Plain generation - multi-step reasoning over a contract clause
verdict = claude.generate(
    "A vendor contract has a 30-day termination-for-convenience clause "
    "but a 90-day data-return obligation that survives termination. "
    "If the customer terminates on day 1, when must vendor-held data "
    "be returned? Answer with the date basis only.",
    temperature=0.1,
)
print(verdict)
# "Day 120 from termination notice. The 90-day return period runs from
#  the termination date (day 30), not from the notice date."

# Structured, schema-validated output
from pydantic import BaseModel

class ContractRisk(BaseModel):
    clause: str
    risk_level: str
    days_to_deadline: int

risk = claude.generate_typed(
    "Extract the termination clause risk from: vendor contract, "
    "30-day termination for convenience, 90-day post-termination "
    "data return obligation.",
    schema=ContractRisk,
)
print(risk.risk_level, risk.days_to_deadline)
# "medium" 90
```

模型选择和其他提供商一样分档：海量的分类任务、成本比深度更重要时用 Haiku 档；大多数抽取与推理任务默认用 Sonnet 档；任务确实需要当前最深的推理能力、延迟和成本靠后站时用 Opus 档。具体模型标识符以 Anthropic 文档为准——它们带版本号，会随时间变化。

## Gemini — 长上下文与多模态输入

**Gemini** 是 Google 的模型家族，上下文窗口大到一次调用就能装下整个代码库或长篇监管申报材料，并且原生支持图像和文档输入与文本并用。任务需要一次性引用大量原始材料，或输入不是纯文本时，就选它。

`Gemini` 提供商会优先尝试较新的 `google-genai` SDK，如果实际安装的是旧包，则回落到 `google-generativeai`。使用前先安装：`pip install "semantica[llm-gemini]"`（或 `pip install google-genai`）。

```python
from semantica.llms import Gemini

gemini = Gemini(model="gemini-pro", api_key="YOUR_GEMINI_KEY")
# api_key falls back to the GEMINI_API_KEY environment variable

if not gemini.is_available():
    raise RuntimeError("Gemini provider not configured - set GEMINI_API_KEY")

response = gemini.generate(
    "Summarize the key obligations in a standard NDA in three bullet points."
)
print(response)

data = gemini.generate_structured(
    "Extract the party names and effective date from: "
    "This Agreement is entered into between Acme Corp and Globex LLC, "
    "effective January 1, 2026."
)
print(data)
```

## Ollama — 本地与气隙隔离推理

**Ollama** 让模型完全跑在你自己的机器上，不要 API key，也没有任何出站网络调用。气隙隔离环境、离线开发，或者源数据不能离开本地网络的工作负载，它都是正解。

与这里其他提供商不同，`Ollama` 接收的是 `base_url` 而不是 `api_key`，它通过 HTTP 与本地 Ollama 服务通信。使用前先用 `ollama serve` 启动服务，再用 `ollama pull llama2` 拉取模型。Python 客户端安装：`pip install "semantica[llm-ollama]"`（或 `pip install ollama`）。

```python
from semantica.llms import Ollama

llm = Ollama(model="llama2", base_url="http://localhost:11434")

if not llm.is_available():
    raise RuntimeError("Ollama provider not configured - is 'ollama serve' running?")

response = llm.generate("Explain the difference between a hash map and a tree map.")
print(response)
```

与上面基于 API key 的提供商不同，Ollama 的 `is_available()` 做的是真实的连通性检查（会调用服务端的 `list()` 端点），所以这里返回 `False` 通常说明服务没在跑，而不是缺凭证。

## DeepSeek — 大规模低成本推理

**DeepSeek** 以几家美国大提供商零头的价格提供 OpenAI 兼容 API，推理质量对付抽取和分类绰绰有余。要处理海量文档、又用不上最深的推理档位时，它是合理的默认之选。

安装：`pip install "semantica[llm-deepseek]"`（或 `pip install openai`——DeepSeek 就是走 OpenAI 客户端，只是指向不同的 base URL）。

```python
from semantica.llms import DeepSeek

llm = DeepSeek(model="deepseek-chat", api_key="YOUR_DEEPSEEK_KEY")
# api_key falls back to the DEEPSEEK_API_KEY environment variable

if not llm.is_available():
    raise RuntimeError("DeepSeek provider not configured - set DEEPSEEK_API_KEY")

response = llm.generate("List three risks of using a floating IP in a Kubernetes ingress.")
print(response)

data = llm.generate_structured(
    "Extract the CVE ID and affected product from: "
    "CVE-2024-3400 affects PAN-OS GlobalProtect gateways."
)
print(data)
```

## LiteLLM — 一个接口，100 多家提供商

**LiteLLM** 是一个通用适配器，为 100 多家不同的 LLM 提供商提供单一接口——包括 Anthropic Claude、Azure OpenAI、AWS Bedrock、Google Vertex AI 和本地 Ollama 实例。它相当于一层翻译层，把你的统一 API 调用转换成各家专属的请求，因此切换提供商不需要改代码。

`LiteLLM` 是把瑞士军刀。它包装了 `litellm` 库，后者用统一的补全(completion) API 对接所有主流提供商。模型字符串同时编码了提供商和模型名：`"anthropic/claude-sonnet-5"`、`"azure/gpt-4o"`、`"bedrock/anthropic.claude-sonnet-4-5-20250929-v1:0"`、`"ollama/llama3.2"`。改字符串就是换提供商——其他代码一概不动。

```python
from semantica.llms import LiteLLM

# Anthropic Claude — highest accuracy for complex reasoning
llm = LiteLLM(model="anthropic/claude-sonnet-5")
# Reads ANTHROPIC_API_KEY from environment

# Azure OpenAI — compliance and data-residency requirements
llm = LiteLLM(model="azure/gpt-4o", api_key="YOUR_AZURE_KEY")

# AWS Bedrock — existing cloud agreement, no new vendor
llm = LiteLLM(model="bedrock/anthropic.claude-sonnet-4-5-20250929-v1:0")

# Google Vertex AI
llm = LiteLLM(model="vertex_ai/gemini-1.5-pro")

# Ollama — fully local, no network calls
llm = LiteLLM(model="ollama/llama3.2")

# All of them: same call
response = llm.generate("Summarise the ICH E6(R2) GCP guideline key requirements.")
```

各提供商的环境变量约定：`ANTHROPIC_API_KEY`、`AZURE_API_KEY`、`OPENAI_API_KEY`、`GOOGLE_APPLICATION_CREDENTIALS` 等，LiteLLM 会自动读取。如果切换提供商由部署环境决定，可以把提供商选择放进一个配置字典、启动时注入——应用代码里不会出现 `if/else` 分支：

```python
import os

PROVIDER_MAP = {
    "prod":    "anthropic/claude-sonnet-5",
    "staging": "openai/gpt-4o-mini",
    "local":   "ollama/llama3.2",
    "azure":   "azure/gpt-4o",
}

env = os.getenv("DEPLOY_ENV", "local")
llm = LiteLLM(model=PROVIDER_MAP[env])
# The rest of the application never touches provider names
```

## HuggingFaceLLM — 气隙隔离与本地部署

**HuggingFaceLLM** 提供对 HuggingFace 生态开源模型的访问——既可以从 HuggingFace Hub 下载，也可以从本地文件路径加载。推理期间完全无网络的部署（如涉密环境或气隙隔离系统），只有这一条路。

`HuggingFaceLLM` 从 HuggingFace Hub 或本地目录路径加载模型，推理期间零网络调用。涉密环境、受 HIPAA 约束的临床部署，以及任何没有出站互联网的网段，都只有这个选项。

```python
from semantica.llms import HuggingFaceLLM

# HuggingFace Hub — authentication via HF_TOKEN environment variable
hf = HuggingFaceLLM(model="mistralai/Mistral-7B-Instruct-v0.3")

# Biomedical fine-tuned model for clinical entity extraction
bio_llm = HuggingFaceLLM(model="aaditya/Llama3-OpenBioLLM-70B")

# Air-gapped deployment — model on local NFS share or mounted volume
# Both `model` and `model_name` are accepted as constructor parameters
air_gapped_llm = HuggingFaceLLM(model="/opt/models/llama-3.1-70b-instruct")

response = air_gapped_llm.generate(
    "Summarise SIGINT collection window 2024-Q3 for APT29 C2 infrastructure.",
    max_length=512,
)
```

要经 Hub 访问受限或私有模型，需在环境里设置 `HF_TOKEN`。本地路径则不需要任何 token——模型目录里必须有标准的 HuggingFace checkpoint 文件。

## 不改应用代码切换提供商

统一接口的真正回报体现在 `query_with_reasoning()` 上。每个 `AgentContext` 中驱动"基于图谱的推理"的正是这个调用。由于它接受任意提供商对象，你可以在流水线的任意层级换上不同的 LLM，周围代码零改动。

```python
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore
from semantica.llms import Groq, LiteLLM

vs    = VectorStore(backend="faiss", dimension=768)
graph = ContextGraph(advanced_analytics=True)
context = AgentContext(vector_store=vs, knowledge_graph=graph, graph_expansion=True)

# Load your knowledge base once
context.store(
    [
        {"content": "APT29 exploits CVE-2024-3400 in PAN-OS GlobalProtect — CVSS 10.0",
         "metadata": {"source": "nvd", "actor": "APT29"}},
        {"content": "NOBELIUM (APT29) leverages OAuth token theft against Azure AD tenants",
         "metadata": {"source": "msft_blog_2023", "actor": "APT29", "technique": "T1528"}},
    ],
    extract_entities=True,
    extract_relationships=True,
)

query = "What is APT29's current exploitation methodology and what cloud services are targeted?"

# Tier 1: fast answer with Groq (< 300ms)
fast_llm = Groq(model="llama-3.1-8b-instant", api_key="YOUR_GROQ_KEY")
fast_result = context.query_with_reasoning(query, llm_provider=fast_llm, max_results=5)
print("FAST: {}  (conf={:.0%})".format(fast_result["response"], fast_result["confidence"]))

# Tier 2: deep answer with Claude if confidence is below threshold
if fast_result["confidence"] < 0.85:
    deep_llm = LiteLLM(model="anthropic/claude-sonnet-5")
    deep_result = context.query_with_reasoning(
        query, llm_provider=deep_llm, max_results=15, max_hops=3
    )
    print("DEEP: {}  (conf={:.0%})".format(deep_result["response"], deep_result["confidence"]))
```

`context`、图谱、检索逻辑——全都没变。两个层级之间唯一的差别就是 `llm_provider` 参数。

## 在语义抽取中使用提供商

做命名实体识别(NER)、关系抽取和三元组(Triplet)抽取时，Semantica 的 `semantica.semantic_extract` 模块接受的是提供商名字符串，而不是类实例。提供商的实例化由模块内部处理。

```python
from semantica.semantic_extract import NamedEntityRecognizer, EventDetector
from semantica.semantic_extract.methods import (
    extract_entities_llm,
    extract_relations_llm,
    extract_triplets_llm,
)

# NER with Groq — provider name as a string
ner = NamedEntityRecognizer(
    methods=["llm"],
    provider="groq",
    llm_model="llama-3.1-8b-instant",
)
entities = ner.extract_entities(
    "APT29 exploited CVE-2024-3400 in PAN-OS GlobalProtect to compromise NATO member networks."
)
for e in entities:
    # Entity fields: .text, .label, .confidence
    print("{} ({}) — conf={:.2f}".format(e.text, e.label, e.confidence))
# APT29 (THREAT_ACTOR) — conf=0.96
# CVE-2024-3400 (CVE) — conf=0.99
# PAN-OS GlobalProtect (PRODUCT) — conf=0.94
# NATO (ORGANIZATION) — conf=0.91

# Event detection with the same provider pattern
detector = EventDetector(method="llm", provider="groq")
events = detector.detect_events(
    "ENISA published the Threat Landscape 2024 report on October 22nd, "
    "covering 11 primary threat categories including ransomware and supply-chain attacks."
)

# Triplet extraction — returns (subject, predicate, object) triples
text = "Warfarin inhibits VKORC1 enzyme activity, reducing vitamin K-dependent clotting factor synthesis."
triplets = extract_triplets_llm(text, provider="groq", model="llama-3.1-8b-instant")
for t in triplets:
    print("{} -> {} -> {}".format(t.subject, t.predicate, t.object))
# warfarin -> inhibits -> VKORC1 enzyme activity
# warfarin -> reduces -> vitamin K-dependent clotting factor synthesis
```

## Novita AI — 高性价比的批量抽取

**Novita AI** 以低廉的单次调用成本提供 OpenAI 兼容 API。在大批量 NER 流水线里，成本比"单次最优答案"更重要的场景下，它是合理之选。

安装：`pip install "semantica[llm-novita]"`（或 `pip install openai`——Novita 同样走 OpenAI 客户端，只是指向不同的 base URL）。

```python
from semantica.llms import Novita

llm = Novita(model="deepseek/deepseek-v3.2", api_key="YOUR_NOVITA_KEY")
# api_key falls back to the NOVITA_API_KEY environment variable

if not llm.is_available():
    raise RuntimeError("Novita provider not configured - set NOVITA_API_KEY")

response = llm.generate("Summarize the Basel III leverage ratio requirement.")

data = llm.generate_structured(
    "Extract drug names and dosages from: "
    "Patient received warfarin 5mg daily, aspirin 75mg daily, metformin 500mg twice daily."
)
```

在 NER 接口里，Novita 也可以用提供商名字符串来调用，不必直接经由 `Novita` 类：

```python
from semantica.semantic_extract import NamedEntityRecognizer

ner = NamedEntityRecognizer(
    methods=["llm"],
    provider="novita",
    llm_model="deepseek/deepseek-v3.2",
)
entities = ner.extract_entities(
    "CVE-2024-3400 is exploited by UNC3886 targeting PAN-OS GlobalProtect."
)
for e in entities:
    print("{} ({}) conf={:.2f}".format(e.text, e.label, e.confidence))
```

## 行业示例

<Tabs>
<Tab title="国防 — CTI/威胁情报">
某涉密威胁情报分析单元必须完全气隙隔离运行——任何形式的出站网络流量都不允许。抽取模型和推理模型都从本地 NFS 共享加载。知识图谱(Knowledge Graph)在整个分析会话期间持续累积；所有推理都在本地完成。

```python
from semantica.llms import HuggingFaceLLM
from semantica.semantic_extract import NamedEntityRecognizer
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore

# Both models load from the air-gapped NFS share — no Hub calls
extraction_llm = HuggingFaceLLM(model="/opt/models/mistral-7b-instruct")
reasoning_llm  = HuggingFaceLLM(model="/opt/models/llama-3.1-70b-instruct")

# The llms module wrappers can also be used directly for raw prompt generation
# when you want to bypass the semantic extraction layer entirely

sigint_text = (
    "[S//NF] APT29 operator observed deploying WARPWIRE credential harvester "
    "via CVE-2024-3400 on perimeter VPN gateways of target BRAVO-7."
)

# For fully local models, call the provider's generate method directly
raw_entities = extraction_llm.generate(
    "Extract all threat actors, CVEs, malware names, and target identifiers "
    "from the following text as a JSON list:\n\n" + sigint_text
)

# Build the graph and run reasoning
vs    = VectorStore(backend="faiss", dimension=768)
graph = ContextGraph(advanced_analytics=True)
context = AgentContext(
    vector_store=vs,
    knowledge_graph=graph,
    graph_expansion=True,
    decision_tracking=True,
)

context.store(
    sigint_text,
    metadata={"source": "SIGINT_Q4_2024", "classification": "SECRET//NOFORN"},
    conversation_id="op-analysis-q4",
)

result = context.query_with_reasoning(
    "What credential-harvesting capabilities has APT29 deployed against "
    "perimeter VPN gateways and what CVEs enable initial access?",
    llm_provider=reasoning_llm,   # fully local — no network calls
    max_results=10,
    max_hops=3,
)
print(result["response"])
print("Confidence: {:.0%}".format(result["confidence"]))

context.save("./classified_output/q4_analysis/")
```

</Tab>

<Tab title="安全 — SOC/事件响应">
某 SOC 流水线在不同层级使用两家提供商：Groq 负责 500 毫秒以内的初始分诊，让分析师保持工作节奏；当 Tier 1 置信度低于升级阈值时，切换到 Anthropic Claude 做深度 ATT&CK 分析。提供商切换由程序判定——无需人工交接。

```python
from semantica.llms import Groq, LiteLLM
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore

vs    = VectorStore(backend="faiss", dimension=768)
graph = ContextGraph()
context = AgentContext(
    vector_store=vs,
    knowledge_graph=graph,
    graph_expansion=True,
    decision_tracking=True,
)

# Preload MITRE ATT&CK runbook knowledge
context.store([
    "T1087.002 (Domain Account Discovery): anomalous LDAP enumeration — isolate source host, reset service account passwords",
    "T1053.005 (Scheduled Task/Job): encoded PowerShell via wmiprvse.exe — collect task XML, check persistence keys, notify IR",
    "T1021.002 (SMB/Windows Admin Shares): PsExec lateral movement to DC — immediate host isolation, reset service accounts",
])

alert = (
    "SIEM Alert: host ws-finance-03, user jsmith — scheduled task with base64-encoded PowerShell. "
    "Parent process: wmiprvse.exe. Sigma: T1053.005. Time: 2025-06-21T09:14:32Z."
)
context.store(alert, metadata={"type": "alert", "severity": "high"})

# Tier 1: fast triage with Groq — target < 500ms end-to-end
fast_llm = Groq(model="llama-3.1-8b-instant", api_key="YOUR_GROQ_KEY")
triage = context.query_with_reasoning(
    "Is this alert a true positive? One sentence verdict and confidence.",
    llm_provider=fast_llm,
    max_results=5,
)
print("TRIAGE: {} (conf={:.0%})".format(triage["response"], triage["confidence"]))

# Tier 2: escalate to Claude for deep analysis if Tier 1 is uncertain
if triage["confidence"] < 0.88:
    deep_llm = LiteLLM(model="anthropic/claude-sonnet-5")
    deep = context.query_with_reasoning(
        "Full MITRE ATT&CK analysis of this alert: identify the attack chain, "
        "blast radius, affected systems, and recommended containment steps.",
        llm_provider=deep_llm,
        max_results=15,
        max_hops=3,
    )
    print("DEEP ANALYSIS: {}".format(deep["response"]))

    context.record_decision(
        category="escalation",
        scenario="Scheduled task T1053.005 on ws-finance-03 — Tier 1 conf {:.0%}".format(triage["confidence"]),
        reasoning=deep["reasoning_path"],
        outcome="escalated_tier2",
        confidence=deep["confidence"],
        entities=["ws-finance-03", "jsmith", "T1053.005"],
        decision_maker="soc_pipeline_v3",
    )
```

</Tab>

<Tab title="生命科学 — 临床/制药">
某临床 NLP 流水线用 HuggingFace 上的领域专用生物医学 NER 模型做实体抽取，再切换到 Anthropic Claude 合成结构化的肿瘤学报告。Claude 调用仍由同一个 `LiteLLM` 包装器完成——为满足 HIPAA 合规切到 Azure OpenAI，只改一行。

```python
from semantica.llms import LiteLLM
from semantica.semantic_extract import NamedEntityRecognizer

# Biomedical NER — HuggingFace extractor for clinical entities
# (Note: HuggingFace NER uses method="huggingface", not the LLM generation interface)
ner = NamedEntityRecognizer(
    methods=["huggingface"],
    huggingface_model="d4data/biomedical-ner-all",
    confidence_threshold=0.75,
)

clinical_note = (
    "Patient presents with HER2+ breast cancer (T2N1M0, Stage IIB). "
    "Recommended: trastuzumab 8mg/kg loading then 6mg/kg q3w + pertuzumab 840mg loading "
    "then 420mg q3w + docetaxel 75mg/m2 q3w (THP regimen) for 6 cycles. "
    "eGFR 78 mL/min/1.73m2, LVEF 62%. Monitor for cardiotoxicity."
)

entities = ner.extract_entities(clinical_note)
# Entity fields: .text, .label (not .type), .confidence
drugs     = [e for e in entities if e.label == "DRUG"]
diagnoses = [e for e in entities if e.label in ("DISEASE", "CANCER")]

print("Drugs identified:")
for d in drugs:
    print("  {} (conf={:.2f})".format(d.text, d.confidence))
# trastuzumab (conf=0.98), pertuzumab (conf=0.97), docetaxel (conf=0.96)

# Report synthesis with Claude — switch to azure/gpt-4o for HIPAA by changing one string
report_llm = LiteLLM(model="anthropic/claude-sonnet-5")
# For HIPAA-constrained Azure deployment:
# report_llm = LiteLLM(model="azure/gpt-4o", api_key="YOUR_AZURE_KEY")

oncology_summary = report_llm.generate(
    "Write a structured oncology treatment summary for the following note. "
    "Include: diagnosis, staging, treatment regimen, monitoring parameters, "
    "and key safety considerations.\n\n" + clinical_note
)
print(oncology_summary)
```

</Tab>

<Tab title="银行 — 风险/合规">
某监管问答系统把同一个巴塞尔 III 问题跑两遍——分别问两家提供商，取置信度更高的答案。这是高风险监管解读场景下一个简单的共识模式：答错可能带来法律风险。

```python
from semantica.llms import OpenAI, LiteLLM
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore

vs    = VectorStore(backend="faiss", dimension=768)
graph = ContextGraph(advanced_analytics=True)
context = AgentContext(
    vector_store=vs,
    knowledge_graph=graph,
    graph_expansion=True,
    retention_days=2555,
)

# Load Basel III / CRR2 regulatory corpus
context.store(
    [
        {"content": "CRR2 Art. 92: minimum total capital ratio 8% + 2.5% conservation buffer + GSIB surcharge",
         "metadata": {"source": "CRR2_Art92", "category": "capital_requirement"}},
        {"content": "Basel III leverage ratio: Tier 1 capital / total exposure >= 3% (Art. 429 CRR2)",
         "metadata": {"source": "CRR2_Art429", "category": "leverage"}},
        {"content": "GSIB buffer surcharges: bucket 1=1%, bucket 2=1.5%, bucket 3=2%, bucket 4=2.5%, bucket 5=3.5%",
         "metadata": {"source": "BCBS_GSIB_2022", "category": "gsib_buffer"}},
    ],
    extract_entities=True,
    extract_relationships=True,
)

question = (
    "Under CRR2 Article 92 and the BCBS GSIB framework, what is the minimum "
    "total capital ratio for a bucket-2 G-SIB? Show the component breakdown."
)

# Two-provider consensus — same query, same graph, different LLMs
gpt4o  = OpenAI(model="gpt-4o", api_key="YOUR_OAI_KEY")
claude = LiteLLM(model="anthropic/claude-sonnet-5")

answer_a = context.query_with_reasoning(question, llm_provider=gpt4o,  max_results=10)
answer_b = context.query_with_reasoning(question, llm_provider=claude, max_results=10)

# Pick higher-confidence answer for the audit trail
best = answer_a if answer_a["confidence"] >= answer_b["confidence"] else answer_b
winner = "GPT-4o" if best is answer_a else "Claude"

print("Selected: {} (conf={:.0%})".format(winner, best["confidence"]))
print(best["response"])
# Expected: 8% (minimum) + 2.5% (conservation) + 1.5% (bucket-2 GSIB) = 12.0% total

# Sources the answer is grounded in
for src in best["sources"]:
    print("  - [{}] {}".format(src.get("source", "?"), src["content"][:60]))
```

</Tab>
</Tabs>

## 常见陷阱

**为简单抽取任务选用昂贵的前沿模型。** 基础实体抽取用 GPT-4o 或 Claude Sonnet 属于大材小用——Groq 的 Llama 模型以零头的成本和延迟就能搞定常规 NER 和分类。前沿模型留给真正需要精细解读的复杂推理。

**忽视提供商之间的延迟差异。** Groq 通常 300 毫秒内响应，同样的查询 Anthropic Claude 可能要 2-3 秒。对实时智能体或交互式工作流来说，延迟差异会在多次 LLM 调用之间累积。请在真实负载下实测你的提供商性能。

**把 LLM 用在正则就能搞定的确定性模式匹配上。** 如果任务是抽取邮箱地址、电话号码或其他模式型实体，正则表达式比 LLM 更快、更便宜、更可靠。只有当上下文、歧义或领域知识会影响解读正确性时，才值得动用 LLM。

**不校验结构化输出。** `generate_structured()` 返回解析后的 JSON（dict，或顶层数组时为 list），但 LLM 仍可能产出格式错误或不完整的结构。在下游使用之前，先对照预期 schema 校验结果——或者直接用 `generate_typed()`，它替你按 Pydantic 模型校验。

**换了提供商却不测试提示词表现。** 不同模型对同一提示词的反应不同。为 GPT-4 调优的提示词，换到 Llama 或 Claude 上可能效果很差。切换提供商时，要重新测试提示词，并按需调整 temperature、指令或示例。

**用本地 HuggingFace 模型处理需要最新知识的任务。** 本地模型的知识截止于它的训练日期，无法访问当前信息。需要最新知识的任务（新出的 CVE、现行法规、最新威胁情报），可能必须改用训练数据更新的云提供商。

## 相关指南

- [智能体记忆](./agent-memory.md) — 用 `query_with_reasoning()` 搭配任意 LLM 提供商做基于图谱的检索
- [多智能体系统](./multi-agent.md) — 在共享图谱流水线中为不同智能体层级接入不同的 LLM 提供商
- [语义抽取](./semantic-extraction.md) — LLM 驱动的命名实体识别(NER)、关系抽取、事件检测(Event Detection)与三元组抽取
- [GraphRAG](./graphrag.md) — 用 `query_with_reasoning()` 做多跳图推理
