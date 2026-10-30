# 大宗商品合约本体（Commodities Contracts Ontology）结构与公理说明

本文档对应 `CommoditiesContracts.rdf` / `CommoditiesContracts.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `CommoditiesContracts-structure.png`（`CommoditiesContracts-structure.svg` 为可缩放版本）。

![大宗商品合约本体（Commodities Contracts Ontology）本体结构图](CommoditiesContracts-structure.png)

## 1. 本体概述

定义以大宗商品（能源、金属、农产品等）为标的的衍生品合约。

**在体系中的位置**：衍生品合约模块中按标的资产特化的本体之一。

**上下游关系**：上游继承衍生品基础、期货与远期本体；下游服务商品市场的套保与交易建模。

**与相近概念的差别**：与金融标的衍生品的差别——商品合约常涉及实物交割、仓储与品质规格，这是金融合约没有的问题。

## 2. 类（Class）

| 类（Class） | 定义（Definition） |
|---|---|
| 农业资源（agricultural resource） | 通过农业过程获得的可转让商品，包括林业、渔业、畜牧、谷物、乳制品、玉米、可可、大豆、糖等。 |
| 基本金属（base metal） | 暴露于空气或湿气中时相对较快失去光泽、氧化或腐蚀、并广泛用于商业和工业的普通金属。 |
| 商品篮子（basket of commodities） | 成分由一种或多种可转让商品组成的定制篮子。 |
| 金银条块（bullion） | 经官方认定纯度至少达 99.5% 的实物贵金属。 |
| 商品篮子成分（commodity basket constituent） | 定制商品篮子的组成部分，其相对于其他篮子成分的重要性为已知。 |
| 商品衍生品（commodity derivative） | 主要标的为实物商品、商品价格、相关指数或与实物商品相关之任何其他方面的衍生工具。 |
| 商品衍生品标的（commodity derivative underlier） | 商品衍生品的标的，包括但不限于可转让商品本身。 |
| 商品远期（commodity forward） | 买方和卖方约定在未来指定日期交付指定质量和数量货物的远期合约。 |
| 商品期货（commodity future） | 在未来特定日期按特定价格买入或卖出预定数量商品的期货合约。 |
| 商品指数（commodity index） | 追踪一篮子商品以衡量其价格和投资回报表现的投资工具。 |
| 商品期权（commodity option） | 期权买方有权在到期日或之前按固定价格或公式买入或卖出指定商品或商品相关指数的期权。 |
| 商品回报腿（commodity return leg） | 商品回报互换中回报基于实物商品、商品价格、价格行为或与商品相关之任何其他方面的一腿。 |
| 商品即期合约（commodity spot contract） | 结算时涉及商品资产实物交割的合约。 |
| 商品互换（commodity swap） | 一种商品衍生品：包括但不限于任何主要名义标的为实物商品或商品价格的互换。 |
| 能源资源（energy resource） | 属于能源相关产品或其衍生品的可转让商品，包括电力、可再生能源等。 |
| 能源输电权（energy transmission rights） | 在配电网络中输送电力的权利。 |
| 环境资源（environmental resource） | 包括抵消信用额在内的可转让商品。 |
| 开采资源（extraction resource） | 通过从自然环境中开采获得的矿产资源类可转让商品。 |
| 化肥资源（fertilizer resource） | 包括氨、磷酸二铵（DAP）、钾肥、硫磺、尿素、尿素硝酸铵（UAN）在内的可转让商品。 |
| 运费资源（freight resource） | 属于运费指数航线的可转让商品。 |
| 天然气商品（gas commodity） | 属于天然气的开采资源。 |
| 发电资源（generated resource） | 通过某种生产过程获得的可转让商品，包括电力、可再生能源或任何通过公用事业网络输送的电力/能源。 |
| 谷物商品（grain commodity） | 属于食用植物（尤其是禾谷类植物）细小坚硬种子的农业资源，如小麦、玉米、黑麦、燕麦、大米和小米。 |
| 工业资源（industrial resource） | 通过工业过程（包括建筑和制造）获得的可转让商品。 |
| 肉类商品（meat commodity） | 源自动物（尤其是哺乳动物）肉体的农业资源，如猪腩肉。 |
| 金属（metal） | 新鲜制备、抛光或断裂时呈现光泽外观、且导电导热性能较好的材料。 |
| 石油商品（oil commodity） | 从石油提炼的粘稠液体类发电资源，用于燃料、润滑剂及多种产品的制造。 |
| 油品等级（oil grade） | 衡量石油在使用过程中粘度的指标。 |
| 纸类资源（paper resource） | 属于纸制品的可转让商品，包括箱板纸、新闻纸、纸浆、回收纸等。 |
| 聚丙烯资源（polypropylene resource） | 包括塑料在内的可转让商品。 |
| 服务资源（service resource） | 涉及运输、通信和贸易等服务的可转让商品。 |
| 天气衍生品（weather derivative） | 主要名义标的基于天气相关事物（例如某地平均温度）的衍生工具。 |

### 2.1 继承关系（Inheritance）

- 农业资源（agricultural resource） ⊑ 可流通商品
- 基本金属（base metal） ⊑ 金属（metal）
- 商品篮子（basket of commodities） ⊑ 加权篮子
- 金银条块（bullion） ⊑ 贵金属
- 商品篮子成分（commodity basket constituent） ⊑ 加权篮子成分
- 商品衍生品（commodity derivative） ⊑ 商品工具
- 商品衍生品（commodity derivative） ⊑ 衍生工具
- 商品衍生品标的（commodity derivative underlier） ⊑ 标的
- 商品远期（commodity forward） ⊑ 商品衍生品（commodity derivative）
- 商品远期（commodity forward） ⊑ 远期合约
- 商品期货（commodity future） ⊑ 商品衍生品（commodity derivative）
- 商品期货（commodity future） ⊑ 期货
- 商品指数（commodity index） ⊑ 参考指数
- 商品期权（commodity option） ⊑ 商品衍生品（commodity derivative）
- 商品期权（commodity option） ⊑ 普通期权
- 商品回报腿（commodity return leg） ⊑ 回报腿
- 商品即期合约（commodity spot contract） ⊑ 商品工具
- 商品即期合约（commodity spot contract） ⊑ 即期合约
- 商品互换（commodity swap） ⊑ 商品衍生品（commodity derivative）
- 商品互换（commodity swap） ⊑ 回报互换
- 能源资源（energy resource） ⊑ 可流通商品
- 能源输电权（energy transmission rights） ⊑ 能源资源（energy resource）
- 环境资源（environmental resource） ⊑ 可流通商品
- 开采资源（extraction resource） ⊑ 可流通商品
- 化肥资源（fertilizer resource） ⊑ 可流通商品
- 运费资源（freight resource） ⊑ 可流通商品
- 天然气商品（gas commodity） ⊑ 能源资源（energy resource）
- 天然气商品（gas commodity） ⊑ 开采资源（extraction resource）
- 发电资源（generated resource） ⊑ 可流通商品
- 谷物商品（grain commodity） ⊑ 农业资源（agricultural resource）
- 工业资源（industrial resource） ⊑ 可流通商品
- 肉类商品（meat commodity） ⊑ 农业资源（agricultural resource）
- 金属（metal） ⊑ 开采资源（extraction resource）
- 石油商品（oil commodity） ⊑ 发电资源（generated resource）
- 油品等级（oil grade） ⊑ 分类符
- 纸类资源（paper resource） ⊑ 可流通商品
- 聚丙烯资源（polypropylene resource） ⊑ 可流通商品
- 服务资源（service resource） ⊑ 可流通商品
- 天气衍生品（weather derivative） ⊑ 商品衍生品（commodity derivative）
- 天气衍生品（weather derivative） ⊑ 衍生工具

## 3. 对象属性（Object Property）

| 属性（Property） | 中文（English） | 定义（Definition） | 说明 |
|---|---|---|---|
| fibo-der-drc-comm:hasCommodityValueAsOfDate | 具有某日商品价值（has commodity value as of date） | 指明某一商品在指定日期的单位价值。 | 值域（range）：货币数量；子属性（subPropertyOf）：具有货币数量 |
| fibo-der-drc-comm:hasGrade | 具有等级（has grade） | 石油的等级，例如布伦特原油（Brent Crude）。 | 定义域（domain）：石油商品（oil commodity）；值域（range）：油品等级（oil grade） |

## 5. 公理约定（Axioms）

- 基本金属（base metal） 与 贵金属 互斥（disjointWith）
- 商品篮子（basket of commodities）：具有成员 some 商品篮子成分（commodity basket constituent）
- 商品篮子成分（commodity basket constituent）：具有某日商品价值（has commodity value as of date） 货币数量 ≥0
- 商品篮子成分（commodity basket constituent）：涉及 商品 ≥0
- 商品篮子成分（commodity basket constituent）：具有截止日 显式日期 ≥0
- 商品篮子成分（commodity basket constituent）：具有量值 标量值 ≥0
- 商品衍生品（commodity derivative）：具有标的 商品衍生品标的（commodity derivative underlier） ≥0
- 商品衍生品标的（commodity derivative underlier）：具有某日商品价值（has commodity value as of date） 货币数量 ≥0
- 商品衍生品标的（commodity derivative underlier）：涉及 商品 ≥0
- 商品衍生品标的（commodity derivative underlier）：具有截止日 显式日期 ≥0
- 商品衍生品标的（commodity derivative underlier）：具有量值 标量值 ≥0
- 商品期货（commodity future） 与 金融期货 互斥（disjointWith）
- 商品指数（commodity index）：基于 some 商品篮子（basket of commodities）
- 商品回报腿（commodity return leg）：具有标的 some 商品衍生品标的（commodity derivative underlier）
- 商品互换（commodity swap）：具有回报腿 some 商品回报腿（commodity return leg）
- 石油商品（oil commodity）：具有等级（has grade） some 油品等级（oil grade）

## 6. 依赖（owl:imports，19 个）

本本体通过 `owl:imports` 引入以下本体，各项的中文名称与简介如下：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `DER/DerivativesContracts/DerivativesBasics.rdf` | 衍生品基础本体（Derivatives Basics Ontology） | 定义衍生品合约（derivatives contract）的核心概念：标的资产、行权、到期等，是 DER 域的根基。 |
| `DER/DerivativesContracts/FuturesAndForwards.rdf` | 期货与远期本体（Futures and Forwards Ontology） | 定义期货（futures）与远期（forwards）合约：标准化与非标准化的远期交割安排。 |
| `DER/DerivativesContracts/Options.rdf` | 期权本体（Options Ontology） | 定义期权（option）：买方权利、行权价、到期日、看涨与看跌等核心结构。 |
| `DER/DerivativesContracts/Swaps.rdf` | 互换本体（Swaps Ontology） | 定义互换（swap）合约的通用结构：互换腿（swap leg）、现金流交换与名义本金。 |
| `FBC/DebtAndEquities/Debt.rdf` | 债务本体（Debt Ontology） | 定义债务（debt）与债权债务关系的核心概念：借款人、贷款人、本金与利息义务。 |
| `FBC/FinancialInstruments/FinancialInstruments.rdf` | 金融工具本体（Financial Instruments Ontology） | FIBO 核心本体之一，定义金融工具（financial instrument）的通用概念：可交易、代表某种权利义务的合同工具，是证券、衍生品等具体工具的共同基础。 |
| `FBC/ProductsAndServices/FinancialProductsAndServices.rdf` | 金融产品与服务本体（Financial Products and Services Ontology） | 定义金融产品（financial product）与金融服务（financial service）及其提供、购买关系。 |
| `FND/Accounting/CurrencyAmount.rdf` | 货币金额本体（Currency Amount Ontology） | 定义「金额＋币种」的货币金额（currency amount）表示，是 FIBO 中表达价格、债务金额、付款额等一切带币种数值的基础构件。 |
| `FND/Agreements/Contracts.rdf` | 合同本体（Contracts Ontology） | 在协议之上定义具有法律约束力的合同（contract）：合同当事方、合同条款、义务与权利，是金融工具与交易合同建模的基石。 |
| `FND/DatesAndTimes/FinancialDates.rdf` | 金融日期本体（Financial Dates Ontology） | 定义金融语境下的日期与期间概念：结算日、付息日、到期日、日计数基准等。 |
| `FND/ProductsAndServices/ProductsAndServices.rdf` | 产品与服务本体（Products and Services Ontology） | 定义产品、服务及其提供者与客户的通用关系。 |
| `FND/Relations/Relations.rdf` | 关系本体（Relations Ontology） | FIBO 最底层的基础本体，定义参考（reference）、分类（classify）等通用关系与抽象概念，全库普遍依赖。 |
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `IND/MarketIndices/BasketIndices.rdf` | 篮子指数本体（Basket Indices Ontology） | 定义以一篮子成分为基础的指数：成分、权重与计算方法。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |
| `https://www.omg.org/spec/Commons/Classifiers/` | OMG 通用分类器本体（OMG Commons Classifiers） | OMG 通用本体库（Commons）中的分类器本体，定义分类方案、类别与归类关系的通用概念，FIBO 的分类建模建立在其上。 |
| `https://www.omg.org/spec/Commons/Collections/` | OMG 通用集合本体（OMG Commons Collections） | Commons 库中的集合本体，定义集合、成员等通用概念。 |
| `https://www.omg.org/spec/Commons/DatesAndTimes/` | OMG 通用日期与时间本体（OMG Commons Dates and Times） | Commons 库中的日期时间本体，定义日期、期间、时间点等通用时间概念。 |
| `https://www.omg.org/spec/Commons/QuantitiesAndUnits/` | OMG 通用量与单位本体（OMG Commons Quantities and Units） | Commons 库中的量与单位本体，定义数量、度量单位、量纲的通用概念，支撑金额、比率等数值表达。 |

## 7. 文件

- 官方 RDF/XML：`CommoditiesContracts.rdf`
- 中文 Turtle：`CommoditiesContracts.ttl`
- 结构图：`CommoditiesContracts-structure.png` / `CommoditiesContracts-structure.svg`