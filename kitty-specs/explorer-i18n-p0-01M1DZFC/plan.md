# Implementation Plan: Explorer 中文界面 P0

**Branch**: `feature/explorer-i18n-p0` | **Date**: 2026-09-01 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/kitty-specs/explorer-i18n-p0-01M1DZFC/spec.md`

## Summary

为 Knowledge Explorer（`explorer/`，React 19 SPA）建立中英双语界面能力：引入 i18next/react-i18next 作为文案基础设施，新增语言资源文件（英文为键基准、中文为译文），头部语言开关即时切换并持久化，P0 范围覆盖全局框架文案（主导航、首屏、子视图页签、连接状态、工作区壳层、加载回退、错误边界）。随附 `tools/i18n/ui_zh_status.py` 译文过期追踪（机制同 docs/zh）。策略为经典抽取式（字面量 → 按键取译文），严守 fork 零侵入边界。

**Engineering Alignment**（用户已确认）：实现策略=经典抽取式；技术选型=react-i18next；范围=P0；分支=feature/explorer-i18n-p0（PR-bound，merge 回 main）。

## Technical Context

**Language/Version**: TypeScript 5.9（strict + erasableSyntaxOnly）、React 19.2（启用 babel-plugin-react-compiler）、Vite 6、Node 18+
**Primary Dependencies**: `react-i18next@17.0.13` + `i18next@26.4.1`（本次新增；React Compiler 修复 ≥16.3.3 已含，见 research.md R1/R4）；既有 react、@tanstack/react-query、Sigma.js 3 不新增不动
**Storage**: N/A（语言偏好存浏览器 localStorage，键 `semantica.explorer.lang`；无服务端存储）
**Testing**: Node 内置 `node:test` + tsx（`explorer/tests/`）+ Playwright e2e；门禁命令 `npm run lint`、`npm run build`（tsc -b）、`npm run test:graph-store|graph-workspace|plugin-registry|deterministic-e2e`
**Target Platform**: 现代浏览器（Chromium/Firefox/Safari 当前版）；开发环境 macOS 与 Linux（charter 部署约束）
**Project Type**: web（既有 SPA 的前端改造，后端 FastAPI 侧零改动）
**Performance Goals**: 语言切换 <1s 内完成 P0 范围文案更新且不整页刷新（NFR-001）；构建产物 gzip 增量 ≤50KB（NFR-002）
**Constraints**: 零侵入边界（C-001/C-002：上游仅可改 `explorer/src/main.tsx`、`explorer/src/App.tsx`、`explorer/src/ErrorBoundary.tsx`、`explorer/package.json`+lock、e2e 测试语言预置行）；语言状态必须响应式传播（C-003）；术语基准 `docs/zh/glossary.md`（C-004）；仅中英两语言但结构可扩展（C-005）
**Scale/Scope**: P0 文案约 200–300 条；改上游 3 个源文件 + 1 个测试文件 + 1 个依赖清单；新增 `explorer/src/i18n/**` 与 `tools/i18n/ui_zh_status.py`

## Charter Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **声明的语言/框架**：TypeScript/React/Vite 均为项目既有声明；新增依赖限 i18n 用途（C-006），符合"只用项目显式声明的工具"精神的扩展，已在 spec 决策记录中留痕（DIRECTIVE_003）。
- **测试方式**：项目已声明（npm scripts + node:test + Playwright），非 NEEDS CLARIFICATION。
- **质量门禁**：仅采用项目已声明者——lint/build/既有测试套件（NFR-004），不新增门禁。
- **评审政策**：mission review 阶段安排 focused reviewer，merge 前完成。
- **DIRECTIVE_010（规格保真）**：实现产物以 spec 的 FR-001…FR-009 为验收基准；偏差须显式记录。
- **结论**：无冲突，PASS。

## Project Structure

### Documentation (this mission)

```
kitty-specs/explorer-i18n-p0-01M1DZFC/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output（资源 schema、键命名契约、追踪脚本 CLI 契约）
└── tasks/               # Phase 2 output（/spec-kitty.tasks 生成，本期尚未创建）
```

### Source Code (repository root)

```
explorer/src/i18n/               # 全部新增
├── index.ts                     # i18next 初始化 + 检测（?lang= → localStorage → navigator.language）
├── locales/
│   ├── en.json                  # 键基准（flat 点号键，区域前缀 nav.* welcome.* connection.* shell.* error.* common.*）
│   └── zh.json                  # 中文译文（术语遵 docs/zh/glossary.md；带 __meta 基准版本）
├── types.d.ts                   # CustomTypeOptions 键类型化；zh 资源与 en 同构（缺键=编译失败）
└── LanguageToggle.tsx           # 头部 中/EN 开关：changeLanguage + localStorage + <html lang> 同步

explorer/src/main.tsx            # +1 行：import './i18n'
explorer/src/App.tsx             # navItems/页签/连接状态/WelcomeScreen/WorkspaceFallback 文案经 t()；
                                 # 头部挂 LanguageToggle；<title> 动态化
explorer/src/ErrorBoundary.tsx   # 2 条说明经 i18next.t()（类组件非 hook API）
explorer/tests/deterministicExplorerRendering.e2e.ts  # +2 行：预置 localStorage 固定英文
explorer/package.json            # + i18next、react-i18next（+package-lock.json）
semantica/explorer/              # 禁触（Python 后端零改动）
explorer/index.html              # 禁触（lang 运行时同步）
explorer/vite.config.ts          # 禁触（资源随 bundle 打包，无需 public/）

tools/i18n/ui_zh_status.py       # 新增：译文过期追踪（仿 zh_status.py：ls-tree blob sha 比对 --meta）
```

**Structure Decision**: 沿用既有 `explorer/` 单前端结构，i18n 作为新增自包含模块挂入入口；不新建目录层级、不动构建配置——资源经 import 进入 bundle，规避 `emptyOutDir: true` 对 `public/` 产物的影响。

## Complexity Tracking

*Fill ONLY if Charter Check has violations that must be justified*

无（Charter Check 通过，无违规项）。

## Implementation Concern Map

### IC-01 — i18n 核心基础设施

- **Purpose**: 建立 i18next 初始化、语言检测顺序、中英资源文件与全键类型化，是所有其他关注点的地基
- **Relevant requirements**: FR-002、FR-003、FR-005、FR-006；C-003、C-005、C-006
- **Affected surfaces**: `explorer/src/i18n/index.ts`、`explorer/src/i18n/locales/{en,zh}.json`、`explorer/src/i18n/types.d.ts`、`explorer/package.json`
- **Sequencing/depends-on**: none（最优先）
- **Risks**: React Compiler 下 locale 必须经 hook 订阅传播（useTranslation 内建 useSyncExternalStore，已核实）；组件内禁直读 `i18n.language`/缓存 t 结果（research.md R4）；`__meta` 与 translation 同级、en 侧留空对象维持同构（R2）；键同构由 `satisfies`（zh 缺键）+ 追踪脚本 extra_keys（zh 多键）双向把关

### IC-02 — 语言开关与文档同步

- **Purpose**: 提供用户可控的 中/EN 切换入口，持久化偏好并同步 `<html lang>` 与标签页标题
- **Relevant requirements**: FR-001、FR-002、FR-007
- **Affected surfaces**: `explorer/src/i18n/LanguageToggle.tsx`（新增）、`explorer/src/App.tsx`（头部挂载点）、`explorer/src/main.tsx`
- **Sequencing/depends-on**: IC-01
- **Risks**: 开关样式须复用 App.tsx 既有头部/工具栏样式 token，不引入新样式体系；隐私模式 localStorage 写入需 try/catch 容错

### IC-03 — 全局框架文案抽取（App 层）

- **Purpose**: 把模块级常量与首屏文案迁入资源键：主导航、子视图页签、连接状态、WelcomeScreen、WorkspaceFallback、ErrorBoundary
- **Relevant requirements**: FR-004、FR-005；NFR-003
- **Affected surfaces**: `explorer/src/App.tsx`、`explorer/src/ErrorBoundary.tsx`、两份 locale 资源
- **Sequencing/depends-on**: IC-01
- **Risks**: `navItems`/`CONNECTION_STATUS_LABEL` 为导入期常量，须改为渲染期经 t() 解析（结构与 icon 留常量）；ErrorBoundary 为类组件，用 i18next.t() 直调（语言切换不热更新，可接受）；WelcomeScreen 文案量大（约 76 处 JSX 文本节点）需逐条入键

### IC-04 — 工作区壳层文案抽取

- **Purpose**: 11 个工作区传给 WorkspaceShell 的标题/副标题/眉题及顶层页签双语化，正文不动
- **Relevant requirements**: FR-004；C-001（仅壳层标签，正文留待 P1/P2）
- **Affected surfaces**: `explorer/src/workspaces/*/`（仅各壳层字符串，约 11 处）——注意 C-001 边界：仅限壳层标签行，若壳层文案在 App.tsx 页签配置中则归 IC-03
- **Sequencing/depends-on**: IC-01
- **Risks**: 壳层文案与正文混杂，抽取时必须逐条核对只动壳层标签；术语对照 glossary（Ontology Hub 保留英文）

### IC-05 — 译文过期追踪脚本

- **Purpose**: 沿用 docs/zh 的基准钉版机制，报告 zh.json 相对 en.json 的 fresh/stale/orphan 与缺失键
- **Relevant requirements**: FR-008
- **Affected surfaces**: `tools/i18n/ui_zh_status.py`（新增；zh.json `__meta.source_version` 记录 en.json 的 HEAD blob sha）
- **Sequencing/depends-on**: IC-01（资源文件就位后）
- **Risks**: 键级 diff（en 有 zh 无 = missing；zh 有 en 无 = orphan）比文档级 sha 更细，需与 sha 门控并存（sha 变 → stale，另有键清单）；输出格式与 zh_status.py 对齐（表格 + --json，退出码语义一致）

### IC-06 — e2e 兼容与回归防护

- **Purpose**: 保证既有 Playwright e2e（按 "Open Semantica Explorer"/"Zoom In" 定位）在英文预置下继续通过，全套门禁绿
- **Relevant requirements**: FR-009；NFR-004
- **Affected surfaces**: `explorer/tests/deterministicExplorerRendering.e2e.ts`（预置行）、全部验证命令
- **Sequencing/depends-on**: IC-01…IC-04 完成后收尾
- **Risks**: 检测顺序须让 e2e 的预置（localStorage 或 `?lang=en`）优先于浏览器语言；预置属最小上游测试改动，PR 描述须显式说明（C-001 允许项）
