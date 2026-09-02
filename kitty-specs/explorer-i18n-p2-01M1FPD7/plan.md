# Implementation Plan: Explorer 中文界面 P2（剩余工作区全量）

**Branch**: `feature/explorer-i18n-p2` | **Date**: 2026-09-02 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/kitty-specs/explorer-i18n-p2-01M1FPD7/spec.md`

## Summary

把剩余全部工作区（分析：推理引擎与 SPARQL；决策；增强：导入导出/差异合并/实体消解/注册表；管理：PROV-O 谱系/KG 概览/本体概要；Ontology Hub 全部页签；SKOS 词表）约 26 个文件、估计 850+ 条界面文案接入既有 i18n 基础设施（i18next 26.4.1 + react-i18next 17.0.13，键同构构建期校验，零新增依赖）。技术路线沿用 P0/P1 先例：字面量 → `t()` 抽取（函数组件用 `useTranslation`，模块级常量留结构、label 改键引用）；数据驱动值（本体 URI、类别枚举值、文件名）不进资源；既有四套测试与 deterministic-e2e 零文案耦合（已核查），预期测试文件零改动。

## Technical Context

**Language/Version**: TypeScript ~5.x（strict + `erasableSyntaxOnly`）+ React 19 + Vite，Node 18+/npm 9+
**Primary Dependencies**: i18next 26.4.1、react-i18next 17.0.13（P0 已就位，本期零新增）
**Storage**: N/A（语言偏好存浏览器 localStorage `semantica.explorer.lang`；图数据为内存 ContextGraph）
**Testing**: `node --test` + tsx 单测套件（graph-workspace / graph-store / plugin-registry / deterministic-rendering）+ Playwright deterministic-e2e（`npm run test:deterministic-e2e`）
**Target Platform**: 现代浏览器 SPA；构建产物打进 `semantica/static/` 随 wheel 分发
**Project Type**: web（前端单页应用，Explorer 前端目录 `explorer/`）
**Performance Goals**: 语言切换 <1s 完成全部工作区文案更新、不重载页面（NFR-001）；构建产物 gzip 增量 ≤60KB（NFR-002）
**Constraints**: C-001 零侵入（仅改 C-001 白名单工作区组件、i18n 资源与类型、既有测试定位器/预置行）；C-002 禁触后端/静态入口/GraphWorkspace/认证流程；C-003 响应式语言状态（React Compiler 下禁用可变全局变量）；C-004 术语以 `docs/zh/glossary.md` 为准；C-005 零新增依赖；C-006 数据值不进资源文件
**Scale/Scope**: 10 个工作区目录 26 文件、约 8400 行、估计 850+ 条文案；键空间新增 reasoning.* / sparql.* / decision.* / importExport.* / diffMerge.* / entityResolution.* / registry.* / lineage.* / kgOverview.* / ontologySummary.* / ontologyHub.* / vocabulary.* 等 `workspaces.*` 一级分段（见 IC-06）

## Charter Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Charter（compact 模式已加载）关键原则对照：

| 原则 | 对照结论 |
| --- | --- |
| 简单优先（Simple First） | 沿用 P0/P1 既有 i18next 机制与抽取模式，不引入新抽象层。PASS |
| 零侵入/开闭原则 | 改动面收敛于 C-001 白名单（剩余工作区组件 + i18n 资源）；后端零改动。PASS |
| 测试纪律（Testing Discipline） | 既有四套测试必须全绿（FR-011）；已核查 e2e/单测与 P2 范围文案零耦合，预期测试文件零改动。PASS |
| 可观察性 | 语言切换经 `languageChanged` 事件传播（P0 已实现），本期为消费侧扩展。PASS |

无 charter 冲突，无需 Complexity Tracking 豁免。

## Project Structure

### Documentation (this mission)

```
kitty-specs/explorer-i18n-p2-01M1FPD7/
├── plan.md              # This file (/spec-kitty.plan command output)
├── research.md          # Phase 0 output (/spec-kitty.plan command)
├── data-model.md        # Phase 1 output (/spec-kitty.plan command)
├── quickstart.md        # Phase 1 output (/spec-kitty.plan command)
└── tasks.md             # Phase 2 output (/spec-kitty.tasks command - NOT created by /spec-kitty.plan)
```

contracts/ 不适用：本 mission 无 API 契约变更（前端消费既有端点，后端禁触）。

### Source Code (repository root)

```
explorer/src/
├── i18n/
│   ├── index.ts                  # P0 既有，本期不动（检测/fallback/同构校验不变）
│   ├── apiError.ts               # P1 既有，本期不动（错误包装已被各工作区按需复用）
│   └── locales/
│       ├── en.json               # 扩展 workspaces.* 键段（英文键基准，值为原文英文）
│       └── zh.json               # 同步中文译文 + 收尾刷新 __meta.source_version
├── ui/primitives.tsx             # 仅当走查发现用户可见英文默认值时抽取（预期零或极小改动）
└── workspaces/                   # C-001 白名单内：文案抽取（GraphWorkspace 除外）
    ├── ReasoningWorkspace.tsx            # 推理引擎页（~243 行）
    ├── SparqlWorkspace/SparqlWorkspace.tsx        # SPARQL 查询页（~271 行）
    ├── DecisionWorkspace/DecisionWorkspace.tsx    # 决策页（~279 行）
    ├── ImportExportWorkspace/ImportExportWorkspace.tsx  # 导入导出（~196 行）
    ├── DiffMergeWorkspace/DiffMergeWorkspace.tsx        # 差异与合并（~121 行）
    ├── EnrichWorkspace/{EntityResolutionTab,RegistryTab}.tsx  # 实体消解/注册表（~738 行）
    ├── LineageWorkspace/LineageDiagram.tsx              # PROV-O 谱系（~177 行）
    ├── ManageWorkspace/{KGOverviewTab,OntologySummaryTab}.tsx # KG 概览/本体概要（~637 行）
    ├── OntologyWorkspace/               # Ontology Hub 11 文件（~5200 行，体量最大）
    └── VocabularyWorkspace/             # SKOS 词表 5 文件（~487 行）
```

**Structure Decision**: 全部改动落在 C-001 白名单内（剩余工作区组件 + i18n 资源）；本期预期零新增文件（apiError.ts 已存在可复用）。不建新目录层级，不设独立翻译中间层。

## Implementation Concern Map

*This mission has multiple distinct architectural areas; concerns below inform task decomposition.*

> **Note**: Implementation concerns are NOT work packages and are NOT executable units.
> `/spec-kitty.tasks` translates these into executable WPs — one concern may become
> multiple WPs; multiple small concerns may merge into one WP. Do not label concerns
> with WP-style IDs or sequencing language.

### IC-01 — 轻量工作区抽取（分析 + 决策）

- **Purpose**: 推理引擎、SPARQL 查询、决策三页文案抽取，覆盖用户高频分析路径。
- **Relevant requirements**: FR-001、FR-002
- **Affected surfaces**: `workspaces/ReasoningWorkspace.tsx`、`workspaces/SparqlWorkspace/SparqlWorkspace.tsx`、`workspaces/DecisionWorkspace/DecisionWorkspace.tsx`
- **Sequencing/depends-on**: none（键段先行由 IC-06 定义）
- **Risks**: 推理/SPARQL 页含代码示例文本（facts/rules 语法示例、SPARQL 查询模板）——示例值属数据/代码不译，仅框架文案入键；SPARQL 关键字（SELECT/WHERE）与模板查询内容保持原样。

### IC-02 — 增强工作区四页签

- **Purpose**: 导入导出、差异与合并、实体消解、注册表页签文案抽取。
- **Relevant requirements**: FR-003
- **Affected surfaces**: `workspaces/ImportExportWorkspace/`、`workspaces/DiffMergeWorkspace/`、`workspaces/EnrichWorkspace/{EntityResolutionTab,RegistryTab}.tsx`
- **Sequencing/depends-on**: none
- **Risks**: 拖放区支持格式（.json/.csv）为数据值；导出格式枚举（JSON/CSV 按钮）为固定 UI 枚举属界面文案——边界在走查中逐项判定；注册表审计 summary 若为调用时拼好的英文数据串，按 Non-goal 豁免并记录（渲染时翻译仅当实现成本低时随本期做，否则记 Execution Notes）。

### IC-03 — 管理工作区三页签

- **Purpose**: PROV-O 谱系、KG 概览、本体概要页签文案抽取。
- **Relevant requirements**: FR-004
- **Affected surfaces**: `workspaces/LineageWorkspace/LineageDiagram.tsx`、`workspaces/ManageWorkspace/{KGOverviewTab,OntologySummaryTab}.tsx`
- **Sequencing/depends-on**: none
- **Risks**: KG 概览的统计卡（NODES/EDGES/DENSITY）与类型分布标签为界面文案；节点/边类型枚举值（ORG/DATE/part_of 等来自数据）不译；"PROV-O Lineage Viewer" 标题含标准名 PROV-O 按术语表保留。

### IC-04 — Ontology Hub 全部页签

- **Purpose**: Ontology Hub 11 文件（注册表/编辑器/版本/对齐/健康/SHACL 工作室/提案评审/SKOS 词表管理器）文案抽取，本期体量最大（约 5200 行）。
- **Relevant requirements**: FR-005
- **Affected surfaces**: `workspaces/OntologyWorkspace/`（index.tsx、OntologyManager、OntologyLoader、OntologySearch、OntologyEditor、AlignmentsTab、VersionsTab、HealthTab、ShaclStudio、ProposalReview、SKOSVocabularyManager）
- **Sequencing/depends-on**: none（与 IC-01~03 无文件交集，可并行规划；实现按串行链推进）
- **Risks**: 体量最大，须按页签拆分多个工作包；SHACL/OWL/SKOS 等标准名与本体 URI 不译；表单校验错误提示量大且重复，优先共用键。

### IC-05 — 词表工作区与全局清扫

- **Purpose**: SKOS 词表 5 文件抽取 + 全局残留英文兜底扫描（`ui/primitives.tsx`、`workspaces/GraphWorkspace/SigmaSceneAdapter.tsx`、非组件层）。
- **Relevant requirements**: FR-006 支撑（全站收口完整性）
- **Affected surfaces**: `workspaces/VocabularyWorkspace/`、`ui/primitives.tsx`（仅文案默认值）
- **Sequencing/depends-on**: 在 IC-01~04 完成后执行，作为收口清扫
- **Risks**: 词表页文案极少（估约 13 条）；清扫阶段若发现 GraphWorkspace 内遗漏，属 P1 回归，修复须单独记录并保持 GraphWorkspace 最小改动。

### IC-06 — 资源键空间扩展与同构校验

- **Purpose**: 新增键段命名定稿、en/zh 双侧同步、构建期同构校验、过期追踪刷新。
- **Relevant requirements**: FR-007、FR-008、FR-012（回落/同步为既有机制回归）
- **Affected surfaces**: `explorer/src/i18n/locales/{en,zh}.json`、`tools/i18n/ui_zh_status.py`（只运行不修改）
- **Sequencing/depends-on**: 键段命名先行定义（各抽取 IC 依赖）；收尾刷新 source_version 依赖全部抽取完成
- **Risks**: 键量约 P1 的 3 倍，gzip 增量预算 60KB 需在收尾实测确认；`zh satisfies typeof en` 保证缺译不可能进产物。

### IC-07 — 既有测试锚点保护

- **Purpose**: 确保四套测试与 deterministic-e2e 在文案抽取后全绿、英文预置行为不变。
- **Relevant requirements**: FR-011
- **Affected surfaces**: `explorer/tests/`（预期零改动；如 e2e 锚点受影响仅允许最小定位器调整并显式记录）
- **Sequencing/depends-on**: 随各抽取 IC 验证；收尾全量复跑
- **Risks**: 已核查 e2e 仅锚定 `Semantica Explorer` 与 `Zoom In`（P0/P1 范围），P2 范围文案零测试耦合；风险主要来自组件结构重构误伤，抽取时保持 DOM 结构与 role/aria 不变。

## Complexity Tracking

无 charter 冲突，无需豁免。
