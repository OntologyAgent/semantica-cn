# Commons Ontology Library：通用上层本体参考样例

Commons Ontology Library（Commons 本体库）是由对象管理组织（OMG）与企业数据管理委员会（EDM Council）共同维护的一套**通用上层本体**。它为金融、医药、制造、政府等不同领域提供跨行业复用的基础概念，例如参与方、角色、情境、组织、地点、数量、单位、标识符、代码集、文档等。

FIBO 从 2023 年起逐步把原先自己定义的上层基础概念迁移到 Commons，因此 Commons 既是 FIBO 的重要依赖，也是一套可以独立使用的参考本体。

本目录是 Commons 的中文导览和官方 RDF 参考快照。`20250801/` 保留 OMG 官方在该版本下的全部模块，原始 `.rdf` 文件未作修改；同名的 `.ttl` 文件是我们转换的 Turtle 版本，并加入了中文标注。

## 1. 快照信息

| 项目 | 内容 |
|---|---|
| 官方来源 | [OMG Commons Ontology Library](https://www.omg.org/spec/Commons/) |
| 本地版本 | `20250801`（2025 年 8 月 1 日发布版本） |
| 固定入口 | [`20250801/AboutCommons/AboutCommons.rdf`](20250801/AboutCommons/AboutCommons.rdf) |
| 本地快照 | [`20250801/`](20250801/) |
| 文件规模 | 23 个模块，每个模块一份 `.rdf` 和一份对应 `.ttl`，共 46 个本体文件 |
| 官方规范 | [OMG 规范页面](https://www.omg.org/spec/Commons/) · [Commons 1.1 PDF](https://www.omg.org/spec/Commons/1.1/PDF) |
| 许可证 | MIT，见各 `.rdf` 文件中的 `dct:license` |

## 2. 背景：为什么需要 Commons

不同行业的本体往往会重复定义相似的上层概念：什么是“组织”、什么是“角色”、什么是“情境”、如何表达“时间”和“地点”。这些概念本身不是某个行业专有，但如果每个领域本体都各自定义，就会造成概念碎片、重复建模和跨领域对齐困难。

Commons 的目标就是把这些通用概念抽出来，形成一套**行业无关、可复用、经过标准化评审**的上层本体。各领域本体（如 FIBO）再在此基础上定义自己的专业概念。这样：

- 同一概念在不同领域中名称和定义一致，便于跨领域数据整合。
- 上层逻辑（如角色扮演、时间区间、数量单位）只维护一次，减少重复工作。
- 工具、推理机和查询可以复用同一套基础结构。

Commons 的开发由 EDM Council、Thematix Partners、Stardog、Working Ontologist、agnos.ai 等多家机构贡献，并由 OMG 作为国际标准发布。

## 3. 与 FIBO 的关系

可以把 Commons 理解为 FIBO 的“地基”之一：

- FIBO 的 [`FND/Agreements/Agreements.rdf`](../FIBO/master_2026Q3/FND/Agreements/Agreements.rdf) 直接导入 `cmns-pts:PartiesAndSituations`、`cmns-rlcmp:RolesAndCompositions` 和 `cmns-av:AnnotationVocabulary`。
- FIBO 中的 `Situation`、`PartyRole`、`hasPartyRole`、`isPlayedBy` 等概念都来自 Commons。
- 随着 FIBO 演进，越来越多的 FND 基础概念会被 Commons 中的对应概念替换。

因此，如果要深入理解 FIBO 的建模方式， Commons 是绕不开的前置知识。

## 4. 模块清单

| 模块目录 | 中英文名称 | 主要内容 |
|---|---|---|
| [`AboutCommons`](20250801/AboutCommons/) | 关于 Commons 本体库 | 一次性加载全部 Commons 模块的入口文件 |
| [`AnnotationVocabulary`](20250801/AnnotationVocabulary/) | Commons 标注词汇表 | 摘要、定义、解释、版权、同义词等通用标注属性 |
| [`BusinessAuthorizations`](20250801/BusinessAuthorizations/) | 业务授权 | 业务授权、许可及其相关角色和关系 |
| [`Classifiers`](20250801/Classifiers/) | 分类器 | 对事物进行分类、分面或归类的通用概念 |
| [`CodesAndCodeSets`](20250801/CodesAndCodeSets/) | 代码与代码集 | 代码、代码集、编码方案及其标识方式 |
| [`Collections`](20250801/Collections/) | 集合 | 集合、成员关系及集合操作 |
| [`ContextualDesignators`](20250801/ContextualDesignators/) | 上下文指称 | 特定上下文中有意义的指称、名称和标识符 |
| [`ContextualIdentifiers`](20250801/ContextualIdentifiers/) | 上下文标识符 | 特定上下文或情境中使用的标识符 |
| [`DatesAndTimes`](20250801/DatesAndTimes/) | 日期与时间 | 日期、时间、时间段及其表示方式 |
| [`Designators`](20250801/Designators/) | 指称 | 名称、标识符等指称事物的通用概念 |
| [`Documents`](20250801/Documents/) | 文档 | 文档、记录及其组成部分 |
| [`Identifiers`](20250801/Identifiers/) | 标识符 | 标识符及其发布、管理与解析 |
| [`Languages`](20250801/Languages/) | 语言 | 语言、语言标签及其相关概念 |
| [`Locations`](20250801/Locations/) | 位置 | 地址、地理区域、位置及其关系 |
| [`Organizations`](20250801/Organizations/) | 组织 | 组织、组织单元及其标识和关系 |
| [`PartiesAndSituations`](20250801/PartiesAndSituations/) | 参与方与情境 | 参与方、角色、情境及其关系，FIBO 直接依赖 |
| [`QuantitiesAndUnits`](20250801/QuantitiesAndUnits/) | 量与单位 | 数量、度量单位、量纲及其转换 |
| [`RegistrationAuthorities`](20250801/RegistrationAuthorities/) | 注册机构 | 注册机构、注册标识符及其管理 |
| [`RegulatoryAgencies`](20250801/RegulatoryAgencies/) | 监管机构 | 监管机构、监管角色及其关系 |
| [`RolesAndCompositions`](20250801/RolesAndCompositions/) | 角色与组合 | 角色、组合及其扮演/组成关系，FIBO 直接依赖 |
| [`SitesAndFacilities`](20250801/SitesAndFacilities/) | 场所与设施 | 场所、设施、地址及其关系 |
| [`StructuredCollections`](20250801/StructuredCollections/) | 结构化集合 | 具有特定结构或模式的集合，如序列、层次结构 |
| [`TextDatatype`](20250801/TextDatatype/) | 文本数据类型 | 文本、字符串及其数据类型 |

## 5. 中文标注说明

每个模块目录下都有两个文件：

- `<ModuleName>.rdf`：OMG 官方原始 RDF/XML，未修改。
- `<ModuleName>.ttl`：转换后的 Turtle，包含中文标注。

中文标注目前分为两层：

1. **文件级**：每个 `.ttl` 都为本体文件添加了 `rdfs:label` 和 `rdfs:comment`（带 `@zh`），例如 `Commons 参与方与情境本体（Commons Parties and Situations Ontology）`。
2. **术语级**：FIBO 直接引用的 3 个核心模块——`PartiesAndSituations`、`RolesAndCompositions`、`AnnotationVocabulary`——中的类、对象属性和标注属性已逐条加入 `rdfs:label` 和 `rdfs:comment`（`中文（English）` 格式）。

其余模块目前仅保留官方英文术语标签。后续可以参照核心模块的方式逐模块补全中文标签；转换脚本位于 [`../../tools/nightly/convert_commons_to_ttl.py`](../../tools/nightly/convert_commons_to_ttl.py)，可重复运行。

## 6. 技术基础

与 FIBO 一样，Commons 使用 W3C OWL 编写，以 RDF 序列化。本快照中的 `.rdf` 为 RDF/XML，`.ttl` 为 Turtle。每个模块通过 `owl:imports` 引用其他模块，构成一个分层的上层本体网络。

## 7. 许可证

所有 Commons 本体文件均采用 MIT 许可证，详见各 `.rdf` 文件中的 `dct:license` 内容。
