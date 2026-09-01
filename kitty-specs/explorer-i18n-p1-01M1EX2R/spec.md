# Specification: Explorer 中文界面 P1（探索工作区）

**Mission**: `explorer-i18n-p1-01M1EX2R` · software-dev · PR-bound
**Branch contract**: 规划与实现均在 `feature/explorer-i18n-p1`，mission merge 时回 `main`
**Date**: 2026-09-02

## Overview

P0 已为 Knowledge Explorer 建立中英双语文案能力（i18n 基础设施 + 全局框架文案）。本轮 P1 将国际化推进到**探索工作区（GraphWorkspace）内部**：搜索栏、分析工具栏、图例、时间轴、Inspector 面板、会话加载与失败面板等约 290 条界面文案，全部纳入中英双语资源并受既有键同构机制约束。同时对 401 等高频 API 错误增加前端中文包装提示（后端 detail 原文保留展示）。

前端 API key 认证界面（设 key 后前端无法登录的部署缺口）经确认**不在本 mission 范围**，另行立项。

## User Scenarios & Testing

### 主流程（探索工作区语言切换）

中文用户打开探索工作区（图谱工作室页签）→ 搜索栏、工具栏分组与按钮、图例、时间轴、Inspector 面板全部显示中文 → 点击语言开关切换英文 → 工作区内部文案立即变英文（页面不刷新）→ 刷新后保持英文。

### 异常路径

- 图谱会话加载失败：失败面板标题、说明与重试按钮以当前语言显示。
- 后端不可达：连接状态与错误提示以当前语言显示。
- API 返回 401：界面显示中文包装提示（如"认证失败：API key 无效或缺失"），后端返回的 detail 原文仍可见，便于排查。

### 边界情况

- 图数据驱动的值不翻译：节点/边 label、实体类型缩写（ORG/PERSON/PRODUCT 等来自数据）保持原样；图例中的固定枚举标签（前端映射表定义）属界面文案，须翻译。
- 禁用本地存储：语言偏好不可持久化时回落自动检测，切换功能不受影响（P0 行为回归确认）。
- 英文偏好用户：探索工作区可见文案与改造前完全一致（数据值豁免同口径）。

## Requirements

### Functional Requirements

| ID | Requirement | Status |
| --- | --- | --- |
| FR-001 | 探索工作区内部全部界面文案中英双语：搜索栏（占位与按钮）、工具栏分组标签与动作按钮（CAMERA/LAYOUT/ANALYSIS/UTILITY 分组及 Effects/Neighbors/Temporal/Run 等）、图例框架文案与固定枚举标签（Biomolecule/Condition/Compound/Process/Community/Other 等）、底部时间轴（标题、播放控制、刻度框架文案）、Inspector 面板、会话加载态与加载失败面板（含重试按钮） | Clear |
| FR-002 | 语言切换时工作区内部文案立即以目标语言重新显示，全程无需刷新页面 | Clear |
| FR-003 | API 返回 401 等高频错误时，界面显示中文包装提示；后端 detail 原文保留可见，不得篡改或丢失 | Clear |
| FR-004 | 任一译文缺失时该处显示英文原文，不得显示键名或空白（沿用 P0 回落机制） | Clear |
| FR-005 | 中文与英文文案资源键集合一致；任一侧缺键在构建（类型检查）阶段即失败（沿用 P0 机制） | Clear |
| FR-006 | 页面语言属性与浏览器标签页标题随语言同步（P0 行为回归保持） | Clear |
| FR-007 | 图数据驱动值（节点/边 label、实体类型枚举值）不进入文案资源、不参与翻译 | Clear |
| FR-008 | 既有自动化测试（graph-store、graph-workspace、plugin-registry、deterministic-e2e）全部通过；e2e 英文预置行为不变 | Clear |
| FR-009 | 译文过期追踪脚本对本期产出报告 fresh | Clear |

### Non-Functional Requirements

| ID | Requirement | Status |
| --- | --- | --- |
| NFR-001 | 语言切换在 1 秒内完成探索工作区范围全部文案更新，且不触发页面重载 | Clear |
| NFR-002 | 构建产物（gzip 计）相对改造前的体积增量 ≤ 30KB | Clear |
| NFR-003 | P1 范围中文文案与术语表一致率 100%（含"探索"定名，禁用"知识探索器"） | Clear |
| NFR-004 | 既有自动化测试全部通过；lint 与类型检查相对改造前零增量（不引入新错误） | Clear |

### Constraints

| ID | Constraint | Status |
| --- | --- | --- |
| C-001 | 零侵入边界：允许修改的上游文件仅限探索工作区组件（`explorer/src/workspaces/GraphWorkspace/**`，文案抽取所及）、i18n 资源与类型定义、既有测试的定位器/预置行、依赖清单（预期零新增）；其余改动必须以新增文件落地 | Clear |
| C-002 | 禁触区：Python 后端、静态入口 HTML、构建配置、其他工作区（分析/决策/增强/管理/Ontology Hub）、认证流程（API key 界面另行立项）；后端 detail 原文保持英文，仅前端包装文案可译 | Clear |
| C-003 | 语言状态必须经响应式机制传播到已渲染界面（编译期自动记忆化，可变全局变量不可靠） | Clear |
| C-004 | 中文术语以 `docs/zh/glossary.md` 为唯一基准；产品名（Ontology Hub、Semantica Explorer 字标）按术语表保留英文 | Clear |
| C-005 | 本期不新增任何依赖 | Clear |
| C-006 | 图数据值不进文案资源文件（运行时数据与界面文案分离） | Clear |

## Success Criteria

1. 中文用户打开探索工作区，FR-001 范围文案 100% 显示中文（逐屏走查 0 处英文残留，数据值豁免）。
2. 点击语言开关后工作区内部文案 100% 即时切换、无需刷新；重开应用后语言保持。
3. 英文偏好用户的探索工作区可见界面与改造前完全一致（文案层对比走查 0 处差异）。
4. 模拟 401 响应时界面出现中文包装提示，detail 原文完整可见。
5. 全部既有自动化测试通过；术语一致率 100%；过期检查脚本报告 fresh。

## Key Entities

- **语言偏好**：用户界面语言选择，仅存浏览器本地（P0 已实现，本轮复用）。
- **文案资源**：稳定键组织的界面文案，中英各一份，英文为键基准；P1 新增工作区命名空间的键。
- **图例枚举映射**：前端固定的实体形状/类型展示映射，其标签属界面文案，进资源文件。
- **过期状态记录**：中文资源内记录翻译时的英文基准版本号，供过期检查脚本比对。

## Domain Language

术语基准：`docs/zh/glossary.md`。P1 相关核心对照：

| English | 中文（冻结） |
| --- | --- |
| Knowledge Explorer | 探索（2026-09 定名，不用"知识探索器"） |
| Graph Workspace | 图谱工作室 |
| Inspector | 检查器 |
| Temporal | 时态 |
| Provenance | 溯源 |
| Reasoning | 推理 |
| Workspace | 工作区（不用"工作台/工作空间"） |
| Ontology Hub | Ontology Hub（产品名保留英文） |

## 决策记录

| 决策 | 结论 | 理由与必须保持为真的约束 |
| --- | --- | --- |
| P1 范围 | 仅探索工作区（~290 条） | 用户 2026-09-02 确认；其余工作区留 P2，控制 mission 体积与验收成本 |
| 认证 UI | 不并入，另行立项 | 用户确认；本 mission 保持 i18n 单一职责，本地部署以匿名模式过渡 |
| 401 错误包装 | 随 P1 做（自 P3 提前） | 用户确认；部署高频遇到，前端包装符合零侵入（detail 原文保留） |
| 分支策略 | 沿用 P0：feature 分支 PR-bound，完成后本地 merge 回 main，不自动 push | 用户确认 |

## Assumptions

- 约 290 条为 P0 期估算；实际以抽取清单为准，越界补键沿用 tasks.md Execution Notes 汇总模式。
- 图例固定枚举（前端映射表常量）全部进资源文件，按 FR-007 与数据值区分。
- deterministic-e2e 锚点若受文案抽取影响，仅允许最小调整定位器（优先 data-testid），调整须在 PR 描述显式说明。
- 日期/数字格式沿用浏览器默认区域行为，本期不显式接管。

## Out of Scope（后续路线，非本期目标）

- P2：OntologyWorkspace（约 350 条）及分析/决策/增强/管理等工作区内部文案分批翻译。
- API key 认证界面：key 输入/存储/附带 X-API-Key 的前端流程（独立任务）。
- P3：注册表审计 summary 的渲染时翻译、后端 detail 错误消息的全面错误码映射。
