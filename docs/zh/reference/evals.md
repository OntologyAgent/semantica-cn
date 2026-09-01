---
title: "评估模块（Evals）"
description: "用于度量知识图谱质量、抽取准确率与流水线性能的评估框架：即将推出。"
source: reference/evals.md
source_version: e39f06b3f1da7b1831ce0191e05dfe1e7ecb7143
icon: "chart-line"
---

**`semantica.evals`** 规划为一个全面的评估框架，用于度量**抽取准确率、图谱质量与流水线性能**。

<Warning>
  **`semantica.evals` 尚未实现。** 该模块目前只是一个占位符，`__all__ = []`，没有任何可导入的类或函数。本页描述的仅为规划中的 API。
</Warning>

## 规划特性

发布后，`semantica.evals` 将提供：

| 规划的类 | 职责 |
| :--- | :--- |
| `KGEvaluator` | 完整性、一致性、模式合规、覆盖率与孤立节点检测 |
| `ExtractionEvaluator` | 对照金标准数据集的命名实体识别(NER)精确率 / 召回率 / F1 与关系抽取指标 |
| `PipelineBenchmark` | 吞吐量（docs/sec）、每步延迟、峰值内存与错误率 |
| `RegressionTracker` | 记录运行结果，跨提交或配置变更比较指标 |
| `EvalReport` | 结构化报告：`{scores, regressions, recommendations}` |
| `DeduplicationEvaluator` | 合并精确率、误报 / 漏报率 |
| `ReasoningEvaluator` | 推理准确率、规则覆盖率与推导深度 |

## 当前的替代方案

在 `semantica.evals` 发布之前，可用 `semantica.ontology.OntologyEvaluator` 获取本体质量指标：

```python
from semantica.ontology import OntologyEvaluator

evaluator = OntologyEvaluator()

# evaluate_ontology 只接收本体 dict
result = evaluator.evaluate_ontology(ontology)

print("Coverage:    ", result.coverage_score)
print("Completeness:", result.completeness_score)
print("Gaps:        ", result.gaps)
print("Suggestions: ", result.suggestions)

# 带类粒度与关系完整度的完整报告
report = evaluator.generate_report(ontology)
print("Coverage score:    ", report["evaluation"]["coverage_score"])
print("Completeness score:", report["evaluation"]["completeness_score"])
print("Relation coverage: ", report["relation_completeness"]["relation_coverage"])
```

`evaluate_ontology()` 返回的 `EvaluationResult` 字段：

| 字段 | 类型 | 说明 |
| :----- | :---- | :----------- |
| `coverage_score` | `float` | 本体可回答的能力问题(competency questions)占比 |
| `completeness_score` | `float` | 类完整度与属性完整度的平均值 |
| `gaps` | `List[str]` | 已识别的覆盖缺口 |
| `suggestions` | `List[str]` | 改进建议 |
| `metrics` | `dict` | 详细的子指标 |

- [语义抽取](../../reference/semantic_extract.md) — 抽取模块。
- [知识图谱](../../reference/kg.md) — 图质量评估。
- [Pipeline](../../reference/pipeline.md) — 流水线性能指标。
- [Ontology Evaluator](./ontology.md) — 本体质量指标现已可用。
