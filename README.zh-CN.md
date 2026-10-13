<!-- Upstream source: README.md (semantica-agi/semantica) -->
<!-- Language switch line in README.md links here. This page is a fork-maintained
     Chinese entry page, not a full translation of the upstream README. -->

# Semantica 中文说明

Semantica 是知识图谱(Knowledge Graph)基础设施：把分散的原始数据加工成一张可查询、可审计的图，充当 LLM 应用底下的确定性基础设施层。

本仓库是上游 [semantica-agi/semantica](https://github.com/semantica-agi/semantica) 的中文文档 fork，同时以 **`semantica-cn`** 为名在 PyPI 发布同源 Python 包（`pip install semantica-cn`，与官方 `semantica` 包二选一安装，不要同时装）。完整的项目介绍、安装方式与功能清单以 [英文 README](README.md) 为准。fork 的 MinerU 解析器额外支持最新版 MinerU 4.x（官方仍钉 2.x）。

## 中文文档

中文文档位于 [`docs_zh/`](docs_zh/index.md)，与英文版 `docs/` 同名镜像，已全量覆盖：`docs/` 下每个 Markdown 页面（含 guides、reference、integrations、best-practices 等子目录）都有中文版。

- [中文文档首页](docs_zh/index.md) — 从安装到第一次使用的完整中文阅读路径
- [快速开始](docs_zh/quickstart.md) · [安装](docs_zh/installation.md) · [核心概念](docs_zh/concepts.md) · [模块](docs_zh/modules.md)
- [常见问题](docs_zh/faq.md) · [CLI 配置](docs_zh/cli-setup.md) · [Explorer 配置](docs_zh/explorer-setup.md)
- [术语表](docs_zh/glossary.md) — 中英对照的冻结术语
- [翻译规范](docs_zh/README.md) — 贡献中文译文前必读

- [MinerU 集成](docs_zh/integrations/mineru.md) — 扫描件、公式密集、中日韩 PDF 的解析（含与 DoclingParser 的实测对比）
- [Docling 集成](docs_zh/integrations/docling.md) — 多格式复杂版面解析

上游新增的页面会先保持英文原页链接，补译后自动切换为中文站内链接，全程无死链。

## 与上游官方版本的差异

本仓库是 [semantica-agi/semantica](https://github.com/semantica-agi/semantica) 的扩展 fork，在官方版本之上增加了三块能力，其余代码跟随上游：

1. **MinerU PDF 解析器**（官方版本没有）——面向扫描件、公式密集和中日韩文档：行内公式还原为 LaTeX、表格数学单元格逐格 OCR、图片元数据规范化。安装 `pip install "semantica[parse-mineru]"`，用法见 [MinerU 集成指南](docs_zh/integrations/mineru.md)，其中附有与 DoclingParser 的同语料实测对比（13 页中文公式 PDF：行内公式 Docling 全丢、MinerU 全还原）。
2. **全量中文文档**（`docs_zh/`）——覆盖 `docs/` 全部页面的中文镜像、冻结术语表与翻译规范，配套 `tools/i18n/zh_status.py` 新鲜度巡检。
3. **Explorer 界面增强**（官方 explorer 没有这些视图）——fork 为 explorer 自建了中英双语 i18n；词表工作区选中概念后补拉 detail 端点，渲染定义、语境注记、同义词与来源，并把数据侧内嵌在定义里的〖谓词名 / 值域签名 / OWL 特征 / 语境〗标记解析成结构化徽标；词表树词条带类型徽标（类 / 属性 / 个体，读图节点全量属性的 `skos:notation`）与类型过滤器；图谱边卡片对推理边展示推理依据、模式与命中规则；图谱工作区带图层切换（全部 / 业务 / 本体视图预设 + 推理边独立开关，按节点/边 `properties.layer` 在 display graph 构建后过滤，无 layer 数据的图自动旁路）；本体 Hub 带「类与属性」页（类层级树 + 属性签名卡，数据取自已注入图谱的模式节点/边）；推理演练场带「从图取事实」按钮（业务层边经属性节点 `az:asciiId` 转 ASCII 谓词后灌入事实框）。另有少量后端配合改动（同 id 节点合并语义、词表 hierarchy 前缀键兜底、推理端点内建谓词、load 注入节点带 prefLabel/注释、CJK 类名与分句），其余仍跟随上游。

向官方版本贡献时，上述三块需要分别评审：MinerU 部分是自包含的（一个模块 + 注册点 + extra + 文档），中文文档零侵入上游文件；Explorer 增强全部是前端扩展（上游同名组件文件合并时需保 fork 侧改动，上游 Python 包与 API 契约不受影响）。

## 参与翻译

- 上游更新后运行 `python tools/i18n/zh_status.py` 查看过期译文，按清单定向同步。
- 翻译流程见 [翻译规范](docs_zh/README.md) 与 `.claude/skills/docs-zh-translation/`。
- 原则：零侵入——只增改 `docs_zh/`、`tools/i18n/` 与翻译工具，不修改上游既有文件。
