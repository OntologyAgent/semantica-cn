---
work_package_id: WP01
title: 术语表与翻译规范（Foundation）
dependencies: []
requirement_refs:
- C-002
- FR-004
- FR-005
- NFR-003
tracker_refs: []
planning_base_branch: feat/docs-zh-translation
merge_target_branch: feat/docs-zh-translation
branch_strategy: Planning artifacts for this mission were generated on feat/docs-zh-translation. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/docs-zh-translation unless the human explicitly redirects the landing branch.
subtasks:
- T001
- T002
- T003
- T004
agent: "claude"
shell_pid: "6715"
history:
- timestamp: '2026-08-31T23:50:32Z'
  action: created
  agent: claude
agent_profile: curator-carla
authoritative_surface: docs/zh/
create_intent:
- docs/zh/README.md
- docs/zh/glossary.md
execution_mode: code_change
owned_files:
- docs/zh/README.md
- docs/zh/glossary.md
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile

Before reading anything else, load your assigned agent profile:

```
/ad-hoc-profile-load curator-carla
```

If that command is unavailable, proceed with your best judgment as a knowledge-base curator: terminology discipline, single-source-of-truth hygiene, and documentation consistency.

## Objective

创建 `docs/zh/glossary.md`（术语表）与 `docs/zh/README.md`（翻译规范）。这两个文件是后续全部翻译工作包（WP03/04/05）的前置依赖：术语表冻结译名，README 固化规则。**本 WP 不翻译任何上游文档正文**——只建地基。

## Context

- 仓库：Semantica fork，主英文文档在 `docs/`（Mintlify，83 篇 md）
- 上游 glossary 原文在 `docs/glossary.md`——先读它，术语表要与上游条目对齐后再加自建术语
- 术语决策已冻结的 10 条见 spec（kitty-specs/docs-zh-translation-01M1D2MJ/spec.md 的 Domain Language 表）；允许补充，不允许更改已定译名
- 零侵入约束（C-001）：不改任何上游文件；两个新文件都在 `docs/zh/` 下
- 中文表达规范：短句、避免欧式中文、术语首次出现标英文

## Subtask Guidance

### T001: 建立 docs/zh/glossary.md 术语表

**Purpose**: 全部译文的术语唯一权威源。

**Steps**:
1. 读上游 `docs/glossary.md`，列出其全部术语条目
2. 创建 `docs/zh/glossary.md`，frontmatter 四字段齐全：

   ```yaml
   ---
   title: 术语表
   description: Semantica 中文文档术语对照表——全部译文的译名权威源
   source: glossary.md
   source_version: "<运行 git rev-parse HEAD:docs/glossary.md 取得>"
   ---
   ```

3. 正文含两张表：
   - **核心术语表**（本 Mission 权威）：spec Domain Language 的 10 条（知识图谱/上下文图/决策智能/溯源/本体/实体消解/三元组/摄取/推理引擎/冲突检测），列：英文 | 中文 | 备注
   - **上游词条翻译**：上游 glossary.md 的条目逐条给出中文译法；拿不准的 zh 列直接填英文原词并在备注注明"待定名"
4. 表格列名用中文（英文原词 | 中文译名 | 备注）

**Validation**:
- [ ] `git rev-parse HEAD:docs/glossary.md` 输出与 frontmatter 一致
- [ ] spec 的 10 条核心术语全部在表内且译名逐字一致

### T002: 编写 docs/zh/README.md 翻译规范

**Purpose**: 贡献者（人或 Claude）翻译任何页面前的必读规则；也是项目 Skill 的单一事实源。

**Steps**:
1. frontmatter 四字段（source: README.md——注意：上游 docs/ 无 README.md，此文件为纯自建，source 填 `README.md` 并在正文注明"本页为自建规范，非上游译文"，source_version 填 `native`）
2. 正文必须覆盖（与 spec FR-005 对应）：
   - **分层表**：P0/P1/P2 内容清单、P3 与 changelog 不翻
   - **frontmatter 约定**：四字段含义、source_version 的取得命令（`git rev-parse HEAD:docs/<file>`）
   - **代码不翻原则**：标识符、CLI、配置键保留；代码块内注释可译
   - **JSX 保留原则**：`<Card>`/`<Tabs>` 等组件结构原样，只译标签内文本
   - **链接回落规则**：目标页有中文版链 `./xxx.md`，否则链英文原页（`../xxx.md` 或上游相对路径）
   - **术语规则**：先查 glossary.md，缺条目先补表再翻，拿不准保留英文
   - **Mermaid 图策略**：图内节点标签可译（保持语法有效），代码类标签保留
   - **验收命令**：`python docs_check.py` 与 `python tools/i18n/zh_status.py`
3. 全文中文，短句，总长控制在 150 行内

**Validation**:
- [ ] 上述 8 个规则块齐备
- [ ] 所有命令示例在仓库当前状态可运行

### T003: 交叉核对术语覆盖

**Purpose**: 保证 glossary 无遗漏、无冲突。

**Steps**:
1. 读 spec 的 Domain Language 表与 T001 产出的 glossary，逐行比对
2. 扫一遍 P0 九篇英文原文的标题/小节标题中的高频概念词（如 Embedding、Chunking、Hybrid Search），按需补入术语表
3. 补条目时同步更新 spec Domain Language？——**不要改 spec**（规划产物已提交）；新术语只进 glossary，备注"规划后补充"

**Validation**:
- [ ] spec 10 条 ↔ glossary 逐字一致
- [ ] 新补条目有备注来源

### T004: 局部验收

**Purpose**: 地基文件通过上游检查器，不把破坏传给后续 WP。

**Steps**:
1. `python docs_check.py` 全量运行，确认这两个文件不引入任何 FAIL（其他既有失败可忽略，记录基线）
2. 手查 glossary/README 内部链接可达（`./` 相对路径在本目录内应自洽）

**Validation**:
- [ ] docs_check 输出中无因 docs/zh/README.md 或 docs/zh/glossary.md 引发的 FAIL
- [ ] 基线失败清单记录在 WP 完成备注中

## Branch Strategy

- Planning branch: `feat/docs-zh-translation`
- Final merge target: `feat/docs-zh-translation`
- Execution happens in the lane worktree allocated from `lanes.json` after finalize-tasks; commit into your lane branch as instructed by the implement action.

## Definition of Done

- [ ] `docs/zh/glossary.md` 与 `docs/zh/README.md` 落盘，frontmatter 合规
- [ ] T001–T004 全部 Validation 勾选
- [ ] 未触碰 owned_files 之外的任何文件
- [ ] 提交信息：`docs(zh): add glossary and translation guide`

## Risks

- 术语定名争议 → C-002 兜底：拿不准保留英文原词
- README 规则与后续 WP 实际操作冲突 → 实现中发现的规则缺陷回写 README 并在本 WP 备注，不静默绕过

## Reviewer Guidance

- 对照 spec 的 Domain Language 表逐字核对 10 条核心译名
- 确认 README 的 8 个规则块与 contracts（zh-status-cli.md）的退出码/参数描述一致
- 确认 frontmatter source_version 命令真实可跑

## Activity Log

- 2026-09-01T01:43:41Z – claude – shell_pid=82409 – Assigned agent via action command
- 2026-09-01T01:52:10Z – claude – shell_pid=82409 – glossary+README 落盘；docs_check 9/10 pass，唯一 FAIL 为 Mintlify export 因本机 Node 26 过新（基线，与改动无关）；链接自洽
- 2026-09-01T02:04:33Z – claude – shell_pid=6715 – Started review via action command
