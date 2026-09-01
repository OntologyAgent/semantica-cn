# Data Model: Explorer 中文界面 P0

**Mission**: `explorer-i18n-p0-01M1DZFC` · 2026-09-01

本 mission 无服务端数据变更；全部实体存在于前端资源与浏览器本地。

## 实体

### 1. LanguagePreference（语言偏好）

| 字段 | 类型 | 存储 | 说明 |
| --- | --- | --- | --- |
| lang | `"en" \| "zh"` | `localStorage["semantica.explorer.lang"]` | 用户显式选择的语言；不存在 = 未做过选择 |

- **生命周期**：语言开关切换时写入；读取失败（隐私模式/禁用存储）视为不存在，功能降级到自动检测。
- **不变量**：只存两值之一；非法值按不存在处理（回落检测）。

### 2. LocaleResource（文案资源）

| 字段 | en.json | zh.json | 说明 |
| --- | --- | --- | --- |
| 键集合 | 基准（single source of truth） | 必须与 en 完全一致 | flat 点号键，区域前缀：`nav.*`、`tabs.*`、`welcome.*`、`connection.*`、`shell.*`、`fallback.*`、`error.*`、`common.*` |
| 值 | 英文原文 | 中文译文 | 插值占位符用 i18next `{{name}}` 语法；两侧占位符集合必须一致 |
| `__meta` | 空对象 `{}`（维持两文件结构同构，供 `satisfies` 键比对） | `{ "source_version": "<40位 blob sha>" }` | 与 `translation` namespace 同级，不进入 `translation` 键空间；记录翻译时 `en.json` 的 HEAD blob sha |

**不变量**：
- INV-1（键同构）：任一侧缺键 = 类型检查失败（FR-006）。
- INV-2（回落安全）：运行时任一取译失败回落英文原文，绝不渲染键名或空白（FR-005）。
- INV-3（占位符对齐）：`{{name}}` 占位符在 en/zh 同键下必须同名同数量。
- INV-4（术语冻结）：zh 值遵 `docs/zh/glossary.md`；产品名（Ontology Hub 等）保留英文（C-004）。

### 3. StalenessRecord（过期状态条目，`ui_zh_status.py` 输出）

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| path | string | 固定 `explorer/src/i18n/locales/zh.json` |
| status | `fresh \| stale \| orphan` | fresh: sha 一致；stale: sha 不一致/缺失/非法；orphan: en.json 已从 HEAD 删除 |
| recorded_source_sha | string\|null | `__meta.source_version` |
| current_source_sha | string\|null | HEAD 中 en.json 的 blob sha |
| missing_keys | string[] | en 有 zh 无（键级增量，sha 判 stale 时附） |
| extra_keys | string[] | zh 有 en 无（键级减量） |

**状态转移**：翻译提交（写入当时 sha）→ `fresh` → en.json 变更 → `stale`（附键清单）→ 重译并刷新 `__meta` → `fresh`。

### 4. DocumentLanguageState（文档语言状态，派生）

`<html lang>` 与 `document.title` 由当前语言派生：`zh → "zh-CN"`、`en → "en"`；标题为 `知识探索器 · Semantica` / `Semantica Knowledge Explorer`。无独立存储，随语言事件即时更新。

## 实体关系

```
LanguagePreference ──初始化──▶ i18next 当前语言 ──驱动──▶ LocaleResource 取译 ──▶ UI 渲染
                                    │
                                    └─languageChanged──▶ DocumentLanguageState
LocaleResource(zh.__meta) ──比对──▶ HEAD:en.json blob ──▶ StalenessRecord（ui_zh_status.py）
```
