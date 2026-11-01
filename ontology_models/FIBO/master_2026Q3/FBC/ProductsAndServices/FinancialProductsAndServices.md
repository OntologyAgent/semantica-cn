# 金融产品与服务本体（Financial Products and Services Ontology）结构与公理说明

本文档对应 `FinancialProductsAndServices.rdf` / `FinancialProductsAndServices.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `FinancialProductsAndServices-structure.png`（`FinancialProductsAndServices-structure.svg` 为可缩放版本）。

![金融产品与服务本体（Financial Products and Services Ontology）本体结构图](FinancialProductsAndServices-structure.png)

## 1. 本体概述

定义金融产品（financial product）与金融服务（financial service）：机构向客户提供的产品目录、条款模板与服务协议。

**在体系中的位置**：FBC 产品与服务模块的核心，连接「机构供给」与「客户需求」。

**上下游关系**：上游依赖金融服务实体与 FND 产品服务本体；下游被 LOAN 贷款产品、卡账户等具体产品本体引用。

**与相近概念的差别**：产品≠金融工具——产品是机构设计的服务组合（如「三年期定额房贷」），工具是据此签订的可交易合约；同一产品可以衍生出无数笔具体合约。

本本体中类与类的核心关系如下（完整细节见各类小节）：

- **代理协议（agency agreement）** 继承 **书面合同（WrittenContract）**
- **法律文书送达代理人（agent for service of process）** 继承 **注册代理人（registered agent）**
- **篮子（basket）** 继承 **集合（Collection）**
- **篮子成分（basket constituent）** 继承 **组成成分（Constituent）**
- **经纪商（broker）** 继承 **合同第三方（ContractThirdParty）**
- **经纪交易商（broker-dealer）** 继承 **功能实体（FunctionalEntity）**
- **产品目录（catalog）** 继承 **出版物（Publication）**
- **合同生命周期（contract lifecycle）** 继承 **生命周期（Lifecycle）**
- **合同生命周期事件（contract lifecycle event）** 继承 **生命周期事件（LifecycleEvent）**
- **合同生命周期事件发生（contract lifecycle event occurrence）** 继承 **生命周期事件发生（LifecycleEventOccurrence）**
- **合同生命周期历程（contract lifecycle occurrence）** 继承 **生命周期发生（LifecycleOccurrence）**
- **合同生命周期阶段（contract lifecycle stage）** 继承 **生命周期阶段（LifecycleStage）**
- 其余 52 条关系从略。

## 2. 类（Class）

| 类（Class） | 定义（Definition） |
|---|---|
| 持仓（Holding） | 持有的金融资产或头寸。 |
| 代理协议（agency agreement） | 指定一方为注册代理人、在某一（通常为法律、财务或医疗）事务中代表另一方行事的协议。<br>agreement that designates a party as a registered agent to represent and act on behalf of another party in some, typically legal, financial, or medical capacity |
| 法律文书送达代理人（agent for service of process） | 由企业实体（如公司）指定、代表该企业接收法律文书的注册代理人（个人或组织）。<br>registered agent (person or organization) designated by a business entity, such as a corporation, to receive legal correspondence on behalf of the business entity in the jurisdiction in which the agent's address is located |
| 篮子（basket） | 可在某市场买卖的商品、服务或其他事物（如金融合约）的集合。<br>collection of goods, services, or other things (e.g., financial contracts) that can be purchased and sold in some marketplace |
| 篮子成分（basket constituent） | 篮子的组成部分。<br>component of a basket |
| 经纪商（broker） | 在买方与卖方之间充当中介、通常收取佣金的任何一方。<br>any party that acts as an intermediary between a buyer and a seller, usually charging a commission |
| 经纪交易商（broker-dealer） | 从事证券买卖业务、视交易情况同时以经纪商和交易商身份运作的任何一方。<br>any party in the business of buying and selling securities, operating as both a broker and a dealer, depending on the transaction |
| 产品目录（catalog） | 列有可供销售产品及其描述、可能还包括价格的出版物。<br>publication including a list of products available for sale with their descriptions and possibly prices |
| 合同生命周期（contract lifecycle） | 协议（包括但不限于信贷协议、金融工具或其他正式合同）从初始阶段到终止的生命周期。<br>lifecycle of an agreement, including, but not limited to a credit agreement, financial instrument, or other formal contract, from initial stages through retirement |
| 合同生命周期事件（contract lifecycle event） | 在协议生命周期的一个或多个阶段中发生的事件类别。<br>kind of event that occurs during one or more stages of the lifecycle of an agreement |
| 合同生命周期事件发生（contract lifecycle event occurrence） | 特定合同生命周期某一阶段中事件的实际发生。<br>actual occurrence of an event during a specific stage of a specific contract lifecycle |
| 合同生命周期历程（contract lifecycle occurrence） | 某一具体合同生命周期的实现。<br>realization of the lifecycle of a specific contract |
| 合同生命周期阶段（contract lifecycle stage） | 协议生命周期中的一个阶段。<br>phase in the lifecycle of an agreement |
| 合同生命周期阶段历程（contract lifecycle stage occurrence） | 某一具体合同生命周期历程中某一阶段从开始到结束的实现。<br>realization, from start to finish of a phase in an occurrence of a specific contract lifecycle |
| 交易商（dealer） | 购入商品或服务用于转售、并在交易中以本人身份行事的任何一方。<br>any party that purchases goods or services for resale and acts on their own behalf in a transaction |
| 风险暴露（exposure） | 个人或组织失去保护、面临损害、危险、损失风险或不确定性的状态。<br>means by which an individual or organization is unprotected and open to damage, danger, risk of suffering a loss, or uncertainty |
| 风险暴露承担方（exposure bearer） | 承受源自特定合同、工具或安排的影响或风险的一方。<br>party subject to influence or risk arising from a specific contract, instrument, or arrangement |
| 风险暴露情形（exposure situation） | 某一方承受源自特定合同、工具或安排的影响或风险的情势。<br>state of affairs in which some party is subject to influence or risk arising from a specific contract, instrument, or arrangement |
| 金融风险暴露（financial exposure） | 个人或组织在交易中或就某项或某组投资面临损失风险的程度。<br>the extent to which an individual or organization is open to risk of suffering a loss in a transaction, or with respect to some investment or set of investments, e.g., some holding; the amount one stands to lose in that transaction or investment |
| 金融中介服务（financial intermediation service） | 由第三方（中介）将贷款人和投资者与需要资金的企业家及其他借款人撮合起来的金融服务。<br>any financial service in which a third party (the intermediary) matches lenders and investors with entrepreneurs and other borrowers in need of capital |
| 金融产品（financial product） | 由银行、保险公司、经纪公司、消费金融公司等金融机构向消费者和企业提供的产品。<br>product provided to consumers and businesses by financial institutions such as banks, insurance companies, brokerage firms, consumer finance companies, and investment companies |
| 金融产品目录（financial product catalog） | 列有可供销售的金融产品和/或服务及其描述和其他产品详情的目录。<br>catalog of financial products and/or services available for sale with their description and other product details |
| 金融服务（financial service） | 由银行、保险公司、经纪公司、消费金融公司等金融机构向消费者和企业提供的服务。<br>service provided to consumers and businesses by financial institutions such as banks, insurance companies, brokerage firms, consumer finance companies, and investment companies |
| 金融服务提供商（financial service provider） | 获许可以向消费者和/或企业提供金融服务、或依法设立以提供金融服务的功能实体。<br>functional entity either licensed to provide financial services to consumers and/or businesses or established by law to provide financial services, such as a central bank |
| 法定代理人（legal agent） | 经合法授权代表另一方行事的任何一方。<br>any party that has been legally empowered to act on behalf of another party |
| 持证代理人（licensed agent） | 经许可执行具有法律约束力职能、并经合法授权代表另一方行事的任何个人。<br>any individual who is licensed to perform a legally binding function, and who has been legally empowered to act on behalf of another party |
| 受要约人（offeree） | 基于要约条款从某方（即要约人）处收到要约的一方。<br>party that receives an offer from something from someone (i.e., an offerer) based on the terms of the offering |
| 发行（offering） | 将证券提供发行的流程步骤，即通过承销使新证券发行可得。<br>expression of interest in providing something to someone that is contingent upon acceptance, forbearance, or some other consideration, as might be desired by an offeree(s) |
| 要约人（offeror） | 基于要约条款提议向某方（即受要约人）提供某物的一方。<br>party that proposes to make something available to someone (i.e., an offeree) based on the terms of the offering |
| 头寸（position） | 因持有、借入、卖空或订立合约（如衍生品）而产生的金融风险暴露。<br>financial exposure resulting from owning, borrowing, shorting, or entering into a contract (e.g., derivatives) |
| 产品生命周期（product lifecycle） | 特定于某一产品或产品族的生命周期。<br>lifecycle specific to a product or product family |
| 产品生命周期事件（product lifecycle event） | 在产品生命周期的一个或多个阶段中发生的事件类别。<br>kind of event that occurs during one or more stages of a product lifecycle |
| 产品生命周期事件发生（product lifecycle event occurrence） | 特定产品生命周期某一阶段中事件的实际发生。<br>actual occurrence of an event that happens during a specific stage of a specific product lifecycle |
| 产品生命周期历程（product lifecycle occurrence） | 某一具体产品生命周期的实现。<br>realization of the lifecycle of a specific product |
| 产品生命周期阶段（product lifecycle stage） | 产品生命周期中的一个阶段。<br>phase in a product lifecycle |
| 产品生命周期阶段历程（product lifecycle stage occurrence） | 某一给定产品生命周期中特定阶段的实现。<br>realization of a specific stage in the lifecycle of a given product |
| 注册代理人（registered agent） | 由某方依据正式代理协议指定、代表其行事的法定代理人。<br>legal agent designated by some party to represent them and act on their behalf under a formal agency agreement |
| 受监管商品（regulated commodity） | 处于监管机构（如美国商品期货交易委员会 CFTC）管辖之下的商品。<br>commodity under the jurisdiction of the regulatory agency, such as the Commodities Futures Trading Commission (CFTF) in the United States, which includes any commodity traded in an organized contracts market |
| 结算条款（settlement terms） | 规定交易一方或多方结算承诺与机制的合同条款。<br>contract terms that define the commitment to and mechanism for settling one or more sides of a transaction |
| 第三方代理人（third-party agent） | 经许可执行具有法律约束力职能、并经合法授权代表另一方行事的任何服务提供商。<br>any service provider that is licensed to perform a legally binding function and has been legally empowered to act on behalf of another party |
| 交易（trade） | 实现参与自愿买卖商品和服务行为的各方之间协议的情势。<br>situation that realizes an agreement between parties participating in a voluntary action of buying and selling goods and services |
| 交易标识符（trade identifier） | 在某一情境中标识一笔交易的字符序列。<br>sequence of characters identifying a trade within some context |
| 交易生命周期（trade lifecycle） | 规定交易从发起到结算之演变过程的生命周期。<br>lifecycle that defines the evolution of a trade, from initiation through settlement |
| 交易生命周期事件（trade lifecycle event） | 在交易生命周期的一个或多个阶段中发生的事件类别。<br>kind of event that occurs during one or more stages of the lifecycle of a trade |
| 交易生命周期事件发生（trade lifecycle event occurrence） | 特定交易生命周期某一阶段中事件的实现。<br>realization of an event that happens during a specific stage of a specific trade lifecycle |
| 交易生命周期历程（trade lifecycle occurrence） | 某一具体交易生命周期的实现。<br>realization of the lifecycle for a specific trade |
| 交易生命周期阶段（trade lifecycle stage） | 交易生命周期中的一个阶段。<br>phase in the lifecycle of a trade |
| 交易生命周期阶段历程（trade lifecycle stage occurrence） | 某一具体交易生命周期中某一阶段的实现。<br>realization of a phase in the lifecycle of a specific trade |
| 交易员（trader） | 代表客户或金融服务提供商在任何金融市场进行金融资产转让的一方。<br>party that engages in the transfer of financial assets in any financial market on behalf of a client or the financial services provider |
| 交易策略（trading strategy） | 在证券市场进行买卖所采用的方法。<br>approach used for buying and selling in the securities markets |
| 唯一交易标识符（unique transaction identifier） | 在交易相关各方或团体认为有用并达成一致时唯一标识一笔金融交易的字符序列。<br>sequence of characters identifying a financial transaction uniquely whenever useful and agreed by the parties or community involved in the transaction |
| 加权篮子（weighted basket） | 各成分彼此之间具有相对重要性的篮子。<br>basket whose constituents have some relative importance with respect to one another |
| 加权篮子成分（weighted basket constituent） | 其相对于其他篮子成分的重要性为已知的篮子组成部分。<br>component of a basket whose relative importance with respect to other basket constituents is known |

以下按类逐个展开：每个类给出继承关系、相关属性与公理约定；子类在父类之下降一级编号。

### 2.1 持仓（Holding）

定义：持有的金融资产或头寸。

### 2.2 代理协议（agency agreement）

定义：指定一方为注册代理人、在某一（通常为法律、财务或医疗）事务中代表另一方行事的协议。

- 父类：**书面合同（WrittenContract）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有合同当事方（hasContractParty）** | — | — |

公理：

- **具有合同当事方（hasContractParty）**至少有一个取值，类型是**注册代理人（registered agent）**。

### 2.3 篮子（basket）

定义：可在某市场买卖的商品、服务或其他事物（如金融合约）的集合。

- 父类：**集合（Collection）**
- 直接子类：**加权篮子（weighted basket）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有挑选方（has selecting party）** | 指明负责确定篮子成分的个人或组织。<br>indicates the person(s) or organization(s) responsible for determining the contents of a basket | 值域：参与方（party）；子属性：具有参与方（has party） |
| **具有挑选标准（has selection criteria）** | 描述用于确定集合成员构成的方法或程序。<br>describes the methodology or program used to determine the membership of a collection | 子属性：具有文本值 |
| **具有成员（hasMember）** | — | — |

公理：

- **具有成员（hasMember）**至少有一个取值，类型是**篮子成分（basket constituent）**。
- **具有挑选方（has selecting party）**可以有 0 个或多个**参与方（party）**。
- **具有挑选标准（has selection criteria）**存在取值约束。

#### 2.3.1 加权篮子（weighted basket）

定义：各成分彼此之间具有相对重要性的篮子。

- 父类：**篮子（basket）**、**结构化集合（StructuredCollection）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有成员（hasMember）** | — | — |
| **具有表达式（hasExpression）** | — | — |

公理：

- **具有成员（hasMember）**至少有一个取值，类型是**加权篮子成分（weighted basket constituent）**。
- **具有表达式（hasExpression）**至少有一个取值，类型是**加权函数（WeightingFunction）**。

### 2.4 篮子成分（basket constituent）

定义：篮子的组成部分。

- 父类：**组成成分（Constituent）**
- 直接子类：**加权篮子成分（weighted basket constituent）**

#### 2.4.1 加权篮子成分（weighted basket constituent）

定义：其相对于其他篮子成分的重要性为已知的篮子组成部分。

- 父类：**篮子成分（basket constituent）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有权重（hasWeight）** | — | — |

公理：

- **具有权重（hasWeight）**存在取值约束。

### 2.5 经纪商（broker）

定义：在买方与卖方之间充当中介、通常收取佣金的任何一方。

- 父类：**合同第三方（ContractThirdParty）**

公理：

- 该属性存在取值约束。

### 2.6 经纪交易商（broker-dealer）

定义：从事证券买卖业务、视交易情况同时以经纪商和交易商身份运作的任何一方。

- 父类：**功能实体（FunctionalEntity）**

公理：

- 该属性存在取值约束。

### 2.7 产品目录（catalog）

定义：列有可供销售产品及其描述、可能还包括价格的出版物。

- 父类：**出版物（Publication）**
- 直接子类：**金融产品目录（financial product catalog）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **描述（describes）** | — | — |
| **由……标识（isIdentifiedBy）** | — | — |

公理：

- **描述（describes）**至少有一个取值，类型是**产品（Product）**。
- **由……标识（isIdentifiedBy）**的所有取值只能是**标识符（Identifier）**。

#### 2.7.1 金融产品目录（financial product catalog）

定义：列有可供销售的金融产品和/或服务及其描述和其他产品详情的目录。

- 父类：**产品目录（catalog）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **描述（describes）** | — | — |

公理：

- **描述（describes）**至少有一个取值，类型是**金融产品（financial product）**。

### 2.8 合同生命周期（contract lifecycle）

定义：协议（包括但不限于信贷协议、金融工具或其他正式合同）从初始阶段到终止的生命周期。

- 父类：**生命周期（Lifecycle）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有阶段（hasStage）** | — | — |
| **是……的生命周期（isLifecycleOf）** | — | — |
| **定义（defines）** | — | — |

公理：

- **具有阶段（hasStage）**至少有一个取值，类型是**合同生命周期阶段（contract lifecycle stage）**。
- **定义（defines）**至少有一个取值，类型是**合同生命周期阶段（contract lifecycle stage）**。
- **是……的生命周期（isLifecycleOf）**至少有一个取值，类型是**合同（Contract）**。

### 2.9 合同生命周期事件（contract lifecycle event）

定义：在协议生命周期的一个或多个阶段中发生的事件类别。

- 父类：**生命周期事件（LifecycleEvent）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **分类（classifies）** | — | — |
| **适用于（appliesTo）** | — | — |
| **后于（succeeds）** | — | 子属性：关联于（relates to） |

公理：

- **分类（classifies）**可以有 0 个或多个**合同生命周期事件发生（contract lifecycle event occurrence）**。
- **后于（succeeds）**可以有 0 个或多个**合同生命周期事件（contract lifecycle event）**。
- **适用于（appliesTo）**至少有一个取值，类型是**合同生命周期阶段（contract lifecycle stage）**。

### 2.10 合同生命周期事件发生（contract lifecycle event occurrence）

定义：特定合同生命周期某一阶段中事件的实际发生。

- 父类：**生命周期事件发生（LifecycleEventOccurrence）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **例证（exemplifies）** | — | — |
| **由……分类（isClassifiedBy）** | — | — |
| **适用于（appliesTo）** | — | — |

公理：

- **例证（exemplifies）**恰好有 1 个**合同生命周期事件（contract lifecycle event）**。
- **由……分类（isClassifiedBy）**至少有一个取值，类型是**合同生命周期事件（contract lifecycle event）**。
- **适用于（appliesTo）**至少有一个取值，类型是**合同生命周期阶段历程（contract lifecycle stage occurrence）**。

### 2.11 合同生命周期历程（contract lifecycle occurrence）

定义：某一具体合同生命周期的实现。

- 父类：**生命周期发生（LifecycleOccurrence）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有阶段（hasStage）** | — | — |
| **例证（exemplifies）** | — | — |

公理：

- **例证（exemplifies）**恰好有 1 个**合同生命周期（contract lifecycle）**。
- **具有阶段（hasStage）**至少有一个取值，类型是**合同生命周期阶段历程（contract lifecycle stage occurrence）**。

### 2.12 合同生命周期阶段（contract lifecycle stage）

定义：协议生命周期中的一个阶段。

- 父类：**生命周期阶段（LifecycleStage）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **是……的阶段（isStageOf）** | — | — |
| **分类（classifies）** | — | — |
| **包含（comprises）** | — | — |
| **后于（succeeds）** | — | 子属性：关联于（relates to） |
| **定义于（isDefinedIn）** | — | — |

公理：

- **分类（classifies）**至少有一个取值，类型是**合同（Contract）**。
- **包含（comprises）**至少有一个取值，类型是**合同生命周期事件（contract lifecycle event）**。
- **后于（succeeds）**可以有 0 个或多个**合同生命周期阶段（contract lifecycle stage）**。
- **定义于（isDefinedIn）**至少有一个取值，类型是**合同生命周期（contract lifecycle）**。
- **是……的阶段（isStageOf）**至少有一个取值，类型是**合同生命周期（contract lifecycle）**。

### 2.13 合同生命周期阶段历程（contract lifecycle stage occurrence）

定义：某一具体合同生命周期历程中某一阶段从开始到结束的实现。

- 父类：**生命周期阶段发生（LifecycleStageOccurrence）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **是……的阶段（isStageOf）** | — | — |
| **例证（exemplifies）** | — | — |
| **包含（comprises）** | — | — |

公理：

- **例证（exemplifies）**恰好有 1 个**合同生命周期阶段（contract lifecycle stage）**。
- **包含（comprises）**至少有一个取值，类型是**合同生命周期事件发生（contract lifecycle event occurrence）**。
- **是……的阶段（isStageOf）**至少有一个取值，类型是**合同生命周期历程（contract lifecycle occurrence）**。

### 2.14 交易商（dealer）

定义：购入商品或服务用于转售、并在交易中以本人身份行事的任何一方。

- 父类：**服务提供方（ServiceProvider）**

公理：

- 该属性存在取值约束。

### 2.15 风险暴露（exposure）

定义：个人或组织失去保护、面临损害、危险、损失风险或不确定性的状态。

- 父类：**承受者（undergoer）**
- 直接子类：**金融风险暴露（financial exposure）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **暴露于（exposes in）** | 指明风险暴露发生的情势。<br>indicates the state of affairs in which exposure occurs | 值域：风险暴露情形（exposure situation）；子属性：承受（undergoes） |
| **是……的风险暴露（is exposure of）** | 是由……承担的影响或风险。<br>is the influence or risk borne by | 值域：风险暴露承担方（exposure bearer）；子属性：受…影响（is affected by） |

#### 2.15.1 金融风险暴露（financial exposure）

定义：个人或组织在交易中或就某项或某组投资面临损失风险的程度。

- 父类：**风险暴露（exposure）**
- 直接子类：**头寸（position）**

##### 2.15.1.1 头寸（position）

定义：因持有、借入、卖空或订立合约（如衍生品）而产生的金融风险暴露。

- 父类：**金融风险暴露（financial exposure）**

### 2.16 风险暴露承担方（exposure bearer）

定义：承受源自特定合同、工具或安排的影响或风险的一方。

- 父类：**行为者（actor）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **在……中为风险暴露方（is exposed party in）** | 指明该方承担风险的情势。<br>indicates the state of affairs in which the party bears the risk | 值域：风险暴露情形（exposure situation）；子属性：在…中行动（acts in） |
| **暴露于（is exposed to）** | 承受来自……的影响或风险。<br>is subject to influence or risk from | 值域：风险暴露（exposure）；逆属性：是……的风险暴露（is exposure of）；子属性：对…采取行动（acts on） |

公理：

- **在……中为风险暴露方（is exposed party in）**至少有一个取值，类型是**风险暴露情形（exposure situation）**。
- **暴露于（is exposed to）**至少有一个取值，类型是**风险暴露（exposure）**。

### 2.17 风险暴露情形（exposure situation）

定义：某一方承受源自特定合同、工具或安排的影响或风险的情势。

- 父类：**情境（situation）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有风险暴露方（has exposed party）** | 指明承受影响或风险的一方。<br>indicates the party subject to influence or risk in | 值域：风险暴露承担方（exposure bearer）；逆属性：在……中为风险暴露方（is exposed party in）；子属性：具有行为者（has actor） |
| **暴露于……的风险（has exposure to）** | 涉及来自……的影响或风险。<br>involves influence or risk from | 值域：风险暴露（exposure）；逆属性：暴露于（exposes in）；子属性：具有承受者（has undergoer） |

公理：

- **具有风险暴露方（has exposed party）**至少有一个取值，类型是**风险暴露承担方（exposure bearer）**。
- **暴露于……的风险（has exposure to）**至少有一个取值，类型是**风险暴露（exposure）**。

### 2.18 金融产品（financial product）

定义：由银行、保险公司、经纪公司、消费金融公司等金融机构向消费者和企业提供的产品。

- 父类：**产品（Product）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由……提供（isProvidedBy）** | — | — |

公理：

- **由……提供（isProvidedBy）**至少有一个取值，类型是**金融服务提供商（financial service provider）**。

### 2.19 金融服务（financial service）

定义：由银行、保险公司、经纪公司、消费金融公司等金融机构向消费者和企业提供的服务。

- 父类：**服务（Service）**
- 直接子类：**金融中介服务（financial intermediation service）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由……提供（isProvidedBy）** | — | — |

公理：

- **由……提供（isProvidedBy）**至少有一个取值，类型是**金融服务提供商（financial service provider）**。

#### 2.19.1 金融中介服务（financial intermediation service）

定义：由第三方（中介）将贷款人和投资者与需要资金的企业家及其他借款人撮合起来的金融服务。

- 父类：**金融服务（financial service）**

### 2.20 金融服务提供商（financial service provider）

定义：获许可以向消费者和/或企业提供金融服务、或依法设立以提供金融服务的功能实体。

- 父类：**功能型企业实体（FunctionalBusinessEntity）**、**服务提供方（ServiceProvider）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **提供（provides）** | — | — |
| **由…扮演（is played by）** | — | — |

公理：

- **提供（provides）**至少有一个取值，类型是**金融服务（financial service）**。
- **由…扮演（is played by）**恰好有 1 个**法律实体（LegalEntity）**。

### 2.21 法定代理人（legal agent）

定义：经合法授权代表另一方行事的任何一方。

- 父类：**智能体角色（agent role）**
- 直接子类：**持证代理人（licensed agent）**、**注册代理人（registered agent）**、**第三方代理人（third-party agent）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由…扮演（is played by）** | — | — |

公理：

- **由…扮演（is played by）**至少有一个取值，该取值满足：**具有能力方（hasCapacity）**至少有一个取值，类型是**受托法律权限（DelegatedLegalAuthority）**。

#### 2.21.1 持证代理人（licensed agent）

定义：经许可执行具有法律约束力职能、并经合法授权代表另一方行事的任何个人。

- 父类：**法定代理人（legal agent）**、**被许可方（Licensee）**、**责任方（ResponsibleParty）**

#### 2.21.2 注册代理人（registered agent）

定义：由某方依据正式代理协议指定、代表其行事的法定代理人。

- 父类：**法定代理人（legal agent）**、**合同当事方（ContractParty）**
- 直接子类：**法律文书送达代理人（agent for service of process）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由…扮演（is played by）** | — | — |

公理：

- **由…扮演（is played by）**至少有一个取值，该取值满足：该属性存在取值约束。

##### 2.21.2.1 法律文书送达代理人（agent for service of process）

定义：由企业实体（如公司）指定、代表该企业接收法律文书的注册代理人（个人或组织）。

- 父类：**注册代理人（registered agent）**

#### 2.21.3 第三方代理人（third-party agent）

定义：经许可执行具有法律约束力职能、并经合法授权代表另一方行事的任何服务提供商。

- 父类：**法定代理人（legal agent）**、**被许可方（Licensee）**、**服务提供方（ServiceProvider）**

### 2.22 受要约人（offeree）

定义：基于要约条款从某方（即要约人）处收到要约的一方。

- 父类：**参与方角色（party role）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由…扮演（is played by）** | — | — |

公理：

- **由…扮演（is played by）**至少有一个取值，该取值满足：**是…的参与方（is a party to）**至少有一个取值，类型是**发行（offering）**。

### 2.23 发行（offering）

定义：将证券提供发行的流程步骤，即通过承销使新证券发行可得。

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **是……的要约（is offering of）** | 将要约与作为要约标的的一个或多个事物关联起来。<br>relates an offering to one or things that are the subject of the offer | — |
| **由……发行（isIssuedBy）** | — | — |
| **适用于（appliesTo）** | — | — |
| **具有参与方角色（has party role）** | — | — |

公理：

- **具有参与方角色（has party role）**可以有 0 个或多个**受要约人（offeree）**。
- **具有参与方角色（has party role）**至少有一个取值，类型是**要约人（offeror）**。
- **由……发行（isIssuedBy）**至少有一个取值，类型是**要约人（offeror）**。
- **适用于（appliesTo）**至少有一个取值，类型是**owl:Thing（Thing）**。

### 2.24 要约人（offeror）

定义：基于要约条款提议向某方（即受要约人）提供某物的一方。

- 父类：**参与方角色（party role）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **发行（issues）** | — | — |
| **由…扮演（is played by）** | — | — |

公理：

- **发行（issues）**至少有一个取值，类型是**发行（offering）**。
- **由…扮演（is played by）**至少有一个取值，该取值满足：**是…的参与方（is a party to）**至少有一个取值，类型是**发行（offering）**。

### 2.25 产品生命周期（product lifecycle）

定义：特定于某一产品或产品族的生命周期。

- 父类：**生命周期（Lifecycle）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有阶段（hasStage）** | — | — |
| **是……的生命周期（isLifecycleOf）** | — | — |
| **定义（defines）** | — | — |

公理：

- **具有阶段（hasStage）**至少有一个取值，类型是**产品生命周期阶段（product lifecycle stage）**。
- **定义（defines）**至少有一个取值，类型是**产品生命周期阶段（product lifecycle stage）**。
- **是……的生命周期（isLifecycleOf）**至少有一个取值，类型是**产品（Product）**。

### 2.26 产品生命周期事件（product lifecycle event）

定义：在产品生命周期的一个或多个阶段中发生的事件类别。

- 父类：**生命周期事件（LifecycleEvent）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **分类（classifies）** | — | — |
| **适用于（appliesTo）** | — | — |
| **后于（succeeds）** | — | 子属性：关联于（relates to） |

公理：

- **分类（classifies）**可以有 0 个或多个**产品生命周期事件发生（product lifecycle event occurrence）**。
- **后于（succeeds）**可以有 0 个或多个**产品生命周期事件（product lifecycle event）**。
- **适用于（appliesTo）**至少有一个取值，类型是**产品生命周期阶段（product lifecycle stage）**。

### 2.27 产品生命周期事件发生（product lifecycle event occurrence）

定义：特定产品生命周期某一阶段中事件的实际发生。

- 父类：**生命周期事件发生（LifecycleEventOccurrence）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **例证（exemplifies）** | — | — |
| **适用于（appliesTo）** | — | — |

公理：

- **例证（exemplifies）**恰好有 1 个**产品生命周期事件（product lifecycle event）**。
- **适用于（appliesTo）**至少有一个取值，类型是**产品生命周期阶段历程（product lifecycle stage occurrence）**。

### 2.28 产品生命周期历程（product lifecycle occurrence）

定义：某一具体产品生命周期的实现。

- 父类：**生命周期发生（LifecycleOccurrence）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有阶段（hasStage）** | — | — |
| **例证（exemplifies）** | — | — |

公理：

- **例证（exemplifies）**恰好有 1 个**产品生命周期（product lifecycle）**。
- **具有阶段（hasStage）**至少有一个取值，类型是**产品生命周期阶段历程（product lifecycle stage occurrence）**。

### 2.29 产品生命周期阶段（product lifecycle stage）

定义：产品生命周期中的一个阶段。

- 父类：**生命周期阶段（LifecycleStage）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **是……的阶段（isStageOf）** | — | — |
| **分类（classifies）** | — | — |
| **包含（comprises）** | — | — |
| **后于（succeeds）** | — | 子属性：关联于（relates to） |
| **定义于（isDefinedIn）** | — | — |

公理：

- **分类（classifies）**至少有一个取值，类型是**产品（Product）**。
- **包含（comprises）**至少有一个取值，类型是**产品生命周期事件（product lifecycle event）**。
- **后于（succeeds）**可以有 0 个或多个**产品生命周期阶段（product lifecycle stage）**。
- **定义于（isDefinedIn）**至少有一个取值，类型是**产品生命周期（product lifecycle）**。
- **是……的阶段（isStageOf）**至少有一个取值，类型是**产品生命周期（product lifecycle）**。

### 2.30 产品生命周期阶段历程（product lifecycle stage occurrence）

定义：某一给定产品生命周期中特定阶段的实现。

- 父类：**生命周期阶段发生（LifecycleStageOccurrence）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **是……的阶段（isStageOf）** | — | — |
| **例证（exemplifies）** | — | — |
| **包含（comprises）** | — | — |

公理：

- **例证（exemplifies）**恰好有 1 个**产品生命周期阶段（product lifecycle stage）**。
- **包含（comprises）**至少有一个取值，类型是**产品生命周期事件发生（product lifecycle event occurrence）**。
- **是……的阶段（isStageOf）**至少有一个取值，类型是**产品生命周期历程（product lifecycle occurrence）**。

### 2.31 受监管商品（regulated commodity）

定义：处于监管机构（如美国商品期货交易委员会 CFTC）管辖之下的商品。

- 父类：**商品（Commodity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **受……管辖（isGovernedBy）** | — | — |
| **受……监管（isRegulatedBy）** | — | — |

公理：

- **受……监管（isRegulatedBy）**的所有取值只能是**监管机构（RegulatoryAgency）**。
- **受……管辖（isGovernedBy）**至少有一个取值，类型是**管辖权（Jurisdiction）**。

### 2.32 结算条款（settlement terms）

定义：规定交易一方或多方结算承诺与机制的合同条款。

- 父类：**合同承诺（ContractualCommitment）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有结算日（has settlement date）** | 指明已执行订单或交易必须完成结算的日期。<br>indicates the date by which an executed order or transaction must be settled | 值域：推算日期；子属性：具有结束日期 |

公理：

- **具有结算日（has settlement date）**的所有取值只能是**日期（Date）**。

### 2.33 交易（trade）

定义：实现参与自愿买卖商品和服务行为的各方之间协议的情势。

- 父类：**情境（situation）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **体现于（is embodied in）** | 标识某事物在某一情境中的表现形式或有形载体。<br>identifies the representation or tangible form of something in some context | 逆属性：体现（embodies） |
| **由……促进（is facilitated by）** | 标识在某一情境中促成某一事件、交易、对话或其他事物的人或事物。<br>identifies someone or something that expedites some event, transaction, conversation or something else in some context | 逆属性：促进（facilitates）；子属性：具有主动参与方（has active party） |
| **具有买方（hasBuyer）** | — | — |
| **具有卖方（hasSeller）** | — | — |
| **涉及（involves）** | — | — |
| **以……为特征（isCharacterizedBy）** | — | — |
| **后于（succeeds）** | — | 子属性：关联于（relates to） |
| **由……标识（isIdentifiedBy）** | — | — |

公理：

- **以……为特征（isCharacterizedBy）**可以有 0 个或多个**交易生命周期（trade lifecycle）**。
- **体现于（is embodied in）**至少有一个取值，类型是**合同（Contract）**。
- **具有买方（hasBuyer）**至少有一个取值，类型是**买方（Buyer）**。
- **具有卖方（hasSeller）**至少有一个取值，类型是**卖方（Seller）**。
- **后于（succeeds）**可以有 0 个或多个**交易（trade）**。
- **涉及（involves）**至少有一个取值，该取值满足：该属性存在取值约束。
- **由……促进（is facilitated by）**可以有 0 个或多个**交易员（trader）**。
- **由……标识（isIdentifiedBy）**可以有 0 个或多个**交易标识符（trade identifier）**。

### 2.34 交易标识符（trade identifier）

定义：在某一情境中标识一笔交易的字符序列。

- 父类：**标识符（Identifier）**
- 直接子类：**唯一交易标识符（unique transaction identifier）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **标识（identifies）** | — | — |

公理：

- **标识（identifies）**至少有一个取值，类型是**交易（trade）**。

#### 2.34.1 唯一交易标识符（unique transaction identifier）

定义：在交易相关各方或团体认为有用并达成一致时唯一标识一笔金融交易的字符序列。

- 父类：**交易标识符（trade identifier）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有生成实体（has generating entity）** | 指明生成某事物的法律实体。<br>specifies a legal entity that generates something | 值域：法律实体；子属性：生成 |
| **具有生成实体标识符（has generating entity identifier）** | 指明生成唯一交易标识符的实体的标识符。<br>specifies an identifier for the entity that generated a unique transaction identifier | — |

公理：

- **具有生成实体（has generating entity）**至少有一个取值，类型是**法律实体（LegalEntity）**。

### 2.35 交易生命周期（trade lifecycle）

定义：规定交易从发起到结算之演变过程的生命周期。

- 父类：**生命周期（Lifecycle）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有阶段（hasStage）** | — | — |
| **是……的生命周期（isLifecycleOf）** | — | — |
| **定义（defines）** | — | — |

公理：

- **具有阶段（hasStage）**至少有一个取值，类型是**交易生命周期阶段（trade lifecycle stage）**。
- **定义（defines）**至少有一个取值，类型是**交易生命周期阶段（trade lifecycle stage）**。
- **是……的生命周期（isLifecycleOf）**至少有一个取值，类型是**交易（trade）**。

### 2.36 交易生命周期事件（trade lifecycle event）

定义：在交易生命周期的一个或多个阶段中发生的事件类别。

- 父类：**生命周期事件（LifecycleEvent）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **分类（classifies）** | — | — |
| **适用于（appliesTo）** | — | — |
| **后于（succeeds）** | — | 子属性：关联于（relates to） |

公理：

- **分类（classifies）**可以有 0 个或多个**交易生命周期事件发生（trade lifecycle event occurrence）**。
- **后于（succeeds）**可以有 0 个或多个**交易生命周期事件（trade lifecycle event）**。
- **适用于（appliesTo）**至少有一个取值，类型是**交易生命周期阶段（trade lifecycle stage）**。

### 2.37 交易生命周期事件发生（trade lifecycle event occurrence）

定义：特定交易生命周期某一阶段中事件的实现。

- 父类：**生命周期事件发生（LifecycleEventOccurrence）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **例证（exemplifies）** | — | — |
| **适用于（appliesTo）** | — | — |
| **后于（succeeds）** | — | 子属性：关联于（relates to） |

公理：

- **例证（exemplifies）**恰好有 1 个**交易生命周期事件（trade lifecycle event）**。
- **后于（succeeds）**可以有 0 个或多个**交易生命周期事件发生（trade lifecycle event occurrence）**。
- **适用于（appliesTo）**至少有一个取值，类型是**交易生命周期阶段历程（trade lifecycle stage occurrence）**。

### 2.38 交易生命周期历程（trade lifecycle occurrence）

定义：某一具体交易生命周期的实现。

- 父类：**生命周期发生（LifecycleOccurrence）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有阶段（hasStage）** | — | — |
| **例证（exemplifies）** | — | — |

公理：

- **例证（exemplifies）**恰好有 1 个**交易生命周期（trade lifecycle）**。
- **具有阶段（hasStage）**至少有一个取值，类型是**交易生命周期阶段历程（trade lifecycle stage occurrence）**。

### 2.39 交易生命周期阶段（trade lifecycle stage）

定义：交易生命周期中的一个阶段。

- 父类：**生命周期阶段（LifecycleStage）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **是……的阶段（isStageOf）** | — | — |
| **分类（classifies）** | — | — |
| **包含（comprises）** | — | — |
| **后于（succeeds）** | — | 子属性：关联于（relates to） |
| **定义于（isDefinedIn）** | — | — |

公理：

- **分类（classifies）**至少有一个取值，类型是**交易（trade）**。
- **包含（comprises）**至少有一个取值，类型是**交易生命周期事件（trade lifecycle event）**。
- **后于（succeeds）**可以有 0 个或多个**交易生命周期阶段（trade lifecycle stage）**。
- **定义于（isDefinedIn）**至少有一个取值，类型是**交易生命周期（trade lifecycle）**。
- **是……的阶段（isStageOf）**至少有一个取值，类型是**交易生命周期（trade lifecycle）**。

### 2.40 交易生命周期阶段历程（trade lifecycle stage occurrence）

定义：某一具体交易生命周期中某一阶段的实现。

- 父类：**生命周期阶段发生（LifecycleStageOccurrence）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **是……的阶段（isStageOf）** | — | — |
| **例证（exemplifies）** | — | — |
| **包含（comprises）** | — | — |
| **后于（succeeds）** | — | 子属性：关联于（relates to） |

公理：

- **例证（exemplifies）**恰好有 1 个**交易生命周期阶段（trade lifecycle stage）**。
- **包含（comprises）**至少有一个取值，类型是**交易生命周期事件发生（trade lifecycle event occurrence）**。
- **后于（succeeds）**可以有 0 个或多个**交易生命周期阶段历程（trade lifecycle stage occurrence）**。
- **是……的阶段（isStageOf）**至少有一个取值，类型是**交易生命周期历程（trade lifecycle occurrence）**。

### 2.41 交易员（trader）

定义：代表客户或金融服务提供商在任何金融市场进行金融资产转让的一方。

- 父类：**服务提供方（ServiceProvider）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **促进（facilitates）** | 在某一事件、任务、对话或其他事物发生的情势中充当促成者。<br>acts as an enabler in a situation in which an event, a task, a conversation or something else occurs | 子属性：在…中扮演主动参与方（plays active party in） |
| **由…扮演（is played by）** | — | — |

公理：

- **促进（facilitates）**至少有一个取值，类型是**交易（trade）**。
- **由…扮演（is played by）**至少有一个取值，该取值满足：**具有能力方（hasCapacity）**至少有一个取值，类型是**缔约能力（ContractualCapability）**。

### 2.42 交易策略（trading strategy）

定义：在证券市场进行买卖所采用的方法。

- 父类：**战略（Strategy）**

## 3. 其他属性

以下属性未绑定到本体的具体类（定义域在外部本体或未声明）：

对象属性（Object Property）：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有要约（has offering）** | 将某事物与买方或卖方（要约人）向另一方（受要约人）提交的、自愿但附条件的承诺关联起来，该承诺一经接受即具约束力。<br>relates something to a voluntary but conditional promise submitted by a buyer or seller (offeror) to another (offeree) for acceptance, and which becomes legally enforceable if accepted by the offeree | 值域：发行（offering）；逆属性：是……的要约（is offering of） |
| **具有要约金额（has offering amount）** | 指明基于参考数据、市场利率或其他约定方法确定的、与某要约相关联的名义货币金额。<br>indicates the notional monetary amount, determined based on reference data, market rates or some other agreed method associated with some offering | 值域：货币数量；子属性：具有名义金额 |
| **具有要约价格（has offering price）** | 指明与要约相关联的价格，可为明示价格或计算价格。<br>indicates the price associated with an offering, which may be an explicit or calculated price | 值域：货币价格；子属性：具有价格 |
| **具有注册代理人（has registered agent）** | 标识在特定情况下具有法律、医疗或财务能力代表他人行事的一方。<br>identifies a party as one that has the legal, medical or financial capacity to act on behalf of someone else under specific circumstances | 值域：法定代理人（legal agent）；子属性：具有参与方角色（has party role） |
| **具有交易日（has trade date）** | 指明证券或其他工具交易实际发生的日期。<br>indicates the date on which a security or other instrument-specific trade actually takes place | 值域：日期；子属性：具有日期 |
| **关联于（relates to）** | 与……存在逻辑或因果联系。<br>has a logical or causal connection with | — |

数据属性（Datatype Property）：

| 属性 | 定义 |
|---|---|
| **具有名义单位数量（has nominal number of units）** | 指明与某要约相关联的基础单位数量。<br>indicates the base number of units of something associated with some offering |
| **具有要约单位数量（has offering units）** | 指明与某要约相关联的实际单位数量，包括单位数量的任何溢价部分。<br>indicates the actual number of units of something, including any premium on the number of units, associated with some offering |

## 4. 依赖（owl:imports，29 个）

本本体通过 `owl:imports` 引入以下本体，各项的中文名称与简介如下：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `BE/FunctionalEntities/FunctionalEntities.rdf` | 功能实体本体（Functional Entities Ontology） | 定义「功能实体」：按其在商业中承担的功能（而非法律形式）刻画的实体，是出版方、登记机构等功能性主体的基础。 |
| `BE/FunctionalEntities/Publishers.rdf` | 出版方本体（Publishers Ontology） | 定义出版方及其出版物，用于标识金融信息与文档的发布来源。 |
| `BE/LegalEntities/LEIEntities.rdf` | LEI 法人实体本体（Legal Entity Identifier Entities Ontology） | 定义持有全球法人识别编码（LEI）的法人实体，对接 ISO 17442 标准的 LEI 体系。 |
| `BE/OwnershipAndControl/OwnershipParties.rdf` | 所有权方本体（Ownership Parties Ontology） | 定义所有权关系中的各方角色：所有者、受益所有人、名义持有人等。 |
| `FND/Accounting/CurrencyAmount.rdf` | 货币金额本体（Currency Amount Ontology） | 定义「金额＋币种」的货币金额（currency amount）表示，是 FIBO 中表达价格、债务金额、付款额等一切带币种数值的基础构件。 |
| `FND/Agreements/Contracts.rdf` | 合同本体（Contracts Ontology） | 在协议之上定义具有法律约束力的合同（contract）：合同当事方、合同条款、义务与权利，是金融工具与交易合同建模的基石。 |
| `FND/Arrangements/Lifecycles.rdf` | 生命周期本体（Lifecycles Ontology） | 定义生命周期、生命周期阶段与状态转移，用于描述合同、金融工具、机构从创设到终止的演化过程。 |
| `FND/DatesAndTimes/FinancialDates.rdf` | 金融日期本体（Financial Dates Ontology） | 定义金融语境下的日期与期间概念：结算日、付息日、到期日、日计数基准等。 |
| `FND/GoalsAndObjectives/Objectives.rdf` | 目标本体（Objectives Ontology） | 定义目标（objective）及其与组织、计划的关系，用于表达机构的经营目标与投资目标。 |
| `FND/Law/LegalCapacity.rdf` | 法律能力本体（Legal Capacity Ontology） | 定义法律能力、缔约能力、签章权等概念，刻画主体从事法律行为的资格。 |
| `FND/OwnershipAndControl/Ownership.rdf` | 所有权本体（Ownership Ontology） | 定义「拥有」关系：所有者、被拥有资产及所有权份额。 |
| `FND/ProductsAndServices/ProductsAndServices.rdf` | 产品与服务本体（Products and Services Ontology） | 定义产品、服务及其提供者与客户的通用关系。 |
| `FND/Relations/Relations.rdf` | 关系本体（Relations Ontology） | FIBO 最底层的基础本体，定义参考（reference）、分类（classify）等通用关系与抽象概念，全库普遍依赖。 |
| `FND/Utilities/Analytics.rdf` | 分析本体（Analytics Ontology） | 定义分析工具、度量与比率的通用概念，支撑指标与模型的表达。 |
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |
| `https://www.omg.org/spec/Commons/BusinessAuthorizations/` | OMG 通用商业授权本体（OMG Commons Business Authorizations） | OMG 通用本体库（Commons）中的商业授权本体，定义授权、签章与代理权限的通用概念。 |
| `https://www.omg.org/spec/Commons/Classifiers/` | OMG 通用分类器本体（OMG Commons Classifiers） | OMG 通用本体库（Commons）中的分类器本体，定义分类方案、类别与归类关系的通用概念，FIBO 的分类建模建立在其上。 |
| `https://www.omg.org/spec/Commons/Collections/` | OMG 通用集合本体（OMG Commons Collections） | Commons 库中的集合本体，定义集合、成员等通用概念。 |
| `https://www.omg.org/spec/Commons/ContextualDesignators/` | OMG 通用语境指称本体（OMG Commons Contextual Designators） | Commons 库中的语境指称本体，定义「在某个语境下指代某物的名称/符号」，是地址、账户号码等语境相关标识的基础。 |
| `https://www.omg.org/spec/Commons/DatesAndTimes/` | OMG 通用日期与时间本体（OMG Commons Dates and Times） | Commons 库中的日期时间本体，定义日期、期间、时间点等通用时间概念。 |
| `https://www.omg.org/spec/Commons/Designators/` | OMG 通用指称符本体（OMG Commons Designators） | Commons 库中的指称符本体，定义名称、标识符等「指代某物的符号」的通用概念。 |
| `https://www.omg.org/spec/Commons/Identifiers/` | OMG 通用标识符本体（OMG Commons Identifiers） | Commons 库中的标识符本体，定义标识符及其编码方案的通用概念。 |
| `https://www.omg.org/spec/Commons/Organizations/` | OMG 通用组织本体（OMG Commons Organizations） | Commons 库中的组织本体，定义组织、组织成员与组织结构的通用概念。 |
| `https://www.omg.org/spec/Commons/PartiesAndSituations/` | OMG 通用参与方与情境本体（OMG Commons Parties and Situations） | Commons 库中的参与方本体，定义独立主体、参与方及其角色扮演的通用概念，是 FIBO 参与方模型的上游。 |
| `https://www.omg.org/spec/Commons/QuantitiesAndUnits/` | OMG 通用量与单位本体（OMG Commons Quantities and Units） | Commons 库中的量与单位本体，定义数量、度量单位、量纲的通用概念，支撑金额、比率等数值表达。 |
| `https://www.omg.org/spec/Commons/RegulatoryAgencies/` | OMG 通用监管机构本体（OMG Commons Regulatory Agencies） | Commons 库中的监管机构本体，定义监管机构及其监管职权的通用概念。 |
| `https://www.omg.org/spec/Commons/RolesAndCompositions/` | OMG 通用角色与构成本体（OMG Commons Roles and Compositions） | Commons 库中的角色本体，定义角色及整体—部分构成关系的通用概念。 |
| `https://www.omg.org/spec/Commons/TextDatatype/` | OMG 通用文本数据类型（OMG Commons Text Datatype） | Commons 库中的文本数据类型定义，提供带语言标记的文本等基础数据类型。 |

## 5. 文件

- 官方 RDF/XML：`FinancialProductsAndServices.rdf`
- 中文 Turtle：`FinancialProductsAndServices.ttl`
- 结构图：`FinancialProductsAndServices-structure.png` / `FinancialProductsAndServices-structure.svg`