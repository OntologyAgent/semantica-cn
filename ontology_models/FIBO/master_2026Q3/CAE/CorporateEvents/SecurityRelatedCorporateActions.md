# 证券相关企业行动本体（Security-related Corporate Actions Ontology）结构与公理说明

本文档对应 `SecurityRelatedCorporateActions.rdf` / `SecurityRelatedCorporateActions.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `SecurityRelatedCorporateActions-structure.png`（`SecurityRelatedCorporateActions-structure.svg` 为可缩放版本）。

![证券相关企业行动本体（Security-related Corporate Actions Ontology）本体结构图](SecurityRelatedCorporateActions-structure.png)

## 1. 本体概述

定义直接改变证券条款或数量的企业行动：拆股、并股、换股、权证行使、证券赎回等。

**在体系中的位置**：CAE 域中企业行动本体的子集特化。

**上下游关系**：上游继承企业行动本体；下游关联 SEC 证券与 DER 权证相关本体。

**与相近概念的差别**：是企业行动的一个子类——专指影响证券本身形态的行动，区别于纯分配类行动（如现金分红不改变证券条款）。

本本体中类与类的核心关系如下（完整细节见各类小节）：

- **债券违约事件（bond default event）** 继承 **强制性公司行动（MandatoryCorporateAction）**
- **债券违约事件（bond default event）** 继承 **债务违约（ObligationDefault）**
- **红股发行（bonus issue）** 继承 **强制性公司行动（MandatoryCorporateAction）**
- **红利认股权发行（bonus rights issue）** 继承 **中介证券分配（intermediate securities distribution）**
- **红股计划分配（bonus share plan distribution）** 继承 **资本分配（capital distribution）**
- **对中介证券的催缴（call on intermediate securities）** 继承 **带选择的强制性公司行动（MandatoryWithChoiceCorporateAction）**
- **股份注销（cancellation of shares）** 继承 **公司行动（CorporateAction）**
- **资本分配（capital distribution）** 继承 **自愿性公司行动（VoluntaryCorporateAction）**
- **资本利得分配（capital gains distribution）** 继承 **自愿性公司行动（VoluntaryCorporateAction）**
- **现金股息行动（cash dividend action）** 继承 **强制性公司行动（MandatoryCorporateAction）**
- **证券交易状态变更事件（change of security trading status event）** 继承 **公司状态变更事件（corporate change of status event）**
- **最小可交易单位变更（change to smallest negotiable unit）** 继承 **公司行动（CorporateAction）**
- 其余 43 条关系从略。

## 2. 类（Class）

| 类（Class） | 定义（Definition） |
|---|---|
| 债券违约事件（bond default event） | 表明发行人未能履行债券协议中定义为违约事件之义务、且未予补救的公司行动。<br>corporate action which indicates a failure by the issuer to perform obligations defined as default events under the bond agreement and that have not been remedied |
| 红股发行（bonus issue） | 发行人按持有比例向证券持有人免费赠予额外资产的公司行动。<br>corporate action in which security holders are awarded additional assets free of payment from the issuer in proportion to their holding |
| 红利认股权发行（bonus rights issue） | 将认股权免费授予相关股份持有人的配股发行。<br>A Rights Issue in which the rights are given to the holders of the referenced shares for free. |
| 红股计划分配（bonus share plan distribution） | 从公司股本溢价储备中发行股份、视为资本分配而非收益发放的事件。<br>Event in which shares are issued from the Share Premium Reserve of the company and are considered as a capital distribution rather than a disbursement of income, with different tax implications. SWIFT Definition (adapted above) "Typically found in Australia, shares are issued from the Share Premium Reserve of the company and are considered as a capital distribution rather than a disbursement of income, with different tax implications." To be researches further. There are certainly Share Plans in Australia, where you can take a dividend as shares. Thewse would be in the nature of Bonus Shares. They are a tradeoff from cash dividends. Other terms to model: A "Scheme of Arrangment" - does this change the capital reserves or is it just another word for restructure. An arrangement with the company's debtors, and coule potentially change the capital base by converting the debt to shares (see other diagram note with these in). |
| 对中介证券的催缴（call on intermediate securities） | 对未缴款证券或中介证券分配产生的中介证券进行催缴或行权的公司行动。<br>corporate action that involves a call or exercise on nil paid securities or intermediate securities resulting from an intermediate securities distribution (RHDI) |
| 股份注销（cancellation of shares） | 股份的注销，仅适用于未公开发行的股份（即库存股）。<br>The cancellation of shares. Further Notes Only possible with shares not publicly issued i.e. treasury shares |
| 资本分配（capital distribution） | 从发行人资本账户向股东支付现金的公司行动。<br>corporate action that pays shareholders an amount in cash issued from the issuer's capital account |
| 资本利得分配（capital gains distribution） | 将出售公司资产所得利润分配给股东的公司行动。<br>corporate action that distributes profits resulting from the sale of company assets to shareholders |
| 现金股息行动（cash dividend action） | 按持股比例向股东分配现金的公司行动。<br>corporate action that distributes cash to shareholders in proportion to their equity holding |
| 证券交易状态变更事件（change of security trading status event） | 可交易证券的交易状态发生变化的事件。<br>An event in which the trading status of a tradable security changes. |
| 最小可交易单位变更（change to smallest negotiable unit） | 修改股份最小可交易单位以获得新的可交易单位（SWIFT：SMAL）。<br>Modification of the smallest negotiable unit of shares in order to obtain a new negotiable unit. SWIFT:SMAL |
| 转换行动（conversion action） | 将证券（通常为可转换债券或优先股）转换为另一形式证券（通常为普通股）的公司行动。<br>corporate action involving conversion of securities (generally convertible bonds or preferred shares) into another form of securities (usually common shares) at a pre-stated price/ratio |
| 转换暂停行动（conversion suspension action） | 暂停证券转换，通常在会议召开前数周（SWIFT：SCOP）。<br>Suspension of conversion of securities, generally a couple of weeks before a meeting takes place. SWIFT = SCOP |
| 公司行动义务（corporate action obligation） | 与持有某证券相关的义务。<br>An obligation related to the holding of a Security. |
| 公司行动付款义务（corporate action payment obligation） | 公司行动情境中支付款项的义务。 |
| 公司行动证券交付义务（corporate action securities delivery obligation） | 公司行动情境中交付某证券的义务；现金对价与证券对价均可表示为合同义务。<br>Some obligation to deliver some security in the thr context of corporate actions. All cash proceeds and security proceeds can be represented a s acontractual obligation. Where does that obligation arise? Usually in the Contract itself - but there may be other answers to this. Defines what has to be delivered. or paid. Entitlement meanwhile is a calculation based on the Contract. |
| 公司状态变更事件（corporate change of status event） | 某证券状态的某种变更。<br>Some change to the status of some security. |
| 息票剥离（coupon strip） | 将未来付息日的利息息票与授予持有人本金权利的证券本金分离的过程。<br>Coupon stripping is the process whereby interest coupons for future payment dates are separated from the security corpus that entitles the holder to the principal repayment. |
| 减值行动（decrease in value action） | 导致股份面值或基金资产价值减少的公司行动。<br>corporate action resulting in a reduction of face value of a share or the value of fund assets |
| 股息选择权行动（dividend option action） | 向股东分配股息、股东可选择收取形式的公司行动。<br>corporate action that involves distribution of a dividend to shareholders with a choice of benefit to receive |
| 股息再投资行动（dividend reinvestment action） | 持有人可保留现金或将现金再投资为发行公司额外股票的股息支付行动。<br>corporate action that involves a dividend payment whereby holders can keep cash or have the cash reinvested into additional shares in the issuing company |
| 抽签赎回（drawing） | 在证券预定最终到期日前部分赎回。<br>Redemption in part before the scheduled final maturity date of a security. |
| 荷兰式拍卖（dutch auction） | 由希望收购某证券的参与方发起的公司行动。<br>corporate action by a party wishing to acquire a security |
| 交换行动（exchange action） | 以持仓换取其他证券和/或现金的公司行动。<br>corporate action that reflects an exchange of holdings for other securities and/or cash |
| 正式要约（formal offer） | 向持有人、潜在持有人或其他利益相关方发出的、达成对参与方具有或将具有法律约束力之交易的要约。<br>corporate action involving an offer to a holder, potential holder, or other intersted party, to enter into a trade which is or would be legally binding on the part of the party making the offer (the offeror). |
| 全额提前赎回行动（full call early redemption action） | 在到期前对某次发行的全部流通证券进行赎回的公司行动。<br>corporate action that involves redemption of an entire issue outstanding of securities prior to maturity |
| 付息行动（interest payment action） | 向计息资产持有人分配定期利息的公司行动。<br>corporate action that involves distribution of a regular interest payment to holders of an interest-bearing asset |
| 实物付息（interest payment in kind） | 以现金以外的任何形式向计息资产持有人分配的利息支付（SWIFT：PINK）。<br>Interest payment, in any kind except cash, distributed to holders of an interest bearing asset. SWIFT = PINK |
| 附本金付息（interest payment with principal） | 除利息支付外，同时支付计息资产部分本金的付款（SWIFT：PRII）。<br>A payment of a portion of the principal of an interest bearing asset, in addition to the interest payment. SWIFT = PRII |
| 利率调整（interest rate adjustment） | 浮动或可调利率证券票面利率的预定调整。<br>Scheduled change to the coupon rate for a floating or adjustable rate security. |
| 中介证券分配（intermediate securities distribution） | 分配中介证券或赋予持有人参与未来事件之权利的特权的公司行动。<br>corporate action involving the distribution of intermediate securities or privilege that gives the holder the right to take part in a future event |
| 退市消息（listing status delisting message） | 证券不再符合交易所上市要求、被从正式报价板移除的消息。<br>Security is no longer able to comply with the listing requirements of a stock exchange and is removed from official board quotation. |
| 零股要约（odd lot offer） | 发行人向零股持有人发出的要约：可按市价进行免佣交易、卖出零股或买入凑整。<br>Offer by issuer to allow holders of an odd lot of a security to order a commission-free transaction at market price, to sell the odd lot, or to buy an amount of shares which will bring the position to a round lot (board lot). SWIFT = ODLT |
| 同等权益行动（pari-passu action） | 不同特征的证券在各方面变得完全相同（同等权益）时发生的公司行动。<br>corporate action that occurs when securities with different characteristics become identical in all respects |
| 部分赎回并削减面值行动（partial redemption with reduction of nominal value action） | 在预定最终到期日前部分赎回证券并削减其面值的公司行动。<br>corporate action that involves redemption of securities in part before their scheduled final maturity date with reduction of the nominal value of the securities |
| 部分赎回不削减面值行动（partial redemption without reduction of nominal value action） | 在预定最终到期日前部分赎回证券但不削减面值的公司行动。<br>corporate action that involves redemption of securities in part before their scheduled final maturity date with no reduction in nominal value |
| 合并后证券交换（post-merger securities exchange） | 因两家或多家公司合并、由发行人发起的流通证券交换（可包括期权）。<br>corporate action that involves the exchange of outstanding securities, initiated by the issuer which may include options, as the result of two or more companies combining assets, that is, an external, third party company |
| 回售赎回行动（put redemption action） | 持有人按发行条款选择提前赎回证券、不削减面值的公司行动。<br>corporate action involving early redemption of a security at the election of the holder subject to the terms and condition of the issue with no reduction in nominal value |
| 到期赎回行动（redemption at maturity action） | 在最终到期日对某次发行的全部流通证券进行赎回的公司行动。<br>corporate action that involves redemption of an entire issue outstanding of securities at final maturity |
| 重新计值行动（redenomination action） | 重新表述证券计值单位（货币和/或面值）的公司行动。<br>corporate action by which the unit (currency and/or nominal) of a security is restated |
| 回购要约（repurchase offer） | 发行公司向现有股东发出的回购股权或可转换为股权之其他证券的要约。<br>corporate action in which an offer is made to existing shareholders by the issuing company to repurchase equity or other securities convertible into equity |
| 并股（reverse stock split） | 在不改变股东权益或总市值的情况下减少公司流通股数量的公司行动。<br>corporate action involving a decrease in a company's number of outstanding equities without any change in the shareholder's equity or the aggregate market value at the time of the split |
| 权利行权事件（rights exercise event） | 行使购买股份之权利的事件，属持有人一方的行动。<br>Exercising the right to purchase the shares. Furhter Notes: This is an action on the part of the holder. SWIFT: Call/exercise on nil-paid securities/rights resulting from a rights distribution (RHDI) (To be used for the second event in case rights issue is dealt with in 2 events, first event being the RHDI). |
| 股本溢价股息行动（shares premium dividend action） | 从股本溢价储备中向股东支付现金的公司行动。<br>corporate action that pays shareholders an amount in cash issued from the shares premium reserve |
| 股票股息行动（stock dividend action） | 以发行公司股票形式向股东分配股息的公司行动。<br>corporate action that involves distribution of a dividend to shareholders in the form of equities of the issuing corporation |
| 拆股（stock split） | 在不改变股东权益或总市值的情况下增加公司流通股数量的公司行动。<br>corporate action involving an increase in a corporation's number of outstanding equities without any change in the shareholder's equity or the aggregate market value at the time of the split |
| 要约收购（tender offer） | 通常由第三方向股东发出的、请求其出售（投标）或交换所持股票的要约。<br>corporate action involving an offer made to shareholders, normally by a third party, requesting them to sell (tender) or exchange their equities |
| 交易状态活跃消息（trading status active message） | 证券交易已开始、或在暂停后恢复交易的消息。<br>Trading in security has commenced or security has been re-activated after a supsension in trading. |
| 交易状态消息（trading status message） | 关于交易状态的消息。<br>A message about trading status. |
| 交易状态暂停消息（trading status suspended message） | 证券交易已被暂停的消息。<br>Trading in the security has been suspended. |
| 认股权证行权行动（warrant exercise action） | 向持有人提供按预定价格买入（认购权证）或卖出（认沽权证）特定数量股票、现金或商品之选择权的公司行动。<br>corporate action that offers holders the option to buy (call warrant) or to sell (put warrant) a specific amount of stock, cash, or commodity, at a predetermined price, during a predetermined period of time (which usually corresponds to the life of the issue) |
| 无价值证券行动（worthless security action） | 涉及将无价值证券核销的公司行动。<br>corporate action that involves booking out of valueless securities |

以下按类逐个展开：每个类给出继承关系、相关属性与公理约定；子类在父类之下降一级编号。

### 2.1 债券违约事件（bond default event）

定义：表明发行人未能履行债券协议中定义为违约事件之义务、且未予补救的公司行动。

- 父类：**强制性公司行动（MandatoryCorporateAction）**、**债务违约（ObligationDefault）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **适用于（appliesTo）** | — | — |

公理：

- **适用于（appliesTo）**至少有一个取值，类型是**债券（Bond）**。

### 2.2 红股发行（bonus issue）

定义：发行人按持有比例向证券持有人免费赠予额外资产的公司行动。

- 父类：**强制性公司行动（MandatoryCorporateAction）**

### 2.3 对中介证券的催缴（call on intermediate securities）

定义：对未缴款证券或中介证券分配产生的中介证券进行催缴或行权的公司行动。

- 父类：**带选择的强制性公司行动（MandatoryWithChoiceCorporateAction）**

### 2.4 股份注销（cancellation of shares）

定义：股份的注销，仅适用于未公开发行的股份（即库存股）。

- 父类：**公司行动（CorporateAction）**

### 2.5 资本分配（capital distribution）

定义：从发行人资本账户向股东支付现金的公司行动。

- 父类：**自愿性公司行动（VoluntaryCorporateAction）**
- 直接子类：**红股计划分配（bonus share plan distribution）**

#### 2.5.1 红股计划分配（bonus share plan distribution）

定义：从公司股本溢价储备中发行股份、视为资本分配而非收益发放的事件。

- 父类：**资本分配（capital distribution）**

### 2.6 资本利得分配（capital gains distribution）

定义：将出售公司资产所得利润分配给股东的公司行动。

- 父类：**自愿性公司行动（VoluntaryCorporateAction）**

### 2.7 现金股息行动（cash dividend action）

定义：按持股比例向股东分配现金的公司行动。

- 父类：**强制性公司行动（MandatoryCorporateAction）**

### 2.8 最小可交易单位变更（change to smallest negotiable unit）

定义：修改股份最小可交易单位以获得新的可交易单位（SWIFT：SMAL）。

- 父类：**公司行动（CorporateAction）**

### 2.9 转换行动（conversion action）

定义：将证券（通常为可转换债券或优先股）转换为另一形式证券（通常为普通股）的公司行动。

- 父类：**自愿性公司行动（VoluntaryCorporateAction）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **转换自（converts from）** | 标识转换前的证券。 | 值域：证券 |
| **转换为（converts to）** | 标识转换后的证券。 | 值域：证券 |

公理：

- **转换为（converts to）**至少有一个取值，类型是**证券（Security）**。
- **转换自（converts from）**至少有一个取值，类型是**证券（Security）**。

### 2.10 转换暂停行动（conversion suspension action）

定义：暂停证券转换，通常在会议召开前数周（SWIFT：SCOP）。

- 父类：**公司行动（CorporateAction）**

### 2.11 公司行动义务（corporate action obligation）

定义：与持有某证券相关的义务。

- 父类：**公司行动（CorporateAction）**、**责任（Duty）**
- 直接子类：**公司行动付款义务（corporate action payment obligation）**、**公司行动证券交付义务（corporate action securities delivery obligation）**

#### 2.11.1 公司行动付款义务（corporate action payment obligation）

定义：公司行动情境中支付款项的义务。

- 父类：**公司行动义务（corporate action obligation）**

#### 2.11.2 公司行动证券交付义务（corporate action securities delivery obligation）

定义：公司行动情境中交付某证券的义务；现金对价与证券对价均可表示为合同义务。

- 父类：**公司行动义务（corporate action obligation）**

### 2.12 公司状态变更事件（corporate change of status event）

定义：某证券状态的某种变更。

- 父类：**公司行动（CorporateAction）**、**生命周期事件（LifecycleEvent）**
- 直接子类：**证券交易状态变更事件（change of security trading status event）**

#### 2.12.1 证券交易状态变更事件（change of security trading status event）

定义：可交易证券的交易状态发生变化的事件。

- 父类：**公司状态变更事件（corporate change of status event）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **适用于（appliesTo）** | — | — |

公理：

- **适用于（appliesTo）**至少有一个取值，类型是**证券交易状态（SecurityTradingStatus）**。

### 2.13 息票剥离（coupon strip）

定义：将未来付息日的利息息票与授予持有人本金权利的证券本金分离的过程。

- 父类：**公司行动（CorporateAction）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **适用于（appliesTo）** | — | — |

公理：

- **适用于（appliesTo）**至少有一个取值，类型是**债券（Bond）**。

### 2.14 减值行动（decrease in value action）

定义：导致股份面值或基金资产价值减少的公司行动。

- 父类：**强制性公司行动（MandatoryCorporateAction）**

### 2.15 股息选择权行动（dividend option action）

定义：向股东分配股息、股东可选择收取形式的公司行动。

- 父类：**带选择的强制性公司行动（MandatoryWithChoiceCorporateAction）**

### 2.16 股息再投资行动（dividend reinvestment action）

定义：持有人可保留现金或将现金再投资为发行公司额外股票的股息支付行动。

- 父类：**带选择的强制性公司行动（MandatoryWithChoiceCorporateAction）**

### 2.17 抽签赎回（drawing）

定义：在证券预定最终到期日前部分赎回。

- 父类：**强制性公司行动（MandatoryCorporateAction）**

### 2.18 荷兰式拍卖（dutch auction）

定义：由希望收购某证券的参与方发起的公司行动。

- 父类：**自愿性公司行动（VoluntaryCorporateAction）**

### 2.19 交换行动（exchange action）

定义：以持仓换取其他证券和/或现金的公司行动。

- 父类：**公司行动（CorporateAction）**

### 2.20 正式要约（formal offer）

定义：向持有人、潜在持有人或其他利益相关方发出的、达成对参与方具有或将具有法律约束力之交易的要约。

- 父类：**自愿性公司行动（VoluntaryCorporateAction）**

### 2.21 全额提前赎回行动（full call early redemption action）

定义：在到期前对某次发行的全部流通证券进行赎回的公司行动。

- 父类：**强制性公司行动（MandatoryCorporateAction）**

### 2.22 付息行动（interest payment action）

定义：向计息资产持有人分配定期利息的公司行动。

- 父类：**强制性公司行动（MandatoryCorporateAction）**
- 直接子类：**实物付息（interest payment in kind）**、**附本金付息（interest payment with principal）**

#### 2.22.1 实物付息（interest payment in kind）

定义：以现金以外的任何形式向计息资产持有人分配的利息支付（SWIFT：PINK）。

- 父类：**付息行动（interest payment action）**

#### 2.22.2 附本金付息（interest payment with principal）

定义：除利息支付外，同时支付计息资产部分本金的付款（SWIFT：PRII）。

- 父类：**付息行动（interest payment action）**

### 2.23 利率调整（interest rate adjustment）

定义：浮动或可调利率证券票面利率的预定调整。

- 父类：**强制性公司行动（MandatoryCorporateAction）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **适用于（appliesTo）** | — | — |

公理：

- **适用于（appliesTo）**至少有一个取值，类型是**浮动票息债券（VariableCouponBond）**。

### 2.24 中介证券分配（intermediate securities distribution）

定义：分配中介证券或赋予持有人参与未来事件之权利的特权的公司行动。

- 父类：**强制性公司行动（MandatoryCorporateAction）**
- 直接子类：**红利认股权发行（bonus rights issue）**

#### 2.24.1 红利认股权发行（bonus rights issue）

定义：将认股权免费授予相关股份持有人的配股发行。

- 父类：**中介证券分配（intermediate securities distribution）**

### 2.25 退市消息（listing status delisting message）

定义：证券不再符合交易所上市要求、被从正式报价板移除的消息。

- 父类：**通知（Notice）**

### 2.26 零股要约（odd lot offer）

定义：发行人向零股持有人发出的要约：可按市价进行免佣交易、卖出零股或买入凑整。

- 父类：**自愿性公司行动（VoluntaryCorporateAction）**

### 2.27 同等权益行动（pari-passu action）

定义：不同特征的证券在各方面变得完全相同（同等权益）时发生的公司行动。

- 父类：**强制性公司行动（MandatoryCorporateAction）**

### 2.28 部分赎回并削减面值行动（partial redemption with reduction of nominal value action）

定义：在预定最终到期日前部分赎回证券并削减其面值的公司行动。

- 父类：**公司行动（CorporateAction）**

### 2.29 部分赎回不削减面值行动（partial redemption without reduction of nominal value action）

定义：在预定最终到期日前部分赎回证券但不削减面值的公司行动。

- 父类：**公司行动（CorporateAction）**

### 2.30 合并后证券交换（post-merger securities exchange）

定义：因两家或多家公司合并、由发行人发起的流通证券交换（可包括期权）。

- 父类：**公司行动（CorporateAction）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **转换自（converts from）** | 标识转换前的证券。 | 值域：证券 |
| **转换为（converts to）** | 标识转换后的证券。 | 值域：证券 |
| **具有货币数量（hasMonetaryAmount）** | — | — |

公理：

- **具有货币数量（hasMonetaryAmount）**可以有 0 个或多个**货币数量（MonetaryAmount）**。
- **转换为（converts to）**至少有一个取值，类型是**证券（Security）**。
- **转换自（converts from）**至少有一个取值，类型是**证券（Security）**。

### 2.31 回售赎回行动（put redemption action）

定义：持有人按发行条款选择提前赎回证券、不削减面值的公司行动。

- 父类：**自愿性公司行动（VoluntaryCorporateAction）**

### 2.32 到期赎回行动（redemption at maturity action）

定义：在最终到期日对某次发行的全部流通证券进行赎回的公司行动。

- 父类：**强制性公司行动（MandatoryCorporateAction）**

### 2.33 重新计值行动（redenomination action）

定义：重新表述证券计值单位（货币和/或面值）的公司行动。

- 父类：**强制性公司行动（MandatoryCorporateAction）**

### 2.34 回购要约（repurchase offer）

定义：发行公司向现有股东发出的回购股权或可转换为股权之其他证券的要约。

- 父类：**自愿性公司行动（VoluntaryCorporateAction）**

### 2.35 并股（reverse stock split）

定义：在不改变股东权益或总市值的情况下减少公司流通股数量的公司行动。

- 父类：**强制性公司行动（MandatoryCorporateAction）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **适用于（appliesTo）** | — | — |

公理：

- **适用于（appliesTo）**至少有一个取值，类型是**股份（Share）**。
- 与**拆股（stock split）**互斥：同一个体不能同时属于两者。

### 2.36 权利行权事件（rights exercise event）

定义：行使购买股份之权利的事件，属持有人一方的行动。

- 父类：**公司行动（CorporateAction）**

### 2.37 股本溢价股息行动（shares premium dividend action）

定义：从股本溢价储备中向股东支付现金的公司行动。

- 父类：**带选择的强制性公司行动（MandatoryWithChoiceCorporateAction）**

### 2.38 股票股息行动（stock dividend action）

定义：以发行公司股票形式向股东分配股息的公司行动。

- 父类：**强制性公司行动（MandatoryCorporateAction）**

### 2.39 拆股（stock split）

定义：在不改变股东权益或总市值的情况下增加公司流通股数量的公司行动。

- 父类：**强制性公司行动（MandatoryCorporateAction）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **适用于（appliesTo）** | — | — |

公理：

- **适用于（appliesTo）**至少有一个取值，类型是**股份（Share）**。

### 2.40 要约收购（tender offer）

定义：通常由第三方向股东发出的、请求其出售（投标）或交换所持股票的要约。

- 父类：**自愿性公司行动（VoluntaryCorporateAction）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **适用于（appliesTo）** | — | — |

公理：

- **适用于（appliesTo）**至少有一个取值，类型是**股份（Share）**。

### 2.41 交易状态消息（trading status message）

定义：关于交易状态的消息。

- 父类：**通知（Notice）**
- 直接子类：**交易状态活跃消息（trading status active message）**、**交易状态暂停消息（trading status suspended message）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **关于（isAbout）** | — | — |
| **引用（refersTo）** | — | — |

公理：

- **关于（isAbout）**至少有一个取值，类型是**证券交易状态（SecurityTradingStatus）**。
- **引用（refersTo）**至少有一个取值，类型是**证券（Security）**。

#### 2.41.1 交易状态活跃消息（trading status active message）

定义：证券交易已开始、或在暂停后恢复交易的消息。

- 父类：**交易状态消息（trading status message）**

#### 2.41.2 交易状态暂停消息（trading status suspended message）

定义：证券交易已被暂停的消息。

- 父类：**交易状态消息（trading status message）**

### 2.42 认股权证行权行动（warrant exercise action）

定义：向持有人提供按预定价格买入（认购权证）或卖出（认沽权证）特定数量股票、现金或商品之选择权的公司行动。

- 父类：**公司行动（CorporateAction）**

### 2.43 无价值证券行动（worthless security action）

定义：涉及将无价值证券核销的公司行动。

- 父类：**强制性公司行动（MandatoryCorporateAction）**

## 3. 依赖（owl:imports，13 个）

本本体通过 `owl:imports` 引入以下本体，各项的中文名称与简介如下：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `CAE/CorporateEvents/CorporateActions.rdf` | 企业行动本体（Corporate Actions Ontology） | 定义企业行动（corporate action）：上市公司发起的、影响股东或证券的事件，如分红、拆股、并购。 |
| `FBC/DebtAndEquities/CreditEvents.rdf` | 信用事件本体（Credit Events Ontology） | 定义信用事件（credit event）：破产、拒付、重组等会触发信用衍生品结算的事件类型。 |
| `FBC/FinancialInstruments/FinancialInstruments.rdf` | 金融工具本体（Financial Instruments Ontology） | FIBO 核心本体之一，定义金融工具（financial instrument）的通用概念：可交易、代表某种权利义务的合同工具，是证券、衍生品等具体工具的共同基础。 |
| `FND/Accounting/CurrencyAmount.rdf` | 货币金额本体（Currency Amount Ontology） | 定义「金额＋币种」的货币金额（currency amount）表示，是 FIBO 中表达价格、债务金额、付款额等一切带币种数值的基础构件。 |
| `FND/Arrangements/Lifecycles.rdf` | 生命周期本体（Lifecycles Ontology） | 定义生命周期、生命周期阶段与状态转移，用于描述合同、金融工具、机构从创设到终止的演化过程。 |
| `FND/Law/LegalCapacity.rdf` | 法律能力本体（Legal Capacity Ontology） | 定义法律能力、缔约能力、签章权等概念，刻画主体从事法律行为的资格。 |
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `MD/TemporalCore/SecurityTradingStatuses.rdf` | 证券交易状态时序本体（Security Trading Statuses Ontology） | 定义证券交易状态（正常、停牌等）随时间的表示。 |
| `SEC/Debt/Bonds.rdf` | 债券本体（Bonds Ontology） | 定义债券（bond）：期限、票面利率、付息方式与偿还结构。 |
| `SEC/Equities/EquityInstruments.rdf` | 股权工具本体（Equity Instruments Ontology） | 定义股票等股权工具：普通股、优先股及其附带的权利。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |
| `https://www.omg.org/spec/Commons/ContextualDesignators/` | OMG 通用语境指称本体（OMG Commons Contextual Designators） | Commons 库中的语境指称本体，定义「在某个语境下指代某物的名称/符号」，是地址、账户号码等语境相关标识的基础。 |
| `https://www.omg.org/spec/Commons/Documents/` | OMG 通用文档本体（OMG Commons Documents） | Commons 库中的文档本体，定义文档及其组成部分的通用概念。 |

## 4. 文件

- 官方 RDF/XML：`SecurityRelatedCorporateActions.rdf`
- 中文 Turtle：`SecurityRelatedCorporateActions.ttl`
- 结构图：`SecurityRelatedCorporateActions-structure.png` / `SecurityRelatedCorporateActions-structure.svg`