---
work_package_id: WP04
title: P0 门面翻译·第二批（concepts/architecture/modules/choose-your-module）
dependencies:
- WP01
- WP02
requirement_refs:
- FR-001
- FR-002
- FR-003
- FR-011
tracker_refs: []
planning_base_branch: feat/docs-zh-translation
merge_target_branch: feat/docs-zh-translation
branch_strategy: Planning artifacts for this mission were generated on feat/docs-zh-translation. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/docs-zh-translation unless the human explicitly redirects the landing branch.
subtasks:
- T014
- T015
- T016
- T017
agent: "claude"
shell_pid: "19871"
history:
- timestamp: '2026-08-31T23:50:32Z'
  action: created
  agent: claude
agent_profile: curator-carla
authoritative_surface: docs/zh/
create_intent:
- docs/zh/concepts.md
- docs/zh/architecture.md
- docs/zh/modules.md
- docs/zh/choose-your-module.md
execution_mode: code_change
owned_files:
- docs/zh/concepts.md
- docs/zh/architecture.md
- docs/zh/modules.md
- docs/zh/choose-your-module.md
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile

Before reading anything else, load your assigned agent profile:

```
/ad-hoc-profile-load curator-carla
```

If that command is unavailable, proceed as a bilingual technical documentation curator with extra care for diagrams and tables.

## Objective

翻译 P0 门面后四篇：`docs/concepts.md`、`docs/architecture.md`、`docs/modules.md`、`docs/choose-your-module.md` → `docs/zh/`。本批难点：architecture 含 Mermaid 图，modules/choose-your-module 含 27 模块大表——图与表的处理策略见下。前置：WP01、WP02 已就位。可与 WP03、WP05 并行（owned_files 无交集）。

## Context

- 翻译规范：`docs/zh/README.md`；术语：`docs/zh/glossary.md`
- Mermaid 策略（规范已定）：图内**自然语言节点标签可译**（保持 Mermaid 语法有效），代码类标签（类名、模块名、函数名）保留英文
- 表格策略：列结构不变；模块名、API 名等标识符列保留英文，描述列翻译
- 通用流程（frontmatter 四字段、代码块、JSX、链接回落、术语查询）与 WP03 相同，先读 WP03 的"通用流程"再开工

## Subtask Guidance

### T014: 翻译 docs/zh/concepts.md

**要点**: 概念密集页。每个核心概念首次出现用"中文(English)"格式，之后用中文；概念间引用要通篇一致（如"实体消解"不能一处一处混用）。

**Validation**:
- [ ] 核心术语译法全篇一致，与 glossary 相符
- [ ] frontmatter 合规

### T015: 翻译 docs/zh/architecture.md（含 Mermaid 图标签策略）

**要点**:
1. Mermaid 代码块：先确认英文版每张图语法；译节点标签时保持引号、括号、箭头结构不动；**译后逐图用肉眼检查语法**（Mermaid 对中文标签中的特殊字符敏感，必要时给标签加双引号）
2. 分层描述文字与图内标签译法统一
3. 图下方如有"图例/说明"文字照常翻译

**Validation**:
- [ ] Mermaid 块数量与英文版一致，每块语法有效（结构未被破坏）
- [ ] 图内代码类标签保留英文

### T016: 翻译 docs/zh/modules.md 与 choose-your-module.md（27 模块表）

**要点**:
1. 27 模块表：模块名列（如 `semantic_extract`）**绝对不动**；"功能描述"列翻译；"适用场景"列翻译
2. choose-your-module 的决策树/选择指引：问题与选项译成自然中文问句，指向的模块名保留
3. 两篇表格行数、行序与英文版一致——不允许增删或重排行

**Validation**:
- [ ] 模块表行数与英文版逐行对应，模块名列零改动
- [ ] 决策指引的分支逻辑与英文版等价

### T017: WP04 自检

**Steps**: 同 WP03 T013——zh_status 四篇 fresh、docs_check 无新增失败、内链点验、JSX 平衡；额外加一项：Mermaid 块逐图目检。

**Validation**:
- [ ] zh_status 显示四篇 fresh
- [ ] docs_check 无新增失败
- [ ] 无死链；Mermaid 图结构完好

## Branch Strategy

- Planning branch: `feat/docs-zh-translation`
- Final merge target: `feat/docs-zh-translation`
- Execution happens in the lane worktree allocated from `lanes.json` after finalize-tasks; commit into your lane branch as instructed by the implement action.

## Definition of Done

- [ ] `docs/zh/` 下四个文件落盘，frontmatter 合规
- [ ] T014–T017 全部 Validation 勾选
- [ ] 未触碰 owned_files 之外的任何文件（glossary 增补同 WP03 规则：写入完成备注）
- [ ] 提交信息：`docs(zh): translate P0 pages (concepts, architecture, modules, choose-your-module)`

## Risks

- Mermaid 中文标签触发解析错误 → 标签一律加双引号兜底
- 27 模块表体量大，易漏行 → 翻完用行数核对一次
- 与 WP03 并行，两批译文的术语表述可能漂移 → 双方都以 glossary 为准；发现冲突记入完成备注，由收尾 WP 统一

## Reviewer Guidance

- 打开 architecture.md 译文，确认每张 Mermaid 图节点标签结构未被改坏
- 抽 5 行模块表与英文版逐列比对
- 核对四篇 frontmatter sha 可复现

## Activity Log

- 2026-09-01T02:16:15Z – claude – shell_pid=19871 – Assigned agent via action command
