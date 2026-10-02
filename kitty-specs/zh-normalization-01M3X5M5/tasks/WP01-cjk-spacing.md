---
work_package_id: WP01
title: CJK 空格规范化器
dependencies: []
requirement_refs:
- FR-001
tracker_refs: []
planning_base_branch: feature/zh-normalization
merge_target_branch: feature/zh-normalization
branch_strategy: Planning artifacts for this mission were generated on feature/zh-normalization. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feature/zh-normalization unless the human explicitly redirects the landing branch.
subtasks:
- T001
- T002
- T003
history: []
agent_profile: python-pedro
authoritative_surface: semantica/normalize/cjk_spacing.py
create_intent:
- semantica/normalize/cjk_spacing.py
- tests/normalize/test_cjk_spacing.py
execution_mode: code_change
owned_files:
- semantica/normalize/cjk_spacing.py
- tests/normalize/test_cjk_spacing.py
role: implementer
tags: []
agent: "python-pedro"
shell_pid: "42211"
---

# WP01 — CJK 空格规范化器

## Requirements

- FR-001

## Purpose

交付 `semantica/normalize/cjk_spacing.py`：`CJKSpacingNormalizer`，三策略（add/remove/preserve）幂等实现，纯西文输入 byte-identical，U+3000 全角空格归一为半角。

## 上下文

- 契约：mission 的 contracts/public-api.md（构造参数、两个方法签名、返回结构）
- 字符类事实：research.md R2（CJK 表意 U+4E00–U+9FFF / U+3400–U+4DBF / U+F900–U+FAFF；中文标点 U+3001–U+303F、全角 ASCII U+FF01–U+FF5E；西文 = ASCII 字母数字）
- 风格基准：同目录 text_normalizer.py / number_normalizer.py（类结构、logger、模块 docstring 格式）
- 零第三方依赖（标准库 re/unicodedata）

## 实现要点

1. 字符类判定用预编译正则或字符区间函数；核心边界规则（pangu 语义）：
   - 西文字符与 CJK 表意文字相邻 → add 策略插入一个半角空格 / remove 策略删除既有空格 / preserve 不动
   - **全角标点与汉字之间不加空格**；全角标点与西文之间默认也不加（不过度修正，与 pangu 默认一致）
   - U+3000 → 半角空格（三种策略都先执行此归一）
2. 幂等性：插入/删除后不产生新边界（add 插入的空格两侧是「西文 空格 CJK」，二次运行不再匹配）
3. `normalize(text) -> str`；`normalize_detailed(text) -> {"normalized", "boundaries_adjusted", "policy"}`
4. 计数 = 本次插入数 + 删除数

## 任务清单

- [ ] T001 字符类判定 + 三策略 + U+3000 归一
- [ ] T002 normalize_detailed + 纯西文 byte-identical（实现层面：无 CJK/全角字符时直接返回原串）
- [ ] T003 测试：幂等（全样例二次运行不变）、三策略往返（add 后 remove 复原）、R2/R4 边界样例（`Semantica知识图谱`、`AI驱动`、`Hello world 123` 零改动、全角标点行为、U+3000、NBSP 不在范围）

## 验收

```bash
uv run --frozen pytest tests/normalize/test_cjk_spacing.py -q   # 全绿，≥20 用例
python -c "from semantica.normalize.cjk_spacing import CJKSpacingNormalizer as C; print(C().normalize('Semantica知识图谱'))"
# 期望输出: Semantica 知识图谱
```

## Activity Log

- 2026-10-02T02:18:15Z – python-pedro – shell_pid=42211 – Assigned agent via action command
