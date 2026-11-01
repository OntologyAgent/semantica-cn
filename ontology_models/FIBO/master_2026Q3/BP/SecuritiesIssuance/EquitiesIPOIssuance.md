# 股票首次公开发行本体（Equities IPO Issuance Ontology）结构与公理说明

本文档对应 `EquitiesIPOIssuance.rdf` / `EquitiesIPOIssuance.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `EquitiesIPOIssuance-structure.png`（`EquitiesIPOIssuance-structure.svg` 为可缩放版本）。

![股票首次公开发行本体（Equities IPO Issuance Ontology）本体结构图](EquitiesIPOIssuance-structure.png)

## 1. 本体概述

定义首次公开发行（IPO）的流程：改制辅导、监管审核、路演询价、定价配售与上市。

**在体系中的位置**：BP 证券发行模块的品种特化本体之一。

**上下游关系**：上游继承发行流程本体；下游关联 SEC/Equities 股权工具与 SEC 证券上市本体。

**与相近概念的差别**：IPO 特指「首次」公开募股，区别于增发（secondary offering）；与债务发行的差别——IPO 涉及股权估值、路演询价，且结果直接关联交易所上市。

本本体中类与类的核心关系如下（完整细节见各类小节）：

- **商定分配依据（agree basis for allocation）** 继承 **首次公开发行流程步骤（initial public offering process step）**
- **分配（allocation）** 继承 **首次公开发行流程步骤（initial public offering process step）**
- **分配依据细节（allocation basis details）** 继承 **文件（Document）**
- **分配细节（allocation details）** 继承 **文件（Document）**
- **公告股票发行（announce equity issue）** 继承 **首次公开发行流程步骤（initial public offering process step）**
- **认购申请（application for shares）** 继承 **文件（Document）**
- **任命顾问（appoint advisors）** 继承 **首次公开发行流程步骤（initial public offering process step）**
- **批准上市（approve for flotation）** 继承 **首次公开发行流程步骤（initial public offering process step）**
- **公司经纪人（corporate broker）** 继承 **经纪商（Broker）**
- **股票发行公告（equity announcement）** 继承 **通知（Notice）**
- **申报细节（filing details）** 继承 **文件（Document）**
- **正式上市交易批准（formal approval for listing and trading）** 继承 **首次公开发行流程步骤（initial public offering process step）**
- 其余 24 条关系从略。

## 2. 类（Class）

| 类（Class） | 定义（Definition） |
|---|---|
| 商定分配依据（agree basis for allocation） | 就股票分配的依据达成一致。 |
| 分配（allocation） | 将发行股票分配给各认购人的行为。 |
| 分配依据细节（allocation basis details） | 关于股票分配依据的详细信息。 |
| 分配细节（allocation details） | 关于股票分配结果的详细信息。 |
| 公告股票发行（announce equity issue） | 对股票发行进行公告。 |
| 认购申请（application for shares） | 投资者提交的认购股票的申请。 |
| 任命顾问（appoint advisors） | 任命发行相关顾问。 |
| 批准上市（approve for flotation） | 批准公司上市发行。 |
| 公司经纪人（corporate broker） | 为公司发行提供经纪服务的参与方。 |
| 股票发行公告（equity announcement） | 关于股票发行的公告。 |
| 申报细节（filing details） | 向监管机构申报的详细信息。 |
| 正式上市交易批准（formal approval for listing and trading） | 对证券上市与交易的正式批准。 |
| IPO 完整招募说明书（i p o full prospectus） | 首次公开发行的完整招募说明书。 |
| IPO 初步招募说明书（i p o preliminary prospectus） | 首次公开发行的初步招募说明书。 |
| IPO 流程（i p o process） | 首次公开发行的完整流程。 |
| IPO 结算细节（i p o settlement details） | 首次公开发行结算的详细信息。 |
| 兴趣表示（indication of interest） | 投资者对认购发行证券表达的兴趣。 |
| 首次公开发行流程步骤（initial public offering process step） | 首次公开发行流程中的一个步骤。 |
| 股票发行营销（marketing of share issue） | 对股票发行进行的市场营销。 |
| 分配通知（notice of allocation） | 向认购人发出的股票分配通知。 |
| 潜在股票承销商（potential share underwriter） | 可能成为股票发行承销商的参与方。 |
| 发布初步招募说明书（publish initial prospectus） | 对外发布初步招募说明书。 |
| 购买价格（purchase price） | 购买证券的价格。 |
| 购入未分配股票（purchase unallocated stock） | 承销商购入未被认购分配的股票。 |
| 接收申请（receive applications） | 接收投资者的认购申请。 |
| 向监管机构注册（register with regulatory authority） | 在监管机构办理发行注册。 |
| 注册说明书文件（registration statement document） | 向监管机构提交的注册说明书文件。 |
| 申报会计师（reporting accountant） | 为发行出具会计报告的会计师。 |
| 定价（set price） | 确定发行价格。 |
| 已分配股票的结算（settlement of allocated shares） | 对已分配股票进行结算。 |
| 股东名册（share register） | 记录股票持有人的名册。 |
| 保荐人（sponsor） | 为发行提供保荐服务的参与方。 |
| 辛迪加成员（syndicate member） | 作为联盟成员、为大型交易汇集资源并分担风险的个人或组织所扮演的角色。 |
| 承销（underwriting） | 承销商承诺购入并转售发行证券的活动。 |

以下按类逐个展开：每个类给出继承关系、相关属性与公理约定；子类在父类之下降一级编号。

### 2.1 分配依据细节（allocation basis details）

定义：关于股票分配依据的详细信息。

- 父类：**文件（Document）**

### 2.2 分配细节（allocation details）

定义：关于股票分配结果的详细信息。

- 父类：**文件（Document）**

### 2.3 认购申请（application for shares）

定义：投资者提交的认购股票的申请。

- 父类：**文件（Document）**

### 2.4 公司经纪人（corporate broker）

定义：为公司发行提供经纪服务的参与方。

- 父类：**经纪商（Broker）**

### 2.5 股票发行公告（equity announcement）

定义：关于股票发行的公告。

- 父类：**通知（Notice）**

### 2.6 申报细节（filing details）

定义：向监管机构申报的详细信息。

- 父类：**文件（Document）**

### 2.7 IPO 完整招募说明书（i p o full prospectus）

定义：首次公开发行的完整招募说明书。

- 父类：**最终招募说明书（FinalProspectus）**

### 2.8 IPO 初步招募说明书（i p o preliminary prospectus）

定义：首次公开发行的初步招募说明书。

- 父类：**初步招募说明书（PreliminaryProspectus）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **先于（precedes）** | — | — |

公理：

- **先于（precedes）**至少有一个取值，类型是**IPO 完整招募说明书（i p o full prospectus）**。

### 2.9 IPO 流程（i p o process）

定义：首次公开发行的完整流程。

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有日期区间（hasDatePeriod）** | — | — |

公理：

- **具有日期区间（hasDatePeriod）**至少有一个取值，类型是**日期区间（DatePeriod）**。

### 2.10 IPO 结算细节（i p o settlement details）

定义：首次公开发行结算的详细信息。

- 父类：**文件（Document）**

### 2.11 兴趣表示（indication of interest）

定义：投资者对认购发行证券表达的兴趣。

- 父类：**文件（Document）**

### 2.12 首次公开发行流程步骤（initial public offering process step）

定义：首次公开发行流程中的一个步骤。

- 父类：**发生类别（OccurrenceKind）**
- 直接子类：**商定分配依据（agree basis for allocation）**、**分配（allocation）**、**公告股票发行（announce equity issue）**、**任命顾问（appoint advisors）**、**批准上市（approve for flotation）**、**正式上市交易批准（formal approval for listing and trading）**、**股票发行营销（marketing of share issue）**、**分配通知（notice of allocation）**、**发布初步招募说明书（publish initial prospectus）**、**购入未分配股票（purchase unallocated stock）**、**接收申请（receive applications）**、**向监管机构注册（register with regulatory authority）**、**定价（set price）**、**已分配股票的结算（settlement of allocated shares）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **适用于（appliesTo）** | — | — |

公理：

- **适用于（appliesTo）**至少有一个取值，类型是**IPO 流程（i p o process）**。

#### 2.12.1 商定分配依据（agree basis for allocation）

定义：就股票分配的依据达成一致。

- 父类：**首次公开发行流程步骤（initial public offering process step）**

#### 2.12.2 分配（allocation）

定义：将发行股票分配给各认购人的行为。

- 父类：**首次公开发行流程步骤（initial public offering process step）**

#### 2.12.3 公告股票发行（announce equity issue）

定义：对股票发行进行公告。

- 父类：**首次公开发行流程步骤（initial public offering process step）**

#### 2.12.4 任命顾问（appoint advisors）

定义：任命发行相关顾问。

- 父类：**首次公开发行流程步骤（initial public offering process step）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **牵头（lead）** | 担任牵头角色。 | 值域：保荐人（sponsor） |
| **指定（designates）** | — | — |
| **扮演角色（plays role）** | — | — |

公理：

- **扮演角色（plays role）**至少有一个取值，类型是**发行人（Issuer）**。
- **指定（designates）**至少有一个取值，该取值满足：该属性存在取值约束。

#### 2.12.5 批准上市（approve for flotation）

定义：批准公司上市发行。

- 父类：**首次公开发行流程步骤（initial public offering process step）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由……提供（isProvidedBy）** | — | — |

公理：

- **由……提供（isProvidedBy）**至少有一个取值，类型是**交易所（Exchange）**。

#### 2.12.6 正式上市交易批准（formal approval for listing and trading）

定义：对证券上市与交易的正式批准。

- 父类：**首次公开发行流程步骤（initial public offering process step）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由……提供（isProvidedBy）** | — | — |

公理：

- **由……提供（isProvidedBy）**至少有一个取值，类型是**交易所（Exchange）**。

#### 2.12.7 股票发行营销（marketing of share issue）

定义：对股票发行进行的市场营销。

- 父类：**首次公开发行流程步骤（initial public offering process step）**

#### 2.12.8 分配通知（notice of allocation）

定义：向认购人发出的股票分配通知。

- 父类：**首次公开发行流程步骤（initial public offering process step）**

#### 2.12.9 发布初步招募说明书（publish initial prospectus）

定义：对外发布初步招募说明书。

- 父类：**首次公开发行流程步骤（initial public offering process step）**

#### 2.12.10 购入未分配股票（purchase unallocated stock）

定义：承销商购入未被认购分配的股票。

- 父类：**首次公开发行流程步骤（initial public offering process step）**

#### 2.12.11 接收申请（receive applications）

定义：接收投资者的认购申请。

- 父类：**首次公开发行流程步骤（initial public offering process step）**

#### 2.12.12 向监管机构注册（register with regulatory authority）

定义：在监管机构办理发行注册。

- 父类：**首次公开发行流程步骤（initial public offering process step）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由……提供（isProvidedBy）** | — | — |

公理：

- **由……提供（isProvidedBy）**至少有一个取值，类型是**交易所（Exchange）**。

#### 2.12.13 定价（set price）

定义：确定发行价格。

- 父类：**首次公开发行流程步骤（initial public offering process step）**

#### 2.12.14 已分配股票的结算（settlement of allocated shares）

定义：对已分配股票进行结算。

- 父类：**首次公开发行流程步骤（initial public offering process step）**

### 2.13 潜在股票承销商（potential share underwriter）

定义：可能成为股票发行承销商的参与方。

- 父类：**潜在承销商（PotentialUnderwriter）**

### 2.14 购买价格（purchase price）

定义：购买证券的价格。

- 父类：**货币价格（MonetaryPrice）**

### 2.15 注册说明书文件（registration statement document）

定义：向监管机构提交的注册说明书文件。

- 父类：**文件（Document）**

### 2.16 申报会计师（reporting accountant）

定义：为发行出具会计报告的会计师。

- 父类：**参与方角色（party role）**

### 2.17 股东名册（share register）

定义：记录股票持有人的名册。

- 父类：**注册簿（Registry）**

### 2.18 保荐人（sponsor）

定义：为发行提供保荐服务的参与方。

- 父类：**参与方角色（party role）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **可能是（may be）** | 标识一种可能性。 | 值域：公司经纪人（corporate broker） |

公理：

- **可能是（may be）**至少有一个取值，类型是**公司经纪人（corporate broker）**。

### 2.19 辛迪加成员（syndicate member）

定义：作为联盟成员、为大型交易汇集资源并分担风险的个人或组织所扮演的角色。

- 父类：**参与方角色（party role）**

### 2.20 承销（underwriting）

定义：承销商承诺购入并转售发行证券的活动。

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **股票承销商（share underwriter）** | 承销股票发行的参与方。 | 值域：潜在股票承销商（potential share underwriter） |
| **辛迪加成员（syndicate member）** | 作为联盟成员、为大型交易汇集资源并分担风险的个人或组织所扮演的角色。 | 值域：辛迪加成员（syndicate member） |

公理：

- **股票承销商（share underwriter）**至少有一个取值，类型是**潜在股票承销商（potential share underwriter）**。
- **辛迪加成员（syndicate member）**至少有一个取值，类型是**辛迪加成员（syndicate member）**。

## 3. 依赖（owl:imports，17 个）

本本体通过 `owl:imports` 引入以下本体，各项的中文名称与简介如下：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `BP/SecuritiesIssuance/IssuanceDocuments.rdf` | 发行文件本体（Issuance Documents Ontology） | 定义证券发行过程中使用的法律文件：募集说明书、条款清单等。 |
| `BP/SecuritiesIssuance/IssuanceProcess.rdf` | 发行流程本体（Issuance Process Ontology） | 定义证券发行的通用流程框架：从筹划、定价到配售的各阶段。 |
| `FBC/FinancialInstruments/FinancialInstruments.rdf` | 金融工具本体（Financial Instruments Ontology） | FIBO 核心本体之一，定义金融工具（financial instrument）的通用概念：可交易、代表某种权利义务的合同工具，是证券、衍生品等具体工具的共同基础。 |
| `FBC/FunctionalEntities/Markets.rdf` | 市场本体（Markets Ontology） | 定义金融市场（market）：交易所、场外市场及其功能。 |
| `FBC/ProductsAndServices/FinancialProductsAndServices.rdf` | 金融产品与服务本体（Financial Products and Services Ontology） | 定义金融产品（financial product）与金融服务（financial service）及其提供、购买关系。 |
| `FND/Accounting/CurrencyAmount.rdf` | 货币金额本体（Currency Amount Ontology） | 定义「金额＋币种」的货币金额（currency amount）表示，是 FIBO 中表达价格、债务金额、付款额等一切带币种数值的基础构件。 |
| `FND/DatesAndTimes/Occurrences.rdf` | 事件与发生本体（Occurrences Ontology） | 定义「发生」（occurrence）、事件与触发条件，用于表达企业行动、信用事件等「发生了什么」。 |
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `SEC/Securities/SecuritiesListings.rdf` | 证券上市本体（Securities Listings Ontology） | 定义证券在交易所上市（listing）及其上市状态。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |
| `https://www.omg.org/spec/Commons/ContextualDesignators/` | OMG 通用语境指称本体（OMG Commons Contextual Designators） | Commons 库中的语境指称本体，定义「在某个语境下指代某物的名称/符号」，是地址、账户号码等语境相关标识的基础。 |
| `https://www.omg.org/spec/Commons/DatesAndTimes/` | OMG 通用日期与时间本体（OMG Commons Dates and Times） | Commons 库中的日期时间本体，定义日期、期间、时间点等通用时间概念。 |
| `https://www.omg.org/spec/Commons/Documents/` | OMG 通用文档本体（OMG Commons Documents） | Commons 库中的文档本体，定义文档及其组成部分的通用概念。 |
| `https://www.omg.org/spec/Commons/Organizations/` | OMG 通用组织本体（OMG Commons Organizations） | Commons 库中的组织本体，定义组织、组织成员与组织结构的通用概念。 |
| `https://www.omg.org/spec/Commons/PartiesAndSituations/` | OMG 通用参与方与情境本体（OMG Commons Parties and Situations） | Commons 库中的参与方本体，定义独立主体、参与方及其角色扮演的通用概念，是 FIBO 参与方模型的上游。 |
| `https://www.omg.org/spec/Commons/RegistrationAuthorities/` | OMG 通用登记主管机构本体（OMG Commons Registration Authorities） | Commons 库中的登记主管机构本体，定义负责登记注册的主管机构及其登记行为的通用概念。 |
| `https://www.omg.org/spec/Commons/RolesAndCompositions/` | OMG 通用角色与构成本体（OMG Commons Roles and Compositions） | Commons 库中的角色本体，定义角色及整体—部分构成关系的通用概念。 |

## 4. 文件

- 官方 RDF/XML：`EquitiesIPOIssuance.rdf`
- 中文 Turtle：`EquitiesIPOIssuance.ttl`
- 结构图：`EquitiesIPOIssuance-structure.png` / `EquitiesIPOIssuance-structure.svg`