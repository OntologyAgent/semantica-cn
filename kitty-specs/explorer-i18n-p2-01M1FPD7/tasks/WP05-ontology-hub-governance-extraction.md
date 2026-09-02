---
work_package_id: WP05
title: Ontology Hub 治理页签抽取（Editor · Alignments · Versions · Health）
dependencies:
- WP04
requirement_refs:
- FR-005
- FR-006
- FR-010
tracker_refs: []
planning_base_branch: feature/explorer-i18n-p2
merge_target_branch: feature/explorer-i18n-p2
branch_strategy: Planning artifacts for this mission were generated on feature/explorer-i18n-p2. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feature/explorer-i18n-p2 unless the human explicitly redirects the landing branch.
subtasks:
- T019
- T020
- T021
- T022
- T023
agent: claude
history:
- timestamp: '2026-09-02T00:00:00Z'
  action: created
  agent: claude
agent_profile: frontend-freddy
authoritative_surface: explorer/src/workspaces/OntologyWorkspace/OntologyEditor.tsx
create_intent:
- explorer/src/i18n/locales/en.json
- explorer/src/i18n/locales/zh.json
execution_mode: code_change
owned_files:
- explorer/src/workspaces/OntologyWorkspace/OntologyEditor.tsx
- explorer/src/workspaces/OntologyWorkspace/AlignmentsTab.tsx
- explorer/src/workspaces/OntologyWorkspace/VersionsTab.tsx
- explorer/src/workspaces/OntologyWorkspace/HealthTab.tsx
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile

```
/ad-hoc-profile-load frontend-freddy
```

不可用时：TypeScript strict + React 19 函数组件 + react-i18next `useTranslation` 模式实施。

## Objective

把 Ontology Hub 四个治理页签（OntologyEditor 498 行、AlignmentsTab 437 行、VersionsTab 546 行、HealthTab 214 行，共约 1695 行）的全部用户可见英文接入 i18n，产出 `ontologyHub.editor/alignments/versions/health.*` 键段。

## Context（实现前必读）

- **全部为函数组件**，用 `useTranslation()` 的 `t`；键类型化、抽取与 locales 同步。
- **新键纯增量**：既有键 + WP01~04 新增段零改动。
- **键段前缀**沿用 WP04 确立的 `ontologyHub.` 一级前缀。
- **错误提示**：fetch 失败接入既有 apiError，复用 `graph.errors.*` 包装。
- **标准名与数据值**：OWL/SHACL/SKOS/RDF 保留英文；本体 URI、类/属性名、对齐映射条目、版本快照内容是数据不译。
- **e2e/单测零耦合**，保持 DOM 结构与 role/aria 不变。

## 键空间规划（本 WP 新增段）

`ontologyHub.editor.*`、`ontologyHub.alignments.*`、`ontologyHub.versions.*`、`ontologyHub.health.*`。

**Ownership rationale（out-of-map edit）**：同 WP01——串行链保护。

## Implementation Guidance

### T019 — OntologyEditor 抽取 → `ontologyHub.editor.*`

`workspaces/OntologyWorkspace/OntologyEditor.tsx`（498 行）：

- 编辑器框架：工具栏按钮（添加类/添加属性/删除等）、保存/取消、撤销重做（若有）。
- 表单控件标签与 placeholder、校验错误提示（**量大且重复——共用键**，如"名称不能为空"类提示建共用键）。
- 类/属性编辑面板的框架文案：域/值域/父类等标签入键；**编辑中的本体条目值是数据不译**。
- 未保存更改提示、只读态提示。

### T020 — AlignmentsTab 抽取 → `ontologyHub.alignments.*`

`workspaces/OntologyWorkspace/AlignmentsTab.tsx`（437 行）：

- 对齐页签标题、说明、创建对齐按钮、对齐类型选择标签。
- 对齐列表：表格列头、置信度标签、审批/删除按钮。
- **对齐条目内容（两侧类名、映射谓词值）是数据不译**。
- 空态、fetch 失败走 apiError。

### T021 — VersionsTab 抽取 → `ontologyHub.versions.*`

`workspaces/OntologyWorkspace/VersionsTab.tsx`（546 行）：

- 版本页签标题、创建快照按钮、快照说明文案。
- 版本列表：列头、时间戳标签、比较/回滚/下载按钮。
- diff 视图框架文案（若有）：侧标题、变更类型标签；**diff 内容行是数据**。
- 空态（尚无版本）、操作确认弹窗文案（确认/取消按钮及提示语）。

### T022 — HealthTab 抽取 → `ontologyHub.health.*`

`workspaces/OntologyWorkspace/HealthTab.tsx`（214 行）：

- 健康页签标题、检查项分组标题、重新检查按钮。
- 健康指标标签（完整性/一致性等框架文案）、通过/警告/失败**状态标签**入键。
- **检查结果的详情数据（违规条目、URI）不译**。
- 空态、检查中提示。

### T023 — 键段写入 en/zh + 键同构校验

- 四段键写入 en/zh；共用校验提示键放 `ontologyHub.editor.validation.*`；`npm run build` 校验。

### 抽取纪律（全程适用，与 WP01 相同）

1. 逐区块：改 `t()` + locales 同步 + 心算英文不变。
2. aria/title/placeholder/alt 全算文案。
3. 插值语法，禁拼接。
4. glossary 术语；拿不准登记。
5. 日志串不抽；不越 owned_files。

## Validation

- [ ] `npm run build` 绿
- [ ] `npm run lint` 零增量（基线 74）
- [ ] `?lang=zh` 走查四页签：框架全中文、本体条目/对齐内容/diff 行保持原样
- [ ] `?lang=en` 对比改造前逐字一致
- [ ] grep 复扫残留并逐项判断

## Risks

- 表单校验提示的重复抽取会造成键膨胀——先扫一遍文件收集全部校验文案，归并为共用键再写入。
- 操作确认弹窗若用 `window.confirm`（原生弹窗不可译）——保持原样并登记（不属于可译界面文案）。

## Reviewer Guidance

- 每文件抽查 3-5 个键：en 逐字、zh 术语。
- 确认对齐条目、版本快照内容未进 locales。
- 确认校验提示共用键无逐处重复定义。

## Activity Log

- 2026-09-02T00:00:00Z – claude – created
