---
work_package_id: WP01
title: 分析工作区抽取（推理引擎 · SPARQL · 决策）
dependencies: []
requirement_refs:
- FR-001
- FR-002
- FR-006
- FR-010
tracker_refs: []
planning_base_branch: feature/explorer-i18n-p2
merge_target_branch: feature/explorer-i18n-p2
branch_strategy: Planning artifacts for this mission were generated on feature/explorer-i18n-p2. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feature/explorer-i18n-p2 unless the human explicitly redirects the landing branch.
subtasks:
- T001
- T002
- T003
- T004
agent: claude
history:
- timestamp: '2026-09-02T00:00:00Z'
  action: created
  agent: claude
agent_profile: frontend-freddy
authoritative_surface: explorer/src/workspaces/ReasoningWorkspace.tsx
create_intent:
- explorer/src/i18n/locales/en.json
- explorer/src/i18n/locales/zh.json
execution_mode: code_change
owned_files:
- explorer/src/workspaces/ReasoningWorkspace.tsx
- explorer/src/workspaces/SparqlWorkspace/**
- explorer/src/workspaces/DecisionWorkspace/**
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile

```
/ad-hoc-profile-load frontend-freddy
```

不可用时：TypeScript strict + React 19 函数组件 + react-i18next `useTranslation` 模式实施。

## Objective

把三个分析工作区（推理引擎 243 行、SPARQL 查询 271 行、决策 279 行，共约 793 行）的全部用户可见英文接入 i18n，产出 `reasoning.*` / `sparql.*` / `decision.*` 三个键段。中文用户打开分析工作区，本 WP 范围内 0 处英文框架残留（数据值豁免）。

## Context（实现前必读）

- **全部为函数组件**（`export function ...` / `export default function`），用 `useTranslation()` 的 `t`。
- **t() 类型化**：键经 P0 `CustomTypeOptions` 全类型化，`t('reasoning.xxx')` 引用不存在的键 = tsc 报错。**每个抽取区块与 locales 键增补必须同步完成**（同一 WP 内连续完成）。
- **既有键基准**：`explorer/src/i18n/locales/en.json` 顶层 `translation` 下已有 414 个扁平键（`graph.toolbar.zoomIn` 式）。P2 新键为**纯增量**，既有键值零改动（INV-4）。
- **错误提示**：fetch 失败提示接入既有 `explorer/src/i18n/apiError.ts`（P1 产物，`describeResponseError` / `describeApiError`），包装文案复用 `graph.errors.*` 键，后端 detail 原文保留展示。不新增错误包装基础设施。
- **e2e 锚点**：`tests/deterministicExplorerRendering.e2e.ts` 仅锚定 `Semantica Explorer` 与 `Zoom In`（均不在本 WP 范围）。本 WP 保持 DOM 结构与 role/aria 不变即可，测试文件零改动。

## 键空间规划（本 WP 新增段）

`reasoning.*`、`sparql.*`、`decision.*`——扁平浅两级（`reasoning.runButton` 式）。

**Ownership rationale（out-of-map edit）**：locales 增补随抽取同步进行，本 WP `owned_files` 仅含组件文件——共享资源文件由依赖链串行保护（WP01→…→WP08），无并行碰撞。

## Implementation Guidance

### T001 — 推理引擎页抽取 → `reasoning.*`

`workspaces/ReasoningWorkspace.tsx`（243 行）：

- 页面标题、说明文字、分组标题。
- 快捷模板区：模板**按钮标签**入键；模板的 facts/rules **语法示例内容**（`fact: (...)`、`rule: ... => ...` 之类）是代码示例/数据值，**不译**（FR-010）。
- 事实/规则编辑区：textarea 的 placeholder、区块标签、添加/删除按钮。
- 写入推断（write-inferred）开关及其说明文案。
- Run Reasoning 按钮与运行中状态提示。
- 结果面板：标题、空态（"Ready to reason" 同位文案）、推断条目的框架文案（类型标签/置信度等）；推断**内容本身**是数据不译。
- fetch 失败提示走 apiError 包装。

### T002 — SPARQL 页抽取 → `sparql.*`

`workspaces/SparqlWorkspace/SparqlWorkspace.tsx`（271 行）：

- 编辑器框架文案：编辑区标签、模板选择器标签、清空/格式化按钮（若有）。
- 查询模板下拉/列表的**框架标签**入键；SPARQL 模板查询**内容**（SELECT/WHERE 语句）不译。
- Run/Execute 按钮与执行状态提示。
- 结果表：列头框架文案（行数、耗时提示等）、空结果态。
- 错误提示：查询失败经 apiError 包装；SPARQL 错误消息正文（后端返回）保留原文。
- SPARQL 关键字（SELECT/WHERE/FILTER）永远保持原样。

### T003 — 决策页抽取 → `decision.*`

`workspaces/DecisionWorkspace/DecisionWorkspace.tsx`（279 行）：

- 列表标题、过滤框 placeholder、排序/过滤控件标签。
- 空态文案（"No decisions" / "No decision selected" 同位）。
- 详情面板：决策链、因果上下文、先例匹配等**框架标题与说明**；决策记录的**内容字段值**（决策描述、状态枚举值、时间戳）是数据不译。
- 刷新/选择按钮、加载态提示。
- fetch 失败提示走 apiError 包装。

### T004 — 键段写入 en/zh + 键同构校验

- 本 WP 全部键写入 `explorer/src/i18n/locales/en.json` 与 `zh.json`（`translation` 对象下按字母序插入；en 值 = 原文逐字，zh 译文遵循 `docs/zh/glossary.md`）。
- `zh.translation satisfies typeof en.translation` 自动保证键同构——`npm run build` 即校验。

### 抽取纪律（全程适用，与 P1 相同）

1. 逐区块推进，每区块：组件改 `t()` + locales 两侧同步加键 + 心算核对英文渲染不变。
2. `aria-label`、`title`、`placeholder`、`alt` 全算界面文案。
3. 含变量插值的模板串用 i18next 插值 `t('key', { count })`，禁止字符串拼接翻译。
4. 术语遵循 `docs/zh/glossary.md`（推理/决策智能/溯源/本体等冻结词条）；拿不准的保留英文并在完成说明登记。
5. 纯日志串（`console.error` 等）不抽。
6. 不改本 WP 范围外的任何组件文件。

## Validation

- [ ] `npm run build` 绿（键同构 + 类型化 t 键全部存在）
- [ ] `npm run lint` 零增量（基线 74：57 errors + 17 warnings）
- [ ] `?lang=zh` 手动过三个分析页：框架文案全中文、facts/rules 示例与 SPARQL 模板保持原样
- [ ] `?lang=en` 对比改造前：可见文案逐字一致
- [ ] 完成后 `grep -n '>[A-Z][a-z]\+ ' <file>` 复扫残留，逐项判断（数据值/日志串豁免，其余补抽）

## Risks

- 推理页快捷模板与 SPARQL 模板的"代码示例 vs 框架文案"边界——判定标准：用户会照着改/复制的原样内容=数据不译；引导用户操作的标签=文案要译。
- `useMemo` 依赖数组遗漏 `t` 会导致语言切换不刷新——改过 memo 的文件段重点核对。

## Reviewer Guidance

- 抽查每页 3-5 个键：en 值与改造前原文逐字一致；zh 术语符合 glossary。
- 确认 facts/rules 示例、SPARQL 模板内容未进 locales。
- 确认既有 414 键零改动（`git diff` locales 只见新增行）。

## Activity Log

- 2026-09-02T00:00:00Z – claude – created
