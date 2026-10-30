# LOAN 域元数据（Metadata for the LOAN Domain）说明

本文档对应 `MetadataLOAN.rdf` / `MetadataLOAN.ttl`。

![LOAN 域元数据（Metadata for the LOAN Domain）结构图](MetadataLOAN-structure.png)

## 1. 本文件是什么

声明贷款（LOAN）域由三个模块构成：贷款通用、具体贷款、房地产贷款。

从机制上说，这是一个元数据清单（metadata manifest）文件：它本身不定义任何类或属性，而是通过 `dct:hasPart` 声明一个域或模块由哪些本体构成，并携带版本 IRI、版权、许可与成熟度等发布管理信息。它回答的问题是「这个域/模块包含什么、当前是什么版本」，供发布工具和文档系统按模块组织内容；它的 `owl:imports` 只引入标注词汇表，不是用来加载业务本体的入口（加载入口是 `All*` 与 `About*` 聚合文件）。

## 2. 声明的构成（dct:hasPart，3 个）

| 构成项 | 中文名称 | 简介 |
|---|---|---|
| `LOAN/LoansGeneral/MetadataLOANLoansGeneral.rdf` | LOAN 贷款通用模块元数据（Metadata for the LOAN Loans General Module） | 声明贷款通用（Loans General）模块由贷款、贷款申请、贷款事件、贷款监管四个本体构成，及版本信息。 |
| `LOAN/LoansSpecific/MetadataLOANLoansSpecific.rdf` | LOAN 具体贷款模块元数据（Metadata for the LOAN Loans Specific Module） | 声明具体贷款（Loans Specific）模块的构成：卡账户、商业贷款、消费贷款、学生贷款、绿色贷款、船舶融资、贷款产品七个本体。 |
| `LOAN/RealEstateLoans/MetadataLOANRealEstateLoans.rdf` | LOAN 房地产贷款模块元数据（Metadata for the LOAN Real Estate Loans Module） | 声明房地产贷款（Real Estate Loans）模块由抵押贷款、抵押贷款发放、建筑贷款、HMDA 覆盖抵押贷款四个本体构成，及版本信息。 |

## 3. 标注依赖（owl:imports，5 个）

以下导入仅用于支撑元数据标注本身（如成熟度等级、概念映射），不属于业务内容：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `LOAN/LoansGeneral/MetadataLOANLoansGeneral.rdf` | LOAN 贷款通用模块元数据（Metadata for the LOAN Loans General Module） | 声明贷款通用（Loans General）模块由贷款、贷款申请、贷款事件、贷款监管四个本体构成，及版本信息。 |
| `LOAN/LoansSpecific/MetadataLOANLoansSpecific.rdf` | LOAN 具体贷款模块元数据（Metadata for the LOAN Loans Specific Module） | 声明具体贷款（Loans Specific）模块的构成：卡账户、商业贷款、消费贷款、学生贷款、绿色贷款、船舶融资、贷款产品七个本体。 |
| `LOAN/RealEstateLoans/MetadataLOANRealEstateLoans.rdf` | LOAN 房地产贷款模块元数据（Metadata for the LOAN Real Estate Loans Module） | 声明房地产贷款（Real Estate Loans）模块由抵押贷款、抵押贷款发放、建筑贷款、HMDA 覆盖抵押贷款四个本体构成，及版本信息。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |

## 4. 文件

- 官方 RDF/XML：`MetadataLOAN.rdf`
- 中文 Turtle：`MetadataLOAN.ttl`
- 结构图：`MetadataLOAN-structure.png` / `MetadataLOAN-structure.svg`