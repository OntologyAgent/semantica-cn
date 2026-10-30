# LOAN 房地产贷款模块元数据（Metadata for the LOAN Real Estate Loans Module）说明

本文档对应 `MetadataLOANRealEstateLoans.rdf` / `MetadataLOANRealEstateLoans.ttl`。

![LOAN 房地产贷款模块元数据（Metadata for the LOAN Real Estate Loans Module）结构图](MetadataLOANRealEstateLoans-structure.png)

## 1. 本文件是什么

声明房地产贷款（Real Estate Loans）模块由抵押贷款、抵押贷款发放、建筑贷款、HMDA 覆盖抵押贷款四个本体构成，及版本信息。

从机制上说，这是一个元数据清单（metadata manifest）文件：它本身不定义任何类或属性，而是通过 `dct:hasPart` 声明一个域或模块由哪些本体构成，并携带版本 IRI、版权、许可与成熟度等发布管理信息。它回答的问题是「这个域/模块包含什么、当前是什么版本」，供发布工具和文档系统按模块组织内容；它的 `owl:imports` 只引入标注词汇表，不是用来加载业务本体的入口（加载入口是 `All*` 与 `About*` 聚合文件）。

## 2. 声明的构成（dct:hasPart，4 个）

| 构成项 | 中文名称 | 简介 |
|---|---|---|
| `LOAN/RealEstateLoans/ConstructionLoans.rdf` | 建筑贷款本体（Construction Loans Ontology） | 定义用于房地产建设、按工程进度阶段性放款的建筑贷款。 |
| `LOAN/RealEstateLoans/HomeMortgageDisclosureActCoveredMortgages.rdf` | HMDA 覆盖抵押贷款本体（HMDA Covered Mortgages Ontology） | 定义受美国《住房抵押贷款披露法》（HMDA）报告要求约束的抵押贷款。 |
| `LOAN/RealEstateLoans/MortgageOrigination.rdf` | 抵押贷款发放本体（Mortgage Origination Ontology） | 定义抵押贷款的发起与发放流程。 |
| `LOAN/RealEstateLoans/Mortgages.rdf` | 抵押贷款本体（Mortgages Ontology） | 定义以不动产为抵押的贷款：抵押物、抵押登记与止赎。 |

## 3. 标注依赖（owl:imports，2 个）

以下导入仅用于支撑元数据标注本身（如成熟度等级、概念映射），不属于业务内容：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |

## 4. 文件

- 官方 RDF/XML：`MetadataLOANRealEstateLoans.rdf`
- 中文 Turtle：`MetadataLOANRealEstateLoans.ttl`
- 结构图：`MetadataLOANRealEstateLoans-structure.png` / `MetadataLOANRealEstateLoans-structure.svg`