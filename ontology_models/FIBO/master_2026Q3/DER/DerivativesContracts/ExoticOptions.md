# 奇异期权本体（Exotic Options Ontology）结构与公理说明

本文档对应 `ExoticOptions.rdf` / `ExoticOptions.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `ExoticOptions-structure.png`（`ExoticOptions-structure.svg` 为可缩放版本）。

![奇异期权本体（Exotic Options Ontology）本体结构图](ExoticOptions-structure.png)

## 1. 本体概述

定义奇异期权（exotic option）：条款非标准化的期权，如障碍期权、亚式期权、百慕大期权等。

**在体系中的位置**：衍生品合约模块中期权本体的扩展。

**上下游关系**：上游继承期权本体；下游主要服务于场外结构化产品设计。

**与相近概念的差别**：与普通（香草，vanilla）期权的差别——行权条件依赖路径、障碍触发或平均价格等复杂机制，定价与风险特征完全不同。

## 2. 类（Class）

| 类（Class） | 定义（Definition） |
|---|---|
| 亚式期权（Asian option） | 行权条款中支付额由标的平均价格（行权价或结算价）决定的期权。 |
| 亚式期权分类器（Asian option classifier） | 按基于利率还是基于价格对亚式期权进行分类的金融工具分类器。 |
| 平均方法（averaging strategy） | 用于计算亚式期权平均利率或平均价格的方法。 |
| 障碍期权（barrier option） | 最终行权取决于标的工具价格路径的期权，即其支付取决于标的价格是否触及特定水平。 |
| 任选期权（chooser option） | 允许持有人（买方）选择按固定价格买入（看涨）或卖出（看跌）指定资产之权利的奇异期权。 |
| 棘轮期权（cliquet option） | 由一系列平值（ATM）期权（看跌或看涨）构成的奇异期权，前一期权到期时后一期权生效。 |
| 康莫多期权（commodore option） | 由若干数字障碍期权构成的奇异期权，当标的或标的篮子达到预定水平时支付票息。 |
| 复合期权（compound option） | 标的资产为另一期权的奇异期权。 |
| 数字期权（digital option） | 在期权处于实值且支付条件满足时支付预定金额的奇异期权。 |
| 双重障碍期权（double barrier option） | 应用于货币或场外股票的障碍期权，其运作方式类似二元（数字）期权，仅在规定情形下支付。 |
| 固定回望行权价表达式（fixed lookback strike expression） | 规定计算回望期权固定行权价所需参数的现金流表达式。 |
| 浮动回望行权价表达式（floating lookback strike expression） | 规定计算回望期权可行权最优预计价格所需参数的现金流表达式。 |
| 远期生效期权（forward start option） | 就已定到期日、标的资产和其他参数完全确定、在购买时付款、但在未来某时生效的奇异期权。 |
| 利率上限期权（interest rate cap option） | 买方在每个利率超过约定行权价的期间结束时收到付款的利率衍生品。 |
| 利率下限期权（interest rate floor option） | 买方在每个利率低于约定行权价的期间结束时收到付款的利率衍生品。 |
| 敲入期权（knock-in option） | 在达到特定价格门槛之前不被触发的障碍期权。 |
| 敲出期权（knock-out option） | 内建机制使期权在标的资产达到指定价格水平时作废失效的障碍期权。 |
| 回望期权（lookback option） | 最大限度降低市场进入时点不确定性的奇异期权，持有人在确定行权时可利用历史价格信息。 |
| 回望行权条款（lookback strike terms） | 基于特定期间（通常截至期权到期）的分析确定标的资产价值的条款。 |
| 低行权价期权（low exercise price option） | 行权价为一分钱的欧式看涨期权，其表现类似于期货合约。 |
| 山岭期权（mountain range option） | 基于多种标的证券的奇异期权。 |
| 观察最优值（observed best value） | 回望期内某一日期观察到的、从期权视角被视为最优的标的资产价值。 |
| 到期预计价值（projected value at maturity） | 在回望期内某一日期计算得出的标的资产到期预期价值。 |
| 彩虹期权（rainbow option） | 与两种或更多标的资产的表现挂钩的奇异期权。 |
| 互换期权（swaption） | 赋予持有人在未来某时进入互换交易的权利（而非义务）的场外期权。 |

### 2.1 继承关系（Inheritance）

- 亚式期权（Asian option） ⊑ 奇异期权
- 亚式期权分类器（Asian option classifier） ⊑ 金融工具分类器
- 平均方法（averaging strategy） ⊑ 战略
- 障碍期权（barrier option） ⊑ 奇异期权
- 任选期权（chooser option） ⊑ 奇异期权
- 棘轮期权（cliquet option） ⊑ 奇异期权
- 康莫多期权（commodore option） ⊑ 奇异期权
- 复合期权（compound option） ⊑ 奇异期权
- 数字期权（digital option） ⊑ 障碍期权（barrier option）
- 双重障碍期权（double barrier option） ⊑ 障碍期权（barrier option）
- 固定回望行权价表达式（fixed lookback strike expression） ⊑ 现金流表达式
- 浮动回望行权价表达式（floating lookback strike expression） ⊑ 现金流表达式
- 远期生效期权（forward start option） ⊑ 奇异期权
- 利率上限期权（interest rate cap option） ⊑ 利率期权
- 利率下限期权（interest rate floor option） ⊑ 利率期权
- 敲入期权（knock-in option） ⊑ 障碍期权（barrier option）
- 敲出期权（knock-out option） ⊑ 障碍期权（barrier option）
- 回望期权（lookback option） ⊑ 奇异期权
- 回望行权条款（lookback strike terms） ⊑ 衍生品条款
- 低行权价期权（low exercise price option） ⊑ 看涨期权
- 低行权价期权（low exercise price option） ⊑ 奇异期权
- 山岭期权（mountain range option） ⊑ 奇异期权
- 观察最优值（observed best value） ⊑ 市场价格
- 到期预计价值（projected value at maturity） ⊑ 计算价格
- 彩虹期权（rainbow option） ⊑ 奇异期权
- 互换期权（swaption） ⊑ 奇异期权

## 3. 对象属性（Object Property）

| 属性（Property） | 中文（English） | 定义（Definition） | 说明 |
|---|---|---|---|
| fibo-der-drc-exo:hasAsianTailPeriod | 具有亚式尾部期间（has Asian tail period） | 标的合约价格平均值计算生效的时间窗口。 | 定义域（domain）：亚式期权（Asian option）；值域（range）：日期区间；子属性（subPropertyOf）：具有日期区间 |
| fibo-der-drc-exo:hasFirstBarrierPrice | 具有第一障碍价格（has first barrier price） | 激活或使期权失效的价格（或水平）。 | 值域（range）：货币价格；子属性（subPropertyOf）：具有价格 |
| fibo-der-drc-exo:hasFirstRebateAmount | 具有第一返还金额（has first rebate amount） | 指明持有人为期权支付的权利金百分比。 | 值域（range）：百分比货币数量；子属性（subPropertyOf）：具有价格 |
| fibo-der-drc-exo:hasLookbackPeriod | 具有回望期（has lookback period） | 回望生效的时间窗口。 | 定义域（domain）：回望行权条款（lookback strike terms）；值域（range）：日期区间；子属性（subPropertyOf）：具有日期区间 |
| fibo-der-drc-exo:hasMonitoringPeriod | 具有监测期（has monitoring period） | 对定价进行监测的时间窗口。 | 定义域（domain）：障碍期权（barrier option）；值域（range）：日期区间；子属性（subPropertyOf）：具有日期区间 |
| fibo-der-drc-exo:hasOptionTypeElectionDate | 具有期权类型选择日（has option type election date） | 指明任选期权合约持有人选择看涨或看跌的日期。 | 定义域（domain）：任选期权（chooser option）；值域（range）：显式日期；子属性（subPropertyOf）：具有显式日期 |
| fibo-der-drc-exo:hasSecondBarrierPrice | 具有第二障碍价格（has second barrier price） | 双重障碍期权中第二重障碍激活或失效的价格（或水平）。 | 值域（range）：货币价格；子属性（subPropertyOf）：具有价格 |
| fibo-der-drc-exo:hasSecondRebateAmount | 具有第二返还金额（has second rebate amount） | 指明双重障碍期权中持有人支付的权利金百分比。 | 值域（range）：百分比货币数量；子属性（subPropertyOf）：具有价格 |
| fibo-der-drc-exo:usesCurrencyInAveraging | 平均值计算所用货币（uses currency in averaging） | 指明平均值计算所使用的货币。 | 值域（range）：货币；子属性（subPropertyOf）：具有货币 |

## 4. 数据属性（Datatype Property）

| 属性（Property） | 中文（English） | 定义（Definition） |
|---|---|---|
| fibo-der-drc-exo:hasMonitoringFrequency | 具有监测频率（has monitoring frequency） | 检查资产价格是否突破障碍的频率（以天计）。 |
| fibo-der-drc-exo:isAboveStrikePrice | 是否高于行权价（is above strike price） | 表明标的价格高于（或低于）行权价（门槛）时是否触发障碍。 |
| fibo-der-drc-exo:usesWeightedAverage | 是否使用加权平均（uses weighted average） | 表明是否使用加权平均来计算平均利率或行权价。 |

## 5. 公理约定（Axioms）

- 亚式期权（Asian option）：由……分类 亚式期权分类器（Asian option classifier） =1
- 亚式期权（Asian option）：由……分类 平均方法（averaging strategy） =1
- 亚式期权（Asian option）：平均值计算所用货币（uses currency in averaging） 货币 =1
- 亚式期权（Asian option）：具有亚式尾部期间（has Asian tail period） 日期区间 =1
- 亚式期权（Asian option）：具有行权日 显式日期 =1
- 亚式期权（Asian option）：restriction
- 亚式期权分类器（Asian option classifier）：分类 some 亚式期权（Asian option）
- 平均方法（averaging strategy）：分类 some 亚式期权（Asian option）
- 障碍期权（barrier option）：具有监测频率（has monitoring frequency） some xsd:positiveInteger
- 障碍期权（barrier option）：具有监测期（has monitoring period） some 日期区间
- 障碍期权（barrier option）：是否高于行权价（is above strike price） some xsd:boolean
- 任选期权（chooser option）：具有期权类型选择日（has option type election date） some 显式日期
- 任选期权（chooser option）：包含 some（restriction）
- 棘轮期权（cliquet option）：包含 some 远期生效期权（forward start option）
- 康莫多期权（commodore option）：包含 some 数字期权（digital option）
- 复合期权（compound option）：包含 some 期权
- 双重障碍期权（double barrier option）：具有第一返还金额（has first rebate amount） 百分比货币数量 ≥0
- 双重障碍期权（double barrier option）：具有第二返还金额（has second rebate amount） 百分比货币数量 ≥0
- 双重障碍期权（double barrier option）：具有第一障碍价格（has first barrier price） some 货币价格
- 双重障碍期权（double barrier option）：具有第二障碍价格（has second barrier price） some 货币价格
- 固定回望行权价表达式（fixed lookback strike expression）：具有被减数 some 行权价
- 固定回望行权价表达式（fixed lookback strike expression）：具有减数 some 观察最优值（observed best value）
- 浮动回望行权价表达式（floating lookback strike expression）：具有被减数 some 到期预计价值（projected value at maturity）
- 浮动回望行权价表达式（floating lookback strike expression）：具有减数 some 观察最优值（observed best value）
- 远期生效期权（forward start option）：包含 some（restriction）
- 利率上限期权（interest rate cap option） 与 利率下限期权（interest rate floor option） 互斥（disjointWith）
- 利率下限期权（interest rate floor option） 与 利率上限期权（interest rate cap option） 互斥（disjointWith）
- 敲入期权（knock-in option）：具有第一返还金额（has first rebate amount） 百分比货币数量 ≥0
- 敲入期权（knock-in option）：具有第一障碍价格（has first barrier price） some 货币价格
- 敲出期权（knock-out option）：具有第一返还金额（has first rebate amount） 百分比货币数量 ≥0
- 敲出期权（knock-out option）：具有第一障碍价格（has first barrier price） some 货币价格
- 回望期权（lookback option）：具有合同要素 some 回望行权条款（lookback strike terms）
- 回望行权条款（lookback strike terms）：具有表达式 固定回望行权价表达式（fixed lookback strike expression） ≥0
- 回望行权条款（lookback strike terms）：具有表达式 浮动回望行权价表达式（floating lookback strike expression） ≥0
- 回望行权条款（lookback strike terms）：具有回望期（has lookback period） some 日期区间
- 回望行权条款（lookback strike terms）：具有自变量 some 价格结构
- 低行权价期权（low exercise price option）：restriction
- 山岭期权（mountain range option）：具有标的 some（由…扮演（is played by） some 混合篮子）
- 观察最优值（observed best value）：具有截止日 some 日期
- 到期预计价值（projected value at maturity）：具有观测日期时间 some cmns-dt:CombinedDateTime
- 彩虹期权（rainbow option）：具有标的 some（由…扮演（is played by） some 混合篮子）
- 互换期权（swaption）：具有标的 some（由…扮演（is played by） some 互换）

## 6. 依赖（owl:imports，21 个）

本本体通过 `owl:imports` 引入以下本体，各项的中文名称与简介如下：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `DER/DerivativesContracts/DerivativesBasics.rdf` | 衍生品基础本体（Derivatives Basics Ontology） | 定义衍生品合约（derivatives contract）的核心概念：标的资产、行权、到期等，是 DER 域的根基。 |
| `DER/DerivativesContracts/Options.rdf` | 期权本体（Options Ontology） | 定义期权（option）：买方权利、行权价、到期日、看涨与看跌等核心结构。 |
| `DER/DerivativesContracts/Swaps.rdf` | 互换本体（Swaps Ontology） | 定义互换（swap）合约的通用结构：互换腿（swap leg）、现金流交换与名义本金。 |
| `FBC/FinancialInstruments/FinancialInstruments.rdf` | 金融工具本体（Financial Instruments Ontology） | FIBO 核心本体之一，定义金融工具（financial instrument）的通用概念：可交易、代表某种权利义务的合同工具，是证券、衍生品等具体工具的共同基础。 |
| `FBC/FinancialInstruments/InstrumentPricing.rdf` | 工具定价本体（Instrument Pricing Ontology） | 定义金融工具的价格、报价与估值概念。 |
| `FND/Accounting/CurrencyAmount.rdf` | 货币金额本体（Currency Amount Ontology） | 定义「金额＋币种」的货币金额（currency amount）表示，是 FIBO 中表达价格、债务金额、付款额等一切带币种数值的基础构件。 |
| `FND/Agreements/Contracts.rdf` | 合同本体（Contracts Ontology） | 在协议之上定义具有法律约束力的合同（contract）：合同当事方、合同条款、义务与权利，是金融工具与交易合同建模的基石。 |
| `FND/DatesAndTimes/FinancialDates.rdf` | 金融日期本体（Financial Dates Ontology） | 定义金融语境下的日期与期间概念：结算日、付息日、到期日、日计数基准等。 |
| `FND/GoalsAndObjectives/Objectives.rdf` | 目标本体（Objectives Ontology） | 定义目标（objective）及其与组织、计划的关系，用于表达机构的经营目标与投资目标。 |
| `FND/Utilities/Analytics.rdf` | 分析本体（Analytics Ontology） | 定义分析工具、度量与比率的通用概念，支撑指标与模型的表达。 |
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `IND/Indicators/Indicators.rdf` | 指标本体（Indicators Ontology） | 定义「指标」（indicator）的通用概念：对某现象的可度量表示，是经济指标、利率等的上位模型。 |
| `SEC/Debt/ExerciseConventions.rdf` | 行权惯例本体（Exercise Conventions Ontology） | 定义债务工具中嵌入期权的行权惯例：美式、欧式、百慕大式。 |
| `SEC/Securities/Baskets.rdf` | 篮子本体（Baskets Ontology） | 定义证券篮子（basket）：作为整体交易或定价的一组证券。 |
| `SEC/Securities/SecuritiesClassification.rdf` | 证券分类本体（Securities Classification Ontology） | 定义证券分类方案：按 CFI 代码、按资产类别等对证券归类。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |
| `https://www.omg.org/spec/Commons/Classifiers/` | OMG 通用分类器本体（OMG Commons Classifiers） | OMG 通用本体库（Commons）中的分类器本体，定义分类方案、类别与归类关系的通用概念，FIBO 的分类建模建立在其上。 |
| `https://www.omg.org/spec/Commons/Collections/` | OMG 通用集合本体（OMG Commons Collections） | Commons 库中的集合本体，定义集合、成员等通用概念。 |
| `https://www.omg.org/spec/Commons/DatesAndTimes/` | OMG 通用日期与时间本体（OMG Commons Dates and Times） | Commons 库中的日期时间本体，定义日期、期间、时间点等通用时间概念。 |
| `https://www.omg.org/spec/Commons/QuantitiesAndUnits/` | OMG 通用量与单位本体（OMG Commons Quantities and Units） | Commons 库中的量与单位本体，定义数量、度量单位、量纲的通用概念，支撑金额、比率等数值表达。 |
| `https://www.omg.org/spec/Commons/RolesAndCompositions/` | OMG 通用角色与构成本体（OMG Commons Roles and Compositions） | Commons 库中的角色本体，定义角色及整体—部分构成关系的通用概念。 |

## 7. 文件

- 官方 RDF/XML：`ExoticOptions.rdf`
- 中文 Turtle：`ExoticOptions.ttl`
- 结构图：`ExoticOptions-structure.png` / `ExoticOptions-structure.svg`