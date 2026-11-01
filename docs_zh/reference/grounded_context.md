---
title: "Grounded Context 组装（Grounded Context Assembly）"
description: "组装与真值维护保持一致的 RAG 上下文：注册的摘要与引用随其证据撤回而撤回，并支持双时态历史读取。"
source: reference/grounded_context.md
source_version: 070072e1fd89614b408c9156a5e81ba84210da42
icon: "shield-check"
---

`GroundedContextAssembler` 把检索到的内容变成模型就绪的上下文，并保证它在组装时刻与真值维护会话一致。当某条注册摘要或引用背后的证据被撤回或取代时，该内容会从当前回答中消失——而历史坐标仍能精确复现当时已知的内容。存储记录本身从不被修改。

## 四个阶段

整个栈是四个小层，每层只消费下一层的公开接口：

| 阶段 | 类 | 职责 |
| :--- | :--- | :--- |
| 1. 真值源 | `TruthMaintenanceSession` / `TemporalTruthMaintenanceAdapter` | 维护事实、支持记录，以及（时态适配器）有效时间与已知时间坐标 |
| 2. 快照 | `TruthSnapshotProvider` | 捕获真值源的不可变 `ContextReadView`（事实、激活的支持、戳记），可取实时状态或历史 `valid_at` / `known_at` 坐标 |
| 3. 注册表 | `ContextArtifactIndex` | 持有不可变的注册内容记录（`GroundedArtifact`），并报告哪些记录在两个视图之间失效或重新合格 |
| 4. 组装 | `GroundedContextAssembler` | 检索候选、对照捕获的视图复核每条注册工件、套用字符预算、渲染带引用脚注的 grounded 文本 |

注册表只管理你显式注册的内容。不带 `grounded_artifact_id` 的普通候选仍按既有的 `truth_maintenance` 标注规则参与：其命名空间、事实、支持与附件必须能通过捕获视图的校验。它们保留检索来源，渲染时不带注册的引用脚注。携带 `grounded_artifact_id` 的候选还必须与注册工件的内容一致并满足其依赖与引用契约；未知 ID 一律排除。

## 完整示例：撤回一个来源

下面的程序可独立运行，无需模型、数据库或网络——只用 `semantica` 本身。它断言 HR 支持，注册一条引用和一条引用它的摘要，组装，然后在同一个 `apply` 批次里撤回 HR 支持并引入一个替代的门禁来源。事实经由门禁存活，但被引用的内容正确地不复存在：

```python
from semantica.context import (
    ContextArtifactIndex,
    ContextDependencies,
    ContextRetriever,
    GroundedArtifact,
    GroundedContextAssembler,
    TruthSnapshotProvider,
)
from semantica.reasoning import FactSupport, Rule, TruthMaintenanceSession

rules = [
    Rule(
        rule_id="eligibility",
        name="Eligibility",
        conditions=["Employed(?x)"],
        conclusion="Eligible(?x)",
    )
]
session = TruthMaintenanceSession(rules=rules)
session.apply(assertions=[FactSupport("hr-1", "Employed(Alice)")])

provider = TruthSnapshotProvider(session, namespace="hr-docs")
index = ContextArtifactIndex(namespace="hr-docs")
view = provider.capture()

citation = GroundedArtifact(
    artifact_id="cite-hr-1",
    kind="citation",
    content="HR record hr-1 states Alice is employed at Acme",
    dependencies=ContextDependencies(frozenset(), frozenset({"hr-1"})),
    built_from=view.stamp,
    validity_policy="dependencies",
    citation_ids=(),
)
summary = GroundedArtifact(
    artifact_id="summary-alice",
    kind="summary",
    content="Alice is eligible.",
    dependencies=ContextDependencies(frozenset({"Eligible(Alice)"}), frozenset()),
    built_from=view.stamp,
    validity_policy="dependencies",
    citation_ids=("cite-hr-1",),
)
index.register(citation)
index.register(summary)

# A tiny read-only store standing in for any real vector backend.
class StaticVectorStore:
    def __init__(self, rows):
        self.rows = [dict(row, metadata=dict(row["metadata"])) for row in rows]

    def search(self, *, query, limit):
        return self.rows[:limit]

def stored_row(record, score=0.9):
    """Project a registered artifact into the row shape the store returns."""
    return {
        "id": record.artifact_id,
        "content": record.content,
        "score": score,
        "metadata": {
            "grounded_artifact_id": record.artifact_id,
            "truth_maintenance": {
                "schema_version": 1,
                "session_id": record.built_from.namespace,
                "required_facts": sorted(record.dependencies.required_facts),
                "required_support_ids": sorted(
                    record.dependencies.required_support_ids
                ),
            },
        },
    }

retriever = ContextRetriever(
    vector_store=StaticVectorStore([stored_row(citation), stored_row(summary)]),
    use_graph_expansion=False,
)
assembler = GroundedContextAssembler(retriever, provider=provider, artifacts=index)

bundle = assembler.assemble("Is Alice eligible?")
assert bundle.text == (
    "[b1] Alice is eligible. (sources: [c1])\n\n"
    "Sources:\n"
    "[c1] HR record hr-1 states Alice is employed at Acme"
)

# Withdraw hr-1 in the same batch as an alternative badge source.
session.apply(
    assertions=[FactSupport("badge-2", "Employed(Alice)")],
    retractions=["hr-1"],
)
report = index.reconcile(provider.capture())
assert sorted(report.invalidated_ids) == ["cite-hr-1", "summary-alice"]

bundle = assembler.assemble("Is Alice eligible?")
assert bundle.text == ""
assert bundle.citations == ()
```

存储的行原封未动：`retriever.vector_store.rows` 仍逐字持有两条记录。变的只有组装出的回答，因为摘要绑定在被撤回的引用上。

## 完整示例：迟到的更正，双时态读取

2026-09-20 记录的一条更正取代了原始 HR 记录 `hr-v1`，但它自身只有效到 2026-09-10。当前回答变空，而历史坐标 `valid_at=2026-09-15, known_at=2026-09-15` 仍精确复现被取代前的回答：

```python
from copy import deepcopy

from semantica.context import (
    ContextArtifactIndex,
    ContextDependencies,
    ContextRetriever,
    GroundedArtifact,
    GroundedContextAssembler,
    TruthSnapshotProvider,
)
from semantica.reasoning import Rule, TemporalTruthMaintenanceAdapter

rules = [
    Rule(
        rule_id="eligibility",
        name="Eligibility",
        conditions=["Employed(?x)"],
        conclusion="Eligible(?x)",
    )
]
graph = {
    "entities": [{"id": "alice"}, {"id": "acme"}],
    "relationships": [
        {
            "source": "alice",
            "target": "acme",
            "type": "EMPLOYED_BY",
            "valid_from": "2026-09-01",
            "valid_until": "2026-09-30",
            "recorded_at": "2026-09-01",
            "metadata": {
                "truth_maintenance": {
                    "support_id": "hr-v1",
                    "fact": "Employed(Alice)",
                }
            },
        }
    ],
}

adapter = TemporalTruthMaintenanceAdapter(rules=rules)
adapter.sync(graph, valid_at="2026-09-15", known_at="2026-09-15")

provider = TruthSnapshotProvider(adapter, namespace="hr-temporal")
index = ContextArtifactIndex(namespace="hr-temporal")
view = provider.capture()

citation = GroundedArtifact(
    artifact_id="cite-hr-v1",
    kind="citation",
    content="HR record hr-v1 states Alice is employed at Acme",
    dependencies=ContextDependencies(frozenset(), frozenset({"hr-v1"})),
    built_from=view.stamp,
    validity_policy="dependencies",
    citation_ids=(),
)
summary = GroundedArtifact(
    artifact_id="summary-alice",
    kind="summary",
    content="Alice is eligible.",
    dependencies=ContextDependencies(frozenset({"Eligible(Alice)"}), frozenset()),
    built_from=view.stamp,
    validity_policy="dependencies",
    citation_ids=("cite-hr-v1",),
)
index.register(citation)
index.register(summary)

class StaticVectorStore:
    def __init__(self, rows):
        self.rows = [dict(row, metadata=dict(row["metadata"])) for row in rows]

    def search(self, *, query, limit):
        return self.rows[:limit]

def stored_row(record, score=0.9):
    return {
        "id": record.artifact_id,
        "content": record.content,
        "score": score,
        "metadata": {
            "grounded_artifact_id": record.artifact_id,
            "truth_maintenance": {
                "schema_version": 1,
                "session_id": record.built_from.namespace,
                "required_facts": sorted(record.dependencies.required_facts),
                "required_support_ids": sorted(
                    record.dependencies.required_support_ids
                ),
            },
        },
    }

retriever = ContextRetriever(
    vector_store=StaticVectorStore([stored_row(citation), stored_row(summary)]),
    use_graph_expansion=False,
)
assembler = GroundedContextAssembler(retriever, provider=provider, artifacts=index)

first = assembler.assemble("Is Alice eligible?")
assert "Alice is eligible." in first.text

# The correction arrives late: hr-v1 is superseded on 9/20 by an
# hr-v2 record that was only valid until 9/10.
revised = deepcopy(graph)
revised["relationships"][0]["superseded_at"] = "2026-09-20"
replacement = deepcopy(graph["relationships"][0])
replacement["valid_until"] = "2026-09-10"
replacement["recorded_at"] = "2026-09-20"
replacement["metadata"]["truth_maintenance"]["support_id"] = "hr-v2"
revised["relationships"].append(replacement)
adapter.sync(revised, valid_at="2026-09-15", known_at="2026-09-20")

current = assembler.assemble("Is Alice eligible?")
assert current.text == ""
assert current.citations == ()

report = index.reconcile(provider.capture())
assert sorted(report.invalidated_ids) == ["cite-hr-v1", "summary-alice"]

# Historical coordinates still reproduce the superseded answer.
historical = assembler.assemble(
    "Is Alice eligible?", valid_at="2026-09-15", known_at="2026-09-15"
)
assert historical.text == first.text

# Asked with the knowledge of the correction, history is empty too.
later = assembler.assemble(
    "Is Alice eligible?", valid_at="2026-09-15", known_at="2026-09-20"
)
assert later.text == ""
```

## API 参考

### `GroundedContextAssembler(retriever, *, provider, artifacts)`

`retriever` 是 `ContextRetriever`，`provider` 是 `TruthSnapshotProvider`，`artifacts` 是与 provider 同命名空间的 `ContextArtifactIndex`。

### `assemble(query, *, max_results=5, max_context_chars=8000, valid_at=None, known_at=None, candidate_pool=None)`

| 参数 | 默认 | 含义 |
| :--- | :--- | :--- |
| `query` | 必填 | 非空搜索查询 |
| `max_results` | `5` | 结果中正文块的上限 |
| `max_context_chars` | `8000` | 完整渲染文本（含脚注）的预算。放不下的块被跳过，绝不截断 |
| `valid_at`, `known_at` | `None` | 时态 provider 的历史坐标；两个都传或都不传 |
| `candidate_pool` | `max(20, max_results * 4)` | 校验前从每个来源取的候选数。校验失败的行也占这个名额，存储里未标注段落多时应调大 |

`assemble` 之前不需要 `reconcile`：组装时会对捕获的视图校验每条工件。想要"哪些工件失效或重新合格"的报告时再调 `index.reconcile(view)`。

Grounded 组装不应用信任等级（`min_trust_tier`）；有效性只来自声明的依赖。

### `GroundedContext`

| 字段 | 含义 |
| :--- | :--- |
| `text` | 渲染出的块（`[b1] ...`）加 `Sources:` 列表（`[c1] ...`） |
| `blocks` | `ContextBlock` 值：`block_id`、`content`、`source`、`citation_ids` |
| `citations` | `ContextCitation` 值：`label`、`artifact_id`、`content`、`support_ids` |
| `stamp` | 组装所依据视图的 `SnapshotStamp` |
| `artifact_revision` | 结果使用的注册表版本 |
| `exclusions` | 每个被排除候选的 `Exclusion(object_id, reason)` |

### 排除原因

| 原因 | 时机 |
| :--- | :--- |
| `missing_annotation` | 候选没有可用的 `truth_maintenance` 标注 |
| `invalid_annotation` | 标注畸形，或引用被当正文检索出来 |
| `wrong_namespace` | 标注或工件属于其他命名空间或来源种类 |
| `missing_fact` | 必需的事实不在视图中 |
| `missing_support` | 必需的支持 ID 在视图中未激活 |
| `unknown_artifact` | `grounded_artifact_id` 未注册 |
| `content_mismatch` | 检索到的文本与注册工件不一致 |
| `snapshot_mismatch` | `snapshot` 策略工件构建自另一个视图 |
| `invalid_citation` | 被引用的工件缺失或自身无效 |
| `empty_content` | 检索到的文本为空或全是空白 |
| `duplicate` | 同一工件或同一文本已被收录 |
| `budget_exceeded` | 块放不进 `max_context_chars` |

### 错误

- `ValidationError`：参数非法、provider 与注册表命名空间不匹配、把别的 provider 的视图传给 `assert_current`、注册时工件非法。
- `ProcessingError`：组装期间来源或注册表发生了变化。重新调 `assemble` 即可。

`GroundedArtifact.validity_policy` 默认 `"snapshot"`（最严策略）：任何新视图都使工件失效。工件应在其声明的事实与支持仍然成立时持续有效，就用 `"dependencies"`。

## 边界

组装的保证刻意收窄。下面每条边界要么是你可依赖的承诺，要么是你**不得**依赖的非承诺：

- **四个阶段，单向信任。** 每层只信任下一层的公开接口。视图是不可变值；注册表记录一经注册即不可变。栈中没有任何环节回写会话、适配器或向量库。
- **过滤器 vs. 组装器。** [真值过滤器](./context.md)在检索期、排序前逐行校验标注。组装器在组装期校验注册工件契约，附加快照一致性、字符预算与引用脚注。两者都不碰存储记录；它们回答不同问题，可以组合使用。
- **命名空间化身。** 注册工件只对盖章时的那个命名空间有效。在新命名空间（或新会话 ID）下重建会话是全新化身：旧化身盖的章在新化身里永远不会重新生效。
- **Provider 实例身份。** 捕获的章含一个不透明的 `provider_id`。`assert_current` 拒绝来自其他 provider 实例的视图，即使两个 provider 包着同一个真值源、所有计数都对得上。手工构造的章可以省略身份做纯值校验，但过不了 provider 新鲜度检查。这个身份不是认证令牌。
- **snapshot 策略对任何新东西都敏感。** `dependencies` 策略工件只要命名空间、来源种类、声明的事实与支持都匹配就持续有效。切换来源种类会重新评估每条注册工件，即使事实与支持 ID 没变。`snapshot` 策略工件额外要求视图章就是它构建时的那个，于是任何新会话版本——即使保留了每个事实——或不同的 provider 实例都使之失效。
- **引用约束。** 引用必须用 `dependencies` 策略且必须声明支持 ID；不得引用其他工件。引用无效的摘要自身被排除（`invalid_citation`）——grounded 回答绝不会保留正文而悄悄丢掉出处。
- **只管理显式注册的内容。** 注册表不推断依赖，也不代你标注记录。普通候选凭有效标注即可参与而无需注册；携带未知工件 ID 的候选无法绕过注册表校验。
- **值校验。** 读视图事实与工件事实依赖使用与真值维护会话相同的基原子校验与规范化空白。时态章以 UTC 存坐标且不改变时刻本身。传给 `capture` 或 `assemble` 的坐标遵循时态适配器（naive 时间按 UTC 读）；手工构造的 `SnapshotStamp` 要求带时区的值。provider 与注册表的命名空间必须一致，即使检索不会返回任何候选。
- **历史读取是隔离的。** 在 `valid_at` / `known_at` 坐标组装只求值历史，绝不改动适配器、provider 或注册表。历史组装期间移动实时游标（advance）是允许的；期间同步新的保留证据则抛 `ProcessingError`，而不是返回混版本的回答。
- **字符预算。** 组装在配置预算内贪心选择内容；超预算的块被排除并上报，而不是在句中截断。它在已收集的、经排序与阈值过滤的候选池里继续，没有预算前的 top-k 截断。每个来源最多返回 `candidate_pool` 个候选；最多产出 `max_results` 个块。普通检索保留其默认 top-k 行为。
- **新鲜度止于返回。** 返回的 bundle 是组装所依据视图的快照。它不过期，也不追踪其后的撤回；要当前回答就再调 `assemble`。
- **不是存储或语义保证。** 这里的一致性指：组装出的上下文按捕获的真值维护视图匹配注册内容契约。它不会让你的向量库事务一致，也不会让模型的结论在语义上正确。

## 相关链接

- [上下文模块（Context）](./context.md) — 检索、真值过滤器与 `ContextRetriever` 细节
- [真值维护（Truth Maintenance）](./truth_maintenance.md) — 会话、支持与撤回语义
- [时态真值维护（Temporal Truth Maintenance）](./temporal_truth_maintenance.md) — 有效窗口、已知时间、取代关系与上文使用的适配器
