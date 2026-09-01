---
work_package_id: WP03
title: P0 门面翻译·第一批（index/quickstart/getting-started/installation）
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
- T010
- T011
- T012
- T013
agent: "claude"
shell_pid: "17870"
history:
- timestamp: '2026-08-31T23:50:32Z'
  action: created
  agent: claude
agent_profile: curator-carla
authoritative_surface: docs/zh/
create_intent:
- docs/zh/index.md
- docs/zh/quickstart.md
- docs/zh/getting-started.md
- docs/zh/installation.md
execution_mode: code_change
owned_files:
- docs/zh/index.md
- docs/zh/quickstart.md
- docs/zh/getting-started.md
- docs/zh/installation.md
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile

Before reading anything else, load your assigned agent profile:

```
/ad-hoc-profile-load curator-carla
```

If that command is unavailable, proceed as a bilingual technical documentation curator: fidelity to structure, natural Chinese, terminology discipline.

## Objective

翻译 P0 门面前四篇：`docs/index.md`、`docs/quickstart.md`、`docs/getting-started.md`、`docs/installation.md` → `docs/zh/` 同名文件。这四篇构成中文用户"落地页 → 跑起来"的完整阅读路径，质量要求最高。前置：WP01 的术语表与翻译规范、WP02 的 zh_status.py 已就位。

## Context

- 英文源在 `docs/`（Mintlify，含 JSX 组件）；译文放 `docs/zh/`，**同目录扁平结构，1:1 镜像**
- 翻译规范全文见 `docs/zh/README.md`（WP01 产出）——开工前先读它；术语查 `docs/zh/glossary.md`
- 中文表达：短句、避免欧式中文、术语首次出现标英文（如"检索增强生成(RAG)"），后续可直接用中文
- 零侵入：只新建 `docs/zh/` 下的四个文件，不改任何上游文件

## Subtask Guidance

每个翻译子任务遵循同一套动作，先列通用流程，再列各篇要点：

**通用流程（每篇必做）**:
1. 通读英文原文，理解结构后再动笔
2. frontmatter 四字段：
   ```yaml
   ---
   title: <中文标题>
   description: <中文一句话描述>
   source: <英文文件名，如 quickstart.md>
   source_version: <git rev-parse HEAD:docs/<英文文件名> 的输出，40 位 sha>
   ---
   ```
3. 结构 1:1：标题层级、列表、表格、代码块、JSX 组件与英文版同构
4. 代码块内只译注释；命令、标识符、URL、配置键原样
5. `<Card>`/`<Tabs>`/`<Steps>` 等 JSX 标签结构原样，只译标签内文本；标签属性值（如图标名）不动
6. 内链回落：目标页有 `docs/zh/` 中文版 → 链 `./xxx.md`；没有 → 保留英文原页链接路径
7. 术语先查 glossary；缺条目先补术语表（在完成备注记录补了什么）再翻；拿不准保留英文

### T010: 翻译 docs/zh/index.md

**要点**: 落地页。突出价值主张的表达要符合中文营销文案习惯，但不过度改写；`<Card>` 网格的每张卡标题/描述对译。

**Validation**:
- [ ] frontmatter source_version 与 `git rev-parse HEAD:docs/index.md` 一致
- [ ] JSX 标签数量与英文版一致

### T011: 翻译 docs/zh/quickstart.md

**要点**: 安装与首次运行命令**逐字符保留**；步骤编号与顺序不变；预期输出示例不译。

**Validation**:
- [ ] 所有 shell 命令与英文版逐字符一致（diff 代码块核对）
- [ ] `source_version` 正确

### T012: 翻译 docs/zh/getting-started.md 与 installation.md

**要点**: getting-started 概念铺垫多，注意术语一致性；installation 的平台分支结构（macOS/Linux/Windows/pip/源码）原样保留，一个分支都不能漏。

**Validation**:
- [ ] installation.md 的安装方式小节数量与英文版一致
- [ ] 两篇 frontmatter 合规

### T013: WP03 自检

**Purpose**: 不把问题传给下游。

**Steps**:
1. `python tools/i18n/zh_status.py`：四篇全部 fresh
2. `python docs_check.py`：无因这四篇新增的 FAIL（对照执行前的基线输出）
3. 内链逐个点验：`./` 链接目标存在于 docs/zh 或回落路径存在于英文 docs
4. JSX 平衡：每篇 `<Tag>` 与 `</Tag>` 数量配对（可用 `grep -c` 粗查）

**Validation**:
- [ ] zh_status 显示四篇 fresh
- [ ] docs_check 无新增失败
- [ ] 无死链

## Branch Strategy

- Planning branch: `feat/docs-zh-translation`
- Final merge target: `feat/docs-zh-translation`
- Execution happens in the lane worktree allocated from `lanes.json` after finalize-tasks; commit into your lane branch as instructed by the implement action.

## Definition of Done

- [ ] `docs/zh/` 下四个文件落盘，frontmatter 合规
- [ ] T010–T013 全部 Validation 勾选
- [ ] 未触碰 owned_files 之外的任何文件（补术语表除外——那是 WP01 owned file，若需补充，在完成备注中列出增补行供 WP01 owner 合并）
- [ ] 提交信息：`docs(zh): translate P0 pages (index, quickstart, getting-started, installation)`

## Risks

- 与 WP01 并行时术语表可能同时被改 → 补条目不直接改 glossary，写入完成备注，由收尾 WP 统一合并
- 英文原文含上游尚未修复的死链 → 回落规则下保留原样并记录，不顺手"修"上游链接

## Reviewer Guidance

- 抽一段代码块与英文版 diff，确认命令未被动过
- 核对四篇 frontmatter 的 sha 均可用 `git rev-parse` 复现
- 读一篇译文全篇，检查是否有翻译腔与术语不一致

## Activity Log

- 2026-09-01T02:06:35Z – claude – shell_pid=9623 – Assigned agent via action command
- 2026-09-01T02:14:00Z – claude – shell_pid=9623 – 四篇译文落盘：zh_status 全 fresh（4/4 新页）；内链零死链（本批互链用 ./，未翻页回落 ../英文）；JSX 与英文源逐组件配平；docs_check 不新增失败（唯一 FAIL 仍为 Node 26 基线）
- 2026-09-01T02:14:13Z – claude – shell_pid=17870 – Started review via action command
