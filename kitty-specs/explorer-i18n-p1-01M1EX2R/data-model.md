# Data Model: Explorer 中文界面 P1（探索工作区）

本 mission 无持久化数据模型变更。唯一"数据"是前端文案资源键空间，模型如下。

## 实体：文案资源键（Translation Key）

| 字段 | 说明 | 约束 |
| --- | --- | --- |
| key | 点号分层名，如 `graph.timeline.play` | 新增键一律 `graph.*` 前缀（浅两级）；全局/框架键不在本期范围 |
| en value | 原文英文（抽取处原文） | 与改造前英文用户所见逐字一致（FR-006 英文不变口径） |
| zh value | 中文译文 | 术语依 `docs/zh/glossary.md`；"探索"定名（NFR-003） |
| `__meta.source_version` | zh.json 顶层元键，翻译时的 en.json git blob sha | i18next 忽略；收尾刷新保证 FR-009 fresh |

### 不变量

- **INV-1（键同构）**：`zh.translation satisfies typeof en.translation`——任一侧缺键/多键在 `tsc` 构建期报错（P0 既有机制，零改动沿用）。
- **INV-2（回落）**：键存在但译文缺失时 i18next `fallbackLng: 'en'` 显示英文，永不显示键名/空白（FR-004）。
- **INV-3（数据值隔离）**：节点/边 label、实体类型枚举值等运行时数据不进资源文件（C-006/FR-007）；图例固定枚举的 label 是键名引用，不是数据值。

## 实体：API 错误包装（apiError.ts 输出）

| 字段 | 说明 | 约束 |
| --- | --- | --- |
| wrapper | 中文包装提示，如"认证失败：API key 无效或缺失" | 按状态码映射（401/403/5xx/网络错误），进 `graph.errors.*` 键空间 |
| detail | 后端返回的 detail 原文 | 原样保留展示，不截断不改写（FR-003）；缺失时省略该段 |

状态转换：无（纯函数，响应 → { wrapper, detail }，渲染点消费）。

## 关系

- 键空间扩展不改变 P0 已有 107 键；`graph.*` 为增量命名空间。
- `ui_zh_status.py` 以 en.json blob sha 为基准比对 `__meta.source_version`，输出 fresh/stale——模型不变，本期只刷新值。
