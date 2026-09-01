# Implementation Plan: Explorer 中文界面 P1（探索工作区）

**Branch**: `feature/explorer-i18n-p1` | **Date**: 2026-09-02 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/kitty-specs/explorer-i18n-p1-01M1EX2R/spec.md`

## Summary

将探索工作区（GraphWorkspace）内部约 290 条界面文案接入 P0 已建立的 i18n 基础设施（i18next 26.4.1 + react-i18next 17.0.13，键同构构建期校验，零新增依赖）。技术路线：字面量 → `t()` 抽取（函数组件用 `useTranslation`，模块级常量结构留常量、label 改为键引用渲染时解析）；图例固定枚举（`ENTITY_VISUAL_KEY`）随组件态翻译；401 等高频 API 错误在渲染点做前端中文包装（新增 `src/i18n/apiError.ts` 纯函数，后端 detail 原文保留）；deterministic-e2e 以 `?lang=en` 预置锚定英文，`"Zoom In"` 定位器行为不变。

## Technical Context

**Language/Version**: TypeScript ~5.x（strict + `erasableSyntaxOnly`）+ React 19 + Vite，Node 18+/npm 9+
**Primary Dependencies**: i18next 26.4.1、react-i18next 17.0.13（P0 已就位，本期零新增）；Sigma.js（画布，不改）
**Storage**: N/A（语言偏好存浏览器 localStorage `semantica.explorer.lang`，P0 已实现；图数据为内存 ContextGraph）
**Testing**: `node --test` + tsx 单测套件（graph-workspace / graph-store / plugin-registry / deterministic-rendering 单测）+ Playwright deterministic-e2e（`npm run test:deterministic-e2e`）
**Target Platform**: 现代浏览器 SPA；构建产物打进 `semantica/static/` 随 wheel 分发
**Project Type**: web（前端单页应用，Explorer 前端目录 `explorer/`）
**Performance Goals**: 语言切换 <1s 内完成工作区全部文案更新、不重载页面（NFR-001）；构建产物 gzip 增量 ≤30KB（NFR-002）
**Constraints**: C-001 零侵入（仅改 GraphWorkspace/**、i18n 资源与类型、既有测试定位器/预置行）；C-002 禁触后端/静态入口/其他工作区/认证流程；C-003 响应式语言状态（React Compiler 下禁用可变全局变量）；C-004 术语以 `docs/zh/glossary.md` 为准（"探索"定名）；C-005 零新增依赖；C-006 数据值不进资源文件
**Scale/Scope**: GraphWorkspace 目录 20+ 文件、约 290 条文案；1 个新前端模块（apiError.ts）；键空间新增 `graph.*` 命名空间

## Charter Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Charter（compact 模式已加载）关键原则对照：

| 原则 | 对照结论 |
| --- | --- |
| 简单优先（Simple First） | 沿用 P0 既有 i18next 机制与抽取模式，不引入新状态库/新抽象层。PASS |
| 零侵入/开闭原则 | 改动面收敛于 C-001 白名单；401 包装以新增纯函数模块落地，不改后端。PASS |
| 测试纪律（Testing Discipline） | 既有四套测试必须全绿（FR-008）；e2e 预置行最小调整且在 PR 描述显式说明。PASS |
| 可观察性 | 语言切换经 `languageChanged` 事件传播（P0 已实现），本期为消费侧扩展。PASS |

无 charter 冲突，无需 Complexity Tracking 豁免。

## Project Structure

### Documentation (this mission)

```
kitty-specs/explorer-i18n-p1-01M1EX2R/
├── plan.md              # This file (/spec-kitty.plan command output)
├── research.md          # Phase 0 output (/spec-kitty.plan command)
├── data-model.md        # Phase 1 output (/spec-kitty.plan command)
├── quickstart.md        # Phase 1 output (/spec-kitty.plan command)
└── tasks.md             # Phase 2 output (/spec-kitty.tasks command - NOT created by /spec-kitty.plan)
```

contracts/ 不适用：本 mission 无 API 契约变更（前端消费既有 `/api/graph/*` 端点，后端禁触）。

### Source Code (repository root)

```
explorer/src/
├── i18n/
│   ├── index.ts                  # P0 既有，本期不动（检测/fallback/同构校验不变）
│   ├── apiError.ts               # 新增：API 错误中文包装纯函数（401 等高频错误 → 中文包装 + detail 原文保留）
│   └── locales/
│       ├── en.json               # 扩展 graph.* 命名空间（英文键基准，值为原文英文）
│       └── zh.json               # 同步中文译文 + 刷新 __meta.source_version
└── workspaces/GraphWorkspace/    # C-001 白名单内：文案抽取
    ├── GraphWorkspace.tsx        # 主体（~3400 行）：工具栏/搜索/图例/Inspector 触发文案
    ├── GraphLoadingOverlay.tsx   # 加载态与失败面板（"Preparing graph session"/"Could not load the graph"）
    ├── GraphCanvas.tsx           # 画布层界面文案（非数据 label）
    ├── GraphInspectorPanel.tsx   # 检查器面板文案
    ├── TimelinePanel.tsx         # 底部时间轴文案
    └── behaviors/plugins/        # graphTheme.ts 等图例枚举标签映射

explorer/tests/
└── deterministicExplorerRendering.e2e.ts   # 既有测试：goto 加 ?lang=en 预置（定位器 "Zoom In" 不变）
```

**Structure Decision**: 全部改动落在 C-001 白名单内（GraphWorkspace 组件 + i18n 资源 + 既有 e2e 预置行）；唯一新增文件 `explorer/src/i18n/apiError.ts`。不建新目录层级，不设独立翻译中间层。

## Implementation Concern Map

*Include this section when the mission has multiple distinct architectural areas that inform how tasks are decomposed.*

> **Note**: Implementation concerns are NOT work packages and are NOT executable units.
> `/spec-kitty.tasks` translates these into executable WPs — one concern may become
> multiple WPs; multiple small concerns may merge into one WP. Do not label concerns
> with WP-style IDs or sequencing language.

### IC-01 — 工作区组件文案抽取

- **Purpose**: GraphWorkspace 及其子组件的 JSX 字面量、placeholder、aria-label、错误提示统一改经 `t()` 解析，中英双语。
- **Relevant requirements**: FR-001、FR-002、FR-004、FR-006、FR-007
- **Affected surfaces**: `explorer/src/workspaces/GraphWorkspace/**`（GraphWorkspace.tsx 主体、GraphLoadingOverlay、GraphCanvas、GraphInspectorPanel、TimelinePanel）；`explorer/src/i18n/locales/{en,zh}.json`
- **Sequencing/depends-on**: none（先行）
- **Risks**: GraphWorkspace.tsx 单文件约 3400 行，70 处 hooks，全函数组件 → `useTranslation` 模式可行；抽取量大易漏项，靠 en.json 键位逐屏走查 + 术语表校验兜底。数据值（节点/边 label、实体类型枚举值）严禁进资源（C-006）。

### IC-02 — 图例固定枚举迁移

- **Purpose**: 前端固定映射的图例标签（`ENTITY_VISUAL_KEY`、graphTheme 形状映射）从模块常量内联英文改为键引用，渲染时经 `t()` 解析；结构与形状枚举保持常量。
- **Relevant requirements**: FR-001（图例部分）、FR-002、FR-007
- **Affected surfaces**: `explorer/src/workspaces/GraphWorkspace/GraphWorkspace.tsx`（L165 `ENTITY_VISUAL_KEY`）、`behaviors/plugins/graphTheme.ts`
- **Sequencing/depends-on**: IC-01（键空间就位后填充）
- **Risks**: 模块常量在导入时求值，够不着 `t()`——必须保持"结构常量 + label 为 i18n 键、渲染时翻译"模式（P0 navItems 同款先例）；误把数据驱动 label 混入会违反 FR-007。

### IC-03 — API 错误前端中文包装

- **Purpose**: 401 等高频 API 错误在界面显示中文包装提示，后端 detail 原文保留可见。
- **Relevant requirements**: FR-003
- **Affected surfaces**: 新增 `explorer/src/i18n/apiError.ts`；接入点为 GraphWorkspace 错误渲染处（加载失败面板、搜索/时间轴/预测错误提示）
- **Sequencing/depends-on**: IC-01（包装文案进键空间）
- **Risks**: 前端 fetch 无集中层（散布各 workspace），本期只接 GraphWorkspace 范围（C-001/C-002 禁触其他工作区与后端）；包装函数必须容忍任意响应形态（非 JSON body、空 detail），detail 原文不得截断丢失。

### IC-04 — 资源键空间扩展与同构校验

- **Purpose**: en.json/zh.json 新增 `graph.*` 命名空间，维持键同构构建期校验与过期追踪。
- **Relevant requirements**: FR-004、FR-005、FR-009、NFR-003
- **Affected surfaces**: `explorer/src/i18n/locales/{en,zh}.json`；`tools/i18n/ui_zh_status.py`（只读使用，不改）
- **Sequencing/depends-on**: 与 IC-01/IC-02/IC-03 同步推进，最终统一刷新 `__meta.source_version`
- **Risks**: zh 侧缺键由 `satisfies typeof en` 编译报错拦截（P0 机制）；收尾必须重算 en.json blob sha 刷 `source_version`，否则 FR-009 报 stale。

### IC-05 — 既有测试锚点保护

- **Purpose**: 保证抽取改造后 deterministic-e2e 与四套单测全绿（FR-008）。
- **Relevant requirements**: FR-008、NFR-004
- **Affected surfaces**: `explorer/tests/deterministicExplorerRendering.e2e.ts`（仅预置行：`page.goto(BASE_URL)` → `page.goto(`${BASE_URL}?lang=en`)`；定位器 `"Zoom In"`、`/Open Semantica Explorer/` 不变——键值英文与原文一致故仍命中）；四套单测经侦查不断言工作区文案，预期零改动
- **Sequencing/depends-on**: IC-01 完成后验证
- **Risks**: e2e 当前无语言预置（默认 en 恰好安全），加 `?lang=en` 显式锚定防回归；若抽取后某定位器失效，仅允许最小定位器调整且在 PR 描述显式说明（spec Assumptions）。

## Complexity Tracking

*Fill ONLY if Charter Check has violations that must be justified*

无 charter 违例，本节不适用。
