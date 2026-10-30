# 债务分析本体（Debt Analytics Ontology）结构与公理说明

本文档对应 `DebtAnalytics.rdf` / `DebtAnalytics.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `DebtAnalytics-structure.png`（`DebtAnalytics-structure.svg` 为可缩放版本）。

![债务分析本体（Debt Analytics Ontology）本体结构图](DebtAnalytics-structure.png)

## 1. 本体概述

定义债务工具分析指标及其时间序列：收益率（yield）、利差（spread）、久期（duration）等随时间的变化。

**在体系中的位置**：MD 债务时序模块的核心，把债券分析从「单点数值」扩展为「历史轨迹」。

**上下游关系**：上游依赖 SEC 债务工具、IND 利率与 FND 分析本体；下游服务固收分析与风险建模。

**与相近概念的差别**：收益率≠利率——利率是合同约定的付息水平，收益率是按市场价格推算的回报度量；分析指标≠行情价格——指标是从价格与条款推算的派生量。

## 2. 类（Class）

| 类（Class） | 定义（Definition） |
|---|---|
| 麦考利久期分析（MacCaulays Duration Analytic） | 麦考利久期的分析度量。 |
| 债券等价收益率（bond equivalent yield） | 按与另一债券收益率等价基准确定的收益率，用于真实比较不同债务工具的价格。 |
| 信用利差（credit spread） | 反映投资者从信用风险较高的证券相对信用风险较低证券所能获得的额外净收益的收益率利差。 |
| 当期收益率计算法（current yield calculation method） | 利息支付额与净价之比。 |
| 债务凸性分析（debt convexity analytic） | 证券价格对其收益率的二阶导数除以证券价格；当价格上升幅度大于收益率下降所暗示的幅度时呈正凸性。 |
| 债务工具收益率（debt instrument yield） | 按所述价格计算的债务工具回报。 |
| 债务价格利差（debt price spread） | 某证券价格与作为参照的另一证券公允价值之差，用于定价比较。 |
| 债务证券做市商（debt securities market maker） | 在给定市场中担任做市商角色的参与者。 |
| 平均期限收益率（debt yield to average life） | 以债券平均期限替代最终到期日计算所得的收益率。 |
| 等价期限收益率（debt yield to equivalent life） | 以债券等价期限替代最终到期日计算所得的收益率。 |
| 到期收益率（debt yield to maturity） | 投资者以当前全价购入债券并持有至到期（假设所有票息按该收益率再投资）可获得的内部收益率。 |
| 至下一赎回日收益率（debt yield to next call） | 债券到下一个可能赎回日的收益率。 |
| 最差收益率（debt yield to worst） | 按该工具可能被赎回的最坏情形计算的收益率。 |
| 贴现工具收益率（discounted instrument yield） | 贴现工具的报价收益率：贴现额与面值之比，再除以以年计（不足一年按分数计）的到期期限。 |
| 久期分析（duration analytic） | 收到全部付款的加权平均时间。 |
| 有效久期（effective duration） | 考虑现金流随利率变化而调整的久期度量。 |
| 有效收益率（effective yield） | 考虑复利影响的实际收益率。 |
| 等价期限分析（equivalent life analytic） | 等价期限的分析度量。 |
| 等价收益率计算法（equivalent yield calculation method） | 按等价基准计算收益率的方法。 |
| 交易所交易债券价格（exchange traded bond price） | 在交易所交易的债券的价格。 |
| FFIEC 降 300 提前偿付速度（f f i e c down 300 prepay speed） | 「降 300」情景下用于基础抵押品现金流计算的公共证券协会（PSA）速度。 |
| FFIEC 升 300 提前偿付速度（f f i e c up 300 prepay speed） | 「升 300」情景下用于基础抵押品现金流计算的公共证券协会（PSA）速度。 |
| ICMA 收益率公式（i c m a yield formula） | 国际资本市场协会（ICMA，原 ISMA）规定的固定利率债券收益率确定方法。 |
| 隐含远期利率（implied forward rate） | 由即期利率结构隐含的远期利率。 |
| 内部确定价格利差（internally determined price spread） | 组织内部根据自有交易台可得信息确定的利差。 |
| 日本复利收益率计算法（japanese compound yield calculation method） | 日本市场使用的复利收益率计算方法。 |
| 日本单利收益率计算法（japanese simple yield calculation method） | 日本市场使用的单利收益率计算方法。 |
| 关键利率久期（key rate duration） | 证券价格对特定期限利率变化的敏感度度量。 |
| 期限分析（life analytic） | 对证券期限的某种度量，而非实际到期时间本身；为基于适当参数计算的导出数值。 |
| 贷款池提前偿付模型（loan pool prepayment model） | 个贷池（如抵押贷款池或贷款池）中贷款提前偿付的模型。 |
| 贷款提前偿付公式（loan prepayment formula） | 体现贷款池提前偿付速度模型的公式。 |
| 到期等价 PSA（maturity equivalent p s a） | 产生与 CMO、ABS 或 MBS 所计算平均期限相同之平均期限的提前偿付速度。 |
| 修正久期分析（modified duration analytic） | 给定收益率变化下证券价格的百分比变化；修正久期越高，风险越高。 |
| 本地收益率（native yield） | 按该证券交易市场的默认收益率计算方法确定的证券收益率。 |
| 本地收益率计算法（native yield calculation method） | 该证券市场通行的计算方法惯例。 |
| 下一赎回（next call） | 截至当前时点该次发行的下一次赎回。 |
| 下一赎回日（next call date） | 自当前日期起该次发行可被赎回的下一日期。 |
| 下一回售（next put） | 截至当前时点该次发行的下一个可回售日。 |
| 场外债券市场价（o t c bond market price） | 场外交易债券的市场价格。 |
| 期权调整收益率（option adjusted yield） | 以利差形式表示、基于不同利率路径计算的期权调整收益率（OAS）。 |
| 部分赎回估计模型（partial calls estimation model） | 估计提前部分赎回的模型。 |
| 池因子（pool factor） | 原始池中仍未清偿的比例，为小于 1 的数，以百分比表示。 |
| 池清偿速度（pool paydown rate） | 池清偿的速度，基于观测因子（CPR、SMM 等），不同证券计量方式不同。 |
| 基点价格值（price value of basis point） | 收益率变动一个基点时价格的敏感度，定义为收益率变动 1 个基点时的价格差。 |
| 相对收益率计算法（relative yield calculation method） | 以相对基准计算收益率的方法。 |
| 相对定义的债务工具收益率（relatively defined debt instrument yield） | 以相对基准定义的债务工具收益率。 |
| 俄罗斯收益率计算法（russian yield calculation method） | 俄罗斯市场用于确定收益率的方法，基于数学基础不同的有效收益率。 |
| 俄罗斯收益率公式（russian yield formula） | 基于与其他市场不同之有效收益率的收益率公式。 |
| 简单收益率计算法（simple yield calculation method） | 以百分比表示的年回报率：回报除以投入再乘以 100。 |
| 西班牙收益率计算法（spanish yield calculation method） | 西班牙公司债市场用于确定年收益率的方法。 |
| 美国公司债收益率计算法（u s corporate bond yield calculation method） | 采用 30/360 计息惯例和半年复利的收益率计算方法。 |
| 美国国债收益率计算法（u s treasury yield calculation method） | 美国国债市场使用的收益率计算方法。 |
| 华尔街收益率计算法（wall street yield calculation method） | 华尔街通行的收益率计算方法。 |
| 现金流收取加权平均时间（weighted average time to receipt of cashflows） | 某工具现金流收取的加权平均时间。 |
| 最差赎回（worst call） | 就工具可能被赎回的时间而言代表最坏情形的赎回事件。 |
| 收益率计算公式（yield calculation formula） | 用于确定收益率的公式。 |
| 收益率计算方法（yield calculation method） | 计算收益率的方法，包括计算公式及特定的天数计算惯例与复利方式。 |
| 至下一回售日收益率（yield to next put） | 到下一个可回售日的收益率。 |

### 2.1 继承关系（Inheritance）

- 麦考利久期分析（MacCaulays Duration Analytic） ⊑ 久期分析（duration analytic）
- 债券等价收益率（bond equivalent yield） ⊑ 相对定义的债务工具收益率（relatively defined debt instrument yield）
- 信用利差（credit spread） ⊑ 收益率差
- 当期收益率计算法（current yield calculation method） ⊑ 收益率计算方法（yield calculation method）
- 债务凸性分析（debt convexity analytic） ⊑ 带日期集合成分
- 债务工具收益率（debt instrument yield） ⊑ 收益率
- 债务价格利差（debt price spread） ⊑ 市场利差
- 债务证券做市商（debt securities market maker） ⊑ 服务提供方
- 平均期限收益率（debt yield to average life） ⊑ 债务工具收益率（debt instrument yield）
- 等价期限收益率（debt yield to equivalent life） ⊑ 债务工具收益率（debt instrument yield）
- 到期收益率（debt yield to maturity） ⊑ 债务工具收益率（debt instrument yield）
- 至下一赎回日收益率（debt yield to next call） ⊑ 债务工具收益率（debt instrument yield）
- 最差收益率（debt yield to worst） ⊑ 债务工具收益率（debt instrument yield）
- 贴现工具收益率（discounted instrument yield） ⊑ 债务工具收益率（debt instrument yield）
- 久期分析（duration analytic） ⊑ 债务池统计度量
- 有效久期（effective duration） ⊑ 久期分析（duration analytic）
- 有效收益率（effective yield） ⊑ 债务工具收益率（debt instrument yield）
- 等价期限分析（equivalent life analytic） ⊑ 期限分析（life analytic）
- 等价收益率计算法（equivalent yield calculation method） ⊑ 相对收益率计算法（relative yield calculation method）
- 交易所交易债券价格（exchange traded bond price） ⊑ 证券价格
- FFIEC 降 300 提前偿付速度（f f i e c down 300 prepay speed） ⊑ 提前偿付速度
- FFIEC 升 300 提前偿付速度（f f i e c up 300 prepay speed） ⊑ 提前偿付速度
- ICMA 收益率公式（i c m a yield formula） ⊑ 收益率计算公式（yield calculation formula）
- 隐含远期利率（implied forward rate） ⊑ 利率
- 内部确定价格利差（internally determined price spread） ⊑ 债务价格利差（debt price spread）
- 日本复利收益率计算法（japanese compound yield calculation method） ⊑ 收益率计算方法（yield calculation method）
- 日本单利收益率计算法（japanese simple yield calculation method） ⊑ 收益率计算方法（yield calculation method）
- 关键利率久期（key rate duration） ⊑ 久期分析（duration analytic）
- 期限分析（life analytic） ⊑ 债务池统计度量
- 贷款池提前偿付模型（loan pool prepayment model） ⊑ 公式
- 贷款提前偿付公式（loan prepayment formula） ⊑ 公式
- 到期等价 PSA（maturity equivalent p s a） ⊑ 提前偿付速度
- 修正久期分析（modified duration analytic） ⊑ 久期分析（duration analytic）
- 本地收益率（native yield） ⊑ 相对定义的债务工具收益率（relatively defined debt instrument yield）
- 本地收益率计算法（native yield calculation method） ⊑ 相对收益率计算法（relative yield calculation method）
- 下一赎回（next call） ⊑ 赎回事件
- 下一赎回日（next call date） ⊑ 日期
- 下一回售（next put） ⊑ 回售事件
- 场外债券市场价（o t c bond market price） ⊑ 证券价格
- 期权调整收益率（option adjusted yield） ⊑ 债务工具收益率（debt instrument yield）
- 部分赎回估计模型（partial calls estimation model） ⊑ 公式
- 池因子（pool factor） ⊑ 百分比
- 池清偿速度（pool paydown rate） ⊑ 比率
- 基点价格值（price value of basis point） ⊑ 债务池统计度量
- 相对收益率计算法（relative yield calculation method） ⊑ 收益率计算方法（yield calculation method）
- 相对定义的债务工具收益率（relatively defined debt instrument yield） ⊑ 债务工具收益率（debt instrument yield）
- 俄罗斯收益率计算法（russian yield calculation method） ⊑ 收益率计算方法（yield calculation method）
- 俄罗斯收益率公式（russian yield formula） ⊑ 收益率计算公式（yield calculation formula）
- 简单收益率计算法（simple yield calculation method） ⊑ 收益率计算方法（yield calculation method）
- 西班牙收益率计算法（spanish yield calculation method） ⊑ 收益率计算方法（yield calculation method）
- 美国公司债收益率计算法（u s corporate bond yield calculation method） ⊑ 收益率计算方法（yield calculation method）
- 美国国债收益率计算法（u s treasury yield calculation method） ⊑ 收益率计算方法（yield calculation method）
- 华尔街收益率计算法（wall street yield calculation method） ⊑ 收益率计算方法（yield calculation method）
- 现金流收取加权平均时间（weighted average time to receipt of cashflows） ⊑ 公式
- 最差赎回（worst call） ⊑ 赎回事件
- 收益率计算公式（yield calculation formula） ⊑ 公式
- 收益率计算方法（yield calculation method） ⊑ 公式
- 至下一回售日收益率（yield to next put） ⊑ 债务工具收益率（debt instrument yield）

## 3. 对象属性（Object Property）

| 属性（Property） | 中文（English） | 定义（Definition） | 说明 |
|---|---|---|---|
| fibo-md-dbtx-aly:calculationFollowing | 按……计算（calculation following） | 标识计算所遵循的方法或惯例。 | 定义域（domain）：债务工具收益率（debt instrument yield）；值域（range）：收益率计算方法（yield calculation method） |
| fibo-md-dbtx-aly:defaultRateValue | 默认利率值（default rate value） | 默认的利率值。 | 定义域（domain）：违约率；值域（range）：百分比 |
| fibo-md-dbtx-aly:determinesMarketPriceForDebt | 确定债务市场价（determines market price for debt） | 确定债务工具的市场价格。 | 定义域（domain）：债务证券做市商（debt securities market maker）；值域（range）：场外债券市场价（o t c bond market price） |
| fibo-md-dbtx-aly:equivalentLifeValue | 等价期限值（equivalent life value） | 所述日期的等价期限（以年计）。 | 定义域（domain）：等价期限分析（equivalent life analytic）；值域（range）：时长 |
| fibo-md-dbtx-aly:hasAnalytic | 具有分析度量（has analytic） | 标识某事物的分析度量。 | 定义域（domain）：债务池；值域（range）：债务池统计度量 |
| fibo-md-dbtx-aly:hasDefaultRate | 具有默认利率（has default rate） | 标识默认利率。 | 定义域（domain）：债务池；值域（range）：违约率 |
| fibo-md-dbtx-aly:hasFactor | 具有因子（has factor） | 标识与另一数或量相乘得到给定数或表达式的数或量。 | 定义域（domain）：债务池；值域（range）：池因子（pool factor） |
| fibo-md-dbtx-aly:hasMeasure | 具有度量（has measure） | 标识某事物的度量。 | 定义域（domain）：债务池；值域（range）：提前偿付速度 |
| fibo-md-dbtx-aly:hasOutlookPeriod | 具有展望期（has outlook period） | 标识展望所覆盖的期间。 | 定义域（domain）：债务工具收益率（debt instrument yield）；值域（range）：Nc80849834122487c88d919613d63d495 |
| fibo-md-dbtx-aly:hasWac | 具有加权平均票息（has wac） | 标识加权平均票息率（WAC）。 | 定义域（domain）：抵押支持证券；值域（range）：加权平均票息 |
| fibo-md-dbtx-aly:hasYield | 具有收益率（has yield） | 标识某事物的收益率。 | 定义域（domain）：可交易债务工具；值域（range）：债务工具收益率（debt instrument yield） |
| fibo-md-dbtx-aly:isAggregateOf | 是……的汇总（is aggregate of） | 标识该汇总值所对应的组成部分。 | 定义域（domain）：债务池统计度量；值域（range）：债务池统计度量 |
| fibo-md-dbtx-aly:isDefaultMethodFor | 是……的默认方法（is default method for） | 标识该方法作为默认所适用的市场。 | 定义域（domain）：本地收益率计算法（native yield calculation method）；值域（range）：可交易债务工具 |
| fibo-md-dbtx-aly:isRateOfChangeOf | 是……的变化率（is rate of change of） | 标识该变化率所针对的对象。 | 定义域（domain）：债务凸性分析（debt convexity analytic）；值域（range）：久期分析（duration analytic） |
| fibo-md-dbtx-aly:modifiedDurationValue | 修正久期值（modified duration value） | 以年计的修正久期。 | 定义域（domain）：修正久期分析（modified duration analytic）；值域（range）：时长 |

## 4. 数据属性（Datatype Property）

| 属性（Property） | 中文（English） | 定义（Definition） |
|---|---|---|
| fibo-md-dbtx-aly:decimalPlaces | 小数位数（decimal places） | 因子值公布所用的小数位数。 |
| fibo-md-dbtx-aly:isCompounded | 复利（is compounded） | 表明收益率是否按复利计算（用于债务工具或贷款等收益与利息支付相关的情形）。 |
| fibo-md-dbtx-aly:priceIsTraded | 价格成交（price is traded） | 该证券在所述期间内以价格成交。 |
| fibo-md-dbtx-aly:priceQuotedExDividend | 除息报价（price quoted ex dividend） | 表明收益率是否基于除息报价；债券除息交易指在付息日前某段时期内成交。 |
| fibo-md-dbtx-aly:quotedExDividend | 除息报价（quoted ex dividend） | 表明价格是否为除息报价。 |
| fibo-md-dbtx-aly:roundingConvention | 舍入惯例（rounding convention） | 计算方法中使用的舍入惯例。 |

## 5. 公理约定（Axioms）

- 麦考利久期分析（MacCaulays Duration Analytic）：引用 some 内部收益率
- 债券等价收益率（bond equivalent yield）：基于 some 等价收益率计算法（equivalent yield calculation method）
- 信用利差（credit spread）：具有自变量 some 参考利率
- 当期收益率计算法（current yield calculation method）：具有自变量 some 净价
- 债务凸性分析（debt convexity analytic）：是……的变化率（is rate of change of） some 久期分析（duration analytic）
- 债务凸性分析（debt convexity analytic）：引用 some 债务工具收益率（debt instrument yield）
- 债务凸性分析（debt convexity analytic）：具有自变量 some 市场利差
- 债务工具收益率（debt instrument yield）：按……计算（calculation following） some 收益率计算方法（yield calculation method）
- 债务工具收益率（debt instrument yield）：具有展望期（has outlook period） some（restriction）
- 债务工具收益率（debt instrument yield）：具有自变量 some 证券价格
- 债务价格利差（debt price spread）：适用于 some 证券价格
- 债务证券做市商（debt securities market maker）：确定债务市场价（determines market price for debt） some 场外债券市场价（o t c bond market price）
- 平均期限收益率（debt yield to average life）：具有展望期（has outlook period） some 加权平均期限
- 等价期限收益率（debt yield to equivalent life）：具有展望期（has outlook period） some 等价期限分析（equivalent life analytic）
- 到期收益率（debt yield to maturity）：具有展望期（has outlook period） some（具有距到期期限 some 显式时长）
- 至下一赎回日收益率（debt yield to next call）：具有展望期（has outlook period） some 下一赎回（next call）
- 最差收益率（debt yield to worst）：具有展望期（has outlook period） some 最差赎回（worst call）
- 久期分析（duration analytic）：引用 some 债务工具收益率（debt instrument yield）
- 等价期限分析（equivalent life analytic）：基于 some 部分赎回估计模型（partial calls estimation model）
- 等价期限分析（equivalent life analytic）：引用 some 可部分赎回债券
- 等价期限分析（equivalent life analytic） 与 加权平均期限 互斥（disjointWith）
- 交易所交易债券价格（exchange traded bond price） 与 场外债券市场价（o t c bond market price） 互斥（disjointWith）
- 贷款池提前偿付模型（loan pool prepayment model）：包含 some 贷款提前偿付公式（loan prepayment formula）
- 修正久期分析（modified duration analytic）：引用 some 麦考利久期分析（MacCaulays Duration Analytic）
- 修正久期分析（modified duration analytic） 与 麦考利久期分析（MacCaulays Duration Analytic） 互斥（disjointWith）
- 本地收益率（native yield）：基于 some 本地收益率计算法（native yield calculation method）
- 本地收益率计算法（native yield calculation method）：是……的默认方法（is default method for） some 可交易债务工具
- 下一赎回（next call）：具有日期 some 下一赎回日（next call date）
- 场外债券市场价（o t c bond market price）：具有定价来源 some 债务证券做市商（debt securities market maker）
- 池清偿速度（pool paydown rate）：restriction
- 池清偿速度（pool paydown rate）：基于 some 池因子（pool factor）
- 基点价格值（price value of basis point）：引用 some 债务工具收益率（debt instrument yield）
- 俄罗斯收益率计算法（russian yield calculation method）：具有公式 some 俄罗斯收益率公式（russian yield formula）
- 简单收益率计算法（simple yield calculation method）：具有自变量 some 全价
- 美国公司债收益率计算法（u s corporate bond yield calculation method）：具有公式 some ICMA 收益率公式（i c m a yield formula）
- 美国国债收益率计算法（u s treasury yield calculation method）：具有公式 some ICMA 收益率公式（i c m a yield formula）
- 华尔街收益率计算法（wall street yield calculation method）：具有公式 some ICMA 收益率公式（i c m a yield formula）
- 收益率计算公式（yield calculation formula）：适用于 some 债务工具收益率（debt instrument yield）
- 收益率计算方法（yield calculation method）：具有复利频率 only 重复区间
- 收益率计算方法（yield calculation method）：具有自变量 only 变量
- 收益率计算方法（yield calculation method）：具有公式 some 收益率计算公式（yield calculation formula）
- 至下一回售日收益率（yield to next put）：具有展望期（has outlook period） some 下一回售（next put）

## 6. 依赖（owl:imports，21 个）

本本体通过 `owl:imports` 引入以下本体，各项的中文名称与简介如下：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `FBC/DebtAndEquities/Debt.rdf` | 债务本体（Debt Ontology） | 定义债务（debt）与债权债务关系的核心概念：借款人、贷款人、本金与利息义务。 |
| `FBC/FinancialInstruments/InstrumentPricing.rdf` | 工具定价本体（Instrument Pricing Ontology） | 定义金融工具的价格、报价与估值概念。 |
| `FND/Accounting/CurrencyAmount.rdf` | 货币金额本体（Currency Amount Ontology） | 定义「金额＋币种」的货币金额（currency amount）表示，是 FIBO 中表达价格、债务金额、付款额等一切带币种数值的基础构件。 |
| `FND/DatesAndTimes/FinancialDates.rdf` | 金融日期本体（Financial Dates Ontology） | 定义金融语境下的日期与期间概念：结算日、付息日、到期日、日计数基准等。 |
| `FND/Utilities/Analytics.rdf` | 分析本体（Analytics Ontology） | 定义分析工具、度量与比率的通用概念，支撑指标与模型的表达。 |
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `IND/Indicators/Indicators.rdf` | 指标本体（Indicators Ontology） | 定义「指标」（indicator）的通用概念：对某现象的可度量表示，是经济指标、利率等的上位模型。 |
| `IND/InterestRates/InterestRates.rdf` | 利率本体（Interest Rates Ontology） | 定义利率（interest rate）的结构：基准利率、利差、期限与重置机制。 |
| `SEC/Debt/Bonds.rdf` | 债券本体（Bonds Ontology） | 定义债券（bond）：期限、票面利率、付息方式与偿还结构。 |
| `SEC/Debt/DebtInstruments.rdf` | 债务工具本体（Debt Instruments Ontology） | 定义债务工具（debt instrument）的通用概念：可交易的债权凭证，是债券、票据等的上位模型。 |
| `SEC/Debt/MortgageBackedSecurities.rdf` | 抵押贷款支持证券本体（Mortgage-backed Securities Ontology） | 定义抵押贷款支持证券（MBS）：以抵押贷款池为支持的证券。 |
| `SEC/Debt/PoolBackedSecurities.rdf` | 池支持证券本体（Pool-backed Securities Ontology） | 定义以资产池为支持的证券的通用结构：资产池、分层（tranche）与过手安排。 |
| `SEC/Securities/Pools.rdf` | 证券池本体（Securities Pools Ontology） | 定义证券池（pool）：归集起来作为证券化基础的一组资产。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |
| `https://www.omg.org/spec/Commons/Classifiers/` | OMG 通用分类器本体（OMG Commons Classifiers） | OMG 通用本体库（Commons）中的分类器本体，定义分类方案、类别与归类关系的通用概念，FIBO 的分类建模建立在其上。 |
| `https://www.omg.org/spec/Commons/Collections/` | OMG 通用集合本体（OMG Commons Collections） | Commons 库中的集合本体，定义集合、成员等通用概念。 |
| `https://www.omg.org/spec/Commons/ContextualDesignators/` | OMG 通用语境指称本体（OMG Commons Contextual Designators） | Commons 库中的语境指称本体，定义「在某个语境下指代某物的名称/符号」，是地址、账户号码等语境相关标识的基础。 |
| `https://www.omg.org/spec/Commons/DatesAndTimes/` | OMG 通用日期与时间本体（OMG Commons Dates and Times） | Commons 库中的日期时间本体，定义日期、期间、时间点等通用时间概念。 |
| `https://www.omg.org/spec/Commons/Documents/` | OMG 通用文档本体（OMG Commons Documents） | Commons 库中的文档本体，定义文档及其组成部分的通用概念。 |
| `https://www.omg.org/spec/Commons/Organizations/` | OMG 通用组织本体（OMG Commons Organizations） | Commons 库中的组织本体，定义组织、组织成员与组织结构的通用概念。 |
| `https://www.omg.org/spec/Commons/QuantitiesAndUnits/` | OMG 通用量与单位本体（OMG Commons Quantities and Units） | Commons 库中的量与单位本体，定义数量、度量单位、量纲的通用概念，支撑金额、比率等数值表达。 |

## 7. 文件

- 官方 RDF/XML：`DebtAnalytics.rdf`
- 中文 Turtle：`DebtAnalytics.ttl`
- 结构图：`DebtAnalytics-structure.png` / `DebtAnalytics-structure.svg`