---
work_package_id: WP02
title: 中文日期解析器
dependencies: []
requirement_refs:
- FR-002
- FR-004
tracker_refs: []
planning_base_branch: feature/zh-normalization
merge_target_branch: feature/zh-normalization
branch_strategy: Planning artifacts for this mission were generated on feature/zh-normalization. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feature/zh-normalization unless the human explicitly redirects the landing branch.
subtasks:
- T004
- T005
- T006
- T007
history: []
agent_profile: python-pedro
authoritative_surface: semantica/normalize/zh_date_parser.py
create_intent:
- semantica/normalize/zh_date_parser.py
- tests/normalize/test_zh_date_parser.py
execution_mode: code_change
owned_files:
- semantica/normalize/zh_date_parser.py
- semantica/normalize/date_normalizer.py
- tests/normalize/test_zh_date_parser.py
- tests/normalize/test_date_normalizer.py
role: implementer
tags: []
agent: "python-pedro"
shell_pid: "43968"
---

# WP02 — 中文日期解析器

## Requirements

- FR-002
- FR-004

## Purpose

交付 `semantica/normalize/zh_date_parser.py`：`ZhDateParser`（R3 全部格式家族）+ `DateNormalizer` 中文路由扩展。失败语义：非法日期拒绝（value=None）、不支持历法原样保留并计数、全程不抛异常。

## 上下文

- 契约：`contracts/public-api.md`（`parse(text, reference=None) -> dict | None`、`no_year_policy`）
- 数据模型：`data-model.md` Entity 2（ZhDateResult 字段与不变量）
- 格式清单：research.md R3（full / no_year / with_time / han_numeral / relative 五族）
- 风格基准：`date_normalizer.py` 的 `RelativeDateProcessor`（英文相对日期，参考其 reference_date 语义）

## 实现要点

1. 每族一个正则 + 专属转换函数；`二〇二六`/`十月` 汉字数字经映射表转 int（〇〇-九九、十位进位）
2. `no_year_policy`：`current_year`（默认，`year_inferred=True`）/ `strict`（返回 value=None 且 family=no_year）
3. 非法日历值（月>12、`2月30日`、`4月31日`）→ value=None；**不做溢出归一**
4. 不支持历法（`腊月初八`、`民国115年`）→ `{"value": None, "unsupported_matched": <子串>}`，类级计数器 `unsupported_count` 递增
5. `DateNormalizer.normalize_date` 路由：输入（str）含 `年|月|日|号|时|分` 汉字模式 → 先走 `ZhDateParser.parse`；命中且 value 非 None → 按既有返回形态返回；未命中/None → 原有 dateutil 路径，**既有英文行为零回改**（先跑全量既有测试确认基线再动手）
6. 相对日期族：今天/明天/昨天/前天/后天/大后天/下周X（周一–周日），reference 缺省 `datetime.now()`，`year_inferred=True`

## 任务清单

- [ ] T004 五族正则 + 汉字数字转换
- [ ] T005 no_year_policy + 非法拒绝 + 不支持保留计数
- [ ] T006 DateNormalizer 路由（含回退）
- [ ] T007 测试：R3 每族 ≥3 正例 + R4 边界（$5M 不误伤、2月30日、回退路径英文用例原样通过）

## 验收

```bash
uv run --frozen pytest tests/normalize/test_zh_date_parser.py tests/normalize/test_date_normalizer.py -q
python -c "from semantica.normalize.zh_date_parser import ZhDateParser as P; print(P().parse('2026年10月2日 14:30'))"
# value == datetime(2026,10,2,14,30)
```

## Activity Log

- 2026-10-02T02:21:06Z – python-pedro – shell_pid=43968 – Assigned agent via action command
- 2026-10-02T03:32:17Z – python-pedro – shell_pid=43968 – 36/36 tests green; notebook families (range/year-only/year-relative/anchored offsets) absorbed
- 2026-10-02T03:34:43Z – user – shell_pid=43968 – Self-review: 36/36 green incl 6/6 legacy regression; notebook families verified
