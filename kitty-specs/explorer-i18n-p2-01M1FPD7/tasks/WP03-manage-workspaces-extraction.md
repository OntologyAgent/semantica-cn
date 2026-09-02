---
work_package_id: WP03
title: 管理工作区三页签抽取（PROV-O 谱系 · KG 概览 · 本体概要）
dependencies:
- WP02
requirement_refs:
- FR-004
- FR-006
- FR-010
tracker_refs: []
planning_base_branch: feature/explorer-i18n-p2
merge_target_branch: feature/explorer-i18n-p2
branch_strategy: Planning artifacts for this mission were generated on feature/explorer-i18n-p2. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feature/explorer-i18n-p2 unless the human explicitly redirects the landing branch.
subtasks:
- T010
- T011
- T012
- T013
agent: claude
history:
- timestamp: '2026-09-02T00:00:00Z'
  action: created
  agent: claude
agent_profile: frontend-freddy
authoritative_surface: explorer/src/workspaces/ManageWorkspace/KGOverviewTab.tsx
create_intent:
- explorer/src/i18n/locales/en.json
- explorer/src/i18n/locales/zh.json
execution_mode: code_change
owned_files:
- explorer/src/workspaces/LineageWorkspace/**
- explorer/src/workspaces/ManageWorkspace/**
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile

```
/ad-hoc-profile-load frontend-freddy
```

不可用时：TypeScript strict + React 19 函数组件 + react-i18next `useTranslation` 模式实施。

## Objective

把管理工作区三个页签（PROV-O 谱系 177 行、KG 概览 291 行、本体概要 346 行，共约 1105 行，含 LineageWorkspace 其他文件若有文案）的全部用户可见英文接入 i18n，产出 `lineage.*` / `kgOverview.*` / `ontologySummary.*` 三个键段。

## Context（实现前必读）

- **全部为函数组件**，用 `useTranslation()` 的 `t`；键类型化、抽取与 locales 同步。
- **新键纯增量**：既有键（414 + WP01/02 新增段）零改动。
- **错误提示**：fetch 失败接入既有 apiError，复用 `graph.errors.*` 包装。
- **标准名**：PROV-O、KG、Ontology Hub 按术语表保留英文（C-004）。
- **e2e/单测零耦合**，保持 DOM 结构与 role/aria 不变。

## 键空间规划（本 WP 新增段）

`lineage.*`、`kgOverview.*`、`ontologySummary.*`。

**Ownership rationale（out-of-map edit）**：同 WP01——串行链保护。

## Implementation Guidance

### T010 — PROV-O 谱系抽取 → `lineage.*`

`workspaces/LineageWorkspace/LineageDiagram.tsx`（177 行；目录内其他文件如有文案一并处理）：

- 标题（"PROV-O Lineage Viewer" 同位——PROV-O 保留，Viewer 部分入键）、说明文字。
- Enter Node ID 输入框 placeholder、Trace 按钮、Export JSON / Export MD 按钮。
- 谱系图空态、加载态、"未找到节点"提示。
- 节点/边上的 **PROV-O 类型值与实体名是数据不译**；图内深度/跳数提示等框架文案入键。

### T011 — KG 概览抽取 → `kgOverview.*`

`workspaces/ManageWorkspace/KGOverviewTab.tsx`（291 行）：

- 统计卡：NODES / EDGES / DENSITY 等卡片标签入键（数字本身是数据）。
- 类型分布：区块标题、TOP CONNECTED NODES 标题入键；**分布条目的类型值（ORG/DATE/part_of 等来自图数据）不译**——截图实证的红线项。
- Refresh 按钮、刷新时间提示。
- 空态/加载态；fetch 失败走 apiError。

### T012 — 本体概要抽取 → `ontologySummary.*`

`workspaces/ManageWorkspace/OntologySummaryTab.tsx`（346 行）：

- 区块标题（类/属性/关系统计的框架标签）、表格列头。
- **本体 URI、类/属性名称是数据不译**。
- 展开收起控件、空态、加载态。

### T013 — 键段写入 en/zh + 键同构校验

- 三段键写入 en/zh；`npm run build` 校验。

### 抽取纪律（全程适用，与 WP01 相同）

1. 逐区块：改 `t()` + locales 同步 + 心算英文不变。
2. aria/title/placeholder/alt 全算文案。
3. 插值语法，禁拼接。
4. glossary 术语；拿不准登记。
5. 日志串不抽；不越 owned_files。

## Validation

- [ ] `npm run build` 绿
- [ ] `npm run lint` 零增量（基线 74）
- [ ] `?lang=zh` 走查三页签：框架全中文、ORG/DATE/part_of 等类型值保持原样
- [ ] `?lang=en` 对比改造前逐字一致
- [ ] grep 复扫残留并逐项判断

## Risks

- 统计卡标签（NODES/EDGES）译不译的边界——它们是界面标签（固定显示文案），入键翻译；卡片上的**数字**是数据。
- 类型分布条目混排风险——只动框架标题与列头，分布条目行整行不动。

## Reviewer Guidance

- 抽查 5 个键：en 逐字、zh 术语。
- 确认 ORG/DATE/part_of 未出现在 locales 键值。
- 确认 PROV-O 在 zh 译文中保留英文。

## Activity Log

- 2026-09-02T00:00:00Z – claude – created
