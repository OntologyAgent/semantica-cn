---
work_package_id: WP02
title: 过期追踪工具 zh_status.py（Foundation）
dependencies: []
requirement_refs:
- FR-006
- FR-007
- NFR-002
tracker_refs: []
planning_base_branch: feat/docs-zh-translation
merge_target_branch: feat/docs-zh-translation
branch_strategy: Planning artifacts for this mission were generated on feat/docs-zh-translation. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/docs-zh-translation unless the human explicitly redirects the landing branch.
subtasks:
- T005
- T006
- T007
- T008
- T009
agent: claude
history:
- timestamp: '2026-08-31T23:50:32Z'
  action: created
  agent: claude
agent_profile: python-pedro
authoritative_surface: tools/i18n/
create_intent: []
execution_mode: code_change
owned_files:
- tools/i18n/**
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile

Before reading anything else, load your assigned agent profile:

```
/ad-hoc-profile-load python-pedro
```

If that command is unavailable, proceed as a careful Python implementer: stdlib-only, typed, small pure functions, no side effects in the scan path.

## Objective

实现 `tools/i18n/zh_status.py`：扫描 `docs/zh/**/*.md` 的 frontmatter，用 git blob sha 比对判定每篇译文 fresh/stale/orphan。CLI 契约已冻结在 `kitty-specs/docs-zh-translation-01M1D2MJ/contracts/zh-status-cli.md`——**以契约为准，不自行发明参数或退出码**。本 WP 与 WP01 并行，是所有翻译 WP 的验收依赖。

## Context

- 仓库根：`/Users/luofisher/ToolsChain/semantica`（执行时在 lane worktree，结构相同）
- 运行环境：uv 管理的 `.venv`（Python 3.11）；工具必须只用标准库，不新增依赖
- `docs/zh/` 在本 WP 执行时**可能尚不存在**（WP03/04/05 与你并行）——这正是退出码 2 的合法场景，不是错误
- 判定基准是 **HEAD 的 blob sha**，不含工作区未提交改动；命令形如 `git rev-parse HEAD:docs/<source>`，或合并为一次 `git ls-tree -r HEAD -- docs/` 批量取（推荐，省子进程）
- 契约要点：`--json`/`--root`/`--verbose` 三参数；退出码 0=扫描完成（允许 stale/orphan）、1=用法/环境错误、2=docs/zh 缺失；只读、不写缓存

## Subtask Guidance

### T005: 扫描与 frontmatter 解析

**Purpose**: 找到全部译文并读出 `source`/`source_version`。

**Steps**:
1. `glob("docs/zh/**/*.md", recursive=True)` 收集文件，保持相对路径输出（如 `docs/zh/quickstart.md`）
2. 解析 frontmatter：只处理文件开头的 `--- ... ---` 块，逐行切 `key: value`；**不要引入 yaml 库**——四字段（title/description/source/source_version）都是简单标量
3. 定义纯函数 `parse_frontmatter(text) -> dict`，便于单测；缺失字段返回不含该 key 的 dict，不抛异常
4. `source` 字段语义：相对 `docs/` 的英文源路径（如 `quickstart.md` → `docs/quickstart.md`）

**Validation**:
- [ ] 对手工构造的最小 md 样例（四字段齐全/缺字段/无 frontmatter 三种）解析结果正确

### T006: sha 比对与三态判定

**Purpose**: 核心逻辑：fresh/stale/orphan。

**Steps**:
1. 一次性 `git ls-tree -r HEAD -- docs/` 建 `{path: blob_sha}` 映射；对每篇译文：
   - 英文源不在 HEAD → `orphan`（current_source_sha 为 None）
   - `recorded == current` → `fresh`
   - 否则 → `stale`
2. `source_version` 缺失或非 40 位十六进制 → 按 `stale` 处理，JSON 条目加 `"reason": "missing_source_version"`（人类输出打印原因）
3. 注意：判定基于 HEAD；工作区未提交的英文改动**不参与**（契约明文）
4. `git` 调用统一走 `subprocess.run([...], capture_output=True, text=True)`；非零退出视为环境错误（归 T007 的退出码 1）

**Validation**:
- [ ] 三种状态各有至少一个真实样例验证（可用临时 git repo 构造）

### T007: CLI 与退出码

**Purpose**: 固化契约的命令面。

**Steps**:
1. `argparse`：`--json`（store_true）、`--root`（default `"."`）、`--verbose`（store_true）
2. 退出码：0=扫描完成（含全 stale）；1=`--root` 非 git 仓库或 git 不可用；2=`docs/zh/` 不存在或无任何 `.md`
3. 人类可读输出：每行 `状态  路径`，末尾 summary 一行；stale 行附 `(recorded <sha7> → current <sha7>)`；`--verbose` 时对 stale 加 `git diff --stat <recorded> -- docs/<source>` 的一行摘要
4. JSON 输出严格按契约 schema：`generated_at`（ISO-8601 UTC）、`summary{fresh,stale,orphan}`、`entries[]`（path/source/status/recorded_source_sha/current_source_sha，orphan 的 current 为 null）
5. 退出码 2 时输出一句中文提示（不是 traceback），`--json` 时输出 `{"error": "docs_zh_missing"}` 结构

**Validation**:
- [ ] 三种退出码各实测一次
- [ ] `--json` 输出可被 `python -m json.tool` 解析且字段与契约一致

### T008: 行为自测

**Purpose**: 对照契约逐条验证，含降级路径。

**Steps**:
1. 真实路径：在仓库根运行 `python tools/i18n/zh_status.py` 与 `--json`——此时 docs/zh 可能为空，预期退出码 2（把该结果记为基线）
2. 降级路径：`--root /tmp`（非 git）→ 退出码 1；构造一个临时 git repo（tempfile + git init）放一篇假译文验证 fresh 与 stale 两态
3. 每条契约"行为规则"在自测记录中逐条打勾，写进完成备注

**Validation**:
- [ ] 契约 6 条行为规则全部有对应实测证据
- [ ] 无任何 traceback 泄漏到用户输出

### T009: 性能验证

**Purpose**: 兑现 ≤5s 预算。

**Steps**:
1. 83 文件规模演练：临时 git repo 里提交 83 个假译文 + 83 个假英文源，`time python tools/i18n/zh_status.py --json` 计时
2. 若超 5s：确认已用单次 `git ls-tree` 而非逐文件 `git rev-parse`；仍是瓶颈再优化（如减少 diff 子进程）
3. 记录实测耗时到完成备注

**Validation**:
- [ ] 83 文件规模实测 ≤5s
- [ ] 实现只依赖标准库

## Branch Strategy

- Planning branch: `feat/docs-zh-translation`
- Final merge target: `feat/docs-zh-translation`
- Execution happens in the lane worktree allocated from `lanes.json` after finalize-tasks; commit into your lane branch as instructed by the implement action.

## Definition of Done

- [ ] `tools/i18n/zh_status.py` 落盘，`python tools/i18n/zh_status.py --help` 可用
- [ ] T005–T009 全部 Validation 勾选
- [ ] 未触碰 owned_files（`tools/i18n/**`）之外的任何文件
- [ ] 提交信息：`feat(i18n): add zh_status translation freshness tracker`

## Risks

- macOS 系统代理不影响本工具（纯本地 git 调用）；但注意 `git ls-tree` 需在仓库根语义下运行——统一用 `git -C <root>`
- frontmatter 手工解析对缩进/引号变体可能误读 → 先按 T005 的三种样例测试再扩展

## Reviewer Guidance

- 逐条比对 contracts/zh-status-cli.md：参数、退出码、JSON 字段名、行为规则
- 确认无第三方 import；确认判定走 HEAD 而非工作区
- 抽查 orphan 路径：把某译文的 source 指向不存在的英文文件，验证输出与退出码
