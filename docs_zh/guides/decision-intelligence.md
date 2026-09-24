---
title: "决策智能"
description: "Semantica 如何把 AI 智能体的决策作为一等知识图谱对象记录、存储、追踪并查询——带因果链、先例检索、策略执行与完整可解释性。"
source: guides/decision-intelligence.md
source_version: 1c8505cd7b967864b9ff3946897662cc8999a839
icon: "scale-balanced"
---

`AgentContext.record_decision()` 把每个 AI 决策存成知识图谱里的节点，用因果边把它与之前的决策、之后的结果连起来。用它可以构建一条可审计的推理轨迹——半年之后仍能精确还原：哪个分类引发了哪次升级，记录之前又校验过哪条策略。

## 什么是决策智能？

决策智能(Decision Intelligence)把智能体(Agent)自己的决策作为结构化数据记录下来并加以分析——这些数据可以被查询、分析、复用。决策不再执行完就消失，而是变成持久的图节点，带可检索的元数据、推理链和因果关系。

**决策智能记录决策**：为智能体做出的每个选择捕获场景、推理、结果、置信度和决策者。这些决策成为知识图谱中可查询的节点。

**决策成为图节点**之后，可以按因果相连（决策 A 导致决策 B）、按相似度搜索（找出与当前场景相似的决策）、做统计分析（置信度趋势、常见结果）。

**目标是可审计、可解释、先例检索和因果追溯。**你可以追溯决策为何做出，查找相似的过往决策以保持一致，并理解从初始检测到最终行动的完整因果链(causal chain)。

**决策智能与智能体记忆(Agent Memory)**：智能体记忆存的是外部知识（文档、事实、观察）；决策智能存的是内部决策（智能体自己做出的分类、审批、行动）。

**决策智能与推理**：推理用逻辑规则从既有数据推导新事实；决策智能记录的是智能体在解决问题过程中做出的选择与判断。

**决策智能与图分析**：图分析分析知识图谱的结构属性；决策智能聚焦决策过程本身及其审计轨迹。

## 为什么要用决策智能？

**AI 行为可审计。**每个决策都连同推理、置信度和时间戳记录下来，为生产系统中的 AI 行为留下完整审计轨迹。

**可解释。**当相关方问"系统为什么做 X？"时，你可以追溯导致该行动的确切决策链，包括中间推理步骤。

**先例(precedent)复用。**做新决策之前，智能体可以搜索相似的过往场景及其结果，保持一致性，并从历史经验中学习。

**因果分析。**沿着决策节点之间的因果关系，理解早期决策如何层层传导为后续结果。

**治理与合规。**策略引擎可以依据合规规则给决策把关，所有策略应用都会记录在案，供监管审计。

## 适用与不适用场景

**以下情况使用决策智能：**
- 构建要做重大选择的自主智能体
- 实现需要审计轨迹的决策工作流
- 在合规要求下运营（金融服务、医疗、国防）
- 构建有多个决策点的审批系统
- 在决策必须可解释的风险敏感环境中工作

**以下情况不要用：**
- 构建只检索信息的无状态聊天机器人
- 实现不做决策的简单检索增强生成(RAG)系统
- 创建只读的信息检索应用
- 构建从不做出需要审计轨迹的行动决策的应用

## API 架构总览

决策智能协调三个主要组件：

**`AgentContext`** 是高层编排层。它提供 `record_decision()`、`find_precedents()` 和因果链方法，同时管理底层的存储与检索系统。

**`PolicyEngine`（策略引擎）** 负责策略评估与合规检查。它把策略规则存成图节点，并在决策记录之前依据这些规则校验决策。

**`DecisionRecorder`** 专职记录结构化决策数据、管理审批链，并在决策需要绕过常规规则时处理策略例外。

<Info>
  决策追踪同时需要 `VectorStore`（用于基于嵌入(Embedding)的先例检索）和 `ContextGraph`（用于因果图存储）。在 `AgentContext` 上设置 `decision_tracking=True`——漏掉 `ContextGraph` 会在调用时抛 `RuntimeError`。`VectorStore` 是 `AgentContext` 自身的必填参数：不传该参数会由 Python 的参数绑定抛 `TypeError`，而传 `vector_store=None` 则会在初始化时抛 `ValueError`。
</Info>

## 记录第一个决策

最常见的入口是 `AgentContext.record_decision()`。它把一个 `Decision` 节点写入图，生成用于混合相似度检索的嵌入，并返回一个 UUID——后续决策靠它与本决策建立因果关联。

```python
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore

graph   = ContextGraph(advanced_analytics=True)
context = AgentContext(
    vector_store=VectorStore(backend="faiss", dimension=768),
    knowledge_graph=graph,
    decision_tracking=True,
)

# 系统刚完成一个新威胁簇的分类。
# 在采取任何行动之前，先记录这条分类决策。
classification_id = context.record_decision(
    category       = "threat_classification",
    scenario       = "Unattributed C2 cluster using HAMMERTOSS-like Twitter dead-drop pattern",
    reasoning      = "Infrastructure overlaps known APT29 hosting ASN; TTP T1102 matches NOBELIUM playbook with 0.88 cosine similarity",
    outcome        = "classified_as_apt29_cluster",
    confidence     = 0.88,
    decision_maker = "cti_pipeline_v2",
    entities       = ["apt29", "hammertoss", "twitter_c2"],
)

print("Decision recorded:", classification_id)
# → "Decision recorded: dec_a3f2b1c4-..."
```

`decision_maker` 字段标识产生该决策的组件、工作流、智能体或系统。使用一致的标识符，比如 `"cti_pipeline_v2"`、`"analyst_chen"` 或 `"risk_model_v3"`，这样才能按决策来源过滤和分析。

支撑该节点的 `Decision` 数据类有以下字段——存储和检索用的就是它们：

```python
from semantica.context import Decision
from datetime import datetime

d = Decision(
    decision_id    = None,                # 必填参数——None/"" 会自动生成 UUID
    category       = "threat_classification",
    scenario       = "Unattributed C2 cluster",
    reasoning      = "Infrastructure overlaps APT29 ASN",
    outcome        = "classified_as_apt29_cluster",
    confidence     = 0.88,               # 浮点数 0.0–1.0
    timestamp      = datetime.now(),
    decision_maker = "cti_pipeline_v2",
    # 可选字段：
    valid_from     = "2025-07-01T00:00:00",   # ISO 日期时间
    valid_until    = "2025-09-30T23:59:59",   # ISO 日期时间
    metadata       = {"source_feed": "isac_partner_b"},
)
```

要把这样构造的决策真正存进图，把它的字段作为关键字参数传给 `ContextGraph.add_decision()`——当你想在必填字段之外再传 `valid_from`/`valid_until` 或额外元数据字段时，这是 `record_decision()` 之外的另一条路：

```python
decision_id = graph.add_decision(
    category       = "threat_classification",
    scenario       = "Unattributed C2 cluster",
    reasoning      = "Infrastructure overlaps APT29 ASN",
    outcome        = "classified_as_apt29_cluster",
    confidence     = 0.88,               # 浮点数 0.0–1.0
    decision_maker = "cti_pipeline_v2",
    # 可选字段：
    valid_from     = "2025-07-01T00:00:00",   # ISO 日期时间
    valid_until    = "2025-09-30T23:59:59",   # ISO 日期时间
    source_feed    = "isac_partner_b",        # 额外关键字参数会存入 metadata
)
```

<Warning>
只能给 `add_decision()` 传关键字参数，不要传预构建的 `Decision` 对象。`add_decision(Decision(...))` 会直接存节点，跳过 `record_decision()` 执行的索引步骤——于是这条决策对 `find_precedents()`、`get_causal_chain()` 和 `get_decision_insights()` 不可见，而且对它调用 `trace_decision_causality()` 会抛 `ValueError`。上面的关键字参数形式没有这个问题——它内部委托给 `record_decision()`。注意，与 `record_decision()` 一样，它总是自己生成 `decision_id`（从调用返回值拿到）；没有办法强行指定 ID。
</Warning>

## 决策之前先搜先例

做重大判断之前，系统应当先搜索过往决策中的相似场景。这样才不会让同一个威胁簇在两次运行中被分成不同的类——第二个智能体会找到第一个智能体的决策，把它当作先验。

```python
# 给新的未归因威胁簇分类之前，先搜索
precedents = context.find_precedents(
    "unattributed C2 cluster Twitter dead-drop infrastructure",
    limit=5,
)

for p in precedents:
    print("[{:.2f} confidence] {} → {}".format(p.confidence, p.category, p.outcome))
    print("  Reasoning: {}".format(p.reasoning[:80]))
    print("  Similarity: {:.3f}".format(p.metadata.get("similarity_score", 0)))
```

混合检索融合两个信号：一是词面重叠——查询与每条决策的 `scenario`、`reasoning`、`entities` 文本之间的重合度（权重 0.7，词级 Jaccard 相似度，中日韩风格的查询会退回到字符二元组）；二是结构相似度——基于每条决策在图中连接了多少其他节点（权重 0.3，仅当图以 `advanced_analytics=True` 构建时才计算）。返回的是按分排序的 `Decision` 对象列表，只保留得分不低于 `similarity_threshold`（默认 0.5）的结果——由于匹配基于词面而非嵌入，措辞与查询差异很大的先例，即使描述的是相似场景，也可能不会被召回。

## 构建因果链

决策很少孤立存在。分类决策引发升级决策，升级决策又引发遏制决策。用因果边把它们连起来，就能沿链双向遍历——向上追溯什么导致了一个结果，向下查看一个早期决策触发了什么。

```python
# 上面的分类决策引发了一次升级
escalation_id = context.record_decision(
    category       = "escalation",
    scenario       = "APT29 cluster confirmed — active C2 beaconing to NATO contractor subnet",
    reasoning      = "Classification confidence 0.88 exceeds 0.80 escalation threshold; active C2 requires immediate SOC notification",
    outcome        = "escalated_to_soc_tier2",
    confidence     = 0.95,
    decision_maker = "escalation_engine",
)

# 连接两条决策：分类导致了升级
graph.add_causal_relationship(classification_id, escalation_id, "CAUSED")

# 升级决策又影响了一次补丁优先级决策
patch_id = context.record_decision(
    category       = "patch_priority",
    scenario       = "CVE-2024-3400 present in two NATO contractor VPN appliances",
    reasoning      = "Active exploitation by classified APT29 cluster elevates CVE-2024-3400 to P0 regardless of base CVSS",
    outcome        = "prioritized_cve_2024_3400_p0",
    confidence     = 0.97,
    decision_maker = "patch_engine",
)

graph.add_causal_relationship(escalation_id, patch_id, "INFLUENCED")
```

现在从补丁决策出发，向上追溯根因：

```python
upstream = context.get_causal_chain(
    patch_id,
    direction = "upstream",
    max_depth = 5,
)

print("Causal chain upstream from patch prioritization:")
for d in upstream:
    depth = d.metadata.get("causal_distance", "?")
    print("  [depth {}] {} → {}  (confidence={:.2f})".format(
        depth, d.category, d.outcome, d.confidence
    ))
# [depth 1] escalation → escalated_to_soc_tier2  (confidence=0.95)
# [depth 2] threat_classification → classified_as_apt29_cluster  (confidence=0.88)
```

再从最初的分类决策向下追溯，看它触发了哪些后续决策：

```python
downstream = context.get_causal_chain(
    classification_id,
    direction = "downstream",
    max_depth = 5,
)
print("Downstream decisions triggered:", len(downstream))
for d in downstream:
    print("  → {} [{}]".format(d.outcome, d.category))
```

## 生成可解释性报告

`trace_decision_explainability` 一次调用给出全貌：上游原因、下游影响和总连接数。事后复盘或审计报告就附这个。

```python
explanation = context.trace_decision_explainability(patch_id)

print("Decision:", patch_id)
print("Total graph connections :", explanation["total_connections"])
print("Upstream causes         :", len(explanation.get("upstream_decisions", [])))
print("Downstream effects      :", len(explanation.get("downstream_decisions", [])))
```

要做带置信衰减和距离带(distance band)的更深入因果分析，直接在图上调用 `trace_decision_causality`：

```python
chains = graph.trace_decision_causality(patch_id, max_depth=5)

for chain in chains:
    print("Chain: {} hops | band={} | decay={:.3f}".format(
        chain["hop_count"], chain["distance_band"], chain["confidence_decay"]
    ))
    print("  Interpretation:", chain["interpretation"])
    # e.g. "Decision chain spans 2 hops in the 'near' band with 84% confidence
    #        — causal attribution is reliable."
```

## 用策略为决策把关

记录高风险决策之前，先对照版本化策略做检查。`PolicyEngine` 把 `Policy` 节点存入图，并用策略规则给 `Decision` 对象把关。

```python
from semantica.context import PolicyEngine, Policy, Decision
from datetime import datetime

engine = PolicyEngine(graph_store=graph)

engine.add_policy(Policy(
    policy_id   = "cti_confidence_gate",
    name        = "CTI Minimum Confidence Policy",
    description = "All threat classifications must have confidence >= 0.80",
    rules       = {"min_confidence": 0.80, "requires_reasoning": True},
    category    = "threat_classification",
    version     = "1.0",
    created_at  = datetime.now(),
    updated_at  = datetime.now(),
))

d = Decision(
    decision_id    = "dec_low_conf",
    category       = "threat_classification",
    scenario       = "Possible APT29 activity — weak signals only",
    reasoning      = "Single IP overlap, no TTP match",
    outcome        = "classified_as_apt29_tentative",
    confidence     = 0.62,   # 低于 0.80 阈值
    timestamp      = datetime.now(),
    decision_maker = "cti_pipeline_v2",
)

if engine.check_compliance(d, "cti_confidence_gate"):
    # 以关键字参数传字段，不要传 Decision 对象本身——见上文
    # 的警告。add_decision() 会自己生成 decision_id。
    decision_id = graph.add_decision(
        category=d.category, scenario=d.scenario, reasoning=d.reasoning,
        outcome=d.outcome, confidence=d.confidence, decision_maker=d.decision_maker,
    )
    engine.record_policy_application(decision_id, "cti_confidence_gate", "1.0")
    print("Decision recorded — policy compliant.")
else:
    print("Decision blocked — confidence 0.62 below policy minimum 0.80.")
    # → "Decision blocked — confidence 0.62 below policy minimum 0.80."
```

`check_compliance` 返回 `False` 表示规则已评估、决策未通过。如果检查本身无法执行——例如某条策略规则无法与决策数据做比较——调用会抛 `ProcessingError` 而不是返回 `False`，评估失败绝不会被当成合规结论上报。完整契约见[策略引擎指南](./policy-engine.md)。

高紧迫性场景需要绕过策略闸门时，记录例外要带上审批人身份和理由：

```python
from semantica.context import DecisionRecorder

recorder = DecisionRecorder(graph_store=graph)

exception_id = recorder.record_exception(
    decision_id     = "dec_low_conf",
    policy_id       = "cti_confidence_gate",
    reason          = "Active exploitation in progress — cannot wait for higher-confidence attribution",
    approver        = "ciso_director",
    approval_method = "slack_dm",
    justification   = "Time-critical incident response; manual CISO sign-off obtained at 03:14 UTC",
)
print("Policy exception recorded:", exception_id)
```

多级审批工作流用 `DecisionRecorder.record_approval_chain()`，并搭配图数据库后端（例如 Neo4j/FalkorDB）。本指南使用的内存 `ContextGraph` 示例不支持经 `execute_query()` 持久化审批链。

## 生成决策审计报告

换班或事件收尾时，`get_decision_insights` 会对图中所有决策给出统计摘要——交接班记录和合规报告都用得上。

```python
insights = graph.get_decision_insights()

print("Total decisions today :", insights["total_decisions"])
print("Confidence — mean={:.2f}  min={:.2f}  max={:.2f}".format(
    insights["confidence_stats"]["mean"],
    insights["confidence_stats"]["min"],
    insights["confidence_stats"]["max"],
))
print("\nDecisions by category:")
for cat, count in sorted(insights["categories"].items(), key=lambda x: -x[1]):
    print("  {:35s} {}".format(cat, count))
print("\nOutcomes:")
for outcome, count in sorted(insights["outcomes"].items(), key=lambda x: -x[1]):
    print("  {:35s} {}".format(outcome, count))
```

示例输出：

```text
Total decisions today : 47
Confidence — mean=0.87  min=0.62  max=0.99

Decisions by category:
  threat_classification                 18
  patch_priority                        12
  escalation                             9
  containment                            8

Outcomes:
  classified_as_apt29_cluster           11
  prioritized_p0_patch                  12
  escalated_to_soc_tier2                 9
  isolated_host                          8
```

## 领域示例

<Tabs>

<Tab title="国防 — 威胁情报">

CTI 流水线对威胁簇分类，把每条分类连同置信度和推理记录下来，把分类决策与升级决策因果相连，并为威胁情报负责人生成每日审计报告。

```python
from semantica.context import AgentContext, ContextGraph, PolicyEngine, Policy
from semantica.vector_store import VectorStore
from datetime import datetime

graph   = ContextGraph(advanced_analytics=True)
engine  = PolicyEngine(graph_store=graph)
context = AgentContext(
    vector_store=VectorStore(backend="faiss", dimension=768),
    knowledge_graph=graph,
    decision_tracking=True,
)

engine.add_policy(Policy(
    policy_id   = "cti_gate",
    name        = "CTI Attribution Confidence Gate",
    description = "Attributions require confidence >= 0.80",
    rules       = {"min_confidence": 0.80},
    category    = "threat_classification",
    version     = "1.0",
    created_at  = datetime.now(),
    updated_at  = datetime.now(),
))

# 分类前先查先例
precedents = context.find_precedents(
    "Twitter dead-drop C2 pattern overlapping APT29 infrastructure",
    limit=3,
)
for p in precedents:
    print("Prior: {} → {} ({:.0%})".format(p.scenario[:40], p.outcome, p.confidence))

# 记录分类决策
class_id = context.record_decision(
    category       = "threat_classification",
    scenario       = "New C2 cluster: Twitter dead-drop, AS200651 hosting, TTP T1102",
    reasoning      = "IP block overlaps APT29 cluster; T1102 matches HAMMERTOSS playbook",
    outcome        = "classified_apt29_march_cluster",
    confidence     = 0.88,
    decision_maker = "cti_pipeline_v2",
    entities       = ["apt29", "hammertoss"],
)

# 关联下游升级决策
esc_id = context.record_decision(
    category       = "escalation",
    scenario       = "APT29 cluster active — beaconing to NATO subnet 10.30.0.0/16",
    reasoning      = "Active C2 with high-confidence attribution requires immediate SOC notification",
    outcome        = "escalated_tier2_soc",
    confidence     = 0.97,
    decision_maker = "escalation_engine",
)
graph.add_causal_relationship(class_id, esc_id, "CAUSED")

# 换班后的审计报告
insights = graph.get_decision_insights()
print("Decisions recorded:", insights["total_decisions"])
print("Mean confidence   :", round(insights["confidence_stats"]["mean"], 2))
```

</Tab>

<Tab title="安全 — SOC/事件响应">

事件处置期间，SOC 把遏制决策连同触发它们的检测决策一起因果相连地记录下来。六小时后复盘时，可以完整重放从第一声告警到最终遏制的每一步决策。

```python
from semantica.context import AgentContext, ContextGraph, DecisionRecorder
from semantica.vector_store import VectorStore

graph    = ContextGraph()
recorder = DecisionRecorder(graph_store=graph)
context  = AgentContext(
    vector_store=VectorStore(backend="faiss", dimension=768),
    knowledge_graph=graph,
    decision_tracking=True,
)

# T+0：检测决策
detect_id = context.record_decision(
    category       = "detection",
    scenario       = "WKSTN-047: wmiprvse.exe spawned scheduled task — T1053.005",
    reasoning      = "Scheduled task creation by WMI provider host is high-fidelity lateral movement indicator",
    outcome        = "flagged_wkstn047_suspicious",
    confidence     = 0.93,
    decision_maker = "edr_engine",
)

# T+8min：由检测引发的遏制决策
contain_id = context.record_decision(
    category       = "containment",
    scenario       = "WKSTN-047 confirmed compromised — lateral movement to DC01 via SMB",
    reasoning      = "PsExec artefact on DC01; isolate before domain-wide credential compromise",
    outcome        = "isolated_wkstn047",
    confidence     = 0.95,
    decision_maker = "analyst_chen",
)
graph.add_causal_relationship(detect_id, contain_id, "CAUSED")

# 复盘：追溯完整因果链
chain = context.get_causal_chain(contain_id, direction="upstream", max_depth=5)
print("Post-mortem — causal chain for isolation decision:")
for d in chain:
    print("  [depth {}] {} → {}  (confidence={:.2f}, maker={})".format(
        d.metadata.get("causal_distance", "?"),
        d.category, d.outcome, d.confidence, d.decision_maker,
    ))

# 遏制决策的完整可解释性
explanation = context.trace_decision_explainability(contain_id)
print("Upstream causes   :", len(explanation.get("upstream_decisions", [])))
print("Total connections :", explanation["total_connections"])
```

</Tab>

<Tab title="生命科学 — 临床/制药">

临床 AI 助手记录治疗调整决策及其指南先例，把它们与之前的诊断决策因果相连，并为 MDT 评审和监管审计生成结构化决策记录。

```python
from semantica.context import AgentContext, ContextGraph, PolicyEngine, Policy
from semantica.context import Decision, DecisionRecorder
from semantica.vector_store import VectorStore
from datetime import datetime

graph   = ContextGraph()
engine  = PolicyEngine(graph_store=graph)
context = AgentContext(
    vector_store=VectorStore(backend="faiss", dimension=768),
    knowledge_graph=graph,
    decision_tracking=True,
)

engine.add_policy(Policy(
    policy_id   = "clinical_confidence_gate",
    name        = "Clinical Decision Confidence Gate",
    description = "Treatment decisions require confidence >= 0.90",
    rules       = {"min_confidence": 0.90},
    category    = "treatment_modification",
    version     = "1.0",
    created_at  = datetime.now(),
    updated_at  = datetime.now(),
))

# 诊断决策先于治疗决策
diag_id = context.record_decision(
    category       = "diagnosis_assessment",
    scenario       = "Patient eGFR 28 mL/min/1.73m2, CKD Stage 4, current metformin 1000mg BD",
    reasoning      = "eGFR 28 confirms CKD Stage 4; below 30 threshold for metformin contraindication",
    outcome        = "confirmed_ckd_stage4_metformin_contraindicated",
    confidence     = 0.99,
    decision_maker = "clinical_ai_v3",
)

# 由诊断评估引发的治疗调整
treat_id = context.record_decision(
    category       = "treatment_modification",
    scenario       = "Metformin discontinuation required — eGFR 28 below contraindication threshold",
    reasoning      = "NICE NG28 and BNF both contraindicate metformin at eGFR < 30; switch to gliclazide MR 30mg OD",
    outcome        = "discontinue_metformin_initiate_gliclazide",
    confidence     = 0.97,
    decision_maker = "clinical_ai_v3",
)
graph.add_causal_relationship(diag_id, treat_id, "CAUSED")

# MDT 审计报告
chain = context.get_causal_chain(treat_id, direction="upstream", max_depth=3)
print("MDT Decision Audit — Treatment Modification")
print("=" * 50)
for d in chain:
    print("Caused by: [{}] {} (confidence={:.0%})".format(
        d.category, d.outcome, d.confidence
    ))

insights = graph.get_decision_insights()
cs = insights["confidence_stats"]
print("\nSession decisions: {}  |  mean confidence: {:.2f}".format(
    insights["total_decisions"], cs["mean"]
))
```

</Tab>

<Tab title="银行 — 风控/合规">

信贷决策系统对照版本化的信贷策略记录每笔贷款决策，把边缘审批与压力测试决策因果相连，并为 SR 11-7 模型治理评审导出完整的决策审计轨迹。

```python
from semantica.context import AgentContext, ContextGraph, PolicyEngine, Policy
from semantica.context import Decision, DecisionRecorder
from semantica.vector_store import VectorStore
from datetime import datetime

graph   = ContextGraph()
engine  = PolicyEngine(graph_store=graph)
context = AgentContext(
    vector_store=VectorStore(backend="faiss", dimension=768),
    knowledge_graph=graph,
    decision_tracking=True,
)

engine.add_policy(Policy(
    policy_id   = "lending_policy_v3",
    name        = "Lending Compliance Policy v3",
    description = "Credit decisions require confidence >= 0.85 and documented reasoning",
    rules       = {"min_confidence": 0.85, "requires_reasoning": True},
    category    = "loan_approval",
    version     = "3.0",
    created_at  = datetime.now(),
    updated_at  = datetime.now(),
))

# 审批前先查先例
precedents = context.find_precedents(
    "first-time buyer mortgage borderline DSTI stressed rate scenario",
    limit=3,
)
for p in precedents:
    print("Prior: {} → {} ({:.0%})".format(p.scenario[:40], p.outcome, p.confidence))

# 压力测试决策先于审批决策
stress_id = context.record_decision(
    category       = "stress_test",
    scenario       = "APP-2025-994421: LTV 78%, DSTI 38% at current rate; DSTI rises to 44% at +300bps",
    reasoning      = "DSTI 44% under stress exceeds 35% guideline threshold — requires LMI and income verification",
    outcome        = "stress_test_conditional_pass",
    confidence     = 0.88,
    decision_maker = "risk_model_v3",
)

# 受压力测试影响的审批决策
d = Decision(
    decision_id    = "loan_dec_994421",
    category       = "loan_approval",
    scenario       = "APP-2025-994421: first-time buyer, LTV 78%, credit score 714, 30yr fixed",
    reasoning      = "Credit score 714 exceeds 700 minimum; LTV within 80% cap; conditional on LMI given stress-test DSTI",
    outcome        = "approved_conditional_lmi_required",
    confidence     = 0.89,
    timestamp      = datetime.now(),
    decision_maker = "credit_model_v3",
)

# False 表示已评估且不合规；如果检查根本无法执行，
# check_compliance 会抛 ProcessingError（见 policy-engine 指南）。
if engine.check_compliance(d, "lending_policy_v3"):
    loan_id = context.record_decision(
        category=d.category, scenario=d.scenario,
        reasoning=d.reasoning, outcome=d.outcome, confidence=d.confidence,
        decision_maker=d.decision_maker,
    )
    graph.add_causal_relationship(stress_id, loan_id, "INFLUENCED")
    engine.record_policy_application(loan_id, "lending_policy_v3", "3.0")
    print("Loan decision recorded — policy compliant.")

    # SR 11-7 可解释性报告
    explanation = context.trace_decision_explainability(loan_id)
    print("Upstream influences:", len(explanation.get("upstream_decisions", [])))
    print("Total connections  :", explanation["total_connections"])
```

</Tab>

</Tabs>

## 跨重启持久化决策

用本地 `ContextGraph` 时，每次会话结束保存、下次开始加载。所有决策节点、因果边和 FAISS 嵌入都会恢复。

```python
# 会话结束时
context.save("agent_state/")
# 写入：agent_state/knowledge_graph.json + FAISS 索引

# 下次会话开始时
context = AgentContext(
    vector_store=VectorStore(backend="faiss", dimension=768),
    knowledge_graph=ContextGraph(),
    decision_tracking=True,
)
context.load("agent_state/")

# 所有历史决策立即可检索
results = context.find_precedents("APT29 infrastructure attribution", limit=5)
```

## 常见陷阱

**记录决策却不连因果关系。**孤立的决策节点提供的信息远少于相连的决策链。用 `add_causal_relationship()` 把相关决策连起来，才能做因果追溯。

**创建孤立的决策节点。**决策与图中的实体、其他决策或结果相连才有价值。用 `entities` 参数把决策关联到相关实体。

**记录过多低价值决策。**不是每个小选择都值得永久记录。聚焦影响结果、需要审计轨迹、或能受益于先例检索的重大决策。

**把先例相似度当成证据。**相似度高只说明场景相关，不说明情形相同。把先例当参考，同时结合每个新决策的具体上下文判断。

**简单检索就够时也用决策智能。**如果系统只检索信息、不做可执行的抉择，传统搜索或智能体记忆可能比决策追踪更合适。

## 相关指南

- [上下文图](./context-graphs.md) — `ContextGraph` 如何存储决策节点与因果边
- [距离智能](./distance-intelligence.md) — `trace_decision_causality()` 以置信衰减和距离带标注因果链
- [溯源](./provenance.md) — 用符合标准的 W3C PROV-O 溯源(Provenance)包裹决策记录，形成审计轨迹
- [MCP 服务器](./mcp-server.md) — 经 `record_decision` 与 `find_precedents` 工具，把决策记录和先例检索开放给大语言模型(LLM)智能体
- [变更管理](./change-management.md) — 用 `flush_checkpoint()` 给决策状态做检查点，生成版本化快照
