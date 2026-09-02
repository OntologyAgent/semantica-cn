---
work_package_id: WP04
title: Ontology Hub 主体抽取（index · Manager · Loader · Search）
dependencies:
- WP03
requirement_refs:
- FR-005
- FR-006
- FR-010
tracker_refs: []
planning_base_branch: feature/explorer-i18n-p2
merge_target_branch: feature/explorer-i18n-p2
branch_strategy: Planning artifacts for this mission were generated on feature/explorer-i18n-p2. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feature/explorer-i18n-p2 unless the human explicitly redirects the landing branch.
subtasks:
- T014
- T015
- T016
- T017
- T018
agent: "claude"
shell_pid: "97400"
history:
- timestamp: '2026-09-02T00:00:00Z'
  action: created
  agent: claude
agent_profile: frontend-freddy
authoritative_surface: explorer/src/workspaces/OntologyWorkspace/OntologyManager.tsx
create_intent:
- explorer/src/i18n/locales/en.json
- explorer/src/i18n/locales/zh.json
execution_mode: code_change
owned_files:
- explorer/src/workspaces/OntologyWorkspace/index.tsx
- explorer/src/workspaces/OntologyWorkspace/OntologyManager.tsx
- explorer/src/workspaces/OntologyWorkspace/OntologyLoader.tsx
- explorer/src/workspaces/OntologyWorkspace/OntologySearch.tsx
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile

```
/ad-hoc-profile-load frontend-freddy
```

不可用时：TypeScript strict + React 19 函数组件 + react-i18next `useTranslation` 模式实施。

## Objective

把 Ontology Hub 的四个主体文件（index 119 行、OntologyManager 930 行、OntologyLoader 913 行、OntologySearch 590 行，共约 2552 行）的全部用户可见英文接入 i18n，产出 `ontologyHub.shell/manager/loader/search.*` 键段。本 WP 是 Ontology Hub 三个 WP（WP04/05/06）中的第一个。

## Context（实现前必读）

- **全部为函数组件**，用 `useTranslation()` 的 `t`；键类型化、抽取与 locales 同步。
- **新键纯增量**：既有键 + WP01/02/03 新增段零改动。
- **Ontology Hub 键段统一前缀 `ontologyHub.`**（三 WP 共用一级前缀，二级为文件域：shell/manager/loader/search/editor/alignments/versions/health/shacl/proposal/skos）。
- **错误提示**：fetch 失败接入既有 apiError，复用 `graph.errors.*` 包装；后端 detail 原文保留。
- **标准名与数据值**：OWL、SKOS、SHACL、RDF 保留英文（C-004）；本体 URI、类别过滤枚举值（OWL/SKOS/INTERNAL/EXTERNAL 作为**过滤值本身**）不译；其周围**过滤按钮/下拉的固定标签**若与枚举值同字面（如按钮就叫 "OWL"），保持字面不译即可（en=zh=OWL，无需键）——仅在标签含解释性文字时入键。
- **e2e/单测零耦合**，保持 DOM 结构与 role/aria 不变。

## 键空间规划（本 WP 新增段）

`ontologyHub.shell.*`、`ontologyHub.manager.*`、`ontologyHub.loader.*`、`ontologyHub.search.*`。

**Ownership rationale（out-of-map edit）**：同 WP01——串行链保护。Hub 三 WP 顺序执行，键段前缀统一由本 WP 先行确立。

## Implementation Guidance

### T014 — Hub 壳层与 index 抽取 → `ontologyHub.shell.*`

`workspaces/OntologyWorkspace/index.tsx`（119 行）：

- Hub 打开/关闭框架文案、页签栏结构常量的**标签改键引用**（结构、icon、id 留常量——P0 navItems 同款模式）。
- 页签标签：Registry/Editor/Versions/Alignments/Health/SHACL Studio/Proposals/SKOS Vocabulary 等以 index 实际为准。
- 加载失败/空态壳层提示。

### T015 — OntologyManager 抽取 → `ontologyHub.manager.*`

`workspaces/OntologyWorkspace/OntologyManager.tsx`（930 行，Hub 最大文件）：

- 注册表主面板：标题、搜索框 placeholder、过滤控件标签（All/OWL/SKOS/INTERNAL/EXTERNAL 的**下拉选项标签**——与枚举值同字面的保持原样，带说明文字的入键）、Entity Search 区块标签、Load Ontology 按钮。
- 本体列表：表格列头、加载状态标签、操作按钮（加载/删除/查看）。
- 空态（"No ontologies loaded yet" 同位）、加载态、批量操作提示。
- fetch 失败走 apiError。
- 930 行文件——按区块推进：头部控件 → 过滤器 → 列表 → 详情/操作区。

### T016 — OntologyLoader 抽取 → `ontologyHub.loader.*`

`workspaces/OntologyWorkspace/OntologyLoader.tsx`（913 行）：

- 本体加载流程：URL/文件输入标签、placeholder、Load/Parse 按钮、格式选择标签。
- 加载进度/成功/失败提示（框架部分）；解析错误的**后端消息正文**保留原文。
- 预置本体列表（如有）：条目**名称是数据**；说明/操作文案入键。
- 上传说明、支持格式串（.owl/.rdf/.ttl 等）不译。

### T017 — OntologySearch 抽取 → `ontologyHub.search.*`

`workspaces/OntologyWorkspace/OntologySearch.tsx`（590 行）：

- 搜索框 placeholder、搜索按钮、范围过滤控件标签。
- 结果列表：列头、匹配类型标签、跳转/选中操作。
- 空结果态、搜索中提示。
- **搜索命中的本体条目内容是数据不译**。

### T018 — 键段写入 en/zh + 键同构校验

- 四段键写入 en/zh；`npm run build` 校验。

### 抽取纪律（全程适用，与 WP01 相同）

1. 逐区块：改 `t()` + locales 同步 + 心算英文不变。
2. aria/title/placeholder/alt 全算文案。
3. 插值语法，禁拼接。
4. glossary 术语（本体/实体消解/注册表为冻结词条）；拿不准登记。
5. 日志串不抽；不越 owned_files（Hub 其余 7 文件归 WP05/06）。

## Validation

- [ ] `npm run build` 绿
- [ ] `npm run lint` 零增量（基线 74）
- [ ] `?lang=zh` 走查 Hub 主体：壳层页签、注册表、加载器、搜索全中文；本体 URI/过滤枚举值保持原样
- [ ] `?lang=en` 对比改造前逐字一致
- [ ] grep 复扫残留并逐项判断

## Risks

- 体量峰值（2552 行、估 ~230 键）——四文件各自分区块推进，每文件完成即复扫该文件。
- Manager/Loader 内若有跨文件共享的常量标签数组，键引用模式统一走"结构留常量 + labelKey 字段"（P1 ENTITY_VISUAL_KEY 同款）。

## Reviewer Guidance

- 每文件抽查 3-5 个键：en 逐字、zh 术语。
- 确认本体 URI、.owl/.ttl 格式串未进 locales。
- 确认页签标签改动后页签 id/icon 未变（App.tsx 页签渲染依赖）。

## Activity Log

- 2026-09-02T00:00:00Z – claude – created
- 2026-09-02T00:57:57Z – claude – shell_pid=36570 – Assigned agent via action command
- 2026-09-02T02:48:55Z – claude – shell_pid=36570 – Ready for review: 116 ontologyHub.* keys (en+zh isomorphic) across Hub shell tabs + Manager/Loader/Search; build green, lint 73 zero-delta, en values verbatim-asserted vs baseline, frozen surface untouched
- 2026-09-02T02:49:42Z – claude – shell_pid=97400 – Started review via action command
- 2026-09-02T02:54:55Z – user – shell_pid=97400 – Review passed: 8-item anti-pattern checklist all PASS/N-A. 116 ontologyHub.shell/manager/loader/search keys en+zh isomorphic; build green; lint 73 zero-delta; en values verbatim-asserted vs baseline 116/116; frozen surface untouched; C-004 standards (OWL/SKOS/SHACL/RDF) preserved; locales serial-chain prefix established for WP05/06
