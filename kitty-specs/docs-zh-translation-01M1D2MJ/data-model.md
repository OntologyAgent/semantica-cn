# Data Model: Semantica 中文文档翻译

**Mission**: docs-zh-translation-01M1D2MJ | **Date**: 2026-08-31

本 Mission 无数据库实体，数据模型描述的是文件产物与其元数据契约。

## Entity 1: 译文页面（TranslatedPage）

**表示**: `docs/zh/**/*.md` 文件

| 字段 | 位置 | 类型 | 约束 |
|------|------|------|------|
| title | frontmatter | string | 必填，中文 |
| description | frontmatter | string | 必填，中文 |
| source | frontmatter | string | 必填，相对 `docs/` 的英文源路径，如 `quickstart.md` |
| source_version | frontmatter | string | 必填，40 位 git blob sha |
| 正文 | body | Markdown | JSX 标签结构与英文版同构 |

**不变量**:
- 存在 `docs/zh/X.md` ⇔ 翻译时存在 `docs/X.md`（上游删除后译文进入"孤儿"状态，由 zh_status 标记，不自动删除）
- `source_version` 必须是写入时 `git rev-parse <blob>` 可解析的真实 sha
- 同目录结构与英文版一一对应，无额外层级

**状态转换**（由 zh_status.py 判定，只读）:
```
fresh ──(英文 blob sha 变化)──▶ stale
任意态 ──(英文文件删除)──────▶ orphan
stale ──(重译并更新 sha)────▶ fresh
```

## Entity 2: 术语条目（GlossaryEntry）

**表示**: `docs/zh/glossary.md` 表格行

| 字段 | 类型 | 约束 |
|------|------|------|
| en | string | 英文原词，唯一键 |
| zh | string | 中文译名；允许与 en 相同（保留英文策略） |
| note | string | 可空，定名理由/使用限制 |

**不变量**: 同一 `en` 不出现两行；全部译文中同一 `en` 的译名与 `zh` 一致（NFR-003）。

## Entity 3: 同步状态记录（SyncStatus）

**表示**: `zh_status.py` 的运行时输出（不落盘持久化）

| 字段 | 类型 | 约束 |
|------|------|------|
| path | string | 译文相对路径 |
| status | enum | `fresh` / `stale` / `orphan` |
| current_source_sha | string \| None | 英文文件当前 blob sha；orphan 时为 None |
| recorded_source_sha | string | 译文 frontmatter 记录的 sha |

**关系**: SyncStatus : TranslatedPage = 1:1（每次扫描每个译文恰好一条）。

## Entity 4: 项目 Skill（TranslationSkill）

**表示**: `.claude/skills/docs-zh-translation/SKILL.md`

frontmatter 含 name/description；正文为流程编排（翻译新页 → 更新 sha → 跑 zh_status → 跑 docs_check），细节一律链接到 `docs/zh/README.md`，不复制规范文本（防双源漂移）。
