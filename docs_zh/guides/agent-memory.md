---
title: 智能体记忆
description: AgentContext 如何存储、检索并管理持久化的智能体记忆——分层短期/长期记忆、FAISS 语义检索、图增强上下文与跨会话持久化，适用于国防、安全、临床与金融等部署场景。
source: guides/agent-memory.md
source_version: 738f7b82b4b641ab0b3cc40370215c1d9686639b
icon: "brain"
---

`AgentContext` 为大语言模型(LLM)智能体(Agent)维护一层持久化记忆——把观察结果保存为嵌入(Embedding)向量，按语义相似度检索，并可选地把图邻近度融入排序。当你的智能体需要跨会话回忆过去的发现、而不是每次重启都重读源材料时，就用它。

## 什么是智能体记忆？

智能体记忆(Agent Memory)提供跨多个智能体会话的持久化存储与智能检索。`AgentContext` 是编排记忆存储、检索与管理的核心组件，它组合了三个关键系统：

**`VectorStore`** 负责基于向量嵌入的语义搜索。它把文本存成高维向量，再通过余弦相似度或其他距离度量找回相似内容。

**`ContextGraph`** 以节点（实体）和边（关系）的形式维护结构化知识。有了它，检索就能沿着相关实体之间的连接做多跳遍历，具备图感知能力。

**`AgentContext`** 编排上述两个组件，提供统一接口：存储记忆、检索相关上下文、跨会话管理对话。

**持久化记忆 vs 无状态检索：** 传统的检索增强生成(RAG)系统在会话之间会丢失上下文。智能体记忆则把学到的信息、对话历史和积累的知识在重启之后保留下来，从而支持长期记忆与跨会话回忆。

## 为什么用智能体记忆？

**跨会话回忆。** 智能体记得此前的交互、发现和决策，重启后无需重新处理源材料。

**长期知识积累。** 随着智能体处理更多文档，信息不断沉淀，为未来的查询构建日益丰富的知识库。

**对话历史。** 智能体在对话中保持上下文，可以引用长周期交互或调查中更早的内容。

**图感知检索。** 不止于简单的语义相似度：检索会沿着实体关系找到纯向量搜索漏掉的关联信息。

**决策追踪。** 连同完整上下文和推理路径一起记录决策，既为审计留下依据，也为将来的类似场景匹配先例。

## 适用与不适用场景

**适合用智能体记忆的场景：**
- 需要长期积累知识的长时间运行智能体
- 跨多个会话逐步建立理解的科研助手
- 上下文需要渐进式积累的调查工作流
- 必须记住此前交互与决策的系统
- 需要审计轨迹和决策先例的场景

**不适合的场景：**
- 构建面向一次性文档查询的简单无状态 RAG 系统
- 执行无需持久化的一次性文档搜索
- 运行不需要知识保留的临时实验
- 实体之间的关系无关紧要的简单检索任务

<Info>
  本指南聚焦记忆层。图增强的遍历与实体消解(Entity Resolution)见[上下文图](./context-graphs.md)。决策问责——记录、审计并因果追溯智能体的选择——见[决策智能](./decision-intelligence.md)。
</Info>

## 搭建持久化记忆上下文

启动时把向量库、知识图谱和 `AgentContext` 配置在一起，让三个组件持久化到同一路径。

```python
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore

# VectorStore 依赖显式的 save()/load() 实现持久化
ti_vs = VectorStore(
    backend="faiss",
    dimension=768,
)

# ContextGraph 保存实体节点及其关系
ti_graph = ContextGraph(advanced_analytics=True)

# AgentContext 负责统筹一切
ti_agent = AgentContext(
    vector_store=ti_vs,
    knowledge_graph=ti_graph,
    retention_days=365,          # CTI 报告的有效期为一年
    max_memories=50000,          # 环形缓冲区上限——最旧的先被逐出
    graph_expansion=True,        # 在 retrieve() 中启用多跳图遍历
    max_expansion_hops=2,
    hybrid_alpha=0.5,            # 50% 语义得分 / 50% 图结构得分
    decision_tracking=True,      # 启用 record_decision() 和 find_precedents()
    kg_algorithms=True,          # Node2Vec 嵌入、中心性、链接预测
)
```

`hybrid_alpha` 参数控制检索如何在语义相似度（纯向量搜索）与图结构相似度（知识图谱的拓扑）之间做混合。取 `0.5` 表示两种信号等权。对一个刚摄取、图还很稀疏的语料库，可以从接近 `0.0` 的值起步，随着图逐渐填满再调高。

## 存储智能体学到的内容

### 单条观察

智能体处理的每一条情报都可以一次调用存入。字符串会被立刻嵌入并建立索引；可选的元数据随行保存，并出现在每一次检索结果里。

```python
# 存储来自开源情报(OSINT)源的一条发现
memory_id = ti_agent.store(
    "APT29 uses HAMMERTOSS for C2 communication over Twitter and GitHub",
    metadata={
        "source": "mandiant_apt29_report",
        "actor": "APT29",
        "technique": "T1102",   # Web Service
        "tlp": "WHITE",
    },
)
# memory_id 是一个 UUID 字符串——之后用它检索或删除这条记忆

# 把观察挂到正在处置的事件上，便于日后按组检索
ti_agent.store(
    "New C2 indicator: c2-upd4te[.]ru resolves to 185.220.101.47, cert hash a3f4b8c1...",
    metadata={"type": "ioc", "confidence": 0.92, "source": "internal_hunt"},
    conversation_id="incident_ir2025_0847",
    user_id="analyst_zhang",
)
```

`conversation_id` 充当命名空间。挂上 `incident_ir2025_0847` 标签的记忆之后可以按组检索——这对构建按事件隔离的上下文窗口很有用，又不会污染全局搜索索引。

### 摄取文档语料

当 `store()` 收到列表时，它把每个元素当作一篇文档，从文本中抽取实体和关系并构建图，然后返回创建内容的统计信息。

```python
stats = ti_agent.store(
    [
        {
            "content": "APT29 infrastructure cluster: 185.220.101.0/24, AS200651",
            "metadata": {"source": "shadowserver", "actor": "APT29", "ioc_type": "network"},
        },
        {
            "content": "SolarWinds supply chain compromise attributed to APT29, 2020",
            "metadata": {"source": "us_cert_aa20-352a", "actor": "APT29", "campaign": "SUNBURST"},
        },
        {
            "content": "NOBELIUM (APT29) leverages OAuth token theft against cloud workloads",
            "metadata": {"source": "msft_blog_2023", "actor": "APT29", "technique": "T1528"},
        },
    ],
    extract_entities=True,       # 抽取行为者、IP、CVE、技术等节点
    extract_relationships=True,  # 串联 行为者 → 活动 → 技术 → 基础设施
    link_entities=True,          # 合并跨文档的重复实体指称
)

print("Stored: {}, Graph nodes: {}, Graph edges: {}".format(
    stats["stored_count"],   # 3 — one per document
    stats["graph_nodes"],    # entities extracted and upserted into the graph
    stats["graph_edges"],    # relationships between those entities
))
```

这次调用之后，知识图谱中就有了 APT29、HAMMERTOSS、基础设施网段、SUNBURST 活动和 OAuth 令牌窃取的节点——彼此相互连接。正是这些图上的连接支撑了多跳检索：问一句"云上 OAuth 攻击"，智能体就能沿着图从技术节点回溯到 APT29，再前进到基础设施指标。

## 检索相关记忆

### 语义检索

最直接的检索调用按语义相似度搜索——不需要关键词匹配。查询文本的嵌入会与所有已存记忆的嵌入比对，返回得分最高的匹配项。

```python
results = ti_agent.retrieve(
    "cloud OAuth token theft campaigns",
    max_results=8,
    min_score=0.2,
)

for r in results:
    actor = r.get("metadata", {}).get("actor", "unknown")
    print("[{:.3f}]  [{}]  {}".format(r["score"], actor, r["content"][:80]))

# [0.912]  [APT29]  NOBELIUM (APT29) leverages OAuth token theft against cloud workloads
# [0.741]  [APT29]  SolarWinds supply chain compromise attributed to APT29, 2020
# [0.683]  [APT29]  APT29 infrastructure cluster: 185.220.101.0/24, AS200651
```

智能体把 OAuth 那条发现排在了最前——不是因为查询里含有完全一致的短语，而是因为在嵌入空间里，"cloud OAuth token theft campaigns" 与 "NOBELIUM leverages OAuth token theft against cloud workloads" 彼此靠近。

### 以图为锚的邻近度检索

当调查已有明确的中心实体时，把检索锚定到该节点，并将语义得分与图邻近度得分混合。

```python
results = ti_agent.retrieve(
    "cloud OAuth token theft campaigns",
    max_results=10,
    use_graph=True,
    anchor_node="APT29",      # 广度优先搜索(BFS)从知识图谱中的这个节点出发
    max_hops=3,
    proximity_weight=0.35,    # 65% 语义 + 35% 邻近度——按图的密度调参
    min_score=0.1,
)

for r in results:
    # combined_score 混合语义得分与图邻近度
    score = r.get("combined_score", r["score"])
    hop  = r.get("hop_distance", "-")
    band = r.get("distance_band", "-")  # "direct", "near", "mid-range", "distant"
    print("[{:.3f}]  hop={}  band={}  {}".format(score, hop, band, r["content"][:70]))
```

`proximity_weight` 是逐次调用可覆盖的参数——围绕特定行为者展开追查时可以加大邻近度权重，大范围探索时再退回纯语义搜索。

### 基于图证据的推理

当你需要一条综合多条记忆的自然语言答案时，用 `query_with_reasoning()` 从图中检索上下文，并让大语言模型把答案落在这些来源上。

```python
from semantica.llms import Groq

llm = Groq(model="llama-3.1-8b-instant", api_key="YOUR_GROQ_KEY")

result = ti_agent.query_with_reasoning(
    "Which threat actors are associated with SMB lateral movement in EMEA "
    "and what infrastructure do they share with cloud OAuth campaigns?",
    llm_provider=llm,
    max_results=15,
    max_hops=3,
)

print(result["response"])       # 有据可依的自然语言答案
print(result["confidence"])     # 聚合的检索置信度

# 查看答案所依据的来源
for src in result["sources"]:
    print("  -", src["content"][:60])
```

返回结果包含 `reasoning_path` 字段，精确记录了为得出答案经过了哪些图的边——便于分析师复核与审计。

## 构建工作记忆窗口

用 `conversation_id` 过滤器把检索范围限定在当前会话，把事件范围的历史与全局语义搜索结合起来。

```python
incident_id = "ir2025_0847"

# 每条新告警到达时即存入，并挂到该事件上
ti_agent.store(
    "Alert: lateral movement detected from WKSTN-047 to DC01 via SMB (PsExec artifact)",
    metadata={"type": "alert", "severity": "critical", "technique": "T1021.002"},
    conversation_id=incident_id,
    user_id="analyst_zhang",
)

ti_agent.store(
    "Analyst note: WKSTN-047 user jsmith flagged for suspicious login from 10.2.5.40 at 03:14 UTC",
    metadata={"type": "analyst_note"},
    conversation_id=incident_id,
    user_id="analyst_zhang",
)

# 检索完整的事件脉络
incident_history = ti_agent.conversation(
    incident_id,
    max_items=50,
    reverse=False,          # chronological order
    include_metadata=True,
)

for item in incident_history:
    role = item["metadata"].get("type", "note")
    print("[{}] {}".format(role, item["content"][:80]))

# 把事件范围内的历史与跨全局记忆的语义搜索结合起来
context_items = ti_agent.retrieve(
    "SMB lateral movement PsExec domain controller",
    max_results=5,
    use_graph=True,
    conversation_id=incident_id,  # 只过滤该事件的记忆
)
```

这种模式让智能体为每个事件构建聚焦的工作记忆窗口，同时全局向量索引随时间积累跨所有事件的知识。

## 领域示例

<Tabs>
<Tab title="国防——CTI/威胁">
威胁情报融合单元持续摄取 OSINT 源、MISP 事件和内部威胁狩猎发现。智能体必须把新指标与已知行为者画像做关联，并产出有积累情报支撑——而不只是最新一份报告——的归因评估。

```python
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore
from semantica.llms import Groq

ti_graph = ContextGraph(advanced_analytics=True, node_embeddings=True)
ti_agent = AgentContext(
    vector_store=VectorStore(backend="faiss", dimension=768),
    knowledge_graph=ti_graph,
    retention_days=365,
    max_memories=50000,
    hybrid_alpha=0.6,
    decision_tracking=True,
)

# 摄取一份新的 CTI 报告——实体和基础设施流入图
ti_agent.store(
    [
        {"content": "APT29 infrastructure cluster: 185.220.101.0/24, AS200651",
         "metadata": {"source": "shadowserver", "actor": "APT29", "tlp": "WHITE"}},
        {"content": "SolarWinds supply chain compromise attributed to APT29, campaign SUNBURST",
         "metadata": {"source": "us_cert_aa20-352a", "actor": "APT29", "campaign": "SUNBURST"}},
        {"content": "NOBELIUM (APT29) leverages OAuth token theft against cloud workloads",
         "metadata": {"source": "msft_blog_2023", "actor": "APT29", "technique": "T1528"}},
    ],
    extract_entities=True,
    extract_relationships=True,
)

# 新的狩猎发现——这个 C2 域名与 APT29 有关吗？
ti_agent.store(
    "New C2 indicator: c2-upd4te[.]ru resolves to 185.220.101.47, cert hash a3f4b8...",
    metadata={"type": "ioc", "confidence": 0.92, "source": "internal_hunt"},
    conversation_id="hunt_2025_q3",
)

# 图锚定的归因查询：从 APT29 出发，遍历 3 跳
llm = Groq(model="llama-3.1-8b-instant", api_key="YOUR_GROQ_KEY")
attribution = ti_agent.query_with_reasoning(
    "Is c2-upd4te[.]ru connected to APT29 based on infrastructure overlap?",
    llm_provider=llm,
    max_results=10,
    max_hops=3,
)
print(attribution["response"])
print("Confidence: {:.0%}".format(attribution["confidence"]))

# 情报库跨分析员班次持久保存
ti_agent.save("ti_state/")
```

</Tab>
<Tab title="安全——SOC/事件响应">
SOC 分析师助手在交接班之间延续上下文。Tier 1 记录初始告警与分诊结论；Tier 2 接手时完整的事件历史已经就位，无需回溯工单记录。智能体会给出相关的响应手册(runbook)步骤，并找出类似的历史事件来估算平均解决时长(MTTR)。

```python
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore
from semantica.llms import Groq

soc_graph = ContextGraph()
soc_agent = AgentContext(
    vector_store=VectorStore(backend="faiss", dimension=768),
    knowledge_graph=soc_graph,
    retention_days=180,
    max_memories=100000,
    decision_tracking=True,
)

# 一次性预载响应手册知识库——重启后依然保留
soc_agent.store([
    "T1021.002 (SMB/Windows Admin Shares): isolate host, reset service accounts, check for credential dumping",
    "T1003.001 (LSASS Memory): collect memory dump, run Mimikatz signatures, notify IR team",
    "T1190 (Exploit Public-Facing Application): check WAF logs, correlate with CVE feed, patch window 4h",
])

incident_id = "ir-2025-0847"

# Tier 1 记录告警
soc_agent.store(
    "Alert: host WKSTN-047 failed 14 Kerberos AS-REQ in 30s from 10.2.5.40",
    metadata={"type": "alert", "severity": "high", "technique": "T1110.003"},
    conversation_id=incident_id,
    user_id="tier1_chen",
)
soc_agent.store(
    "Lateral movement confirmed: 10.2.5.40 connected to DC01 via PsExec",
    metadata={"type": "finding", "severity": "critical", "technique": "T1021.002"},
    conversation_id=incident_id,
    user_id="tier1_chen",
)

# 记录遏制决策，供审计与先例匹配
decision_id = soc_agent.record_decision(
    category="containment",
    scenario="Confirmed lateral movement from WKSTN-047 to DC01 via SMB",
    reasoning="PsExec artifact detected; immediate isolation prevents DC compromise",
    outcome="isolated_wkstn047",
    confidence=0.95,
    entities=["WKSTN-047", "DC01"],
    decision_maker="tier1_chen",
)

# 给出匹配的响应手册步骤
runbook = soc_agent.retrieve(
    "SMB lateral movement with PsExec to domain controller",
    max_results=3,
    use_graph=True,
)
for step in runbook:
    print("[{:.3f}] {}".format(step["score"], step["content"]))

# 查找类似的历史事件——Tier 2 用它们估算处置时长
precedents = soc_agent.find_precedents(
    "lateral movement SMB domain controller compromise",
    category="containment",
    limit=3,
)
for p in precedents:
    print("Past: {} -> {} ({:.0%})".format(p.scenario[:50], p.outcome, p.confidence))

# Tier 2 无需读工单即可加载完整事件上下文
soc_agent.save("soc_state/")
```

</Tab>
<Tab title="生命科学——临床/制药">
临床决策支持智能体在多次问诊之间维护患者上下文，并把治疗史延续下去。在开具处方前，智能体会提示指南中的禁忌；随后记录决策，附带完整的因果追溯，供多学科团队(MDT)审计。

```python
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore

clinical_graph = ContextGraph(advanced_analytics=True)
clinical_agent = AgentContext(
    vector_store=VectorStore(backend="faiss", dimension=768),
    knowledge_graph=clinical_graph,
    retention_days=3650,      # 10-year clinical record retention
    max_memories=500000,
    decision_tracking=True,
)

# 一次性载入指南——ADA、BNF、NICE——跨会话保留
clinical_agent.store([
    {"content": "ACE inhibitors are first-line for hypertension in diabetic patients (ADA 2024)",
     "metadata": {"source": "ADA_2024", "category": "guideline", "strength": "A"}},
    {"content": "Metformin contraindicated in eGFR < 30 mL/min/1.73m2 — risk of lactic acidosis",
     "metadata": {"source": "BNF_2024", "category": "contraindication", "strength": "absolute"}},
    {"content": "SGLT2 inhibitors reduce cardiovascular events in T2DM with CKD stage 3a (CREDENCE trial)",
     "metadata": {"source": "NEJM_CREDENCE", "category": "guideline", "strength": "A"}},
], extract_entities=True, extract_relationships=True)

patient_id = "PT-00841"

# 为本次问诊构建患者上下文
clinical_agent.store(
    "Patient PT-00841: T2DM, hypertension, eGFR 28 mL/min/1.73m2, no penicillin allergy",
    metadata={"type": "patient_summary", "patient_id": patient_id},
    conversation_id="consult_2025_07_01",
    user_id="dr_okonkwo",
)
clinical_agent.store(
    "Current medications: lisinopril 10mg, atorvastatin 40mg, aspirin 75mg",
    metadata={"type": "medication_list", "patient_id": patient_id},
    conversation_id="consult_2025_07_01",
)

# 开具二甲双胍之前——先查指南库
contraindications = clinical_agent.retrieve(
    "metformin prescribing with reduced kidney function eGFR",
    max_results=5,
    use_graph=True,
    conversation_id="consult_2025_07_01",
)
for item in contraindications:
    category = item.get("metadata", {}).get("category", "?")
    print("[{:.3f}]  [{}]  {}".format(item["score"], category, item["content"][:80]))
# [0.947]  [contraindication]  Metformin contraindicated in eGFR < 30 mL/min/1.73m2 ...
# [0.821]  [guideline]         SGLT2 inhibitors reduce cardiovascular events in T2DM with CKD ...

# 记录决策——eGFR 28 已低于绝对禁忌阈值
decision_id = clinical_agent.record_decision(
    category="treatment_modification",
    scenario="T2DM patient PT-00841 eGFR 28: metformin dose review required",
    reasoning=(
        "eGFR 28 falls below absolute contraindication threshold of 30 mL/min/1.73m2 "
        "per BNF_2024. Discontinue metformin; initiate dapagliflozin review per CREDENCE."
    ),
    outcome="discontinued_metformin_initiated_dapagliflozin_review",
    confidence=0.97,
    entities=["PT-00841", "metformin", "dapagliflozin", "eGFR"],
    decision_maker="dr_okonkwo",
)

# 供 MDT 审计的可解释性轨迹
explanation = clinical_agent.trace_decision_explainability(decision_id)
print("Guideline connections traced: {}".format(explanation.get("total_connections", 0)))

clinical_agent.save("clinical_state/{}/".format(patient_id))
```

</Tab>
<Tab title="银行——风险/合规">
抵押贷款承保智能体在决策流程中携带监管知识和申请上下文。每一笔信贷决策都记录了据以做出的确切监管指引，为模型风险治理审查产出经得起质询的审计轨迹。

```python
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore

credit_graph = ContextGraph(advanced_analytics=True)
credit_agent = AgentContext(
    vector_store=VectorStore(backend="faiss", dimension=768),
    knowledge_graph=credit_graph,
    retention_days=2555,      # 7-year regulatory retention
    max_memories=1000000,
    decision_tracking=True,
    kg_algorithms=True,
)

# 载入监管知识库——Basel III、CRR、EBA 指南
credit_agent.store([
    {"content": "Basel III: CET1 capital ratio minimum 4.5% + 2.5% conservation buffer",
     "metadata": {"source": "BCBS_Basel3", "category": "capital_requirement"}},
    {"content": "PD floor for retail exposures: 0.1% under IRB approach (CRR Art. 160)",
     "metadata": {"source": "CRR_Art160", "category": "risk_parameter"}},
    {"content": "DSTI ratio > 40% requires enhanced creditworthiness assessment per EBA GL 2020/06",
     "metadata": {"source": "EBA_GL_2020_06", "category": "affordability"}},
    {"content": "Adverse action notice required within 30 days of credit denial (ECOA Reg. B)",
     "metadata": {"source": "ECOA_RegB", "category": "regulatory_obligation"}},
], extract_entities=True, extract_relationships=True)

app_id = "APP-2025-994421"

# 载入申请上下文
credit_agent.store(
    "Applicant APP-2025-994421: gross income 82000 GBP, requested 320000 GBP 30yr mortgage, LTV 78%",
    metadata={"type": "application_summary", "app_id": app_id},
    conversation_id=app_id,
)
credit_agent.store(
    "Credit bureau: score 714, 0 defaults in 7yr, 2 hard inquiries last 12mo, DSTI 38%",
    metadata={"type": "bureau_data", "app_id": app_id},
    conversation_id=app_id,
)

# 检索与本申请相关的监管指引
guidance = credit_agent.retrieve(
    "mortgage affordability DSTI 38% regulatory requirements LTV 78%",
    max_results=5,
    use_graph=True,
    conversation_id=app_id,
)
for g in guidance:
    source = g.get("metadata", {}).get("source", "?")
    print("[{:.3f}]  [{}]  {}".format(g["score"], source, g["content"][:80]))
# [0.891]  [EBA_GL_2020_06]  DSTI ratio > 40% requires enhanced creditworthiness ...
# [0.724]  [CRR_Art160]      PD floor for retail exposures: 0.1% under IRB approach ...

# 记录决策——DSTI 38% 低于 EBA 的 40% 阈值
decision_id = credit_agent.record_decision(
    category="mortgage_origination",
    scenario="320k GBP 30yr mortgage, LTV 78%, DSTI 38%, credit score 714",
    reasoning=(
        "Score 714 exceeds 680 floor; DSTI 38% within EBA GL 2020/06 threshold of 40%; "
        "LTV 78% requires standard LMI; no derogatory history in 7yr; "
        "stress test at +300bps passes affordability."
    ),
    outcome="approved_conditional_lmi",
    confidence=0.89,
    entities=[app_id, "LTV_78pct", "DSTI_38pct"],
    decision_maker="underwriting_model_v4",
)

# 为模型治理审查查找类似先例
precedents = credit_agent.find_precedents(
    "mortgage approval borderline DSTI affordability stress test",
    category="mortgage_origination",
    limit=5,
)
for p in precedents:
    print("Precedent: {} -> {} ({:.0%})".format(p.scenario[:50], p.outcome, p.confidence))

credit_agent.save("credit_state/{}/".format(app_id))
```

</Tab>
</Tabs>

## 持久化与恢复状态

在分析员轮班结束——或进程重启之前——调用 `save()` 把完整上下文写入磁盘。下次启动时调用 `load()` 完整还原。

```python
# save() 写入记忆 JSON 以及后端专属的向量库工件，
# 存放在 agent_state/vector_store/ 下，图导出位于 knowledge_graph.json。
# 使用默认 VectorStore 实现时包括：
#   agent_state/agent_memory.json
#   agent_state/vector_store/store_data.pkl
#   agent_state/vector_store/index.bin
#   agent_state/knowledge_graph.json
ti_agent.save("agent_state/")
```

新进程启动——或新分析员登录——时，从该检查点(Checkpoint)恢复：

```python
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore

# 创建配置匹配的全新上下文
ti_agent_restored = AgentContext(
    vector_store=VectorStore(backend="faiss", dimension=768),
    knowledge_graph=ContextGraph(advanced_analytics=True),
    retention_days=365,
    decision_tracking=True,
)

# load() 从磁盘还原全部三个组件
ti_agent_restored.load("agent_state/")

# 现在每条记忆、每条图的边、每个决策先例都可用
results = ti_agent_restored.retrieve("APT29 OAuth token theft cloud infrastructure")
```

<Info>
  `AgentMemory` 本身以 JSON 保存，但向量库会单独持久化自己的索引和向量数据。`load()` 还原的是这些后端工件，而不是按需重新嵌入记忆，因此跨会话请保持相同的向量库后端、维度和打分配置。
</Info>

## 分析过程中的检查点

长时间运行的分析循环，可以在关键步骤前后打命名快照，以便对比智能体在每个阶段新增了什么。

```python
# 分析循环开始前打快照
ti_agent.checkpoint("pre_enrichment")

# ... 存入新证据、抽取实体、记录决策 ...

# 富集完成后打快照
ti_agent.checkpoint("post_enrichment")

# 精确查看变化
diff = ti_agent.diff_checkpoints("pre_enrichment", "post_enrichment")
print("Decisions added:     {}".format(len(diff["decisions_added"])))
print("Relationships added: {}".format(len(diff["relationships_added"])))

# 可选：通过 TemporalVersionManager 持久化（初始化时需传 temporal_version_manager=）
# ti_agent.flush_checkpoint("post_enrichment")
```

## 记忆生命周期与日常维护

保留策略在每次 `store()` 调用时自动生效——超过 `retention_days` 的条目会被修剪，无需人工干预。你也可以删除特定记忆，或清空整个对话命名空间。

```python
# 按 ID 忘掉一条特定记忆
ti_agent.forget(memory_id="some-uuid-string")

# 清空挂到某事件上的全部记忆
cleared = ti_agent.forget(conversation_id="incident_ir2025_0847")
print("Cleared {} items".format(cleared))

# 清空 90 天前的所有内容
old_cleared = ti_agent.clear(days_old=90)

# 获取当前记忆统计
s = ti_agent.stats()
print("Total memories: {}".format(s.get("total_items", 0)))
```

## 常见陷阱

**停机前忘记持久化记忆。** 智能体记忆在运行期间存放在内存里。进程终止前不调用 `save()`，积累的记忆、图关系和对话会全部丢失。

**给无关任务用同一个对话命名空间。** 对话 ID 应当用来圈定相关交互。多项无关调查共用一个对话，会污染检索结果，让上下文失焦。

**存入过多低价值信息。** 并非每条观察都值得永久保存。聚焦于洞见、决策和重要发现，而不是冗长的原始日志或临时计算。

**简单检索就够时却用了智能体记忆。** 对于一次性文档查询或无状态请求，传统检索比搭建持久化记忆基础设施更简单、更高效。

**检索过多上下文推高延迟。** 过大的 `max_results`、过高的 `max_hops` 或过宽的查询会取回过量上下文，推高大语言模型的 token 用量和响应延迟。从聚焦的检索参数起步。

## 相关指南

- [上下文图](./context-graphs.md) — 底层 `ContextGraph` 如何存储实体节点与决策节点；时态区间推理；节点插入前去重；从图生成本体。
- [决策智能](./decision-intelligence.md) — 把决策连同因果链与策略门控记录为图节点。
- [多智能体系统](./multi-agent.md) — 通过共享的 `AgentContext` 协调多个智能体，并用 save/load 交接。
- [LLM 集成](./llm-integrations.md) — 配置传给 `query_with_reasoning()` 的大语言模型提供商。
- [去重指南](./deduplication.md) — `DuplicateDetector`、`EntityMerger`、相似度方法与聚类策略的完整参考。
- [本体管理](./ontology.md) — 从知识图谱生成并校验 OWL 本体；导出 Turtle、OWL/XML、JSON-LD。
- [上下文模块参考](../reference/context.md) — 完整 API：`AgentContext`、`AgentMemory`、`MemoryItem`、`ContextRetriever`。
- [向量库参考](../reference/vector_store.md) — FAISS、Qdrant、pgvector、Pinecone 后端。
