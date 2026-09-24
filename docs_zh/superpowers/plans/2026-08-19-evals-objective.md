---
title: semantica.evals 运行器目标层——实现计划
description: 为 evaluate() 运行器添加逐指标目标支持（方向加阈值，或布尔期望）并保持向后兼容的分任务实现计划
source: superpowers/plans/2026-08-19-evals-objective.md
source_version: 61a65dad79a0a24c50d7396c9e0b057a3383cdb9
---

# semantica.evals 运行器的目标层(Objective Layer)——实现计划

> **面向智能体工作者(agentic workers)：** 必需子技能(REQUIRED SUB-SKILL)：使用 superpowers:subagent-driven-development（推荐）或 superpowers:executing-plans 逐任务实现本计划。各步骤使用复选框(`- [ ]`)语法进行跟踪。

**目标：** 为 `evaluate()` 运行器(runner)添加逐指标目标(objective)支持（方向 + 阈值(threshold)，或布尔期望(Boolean expectation)），覆盖评估器(evaluator)的默认通过判定(pass verdict)；未配置目标时保持向后兼容(backward-compatible)。

**架构：** 运行器已经会遍历各评估器并计算每个用例(case)的状态。目标从 `config["<name>"]["objective"]` 读取，先做前置校验，然后在聚合(aggregation)之前应用到每个返回指标(metric)的 `passed` 字段（以及 `details`）。错误指标永远优先于目标。

**技术栈：** Python 3.8+，仅用标准库(stdlib)（typing、dataclasses）。测试使用 pytest。

## 全局约束

- Python >= 3.8：使用 `typing.Dict/List/Optional/Union`，禁止内建泛型或 `|`。
- 零新增依赖。
- 不得改动 `EvalMetric` 的结构、`evaluate()` 的签名或评估器函数的签名。
- 未配置 `objective` 时，现有行为必须逐字节保持不变（62 个既有测试全部继续通过）。
- 错误指标（`meta` 含 `"error"`）无论目标如何，一律把用例归类为 `error`。
- 配置错误属于程序员错误：在任何评估器运行之前，由 `evaluate()` 抛出 `ValueError`（快速失败(fail-fast)）。
- 测试放在 `tests/evals/`，采用 pytest 类风格；除列出的路径外不得新增文件。

---

### 任务 1：运行器中的目标解析、校验与重新判定

**文件：**
- 修改：`semantica/evals/runner.py`
- 测试：`tests/evals/test_runner.py`

**接口：**
- 消费：来自 `.types` 的 `EvalMetric`（字段：`score`、`passed`、`meta`）；既有的 `evaluate(cases, evaluators, config=None, target_fn=None)` 签名。
- 产出：私有辅助函数 `_parse_objective(name, eval_config) -> Optional[Dict]`（未配置目标时返回 `None`，配置非法时抛出 `ValueError`）和 `_apply_objective(metric, objective) -> bool`（返回重新判定的 `passed`）。公开的 `evaluate()` 行为按规范扩展。

- [ ] **步骤 1：编写失败的测试**

在 `tests/evals/test_runner.py` 末尾追加一个新的测试类：

```python
class TestObjective:
    def test_maximize_with_threshold_pass(self):
        # levenshtein similarity 1.0 for identical, objective demands >= 0.5
        result = evaluate(
            [("apple", "apple")],
            evaluators=["levenshtein"],
            config={"levenshtein": {"objective": {"direction": "maximize", "threshold": 0.5}}},
        )
        assert result.cases[0].status == "pass"
        assert result.cases[0].metrics["levenshtein"].passed is True

    def test_maximize_with_threshold_fail(self):
        result = evaluate(
            [("apple", "aple")],  # similarity < 1.0
            evaluators=["levenshtein"],
            config={"levenshtein": {"objective": {"direction": "maximize", "threshold": 0.99}}},
        )
        assert result.cases[0].status == "fail"
        assert result.cases[0].metrics["levenshtein"].passed is False
        assert "levenshtein" in result.cases[0].details

    def test_minimize_with_threshold_pass(self):
        # edit distance normalized ~0.2; objective: distance <= 0.5
        result = evaluate(
            [("night", "nacht")],
            evaluators=["levenshtein"],
            config={"levenshtein": {"objective": {"direction": "minimize", "threshold": 0.5}}},
        )
        assert result.cases[0].status == "pass"
        assert result.cases[0].metrics["levenshtein"].passed is True

    def test_minimize_with_threshold_fail(self):
        result = evaluate(
            [("night", "nacht")],
            evaluators=["levenshtein"],
            config={"levenshtein": {"objective": {"direction": "minimize", "threshold": 0.1}}},
        )
        assert result.cases[0].status == "fail"

    def test_expect_true_on_boolean_metric(self):
        result = evaluate(
            [("ok", "ok")],
            evaluators=["exact_match"],
            config={"exact_match": {"objective": {"expect": True}}},
        )
        assert result.cases[0].status == "pass"

    def test_expect_false_overrides_passing_metric(self):
        # exact_match passes (score 1.0) but expectation is false -> fail
        result = evaluate(
            [("ok", "ok")],
            evaluators=["exact_match"],
            config={"exact_match": {"objective": {"expect": False}}},
        )
        assert result.cases[0].status == "fail"
        assert result.cases[0].metrics["exact_match"].passed is False
        assert "exact_match" in result.cases[0].details

    def test_maximize_without_threshold_is_noop(self):
        # identical behavior to no objective: evaluator's own verdict stands
        result = evaluate(
            [("ok", "no")],
            evaluators=["exact_match"],
            config={"exact_match": {"objective": {"direction": "maximize"}}},
        )
        assert result.cases[0].status == "fail"

    def test_minimize_without_threshold_raises(self):
        with pytest.raises(ValueError):
            evaluate(
                [("a", "b")],
                evaluators=["levenshtein"],
                config={"levenshtein": {"objective": {"direction": "minimize"}}},
            )

    def test_bad_direction_raises(self):
        with pytest.raises(ValueError):
            evaluate(
                [("a", "b")],
                evaluators=["levenshtein"],
                config={"levenshtein": {"objective": {"direction": "sideways", "threshold": 0.5}}},
            )

    def test_expect_with_direction_raises(self):
        with pytest.raises(ValueError):
            evaluate(
                [("a", "b")],
                evaluators=["levenshtein"],
                config={"levenshtein": {"objective": {"expect": True, "direction": "maximize"}}},
            )

    def test_error_metric_wins_over_objective(self):
        result = evaluate(
            [("[invalid", "x")],
            evaluators=["regex_match"],
            config={"regex_match": {"objective": {"direction": "maximize", "threshold": 0.0}}},
        )
        assert result.cases[0].status == "error"
        assert result.errors == 1
        assert result.failed == 0

    def test_no_objective_unchanged(self):
        result = evaluate([("ok", "no")], evaluators=["exact_match"])
        assert result.cases[0].status == "fail"
```

- [ ] **步骤 2：运行测试确认其失败**

运行：`python3 -m pytest tests/evals/test_runner.py -q`
预期：新增的 `TestObjective` 测试失败（目标配置被忽略 → `expect:false` 下 `exact_match` 依然通过等）；文件中既有的测试仍然通过。

- [ ] **步骤 3：实现目标解析、校验与重新判定**

在 `semantica/evals/runner.py` 中，于 `evaluate` 之前添加两个辅助函数，并把它们接入评估器循环。

```python
def _parse_objective(name, eval_config):
    """Return the validated objective dict, or None when not configured.

    Raises ValueError for invalid configurations (programmer error).
    """
    objective = (eval_config or {}).get("objective")
    if objective is None:
        return None
    direction = objective.get("direction")
    threshold = objective.get("threshold")
    expect = objective.get("expect")

    if expect is not None:
        if direction is not None or threshold is not None:
            raise ValueError(
                f"objective for '{name}': 'expect' cannot be combined with "
                "'direction' or 'threshold'"
            )
        return {"expect": bool(expect)}
    if direction == "minimize":
        if threshold is None:
            raise ValueError(
                f"objective for '{name}': 'minimize' requires a 'threshold'"
            )
        return {"direction": "minimize", "threshold": float(threshold)}
    if direction == "maximize":
        if threshold is None:
            # no bar to re-decide against; treat as absent (evaluator default stands)
            return None
        return {"direction": "maximize", "threshold": float(threshold)}
    raise ValueError(
        f"objective for '{name}': 'direction' must be 'maximize' or 'minimize' "
        f"(got {direction!r})"
    )


def _apply_objective(metric, objective):
    """Return the objective-adjusted pass verdict for a non-error metric."""
    if "expect" in objective:
        return bool(metric.score) == objective["expect"]
    if objective["direction"] == "minimize":
        return metric.score <= objective["threshold"]
    return metric.score >= objective["threshold"]
```

然后修改 `evaluate()` 中的评估器循环：解析出的目标每个用例只计算一次（放在评估器循环之外，因为它只依赖合并后的配置），并在循环内部应用：

```python
        objective_by_name = {
            name: _parse_objective(name, merged.get(name) or {})
            for name in evaluators
        }
        metrics: Dict[str, EvalMetric] = {}
        details: Dict[str, Any] = {}
        failed, errored = False, False
        for name in evaluators:
            eval_config = merged.get(name) or {}
            try:
                metric = get_evaluator(name)(actual, expected, config=eval_config)
                objective = objective_by_name.get(name)
                if objective is not None and "error" not in metric.meta:
                    metric = EvalMetric(metric.score, _apply_objective(metric, objective), metric.meta)
                metrics[name] = metric
                if "error" in metric.meta:
                    errored = True
                    details[name] = metric.meta
                elif not metric.passed:
                    failed = True
                    details[name] = metric.meta
            except Exception as exc:  # noqa: BLE001
                errored = True
                metrics[name] = EvalMetric(0.0, False, {"error": str(exc)})
                details[name] = {"error": str(exc)}
```

注意：`objective_by_name` 每个用例只计算一次（它只依赖合并后的配置），因此非法配置会在第一个用例处抛出 `ValueError`——满足快速失败要求。`EvalMetric` 是冻结数据类(frozen dataclass)，因此重新判定会构造一个保留 score/meta 的新实例。

- [ ] **步骤 4：运行测试确认其通过**

运行：`python3 -m pytest tests/evals/test_runner.py -q`
预期：`TestObjective` 全部测试通过；既有测试仍然通过。

- [ ] **步骤 5：运行完整的 evals 测试套件**

运行：`python3 -m pytest tests/evals -q`
预期：62 个既有测试加新增测试全部通过（无回归）。

- [ ] **步骤 6：提交**

```bash
git add semantica/evals/runner.py tests/evals/test_runner.py
git commit -m "feat(evals): add per-metric objective support to runner"
```

---

### 任务 2：文档——usage.md 与 CHANGELOG

**文件：**
- 修改：`semantica/evals/usage.md`
- 修改：`CHANGELOG.md`

**接口：**
- 消费：任务 1 实现的目标配置面（确切键名：`objective.direction`、`objective.threshold`、`objective.expect`；以及校验规则）。
- 产出：仅文档。

- [ ] **步骤 1：在 usage.md 中添加目标章节**

在既有的"Run the runner over decision records"章节之后追加一个章节：

```markdown
## Set per-evaluator objectives

By default each evaluator decides its own pass/fail. To override that
verdict at the run level, configure an **objective** per evaluator name:

```python
from semantica.evals import evaluate

# Require a minimum similarity (default direction is maximize):
evaluate(
    [("apple", "aple")],
    evaluators=["levenshtein"],
    config={"levenshtein": {"objective": {"direction": "maximize", "threshold": 0.7}}},
)

# Lower is better — override the direction:
evaluate(
    [("night", "nacht")],
    evaluators=["levenshtein"],
    config={"levenshtein": {"objective": {"direction": "minimize", "threshold": 0.5}}},
)

# Boolean expectation on a 0/1 metric:
evaluate(
    [("ok", "ok")],
    evaluators=["exact_match"],
    config={"exact_match": {"objective": {"expect": False}}},
)
```

Rules:

- `maximize` + `threshold`: pass iff `score >= threshold`. `maximize` without
  a threshold is a no-op (the evaluator's own verdict stands).
- `minimize` + `threshold`: pass iff `score <= threshold`. `minimize`
  **requires** a threshold — omitting it raises `ValueError`.
- `expect` (`true`/`false`): pass iff `bool(score)` matches; cannot be
  combined with `direction`/`threshold`.
- A metric whose `meta` contains `"error"` is always an error, never affected
  by an objective.
- Invalid objective config raises `ValueError` before any evaluator runs.
```

- [ ] **步骤 2：添加 CHANGELOG 条目**

在 `## [Unreleased]` → `### Added` 之下，遵循既有风格，在列表顶部（`semantica.evals` 模块条目之前）插入一个新条目：

```markdown
- **`semantica.evals` runner gains per-metric objectives** (#1091)
  - `evaluate()` now accepts `config={"<evaluator>": {"objective": {"direction": "maximize"|"minimize", "threshold": X}}}` to override the evaluator's default pass verdict with a threshold; `{"objective": {"expect": bool}}` expresses a Boolean expectation
  - `minimize` requires a `threshold`; `maximize` without one is a no-op; `expect` cannot be combined with `direction`/`threshold`; invalid config raises `ValueError` before any evaluator runs
  - Error metrics are never affected by objectives (error wins over fail)
  - Backward compatible: no `objective` key → existing behavior unchanged
  - New tests in `tests/evals/test_runner.py::TestObjective`
```

- [ ] **步骤 3：验证文档示例可以运行**

把步骤 1 的三个示例作为 Python 脚本运行（导入 `evaluate`，逐段执行），确认它们不会意外抛出异常。除了"无异常"和状态值合理之外，不需要断言测试输出。

- [ ] **步骤 4：提交**

```bash
git add semantica/evals/usage.md CHANGELOG.md
git commit -m "docs(evals): document per-metric objectives"
```

---

## 自查说明

- **规格覆盖：** §3.1（配置面）→ 任务 1 的辅助函数 + 任务 2 的文档；§3.2（语义：maximize/minimize/expect）→ 任务 1 的 `_apply_objective`；§3.3（错误优先）→ 任务 1 的错误分支 + `test_error_metric_wins_over_objective`；§3.4 规则 1-3（校验）→ 任务 1 的 `_parse_objective` + 4 个校验测试；§3.4 规则 4 → 错误分支；§3.5（聚合不变，details 基于最终判定）→ 任务 1 的循环 + `test_expect_false_overrides_passing_metric` 断言 `details`；§4（快速失败的 `ValueError`）→ 在用例开头运行的 `_parse_objective`；§5（测试）→ 任务 1 的测试类；§6（兼容性）→ `test_no_objective_unchanged` + 全套件通过。
- **类型一致性：** `_parse_objective(name, eval_config) -> Optional[Dict]`、`_apply_objective(metric, objective) -> bool`；`EvalMetric(score, passed, meta)` 在所有位置都按位置参数构造，保持不变。
- **向后兼容：** 配置缺失时目标解析为 `None` → 循环行为与之前完全一致。
