---
work_package_id: WP07
title: 词表工作区与全局清扫（VocabularyWorkspace · primitives · 残留扫描）
dependencies:
- WP06
requirement_refs:
- FR-006
- FR-010
tracker_refs: []
planning_base_branch: feature/explorer-i18n-p2
merge_target_branch: feature/explorer-i18n-p2
branch_strategy: Planning artifacts for this mission were generated on feature/explorer-i18n-p2. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feature/explorer-i18n-p2 unless the human explicitly redirects the landing branch.
subtasks:
- T028
- T029
- T030
agent: claude
history:
- timestamp: '2026-09-02T00:00:00Z'
  action: created
  agent: claude
agent_profile: frontend-freddy
authoritative_surface: explorer/src/workspaces/VocabularyWorkspace/
create_intent:
- explorer/src/i18n/locales/en.json
- explorer/src/i18n/locales/zh.json
execution_mode: code_change
owned_files:
- explorer/src/workspaces/VocabularyWorkspace/**
- explorer/src/ui/primitives.tsx
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile

```
/ad-hoc-profile-load frontend-freddy
```

不可用时：TypeScript strict + React 19 函数组件 + react-i18next `useTranslation` 模式实施。

## Objective

SKOS 词表工作区五个文件（共约 487 行）文案抽取为 `vocabulary.*` 键段；`ui/primitives.tsx` 用户可见英文默认值清扫；全站残留英文兜底扫描并把结果记入 Execution Notes。本 WP 是全部抽取工作（WP01~06）之后的收口清扫（plan IC-05 排序约束）。

## Context（实现前必读）

- **全部为函数组件**，用 `useTranslation()` 的 `t`；键类型化、抽取与 locales 同步。
- **新键纯增量**：既有键 + WP01~06 新增段零改动。
- **primitives 修改边界（C-001）**：`ui/primitives.tsx` **仅限文案默认值抽取**（如按钮默认文字、空态默认提示）——不改组件 API、不改样式逻辑、不加 props。若默认值实为各调用方传入（组件自身无硬编码英文），则零改动并记录核查结论。
- **e2e/单测零耦合**，保持 DOM 结构与 role/aria 不变。

## 键空间规划（本 WP 新增段）

`vocabulary.*`。

**Ownership rationale（out-of-map edit）**：同 WP01——串行链保护。

## Implementation Guidance

### T028 — VocabularyWorkspace 五文件抽取 → `vocabulary.*`

`workspaces/VocabularyWorkspace/`（VocabularyWorkspace.tsx 69 行、Sidebar.tsx 112 行、ConceptTree.tsx 96 行、PropertyPanel.tsx 116 行、ImportDropzone.tsx 94 行）：

- 工作区标题、侧栏标题、区块标题。
- ConceptTree：树框架文案（展开/折叠提示、空态）；**概念节点标签是数据不译**。
- PropertyPanel：属性行的框架标签（标签/定义/同义词等字段名）；**属性值是数据**。
- ImportDropzone：拖放提示、选择按钮、导入结果框架文案；**支持格式串不译**。
- 空态、加载态、fetch 失败走 apiError（如有 fetch）。

### T029 — primitives 文案默认值清扫

`ui/primitives.tsx`：

- 先核查：grep 文件内全部字符串字面量，区分「用户可见默认文案」与「className/样式值/内部标识」。
- 仅把用户可见英文默认值改为键引用（组件内 `useTranslation` + `t('common.xxx')` 或 `vocabulary.*` 视语义归段；若通用则用既有 `common.*` 段）。
- 若核查结论是无硬编码英文——零改动，在 Execution Notes 记录核查范围与结论。

### T030 — 全局残留英文扫描

- 扫描范围：`explorer/src/workspaces/` 全目录 + `explorer/src/ui/` + `explorer/src/App.tsx`（对照确认 P0/P1 面无回归）。
- 方法：`grep -rn '>[A-Z][a-z]\+ ' --include='*.tsx'` 粗筛 JSX 文本节点 + 抽查 `placeholder="`、`title="`、`aria-label="`，逐项判定：
  - 数据值/日志串/标准名 → 豁免，逐项列明理由；
  - 真实残留 → 属于本 WP owned_files 内的直接补抽；**属于 GraphWorkspace（P1 面）的属于 P1 回归**——保持最小改动修复并在 Execution Notes 单独记录（IC-05 风险条款）；属于其他 WP 已完成文件的，同样补抽并记录。
- 扫描结果（豁免清单 + 修复清单）完整记入 Execution Notes，供 WP08 终扫对照。

### 抽取纪律（全程适用，与 WP01 相同）

1. 逐区块：改 `t()` + locales 同步 + 心算英文不变。
2. aria/title/placeholder/alt 全算文案。
3. 插值语法，禁拼接。
4. glossary 术语；拿不准登记。
5. 日志串不抽；不越 owned_files。

## Validation

- [ ] `npm run build` 绿
- [ ] `npm run lint` 零增量（基线 74）
- [ ] `?lang=zh` 走查词表工作区：框架全中文、概念标签/属性值保持原样
- [ ] `?lang=en` 对比改造前逐字一致
- [ ] T030 扫描结果已记入 Execution Notes

## Risks

- primitives 是共享组件——改动会波及全部调用方，故边界锁死为"文案默认值"；任何超出（新 props、行为变更）立即停止并上报。
- 残留扫描误报率高（className、样式 token 都含英文）——以 JSX 文本节点与用户可见属性为准，不追内部标识。

## Reviewer Guidance

- 抽查词表 3-5 个键：en 逐字、zh 术语。
- 确认 primitives 改动仅文案默认值（git diff 无 API/样式变更）。
- 确认 Execution Notes 含完整豁免/修复清单。

## Activity Log

- 2026-09-02T00:00:00Z – claude – created
