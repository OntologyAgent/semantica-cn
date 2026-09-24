---
title: 多智能体系统
description: 通过共享记忆、知识图谱与决策历史协调多个 AI 智能体——无需消息中间件。
source: guides/multi-agent.md
source_version: 79596c6aee4d42b50a566a86a396b4b60da49d3c
---

## 什么是多智能体协作？

多智能体(Multi-Agent)系统是一种软件架构：多个自主的智能体(Agent)协同工作，完成单个智能体难以有效搞定、甚至根本无法完成的复杂任务。开发者不再构建一个试图包揽一切的单体智能体，而是把工作拆分给各司其职的专职智能体。

**为什么要拆分给多个智能体：**
- **关注点分离** —— 每个智能体专注一个领域（摄取、分析、报告），而不是试图样样精通
- **独立推理** —— 不同智能体可以针对各自任务，使用不同的模型、提示词和推理策略
- **并行处理** —— 多个智能体可以同时处理同一个问题的不同侧面
- **类人的工作流分解** —— 模拟人类团队分解复杂分析工作的自然方式

**Semantica 的协作方式：**
Semantica 通过共享上下文（记忆和知识图谱）来协调智能体，而不是靠消息中间件或服务间 API 调用。所有智能体读写同一套底层数据结构，无需复杂的中间件就能无缝共享信息。

**单智能体与多智能体架构对比：**
- **单智能体** —— 一个 `AgentContext` 承担从摄取(Ingestion)到最终输出的全部任务
- **多智能体** —— 多个 `AgentContext` 实例或按命名空间划分的工作流，各自负责特定的流水线阶段或分析角色

## 为什么使用多智能体系统？

**职责分离。** 把复杂工作流拆成专注、可控的多个阶段，让每个智能体在各自领域做到最好，不被旁枝末节拖累。

**复杂工作流的可扩展性。** 应对需要不同专业领域、处理速度和推理方式的复杂分析流水线，而不必造出臃肿的单体智能体。

**独立的推理阶段。** 让不同智能体针对各自任务使用不同的大语言模型(LLM)、提示词、置信度阈值和推理策略，而不是迁就一刀切的方案。

**专职的智能体角色。** 为摄取、增强、分析、综合与报告分别打造专属智能体，每个都配备与其角色匹配的配置和能力。

**共享的知识与证据。** 多个智能体共同写入并读取同一套知识图谱(Knowledge Graph)和记忆库，形成不断累积的证据基础——贡献发现的智能体越多，这个基础就越好。

**类人的工作流分解。** 复刻人类团队的自然分工：分析师、研究员和决策者各自贡献专长，协同完成分析工作。

## 适用与不适用场景

**适合使用多智能体系统的场景：**
- 需要多个阶段的复杂分析工作流（研究 → 分析 → 综合 → 报告）
- 阶段分明、各阶段能从专职方法中受益的多阶段处理流水线
- 不同智能体分别处理不同信息源或不同分析方法的研究调查工作流
- 角色各异的专职智能体团队（OSINT 采集员、增强分析师、融合官）
- 不同智能体在不同时间或按不同计划运行的长时工作流
- 不同分析阶段需要不同 LLM、推理方式或置信度阈值的场景

**不要使用多智能体系统的场景：**
- 简单的文档摘要或单步信息检索任务
- 一个智能体就能有效搞定全部步骤、专业分工没有额外收益的线性工作流
- 协调开销超过核心工作复杂度的小型直接任务
- 配置得当的单个智能体即可高效完成整个工作流的情形

**重要考量：** 多智能体系统会引入额外的架构复杂度，包括状态管理、协作模式和调试难题。只有当专业分工和关注点分离的收益大于这些额外复杂度时，才选择多智能体方案。

Semantica 通过共享的 `ContextGraph` 协调多个智能体——大家读写同一张图，或者通过 `save()` 和 `load()` 交接序列化状态，全程不需要消息中间件。当你把工作拆给摄取、增强、推理、报告等角色、又要求它们共享同一份证据基础时，就用这套模式。

<Info>
  本指南聚焦多智能体协作。各智能体内部使用的记忆层见[智能体记忆](./agent-memory.md)；图的遍历与实体消解见[上下文图](./context-graphs.md)；决策记录与先例匹配见[决策智能](./decision-intelligence.md)。
</Info>

## 三种协作模式

写代码之前，先为你的流水线选对协作模式。

**共享图模式：** 多个智能体在同一个进程内共享对同一 `ContextGraph` 和 `VectorStore` 对象的引用。所有智能体立刻看到彼此的变更，延迟最低，并自带并发访问的线程安全。当各智能体在同一应用中同时运行、需要实时读取彼此的产出时，选这种。

**保存/加载交接模式：** 智能体运行在不同进程、不同容器或不同时间。前一个智能体完成工作后调用 `context.save(path)`，把完整状态序列化；下一个智能体调用 `context.load(path)`，从上一个智能体停下的地方原样恢复，包括全部记忆、图数据和向量索引。分布式系统、定时任务，或智能体运行在不同机器上、需要访问共享存储时，选这种。

**命名空间记忆模式：** 一个 `AgentContext` 服务多个逻辑智能体，每个智能体用唯一的 `conversation_id` 值划定自己的读写范围。智能体靠命名空间而非独立的上下文实例来隔离。需要轻量级角色区分、又不想为维护多套完整上下文付出资源开销时，选这种。

本指南的流水线把三种模式都用上了。

## 模式 1 —— 共享图支撑并发摄取

OSINT（**开源情报**(Open Source Intelligence)——公开可得的信息）采集员与增强智能体并发运行。二者共享同一个 `ContextGraph` 和同一个 `VectorStore`——图内部自带的 `RLock` 让并发写入很安全。

```python
import threading
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore

# 一张图、一个向量库——两个智能体都写入它们
shared_graph = ContextGraph(advanced_analytics=True)
shared_vs    = VectorStore(backend="faiss", dimension=768)

def make_agent() -> AgentContext:
    """工厂函数：每个智能体得到自己的 AgentContext，包装同一套共享底层存储。"""
    return AgentContext(
        vector_store=shared_vs,            # 同一个 VectorStore 实例
        knowledge_graph=shared_graph,      # 同一个 ContextGraph 实例
        graph_expansion=True,
        max_expansion_hops=2,
        decision_tracking=True,
    )

osint_agent      = make_agent()
enrichment_agent = make_agent()
reasoning_agent  = make_agent()
```

OSINT 采集员的职责是摄取原始情报流并抽取实体。它不做推理——只管摄取，让图自己积累结构。

```python
def osint_collection():
    """智能体 1：摄取原始威胁情报流和 CVE 数据。"""
    osint_agent.store(
        [
            {
                "content": "APT29 exploits CVE-2024-3400 in PAN-OS GlobalProtect — unauthenticated RCE, CVSS 10.0",
                "metadata": {"source": "nvd_feed", "cve": "CVE-2024-3400", "actor": "APT29"},
            },
            {
                "content": "Volexity confirms active exploitation of CVE-2024-3400 against NATO member networks",
                "metadata": {"source": "volexity_blog", "actor": "APT29", "target": "NATO"},
            },
            {
                "content": "PAN-OS GlobalProtect affected versions: < 10.2.9-h1, < 11.0.4-h1, < 11.1.2-h3",
                "metadata": {"source": "paloalto_advisory", "cve": "CVE-2024-3400", "product": "GlobalProtect"},
            },
        ],
        extract_entities=True,
        extract_relationships=True,
        conversation_id="osint-pipeline",    # 命名空间充当智能体标识符
    )
```

OSINT 采集员运行的同时，增强智能体在独立拉取攻击者画像数据，并关联到同一张图里。

```python
def enrichment():
    """智能体 2：用攻击者画像和 TTP 背景充实图谱。"""
    enrichment_agent.store(
        [
            {
                "content": "APT29 TTP profile: T1190 (Exploit Public-Facing Application), T1071.001 (Web Protocols C2), T1078 (Valid Accounts)",
                "metadata": {"source": "mitre_attck", "actor": "APT29", "type": "ttp_profile"},
            },
            {
                "content": "APT29 infrastructure fingerprint: use of Cloudflare Workers for C2 relay, certificate reuse across campaigns",
                "metadata": {"source": "recorded_future", "actor": "APT29", "type": "infrastructure"},
            },
        ],
        extract_entities=True,
        extract_relationships=True,
        conversation_id="enrichment-pipeline",    # 与 OSINT 智能体不同的命名空间
    )
```

让两者并发运行——加锁的事交给图。

```python
t1 = threading.Thread(target=osint_collection)
t2 = threading.Thread(target=enrichment)
t1.start(); t2.start()
t1.join();  t2.join()

# 现在共享图里已有两个智能体写入的实体和关系。
# 推理智能体可以跨查询两个智能体存储的全部内容。
```

## 模式 2 —— 保存/加载交接给推理智能体

推理智能体在摄取完成后运行。生产流水线中，它可能是一个独立进程、另一个容器，或一个定时任务。摄取类智能体保存共享状态，推理智能体负责加载。

**重要部署提示：** 智能体运行在不同容器或不同机器上时，必须能通过共享存储（网络文件系统、云存储或共享卷）访问同一个保存位置。

```python
# 摄取完成后：保存合并后的图和向量索引
osint_agent.save("./pipeline/enriched_intel/")
# 写入内容：
#   pipeline/enriched_intel/agent_memory.json     — 全部 MemoryItems
#   pipeline/enriched_intel/vector_store/         — FAISS 索引
#   pipeline/enriched_intel/knowledge_graph.json  — 全部节点和边

print("Ingestion complete. State saved for reasoning agent.")
```

推理智能体从全新状态启动，加载这份状态之后，就能完整访问摄取类智能体构建的一切。

```python
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore
from semantica.llms import LiteLLM

# 创建一个用于装载检查点的上下文——load() 会覆盖已有状态
reasoning_vs    = VectorStore(backend="faiss", dimension=768)
reasoning_graph = ContextGraph(advanced_analytics=True)
reasoning_agent = AgentContext(
    vector_store=reasoning_vs,
    knowledge_graph=reasoning_graph,
    graph_expansion=True,
    max_expansion_hops=3,
    decision_tracking=True,
)

reasoning_agent.load("./pipeline/enriched_intel/")
# 两个摄取智能体的全部记忆、图节点和向量嵌入现在都可用了。

# 综合步骤使用能力更强的模型
llm = LiteLLM(model="anthropic/claude-sonnet-5")

synthesis = reasoning_agent.query_with_reasoning(
    "Summarize the APT29 exploitation of CVE-2024-3400: affected products, "
    "observed TTPs, targeted sectors, and recommended mitigations.",
    llm_provider=llm,
    max_results=15,
    max_hops=3,
)

print(synthesis["response"])
print("Confidence: {:.0%}".format(synthesis["confidence"]))

# 把综合结果存回图——报告智能体稍后会取用
reasoning_agent.store(
    "SYNTHESIS: " + synthesis["response"],
    metadata={"type": "synthesis", "agent": "reasoning", "confidence": synthesis["confidence"]},
    conversation_id="synthesis-output",
)

# 把分析判断记录为一条可追溯的决策
reasoning_agent.record_decision(
    category="threat_assessment",
    scenario="APT29 active exploitation of CVE-2024-3400 in PAN-OS",
    reasoning=synthesis["reasoning_path"],
    outcome="high_priority_patch_advisory",
    confidence=synthesis["confidence"],
    entities=["APT29", "CVE-2024-3400", "GlobalProtect", "NATO"],
    decision_maker="reasoning_agent_v2",
)

# 交接给报告智能体
reasoning_agent.save("./pipeline/synthesis_output/")
```

<Info>
  `load()` 会覆盖现有上下文——加载前会先清空当前的记忆、图和向量状态。调用 `load()` 之前未保存的数据都会丢失。
</Info>

## 模式 3 —— 命名空间记忆实现角色隔离

报告智能体不需要自己的图实例。它与推理智能体共享上下文，但把写入范围限定在自己的命名空间里——`conversation_id` 充当智能体标识符，用来分隔记忆流，防止不同逻辑智能体之间互相污染。

**用 conversation_id 实现命名空间隔离：**
- `conversation_id` 在同一个 `AgentContext` 内创建相互独立的记忆命名空间
- 各智能体的记忆彼此隔离，除非显式跨命名空间查询
- 防止不同逻辑智能体处理相关但不同的任务时发生记忆串扰

```python
# 报告智能体加载综合输出
reporting_vs    = VectorStore(backend="faiss", dimension=768)
reporting_graph = ContextGraph()
reporting_agent = AgentContext(
    vector_store=reporting_vs,
    knowledge_graph=reporting_graph,
    graph_expansion=True,
)
reporting_agent.load("./pipeline/synthesis_output/")

# 取回推理智能体产出的全部内容
synthesis_items = reporting_agent.retrieve(
    "APT29 CVE-2024-3400 threat assessment synthesis",
    max_results=10,
    conversation_id="synthesis-output",   # 限定在推理智能体的输出范围内
)

# 组装最终简报
brief_sections = []
for item in synthesis_items:
    brief_sections.append(item["content"])

# 把最终报告存入报告智能体自己的命名空间
reporting_agent.store(
    "\n\n".join(brief_sections),
    metadata={"type": "finished_report", "classification": "TLP:GREEN"},  # TLP（交通灯协议，Traffic Light Protocol）——信息共享规范
    conversation_id="reporting-output",    # 报告智能体的命名空间
    user_id="reporting_agent",
)

# 完整的流水线审计轨迹：跨所有命名空间检索
full_trail = reporting_agent.retrieve("APT29 CVE-2024-3400", max_results=25)
print("Pipeline produced {} traceable context items".format(len(full_trail)))
```

按 `conversation_id` 过滤，可以单独取回每个智能体的贡献；不加过滤条件查询，则能取回全部。

## 常见陷阱

**忘记设置 conversation_id 命名空间。** 没有唯一的 `conversation_id`，不同智能体的记忆就会混在一起，无法追溯哪条洞察出自哪个智能体。务必为每个逻辑智能体使用相互区分、含义明确的会话 ID。

**load() 造成意外状态丢失。** `load()` 函数是覆盖而非合并现有上下文。`AgentContext` 里若有未保存的状态，调用 `load()` 后就会丢失。加载检查点之前，务必先保存当前状态，或改用全新的上下文。

**跨进程使用共享图模式。** 共享图模式只在单个进程内有效，前提是智能体共享对象引用。分布式智能体运行在不同容器或不同机器上时，请改用保存/加载交接模式。

**以为没有共享存储也能用保存/加载。** 不同进程、容器或机器上的智能体必须能访问同一个文件系统位置，保存/加载交接才能生效。请确保共享存储（NFS、云存储、共享卷）配置到位。

**给简单工作流强行套多智能体。** 多智能体系统会带来协调复杂度和潜在故障点。对直截了当的单步任务来说，简单的单智能体方案通常更可靠，也更容易调试。

**过度混杂智能体职责。** 每个智能体都应有清晰、专注的角色。什么活都想干的智能体享受不到专业分工的好处，优化、调试和维护都会更困难。

**忽视记忆隔离边界。** 使用命名空间记忆时，要当心跨多个 `conversation_id` 的查询。不加范围限定的查询可能意外取回其他智能体的记忆，破坏逻辑隔离。

## 领域示例

<Tabs>
<Tab title="国防——CTI/威胁情报">
一个三人情报融合小组：OSINT 采集员摄取公开情报流，HUMINT（**人力情报**(Human Intelligence)——从人力来源获取的信息）分析师导入涉密摘要，融合官把两股情报流综合成一份 PIR（**优先情报需求**(Priority Intelligence Requirement)——决策所需的关键信息）答案。OSINT 和 HUMINT 智能体在共享图上并发运行；融合官在**气隙环境**（出于安全考虑与互联网完全隔离的网络）里用独立进程加载合并后的状态。

```python
import threading
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore
from semantica.llms import HuggingFaceLLM

# 共享图，支撑多源情报(INT)并发采集
shared_graph = ContextGraph(advanced_analytics=True)
shared_vs    = VectorStore(backend="faiss", dimension=768)

osint_agent  = AgentContext(vector_store=shared_vs, knowledge_graph=shared_graph, graph_expansion=True)
humint_agent = AgentContext(vector_store=shared_vs, knowledge_graph=shared_graph, graph_expansion=True)

def osint_collection():
    osint_agent.store(
        [
            {"content": "CVE-2024-3400 confirmed exploited by APT29 against NATO member VPN gateways",
             "metadata": {"source": "NVD", "classification": "UNCLASSIFIED", "actor": "APT29"}},
            {"content": "Palo Alto PSIRT: GlobalProtect OS command injection via crafted SESSID cookie",
             "metadata": {"source": "PAN-SA-2024-0006", "classification": "UNCLASSIFIED"}},
        ],
        extract_entities=True,
        extract_relationships=True,
        conversation_id="osint-collector",
    )

def humint_analysis():
    # 在涉密环境中，HUMINT 文档来自本地涉密存储
    humint_agent.store(
        [
            {"content": "[S//NF] APT29 operator tradecraft: deploy WARPWIRE credential harvester post-exploitation of perimeter VPNs",
             "metadata": {"source": "HUMINT_Q4_2024", "classification": "SECRET//NOFORN", "actor": "APT29"}},
            {"content": "[S//NF] Target selection pattern: APT29 prioritizes Foreign Ministry and Defense Attache networks within NATO",
             "metadata": {"source": "HUMINT_Q4_2024", "classification": "SECRET//NOFORN", "actor": "APT29"}},
        ],
        extract_entities=True,
        extract_relationships=True,
        conversation_id="humint-analyst",
    )

# 多源情报并发采集——线程安全由图负责
t1 = threading.Thread(target=osint_collection)
t2 = threading.Thread(target=humint_analysis)
t1.start(); t2.start()
t1.join();  t2.join()

# 保存合并后的情报基础，供气隙段的融合官使用
osint_agent.save("./fusion/combined_intel/")

# --- 融合官（气隙段，独立进程）---
fusion_vs    = VectorStore(backend="faiss", dimension=768)
fusion_graph = ContextGraph(advanced_analytics=True)
fusion_officer = AgentContext(
    vector_store=fusion_vs,
    knowledge_graph=fusion_graph,
    graph_expansion=True,
    decision_tracking=True,
)
fusion_officer.load("./fusion/combined_intel/")

# 气隙推理：运行 NFS 共享上的本地模型
llm = HuggingFaceLLM(model="/opt/models/llama-3.1-70b-instruct")

pir_answer = fusion_officer.query_with_reasoning(
    "PIR: What is APT29's current exploitation methodology against NATO perimeter VPNs "
    "and what post-exploitation capabilities have they deployed in Q4 2024?",
    llm_provider=llm,
    max_results=20,
    max_hops=3,
)
print(pir_answer["response"])
fusion_officer.save("./fusion/pir_report/")
```

</Tab>

<Tab title="安全——SOC/事件响应">
三级安全运营中心(SOC)流水线：Tier 1 用快速的 Groq 模型给告警做分诊；Tier 1 置信度偏低时，Tier 2 用 Claude 做深度分析并升级处置；经理智能体跨所有层级通读完整的事件线程。三个层级共享一个 `ContextGraph`——每个层级用带层级前缀的 `conversation_id` 给自己的发现划命名空间。

```python
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore
from semantica.llms import Groq, LiteLLM

shared_graph = ContextGraph()
shared_vs    = VectorStore(backend="faiss", dimension=768)

def make_soc_agent() -> AgentContext:
    return AgentContext(
        vector_store=shared_vs,
        knowledge_graph=shared_graph,
        graph_expansion=True,
        decision_tracking=True,
    )

tier1   = make_soc_agent()
tier2   = make_soc_agent()
manager = make_soc_agent()

incident_id = "INC-2025-110342"

# --- Tier 1：用 Groq 快速分诊（目标 < 500ms）---
fast_llm = Groq(model="llama-3.1-8b-instant", api_key="YOUR_GROQ_KEY")

alert = (
    "Host: ws-finance-03  User: jsmith  Event: Scheduled task — base64-encoded PowerShell\n"
    "Sigma: T1053.005  Parent: wmiprvse.exe  Time: 2025-06-21T09:14:32Z"
)
tier1.store(alert, metadata={"tier": 1, "incident": incident_id})

triage = tier1.query_with_reasoning(
    "Is this a true positive? One-line verdict.",
    llm_provider=fast_llm,
    max_results=5,
)
tier1.store(
    "TIER1 VERDICT: " + triage["response"],
    metadata={"tier": 1, "incident": incident_id, "confidence": triage["confidence"]},
    conversation_id="{}-tier1".format(incident_id),
)

# --- Tier 2：Tier 1 置信度偏低时深入调查 ---
if triage["confidence"] < 0.90:
    deep_llm = LiteLLM(model="anthropic/claude-sonnet-5")

    investigation = tier2.query_with_reasoning(
        "Full MITRE ATT&CK analysis of incident {}. "
        "Identify attack chain, affected systems, blast radius, and recommended containment.".format(incident_id),
        llm_provider=deep_llm,
        max_results=15,
        max_hops=3,
    )
    tier2.store(
        "TIER2 ANALYSIS: " + investigation["response"],
        metadata={"tier": 2, "incident": incident_id},
        conversation_id="{}-tier2".format(incident_id),
    )
    tier2.record_decision(
        category="escalation",
        scenario="Escalate {} — Tier 1 confidence {:.0%}".format(incident_id, triage["confidence"]),
        reasoning=investigation["reasoning_path"],
        outcome="escalated_to_tier3",
        confidence=investigation["confidence"],
        entities=["ws-finance-03", "jsmith", "wmiprvse.exe"],
        decision_maker="tier2_analyst",
    )

# --- 经理智能体：跨所有层级通读完整事件线程 ---
full_thread = manager.retrieve(
    "incident {}".format(incident_id),
    use_graph=True,
    max_results=25,
)
print("Full incident thread ({} items):".format(len(full_thread)))
for item in full_thread:
    tier = item.get("metadata", {}).get("tier", "?")
    print("  [Tier {}] {}".format(tier, item["content"][:100]))

# 各层级历史记录，供事后复盘使用
t1_history = manager.conversation("{}-tier1".format(incident_id))
t2_history = manager.conversation("{}-tier2".format(incident_id))
```

</Tab>

<Tab title="生命科学——临床/制药">
三智能体药物发现流水线：文献智能体摄取 PubMed 论文，实验智能体导入经过验证的实验测定结果，首席智能体综合两者来挑选先导化合物。文献与实验智能体在共享图上并行运行；摄取完成后，首席智能体跨两者查询。

```python
import threading
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore
from semantica.llms import LiteLLM

shared_graph = ContextGraph(advanced_analytics=True)
shared_vs    = VectorStore(backend="faiss", dimension=768)

def make_agent() -> AgentContext:
    return AgentContext(
        vector_store=shared_vs,
        knowledge_graph=shared_graph,
        graph_expansion=True,
        max_expansion_hops=3,
        retention_days=None,      # 科研数据无限期保留
    )

lit_agent = make_agent()
exp_agent = make_agent()
chief     = make_agent()

def literature_review():
    # 摄取 KRAS G12C 抑制剂的 PubMed 摘要
    lit_agent.store(
        [
            {"content": "Sotorasib (AMG-510) achieves 37.1% ORR in KRAS G12C NSCLC (CodeBreaK 100, NEJM 2021)",
             "metadata": {"source": "CodeBreaK100", "target": "KRAS_G12C", "compound": "sotorasib"}},
            {"content": "Adagrasib (MRTX849) ORR 42.9% in KRAS G12C NSCLC with CNS activity (KRYSTAL-1, NEJM 2022)",
             "metadata": {"source": "KRYSTAL-1", "target": "KRAS_G12C", "compound": "adagrasib"}},
            {"content": "Resistance to KRAS G12C inhibitors frequently driven by Y96D mutation in switch-II pocket",
             "metadata": {"source": "Tanaka_CancerCell_2021", "target": "KRAS_G12C", "mechanism": "resistance"}},
        ],
        extract_entities=True,
        extract_relationships=True,
        conversation_id="literature-agent",
    )

def experimental_results():
    # 导入经过验证的体外与体内实验测定数据
    exp_agent.store(
        [
            {"content": "Compound RMC-6291: IC50=0.6nM KRAS G12C, selectivity index 480, in-vivo efficacy 82%, toxicity grade 1",
             "metadata": {"source": "internal_assay", "compound": "RMC-6291", "source_type": "experimental"}},
            {"content": "Compound BI-7273: IC50=1.4nM KRAS G12C, selectivity index 310, in-vivo efficacy 71%, toxicity grade 2",
             "metadata": {"source": "internal_assay", "compound": "BI-7273", "source_type": "experimental"}},
            {"content": "Compound GDC-6036: IC50=0.9nM KRAS G12C, active against Y96D resistance mutation, toxicity grade 1",
             "metadata": {"source": "internal_assay", "compound": "GDC-6036", "source_type": "experimental"}},
        ],
        extract_entities=True,
        conversation_id="experimental-agent",
    )

# 并行摄取——并发由图负责
t1 = threading.Thread(target=literature_review)
t2 = threading.Thread(target=experimental_results)
t1.start(); t2.start()
t1.join();  t2.join()

# 首席智能体跨文献与实验数据做综合
llm = LiteLLM(model="anthropic/claude-sonnet-5")

synthesis = chief.query_with_reasoning(
    "Identify the top two candidate compounds for KRAS G12C NSCLC that show "
    "both strong experimental IC50 selectivity and clinical/literature support "
    "for the target pathway, including any coverage of resistance mechanisms.",
    llm_provider=llm,
    max_results=20,
    max_hops=3,
)
print(synthesis["response"])
chief.save("./drug_discovery/kras_g12c_checkpoint/")
```

</Tab>

<Tab title="银行——风险/合规">
四智能体信贷委员会：风险台智能体计算违约概率(PD)/违约损失率(LGD)，合规台智能体核对巴塞尔协议III(Basel III)与 EBA（欧洲银行管理局）要求，信贷官智能体执行授信政策，委员会主席智能体通读三个台位的产出，给出带完整审计轨迹的最终决策。每个台位给自己的发现划命名空间；主席跨所有命名空间读取。

```python
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore
from semantica.llms import LiteLLM

shared_graph = ContextGraph(advanced_analytics=True)
shared_vs    = VectorStore(backend="faiss", dimension=768)

def make_desk_agent() -> AgentContext:
    return AgentContext(
        vector_store=shared_vs,
        knowledge_graph=shared_graph,
        graph_expansion=True,
        decision_tracking=True,
        retention_days=2555,    # Basel III 要求的 7 年留存
        kg_algorithms=True,
    )

risk_desk       = make_desk_agent()
compliance_desk = make_desk_agent()
credit_officer  = make_desk_agent()
committee_chair = make_desk_agent()

app_id = "LOAN-2025-88421"
llm    = LiteLLM(model="anthropic/claude-sonnet-5")

# --- 风险台：PD/LGD/EL 分析 ---
risk_desk.store(
    "Risk analysis {}: PD=2.3%, LGD=45%, EL=89k GBP, DSCR=1.12, LTV=78%. "
    "Stress test +300bps: DSCR falls to 0.98 — marginal but within policy floor of 0.95.".format(app_id),
    metadata={"desk": "risk", "application": app_id},
    conversation_id="{}-risk".format(app_id),
)
risk_desk.record_decision(
    category="credit_risk",
    scenario="Risk assessment {}".format(app_id),
    reasoning="PD 2.3% within 3% internal threshold; LTV 78% marginal — LMI required; stress test passes",
    outcome="conditional_approval_lmi_required",
    confidence=0.78,
    entities=[app_id, "LTV_78pct", "PD_2pct"],
    decision_maker="risk_model_v6",
)

# --- 合规台：Basel III / EBA GL 2020/06 核对 ---
compliance_desk.store(
    [
        {"content": "Basel III CRR2 Art. 92: total capital ratio minimum 8% + 2.5% conservation buffer",
         "metadata": {"source": "CRR2_Art92", "category": "capital_requirement"}},
        {"content": "EBA GL 2020/06: DSTI > 40% requires enhanced creditworthiness assessment and senior credit officer sign-off",
         "metadata": {"source": "EBA_GL_2020_06", "category": "affordability"}},
        {"content": "CRE20: LTV > 80% for residential mortgages requires LMI or equivalent credit enhancement",
         "metadata": {"source": "Basel_CRE20", "category": "collateral"}},
    ],
    extract_entities=True,
    extract_relationships=True,
)

compliance_check = compliance_desk.query_with_reasoning(
    "Does application {} (residential mortgage, LTV 78%, DSTI 35%) satisfy "
    "Basel III CRE20, EBA GL 2020/06 affordability requirements, and CRR2 Art. 92?".format(app_id),
    llm_provider=llm,
    max_results=10,
)
compliance_desk.store(
    "COMPLIANCE FINDING: " + compliance_check["response"],
    metadata={"desk": "compliance", "application": app_id, "confidence": compliance_check["confidence"]},
    conversation_id="{}-compliance".format(app_id),
)

# --- 委员会主席：跨台位综合并产出最终决策 ---
committee_decision = committee_chair.query_with_reasoning(
    "Summarize all desk findings for application {} and produce the final "
    "credit committee decision with all conditions stated explicitly.".format(app_id),
    llm_provider=llm,
    max_results=25,
    max_hops=3,
)
print(committee_decision["response"])

# 记录最终决策——这就是监管者看到的内容
committee_chair.record_decision(
    category="credit_committee",
    scenario="Final committee decision {}".format(app_id),
    reasoning=committee_decision["reasoning_path"],
    outcome="approved_with_conditions_lmi",
    confidence=committee_decision["confidence"],
    entities=[app_id, "LTV_78pct", "DSTI_35pct"],
    decision_maker="credit_committee_2025",
)

# 按台位做审计检索
risk_thread       = committee_chair.conversation("{}-risk".format(app_id))
compliance_thread = committee_chair.conversation("{}-compliance".format(app_id))

committee_chair.save("./credit_files/{}/context/".format(app_id))
```

</Tab>
</Tabs>

## 记忆隔离参考

多个智能体写入同一个共享上下文时，用 `conversation_id` 隔离各自的记忆流，并按需单独取回。

```python
# 给某条记忆打上智能体的命名空间标签
context.store("Finding: lateral movement confirmed", conversation_id="tier2-ir")

# 只取回该智能体的记忆
tier2_history = context.retrieve("lateral movement", conversation_id="tier2-ir")

# 取回某个命名空间的完整时序历史
full_history = context.conversation("tier2-ir", max_items=100)

# 删除某个智能体的整个命名空间
context.forget(conversation_id="tier2-ir")
```

同样的模式也适用于按用户隔离——把 `conversation_id` 换成 `user_id` 即可：

```python
context.store("...", user_id="analyst-jsmith")
context.retrieve("...", user_id="analyst-jsmith")
```

## 相关指南

- [智能体记忆](./agent-memory.md) — 记忆的存储、检索与持久化，以及每个智能体内部使用的工作记忆窗口
- [上下文图](./context-graphs.md) — 直接构建并遍历共享的 `ContextGraph`；时态区间推理；节点插入前的实体去重
- [决策智能](./decision-intelligence.md) — 记录并追踪跨智能体交接的决策，附带因果链分析
- [LLM 集成](./llm-integrations.md) — 配置传给每个智能体 `query_with_reasoning()` 的 LLM 提供商
