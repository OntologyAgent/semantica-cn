---
title: "冲突检测模块（Conflicts）"
description: "多源冲突检测与消解：值、类型、时序和逻辑冲突，附调查指南。"
source: reference/conflicts.md
source_version: b23cefe54bf5404f1ad25b381d2be1fef18c8d84
icon: "triangle-exclamation"
---

**`semantica.conflicts`** 在**多个数据源对同一事实各执一词**时检测并消解矛盾：

- 五种冲突类型：值、类型、时序、逻辑、关系
- 七种消解策略：投票、可信度加权、最近优先、最先出现、置信度最高、人工审核、专家审核
- `InvestigationGuideGenerator` 为人工消解产出分步调查指引
- `SourceTracker` 把每个属性值映射到贡献它的数据源，归属完整
- 冲突被显式呈现：绝不静默污染知识图谱


## 为什么要检测冲突

从多个数据源摄取数据时，矛盾不可避免。一份年报说苹果营收 3910 亿美元，一条财经快讯说 3830 亿。没有冲突检测，两个值都会进图，查询会静默返回不一致的答案。

Semantica 的冲突检测把分歧变得显式、可处理：

- **值冲突**：SEC 说营收 3910 亿；路透社说 3830 亿
- **类型冲突**："Python" 在一个源里是 `ProgrammingLanguage`，在另一个源里是 `Snake` 物种
- **时序冲突**：一位 CEO 在重叠的日期区间里有两个不同的雇主
- **逻辑冲突**：一个实体同时持有两个互斥属性
- **关系冲突**：同一条关系在不同源之间的基数或属性不一致

## 导出的类

| 类 | 职责 |
| :--- | :--- |
| `ConflictDetector` | 跨实体列表检测值、类型、关系冲突 |
| `ConflictResolver` | 用可配置策略消解冲突：`voting`、`credibility_weighted`、`most_recent`、`first_seen`、`highest_confidence`、`manual_review`、`expert_review` |
| `ConflictType` | 枚举：`VALUE_CONFLICT`、`TYPE_CONFLICT`、`TEMPORAL_CONFLICT`、`LOGICAL_CONFLICT`、`RELATIONSHIP_CONFLICT` |
| `ResolutionStrategy` | 传给 `ConflictResolver` 的消解策略枚举 |
| `ResolutionResult` | `resolve_conflict` / `resolve_conflicts` 返回的 dataclass |
| `SourceTracker` | 追踪每个实体上每个属性值由哪个源贡献 |
| `SourceReference` | 源文档引用：文档、页码、章节、置信度 |
| `PropertySource` | 属性级聚合溯源：值 + `SourceReference` 对象列表 |
| `ConflictAnalyzer` | 分析冲突模式、严重度分布与分源统计 |
| `ConflictPattern` | 描述检测到的冲突模式的 dataclass |
| `InvestigationGuideGenerator` | 为需人工审核的冲突生成分步调查指南 |
| `InvestigationGuide` | 指南 dataclass：`conflict_id`、`conflict_summary`、`severity`、`investigation_steps`、`recommended_actions` |
| `InvestigationStep` | 步骤 dataclass：`step_number`、`description`、`action`、`expected_outcome` |

## 你能得到什么

- **ConflictDetector** — 跨实体和关系列表检测值、类型、关系冲突。
- **ConflictResolver** — 7 种消解策略：投票、可信度加权、时序偏好等。
- **SourceTracker** — 追踪每条冲突事实来自哪个源，带分源可信度得分。
- **ConflictAnalyzer** — 模式分析、严重度分组、分源统计与趋势识别。
- **InvestigationGuideGenerator** — 为人工审核和专家审核自动生成分步调查清单。
- **便捷函数** — `detect_conflicts()` 和 `resolve_conflicts()`，一次调用搞定。

## 快速开始

<Steps>
  <Step title="摄取前设置可信度得分">
    ```python
    from semantica.conflicts import SourceTracker

    tracker = SourceTracker()
    tracker.set_source_credibility("sec_filings",   0.95)
    tracker.set_source_credibility("pubmed",        0.92)
    tracker.set_source_credibility("wikipedia",     0.80)
    tracker.set_source_credibility("news_articles", 0.65)
    ```
  </Step>
  <Step title="建图后检测冲突">
    ```python
    from semantica.conflicts import ConflictDetector

    detector = ConflictDetector()

    # Detect value conflicts on a specific property
    conflicts = detector.detect_value_conflicts(entities, "revenue")
    print("Found %d conflicts" % len(conflicts))

    for conflict in conflicts:
        print("[%s] entity='%s'  attr='%s'" % (
            conflict.conflict_type, conflict.entity_id, conflict.property_name))
        print("  Values: %s  Severity: %s" % (
            conflict.conflicting_values, conflict.severity))
    ```
  </Step>
  <Step title="按严重度分诊">
    ```python
    from semantica.conflicts import ConflictAnalyzer

    analyzer  = ConflictAnalyzer()
    analysis  = analyzer.analyze_conflicts(conflicts)
    severity_counts = analysis["by_severity"]["counts"]
    severity_details = analysis["by_severity"]["details"]
    print("Critical: %d" % severity_counts.get("critical", 0))
    print("High:     %d" % severity_counts.get("high", 0))
    print("Low:      %d" % severity_counts.get("low", 0))
    ```
  </Step>
  <Step title="低严重度自动消解，严重升级人工">
    ```python
    from semantica.conflicts import ConflictResolver, InvestigationGuideGenerator, ResolutionStrategy

    resolver = ConflictResolver(source_tracker=tracker)

    # Auto-resolve low-severity conflicts
    low_conflicts = severity_details.get("low", [])
    # Re-fetch full Conflict objects if needed: severity_details contains dicts
    auto_resolved = resolver.resolve_conflicts(
        conflicts,
        strategy=ResolutionStrategy.CREDIBILITY_WEIGHTED,
    )

    # Generate investigation guides for critical conflicts
    critical_ids = {d["conflict_id"] for d in severity_details.get("critical", [])}
    critical_conflicts = [c for c in conflicts if c.conflict_id in critical_ids]

    generator = InvestigationGuideGenerator()
    for conflict in critical_conflicts:
        guide = generator.generate_guide(conflict)
        print("\n%s" % guide.title)
        for step in guide.investigation_steps:
            print("  [%d] %s" % (step.step_number, step.description))
            print("       Action: %s" % step.action)
    ```
  </Step>
</Steps>

<Warning>
  **先检测，后合并。** 在去重和图构建之前，对原始实体数据跑冲突检测。在已含合并实体的活图上补检测要难得多：原始来源归属已经丢了。
</Warning>

## ConflictDetector

```python
from semantica.conflicts import ConflictDetector

detector = ConflictDetector()

# Detect value conflicts on a specific property
conflicts = detector.detect_value_conflicts(entities, "revenue")
```

### 检测类型

| 类型 | 检测内容 | 示例 |
| :---- | :--------------- | :------- |
| `VALUE` | 同一实体、同一属性在不同源之间取值不同 | 营收 3910 亿 vs 3830 亿 |
| `TYPE` | 同一实体被归为不同类型 | "Python" 是语言还是蛇 |
| `TEMPORAL` | 时间戳或有效期窗口冲突 | 一位 CEO 同时任职两家公司 |
| `LOGICAL` | 属性组合在逻辑上不一致 | `is_alive=True` 但设了 `death_date` |
| `RELATIONSHIP` | 关系属性在不同源之间不一致 | 两个源给出边权重 0.9 vs 0.3 |

<Warning>
  **`ConflictDetector` 没有直接实现 `TEMPORAL` 和 `LOGICAL` 冲突检测。** `ConflictType` 枚举保留这两个类型供自定义流水线使用，但检测器类只实现了 `detect_value_conflicts`、`detect_type_conflicts`、`detect_relationship_conflicts` 和 `detect_entity_conflicts`。
</Warning>

按类型做定向检测：

```python
# Detect value conflicts for a specific property
value_conflicts = detector.detect_value_conflicts(entities, "revenue")

# Detect type classification conflicts
type_conflicts = detector.detect_type_conflicts(entities)

# Detect relationship property conflicts (takes a list of relationship dicts)
relation_conflicts = detector.detect_relationship_conflicts(relationships)

# Detect conflicts across all properties of a set of entities
all_conflicts = detector.detect_entity_conflicts(entities)
```

### ConflictDetector 方法

| 方法 | 返回 | 说明 |
| :------ | :------- | :----------- |
| `detect_value_conflicts(entities, property_name, entity_type=None)` | `List[Conflict]` | 检测同一属性在实体实例之间的取值分歧 |
| `detect_type_conflicts(entities)` | `List[Conflict]` | 检测类型归类冲突 |
| `detect_relationship_conflicts(relationships)` | `List[Conflict]` | 检测关系属性冲突（接受关系 dict 列表） |
| `detect_entity_conflicts(entities, entity_type=None)` | `List[Conflict]` | 检测一组实体在全部受监控属性上的冲突 |
| `get_conflict_report()` | `Dict[str, Any]` | 生成所有已检测冲突的汇总报告 |

## ConflictResolver

```python
from semantica.conflicts import ConflictResolver, ResolutionStrategy

resolver = ConflictResolver()
results  = resolver.resolve_conflicts(conflicts, strategy=ResolutionStrategy.VOTING)

for result in results:
    print("Resolved '%s' -> %s" % (result.conflict_id, result.resolved_value))
    print("  Strategy: %s  Confidence: %.2f" % (result.resolution_strategy, result.confidence))
```

<Tip>
  **不要全自动消解一切。** `severity == "critical"` 或 `severity == "high"` 的冲突用 `MANUAL_REVIEW`：严重度高意味着分歧大，判错的代价也大。
</Tip>

### 消解策略怎么选

<Tabs>
  <Tab title="CREDIBILITY_WEIGHTED（推荐）">
    按各源被赋予的可信度得分给值加权：自动偏向权威来源：

    ```python
    from semantica.conflicts import ConflictResolver, SourceTracker, ResolutionStrategy

    tracker = SourceTracker()
    tracker.set_source_credibility("sec_filings",   0.92)
    tracker.set_source_credibility("wikipedia",     0.80)
    tracker.set_source_credibility("news_articles", 0.65)

    resolver = ConflictResolver(source_tracker=tracker)
    results  = resolver.resolve_conflicts(
        conflicts,
        strategy=ResolutionStrategy.CREDIBILITY_WEIGHTED,
    )
    ```

    **最适合：** 数据源有已知可靠性排序的场景（SEC > 博客）。
  </Tab>
  <Tab title="VOTING">
    多数投票：跨源最常见的值胜出：

    ```python
    results = resolver.resolve_conflicts(conflicts, strategy=ResolutionStrategy.VOTING)
    ```

    **最适合：** 3 个以上可信度大致相当的源。所有源可信度得完全相同时，`CREDIBILITY_WEIGHTED` 的行为与 `VOTING` 一致。
  </Tab>
  <Tab title="MOST_RECENT / FIRST_SEEN">
    ```python
    # Most recent source wins: for fast-changing facts
    results = resolver.resolve_conflicts(conflicts, strategy=ResolutionStrategy.MOST_RECENT)

    # First seen wins: for stable facts (founding date, original name)
    results = resolver.resolve_conflicts(conflicts, strategy=ResolutionStrategy.FIRST_SEEN)
    ```
  </Tab>
  <Tab title="MANUAL_REVIEW / EXPERT_REVIEW">
    ```python
    # Flag for human review: use with InvestigationGuideGenerator
    results   = resolver.resolve_conflicts(conflicts, strategy=ResolutionStrategy.MANUAL_REVIEW)
    generator = InvestigationGuideGenerator()

    for conflict in conflicts:
        guide = generator.generate_guide(conflict)
        print("%s" % guide.title)
        for step in guide.investigation_steps:
            print("  [%d] %s" % (step.step_number, step.description))
    ```

    **最适合：** 高风险决策（`severity == "critical"`）、受监管数据（HIPAA/SOX）、领域歧义。
  </Tab>
  <Tab title="策略对比">

    | 策略 | 枚举 | 适用场景 |
    | :-------- | :---- | :----------- |
    | 多数投票 | `VOTING` | 3 个以上可信度大致相当的源 |
    | 可信度加权 | `CREDIBILITY_WEIGHTED` | 各源权威级别不同 |
    | 最近优先 | `MOST_RECENT` | 快速变化的事实：股价、人数、状态 |
    | 最先出现 | `FIRST_SEEN` | 稳定事实：成立日期、原始名称 |
    | 置信度最高 | `HIGHEST_CONFIDENCE` | 抽取流水线输出带置信度得分 |
    | 人工审核 | `MANUAL_REVIEW` | 高风险决策、受监管数据 |
    | 专家审核 | `EXPERT_REVIEW` | 领域歧义：升级给专家 |

  </Tab>
</Tabs>

用便捷别名让代码更短：

```python
from semantica.conflicts import voting, credibility_weighted, most_recent, highest_confidence

results = resolver.resolve_conflicts(conflicts, strategy=voting)
```

## SourceTracker

```python
from semantica.conflicts import SourceTracker, SourceReference

tracker = SourceTracker()
tracker.set_source_credibility("sec_10k",   0.92)
tracker.set_source_credibility("wikipedia", 0.80)

source_ref = SourceReference(
    document="sec_10k_2023",
    page=12,
    confidence=0.95,
)
tracker.track_property_source(
    entity_id="apple_inc",
    property_name="revenue",
    value="$391B",
    source=source_ref,
)

# Returns a PropertySource object with .value and .sources (List[SourceReference])
prop_source = tracker.get_property_sources("apple_inc", "revenue")
if prop_source:
    print("Value: %s" % prop_source.value)
    for s in prop_source.sources:
        credibility = tracker.get_source_credibility(s.document)
        print("  %s (confidence: %.2f, credibility: %.2f)" % (
            s.document, s.confidence, credibility))

chain = tracker.get_traceability_chain("apple_inc")
```

**关键行为：**
- 未显式设置的源，可信度得分默认 0.50
- `SourceTracker` 存储属性级溯源：每个值由哪个源贡献都能精确回溯

<Warning>
  **可信度得分务必显式设置。** 所有源的默认可信度都是 0.50。不设分的话，`CREDIBILITY_WEIGHTED` 的行为与 `VOTING` 完全相同。这个策略的威力全在区分度上。
</Warning>

<Tip>
  **与溯源联动。** `SourceTracker` 直接对接 [Provenance](./provenance.md) 模块的审计链。要解释一个消解后的值是怎么选出来的，溯源记录能给出完整链条。
</Tip>

## ConflictAnalyzer

```python
from semantica.conflicts import ConflictAnalyzer

analyzer = ConflictAnalyzer()

analysis     = analyzer.analyze_conflicts(conflicts)
patterns     = analysis["patterns"]
severity_counts = analysis["by_severity"]["counts"]
source_stats = analysis["by_source"]
trends       = analyzer.analyze_trends(conflicts)

# analyze_trends returns a list of dicts, one per time period
for t in trends:
    print("Period: %s  Count: %d  Trend: %s" % (
        t["period"], t["conflict_count"], t["trend"]))
```

**关键行为：**
- `analyze_conflicts()["patterns"]` 返回 `ConflictPattern` 对象列表：用 `pattern.pattern_type` 和 `pattern.frequency` 找出系统性的数据质量问题
- `analyze_conflicts()["by_source"]` 含 `counts` 和 `top_sources`：频繁出现在冲突里的源，上游数据可能有问题
- `analyze_trends()` 返回按时间段的 dict 列表（`period`、`conflict_count`、`trend`、`trend_direction`）：`trend` 取 `"increasing"`、`"decreasing"` 或 `"stable"`

<Tip>
  **用 `analyze_conflicts()["by_source"]["top_sources"]` 定位劣质数据源。** 单个源频繁出现在冲突里，是上游的数据质量问题，不是逐条记录能消解的冲突。标记它，去查该源的摄取流水线。
</Tip>

<Tip>
  **严重度是字符串标签，不是分数。** `ConflictDetector` 依据属性重要性和值差异给出 `"critical"`、`"high"` 或 `"medium"`。关键字段（`id`、`name`、`type`、`revenue`）一律判 `"critical"`。优先处理什么由领域上下文决定。
</Tip>

## InvestigationGuideGenerator

为需要人工或专家审核的冲突自动生成人类可读的调查清单：

```python
from semantica.conflicts import InvestigationGuideGenerator

generator = InvestigationGuideGenerator()
guide     = generator.generate_guide(conflict)

print("Title:   %s" % guide.title)
print("Summary: %s" % guide.conflict_summary)

for step in guide.investigation_steps:
    print("  [%d] %s" % (step.step_number, step.description))
    print("       Action: %s" % step.action)
    if step.expected_outcome:
        print("       Expected: %s" % step.expected_outcome)
```

## 数据模式

<AccordionGroup>
  <Accordion title="Conflict schema">

```python
@dataclass
class Conflict:
    conflict_id:        str
    conflict_type:      ConflictType        # VALUE_CONFLICT | TYPE_CONFLICT | ...
    entity_id:          Optional[str]       # entity involved (None for relationship conflicts)
    property_name:      Optional[str]       # the conflicting property name
    relationship_id:    Optional[str]       # relationship involved (for RELATIONSHIP_CONFLICT)
    conflicting_values: List[Any]           # conflicting values (one per source)
    sources:            List[Dict[str, Any]]# source dicts for each value
    confidence:         float               # detection confidence 0–1 (default: 1.0)
    severity:           str                 # "low" | "medium" | "high" | "critical"
    recommended_action: Optional[str]
    metadata:           Dict[str, Any]
```

  </Accordion>
  <Accordion title="ResolutionResult schema">

```python
@dataclass
class ResolutionResult:
    conflict_id:        str
    resolved:           bool
    resolved_value:     Any                 # None if unresolved or flagged for review
    resolution_strategy: Optional[str]      # e.g. "voting", "credibility_weighted"
    confidence:         float               # 0.0–1.0
    sources_used:       List[str]           # document IDs that contributed
    resolution_notes:   Optional[str]
    metadata:           Dict[str, Any]
```

  </Accordion>

  <Accordion title="ConflictType enum">

```python
from semantica.conflicts import ConflictType

ConflictType.VALUE_CONFLICT         # revenue is $391B in source A, $383B in source B
ConflictType.TYPE_CONFLICT          # "Apple" is ORGANIZATION in one source, PRODUCT in another
ConflictType.TEMPORAL_CONFLICT      # overlapping validity windows with contradictory states
ConflictType.LOGICAL_CONFLICT       # fact violates an ontology axiom or SHACL constraint
ConflictType.RELATIONSHIP_CONFLICT  # inconsistent relationship properties across sources
```

  </Accordion>
  <Accordion title="InvestigationGuide and InvestigationStep schemas">

```python
@dataclass
class InvestigationGuide:
    conflict_id:         str
    conflict_summary:    str                      # generated summary of the disagreement
    severity:            str                      # "low" | "medium" | "high" | "critical"
    conflicting_sources: List[Dict[str, Any]]
    investigation_steps: List[InvestigationStep]
    recommended_actions: List[str]
    context:             Dict[str, Any]
    generated_at:        str                      # ISO timestamp
    # title is a @property: "Investigation: <conflict_id>"

@dataclass
class InvestigationStep:
    step_number:      int
    description:      str   # what to do
    action:           str   # specific action to take
    expected_outcome: Optional[str]
```

  </Accordion>
</AccordionGroup>

- [Deduplication](./deduplication.md) — 冲突检测前先消解重复实体。
- [Ontology](./ontology.md) — 逻辑冲突用 SHACL 形状和本体公理判定。
- [Provenance](./provenance.md) — 追踪每条冲突事实的来源。
- [Knowledge Graph](./kg.md) — 被检测冲突的那张图。
