# Tasks: Explorer 中文界面 P0

**Mission**: explorer-i18n-p0-01M1DZFC
**Branch**: feature/explorer-i18n-p0
**Generated**: 2026-09-01T09:51:16Z

## Subtask Index

| ID | Description | WP | Parallel | Status |
|----|-------------|----|----------|--------|
| T001 | 添加 i18next@26.4.1 + react-i18next@17.0.13 依赖并更新锁文件 | WP01 |  | pending |
| T002 | 创建 locales/en.json + zh.json（完整 P0 键清单，约 95 键 + \_\_meta） | WP01 |  | pending |
| T003 | types.d.ts 全键类型化（CustomTypeOptions + zh satisfies typeof en） | WP01 |  | pending |
| T004 | index.ts 初始化：四级语言检测 + languageChanged 文档同步 | WP01 |  | pending |
| T005 | LanguageToggle.tsx 语言开关组件（changeLanguage + 持久化容错） | WP01 |  | pending |
| T006 | main.tsx 接线 + lint/build 验证 | WP01 |  | pending |
| T007 | 主导航 navItems 渲染期 t() 化 + 头部挂载 LanguageToggle + brand-pill title | WP02 |  | pending |
| T008 | 7 处 WorkspaceShell title/subtitle/kicker/tabs 入键 | WP02 |  | pending |
| T009 | CONNECTION_STATUS_LABEL 渲染期化 + 首屏状态栏/metrics/启动卡 | WP02 |  | pending |
| T010 | 首屏 Hero/预览面板/能力带全量入键（~40 节点） | WP02 |  | pending |
| T011 | WorkspaceFallback + ErrorBoundary 文案（类组件 i18n.t 直调） | WP02 |  | pending |
| T012 | P0 残留清点 + 基准 sha 刷新（zh.json \_\_meta.source_version）+ lint/build 自检 | WP02 |  | pending |
| T013 | ui_zh_status.py：资源扫描与键级 diff（missing/extra，排除 \_\_meta） | WP03 | [P] | pending |
| T014 | CLI 与输出（表格/--json/退出码 0/1/2）对齐契约 | WP03 |  | pending |
| T015 | 本期资源实跑自检 → fresh + missing=0 + extra=0 | WP03 |  | pending |
| T016 | e2e 预置 localStorage 固定英文（addInitScript，≤5 行） | WP04 |  | pending |
| T017 | npm run test:deterministic-e2e 全绿 | WP04 |  | pending |
| T018 | 全套静态与单元门禁（lint/build/graph-store/graph-workspace/plugin-registry） | WP04 |  | pending |
| T019 | 体积预算（NFR-002）+ ui_zh_status fresh（FR-008）+ quickstart §3 手动走查与 §4 术语抽查（NFR-001/NFR-003）+ 验收表 | WP04 |  | pending |

## WP01 — i18n 基础设施与语言开关（Foundation）

**Prompt**: `tasks/WP01-i18n-core-infrastructure.md`
**Goal**: 建立 i18n 模块（依赖/资源/类型化/检测/开关组件/接线），是全部其他 WP 的地基
**Priority**: P0（最高，串行第一棒）
**Independent test**: `cd explorer && npm run lint && npm run build` 全绿；en/zh 键集合一致；界面（未接线部分）无可见变化
**Estimated prompt size**: ~330 lines

- [x] T001 添加 i18next@26.4.1 + react-i18next@17.0.13 依赖并更新锁文件 (WP01)
- [x] T002 创建 locales/en.json + zh.json（完整 P0 键清单，约 95 键 + \_\_meta） (WP01)
- [x] T003 types.d.ts 全键类型化（CustomTypeOptions + zh satisfies typeof en） (WP01)
- [x] T004 index.ts 初始化：四级语言检测 + languageChanged 文档同步 (WP01)
- [x] T005 LanguageToggle.tsx 语言开关组件（changeLanguage + 持久化容错） (WP01)
- [x] T006 main.tsx 接线 + lint/build 验证 (WP01)

**Dependencies**: none
**Parallel opportunities**: 无（串行第一棒）
**Risks**: React Compiler 记忆化约束（locale 必须经 useTranslation 订阅）；键清单是 WP02 的接线契约，遗漏会传导

## WP02 — App 层全局文案抽取与语言开关挂载

**Prompt**: `tasks/WP02-app-chrome-extraction.md`
**Goal**: App.tsx/ErrorBoundary.tsx 的 P0 文案全部入键（导航/壳层/页签/连接状态/首屏/回退/错误边界），挂载语言开关
**Priority**: P0（核心功能交付）
**Independent test**: 中文模式下 P0 范围零英文残留；英文模式与改造前一致（e2e 锚点逐字未动）；lint/build 全绿
**Estimated prompt size**: ~230 lines

- [x] T007 主导航 navItems 渲染期 t() 化 + 头部挂载 LanguageToggle + brand-pill title (WP02)
- [x] T008 7 处 WorkspaceShell title/subtitle/kicker/tabs 入键 (WP02)
- [x] T009 CONNECTION_STATUS_LABEL 渲染期化 + 首屏状态栏/metrics/启动卡 (WP02)
- [x] T010 首屏 Hero/预览面板/能力带全量入键（~40 节点） (WP02)
- [x] T011 WorkspaceFallback + ErrorBoundary 文案（类组件 i18n.t 直调） (WP02)
- [x] T012 P0 残留清点 + 基准 sha 刷新（zh.json \_\_meta.source_version）+ lint/build 自检 (WP02)

**Dependencies**: WP01
**Parallel opportunities**: 与 WP03 并行（文件不相交）
**Risks**: 模块常量重构（navItems/CONNECTION_STATUS_LABEL）须保持结构/icon/行为不变；React key 禁用译文；e2e 锚点文案逐字保护

## WP03 — 译文过期追踪脚本 ui_zh_status.py

**Prompt**: `tasks/WP03-ui-zh-staleness-script.md`
**Goal**: 沿用 docs/zh 的 sha 钉版机制报告 zh.json 过期状态与键级 diff，契约见 contracts/ui-zh-status-cli.md
**Priority**: P0（配套工具）
**Independent test**: `python tools/i18n/ui_zh_status.py` 对本期资源报告 fresh、missing=0、extra=0；退出码 0/1/2 语义正确
**Estimated prompt size**: ~150 lines

- [x] T013 ui_zh_status.py：资源扫描与键级 diff（missing/extra，排除 \_\_meta） (WP03)
- [x] T014 CLI 与输出（表格/--json/退出码 0/1/2）对齐契约 (WP03)
- [x] T015 本期资源实跑自检 → fresh + missing=0 + extra=0 (WP03)

**Dependencies**: WP01
**Parallel opportunities**: 与 WP02 并行（只依赖 WP01）
**Risks**: source_version 的 sha 时点（hash-object vs HEAD）漂移；只依赖 WP01 的资源结构

## WP04 — e2e 英文预置与全套门禁回归（收尾）

**Prompt**: `tasks/WP04-e2e-preset-regression-gates.md`
**Goal**: e2e 固定英文继续全绿（FR-009），跑全套门禁完成集成验收（NFR-004/NFR-002/FR-008 复核），并收口 quickstart §3 手动走查与 §4 术语抽查（成功标准 1-3、NFR-001/NFR-003 的验证位）
**Priority**: P0（集成验收，必须最后）
**Independent test**: 六条门禁命令全绿；e2e diff 仅预置行；体积增量 ≤50KB；ui_zh_status fresh；§3 七项走查与 §4 术语抽查逐项有结果
**Estimated prompt size**: ~180 lines

- [ ] T016 e2e 预置 localStorage 固定英文（addInitScript，≤5 行） (WP04)
- [ ] T017 npm run test:deterministic-e2e 全绿 (WP04)
- [ ] T018 全套静态与单元门禁（lint/build/graph-store/graph-workspace/plugin-registry） (WP04)
- [ ] T019 体积预算（NFR-002）+ ui_zh_status fresh（FR-008）+ quickstart §3 手动走查与 §4 术语抽查（NFR-001/NFR-003）+ 验收表 (WP04)

**Dependencies**: WP01, WP02, WP03
**Parallel opportunities**: 无（收尾集成位）
**Risks**: e2e 锚点回归时纪律是上报阻塞而非改测试；macOS 代理干扰需 NO_PROXY 前缀

## Execution Notes

- **MVP 路径**：WP01 单独可交付（基础设施落地、界面无变化、可合入待用）。
- **推荐批次**：WP01 → (WP02 ∥ WP03) → WP04。
- **实现命令**：`spec-kitty agent action implement WP01 --agent claude`（其余 WP 同理）。
- **键位契约流**：WP01 定键 → WP02 消费键（越界补键需记录，收尾时刷新基准 sha）→ WP03 校验键 → WP04 复核 fresh。
- **计数口径（键数 vs 文案条数）**：spec/plan 估的"约 200-300 条文案"是含中英双语渲染与重复实例的字符串计数口径；任务清单键位口径为去重后的键数——实际交付 **107 键**（清单约 95-100 + 越界补键 6 + 拆分净增 1）。两者描述同一范围，不矛盾。
- **设计内越界补键汇总（T002 键清单之外，供 mission review 逐项核验 en/zh 成对 + 理由记录）**：
  - WP01-T005：`language.toggle`（LanguageToggle 的 aria-label）
  - WP01-T002/T011 联动：`error.boundary.title` / `error.boundary.detail` / `error.boundary.fatal` / `error.boundary.retry` / `error.boundary.reload`（ErrorBoundary 5 条文案；实现期在 WP01 一次性补入 en/zh，WP02 只消费）
  - WP02-T010：`welcome.titleLine2` 拆为 `welcome.titleLine2Lead` + `welcome.titleLine2Accent`（原 JSX 高亮结构 `like a <span>living system.</span>` 的 span 在句中，单键纯文本无法承载；en/zh 成对拆分，英文渲染逐字一致）
  - WP02-T012：对 WP01 owned 的 zh.json 做一次预期内越界编辑（仅 `__meta.source_version` 一行；因 T010 拆键 en.json 变为 `6e6cf42b…`，已实刷并复核一致）
- **spec 覆盖**：FR-001/FR-004 → WP02；FR-002/FR-003/FR-005/FR-006/FR-007 → WP01；FR-008 → WP03+WP04；FR-009 → WP04；NFR-001/NFR-003 由 WP04 的 quickstart §3 走查与 §4 术语抽查验收（WP01/WP02 落实实现与术语规则）；NFR-002/NFR-004 由 WP04 验收。
