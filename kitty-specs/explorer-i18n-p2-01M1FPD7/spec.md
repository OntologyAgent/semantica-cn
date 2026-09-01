# Specification: Explorer 中文界面 P2（剩余工作区全量）

**Mission**: `explorer-i18n-p2-01M1FPD7` · software-dev · PR-bound
**Branch contract**: 规划与实现均在 `feature/explorer-i18n-p2`，mission merge 时回 `main`
**Date**: 2026-09-02

## Overview

P0 建立了 Knowledge Explorer 的中英双语文案能力（i18n 基础设施 + 全局框架），P1 覆盖了探索工作区（GraphWorkspace）。本轮 P2 把国际化推进到**剩余全部工作区**，完成全站中文化收口：分析（推理引擎、SPARQL 查询）、决策、增强（导入导出、差异与合并、实体消解、注册表）、管理（PROV-O 谱系、KG 概览、本体概要）、Ontology Hub（注册表/编辑器/版本/对齐/健康/SHACL 工作室全部页签）与 SKOS 词表，约 26 个文件、估计 850+ 条用户可见文案。

用户指令为"仍然有很多页面没有翻译，充分挖掘后，继续完成"——即全量收口，不留 P3 文案批次。API key 认证界面维持 P1 决策（另行立项）不在本期。

## User Scenarios & Testing

### 主流程（剩余工作区语言切换）

中文用户依次打开分析、决策、增强、管理、Ontology Hub、词表各工作区 → 各页签内部文案（标题、分组标签、按钮、占位符、空态、表格表头、对话框、开关与提示）全部显示中文 → 点击语言开关切换英文 → 全部文案立即变英文（页面不刷新）→ 刷新后保持。

### 异常路径

- 操作失败（推理执行失败、导入解析失败、加载本体失败、SHACL 校验失败等）：失败提示以当前语言显示，后端返回的 detail 原文保留可见。
- 空数据态（无决策、无本体、无版本、无对齐等）：空态标题与引导文案以当前语言显示。

### 边界情况

- 数据驱动值不翻译：本体 URI、实体名、类别枚举值（OWL/SKOS/INTERNAL/EXTERNAL 等过滤器值）、文件名、错误码原样显示；其周围的框架文案（标签、说明、按钮）属界面文案，须翻译。
- 英文偏好用户：各工作区可见文案与改造前完全一致（数据值豁免同口径）。
- 模块级组件或非 hook 上下文（若有）：沿用 `i18next.t()` 直调模式，接受已知的切换周期滞后窗口（P1 已披露的同类限制）。

## Requirements

### Functional Requirements

| ID | Requirement | Status |
| --- | --- | --- |
| FR-001 | 分析工作区全部界面文案中英双语：推理引擎页（前向链标题、快捷模板、事实/规则编辑区、写入推断开关、运行按钮、结果面板与空态）与 SPARQL 查询页（编辑器框架、执行按钮、结果表与错误提示） | Clear |
| FR-002 | 决策工作区全部界面文案中英双语：决策列表、过滤框、空态、详情面板（决策链、因果上下文、先例匹配等） | Clear |
| FR-003 | 增强工作区四个页签全部界面文案中英双语：导入与导出（拖放区、格式说明、上传/下载按钮）、差异与合并、实体消解、注册表 | Clear |
| FR-004 | 管理工作区三个页签全部界面文案中英双语：PROV-O 谱系（输入框、Trace 按钮、导出按钮、谱系图空态）、KG 概览（统计卡、类型分布、高度连接节点、刷新）、本体概要 | Clear |
| FR-005 | Ontology Hub 全部页签界面文案中英双语：注册表（搜索、过滤、加载本体、空态）、编辑器、版本、对齐、健康、SHACL 工作室、提案评审、SKOS 词表管理器 | Clear |
| FR-006 | 语言切换时上述全部文案立即以目标语言重新显示，全程无需刷新页面 | Clear |
| FR-007 | 任一译文缺失时该处显示英文原文，不得显示键名或空白（沿用既有回落机制） | Clear |
| FR-008 | 中文与英文文案资源键集合一致；任一侧缺键在构建（类型检查）阶段即失败（沿用既有机制） | Clear |
| FR-009 | 页面语言属性与浏览器标签页标题随语言同步（既有行为回归保持） | Clear |
| FR-010 | 数据驱动值（本体 URI、实体/类别枚举值、文件名、节点/边 label）不进入文案资源、不参与翻译 | Clear |
| FR-011 | 既有自动化测试（graph-store、graph-workspace、plugin-registry、deterministic-e2e）全部通过；e2e 英文预置行为不变 | Clear |
| FR-012 | 译文过期追踪脚本对本期产出报告 fresh | Clear |

### Non-Functional Requirements

| ID | Requirement | Status |
| --- | --- | --- |
| NFR-001 | 语言切换在 1 秒内完成上述全部工作区文案更新，且不触发页面重载 | Clear |
| NFR-002 | 构建产物（gzip 计）相对改造前的体积增量 ≤ 60KB（本期新增键约为 P1 的 3 倍，P1 实测增量 9.8KB/307 键） | Clear |
| NFR-003 | 本期中文文案与术语表一致率 100%（沿用"探索/Ontology Hub"等既有定名） | Clear |
| NFR-004 | 既有自动化测试全部通过；lint 与类型检查相对改造前零增量（不引入新错误） | Clear |

### Constraints

| ID | Constraint | Status |
| --- | --- | --- |
| C-001 | 零侵入边界：允许修改的上游文件仅限剩余工作区组件（`explorer/src/workspaces/{ReasoningWorkspace.tsx,DecisionWorkspace/**,DiffMergeWorkspace/**,EnrichWorkspace/**,ImportExportWorkspace/**,LineageWorkspace/**,ManageWorkspace/**,OntologyWorkspace/**,SparqlWorkspace/**,VocabularyWorkspace/**}` 及 `ui/primitives.tsx` 仅限文案默认值抽取）、i18n 资源与类型定义、既有测试的定位器/预置行；依赖清单预期零新增 | Clear |
| C-002 | 禁触区：Python 后端、静态入口 HTML、构建配置、GraphWorkspace（P1 已收口）、认证流程（API key 界面另行立项）；后端 detail 原文保持英文，仅前端包装文案可译 | Clear |
| C-003 | 语言状态必须经响应式机制传播到已渲染界面（编译期自动记忆化，可变全局变量不可靠） | Clear |
| C-004 | 中文术语以 `docs/zh/glossary.md` 为唯一基准；产品名（Ontology Hub、Semantica 字标、SPARQL、SHACL、PROV-O、SKOS、OWL）按术语表保留英文 | Clear |
| C-005 | 本期不新增任何依赖 | Clear |
| C-006 | 图数据值不进文案资源文件（运行时数据与界面文案分离） | Clear |

## Success Criteria

1. 中文用户逐屏走查分析/决策/增强/管理/Ontology Hub/词表全部页签，界面文案 100% 显示中文（0 处英文残留，数据值豁免）。
2. 点击语言开关后上述文案 100% 即时切换、无需刷新；重开应用后语言保持。
3. 英文偏好用户的全部工作区可见界面与改造前完全一致（文案层对比走查 0 处差异）。
4. 全部既有自动化测试通过；术语一致率 100%；过期检查脚本报告 fresh。
5. 构建产物 gzip 增量 ≤ 60KB；lint/类型检查零增量。

## Key Entities

- **文案资源**：稳定键组织的界面文案，中英各一份，英文为键基准；本期新增各工作区命名空间键段（如 reasoning.*、sparql.*、decision.*、importExport.*、diffMerge.*、entityResolution.*、registry.*、lineage.*、kgOverview.*、ontologySummary.*、ontologyHub.*、vocabulary.*，命名以 plan 阶段定稿为准）。
- **语言偏好**：浏览器本地存储（既有，复用）。
- **过期状态记录**：中文资源内记录翻译时的英文基准版本号，供过期检查脚本比对（既有，需刷新）。

## Domain Language

术语基准：`docs/zh/glossary.md`。本期相关核心对照（沿用既有定名）：

| English | 中文（冻结） |
| --- | --- |
| Knowledge Explorer | 探索（2026-09 定名，不用"知识探索器"） |
| Workspace | 工作区（不用"工作台/工作空间"） |
| Reasoning | 推理 |
| Decision Intelligence | 决策智能 |
| Entity Resolution | 实体消解 |
| Provenance / PROV-O | 溯源 / PROV-O（标准名保留） |
| Ontology | 本体 |
| Ontology Hub | Ontology Hub（产品名保留英文） |
| SPARQL / SHACL / SKOS / OWL | 保留英文（W3C 标准名） |
| Registry | 注册表 |
| Lineage | 谱系 |
| Import / Export | 导入 / 导出 |

## 决策记录

| 决策 | 结论 | 理由与必须保持为真的约束 |
| --- | --- | --- |
| P2 范围 | 剩余全部工作区一次收口 | 用户 2026-09-02 指令"充分挖掘后，继续完成"；不留 P3 文案批次 |
| 认证 UI | 继续排除，另行立项 | 维持 P1 决策；本 mission 保持 i18n 单一职责 |
| 分支策略 | 沿用 P0/P1：feature 分支 PR-bound，完成后本地 merge 回 main，不自动 push | 用户既定先例 |
| 键命名空间 | 按工作区新增键段，具体段名 plan 阶段定稿 | 与既有 graph.* 段并列，避免键冲突 |

## Assumptions

- 约 850+ 条为 P0/P1 口径估算（引号字符串 × UI 占比），实际以抽取清单为准；越界补键沿用 tasks.md Execution Notes 汇总模式。
- Ontology Hub 体量最大（11 文件约 5200 行），实现时按页签分组推进，每组成员在 tasks 阶段定稿。
- deterministic-e2e 与既有测试锚点若受文案抽取影响，仅允许最小调整定位器（优先 data-testid），调整须在 PR 描述显式说明。
- 日期/数字格式沿用浏览器默认区域行为，本期不显式接管。
- `ui/primitives.tsx` 预期仅含少量文案默认值；若走查证实无用户可见英文则零改动。

## Out of Scope（非本期目标）

- API key 认证界面：key 输入/存储/附带 X-API-Key 的前端流程（独立任务）。
- 后端 detail 错误消息的全面错误码映射（维持 P1 的前端包装 + 原文透传口径）。
- Sigma 画布上的节点/边 label（后端数据，非 chrome）。
- 注册表审计 summary 的渲染时翻译（若抽取中发现随本期一并处理，在 Execution Notes 记录）。
