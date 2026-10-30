# 英国政府实体与法域本体（UK Government Entities and Jurisdictions Ontology）说明

本文档对应 `UKGovernmentEntitiesAndJurisdictions.rdf` / `UKGovernmentEntitiesAndJurisdictions.ttl`。

![英国政府实体与法域本体（UK Government Entities and Jurisdictions Ontology）结构图](UKGovernmentEntitiesAndJurisdictions-structure.png)

## 1. 本文件是什么

收录大不列颠及北爱尔兰联合王国的政体、政府与法域个体（英格兰、苏格兰、威尔士、北爱尔兰）。

从机制上说，这是一个个体（individuals）文件：它本身不定义任何新的类或属性，装的全是命名个体（owl:NamedIndividual）——也就是一条条真实存在的实例数据（如具体的货币、市场、监管机构、法域）。它的 `owl:imports` 引入的是这些个体所属的类定义所在的本体。应用需要实例级参考数据时加载这类文件。

## 2. 个体构成（共 21 个）

按个体所属类型统计（类型名为中文（English）对照）：

| 类型（Class） | 个体数量 |
|---|---|
| 管辖权（Jurisdiction） | 7 |
| 地区政府（RegionalGovernment） | 6 |
| 地区主权体（RegionalSovereignty） | 6 |
| 权力下放政府（DevolvedGovernment） | 3 |
| 国家政府（NationalGovernment） | 1 |
| 主权国家（SovereignState） | 1 |

个体数量较多，仅举前 10 个示例，完整清单见同名 `.ttl` 文件：

| 个体（示例） | 类型 |
|---|---|
| England and Wales jurisdiction | 管辖权（Jurisdiction） |
| Government of Guernsey | 地区政府（RegionalGovernment） |
| Government of Jersey | 地区政府（RegionalGovernment） |
| Government of Scotland | 权力下放政府（DevolvedGovernment）、地区政府（RegionalGovernment） |
| Government of the Isle of Man | 地区政府（RegionalGovernment） |
| Government of the United Kingdom | 国家政府（NationalGovernment） |
| Guernsey entity | 地区主权体（RegionalSovereignty） |
| Isle of Man entity | 地区主权体（RegionalSovereignty） |
| Jersey entity | 地区主权体（RegionalSovereignty） |
| National Assembly for Wales | 权力下放政府（DevolvedGovernment）、地区政府（RegionalGovernment） |

## 3. 依赖的本体（owl:imports，6 个）

以下导入提供个体所属的类定义与相关参考数据：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `BE/GovernmentEntities/GovernmentEntities.rdf` | 政府实体本体（Government Entities Ontology） | 定义政府、政体（polity）、法域（jurisdiction）及政府实体的核心概念，是各区域政府实体本体的共同基础。 |
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |
| `https://www.omg.org/spec/Commons/RegulatoryAgencies/` | OMG 通用监管机构本体（OMG Commons Regulatory Agencies） | Commons 库中的监管机构本体，定义监管机构及其监管职权的通用概念。 |
| `https://www.omg.org/spec/LCC/Countries/ISO3166-1-CountryCodes/` | LCC ISO 3166-1 国家代码（ISO 3166-1 Country Codes） | LCC 中 ISO 3166-1 标准的国家/地区代码个体集（如 CN、US、MX），供法域与地址建模引用。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-GB/` | LCC ISO 3166-2 子分区代码·GB（ISO 3166-2 Subdivision Codes for 英国） | LCC 中 ISO 3166-2 标准下英国的省/州级行政区代码个体集。 |

## 4. 文件

- 官方 RDF/XML：`UKGovernmentEntitiesAndJurisdictions.rdf`
- 中文 Turtle：`UKGovernmentEntitiesAndJurisdictions.ttl`
- 结构图：`UKGovernmentEntitiesAndJurisdictions-structure.png` / `UKGovernmentEntitiesAndJurisdictions-structure.svg`