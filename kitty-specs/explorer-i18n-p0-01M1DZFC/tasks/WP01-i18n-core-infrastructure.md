---
work_package_id: WP01
title: i18n 基础设施与语言开关（Foundation）
dependencies: []
requirement_refs:
- FR-002
- FR-003
- FR-005
- FR-006
- FR-007
tracker_refs: []
planning_base_branch: feature/explorer-i18n-p0
merge_target_branch: feature/explorer-i18n-p0
branch_strategy: Planning artifacts for this mission were generated on feature/explorer-i18n-p0. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feature/explorer-i18n-p0 unless the human explicitly redirects the landing branch.
subtasks:
- T001
- T002
- T003
- T004
- T005
- T006
agent: "claude"
shell_pid: "37250"
history:
- timestamp: '2026-09-01T09:51:16Z'
  action: created
  agent: claude
agent_profile: frontend-freddy
authoritative_surface: explorer/src/i18n/
create_intent:
- explorer/src/i18n/index.ts
- explorer/src/i18n/types.d.ts
- explorer/src/i18n/LanguageToggle.tsx
- explorer/src/i18n/locales/en.json
- explorer/src/i18n/locales/zh.json
execution_mode: code_change
owned_files:
- explorer/src/i18n/**
- explorer/src/main.tsx
- explorer/package.json
- explorer/package-lock.json
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile

Before reading anything else, load your assigned agent profile:

```
/ad-hoc-profile-load frontend-freddy
```

If that command is unavailable, proceed as a careful frontend implementer: TypeScript strict、React 19 函数组件、零不必要依赖。

## Objective

为 Knowledge Explorer（`explorer/`，React 19 SPA + Vite）建立 i18n 基础设施：安装 i18next/react-i18next，创建 `explorer/src/i18n/` 模块（初始化 + 语言检测 + 双语资源 + 全键类型化 + 语言开关组件），并在 `main.tsx` 接线。完成后应用可启动、`t()` 可用、键全类型化，但 App.tsx 尚未消费（那是 WP02 的事）。

本 WP 是全部其他 WP 的地基（WP02/WP03/WP04 都依赖你）。

## Context

- 仓库根：`/Users/luofisher/ToolsChain/semantica`（执行时在 lane worktree，结构相同）
- 前端目录：`explorer/`；包管理 npm（`package-lock.json` 必须随 `package.json` 一起更新）；Node 18+
- **React Compiler 已启用**（`babel-plugin-react-compiler`）：语言状态必须经响应式订阅传播。`useTranslation()` 内部走 `useSyncExternalStore`（react-i18next ≥16.3.3 已修复相关 issue），天然兼容。**禁止**在模块常量、memoized 回调里直读 `i18n.language` 或缓存 `t` 的结果
- TypeScript 配置为 `strict` + `erasableSyntaxOnly`（禁 enum/namespace）+ `resolveJsonRequired`（JSON import 类型化，需确认 tsconfig 已含 `resolveJsonModule`；Vite 模板通常默认开启，若未开启需在探索后确认——注意 tsconfig 也可能不在你的 owned_files 内，此时在完成报告中记录该需求而不是改文件）
- 技术决策（已冻结，不要重新选型）：`i18next@26.4.1` + `react-i18next@17.0.13`；无 detector 插件，应用内自解析语言；`fallbackLng: 'en'`；`interpolation.escapeValue: false`（React 已防转义）；`react: { useSuspense: false }`
- 行为契约（**必须逐条遵守**）：`kitty-specs/explorer-i18n-p0-01M1DZFC/contracts/language-detection.md`
- 资源 schema 与键前缀：`kitty-specs/explorer-i18n-p0-01M1DZFC/data-model.md`（LocaleResource 实体）
- 术语基准：`docs/zh/glossary.md`（知识图谱/本体/溯源/实体消解/决策智能/推理引擎/去重/工作区；Ontology Hub 产品名保留英文）
- 零侵入边界：你只动 owned_files 清单内的文件。`explorer/index.html`、`explorer/vite.config.ts`、`semantica/explorer/`（Python 后端）**禁触**

## Subtask Guidance

### T001: 添加依赖并更新锁文件

**Purpose**: 引入 i18n 运行时，锁文件同步更新。

**Steps**:
1. 在 `explorer/package.json` 的 `dependencies` 中添加（精确版本，不带 `^` 以外的前缀变更；跟随项目现有版本写法）：
   - `"i18next": "^26.4.1"`
   - `"react-i18next": "^17.0.13"`
2. 在 `explorer/` 下运行 `npm install` 更新 `package-lock.json`（不要用 `--no-save`，不要手改锁文件）。
3. 确认 peer 依赖无冲突告警（react 19.2 ✓，i18next ≥26.2 ✓）。

**Files**: `explorer/package.json`、`explorer/package-lock.json`

**Validation**:
- [ ] `npm ls i18next react-i18next` 在 explorer/ 下解析成功且版本正确
- [ ] `package-lock.json` 已更新且与 package.json 一致

### T002: 创建双语资源文件（完整 P0 键清单）

**Purpose**: 建立 en/zh 两份资源，英文为键基准，中文为译文。**键清单是 WP02 的接线契约——必须完整、逐条落实，不许偷工减料。**

**Steps**:
1. 创建 `explorer/src/i18n/locales/en.json`，结构为 `{ "translation": { ...全部键... }, "__meta": {} }`。键为 flat 点号字符串（如 `"nav.explore.label"`）。`__meta` 与 `translation` 同级、留空对象（维持与 zh.json 结构同构，供类型比对）。
2. 创建 `explorer/src/i18n/locales/zh.json`，结构同构：`{ "translation": { ...同键集中文译文... }, "__meta": { "source_version": "<en.json 的 HEAD blob sha，40 位>" } }`。`source_version` 在两个文件都写完后用 `git hash-object explorer/src/i18n/locales/en.json` 或提交后的 `git rev-parse HEAD:<path>` 取得——若文件尚未提交，用 `git hash-object` 的值，并在 WP 完成报告里注明。
3. en 键值 = App.tsx 当前英文原文**逐字保留**（含标点与省略号）。完整键清单：

   **主导航（nav.\*，6 项 × label+hint）**：
   | 键 | en |
   | --- | --- |
   | nav.explore.label / nav.explore.hint | Knowledge Explorer / Graph and vocabulary browsing |
   | nav.analyze.label / nav.analyze.hint | Analyze / Query and inspect the dataset |
   | nav.decisions.label / nav.decisions.hint | Decisions / Decision chains and precedent review |
   | nav.enrich.label / nav.enrich.hint | Enrich / Import, export, and merge workflows |
   | nav.manage.label / nav.manage.hint | Manage / Lineage and governance tooling |
   | nav.ontologyHub.label / nav.ontologyHub.hint | Ontology Hub / Schema governance, registry, and vocabulary management |

   **连接状态（connection.\*）**：connection.checking=`Connecting…`、connection.online=`System Online`、connection.offline=`Backend Unreachable`

   **工作区壳层（shell.\*）**：
   | 键 | en |
   | --- | --- |
   | shell.explore.title / shell.explore.subtitle / shell.explore.kickerGraph / shell.explore.kickerVocab | Explore / Browse the graph and switch views without leaving the workspace. / Graph Studio / Vocabulary Browser |
   | shell.analyze.title / shell.analyze.subtitle / shell.analyze.kickerReasoning / shell.analyze.kickerSparql | Analyze / Query the active graph and test inference rules. / Reasoning Engine / SPARQL Query |
   | shell.decisions.title / shell.decisions.subtitle / shell.decisions.kicker | Decisions / Inspect decision chains, causal context, and precedent matches. / Decision Intelligence |
   | shell.enrich.title / shell.enrich.subtitle / shell.enrich.kicker | Enrich / Import, export, reconcile, and audit graph entities. / Knowledge Audit |
   | shell.ontologyHub.title / shell.ontologyHub.subtitle / shell.ontologyHub.kicker | Ontology Hub / Load, browse, edit, and govern ontologies and vocabularies. / Schema Governance |
   | shell.manage.title / shell.manage.subtitle / shell.manage.kicker | Manage / Review provenance, lineage, ontology, and governance context. / Graph Governance |

   **子视图页签（tabs.\*）**：tabs.explore.graph=`Semantica Explorer`、tabs.explore.vocabulary=`Vocabulary Browser`、tabs.analyze.reasoning=`Reasoning Playground`、tabs.analyze.sparql=`SPARQL Querying`、tabs.enrich.import=`Import and Export`、tabs.enrich.merge=`Diff and Merge`、tabs.enrich.resolve=`Entity Resolution`、tabs.enrich.registry=`Registry`、tabs.manage.lineage=`PROV-O Lineage`、tabs.manage.kgOverview=`KG Overview`、tabs.manage.ontology=`Ontology Summary`

   **加载回退与通用（fallback.\*/common.\*）**：fallback.loading=`Loading workspace…`；common.appTitle=`Semantica Knowledge Explorer`（brand-pill 的 title）

   **首屏（welcome.\*）**：
   | 键 | en |
   | --- | --- |
   | welcome.status.version | Semantica v2 · Semantic Intelligence |
   | welcome.kicker.aria / welcome.kicker.text | Product category / Knowledge Explorer |
   | welcome.titleLine1 / welcome.titleLine2 | Navigate knowledge / like a living system. |
   | welcome.subtitle | Semantica turns dense knowledge graphs into a navigable command center — discovery, reasoning, provenance, distance intelligence, and decision context, all in one interface. |
   | welcome.cta.open / welcome.cta.reasoning | Open Semantica Explorer / Run Reasoning |
   | welcome.preview.aria / welcome.preview.tab | Knowledge graph preview / Semantica Explorer |
   | welcome.command.label / welcome.command.meta | Search command, node, or concept / distance heatmap · focused view · causal path |
   | welcome.dossier.kicker | Entity Dossier |
   | welcome.dossier.distance / welcome.dossier.distanceValue | Distance band / Near |
   | welcome.dossier.coherence | Path coherence |
   | welcome.dossier.provenance / welcome.dossier.provenanceValue | Provenance / Audited |
   | welcome.timeline.title / welcome.timeline.badge | Temporal Evidence / 66% coverage |
   | welcome.metrics.aria | System status |
   | welcome.metrics.nodes / welcome.metrics.nodesFallback | Knowledge nodes / Live |
   | welcome.metrics.edges / welcome.metrics.edgesFallback | Relationships mapped / Ready |
   | welcome.metrics.modes | Graph modes |
   | welcome.metrics.datasetOnline / welcome.metrics.datasetOnlineValue | Dataset online / Active |
   | welcome.metrics.readyToExplore / welcome.metrics.readyToExploreValue | Ready to explore / Standby |
   | welcome.section.aria / welcome.section.title | Workspaces / Workspaces |
   | welcome.card.primary.eyebrow / welcome.card.primary.title | Primary Workspace / Semantica Explorer |
   | welcome.card.primary.desc | Full graph, grouped communities, focused neighborhoods, and distance intelligence — all in one canvas. |
   | welcome.card.vocabulary.label / welcome.card.vocabulary.desc | Vocabulary / Schemes and terms |
   | welcome.card.analyze.label / welcome.card.analyze.desc | Analyze / Inference and queries |
   | welcome.card.decisions.label / welcome.card.decisions.desc | Decisions / Chains and precedents |
   | welcome.card.enrich.label / welcome.card.enrich.desc | Enrich / Import and resolve |
   | welcome.card.manage.label / welcome.card.manage.desc | Manage / Lineage and ontology |
   | welcome.capability.aria / welcome.capability.label | Intelligence capabilities / Intelligence Layer |
   | welcome.capability.heatmap / welcome.capability.neighborhood / welcome.capability.communities / welcome.capability.causalPath / welcome.capability.provenanceDossier | Distance Heatmap / Focused Neighborhood / Grouped Communities / Trace Causal Path / Provenance Dossier |

   注意：`welcome.dossier.title`（NSRP1）与 timeline 年份（1970/2030）是演示数据，**不入键**。上表约 95 键。

4. 中文译文要求：
   - 术语严格遵 `docs/zh/glossary.md`； Ontology Hub 保留英文；"Workspace"译"工作区"（禁"工作台/工作空间"）
   - 品牌串保留：`Semantica v2`、`Semantica Explorer`（产品名整体可译为"Semantica 探索器"或保留英文，二选一后全篇一致——**推荐按钮 CTA 译"打开 Semantica 探索器"，页签名保留 "Semantica Explorer" 以贴近产品名**；无论哪种，welcome.cta.open 的英文键值必须逐字保留 `Open Semantica Explorer`，因为 e2e 按此文案定位）
   - 插值占位符：本清单暂无 `{{}}` 占位符；若你判断某键需要，en/zh 两侧必须同名同数量
   - 标点用中文全角；省略号用 `……`；中英混排空格遵循仓库中文文案惯例（参照 docs/zh/ 现有文档）
5. 两个 JSON 用 2 空格缩进，键序按上表分组排列（nav → connection → shell → tabs → fallback → common → welcome），保持两文件键序一致。

**Files**: `explorer/src/i18n/locales/en.json`（新增）、`explorer/src/i18n/locales/zh.json`（新增）

**Validation**:
- [ ] 两文件均为合法 JSON，键集合完全一致（可用 `python3 -c` 快速比对 flatten 后的键集）
- [ ] en 值与 App.tsx 现有字面量逐字一致（抽查 nav/shell/cta）
- [ ] zh 术语对照 glossary 无违例
- [ ] zh.json `__meta.source_version` 为 40 位十六进制

### T003: 全键类型化（types.d.ts）

**Purpose**: `t()` 键全类型化；zh 缺键 = 编译失败（FR-006）。

**Steps**:
1. 创建 `explorer/src/i18n/types.d.ts`：
   ```ts
   import type en from "./locales/en.json";

   declare module "i18next" {
     interface CustomTypeOptions {
       defaultNS: "translation";
       resources: {
         translation: typeof en.translation;
       };
     }
   }
   ```
2. 在资源组装处（index.ts 或 types 同文件导出）用 `zh satisfies typeof en` 约束 zh 资源（拦 zh 缺键）。zh 多键 `satisfies` 不报错——这由 WP03 的 `extra_keys` 运行时把关，你可再加一个 `keyof` 双向 parity 类型断言做编译期兜底（可选加分项）。
3. `__meta` 放语言码层级（`resources = { en, zh }` 的兄弟位置不进 translation），不会污染键类型。

**Files**: `explorer/src/i18n/types.d.ts`（新增）

**Validation**:
- [ ] 任选一处 `t("nav.explore.label")` 能获得字面量类型补全（临时试验后删除）
- [ ] 从 zh.json 临时删一个键 → `tsc` 报错（验证后恢复）

### T004: 初始化与语言检测（index.ts）

**Purpose**: i18next 初始化 + 四级检测 + 文档语言同步。契约：`contracts/language-detection.md`。

**Steps**:
1. 创建 `explorer/src/i18n/index.ts`：
   - `resolveInitialLanguage()`：按序检测——① `URL ?lang=`（合法值 `en|zh`）；② `localStorage["semantica.explorer.lang"]`（合法值 `en|zh`）；③ `navigator.language` 前缀 `zh`（zh/zh-CN/zh-TW…）→ `zh`；④ 兜底 `en`。任一步读取抛异常（隐私模式）视为未命中继续下一步。非法值一律视为未命中。
   - `i18next.use(initReactI18next).init({ resources, lng: resolveInitialLanguage(), fallbackLng: "en", interpolation: { escapeValue: false }, react: { useSuspense: false } })`。**必须传 `lng`**（零闪烁：不传会先落 fallback 再闪变）。禁止引入 i18next-browser-languagedetector 插件。
2. 文档同步：订阅 `i18n.on("languageChanged", ...)`，同步 `document.documentElement.lang`（zh → `"zh-CN"`，en → `"en"`）与 `document.title`（zh → `"知识探索器 · Semantica"`，en → `"Semantica Knowledge Explorer"`）。初始化命中时也要触发（初始化后手动调用一次同步函数即可）。
3. localStorage 读取与后续写入都包 try/catch；默认导出 i18n 实例，并 `export` 便于类型与测试。

**Files**: `explorer/src/i18n/index.ts`（新增）

**Validation**:
- [ ] `?lang=zh` 强制中文、`?lang=en` 强制英文、非法 `?lang=fr` 落入下一级检测
- [ ] 隐私模式（mock localStorage 抛异常）不崩溃，继续 navigator 检测

### T005: 语言开关组件（LanguageToggle.tsx）

**Purpose**: 头部 中/EN 切换组件（本 WP 只建组件不挂载，WP02 负责挂到 App 头部）。

**Steps**:
1. 创建 `explorer/src/i18n/LanguageToggle.tsx`：
   - 函数组件，内部 `const { i18n } = useTranslation()`；当前语言读 `i18n.resolvedLanguage`（经订阅响应式更新，禁止模块级可变变量）
   - 点击切换：`i18n.changeLanguage(next)`；持久化写 `localStorage["semantica.explorer.lang"] = next`，写失败静默（try/catch，仅本次会话生效）
   - UI：紧凑两态开关（`中` / `EN`），样式内联或复用现有 CSS 变量（`--panel-border`、`--text-muted`、`--accent` 等，见 App.tsx `shellStyles`），不引入新样式体系；`aria-label` 用 `common.appTitle` 不合适，直接用 `t("language.toggle")`——**给 en/zh 各补一个键 `language.toggle`（en: "Switch language", zh: "切换语言"）**，两文件同步加
   - 不自行调 `document.title`/`html lang`（T004 的 languageChanged 监听已统一处理）
2. 组件保持无副作用渲染（React Compiler 友好），切换逻辑放事件回调内。

**Files**: `explorer/src/i18n/LanguageToggle.tsx`（新增）

**Validation**:
- [ ] 点击在 en↔zh 间切换，`useTranslation` 消费方会重渲染（临时挂一个 `t()` 文本试验后删除）
- [ ] localStorage 写入失败（mock 抛异常）不报错

### T006: 入口接线与构建验证

**Purpose**: i18n 模块随应用启动加载，构建门禁通过。

**Steps**:
1. `explorer/src/main.tsx` 顶部加一行 `import "./i18n";`（副作用导入，置于其他导入之后、`createRoot` 之前皆可，遵循现有导入排序风格）。
2. 运行 `cd explorer && npm run build`（tsc -b + vite build）确认零错误；`npm run lint` 零错误。
3. 此时 App.tsx 尚未消费 t()——界面应与改造前完全一致（T002 的键只是"待用"状态）。若 lint 对未使用导出报警，调整导出方式而不是删功能。

**Files**: `explorer/src/main.tsx`

**Validation**:
- [ ] `npm run lint` 零错误
- [ ] `npm run build` 零错误（tsc 键同构检查在此把关）
- [ ] 记录 build 产物 gzip 体积（`du` 或 vite 输出），供 WP04 复核 NFR-002（预算：增量 ≤ 50KB）

## Test Strategy

项目未要求为本 WP 新增单测（spec 未列）；正确性由 tsc 类型检查 + WP04 的 e2e 门禁兜底。手动验证命令如上各 Validation 节。

## Definition of Done

- [ ] T001–T006 全部完成且 Validation 勾稽
- [ ] `explorer/src/i18n/` 含 index.ts、types.d.ts、LanguageToggle.tsx、locales/en.json、locales/zh.json
- [ ] en/zh 键集合一致、术语合规、`__meta` 就位
- [ ] lint + build 零错误，界面（未接线部分）无任何可见变化
- [ ] 零侵入边界未破：只动了 owned_files 内的文件

## Risks

- **tsconfig 的 `resolveJsonModule` 若未开启**：JSON import 无类型，`typeof en` 退化为 any。探索后确认；若 tsconfig 不在 owned_files 内，在完成报告记录并采用 `defineResources` 式的显式类型标注兜底，同时在报告中说明需要一行 tsconfig 跟进。
- **React Compiler 记忆化**：组件内只经 `useTranslation()` 订阅消费语言；不要把 `i18n.language` 提升到模块常量。
- **键清单遗漏**：WP02 接线时若发现缺键，允许小幅越界补 en/zh 两文件（各加一键），并在完成报告记一行理由——不许只加 en 不加 zh（会编译失败，这本身就是护栏）。

## Reviewer Guidance

核对：① en 值与 App.tsx 原文逐字一致（防"顺手润色"破坏 e2e 文案锚点）；② zh 术语对照 glossary；③ 检测顺序与契约一致且每步异常安全；④ 无 eager import 进入包顶层（main.tsx 的一行副作用导入是允许的入口接线）；⑤ `__meta` 不在 translation 键空间内。

## Activity Log

- 2026-09-01T11:01:57Z – claude – shell_pid=37250 – Assigned agent via action command
- 2026-09-01T12:41:09Z – claude – shell_pid=37250 – Ready for review
