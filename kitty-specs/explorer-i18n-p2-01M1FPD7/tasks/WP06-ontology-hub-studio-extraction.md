---
work_package_id: WP06
title: Ontology Hub 工作室与评审抽取（SHACL Studio · Proposal Review · SKOS Manager）
dependencies:
- WP05
requirement_refs:
- FR-005
- FR-006
- FR-010
tracker_refs: []
planning_base_branch: feature/explorer-i18n-p2
merge_target_branch: feature/explorer-i18n-p2
branch_strategy: Planning artifacts for this mission were generated on feature/explorer-i18n-p2. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feature/explorer-i18n-p2 unless the human explicitly redirects the landing branch.
subtasks:
- T024
- T025
- T026
- T027
agent: claude
history:
- timestamp: '2026-09-02T00:00:00Z'
  action: created
  agent: claude
agent_profile: frontend-freddy
authoritative_surface: explorer/src/workspaces/OntologyWorkspace/SKOSVocabularyManager.tsx
create_intent:
- explorer/src/i18n/locales/en.json
- explorer/src/i18n/locales/zh.json
execution_mode: code_change
owned_files:
- explorer/src/workspaces/OntologyWorkspace/ShaclStudio.tsx
- explorer/src/workspaces/OntologyWorkspace/ProposalReview.tsx
- explorer/src/workspaces/OntologyWorkspace/SKOSVocabularyManager.tsx
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile

```
/ad-hoc-profile-load frontend-freddy
```

不可用时：TypeScript strict + React 19 函数组件 + react-i18next `useTranslation` 模式实施。

## Objective

把 Ontology Hub 剩余三个文件（ShaclStudio 363 行、ProposalReview 429 行、SKOSVocabularyManager 696 行，共约 1488 行）的全部用户可见英文接入 i18n，产出 `ontologyHub.shacl/proposal/skos.*` 键段。本 WP 完成后 Hub 11 文件全部收口。

## Context（实现前必读）

- **全部为函数组件**，用 `useTranslation()` 的 `t`；键类型化、抽取与 locales 同步。
- **新键纯增量**：既有键 + WP01~05 新增段零改动。
- **键段前缀**沿用 WP04 确立的 `ontologyHub.` 一级前缀。
- **错误提示**：fetch 失败接入既有 apiError，复用 `graph.errors.*` 包装。
- **标准名与数据值**：SHACL/SKOS/OWL 保留英文；SHACL shapes 数据、约束示例、提案 diff 内容、SKOS 概念条目是数据不译。
- **e2e/单测零耦合**，保持 DOM 结构与 role/aria 不变。

## 键空间规划（本 WP 新增段）

`ontologyHub.shacl.*`、`ontologyHub.proposal.*`、`ontologyHub.skos.*`。

**Ownership rationale（out-of-map edit）**：同 WP01——串行链保护。

## Implementation Guidance

### T024 — ShaclStudio 抽取 → `ontologyHub.shacl.*`

`workspaces/OntologyWorkspace/ShaclStudio.tsx`（363 行）：

- 工作室标题、说明文字、生成/验证/导出按钮。
- shapes 编辑区框架标签、验证结果面板标题。
- **SHACL shapes 数据、约束定义文本（sh:property 等语法内容）、验证消息正文是数据/代码不译**。
- 验证通过/失败状态标签、空态、fetch 失败走 apiError。

### T025 — ProposalReview 抽取 → `ontologyHub.proposal.*`

`workspaces/OntologyWorkspace/ProposalReview.tsx`（429 行）：

- 提案页签标题、过滤控件、提案列表列头。
- 评审操作：批准/拒绝/评论按钮、评审意见输入标签与 placeholder。
- 提案状态标签（pending/approved 等的**显示标签**）入键。
- **提案内容、diff 行、提案描述正文是数据不译**（描述若为后端数据字段保持原样）。
- 空态、操作成功/失败提示走 apiError。

### T026 — SKOSVocabularyManager 抽取 → `ontologyHub.skos.*`

`workspaces/OntologyWorkspace/SKOSVocabularyManager.tsx`（696 行，本 WP 最大）：

- 管理器标题、说明、导入/导出按钮、新建概念方案按钮。
- 概念方案列表：列头、条目操作按钮、层级导航框架文案。
- **SKOS 概念标签、URI、定义正文是数据不译**。
- 导入结果摘要框架文案、空态、fetch 失败走 apiError。
- 696 行——按区块推进：头部 → 方案列表 → 详情面板。

### T027 — 键段写入 en/zh + 键同构校验

- 三段键写入 en/zh；`npm run build` 校验。

### 抽取纪律（全程适用，与 WP01 相同）

1. 逐区块：改 `t()` + locales 同步 + 心算英文不变。
2. aria/title/placeholder/alt 全算文案。
3. 插值语法，禁拼接。
4. glossary 术语（SKOS 词表相关词条查 glossary；无冻结词条取直白中文并登记）。
5. 日志串不抽；不越 owned_files。

## Validation

- [ ] `npm run build` 绿
- [ ] `npm run lint` 零增量（基线 74）
- [ ] `?lang=zh` 走查三文件：框架全中文、shapes 数据/提案 diff/概念条目保持原样
- [ ] `?lang=en` 对比改造前逐字一致
- [ ] grep 复扫残留并逐项判断

## Risks

- SKOSVocabularyManager 体量大——三区块推进，每块完成即复扫。
- 提案状态枚举的显示标签与枚举值同字面（如直接显示 "approved"）——与 WP04 过滤器同款判定：纯值保持，含标签语义的入键；拿不准保持并登记。

## Reviewer Guidance

- 每文件抽查 3-5 个键：en 逐字、zh 术语。
- 确认 SHACL shapes、提案 diff、SKOS 概念标签未进 locales。
- 确认 Hub 11 文件至此全部覆盖（对照 WP04/05/06 owned_files 并集）。

## Activity Log

- 2026-09-02T00:00:00Z – claude – created
