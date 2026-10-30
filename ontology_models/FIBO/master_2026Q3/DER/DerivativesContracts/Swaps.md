# 互换本体（Swaps Ontology）结构与公理说明

本文档对应 `Swaps.rdf` / `Swaps.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `Swaps-structure.png`（`Swaps-structure.svg` 为可缩放版本）。

![互换本体（Swaps Ontology）本体结构图](Swaps-structure.png)

## 1. 本体概述

定义互换（swap）合约的通用结构：两个或多个互换腿（swap leg）之间按约定公式交换现金流，含名义本金、支付日程等。

**在体系中的位置**：衍生品合约模块的四大基础结构本体之一，是利率互换、股权互换、信用违约互换的共同基础。

**上下游关系**：上游继承衍生品基础本体；下游被利率互换（DER/RateDerivatives）、股权互换（DER/SecurityBasedDerivatives）、信用违约互换（DER/CreditDerivatives）特化；互换个体本体提供标准市场约定实例。

**与相近概念的差别**：互换是「现金流交换」而非一次性买卖——这是它与期货、期权的本质差别；与债券的差别——债券交换的是本金与利息，互换通常只交换利息差额，名义本金不交割。

## 2. 类（Class）

| 类（Class） | 定义（Definition） |
|---|---|
| 基差互换（basis swap） | 支付流参考不同基准的互换。 |
| 相关性腿（correlation leg） | 相关性互换的浮动腿，支付金额基于一组标的产品价格的观察平均相关性。 |
| 相关性互换（correlation swap） | 一种场外统计衍生品，用于对冲一组标的产品价格观察平均相关性相关的风险。 |
| 离散度腿（dispersion leg） | 离散度互换的浮动腿，支付金额基于标的产品价格变动的已实现离散度。 |
| 离散度互换（dispersion swap） | 用于对冲标的资产价格变动幅度的统计衍生品。 |
| 超额回报互换（excess return swap） | 回报互换的一种：指数水平变动等于主要由各成分价格变化产生的回报。 |
| 固定腿（fixed leg） | 付款方有义务在互换期限内按固定年利率或固定金额不定期付款的互换腿。 |
| 固定支付腿（fixed payment leg） | 规定按固定年利率计算的付款计划相关合同条款的互换腿。 |
| 浮动腿（floating leg） | 付款方有义务在互换期限内按某一浮动利率不定期付款的互换腿。 |
| 指数回报互换（index return swap） | 付款基于向互换卖方支付的费用以及基于指数水平变动的浮动参考价格的回报互换。 |
| 主要互换参与者（major swap participant） | 在任何主要互换类别中持有大量头寸的金融服务提供商。 |
| 基于业绩的浮动腿（performance-based variable leg） | 支付取决于标的业绩某种统计度量的互换浮动腿。 |
| 利率类腿（rate-based leg） | 基于浮动利率、浮动通胀率或固定利率的利率类互换腿。 |
| 利率互换（rates swap） | 两个交易对手约定在协议期间的规定日期、基于指定名义本金和利率互相支付现金流的互换。 |
| 已实现浮动腿（realized variable leg） | 付款在到期时一次性净额结算（而非定期支付）的基于业绩的互换腿。 |
| 回报腿（return leg） | 支付标的所产生收益的互换腿。 |
| 回报互换（return swap） | 其中一腿（回报腿）基于某一标的所产生收益的互换。 |
| 简单回报腿（simple return leg） | 严格基于标的资产所产生收益、不含升值、减值、资本利得和任何费用的回报腿。 |
| 统计互换（statistical swap） | 支付取决于标的业绩某种统计度量的互换。 |
| 执行腿（strike leg） | 规定在执行时报出的固定金额（即「执行额」）的互换腿。 |
| 互换（swap） | 交易对手约定交换来自两种不同金融工具的周期性现金流或负债流的衍生工具。 |
| 互换确认书（swap confirmation） | 将双方整体交易中与生命周期事件相关的具体条款和条件成文化的正式确认书。 |
| 互换数据存库机构（swap data repository） | 为互换数据报告和记录保存提供集中设施的金融服务提供商。 |
| 互换交易商（swap dealer） | 经营互换、为互换做市、并在日常业务中经常与交易对手订立互换的非存款性机构。 |
| 互换腿（swap leg） | 规定互换某一组成部分的现金流要求（如利息支付、票息支付等）及履约承诺的条款。 |
| 互换腿事件（swap leg event） | 适用于互换某一腿的互换生命周期事件，如付款或利率重置事件。 |
| 互换生命周期事件（swap lifecycle event） | 互换生命周期内发生的事件，整体事件集包括发行人、前台、中台、后台各自特有的事件。 |
| 互换生命周期事件标识符（swap lifecycle event identifier） | 唯一标识互换生命周期中特定事件的标识符。 |
| 互换方（swap party） | 互换的一方，因此也是体现该交易的合约的法定当事方。 |
| 互换付款方（swap paying party） | 按合约规定为交易某一腿负责付款的互换方。 |
| 互换收款方（swap receiving party） | 按合约规定收取交易某一腿款项的互换方。 |
| 互换条款（swap terms） | 互换交易的法律合同条款。 |
| 总回报腿（total return leg） | 基于标的资产所产生收益以及任何升值、减值、资本利得和费用的回报腿。 |
| 总回报互换（total return swap） | 卖方同意向另一方支付标的资产价值变动乘以约定名义金额的回报互换。 |
| 唯一互换标识符（unique swap identifier） | 用于记录保存和互换数据报告的互换标识符。 |

### 2.1 继承关系（Inheritance）

- 基差互换（basis swap） ⊑ 利率互换（rates swap）
- 相关性腿（correlation leg） ⊑ 基于业绩的浮动腿（performance-based variable leg）
- 相关性互换（correlation swap） ⊑ 统计互换（statistical swap）
- 离散度腿（dispersion leg） ⊑ 基于业绩的浮动腿（performance-based variable leg）
- 离散度互换（dispersion swap） ⊑ 统计互换（statistical swap）
- 超额回报互换（excess return swap） ⊑ 指数回报互换（index return swap）
- 固定腿（fixed leg） ⊑ 互换腿（swap leg）
- 固定支付腿（fixed payment leg） ⊑ 互换腿（swap leg）
- 浮动腿（floating leg） ⊑ 互换腿（swap leg）
- 指数回报互换（index return swap） ⊑ 回报互换（return swap）
- 主要互换参与者（major swap participant） ⊑ 非存款性机构
- 基于业绩的浮动腿（performance-based variable leg） ⊑ 浮动腿（floating leg）
- 利率类腿（rate-based leg） ⊑ 互换腿（swap leg）
- 利率互换（rates swap） ⊑ 互换（swap）
- 已实现浮动腿（realized variable leg） ⊑ 基于业绩的浮动腿（performance-based variable leg）
- 回报腿（return leg） ⊑ 浮动腿（floating leg）
- 回报互换（return swap） ⊑ 互换（swap）
- 简单回报腿（simple return leg） ⊑ 回报腿（return leg）
- 统计互换（statistical swap） ⊑ 互换（swap）
- 执行腿（strike leg） ⊑ 固定腿（fixed leg）
- 互换（swap） ⊑ 衍生工具
- 互换确认书（swap confirmation） ⊑ 互换生命周期事件（swap lifecycle event）
- 互换确认书（swap confirmation） ⊑ 交易确认书
- 互换数据存库机构（swap data repository） ⊑ 金融服务提供商
- 互换交易商（swap dealer） ⊑ 非存款性机构
- 互换交易商（swap dealer） ⊑ 交易商
- 互换腿（swap leg） ⊑ 现金流条款
- 互换腿（swap leg） ⊑ 互换条款（swap terms）
- 互换腿事件（swap leg event） ⊑ 互换生命周期事件（swap lifecycle event）
- 互换生命周期事件（swap lifecycle event） ⊑ 生命周期事件
- 互换生命周期事件标识符（swap lifecycle event identifier） ⊑ 标识符
- 互换方（swap party） ⊑ 合同当事方
- 互换付款方（swap paying party） ⊑ 付款方
- 互换付款方（swap paying party） ⊑ 互换方（swap party）
- 互换收款方（swap receiving party） ⊑ 收款对手方
- 互换收款方（swap receiving party） ⊑ 互换方（swap party）
- 互换条款（swap terms） ⊑ 衍生品条款
- 总回报腿（total return leg） ⊑ 回报腿（return leg）
- 总回报互换（total return swap） ⊑ 信用衍生品
- 总回报互换（total return swap） ⊑ 回报互换（return swap）
- 唯一互换标识符（unique swap identifier） ⊑ 金融工具标识符

## 3. 对象属性（Object Property）

| 属性（Property） | 中文（English） | 定义（Definition） | 说明 |
|---|---|---|---|
| fibo-der-drc-swp:hasFundingLeg | 具有融资腿（has funding leg） | 指明回报互换中规定固定支付率（通常基于基准、也可能为固定利率）的一腿。 | 定义域（domain）：回报互换（return swap）；子属性（subPropertyOf）：具有腿（has leg） |
| fibo-der-drc-swp:hasLeg | 具有腿（has leg） | 将互换合约与构成该互换的一腿关联起来。 | 定义域（domain）：互换（swap）；值域（range）：互换腿（swap leg）；子属性（subPropertyOf）：具有合同要素 |
| fibo-der-drc-swp:hasReturnLeg | 具有回报腿（has return leg） | 指明回报互换中支付基于标的资产回报的一腿。 | 定义域（domain）：回报互换（return swap）；值域（range）：回报腿（return leg）；子属性（subPropertyOf）：具有腿（has leg） |
| fibo-der-drc-swp:hasSwapIdentifier | 具有互换标识符（has swap identifier） | 将互换生命周期事件与该互换的标识符关联起来。 | 值域（range）：金融工具标识符；子属性（subPropertyOf）：引用 |
| fibo-der-drc-swp:isLegOf | 是……的腿（is leg of） | 将互换腿与包含该腿的互换关联起来。 | 定义域（domain）：互换腿（swap leg）；值域（range）：互换（swap）；逆属性（inverseOf）：具有腿（has leg）；子属性（subPropertyOf）：被包含于 |

## 5. 公理约定（Axioms）

- 相关性腿（correlation leg）：是……的腿（is leg of） some 相关性互换（correlation swap）
- 离散度腿（dispersion leg）：是……的腿（is leg of） some 离散度互换（dispersion swap）
- 离散度互换（dispersion swap）：具有腿（has leg） 离散度腿（dispersion leg） =1
- 固定腿（fixed leg）：具有支付进度表 支付进度表 ≥0
- 固定腿（fixed leg） 与 浮动腿（floating leg） 互斥（disjointWith）
- 固定支付腿（fixed payment leg）：具有支付进度表 some 支付进度表
- 浮动腿（floating leg）：具有支付进度表 支付进度表 ≥0
- 基于业绩的浮动腿（performance-based variable leg）：是……的腿（is leg of） some 统计互换（statistical swap）
- 利率类腿（rate-based leg）：是……的腿（is leg of） some 利率互换（rates swap）
- 利率类腿（rate-based leg）：具有标的 some（由…扮演（is played by） some（restriction））
- 利率互换（rates swap）：具有腿（has leg） 利率类腿（rate-based leg） =2
- 回报腿（return leg）：是……的腿（is leg of） some 回报互换（return swap）
- 回报腿（return leg）：具有标的 some（restriction）
- 回报互换（return swap）：具有融资腿（has funding leg） some 固定支付腿（fixed payment leg）
- 回报互换（return swap）：具有回报腿（has return leg） some 回报腿（return leg）
- 统计互换（statistical swap）：具有腿（has leg） 固定腿（fixed leg） ≥0
- 统计互换（statistical swap）：具有腿（has leg） some 基于业绩的浮动腿（performance-based variable leg）
- 互换（swap）：由……标识 唯一互换标识符（unique swap identifier） ≥0
- 互换（swap）：具有合同当事方 some 互换方（swap party）
- 互换（swap）：具有合同要素 some 互换条款（swap terms）
- 互换（swap）：交换 some 互换腿（swap leg）
- 互换确认书（swap confirmation）：取代 only 互换确认书（swap confirmation）
- 互换确认书（swap confirmation）：具有合同当事方 some 互换方（swap party）
- 互换腿（swap leg）：restriction
- 互换腿（swap leg）：具有终止日 日期 ≥0
- 互换腿（swap leg）：具有买方 互换付款方（swap paying party） =1
- 互换腿（swap leg）：具有卖方 互换收款方（swap receiving party） =1
- 互换腿（swap leg）：以……计价 货币 =1
- 互换腿（swap leg）：具有生效日期 日期 =1
- 互换腿（swap leg）：是……的腿（is leg of） some 互换（swap）
- 互换腿事件（swap leg event）：适用于 some 互换腿（swap leg）
- 互换生命周期事件（swap lifecycle event）：由……标识 互换生命周期事件标识符（swap lifecycle event identifier） =1
- 互换生命周期事件（swap lifecycle event）：具有互换标识符（has swap identifier） 唯一互换标识符（unique swap identifier） =1
- 互换生命周期事件（swap lifecycle event）：适用于 some 互换（swap）
- 互换生命周期事件（swap lifecycle event）：具有参与方角色（has party role） some 互换方（swap party）
- 互换生命周期事件标识符（swap lifecycle event identifier）：标识 互换生命周期事件（swap lifecycle event） =1
- 互换方（swap party）：由…扮演（is played by） some（是…的参与方（is a party to） some 互换（swap））
- 总回报互换（total return swap）：具有回报腿（has return leg） some 总回报腿（total return leg）
- 唯一互换标识符（unique swap identifier）：标识 互换（swap） =1

## 6. 依赖（owl:imports，28 个）

本本体通过 `owl:imports` 引入以下本体，各项的中文名称与简介如下：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `DER/DerivativesContracts/DerivativesBasics.rdf` | 衍生品基础本体（Derivatives Basics Ontology） | 定义衍生品合约（derivatives contract）的核心概念：标的资产、行权、到期等，是 DER 域的根基。 |
| `FBC/DebtAndEquities/Debt.rdf` | 债务本体（Debt Ontology） | 定义债务（debt）与债权债务关系的核心概念：借款人、贷款人、本金与利息义务。 |
| `FBC/FinancialInstruments/FinancialInstruments.rdf` | 金融工具本体（Financial Instruments Ontology） | FIBO 核心本体之一，定义金融工具（financial instrument）的通用概念：可交易、代表某种权利义务的合同工具，是证券、衍生品等具体工具的共同基础。 |
| `FBC/FunctionalEntities/FinancialServicesEntities.rdf` | 金融服务实体本体（Financial Services Entities Ontology） | FBC 域核心本体，定义金融服务机构（银行、券商、保险公司、资管机构等）的功能分类体系。 |
| `FBC/ProductsAndServices/FinancialProductsAndServices.rdf` | 金融产品与服务本体（Financial Products and Services Ontology） | 定义金融产品（financial product）与金融服务（financial service）及其提供、购买关系。 |
| `FND/Accounting/CurrencyAmount.rdf` | 货币金额本体（Currency Amount Ontology） | 定义「金额＋币种」的货币金额（currency amount）表示，是 FIBO 中表达价格、债务金额、付款额等一切带币种数值的基础构件。 |
| `FND/Agreements/Contracts.rdf` | 合同本体（Contracts Ontology） | 在协议之上定义具有法律约束力的合同（contract）：合同当事方、合同条款、义务与权利，是金融工具与交易合同建模的基石。 |
| `FND/Arrangements/Documents.rdf` | 文档本体（Documents Ontology） | 定义文档、文档类型及文档与其所记载内容的关系，为合同文本、募集说明书等法律文书建模。 |
| `FND/Arrangements/Lifecycles.rdf` | 生命周期本体（Lifecycles Ontology） | 定义生命周期、生命周期阶段与状态转移，用于描述合同、金融工具、机构从创设到终止的演化过程。 |
| `FND/OwnershipAndControl/Ownership.rdf` | 所有权本体（Ownership Ontology） | 定义「拥有」关系：所有者、被拥有资产及所有权份额。 |
| `FND/ProductsAndServices/PaymentsAndSchedules.rdf` | 付款与计划表本体（Payments and Schedules Ontology） | 定义付款、付款计划表（payment schedule）及其日期与金额结构，是贷款还款、债券付息建模的基础。 |
| `FND/ProductsAndServices/ProductsAndServices.rdf` | 产品与服务本体（Products and Services Ontology） | 定义产品、服务及其提供者与客户的通用关系。 |
| `FND/Relations/Relations.rdf` | 关系本体（Relations Ontology） | FIBO 最底层的基础本体，定义参考（reference）、分类（classify）等通用关系与抽象概念，全库普遍依赖。 |
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `IND/EconomicIndicators/EconomicIndicators.rdf` | 经济指标本体（Economic Indicators Ontology） | 定义宏观经济指标（GDP、CPI、失业率等）的通用结构：发布机构、发布频率与数值。 |
| `IND/ForeignExchange/ForeignExchange.rdf` | 外汇本体（Foreign Exchange Ontology） | 定义外汇、汇率（exchange rate）与货币对的概念。 |
| `IND/Indicators/Indicators.rdf` | 指标本体（Indicators Ontology） | 定义「指标」（indicator）的通用概念：对某现象的可度量表示，是经济指标、利率等的上位模型。 |
| `IND/MarketIndices/BasketIndices.rdf` | 篮子指数本体（Basket Indices Ontology） | 定义以一篮子成分为基础的指数：成分、权重与计算方法。 |
| `SEC/Securities/Baskets.rdf` | 篮子本体（Baskets Ontology） | 定义证券篮子（basket）：作为整体交易或定价的一组证券。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |
| `https://www.omg.org/spec/Commons/Collections/` | OMG 通用集合本体（OMG Commons Collections） | Commons 库中的集合本体，定义集合、成员等通用概念。 |
| `https://www.omg.org/spec/Commons/ContextualDesignators/` | OMG 通用语境指称本体（OMG Commons Contextual Designators） | Commons 库中的语境指称本体，定义「在某个语境下指代某物的名称/符号」，是地址、账户号码等语境相关标识的基础。 |
| `https://www.omg.org/spec/Commons/DatesAndTimes/` | OMG 通用日期与时间本体（OMG Commons Dates and Times） | Commons 库中的日期时间本体，定义日期、期间、时间点等通用时间概念。 |
| `https://www.omg.org/spec/Commons/Documents/` | OMG 通用文档本体（OMG Commons Documents） | Commons 库中的文档本体，定义文档及其组成部分的通用概念。 |
| `https://www.omg.org/spec/Commons/Identifiers/` | OMG 通用标识符本体（OMG Commons Identifiers） | Commons 库中的标识符本体，定义标识符及其编码方案的通用概念。 |
| `https://www.omg.org/spec/Commons/PartiesAndSituations/` | OMG 通用参与方与情境本体（OMG Commons Parties and Situations） | Commons 库中的参与方本体，定义独立主体、参与方及其角色扮演的通用概念，是 FIBO 参与方模型的上游。 |
| `https://www.omg.org/spec/Commons/QuantitiesAndUnits/` | OMG 通用量与单位本体（OMG Commons Quantities and Units） | Commons 库中的量与单位本体，定义数量、度量单位、量纲的通用概念，支撑金额、比率等数值表达。 |
| `https://www.omg.org/spec/Commons/RolesAndCompositions/` | OMG 通用角色与构成本体（OMG Commons Roles and Compositions） | Commons 库中的角色本体，定义角色及整体—部分构成关系的通用概念。 |

## 7. 文件

- 官方 RDF/XML：`Swaps.rdf`
- 中文 Turtle：`Swaps.ttl`
- 结构图：`Swaps-structure.png` / `Swaps-structure.svg`