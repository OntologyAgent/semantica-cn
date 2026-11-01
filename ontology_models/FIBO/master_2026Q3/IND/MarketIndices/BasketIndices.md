# 篮子指数本体（Basket Indices Ontology）结构与公理说明

本文档对应 `BasketIndices.rdf` / `BasketIndices.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `BasketIndices-structure.png`（`BasketIndices-structure.svg` 为可缩放版本）。

![篮子指数本体（Basket Indices Ontology）本体结构图](BasketIndices-structure.png)

## 1. 本体概述

定义以一篮子成分为基础的指数（basket index）：成分、权重、计算方法与维护规则。

**在体系中的位置**：IND 市场指数模块的核心，股指示例（如道琼斯）以此为基础。

**上下游关系**：上游继承指标本体并引用 SEC 篮子本体；下游服务指数基金、衍生品标的建模。

**与相近概念的差别**：指数≠指标——指数是按既定规则对一篮子成分加权计算的合成数值，可投资可复制；指标是单一统计量，不可直接投资。

本本体中类与类的核心关系如下（完整细节见各类小节）：

- **信用风险篮子（basket of credit risks）** 继承 **加权篮子（WeightedBasket）**
- **信用风险篮子（basket of credit risks）** 继承 **带日期结构化集合（DatedStructuredCollection）**
- **股票篮子（basket of equities）** 继承 **证券篮子（BasketOfSecurities）**
- **市值加权函数（capitalization-based weighting function）** 继承 **加权函数（WeightingFunction）**
- **信用指数（credit index）** 继承 **参考指数（reference index）**
- **信用指数成分（credit index constituent）** 继承 **加权篮子成分（WeightedBasketConstituent）**
- **信用指数成分（credit index constituent）** 继承 **带日期集合成分（DatedCollectionConstituent）**
- **股票指数（equity index）** 继承 **参考指数（reference index）**
- **市值（market capitalization）** 继承 **表达式（Expression）**
- **参考指数（reference index）** 继承 **限定范围度量（ScopedMeasure）**

## 2. 类（Class）

| 类（Class） | 定义（Definition） |
|---|---|
| 信用风险篮子（basket of credit risks） | 为风险分析目的而汇集的工具、法律实体或其组合的篮子。<br>basket of instruments, legal entities, or a combination thereof collected for the purpose of analyzing risk |
| 股票篮子（basket of equities） | 成分为上市股票的证券篮子。<br>basket of securities whose constituents are listed shares |
| 市值加权函数（capitalization-based weighting function） | 由指数所跟踪公司的相对市值（股价乘以流通股数）导出的加权函数。<br>weighting function derived from the relative market capitalization (share price times the number of shares outstanding) of the companies tracked by an index |
| 信用指数（credit index） | 以改变标的组合价值的信用事件为函数的参考指数。<br>reference index that is a function of credit events that change the value of an underlying portfolio |
| 信用指数成分（credit index constituent） | 信用风险篮子的组成成分。<br>constituent of a basket of credit risks |
| 股票指数（equity index） | 成分全部为股票工具的基准指数。<br>benchmark whose constituents are exclusively equity instruments |
| 市值（market capitalization） | 表示股票市场在特定时点对公司之估值的表达式。<br>expression representing the perceived value of a company as determined by the stock market at a specific point in time |
| 参考指数（reference index） | 篮子内容在给定时期内价值变化的度量。<br>measure of change in the value of the contents of a basket over a given period of time |

以下按类逐个展开：每个类给出继承关系、相关属性与公理约定；子类在父类之下降一级编号。

### 2.1 信用风险篮子（basket of credit risks）

定义：为风险分析目的而汇集的工具、法律实体或其组合的篮子。

- 父类：**加权篮子（WeightedBasket）**、**带日期结构化集合（DatedStructuredCollection）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有成员（hasMember）** | — | — |

公理：

- **具有成员（hasMember）**至少有一个取值，类型是**信用指数成分（credit index constituent）**。

### 2.2 股票篮子（basket of equities）

定义：成分为上市股票的证券篮子。

- 父类：**证券篮子（BasketOfSecurities）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有成员（hasMember）** | — | — |

公理：

- **具有成员（hasMember）**至少有一个取值，该取值满足：该属性存在取值约束。

### 2.3 市值加权函数（capitalization-based weighting function）

定义：由指数所跟踪公司的相对市值（股价乘以流通股数）导出的加权函数。

- 父类：**加权函数（WeightingFunction）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有市值（has market capitalization）** | 标识某发行人在某日期的市值。<br>indicates the market capitalization of some issuer as of some date | 值域：市值（market capitalization） |

公理：

- **具有市值（has market capitalization）**至少有一个取值，类型是**市值（market capitalization）**。

### 2.4 信用指数成分（credit index constituent）

定义：信用风险篮子的组成成分。

- 父类：**加权篮子成分（WeightedBasketConstituent）**、**带日期集合成分（DatedCollectionConstituent）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有货币（hasCurrency）** | — | — |
| **具有债务排序（has debt ranking）** | 标识该债务工具相对于信用指数整体的排序。<br>indicates the ranking of this debt instrument with respect to the credit index as a whole | 值域：xsd:string |
| **引用（refersTo）** | — | — |

公理：

- **具有货币（hasCurrency）**至少有一个取值，类型是**货币（Currency）**。
- **引用（refersTo）**至少有一个取值，类型是**信用事件（CreditEvent）**。

### 2.5 市值（market capitalization）

定义：表示股票市场在特定时点对公司之估值的表达式。

- 父类：**表达式（Expression）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有市值金额（has market capitalization value）** | 标识表示某发行人在某日期市值的货币金额。<br>indicates the monetary amount representing the market capitalization of some issuer as of some date | 值域：货币数量；子属性：具有货币数量 |
| **具有流通股数（hasSharesOutstanding）** | — | — |
| **适用于（appliesTo）** | — | — |
| **具有观测日期时间（hasObservedDateTime）** | — | — |
| **具有自变量（hasArgument）** | — | — |

公理：

- **具有市值金额（has market capitalization value）**至少有一个取值，类型是**货币数量（MonetaryAmount）**。
- **具有流通股数（hasSharesOutstanding）**至少有一个取值，类型是**xsd:nonNegativeInteger（nonNegativeInteger）**。
- **具有自变量（hasArgument）**至少有一个取值，类型是**每股价格（PricePerShare）**。
- **具有观测日期时间（hasObservedDateTime）**至少有一个取值，类型是**cmns-dt:CombinedDateTime（CombinedDateTime）**。
- **适用于（appliesTo）**至少有一个取值，类型是**股份发行人（ShareIssuer）**。

### 2.6 参考指数（reference index）

定义：篮子内容在给定时期内价值变化的度量。

- 父类：**限定范围度量（ScopedMeasure）**
- 直接子类：**信用指数（credit index）**、**股票指数（equity index）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **基于（isBasedOn）** | — | — |
| **具有报告期（hasReportingPeriod）** | — | — |
| **具有周期性（hasPeriodicity）** | — | — |
| **具有发布日期（hasReleaseDate）** | — | — |
| **具有发布日期时间（hasReleaseDateTime）** | — | — |
| **具有指数名称（has index name）** | 指明该指数的正式名称。<br>specifies a formal name for the index | 值域：xsd:string；子属性：具有正式名称 |
| **由……分类（isClassifiedBy）** | — | — |

公理：

- **具有发布日期时间（hasReleaseDateTime）**存在取值约束。
- **具有发布日期（hasReleaseDate）**可以有 0 个或多个**日期（Date）**。
- **具有周期性（hasPeriodicity）**的所有取值只能是**重复区间（RecurrenceInterval）**。
- **具有报告期（hasReportingPeriod）**恰好有 1 个**显式日期区间（ExplicitDatePeriod）**。
- **基于（isBasedOn）**至少有一个取值，类型是**加权篮子（WeightedBasket）**。
- **由……分类（isClassifiedBy）**可以有 0 个或多个**行业部门分类器（IndustrySectorClassifier）**。
- **由……分类（isClassifiedBy）**可以有 0 个或多个**资产类别（AssetClass）**。

#### 2.6.1 信用指数（credit index）

定义：以改变标的组合价值的信用事件为函数的参考指数。

- 父类：**参考指数（reference index）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **基于（isBasedOn）** | — | — |
| **具有原始名义价值（has original notional value）** | 标识该指数最初构成时所代表的名义金额。<br>indicates the notional amount represented by the index when it is first constituted | 值域：货币数量；子属性：具有名义金额 |
| **具有权利金（has premium）** | 标识基于该指数的合同应付的权利金。<br>indicates a premium payable for a contract based on the index | 值域：货币数量；子属性：具有货币数量 |
| **具有利差区间（has spread range）** | 指数各成分的信用利差区间。<br>the range of credit spread for the constituents of the index | 值域：xsd:string |
| **具有预付费用（has up front fee）** | 指明任何希望在合同开始后参与基于该指数之合同的参与方应付的费用。<br>specifies a fee payable by any party that wishes to participate in a contract based on the index after the start of its life | 值域：货币数量 |

公理：

- **基于（isBasedOn）**至少有一个取值，类型是**信用风险篮子（basket of credit risks）**。

#### 2.6.2 股票指数（equity index）

定义：成分全部为股票工具的基准指数。

- 父类：**参考指数（reference index）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **基于（isBasedOn）** | — | — |

公理：

- **基于（isBasedOn）**至少有一个取值，类型是**股票篮子（basket of equities）**。

## 3. 其他属性

以下属性未绑定到本体的具体类（定义域在外部本体或未声明）：

数据属性（Datatype Property）：

| 属性 | 定义 |
|---|---|
| **具有指数值（has index value）** | 指明给定指数在发布日的值。<br>specifies the value of a given index as of the release date |

## 4. 依赖（owl:imports，21 个）

本本体通过 `owl:imports` 引入以下本体，各项的中文名称与简介如下：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `FBC/DebtAndEquities/CreditEvents.rdf` | 信用事件本体（Credit Events Ontology） | 定义信用事件（credit event）：破产、拒付、重组等会触发信用衍生品结算的事件类型。 |
| `FBC/DebtAndEquities/Debt.rdf` | 债务本体（Debt Ontology） | 定义债务（debt）与债权债务关系的核心概念：借款人、贷款人、本金与利息义务。 |
| `FBC/ProductsAndServices/FinancialProductsAndServices.rdf` | 金融产品与服务本体（Financial Products and Services Ontology） | 定义金融产品（financial product）与金融服务（financial service）及其提供、购买关系。 |
| `FND/Accounting/CurrencyAmount.rdf` | 货币金额本体（Currency Amount Ontology） | 定义「金额＋币种」的货币金额（currency amount）表示，是 FIBO 中表达价格、债务金额、付款额等一切带币种数值的基础构件。 |
| `FND/Agreements/Contracts.rdf` | 合同本体（Contracts Ontology） | 在协议之上定义具有法律约束力的合同（contract）：合同当事方、合同条款、义务与权利，是金融工具与交易合同建模的基石。 |
| `FND/Arrangements/ClassificationSchemes.rdf` | 分类方案本体（Classification Schemes Ontology） | 定义分类方案（classification scheme）、类别及「将事物归入类别」的关系，支撑证券分类、行业分类等具体分类体系。 |
| `FND/Arrangements/Documents.rdf` | 文档本体（Documents Ontology） | 定义文档、文档类型及文档与其所记载内容的关系，为合同文本、募集说明书等法律文书建模。 |
| `FND/DatesAndTimes/FinancialDates.rdf` | 金融日期本体（Financial Dates Ontology） | 定义金融语境下的日期与期间概念：结算日、付息日、到期日、日计数基准等。 |
| `FND/Relations/Relations.rdf` | 关系本体（Relations Ontology） | FIBO 最底层的基础本体，定义参考（reference）、分类（classify）等通用关系与抽象概念，全库普遍依赖。 |
| `FND/Utilities/Analytics.rdf` | 分析本体（Analytics Ontology） | 定义分析工具、度量与比率的通用概念，支撑指标与模型的表达。 |
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `SEC/Equities/EquityInstruments.rdf` | 股权工具本体（Equity Instruments Ontology） | 定义股票等股权工具：普通股、优先股及其附带的权利。 |
| `SEC/Securities/Baskets.rdf` | 篮子本体（Baskets Ontology） | 定义证券篮子（basket）：作为整体交易或定价的一组证券。 |
| `SEC/Securities/SecuritiesClassification.rdf` | 证券分类本体（Securities Classification Ontology） | 定义证券分类方案：按 CFI 代码、按资产类别等对证券归类。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |
| `https://www.omg.org/spec/Commons/Classifiers/` | OMG 通用分类器本体（OMG Commons Classifiers） | OMG 通用本体库（Commons）中的分类器本体，定义分类方案、类别与归类关系的通用概念，FIBO 的分类建模建立在其上。 |
| `https://www.omg.org/spec/Commons/Collections/` | OMG 通用集合本体（OMG Commons Collections） | Commons 库中的集合本体，定义集合、成员等通用概念。 |
| `https://www.omg.org/spec/Commons/ContextualDesignators/` | OMG 通用语境指称本体（OMG Commons Contextual Designators） | Commons 库中的语境指称本体，定义「在某个语境下指代某物的名称/符号」，是地址、账户号码等语境相关标识的基础。 |
| `https://www.omg.org/spec/Commons/DatesAndTimes/` | OMG 通用日期与时间本体（OMG Commons Dates and Times） | Commons 库中的日期时间本体，定义日期、期间、时间点等通用时间概念。 |
| `https://www.omg.org/spec/Commons/Documents/` | OMG 通用文档本体（OMG Commons Documents） | Commons 库中的文档本体，定义文档及其组成部分的通用概念。 |
| `https://www.omg.org/spec/Commons/QuantitiesAndUnits/` | OMG 通用量与单位本体（OMG Commons Quantities and Units） | Commons 库中的量与单位本体，定义数量、度量单位、量纲的通用概念，支撑金额、比率等数值表达。 |

## 5. 文件

- 官方 RDF/XML：`BasketIndices.rdf`
- 中文 Turtle：`BasketIndices.ttl`
- 结构图：`BasketIndices-structure.png` / `BasketIndices-structure.svg`