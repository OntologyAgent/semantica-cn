---
title: 参与贡献
description: 如何为 Semantica 贡献代码、文档、测试与社区支持。
source: contributing-guide.md
source_version: d2bb7391860d9b757e0b5dbaee7bb74eb33a3322
icon: "code-pull-request"
---

我们欢迎各种形式的贡献——代码、文档、测试与社区支持。每一份贡献都会在发布说明和 GitHub 贡献者名单中得到署名。


## 快速开始

```bash
# Fork the repo on GitHub, then:
git clone https://github.com/your-username/semantica.git
cd semantica
pip install -e . --group dev   # needs pip 25.1+ (or: uv sync)
pytest
```

初次贡献者可以从带 [`good-first-issue`](https://github.com/semantica-agi/semantica/labels/good-first-issue) 标签的工单入手：这些工单的范围都经过刻意划分，几个小时就能完成，也不需要深入了解代码库。


## 贡献方式

- **代码**：修复缺陷、实现新功能、优化性能，或借助插件注册表(plugin registry)添加新的摄取器(ingestor)、解析器(parser)与导出器(exporter)。
- **文档**：修正错别字、改进表述、补齐缺失示例、撰写教程，并在模块演进的过程中保持 API 参考的准确。
- **测试**：为尚未覆盖的模块或边界情况补充测试、用最小复现脚本重现他人报告的缺陷，或提升跨平台可靠性。
- **社区**：在 GitHub Issues 和 Discussions 里回答问题、以建设性的意见评审拉取请求(Pull Request)，或通过博客文章与技术演讲传播 Semantica。


## 开发环境

```bash
git clone https://github.com/your-username/semantica.git
cd semantica
pip install -e . --group dev   # needs pip 25.1+ (or: uv sync)
```

**代码风格工具：**

```bash
pytest                      # full test suite
black semantica/ tests/     # auto-format
isort semantica/ tests/     # sort imports
flake8 semantica/           # lint
```

风格约定：格式化用 **Black**，导入排序用 **isort**，静态检查用 **flake8**。三项检查都会在 CI 中运行。


## 报告问题

**缺陷报告**应当包含：

- 实际发生了什么，以及你期望发生什么
- 最小复现步骤
- 你的环境信息：Python 版本、操作系统、Semantica 版本（`python -c "import semantica; print(semantica.__version__)"`）

**功能建议**应当包含：

- 你的具体使用场景
- 你希望 Semantica 做什么
- 为什么它能让广大用户受益，而不只是服务于你个人的工作流


## 拉取请求清单

提交 PR 之前，请确认：

<Check>测试在本地全部通过：`pytest`</Check>
<Check>新功能附带文档，且代码示例可正常运行</Check>
<Check>代码遵循项目风格：Black、isort、flake8</Check>
<Check>提交信息清晰，说明了*为什么*改，而不只是*改了什么*</Check>
<Check>没有未解决的合并冲突</Check>


## 行为准则

所有贡献者都应遵守[贡献者公约行为准则](https://github.com/semantica-agi/semantica/blob/main/CODE_OF_CONDUCT.md)。请保持尊重、耐心与建设性，对新人尤应如此。发现违规行为，请开一个带 `[CoC]` 前缀的 issue 举报。


## 求助

- [GitHub Issues](https://github.com/semantica-agi/semantica/issues)
- [GitHub Discussions](https://github.com/semantica-agi/semantica/discussions)
- [Discord](https://discord.gg/sV34vps5hH)

- [社区](./community.md)：社区准则与价值观。
- [治理](./governance.md)：项目如何做决策、如何日常运转。
