# Data Model: Explorer 中文界面 P2（剩余工作区全量）

本 mission 无持久化数据模型变更。唯一"数据"是前端文案资源键空间，模型如下（沿用 P1 模型，扩展键段）。

## 实体：文案资源键（Translation Key）

| 字段 | 说明 | 约束 |
| --- | --- | --- |
| key | 点号分层扁平名，如 `ontologyHub.registry.loadOntology` | 新增键按工作区分段：reasoning/sparql/decision/importExport/diffMerge/entityResolution/registry/lineage/kgOverview/ontologySummary/ontologyHub/vocabulary |
| en value | 原文英文（抽取处原文） | 与改造前英文用户所见逐字一致（英文不变口径） |
| zh value | 中文译文 | 术语依 `docs/zh/glossary.md`；标准名 SPARQL/SHACL/SKOS/OWL/PROV-O 保留 |
| `__meta.source_version` | zh.json 顶层元键，翻译时的 en.json git blob sha | i18next 忽略；收尾刷新保证 FR-012 fresh |

### 不变量

- **INV-1（键同构）**：`zh.translation satisfies typeof en.translation`——任一侧缺键/多键在 `tsc` 构建期报错（P0 既有机制，零改动沿用）。
- **INV-2（回落）**：键存在但译文缺失时 i18next `fallbackLng: 'en'` 显示英文，永不显示键名/空白（FR-007）。
- **INV-3（数据值隔离）**：本体 URI、实体/类别枚举值、文件名、查询模板内容等运行时数据不进资源文件（C-006/FR-010）。
- **INV-4（P1 面不回归）**：既有 414 键（nav/shell/tabs/welcome/graph.* 等）值零改动；新增键为纯增量。

## 实体：API 错误包装（既有 apiError.ts，复用不改）

| 字段 | 说明 | 约束 |
| --- | --- | --- |
| wrapper | 中文包装提示（按状态码映射） | P1 已建，本期仅新增消费点，不新增键（graph.errors.* 复用） |
| detail | 后端返回的 detail 原文 | 原样保留展示（C-002）；缺失时省略该段 |

## 关系

- 键空间扩展不改变 P0/P1 已有 414 键；新增工作区段为纯增量命名空间。
- `ui_zh_status.py` 以 en.json blob sha 为基准比对 `__meta.source_version`，输出 fresh/stale——模型不变，本期只刷新值。
