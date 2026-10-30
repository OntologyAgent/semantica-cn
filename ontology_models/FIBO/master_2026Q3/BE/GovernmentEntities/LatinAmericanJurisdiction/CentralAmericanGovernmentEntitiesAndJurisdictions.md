# 中美洲政府实体与法域本体（Central American Government Entities and Jurisdictions Ontology）说明

本文档对应 `CentralAmericanGovernmentEntitiesAndJurisdictions.rdf` / `CentralAmericanGovernmentEntitiesAndJurisdictions.ttl`。

![中美洲政府实体与法域本体（Central American Government Entities and Jurisdictions Ontology）结构图](CentralAmericanGovernmentEntitiesAndJurisdictions-structure.png)

## 1. 本文件是什么

收录中美洲各国（巴拿马、哥斯达黎加等）的政体、政府与法域个体。

从机制上说，这是一个个体（individuals）文件：它本身不定义任何新的类或属性，装的全是命名个体（owl:NamedIndividual）——也就是一条条真实存在的实例数据（如具体的货币、市场、监管机构、法域）。它的 `owl:imports` 引入的是这些个体所属的类定义所在的本体。应用需要实例级参考数据时加载这类文件。

## 2. 个体构成（共 21 个）

按个体所属类型统计（类型名为中文（English）对照）：

| 类型（Class） | 个体数量 |
|---|---|
| 主权国家（SovereignState） | 7 |
| 国家政府（NationalGovernment） | 7 |
| 管辖权（Jurisdiction） | 7 |

个体数量较多，仅举前 10 个示例，完整清单见同名 `.ttl` 文件：

| 个体（示例） | 类型 |
|---|---|
| Belizean entity | 主权国家（SovereignState） |
| Costa Rican entity | 主权国家（SovereignState） |
| Government of Belize | 国家政府（NationalGovernment） |
| Government of the Republic of Costa Rica | 国家政府（NationalGovernment） |
| Government of the Republic of El Salvador | 国家政府（NationalGovernment） |
| Government of the Republic of Guatemala | 国家政府（NationalGovernment） |
| Government of the Republic of Honduras | 国家政府（NationalGovernment） |
| Government of the Republic of Nicaragua | 国家政府（NationalGovernment） |
| Government of the Republic of Panama | 国家政府（NationalGovernment） |
| Guatemalan entity | 主权国家（SovereignState） |

## 3. 依赖的本体（owl:imports，5 个）

以下导入提供个体所属的类定义与相关参考数据：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `BE/GovernmentEntities/GovernmentEntities.rdf` | 政府实体本体（Government Entities Ontology） | 定义政府、政体（polity）、法域（jurisdiction）及政府实体的核心概念，是各区域政府实体本体的共同基础。 |
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |
| `https://www.omg.org/spec/Commons/RegulatoryAgencies/` | OMG 通用监管机构本体（OMG Commons Regulatory Agencies） | Commons 库中的监管机构本体，定义监管机构及其监管职权的通用概念。 |
| `https://www.omg.org/spec/LCC/Countries/ISO3166-1-CountryCodes/` | LCC ISO 3166-1 国家代码（ISO 3166-1 Country Codes） | LCC 中 ISO 3166-1 标准的国家/地区代码个体集（如 CN、US、MX），供法域与地址建模引用。 |

## 4. 文件

- 官方 RDF/XML：`CentralAmericanGovernmentEntitiesAndJurisdictions.rdf`
- 中文 Turtle：`CentralAmericanGovernmentEntitiesAndJurisdictions.ttl`
- 结构图：`CentralAmericanGovernmentEntitiesAndJurisdictions-structure.png` / `CentralAmericanGovernmentEntitiesAndJurisdictions-structure.svg`