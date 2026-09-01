# Specification: Semantica 中文文档翻译

**Mission**: docs-zh-translation-01M1D2MJ
**Status**: Draft
**Created**: 2026-08-31

## Overview

为 Semantica（上游 semantica-agi/semantica 的 fork）建立可持续维护的中文文档体系。英文文档位于 `docs/`（83 篇 Mintlify 页面，约 16 万英文词），随上游持续演进。译文落在 `docs/zh/`，路径与英文版 1:1 镜像；以 git blob sha 追踪英文源变动并驱动译文同步。全程零侵入上游文件。

## User Scenarios & Testing

### 场景 1：中文用户快速上手（主流程）

- **角色**：中文开发者/用户
- **触发**：用户从 GitHub 仓库进入 `docs/zh/index.md`
- **成功结果**：沿 P0 门面页（index → quickstart → concepts → modules）完成从安装到第一次使用的中文阅读路径，无需切换英文
- **主异常路径**：某页尚未翻译 → 页面内链接回落到英文原页，读者可继续，无死链

### 场景 2：上游更新英文文档（同步流程）

- **角色**：仓库维护者
- **触发**：`git merge upstream/main` 后英文文档发生变化
- **成功结果**：运行 `python tools/i18n/zh_status.py`，5 秒内输出三类清单（✅ 最新 / 🟡 英文已更新 / 🔴 英文已删除），维护者按清单定向更新译文
- **主异常路径**：英文文件被上游删除 → 清单标记 🔴，译文标记为待归档而非报错

### 场景 3：贡献者翻译新页面（扩展流程）

- **角色**：贡献者（人或 Claude 实例）
- **触发**：按翻译规范翻译一篇新文档
- **成功结果**：译文 frontmatter 携带 `source` 与 `source_version`（翻译时的英文文件 blob sha），提交后进入追踪体系；`python docs_check.py` 保持全绿

## Requirements

### Functional Requirements

| ID | Requirement | Status |
|----|-------------|--------|
| FR-001 | `docs/zh/` 目录结构与 `docs/` 英文版 1:1 镜像（`docs/zh/quickstart.md` ↔ `docs/quickstart.md`） | Approved |
| FR-002 | P0 门面九篇完成中文翻译：index、quickstart、getting-started、installation、concepts、architecture、modules、choose-your-module、glossary | Approved |
| FR-003 | 每篇译文 frontmatter 包含 `source`（相对英文路径）与 `source_version`（翻译时英文文件的 git blob sha）字段 | Approved |
| FR-004 | `docs/zh/glossary.md` 术语表冻结首批核心术语（知识图谱、上下文图、决策智能、溯源、本体等），提供中英对照 | Approved |
| FR-005 | `docs/zh/README.md` 承载翻译规范：代码不翻原则、JSX 保留、链接回落规则、frontmatter 约定 | Approved |
| FR-006 | `tools/i18n/zh_status.py` 遍历全部译文，比对 blob sha，输出最新/过期/已删除三类清单 | Approved |
| FR-007 | `zh_status.py` 对不存在的 `docs/zh/` 或空目录给出明确提示而非 traceback | Approved |
| FR-008 | 全部译文文件通过 `python docs_check.py` 检查，且不修改该脚本 | Approved |
| FR-009 | P1 高频页完成翻译：faq、cli-setup、storage-backends、explorer-setup（约 4 篇起步，guides/ 按使用频率追加） | Approved |
| FR-010 | `docs/zh/changelog.md` 仅含指向上游英文 changelog 的说明，不翻译正文 | Approved |
| FR-011 | 译文内部链接零死链：目标页有中文版则链中文，无则链英文原页 | Approved |

### Non-Functional Requirements

| ID | Requirement | Status |
|----|-------------|--------|
| NFR-001 | 零侵入：不修改任何上游已存在的文件；可通过 `git diff upstream/main --name-only --diff-filter=M` 验证为空 | Approved |
| NFR-002 | `zh_status.py` 全量扫描在 5 秒内完成（83 文件规模） | Approved |
| NFR-003 | 术语一致性：同一英文术语在全部译文中使用同一译名，以 glossary 为准 | Approved |
| NFR-004 | 译文代码块内的标识符、命令、配置键与英文版一致（仅注释可译） | Approved |

### Constraints

| ID | Constraint | Status |
|----|------------|--------|
| C-001 | 不修改 `docs/docs.json`、`docs_check.py`、`.github/` 及其他一切上游既有文件 | Approved |
| C-002 | 术语拿不准时保留英文原词，不硬造译名 | Approved |
| C-003 | Mintlify JSX 组件结构（`<Card>`、`<Tabs>` 等）原样保留，只译标签内文本 | Approved |
| C-004 | P3 页面（community*、governance、citation、contributing-guide、project-license）与 changelog 正文不翻译 | Approved |

## Success Criteria

1. 中文用户可从 `docs/zh/index.md` 出发，全程中文完成 P0 九篇的入门阅读路径，路径上无死链
2. 上游合并后运行 `python tools/i18n/zh_status.py`，5 秒内得到准确的过期清单
3. `python docs_check.py` 全部检查通过
4. `git diff upstream/main --name-only --diff-filter=M` 为空（零侵入验证）

## Domain Language

| 英文术语 | 中文译名 | 备注 |
|---------|---------|------|
| Knowledge Graph | 知识图谱 | |
| Context Graph | 上下文图 | |
| Decision Intelligence | 决策智能 | |
| Provenance | 溯源 | |
| Ontology | 本体 | |
| Entity Resolution | 实体消解 | |
| Triplet | 三元组 | |
| Ingestion | 摄取 | |
| Reasoning Engine | 推理引擎 | |
| Conflict Detection | 冲突检测 | |

完整术语表见 `docs/zh/glossary.md`（本 Mission 产物）。

## Assumptions

- 中文站点部署不在本 Mission 范围内（第三期评估，独立决策）
- P1 的 guides/ 22 篇不要求全翻，按使用频率追加，数量开放式
- 翻译工作由 Claude 实例执行，人工抽查验收

## Key Entities

- **译文页面**（docs/zh/ 下 md 文件）：frontmatter 含 title / description / source / source_version
- **术语条目**（glossary.md）：英文原词 → 中文译名 → 备注
- **同步状态**（zh_status.py 输出）：文件路径、状态（fresh/stale/missing）、源 sha 对比结果
