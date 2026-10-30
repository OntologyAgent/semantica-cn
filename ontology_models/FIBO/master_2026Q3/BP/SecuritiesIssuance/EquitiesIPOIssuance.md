# 股票首次公开发行本体（Equities IPO Issuance Ontology）结构与公理说明

本文档对应 `EquitiesIPOIssuance.rdf` / `EquitiesIPOIssuance.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `EquitiesIPOIssuance-structure.png`（`EquitiesIPOIssuance-structure.svg` 为可缩放版本）。

![股票首次公开发行本体（Equities IPO Issuance Ontology）本体结构图](EquitiesIPOIssuance-structure.png)

## 1. 本体概述

定义首次公开发行（IPO）的流程：改制辅导、监管审核、路演询价、定价配售与上市。

**在体系中的位置**：BP 证券发行模块的品种特化本体之一。

**上下游关系**：上游继承发行流程本体；下游关联 SEC/Equities 股权工具与 SEC 证券上市本体。

**与相近概念的差别**：IPO 特指「首次」公开募股，区别于增发（secondary offering）；与债务发行的差别——IPO 涉及股权估值、路演询价，且结果直接关联交易所上市。

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

### 2.1 继承关系（Inheritance）

- 商定分配依据（agree basis for allocation） ⊑ 首次公开发行流程步骤（initial public offering process step）
- 分配（allocation） ⊑ 首次公开发行流程步骤（initial public offering process step）
- 分配依据细节（allocation basis details） ⊑ 文件
- 分配细节（allocation details） ⊑ 文件
- 公告股票发行（announce equity issue） ⊑ 首次公开发行流程步骤（initial public offering process step）
- 认购申请（application for shares） ⊑ 文件
- 任命顾问（appoint advisors） ⊑ 首次公开发行流程步骤（initial public offering process step）
- 批准上市（approve for flotation） ⊑ 首次公开发行流程步骤（initial public offering process step）
- 公司经纪人（corporate broker） ⊑ 经纪商
- 股票发行公告（equity announcement） ⊑ 通知
- 申报细节（filing details） ⊑ 文件
- 正式上市交易批准（formal approval for listing and trading） ⊑ 首次公开发行流程步骤（initial public offering process step）
- IPO 完整招募说明书（i p o full prospectus） ⊑ 最终招募说明书
- IPO 初步招募说明书（i p o preliminary prospectus） ⊑ 初步招募说明书
- IPO 结算细节（i p o settlement details） ⊑ 文件
- 兴趣表示（indication of interest） ⊑ 文件
- 首次公开发行流程步骤（initial public offering process step） ⊑ 发生类别
- 股票发行营销（marketing of share issue） ⊑ 首次公开发行流程步骤（initial public offering process step）
- 分配通知（notice of allocation） ⊑ 首次公开发行流程步骤（initial public offering process step）
- 潜在股票承销商（potential share underwriter） ⊑ 潜在承销商
- 发布初步招募说明书（publish initial prospectus） ⊑ 首次公开发行流程步骤（initial public offering process step）
- 购买价格（purchase price） ⊑ 货币价格
- 购入未分配股票（purchase unallocated stock） ⊑ 首次公开发行流程步骤（initial public offering process step）
- 接收申请（receive applications） ⊑ 首次公开发行流程步骤（initial public offering process step）
- 向监管机构注册（register with regulatory authority） ⊑ 首次公开发行流程步骤（initial public offering process step）
- 注册说明书文件（registration statement document） ⊑ 文件
- 申报会计师（reporting accountant） ⊑ 参与方角色（party role）
- 定价（set price） ⊑ 首次公开发行流程步骤（initial public offering process step）
- 已分配股票的结算（settlement of allocated shares） ⊑ 首次公开发行流程步骤（initial public offering process step）
- 股东名册（share register） ⊑ 注册簿
- 保荐人（sponsor） ⊑ 参与方角色（party role）
- 辛迪加成员（syndicate member） ⊑ 参与方角色（party role）

## 3. 对象属性（Object Property）

| 属性（Property） | 中文（English） | 定义（Definition） | 说明 |
|---|---|---|---|
| fibo-bp-iss-ipo:lead | 牵头（lead） | 担任牵头角色。 | 定义域（domain）：任命顾问（appoint advisors）；值域（range）：保荐人（sponsor） |
| fibo-bp-iss-ipo:mayBe | 可能是（may be） | 标识一种可能性。 | 定义域（domain）：保荐人（sponsor）；值域（range）：公司经纪人（corporate broker） |
| fibo-bp-iss-ipo:shareUnderwriter | 股票承销商（share underwriter） | 承销股票发行的参与方。 | 定义域（domain）：承销（underwriting）；值域（range）：潜在股票承销商（potential share underwriter） |
| fibo-bp-iss-ipo:syndicateMember | 辛迪加成员（syndicate member） | 作为联盟成员、为大型交易汇集资源并分担风险的个人或组织所扮演的角色。 | 定义域（domain）：承销（underwriting）；值域（range）：辛迪加成员（syndicate member） |

## 5. 公理约定（Axioms）

- 任命顾问（appoint advisors）：指定 some（restriction）
- 任命顾问（appoint advisors）：扮演角色（plays role） some 发行人
- 批准上市（approve for flotation）：由……提供 some 交易所
- 正式上市交易批准（formal approval for listing and trading）：由……提供 some 交易所
- IPO 初步招募说明书（i p o preliminary prospectus）：先于 some IPO 完整招募说明书（i p o full prospectus）
- IPO 流程（i p o process）：具有日期区间 some 日期区间
- 首次公开发行流程步骤（initial public offering process step）：适用于 some IPO 流程（i p o process）
- 向监管机构注册（register with regulatory authority）：由……提供 some 交易所
- 保荐人（sponsor）：可能是（may be） some 公司经纪人（corporate broker）
- 承销（underwriting）：股票承销商（share underwriter） some 潜在股票承销商（potential share underwriter）
- 承销（underwriting）：辛迪加成员（syndicate member） some 辛迪加成员（syndicate member）

## 6. 依赖（owl:imports，17 个）

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

## 7. 文件

- 官方 RDF/XML：`EquitiesIPOIssuance.rdf`
- 中文 Turtle：`EquitiesIPOIssuance.ttl`
- 结构图：`EquitiesIPOIssuance-structure.png` / `EquitiesIPOIssuance-structure.svg`