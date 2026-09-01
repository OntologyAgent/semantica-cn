---
work_package_id: WP02
title: GraphWorkspace 主体文案抽取（工具栏/搜索/图例/HUD）
dependencies:
- WP01
requirement_refs:
- FR-001
- FR-002
- FR-006
- FR-007
- NFR-001
tracker_refs: []
planning_base_branch: feature/explorer-i18n-p1
merge_target_branch: feature/explorer-i18n-p1
branch_strategy: Planning artifacts for this mission were generated on feature/explorer-i18n-p1. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feature/explorer-i18n-p1 unless the human explicitly redirects the landing branch.
subtasks:
- T004
- T005
- T006
- T007
- T008
agent: "claude"
shell_pid: "83974"
history:
- timestamp: '2026-09-02T00:00:00Z'
  action: created
  agent: claude
agent_profile: frontend-freddy
authoritative_surface: explorer/src/workspaces/GraphWorkspace/GraphWorkspace.tsx
create_intent:
- explorer/src/i18n/locales/en.json
- explorer/src/i18n/locales/zh.json
execution_mode: code_change
owned_files:
- explorer/src/workspaces/GraphWorkspace/GraphWorkspace.tsx
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile

```
/ad-hoc-profile-load frontend-freddy
```

不可用时：TypeScript strict + React 19 函数组件 + react-i18next `useTranslation` 模式实施。

## Objective

把 `explorer/src/workspaces/GraphWorkspace/GraphWorkspace.tsx`（约 3400 行的主文件，粗估 95 处界面文案）的全部用户可见英文接入 i18n：工具栏、搜索栏、图例固定枚举、HUD/预测/路径面板、时间轴入口等。中文用户打开探索工作区，本文件范围内 0 处英文残留（数据值豁免）。

## Context（实现前必读）

- **组件形态**：`export function GraphWorkspace(...)` 在 L1281 起，全函数组件、70 处 hooks——用 `useTranslation()` 的 `t`。本文件无类组件。
- **模块级常量**（导入时求值，够不着 `t()`）：
  - `ENTITY_VISUAL_KEY`（L165 起）：图例固定枚举数组 `{ shape, label }`——T006 迁移对象。
  - `COMPACT_TOOLBAR_CLUSTER_IDS`、`STRUCTURAL_DISTANCE_MAX_HOPS` 等：结构常量，**不动**。
  - `HUD_CSS`（L468 起）：CSS 模板串，**不动**（除非内嵌 content 文案，确认后处理）。
- **P0 模式先例**：`App.tsx` 的 `navItems` 是"结构留模块常量 + label 改 i18n 键引用 + 渲染时 `t(key)` 解析"——本文件同款。
- **e2e 锚点**：`tests/deterministicExplorerRendering.e2e.ts` L102 `getByRole("button", { name: "Zoom In" })`。**"Zoom In" 的 en 键值必须逐字等于原文案**，锚点才不破。
- **t() 类型化**：键经 `CustomTypeOptions` 全类型化，`t('graph.xxx')` 引用不存在的键 = tsc 报错。**每个抽取区块与 locales 键增补必须同步提交**（同一 WP 内连续完成）。
- **401 接入依赖**：`import { describeResponseError } from '../../i18n/apiError'`（WP01 产物，已合入）。

## 键空间规划（本 WP 新增段）

`graph.toolbar.*`、`graph.search.*`、`graph.legend.*`、`graph.hud.*`、`graph.prediction.*`、`graph.path.*`、`graph.errors.*`（消费 WP01 的键）。

**Ownership rationale（out-of-map edit）**：locales 增补随抽取同步进行，本 WP `owned_files` 仅含组件文件——共享资源文件由依赖链串行保护（WP02→WP03→WP04→WP05），无并行碰撞。

## Implementation Guidance

### T004 — 工具栏抽取 → `graph.toolbar.*`

GraphWorkspace 的工具栏分簇（CAMERA/LAYOUT/ANALYSIS/UTILITY，见 `COMPACT_TOOLBAR_CLUSTER_IDS` 相关渲染代码）：

- 分组标签：Camera/Camera & view/Layout/Analysis/Utility 等 → `graph.toolbar.group.camera` 等。
- 动作按钮：Zoom In / Zoom Out / Fit to view（或 Fit）/ Center、布局类（如 Re-run layout / Freeze）、Effects、Neighbors、Temporal、Run（分析）、Reset、Fullscreen、Export（以文件内实际文案为准，逐个登记）。
- 每键 en 值 = **原文逐字**（含大小写与标点；`Zoom In` 尤其严格）。
- 按钮 `title`/`aria-label` 同步抽取（无障碍文案同属界面文案）。
- 工具栏按钮数组若在 `useMemo(..., [])` 内定义 label 字面量——把数组结构留在 memo，label 改为键名，渲染处 `t(item.labelKey)`；或把数组构造改为函数内 `useMemo([t])`。两种皆可，选对现有结构侵入小的。

### T005 — 搜索栏抽取 → `graph.search.*`

- placeholder（L420 附近 `"Search command, node, or concept"`）→ `graph.search.placeholder`。
- 建议列表空态/上限提示、搜索执行错误提示、键盘导航 aria 文案。
- T008 顺带接入：搜索 fetch 失败（L1781 `/api/graph/search`、L331 建议请求）的错误提示改走 `describeResponseError(response)` → `t(view.wrapperKey)` 渲染包装文案；`view.detail` 非空时以小字展示 `t('graph.errors.detailPrefix') + ': ' + view.detail`。建议请求（L331）失败当前静默 `catch`——保持静默，不为建议框加错误 UI（行为不变原则）。

### T006 — 图例固定枚举迁移 → `graph.legend.*`

`ENTITY_VISUAL_KEY`（L165）：

```ts
// before
const ENTITY_VISUAL_KEY = [ { shape: "biomolecule", label: "Biomolecule" }, ... ]
// after（结构留常量，label 换键名）
const ENTITY_VISUAL_KEY = [ { shape: "biomolecule", labelKey: "graph.legend.biomolecule" }, ... ]
```

- 渲染图例处 `t(item.labelKey)`。字段改名 `label → labelKey` 时全文件搜引用点一并更新（含 graphTheme 联动处若有）。
- 枚举清单以文件实际为准（Biomolecule/Condition/Compound/Process/Community/Other 等）。en 值=原文。
- **数据值红线**：节点/边 label、实体类型缩写（ORG/PERSON/PRODUCT/DATE/CONCEPT 等来自图数据）绝不进资源、不包 `t()`（C-006/FR-007）。图例中若混有数据驱动段（如按数据聚合的类型 chips），那段不动。
- 图例框架文案（标题 Legend / 显示数量 / 折叠提示等）→ `graph.legend.title` 等。

### T007 — 剩余主体文案 → `graph.hud.*` / `graph.prediction.*` / `graph.path.*` 等

- HUD 浮层文案、距离/热力提示（`STRUCTURAL_DISTANCE_MAX_HOPS` 相关 UI 文案）。
- 预测/enrich 卡片（L1805 `/api/enrich/links` 结果渲染）：标题、置信度标签、空态、失败提示。
- 路径/邻域面板入口、时间轴入口按钮、底栏连接/统计提示（以文件实际为准）。
- 纯日志串（`console.error` 等）**不抽**——不是界面文案。
- T008 顺带接入：预测失败（L1820）当前仅 `console.error`——保持（无 UI 不加）。

### 抽取纪律（全程适用）

1. 逐区块推进（工具栏 → 搜索 → 图例 → HUD），每区块：组件改 `t()` + locales 两侧同步加键 + 心算核对英文渲染不变。
2. `aria-label`、`title`、`placeholder`、`alt` 全算界面文案。
3. 模板串（含变量插值）用 i18next 插值 `t('key', { count })`，禁止字符串拼接翻译。
4. zh 译文遵循 `docs/zh/glossary.md`：图例枚举无冻结词条时取直白中文（如 Biomolecule→生物分子），拿不准保留英文并在完成说明中登记。
5. 不改其他文件（GraphCanvas/Overlay/Inspector/插件归 WP03/WP04）。

## Validation

- [ ] `npm run build` 绿（键同构 + 类型化 t 键全部存在）
- [ ] `npm run test:deterministic-e2e` 全绿——"Zoom In" 锚点不改自破
- [ ] `npm run lint` 零增量
- [ ] `?lang=zh` 手动过一遍工作区：本文件范围文案全中文、数据值保持原文
- [ ] `?lang=en` 对比改造前：可见文案逐字一致

## Risks

- 文件大，漏抽难免——完成后 `grep -n '>[A-Z][a-z]\+ ' GraphWorkspace.tsx` 复扫残留，剩余项逐个判断（数据值/日志串豁免，其余补抽）。
- `useMemo` 依赖数组遗漏 `t` 会导致语言切换不刷新（React Compiler 通常兜底，但显式 memo 需自查）——改完 memo 的文件段重点核对。

## Reviewer Guidance

- 抽查 5 个键：en 值与改造前原文逐字一致；zh 术语符合 glossary。
- 确认 `ENTITY_VISUAL_KEY` 字段改名后无引用遗漏（tsc 会兜底）。
- 确认数据值未进 locales（抽查 graph.* 键值无 ORG/PERSON 等数据枚举）。

## Activity Log

- 2026-09-01T17:01:36Z – claude – shell_pid=68463 – Assigned agent via action command
- 2026-09-01T17:27:40Z – claude – shell_pid=68463 – GraphWorkspace.tsx full extraction: toolbar/search/legend/HUD/distance/edge/dock ~120 keys; en verbatim 44/44 mechanical check; build+lint(0 delta)+deterministic-e2e green; search error wired to describeResponseError (wrapper t() + detail verbatim); TranslationKey union for constants, wrapperKey cast at consumption (apiError.ts owned by WP01)
- 2026-09-01T17:27:45Z – claude – shell_pid=83974 – Started review via action command
- 2026-09-01T17:28:24Z – user – shell_pid=83974 – Review passed: en values verbatim (44/44 mechanical diff check); FR-007 data-value red line clean (no ORG/PERSON/bundleKind enums in locales); frozen surfaces untouched (e2e 4-line change is WP01's); 41 useMemo dep arrays include t; anti-pattern checklist 1-8 PASS; build + lint(74=baseline) + deterministic-e2e green
