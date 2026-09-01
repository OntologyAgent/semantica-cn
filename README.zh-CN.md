<!-- Upstream source: README.md (semantica-agi/semantica) -->
<!-- Language switch line in README.md links here. This page is a fork-maintained
     Chinese entry page, not a full translation of the upstream README. -->

# Semantica 中文说明

Semantica 是知识图谱(Knowledge Graph)基础设施：把分散的原始数据加工成一张可查询、可审计的图，充当 LLM 应用底下的确定性基础设施层。

本仓库是上游 [semantica-agi/semantica](https://github.com/semantica-agi/semantica) 的中文文档 fork。完整的项目介绍、安装方式与功能清单以 [英文 README](README.md) 为准。

## 中文文档

中文文档位于 [`docs/zh/`](docs/zh/index.md)，与英文版 `docs/` 同名镜像，按 P0/P1 分层翻译：

- [中文文档首页](docs/zh/index.md) — 从安装到第一次使用的完整中文阅读路径
- [快速开始](docs/zh/quickstart.md) · [安装](docs/zh/installation.md) · [核心概念](docs/zh/concepts.md) · [模块](docs/zh/modules.md)
- [常见问题](docs/zh/faq.md) · [CLI 配置](docs/zh/cli-setup.md) · [Explorer 配置](docs/zh/explorer-setup.md)
- [术语表](docs/zh/glossary.md) — 中英对照的冻结术语
- [翻译规范](docs/zh/README.md) — 贡献中文译文前必读

英文文档未翻译的部分保持英文原页，译文内链会自动回落，无死链。

## 参与翻译

- 上游更新后运行 `python tools/i18n/zh_status.py` 查看过期译文，按清单定向同步。
- 翻译流程见 [翻译规范](docs/zh/README.md) 与 `.claude/skills/docs-zh-translation/`。
- 原则：零侵入——只增改 `docs/zh/`、`tools/i18n/` 与翻译工具，不修改上游既有文件。
