---
title: semantica.evals 运行器目标层——设计文档
description: semantica.evals 运行器逐指标目标层的设计规范，覆盖配置面、评估语义、歧义规则、聚合行为与兼容性
source: superpowers/specs/2026-08-19-evals-objective-design.md
source_version: b2cd7e2f1fe176bc9460ffd3eb94b0cb1bc6b326
---

# 设计：`semantica.evals` 运行器的目标层(Objective Layer)

**日期：** 2026-08-19
**议题：** semantica-agi/semantica#1091（分配给 pkupt）
**基线：** PR #1090（`semantica.evals` 模块）

## 1. 问题

`semantica.evals` 运行具名评估器(evaluator)并聚合每个用例(case)的通过/失败结果，但通过与否的判断硬编码在每个评估器内部——分数越高总是意味着"更好"。因此，无法在运行(run)层面表达评估目标(objective)：

- 施加评估器本身不编码的阈值(threshold)（例如「F1 必须达到 ≥ 0.7」）；
- 反转方向(direction)（例如「编辑距离越低越好」）；
- 表达布尔期望(Boolean expectation)（例如「该指标(metric)应当为 `false`」）。

这阻碍了 `docs/community-projects.md` 所称 `semantica.evals` 支持的领域专用基准测试框架(benchmark harness)。Palantir AIP Evals 正是这样建模的：每个指标都有一个**目标**（布尔期望值，或带可选阈值的数值型 `maximize`/`minimize` 方向），并且只有当**全部**指标都满足各自目标时，测试用例才算通过。

## 2. 范围

在范围内：

- 由 `evaluate()` 运行器(runner)消费的逐指标目标配置。
- 针对数值分数与布尔指标的运行器级通过/失败重新判定。
- 未配置目标时的向后兼容(backward-compatible)行为。
- 测试与文档。

不在范围内：

- 改动评估器签名或 `EvalMetric` 结构。
- 多轮迭代测试用例（AIP Evals 支持多轮；Semantica 的运行器每个用例只运行一轮）。
- 超出用例级 `pass`/`fail` 的目标感知聚合（既有 `pass_rate` 语义保持不变）。

## 3. 设计

### 3.1 配置面

目标按评估器逐一配置在运行器的 `config` 中，挂在评估器名称之下：

```python
config = {
    "<evaluator_name>": {
        "objective": {
            "direction": "maximize" | "minimize",
            "threshold": <float>,   # optional
        }
    }
}
```

布尔形式的目标（简写）：当指标的分数是布尔型（0.0/1.0），或为了语义更清晰时，也支持 `{"objective": {"expect": true}}` / `{"objective": {"expect": false}}`。

### 3.2 评估语义

对于用例运行期间评估器产出的每个指标，如果该评估器名称存在对应目标，运行器就会重新计算该指标的通过判定：

- **maximize**：当且仅当 `score >= threshold` 时通过。若未给出 `threshold`，则视同未配置目标（以评估器自身的判定为准）——见 3.4 规则 2。
- **minimize**：当且仅当 `score <= threshold` 时通过（必须有 threshold，见 3.4 规则 1）。
- **expect**：当且仅当 `bool(score)` 等于 `expect` 时通过（适用于布尔型指标）。

存在目标时，运行器会用目标判定**覆盖** `metric.passed`；不存在时，`metric.passed` 原样使用（既有行为）。

`objective` 键是**运行器级保留键**：运行器既会消费它，也会把它随 `eval_config` 透传给评估器函数（评估器本来就通过 `cfg.get(...)` 忽略未知配置键，因此这样传并无危害）；评估器不得依赖它。运行器的重新判定发生在评估器返回的指标上，所以不需要改动任何评估器。

### 3.3 与错误的交互

`meta` 含 `"error"` 的 `EvalMetric` 无论有无目标，都保持归类为错误（按既有契约，错误优先于失败）。目标只影响非错误指标。

### 3.4 歧义规则（明确决策）

1. **`minimize` 缺少 `threshold`**：在配置校验阶段即被拒绝，并给出明确错误（`ValueError`），因为"越低越好"在缺少阈值时没有绝对的通过线。（AIP Evals 允许只给方向；我们要求必须给阈值，以保证通过/失败定义明确。）——*为确定性而做的选择；若有场景要求只给方向的 minimize，再行重议。*
2. **`maximize` 缺少 `threshold`**：表现得如同未配置目标（当且仅当评估器自身的 `passed` 为真时通过），因为评估器的默认语义本来就是"越高越好"。
3. **`expect` 与数值型 `direction`/`threshold` 同时出现**：属于配置错误（`ValueError`），两种形式二选一。
4. **目标作用于出错的指标** → 错误优先（见 3.3），目标被忽略。

### 3.5 聚合

保持不变：

- 用例 `status`：任一指标出错则为 `"error"`；否则任一指标失败则为 `"fail"`；否则为 `"pass"`。
- `pass_rate` = 通过数 / 总数（空集时为 1.0）。
- `metrics` 字典保存（可能已被重新判定的）`EvalMetric`；重新判定的结果可通过 `metric.passed` 观察。
- 只有当指标在目标重新判定**之后**最终失败时，才写入 `details[name]`（即因目标而失败的指标会出现在 `details` 中；在目标下通过的指标不会记录在内）。这沿用了既有的"把失败记录进 details"行为，只是将其作用于最终判定。

### 3.6 文件

- `semantica/evals/runner.py` — 添加目标解析/校验，并在评估器循环内做重新判定。
- `tests/evals/test_runner.py` — 新增针对目标语义的测试类。
- `semantica/evals/usage.md` — 记录目标配置与示例。
- `CHANGELOG.md` — `[Unreleased]` 条目。

无新增依赖；Python ≥ 3.8（标准库 `typing`）。

## 4. 错误处理

- 非法的目标配置（`direction` 不在 {maximize, minimize} 中、`expect` 与 `direction` 同时出现、`minimize` 缺少 threshold、threshold 非数值）→ 在运行器解析配置时抛出 `ValueError`，早于任何评估器运行。行为确定，快速失败(fail-fast)。
- 这些属于程序员错误，而非用例级数据错误——不涉及任何用例级 `error` 状态。

## 5. 测试

在 `tests/evals/test_runner.py` 中新增测试：

1. maximize + threshold：score ≥ threshold → 通过；低于 → 失败。
2. minimize + threshold：score ≤ threshold → 通过；高于 → 失败（例如对相近文本对运行 levenshtein）。
3. minimize 缺少 threshold → `ValueError`。
4. 布尔指标（exact_match）上的 expect=true / expect=false——按期望通过/失败。
5. 无目标 → 既有行为不变（以评估器自身判定为准）。
6. 目标 + 错误指标 → 错误优先（status=error，而非 fail）。
7. 配置错误（非法 direction）→ 由 `evaluate()` 抛出 `ValueError`。
8. 目标把原本通过的指标判为失败 → `details` 记录该指标；用例状态变为 fail。
9. 向后兼容：62 个既有测试全部保持通过。

## 6. 兼容性

- 公开 API（`evaluate`、`list_evaluators`、`get_evaluator`、类型定义）签名不变。
- `EvalMetric` 结构不变（score, passed, meta）——只有 `passed` 可能被运行器重新计算。
- 既有配置（不含 `objective` 键）行为完全一致。
