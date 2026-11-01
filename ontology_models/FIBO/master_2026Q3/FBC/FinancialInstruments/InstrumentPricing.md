# 工具定价本体（Instrument Pricing Ontology）结构与公理说明

本文档对应 `InstrumentPricing.rdf` / `InstrumentPricing.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `InstrumentPricing-structure.png`（`InstrumentPricing-structure.svg` 为可缩放版本）。

![工具定价本体（Instrument Pricing Ontology）本体结构图](InstrumentPricing-structure.png)

## 1. 本体概述

定义金融工具的价格（price）、报价（quote）与估值（valuation）相关概念。

**在体系中的位置**：FBC 金融工具模块的配套本体，与结算本体并列。

**上下游关系**：上游依赖金融工具、货币金额与 IND 指标本体；下游被 MD 市场数据各时序本体引用（时序数据就是价格的历史记录）。

**与相近概念的差别**：价格≠价值——价格是市场成交或报价的数值，估值是模型推算的理论价值；本本体两者都覆盖但侧重市场报价结构。

本本体中类与类的核心关系如下（完整细节见各类小节）：

- **调整后收盘价（adjusted closing price）** 继承 **收盘价（closing price）**
- **最优买价（best bid）** 继承 **买价（bid price）**
- **最优卖价（best offer）** 继承 **卖价（offer price）**
- **买卖价差（bid ask spread）** 继承 **价格差（price spread）**
- **买价（bid price）** 继承 **证券价格（security price）**
- **净价（clean price）** 继承 **证券价格（security price）**
- **收盘价（closing price）** 继承 **市场价格（market price）**
- **收盘价确定方法（closing price determination method）** 继承 **价格确定方法（price determination method）**
- **证券价格集合（collection of security prices）** 继承 **带日期结构化集合（DatedStructuredCollection）**
- **综合市场（composite market）** 继承 **结构化集合（StructuredCollection）**
- **衍生价格（derived price）** 继承 **证券价格（security price）**
- **衍生价格（derived price）** 继承 **计算价格（CalculatedPrice）**
- 其余 23 条关系从略。

## 2. 类（Class）

| 类（Class） | 定义（Definition） |
|---|---|
| 调整后收盘价（adjusted closing price） | 在计入拆股、分红、配股等公司行为后，经修正以反映证券价值的收盘价。 |
| 最优买价（best bid） | 潜在买方在特定时点就某一证券愿意支付的最高买入价。 |
| 最优卖价（best offer） | 潜在卖方在特定时点就某一证券可接受的最低卖出价。 |
| 买卖价差（bid ask spread） | 卖出（要价）与买入（出价）之间的差额。 |
| 买价（bid price） | 潜在买方愿意支付的价格。 |
| 净价（clean price） | 不含应计利息的债务工具价格。 |
| 收盘价（closing price） | 市场收盘前最后一笔成交价格的现金价值。 |
| 收盘价确定方法（closing price determination method） | 计算或以其他方式确定官方收盘价的策略。 |
| 证券价格集合（collection of security prices） | 由一系列价格组成的集合，每一价格均与特定日期和时间相关联。 |
| 综合市场（composite market） | 为定价目的而参考的一组交易所和交易场所。 |
| 衍生价格（derived price） | 来源于其他数据源或计算、而非报价或基于实际交易数据的价格。 |
| 全价（dirty price） | 含应计利息的债务工具价格。 |
| 最高价（high price） | 指定期间内某一证券的最高价格。 |
| 内部收益率（internal rate of return） | 使一系列未来现金流净现值（NPV）为零的折现率。 |
| 盘中价格（intra day price） | 交易所开盘价与官方收盘价之间某一时点的证券价格。 |
| 最低价（low price） | 指定期间内某一证券的最低价格。 |
| 市场价格（market price） | 证券最近一次成交的报告价格。 |
| 中间价（mid price） | 买价与卖价的算术平均值。 |
| 卖价（offer price） | 潜在卖方在特定时点就某一证券提出的价格。 |
| 官方收盘价（official closing price） | 某一交易所交易日结束时证券最后一笔成交的价格。 |
| 开盘价（opening price） | 交易日开始时的首次成交价格。 |
| 价格分析指标（price analytic） | 涉及证券价格的统计度量。 |
| 价格确定方法（price determination method） | 计算或以其他方式确立某物价格的策略。 |
| 价格差（price spread） | 两个价格之间的差额。 |
| 定价模型（pricing model） | 用于确定工具在某一时点价值的表达式。 |
| 收益率（rate of return） | 投资在规定期间内的净收益或净损失，以占投资初始成本或某一时点价值的百分比表示。 |
| 证券价格（security price） | 金融工具在某一时点的货币价格。 |
| 交易日（trading day） | 某一交易场所开放的时间跨度。 |
| 交易时段（trading session） | 交易日内可以提交并成交订单的时间窗口。 |
| 成交量加权平均价（volume-weighted average price） | 证券在全日交易中的平均价格，由每笔成交价格乘以其成交量后加总，再除以总成交量得出。 |
| 成交量加权开盘价（volume-weighted open price） | 由每笔成交价格乘以其成交量后加总，再除以交易日内某一期间的成交量得出的价格。 |
| 收益率（yield） | 投资人资本投资的回报。 |
| 收益率差（yield spread） | 两个项目收益率之间的差值。 |

以下按类逐个展开：每个类给出继承关系、相关属性与公理约定；子类在父类之下降一级编号。

### 2.1 证券价格集合（collection of security prices）

定义：由一系列价格组成的集合，每一价格均与特定日期和时间相关联。

- 父类：**带日期结构化集合（DatedStructuredCollection）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有成员（hasMember）** | — | — |

公理：

- **具有成员（hasMember）**至少有一个取值，类型是**证券价格（security price）**。

### 2.2 综合市场（composite market）

定义：为定价目的而参考的一组交易所和交易场所。

- 父类：**结构化集合（StructuredCollection）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有成员（hasMember）** | — | — |

公理：

- **具有成员（hasMember）**至少有一个取值，类型是**交易所（Exchange）**。

### 2.3 价格分析指标（price analytic）

定义：涉及证券价格的统计度量。

- 父类：**限定范围度量（ScopedMeasure）**
- 直接子类：**成交量加权平均价（volume-weighted average price）**、**成交量加权开盘价（volume-weighted open price）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **适用于（appliesTo）** | — | — |
| **具有适用期间（hasApplicablePeriod）** | — | — |
| **引用（refersTo）** | — | — |

公理：

- **具有适用期间（hasApplicablePeriod）**至少有一个取值，类型是**日期区间（DatePeriod）**。
- **引用（refersTo）**至少有一个取值，类型是**证券（Security）**。
- **适用于（appliesTo）**至少有一个取值，类型是**证券价格集合（collection of security prices）**。

#### 2.3.1 成交量加权平均价（volume-weighted average price）

定义：证券在全日交易中的平均价格，由每笔成交价格乘以其成交量后加总，再除以总成交量得出。

- 父类：**价格分析指标（price analytic）**

#### 2.3.2 成交量加权开盘价（volume-weighted open price）

定义：由每笔成交价格乘以其成交量后加总，再除以交易日内某一期间的成交量得出的价格。

- 父类：**价格分析指标（price analytic）**

### 2.4 价格确定方法（price determination method）

定义：计算或以其他方式确立某物价格的策略。

- 父类：**战略（Strategy）**
- 直接子类：**收盘价确定方法（closing price determination method）**

#### 2.4.1 收盘价确定方法（closing price determination method）

定义：计算或以其他方式确定官方收盘价的策略。

- 父类：**价格确定方法（price determination method）**

### 2.5 价格差（price spread）

定义：两个价格之间的差额。

- 父类：**差（Difference）**
- 直接子类：**买卖价差（bid ask spread）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有适用期间（hasApplicablePeriod）** | — | — |
| **具有自变量（hasArgument）** | — | — |

公理：

- **具有自变量（hasArgument）**恰好有 2 个**货币价格（MonetaryPrice）**。
- **具有适用期间（hasApplicablePeriod）**至少有一个取值，类型是**日期区间（DatePeriod）**。

#### 2.5.1 买卖价差（bid ask spread）

定义：卖出（要价）与买入（出价）之间的差额。

- 父类：**价格差（price spread）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有自变量（hasArgument）** | — | — |

公理：

- **具有自变量（hasArgument）**至少有一个取值，类型是**买价（bid price）**。
- **具有自变量（hasArgument）**至少有一个取值，类型是**卖价（offer price）**。

### 2.6 定价模型（pricing model）

定义：用于确定工具在某一时点价值的表达式。

- 父类：**表达式（Expression）**

### 2.7 收益率（rate of return）

定义：投资在规定期间内的净收益或净损失，以占投资初始成本或某一时点价值的百分比表示。

- 父类：**百分比（Percentage）**
- 直接子类：**内部收益率（internal rate of return）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有适用期间（hasApplicablePeriod）** | — | — |
| **引用（refersTo）** | — | — |

公理：

- **具有适用期间（hasApplicablePeriod）**至少有一个取值，类型是**日期区间（DatePeriod）**。
- **引用（refersTo）**至少有一个取值，类型是**证券（Security）**。

#### 2.7.1 内部收益率（internal rate of return）

定义：使一系列未来现金流净现值（NPV）为零的折现率。

- 父类：**收益率（rate of return）**

### 2.8 证券价格（security price）

定义：金融工具在某一时点的货币价格。

- 父类：**货币价格（MonetaryPrice）**
- 直接子类：**买价（bid price）**、**净价（clean price）**、**衍生价格（derived price）**、**全价（dirty price）**、**最高价（high price）**、**最低价（low price）**、**市场价格（market price）**、**中间价（mid price）**、**卖价（offer price）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有盘口深度（has book depth）** | 指明价格所对应的订单簿深度。 | 值域：xsd:integer |
| **具有定价来源（has pricing source）** | 指明金融工具某一报价或价格的来源。 | 子属性：引用 |
| **具有报价批量规模（has quote lot size）** | 报价所对应标的的规模。 | 值域：xsd:decimal；子属性：具有批量规模（has lot size） |
| **具有交易日期时间（has trading date time）** | 指明与某一价格相关联的具体日期和时间。 | 值域：日期时间；子属性：具有日期时间 |
| **是……的价格（isPriceFor）** | — | — |
| **具有观测日期时间（hasObservedDateTime）** | — | — |

公理：

- **具有定价来源（has pricing source）**可以有 0 个或多个**N68d8e5bde4da4ec49b0a7fc8421752b3**。
- **具有观测日期时间（hasObservedDateTime）**存在取值约束。
- **是……的价格（isPriceFor）**至少有一个取值，类型是**证券（Security）**。

#### 2.8.1 买价（bid price）

定义：潜在买方愿意支付的价格。

- 父类：**证券价格（security price）**
- 直接子类：**最优买价（best bid）**

公理：

- 与**卖价（offer price）**互斥：同一个体不能同时属于两者。

##### 2.8.1.1 最优买价（best bid）

定义：潜在买方在特定时点就某一证券愿意支付的最高买入价。

- 父类：**买价（bid price）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有适用期间（hasApplicablePeriod）** | — | — |

公理：

- **具有适用期间（hasApplicablePeriod）**至少有一个取值，类型是**日期区间（DatePeriod）**。

#### 2.8.2 净价（clean price）

定义：不含应计利息的债务工具价格。

- 父类：**证券价格（security price）**

公理：

- 与**全价（dirty price）**互斥：同一个体不能同时属于两者。

#### 2.8.3 衍生价格（derived price）

定义：来源于其他数据源或计算、而非报价或基于实际交易数据的价格。

- 父类：**证券价格（security price）**、**计算价格（CalculatedPrice）**

#### 2.8.4 全价（dirty price）

定义：含应计利息的债务工具价格。

- 父类：**证券价格（security price）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **包含（comprises）** | — | — |

公理：

- **包含（comprises）**至少有一个取值，类型是**应计利息（AccruedInterest）**。

#### 2.8.5 最高价（high price）

定义：指定期间内某一证券的最高价格。

- 父类：**证券价格（security price）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有适用期间（hasApplicablePeriod）** | — | — |

公理：

- **具有适用期间（hasApplicablePeriod）**至少有一个取值，类型是**日期区间（DatePeriod）**。

#### 2.8.6 最低价（low price）

定义：指定期间内某一证券的最低价格。

- 父类：**证券价格（security price）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有适用期间（hasApplicablePeriod）** | — | — |

公理：

- **具有适用期间（hasApplicablePeriod）**至少有一个取值，类型是**日期区间（DatePeriod）**。

#### 2.8.7 市场价格（market price）

定义：证券最近一次成交的报告价格。

- 父类：**证券价格（security price）**
- 直接子类：**收盘价（closing price）**、**盘中价格（intra day price）**、**开盘价（opening price）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有定价来源（has pricing source）** | 指明金融工具某一报价或价格的来源。 | 子属性：引用 |

公理：

- **具有定价来源（has pricing source）**至少有一个取值，该取值满足：该属性存在取值约束。

##### 2.8.7.1 收盘价（closing price）

定义：市场收盘前最后一笔成交价格的现金价值。

- 父类：**市场价格（market price）**
- 直接子类：**调整后收盘价（adjusted closing price）**、**官方收盘价（official closing price）**

###### 2.8.7.1.1 调整后收盘价（adjusted closing price）

定义：在计入拆股、分红、配股等公司行为后，经修正以反映证券价值的收盘价。

- 父类：**收盘价（closing price）**

###### 2.8.7.1.2 官方收盘价（official closing price）

定义：某一交易所交易日结束时证券最后一笔成交的价格。

- 父类：**收盘价（closing price）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有收盘价确定方法（has closing price determination method）** | 指明确定官方收盘价所采用的策略。 | 值域：收盘价确定方法（closing price determination method）；子属性：具有价格确定方法（has price determination method） |

公理：

- **具有收盘价确定方法（has closing price determination method）**至少有一个取值，类型是**收盘价确定方法（closing price determination method）**。

##### 2.8.7.2 盘中价格（intra day price）

定义：交易所开盘价与官方收盘价之间某一时点的证券价格。

- 父类：**市场价格（market price）**

##### 2.8.7.3 开盘价（opening price）

定义：交易日开始时的首次成交价格。

- 父类：**市场价格（market price）**

#### 2.8.8 中间价（mid price）

定义：买价与卖价的算术平均值。

- 父类：**证券价格（security price）**、**算术平均值（ArithmeticMean）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有货币（hasCurrency）** | — | — |
| **具有适用期间（hasApplicablePeriod）** | — | — |
| **具有自变量（hasArgument）** | — | — |

公理：

- **具有自变量（hasArgument）**至少有一个取值，类型是**买价（bid price）**。
- **具有自变量（hasArgument）**至少有一个取值，类型是**卖价（offer price）**。
- **具有货币（hasCurrency）**恰好有 1 个**货币（Currency）**。
- **具有适用期间（hasApplicablePeriod）**至少有一个取值，类型是**日期区间（DatePeriod）**。

#### 2.8.9 卖价（offer price）

定义：潜在卖方在特定时点就某一证券提出的价格。

- 父类：**证券价格（security price）**
- 直接子类：**最优卖价（best offer）**

##### 2.8.9.1 最优卖价（best offer）

定义：潜在卖方在特定时点就某一证券可接受的最低卖出价。

- 父类：**卖价（offer price）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有适用期间（hasApplicablePeriod）** | — | — |

公理：

- **具有适用期间（hasApplicablePeriod）**至少有一个取值，类型是**日期区间（DatePeriod）**。

### 2.9 交易日（trading day）

定义：某一交易场所开放的时间跨度。

- 父类：**显式日期区间（ExplicitDatePeriod）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有截止日时间（hasClosingDateTime）** | — | — |
| **具有开启日时间（hasOpeningDateTime）** | — | — |
| **具有时长（hasDuration）** | — | — |

公理：

- **具有开启日时间（hasOpeningDateTime）**存在取值约束。
- **具有截止日时间（hasClosingDateTime）**存在取值约束。
- **具有时长（hasDuration）**的取值固定为 Day。

### 2.10 交易时段（trading session）

定义：交易日内可以提交并成交订单的时间窗口。

- 父类：**显式日期区间（ExplicitDatePeriod）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有截止日时间（hasClosingDateTime）** | — | — |
| **具有开启日时间（hasOpeningDateTime）** | — | — |

公理：

- **具有开启日时间（hasOpeningDateTime）**存在取值约束。
- **具有截止日时间（hasClosingDateTime）**存在取值约束。

### 2.11 收益率（yield）

定义：投资人资本投资的回报。

- 父类：**百分比（Percentage）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有货币（hasCurrency）** | — | — |
| **具有适用期间（hasApplicablePeriod）** | — | — |
| **引用（refersTo）** | — | — |

公理：

- **具有货币（hasCurrency）**恰好有 1 个**货币（Currency）**。
- **具有适用期间（hasApplicablePeriod）**至少有一个取值，类型是**日期区间（DatePeriod）**。
- **引用（refersTo）**至少有一个取值，类型是**证券（Security）**。

### 2.12 收益率差（yield spread）

定义：两个项目收益率之间的差值。

- 父类：**差（Difference）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有自变量（hasArgument）** | — | — |

公理：

- **具有自变量（hasArgument）**恰好有 2 个**收益率（yield）**。

## 3. 其他属性

以下属性未绑定到本体的具体类（定义域在外部本体或未声明）：

对象属性（Object Property）：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有价格确定方法（has price determination method）** | 指明确定某一价格所采用的策略。 | 值域：价格确定方法（price determination method）；子属性：具有战略 |
| **具有收益率（has rate of return）** | 指明某一金融工具在一段时间内的回顾性收益率。 | 值域：收益率（rate of return）；子属性：具有量值 |

数据属性（Datatype Property）：

| 属性 | 定义 |
|---|---|
| **具有批量规模（has lot size）** | 项目的规模（即总数量）。 |
| **具有应计天数（has number of days accrued）** | 指明利息已计提但尚未收到的天数。 |
| **具有整手规模（has round lot size）** | 交易所证券交易的标准手数。 |
| **具有成交量（has trading volume）** | 指明某一交易日成交的股份/单位数量。 |

## 4. 依赖（owl:imports，17 个）

本本体通过 `owl:imports` 引入以下本体，各项的中文名称与简介如下：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `BE/FunctionalEntities/Publishers.rdf` | 出版方本体（Publishers Ontology） | 定义出版方及其出版物，用于标识金融信息与文档的发布来源。 |
| `FBC/DebtAndEquities/Debt.rdf` | 债务本体（Debt Ontology） | 定义债务（debt）与债权债务关系的核心概念：借款人、贷款人、本金与利息义务。 |
| `FBC/FinancialInstruments/FinancialInstruments.rdf` | 金融工具本体（Financial Instruments Ontology） | FIBO 核心本体之一，定义金融工具（financial instrument）的通用概念：可交易、代表某种权利义务的合同工具，是证券、衍生品等具体工具的共同基础。 |
| `FBC/FunctionalEntities/Markets.rdf` | 市场本体（Markets Ontology） | 定义金融市场（market）：交易所、场外市场及其功能。 |
| `FBC/ProductsAndServices/FinancialProductsAndServices.rdf` | 金融产品与服务本体（Financial Products and Services Ontology） | 定义金融产品（financial product）与金融服务（financial service）及其提供、购买关系。 |
| `FND/Accounting/CurrencyAmount.rdf` | 货币金额本体（Currency Amount Ontology） | 定义「金额＋币种」的货币金额（currency amount）表示，是 FIBO 中表达价格、债务金额、付款额等一切带币种数值的基础构件。 |
| `FND/DatesAndTimes/FinancialDates.rdf` | 金融日期本体（Financial Dates Ontology） | 定义金融语境下的日期与期间概念：结算日、付息日、到期日、日计数基准等。 |
| `FND/GoalsAndObjectives/Objectives.rdf` | 目标本体（Objectives Ontology） | 定义目标（objective）及其与组织、计划的关系，用于表达机构的经营目标与投资目标。 |
| `FND/OwnershipAndControl/Ownership.rdf` | 所有权本体（Ownership Ontology） | 定义「拥有」关系：所有者、被拥有资产及所有权份额。 |
| `FND/Utilities/Analytics.rdf` | 分析本体（Analytics Ontology） | 定义分析工具、度量与比率的通用概念，支撑指标与模型的表达。 |
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |
| `https://www.omg.org/spec/Commons/Collections/` | OMG 通用集合本体（OMG Commons Collections） | Commons 库中的集合本体，定义集合、成员等通用概念。 |
| `https://www.omg.org/spec/Commons/ContextualDesignators/` | OMG 通用语境指称本体（OMG Commons Contextual Designators） | Commons 库中的语境指称本体，定义「在某个语境下指代某物的名称/符号」，是地址、账户号码等语境相关标识的基础。 |
| `https://www.omg.org/spec/Commons/DatesAndTimes/` | OMG 通用日期与时间本体（OMG Commons Dates and Times） | Commons 库中的日期时间本体，定义日期、期间、时间点等通用时间概念。 |
| `https://www.omg.org/spec/Commons/Documents/` | OMG 通用文档本体（OMG Commons Documents） | Commons 库中的文档本体，定义文档及其组成部分的通用概念。 |
| `https://www.omg.org/spec/Commons/QuantitiesAndUnits/` | OMG 通用量与单位本体（OMG Commons Quantities and Units） | Commons 库中的量与单位本体，定义数量、度量单位、量纲的通用概念，支撑金额、比率等数值表达。 |

## 5. 文件

- 官方 RDF/XML：`InstrumentPricing.rdf`
- 中文 Turtle：`InstrumentPricing.ttl`
- 结构图：`InstrumentPricing-structure.png` / `InstrumentPricing-structure.svg`