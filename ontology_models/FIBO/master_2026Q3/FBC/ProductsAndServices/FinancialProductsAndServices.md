# 金融产品与服务本体（Financial Products and Services Ontology）结构与公理说明

本文档对应 `FinancialProductsAndServices.rdf` / `FinancialProductsAndServices.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `FinancialProductsAndServices-structure.png`（`FinancialProductsAndServices-structure.svg` 为可缩放版本）。

![金融产品与服务本体（Financial Products and Services Ontology）本体结构图](FinancialProductsAndServices-structure.png)

## 1. 本体概述

定义金融产品（financial product）与金融服务（financial service）：机构向客户提供的产品目录、条款模板与服务协议。

**在体系中的位置**：FBC 产品与服务模块的核心，连接「机构供给」与「客户需求」。

**上下游关系**：上游依赖金融服务实体与 FND 产品服务本体；下游被 LOAN 贷款产品、卡账户等具体产品本体引用。

**与相近概念的差别**：产品≠金融工具——产品是机构设计的服务组合（如「三年期定额房贷」），工具是据此签订的可交易合约；同一产品可以衍生出无数笔具体合约。

## 2. 类（Class）

| 类（Class） | 定义（Definition） |
|---|---|
| 持仓（Holding） | 持有的金融资产或头寸。 |
| 代理协议（agency agreement） | 指定一方为注册代理人、在某一（通常为法律、财务或医疗）事务中代表另一方行事的协议。 |
| 法律文书送达代理人（agent for service of process） | 由企业实体（如公司）指定、代表该企业接收法律文书的注册代理人（个人或组织）。 |
| 篮子（basket） | 可在某市场买卖的商品、服务或其他事物（如金融合约）的集合。 |
| 篮子成分（basket constituent） | 篮子的组成部分。 |
| 经纪商（broker） | 在买方与卖方之间充当中介、通常收取佣金的任何一方。 |
| 经纪交易商（broker-dealer） | 从事证券买卖业务、视交易情况同时以经纪商和交易商身份运作的任何一方。 |
| 产品目录（catalog） | 列有可供销售产品及其描述、可能还包括价格的出版物。 |
| 合同生命周期（contract lifecycle） | 协议（包括但不限于信贷协议、金融工具或其他正式合同）从初始阶段到终止的生命周期。 |
| 合同生命周期事件（contract lifecycle event） | 在协议生命周期的一个或多个阶段中发生的事件类别。 |
| 合同生命周期事件发生（contract lifecycle event occurrence） | 特定合同生命周期某一阶段中事件的实际发生。 |
| 合同生命周期历程（contract lifecycle occurrence） | 某一具体合同生命周期的实现。 |
| 合同生命周期阶段（contract lifecycle stage） | 协议生命周期中的一个阶段。 |
| 合同生命周期阶段历程（contract lifecycle stage occurrence） | 某一具体合同生命周期历程中某一阶段从开始到结束的实现。 |
| 交易商（dealer） | 购入商品或服务用于转售、并在交易中以本人身份行事的任何一方。 |
| 风险暴露（exposure） | 个人或组织失去保护、面临损害、危险、损失风险或不确定性的状态。 |
| 风险暴露承担方（exposure bearer） | 承受源自特定合同、工具或安排的影响或风险的一方。 |
| 风险暴露情形（exposure situation） | 某一方承受源自特定合同、工具或安排的影响或风险的情势。 |
| 金融风险暴露（financial exposure） | 个人或组织在交易中或就某项或某组投资面临损失风险的程度。 |
| 金融中介服务（financial intermediation service） | 由第三方（中介）将贷款人和投资者与需要资金的企业家及其他借款人撮合起来的金融服务。 |
| 金融产品（financial product） | 由银行、保险公司、经纪公司、消费金融公司等金融机构向消费者和企业提供的产品。 |
| 金融产品目录（financial product catalog） | 列有可供销售的金融产品和/或服务及其描述和其他产品详情的目录。 |
| 金融服务（financial service） | 由银行、保险公司、经纪公司、消费金融公司等金融机构向消费者和企业提供的服务。 |
| 金融服务提供商（financial service provider） | 获许可以向消费者和/或企业提供金融服务、或依法设立以提供金融服务的功能实体。 |
| 法定代理人（legal agent） | 经合法授权代表另一方行事的任何一方。 |
| 持证代理人（licensed agent） | 经许可执行具有法律约束力职能、并经合法授权代表另一方行事的任何个人。 |
| 受要约人（offeree） | 基于要约条款从某方（即要约人）处收到要约的一方。 |
| 发行（offering） | 将证券提供发行的流程步骤，即通过承销使新证券发行可得。 |
| 要约人（offeror） | 基于要约条款提议向某方（即受要约人）提供某物的一方。 |
| 头寸（position） | 因持有、借入、卖空或订立合约（如衍生品）而产生的金融风险暴露。 |
| 产品生命周期（product lifecycle） | 特定于某一产品或产品族的生命周期。 |
| 产品生命周期事件（product lifecycle event） | 在产品生命周期的一个或多个阶段中发生的事件类别。 |
| 产品生命周期事件发生（product lifecycle event occurrence） | 特定产品生命周期某一阶段中事件的实际发生。 |
| 产品生命周期历程（product lifecycle occurrence） | 某一具体产品生命周期的实现。 |
| 产品生命周期阶段（product lifecycle stage） | 产品生命周期中的一个阶段。 |
| 产品生命周期阶段历程（product lifecycle stage occurrence） | 某一给定产品生命周期中特定阶段的实现。 |
| 注册代理人（registered agent） | 由某方依据正式代理协议指定、代表其行事的法定代理人。 |
| 受监管商品（regulated commodity） | 处于监管机构（如美国商品期货交易委员会 CFTC）管辖之下的商品。 |
| 结算条款（settlement terms） | 规定交易一方或多方结算承诺与机制的合同条款。 |
| 第三方代理人（third-party agent） | 经许可执行具有法律约束力职能、并经合法授权代表另一方行事的任何服务提供商。 |
| 交易（trade） | 实现参与自愿买卖商品和服务行为的各方之间协议的情势。 |
| 交易标识符（trade identifier） | 在某一情境中标识一笔交易的字符序列。 |
| 交易生命周期（trade lifecycle） | 规定交易从发起到结算之演变过程的生命周期。 |
| 交易生命周期事件（trade lifecycle event） | 在交易生命周期的一个或多个阶段中发生的事件类别。 |
| 交易生命周期事件发生（trade lifecycle event occurrence） | 特定交易生命周期某一阶段中事件的实现。 |
| 交易生命周期历程（trade lifecycle occurrence） | 某一具体交易生命周期的实现。 |
| 交易生命周期阶段（trade lifecycle stage） | 交易生命周期中的一个阶段。 |
| 交易生命周期阶段历程（trade lifecycle stage occurrence） | 某一具体交易生命周期中某一阶段的实现。 |
| 交易员（trader） | 代表客户或金融服务提供商在任何金融市场进行金融资产转让的一方。 |
| 交易策略（trading strategy） | 在证券市场进行买卖所采用的方法。 |
| 唯一交易标识符（unique transaction identifier） | 在交易相关各方或团体认为有用并达成一致时唯一标识一笔金融交易的字符序列。 |
| 加权篮子（weighted basket） | 各成分彼此之间具有相对重要性的篮子。 |
| 加权篮子成分（weighted basket constituent） | 其相对于其他篮子成分的重要性为已知的篮子组成部分。 |

### 2.1 继承关系（Inheritance）

- 代理协议（agency agreement） ⊑ 书面合同
- 法律文书送达代理人（agent for service of process） ⊑ 注册代理人（registered agent）
- 篮子（basket） ⊑ 集合
- 篮子成分（basket constituent） ⊑ 组成成分
- 经纪商（broker） ⊑ 合同第三方
- 经纪交易商（broker-dealer） ⊑ 功能实体
- 产品目录（catalog） ⊑ 出版物
- 合同生命周期（contract lifecycle） ⊑ 生命周期
- 合同生命周期事件（contract lifecycle event） ⊑ 生命周期事件
- 合同生命周期事件发生（contract lifecycle event occurrence） ⊑ 生命周期事件发生
- 合同生命周期历程（contract lifecycle occurrence） ⊑ 生命周期发生
- 合同生命周期阶段（contract lifecycle stage） ⊑ 生命周期阶段
- 合同生命周期阶段历程（contract lifecycle stage occurrence） ⊑ 生命周期阶段发生
- 交易商（dealer） ⊑ 服务提供方
- 风险暴露（exposure） ⊑ 承受者（undergoer）
- 风险暴露承担方（exposure bearer） ⊑ 行为者（actor）
- 风险暴露情形（exposure situation） ⊑ 情境（situation）
- 金融风险暴露（financial exposure） ⊑ 风险暴露（exposure）
- 金融中介服务（financial intermediation service） ⊑ 金融服务（financial service）
- 金融产品（financial product） ⊑ 产品
- 金融产品目录（financial product catalog） ⊑ 产品目录（catalog）
- 金融服务（financial service） ⊑ 服务
- 金融服务提供商（financial service provider） ⊑ 功能型企业实体
- 金融服务提供商（financial service provider） ⊑ 服务提供方
- 法定代理人（legal agent） ⊑ 智能体角色（agent role）
- 持证代理人（licensed agent） ⊑ 法定代理人（legal agent）
- 持证代理人（licensed agent） ⊑ 被许可方
- 持证代理人（licensed agent） ⊑ 责任方
- 受要约人（offeree） ⊑ 参与方角色（party role）
- 要约人（offeror） ⊑ 参与方角色（party role）
- 头寸（position） ⊑ 金融风险暴露（financial exposure）
- 产品生命周期（product lifecycle） ⊑ 生命周期
- 产品生命周期事件（product lifecycle event） ⊑ 生命周期事件
- 产品生命周期事件发生（product lifecycle event occurrence） ⊑ 生命周期事件发生
- 产品生命周期历程（product lifecycle occurrence） ⊑ 生命周期发生
- 产品生命周期阶段（product lifecycle stage） ⊑ 生命周期阶段
- 产品生命周期阶段历程（product lifecycle stage occurrence） ⊑ 生命周期阶段发生
- 注册代理人（registered agent） ⊑ 法定代理人（legal agent）
- 注册代理人（registered agent） ⊑ 合同当事方
- 受监管商品（regulated commodity） ⊑ 商品
- 结算条款（settlement terms） ⊑ 合同承诺
- 第三方代理人（third-party agent） ⊑ 法定代理人（legal agent）
- 第三方代理人（third-party agent） ⊑ 被许可方
- 第三方代理人（third-party agent） ⊑ 服务提供方
- 交易（trade） ⊑ 情境（situation）
- 交易标识符（trade identifier） ⊑ 标识符
- 交易生命周期（trade lifecycle） ⊑ 生命周期
- 交易生命周期事件（trade lifecycle event） ⊑ 生命周期事件
- 交易生命周期事件发生（trade lifecycle event occurrence） ⊑ 生命周期事件发生
- 交易生命周期历程（trade lifecycle occurrence） ⊑ 生命周期发生
- 交易生命周期阶段（trade lifecycle stage） ⊑ 生命周期阶段
- 交易生命周期阶段历程（trade lifecycle stage occurrence） ⊑ 生命周期阶段发生
- 交易员（trader） ⊑ 服务提供方
- 交易策略（trading strategy） ⊑ 战略
- 唯一交易标识符（unique transaction identifier） ⊑ 交易标识符（trade identifier）
- 加权篮子（weighted basket） ⊑ 篮子（basket）
- 加权篮子（weighted basket） ⊑ 结构化集合
- 加权篮子成分（weighted basket constituent） ⊑ 篮子成分（basket constituent）

## 3. 对象属性（Object Property）

| 属性（Property） | 中文（English） | 定义（Definition） | 说明 |
|---|---|---|---|
| fibo-fbc-pas-fpas:exposesIn | 暴露于（exposes in） | 指明风险暴露发生的情势。 | 定义域（domain）：风险暴露（exposure）；值域（range）：风险暴露情形（exposure situation）；子属性（subPropertyOf）：承受（undergoes） |
| fibo-fbc-pas-fpas:facilitates | 促进（facilitates） | 在某一事件、任务、对话或其他事物发生的情势中充当促成者。 | 子属性（subPropertyOf）：在…中扮演主动参与方（plays active party in） |
| fibo-fbc-pas-fpas:hasExposedParty | 具有风险暴露方（has exposed party） | 指明承受影响或风险的一方。 | 定义域（domain）：风险暴露情形（exposure situation）；值域（range）：风险暴露承担方（exposure bearer）；逆属性（inverseOf）：在……中为风险暴露方（is exposed party in）；子属性（subPropertyOf）：具有行为者（has actor） |
| fibo-fbc-pas-fpas:hasExposureTo | 暴露于……的风险（has exposure to） | 涉及来自……的影响或风险。 | 定义域（domain）：风险暴露情形（exposure situation）；值域（range）：风险暴露（exposure）；逆属性（inverseOf）：暴露于（exposes in）；子属性（subPropertyOf）：具有承受者（has undergoer） |
| fibo-fbc-pas-fpas:hasGeneratingEntity | 具有生成实体（has generating entity） | 指明生成某事物的法律实体。 | 值域（range）：法律实体；子属性（subPropertyOf）：生成 |
| fibo-fbc-pas-fpas:hasGeneratingEntityIdentifier | 具有生成实体标识符（has generating entity identifier） | 指明生成唯一交易标识符的实体的标识符。 | 定义域（domain）：唯一交易标识符（unique transaction identifier） |
| fibo-fbc-pas-fpas:hasOffering | 具有要约（has offering） | 将某事物与买方或卖方（要约人）向另一方（受要约人）提交的、自愿但附条件的承诺关联起来，该承诺一经接受即具约束力。 | 值域（range）：发行（offering）；逆属性（inverseOf）：是……的要约（is offering of） |
| fibo-fbc-pas-fpas:hasOfferingAmount | 具有要约金额（has offering amount） | 指明基于参考数据、市场利率或其他约定方法确定的、与某要约相关联的名义货币金额。 | 值域（range）：货币数量；子属性（subPropertyOf）：具有名义金额 |
| fibo-fbc-pas-fpas:hasOfferingPrice | 具有要约价格（has offering price） | 指明与要约相关联的价格，可为明示价格或计算价格。 | 值域（range）：货币价格；子属性（subPropertyOf）：具有价格 |
| fibo-fbc-pas-fpas:hasLegalAgent | 具有注册代理人（has registered agent） | 标识在特定情况下具有法律、医疗或财务能力代表他人行事的一方。 | 值域（range）：法定代理人（legal agent）；子属性（subPropertyOf）：具有参与方角色（has party role） |
| fibo-fbc-pas-fpas:hasSelectingParty | 具有挑选方（has selecting party） | 指明负责确定篮子成分的个人或组织。 | 值域（range）：参与方（party）；子属性（subPropertyOf）：具有参与方（has party） |
| fibo-fbc-pas-fpas:hasSettlementDate | 具有结算日（has settlement date） | 指明已执行订单或交易必须完成结算的日期。 | 值域（range）：推算日期；子属性（subPropertyOf）：具有结束日期 |
| fibo-fbc-pas-fpas:hasTradeDate | 具有交易日（has trade date） | 指明证券或其他工具交易实际发生的日期。 | 值域（range）：日期；子属性（subPropertyOf）：具有日期 |
| fibo-fbc-pas-fpas:isEmbodiedIn | 体现于（is embodied in） | 标识某事物在某一情境中的表现形式或有形载体。 | 逆属性（inverseOf）：体现（embodies） |
| fibo-fbc-pas-fpas:isExposedPartyIn | 在……中为风险暴露方（is exposed party in） | 指明该方承担风险的情势。 | 定义域（domain）：风险暴露承担方（exposure bearer）；值域（range）：风险暴露情形（exposure situation）；子属性（subPropertyOf）：在…中行动（acts in） |
| fibo-fbc-pas-fpas:isExposedTo | 暴露于（is exposed to） | 承受来自……的影响或风险。 | 定义域（domain）：风险暴露承担方（exposure bearer）；值域（range）：风险暴露（exposure）；逆属性（inverseOf）：是……的风险暴露（is exposure of）；子属性（subPropertyOf）：对…采取行动（acts on） |
| fibo-fbc-pas-fpas:isExposureOf | 是……的风险暴露（is exposure of） | 是由……承担的影响或风险。 | 定义域（domain）：风险暴露（exposure）；值域（range）：风险暴露承担方（exposure bearer）；子属性（subPropertyOf）：受…影响（is affected by） |
| fibo-fbc-pas-fpas:isFacilitatedBy | 由……促进（is facilitated by） | 标识在某一情境中促成某一事件、交易、对话或其他事物的人或事物。 | 逆属性（inverseOf）：促进（facilitates）；子属性（subPropertyOf）：具有主动参与方（has active party） |
| fibo-fbc-pas-fpas:isOfferingOf | 是……的要约（is offering of） | 将要约与作为要约标的的一个或多个事物关联起来。 | 定义域（domain）：发行（offering） |
| fibo-fbc-pas-fpas:relatesTo | 关联于（relates to） | 与……存在逻辑或因果联系。 | — |

## 4. 数据属性（Datatype Property）

| 属性（Property） | 中文（English） | 定义（Definition） |
|---|---|---|
| fibo-fbc-pas-fpas:hasNominalNumberOfUnits | 具有名义单位数量（has nominal number of units） | 指明与某要约相关联的基础单位数量。 |
| fibo-fbc-pas-fpas:hasOfferingUnits | 具有要约单位数量（has offering units） | 指明与某要约相关联的实际单位数量，包括单位数量的任何溢价部分。 |
| fibo-fbc-pas-fpas:hasSelectionCriteria | 具有挑选标准（has selection criteria） | 描述用于确定集合成员构成的方法或程序。 |

## 5. 公理约定（Axioms）

- 代理协议（agency agreement）：具有合同当事方 some 注册代理人（registered agent）
- 篮子（basket）：具有挑选方（has selecting party） 参与方（party） ≥0
- 篮子（basket）：restriction
- 篮子（basket）：具有成员 some 篮子成分（basket constituent）
- 经纪商（broker）：restriction
- 经纪交易商（broker-dealer）：restriction
- 产品目录（catalog）：由……标识 only 标识符
- 产品目录（catalog）：描述 some 产品
- 合同生命周期（contract lifecycle）：具有阶段 some 合同生命周期阶段（contract lifecycle stage）
- 合同生命周期（contract lifecycle）：是……的生命周期 some 合同
- 合同生命周期（contract lifecycle）：定义 some 合同生命周期阶段（contract lifecycle stage）
- 合同生命周期事件（contract lifecycle event）：后于 合同生命周期事件（contract lifecycle event） ≥0
- 合同生命周期事件（contract lifecycle event）：分类 合同生命周期事件发生（contract lifecycle event occurrence） ≥0
- 合同生命周期事件（contract lifecycle event）：适用于 some 合同生命周期阶段（contract lifecycle stage）
- 合同生命周期事件发生（contract lifecycle event occurrence）：例证 合同生命周期事件（contract lifecycle event） =1
- 合同生命周期事件发生（contract lifecycle event occurrence）：由……分类 some 合同生命周期事件（contract lifecycle event）
- 合同生命周期事件发生（contract lifecycle event occurrence）：适用于 some 合同生命周期阶段历程（contract lifecycle stage occurrence）
- 合同生命周期历程（contract lifecycle occurrence）：例证 合同生命周期（contract lifecycle） =1
- 合同生命周期历程（contract lifecycle occurrence）：具有阶段 some 合同生命周期阶段历程（contract lifecycle stage occurrence）
- 合同生命周期阶段（contract lifecycle stage）：后于 合同生命周期阶段（contract lifecycle stage） ≥0
- 合同生命周期阶段（contract lifecycle stage）：是……的阶段 some 合同生命周期（contract lifecycle）
- 合同生命周期阶段（contract lifecycle stage）：分类 some 合同
- 合同生命周期阶段（contract lifecycle stage）：包含 some 合同生命周期事件（contract lifecycle event）
- 合同生命周期阶段（contract lifecycle stage）：定义于 some 合同生命周期（contract lifecycle）
- 合同生命周期阶段历程（contract lifecycle stage occurrence）：例证 合同生命周期阶段（contract lifecycle stage） =1
- 合同生命周期阶段历程（contract lifecycle stage occurrence）：是……的阶段 some 合同生命周期历程（contract lifecycle occurrence）
- 合同生命周期阶段历程（contract lifecycle stage occurrence）：包含 some 合同生命周期事件发生（contract lifecycle event occurrence）
- 交易商（dealer）：restriction
- 风险暴露承担方（exposure bearer）：在……中为风险暴露方（is exposed party in） some 风险暴露情形（exposure situation）
- 风险暴露承担方（exposure bearer）：暴露于（is exposed to） some 风险暴露（exposure）
- 风险暴露情形（exposure situation）：具有风险暴露方（has exposed party） some 风险暴露承担方（exposure bearer）
- 风险暴露情形（exposure situation）：暴露于……的风险（has exposure to） some 风险暴露（exposure）
- 金融产品（financial product）：由……提供 some 金融服务提供商（financial service provider）
- 金融产品目录（financial product catalog）：描述 some 金融产品（financial product）
- 金融服务（financial service）：由……提供 some 金融服务提供商（financial service provider）
- 金融服务提供商（financial service provider）：由…扮演（is played by） 法律实体 =1
- 金融服务提供商（financial service provider）：提供 some 金融服务（financial service）
- 法定代理人（legal agent）：由…扮演（is played by） some（具有能力方 some 受托法律权限）
- 受要约人（offeree）：由…扮演（is played by） some（是…的参与方（is a party to） some 发行（offering））
- 发行（offering）：具有参与方角色（has party role） 受要约人（offeree） ≥0
- 发行（offering）：由……发行 some 要约人（offeror）
- 发行（offering）：适用于 some owl:Thing
- 发行（offering）：具有参与方角色（has party role） some 要约人（offeror）
- 要约人（offeror）：发行 some 发行（offering）
- 要约人（offeror）：由…扮演（is played by） some（是…的参与方（is a party to） some 发行（offering））
- 产品生命周期（product lifecycle）：具有阶段 some 产品生命周期阶段（product lifecycle stage）
- 产品生命周期（product lifecycle）：是……的生命周期 some 产品
- 产品生命周期（product lifecycle）：定义 some 产品生命周期阶段（product lifecycle stage）
- 产品生命周期事件（product lifecycle event）：后于 产品生命周期事件（product lifecycle event） ≥0
- 产品生命周期事件（product lifecycle event）：分类 产品生命周期事件发生（product lifecycle event occurrence） ≥0
- 产品生命周期事件（product lifecycle event）：适用于 some 产品生命周期阶段（product lifecycle stage）
- 产品生命周期事件发生（product lifecycle event occurrence）：例证 产品生命周期事件（product lifecycle event） =1
- 产品生命周期事件发生（product lifecycle event occurrence）：适用于 some 产品生命周期阶段历程（product lifecycle stage occurrence）
- 产品生命周期历程（product lifecycle occurrence）：例证 产品生命周期（product lifecycle） =1
- 产品生命周期历程（product lifecycle occurrence）：具有阶段 some 产品生命周期阶段历程（product lifecycle stage occurrence）
- 产品生命周期阶段（product lifecycle stage）：后于 产品生命周期阶段（product lifecycle stage） ≥0
- 产品生命周期阶段（product lifecycle stage）：是……的阶段 some 产品生命周期（product lifecycle）
- 产品生命周期阶段（product lifecycle stage）：分类 some 产品
- 产品生命周期阶段（product lifecycle stage）：包含 some 产品生命周期事件（product lifecycle event）
- 产品生命周期阶段（product lifecycle stage）：定义于 some 产品生命周期（product lifecycle）
- 产品生命周期阶段历程（product lifecycle stage occurrence）：例证 产品生命周期阶段（product lifecycle stage） =1
- 产品生命周期阶段历程（product lifecycle stage occurrence）：是……的阶段 some 产品生命周期历程（product lifecycle occurrence）
- 产品生命周期阶段历程（product lifecycle stage occurrence）：包含 some 产品生命周期事件发生（product lifecycle event occurrence）
- 注册代理人（registered agent）：由…扮演（is played by） some（restriction）
- 受监管商品（regulated commodity）：受……监管 only 监管机构
- 受监管商品（regulated commodity）：受……管辖 some 管辖权
- 结算条款（settlement terms）：具有结算日（has settlement date） only 日期
- 交易（trade）：后于 交易（trade） ≥0
- 交易（trade）：由……标识 交易标识符（trade identifier） ≥0
- 交易（trade）：以……为特征 交易生命周期（trade lifecycle） ≥0
- 交易（trade）：由……促进（is facilitated by） 交易员（trader） ≥0
- 交易（trade）：体现于（is embodied in） some 合同
- 交易（trade）：具有买方 some 买方
- 交易（trade）：具有卖方 some 卖方
- 交易（trade）：涉及 some（restriction）
- 交易标识符（trade identifier）：标识 some 交易（trade）
- 交易生命周期（trade lifecycle）：具有阶段 some 交易生命周期阶段（trade lifecycle stage）
- 交易生命周期（trade lifecycle）：是……的生命周期 some 交易（trade）
- 交易生命周期（trade lifecycle）：定义 some 交易生命周期阶段（trade lifecycle stage）
- 交易生命周期事件（trade lifecycle event）：后于 交易生命周期事件（trade lifecycle event） ≥0
- 交易生命周期事件（trade lifecycle event）：分类 交易生命周期事件发生（trade lifecycle event occurrence） ≥0
- 交易生命周期事件（trade lifecycle event）：适用于 some 交易生命周期阶段（trade lifecycle stage）
- 交易生命周期事件发生（trade lifecycle event occurrence）：后于 交易生命周期事件发生（trade lifecycle event occurrence） ≥0
- 交易生命周期事件发生（trade lifecycle event occurrence）：例证 交易生命周期事件（trade lifecycle event） =1
- 交易生命周期事件发生（trade lifecycle event occurrence）：适用于 some 交易生命周期阶段历程（trade lifecycle stage occurrence）
- 交易生命周期历程（trade lifecycle occurrence）：例证 交易生命周期（trade lifecycle） =1
- 交易生命周期历程（trade lifecycle occurrence）：具有阶段 some 交易生命周期阶段历程（trade lifecycle stage occurrence）
- 交易生命周期阶段（trade lifecycle stage）：后于 交易生命周期阶段（trade lifecycle stage） ≥0
- 交易生命周期阶段（trade lifecycle stage）：是……的阶段 some 交易生命周期（trade lifecycle）
- 交易生命周期阶段（trade lifecycle stage）：分类 some 交易（trade）
- 交易生命周期阶段（trade lifecycle stage）：包含 some 交易生命周期事件（trade lifecycle event）
- 交易生命周期阶段（trade lifecycle stage）：定义于 some 交易生命周期（trade lifecycle）
- 交易生命周期阶段历程（trade lifecycle stage occurrence）：后于 交易生命周期阶段历程（trade lifecycle stage occurrence） ≥0
- 交易生命周期阶段历程（trade lifecycle stage occurrence）：例证 交易生命周期阶段（trade lifecycle stage） =1
- 交易生命周期阶段历程（trade lifecycle stage occurrence）：是……的阶段 some 交易生命周期历程（trade lifecycle occurrence）
- 交易生命周期阶段历程（trade lifecycle stage occurrence）：包含 some 交易生命周期事件发生（trade lifecycle event occurrence）
- 交易员（trader）：促进（facilitates） some 交易（trade）
- 交易员（trader）：由…扮演（is played by） some（具有能力方 some 缔约能力）
- 唯一交易标识符（unique transaction identifier）：具有生成实体（has generating entity） some 法律实体
- 加权篮子（weighted basket）：具有成员 some 加权篮子成分（weighted basket constituent）
- 加权篮子（weighted basket）：具有表达式 some 加权函数
- 加权篮子成分（weighted basket constituent）：restriction

## 6. 依赖（owl:imports，29 个）

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

## 7. 文件

- 官方 RDF/XML：`FinancialProductsAndServices.rdf`
- 中文 Turtle：`FinancialProductsAndServices.ttl`
- 结构图：`FinancialProductsAndServices-structure.png` / `FinancialProductsAndServices-structure.svg`