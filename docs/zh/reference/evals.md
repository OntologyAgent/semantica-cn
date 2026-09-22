---
title: "评估模块（Evals）"
description: "用确定性评估器与模型支撑的评估器加一个小型运行框架，为决策记录、审计轨迹和推理输出打分。"
source: reference/evals.md
source_version: 5c59a3461c27d441e32dfd1e5407a24574b46a98
icon: "chart-line"
---

`semantica.evals` 度量决策智能产出的质量。它拿流水线产出的决策、审计轨迹和推理文本，按你定义的期望打分，返回一个结构化的汇总，可用于日志记录、测试断言或跨运行追踪。

- 一个按名注册的评估器注册表：从精确字符串匹配到 ROUGE 重叠、LLM 评审（LLM-as-judge）
- `decision_scores`：面向 `Decision` 对象的复合评估器，检查结果(outcome)、置信度区间、必填字段、溯源(Provenance)以及（可选的）策略合规
- `evaluate()` 运行器：把多个评估器应用到一个用例列表，聚合通过/失败/错误计数
- 每评估器**目标(objective)**：可在运行级覆盖评估器内置的判定结论

<Note>
  该模块独立于包本身做版本管理：`semantica.evals.__version__` 为 `"0.1.0"`。这里描述的公开接口是稳定的，但在到 1.0 之前会有增量变更（新评估器、新 objective 选项）。
</Note>

## 公开 API

| 名称 | 类型 | 职责 |
| :--- | :--- | :--- |
| `evaluate(cases, evaluators, config=None, target_fn=None)` | 函数 | 对每个用例运行具名评估器，返回 `EvalSummary` |
| `evaluate_repeated(cases, evaluators, config=None, target_fn=None, runs=10)` | 函数 | 对每个用例重复运行 `target_fn` 并聚合统计，返回 `RepeatedSummary` |
| `list_evaluators()` | 函数 | 全部已注册评估器的排序名单 |
| `get_evaluator(name)` | 函数 | 按名查找单个评估器函数 |
| `EvalMetric` | dataclass（frozen） | 单个评估器的结果：`score`、`passed`、`meta` |
| `CaseResult` | namedtuple | 单个用例的结果：`case_id`、`status`、`metrics`、`details` |
| `EvalSummary` | dataclass | 跨用例聚合：`total`、`passed`、`failed`、`errors`、`pass_rate`、`cases` |
| `SampleStats` | dataclass（frozen） | 单评估器在重复运行上的统计：`n`、`passes`、`errors`、`pass_rate`、`mean_score`、`stddev`、`any_passed`、`all_passed`、`objective_passed`、`samples` |
| `RepeatedCaseResult` | dataclass（frozen） | 单个用例的重复运行结果：`case_id`、`verdict`、`stats` |
| `RepeatedSummary` | dataclass | 跨重复采样用例的聚合：`runs`、`stable_pass`、`flaky`、`stable_fail`、`errors`、`cases` |

```python
import semantica.evals as evals
from semantica.evals import evaluate, evaluate_repeated, list_evaluators, get_evaluator
```

## 内置评估器

每个评估器都是形如 `fn(actual, expected, config=None) -> EvalMetric` 的普通函数，以稳定名称注册。`list_evaluators()` 返回当前集合：

```python
>>> list_evaluators()
['decision_scores', 'exact_match', 'keyword_check', 'length_range',
 'levenshtein', 'llm_as_judge', 'numeric_range', 'regex_match', 'rouge',
 'temporal_range']
```

| 名称 | 通过条件 | 相关 `config` 键 |
| :--- | :--- | :--- |
| `exact_match` | `actual == expected` | 无 |
| `regex_match` | `re.search(expected, actual)` 匹配到 | 无 |
| `keyword_check` | 每个必需词都出现在 `actual` 中（词边界） | `required`（缺省回退到 `expected`） |
| `numeric_range` | `min <= actual <= max` | `min`、`max`（都必填） |
| `temporal_range` | ISO 日期时间的 `actual` 落在 `[min, max]` 内 | `min`、`max`（ISO 字符串，都必填） |
| `length_range` | `min <= len(actual) <= max` | `min`（默认 0）、`max`（必填） |
| `levenshtein` | 归一化相似度 `>= threshold` | `threshold`（默认 0.8） |
| `rouge` | ROUGE-1 F1 `> 0` 且 `>= threshold` | `threshold`（默认 0.0） |
| `llm_as_judge` | 调用方提供的 `judge_fn(actual, expected)` 返回真值 | `judge_fn`（必填，可调用） |
| `decision_scores` | 对 `Decision` 的全部已配置子检查通过 | 见下 |

无法执行的评估器（坏正则、解析不了的日期时间、缺 `judge_fn`）不抛异常，而是返回 `meta` 里带 `"error"` 键的 `EvalMetric`。需要数值边界的评估器（`numeric_range`、`length_range`）在缺边界时返回带 `"reason"` 键的失败 metric——既不抛异常也不设 `"error"`。

### `decision_scores`

`decision_scores` 接受一个 `Decision`（来自 `semantica.context.decision_models`）或其 dict 形式，运行一组字段级与治理级检查。分数是通过检查的占比；只有全部通过时 `passed` 才为 `True`。

| 子检查 | 控制方式 |
| :--- | :--- |
| 结果匹配 | config 里的 `expected_outcome`，或用例的 `expected`；两者都没设时**跳过** |
| 置信度在区间内 | `min_confidence`（默认 0.0）、`max_confidence`（默认 1.0）；始终运行 |
| `decision_maker`、`reasoning`、`scenario` 非空 | 始终运行 |
| metadata 中存在溯源 | `provenance_key`（默认 `"provenance"`）；始终运行 |
| 策略合规 | `policy_engine` 与 `policy_id` 都设置时才评估；否则跳过 |

在 config 里传 `causal_chain_exists` 会抛 `NotImplementedError`——该键是为未来版本预留的槽位。

## 运行一次评估

`evaluate()` 接受用例列表和评估器名称列表。用例可以是 `(expected, actual)` 元组或 dict：

```python
{
    "id": "loan-001",          # 可选，缺省自动生成
    "expected": ...,           # 可选；有的评估器读它，有的不读
    "actual": ...,             # 被测的值
    "config": {...},           # 可选，本用例的逐评估器设置
    "target_fn": callable,     # 可选，对用例调用以产出 `actual`
}
```

`actual` 缺失时，运行器调用用例的 `target_fn`（或传给 `evaluate()` 的 `target_fn`）来产出它。用例级 `config` 深合并到顶层 `config` 之上，因此单个用例可以只覆盖某个评估器的设置而不丢掉其余设置。

```python
from datetime import datetime

from semantica.context.decision_models import Decision
from semantica.evals import evaluate

decision = Decision(
    decision_id="d-1",
    category="loan",
    scenario="loan-request",
    reasoning="vetted against lending policy v3",
    outcome="approve",
    confidence=0.87,
    timestamp=datetime.now(),
    decision_maker="approver-a",
    metadata={"provenance": "workflow:loan/v3"},
)

cases = [
    {
        "id": "loan-001",
        "actual": decision,
        "config": {
            "decision_scores": {
                "expected_outcome": "approve",
                "min_confidence": 0.7,
            }
        },
    },
]

summary = evaluate(cases, ["decision_scores"])
print(summary.pass_rate)   # 1.0
```

各评估器对每个用例独立运行。某个评估器抛异常时，该用例的 `status` 变为 `"error"`，异常文本记入 metric 的 `meta`；运行其余部分继续。

## 目标（Objectives）

默认每个评估器自行判定通过/失败。**目标(objective)** 在运行级覆盖该判定，按评估器名挂在 `config` 下：

```python
# 把 levenshtein 的门槛从默认 0.8 提到 0.9
evaluate(
    [("apple", "aple")],
    evaluators=["levenshtein"],
    config={"levenshtein": {"objective": {"direction": "maximize", "threshold": 0.9}}},
)

# 越低越好
evaluate(
    [("night", "nacht")],
    evaluators=["levenshtein"],
    config={"levenshtein": {"objective": {"direction": "minimize", "threshold": 0.5}}},
)

# 期望指标「不」匹配
evaluate(
    [("ok", "ok")],
    evaluators=["exact_match"],
    config={"exact_match": {"objective": {"expect": False}}},
)
```

规则：

- `maximize` 带 `threshold`：当且仅当 `score >= threshold` 通过。`maximize` 不带 threshold 是空操作，评估器自己的判定生效。
- `minimize` 带 `threshold`：当且仅当 `score <= threshold` 通过。`minimize` **必须**给 threshold，缺省抛 `ValueError`。
- `expect`（`True` / `False`）：当且仅当 `bool(score)` 等于它时通过。不能与 `direction` 或 `threshold` 同时使用，且必须是真正的布尔值。
- `meta` 里已带 `"error"` 的 metric 不受任何 objective 影响。
- 非法的 objective 配置会在任何评估器运行之前对每个用例做校验——坏 objective 会让整次运行提前失败，而不是跑到一半。

## 读取汇总

```python
summary = evaluate(cases, ["decision_scores"])

summary.total, summary.passed, summary.failed, summary.errors
summary.pass_rate    # passed / total；空用例列表时为 1.0

for case in summary.cases:
    print(case.case_id, case.status)          # status: "pass" | "fail" | "error"
    for name, metric in case.metrics.items():
        print(name, metric.score, metric.passed)
        print(metric.meta.get("reasons", {}))  # 逐子检查的失败原因
```

`EvalMetric`、`SampleStats`、`RepeatedCaseResult` 是 frozen dataclass（`score: float`、`passed: bool`、`meta: dict` 等）；`CaseResult` 是 namedtuple，两个 `*Summary` 类是普通 dataclass——全部都便于序列化，可记日志或做回归追踪。

## 重复采样

对不确定性的目标（LLM 支撑的抽取、agent 管线、基于采样的评审器）来说，单次判定说明不了什么。`evaluate_repeated` 会对每个用例把 `target_fn` 重跑 `n` 次，并按评估器聚合统计：

```python
from semantica.evals import evaluate_repeated

summary = evaluate_repeated(
    cases,                       # 必须是 dict 用例；见下
    evaluators=["exact_match"],
    target_fn=pipeline_run,      # 每次运行调用一次，产生新鲜的 `actual`
    runs=10,
)

summary.runs            # 10
summary.cases[0].verdict  # "stable_pass" | "flaky" | "stable_fail" | "error"
summary.cases[0].stats["exact_match"].pass_rate   # 例如 0.8
summary.cases[0].stats["exact_match"].stddev      # 例如 0.13
```

每个评估器的 `SampleStats` 携带 `n`、`passes`、`errors`、`pass_rate`（即 `passes / n`）、`mean_score`、`stddev`，以及派生布尔值 `any_passed`（实测 pass@n）和 `all_passed`（实测 pass^n）。判定汇总全部样本：每一轮都通过所有评估器为 `stable_pass`；全部未通过为 `stable_fail`；通过与未通过混杂为 `flaky`；某一轮出错为 `error`。

前提与边界情况：

- 每个用例可以是 dict 或 `(expected, actual)` 元组，与 `evaluate()` 一致。携带**非空**静态 `actual` 的用例没有可采样的东西；把它与 `runs > 1` 同用会抛 `ValueError`。`actual` 为 `None` 视同缺席，与 `evaluate()` 中一样回退到解析器。
- `target_fn` 的异常与评估器失败会成为单轮错误样本，并把用例标记为 `error`；绝不会让整个运行崩溃。
- 目标（objective）层与 `evaluate()` 中一样逐轮生效，同一个目标通过 `SampleStats.objective_passed` 把关聚合 `pass_rate`（例如 `{direction: maximize, threshold: 0.8}` 要求跨轮 80% 的通过率）。
- 至少需要一个评估器，且评估器名必须唯一。
- `runs` 必须 `>= 1`。

## 注意

- `llm_as_judge` 需要 `config["judge_fn"]`，即你提供的可调用对象 `judge_fn(actual, expected) -> bool`。不传入就不会导入任何 LLM 后端。
- `decision_scores` 的治理检查是可选的：只有 `policy_engine` 与 `policy_id` 同时在场才评估策略合规。

## 另见

- [决策智能](../guides/decision-intelligence.md) — 产出本模块打分的 `Decision` 记录
- [推理](./reasoning.md) — 推理文本类评估器可度量的推理输出
- [策略引擎](../guides/policy-engine.md) — `decision_scores` 使用的 `policy_engine`
- [本体评估](./ontology.md) — 本体质量指标的独立工具链
