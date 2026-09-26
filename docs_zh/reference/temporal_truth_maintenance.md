---
title: "时态真值维护(Temporal Truth Maintenance)"
description: "在相互独立的有效时间与已知时间图切片上维护派生事实。"
source: reference/temporal_truth_maintenance.md
source_version: fc9edbb07b7435da212428345f7d6a4c884e20a0
icon: "clock"
---

`TemporalTruthMaintenanceAdapter` 把显式标注的时态图(Temporal Graph)关系接入[真值维护(Truth Maintenance)会话](./truth_maintenance.md)。一句话点破：它给真值维护装上了两个独立的时间坐标——"事实何时在现实中成立"和"我们何时知道它"，换一组坐标，就按那组证据重算该相信什么。它把所选证据的变化转换成一批来源断言与撤回；只要结论仍有另一条激活支持，结论就保留下来。

两个查询坐标相互独立：

- **`valid_at`**：断言在现实世界中适用的时间。
- **`known_at`**：证据被记录、且尚未被后续版本取代的时间。

这样一来，"我们当时相信什么？"和"现在如何看待当时？"可以有不同答案。它不改变 `TemporalGraphQuery` 及其现有 `time_axis="both"` 的行为——那是在同一时间戳上同时检查两条轴。

## 示例：一次迟到的更正与过期

这个示例不需要数据库、嵌入模型或大语言模型(LLM)：

```python
from copy import deepcopy

from semantica.reasoning import Rule, TemporalTruthMaintenanceAdapter

adapter = TemporalTruthMaintenanceAdapter(rules=[
    Rule("eligibility", "Eligibility", ["Employed(?x)"], "Eligible(?x)"),
])
original = {
    "source": "alice",
    "target": "acme",
    "type": "EMPLOYED_BY",
    "valid_from": "2026-09-01T00:00:00Z",
    "valid_until": "2026-09-30T00:00:00Z",
    "recorded_at": "2026-09-01T00:00:00Z",
    "metadata": {
        "truth_maintenance": {
            "support_id": "hr-v1:employment",
            "fact": "Employed(Alice)",
        },
    },
}
graph = {
    "entities": [{"id": "alice"}, {"id": "acme"}],
    "relationships": [original],
}
adapter.sync(graph, valid_at="2026-09-15", known_at="2026-09-15")
assert "Eligible(Alice)" in adapter.facts

# On September 20, we learn employment actually ended on September 10.
# Keep the old claim and close its transaction interval, not its valid interval.
corrected_graph = deepcopy(graph)
corrected_graph["relationships"][0]["superseded_at"] = "2026-09-20"
revision = deepcopy(original)
revision["valid_until"] = "2026-09-10"
revision["recorded_at"] = "2026-09-20"
revision["metadata"]["truth_maintenance"]["support_id"] = "hr-v2:employment"
corrected_graph["relationships"].append(revision)

delta = adapter.sync(
    corrected_graph, valid_at="2026-09-15", known_at="2026-09-20",
)
assert delta.removed_facts == frozenset({"Employed(Alice)", "Eligible(Alice)"})

then = adapter.query_at(valid_at="2026-09-15", known_at="2026-09-15")
with_correction = adapter.query_at(valid_at="2026-09-15", known_at="2026-09-20")
assert "Eligible(Alice)" in then.facts
assert not with_correction.facts
assert then.explain("Employed(Alice)").explicit_support_ids == ("hr-v1:employment",)
assert not adapter.facts  # Historical queries did not move the live state.

# Explicitly move through the corrected valid-time boundary.
adapter.advance(valid_at="2026-09-09", known_at="2026-09-20")
assert "Eligible(Alice)" in adapter.facts
expired = adapter.advance(valid_at="2026-09-10", known_at="2026-09-20")
assert "Eligible(Alice)" in expired.removed_facts
assert graph["relationships"][0]["valid_until"] == "2026-09-30T00:00:00Z"
```

## 图输入与历史

传入一个包含 `entities` 和 `relationships` 的字典；已有 `ContextGraph` 的调用方可以先导出 `to_kg_dict()`，再把结果原样传入。调用方必须自行提供并保留完整的托管证据历史，包括已被取代的关系版本。只导出活跃视图，是无法还原它未曾包含的证据的。

使用 `ContextGraph` 时，标注和时间边界就是普通的关键字参数：`graph.add_edge(source, target, relation_type, valid_from=..., valid_until=..., recorded_at=..., truth_maintenance={"support_id": ..., "fact": ...})`。多余的关键字参数会存进边的元数据，因此不要把它们再包进一个显式的 `metadata=` 字典。

每条托管关系都有一个 `metadata.truth_maintenance` 字典，恰好只含 `support_id` 和 `fact` 两个键。事实串使用 PR1 的规范原子语法；关系标签不会被自动翻译成规则谓词。一个支持 ID 标识**一个来源断言修订版**。同一文档中的不同事实要用不同的 ID，后续修订也要换新 ID。未标注的关系会被忽略；格式非法的标注抛 `ValidationError`。

时态字段从每条记录本身读取；如果存在，也从它的 `metadata` 和 `properties` 字典读取。第二个位置很重要，因为 `ContextGraph` 把除有效时间边界之外的一切都放在 `metadata` 里（实体还会通过 `properties` 暴露这些字段），所以 `to_kg_dict()` 的输出无需改写即可使用。同一字段在多处给出时必须指同一个时刻；相互冲突的重复值抛 `TemporalValidationError`。

| 字段 | 含义 | 托管证据的默认值 |
|---|---|---|
| `valid_from` | 有效时间起点（含） | 无界过去 |
| `valid_until` | 有效时间终点（不含） | 无界未来 |
| `recorded_at` | 已知时间起点（含） | 必须显式给出 |
| `superseded_at` | 已知时间终点（不含） | 无界未来 |

关系端点从 `source`/`target` 读取，或从 `to_kg_dict()` 输出的规范形式 `source_id`/`target_id` 读取。两种形式同时给出且值不同时抛 `ValidationError`，而不是静默偏爱其中之一。

空上界、`"OPEN"` 与 `TemporalBound.OPEN` 都表示无界未来。有限区间要求 `start < end`。时间值使用现有的时态解析器：接受 ISO 字符串、datetime 与数字型 Unix 时间戳；不带时区的 naive datetime 按 UTC 处理。布尔值会被拒绝。不做天/秒级截断，也不从系统挂钟取任何默认值。

已保留的记录不能从后续的 `sync()` 中消失。它们的事实、端点、关系类型、有效区间和记录时间都不可改写。开放的 `superseded_at` 只能闭合一次；闭合后的区间不能再打开或更改。更正的做法是关闭旧修订、追加新修订。要把某个来源从当前已知时间视图中撤回，就关闭它的事务区间，并把 `known_at` 前移到该边界或更晚。物理删除一行会被拒绝。

适配器把调用方提供的显式事务历史当作权威；它不推断到达时间，不裁决冲突证据，也不会自动指派替代关系。

实体 ID 必须是唯一的字符串。如果图中包含实体，每条托管边都必须有已存在的端点，且两个端点在两个查询坐标上都活跃。没有时态字段的实体脚手架（仅为承载边而存在的实体）与时间无关；其保留的时间字段遵循同样的不可变/事务闭合规则。只含关系的图也受支持，但同一适配器不能事后追加端点约束：那会重新解释已保留的历史。要切换这种模式，请新建一个适配器。谓词元数的检查覆盖全部保留证据，包括在所请求坐标上不活跃的记录。

## API

### `TemporalTruthMaintenanceAdapter(rules=...)`

适配器内部新建并持有一个会话，规则是复制后固定的 PR1 规则。不接受外部可变会话。PR1 规则的全部限制照常适用，包括非递归与无副作用。访问必须由调用方串行化。

### `sync(graph, *, valid_at, known_at) -> MaintenanceDelta`

校验并摄取保留证据投影。把其中选中的支持 ID 与当前激活的支持 ID 求差异，然后应用一个 PR1 批次。同一事实的来源替换只带来支持层面的变化，事实集合不会经历中间状态的反复增删。

校验或推理失败时，保留证据、当前事实、时钟和计数器全部原样不动。输入字典不会被修改，也不会按引用保留。非时态属性与无关元数据不属于托管投影。

### `advance(*, valid_at, known_at) -> MaintenanceDelta`

选择保留证据的另一个切片。调用方就是这样在不修改图的情况下触发过期或激活。向前和向后移动都允许。这里没有定时器：光靠等待不会更新当前事实。

### `query_at(*, valid_at, known_at) -> TemporalFactSnapshot`

为所请求的切片新建一个全新会话，返回该切片的事实、激活来源支持与直接解释。这个冻结结果只含不可变值；它提供 `explain(fact)`，且不会被后续更新改动。它携带 `valid_at`、`known_at` 与 `graph_revision`。它不会改动当前会话，也不会假装一次历史重算拥有实时的提交版本号。

### 当前属性与解释

- `facts`：当前显式事实与派生事实的不可变集合。
- `explain(fact)`：当前 PR1 的直接来源与推导。
- `version`：PR1 的已提交支持集计数器。只移动时钟的变化不必使它递增。
- `graph_revision`：规范化保留投影发生变化的计数器，含不活跃证据的变化。它是本适配器内部的计数，不是全局图 ID。
- `valid_at`、`known_at`：当前 UTC 坐标，初始为 `None`。

构造缓存标识时，要区分适配器实例、保留图修订号与两个时间坐标；不要只用当前支持版本号。

## 成本与边界

每次图同步都要对提供的托管历史做规范化/校验。切片选择会扫描保留证据与端点生命周期。PR1 执行它既有的更新工作与状态暂存；历史查询则要重新计算一份全新闭包，并捕获全部直接解释。保留历史随证据修订不断增长。本实现不提供存储侧的索引化时态查询，也不承诺亚线性更新成本。

适配器不持久化自己的档案，不把结论写回图，不调度过期任务，不修改 RETE，不支持递归规则，也不更新 RAG 提示词与向量记录。一致性只相对于所提供的证据和固定规则而言；失去支持意味着"当前不可推导"，而不是"为假"。
