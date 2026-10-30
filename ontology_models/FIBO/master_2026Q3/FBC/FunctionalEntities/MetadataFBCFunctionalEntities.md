# FBC 功能实体模块元数据（Metadata for the FBC Functional Entities Module）说明

本文档对应 `MetadataFBCFunctionalEntities.rdf` / `MetadataFBCFunctionalEntities.ttl`。

![FBC 功能实体模块元数据（Metadata for the FBC Functional Entities Module）结构图](MetadataFBCFunctionalEntities-structure.png)

## 1. 本文件是什么

声明功能实体（Functional Entities）模块的构成：金融服务实体、市场、监管机构、商业登记、商业中心及欧美区域扩展、各国参考个体等本体。

从机制上说，这是一个元数据清单（metadata manifest）文件：它本身不定义任何类或属性，而是通过 `dct:hasPart` 声明一个域或模块由哪些本体构成，并携带版本 IRI、版权、许可与成熟度等发布管理信息。它回答的问题是「这个域/模块包含什么、当前是什么版本」，供发布工具和文档系统按模块组织内容；它的 `owl:imports` 只引入标注词汇表，不是用来加载业务本体的入口（加载入口是 `All*` 与 `About*` 聚合文件）。

## 2. 声明的构成（dct:hasPart，17 个）

| 构成项 | 中文名称 | 简介 |
|---|---|---|
| `FBC/FunctionalEntities/BusinessCenters.rdf` | 商业中心本体（Business Centers Ontology） | 定义金融中心、商业中心等功能性地点概念，用于确定市场所在地与营业日历。 |
| `FBC/FunctionalEntities/BusinessCentersIndividuals.rdf` | 商业中心个体本体（Business Centers Individuals） | 收录全球主要商业中心（如纽约、伦敦、东京）的参考个体。 |
| `FBC/FunctionalEntities/BusinessRegistries.rdf` | 商业登记机构本体（Business Registries Ontology） | 定义商业登记机构（如公司注册处）及其登记职能。 |
| `FBC/FunctionalEntities/CommercialRegistrationAuthorities.rdf` | 商事登记主管机关本体（Commercial Registration Authorities Ontology） | 定义负责商事登记的主管机关及其维护的登记记录。 |
| `FBC/FunctionalEntities/EuropeanEntities/EUFinancialServicesEntities.rdf` | 欧盟金融服务实体本体（EU Financial Services Entities Ontology） | 定义欧盟法域下的金融服务机构类型与个体。 |
| `FBC/FunctionalEntities/EuropeanEntities/EURegulatoryAgencies.rdf` | 欧盟监管机构本体（EU Regulatory Agencies Ontology） | 收录欧盟层面的金融监管机构个体（如欧洲央行、欧洲证券和市场管理局 ESMA）。 |
| `FBC/FunctionalEntities/EuropeanEntities/EuropeanFinancialServicesEntitiesIndividuals.rdf` | 欧洲金融服务实体个体本体（European Financial Services Entities Individuals Ontology） | 收录欧洲各国金融服务机构与市场的参考个体。 |
| `FBC/FunctionalEntities/FinancialServicesEntities.rdf` | 金融服务实体本体（Financial Services Entities Ontology） | FBC 域核心本体，定义金融服务机构（银行、券商、保险公司、资管机构等）的功能分类体系。 |
| `FBC/FunctionalEntities/InternationalRegistriesAndAuthorities.rdf` | 国际登记与主管机构本体（International Registries and Authorities Ontology） | 收录国际性登记机构与主管当局的参考个体。 |
| `FBC/FunctionalEntities/Markets.rdf` | 市场本体（Markets Ontology） | 定义金融市场（market）：交易所、场外市场及其功能。 |
| `FBC/FunctionalEntities/MarketsIndividuals.rdf` | 市场个体本体（Markets Individuals） | 收录全球主要金融市场的参考个体。 |
| `FBC/FunctionalEntities/NorthAmericanEntities/CAFinancialServicesEntities.rdf` | 加拿大金融服务实体本体（Canadian Financial Services Entities Ontology） | 定义加拿大法域下的金融服务机构类型与个体。 |
| `FBC/FunctionalEntities/NorthAmericanEntities/CARegulatoryAgencies.rdf` | 加拿大监管机构本体（Canadian Regulatory Agencies Ontology） | 收录加拿大金融监管机构个体（如加拿大金融机构监管署 OSFI）。 |
| `FBC/FunctionalEntities/NorthAmericanEntities/USFinancialServicesEntities.rdf` | 美国金融服务实体本体（US Financial Services Entities Ontology） | 定义美国法域下的金融服务机构类型与个体。 |
| `FBC/FunctionalEntities/NorthAmericanEntities/USNationalInformationCenterControlledVocabularies.rdf` | 美国国家信息中心受控词汇本体（US NIC Controlled Vocabularies Ontology） | 收录美联储国家信息中心（NIC）用于描述金融机构属性的受控词汇个体。 |
| `FBC/FunctionalEntities/NorthAmericanEntities/USRegulatoryAgencies.rdf` | 美国监管机构本体（US Regulatory Agencies Ontology） | 收录美国金融监管机构个体（如美联储、证监会 SEC、货币监理署 OCC）。 |
| `FBC/FunctionalEntities/RegulatoryAgencies.rdf` | 监管机构本体（Regulatory Agencies Ontology） | 定义金融监管机构（regulatory agency）及其监管职能的通用概念。 |

## 3. 标注依赖（owl:imports，2 个）

以下导入仅用于支撑元数据标注本身（如成熟度等级、概念映射），不属于业务内容：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |

## 4. 文件

- 官方 RDF/XML：`MetadataFBCFunctionalEntities.rdf`
- 中文 Turtle：`MetadataFBCFunctionalEntities.ttl`
- 结构图：`MetadataFBCFunctionalEntities-structure.png` / `MetadataFBCFunctionalEntities-structure.svg`