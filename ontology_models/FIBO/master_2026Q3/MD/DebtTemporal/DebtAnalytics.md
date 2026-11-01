# 债务分析本体（Debt Analytics Ontology）结构与公理说明

本文档对应 `DebtAnalytics.rdf` / `DebtAnalytics.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `DebtAnalytics-structure.png`（`DebtAnalytics-structure.svg` 为可缩放版本）。

![债务分析本体（Debt Analytics Ontology）本体结构图](DebtAnalytics-structure.png)

## 1. 本体概述

定义债务工具分析指标及其时间序列：收益率（yield）、利差（spread）、久期（duration）等随时间的变化。

**在体系中的位置**：MD 债务时序模块的核心，把债券分析从「单点数值」扩展为「历史轨迹」。

**上下游关系**：上游依赖 SEC 债务工具、IND 利率与 FND 分析本体；下游服务固收分析与风险建模。

**与相近概念的差别**：收益率≠利率——利率是合同约定的付息水平，收益率是按市场价格推算的回报度量；分析指标≠行情价格——指标是从价格与条款推算的派生量。

本本体中类与类的核心关系如下（完整细节见各类小节）：

- **麦考利久期分析（MacCaulays Duration Analytic）** 继承 **久期分析（duration analytic）**
- **债券等价收益率（bond equivalent yield）** 继承 **相对定义的债务工具收益率（relatively defined debt instrument yield）**
- **信用利差（credit spread）** 继承 **收益率差（YieldSpread）**
- **当期收益率计算法（current yield calculation method）** 继承 **收益率计算方法（yield calculation method）**
- **债务凸性分析（debt convexity analytic）** 继承 **带日期集合成分（DatedCollectionConstituent）**
- **债务工具收益率（debt instrument yield）** 继承 **收益率（Yield）**
- **债务价格利差（debt price spread）** 继承 **市场利差（MarketSpread）**
- **债务证券做市商（debt securities market maker）** 继承 **服务提供方（ServiceProvider）**
- **平均期限收益率（debt yield to average life）** 继承 **债务工具收益率（debt instrument yield）**
- **等价期限收益率（debt yield to equivalent life）** 继承 **债务工具收益率（debt instrument yield）**
- **到期收益率（debt yield to maturity）** 继承 **债务工具收益率（debt instrument yield）**
- **至下一赎回日收益率（debt yield to next call）** 继承 **债务工具收益率（debt instrument yield）**
- 其余 49 条关系从略。

## 2. 类（Class）

| 类（Class） | 定义（Definition） |
|---|---|
| 麦考利久期分析（MacCaulays Duration Analytic） | 麦考利久期的分析度量。 |
| 债券等价收益率（bond equivalent yield） | 按与另一债券收益率等价基准确定的收益率，用于真实比较不同债务工具的价格。<br>Yield determined on an equivalent basis to the yield of another bond. This is used to be able to realistically compare prices between debt instruments across different markets. |
| 信用利差（credit spread） | 反映投资者从信用风险较高的证券相对信用风险较低证券所能获得的额外净收益的收益率利差。<br>yield spread that reflects the additional net yield an investor can earn from a security with more credit risk relative to one with less credit risk |
| 当期收益率计算法（current yield calculation method） | 利息支付额与净价之比。<br>The ratio of the interest payment amount to the clean price. |
| 债务凸性分析（debt convexity analytic） | 证券价格对其收益率的二阶导数除以证券价格；当价格上升幅度大于收益率下降所暗示的幅度时呈正凸性。<br>The second derivative of a security's price with respect to its yield, divided by the security's price. A security exhibits positive convexity when its price rises more for a downward move in its yield than its price declines for an equal upward move in its yield. Further notes: A measure of the change in price for a given change in Modified Duration. This always (necessarily) refers to Modified Duration. This is used as another risk measurement. Numerator is always (a) duration - either MacCaulays or Modified. Always rate of change of (one of the) Duration against some other parameter. The other paramater can be characterised as a Yield (it may be the Price, but that has a relationship to the Yield in any case). REVIEW: Inconsistency in the above - is it always necessarily Modified Duration that is referred to, or "any" Duration measure (Macaulays and.or Modified)? notes 9 Dec A measure of the sensitivity of the price with reference to interest rates. This is normally determined with reference to maturity, but since there are different maturity dates, this figure gives an estimate of the equitvalent if you had a homogenous portfolio, i.e. this is an estimate based on a pure equivalent, homogenous portfolio. Convexity of instrument versus portfolio. Sees instrument in terms of the set of cashflows. The term Convexity can be applied either to a bond or to a portfolio. More notes: When you get Convexit in MD, it will tell you what Duration it is refrfering to, along with Redemption Date (logically). Also if there is Option Adjusted Yield, there is a third set of analytics. What are they? i.e. OA Convexity, Duration Yield and the rest. Conclusions: Agreed to revisit this in OTC. |
| 债务工具收益率（debt instrument yield） | 按所述价格计算的债务工具回报。<br>The return on the debt instrument at the stated price. |
| 债务价格利差（debt price spread） | 某证券价格与作为参照的另一证券公允价值之差，用于定价比较。<br>The difference between the [what?] of a security and the fair price value of a different security which is used as a point of reference. The spread is used to determine the price of the instrument. (draft definition) |
| 债务证券做市商（debt securities market maker） | 在给定市场中担任做市商角色的参与者。<br>An actor which has the role of Market Maker in a given market. |
| 平均期限收益率（debt yield to average life） | 以债券平均期限替代最终到期日计算所得的收益率。<br>The yield achieved by substituting a bond's average life for the issue's final maturity date. |
| 等价期限收益率（debt yield to equivalent life） | 以债券等价期限替代最终到期日计算所得的收益率。<br>The yield achieved by substituting a bond's equivalent life for the issue's final maturity date. |
| 到期收益率（debt yield to maturity） | 投资者以当前全价购入债券并持有至到期（假设所有票息按该收益率再投资）可获得的内部收益率。<br>The internal rate of return an investor would achieve if he or she purchased that bond at its current dirty price, and held it to maturity, assuming all coupon and principal payments are received as scheduled. |
| 至下一赎回日收益率（debt yield to next call） | 债券到下一个可能赎回日的收益率。<br>The yield of a bond to the next possible call date. |
| 最差收益率（debt yield to worst） | 按该工具可能被赎回的最坏情形计算的收益率。<br>Yield to the worst case of when the instrument might be called. |
| 贴现工具收益率（discounted instrument yield） | 贴现工具的报价收益率：贴现额与面值之比，再除以以年计（不足一年按分数计）的到期期限。<br>Yield quoted for a discount instrument. This is the ratio of the discount to the face value, divided by the period to maturity as a fraction of a year. |
| 久期分析（duration analytic） | 收到全部付款的加权平均时间。<br>Weighted average time to receipt of all the payments. |
| 有效久期（effective duration） | 考虑现金流随利率变化而调整的久期度量。 |
| 有效收益率（effective yield） | 考虑复利影响的实际收益率。 |
| 等价期限分析（equivalent life analytic） | 等价期限的分析度量。 |
| 等价收益率计算法（equivalent yield calculation method） | 按等价基准计算收益率的方法。 |
| 交易所交易债券价格（exchange traded bond price） | 在交易所交易的债券的价格。 |
| FFIEC 降 300 提前偿付速度（f f i e c down 300 prepay speed） | 「降 300」情景下用于基础抵押品现金流计算的公共证券协会（PSA）速度。<br>Public Securities Association (PSA) speed used for the underlying collateral for cash-flow calculations in the "down 300" scenario. |
| FFIEC 升 300 提前偿付速度（f f i e c up 300 prepay speed） | 「升 300」情景下用于基础抵押品现金流计算的公共证券协会（PSA）速度。<br>Public Securities Association (PSA) speed used for the underlying collateral for cash-flow calculations in the "up 300" scenario. |
| ICMA 收益率公式（i c m a yield formula） | 国际资本市场协会（ICMA，原 ISMA）规定的固定利率债券收益率确定方法。<br>The calculation method specified by ICMA (formerly ISMA) for determination of yield for fixed-rate bonds. |
| 隐含远期利率（implied forward rate） | 由即期利率结构隐含的远期利率。 |
| 内部确定价格利差（internally determined price spread） | 组织内部根据自有交易台可得信息确定的利差。<br>The spread determined internally within the organisation from information available at their own trading desks. Further Notes Internal prices within a bank would be determined by surveying their own traders. So e.g. corporate desk trades these 30 bonds, get the daily spreads on those at the end of the day and calculate the price. The traders determine the pricing during the based on market movements. (this is all for OTC traded bonds, not exchange traded bonds). |
| 日本复利收益率计算法（japanese compound yield calculation method） | 日本市场使用的复利收益率计算方法。<br>No definition in selection list. |
| 日本单利收益率计算法（japanese simple yield calculation method） | 日本市场使用的单利收益率计算方法。<br>No definition.Term put here from memory. 02 Dec changed from Japanese Yield to Japanese Simple Yield. note hat Japanese Compound yield also here (from FIBIM or anothe rlist, added 25 nov with the rest). |
| 关键利率久期（key rate duration） | 证券价格对特定期限利率变化的敏感度度量。 |
| 期限分析（life analytic） | 对证券期限的某种度量，而非实际到期时间本身；为基于适当参数计算的导出数值。<br>Some measure of the life of a security, other than the actual time to maturity itself. This is a derived figure, based on certain parameters as appropriate to that type of instrument, to give a figure that is equivalent to and similar to the basic maturity of the instrument, for the purposes of analysing that security. |
| 贷款池提前偿付模型（loan pool prepayment model） | 个贷池（如抵押贷款池或贷款池）中贷款提前偿付的模型。<br>Model of the prepayments of loans in a pool of individual loans, such as a mortgage pool or loan pool. |
| 贷款提前偿付公式（loan prepayment formula） | 体现贷款池提前偿付速度模型的公式。<br>The formula which embodies the model for loan pool prepayment speed. |
| 到期等价 PSA（maturity equivalent p s a） | 产生与 CMO、ABS 或 MBS 所计算平均期限相同之平均期限的提前偿付速度。<br>Prepayment speed that results in the same average life as that computed for the Collateralized Mortgage Obligation (CMO), Asset Backed Securities (ABS) or Mortgage Backed Securities (MBS) using the Maturity Prepay Model. |
| 修正久期分析（modified duration analytic） | 给定收益率变化下证券价格的百分比变化；修正久期越高，风险越高。<br>The percentage price change of a security for a given change in yield. The higher the modified duration of a security, the higher its risk. Ad/ModDuration = [duration / {1 + (IRR/M)}]; where IRR is the internal rate of return and M is the number of compounding periods per year. |
| 本地收益率（native yield） | 按该证券交易市场的默认收益率计算方法确定的证券收益率。<br>The yield of the security as determined using the Yield Calculation Method that is the default for the market that the security is traded in. |
| 本地收益率计算法（native yield calculation method） | 该证券市场通行的计算方法惯例。<br>The convention used in the marketplace for that security. |
| 下一赎回（next call） | 截至当前时点该次发行的下一次赎回。<br>The next call of the issue, as at the current time. |
| 下一赎回日（next call date） | 自当前日期起该次发行可被赎回的下一日期。<br>The next date on which the issue can be called, from the present date. |
| 下一回售（next put） | 截至当前时点该次发行的下一个可回售日。<br>The next available put date for the issue, as at the current time. |
| 场外债券市场价（o t c bond market price） | 场外交易债券的市场价格。<br>The price determined for the marketplace for a bond which is traded over the counter. |
| 期权调整收益率（option adjusted yield） | 以利差形式表示、基于不同利率路径计算的期权调整收益率（OAS）。<br>NB specified as a spread. synonym: OAS Based on different Int Rate paths. There are different OAS models just like there are different Yield methods. Also would make reference to the Yield Curve - but these are parameters that go into that model. Limit this model at the point where it distinguishes the difference between things - we are not in a position to mathematically model the things themselves, just capture the basic facts. |
| 部分赎回估计模型（partial calls estimation model） | 估计提前部分赎回的模型。<br>A model of how the early partial calls are estimated. |
| 池因子（pool factor） | 原始池中仍未清偿的比例，为小于 1 的数，以百分比表示。<br>How much of the original pool is still outstanding. This is a number below one. Expressed as percentage. |
| 池清偿速度（pool paydown rate） | 池清偿的速度，基于观测因子（CPR、SMM 等），不同证券计量方式不同。<br>The rate at which the pool is paying down. This is based on observed factor. CPR, SMM, etc. etc. Measured differently for different kinds of security. CBO might have a prepayment rate for example if the underlying bond is callable. with a non agency mortgge dela, defualts will effect this. so for instance there is principal is no lnger inthe pool because the mortgagee defaults. With agency these are not taken out in the case of default but for non agency these mortgages are removed from the pool if and when a mortgagee defualts. |
| 基点价格值（price value of basis point） | 收益率变动一个基点时价格的敏感度，定义为收益率变动 1 个基点时的价格差。<br>Sensitivity of the price for one basis point change in yield, defined as the difference in price given 1 bp change in yield. |
| 相对收益率计算法（relative yield calculation method） | 以相对基准计算收益率的方法。 |
| 相对定义的债务工具收益率（relatively defined debt instrument yield） | 以相对基准定义的债务工具收益率。 |
| 俄罗斯收益率计算法（russian yield calculation method） | 俄罗斯市场用于确定收益率的方法，基于数学基础不同的有效收益率。<br>The method used in determining Yield in the Russian markets. This is based on an effective yield with fundamentally different math. To give an example of the use of a different "yield type", we have Russia, which trades based on an effective yield. The price-yield math is fundamentally different. Notes Origin:Fidessa Uses a trade space and effective yield formula. MAy have same day types but different math. |
| 俄罗斯收益率公式（russian yield formula） | 基于与其他市场不同之有效收益率的收益率公式。<br>This is based on a different Effective Yield than on another market. |
| 简单收益率计算法（simple yield calculation method） | 以百分比表示的年回报率：回报除以投入再乘以 100。<br>The annual rate of return expressed as a percentage. This is the return divided by the outlay and multiplied by 100 to express the figure as a percentage. |
| 西班牙收益率计算法（spanish yield calculation method） | 西班牙公司债市场用于确定年收益率的方法。<br>The method used in determining annual yield in Spanish corporate bonds. |
| 美国公司债收益率计算法（u s corporate bond yield calculation method） | 采用 30/360 计息惯例和半年复利的收益率计算方法。<br>This has 30/360 and semi-annual compounding. |
| 美国国债收益率计算法（u s treasury yield calculation method） | 美国国债市场使用的收益率计算方法。 |
| 华尔街收益率计算法（wall street yield calculation method） | 华尔街通行的收益率计算方法。<br>No definition.Term put here from memory. |
| 现金流收取加权平均时间（weighted average time to receipt of cashflows） | 某工具现金流收取的加权平均时间。<br>The weighted average time to the receipt of cashflows for an instrument. |
| 最差赎回（worst call） | 就工具可能被赎回的时间而言代表最坏情形的赎回事件。<br>call event representing the worst case with respect to when the instrument might be called |
| 收益率计算公式（yield calculation formula） | 用于确定收益率的公式。<br>The formula used in determining the Yield. |
| 收益率计算方法（yield calculation method） | 计算收益率的方法，包括计算公式及特定的天数计算惯例与复利方式。<br>The method by which the yield is calculated. This includes a formula for calculation and a specific day count convention and compounding. You would apply this calculation method on top of the underlying terms and conditions, do for example the holiday calenders and so on, are used in these formulae. For final cash flow: Japanese yield will round down accrued interest. Add: The actual underlying math. Wall Street uses the same ICMA formula. |
| 至下一回售日收益率（yield to next put） | 到下一个可回售日的收益率。 |

以下按类逐个展开：每个类给出继承关系、相关属性与公理约定；子类在父类之下降一级编号。

### 2.1 信用利差（credit spread）

定义：反映投资者从信用风险较高的证券相对信用风险较低证券所能获得的额外净收益的收益率利差。

- 父类：**收益率差（YieldSpread）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有自变量（hasArgument）** | — | — |

公理：

- **具有自变量（hasArgument）**至少有一个取值，类型是**参考利率（ReferenceInterestRate）**。

### 2.2 债务凸性分析（debt convexity analytic）

定义：证券价格对其收益率的二阶导数除以证券价格；当价格上升幅度大于收益率下降所暗示的幅度时呈正凸性。

- 父类：**带日期集合成分（DatedCollectionConstituent）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **是……的变化率（is rate of change of）** | 标识该变化率所针对的对象。 | 值域：久期分析（duration analytic） |
| **引用（refersTo）** | — | — |
| **具有自变量（hasArgument）** | — | — |

公理：

- **具有自变量（hasArgument）**至少有一个取值，类型是**市场利差（MarketSpread）**。
- **引用（refersTo）**至少有一个取值，类型是**债务工具收益率（debt instrument yield）**。
- **是……的变化率（is rate of change of）**至少有一个取值，类型是**久期分析（duration analytic）**。

### 2.3 债务工具收益率（debt instrument yield）

定义：按所述价格计算的债务工具回报。

- 父类：**收益率（Yield）**
- 直接子类：**平均期限收益率（debt yield to average life）**、**等价期限收益率（debt yield to equivalent life）**、**到期收益率（debt yield to maturity）**、**至下一赎回日收益率（debt yield to next call）**、**最差收益率（debt yield to worst）**、**贴现工具收益率（discounted instrument yield）**、**有效收益率（effective yield）**、**期权调整收益率（option adjusted yield）**、**相对定义的债务工具收益率（relatively defined debt instrument yield）**、**至下一回售日收益率（yield to next put）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **按……计算（calculation following）** | 标识计算所遵循的方法或惯例。 | 值域：收益率计算方法（yield calculation method） |
| **具有展望期（has outlook period）** | 标识展望所覆盖的期间。 | 值域：Nf6187ddb78624b4b8bf9ccab70a327bf |
| **复利（is compounded）** | 表明收益率是否按复利计算（用于债务工具或贷款等收益与利息支付相关的情形）。<br>Definition needed Moved from Yield - assume this can only be about debt instrument or loan / debt yields i..e where the income relates to interest payments. . | 值域：xsd:boolean |
| **除息报价（price quoted ex dividend）** | 表明收益率是否基于除息报价；债券除息交易指在付息日前某段时期内成交。<br>Whether or not the yield is based on a price which is quoted ex-dividend. When a bond is said to trade ex-dividend it means that there is a period of time prior to each coupon payment during which a bond purchaser does not receive custody of the next coupon. That payment is made to the previous bond holder and accrued interest is therefore negative during the ex-dividend period. | 值域：xsd:boolean |
| **具有自变量（hasArgument）** | — | — |

公理：

- **具有展望期（has outlook period）**至少有一个取值，该取值满足：该属性存在取值约束。
- **具有自变量（hasArgument）**至少有一个取值，类型是**证券价格（SecurityPrice）**。
- **按……计算（calculation following）**至少有一个取值，类型是**收益率计算方法（yield calculation method）**。

#### 2.3.1 平均期限收益率（debt yield to average life）

定义：以债券平均期限替代最终到期日计算所得的收益率。

- 父类：**债务工具收益率（debt instrument yield）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有展望期（has outlook period）** | 标识展望所覆盖的期间。 | 值域：Nf6187ddb78624b4b8bf9ccab70a327bf |

公理：

- **具有展望期（has outlook period）**至少有一个取值，类型是**加权平均期限（WeightedAverageLife）**。

#### 2.3.2 等价期限收益率（debt yield to equivalent life）

定义：以债券等价期限替代最终到期日计算所得的收益率。

- 父类：**债务工具收益率（debt instrument yield）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有展望期（has outlook period）** | 标识展望所覆盖的期间。 | 值域：Nf6187ddb78624b4b8bf9ccab70a327bf |

公理：

- **具有展望期（has outlook period）**至少有一个取值，类型是**等价期限分析（equivalent life analytic）**。

#### 2.3.3 到期收益率（debt yield to maturity）

定义：投资者以当前全价购入债券并持有至到期（假设所有票息按该收益率再投资）可获得的内部收益率。

- 父类：**债务工具收益率（debt instrument yield）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有展望期（has outlook period）** | 标识展望所覆盖的期间。 | 值域：Nf6187ddb78624b4b8bf9ccab70a327bf |

公理：

- **具有展望期（has outlook period）**至少有一个取值，该取值满足：**具有距到期期限（hasOriginalTimeToMaturity）**至少有一个取值，类型是**显式时长（ExplicitDuration）**。

#### 2.3.4 至下一赎回日收益率（debt yield to next call）

定义：债券到下一个可能赎回日的收益率。

- 父类：**债务工具收益率（debt instrument yield）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有展望期（has outlook period）** | 标识展望所覆盖的期间。 | 值域：Nf6187ddb78624b4b8bf9ccab70a327bf |

公理：

- **具有展望期（has outlook period）**至少有一个取值，类型是**下一赎回（next call）**。

#### 2.3.5 最差收益率（debt yield to worst）

定义：按该工具可能被赎回的最坏情形计算的收益率。

- 父类：**债务工具收益率（debt instrument yield）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有展望期（has outlook period）** | 标识展望所覆盖的期间。 | 值域：Nf6187ddb78624b4b8bf9ccab70a327bf |

公理：

- **具有展望期（has outlook period）**至少有一个取值，类型是**最差赎回（worst call）**。

#### 2.3.6 贴现工具收益率（discounted instrument yield）

定义：贴现工具的报价收益率：贴现额与面值之比，再除以以年计（不足一年按分数计）的到期期限。

- 父类：**债务工具收益率（debt instrument yield）**

#### 2.3.7 有效收益率（effective yield）

定义：考虑复利影响的实际收益率。

- 父类：**债务工具收益率（debt instrument yield）**

#### 2.3.8 期权调整收益率（option adjusted yield）

定义：以利差形式表示、基于不同利率路径计算的期权调整收益率（OAS）。

- 父类：**债务工具收益率（debt instrument yield）**

#### 2.3.9 相对定义的债务工具收益率（relatively defined debt instrument yield）

定义：以相对基准定义的债务工具收益率。

- 父类：**债务工具收益率（debt instrument yield）**
- 直接子类：**债券等价收益率（bond equivalent yield）**、**本地收益率（native yield）**

##### 2.3.9.1 债券等价收益率（bond equivalent yield）

定义：按与另一债券收益率等价基准确定的收益率，用于真实比较不同债务工具的价格。

- 父类：**相对定义的债务工具收益率（relatively defined debt instrument yield）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **基于（isBasedOn）** | — | — |

公理：

- **基于（isBasedOn）**至少有一个取值，类型是**等价收益率计算法（equivalent yield calculation method）**。

##### 2.3.9.2 本地收益率（native yield）

定义：按该证券交易市场的默认收益率计算方法确定的证券收益率。

- 父类：**相对定义的债务工具收益率（relatively defined debt instrument yield）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **基于（isBasedOn）** | — | — |

公理：

- **基于（isBasedOn）**至少有一个取值，类型是**本地收益率计算法（native yield calculation method）**。

#### 2.3.10 至下一回售日收益率（yield to next put）

定义：到下一个可回售日的收益率。

- 父类：**债务工具收益率（debt instrument yield）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有展望期（has outlook period）** | 标识展望所覆盖的期间。 | 值域：Nf6187ddb78624b4b8bf9ccab70a327bf |

公理：

- **具有展望期（has outlook period）**至少有一个取值，类型是**下一回售（next put）**。

### 2.4 债务价格利差（debt price spread）

定义：某证券价格与作为参照的另一证券公允价值之差，用于定价比较。

- 父类：**市场利差（MarketSpread）**
- 直接子类：**内部确定价格利差（internally determined price spread）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **适用于（appliesTo）** | — | — |

公理：

- **适用于（appliesTo）**至少有一个取值，类型是**证券价格（SecurityPrice）**。

#### 2.4.1 内部确定价格利差（internally determined price spread）

定义：组织内部根据自有交易台可得信息确定的利差。

- 父类：**债务价格利差（debt price spread）**

### 2.5 债务证券做市商（debt securities market maker）

定义：在给定市场中担任做市商角色的参与者。

- 父类：**服务提供方（ServiceProvider）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **确定债务市场价（determines market price for debt）** | 确定债务工具的市场价格。 | 值域：场外债券市场价（o t c bond market price） |

公理：

- **确定债务市场价（determines market price for debt）**至少有一个取值，类型是**场外债券市场价（o t c bond market price）**。

### 2.6 久期分析（duration analytic）

定义：收到全部付款的加权平均时间。

- 父类：**债务池统计度量（DebtPoolStatisticalMeasure）**
- 直接子类：**麦考利久期分析（MacCaulays Duration Analytic）**、**有效久期（effective duration）**、**关键利率久期（key rate duration）**、**修正久期分析（modified duration analytic）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **引用（refersTo）** | — | — |

公理：

- **引用（refersTo）**至少有一个取值，类型是**债务工具收益率（debt instrument yield）**。

#### 2.6.1 麦考利久期分析（MacCaulays Duration Analytic）

定义：麦考利久期的分析度量。

- 父类：**久期分析（duration analytic）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **引用（refersTo）** | — | — |

公理：

- **引用（refersTo）**至少有一个取值，类型是**内部收益率（InternalRateOfReturn）**。

#### 2.6.2 有效久期（effective duration）

定义：考虑现金流随利率变化而调整的久期度量。

- 父类：**久期分析（duration analytic）**

#### 2.6.3 关键利率久期（key rate duration）

定义：证券价格对特定期限利率变化的敏感度度量。

- 父类：**久期分析（duration analytic）**

#### 2.6.4 修正久期分析（modified duration analytic）

定义：给定收益率变化下证券价格的百分比变化；修正久期越高，风险越高。

- 父类：**久期分析（duration analytic）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **修正久期值（modified duration value）** | 以年计的修正久期。<br>The Modified Duration in Years. | 值域：时长 |
| **引用（refersTo）** | — | — |

公理：

- **引用（refersTo）**至少有一个取值，类型是**麦考利久期分析（MacCaulays Duration Analytic）**。
- 与**麦考利久期分析（MacCaulays Duration Analytic）**互斥：同一个体不能同时属于两者。

### 2.7 交易所交易债券价格（exchange traded bond price）

定义：在交易所交易的债券的价格。

- 父类：**证券价格（SecurityPrice）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **价格成交（price is traded）** | 该证券在所述期间内以价格成交。<br>The highest valuation over the period specified. Notes from Equity review, may apply to Debt also: this can be regarded as a derived price. See also note in LowPrice Difference: different rules used. May be based on trade OR quote price Analytic or Price?? this is a derived type but with a much simpler rule. | 值域：xsd:boolean |

公理：

- 与**场外债券市场价（o t c bond market price）**互斥：同一个体不能同时属于两者。

### 2.8 FFIEC 降 300 提前偿付速度（f f i e c down 300 prepay speed）

定义：「降 300」情景下用于基础抵押品现金流计算的公共证券协会（PSA）速度。

- 父类：**提前偿付速度（PrepaymentSpeed）**

### 2.9 FFIEC 升 300 提前偿付速度（f f i e c up 300 prepay speed）

定义：「升 300」情景下用于基础抵押品现金流计算的公共证券协会（PSA）速度。

- 父类：**提前偿付速度（PrepaymentSpeed）**

### 2.10 隐含远期利率（implied forward rate）

定义：由即期利率结构隐含的远期利率。

- 父类：**利率（InterestRate）**

### 2.11 期限分析（life analytic）

定义：对证券期限的某种度量，而非实际到期时间本身；为基于适当参数计算的导出数值。

- 父类：**债务池统计度量（DebtPoolStatisticalMeasure）**
- 直接子类：**等价期限分析（equivalent life analytic）**

#### 2.11.1 等价期限分析（equivalent life analytic）

定义：等价期限的分析度量。

- 父类：**期限分析（life analytic）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **基于（isBasedOn）** | — | — |
| **等价期限值（equivalent life value）** | 所述日期的等价期限（以年计）。<br>The Equivalent Life in years at the stated date. | 值域：时长 |
| **引用（refersTo）** | — | — |

公理：

- **基于（isBasedOn）**至少有一个取值，类型是**部分赎回估计模型（partial calls estimation model）**。
- **引用（refersTo）**至少有一个取值，类型是**可部分赎回债券（BondWithPartialCall）**。
- 与**加权平均期限（WeightedAverageLife）**互斥：同一个体不能同时属于两者。

### 2.12 贷款池提前偿付模型（loan pool prepayment model）

定义：个贷池（如抵押贷款池或贷款池）中贷款提前偿付的模型。

- 父类：**公式（Formula）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **包含（comprises）** | — | — |

公理：

- **包含（comprises）**至少有一个取值，类型是**贷款提前偿付公式（loan prepayment formula）**。

### 2.13 贷款提前偿付公式（loan prepayment formula）

定义：体现贷款池提前偿付速度模型的公式。

- 父类：**公式（Formula）**

### 2.14 到期等价 PSA（maturity equivalent p s a）

定义：产生与 CMO、ABS 或 MBS 所计算平均期限相同之平均期限的提前偿付速度。

- 父类：**提前偿付速度（PrepaymentSpeed）**

### 2.15 下一赎回（next call）

定义：截至当前时点该次发行的下一次赎回。

- 父类：**赎回事件（CallEvent）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有日期（hasDate）** | — | — |

公理：

- **具有日期（hasDate）**至少有一个取值，类型是**下一赎回日（next call date）**。

### 2.16 下一赎回日（next call date）

定义：自当前日期起该次发行可被赎回的下一日期。

- 父类：**日期（Date）**

### 2.17 下一回售（next put）

定义：截至当前时点该次发行的下一个可回售日。

- 父类：**回售事件（PutEvent）**

### 2.18 场外债券市场价（o t c bond market price）

定义：场外交易债券的市场价格。

- 父类：**证券价格（SecurityPrice）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有定价来源（hasPricingSource）** | — | — |

公理：

- **具有定价来源（hasPricingSource）**至少有一个取值，类型是**债务证券做市商（debt securities market maker）**。

### 2.19 部分赎回估计模型（partial calls estimation model）

定义：估计提前部分赎回的模型。

- 父类：**公式（Formula）**

### 2.20 池因子（pool factor）

定义：原始池中仍未清偿的比例，为小于 1 的数，以百分比表示。

- 父类：**百分比（Percentage）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **小数位数（decimal places）** | 因子值公布所用的小数位数。<br>The number of decimal places used in the publication of the factor value. | 值域：xsd:integer |

### 2.21 池清偿速度（pool paydown rate）

定义：池清偿的速度，基于观测因子（CPR、SMM 等），不同证券计量方式不同。

- 父类：**比率（Ratio）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **基于（isBasedOn）** | — | — |
| **具有比率值（hasRateValue）** | — | — |

公理：

- **具有比率值（hasRateValue）**存在取值约束。
- **基于（isBasedOn）**至少有一个取值，类型是**池因子（pool factor）**。

### 2.22 基点价格值（price value of basis point）

定义：收益率变动一个基点时价格的敏感度，定义为收益率变动 1 个基点时的价格差。

- 父类：**债务池统计度量（DebtPoolStatisticalMeasure）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **引用（refersTo）** | — | — |

公理：

- **引用（refersTo）**至少有一个取值，类型是**债务工具收益率（debt instrument yield）**。

### 2.23 现金流收取加权平均时间（weighted average time to receipt of cashflows）

定义：某工具现金流收取的加权平均时间。

- 父类：**公式（Formula）**

### 2.24 最差赎回（worst call）

定义：就工具可能被赎回的时间而言代表最坏情形的赎回事件。

- 父类：**赎回事件（CallEvent）**

### 2.25 收益率计算公式（yield calculation formula）

定义：用于确定收益率的公式。

- 父类：**公式（Formula）**
- 直接子类：**ICMA 收益率公式（i c m a yield formula）**、**俄罗斯收益率公式（russian yield formula）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **适用于（appliesTo）** | — | — |

公理：

- **适用于（appliesTo）**至少有一个取值，类型是**债务工具收益率（debt instrument yield）**。

#### 2.25.1 ICMA 收益率公式（i c m a yield formula）

定义：国际资本市场协会（ICMA，原 ISMA）规定的固定利率债券收益率确定方法。

- 父类：**收益率计算公式（yield calculation formula）**

#### 2.25.2 俄罗斯收益率公式（russian yield formula）

定义：基于与其他市场不同之有效收益率的收益率公式。

- 父类：**收益率计算公式（yield calculation formula）**

### 2.26 收益率计算方法（yield calculation method）

定义：计算收益率的方法，包括计算公式及特定的天数计算惯例与复利方式。

- 父类：**公式（Formula）**
- 直接子类：**当期收益率计算法（current yield calculation method）**、**日本复利收益率计算法（japanese compound yield calculation method）**、**日本单利收益率计算法（japanese simple yield calculation method）**、**相对收益率计算法（relative yield calculation method）**、**俄罗斯收益率计算法（russian yield calculation method）**、**简单收益率计算法（simple yield calculation method）**、**西班牙收益率计算法（spanish yield calculation method）**、**美国公司债收益率计算法（u s corporate bond yield calculation method）**、**美国国债收益率计算法（u s treasury yield calculation method）**、**华尔街收益率计算法（wall street yield calculation method）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有复利频率（hasCompoundingFrequency）** | — | — |
| **具有公式（hasFormula）** | — | — |
| **舍入惯例（rounding convention）** | 计算方法中使用的舍入惯例。<br>The rounding convention used in the calculation method. | 值域：xsd:string |
| **具有自变量（hasArgument）** | — | — |

公理：

- **具有公式（hasFormula）**至少有一个取值，类型是**收益率计算公式（yield calculation formula）**。
- **具有复利频率（hasCompoundingFrequency）**的所有取值只能是**重复区间（RecurrenceInterval）**。
- **具有自变量（hasArgument）**的所有取值只能是**变量（Variable）**。

#### 2.26.1 当期收益率计算法（current yield calculation method）

定义：利息支付额与净价之比。

- 父类：**收益率计算方法（yield calculation method）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有自变量（hasArgument）** | — | — |

公理：

- **具有自变量（hasArgument）**至少有一个取值，类型是**净价（CleanPrice）**。

#### 2.26.2 日本复利收益率计算法（japanese compound yield calculation method）

定义：日本市场使用的复利收益率计算方法。

- 父类：**收益率计算方法（yield calculation method）**

#### 2.26.3 日本单利收益率计算法（japanese simple yield calculation method）

定义：日本市场使用的单利收益率计算方法。

- 父类：**收益率计算方法（yield calculation method）**

#### 2.26.4 相对收益率计算法（relative yield calculation method）

定义：以相对基准计算收益率的方法。

- 父类：**收益率计算方法（yield calculation method）**
- 直接子类：**等价收益率计算法（equivalent yield calculation method）**、**本地收益率计算法（native yield calculation method）**

##### 2.26.4.1 等价收益率计算法（equivalent yield calculation method）

定义：按等价基准计算收益率的方法。

- 父类：**相对收益率计算法（relative yield calculation method）**

##### 2.26.4.2 本地收益率计算法（native yield calculation method）

定义：该证券市场通行的计算方法惯例。

- 父类：**相对收益率计算法（relative yield calculation method）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **是……的默认方法（is default method for）** | 标识该方法作为默认所适用的市场。 | 值域：可交易债务工具 |

公理：

- **是……的默认方法（is default method for）**至少有一个取值，类型是**可交易债务工具（TradableDebtInstrument）**。

#### 2.26.5 俄罗斯收益率计算法（russian yield calculation method）

定义：俄罗斯市场用于确定收益率的方法，基于数学基础不同的有效收益率。

- 父类：**收益率计算方法（yield calculation method）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有公式（hasFormula）** | — | — |

公理：

- **具有公式（hasFormula）**至少有一个取值，类型是**俄罗斯收益率公式（russian yield formula）**。

#### 2.26.6 简单收益率计算法（simple yield calculation method）

定义：以百分比表示的年回报率：回报除以投入再乘以 100。

- 父类：**收益率计算方法（yield calculation method）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有自变量（hasArgument）** | — | — |

公理：

- **具有自变量（hasArgument）**至少有一个取值，类型是**全价（DirtyPrice）**。

#### 2.26.7 西班牙收益率计算法（spanish yield calculation method）

定义：西班牙公司债市场用于确定年收益率的方法。

- 父类：**收益率计算方法（yield calculation method）**

#### 2.26.8 美国公司债收益率计算法（u s corporate bond yield calculation method）

定义：采用 30/360 计息惯例和半年复利的收益率计算方法。

- 父类：**收益率计算方法（yield calculation method）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有公式（hasFormula）** | — | — |

公理：

- **具有公式（hasFormula）**至少有一个取值，类型是**ICMA 收益率公式（i c m a yield formula）**。

#### 2.26.9 美国国债收益率计算法（u s treasury yield calculation method）

定义：美国国债市场使用的收益率计算方法。

- 父类：**收益率计算方法（yield calculation method）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有公式（hasFormula）** | — | — |

公理：

- **具有公式（hasFormula）**至少有一个取值，类型是**ICMA 收益率公式（i c m a yield formula）**。

#### 2.26.10 华尔街收益率计算法（wall street yield calculation method）

定义：华尔街通行的收益率计算方法。

- 父类：**收益率计算方法（yield calculation method）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有公式（hasFormula）** | — | — |

公理：

- **具有公式（hasFormula）**至少有一个取值，类型是**ICMA 收益率公式（i c m a yield formula）**。

## 3. 其他属性

以下属性未绑定到本体的具体类（定义域在外部本体或未声明）：

对象属性（Object Property）：

| 属性 | 定义 | 说明 |
|---|---|---|
| **默认利率值（default rate value）** | 默认的利率值。 | 值域：百分比 |
| **具有分析度量（has analytic）** | 标识某事物的分析度量。 | 值域：债务池统计度量 |
| **具有默认利率（has default rate）** | 标识默认利率。 | 值域：违约率 |
| **具有因子（has factor）** | 标识与另一数或量相乘得到给定数或表达式的数或量。 | 值域：池因子（pool factor） |
| **具有度量（has measure）** | 标识某事物的度量。 | 值域：提前偿付速度 |
| **具有加权平均票息（has wac）** | 标识加权平均票息率（WAC）。 | 值域：加权平均票息 |
| **具有收益率（has yield）** | 标识某事物的收益率。 | 值域：债务工具收益率（debt instrument yield） |
| **是……的汇总（is aggregate of）** | 标识该汇总值所对应的组成部分。 | 值域：债务池统计度量 |

数据属性（Datatype Property）：

| 属性 | 定义 |
|---|---|
| **除息报价（quoted ex dividend）** | 表明价格是否为除息报价。<br>Whether or not the price is quoted ex-dividend. When a bond is said to trade ex-dividend it means that there is a period of time prior to each coupon payment during which a bond purchaser does not receive custody of the next coupon. That payment is made to the previous bond holder and accrued interest is therefore negative during the ex-dividend period. |

## 4. 依赖（owl:imports，21 个）

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

## 5. 文件

- 官方 RDF/XML：`DebtAnalytics.rdf`
- 中文 Turtle：`DebtAnalytics.ttl`
- 结构图：`DebtAnalytics-structure.png` / `DebtAnalytics-structure.svg`