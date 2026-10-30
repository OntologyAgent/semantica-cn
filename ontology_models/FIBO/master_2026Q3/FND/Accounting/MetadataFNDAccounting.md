# FND 会计模块元数据（Metadata for the FND Accounting Module）说明

本文档对应 `MetadataFNDAccounting.rdf` / `MetadataFNDAccounting.ttl`。

![FND 会计模块元数据（Metadata for the FND Accounting Module）结构图](MetadataFNDAccounting-structure.png)

## 1. 本文件是什么

声明会计（Accounting）模块由货币金额、现金流、ISO 4217 货币代码三个本体构成，及版本信息。

从机制上说，这是一个元数据清单（metadata manifest）文件：它本身不定义任何类或属性，而是通过 `dct:hasPart` 声明一个域或模块由哪些本体构成，并携带版本 IRI、版权、许可与成熟度等发布管理信息。它回答的问题是「这个域/模块包含什么、当前是什么版本」，供发布工具和文档系统按模块组织内容；它的 `owl:imports` 只引入标注词汇表，不是用来加载业务本体的入口（加载入口是 `All*` 与 `About*` 聚合文件）。

## 2. 声明的构成（dct:hasPart，3 个）

| 构成项 | 中文名称 | 简介 |
|---|---|---|
| `FND/Accounting/CashFlows.rdf` | 现金流本体（Cash Flows Ontology） | 定义现金流（cash flow）的概念结构：现金的流入与流出、预计现金流与实际现金流、现金流金额等，用于财务分析与会计报表场景。 |
| `FND/Accounting/CurrencyAmount.rdf` | 货币金额本体（Currency Amount Ontology） | 定义「金额＋币种」的货币金额（currency amount）表示，是 FIBO 中表达价格、债务金额、付款额等一切带币种数值的基础构件。 |
| `FND/Accounting/ISO4217-CurrencyCodes.rdf` | ISO 4217 货币代码本体（ISO 4217-1 Currency Codes Ontology） | 收录 ISO 4217-1 标准的全部货币代码个体（如 USD、CNY、EUR），为货币金额提供标准化的币种取值。 |

## 3. 标注依赖（owl:imports，2 个）

以下导入仅用于支撑元数据标注本身（如成熟度等级、概念映射），不属于业务内容：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |

## 4. 文件

- 官方 RDF/XML：`MetadataFNDAccounting.rdf`
- 中文 Turtle：`MetadataFNDAccounting.ttl`
- 结构图：`MetadataFNDAccounting-structure.png` / `MetadataFNDAccounting-structure.svg`