---
title: 翻译规范
description: Semantica 中文文档（docs/zh/）翻译流程、规则与验收标准
source: README.md
source_version: native
---

# 翻译规范

**本页为自建规范，非上游译文**——上游 `docs/` 目录没有 README.md，本页与上游无对应关系。

任何人（或 Claude 实例）翻译、更新中文文档之前，先读完本页。术语对照见[术语表](./glossary.md)。

## 分层策略

| 层级 | 范围 | 处理方式 |
|------|------|---------|
| P0 门面 | index、quickstart、getting-started、installation、concepts、architecture、modules、choose-your-module、glossary | 必翻，质量最高 |
| P1 高频 | faq、cli-setup、storage-backends、explorer-setup，guides/ 按使用频率追加 | 必翻，准确优先 |
| P2 参考 | reference/ 下约 29 篇 | 按需翻译 |
| P3 不翻 | community*、governance、citation、contributing-guide、project-license | 保留英文 |
| changelog | docs/changelog.md | 只做指路页，正文不翻 |

优先级顺序：P0 → P1 → P2。P0/P1 完成后再评估 P2。

## 译文 frontmatter

每篇译文必须带四个字段：

```yaml
---
title: 快速开始
description: 五分钟跑通第一个知识图谱
source: quickstart.md
source_version: <40 位 git blob sha>
---
```

- `source`：相对 `docs/` 的英文源文件名（如 `quickstart.md`）。
- `source_version`：翻译时英文文件的 blob sha，取法：

  ```bash
  git rev-parse HEAD:docs/quickstart.md
  ```

- `title` / `description`：中文，description 为一句话。
- **自建页**（本页、changelog 指路页）不对应英文原文，`source_version` 填 `native`，正文需注明"自建页"。

## 代码不翻原则

- 标识符、类名、函数名、模块名、CLI 命令、flag、环境变量、配置键、URL、路径示例：原样保留。
- 代码块内的注释可以翻译；代码本身逐字符不动。
- 预期输出示例不翻（用户要拿它和真实输出比对）。

## JSX 保留原则

Mintlify 组件（`Card`、`Tabs`、`Steps`、`Accordion` 等，源文件中写作带尖括号的 JSX 标签）：

- 标签结构、属性（图标名、id 等属性值）原样保留。
- 只翻译标签内的文本内容。
- 开闭标签数量必须与英文版一致（`docs_check.py` 会校验配平）。
- 行文提及组件名时写代码格式的裸名（如 `Card`），**不要带尖括号**——配平检查按字面统计，会被误判为未闭合标签。

## 链接回落规则

译文内链指向其他文档时：

1. 目标页已有中文版 → 链接 `./xxx.md`（docs/zh/ 内相对路径）。
2. 目标页没有中文版 → 链接英文原页（`../xxx.md` 或上游相对路径）。
3. 验收要求零死链：每个链接的目标必须真实存在。

## 术语规则

1. 翻译前先查[术语表](./glossary.md)，同一术语全库只用一个译名。
2. 缺条目：先补术语表，再翻译。
3. 拿不准：保留英文原词，不硬造译名。
4. 核心术语译名已冻结，不得更改。

## Mermaid 图策略

- 图内自然语言节点标签可译，但必须保持 Mermaid 语法有效；拿不准就给标签加双引号。
- 代码类标签（类名、函数名、模块名）保留英文。
- 译后逐图目检语法结构未被破坏。

## 验收命令

每次翻译或更新后，两道检查必须通过：

```bash
python docs_check.py             # 上游检查器：JSX 配平、死链、代码块等
python tools/i18n/zh_status.py   # 译文过期状态：新译文应显示 fresh
```

`docs_check.py` 不新增任何失败；新翻译的页面在 `zh_status.py` 中应为 fresh。

## 上游同步例行动作

```bash
git fetch upstream && git merge upstream/main
python tools/i18n/zh_status.py   # 拿到过期清单
# 逐篇重译 stale 页，重译后把 frontmatter 的 source_version 刷成当前 sha
```

英文文件被上游删除时，译文标记为 orphan（孤儿），人工决定去留，不自动删除。

## 提交信息约定

```
docs(zh): translate quickstart        # 新译文
docs(zh): sync 3 stale pages          # 上游同步后的译文更新
docs(zh): add glossary entries for …  # 术语表补充
```
