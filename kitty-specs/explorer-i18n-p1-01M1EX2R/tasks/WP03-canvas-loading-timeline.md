---
work_package_id: WP03
title: 画布/加载/时间轴文案（GraphCanvas · GraphLoadingOverlay · TimelinePanel）
dependencies:
- WP02
requirement_refs:
- FR-001
- FR-002
- FR-003
tracker_refs: []
planning_base_branch: feature/explorer-i18n-p1
merge_target_branch: feature/explorer-i18n-p1
branch_strategy: Planning artifacts for this mission were generated on feature/explorer-i18n-p1. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feature/explorer-i18n-p1 unless the human explicitly redirects the landing branch.
subtasks:
- T009
- T010
- T011
agent: "claude"
shell_pid: "96412"
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
- explorer/src/workspaces/GraphWorkspace/GraphCanvas.tsx
- explorer/src/workspaces/GraphWorkspace/GraphLoadingOverlay.tsx
- explorer/src/workspaces/GraphWorkspace/TimelinePanel.tsx
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile

```
/ad-hoc-profile-load frontend-freddy
```

不可用时：TypeScript strict + React 19 函数组件 + react-i18next `useTranslation` 模式实施。

## Objective

抽取探索工作区的画布层与加载/时间轴界面文案：`GraphCanvas.tsx`（约 2670 行、粗估 42 处）、`GraphLoadingOverlay.tsx`（410 行、12 处——含 401 场景主入口"加载失败面板"）、`TimelinePanel.tsx`（199 行）。中文用户的加载、失败、重试、时间轴体验全中文；401 时显示中文包装提示且后端 detail 原文完整可见（FR-003 验收重点）。

## Context

- 三个文件均为函数组件（GraphCanvas 若含内部子函数组件同样用 `useTranslation`）。
- `GraphLoadingOverlay` 关键文案：L240 `"Preparing graph session"`、L301 `"Could not load the graph"`——失败面板是 `graphLoadError`（GraphWorkspace 会话 hook 抛出）的渲染处，本 WP 在此接入 `describeApiError`（WP01 产物）。
- 画布上的**节点/边 label 是 Sigma.js 渲染的数据值**——绝不触碰（C-006/FR-007）。只抽 DOM 层界面文案（空态、覆盖控件、提示条）。
- e2e 捕获画布文本（`__capturedCanvasText`）断言 `WORKS_AT/KNOWS/LOCATED_IN/Alice`——这些是数据 label，抽取不得影响。
- `t()` 类型化：键引用必须与 locales 同步落键（同 WP 连续完成）。

## 键空间规划（本 WP 新增段）

`graph.canvas.*`、`graph.loading.*`、`graph.timeline.*`（时间轴面板本体；GraphWorkspace 主体里的时间轴入口按钮归 WP02 的 `graph.hud.*`，已抽取的不动）。

**Ownership rationale（out-of-map edit）**：locales 增补随抽取同步；依赖链串行（WP02→WP03）无并行碰撞。

## Implementation Guidance

### T009 — GraphCanvas 抽取 → `graph.canvas.*`

以文件实际为准逐个登记，典型目标：

- 画布空态/无数据提示、加载提示条。
- 画布覆盖控件（重置视图/适配/截图类按钮、图例浮层若在本文件）。
- 交互提示（框选/平移/缩放 hint、hover 卡片框架文案）。
- `aria-label`/`title` 全抽；Canvas 绘制文本（`fillText`）是数据渲染层，**不抽**。
- 判定法：字符串若会随图数据变化 → 数据值不抽；字符串固定于代码 → 界面文案抽。

### T010 — GraphLoadingOverlay 抽取 + apiError 接入 → `graph.loading.*`

- 加载态：`Preparing graph session` → `graph.loading.preparing`；阶段进度文案（若有：解析/布局/渲染阶段提示）逐个抽。
- 失败面板：`Could not load the graph` → `graph.loading.failedTitle`；说明文字、重试按钮（Retry）→ `graph.loading.retry`。
- **401 接入（本 WP 核心交付）**：失败面板渲染 `graphLoadError` 处，若 error 携带响应状态/body（检查会话 hook 抛出的错误对象形态；`Error` 实例 message 见 L1422 `Unknown error while loading the graph.`）：
  - 能取到 `Response`/状态码时走 `describeResponseError` / `describeApiError` → 渲染 `t(view.wrapperKey)` + detail 原文段（`t('graph.errors.detailPrefix')` 前缀）。
  - 取不到结构化信息（纯 Error message）时显示 `t('graph.loading.failedTitle')` + 原始 message 兜底——**不改会话 hook 的抛错行为**（hook 文件不在本 WP owned 范围，只在渲染层消费）。
- detail 原文必须完整可见（不截断）；`detail === ""` 时隐藏该段。

### T011 — TimelinePanel 抽取 → `graph.timeline.*`

- 面板标题、播放/暂停按钮（Play/Pause）、时间刻度框架文案、空态提示（以文件实际为准，约 1-5 处）。
- 懒加载组件（`LazyTimelinePanel`）内用 `useTranslation` 正常工作（i18next 全局实例），无需额外接线；验证语言切换时面板文案即时刷新。

## Validation

- [ ] `npm run build` 绿；`npm run lint` 零增量
- [ ] `npm run test:deterministic-e2e` 全绿（画布数据 label 断言不受影响）
- [ ] `npm run test:graph-workspace` 全绿
- [ ] `?lang=zh`：加载/失败/重试、时间轴全中文；`?lang=en`：与改造前逐字一致
- [ ] 401 场景手动验证（`SEMANTICA_API_KEY=test python -m semantica.explorer ...`，前端无 key）：失败面板中文包装 + 英文 detail 完整可见

## Risks

- `graphLoadError` 的错误对象形态未经结构化包装时，401 包装可能拿不到状态码——按 T010 兜底路径处理，禁止为拿到 Response 而改会话 hook（越 owned 范围）。
- GraphCanvas 大文件易漏——完成后 grep 复扫，数据值/绘制文本豁免。

## Reviewer Guidance

- 重点核 T010 的 detail 原样保留路径与空 detail 隐藏逻辑。
- 核对画布数据渲染零改动（`git diff` 中不应出现 Sigma 场景/label 相关逻辑变化）。

## Activity Log

- 2026-09-01T17:28:37Z – claude – shell_pid=84623 – Assigned agent via action command
- 2026-09-01T17:48:25Z – claude – shell_pid=84623 – Implemented per prompt: T009 GraphCanvas (single DOM string Fit View; ~28 diagnostics reason strings exempted as dev-gated availability snapshot data, render surface in WP04 plugins); T010 GraphLoadingOverlay full extraction + FR-003 fallback path (session hook throws pure Error message, Response unreachable -> error panel chrome fully localized with original message kept verbatim in detail section, hook untouched); T011 TimelinePanel 3 strings. +42 keys en/zh isomorphic. Validation: build green, lint 74 (=baseline), graph-workspace 73/73, deterministic-e2e 1/1, en verbatim-checked.
- 2026-09-01T17:48:31Z – claude – shell_pid=96412 – Started review via action command
- 2026-09-01T17:49:40Z – user – shell_pid=96412 – Review passed: (1) GraphCanvas diff is 3 lines (import/hook/Fit View) — Sigma scene, label and fillText logic untouched, deterministic-e2e green confirms canvas data assertions intact; (2) detail preserved verbatim: {error} rendered as-is in .graph-stage-loader-error-detail, no truncation/rewrite (FR-003); session hook untouched (useLoadGraph not in diff); (3) 401 handled via prompt-sanctioned fallback path since hook throws pure Error message (Response unreachable) — describeApiError/describeResponseError intentionally not wired (no structured info available; hook out of owned scope), recorded for mission review; (4) +42 keys en/zh isomorphic, en values machine-verified verbatim, placeholder parity OK; (5) zh terms follow glossary (关系/节点/边/时态/布局/回退); (6) build green, lint 74 = baseline zero delta, graph-workspace 73/73, e2e 1/1; (7) exemptions logged: CSS font-family strings, createGraphLoadProgress contract-required message field (no longer rendered), ~28 diagnostics reason strings (dev-gated availability snapshot, render surface in WP04 plugins). No blockers.
