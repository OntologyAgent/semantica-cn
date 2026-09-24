---
title: "GraphRAG：图增强检索"
description: "超越向量检索：取回事实、追踪推理路径，让大语言模型的回答扎根于你的知识图谱。"
source: guides/graphrag.md
source_version: f1c84fbf1d9c1378257629236add1ff6a950a7b8
---

GraphRAG 把向量相似度与知识图谱(Knowledge Graph)遍历结合起来，让检索找到的是结构上相连的事实，而不只是听起来相关的文本。`ContextGraph` 挂到 `AgentContext` 上之后，每次检索调用都会自动把语义搜索与多跳图扩展融合，`query_with_reasoning()` 则会在大语言模型(LLM)的答案之外，返回一条可审计的推理路径。

## 什么是 GraphRAG？

GraphRAG（图增强检索增强生成）在传统检索增强生成(RAG)之上叠加知识图谱遍历。它不只检索语义相似的文本，还沿着实体之间的关系走，把散落在多篇文档中的关联证据找出来。

**GraphRAG 与纯向量 RAG 的区别**：向量 RAG 找与查询文本相似的文档；GraphRAG 既找与查询相似的文档，*也*找通过实体关系与这些文档相连的其他文档——即使后者只字未提你的查询词。

**图遍历的作用**：从向量相似文档中发现的实体出发，GraphRAG 沿关系边向外扩展，发现相关事实。纯文本相似度会漏掉的连接由此显形——比如沿"行为者 → 工具 → 受害组织 → 行业"这条路径，发现某威胁行为者在针对医疗行业。

## 为什么要用 GraphRAG？

**多跳发现。**找到距查询 2–3 步关系远的事实。问"APT29 是否针对医疗行业"，可以沿 APT29 → HAMMERTOSS → LifeCare → 医疗行业这条路径，翻出关于具体医院的证据。

**相连的证据。**检索到的不是孤立的文档碎片，而是相关实体及其关系的连贯链条。无论对 LLM 回答还是人工分析，上下文都更丰富。

**调查工作流。**从已知实体出发，沿连接向外扩展，追踪证据线索。从一个可疑 IP 入手，挖出完整基础设施链；或沿代谢通路追踪一种药物相互作用。

**更丰富的检索上下文。**图扩展能浮出关键词或语义搜索单独会漏掉的相关上下文，让 LLM 回答更完整、更准确。

**可解释性。**GraphRAG 提供审计轨迹，明确显示每条检索证据经由哪些实体和关系得出，检索过程透明、可验证。

## 适用与不适用场景

**GraphRAG 创造价值的情形：**
- 领域内实体关系丰富（威胁情报、临床数据、监管文档）
- 问题需要跨文档连接事实
- 调查工作流受益于沿实体连接追踪
- 可解释性与审计轨迹很重要
- 已有结构良好、关系有意义的知识图谱

**简单向量检索可能就够用的场景：**
- 基于主题相似度的文档检索
- 单文档问答
- 不知道要找什么的探索式搜索
- 实体关系稀少的领域

**时延与复杂度考量：**
- 图遍历带来额外计算开销
- 多跳扩展增加检索时间和 token 用量
- 图质量直接影响检索质量
- 搭建需要实体抽取和关系构建

**以下场景 GraphRAG 可能大材小用：**
- 答案就在特定文档里的简单查询
- 时延敏感的实时应用
- 实体关系提供不了额外价值的领域

## 典型 GraphRAG 工作流

**摄取 → 建图 → 检索 → 扩展上下文 → 推理 → 回答**

1. **摄取**文档：用 `AgentContext.store()` 并开启实体抽取
2. **建图**：通过命名实体识别(NER)和关系抽取填充 `ContextGraph`
3. **检索**语义相似文档，并找出作为图扩展起点的种子实体
4. **扩展上下文**：在指定跳数上限内沿实体关系扩展
5. **推理**（可选）：用推理引擎处理扩展后的上下文
6. **回答**：通过 `query_with_reasoning()` 把充实后的上下文交给 LLM

<Info>
  **图质量依赖：**GraphRAG 的检索质量高度依赖图质量、一致的实体消解和有意义的关系。糟糕的实体抽取、重复实体或薄弱的关系都会直接拖累检索效果。
</Info>

<Info>
  **上下文扩展警告：**跳数越大，检索到的上下文呈指数增长，LLM 的 token 用量和处理时间都会显著上升。从 2–3 跳起步，并针对你的场景关注上下文规模。
</Info>

<Info>
给 `AgentContext` 传入 `knowledge_graph=`，GraphRAG 即自动生效，没有单独的开关。`hybrid_alpha` 参数与 `proximity_weight` 实参控制图结构相对向量相似度的影响力大小。
</Info>

## 构建图谱并灌入情报

查询图之前，先把它建起来。配置就三个对象：一个支撑嵌入检索的向量库(Vector Store)、一个负责结构遍历的 `ContextGraph`，以及一个把两者接在一起的 `AgentContext`。

```python
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore

# FAISS 本地运行，无外部依赖
vs = VectorStore(backend="faiss", dimension=768)
graph = ContextGraph(advanced_analytics=True)

context = AgentContext(
    vector_store=vs,
    knowledge_graph=graph,
    graph_expansion=True,     # 开启从种子节点出发的多跳遍历
    max_expansion_hops=3,     # APT29 → 基础设施 → 受害者 → 行业 是 3 跳
    hybrid_alpha=0.6,         # 60% 图影响，40% 向量相似度
    decision_tracking=True,   # 把分析师查询记录为可审计的决策
)
```

接下来摄取文档。`store()` 加上 `extract_entities=True` 会在内部跑完整个抽取流水线（命名实体识别、关系抽取、实体消解），同时填充向量索引和图：

```python
intel_documents = [
    {
        "content": "APT29 deployed HAMMERTOSS malware against NATO logistics networks in Jan–Mar 2025. "
                   "C2 infrastructure used Tor exit nodes in AS59796.",
        "metadata": {"source": "FINTEL_2025_0192", "classification": "SECRET//NOFORN"},
    },
    {
        "content": "HAMMERTOSS was subsequently observed on hosts in the LifeCare hospital network "
                   "(AS64496), suggesting lateral movement beyond the initial NATO targets.",
        "metadata": {"source": "FINTEL_2025_0211"},
    },
    {
        "content": "LifeCare operates 47 acute-care hospitals and is classified as Tier-1 "
                   "healthcare critical infrastructure under CISA Sector 6.",
        "metadata": {"source": "CISA_CI_REGISTRY_2025"},
    },
    {
        "content": "Healthcare critical infrastructure has been a high-priority targeting class "
                   "for Russian state-sponsored threat actors since 2022.",
        "metadata": {"source": "NCSC_ADVISORY_2024_12"},
    },
]

stats = context.store(
    intel_documents,
    extract_entities=True,
    extract_relationships=True,
    link_entities=True,    # 合并跨文档的重复实体指称
)

print("Graph built: {} nodes, {} edges".format(
    stats["graph_nodes"], stats["graph_edges"]
))
```

`store()` 返回一个含 `stored_count`、`memory_ids`、`graph_nodes` 和 `graph_edges` 的 dict。抽取出的节点（APT29、HAMMERTOSS、LifeCare、AS59796……）和边（`deployed`、`observed_on`、`classified_as`……）就此横跨全部四篇文档。

此时图里已经有一条连通子图，跨越四篇文档的边界把 APT29 与医疗基础设施连在一起——纯向量检索对此完全无感。

## 检索相关子图

图填充完毕后，一句普通的 `retrieve()` 就已强于纯向量检索。`use_graph=True` 时，检索器以 top-k 向量匹配为种子发起图遍历，沿边向外扩展。扩展深度由 `AgentContext` 构造函数上的 `max_expansion_hops` 一处设定：

```python
results = context.retrieve(
    "APT29 tactics against healthcare",
    use_graph=True,
    max_results=10,
    expand_graph=True,
)

for r in results:
    print("[score={:.3f}]  {}".format(
        r["score"],
        r["content"][:90],
    ))

# [score=0.921]  APT29 deployed HAMMERTOSS malware against NATO...
# [score=0.887]  HAMMERTOSS was subsequently observed on hosts in the LifeCare...
# [score=0.841]  LifeCare operates 47 acute-care hospitals...
# [score=0.798]  Healthcare critical infrastructure has been a high-priority...
```

注意排名靠前的结果：纯向量搜索可能因为关键词不重叠而把这些相连事实排在后面，GraphRAG 却抬高了它们的最终 `score`——因为它们在图上与种子节点结构相邻。返回的 `score` 是向量相关度与图连通性的透明混合。

当你明确知道要把遍历锚定在哪个实体上时，传入 `anchor_node`：

```python
# 显式锚定 APT29：邻近度得分以该节点为基准计算
apt29_intel = context.retrieve(
    "C2 infrastructure beaconing patterns",
    use_graph=True,
    anchor_node="APT29",
    proximity_weight=0.7,   # 强烈偏向靠近 APT29 的节点
    max_hops=3,             # 设置锚点时，该参数限定邻近度半径
    max_results=8,
)
```

<Note>
  `retrieve()` 的 `max_hops` 只在设置了 `anchor_node` 时生效：它限定打分用的邻近度半径，并丢弃距锚点超过 `max_hops` 的结果。没有 `anchor_node` 时它会被忽略。它**不会**改变图扩展的范围：那由构造函数的 `max_expansion_hops` 固定。
</Note>

## 获取带推理路径的有据回答

`retrieve()` 给出的是有据可依的上下文。`query_with_reasoning()` 更进一步：它把这段子图上下文交给 LLM，在返回答案的同时，还附上检索系统在图中走出的多跳路径。这条路径就是你的审计轨迹。

```python
from semantica.llms import LiteLLM

llm = LiteLLM(model="anthropic/claude-sonnet-5")

result = context.query_with_reasoning(
    "What are APT29's known TTPs against healthcare infrastructure, "
    "and what is the evidence chain connecting them?",
    llm_provider=llm,
    max_results=12,
    max_hops=3,
)

# LLM 的回答，扎根于图检索到的上下文，而非训练记忆
print(result["response"])

# 多跳轨迹：APT29 → deployed → HAMMERTOSS → observed_on → LifeCare → ...
print("\n--- Reasoning Path ---")
print(result["reasoning_path"])

# 置信度反映检索到的上下文对回答的支持程度
print("\nConfidence: {:.1%}".format(result["confidence"]))

# 查看 LLM 拿到的每一个来源
print("\nSources ({} total):".format(result["num_sources"]))
for src in result["sources"]:
    print("  [{:.3f}] {}".format(src["score"], src["content"][:80]))
```

`reasoning_path` 字段正是 GraphRAG 与黑盒 LLM 调用的分野。分析师问"你怎么知道 APT29 针对医疗行业？"时，你可以展示系统在你的文档之间走出的精确遍历，而不是模型凭训练数据生成的说辞。

`query_with_reasoning()` 的完整返回结构：

```python
{
    "response":             str,   # LLM 生成的回答，扎根于检索到的子图
    "reasoning_path":       str,   # 多跳遍历的叙述
    "sources":              list,  # 带分数的检索上下文 dict 列表
    "confidence":           float, # 0–1 的综合置信度
    "num_sources":          int,
    "num_reasoning_paths":  int,
}
```

## 领域示例

<Tabs>

<Tab title="国防：CTI/威胁情报">

多源情报(Multi-INT)融合：OSINT 威胁情报流、NVD CVE 数据和 HUMINT 摘要汇入同一张图，再用多跳推理查询，追踪 C2 基础设施链并把攻击活动归因到具体行为者。

涉密环境中，图可以按数据处理限制(handling caveat)分区：每个 `AgentContext` 只在查询用户已获许可的文档子集上工作。`reasoning_path` 输出还兼作降密报告时可净化的审计轨迹。

```python
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore
from semantica.llms import LiteLLM

vs    = VectorStore(backend="faiss", dimension=768)
graph = ContextGraph()

context = AgentContext(
    vector_store=vs,
    knowledge_graph=graph,
    graph_expansion=True,
    max_expansion_hops=3,  # 行为者 → 基础设施 → 受害者 → 归因链
    hybrid_alpha=0.6,      # 偏重图：结构化情报受益于拓扑
    decision_tracking=True,
)

# 摄取多源情报语料
humint_summary = """
HUMINT-2025-Q1-007: Source BRAVO-9 confirms APT29 operating from
infrastructure in AS59796. C2 beacons use Tor exit nodes in DE/NL.
Targets: ITAR-controlled defense contractors in aerospace sector.
"""
cti_report_text = "APT29 exploited CVE-2025-3400 in PAN-OS GlobalProtect to gain initial access..."

context.store(
    [
        {"content": humint_summary,    "metadata": {"source": "HUMINT-2025-Q1-007"}},
        {"content": cti_report_text,   "metadata": {"source": "CTI_RPT_APT29_2025"}},
    ],
    extract_entities=True,
    extract_relationships=True,
    link_entities=True,
)

llm    = LiteLLM(model="anthropic/claude-sonnet-5")
result = context.query_with_reasoning(
    "Trace the C2 infrastructure chain for APT29 operations targeting "
    "ITAR-controlled contractors in 2025. Include IP ranges, ASNs, and TTPs.",
    llm_provider=llm,
    max_results=15,
    max_hops=3,
)

print(result["response"])
print("\n--- Reasoning Path ---")
print(result["reasoning_path"])
print("Confidence: {:.1%}".format(result["confidence"]))

# 锚定 APT29，做一次邻近度加权的后续检索
proximate = context.retrieve(
    "C2 beaconing patterns Tor exit nodes",
    use_graph=True,
    anchor_node="APT29",
    proximity_weight=0.7,
    max_hops=3,
    max_results=10,
)
```

</Tab>

<Tab title="安全：SOC/事件响应">

安全运营：针对一张包含主机、CVE、用户账号、响应手册和历史事件的图做实时告警分诊。GraphRAG 一次调用同时取回相关响应手册与相似历史事件，缩短平均响应时间。

`decision_tracking=True` 把每次分诊查询连同提供给 LLM 的完整上下文，一起记录为可审计的决策。事后复盘和 SOC 指标都靠它。

```python
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore
from semantica.llms import LiteLLM

vs    = VectorStore(backend="faiss", dimension=768)
graph = ContextGraph()

soc_context = AgentContext(
    vector_store=vs,
    knowledge_graph=graph,
    graph_expansion=True,
    max_expansion_hops=2,
    hybrid_alpha=0.5,
    decision_tracking=True,
    retention_days=365,
)

runbooks = [
    "RB-001: Lateral movement — isolate source host, collect memory dump, "
    "escalate if EDR alert on LSASS access.",
    "RB-002: Ransomware precursor — block C2 range, snapshot affected volumes, "
    "engage IR team within 15 minutes.",
    "RB-003: Scheduled task persistence — review parent process, check Sigma "
    "T1053.005, quarantine if encoded payload confirmed.",
]
soc_context.store(runbooks, extract_entities=True)

alert_text = """
ALERT-2025-110342 [CRITICAL]
Host: dc01.corp.internal (10.10.1.5)
User: svc_backup (DOMAIN\\svc_backup)
Event: Scheduled task created — cmd.exe /c powershell -enc <base64>
Parent: wmiprvse.exe
Sigma match: T1053.005 Scheduled Task/Job
"""

llm    = LiteLLM(model="anthropic/claude-sonnet-5")
triage = soc_context.query_with_reasoning(
    "Triage this SIEM alert and identify the correct response runbook:\n{}".format(alert_text),
    llm_provider=llm,
    max_results=8,
    max_hops=2,
)

print("TRIAGE: {}".format(triage["response"]))
# TRIAGE: Based on the wmiprvse.exe parent spawning an encoded PowerShell scheduled task,
# this matches the persistence pattern in RB-003. Recommended action: review parent process
# chain, confirm encoded payload, quarantine dc01.corp.internal if confirmed...
print("Confidence: {:.1%}".format(triage["confidence"]))

# 同时取回相似的历史事件，供分析师参考
similar = soc_context.retrieve(
    "wmiprvse.exe encoded powershell scheduled task persistence",
    use_graph=True,
    max_results=5,
)
for inc in similar:
    print("[{:.3f}] {}".format(inc["score"], inc["content"][:100]))
```

</Tab>

<Tab title="生命科学：临床/制药">

临床决策支持：FDA 药品说明书、临床指南和试验摘要汇入图中，药物-酶-代谢物-相互作用链条成为可遍历的路径。一次三跳查询（药物 → 酶 → 代谢物 → 禁忌）就能翻出任何单篇文档都不会明说的相互作用风险。

`max_expansion_hops=3` 是有意为之：从胺碘酮到华法林血药浓度升高的药代动力学链条是 药物 → CYP2C9 抑制 → 华法林代谢减弱 → 出血风险，恰好三个结构跳。

```python
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore
from semantica.llms import LiteLLM

vs    = VectorStore(backend="faiss", dimension=768)
graph = ContextGraph()

clinical_context = AgentContext(
    vector_store=vs,
    knowledge_graph=graph,
    graph_expansion=True,
    max_expansion_hops=3,  # 药物 → 酶 → 代谢物 → 相互作用
    hybrid_alpha=0.55,
    retention_days=None,   # 临床记录：不过期
)

fda_label_text = (
    "Warfarin sodium: narrow therapeutic index anticoagulant. CYP2C9 is the "
    "primary metabolic pathway. Amiodarone is a potent CYP2C9 inhibitor..."
)

guideline_text = (
    "ESC 2023 AF Guidelines: bridging therapy with heparin is not recommended "
    "for most patients with AF undergoing elective procedures..."
)

clinical_context.store(
    [
        {"content": fda_label_text,  "metadata": {"source": "FDA_WARFARIN_LABEL_2024"}},
        {"content": guideline_text,  "metadata": {"source": "ESC_AF_GUIDELINE_2023"}},
    ],
    extract_entities=True,
    extract_relationships=True,
    link_entities=True,
)

patient_context = """
Patient: 68F, AF, CKD stage 3b (eGFR 32). On warfarin (INR target 2.0–3.0).
Presenting for elective hip replacement. Concurrent: amiodarone 200mg, atorvastatin 40mg.
"""

llm    = LiteLLM(model="anthropic/claude-sonnet-5")
answer = clinical_context.query_with_reasoning(
    "What is the evidence-based warfarin bridging protocol for this patient "
    "given CKD and amiodarone interaction risk?\n\n{}".format(patient_context),
    llm_provider=llm,
    max_results=12,
    max_hops=3,
)

print(answer["response"])
print("Evidence sources: {}".format(answer["num_sources"]))
print("Reasoning hops:   {}".format(answer["num_reasoning_paths"]))

# 显式拉出禁忌链
contra_chain = clinical_context.retrieve(
    "CYP2C9 inhibition amiodarone warfarin bleeding risk",
    use_graph=True,
    anchor_node="warfarin",
    proximity_weight=0.65,
    max_hops=3,
    max_results=6,
)
```

</Tab>

<Tab title="银行：风险/合规">

监管合规：巴塞尔 III（CRE20）、BCBS 239、SR 11-7 和 EBA IRRBB 指南汇入图后，监管条款之间的交叉引用成为边。多跳查询自动穿过这些交叉引用——问一个商业地产 RWA 的问题，一次调用就能带出相关 CRE20 段落，以及支配其计算的 BCBS 239 数据质量要求。

`reasoning_path` 输出可直接充当监管机构要求的审计轨迹，证明资本计算有引用的监管文本作为依据。

```python
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore
from semantica.llms import LiteLLM

vs    = VectorStore(backend="faiss", dimension=768)
graph = ContextGraph()

compliance_context = AgentContext(
    vector_store=vs,
    knowledge_graph=graph,
    graph_expansion=True,
    max_expansion_hops=2,
    hybrid_alpha=0.5,
    retention_days=2555,   # 7 年监管留存
)

# 生产环境中文本来自解析后的文件，如 FileIngestor().ingest_file(path).text；
# 此处为简洁使用内联字符串
basel_cre20_text = (
    "CRE20.32: For income-producing real estate where repayment depends on "
    "property cash flows, RWA = exposure × risk weight, where risk weight "
    "is determined by LTV bucket per Table CRE20.3..."
)
bcbs239_text = (
    "Principle 3: Risk data should be accurate and have a single authoritative source. "
    "Where data is aggregated across systems, reconciliation must be documented..."
)

compliance_context.store(
    [
        {"content": basel_cre20_text, "metadata": {"source": "BCBS_CRE20_2024"}},
        {"content": bcbs239_text,     "metadata": {"source": "BCBS239_2013"}},
    ],
    extract_entities=True,
    extract_relationships=True,
)

llm    = LiteLLM(model="anthropic/claude-sonnet-5")
answer = compliance_context.query_with_reasoning(
    "Under Basel III CRE20, what are the RWA calculation requirements for "
    "commercial real estate exposures with LTV > 80%? "
    "Cross-reference with BCBS 239 data quality requirements.",
    llm_provider=llm,
    max_results=12,
    max_hops=2,
)

print(answer["response"])
print("Regulatory sources cited: {}".format(answer["num_sources"]))
print("Confidence: {:.1%}".format(answer["confidence"]))

# 推理路径就是审计日志：直接出示给监管机构
print("\n--- Reasoning Path (audit log) ---")
print(answer["reasoning_path"])
```

</Tab>

</Tabs>

## 常见误区

**跳数过大。**`max_expansion_hops` 设得太高（>4）会生成指数级膨胀的上下文，既压垮 LLM 又抬高成本。从 2–3 跳起步，确有需要再加大。

**图质量差。**GraphRAG 会放大图质量问题。实体重复、命名不一致、关系薄弱都会产生糟糕的检索结果。把重要查询托付给 GraphRAG 之前，先清洗图数据。

**实体重复。**"APT-29"、"APT29" 和 "Cozy Bear" 各立节点会破坏关系遍历。摄取时做实体消解有帮助，但可能仍需手工去重。

**拿 GraphRAG 做简单查询。**明知答案在特定文档里、只需取回时，传统向量检索比 GraphRAG 更快更简单。

**以为图扩展总是有益。**上下文并非越多越好。有时精准聚焦的检索胜过大范围图扩展。针对你的具体场景把两种方式都测一测。

## 调节向量与图的配比

`AgentContext` 构造函数里的 `hybrid_alpha` 参数设定向量相似度与图影响力的默认配比。`0.0` 是纯向量检索，`1.0` 是纯图遍历，推荐起步值是 `0.5`。

锚定特定 `anchor_node` 时，可以在 `retrieve()` 里使用 `proximity_weight`，把与锚点的结构距离动态混入最终得分：

```python
# 提供了锚点：让向量语义主导，图邻近度只轻微加分
results = context.retrieve(
    query, use_graph=True, anchor_node="APT29", proximity_weight=0.2
)

# 已知实体追踪：拓扑驱动检索
results = context.retrieve(
    query, use_graph=True, anchor_node="APT29", proximity_weight=0.8
)
```

扩展每多一跳，子图规模就指数级增大。各领域的实用默认值：

```text
General Q&A             max_expansion_hops=2  (95% of useful facts within 2 hops)
Threat intel (APT)      max_expansion_hops=3  (actor → infra → victim → attribution)
Drug interactions       max_expansion_hops=3  (drug → enzyme → metabolite → interaction)
Regulatory cross-ref    max_expansion_hops=2  (rule → article → article)
```

扩展深度只能在构造函数里设定（`max_expansion_hops`），`retrieve()` 没有逐调用覆盖。`query_with_reasoning()` 则接受逐调用的 `max_hops` 实参。

## GraphRAG 的内部原理

```text
Query text
    |
    v
Vector embedding  ─────────────────────────────────────┐
    |                                                   |
    v                                                   v
Semantic search                         Graph traversal (BFS)
(FAISS / Qdrant)                        from anchor / top-k seeds
    |                                                   |
    └──────────┐                ┌──────────────────────┘
               v                v
         Score fusion (proximity_weight blend)
               |
               v
          Ranked subgraph
               |
               v
         LLM grounding  <── query_with_reasoning()
               |
               v
     {response, reasoning_path, sources, confidence}
```

向量搜索与图遍历各自独立运行，之后融合分数。图遍历从向量搜索找出的种子节点做广度优先扩展，因此图这一侧始终锚定在语义相关性上，而不是盲目探索整张图。

## 相关指南

- [语义抽取](./semantic-extraction.md)：从原始非结构化文本建图
- [智能体记忆](./agent-memory.md)：存储、检索与持久化智能体记忆
- [上下文图](./context-graphs.md)：直接构建与遍历知识图谱
- [推理](./reasoning.md)：在图上推导新事实、运行推理规则
- [决策智能](./decision-intelligence.md)：因果链、策略执行与决策追踪
- [LLM 集成](./llm-integrations.md)：连接 Groq、OpenAI、Anthropic、HuggingFace 等 100 多家提供商
