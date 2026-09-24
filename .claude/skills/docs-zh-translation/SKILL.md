---
name: docs-zh-translation
description: 翻译或更新 Semantica 中文文档（docs_zh/）。当用户要求翻译某篇文档、同步过期译文、或补充术语时使用。
---

# Semantica 中文文档翻译

本 Skill 是**流程编排层**：只定义"做什么、按什么顺序、用什么命令验收"。全部翻译规范（frontmatter 格式、术语表、JSX 处理、链接规则）以 [`docs_zh/README.md`](../../../docs_zh/README.md) 为单一事实源，本文件不复制其内容。

## 触发场景与入口

| 场景 | 走哪条流程 |
| --- | --- |
| 翻译一篇尚未有中文版的文档 | [翻译新页](#翻译新页流程) |
| 上游更新后译文过期 | [同步过期译文](#同步过期译文流程) |
| 新术语需要统一译法 | [补充术语](#补充术语流程) |

## 翻译新页流程

1. 读规范：`docs_zh/README.md`（frontmatter 四+二字段、JSX 组件对照、链接规则）。
2. 读术语表：`docs_zh/glossary.md`，冻结术语必须按表译；表外术语首现用"中文(English)"格式。
3. 读英文源 `docs/<name>.md` 全文，再动笔。
4. 建 `docs_zh/<name>.md`：
   - frontmatter 至少含 `title`（中文）、`description`（中文）、`source: <name>.md`、`source_version`；
   - `source_version` 取真实 blob sha：`git rev-parse HEAD:docs/<name>.md`；
   - 已翻译页面间互链用 `./xxx.md`，未翻译页面回退 `../xxx.md`；
   - 内部锚点指向**中文标题**的 slug（如 `#installation` → `#安装`）；
   - 显示属性（title=、alt=）翻译，技术属性（icon=、id=）保留英文；JSX 标签数量必须与源逐一相等；代码块原样保留，仅翻译说明性注释。
5. 自检（见下）后提交：`feat(i18n): translate <name> to zh`。

## 同步过期译文流程

1. 同步上游：`git fetch upstream && git merge upstream/main`。
2. 跑 `python tools/i18n/zh_status.py`，列出 stale 条目。
3. 逐篇：diff 英文源新旧版本（`git diff <旧sha>..<新sha> -- docs/<name>.md`），只重译变更部分，更新 frontmatter `source_version` 为新 sha。
4. 自检后提交：`fix(i18n): sync <name> with upstream <新sha截断>`。

## 补充术语流程

1. 在 `docs_zh/glossary.md` 增补词条：英文术语 + 冻结中文译法。
2. `grep -rn "<英文>" docs_zh/` 找出已有译文的分歧译法，统一为新译法。
3. 自检后提交：`docs(i18n): add glossary entry <term>`。

## 验收命令（每次改动后必跑）

```bash
python docs_check.py                # docs/ 一致性（既有基线不能新增失败）
python tools/i18n/zh_status.py      # 译文过期状态：翻译页应为 fresh
```

另有三项人工抽查（自检脚本模式见 docs_zh/README.md）：

- JSX 平衡：逐组件对比译文与源的 `<Comp>`/`</Comp>` 数量；
- 链接：`./` 目标在 docs_zh/ 全集中存在，`../` 目标在 docs/ 中存在；
- 术语：冻结术语译法与 glossary 一致。

## 边界

- P3 页面（低频 reference 深页）与 changelog 正文**不翻**（changelog 指路页已建于 `docs_zh/changelog.md`）。
- 不修改上游文件：`docs/docs.json`、`docs_check.py`、`.github/` 及一切既有英文文档。
- 只新增/修改 `docs_zh/`、`tools/i18n/`、本 Skill 目录内的文件。
- 规范细节（frontmatter 完整字段说明、代码块注释翻译口径、进度约定）一律见 `docs_zh/README.md`，本 Skill 与其冲突时以 README 为准。
