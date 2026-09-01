# Tasks: Semantica 中文文档翻译

**Mission**: docs-zh-translation-01M1D2MJ
**Branch**: feat/docs-zh-translation
**Generated**: 2026-08-31T23:50:32Z

## Subtask Index

| ID | Description | WP | Parallel | Status |
|----|-------------|----|----------|--------|
| T001 | 建立 docs/zh/glossary.md 术语表（10 条核心术语 + 表结构 + frontmatter） | WP01 | [P] | pending |
| T002 | 编写 docs/zh/README.md 翻译规范 | WP01 | [P] | pending |
| T003 | 交叉核对 spec Domain Language 与 glossary，补齐遗漏术语 | WP01 |  | pending |
| T004 | 验证 glossary/README 通过 docs_check.py 局部检查 | WP01 |  | pending |
| T005 | 实现 zh_status.py 扫描与 frontmatter 解析 | WP02 | [P] | pending |
| T006 | 实现 git blob sha 比对与 fresh/stale/orphan 判定 | WP02 |  | pending |
| T007 | 实现 CLI（--json/--root/--verbose）与退出码 0/1/2 | WP02 |  | pending |
| T008 | 按 contracts/zh-status-cli.md 做行为自测（真实 docs/zh + 降级路径） | WP02 |  | pending |
| T009 | 性能验证（≤5s）与 83 文件规模演练 | WP02 |  | pending |
| T010 | 翻译 docs/zh/index.md | WP03 | [P] | pending |
| T011 | 翻译 docs/zh/quickstart.md | WP03 | [P] | pending |
| T012 | 翻译 docs/zh/getting-started.md 与 installation.md | WP03 | [P] | pending |
| T013 | WP03 自检：内链回落、JSX 平衡、zh_status 全 fresh、docs_check | WP03 |  | pending |
| T014 | 翻译 docs/zh/concepts.md | WP04 | [P] | pending |
| T015 | 翻译 docs/zh/architecture.md（含 Mermaid 图标签策略） | WP04 | [P] | pending |
| T016 | 翻译 docs/zh/modules.md 与 choose-your-module.md（27 模块表） | WP04 | [P] | pending |
| T017 | WP04 自检（同 T013 标准） | WP04 |  | pending |
| T018 | 翻译 docs/zh/faq.md | WP05 | [P] | pending |
| T019 | 翻译 docs/zh/cli-setup.md | WP05 | [P] | pending |
| T020 | 翻译 docs/zh/storage-backends.md | WP05 | [P] | pending |
| T021 | 翻译 docs/zh/explorer-setup.md | WP05 | [P] | pending |
| T022 | 编写 docs/zh/changelog.md 指路页 + WP05 自检 | WP05 |  | pending |
| T023 | 编写 .claude/skills/docs-zh-translation/SKILL.md | WP06 |  | pending |
| T024 | 零侵入验证与 init 伴生产物规整（README.md 一行链接、.gitignore/.gitattributes 说明） | WP06 |  | pending |
| T025 | 全局验收：docs_check 全绿、zh_status 全 fresh、quickstart 五步走查 | WP06 |  | pending |
| T026 | 更新 CLAUDE.md：docs/zh 体系与 Skill 入口 | WP06 |  | pending |

## WP01 — 术语表与翻译规范（Foundation）

**Prompt**: `tasks/WP01-glossary-and-translation-guide.md`
**Goal**: 冻结译名与规则，所有翻译工作包的前置
**Priority**: P0（最高，其他 WP 的依赖）
**Independent test**: glossary.md/README.md 存在且通过 docs_check.py；术语表覆盖 spec Domain Language 全部条目
**Estimated prompt size**: ~300 lines

- [x] T001 建立 docs/zh/glossary.md 术语表（10 条核心术语 + 表结构 + frontmatter） (WP01)
- [x] T002 编写 docs/zh/README.md 翻译规范 (WP01)
- [x] T003 交叉核对 spec Domain Language 与 glossary，补齐遗漏术语 (WP01)
- [x] T004 验证 glossary/README 通过 docs_check.py 局部检查 (WP01)

**Dependencies**: none
**Parallel opportunities**: 与 WP02 并行

## WP02 — 过期追踪工具 zh_status.py（Foundation）

**Prompt**: `tasks/WP02-zh-status-tool.md`
**Goal**: 实现 blob sha 比对的过期检测工具，契约见 contracts/zh-status-cli.md
**Priority**: P0（与 WP01 并行的地基）
**Independent test**: 对真实 docs/zh 运行输出合法 JSON；退出码语义正确；83 文件 ≤5s
**Estimated prompt size**: ~400 lines

- [x] T005 实现 zh_status.py 扫描与 frontmatter 解析 (WP02)
- [x] T006 实现 git blob sha 比对与 fresh/stale/orphan 判定 (WP02)
- [x] T007 实现 CLI（--json/--root/--verbose）与退出码 0/1/2 (WP02)
- [x] T008 按 contracts/zh-status-cli.md 做行为自测（真实 docs/zh + 降级路径） (WP02)
- [x] T009 性能验证（≤5s）与 83 文件规模演练 (WP02)

**Dependencies**: none
**Parallel opportunities**: 与 WP01 并行

## WP03 — P0 门面翻译·第一批（index/quickstart/getting-started/installation）

**Prompt**: `tasks/WP03-p0-batch1.md`
**Goal**: 打通中文用户从落地页到装好能跑的阅读路径
**Priority**: P0
**Independent test**: 四篇译文存在、frontmatter 合规、zh_status 全 fresh、docs_check 不新增失败
**Estimated prompt size**: ~450 lines

- [ ] T010 翻译 docs/zh/index.md (WP03)
- [ ] T011 翻译 docs/zh/quickstart.md (WP03)
- [ ] T012 翻译 docs/zh/getting-started.md 与 installation.md (WP03)
- [ ] T013 WP03 自检：内链回落、JSX 平衡、zh_status 全 fresh、docs_check (WP03)

**Dependencies**: WP01, WP02
**Parallel opportunities**: 与 WP04、WP05 并行（owned_files 无交集）

## WP04 — P0 门面翻译·第二批（concepts/architecture/modules/choose-your-module）

**Prompt**: `tasks/WP04-p0-batch2.md`
**Goal**: 补齐 P0 概念与导航页
**Priority**: P0
**Independent test**: 四篇译文存在、frontmatter 合规、Mermaid 图策略一致、docs_check 不新增失败
**Estimated prompt size**: ~450 lines

- [ ] T014 翻译 docs/zh/concepts.md (WP04)
- [ ] T015 翻译 docs/zh/architecture.md（含 Mermaid 图标签策略） (WP04)
- [ ] T016 翻译 docs/zh/modules.md 与 choose-your-module.md（27 模块表） (WP04)
- [ ] T017 WP04 自检（同 T013 标准） (WP04)

**Dependencies**: WP01, WP02
**Parallel opportunities**: 与 WP03、WP05 并行

## WP05 — P1 高频页与 changelog 指路页

**Prompt**: `tasks/WP05-p1-pages.md`
**Goal**: 覆盖安装后最常查阅的运维页面
**Priority**: P1
**Independent test**: 五篇产物存在、frontmatter 合规、changelog 仅指路一行、docs_check 不新增失败
**Estimated prompt size**: ~400 lines

- [ ] T018 翻译 docs/zh/faq.md (WP05)
- [ ] T019 翻译 docs/zh/cli-setup.md (WP05)
- [ ] T020 翻译 docs/zh/storage-backends.md (WP05)
- [ ] T021 翻译 docs/zh/explorer-setup.md (WP05)
- [ ] T022 编写 docs/zh/changelog.md 指路页 + WP05 自检 (WP05)

**Dependencies**: WP01, WP02
**Parallel opportunities**: 与 WP03、WP04 并行

## WP06 — Skill 封装与全局验收（Polish）

**Prompt**: `tasks/WP06-skill-and-acceptance.md`
**Goal**: 固化可复用 Skill，完成零侵入与全绿验收，更新 CLAUDE.md
**Priority**: P1（收尾门）
**Independent test**: Skill 文件就位且含 Do-This-First 段；`git diff upstream/main --diff-filter=M` 仅含 init 声明的脚手架文件；docs_check 全绿
**Estimated prompt size**: ~300 lines

- [ ] T023 编写 .claude/skills/docs-zh-translation/SKILL.md (WP06)
- [ ] T024 零侵入验证与 init 伴生产物规整 (WP06)
- [ ] T025 全局验收：docs_check 全绿、zh_status 全 fresh、quickstart 五步走查 (WP06)
- [ ] T026 更新 CLAUDE.md：docs/zh 体系与 Skill 入口 (WP06)

**Dependencies**: WP01, WP02, WP03, WP04, WP05
**Parallel opportunities**: none（收尾串行）
