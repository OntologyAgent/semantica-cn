# BP 证券发行模块元数据（Metadata for the BP Securities Issuance Module）说明

本文档对应 `MetadataBPSecuritiesIssuance.rdf` / `MetadataBPSecuritiesIssuance.ttl`。

![BP 证券发行模块元数据（Metadata for the BP Securities Issuance Module）结构图](MetadataBPSecuritiesIssuance-structure.png)

## 1. 本文件是什么

声明证券发行（Securities Issuance）模块的构成：发行流程、发行文件、债务发行、IPO 发行、MBS 发行（机构/私人品牌）、市政债发行等本体。

从机制上说，这是一个元数据清单（metadata manifest）文件：它本身不定义任何类或属性，而是通过 `dct:hasPart` 声明一个域或模块由哪些本体构成，并携带版本 IRI、版权、许可与成熟度等发布管理信息。它回答的问题是「这个域/模块包含什么、当前是什么版本」，供发布工具和文档系统按模块组织内容；它的 `owl:imports` 只引入标注词汇表，不是用来加载业务本体的入口（加载入口是 `All*` 与 `About*` 聚合文件）。

## 2. 声明的构成（dct:hasPart，8 个）

| 构成项 | 中文名称 | 简介 |
|---|---|---|
| `BP/SecuritiesIssuance/AgencyMBSIssuance.rdf` | 机构 MBS 发行本体（Agency MBS Issuance Ontology） | 定义机构抵押贷款支持证券（agency MBS，如房利美、房地美发行）的发行流程。 |
| `BP/SecuritiesIssuance/DebtIssuance.rdf` | 债务发行本体（Debt Issuance Ontology） | 定义债券等债务工具的发行流程与参与方。 |
| `BP/SecuritiesIssuance/EquitiesIPOIssuance.rdf` | 股票首次公开发行本体（Equities IPO Issuance Ontology） | 定义首次公开发行（IPO）的流程、阶段与参与方。 |
| `BP/SecuritiesIssuance/IssuanceDocuments.rdf` | 发行文件本体（Issuance Documents Ontology） | 定义证券发行过程中使用的法律文件：募集说明书、条款清单等。 |
| `BP/SecuritiesIssuance/IssuanceProcess.rdf` | 发行流程本体（Issuance Process Ontology） | 定义证券发行的通用流程框架：从筹划、定价到配售的各阶段。 |
| `BP/SecuritiesIssuance/MBSIssuance.rdf` | MBS 发行本体（MBS Issuance Ontology） | 定义抵押贷款支持证券（MBS）发行的通用流程：资产池组建、分层与发售。 |
| `BP/SecuritiesIssuance/MuniIssuance.rdf` | 市政债发行本体（Municipal Issuance Ontology） | 定义美国市政债券（municipal bond）的发行流程。 |
| `BP/SecuritiesIssuance/PrivateLabelMBSIssuance.rdf` | 私人品牌 MBS 发行本体（Private Label MBS Issuance Ontology） | 定义私人机构（非政府机构）发行抵押贷款支持证券的流程。 |

## 3. 标注依赖（owl:imports，2 个）

以下导入仅用于支撑元数据标注本身（如成熟度等级、概念映射），不属于业务内容：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |

## 4. 文件

- 官方 RDF/XML：`MetadataBPSecuritiesIssuance.rdf`
- 中文 Turtle：`MetadataBPSecuritiesIssuance.ttl`
- 结构图：`MetadataBPSecuritiesIssuance-structure.png` / `MetadataBPSecuritiesIssuance-structure.svg`