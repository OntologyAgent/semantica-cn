# 美国政府实体与法域本体（US Government Entities and Jurisdictions Ontology）说明

本文档对应 `USGovernmentEntitiesAndJurisdictions.rdf` / `USGovernmentEntitiesAndJurisdictions.ttl`。

![美国政府实体与法域本体（US Government Entities and Jurisdictions Ontology）结构图](USGovernmentEntitiesAndJurisdictions-structure.png)

## 1. 本文件是什么

收录美国的政体、联邦与各州政府、法域个体，是北美金融建模最常用的法域参考数据。

从机制上说，这是一个个体（individuals）文件：它本身不定义任何新的类或属性，装的全是命名个体（owl:NamedIndividual）——也就是一条条真实存在的实例数据（如具体的货币、市场、监管机构、法域）。它的 `owl:imports` 引入的是这些个体所属的类定义所在的本体。应用需要实例级参考数据时加载这类文件。

## 2. 个体构成（共 171 个）

按个体所属类型统计（类型名为中文（English）对照）：

| 类型（Class） | 个体数量 |
|---|---|
| 管辖权（Jurisdiction） | 57 |
| 地区主权体（RegionalSovereignty） | 56 |
| 地区政府（RegionalGovernment） | 56 |
| 联邦主权体（FederatedSovereignty） | 1 |
| 联邦政府（FederalGovernment） | 1 |

个体数量较多，仅举前 10 个示例，完整清单见同名 `.ttl` 文件：

| 个体（示例） | 类型 |
|---|---|
| American Samoa entity | 地区主权体（RegionalSovereignty） |
| American Samoa jurisdiction | 管辖权（Jurisdiction） |
| Commonwealth of Puerto Rico entity | 地区主权体（RegionalSovereignty） |
| Commonwealth of the Northern Mariana Islands entity | 地区主权体（RegionalSovereignty） |
| District of Columbia entity | 地区主权体（RegionalSovereignty） |
| District of Columbia government | 地区政府（RegionalGovernment） |
| District of Columbia jurisdiction | 管辖权（Jurisdiction） |
| Guam entity | 地区主权体（RegionalSovereignty） |
| Guam jurisdiction | 管辖权（Jurisdiction） |
| Northern Mariana Islands jurisdiction | 管辖权（Jurisdiction） |

## 3. 依赖的本体（owl:imports，6 个）

以下导入提供个体所属的类定义与相关参考数据：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `BE/GovernmentEntities/GovernmentEntities.rdf` | 政府实体本体（Government Entities Ontology） | 定义政府、政体（polity）、法域（jurisdiction）及政府实体的核心概念，是各区域政府实体本体的共同基础。 |
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |
| `https://www.omg.org/spec/Commons/RegulatoryAgencies/` | OMG 通用监管机构本体（OMG Commons Regulatory Agencies） | Commons 库中的监管机构本体，定义监管机构及其监管职权的通用概念。 |
| `https://www.omg.org/spec/LCC/Countries/ISO3166-1-CountryCodes/` | LCC ISO 3166-1 国家代码（ISO 3166-1 Country Codes） | LCC 中 ISO 3166-1 标准的国家/地区代码个体集（如 CN、US、MX），供法域与地址建模引用。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-US/` | LCC ISO 3166-2 子分区代码·US（ISO 3166-2 Subdivision Codes for 美国） | LCC 中 ISO 3166-2 标准下美国的省/州级行政区代码个体集。 |

## 4. 文件

- 官方 RDF/XML：`USGovernmentEntitiesAndJurisdictions.rdf`
- 中文 Turtle：`USGovernmentEntitiesAndJurisdictions.ttl`
- 结构图：`USGovernmentEntitiesAndJurisdictions-structure.png` / `USGovernmentEntitiesAndJurisdictions-structure.svg`