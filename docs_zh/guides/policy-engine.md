---
title: 策略引擎
description: 对知识图谱决策定义、版本化并执行治理策略——支持合规检查、违规追踪、影响分析和多级审批工作流。
source: guides/policy-engine.md
source_version: 2baf69e68d5c4d1b631bad65c71fbd87235de68a
icon: "scale-balanced"
---

## 什么是策略引擎？

策略评估(Policy evaluation)是指依据预定义的治理规则和约束，对决策(Decision)做系统性检查。与自动拦截不合规操作的应用层强制不同，策略评估给出的是合规状态——由它来触发不同的工作流：审批流程、例外处理，或审计要求。

**关键策略概念：**

**策略评估**检查决策是否满足既定标准，但不自动阻止操作，从而支持灵活的治理工作流。

**治理与合规工作流**利用策略评估结果，把决策路由到相应的审批链、例外流程或审计留痕。

**审批流程**可由策略违规触发，形成有书面理由、审批人可追责的例外通道。

**与强制执行的区别：** 策略评估返回合规状态（`True`/`False`），但不会自动阻止操作。接下来怎么办由你的工作流决定——立即批准、升级处理、例外处理或驳回。

## 为什么使用策略引擎？

**治理与问责。** 构建可审计的决策工作流：每一次策略评估、例外和审批都连同完整溯源(Provenance)永久记录在知识图谱(Knowledge Graph)中。

**合规验证。** 在决策定稿或执行之前，系统性地对照监管要求、内部政策和风险管理规则逐项检查。

**审批工作流编排。** 把不合规的决策送入结构化的审批流程，附带书面理由和多级签核。

**监管合规。** 维护完整的策略版本历史、例外记录和合规检查留痕，满足监管机构随时可查的审计要求。

**风险管理。** 标记高风险决策以供复核，同时让常规合规决策低摩擦通过。

**策略演进追踪。** 保留策略变更的版本历史并做影响分析，让策略优化有据可循，也便于对监管做汇报。

## 适用与不适用场景

**适合用策略引擎：**
- 需要结构化审批流程和审计留痕的治理工作流
- 要求策略遵从可记录、可验证的监管合规场景
- 高风险决策的多级审批工作流（财务审批、安全例外、临床治疗）
- 策略违规会触发特定升级程序的受监管环境
- 不合规决策需要额外监督的风险管理工作流
- 要求完整策略执行与例外追踪的审计要求

**不要用策略引擎：**
- 简单的表单校验或基础输入检查——用标准校验库就够了
- 不需要审计留痕或治理工作流的基础业务规则
- 低风险、高吞吐的检查——策略评估的开销会影响性能
- 用不上版本追踪和审批流程的确定性规则检查
- 策略评估延迟不可接受的实时运营决策

**警告：** 策略引擎会带来治理开销，且需要精心设计工作流。只有当结构化策略管理的收益大于额外复杂度时才使用它。

`PolicyEngine` 用具名策略校验已记录的决策，决策满足全部策略规则时返回 `True`。用它给 AI 决策把门——例如需要双来源确认的归因、需要上级审批的升级操作，或任何必须在结果落库前验证合规的决策类别。策略本身是带版本的图节点，因此每一次检查、例外和审批链都是永久审计轨迹的一部分。

<Info>
策略引擎(Policy Engine)位于 `AgentContext` 和 `ContextGraph` 之上。策略与决策存放在同一张图中，作为节点存在，因此享有与其他知识图谱实体同等的因果追踪、溯源和时态有效性。

**关键对象：** `PolicyEngine` 和 `Policy` 从 `semantica.context` 导入。`Decision` 是一个 dataclass，字段包括 `decision_id`、`category`、`scenario`、`reasoning`、`outcome`、`confidence`、`timestamp`、`decision_maker` 和 `metadata`。`DecisionRecorder` 从 `semantica.context.decision_recorder` 导入，用于审批工作流追踪。
</Info>

## 支持的规则类型

`PolicyEngine` 的实现支持特定的规则模式，用于评估决策属性和元数据：

**置信度规则：**
- `min_confidence: 0.85` — `decision.confidence >= 0.85`

**结果校验：**
- `allowed_outcomes: ["approved", "approved_with_conditions"]` — `decision.outcome` 必须在列表中

**类别校验：**
- `required_categories: ["credit_risk", "operational_risk"]` — `decision.category` 必须在列表中

**元数据字段规则：**
- `min_*: value` — 元数据字段必须 `>= value`（如 `min_credit_score: 680`）
- `max_*: value` — 元数据字段必须 `<= value`（如 `max_ltv: 0.85`）
- `required_*: value` — 元数据字段必须等于 `value`（字符串）或包含全部元素（列表）

**字段查找行为：** 对于规则 `min_credit_score`，引擎依次检查 `metadata["credit_score"]`、`metadata["*_credit_score"]`（后缀匹配），最后是 `decision.credit_score` 属性。

**重要：** 以下规则类型不受支持，使用会导致意外行为：
- `disallowed_outcomes`（请改用 `allowed_outcomes`）
- `mandatory_fields`（针对具体字段请用 `required_*`）
- `requires_mfa`（请用元数据字段检查，如 `required_mfa_verified`）
- 复杂嵌套条件或运算符

---

## 定义策略

`Policy` 是一个 dataclass，`rules` dict 的内容自由定义——用受支持的规则模式编码你的领域所需。

```python
from semantica.context import ContextGraph, PolicyEngine, Policy
from datetime import datetime

graph  = ContextGraph()
engine = PolicyEngine(graph_store=graph)

attribution_policy = Policy(
    policy_id   = "pol-attr-001",
    name        = "Nation-State Attribution — Dual Source + Senior Approval",
    description = (
        "Attributions to nation-state actors require corroboration from two independent "
        "intelligence sources and explicit senior analyst approval before being recorded "
        "in the authoritative graph."
    ),
    rules = {
        "min_independent_sources":  2,
        "required_approver_role":   "senior_analyst",
        "allowed_outcomes":         ["nation_state_attributed_dual_source"],
        "min_confidence":           0.85,
        "required_source_a":        True,
        "required_source_b":        True,
        "required_approver":        True,
    },
    category   = "threat_attribution",
    version    = "1.0.0",
    created_at = datetime.utcnow(),
    updated_at = datetime.utcnow(),
)

policy_id = engine.add_policy(attribution_policy)
print(f"Policy registered: {policy_id}")
# Policy registered: pol-attr-001
```

策略至此成为图中的一个节点。它带版本字符串、创建时间戳，以及一个 `rules` dict——合规检查器评估决策时会读取它。

---

## 检查决策的合规性

`check_compliance` 接收一个 `Decision` 对象和策略 ID，返回布尔值：决策合规返回 `True`；经过评估发现不合规返回 `False`。如果检查本身无法执行——比如某个规则值无法与决策元数据比较——`check_compliance` 会抛出 `ProcessingError`，而不是返回 `False`。

```python
from semantica.context import Decision

# The AI analyst's APT29 attribution — only one source cited, no senior approval yet
decision = Decision(
    decision_id   = "",                        # auto-generated if left empty
    category      = "threat_attribution",
    scenario      = "APT29 activity cluster in NATO network telemetry Q2 2025",
    reasoning     = (
        "Observed TTPs match APT29 historical patterns: HAMMERTOSS C2, "
        "spear-phishing via OneDrive lure, targeting foreign ministry staff. "
        "Single source: internal SIEM telemetry."
    ),
    outcome       = "nation_state_attributed_single_source",
    confidence    = 0.91,
    timestamp     = datetime.utcnow(),
    decision_maker= "ai_threat_analyst_v3",
    metadata      = {
        "independent_sources": 1,  # Below min_independent_sources requirement
        "approver_role": "analyst",  # Below required_approver_role
        "source_a": True,  # Has first source
        # Missing source_b and approver fields
    }
)

is_compliant = engine.check_compliance(decision, policy_id)
print(f"Compliant: {is_compliant}")
# Compliant: False
#
# Multiple rule violations:
# - outcome "nation_state_attributed_single_source" not in allowed_outcomes
# - independent_sources (1) < min_independent_sources (2)
# - approver_role "analyst" != required_approver_role "senior_analyst"
# - missing required_source_b and required_approver fields
```

引擎返回 `False`。这条决策并没有被驳回——它被标记了。接下来如何处理取决于你的工作流：有的组织直接阻止向权威图谱写入；有的则触发例外流程，由人工审批人审阅证据后签核。

### 检查本身失败时

返回 `False` 一定是一个裁决：规则运行了，而决策不满足规则。这也包括决策缺少规则所需证据的情形——`min_`/`max_`/`required_` 规则指向决策未携带的元数据字段时，按策略计为不合规。

另一种情形是规则根本无法评估，例如 `min_confidence` 的值是 `"high"`，无法与数值型的决策置信度比较。此时 `check_compliance` 抛出 `ProcessingError`，而不是报告为不合规——评估缺陷永远不能伪装成策略违规。如果你需要把"失败"与"裁决"分开报告，可以这样包装调用：

```python
from semantica.utils.exceptions import ProcessingError

try:
    is_compliant = engine.check_compliance(decision, policy_id)
except ProcessingError as e:
    # The rules could not be evaluated — an operational error,
    # not a compliance verdict.
    print(f"Compliance check failed: {e}")
```

---

## 记录策略例外

`record_exception` 把决策、被违反的策略、审批人身份和理由永久关联起来。

```python
exception_id = engine.record_exception(
    decision_id  = decision.decision_id,
    policy_id    = policy_id,
    reason       = "Time-sensitive attribution — protective action required before second source available",
    approver     = "sr_analyst_chen",
    justification= (
        "Senior analyst reviewed SIEM telemetry and concurs with TTP matching. "
        "Exception approved under Emergency Attribution Procedure §3.2. "
        "Second source corroboration to be completed within 72 hours."
    ),
)

print(f"Exception recorded: {exception_id}")
# Exception recorded: exc-pol-attr-001-20250621-001
#
# The exception node is linked to both the decision and the policy in the graph,
# creating a permanent three-way provenance link: decision → exception → policy.
```

---

## 构建多级审批链

对风险级别最高的决策——比如将提交给政府合作伙伴的正式归因报告——一个审批人远远不够，需要三个人签核：团队负责人、部门主管和 CISO（首席信息安全官）。`DecisionRecorder.record_approval_chain` 一次调用即可记录全部三人，并把每位审批人与其签核的沟通方式和上下文关联起来。

```python
from semantica.context.decision_recorder import DecisionRecorder

recorder = DecisionRecorder(graph_store=graph)

# approvers, methods, and contexts must be equal-length parallel lists
recorder.record_approval_chain(
    decision_id = decision.decision_id,
    approvers   = ["team_lead_okonkwo",  "dept_head_zhang",    "ciso_miller"],
    methods     = ["slack_dm",            "zoom_call",           "email"],
    contexts    = [
        "Team lead reviewed TTPs and SIEM evidence",
        "Dept head approved sharing with Five Eyes partners",
        "CISO authorised formal nation-state attribution report",
    ],
)

print("Three-level approval chain recorded")
# The graph now carries a directed approval chain:
#   decision → team_lead_okonkwo → dept_head_zhang → ciso_miller
# Each link is stamped with method and context for Inspector General review.
```

---

## 修改策略前的假设影响分析

六个月后，威胁情报主管想收紧策略：把最低置信度阈值从 0.85 提高到 0.92，以减少误报归因。更新策略之前，她想知道有多少历史决策会在更严格的规则下被拦下。

`analyze_policy_impact` 对历史决策记录做一次假设(what-if)模拟——不会产生任何永久变更。

```python
current_policy = engine.get_policy(policy_id)

impact = engine.analyze_policy_impact(
    policy_id      = policy_id,
    proposed_rules = {**current_policy.rules, "min_confidence": 0.92},
)

print(f"Decisions affected by raising confidence floor to 0.92: {impact.get('affected_decisions', 0)}")
# Decisions affected by raising confidence floor to 0.92: 4
#
# Four past attributions had confidence between 0.85 and 0.92.
# Under the new rule, all four would have required exceptions.
# The lead can now make an evidence-based choice: is that trade-off acceptable?
```

影响结果 dict 包含每个决策的明细，而不只是一个数量。你可以查看具体哪些归因决策会受影响、审阅它们的推理过程，再判断收紧阈值是否值得。

---

## 更新策略并找出受影响的决策

主管决定执行阈值上调。她把策略更新到 1.1.0 版本，并记录了变更原因。旧版本保留在历史中。

```python
engine.update_policy(
    policy_id     = policy_id,
    rules         = {**current_policy.rules, "min_confidence": 0.92},
    change_reason = "Q3 attribution quality review — raise confidence floor from 0.85 to 0.92 "
                    "to reduce false-positive nation-state attributions",
    new_version   = "1.1.0",
)

print(f"Policy updated: {policy_id} to version 1.1.0")
# Policy updated: pol-attr-001 to version 1.1.0

# Find all decisions that were evaluated under v1.0.0 —
# these need to be re-reviewed to confirm they still meet the new standard.
affected = engine.get_affected_decisions(
    policy_id    = policy_id,
    from_version = "1.0.0",
    to_version   = "1.1.0",
)

print(f"Decisions to re-audit: {len(affected)}")
for dec in affected:
    print(f"  {dec.get('decision_id')}  confidence={dec.get('confidence')}  outcome={dec.get('outcome')}")
# decision-a3f1  confidence=0.87  outcome=nation_state_attributed
# decision-b22c  confidence=0.89  outcome=nation_state_attributed
# ...
```

这就是复审工作流：旧策略下的每个决策都被找出来，对照新标准复核，或重新确认、或标记修正。图谱保留完整历史——哪条决策受哪个策略版本管辖，一目了然。

---

## 查看完整审计轨迹

任何时候——总监察长审查、董事会汇报或事件调查——你都可以取回某个策略的完整版本历史。

```python
history = engine.get_policy_history(policy_id)

print(f"Policy versions on record: {len(history)}")
for version in history:
    print(f"  v{version.version}  updated={version.updated_at.date()}  rules_keys={list(version.rules.keys())}")
# v1.0.0  updated=2025-06-21  rules_keys=[min_independent_sources, required_approver_role, ...]
# v1.1.0  updated=2025-09-14  rules_keys=[min_independent_sources, required_approver_role, ...]
#
# The full rules dict for each version is preserved — you can replay exactly
# what the compliance check would have returned for any past decision against
# any past version of the policy.
```

---

## 常见陷阱

**以为合规失败会自动阻止操作。** `PolicyEngine` 返回合规状态，但不会自动阻止操作。你的工作流必须检查返回的布尔值，并决定下一步——批准、驳回、例外处理或升级。

**使用不受支持的规则键。** 实现只支持特定模式：`min_*`、`max_*`、`required_*`、`min_confidence`、`allowed_outcomes` 和 `required_categories`。其他规则键一律退化为键存在性检查：仅当该键在 `decision.metadata` 中恰好存在时才通过，与值无关。这意味着 `disallowed_outcomes` 这类键，在元数据中没有这个字面键时（常见情形）会静默**不通过**；而当元数据中碰巧存在 `disallowed_outcomes` 键时，无论实际 outcome 是什么都静默**通过**。两种行为都不符合"outcome 不得在此列表中"的本意——请改用 `allowed_outcomes`。

**把例外当成审批。** 用 `record_exception()` 记录策略例外，并不会自动让不合规决策变得合规。例外只是审计轨迹条目——是否继续执行不合规决策，仍由你的工作流决定。

**以为 PolicyEngine 会自动修改图状态。** `PolicyEngine` 只做合规评估，并记录策略应用、例外和审批链。它不修改决策结果或元数据，也不阻止操作——这些是工作流的责任。

**使用复杂嵌套规则结构。** 实现不支持复杂条件逻辑、嵌套运算符或任意表达式。保持规则简单：只做单字段比较、列表成员检查和阈值校验。

**规则评估缺少元数据。** 像 `min_credit_score` 这样的规则，要求 `decision.metadata` 中存在对应字段（`credit_score`）。元数据字段缺失会导致规则评估失败，决策即被判为不合规。

**忘记检查规则评估结果。** 合规与不合规两种情况都要显式处理。不合规决策未经妥善例外处理就继续执行，会造成审计缺口和治理风险。

---

## 领域示例

<Tabs>

<Tab title="国防 — CTI/威胁情报">

TLP:RED 情报未经指挥官级审批，不得在原组织之外共享。该策略作用于每一条涉及涉密威胁报告的信息共享决策。违规不会静默记日志，而是路由给 J2 情报官做例外审查。

```python
from semantica.context import ContextGraph, PolicyEngine, Policy, Decision
from semantica.context.decision_recorder import DecisionRecorder
from datetime import datetime

graph    = ContextGraph()
engine   = PolicyEngine(graph_store=graph)
recorder = DecisionRecorder(graph_store=graph)

opsec_policy = Policy(
    policy_id   = "pol-opsec-001",
    name        = "TLP:RED — Restricted Dissemination",
    description = "TLP:RED intelligence must not be shared outside the originating organisation",
    rules = {
        "required_classification":      "TLP:RED",
        "allowed_outcomes":             ["retained_internal", "escalated_internal"],
        "min_confidence":               0.95,
        "required_tlp":                 True,
        "required_authorised_recipients": True,
    },
    category   = "information_sharing",
    version    = "2.1.0",
    created_at = datetime.utcnow(),
    updated_at = datetime.utcnow(),
)
engine.add_policy(opsec_policy)

decision = Decision(
    decision_id   = "",
    category      = "information_sharing",
    scenario      = "APT29 SIGINT report TLP:RED — share with Five Eyes partners?",
    reasoning     = "Tactical intelligence — partner request via UKIC liaison",
    outcome       = "shared_with_partner",   # violates allowed_outcomes policy
    confidence    = 0.88,                    # below min_confidence threshold
    timestamp     = datetime.utcnow(),
    decision_maker= "analyst_rodriguez",
    metadata      = {
        "classification": "TLP:RED",
        "tlp": True,
        "authorised_recipients": True,
    }
)

is_compliant = engine.check_compliance(decision, "pol-opsec-001")
print(f"Compliant: {is_compliant}")
# Compliant: False — outcome 'shared_with_partner' not in allowed_outcomes; confidence below 0.95

if not is_compliant:
    # Route to J2 for exception review — dual commander approval required
    exception_id = engine.record_exception(
        decision_id  = decision.decision_id,
        policy_id    = "pol-opsec-001",
        reason       = "Five Eyes partner urgent request — time-critical tactical intelligence",
        approver     = "j2_officer_hayes",
        justification= "Commander approved limited dissemination under UKUSA Article 4 emergency clause",
    )
    recorder.record_approval_chain(
        decision_id = decision.decision_id,
        approvers   = ["j2_officer_hayes", "unit_commander_brooks"],
        methods     = ["email",             "zoom_call"],
        contexts    = ["J2 tactical review", "Commander emergency approval"],
    )
    print(f"Exception recorded with dual-commander approval: {exception_id}")

# Version history for Inspector General review
history = engine.get_policy_history("pol-opsec-001")
print(f"Policy versions on record: {len(history)}")
```

</Tab>

<Tab title="安全 — SOC/事件响应">

零信任访问策略要求 Tier-1 系统强制多因素认证(MFA)，特权账号必须经 PAM（特权访问管理）会话签出。每一条自动化访问决策都要对照这两条策略检查。当紧急补丁窗口期间 PAM 门户不可用时，SOC 负责人在开工前（而不是事后）登记一条带本人签核的限时例外。

```python
from semantica.context import ContextGraph, PolicyEngine, Policy, Decision
from datetime import datetime

graph  = ContextGraph()
engine = PolicyEngine(graph_store=graph)

for pol in [
    Policy(
        policy_id   = "pol-zt-mfa",
        name        = "MFA Required — All Tier-1",
        description = "Every Tier-1 access decision must verify MFA",
        rules       = {
            "required_mfa_verified":       True,
            "allowed_outcomes":            ["access_granted_with_mfa"],
            "min_confidence":              0.90,
        },
        category   = "access_control",
        version    = "1.0.0",
        created_at = datetime.utcnow(),
        updated_at = datetime.utcnow(),
    ),
    Policy(
        policy_id   = "pol-zt-pam",
        name        = "PAM Checkout — Privileged Accounts",
        description = "Privileged account use requires PAM session checkout",
        rules       = {
            "required_pam_session":        True,
            "required_session_recording":  True,
            "max_session_hours":           4,
            "allowed_outcomes":            ["privileged_access_granted_with_pam"],
        },
        category   = "privileged_access",
        version    = "1.0.0",
        created_at = datetime.utcnow(),
        updated_at = datetime.utcnow(),
    ),
]:
    engine.add_policy(pol)

# Emergency patch window — PAM portal down
decision = Decision(
    decision_id   = "",
    category      = "privileged_access",
    scenario      = "sysadmin_kim patching DC-04 — PAM portal unreachable",
    reasoning     = "Critical patch CVE-2025-1234 — 4-hour RTO — PAM portal offline",
    outcome       = "privileged_access_granted_no_pam",
    confidence    = 0.78,
    timestamp     = datetime.utcnow(),
    decision_maker= "soc_automation",
    metadata      = {
        "pam_session": False,      # PAM checkout failed
        "session_recording": True, # Manual recording in place
        "session_hours": 3,        # Planned session duration
    }
)

pam_compliant = engine.check_compliance(decision, "pol-zt-pam")
print(f"PAM policy compliant: {pam_compliant}")
# PAM policy compliant: False

# SOC lead records the exception before work begins
exception_id = engine.record_exception(
    decision_id  = decision.decision_id,
    policy_id    = "pol-zt-pam",
    reason       = "PAM portal offline during critical patch window",
    approver     = "soc_lead_okafor",
    justification= "Emergency patch approved under BCP §7.3 — manual session logging in place",
)

# What-if: impact of cutting max session hours from 4 to 2 for board risk review
pam_policy = engine.get_policy("pol-zt-pam")
impact = engine.analyze_policy_impact(
    policy_id      = "pol-zt-pam",
    proposed_rules = {**pam_policy.rules, "max_session_hours": 2},
)
print(f"Decisions affected by tighter session cap: {impact.get('affected_decisions', 0)}")
```

</Tab>

<Tab title="生命科学 — 临床/制药">

绝对用药禁忌策略规定：eGFR 低于 30 时禁用二甲双胍。AI 临床决策支持系统在每一条处方决策送达电子健康记录(EHR)之前，先对照该策略检查。当边缘病例需要临床例外时，先记录三人 MDT（多学科团队）审批链——主治医师、肾内科专家和药师——再开具处方。

```python
from semantica.context import ContextGraph, PolicyEngine, Policy, Decision
from semantica.context.decision_recorder import DecisionRecorder
from datetime import datetime

graph    = ContextGraph()
engine   = PolicyEngine(graph_store=graph)
recorder = DecisionRecorder(graph_store=graph)

safety_policy = Policy(
    policy_id   = "pol-clin-001",
    name        = "Metformin Absolute Contraindication — eGFR < 30",
    description = "Metformin must not be prescribed when eGFR is below 30 ml/min/1.73m²",
    rules = {
        "min_egfr":                    30,      # eGFR must be >= 30
        "allowed_outcomes":            ["metformin_discontinued", "metformin_contraindicated", "alternative_prescribed"],
        "required_clinician_sign_off": True,
        "required_egfr_check":         True,
    },
    category   = "clinical_safety",
    version    = "3.0.0",   # aligned to BNF 2024
    created_at = datetime.utcnow(),
    updated_at = datetime.utcnow(),
    metadata   = {"source": "BNF_2024", "strength": "absolute"},
)
engine.add_policy(safety_policy)

# AI decision-support recommendation
decision = Decision(
    decision_id   = "",
    category      = "treatment_modification",
    scenario      = "PT-00841: T2DM, eGFR 28 — metformin review",
    reasoning     = "eGFR 28 is below the 30 threshold; discontinue metformin and initiate SGLT2i",
    outcome       = "metformin_discontinued_dapagliflozin_initiated",
    confidence    = 0.97,
    timestamp     = datetime.utcnow(),
    decision_maker= "cdss_v4",
    metadata      = {
        "egfr": 28,                    # Below minimum threshold
        "clinician_sign_off": True,
        "egfr_check": True,
        "drug": "metformin",
    }
)

is_compliant = engine.check_compliance(decision, "pol-clin-001")
print(f"Compliant: {is_compliant}")
# Compliant: True — outcome is metformin_discontinued, which is allowed

# MDT approval chain for the prescribing record
recorder.record_approval_chain(
    decision_id = decision.decision_id,
    approvers   = ["dr_okonkwo",  "consultant_renal_patel", "pharmacist_kwon"],
    methods     = ["zoom_call",    "zoom_call",               "email"],
    contexts    = [
        "Prescribing physician MDT review",
        "Renal consultant confirmed eGFR 28 — supports discontinuation",
        "Clinical pharmacist approved SGLT2i initiation protocol",
    ],
)
print("MDT approval chain recorded — prescription safe to issue")

# Policy version history for CQC inspection
history = engine.get_policy_history("pol-clin-001")
print(f"Policy versions on record: {len(history)}")
```

</Tab>

<Tab title="银行业 — 风险/合规">

巴塞尔 III 抵押贷款承保策略把贷款价值比(LTV)上限设在 85%，偿债收入比(DSTI)上限设在 40%。信贷模型在每笔放贷决策入账前对照该策略检查。当信贷委员会想在下季度前上调最低信用分门槛时，影响分析会显示当前贷款簿中有多少已批准贷款过不了新规则——而策略变更的审计轨迹会呈送董事会风险委员会。

```python
from semantica.context import ContextGraph, PolicyEngine, Policy, Decision
from datetime import datetime

graph  = ContextGraph()
engine = PolicyEngine(graph_store=graph)

mortgage_policy = Policy(
    policy_id   = "pol-credit-001",
    name        = "Retail Mortgage Underwriting — Basel III CRE20",
    description = "Standard residential mortgage policy aligned to Basel III CRE20",
    rules = {
        "max_ltv":                         0.85,
        "max_dsti":                        0.40,
        "min_credit_score":                680,
        "min_stress_test_bps":             300,
        "allowed_outcomes":                ["approved", "approved_with_conditions"],
    },
    category   = "credit_risk",
    version    = "2.3.0",
    created_at = datetime.utcnow(),
    updated_at = datetime.utcnow(),
    metadata   = {"regulatory_basis": "Basel_III_CRE20", "effective_date": "2025-01-01"},
)
engine.add_policy(mortgage_policy)

# Borderline decision — LTV 86%, one point over the cap
decision = Decision(
    decision_id   = "",
    category      = "mortgage_origination",
    scenario      = "APP-2025-9921: £320k mortgage, LTV 86%, DSTI 38%, credit score 710",
    reasoning     = (
        "LTV 86% exceeds 85% cap. Stress test at +300bps passes. "
        "Credit score 710 above 680 floor. DSTI 38% within 40% limit."
    ),
    outcome       = "approved_ltv_exception",   # not in allowed_outcomes — flags non-compliance
    confidence    = 0.72,
    timestamp     = datetime.utcnow(),
    decision_maker= "underwriting_model_v4",
    metadata      = {
        "ltv": 0.86,           # Exceeds max_ltv of 0.85
        "dsti": 0.38,          # Within max_dsti of 0.40
        "credit_score": 710,   # Above min_credit_score of 680
        "pd": 0.023,           # Recorded for audit — no threshold rule in this policy
        "lgd": 0.45,           # Recorded for audit — no threshold rule in this policy
        "stress_test_bps": 300,
    }
)

is_compliant = engine.check_compliance(decision, "pol-credit-001")
print(f"Compliant: {is_compliant}")
# Compliant: False — ltv (0.86) > max_ltv (0.85) and outcome not in allowed_outcomes

if not is_compliant:
    exception_id = engine.record_exception(
        decision_id  = decision.decision_id,
        policy_id    = "pol-credit-001",
        reason       = "LTV 86% — one point over cap; stress test and all other metrics pass",
        approver     = "sr_underwriter_walsh",
        justification= "Credit committee approved exception under high-quality borrower criteria §4.1",
    )
    print(f"Exception recorded: {exception_id}")

# What-if before raising the credit score floor — present to board risk committee
impact = engine.analyze_policy_impact(
    policy_id      = "pol-credit-001",
    proposed_rules = {**mortgage_policy.rules, "min_credit_score": 700},
)
print(f"Decisions affected by raising credit score floor to 700: {impact.get('affected_decisions', 0)}")

# Find all decisions made under v2.3.0 — re-audit after policy update
affected = engine.get_affected_decisions("pol-credit-001", "2.3.0", "2.4.0")
print(f"Decisions to re-audit: {len(affected)}")

# Commit the update — version bump with full change attribution
engine.update_policy(
    policy_id     = "pol-credit-001",
    rules         = {**mortgage_policy.rules, "min_credit_score": 700},
    change_reason = "Credit committee Q3 review — raise score floor from 680 to 700",
    new_version   = "2.4.0",
)
print("Policy updated to v2.4.0")
```

</Tab>

</Tabs>

---

## 延伸阅读

- [决策智能](./decision-intelligence.md) — `record_decision()`、因果链与先例检索——`check_compliance()` 评估的正是这些决策
- [推理与规则](./reasoning.md) — 用形式化推理补充策略规则，实现逻辑冲突检测
- [SHACL 校验](./shacl-validation.md) — 对策略节点自身施加结构约束
- [变更管理](./change-management.md) — 对策略图谱与知识图谱一起做版本快照
- [溯源](./provenance.md) — 每条策略决策与例外的 W3C PROV-O 血缘
- [MCP 服务器](./mcp-server.md) — 把 `record_decision` 和 `find_precedents` 暴露为模型上下文协议(MCP)工具，供 AI 智能体调用
