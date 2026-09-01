# Quickstart: 参与中文文档翻译

**Mission**: docs-zh-translation-01M1D2MJ

面向贡献者（人或 Claude 实例）的五步上手路径。规范全文见 `docs/zh/README.md`（Mission 产物落地后生效）。

## 1. 环境就绪

```bash
source .venv/bin/activate        # uv 管理的环境（见 CLAUDE.md）
git fetch upstream               # 确认英文源是最新的
```

## 2. 选一篇待翻译页

```bash
python tools/i18n/zh_status.py   # 已有译文的健康度
ls docs/ | grep -v zh            # 英文全集；对照 docs/zh/ 找缺失页
```

优先级：P0 门面九篇 → P1 高频 → P2 reference。P3（community*、governance、citation、contributing-guide、project-license）与 changelog 不翻。

## 3. 翻译

- 新建 `docs/zh/<同名>.md`，frontmatter 必带四个字段：

  ```yaml
  ---
  title: 快速开始
  description: 五分钟跑通第一个知识图谱
  source: quickstart.md
  source_version: <git rev-parse HEAD:docs/quickstart.md 的输出>
  ---
  ```

- 代码块里只翻注释；CLI 命令、API 名、配置键原样保留
- JSX 组件（`<Card>`、`<Tabs>`…）结构与英文版一致，只译标签内文本
- 术语先查 `docs/zh/glossary.md`；没有的条目先补术语表再翻译；拿不准保留英文
- 内链：目标页有中文版链 `./xxx.md`，没有就链英文原页

## 4. 自检

```bash
python docs_check.py             # 必须全绿（JSX 平衡、死链、stale URL 等）
python tools/i18n/zh_status.py   # 新页应显示 fresh
```

## 5. 提交

```
docs(zh): translate quickstart        # 新译文
docs(zh): sync 3 stale pages          # 上游同步后的译文更新
docs(zh): add glossary entries for …  # 术语表补充
```

## 上游同步例行动作

```bash
git fetch upstream && git merge upstream/main
python tools/i18n/zh_status.py         # 拿到过期清单
# 逐篇重译 stale 页：更新译文后把 frontmatter 的 source_version 刷成当前 sha
```
