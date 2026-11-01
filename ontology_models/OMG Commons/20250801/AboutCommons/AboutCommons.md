# Commons 库总入口（About Commons）聚合说明

本文档对应 `AboutCommons.rdf` / `AboutCommons.ttl`。

![Commons 库总入口（About Commons）聚合结构图](AboutCommons-structure.png)

## 1. 本文件是什么

聚合 OMG 通用本体库（Commons）全部 22 个模块，一次导入即获得完整 Commons 概念体系，是使用 Commons 的标准入口。

从机制上说，这是一个聚合入口（load-all）文件：它本身不定义任何新的类或属性，只通过 `owl:imports` 把一组本体打包在一起。应用只要导入这一个文件，推理机就会把它列出的所有本体一次性加载进来，免去逐个声明的麻烦。因此它的价值不在「内容」，而在「组合」——组合方式本身就表达了发布方的意图（例如按域打包、按区域扩展打包、按是否含参考数据打包）。

## 2. 聚合的本地本体（22 个）

以下本体均可在本目录结构中找到同名 `.rdf` 文件及配套中文文档：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `AnnotationVocabulary/AnnotationVocabulary.rdf` | Commons 标注词汇表（Commons Annotation Vocabulary） | 提供文档标注常用的属性，如摘要、定义、解释、版权、同义词等，并梳理 SKOS 与 Dublin Core 标注属性之间的关系。 |
| `BusinessAuthorizations/BusinessAuthorizations.rdf` | Commons 业务授权本体（Commons Business Authorizations Ontology） | 定义业务授权、许可及其相关角色和关系。 |
| `Classifiers/Classifiers.rdf` | Commons 分类器本体（Commons Classifiers Ontology） | 定义用于对事物进行分类、分面或归类的通用概念。 |
| `CodesAndCodeSets/CodesAndCodeSets.rdf` | Commons 代码与代码集本体（Commons Codes and Code Sets Ontology） | 定义代码、代码集、编码方案及其标识方式。 |
| `Collections/Collections.rdf` | Commons 集合本体（Commons Collections Ontology） | 定义集合、成员关系及集合操作的基础概念。 |
| `ContextualDesignators/ContextualDesignators.rdf` | Commons 上下文指称本体（Commons Contextual Designators Ontology） | 定义在特定上下文中有意义的指称、名称和标识符。 |
| `ContextualIdentifiers/ContextualIdentifiers.rdf` | Commons 上下文标识符本体（Commons Contextual Identifiers Ontology） | 定义在特定上下文或情境中使用的标识符。 |
| `DatesAndTimes/DatesAndTimes.rdf` | Commons 日期与时间本体（Commons Dates and Times Ontology） | 定义日期、时间、时间段及其表示方式。 |
| `Designators/Designators.rdf` | Commons 指称本体（Commons Designators Ontology） | 定义名称、标识符等指称事物的通用概念。 |
| `Documents/Documents.rdf` | Commons 文档本体（Commons Documents Ontology） | 定义文档、记录及其组成部分的通用概念。 |
| `Identifiers/Identifiers.rdf` | Commons 标识符本体（Commons Identifiers Ontology） | 定义标识符及其发布、管理与解析的基础概念。 |
| `Languages/Languages.rdf` | Commons 语言本体（Commons Languages Ontology） | 定义语言、语言标签及其相关概念。 |
| `Locations/Locations.rdf` | Commons 位置本体（Commons Locations Ontology） | 定义地址、地理区域、位置及其关系。 |
| `Organizations/Organizations.rdf` | Commons 组织本体（Commons Organizations Ontology） | 定义组织、组织单元及其标识和关系。 |
| `PartiesAndSituations/PartiesAndSituations.rdf` | Commons 参与方与情境本体（Commons Parties and Situations Ontology） | 定义参与方、角色、情境以及它们之间关系的高层概念，是 FIBO 等多领域的上层本体。 |
| `QuantitiesAndUnits/QuantitiesAndUnits.rdf` | Commons 量与单位本体（Commons Quantities and Units Ontology） | 定义数量、度量单位、量纲及其转换。 |
| `RegistrationAuthorities/RegistrationAuthorities.rdf` | Commons 注册机构本体（Commons Registration Authorities Ontology） | 定义注册机构、注册标识符及其管理。 |
| `RegulatoryAgencies/RegulatoryAgencies.rdf` | Commons 监管机构本体（Commons Regulatory Agencies Ontology） | 定义监管机构、监管角色及其关系。 |
| `RolesAndCompositions/RolesAndCompositions.rdf` | Commons 角色与组合本体（Commons Roles and Compositions Ontology） | 定义角色、组合及其扮演/组成关系的基础本体。 |
| `SitesAndFacilities/SitesAndFacilities.rdf` | Commons 场所与设施本体（Commons Sites and Facilities Ontology） | 定义场所、设施、地址及其关系。 |
| `StructuredCollections/StructuredCollections.rdf` | Commons 结构化集合本体（Commons Structured Collections Ontology） | 定义具有特定结构或模式的集合，如序列、层次结构等。 |
| `TextDatatype/TextDatatype.rdf` | Commons 文本数据类型本体（Commons Text Datatype Ontology） | 定义文本、字符串及其数据类型的基础概念。 |

## 3. 文件

- 官方 RDF/XML：`AboutCommons.rdf`
- 中文 Turtle：`AboutCommons.ttl`
- 结构图：`AboutCommons-structure.png` / `AboutCommons-structure.svg`