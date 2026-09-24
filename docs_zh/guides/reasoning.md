---
title: 推理与规则
description: 在知识图谱上应用前向链、后向链、Datalog、SPARQL、RETE、时态区间与大语言模型推理——推导新事实、检查约束并解释推理过程。
source: guides/reasoning.md
source_version: f715be19a86132dcc0b7f0bb98bc5abe4020a7f6
---

Semantica 的推理层把领域逻辑编码成规则，应用到你的知识图谱(Knowledge Graph)上，推导出任何单篇文档都没有明说的结论。八种互补的推理模式——从符号规则的前向链(Forward Chaining)，到递归的 Datalog，再到由大语言模型(LLM)支撑的自由问答——让你为每个推理问题选对工具，而不必切换框架。

## 什么是推理？

推理(Reasoning)用逻辑规则从显式事实中推导出隐含知识。与检索、搜索或图遍历不同，推理会产生原始数据中没有直接写明的新结论。

**推理与检索：** 检索找到的是与查询匹配的既有信息；推理则运用逻辑规则，推导出从未显式存储的新事实。

**推理与搜索：** 搜索匹配的是关键词或语义相似度；推理用逻辑推演得出结论，比如"若 A 蕴含 B，且 A 为真，则 B 必为真"。

**推理与图遍历：** 遍历沿节点间已有的边走；推理能依据规则推断出新的关系——例如在不存在直接边的情况下，断定两个实体之间存在关联。

## 为什么使用推理？

**推导隐含知识。** 文档可能分别提到"APT29 使用 SUNBURST"和"SUNBURST 利用 CVE-2020-10148"，推理会自动得出"APT29 利用 CVE-2020-10148"。

**识别模式。** 规则可以检测知识图谱中的复杂模式——共享相同 TTP 的威胁行为者(Threat Actor)、处于传递关系中的供应商，或者由多个条件组合涌现出的合规违规。

**辅助调查。** 推理帮分析师突出非显而易见的关联，标记满足风险标准的实体，并解释结论是如何得出的。

**决策支持。** 把政策、法规或业务规则编码成逻辑命题，推理引擎(Reasoning Engine)会始终如一地评估它们，并为决策留下审计轨迹(audit trail)。

## 适用与不适用场景

**适合用推理：**
- 逻辑关系定义清晰的复杂领域
- 政策执行与合规检查
- 结论依赖事实链条的多步推断
- 需要可解释、可审计的决策并保留审计轨迹的场合
- 识别未明确表述的隐含关系

**检索可能已经够用：**
- 查找能直接回答问题的文档或信息
- 尚不知道要找什么模式的探索性研究
- 简单的关键词或语义搜索

**图遍历可能已经够用：**
- 沿实体间的显式关系追踪
- 围绕已知起点做邻域分析
- 在有直接连接的实体之间寻路

**推理能带来额外价值：**
- 领域中存在能推导新事实的逻辑规则
- 需要检测须满足多个条件的模式
- 决策必须可解释、可审计
- 隐含关系与显式关系同样重要

## 核心推理概念

**Datalog** 是一种基于规则和事实的逻辑编程语言。事实是简单命题，比如 "parent(tom, bob)"；规则用来推导新事实："grandparent(X, Z) :- parent(X, Y), parent(Y, Z)"。Datalog 擅长递归查询和传递关系。

**SPARQL** 是面向资源描述框架(RDF)数据的查询语言，可以结合推理规则使用。它用三元组模式匹配图数据，还能扩展出推理能力，在查询之前先推导出隐含三元组。

**RETE** 是一种在事实工作内存(Working Memory)上高效评估大量规则的算法。它构建一张网络，避免对未变化的条件重复求值，因此适合拥有数百条规则或处理流式数据的系统。

**基于规则的推理** 应用"如果-那么"规则推导新结论。前向链应用所有适用的规则，推导出一切可推导的结论；后向链(Backward Chaining)则从目标出发反向求解，找到最小的证明。

## 图数据如何变成推理事实

调用 `DatalogReasoner.load_from_graph()` 时，知识图谱的节点和边会被转换成 Datalog 事实，所有谓词和参数都转为小写：

- 类型为 "ThreatActor"、id 为 "APT29" 的节点变成 `threatactor(apt29)`
- 从 APT29 指向 SUNBURST、类型为 "uses" 的边变成 `uses(apt29, sunburst)`

推理引擎把这些事实当作推理的起点，应用规则推导出新结论，并把它们加入工作内存。

<Info>
推理模块处理你直接提供的事实，或从 `ContextGraph` 加载的事实。派生事实会加入工作内存，并在同一会话中立即可用于进一步的推理。要把派生事实持久化回图谱，请把它们传给 `AgentContext.store()`。
</Info>

## 选择推理模式

| 模式 | 最适合 | 类 |
|---|---|---|
| 前向链 | 从基础事实出发，物化所有隐含事实 | `Reasoner.forward_chain()` |
| 后向链 | 证明特定目标；拿到最小证据链 | `Reasoner.backward_chain()` |
| Datalog | 任意深度的递归遍历（供应链、组织架构图） | `DatalogReasoner` |
| SPARQL | 在增强后的工作内存上做模式匹配查询 | `SPARQLReasoner` |
| RETE | 100 条以上的规则集——经 alpha/beta 网络增量传播事实 | `ReteEngine` |
| 时态推理(Temporal Reasoning) | 时间窗口之间的 Allen 区间代数(Allen Interval Algebra)关系 | `TemporalReasoningEngine` |
| 自然语言 | 由 LLM 支撑、面向图上下文的自由问答 | `GraphReasoner` |
| 解释 | 把推理结果翻译成人类可读的论证 | `ExplanationGenerator` |

## 第 1 步 — 基础事实与工作内存

`Reasoner` 类维护一组基础事实(ground facts)和一份规则列表。事实可以作为谓词字符串添加，也可以从 `ContextGraph` 加载。先从抽取流水线产出的显式知识开始：

```python
from semantica.reasoning import Reasoner, Rule, RuleType

reasoner = Reasoner()

# Ground facts: Predicate(arg) or Predicate(arg1, arg2)
reasoner.add_fact("ThreatActor(APT29)")
reasoner.add_fact("ThreatActor(GAMMA-7)")
reasoner.add_fact("ThreatActor(DELTA-3)")
reasoner.add_fact("Exploits(APT29, CVE-2025-3400)")
reasoner.add_fact("Exploits(GAMMA-7, CVE-2025-1234)")
reasoner.add_fact("Exploits(GAMMA-7, CVE-2025-5678)")
reasoner.add_fact("CriticalVuln(CVE-2025-3400)")
reasoner.add_fact("CriticalVuln(CVE-2025-1234)")
reasoner.add_fact("CriticalVuln(CVE-2025-5678)")
reasoner.add_fact("Targets(APT29, NATOLogistics)")
reasoner.add_fact("Targets(GAMMA-7, NATOLogistics)")
reasoner.add_fact("SuppliedExploits(DELTA-3, GAMMA-7)")
reasoner.add_fact("SectorOverlap(NATOLogistics, CriticalInfrastructure)")
```

这些基础事实代表文档明确说过的内容。接下来添加的规则，则告诉系统这些事实*蕴含*着什么。

## 第 2 步 — 前向链：物化派生事实

前向链从基础事实出发，反复应用所有匹配的规则，直到推不出任何新结论——也就是到达不动点(Fixpoint)：

```python
# String-format rules are parsed automatically
# Variables are single uppercase letters or multi-character uppercase words
reasoner.add_rule(
    "IF ThreatActor(X) AND Exploits(X, Y) AND CriticalVuln(Y) THEN HighRiskActor(X)"
)
reasoner.add_rule(
    "IF HighRiskActor(X) AND Targets(X, Z) THEN CriticalTarget(Z)"
)
reasoner.add_rule(
    "IF SuppliedExploits(A, B) AND HighRiskActor(B) THEN HighRiskSupplier(A)"
)

# forward_chain() applies all rules until fixpoint
derived = reasoner.forward_chain()

for result in derived:
    print("{:<40s}  conf={:.0%}  rule={}".format(
        result.conclusion,
        result.confidence,
        result.rule_used.name if result.rule_used else "n/a",
    ))
```

```text
HighRiskActor(APT29)                      conf=100%  rule=Rule 1
HighRiskActor(GAMMA-7)                    conf=100%  rule=Rule 1
CriticalTarget(NATOLogistics)             conf=100%  rule=Rule 2
HighRiskSupplier(DELTA-3)                 conf=100%  rule=Rule 3
```

DELTA-3 被标记了出来，尽管没有任何文档这样描述过它——系统回溯出了这条链：DELTA-3 向 GAMMA-7 供给漏洞利用，而 GAMMA-7 利用的是关键 CVE。规则需要优先级排序或分级置信度时，改用 `Rule` dataclass：

如果规则带有副作用动作，同一个具体激活在 `Reasoner` 实例上至多执行这些动作一次。因此重复调用 `forward_chain()` 是安全的：已经尝试过的动作不会再次执行。当你有意想重放这些动作时，调用 `reasoner.reset_action_history()`；`reasoner.clear()` 和 `reasoner.reset()` 也会清空这段历史。

```python
# Higher priority rules fire first; confidence propagates into InferenceResult.confidence
reasoner.add_rule(Rule(
    rule_id="attr-1",
    name="ttp_match_attribution",
    conditions=["ThreatActor(X)", "Exploits(X, CVE)", "CriticalVuln(CVE)"],
    conclusion="HighRiskActor(X)",
    rule_type=RuleType.IMPLICATION,
    confidence=0.92,
    priority=10,
))

reasoner.add_rule(Rule(
    rule_id="attr-2",
    name="supplier_elevation",
    conditions=["SuppliedExploits(A, B)", "HighRiskActor(B)"],
    conclusion="HighRiskSupplier(A)",
    rule_type=RuleType.IMPLICATION,
    confidence=0.85,
    priority=5,
))
```

## 第 3 步 — 后向链：证明特定目标

后向链在规则中反向回溯，检验单个假设——当你需要一个"是/否"答案和最小证据链，而不想先把其他所有可能的事实都推导一遍时，它正是合适的工具：

```python
# backward_chain() returns an InferenceResult if the goal is provable, None otherwise
result = reasoner.backward_chain("HighRiskSupplier(DELTA-3)", max_depth=5)

if result:
    print("Proved: {}".format(result.conclusion))
    print("Via premises:")
    for p in result.premises:
        print("  - {}".format(p))
    print("Confidence: {:.0%}".format(result.confidence))
else:
    print("Goal not provable — DELTA-3 is not classified as a high-risk supplier "
          "given current facts and rules")
```

```text
Proved: HighRiskSupplier(DELTA-3)
Via premises:
  - SuppliedExploits(DELTA-3, GAMMA-7)
  - HighRiskActor(GAMMA-7)
Confidence: 85%
```

premises 列表就是解释链——其中每一项都是得出结论所必需的事实。当分析师问"为什么 DELTA-3 被归为高风险？"时，把这份列表展示给他们。

## 第 4 步 — 用 Datalog 做递归推理

`DatalogReasoner` 处理需要任意深度遍历的问题——"哪些行为者能传递地到达关键基础设施？"——它使用递归 Horn 子句(Horn clause)和半朴素(semi-naive)自底向上的不动点求值：

```python
from semantica.reasoning import DatalogReasoner

dl = DatalogReasoner()

# EDB (Extensional DB) — base facts; arguments are constants (lowercase)
dl.add_fact("supplied(delta3, gamma7)")
dl.add_fact("supplied(gamma7, apt29_affiliate)")
dl.add_fact("supplied(apt29_affiliate, apt29)")
dl.add_fact("targets(apt29, nato_logistics)")
dl.add_fact("targets(gamma7, nato_logistics)")
dl.add_fact("sector(nato_logistics, critical_infrastructure)")

# IDB (Intensional DB) — recursive rules; uppercase = variable
# Base case: direct supply link
dl.add_rule("reaches(X, Y) :- supplied(X, Y).")
# Recursive case: X reaches Y if X supplies Z and Z reaches Y
dl.add_rule("reaches(X, Y) :- supplied(X, Z), reaches(Z, Y).")

# Derived predicate combining reachability with sector membership
dl.add_rule("sector_exposure(Actor, Sector) :- reaches(Actor, Target), sector(Target, Sector).")
dl.add_rule("sector_exposure(Actor, Sector) :- targets(Actor, Target), sector(Target, Sector).")

# derive_all() runs semi-naive fixpoint until no new facts emerge
dl.derive_all()

# Query with free variables — returns list of binding dicts
exposures = dl.query("sector_exposure(?actor, critical_infrastructure)")
for row in exposures:
    print("CI-exposed actor: {}".format(row["actor"]))
```

```text
CI-exposed actor: delta3
CI-exposed actor: gamma7
CI-exposed actor: apt29_affiliate
CI-exposed actor: apt29
```

DELTA-3 也出现了，尽管没有任何文档把它与关键基础设施直接关联。Datalog 追踪出了完整链条：delta3 → gamma7 → apt29_affiliate → apt29 → nato_logistics → critical_infrastructure。

绑定变量可以提出有方向的问题：

```python
# Which sectors does delta3 have exposure to?
rows = dl.query("sector_exposure(delta3, ?sector)")
for row in rows:
    print("delta3 → sector: {}".format(row["sector"]))
```

跳过手动调用 `add_fact()`，直接加载 `ContextGraph`：

```python
from semantica.context import ContextGraph

graph = ContextGraph()
# ... graph populated by AgentContext.store() or extraction pipeline ...
count = dl.load_from_graph(graph)
print("Loaded {} facts from graph".format(count))
```

## 第 5 步 — 在增强后的工作内存上做 SPARQL 查询

前向链推导出新事实之后，`SPARQLReasoner` 在增强后的工作内存上准备 SPARQL 查询，并可选地做推理扩展：

```python
from semantica.reasoning import SPARQLReasoner

sparql = SPARQLReasoner()

# Inference rules expand the SPARQL query before execution
sparql.add_inference_rule(
    "IF ThreatActor(X) AND Exploits(X, Y) AND CriticalVuln(Y) THEN HighRiskActor(X)"
)

query = """
    SELECT ?actor ?cve WHERE {
        ?actor <Exploits> ?cve .
        ?cve   <CriticalVuln> true .
    }
"""

# expand_query() applies inference rules to the query text:
expanded = sparql.expand_query(query)
print(expanded)
```

`execute_query()` 尚未实现：目前不存在三元组库(Triplet Store)执行路径，所以它会抛出 `NotImplementedError`，而不是返回一个容易被调用方误读为"无匹配"的空结果集。在执行能力落地之前，请把扩展后的查询直接对着你的 RDF 库运行（例如用 `rdflib`）。

运行前先检查扩展后的查询：

```python
# See the query after inference rules are applied
expanded = sparql.expand_query(query)
print(expanded)
```

## 第 6 步 — 面向大规模规则集的 RETE 引擎

`ReteEngine` 实现了 RETE 算法——一张由 alpha 节点（单条件匹配）和 beta 节点（连接操作）组成的网络，避免每来一条新事实就对未变化的条件重新求值。当你的规则超过 100 条，或者需要在流式、事件驱动场景下增量传播事实时，用它：

```python
from semantica.reasoning import ReteEngine, Rule, RuleType, Fact

# Define rules as Rule objects — same Rule class used by Reasoner
rules = [
    Rule(
        rule_id="r1", name="port_scan_detected",
        conditions=["PortScan(Source)", "HighFrequency(Source)"],
        conclusion="Scanning(Source)",
        confidence=0.90, priority=10,
    ),
    Rule(
        rule_id="r2", name="c2_beacon_identified",
        conditions=["Scanning(Source)", "BeaconPattern(Source, Dest)"],
        conclusion="C2Channel(Source, Dest)",
        confidence=0.85, priority=8,
    ),
    Rule(
        rule_id="r3", name="lateral_movement_detected",
        conditions=["C2Channel(Source, Dest)", "InternalHost(Dest)"],
        conclusion="LateralMovement(Source, Dest)",
        confidence=0.80, priority=5,
    ),
]

engine = ReteEngine()
engine.build_network(rules)   # compile rules into alpha/beta/terminal node network

# Facts are structured: Fact(fact_id, predicate, [arguments])
engine.add_fact(Fact("f1", "PortScan",      ["192.168.1.50"]))
engine.add_fact(Fact("f2", "HighFrequency", ["192.168.1.50"]))
engine.add_fact(Fact("f3", "BeaconPattern", ["192.168.1.50", "10.0.0.5"]))
engine.add_fact(Fact("f4", "InternalHost",  ["10.0.0.5"]))

# match_patterns() returns Match objects: rule + matched facts + confidence
matches = engine.match_patterns()
print("Rule activations: {}".format(len(matches)))

# execute_matches() fires each matched rule and returns the derived conclusions
conclusions = engine.execute_matches(matches)
for c in conclusions:
    print("Derived:", c)

# Network diagnostics — useful for verifying rule compilation
stats = engine.get_network_stats()
print("Nodes: {total_nodes}  Alpha: {alpha_nodes}  Beta: {beta_nodes}  Facts: {facts}".format(**stats))

# Clear working memory without recompiling the rule network
engine.reset()
```

规则网络由 `build_network()` 编译一次。之后每次调用 `add_fact()`，事实只增量穿过条件得到满足的那些节点——而不是整套规则——求值开销因此与新激活的数量成正比，而不是与规则总数成正比。

绑定了 `Reasoner` 时，RETE 的动作副作用按"每条规则、每组绑定、每个匹配事实"至多尝试一次。把同一个 match 再次传给 `execute_matches()` 仍会返回相同的结论，但不会重复执行动作。调用 `engine.reset_action_history()` 可以在不清空工作内存的前提下重放动作；`engine.reset()` 和 `engine.build_network()` 同样会清空动作历史。

## 第 7 步 — 时态区间推理

`TemporalReasoningEngine` 计算时间窗口之间的 Allen 区间关系，让你在图谱中判断两个事件是重叠、一个包含另一个、还是在边界相接，等等：

```python
from datetime import datetime, timezone
from semantica.reasoning import TemporalReasoningEngine, TemporalInterval, IntervalRelation

engine = TemporalReasoningEngine()

def dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)

# Encode time windows as datetimes
nightfall  = TemporalInterval(start=dt("2025-01-01T00:00:00Z"), end=dt("2025-03-31T23:59:59Z"))
sandstorm  = TemporalInterval(start=dt("2025-03-15T00:00:00Z"), end=dt("2025-06-30T23:59:59Z"))
frostbite  = TemporalInterval(start=dt("2025-07-01T00:00:00Z"), end=dt("2025-09-30T23:59:59Z"))

relation_ns = engine.relation(nightfall, sandstorm)
relation_nf = engine.relation(nightfall, frostbite)

print("NIGHTFALL vs SANDSTORM:", relation_ns)
# IntervalRelation.OVERLAPS — both active simultaneously in mid-March 2025
# Warrants investigation for shared C2 infrastructure or coordination

print("NIGHTFALL vs FROSTBITE:", relation_nf)
# IntervalRelation.BEFORE — no temporal overlap; likely independent campaigns
```

13 种 Allen 关系覆盖了所有可能的时间关系：

| 关系 | 含义 |
|---|---|
| `BEFORE` | A 在 B 开始之前结束 |
| `MEETS` | A 的结束恰好是 B 的开始（无间隙、无重叠） |
| `OVERLAPS` | A 在 B 之前开始，并在 B 期间结束 |
| `STARTS` | A 与 B 同时开始；A 先结束 |
| `DURING` | A 完全包含在 B 之内 |
| `FINISHES` | A 与 B 同时结束；A 后开始 |
| `EQUALS` | A 与 B 是完全相同的区间 |
| `AFTER`, `MET_BY`, `OVERLAPPED_BY`, `STARTED_BY`, `CONTAINS`, `FINISHED_BY` | 以上关系的逆 |

两个归到不同行为者名下的行动之间出现 `OVERLAPS` 或 `EQUALS`，是值得标记出来供分析师复核的信号——时间上的巧合只是假设，不是结论。

## 第 8 步 — 基于 LLM 的图推理

`GraphReasoner` 把自由形式的自然语言查询交给 LLM 提供方处理，并把图谱作为有据可查的上下文。适合那些无法干净映射到预定义规则集的探索性问题：

```python
from semantica.reasoning import GraphReasoner
from semantica.context import ContextGraph

# Initialise with any supported LLM provider
gr = GraphReasoner(provider="openai", model="gpt-4o-mini")

# Build a knowledge graph
graph = ContextGraph()
graph.add_node("apt29",          "ThreatActor",   "APT29 / NOBELIUM", country="Russia")
graph.add_node("cve-2025-3400",  "Vulnerability", "PAN-OS RCE",       cvss=9.8)
graph.add_node("nato_logistics", "Target",        "NATO Logistics Network")
graph.add_edge("apt29", "cve-2025-3400",  "exploits", weight=0.97)
graph.add_edge("apt29", "nato_logistics", "targets",  weight=0.88)

# GraphReasoner expects {"entities": [...], "relationships": [...]}
raw = graph.to_dict()
graph_data = {
    "entities":      raw.get("nodes", []),
    "relationships": raw.get("edges", []),
}

answer = gr.reason(
    graph=graph_data,
    query="Which threat actors pose the highest risk to NATO infrastructure, "
          "and what evidence in the graph supports that assessment?"
)
print(answer)
```

`GraphReasoner` 适合调查的早期阶段——问题仍处于探索状态、推理规则尚未形式化的时候。需要可复现、可审计的决策时，请改用 `Reasoner` 或 `DatalogReasoner`。

## 第 9 步 — 用自然语言解释推理

`ExplanationGenerator` 把任意 `InferenceResult`（来自前向链或后向链）翻译成人类可读的解释、逐步的 `ReasoningPath`，以及附支撑证据的 `Justification`：

```python
from semantica.reasoning import Reasoner, Rule, RuleType, ExplanationGenerator

# Run inference first
reasoner = Reasoner()
reasoner.add_fact("ThreatActor(APT29)")
reasoner.add_fact("Exploits(APT29, CVE-2025-3400)")
reasoner.add_fact("CriticalVuln(CVE-2025-3400)")

reasoner.add_rule(Rule(
    rule_id="r1", name="high_risk_actor",
    conditions=["ThreatActor(X)", "Exploits(X, Y)", "CriticalVuln(Y)"],
    conclusion="HighRiskActor(X)",
    confidence=0.92,
))

derived = reasoner.forward_chain()

# detail_level options: "simple", "detailed", "verbose"
gen = ExplanationGenerator(generate_nl=True, detail_level="detailed")

for result in derived:
    exp = gen.generate_explanation(result)
    print("Conclusion:  {}".format(exp.conclusion))
    print("Explanation: {}".format(exp.natural_language))
    print()

    # Step-by-step reasoning path
    path = gen.show_reasoning_path(result)
    print("Reasoning path ({} steps, confidence {:.0%}):".format(
        len(path.steps), path.total_confidence
    ))
    for step in path.steps:
        print("  [{}] {}".format(step.step_id, step.description))

    # Justification with full evidence list
    just = gen.justify_conclusion(result.conclusion, path)
    print("Justification: {}".format(just.explanation_text))
    print("Supporting evidence: {}".format(just.supporting_evidence))
```

```text
Conclusion:  HighRiskActor(APT29)
Explanation: Given the premises: ThreatActor(APT29), Exploits(APT29, CVE-2025-3400),
             CriticalVuln(CVE-2025-3400), we conclude: HighRiskActor(APT29)
             using rule 'high_risk_actor'.
```

三个细节级别控制解释的详略程度：`"simple"` 给出一行摘要，`"detailed"` 列出前提与规则名，`"verbose"` 生成带完整置信度标注的叙述。

## 组合起来：完整的推理流水线

一条为威胁情报(Threat Intelligence)图谱组合了前向链、Datalog 可达性与自然语言解释的流水线：

```python
from semantica.reasoning import (
    Reasoner, Rule, RuleType,
    DatalogReasoner, ExplanationGenerator,
)
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore


def run_threat_reasoning(graph: ContextGraph) -> dict:
    """Apply inference rules to a threat intelligence graph."""

    # --- Forward chaining: derive actor classifications ---
    reasoner = Reasoner()

    for edge in graph.find_edges():
        src = edge.get("source", "")
        dst = edge.get("target", "")
        rel = edge.get("type", "related_to")
        if src and dst:
            reasoner.add_fact("{}({}, {})".format(rel.replace(" ", "_"), src, dst))

    for node in graph.find_nodes():
        name  = node.get("name", node.get("id", ""))
        ntype = node.get("type", "Entity")
        if name:
            reasoner.add_fact("{}({})".format(ntype.replace(" ", "_"), name))

    reasoner.add_rule(Rule(
        rule_id="r1", name="high_risk_actor",
        conditions=["ThreatActor(X)", "Exploits(X, CVE)", "CriticalVuln(CVE)"],
        conclusion="HighRiskActor(X)", confidence=0.92, priority=10,
    ))
    reasoner.add_rule(Rule(
        rule_id="r2", name="critical_target",
        conditions=["HighRiskActor(X)", "Targets(X, Z)"],
        conclusion="CriticalTarget(Z)", confidence=0.88, priority=8,
    ))
    reasoner.add_rule(Rule(
        rule_id="r3", name="supplier_elevation",
        conditions=["SuppliedExploits(A, B)", "HighRiskActor(B)"],
        conclusion="HighRiskSupplier(A)", confidence=0.85, priority=5,
    ))

    derived = reasoner.forward_chain()

    high_risk_actors    = [r for r in derived if "HighRiskActor"    in r.conclusion]
    critical_targets    = [r for r in derived if "CriticalTarget"   in r.conclusion]
    high_risk_suppliers = [r for r in derived if "HighRiskSupplier" in r.conclusion]

    # --- Backward chaining: verify a specific supplier hypothesis ---
    supplier_result = reasoner.backward_chain("HighRiskSupplier(DELTA-3)", max_depth=5)

    # --- Datalog: transitive supply-chain reachability ---
    dl = DatalogReasoner()
    dl.load_from_graph(graph)
    dl.add_rule("reaches(X, Y) :- supplied(X, Y).")
    dl.add_rule("reaches(X, Y) :- supplied(X, Z), reaches(Z, Y).")
    dl.add_rule("sector_exposure(Actor, Sector) :- reaches(Actor, T), sector(T, Sector).")
    dl.add_rule("sector_exposure(Actor, Sector) :- targets(Actor, T), sector(T, Sector).")
    dl.derive_all()
    ci_exposures = dl.query("sector_exposure(?actor, critical_infrastructure)")

    # --- ExplanationGenerator: analyst-readable justifications ---
    gen = ExplanationGenerator(generate_nl=True, detail_level="detailed")
    explanations = {}
    for result in high_risk_actors:
        exp = gen.generate_explanation(result)
        explanations[result.conclusion] = exp.natural_language

    return {
        "high_risk_actors":    [r.conclusion for r in high_risk_actors],
        "critical_targets":    [r.conclusion for r in critical_targets],
        "high_risk_suppliers": [r.conclusion for r in high_risk_suppliers],
        "delta3_flagged":      supplier_result is not None,
        "ci_exposed_actors":   [row["actor"] for row in ci_exposures],
        "total_derived":       len(derived),
        "explanations":        explanations,
    }


intel_graph = ContextGraph(advanced_analytics=True)
agent = AgentContext(
    vector_store=VectorStore(backend="faiss", dimension=768),
    knowledge_graph=intel_graph,
)
# ... populate via agent.store() or extraction pipeline ...

report = run_threat_reasoning(intel_graph)
print("Derived {} new facts".format(report["total_derived"]))
print("High-risk actors:  {}".format(report["high_risk_actors"]))
print("CI-exposed actors: {}".format(report["ci_exposed_actors"]))
print("DELTA-3 flagged:   {}".format(report["delta3_flagged"]))

for conclusion, text in report["explanations"].items():
    print("\n[{}]\n  {}".format(conclusion, text))
```

## 领域示例

<Tabs>

<Tab title="国防 — CTI/威胁情报">

威胁情报中的归因链需要多跳置信度传播：一次 TTP 匹配提高行为者归因的概率，ASN 地理位置的佐证让它更进一步，而针对被归因行业的已知目标模式则把它提升到可行动的置信度。每一跳都是一条独立规则，各带自己的置信度权重，`InferenceResult` 携带传播后的值穿过整条链。

```python
from semantica.reasoning import Reasoner, Rule, RuleType

reasoner = Reasoner()

# SIGINT-derived facts
reasoner.add_fact("C2Beacon(10.0.0.5, AS59796)")
reasoner.add_fact("ASN_Country(AS59796, Russia)")
reasoner.add_fact("TTP(T1566.001, APT29)")           # MITRE ATT&CK mapping
reasoner.add_fact("ObservedTTP(10.0.0.5, T1566.001)")
reasoner.add_fact("TargetSector(10.0.0.5, Aerospace)")

# Three-stage attribution ruleset with confidence ladder
reasoner.add_rule(Rule(
    rule_id="attr-1", name="ttp_match",
    conditions=["ObservedTTP(IP, TTP)", "TTP(TTP, Actor)"],
    conclusion="SuspectedActor(IP, Actor)",
    confidence=0.75, priority=10,
))
reasoner.add_rule(Rule(
    rule_id="attr-2", name="asn_corroboration",
    conditions=["SuspectedActor(IP, Actor)", "C2Beacon(IP, ASN)", "ASN_Country(ASN, Country)"],
    conclusion="CorroboratedActor(IP, Actor, Country)",
    confidence=0.90, priority=5,
))
reasoner.add_rule(Rule(
    rule_id="attr-3", name="sector_confirmation",
    conditions=["CorroboratedActor(IP, Actor, Russia)", "TargetSector(IP, Aerospace)"],
    conclusion="HighConfidenceAttribution(IP, Actor)",
    confidence=0.95, priority=1,
))

derived = reasoner.forward_chain()
attributions = [r for r in derived if "HighConfidenceAttribution" in r.conclusion]

for a in attributions:
    print("{:50s}  conf={:.0%}".format(a.conclusion, a.confidence))
    print("  Premises: {}".format(a.premises))

# HighConfidenceAttribution(10.0.0.5, APT29)    conf=95%
#   Premises: ['SuspectedActor(10.0.0.5, APT29)', 'CorroboratedActor(10.0.0.5, APT29, Russia)', ...]
```

</Tab>

<Tab title="安全 — SOC/事件响应">

零信任(Zero Trust)访问控制决策可以在查询时求值：把策略编码成规则，对具体的访问请求做后向链推理。证明本身——或证明的缺失——就是可解释的决策记录，随时可供审计。

如果后向链失败，部分结果里的 premises 列表会准确告诉分析师是哪条策略条件未被满足——比一句笼统的"访问被拒绝"有用得多。

```python
from semantica.reasoning import Reasoner, Rule, RuleType

reasoner = Reasoner()

# Identity and resource facts for the current session
reasoner.add_fact("User(alice)")
reasoner.add_fact("HasMFA(alice)")
reasoner.add_fact("Role(alice, analyst)")
reasoner.add_fact("Clearance(alice, SECRET)")
reasoner.add_fact("Resource(kube-api, tier1)")
reasoner.add_fact("RequiresClearance(kube-api, SECRET)")
reasoner.add_fact("RequiresMFA(tier1)")

# Zero-trust access policy as inference rules
reasoner.add_rule(
    "IF User(U) AND HasMFA(U) AND RequiresMFA(T) AND Resource(R, T) THEN MFASatisfied(U, R)"
)
reasoner.add_rule(
    "IF User(U) AND Clearance(U, C) AND RequiresClearance(R, C) THEN ClearanceSatisfied(U, R)"
)
reasoner.add_rule(
    "IF MFASatisfied(U, R) AND ClearanceSatisfied(U, R) THEN AccessGranted(U, R)"
)

# Backward-chain the access decision
result = reasoner.backward_chain("AccessGranted(alice, kube-api)", max_depth=5)

if result:
    print("ACCESS GRANTED: {}".format(result.conclusion))
    print("Justified by:")
    for p in result.premises:
        print("  - {}".format(p))
else:
    print("ACCESS DENIED — one or more policy conditions not satisfied")
    partial = reasoner.forward_chain()
    for r in partial:
        print("  Partial: {}".format(r.conclusion))
```

</Tab>

<Tab title="生命科学 — 临床/制药">

药物相互作用检测与前向链天然契合：酶抑制和代谢通路的事实是静态的，相互作用风险的规则是标准化的药理学知识，而输出——派生事实 `ClinicallySignificantInteraction`——需要在处方确认之前可靠地触发。

传递情形交给 Datalog：如果药物 A 诱导酶 E1，而 E1 代谢药物 B，整条暴露链可以递归追踪，无需预先知道它的深度。

```python
from semantica.reasoning import Reasoner, DatalogReasoner

# Forward-chain: detect clinically significant interactions
reasoner = Reasoner()

reasoner.add_fact("Metabolizes(CYP2C9, Warfarin)")
reasoner.add_fact("Inhibits(Amiodarone, CYP2C9)")
reasoner.add_fact("DrugInPatient(Warfarin)")
reasoner.add_fact("DrugInPatient(Amiodarone)")
reasoner.add_fact("TherapeuticWindow(Warfarin, narrow)")

reasoner.add_rule(
    "IF Inhibits(DrugA, Enzyme) AND Metabolizes(Enzyme, DrugB) "
    "AND DrugInPatient(DrugA) AND DrugInPatient(DrugB) "
    "THEN PotentialInteraction(DrugA, DrugB)"
)
reasoner.add_rule(
    "IF PotentialInteraction(DrugA, DrugB) AND TherapeuticWindow(DrugB, narrow) "
    "THEN ClinicallySignificantInteraction(DrugA, DrugB)"
)

derived = reasoner.forward_chain()
for r in derived:
    if "ClinicallySignificant" in r.conclusion:
        print("ALERT: {}  (conf={:.0%})".format(r.conclusion, r.confidence))
        print("  Rule: {}".format(r.rule_used.name if r.rule_used else "n/a"))

# ALERT: ClinicallySignificantInteraction(Amiodarone, Warfarin)  (conf=100%)

# Datalog: transitive enzyme induction chain
dl = DatalogReasoner()
dl.add_fact("metabolises(CYP3A4, midazolam)")
dl.add_fact("metabolises(CYP3A4, cyclosporin)")
dl.add_fact("induces(rifampicin, CYP3A4)")
dl.add_rule("reduces_exposure(X, Drug) :- induces(X, Enzyme), metabolises(Enzyme, Drug).")
dl.add_rule("reduces_exposure(X, Drug) :- induces(X, Z), reduces_exposure(Z, Drug).")

dl.derive_all()
reductions = dl.query("reduces_exposure(rifampicin, ?drug)")
for row in reductions:
    print("Rifampicin reduces exposure to: {}".format(row["drug"]))

# Rifampicin reduces exposure to: midazolam
# Rifampicin reduces exposure to: cyclosporin
```

</Tab>

<Tab title="银行业 — 风险/合规">

巴塞尔协议 III(Basel III)的资本充足率规则可以自然转写成前向链推理规则：每条监管条件是一个事实，每个条款是一条规则，资本决策是推导出的结论。规则链就是审计轨迹——审查员可以确切检查哪些条件被触发、以何种顺序触发。

后向链适合压力测试："在什么条件下这笔贷款会得到 `ConditionalApproval`？"——通过证明该目标并呈现所需的最小事实集合来回答。

```python
from semantica.reasoning import Reasoner, Rule, RuleType

reasoner = Reasoner()

# Loan application facts
reasoner.add_fact("Loan(LOAN-2025-88421)")
reasoner.add_fact("LTV(LOAN-2025-88421, 0.78)")
reasoner.add_fact("PD(LOAN-2025-88421, 0.023)")
reasoner.add_fact("LGD(LOAN-2025-88421, 0.45)")
reasoner.add_fact("AssetClass(LOAN-2025-88421, CRE)")
reasoner.add_fact("DSCR(LOAN-2025-88421, 1.12)")

# Basel III CRE20 capital rules
reasoner.add_rule(Rule(
    rule_id="cre20-1", name="ltv_rwa_bucket",
    conditions=["Loan(L)", "LTV(L, V)", "AssetClass(L, CRE)"],
    conclusion="RWABucket(L, high)",
    confidence=0.98, priority=10,
))
reasoner.add_rule(Rule(
    rule_id="cre20-2", name="dscr_adequate",
    conditions=["Loan(L)", "DSCR(L, D)"],
    conclusion="DSCRAdequate(L)",
    confidence=0.95, priority=8,
))
reasoner.add_rule(Rule(
    rule_id="cre20-3", name="conditional_approval",
    conditions=["Loan(L)", "RWABucket(L, high)", "DSCRAdequate(L)"],
    conclusion="ConditionalApproval(L)",
    confidence=0.87, priority=5,
))

derived = reasoner.forward_chain()
for r in derived:
    print("{:45s}  [{:.0%}]".format(r.conclusion, r.confidence))

# RWABucket(LOAN-2025-88421, high)                  [98%]
# DSCRAdequate(LOAN-2025-88421)                      [95%]
# ConditionalApproval(LOAN-2025-88421)               [87%]

# Audit: prove the approval decision and show its full justification
proof = reasoner.backward_chain("ConditionalApproval(LOAN-2025-88421)", max_depth=5)
if proof:
    print("\nAudit trail for {}:".format(proof.conclusion))
    for p in proof.premises:
        print("  - {}".format(p))
```

</Tab>

</Tabs>

## 常见陷阱

**过度使用推理。** 并非每个查询都需要推理。如果简单检索或图遍历就能回答问题，推理只会徒增复杂度。只有需要推导未明确表述的事实时才用推理。

**图谱质量差。** 推理会放大数据质量问题。如果图谱中实体名称不一致、关系缺失或事实有误，推理会把这些错误扩散出去。应用推理规则之前，先清洗图数据。

**把推断事实当成已验证事实。** 推理结论的可靠性取决于它所依据的规则和事实。像 "HighRiskActor(APT29)" 这样的推断事实反映的是你的规则逻辑，而不是真实情况。观察到的事实和推断出的结论，始终要区分开来。

**规则过度复杂。** 条件繁多的复杂规则难以调试和维护。从简单规则起步，逐步增加复杂度。一条带 10 个条件的规则，多半应该拆成更小、更聚焦的规则。

**在大数据集上递归推理。** 递归 Datalog 规则在大图上可能生成指数级的派生事实。监控工作内存大小，并加上深度限制或终止条件，防止推理失控。

## 延伸阅读

- [语义抽取](./semantic-extraction.md) — 抽取实体和关系，填充你推理所依据的图事实
- [GraphRAG](./graphrag.md) — 为 LLM 的回答检索图谱锚定的上下文
- [本体管理](./ontology.md) — 生成网络本体语言(OWL)本体，给规则以形式化语义
- [决策智能](./decision-intelligence.md) — 沿完整因果链记录并追踪推导出的决策
- [上下文图](./context-graphs.md) — 推理所作用的那个知识图谱
- [MCP 服务器](./mcp-server.md) — 把 `run_reasoning` 作为工具暴露给 Claude 等智能体
