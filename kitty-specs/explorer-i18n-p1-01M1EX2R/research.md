# Research: Explorer 中文界面 P1（探索工作区）

Date: 2026-09-02 · 无 NEEDS CLARIFICATION——四项范围决策已在 specify 阶段经用户确认（见 spec.md 决策记录）。

## R1 — 组件形态与抽取模式

**Decision**: 函数组件用 `useTranslation()`，模块级常量保持"结构常量 + label 为 i18n 键"模式，渲染时解析。
**Rationale**: 代码侦查确认 `GraphWorkspace.tsx` 为单文件约 3400 行的函数组件（`export function GraphWorkspace` L1281），70 处 hooks，无类组件——`useTranslation` 全面适用；模块常量（`ENTITY_VISUAL_KEY` L165、`COMPACT_TOOLBAR_CLUSTER_IDS` L164 等）在导入时求值够不着 `t()`，须沿用 P0 `navItems` 先例。本目录未发现类组件，无需 `i18next.t()` 直调路径。
**Alternatives considered**: ① 全部文案迁入独立常量文件——放弃，侵入更大且违背"结构留常量"；② 可变全局 locale 变量——放弃，违反 C-003（React Compiler 下不可靠）。

## R2 — 图例枚举归属

**Decision**: 前端固定映射的图例标签（Biomolecule/Condition/Compound/Process/Community/Other 等）进翻译资源；节点/边携带的数据值不翻。
**Rationale**: 侦查确认图例为前端固定数组（`GraphWorkspace.tsx` L166 起 `ENTITY_VISUAL_KEY`，`graphTheme.ts` L620 同款），属界面文案；数据值的豁免边界已写入 FR-007/C-006。
**Alternatives considered**: 数据驱动图例（从图数据聚合类型生成）——放弃，改语义属上游行为变更。

## R3 — 401 错误包装点

**Decision**: 新增 `explorer/src/i18n/apiError.ts` 纯函数（响应 → 中文包装文案 + detail 原文），仅在 GraphWorkspace 错误渲染处接入。
**Rationale**: 前端 fetch 无集中 API 层（侦查：fetch 散布于各 workspace 组件，GraphWorkspace 内 5 处——graph search L331/L1781、temporal L1461/L1557、enrich L1805；加载错误经 session hook 的 `graphLoadError` 汇入）。后端 401 detail 见 `semantica/explorer/dependencies.py` L70-71。包装函数不改后端（C-002），detail 原文保留。
**Alternatives considered**: ① 全局 fetch 拦截/monkey-patch——放弃，隐式行为且影响所有工作区越 C-001 界；② 逐 fetch 点内联包装——放弃，重复代码多，纯函数 + 渲染点接入最小。

## R4 — e2e 锚点依赖

**Decision**: e2e 的 `page.goto(BASE_URL)` 改为 `?lang=en` 预置；定位器不变。
**Rationale**: `tests/deterministicExplorerRendering.e2e.ts` 两处文案锚点：`/Open Semantica Explorer/`（L87，App 层，P0 已 i18n，英文键值即原文）与 `"Zoom In"`（L102，GraphWorkspace 工具栏）。当前 e2e 无语言预置、默认 en 恰好安全，但属隐性依赖——显式 `?lang=en` 锚定（P0 检测链第 1 优先级，零成本）。单测四套（graphSceneState.display / temporalLifecycle / markdownContentViewer / deterministicExplorerRendering.test）经 grep 不断言工作区文案，预期零改动。
**Alternatives considered**: 改用 data-testid 定位——本期不需要（英文键值不变），留给未来批次按需采用。

## R5 — 键空间与规模

**Decision**: 新增键统一挂 `graph.*` 命名空间，英文键值 = 原文英文；收尾刷新 `__meta.source_version`。
**Rationale**: 沿用 P0 键组织（`nav.*`/`welcome.*`/`shell.*`…）与 `ui_zh_status.py` 追踪机制（源基准 = en.json HEAD blob sha）。估算约 290 条来自 P0 期走查，实际以抽取清单为准（spec Assumptions 允许越界补键）。
**Alternatives considered**: 按子组件再分命名空间（`graph.timeline.*` 等）——采用浅两级即可，避免键名过度设计。
