# Tasks: Explorer 中文界面 P1（探索工作区）

**Mission**: `explorer-i18n-p1-01M1EX2R` · Branch: `feature/explorer-i18n-p1` · Generated: 2026-09-02

**执行模型说明**：WP01→WP05 为串行依赖链（单 lane）。原因：`t()` 经 P0 `CustomTypeOptions` 全类型化，组件抽取与 locales 键增补必须在同一 WP 同步完成（缺键 = tsc 报错），而 `locales/{en,zh}.json` 是所有 WP 的共享汇聚点——串行执行避免并行 merge 冲突。各 WP 对 locales 的增补相对其 `owned_files` 是"well-justified out-of-map edit"，已逐 WP 记录 rationale。

## Subtask Index

| ID | Description | WP | Parallel |
| --- | --- | --- | --- |
| T001 | 新建 `explorer/src/i18n/apiError.ts`：API 错误中文包装纯函数（状态码映射 + detail 原文保留） | WP01 | |
| T002 | locales 增补 `graph.errors.*` 包装文案键（en/zh） | WP01 | |
| T003 | deterministic-e2e `page.goto` 加 `?lang=en` 预置并验证锚点不变 | WP01 | |
| T004 | GraphWorkspace 工具栏抽取：分组标签 + 动作按钮 → `graph.toolbar.*` | WP02 | |
| T005 | GraphWorkspace 搜索栏抽取（placeholder/建议/错误）→ `graph.search.*` | WP02 | |
| T006 | 图例固定枚举迁移：`ENTITY_VISUAL_KEY` label 改键引用渲染时翻译 → `graph.legend.*` | WP02 | |
| T007 | GraphWorkspace 剩余主体文案（HUD/预测卡片/路径面板/时间轴入口）→ `graph.hud.*` 等 | WP02 | |
| T008 | GraphWorkspace 内错误提示点接入 apiError（搜索/预测） | WP02 | |
| T009 | GraphCanvas 界面文案抽取 → `graph.canvas.*` | WP03 | |
| T010 | GraphLoadingOverlay 加载态/失败面板（含重试）+ apiError 接入 `graphLoadError` 渲染 | WP03 | |
| T011 | TimelinePanel 文案 → `graph.timeline.*` | WP03 | |
| T012 | GraphInspectorPanel 抽取（属性/关系/溯源框架文案）→ `graph.inspector.*` | WP04 | |
| T013 | explorationEffects 两插件抽取 → `graph.effects.*` | WP04 | |
| T014 | temporalOverlay/neighborhoodPanel/legendPlugin 抽取 → `graph.temporalOverlay.*` 等 | WP04 | |
| T015 | MarkdownContentViewer + graphTheme 标签映射抽取 | WP04 | |
| T016 | 键同构复核（tsc）+ en/zh 键位逐屏走查 | WP05 | |
| T017 | 刷新 `__meta.source_version`（en.json HEAD blob sha）+ ui_zh_status fresh | WP05 | |
| T018 | 四套测试全绿 + lint/build 零增量 | WP05 | |
| T019 | 双语手动走查（quickstart §4-7）+ 术语表一致率核对 | WP05 | |

## Work Packages

### WP01 — i18n 错误包装基础与 e2e 锚定

**Goal**: 交付 `apiError.ts` 纯函数与 `graph.errors.*` 键段，e2e 显式锚定英文。后续 WP 的错误接入与抽取以此为依赖。
**Priority**: High（先行） · **Independent test**: apiError 单元行为经 e2e/构建间接验证；e2e 全绿
**Prompt**: `tasks/WP01-i18n-error-wrapper-foundation.md` · ~260 lines

- [x] T001 新建 apiError.ts 纯函数（WP01）
- [x] T002 locales 增补 graph.errors.* 键（WP01）
- [x] T003 e2e ?lang=en 预置（WP01）

Dependencies: none。Risks: 包装函数必须容忍任意响应形态（非 JSON body、空 detail）。

### WP02 — GraphWorkspace 主体文案抽取

**Goal**: 主文件（~3400 行）约 95 处文案抽取 + 图例枚举迁移 + 错误接入，含 `graph.toolbar/search/legend/hud` 等键段。
**Priority**: High · **Independent test**: `npm run build`（键同构）+ e2e "Zoom In" 锚点不变
**Prompt**: `tasks/WP02-graphworkspace-main-extraction.md` · ~420 lines

- [x] T004 工具栏抽取（WP02）
- [x] T005 搜索栏抽取（WP02）
- [x] T006 图例枚举迁移（WP02）
- [x] T007 剩余主体文案（WP02）
- [x] T008 错误点接入 apiError（WP02）

Dependencies: WP01。Risks: 文件大，逐区块抽取防漏项；数据值严禁进资源（C-006）。

### WP03 — 画布/加载/时间轴文案

**Goal**: GraphCanvas（~42 处）、GraphLoadingOverlay（加载态/失败面板/重试 + 401 接入）、TimelinePanel。
**Priority**: High · **Independent test**: build + e2e 全绿
**Prompt**: `tasks/WP03-canvas-loading-timeline.md` · ~320 lines

- [x] T009 GraphCanvas 抽取（WP03）
- [x] T010 加载覆盖层抽取 + apiError 接入（WP03）
- [x] T011 TimelinePanel 抽取（WP03）

Dependencies: WP02。Risks: 失败面板是 401 场景主入口，detail 原文保留是验收重点（FR-003）。

### WP04 — Inspector 与插件文案

**Goal**: GraphInspectorPanel（~30 处）、explorationEffects 两插件（~67 处）、temporalOverlay/neighborhoodPanel/legendPlugin、MarkdownContentViewer、graphTheme 标签映射。
**Priority**: Medium · **Independent test**: build + e2e + plugin-registry 套件
**Prompt**: `tasks/WP04-inspector-plugins-theme.md` · ~400 lines

- [x] T012 InspectorPanel 抽取（WP04）
- [x] T013 explorationEffects 插件抽取（WP04）
- [x] T014 temporal/neighborhood/legend 插件抽取（WP04）
- [x] T015 MarkdownViewer + graphTheme（WP04）

Dependencies: WP03。Risks: 插件文案经 plugin registry 渲染，确认 `t()` 在 lazy 组件内正常订阅语言切换。

### WP05 — 资源收口与全量验证

**Goal**: 键同构复核、source_version 刷新、ui_zh_status fresh、四套测试全绿、双语走查与术语核对。
**Priority**: High（验收关） · **Independent test**: quickstart.md 全部场景
**Prompt**: `tasks/WP05-resource-finalization-verification.md` · ~280 lines

- [x] T016 键同构复核与走查（WP05）
- [x] T017 source_version 刷新（WP05）
- [ ] T018 测试全绿与零增量（WP05）
- [ ] T019 双语走查与术语核对（WP05）

Dependencies: WP04。Risks: source_version 必须在 en.json 定稿后取 HEAD blob sha，早刷会 stale。

## Requirement Coverage

| FR/NFR | WPs |
| --- | --- |
| FR-001 | WP02, WP03, WP04 |
| FR-002 | WP02, WP03, WP04 |
| FR-003 | WP01, WP02, WP03 |
| FR-004 | WP05 |
| FR-005 | WP05 |
| FR-006 | WP02 |
| FR-007 | WP02, WP04 |
| FR-008 | WP01, WP05 |
| FR-009 | WP05 |
| NFR-001 | WP02 |
| NFR-002 | WP05 |
| NFR-003 | WP05 |
| NFR-004 | WP05 |
