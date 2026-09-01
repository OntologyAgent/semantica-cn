---
work_package_id: WP04
title: Inspector 与插件文案（InspectorPanel · plugins · MarkdownViewer · graphTheme）
dependencies:
- WP03
requirement_refs:
- FR-001
- FR-002
- FR-007
tracker_refs: []
planning_base_branch: feature/explorer-i18n-p1
merge_target_branch: feature/explorer-i18n-p1
branch_strategy: Planning artifacts for this mission were generated on feature/explorer-i18n-p1. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feature/explorer-i18n-p1 unless the human explicitly redirects the landing branch.
subtasks:
- T012
- T013
- T014
- T015
agent: claude
history:
- timestamp: '2026-09-02T00:00:00Z'
  action: created
  agent: claude
agent_profile: frontend-freddy
authoritative_surface: explorer/src/workspaces/GraphWorkspace/
create_intent:
- explorer/src/i18n/locales/en.json
- explorer/src/i18n/locales/zh.json
execution_mode: code_change
owned_files:
- explorer/src/workspaces/GraphWorkspace/GraphInspectorPanel.tsx
- explorer/src/workspaces/GraphWorkspace/plugins/**
- explorer/src/workspaces/GraphWorkspace/MarkdownContentViewer.tsx
- explorer/src/workspaces/GraphWorkspace/behaviors/**
- explorer/src/workspaces/GraphWorkspace/graphTheme.ts
- explorer/src/workspaces/GraphWorkspace/graphEntityShape.ts
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile

```
/ad-hoc-profile-load frontend-freddy
```

不可用时：TypeScript strict + React 19 函数组件 + react-i18next `useTranslation` 模式实施。

## Objective

抽取探索工作区剩余界面文案：Inspector 检查器面板（约 770 行、30 处）、探索效果插件两枚（约 67 处）、时态覆盖/邻域/图例插件、Markdown 查看器、`graphTheme`/`graphEntityShape` 的固定标签映射。本 WP 完成后 P1 范围抽取收口，P1 范围内界面文案全双语。

## Context

- `GraphInspectorPanel.tsx`：函数组件，属性/关系/溯源三区框架文案（标题、空态、字段标签）。`PROVENANCE_KEYS`（GraphWorkspace.tsx L137，不在本 WP 范围）只是数据键名列表——字段标签若在本文件渲染则抽。
- 插件经 plugin registry 动态加载（`loadTemporalOverlayPlugin` 等 lazy import）：`useTranslation` 基于全局 i18next 实例，lazy 组件内正常订阅 `languageChanged`——无需额外接线，但**验证**切换即时性。
- `graphTheme.ts`（L620 附近）与 `graphEntityShape.ts`：形状/颜色主题的**固定标签映射**（如 Biomolecule 等形状名、图例用展示名）——同 WP02 T006 模式：映射结构留常量、标签改键引用、渲染处翻译。**主题内部形状枚举值（如 "biomolecule"）是结构标识符，不改**。
- `behaviors/*.ts`：纯交互行为，预计零文案；确认后无改动即跳过（不要为改而改）。
- 数据值红线同前：节点/边 label、类型枚举值不进资源。

## 键空间规划（本 WP 新增段）

`graph.inspector.*`、`graph.effects.*`、`graph.temporalOverlay.*`、`graph.neighborhood.*`、`graph.markdown.*`、`graph.theme.*`；legendPlugin 若有固定枚举标签并入 WP02 已建的 `graph.legend.*` 段（同段追加，不新开段）。

**Ownership rationale（out-of-map edit）**：locales 增补随抽取同步；串行链末端（WP04→WP05）无并行碰撞。

## Implementation Guidance

### T012 — GraphInspectorPanel → `graph.inspector.*`

- 面板标题/关闭按钮、属性区（Properties）、关系区（Relationships）、溯源区（Provenance）标题与空态（"No relationships" 等）。
- 字段展示标签（confidence/source/pmid 等 PII 键对应的展示名）、复制按钮、展开/收起。
- Markdown 渲染入口文案（若引用 MarkdownContentViewer 的触发标签）。

### T013 — explorationEffects 两插件 → `graph.effects.*`

- `explorationEffectsPlugin.tsx`（约 24 处）与 `explorationEffectsPluginPhaseC.tsx`（约 43 处）：效果面板标题、开关标签、距离档位（near/mid/far → 近/中/远）、热力图/结构距离提示、应用/重置按钮、空态与错误提示。
- 两插件共用文案（如距离档位）合并同键，不重复造键。

### T014 — temporalOverlay / neighborhoodPanel / legendPlugin

- `temporalOverlayPlugin.tsx`（约 10 处）：覆盖层标题、时间点提示、快照状态文案 → `graph.temporalOverlay.*`。
- `neighborhoodPanelPlugin.tsx`（约 7 处）：面板标题、邻域范围标签、空态 → `graph.neighborhood.*`。
- `legendPlugin.tsx`（约 5 处）：图例浮层框架文案并入 `graph.legend.*`；形状标签若引用 `graphTheme` 映射，统一走 T015 的键。
- 插件 API 若要求文案从 registry 传入（非组件内渲染），在插件组件内 `t()` 后再上屏——不改 plugin registry 契约（`pluginRegistryPredicates.ts` 不动）。

### T015 — MarkdownContentViewer + graphTheme/graphEntityShape 标签

- `MarkdownContentViewer.tsx`（约 7 处）：查看器标题、关闭/展开、加载与错误提示 → `graph.markdown.*`。（既有单测 `markdownContentViewer.test.ts` 不断言英文文案——改造后跑一遍确认。）
- `graphTheme.ts`/`graphEntityShape.ts`：固定展示标签改键引用（同 WP02 T006 模式）；纯色值/形状常量不动。预计约 6 处。

### 纪律（全程适用）

- 逐文件推进，键同步落 locales 两侧；en 值逐字等于原文。
- `console.*` 日志串不抽；`import.meta.env.DEV` 调试文案（`DEBUG_GRAPH_WORKSPACE` 相关）不抽。
- 不改 GraphWorkspace.tsx / GraphCanvas / Overlay / TimelinePanel（归前序 WP，已完成合入）。

## Validation

- [ ] `npm run build` 绿；`npm run lint` 零增量
- [ ] `npm run test:plugin-registry`、`npm run test:markdown-content-viewer`（如存在对应 script，否则 node --test 相应文件）全绿
- [ ] `npm run test:deterministic-e2e` 全绿
- [ ] `?lang=zh` 打开 Inspector、效果面板、时态覆盖、邻域面板、图例、Markdown 查看器：全中文；切换语言即时刷新（lazy 组件重点验）
- [ ] `?lang=en`：与改造前逐字一致

## Risks

- 插件渲染路径多样（面板/覆盖层/HUD 注入），语言切换订阅经 registry 中转——若发现某插件切换不刷新，检查该插件是否用了非 hook 的 `i18next.t` 直调（直调不订阅；改回 `useTranslation`）。
- graphTheme 标签改键引用的引用点可能跨文件（WP02 已抽的图例若直接引用 theme 标签）——改名后 tsc 兜底，但需同步核对渲染处已用 `t()`。

## Reviewer Guidance

- 抽查 Inspector 三区各 1 键 + 效果面板距离档位 1 键：en 原文一致、zh 符合 glossary（近/中/远）。
- 确认 plugin registry 契约文件零改动。
- 确认形状枚举值（结构标识符）未被翻译。
