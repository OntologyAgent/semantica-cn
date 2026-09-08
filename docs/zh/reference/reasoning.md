---
title: "推理模块（Reasoning）"
description: "前向链接、Rete、演绎、溯因、SPARQL、Datalog 与时态推理，附可解释的推理路径。"
source: reference/reasoning.md
source_version: 7c539d72c462ea974937c6dc632a9e22b692ac66
icon: "microchip"
---

`semantica.reasoning` 用逻辑规则从既有事实推导新知识：

- 六种推理引擎：前向链接、Rete、SPARQL、Datalog、时态、LLM 驱动的 GraphReasoner
- 每个引擎都产出可解释的推理路径：规则与事实构成的可追溯链条
- `DatalogReasoner` 经半朴素(semi-naive)不动点求值保证终止
- `TemporalReasoningEngine` 实现全部 13 种 Allen 区间代数关系
- `ExplanationGenerator` 生成逐步的自然语言论证


## 导出的类

| 类 | 职责 |
| :--- | :--- |
| `Reasoner` | 前向链接推理：`add_fact`、`add_rule`、`forward_chain`、`backward_chain`、`infer_facts` |
| `GraphReasoner` | 对 KG dict 做 LLM 驱动推理：经 `reason(graph, query)` 回答自然语言查询 |
| `ReteEngine` | Rete 模式匹配：`build_network`、`add_fact`、`match_patterns`、`execute_matches` |
| `SPARQLReasoner` | 基于规则的 SPARQL 查询扩展：`execute_query`、`expand_query`、`infer_results` |
| `DatalogReasoner` | 递归 Horn 子句规则 + 半朴素不动点：`add_fact`、`add_rule`、`derive_all`、`query` |
| `TemporalReasoningEngine` | 全部 13 种 Allen 区间代数关系：`relation(a, b)`、`overlaps`、`contains`、`active_at` |
| `ExplanationGenerator` | 逐步解释：`generate_explanation(inference_result)` |
| `Rule` | IF/THEN 规则：`{rule_id, name, conditions, conclusion, rule_type, confidence, priority}` |
| `Fact` | 工作记忆事实：`{fact_id, predicate, arguments}` |
| `InferenceResult` | 单条推导结论：`{conclusion, rule_used, premises, confidence}` |


## 该用哪个引擎？

- [Reasoner](#reasoner-forwardbackward-chaining) — IF/THEN 规则，前向与后向链接。**从这里开始**：覆盖 90% 的使用场景，无需查询语言。
- [GraphReasoner](#graphreasoner) — 经 LLM 对知识图谱做自然语言查询。不用 SPARQL 也不用规则：直接提问即可。
- [DatalogReasoner](#datalogreasoner) — 保证终止的递归 Horn 子句规则。复杂的多跳传递规则用它。
- [ReteEngine](#reteengine) — 高频推理用 Rete 模式匹配。要把大量事实同时匹配大量规则时用它。
- [SPARQLReasoner](#sparqlreasoner) — SPARQL 查询扩展与基于规则的推理。处理 RDF/OWL 数据时用它。
- [TemporalReasoningEngine](#temporalreasoningengine) — 全部 13 种 Allen 区间代数关系。时间感知推理用它：重叠、先后、包含等。


## 快速开始

最常见的模式是用 `Reasoner` 做 IF/THEN 前向链接：

```python
from semantica.reasoning import Reasoner, Rule, RuleType

reasoner = Reasoner()

# Add facts as strings in predicate(args) form
reasoner.add_fact("Manager(Alice)")
reasoner.add_fact("Employee(Alice)")

# Add an IF-THEN rule using the string form
reasoner.add_rule("IF Manager(?x) THEN HasAuthority(?x)")

# Run forward chaining: returns List[InferenceResult]
results = reasoner.forward_chain()
for r in results:
    print(r.conclusion)         # "HasAuthority(Alice)"
    print(r.confidence)         # 1.0
    if r.rule_used:
        print(r.rule_used.name) # name of the rule applied
```

也可以用 `Rule` dataclass 以编程方式构建规则：

```python
from semantica.reasoning import Rule, RuleType

rule = Rule(
    rule_id="rule_001",
    name="manager_authority",
    conditions=["Manager(?x)"],
    conclusion="HasAuthority(?x)",
    rule_type=RuleType.IMPLICATION,
    confidence=0.9,
)
reasoner.add_rule(rule)
```


## Reasoner（前向/后向链接）

**`Reasoner`** 是基于规则推理的统一入口：迭代事实与规则直至**不动点**，再按需经后向链接证明特定目标：

```python
from semantica.reasoning import Reasoner, Rule, RuleType, InferenceResult

reasoner = Reasoner()

# Facts can be strings, KG entity dicts, or KG relationship dicts
reasoner.add_fact("Manager(John)")
reasoner.add_fact("Employee(John)")

# IF-THEN string form
reasoner.add_rule("IF Manager(?x) AND Employee(?x) THEN SeniorStaff(?x)")

# Forward chaining: iterates until fixpoint
results = reasoner.forward_chain()
for r in results:
    print(r.conclusion)   # e.g. "SeniorStaff(John)"
    print(r.premises)     # list of premise strings matched
    print(r.confidence)   # float

# Backward chaining: prove a specific goal
result = reasoner.backward_chain("SeniorStaff(John)", max_depth=10)
if result:
    print(f"Proven: {result.conclusion}")
    print(f"Premises: {result.premises}")

# infer_facts() loads facts and rules in one call, returns conclusion strings
conclusions = reasoner.infer_facts(
    facts=["Manager(Alice)", "Employee(Alice)"],
    rules=["IF Manager(?x) THEN HasAuthority(?x)"],
)
# → ["HasAuthority(Alice)"]
```

### Reasoner 方法

| 方法 | 返回 | 说明 |
| :------ | :------- | :----------- |
| `add_fact(fact)` | `None` | 向工作记忆添加字符串、实体 dict 或关系 dict |
| `add_rule(rule)` | `Rule` | 添加 `Rule` 对象或 IF-THEN 字符串；规则按 `priority` 降序排序 |
| `forward_chain()` | `List[InferenceResult]` | 迭代推导所有可能的结论，直至不动点 |
| `backward_chain(goal, max_depth)` | `InferenceResult \| None` | 证明特定目标字符串，证不出则返回 `None` |
| `infer_facts(facts, rules)` | `List[str]` | 装载事实与规则后运行 `forward_chain()`，返回结论字符串列表 |
| `reset_action_history()` | `None` | 允许此前已触发的激活重新执行动作 |
| `clear()` | `None` | 清空全部事实、规则和动作激活历史 |
| `reset()` | `None` | `clear()` 的别名 |

带动作的规则对每个具体激活（规则 ID、绑定与匹配的事实）采用**至多一次尝试**语义。对同一实例再次调用 `forward_chain()`，不会为已尝试过的激活重复副作用——即便该动作曾抛出异常。要刻意重试且不清空事实与规则时，调用 `reset_action_history()`；`clear()` 和 `reset()` 也会清掉这段历史。就地替换某条规则的动作不会使已有激活失效；若希望替换后的动作重放，须显式重置历史。

### Rule 与 Fact 的 dataclass 字段

```python
from semantica.reasoning import Rule, Fact, RuleType

# Rule: all fields
rule = Rule(
    rule_id="rule_001",            # required: unique identifier
    name="manager_authority",      # required: display name
    conditions=["Manager(?x)"],    # list of condition strings
    conclusion="HasAuthority(?x)", # conclusion string
    rule_type=RuleType.IMPLICATION, # IMPLICATION | EQUIVALENCE | CONSTRAINT | TRANSFORMATION
    confidence=1.0,                 # default 1.0
    priority=0,                     # higher priority rules run first
)

# Fact: for working with the Rete engine directly
from semantica.reasoning import Fact
fact = Fact(
    fact_id="f001",                # required: unique identifier
    predicate="Manager",
    arguments=["John"],
    metadata={},
)
```


## GraphReasoner

**`GraphReasoner`** 用 LLM 回答对知识图谱 dict 的**自然语言查询**：无需编写 SPARQL 或规则：

```python
from semantica.reasoning import GraphReasoner

# Initialize: uses openai by default; override via kwargs
reasoner = GraphReasoner(provider="openai", model="gpt-4o-mini")

kg = {
    "entities": [
        {"id": "alice",   "name": "Alice",   "type": "Person",       "properties": {"role": "CEO"}},
        {"id": "acme",    "name": "Acme Inc", "type": "Organization"},
    ],
    "relationships": [
        {"source": "alice", "target": "acme", "type": "leads"}
    ],
}

answer: str = reasoner.reason(
    graph=kg,
    query="Who leads Acme Inc. and what is their role?"
)
print(answer)
```

`reason()` 把图转成文本上下文，用结构化提示调用 LLM，返回纯字符串答案。


## ReteEngine

面向大型规则集的高性能 Rete 模式匹配：

```python
from semantica.reasoning import ReteEngine, Rule, Fact, RuleType

engine = ReteEngine()

# Build the Rete network from a list of Rule objects
rules = [
    Rule(
        rule_id="r1",
        name="manager_authority",
        conditions=["Manager(?x)"],
        conclusion="HasAuthority(?x)",
    )
]
engine.build_network(rules)

# Add facts to working memory
engine.add_fact(Fact(fact_id="f1", predicate="Manager", arguments=["Alice"]))

# Match patterns and execute
matches = engine.match_patterns()
results = engine.execute_matches(matches)
# results is a list of conclusion values from matched rules

# Network statistics
stats = engine.get_network_stats()
# → {"total_nodes": N, "alpha_nodes": A, "beta_nodes": B, "terminal_nodes": T, "facts": F}

engine.reset()
```

### ReteEngine 方法

| 方法 | 返回 | 说明 |
| :------ | :------- | :----------- |
| `build_network(rules)` | `None` | 从 `Rule` 对象列表构建 Rete 网络 |
| `add_fact(fact)` | `None` | 向工作记忆添加 `Fact` 并在网络中传播 |
| `match_patterns(facts)` | `List[Match]` | 匹配全部模式；可选先添加事实再匹配 |
| `execute_matches(matches)` | `List[Any]` | 执行命中的规则，返回其结论值 |
| `reset_action_history()` | `None` | 允许此前已执行的激活重新运行动作 |
| `reset()` | `None` | 清空事实、节点激活状态和动作激活历史 |
| `get_network_stats()` | `dict` | 返回 alpha、beta、终端节点和事实的计数 |

绑定了 Reasoner 时，`execute_matches()` 会按规则 ID、绑定与匹配事实的标识对动作副作用去重。重复执行同一匹配仍会为兼容而返回其结论，但其动作在首次尝试后即被跳过。`reset_action_history()`、`reset()` 和 `build_network()` 会让这些动作再次运行。


## SPARQLReasoner

**`SPARQLReasoner`** 用**推理规则扩展**增强 SPARQL：添加 IF-THEN 规则后，执行前会自动织入查询：

```python
from semantica.reasoning import SPARQLReasoner

reasoner = SPARQLReasoner()

# Add an inference rule (IF-THEN string form)
reasoner.add_inference_rule("IF is_a(?x, Manager) THEN has_authority(?x)")

# Execute a query: returns SPARQLQueryResult
result = reasoner.execute_query("""
    PREFIX ex: <http://example.org/>
    SELECT ?person ?company WHERE {
        ?person ex:founded ?company .
        ?company ex:located_in ex:SiliconValley .
    }
""")

for row in result.bindings:
    print(row)   # each row is a dict of variable → {"value": ..., "type": ...}

# Expand a query with inference rules (returns modified query string)
expanded = reasoner.expand_query("SELECT ?x WHERE { ?x a :Manager }")

# Infer additional bindings from existing results
enriched = reasoner.infer_results(result)
```

### SPARQLReasoner 构造参数

```python
SPARQLReasoner(
    config=None,         # optional config dict
    triplet_store=None,  # optional TripletStore instance for live query execution
    enable_inference=True,
)
```

<Note>
  未配置 `triplet_store` 时，`execute_query()` 返回空的 bindings。要对着真实后端执行查询，须经 `triplet_store=` 关键字参数传入 `TripletStore` 实例。
</Note>


## DatalogReasoner

纯 Python 的自底向上半朴素不动点求值，支持递归 Horn 子句规则。终止**有保证**：引擎检测到不动点收敛即停止：

```python
from semantica.reasoning import DatalogReasoner, DatalogFact

datalog = DatalogReasoner()

# Add base facts: string form is the simplest
datalog.add_fact("parent(alice, bob)")
datalog.add_fact("parent(bob, charlie)")

# Or use DatalogFact directly (args is a tuple of strings)
datalog.add_fact(DatalogFact(predicate="parent", args=("charlie", "dave")))

# Add recursive rules using Horn clause syntax
datalog.add_rule("ancestor(X, Y) :- parent(X, Y).")
datalog.add_rule("ancestor(X, Z) :- parent(X, Y), ancestor(Y, Z).")

# Evaluate to fixpoint: returns all derived fact strings
all_facts = datalog.derive_all()
# e.g. ["parent(alice, bob)", "parent(bob, charlie)", ..., "ancestor(alice, bob)", ...]

# Query with variable pattern: variables start with uppercase or ?
results = datalog.query("ancestor(alice, ?Z)")
# → 一组绑定字典: [{"Z": "bob"}, {"Z": "charlie"}, {"Z": "dave"}]（顺序不保证）

# Clear and start over
datalog.clear()
```

### DatalogFact、DatalogRule 字段

```python
from semantica.reasoning import DatalogFact, DatalogRule

# DatalogFact: ground fact; args must all be constants (lowercase start)
fact = DatalogFact(predicate="parent", args=("alice", "bob"))

# DatalogRule: parsed from string; head and body are set by the parser
# Use add_rule("head(X, Y) :- body(X, Z), body2(Z, Y)."): do not construct directly
```

### DatalogReasoner 方法

| 方法 | 返回 | 说明 |
| :------ | :------- | :----------- |
| `add_fact(fact)` | `None` | 添加字符串、dict 或 `DatalogFact`；常量必须以小写开头 |
| `add_rule(rule_str)` | `None` | 解析并添加 Horn 子句字符串，如 `"ancestor(X,Y) :- parent(X,Y)."` |
| `derive_all()` | `List[str]` | 运行半朴素不动点求值，以字符串形式返回全部事实 |
| `query(pattern)` | `List[dict]` | 查询推导出的事实：必要时自动先跑 `derive_all()` |
| `load_from_graph(graph)` | `int` | 把 ContextGraph 的节点/边装载为 Datalog 事实，返回添加数量 |
| `clear()` | `None` | 清空全部事实与规则 |


## TemporalReasoningEngine

纯 Python 的 Allen 区间代数：全部 13 种关系，零 LLM 调用：

```python
from datetime import datetime
from semantica.reasoning import TemporalReasoningEngine, TemporalInterval, IntervalRelation

engine = TemporalReasoningEngine()

ceo_tenure   = TemporalInterval(start=datetime(1997, 9, 16), end=datetime(2011, 8, 24))
board_member = TemporalInterval(start=datetime(2000, 1,  1), end=datetime(2012, 6,  1))

# Compute Allen relation: method is relation(), not get_relation()
rel = engine.relation(ceo_tenure, board_member)
# → IntervalRelation.DURING  (ceo_tenure is fully inside board_member)

# Other helpers
engine.overlaps(ceo_tenure, board_member)   # bool
engine.contains(board_member, ceo_tenure)   # bool

# Is a given point in time inside an interval?
engine.active_at(ceo_tenure, datetime(2005, 6, 1))   # True
```

全部 13 种 Allen 区间代数关系：

| 关系 | 含义 |
| :-------- | :------- |
| `BEFORE` | A 结束于 B 开始之前 |
| `MEETS` | A 结束的时刻恰好是 B 开始的时刻 |
| `OVERLAPS` | A 先于 B 开始，结束在 B 之内 |
| `DURING` | A 完全位于 B 之内 |
| `STARTS` | A 与 B 同时开始，A 先结束 |
| `FINISHES` | A 与 B 同时结束，A 更晚开始 |
| `EQUALS` | 区间完全相同 |
| `AFTER` | BEFORE 的逆 |
| `MET_BY` | MEETS 的逆 |
| `OVERLAPPED_BY` | OVERLAPS 的逆 |
| `CONTAINS` | DURING 的逆 |
| `STARTED_BY` | STARTS 的逆 |
| `FINISHED_BY` | FINISHES 的逆 |

<Note>
  `TemporalInterval.start` 接受 `datetime` 对象，不是字符串。从标准库导入 `datetime`，用 `datetime(year, month, day)` 构造区间。
</Note>


## ExplanationGenerator

为任意 `InferenceResult` 生成结构化解释：

```python
from semantica.reasoning import ExplanationGenerator, Reasoner, Rule

reasoner = Reasoner()
reasoner.add_fact("Manager(John)")
reasoner.add_rule("IF Manager(?x) THEN HasAuthority(?x)")
results = reasoner.forward_chain()

# ExplanationGenerator takes no positional args
generator = ExplanationGenerator()

# Pass an InferenceResult object: not a dict
explanation = generator.generate_explanation(results[0])

print(f"Type:       {explanation.explanation_type}")   # "inference"
print(f"Conclusion: {explanation.conclusion}")
print(f"NL:         {explanation.natural_language}")

if explanation.reasoning_path:
    for step in explanation.reasoning_path.steps:
        print(f"  Step {step.step_id}: {step.description}")
        if step.rule_applied:
            print(f"    Rule: {step.rule_applied.name}")

# Justify a conclusion with a reasoning path
path = generator.show_reasoning_path(results[0])
justification = generator.justify_conclusion(results[0].conclusion, path)
print(justification.explanation_text)
```

### ExplanationGenerator 方法

| 方法 | 返回 | 说明 |
| :------ | :------- | :----------- |
| `generate_explanation(reasoning)` | `Explanation` | 为 `InferenceResult`、`Proof` 或溯因结果生成结构化解释 |
| `show_reasoning_path(reasoning)` | `ReasoningPath` | 从任意结果中提取并返回推理路径 |
| `justify_conclusion(conclusion, path)` | `Justification` | 为结论构建带证据和自然语言文本的 `Justification` |

### 关键 dataclass 字段

```python
# Explanation
explanation.explanation_id    # str
explanation.explanation_type  # "inference" | "proof" | "abductive" | "generic"
explanation.conclusion        # conclusion value
explanation.reasoning_path    # ReasoningPath | None
explanation.natural_language  # NL string (when generate_nl=True, the default)

# ReasoningStep
step.step_id        # str
step.description    # str
step.rule_applied   # Rule | None  (NOT rule_name)
step.input_facts    # List[Any]
step.output_fact    # Any
step.confidence     # float
```


## 引擎选择指南

| 引擎 | 最适合 | 终止性 | 关键方法 |
| :------ | :-------- | :----------- | :---------- |
| `Reasoner` | 简单 IF/THEN 规则 | 总是（有 `max_iterations` 上限） | `forward_chain()` |
| `GraphReasoner` | 经 LLM 对 KG 做自然语言查询 | 总是 | `reason(graph, query)` |
| `ReteEngine` | 大量事实配大型规则集 | 总是 | `match_patterns()` |
| `SPARQLReasoner` | 规则增强的 SPARQL 查询 | 总是 | `execute_query()` |
| `DatalogReasoner` | 递归规则（祖先、可达性） | 不动点保证 | `derive_all()` / `query()` |
| `TemporalReasoningEngine` | 时间区间关系 | 总是 | `relation(a, b)` |

<Tip>
  递归规则（祖先、可达性、传递性等）用 `DatalogReasoner`：半朴素自底向上不动点求值保证终止。`Reasoner.forward_chain()` 有 `max_iterations` 上限（默认 50），深层递归时会静默提前停止。
</Tip>

<Warning>
  `GraphReasoner` 需要配置好的 LLM 提供商。提供商初始化失败时，`reason()` 返回错误字符串而不是抛异常。若需要显式暴露失败，调用前先检查 `reasoner.provider is not None`。
</Warning>

- [Knowledge Graph](./kg.md) — 被推理的那张知识图谱。
- [Ontology](./ontology.md) — 逻辑推理用的本体公理与 SHACL 约束。
- [Triplet Store](./triplet_store.md) — 支撑 SPARQL 推理的 RDF 后端。
- [Context](./context.md) — 推理融入智能体决策智能。
