# Implementation Plan: Semantica 中文文档翻译

**Branch**: `feat/docs-zh-translation` | **Date**: 2026-08-31 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/kitty-specs/docs-zh-translation-01M1D2MJ/spec.md`

## Summary

为 83 篇 Mintlify 英文文档建立中文镜像体系：`docs/zh/` 按 1:1 路径结构承接分层翻译（P0 门面 9 篇 → P1 高频 → P2 reference），以 git blob sha 在译文 frontmatter 中记录英文源版本，配套 `tools/i18n/zh_status.py` 输出过期清单驱动同步。术语表与翻译规范先于翻译落地，并把三者（规范、工具、流程）封装为可复用的项目级 Claude Skill。全程零侵入上游文件。

## Technical Context

**Language/Version**: Python 3.11（`.venv`，uv 管理；与仓库 CI 版本一致）
**Primary Dependencies**: 仅 Python 标准库（`subprocess` 调 git 获取 blob sha、`pathlib`、`argparse`）；文档为 Markdown + Mintlify JSX
**Storage**: N/A（纯文件产物，无数据库；状态即 git 对象本身）
**Testing**: `python tools/i18n/zh_status.py` 自测 + `python docs_check.py` 全绿作为验收门；工具行为用小型冒烟用例验证（fixture 目录）
**Target Platform**: macOS / Linux（维护者本地运行；不进 CI 强制门）
**Project Type**: 文档工程 + 单脚本工具（非 web/mobile）
**Performance Goals**: `zh_status.py` 全量扫描 ≤5s（83 文件）
**Constraints**: 零侵入上游文件；术语不硬造，拿不准保留英文；JSX 组件结构原样保留
**Scale/Scope**: P0 9 篇 + P1 起步 4 篇 + glossary + README 规范 + 1 个追踪工具 + 1 个项目 Skill

## Charter Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

项目无 charter 文件（`.kittify/charter/charter.md` 不存在），本节跳过。治理约束以 spec 的 C-001~C-004（零侵入、术语保守、JSX 保留、P3 不翻）为准。

## Project Structure

### Documentation (this mission)

```
kitty-specs/docs-zh-translation-01M1D2MJ/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (zh_status.py CLI contract)
│   └── zh-status-cli.md
└── tasks.md             # Phase 2 output (/spec-kitty.tasks, NOT in this command)
```

### Source Code (repository root)

```
docs/zh/                          # 译文目录（本 Mission 核心产物）
├── README.md                     # 翻译规范（FR-005）
├── glossary.md                   # 术语表（FR-004）
├── index.md                      # P0
├── quickstart.md                 # P0
├── getting-started.md            # P0
├── installation.md               # P0
├── concepts.md                   # P0
├── architecture.md               # P0
├── modules.md                    # P0
├── choose-your-module.md         # P0
├── glossary.md                   # P0（与术语表合一：上游 glossary 的翻译 + 自建术语表）
├── faq.md                        # P1
├── cli-setup.md                  # P1
├── storage-backends.md           # P1
├── explorer-setup.md             # P1
└── changelog.md                  # 仅指路一行（FR-010）

tools/i18n/
└── zh_status.py                  # 过期追踪工具（FR-006/007）

.claude/skills/docs-zh-translation/
└── SKILL.md                      # 项目 Skill：规范+流程+工具的复用封装
```

**Structure Decision**: 译文镜像英文路径是同步机制的基石（无需路径映射表）；工具放 `tools/i18n/`（仓库无 `tools/` 目录，属新增，不与上游任何路径冲突）；Skill 放 `.claude/skills/`（已存在的本地机制目录，spec-kitty init 又新增了命令面，均为增量）。

## Complexity Tracking

*Fill ONLY if Charter Check has violations that must be justified*

无违规项。

## Implementation Concern Map

### IC-01 — 术语表与翻译规范

- **Purpose**: 先冻结译名与规则，再动笔翻译，避免返工和术语漂移
- **Relevant requirements**: FR-004, FR-005, NFR-003, C-002, C-003
- **Affected surfaces**: `docs/zh/glossary.md`, `docs/zh/README.md`
- **Sequencing/depends-on**: none（最先行，其他 IC 的前置）
- **Risks**: 术语定名争议（用"拿不准保留英文"原则兜底）

### IC-02 — 过期追踪工具 zh_status.py

- **Purpose**: 用 git blob sha 比对实现译文过期检测，让上游演进可追踪
- **Relevant requirements**: FR-003, FR-006, FR-007, NFR-002
- **Affected surfaces**: `tools/i18n/zh_status.py`
- **Sequencing/depends-on**: none（与 IC-01 并行；IC-03/04 翻译时需按其 frontmatter 约定写入 source_version）
- **Risks**: git 不可用/非 git 环境的降级提示；blob sha 与工作区未提交状态的一致性

### IC-03 — P0 门面九篇翻译

- **Purpose**: 打通中文用户的完整入门阅读路径，是 Mission 的价值核心
- **Relevant requirements**: FR-001, FR-002, FR-003, FR-008, FR-011, C-003
- **Affected surfaces**: `docs/zh/` 下 index、quickstart、getting-started、installation、concepts、architecture、modules、choose-your-module、glossary
- **Sequencing/depends-on**: IC-01（术语表先行）
- **Risks**: JSX 组件翻译时破坏标签平衡（docs_check.py 兜底）；内链指向未翻译页（回落英文规则兜底）

### IC-04 — P1 高频页翻译与 changelog 指路页

- **Purpose**: 覆盖安装后最常查阅的运维页面
- **Relevant requirements**: FR-009, FR-010, FR-011
- **Affected surfaces**: `docs/zh/` 下 faq、cli-setup、storage-backends、explorer-setup、changelog
- **Sequencing/depends-on**: IC-01
- **Risks**: 无（模式与 IC-03 相同，难度更低）

### IC-05 — 项目 Skill 封装（docs-zh-translation）

- **Purpose**: 把规范、工具用法、同步流程固化为 Claude 项目技能，后续任一会话可复用
- **Relevant requirements**: FR-005, FR-006 派生（复用封装，非新增功能面）
- **Affected surfaces**: `.claude/skills/docs-zh-translation/SKILL.md`
- **Sequencing/depends-on**: IC-01, IC-02（Skill 引用其产物）
- **Risks**: SKILL.md 与实际流程漂移（写明"以 docs/zh/README.md 为准"的单一事实源）
