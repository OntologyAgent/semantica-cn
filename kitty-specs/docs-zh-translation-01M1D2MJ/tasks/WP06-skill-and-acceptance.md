---
work_package_id: WP06
title: Skill 封装与全局验收（Polish）
dependencies:
- WP01
- WP02
- WP03
- WP04
- WP05
requirement_refs:
- C-001
- C-004
- FR-005
- FR-008
- NFR-004
tracker_refs: []
planning_base_branch: feat/docs-zh-translation
merge_target_branch: feat/docs-zh-translation
branch_strategy: feature-branch
subtasks:
- T023
- T024
- T025
- T026
agent: claude
history:
- timestamp: '2026-08-31T23:50:32Z'
  action: created
  agent: claude
agent_profile: generic-agent
authoritative_surface: .claude/skills/docs-zh-translation/
create_intent: []
execution_mode: code_change
owned_files:
- .claude/skills/docs-zh-translation/**
- CLAUDE.md
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile

Before reading anything else, load your assigned agent profile:

```
/ad-hoc-profile-load generic-agent
```

If that command is unavailable, proceed as a generalist finisher: this WP is the closing gate — it packages the reusable Skill, verifies zero-invasion, runs global acceptance, and updates CLAUDE.md.

## Objective

收尾门。四件事：把翻译流程固化为可反复调用的项目 Skill（`.claude/skills/docs-zh-translation/SKILL.md`）；验证零侵入承诺；跑全局验收；把 docs/zh 体系与 Skill 入口写进 CLAUDE.md。必须在 WP01–WP05 全部合并到本分支后执行。

## Context

- Skill 设计原则（plan 已定）：**流程编排层**——SKILL.md 只写"翻译一页的步骤 + 验收命令"，规范细节一律链接 `docs/zh/README.md`，**不复制规范文本**（防双源漂移）
- 本仓 CLAUDE.md 是用户维护的中文项目指南，已有"与上游同步"与"常用命令"节——T026 是**增补**，不重写
- 零侵入验证命令：`git diff upstream/main --name-only --diff-filter=M`——期望输出为空或仅含 init 脚手架声明的文件；任何上游文件被修改即违规

## Subtask Guidance

### T023: 编写 .claude/skills/docs-zh-translation/SKILL.md

**Steps**:
1. frontmatter：
   ```yaml
   ---
   name: docs-zh-translation
   description: 翻译或更新 Semantica 中文文档（docs/zh/）。当用户要求翻译某篇文档、同步过期译文、或补充术语时使用。
   ---
   ```
2. 正文结构（编排层，目标 ≤120 行）：
   - **触发场景**：翻新页 / 同步 stale / 补术语 三种入口
   - **翻译新页流程**：读 `docs/zh/README.md` 规范 → 查 glossary → 建 `docs/zh/<同名>.md`（frontmatter 四字段，sha 用 `git rev-parse HEAD:docs/<file>`）→ 自检两命令
   - **同步 stale 流程**：`git fetch upstream && git merge upstream/main` → `python tools/i18n/zh_status.py` → 逐篇重译 stale 页并刷新 sha
   - **验收命令**：`python docs_check.py` + `python tools/i18n/zh_status.py`（必须给出）
   - **边界**：P3 页与 changelog 不翻；不改 docs.json/docs_check.py/.github；规范细节以 README.md 为准（附相对链接）
3. 语言：正文中文；命令与路径原文

**Validation**:
- [ ] SKILL.md 存在且 frontmatter 含 name/description
- [ ] 正文不含从 README.md 复制的规范长文（抽查：规范细节处应为链接而非转述全文）
- [ ] 流程中的每条命令在当前仓库状态可运行

### T024: 零侵入验证与 init 伴生产物规整

**Steps**:
1. 运行 `git diff upstream/main --name-only --diff-filter=M`，逐个核对出现的路径是否均为 init 脚手架声明文件（.kittify/、.claudeignore、.gitattributes、.gitignore、README.md）
2. 发现非脚手架的上游文件被修改 → **立即报告，不得静默继续**；列出文件与改动性质
3. 确认 `README.md` 的语言切换行（`**English** | [中文](README.zh-CN.md)`）仍在；README.zh-CN.md 头部的 source commit 记录仍指向当前 HEAD 的祖先

**Validation**:
- [ ] diff-filter=M 输出仅含脚手架文件（清单记入完成备注）
- [ ] docs/、semantica/、tests/、pyproject.toml 等上游路径零改动

### T025: 全局验收

**Steps**:
1. `python docs_check.py` 全绿（对照 WP 各自基线：无任何因 docs/zh 引发的失败）
2. `python tools/i18n/zh_status.py`：13 个译文条目（4+4+4 翻译页 + glossary + README + changelog 指路页）状态符合各自预期（翻译页 fresh；自建页按 T022 记录的口径）
3. quickstart.md（mission 产物）五步走查：以贡献者视角按步骤 1-5 实际走一遍，确认命令、路径、预期输出全部成立
4. 术语一致性抽检：任选 3 个 glossary 核心术语，grep 全部 docs/zh/ 译文，确认译法统一

**Validation**:
- [ ] docs_check 全绿
- [ ] zh_status 输出符合预期并记录
- [ ] 五步走查每步有实际执行证据（命令输出摘录入完成备注）
- [ ] 术语抽检通过

### T026: 更新 CLAUDE.md

**Steps**:
1. 在"工程结构"节补 `docs/zh/`（中文文档镜像 + glossary/README 规范）与 `tools/i18n/zh_status.py`
2. 在"常用命令"节补：
   ```bash
   python tools/i18n/zh_status.py   # 中文译文过期状态
   ```
3. 新增一小节"中文文档翻译"（≤10 行）：Skill 入口 `.claude/skills/docs-zh-translation`、规范单一事实源 `docs/zh/README.md`、上游同步后先跑 zh_status
4. **只增不改**：不重排既有小节、不改既有命令描述

**Validation**:
- [ ] CLAUDE.md 三处增补就位
- [ ] `git diff CLAUDE.md` 仅含新增行（无删除/改写既有行）

## Branch Strategy

- Planning branch: `feat/docs-zh-translation`
- Final merge target: `feat/docs-zh-translation`
- Execution happens in the lane worktree allocated from `lanes.json` after finalize-tasks; commit into your lane branch as instructed by the implement action.

## Definition of Done

- [ ] SKILL.md 落盘且为纯编排层
- [ ] T023–T026 全部 Validation 勾选
- [ ] 零侵入验证通过
- [ ] 提交信息：`feat(i18n): add docs-zh-translation skill and finalize acceptance`

## Risks

- T025 发现前面 WP 的残留问题 → 属预期：本 WP 是收尾门，发现问题回退给对应 WP 修复，不在本 WP 内跨 owned_files 修补
- SKILL.md 与 README.md 边界把握不准 → 判断标准：删掉 SKILL.md 后，仅凭 README.md 能否完成一次翻译？能，则 SKILL.md 没有多余规范文本

## Reviewer Guidance

- 对照 plan.md 的 IC-05 检查 Skill 设计原则落实情况
- 亲自跑一遍 `git diff upstream/main --name-only --diff-filter=M` 与 zh_status，不信完成备注
- 检查 CLAUDE.md 的 diff 是否纯新增
