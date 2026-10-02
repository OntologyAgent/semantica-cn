---
work_package_id: WP03
title: 注册与集成验收
dependencies:
- WP01
- WP02
requirement_refs:
- FR-003
- FR-004
tracker_refs: []
planning_base_branch: feature/zh-normalization
merge_target_branch: feature/zh-normalization
branch_strategy: Planning artifacts for this mission were generated on feature/zh-normalization. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feature/zh-normalization unless the human explicitly redirects the landing branch.
subtasks:
- T008
- T009
- T010
history: []
agent_profile: python-pedro
authoritative_surface: semantica/normalize/
create_intent: []
execution_mode: code_change
owned_files:
- semantica/normalize/__init__.py
- semantica/normalize/registry.py
- tests/normalize/test_integration.py
role: implementer
tags: []
agent: "python-pedro"
shell_pid: "77199"
---

# WP03 — 注册与集成验收

## Requirements

- FR-003
- FR-004（全量复核）

## Purpose

两个规范化器接入公共面：`method_registry` 注册、`__init__.py` 导出、组合流水线语义、门禁收口。

## 上下文

- 契约：`contracts/public-api.md` 注册表两条 lambda 形态与导出清单
- 注册表实现：`registry.py`（`method_registry.register(task, name, fn)`，task ∈ text/entity/date/…）
- 门禁：`tools/nightly/run_gate.sh`，基线 `tools/nightly/baseline_failures.txt` 51 条

## 实现要点

1. `__init__.py` 导出 `CJKSpacingNormalizer`、`ZhDateParser`（加入模块 docstring 的 Main Classes 清单）
2. 注册：`text` 域挂 `cjk_spacing`，`date` 域挂 `zh_date`（按契约的 lambda 形态，失败返回 None 而非抛异常）
3. 组合语义测试（test_integration.py 扩展）：
   - `CJKSpacingNormalizer().normalize()` 不破坏后续 `ZhDateParser().parse()` 的 `matched_text` 原文性（先空格后日期，`matched_text` 允许取自规范化后文本）
   - 两者可单独调用、可按 registry 检索调用（`method_registry.list_all("text")` 含 `cjk_spacing`）
4. 门禁：`bash tools/nightly/run_gate.sh` exit 0（失败数 ≤ 51 基线）
5. quickstart §3 命令逐条实跑（含 `DateNormalizer().normalize_date("2026年10月2日")` 路由验证）

## 任务清单

- [ ] T008 注册 + 导出
- [ ] T009 组合/单独调用测试
- [ ] T010 门禁全量 + quickstart 走查

## 验收

```bash
bash tools/nightly/run_gate.sh && echo GATE-OK
python -c "from semantica.normalize import CJKSpacingNormalizer, ZhDateParser, DateNormalizer; print('exports ok')"
```

## Activity Log

- 2026-10-02T03:36:00Z – python-pedro – shell_pid=77199 – Assigned agent via action command
- 2026-10-02T03:37:16Z – python-pedro – shell_pid=77199 – 10/10 registry/dispatch/composition tests
