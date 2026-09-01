---
work_package_id: WP02
title: App 层全局文案抽取与语言开关挂载
dependencies:
- WP01
requirement_refs:
- FR-001
- FR-004
tracker_refs: []
planning_base_branch: feature/explorer-i18n-p0
merge_target_branch: feature/explorer-i18n-p0
branch_strategy: Planning artifacts for this mission were generated on feature/explorer-i18n-p0. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feature/explorer-i18n-p0 unless the human explicitly redirects the landing branch.
subtasks:
- T007
- T008
- T009
- T010
- T011
- T012
agent: "claude"
shell_pid: "14272"
history:
- timestamp: '2026-09-01T09:51:16Z'
  action: created
  agent: claude
agent_profile: frontend-freddy
authoritative_surface: explorer/src/App
create_intent: []
execution_mode: code_change
owned_files:
- explorer/src/App.tsx
- explorer/src/ErrorBoundary.tsx
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile

Before reading anything else, load your assigned agent profile:

```
/ad-hoc-profile-load frontend-freddy
```

If that command is unavailable, proceed as a careful frontend implementer: TypeScript strict、React 19 函数组件、最小 diff。

## Objective

把 App 层 P0 范围的全部英文文案替换为 `t()` 取译（键位契约 = WP01 交付的 `explorer/src/i18n/locales/en.json`），把 `<LanguageToggle/>` 挂到应用头部。完成后：中文浏览器用户首屏即中文，切换即时生效不刷新（FR-001/FR-004），英文用户界面与改造前逐像素一致。

## Context

- 仓库根：`/Users/luofisher/ToolsChain/semantica`（执行时在 lane worktree，结构相同）
- **前置**：WP01 已交付 `explorer/src/i18n/`（init/资源/类型/LanguageToggle）。你的分支基于 WP01 完成后的 lane 基线
- **键位契约**：所有键名与英文值以 `explorer/src/i18n/locales/en.json` 为准（T002 清单已列）。接线时逐键对照，**不要自行发明键名**。发现缺键/键名不贴切：小幅越界补改 en+zh 两文件（一次一处，完成报告记一行理由）
- **React Compiler 已启用**（关键约束，详见 plan.md IC-03）：
  - `navItems`（App.tsx ~L87）、`CONNECTION_STATUS_LABEL`（~L79）是**导入期模块常量**，够不着 `t()`。改法：结构（id/icon）留常量，label/hint 改为渲染期经 `t()` 解析（组件内由 `useTranslation()` 的 `t` 现取，映射表只存键名）
  - 禁止在 memoized 回调里直读 `i18n.language` 或缓存 `t` 的结果
- **ErrorBoundary 是类组件**：不能用 hook，直接 `import i18n from "./i18n"` 后调 `i18n.t("error.boundary.*")`。语言切换时已渲染的错误面板不热更新——可接受（错误面板是瞬态 UI），spec 已认可
- **e2e 锚点保护**：`explorer/tests/deterministicExplorerRendering.e2e.ts` 按 `/Open Semantica Explorer/` 与 `"Zoom In"` 定位。英文下 `welcome.cta.open` 必须逐字保持 `Open Semantica Explorer`（Zoom In 在 GraphWorkspace 内部，不在 P0 范围，勿动）
- 布局事实（已核实）：7 处 `WorkspaceShell` 调用全部在 App.tsx 内（explore/analyze/decisions/enrich/ontology-hub/manage + 兜底分支）；工作区组件不自带壳层，**本 WP 不碰 `explorer/src/workspaces/**`**
- 零侵入边界：只动 owned_files（App.tsx、ErrorBoundary.tsx）。`index.html`、`vite.config.ts`、Python 后端禁触

## Subtask Guidance

### T007: 主导航与头部（navItems + LanguageToggle 挂载）

**Purpose**: 左侧导航六项双语化；头部出现语言开关。

**Steps**:
1. `NavItem` 类型改为存键名：`{ id: WorkspaceId; labelKey: "nav.explore.label" | ...; hintKey: ...; icon: LucideIcon }`（或 `labelKey: keyof typeof en.translation` 风格，取类型安全更好者）。`navItems` 常量只存 id/键名/icon。
2. 导航渲染处（`navItems.map(...)`）改用 `useTranslation()` 的 `t`：`<span className="nav-label">{t(item.labelKey)}</span>`、`title={t(item.hintKey)}`。
3. `brand-pill`（~L1980）：`title="Semantica Knowledge Explorer"` → `title={t("common.appTitle")}`。
4. 在 `app-rail` 适当位置（brand-pill 之后、导航项之前或 rail 底部，选视觉合理者）挂 `<LanguageToggle />`（从 `./i18n/LanguageToggle` 导入）。
5. App 根组件顶部 `const { t } = useTranslation();`。

**Files**: `explorer/src/App.tsx`

**Validation**:
- [ ] 导航六项 label+hint（hover title）随语言切换
- [ ] 头部出现 中/EN 开关，点击即时切换整层文案、页面不刷新

### T008: 工作区壳层与子视图页签（7 处 WorkspaceShell）

**Purpose**: 六个工作区 + 兜底分支的 title/subtitle/kicker/tabs 双语化（FR-004 壳层部分）。

**Steps**:
1. 逐处替换（键名对照 en.json，注意 explore/analyze 的 kicker 是**视图条件值**）：
   - explore：`title={t("shell.explore.title")}`、subtitle 仅 vocabulary 视图传 `t("shell.explore.subtitle")`、kicker 按视图 `t("shell.explore.kickerGraph" | "shell.explore.kickerVocab")`；两个页签 `t("tabs.explore.graph")` / `t("tabs.explore.vocabulary")`
   - analyze：同理（kickerReasoning/kickerSparql；tabs.analyze.reasoning/sparql）
   - decisions / enrich / ontology-hub / manage：直译键替换；enrich 四页签、manage 三页签
2. `WorkspaceShell` 组件签名的 `kicker = 'Workspace'` 默认值保留原样（所有调用点都显式传 kicker，默认值是死代码；如你判断顺手改为 `t("shell.kickerFallback")` 亦可，但需在 en/zh 同步补键并记一行理由——二选一，不许只改一半）
3. 页签按钮的文案节点逐个替换，`data-active` 逻辑不动。

**Files**: `explorer/src/App.tsx`

**Validation**:
- [ ] 六工作区壳层标题/副标题/眉题/页签全部随语言切换
- [ ] 视图切换（graph↔vocabulary、reasoning↔sparql）时 kicker 正确联动

### T009: 连接状态与首屏数据卡（状态栏 + metrics + 启动器）

**Purpose**: CONNECTION_STATUS_LABEL 渲染期化；首屏状态栏/指标卡/工作区卡片按钮双语化。

**Steps**:
1. 删除 `CONNECTION_STATUS_LABEL` 常量（或改为键映射 `Record<ConnectionStatus, 键名>`），渲染处（WelcomeScreen 状态栏 ~L1614 与任何其他引用点，grep 确认）经 `t()` 取 `connection.checking/online/offline`。
2. `metrics: LandingMetric[]` 数组在组件体内构建（本就在渲染期），label/value-fallback 换 `t("welcome.metrics.*")`；注意 `isOnline ? 'Dataset online' : 'Ready to explore'` 的条件结构保留，只换字面量为 t() 调用。
3. `secondaryLaunchers` 5 项的 label/description 换键（`welcome.card.*.label/desc`）；icon/onClick 结构不动。`key={launcher.label}` 若改用 label 作 key，换成 `launcher.label` 对应的稳定键名（如 card id）而不是译文——**译文不能当 React key**。
4. 状态栏：`welcome.status.version`（`Semantica v2 · Semantic Intelligence` 品牌串照键翻译）。

**Files**: `explorer/src/App.tsx`

**Validation**:
- [ ] 断开后端 → 状态栏显示 `Backend Unreachable`/`后端不可达`（随当前语言）
- [ ] 指标卡与 5 张启动卡全部双语切换，卡片渲染顺序与 key 稳定

### T010: 首屏 Hero 与预览面板（剩余 welcome.* 全量）

**Purpose**: 标题、副标题、CTA、预览面板、能力带逐节点入键（FR-004 首屏部分，约 40 节点）。

**Steps**:
1. Hero：`welcome.kicker.aria`（aria-label）、`welcome.kicker.text`、`welcome.titleLine1`/`titleLine2`（保留 `<br/>` 与 `<span>` 高亮结构，只换文本）、`welcome.subtitle`、两个 CTA（`welcome.cta.open`——**英文值逐字 `Open Semantica Explorer`，勿动**、`welcome.cta.reasoning`）。
2. 预览面板：`welcome.preview.aria`、`welcome.preview.tab`、`welcome.command.label`/`meta`、dossier 的 kicker/行标题/值（`welcome.dossier.*`；`NSRP1` 与 `0.84` 是数据不换）、timeline 的 title/badge（`welcome.timeline.*`；年份 1970/2030 不换）。
3. 工作区区块：`welcome.section.aria`/`title`、主卡三行（`welcome.card.primary.*`）。
4. 能力带：`welcome.capability.aria`/`label` 与 5 个能力项。
5. 逐节点核对 en.json 键清单；确有遗漏的文本节点（如 aria-label）补键（en+zh 同步）并记一行理由。

**Files**: `explorer/src/App.tsx`

**Validation**:
- [ ] 首屏从状态栏到能力带逐屏走查：英文模式与改造前渲染逐字一致；中文模式无英文残留（品牌名除外）
- [ ] `npm run build` 通过（类型化 t() 键名若有拼错此处即报错）

### T011: 加载回退与错误边界

**Purpose**: WorkspaceFallback 与 ErrorBoundary 文案双语化。

**Steps**:
1. `WorkspaceFallback`（~L1487）：`Loading workspace…` → `t("fallback.loading")`。它是函数组件，可 `useTranslation()`。
2. `ErrorBoundary.tsx`（类组件）：`import i18n from "./i18n";`，render 中 5 处文案换 `i18n.t(...)`，键**已由 WP01 交付，直接消费、勿重复补键**：`error.boundary.title`（Something went wrong in this view.）、`error.boundary.detail`（可重试分支长句）、`error.boundary.fatal`（重试耗尽分支长句）、`error.boundary.retry`（Try Again）、`error.boundary.reload`（Reload Application）。
3. 上述 5 个 `error.boundary.*` 键在 WP01 实现时已越界补入 en/zh（en 值逐字取自现有文件原文），不在你的改动范围。
4. console.error 的调试日志（`ErrorBoundary caught an error:`）是开发者日志，不翻译。

**Files**: `explorer/src/App.tsx`、`explorer/src/ErrorBoundary.tsx`

**Validation**:
- [ ] 中文模式下人为触发渲染错误（临时抛错试验后删除）→ 错误面板中文；按钮可用
- [ ] `npm run lint` 零错误

### T012: P0 残留清点、基准 sha 刷新与门禁自检

**Purpose**: 确认 P0 范围零英文残留；把 zh.json 的过期基准钉回**最终** en.json（A1 修复位）；本 WP 门禁绿。

**Steps**:
1. 清点：grep App.tsx 中剩余的 JSX 文本节点与字符串字面量，逐一分类——属 P0 范围者必须已入键；`aria-hidden` 装饰文本、纯数据（NSRP1/年份/数字）、`Semantica v2` 类品牌串可留。把清点结论写进完成报告（残留清单 + 豁免理由）。
2. `document.title` 动态化核验：语言切到 zh → 标签页标题变 `知识探索器 · Semantica`，`<html lang>` 变 `zh-CN`（WP01 的 languageChanged 监听负责；你只验证联动生效）。
3. **基准 sha 校验/刷新（必做）**：至此 en.json 内容定稿（error.boundary.* 键已由 WP01 交付；若你接线中又补了新键，en.json 才会真变）。执行 `git hash-object explorer/src/i18n/locales/en.json` 并与 `explorer/src/i18n/locales/zh.json` 的 `__meta.source_version` 比对：一致则记录"无需刷新"即可；不一致（你补过键）则把 `__meta.source_version` 更新为当前值——这是对 WP01 owned 文件的一次预期内越界编辑（仅 `__meta` 一行），完成报告记一行理由。不刷新则 WP03/WP04 的 fresh 门禁必然 false-fail。
4. 门禁：`cd explorer && npm run lint && npm run build` 全绿。

**Files**: `explorer/src/i18n/locales/zh.json`（仅 `__meta.source_version` 一行）

**Validation**:
- [ ] 残留清点表写入完成报告
- [ ] zh.json `__meta.source_version` == 当前 en.json 的 `git hash-object` 值
- [ ] lint + build 全绿

## Test Strategy

不新增单测（spec 未要求）。正确性门禁 = tsc 类型化键名 + WP04 的 e2e。手动验证：`npm run dev` + 后端（quickstart §3 走查 1-5 项可在此 WP 预演，正式验收在 WP04）。

## Definition of Done

- [ ] T007–T012 全部完成且 Validation 勾稽
- [ ] P0 范围（导航/壳层/页签/连接状态/首屏/回退/错误边界）零英文残留（豁免项有记录）
- [ ] 语言开关在头部可用，切换即时且不刷新
- [ ] 英文模式下可见界面与改造前一致（e2e 锚点文案逐字未动）
- [ ] zh.json `__meta.source_version` 已刷新至最终 en.json 的 blob sha
- [ ] lint + build 全绿；`error.boundary.*` 5 键由 WP01 交付并正确消费；如另有补键均有理由记录

## Risks

- **键位漂移**：接线时键名与 en.json 不一致 → tsc 立即报错（类型化红利），照报错修齐即可。
- **React key 用译文**：启动卡 map 的 key 若用 label 必须改稳定键名，否则切换语言时组件重建、动画闪烁。
- **welcome 文案量大**（~60 节点）：逐区块小步替换，每完成一个区块跑一次 build，不要一把梭。
- **条件文案结构**（isOnline 三元、视图条件 kicker）：只换字面量，不动条件逻辑。

## Reviewer Guidance

核对：① grep 确认 App.tsx 中 P0 范围无内联英文残留；② e2e 锚点 `Open Semantica Explorer` 逐字未变；③ 模块常量重构未改变导航结构/图标/行为；④ ErrorBoundary 用 i18n.t 直调而非 hook；⑤ 越界补键 en/zh 成对出现。

## Activity Log

- 2026-09-01T13:09:35Z – claude – shell_pid=14272 – Assigned agent via action command
- 2026-09-01T13:54:37Z – claude – shell_pid=14272 – Ready for review
- 2026-09-01T14:01:19Z – user – shell_pid=14272 – 验收通过：diff 仅 owned_files + 允许越界（titleLine2 成对拆分+source_version 一行）；e2e 锚点逐字；键同构 107；source_version=6e6cf42b 一致；eslint 零问题、build exit 0；React key 改稳定键名；commit d6dfef3d
