---
work_package_id: WP03
title: 译文过期追踪脚本 ui_zh_status.py
dependencies:
- WP01
requirement_refs:
- FR-008
tracker_refs: []
planning_base_branch: feature/explorer-i18n-p0
merge_target_branch: feature/explorer-i18n-p0
branch_strategy: Planning artifacts for this mission were generated on feature/explorer-i18n-p0. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feature/explorer-i18n-p0 unless the human explicitly redirects the landing branch.
subtasks:
- T013
- T014
- T015
agent: claude
history:
- timestamp: '2026-09-01T09:51:16Z'
  action: created
  agent: claude
agent_profile: python-pedro
authoritative_surface: tools/i18n/
create_intent:
- tools/i18n/ui_zh_status.py
execution_mode: code_change
owned_files:
- tools/i18n/ui_zh_status.py
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile

Before reading anything else, load your assigned agent profile:

```
/ad-hoc-profile-load python-pedro
```

If that command is unavailable, proceed as a careful Python implementer: stdlib-only、typed、小而纯的函数、扫描路径无副作用。

## Objective

实现 `tools/i18n/ui_zh_status.py`：以 git blob sha 比对判定 `explorer/src/i18n/locales/zh.json` 相对 `en.json` 基准的过期状态（fresh/stale/orphan），并做键级 diff（missing_keys/extra_keys）。CLI 契约已冻结在 `kitty-specs/explorer-i18n-p0-01M1DZFC/contracts/ui-zh-status-cli.md`——**以契约为准，不自行发明参数或退出码**。本 WP 与 WP02 并行（都只依赖 WP01）。

## Context

- 仓库根：`/Users/luofisher/ToolsChain/semantica`（执行时在 lane worktree，结构相同）
- 运行环境：仓库 uv 管理的 `.venv`（Python 3.11）；只用标准库（argparse/json/subprocess/re），不新增依赖
- **同族参照物**：`tools/i18n/zh_status.py`（已上线，服务 docs/zh）。你的脚本沿用其机制与代码风格，但输入是 JSON 资源而非 Markdown——读一遍它再动手，输出格式（表格 + --json）与退出码语义保持一致
- 与 docs 版的两个机制差异：
  1. **基准判定**：`zh.json` 的 `__meta.source_version`（40 位 blob sha）对照 HEAD 中 `en.json` 的 blob sha。en.json **不存在 `source_version` 自比**——它是基准本身
  2. **键级 diff**：flatten 两文件 `translation` 下的点号键（**排除 `__meta`**），en 有 zh 无 → `missing_keys`；zh 有 en 无 → `extra_keys`。sha 判 stale 时附带 missing 清单；extra_keys 无条件报告
- 状态判定（contracts/ui-zh-status-cli.md）：`fresh` = sha 一致；`stale` = sha 不一致/`source_version` 缺失或非法；`orphan` = en.json 已不在 HEAD
- 判定基准是 **HEAD 的 blob sha**（`git rev-parse HEAD:<path>` 或一次 `git ls-tree -r HEAD -- explorer/src/i18n/locales/` 批量取），不含工作区未提交改动
- 零侵入：只新增 `tools/i18n/ui_zh_status.py`，不动 zh_status.py 与任何上游文件

## Subtask Guidance

### T013: 资源扫描与键级 diff

**Purpose**: 读两份 JSON、flatten 键集、算 diff。

**Steps**:
1. 定位资源：`explorer/src/i18n/locales/{en,zh}.json`（相对仓库根；`--root` 可改根目录，同 zh_status.py 语义）。
2. `flatten(obj)`：递归展平 `translation` 对象为 `{"nav.explore.label": "..."}` 形式；**跳过 `__meta` 顶层键**（它与 translation 同级，本就不在 translation 内——你 flatten 的输入就是 `data["translation"]`，天然排除；加一道防御即可）。
3. `missing_keys = sorted(en_keys - zh_keys)`；`extra_keys = sorted(zh_keys - en_keys)`。
4. sha 获取：zh 侧读文件 JSON 取 `__meta.source_version`（缺失/非 40 位十六进制 → 视为非法）；en 侧从 `git ls-tree`/`git rev-parse HEAD:` 取 HEAD blob sha（文件不在 HEAD → None → orphan）。

**Validation**:
- [ ] 对 WP01 产出的真实资源文件跑通，键集各约 95-100 键
- [ ] `__meta` 不出现在任何键清单里

### T014: CLI 与输出（表格 / --json / 退出码）

**Purpose**: 冻结契约的对外面。

**Steps**:
1. 参数（契约）：`--json`（机器可读输出）、`--root`（仓库根，默认当前工作目录定位）、`--verbose`（附键清单明细）。
2. 表格输出仿 zh_status.py：路径 | 状态 | recorded sha | current sha | missing | extra；`--json` 输出结构按契约 schema：`{"records": [{"path", "status", "recorded_source_sha", "current_source_sha", "missing_keys", "extra_keys"}], "summary": {"fresh": n, "stale": n, "orphan": n, "missing_keys": n, "extra_keys": n}}`。
3. 退出码：`0` = 扫描完成（允许 stale/orphan，那是报告不是错误）；`1` = 用法/环境错误（资源文件缺失、JSON 解析失败等）；`2` = 保留语义与 zh_status.py 对齐（如输入目录不存在），具体分派照契约表。
4. 只读：不写任何缓存/文件。

**Validation**:
- [ ] `--json` 输出可被 `python3 -m json.tool` 解析且字段齐全
- [ ] 人为改坏 `source_version` → stale + 退出码 0；删 en.json → orphan；删 zh.json → 退出码 1

### T015: 本期产出自检（fresh 门禁）

**Purpose**: 对本 mission 的资源实跑，确认报告 fresh。

**Steps**:
1. 在 WP01 已合入的基线上运行 `python tools/i18n/ui_zh_status.py` 与 `--json`。
2. 期望：`status=fresh`、`summary.missing_keys=0`、`summary.extra_keys=0`、退出码 0。
3. 若报 stale：核对 `source_version` 是否取自 en.json 的正确 blob sha（WP01 用 `git hash-object` 而文件后又被改过 → sha 漂移）。属 WP01 侧问题则反馈给协调方，不要私改资源文件（那超出你的 owned_files）。
4. 性能：单文件对，毫秒级即可，无需优化。

**Validation**:
- [ ] fresh + missing=0 + extra=0 + 退出码 0（在最终基线复核，WP04 会再跑一次作为集成门禁）
- [ ] 输出样式与 zh_status.py 视觉一致（列对齐、状态词一致）

## Test Strategy

不新增 pytest（quickstart 以命令行实跑为验收）；自测 = 上面各 Validation 的降级路径演练（改坏 sha/删文件在临时副本或 git stash 场景做，勿留脏工作区）。

## Definition of Done

- [ ] T013–T015 全部完成且 Validation 勾稽
- [ ] 契约逐条对齐（参数、JSON schema、退出码 0/1/2）
- [ ] 对本期资源报告 fresh
- [ ] 只新增 `tools/i18n/ui_zh_status.py` 一个文件

## Risks

- **sha 时点漂移**：`git hash-object`（工作区内容）与 HEAD blob sha 在提交后可能不同——脚本只认 HEAD；若 WP01 记录的 source_version 是 hash-object 值且提交后 en.json 未再变，两者一致；若不一致，fresh 判定会失败，按 T015.3 处理。
- **JSON 解析容错**：坏 JSON 应走退出码 1，而不是堆栈崩给用户。

## Reviewer Guidance

核对：① 与 contracts/ui-zh-status-cli.md 逐条对照（参数名、schema 字段、退出码）；② `__meta` 排除正确；③ 只读无副作用；④ 与 zh_status.py 风格/输出一致。
