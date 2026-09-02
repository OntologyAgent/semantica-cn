# Research: Explorer 中文界面 P2（剩余工作区全量）

Date: 2026-09-02 · 无 NEEDS CLARIFICATION——范围决策沿用 spec.md 决策记录（用户 2026-09-02 指令"充分挖掘后，继续完成"，P0/P1 先例全部有效）。

## R1 — 抽取模式沿用

**Decision**: 函数组件用 `useTranslation()`；模块级常量保持"结构常量 + label 为 i18n 键"模式，渲染时解析；非 hook 上下文用 `i18next.t()` 直调（接受已知滞后窗口）。
**Rationale**: P1 已在同类代码形态上验证（GraphWorkspace 70 处 hooks 全用 useTranslation；P1 memo 冻结架构的滞后限制已披露可接受）。P2 目标文件侦查确认全部为函数组件（`export function`/`export default function`），无类组件。
**Alternatives considered**: 可变全局 locale——放弃，违反 C-003（React Compiler 下不可靠）。

## R2 — 数据值与界面文案边界

**Decision**: 本体 URI、节点/边类型枚举值（ORG/PERSON/part_of 等）、类别过滤器值（OWL/SKOS/INTERNAL/EXTERNAL）、文件名、SPARQL 查询模板内容、facts/rules 语法示例——不译；其周围框架文案（标签、按钮、说明、空态、错误提示）——入键翻译。
**Rationale**: 沿用 P1 FR-007/C-006 判据（"结构枚举原值不译，固定显示标签经键映射"）。截图证据：增强页 JSON/CSV 切换按钮属界面文案（用户点击对象）；KG 概览的 ORG/DATE/part_of 分布标签属数据值。
**Alternatives considered**: 无新分歧。

## R3 — 错误提示策略

**Decision**: 各工作区操作失败提示沿用既有 `apiError.ts` 包装（P1 已建），fetch 错误渲染点接入；后端 detail 原文保留。
**Rationale**: P1 已建立纯函数 + 渲染点接入模式（`describeApiError`/`describeResponseError`），P2 各工作区 fetch 点直接复用，零新增基础设施。注册表审计 summary 为调用时拼好的英文数据串（P0 已记录），按 Non-goal 豁免；若某处实现成本低可随本期做，记 Execution Notes。
**Alternatives considered**: 全局 fetch 拦截——放弃，越 C-001 界（P1 R3 同款结论）。

## R4 — 测试锚点核查

**Decision**: 预期测试文件零改动。
**Rationale**: 2026-09-02 核查 `explorer/tests/`：deterministic-e2e 仅两处文案锚点（`Semantica Explorer`、`Zoom In`，均在 P0/P1 范围且已带 `?lang=en` 预置）；四套单测（graphSceneState.display / temporalLifecycle / markdownContentViewer / pluginRegistry.temporal / graphStore.multi-edge）不断言 P2 范围文案。P2 抽取保持 DOM 结构与 role/aria 不变即可。
**Alternatives considered**: 无。

## R5 — 键空间与规模

**Decision**: 新增键沿用扁平命名，按工作区一级分段：`reasoning.*`、`sparql.*`、`decision.*`、`importExport.*`、`diffMerge.*`、`entityResolution.*`、`registry.*`、`lineage.*`、`kgOverview.*`、`ontologySummary.*`、`ontologyHub.*`、`vocabulary.*`；英文键值 = 原文英文；收尾刷新 `__meta.source_version`。
**Rationale**: P0/P1 键组织为扁平字符串键（`graph.toolbar.zoomIn` 式浅两级）；P2 键量约 P1 的 3 倍（估 850+ vs 307），按工作区分段保持可导航性。gzip 预算按 P1 实测 9.8KB/307 键线性外推约 27KB，60KB 上限留足余量（NFR-002）。
**Alternatives considered**: 单一 `workspaces.*` 前缀——放弃，嵌套过深徒增键长。

## R6 — 体量与分批

**Decision**: Ontology Workspace（11 文件约 5200 行、估约 500 键）拆分为多个工作包（按页签分组），其余工作区按目录聚合；串行链推进。
**Rationale**: P1 经验：单 WP 舒适区约 100-150 键（WP02-04 各约 100 条）。Ontology Hub 体量须 2-3 个 WP 承载，避免单 WP 过载。
**Alternatives considered**: 并行 lane——放弃，locales 两文件是共享写入面，串行链是 P1 已验证的安全模式（lane 链式 merge）。
