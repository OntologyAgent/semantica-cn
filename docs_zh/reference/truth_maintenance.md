---
title: "真值维护(Truth Maintenance)"
description: "针对固定非递归规则的、感知来源的逻辑撤回。"
source: reference/truth_maintenance.md
source_version: f7b0cb484b6a7e35454b6564357c3ad7cbedf27f
icon: "microchip"
---

`TruthMaintenanceSession` 是 Semantica 对真值维护(Truth Maintenance)的实现：让派生事实与不断变化的外部证据保持同步。你可以把它理解成一套自动回收机制——证据一变，结论就跟着重算，撤回一条证据时只回收真正失去依据的结论。它维护的不变式是：

```text
session.facts == closure(fixed_rules, facts_with_remaining_external_support)
```

撤回一个来源后，失去前提的结论随之失效；仍有其他推导或显式支持的结论则保留下来。

这是一个**可选启用**的会话：现有 `Reasoner`、action、RETE 和 Datalog 的行为完全不受影响。


## 何时使用

以下情况适合用 `TruthMaintenanceSession`：

- 事实来自**可能更正或撤回**的外部证据（比如文档修订后，一条断言换成了另一条）。
- 你需要派生结论**只在失去全部支持时**才移除，而不是一有删除就动。
- 你希望批量更新只发布最终状态和**净变化**，而不是重放中间状态。
- 你碰到了 `RetractAction` 的局限：它只移除请求的那条事实，把失去支持的结论留在原地；而朴素的级联删除又会误删那些仍有其他推导或显式支持的结论。

递归规则、时态有效性、外部副作用、多线程访问都不适用——见[局限性](#局限性)。


## 快速开始

```python
from semantica.reasoning import FactSupport, Rule, TruthMaintenanceSession

rules = [
    Rule(
        rule_id="employment-eligibility",
        name="Employment eligibility",
        conditions=["Employed(?x)"],
        conclusion="Eligible(?x)",
    ),
]
session = TruthMaintenanceSession(rules=rules)

session.apply(assertions=[
    FactSupport(support_id="document-v1", fact="Employed(Alice)"),
])

delta = session.apply(
    assertions=[FactSupport("document-v2", "Employed(Alice)")],
    retractions=["document-v1"],
)
assert not delta.added_facts
assert not delta.removed_facts
assert session.explain("Eligible(Alice)").active

delta = session.apply(retractions=["document-v2"])
assert delta.removed_facts == frozenset({
    "Employed(Alice)", "Eligible(Alice)",
})
```

上面的例子演示的是**来源替换**：在同一个批次里把一份支撑文档换成另一份，事实层面没有净增删——因为 `Employed(Alice)` 仍有支持，`Eligible(Alice)` 的推导也依然成立。


## 核心概念

- **支持**：一条外部事实断言，用调用方提供的 `support_id` 标识。一个支持 ID 在会话生命周期内永久绑定到一条事实；允许先撤回、之后重新激活同一绑定，但把同一个 ID 绑到另一条事实会抛 `ValidationError`。
- **推导**：一次规则应用，包含规则身份、有序前提、变量绑定和结论。同一结论的多条独立推导全部保留；重复匹配不会虚增支持。
- **版本**：单调递增的提交计数器。凡是改变了支持集的批次，版本加一（即使事实集没变）；无操作则保持不变。
- **真值语义**：失去全部支持意味着"当前不可推导"，而不是"逻辑上为假"。


## 会话 API

### `TruthMaintenanceSession(rules=...)`

用一组现有的 [`Rule`](./reasoning.md#rule-与-fact-的-dataclass-字段) 对象构造会话。规则会被复制成不可变的内部快照：之后修改原始 `Rule` 对象不影响会话。

规则集必须满足：

- **正向、无函数符号的蕴含**，且至少含一个体原子。
- **值域受限**：头部的每个变量都出现在体中。
- **无环**：谓词依赖图不得含有直接或间接递归；构造阶段就会拒绝带环的规则集。
- **无副作用**：action、handler 和非蕴含类规则一律拒绝；`confidence` 必须为 `1.0`。

### `apply(assertions=..., retractions=...)`

原子化地应用一个批次：

- `assertions`：`FactSupport` 的可迭代对象。
- `retractions`：支持 ID 字符串的可迭代对象。

返回一个 `MaintenanceDelta`，含 `version`、`added_facts`、`removed_facts`、`added_supports` 和 `removed_supports`（均为净变化，在提交后观测）。

校验与错误语义：

- 对已激活的支持重复断言同一事实是无操作；撤回未知或未激活的支持也是无操作。
- 支持 ID 绑到不同的事实、同一批次中同一个 ID 同时出现在断言与撤回里、以及其他任何格式非法的输入，都会抛现有的 `ValidationError`。
- 未预期的内部故障会抛 `ProcessingError`，并附带原始原因。
- **任何失败的批次都不改动已提交的事实、支持目录、推导和版本。**

### `explain(fact)`

返回当前状态的 `FactExplanation`：

- `fact`：规范化的事实字符串。
- `active`：该事实当前是否成立。
- `explicit_support_ids`：外部支持的 ID 列表（已排序）。
- `derivations`：全部保留的直接推导（规则 ID、有序前提、绑定）。

### 只读视图

- `facts`：当前相信的全部事实组成的 frozenset（显式事实加派生事实）。
- `version`：前文提到的提交计数器。
- `snapshot()`：返回 `TruthMaintenanceSnapshot`——一个 frozen dataclass，含 `version`、`facts` 和 `active_supports`（按支持 ID 排序的元组）。快照是完全独立的副本：后续的 `apply()` 批次绝不会改动已有快照。

所有只读视图（`facts`、`version`、`snapshot()`、`explain()`）都不改动会话状态。返回的快照对象（`MaintenanceDelta`、`FactExplanation`、`Derivation`、`TruthMaintenanceSnapshot`）都是带不可变集合的 frozen dataclass；修改调用方自有的规则或先前返回的结果，也动不了会话。


## 成本模型

- **删除传播**与**受影响规则匹配**都是定向的：纯删除批次先用依赖索引算出受影响的事实集，再只重新匹配体谓词与该集合相交的规则（受影响性扫描本身要遍历规则列表，因此成本仍随规则数量增长）；插入则只重新评估从新激活谓词可达的规则。
- 为了保证原子提交，每个*生效的* `apply()` 批次都要**暂存整份会话状态**（空批次或已应用过的批次是无操作，不做暂存）；会话还会在整个生命周期内把**支持目录保留在内存里**（包括已撤回的支持，因此 ID 始终保持绑定）。
- **每次 `snapshot()` 调用都会再复制一份完整的已提交状态**（事实、激活支持、版本），因此 [`TruthMaintenanceContextFilter`](./context.md) 这类消费者每次过滤检索都要付一次全状态复制的代价。一次共享读取就够用时，别在紧循环里反复调用。
- 更新时复制与支持目录的开销都是按批次计的全状态开销；别假设端到端延迟严格正比于受影响的子图。依赖性能之前，先实测。


## 局限性

- **仅支持非递归规则**；构造函数会拒绝带环的谓词依赖。
- **原子语法很窄**：只接受 ASCII 谓词/变量标识符和不带引号的标量符号常量，包括零元原子。不支持带引号的字符串、含空白的常量、嵌套项、比较、聚合、否定或析取。会话内每个谓词只能有一种元数。
- **布尔支持语义**；不支持置信度传播，也不支持概率推理。
- **无副作用**：会话从不执行 action 或 handler，也不创建大语言模型(LLM)或存储客户端。
- **不保证线程安全、持久化、时态有效性或跨存储同步**。访问必须由调用方在单进程内串行化。
- **规则固定**：要改规则就得新建会话。
- 没有历史证明档案：`explain()` 只描述当前状态。


## 相关链接

- [Reasoning](./reasoning.md) — 本会话赖以构建的规则引擎，包括 `Rule` 的表示。
- [Context](./context.md) — `TruthMaintenanceContextFilter` 消费不可变快照，按激活支持过滤检索到的上下文。
- [Ontology](./ontology.md) — 本体公理与 SHACL 约束。
