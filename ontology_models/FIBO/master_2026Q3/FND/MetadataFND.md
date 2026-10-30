# FND 域元数据（Metadata for the FND Domain）说明

本文档对应 `MetadataFND.rdf` / `MetadataFND.ttl`。

![FND 域元数据（Metadata for the FND Domain）结构图](MetadataFND-structure.png)

## 1. 本文件是什么

声明基础（Foundations，FND）域由 15 个模块构成：会计、代理人与人员、协议、安排、日期与时间、目标、法律、组织、所有权与控制、参与方、地点、产品与服务、关系、交易扩展、工具。

从机制上说，这是一个元数据清单（metadata manifest）文件：它本身不定义任何类或属性，而是通过 `dct:hasPart` 声明一个域或模块由哪些本体构成，并携带版本 IRI、版权、许可与成熟度等发布管理信息。它回答的问题是「这个域/模块包含什么、当前是什么版本」，供发布工具和文档系统按模块组织内容；它的 `owl:imports` 只引入标注词汇表，不是用来加载业务本体的入口（加载入口是 `All*` 与 `About*` 聚合文件）。

## 2. 声明的构成（dct:hasPart，15 个）

| 构成项 | 中文名称 | 简介 |
|---|---|---|
| `FND/Accounting/MetadataFNDAccounting.rdf` | FND 会计模块元数据（Metadata for the FND Accounting Module） | 声明会计（Accounting）模块由货币金额、现金流、ISO 4217 货币代码三个本体构成，及版本信息。 |
| `FND/AgentsAndPeople/MetadataFNDAgentsAndPeople.rdf` | FND 代理人与人员模块元数据（Metadata for the FND Agents and People Module） | 声明代理人与人员（Agents and People）模块由人员本体构成，及版本信息。 |
| `FND/Agreements/MetadataFNDAgreements.rdf` | FND 协议模块元数据（Metadata for the FND Agreements Module） | 声明协议（Agreements）模块由协议本体与合同本体构成，及版本信息。 |
| `FND/Arrangements/MetadataFNDArrangements.rdf` | FND 安排模块元数据（Metadata for the FND Arrangements Module） | 声明安排（Arrangements）模块的构成：安排、分类方案、标识符与索引、文档、生命周期、评估、评级、报告八个本体。 |
| `FND/DatesAndTimes/MetadataFNDDatesAndTimes.rdf` | FND 日期与时间模块元数据（Metadata for the FND Dates and Times Module） | 声明日期与时间（Dates and Times）模块由金融日期、营业日期、事件与发生三个本体构成，及版本信息。 |
| `FND/GoalsAndObjectives/MetadataFNDGoalsAndObjectives.rdf` | FND 目标模块元数据（Metadata for the FND Goals and Objectives Module） | 声明目标（Goals and Objectives）模块由目标本体构成，及版本信息。 |
| `FND/Law/MetadataFNDLaw.rdf` | FND 法律模块元数据（Metadata for the FND Law Module） | 声明法律（Law）模块由法律核心本体与法律能力本体构成，及版本信息。 |
| `FND/Organizations/MetadataFNDOrganizations.rdf` | FND 组织模块元数据（Metadata for the FND Organizations Module） | 声明组织（Organizations）模块由正式组织本体构成，及版本信息。 |
| `FND/OwnershipAndControl/MetadataFNDOwnershipAndControl.rdf` | FND 所有权与控制模块元数据（Metadata for the FND Ownership and Control Module） | 声明所有权与控制（Ownership and Control）模块由所有权、控制、所有权与控制三个本体构成，及版本信息。 |
| `FND/Parties/MetadataFNDParties.rdf` | FND 参与方模块元数据（Metadata for the FND Parties Module） | 声明参与方（Parties）模块由参与方本体构成，及版本信息。 |
| `FND/Places/MetadataFNDPlaces.rdf` | FND 地点模块元数据（Metadata for the FND Places Module） | 声明地点（Places）模块的构成：地址、虚拟地点、不动产及美国邮政地址（含个体）等本体。 |
| `FND/ProductsAndServices/MetadataFNDProductsAndServices.rdf` | FND 产品与服务模块元数据（Metadata for the FND Products and Services Module） | 声明产品与服务（Products and Services）模块由产品与服务、付款与计划表两个本体构成，及版本信息。 |
| `FND/Relations/MetadataFNDRelations.rdf` | FND 关系模块元数据（Metadata for the FND Relations Module） | 声明关系（Relations）模块由关系本体构成——这是 FIBO 最底层的基础本体，及版本信息。 |
| `FND/TransactionsExt/MetadataFNDTransactionsExt.rdf` | FND 交易扩展模块元数据（Metadata for the FND Transactions Extended Module） | 声明交易扩展（Transactions Extended）模块由 REA 交易、市场交易、证券交易三个本体构成，及版本信息。 |
| `FND/Utilities/MetadataFNDUtilities.rdf` | FND 工具模块元数据（Metadata for the FND Utilities Module） | 声明工具（Utilities）模块由分析本体与 FIBO 标注词汇表构成，及版本信息。 |

## 3. 标注依赖（owl:imports，17 个）

以下导入仅用于支撑元数据标注本身（如成熟度等级、概念映射），不属于业务内容：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `FND/Accounting/MetadataFNDAccounting.rdf` | FND 会计模块元数据（Metadata for the FND Accounting Module） | 声明会计（Accounting）模块由货币金额、现金流、ISO 4217 货币代码三个本体构成，及版本信息。 |
| `FND/AgentsAndPeople/MetadataFNDAgentsAndPeople.rdf` | FND 代理人与人员模块元数据（Metadata for the FND Agents and People Module） | 声明代理人与人员（Agents and People）模块由人员本体构成，及版本信息。 |
| `FND/Agreements/MetadataFNDAgreements.rdf` | FND 协议模块元数据（Metadata for the FND Agreements Module） | 声明协议（Agreements）模块由协议本体与合同本体构成，及版本信息。 |
| `FND/Arrangements/MetadataFNDArrangements.rdf` | FND 安排模块元数据（Metadata for the FND Arrangements Module） | 声明安排（Arrangements）模块的构成：安排、分类方案、标识符与索引、文档、生命周期、评估、评级、报告八个本体。 |
| `FND/DatesAndTimes/MetadataFNDDatesAndTimes.rdf` | FND 日期与时间模块元数据（Metadata for the FND Dates and Times Module） | 声明日期与时间（Dates and Times）模块由金融日期、营业日期、事件与发生三个本体构成，及版本信息。 |
| `FND/GoalsAndObjectives/MetadataFNDGoalsAndObjectives.rdf` | FND 目标模块元数据（Metadata for the FND Goals and Objectives Module） | 声明目标（Goals and Objectives）模块由目标本体构成，及版本信息。 |
| `FND/Law/MetadataFNDLaw.rdf` | FND 法律模块元数据（Metadata for the FND Law Module） | 声明法律（Law）模块由法律核心本体与法律能力本体构成，及版本信息。 |
| `FND/Organizations/MetadataFNDOrganizations.rdf` | FND 组织模块元数据（Metadata for the FND Organizations Module） | 声明组织（Organizations）模块由正式组织本体构成，及版本信息。 |
| `FND/OwnershipAndControl/MetadataFNDOwnershipAndControl.rdf` | FND 所有权与控制模块元数据（Metadata for the FND Ownership and Control Module） | 声明所有权与控制（Ownership and Control）模块由所有权、控制、所有权与控制三个本体构成，及版本信息。 |
| `FND/Parties/MetadataFNDParties.rdf` | FND 参与方模块元数据（Metadata for the FND Parties Module） | 声明参与方（Parties）模块由参与方本体构成，及版本信息。 |
| `FND/Places/MetadataFNDPlaces.rdf` | FND 地点模块元数据（Metadata for the FND Places Module） | 声明地点（Places）模块的构成：地址、虚拟地点、不动产及美国邮政地址（含个体）等本体。 |
| `FND/ProductsAndServices/MetadataFNDProductsAndServices.rdf` | FND 产品与服务模块元数据（Metadata for the FND Products and Services Module） | 声明产品与服务（Products and Services）模块由产品与服务、付款与计划表两个本体构成，及版本信息。 |
| `FND/Relations/MetadataFNDRelations.rdf` | FND 关系模块元数据（Metadata for the FND Relations Module） | 声明关系（Relations）模块由关系本体构成——这是 FIBO 最底层的基础本体，及版本信息。 |
| `FND/TransactionsExt/MetadataFNDTransactionsExt.rdf` | FND 交易扩展模块元数据（Metadata for the FND Transactions Extended Module） | 声明交易扩展（Transactions Extended）模块由 REA 交易、市场交易、证券交易三个本体构成，及版本信息。 |
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `FND/Utilities/MetadataFNDUtilities.rdf` | FND 工具模块元数据（Metadata for the FND Utilities Module） | 声明工具（Utilities）模块由分析本体与 FIBO 标注词汇表构成，及版本信息。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |

## 4. 文件

- 官方 RDF/XML：`MetadataFND.rdf`
- 中文 Turtle：`MetadataFND.ttl`
- 结构图：`MetadataFND-structure.png` / `MetadataFND-structure.svg`