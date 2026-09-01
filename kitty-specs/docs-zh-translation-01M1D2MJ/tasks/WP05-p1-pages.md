---
work_package_id: WP05
title: P1 高频页与 changelog 指路页
dependencies:
- WP01
- WP02
requirement_refs:
- FR-003
- FR-009
- FR-010
- FR-011
tracker_refs: []
planning_base_branch: feat/docs-zh-translation
merge_target_branch: feat/docs-zh-translation
branch_strategy: Planning artifacts for this mission were generated on feat/docs-zh-translation. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/docs-zh-translation unless the human explicitly redirects the landing branch.
subtasks:
- T018
- T019
- T020
- T021
- T022
agent: "claude"
shell_pid: "38784"
history:
- timestamp: '2026-08-31T23:50:32Z'
  action: created
  agent: claude
agent_profile: curator-carla
authoritative_surface: docs/zh/
create_intent:
- docs/zh/faq.md
- docs/zh/cli-setup.md
- docs/zh/storage-backends.md
- docs/zh/explorer-setup.md
- docs/zh/changelog.md
execution_mode: code_change
owned_files:
- docs/zh/faq.md
- docs/zh/cli-setup.md
- docs/zh/storage-backends.md
- docs/zh/explorer-setup.md
- docs/zh/changelog.md
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile

Before reading anything else, load your assigned agent profile:

```
/ad-hoc-profile-load curator-carla
```

If that command is unavailable, proceed as a bilingual technical documentation curator. Note that T022 is special: it is a pointer page, not a translation.

## Objective

覆盖安装后最常查阅的运维页面：`faq.md`、`cli-setup.md`、`storage-backends.md`、`explorer-setup.md` 四篇全译；`changelog.md` 只做指路页（一行说明 + 链回英文原文，**正文不翻**——changelog 变更频繁，翻译必然持续过期）。前置：WP01、WP02 已就位。可与 WP03、WP04 并行。

## Context

- 翻译规范：`docs/zh/README.md`；术语：`docs/zh/glossary.md`
- 通用流程（frontmatter 四字段、代码块、JSX、链接回落、术语查询）与 WP03 相同，先读其"通用流程"
- 优先级为 P1：这四篇是用户装好后排障时最常打开的页面，准确优先于文采

## Subtask Guidance

### T018: 翻译 docs/zh/faq.md

**要点**: Q&A 结构保持；问题句译成自然中文疑问句；答案中的报错信息原文保留（用户要拿它去搜索/比对），报错解释文字翻译。

**Validation**:
- [ ] Q&A 条数与英文版一致
- [ ] 报错/日志样例保留英文原文

### T019: 翻译 docs/zh/cli-setup.md

**要点**: CLI 命令、flag、环境变量名零改动；安装路径示例（`~/.semantica` 等）原样。

**Validation**:
- [ ] 所有命令与 flag 与英文版逐字符一致
- [ ] frontmatter 合规

### T020: 翻译 docs/zh/storage-backends.md

**要点**: 后端名称（SQLite/PostgreSQL/Neo4j 等）与连接串示例保留；配置表逐行翻译描述列；性能/兼容性说明忠实原文，不添不减。

**Validation**:
- [ ] 后端配置表行数与英文版一致
- [ ] 连接串示例未改动

### T021: 翻译 docs/zh/explorer-setup.md

**要点**: npm/Node 命令保留；端口、URL 示例原样；UI 上的英文按钮名可括注中文（如 Dashboard（仪表盘）），首次出现标注即可。

**Validation**:
- [ ] 命令与端口配置未改动
- [ ] UI 术语括注风格统一

### T022: 编写 docs/zh/changelog.md 指路页 + WP05 自检

**要点**:
1. 指路页不是翻译：正文约 3-5 行——说明 changelog 持续更新、为保证时效不提供译文，附英文原页链接
2. frontmatter 四字段照常，但 `source_version` 填 `native`（同 WP01 README 的自建页处理），正文注明"指路页，非上游译文"
3. WP05 自检：zh_status 五个条目状态合规（四篇翻译 fresh；changelog.md 为自建页，按 zh_status 对 missing/invalid source_version 的处理可能显示 stale——**在完成备注记录实际输出并说明原因**，这不是缺陷）

**Validation**:
- [ ] changelog.md 为指路页形态（≤10 行正文）
- [ ] 四篇翻译 zh_status 全 fresh
- [ ] docs_check 无因本 WP 新增的失败

## Branch Strategy

- Planning branch: `feat/docs-zh-translation`
- Final merge target: `feat/docs-zh-translation`
- Execution happens in the lane worktree allocated from `lanes.json` after finalize-tasks; commit into your lane branch as instructed by the implement action.

## Definition of Done

- [ ] `docs/zh/` 下五个文件落盘
- [ ] T018–T022 全部 Validation 勾选
- [ ] 未触碰 owned_files 之外的任何文件（glossary 增补同 WP03 规则）
- [ ] 提交信息：`docs(zh): translate P1 ops pages and add changelog pointer`

## Risks

- zh_status 对 `source_version: native` 的自建页判定可能与预期不符 → 如出现，记录输出；若需要为 native 页增加豁免逻辑，报告而不擅自改 WP02 的工具（owned_files 不含 tools/i18n）
- FAQ 中上游答案本身过时 → 忠实翻译原文，过时感在完成备注指出，不代上游改内容

## Reviewer Guidance

- 确认 changelog.md 是指路页而非部分翻译
- 抽一篇（建议 storage-backends.md）对照英文版核对配置表完整性
- 检查四篇 frontmatter sha 可复现

## Activity Log

- 2026-09-01T02:34:28Z – claude – shell_pid=38784 – Assigned agent via action command
