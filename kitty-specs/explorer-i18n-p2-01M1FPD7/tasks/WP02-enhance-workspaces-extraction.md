---
work_package_id: WP02
title: 增强工作区四页签抽取（导入导出 · 差异合并 · 实体消解 · 注册表）
dependencies:
- WP01
requirement_refs:
- FR-003
- FR-006
- FR-010
tracker_refs: []
planning_base_branch: feature/explorer-i18n-p2
merge_target_branch: feature/explorer-i18n-p2
branch_strategy: Planning artifacts for this mission were generated on feature/explorer-i18n-p2. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feature/explorer-i18n-p2 unless the human explicitly redirects the landing branch.
subtasks:
- T005
- T006
- T007
- T008
- T009
agent: claude
history:
- timestamp: '2026-09-02T00:00:00Z'
  action: created
  agent: claude
agent_profile: frontend-freddy
authoritative_surface: explorer/src/workspaces/EnrichWorkspace/EntityResolutionTab.tsx
create_intent:
- explorer/src/i18n/locales/en.json
- explorer/src/i18n/locales/zh.json
execution_mode: code_change
owned_files:
- explorer/src/workspaces/ImportExportWorkspace/**
- explorer/src/workspaces/DiffMergeWorkspace/**
- explorer/src/workspaces/EnrichWorkspace/**
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile

```
/ad-hoc-profile-load frontend-freddy
```

不可用时：TypeScript strict + React 19 函数组件 + react-i18next `useTranslation` 模式实施。

## Objective

把增强工作区四个页签（导入导出 196 行、差异合并 121 行、实体消解 454 行、注册表 284 行，共约 1055 行）的全部用户可见英文接入 i18n，产出 `importExport.*` / `diffMerge.*` / `entityResolution.*` / `registry.*` 四个键段。

## Context（实现前必读）

- **全部为函数组件**，用 `useTranslation()` 的 `t`。
- **t() 类型化**：键引用不存在 = tsc 报错，抽取与 locales 增补同步完成。
- **新键为纯增量**：既有 414 键（含 WP01 刚新增的 reasoning/sparql/decision 段）零改动。
- **错误提示**：fetch 失败接入既有 `explorer/src/i18n/apiError.ts`（`describeResponseError` / `describeApiError`），包装文案复用 `graph.errors.*`，后端 detail 原文保留。
- **e2e/单测**：零文案耦合（plan R4 已核查），保持 DOM 结构与 role/aria 不变。

## 键空间规划（本 WP 新增段）

`importExport.*`、`diffMerge.*`、`entityResolution.*`、`registry.*`。

**Ownership rationale（out-of-map edit）**：同 WP01——locales 由串行依赖链保护，本 WP 顺序写入无碰撞。

## Implementation Guidance

### T005 — 导入导出抽取 → `importExport.*`

`workspaces/ImportExportWorkspace/ImportExportWorkspace.tsx`（196 行）：

- 拖放区：提示文案（"Drop files here" 同位）、点击选择按钮、拖放态提示。**支持的格式串（.json/.csv 等）是数据值不译**。
- 格式说明文字（框架解释性文案）入键。
- Upload to Graph、Export Graph Snapshot、Download Export 等按钮。
- What's included 折叠区标题与内部说明。
- FORMAT 标签、导出格式枚举（**JSON/CSV 切换按钮属界面文案**——用户点击对象，入键）。
- 导入结果摘要/错误提示（框架部分）；fetch 失败走 apiError。

### T006 — 差异与合并抽取 → `diffMerge.*`

`workspaces/DiffMergeWorkspace/DiffMergeWorkspace.tsx`（121 行）：

- 页签标题、比较/合并按钮、操作说明。
- diff 视图框架文案（侧标题、变更类型标签 added/removed 的显示标签若有）。
- **diff 内容行**是数据不译。
- 空态与加载态。

### T007 — 实体消解抽取 → `entityResolution.*`

`workspaces/EnrichWorkspace/EntityResolutionTab.tsx`（454 行，本 WP 最大）：

- 页签内标题、说明、运行按钮、阈值/策略控件标签。
- 候选组列表框架文案：匹配分数标签、合并/忽略按钮、批量操作。
- 结果面板：消解结果统计的框架文案；**实体名/URI 是数据不译**。
- 空态（无候选时）、运行中状态、fetch 失败走 apiError。
- 文件大，逐区块推进（头部控件 → 候选列表 → 结果面板）。

### T008 — 注册表抽取 → `registry.*`

`workspaces/EnrichWorkspace/RegistryTab.tsx`（284 行）：

- 页签标题、过滤/搜索控件、表格列头（框架文案）。
- 注册/取消注册按钮、状态标签。
- **审计日志的 summary 是调用时拼好的英文数据串（存进状态，非渲染时求值）——按 Non-goal 豁免不译**；若某条实现成本低（如渲染端有结构化字段可拼）可随本期做，否则在 Execution Notes 记录豁免决定（plan R3 条款）。
- 时间戳/来源等数据列保持原样。

### T009 — 键段写入 en/zh + 键同构校验

- 四段键写入 en/zh 两文件；en 值 = 原文逐字；zh 译文遵循 `docs/zh/glossary.md`（实体消解为冻结词条）。
- `npm run build` 校验键同构。

### 抽取纪律（全程适用，与 WP01 相同）

1. 逐区块：组件改 `t()` + locales 同步加键 + 心算英文不变。
2. `aria-label`/`title`/`placeholder`/`alt` 全算界面文案。
3. 插值用 i18next 插值语法，禁拼接。
4. 术语遵循 glossary；拿不准保留英文并登记。
5. 日志串不抽；不越 owned_files。

## Validation

- [ ] `npm run build` 绿
- [ ] `npm run lint` 零增量（基线 74）
- [ ] `?lang=zh` 走查四个页签：框架全中文、格式串/diff 内容/实体名保持原样
- [ ] `?lang=en` 对比改造前逐字一致
- [ ] grep 复扫残留并逐项判断

## Risks

- EntityResolutionTab 454 行为体量峰值，漏抽风险最高——分三区块推进，完成后复扫。
- 注册表 summary 豁免 vs 顺手翻译的判定——拿不准就豁免并记录（宁可少做不越界）。

## Reviewer Guidance

- 抽查 5 个键：en 逐字、zh 术语。
- 确认 .json/.csv 格式串、实体 URI 未进 locales。
- 确认审计 summary 的处理与 Execution Notes 记录一致。

## Activity Log

- 2026-09-02T00:00:00Z – claude – created
