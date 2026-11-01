# 权利与权证本体（Rights and Warrants Ontology）结构与公理说明

本文档对应 `RightsAndWarrants.rdf` / `RightsAndWarrants.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `RightsAndWarrants-structure.png`（`RightsAndWarrants-structure.svg` 为可缩放版本）。

![权利与权证本体（Rights and Warrants Ontology）本体结构图](RightsAndWarrants-structure.png)

## 1. 本体概述

定义认股权证（warrant）与配股权（rights）：赋予持有人按约定价格认购证券的权利的凭证。

**在体系中的位置**：衍生品合约模块的四大基础结构本体之一。

**上下游关系**：上游继承衍生品基础与期权本体；下游关联 SEC 股权工具（权证常依附于股票或债券发行）。

**与相近概念的差别**：与期权的差别——权证由公司或发行人发行、行权会稀释股本、期限长，期权多为交易所标准化合约、行权不涉及新股发行；配股权则是面向现有股东的短期认购权。

本本体中类与类的核心关系如下（完整细节见各类小节）：

- **配股权（allotment right）** 继承 **股票衍生品（EquityDerivative）**
- **配股权（allotment right）** 继承 **权益凭证（Entitlement）**
- **配股权公式（allotment right formula）** 继承 **表达式（Expression）**
- **基于障碍工具的迷你期货凭证（barrier instrument-based mini-future certificate）** 继承 **迷你期货凭证（mini-future certificate）**
- **标的障碍迷你期货凭证（barrier underlying mini-future certificate）** 继承 **迷你期货凭证（mini-future certificate）**
- **篮子权证（basket warrant）** 继承 **权证（warrant）**
- **债券购买权（bond purchase right）** 继承 **购买权（purchase right）**
- **债券认购权（bond subscription right）** 继承 **认购权（subscription right）**
- **认购认沽权证（call put warrant）** 继承 **认购权证（call warrant）**
- **认购认沽权证（call put warrant）** 继承 **认沽权证（put warrant）**
- **认购权证（call warrant）** 继承 **权证（warrant）**
- **组合工具购买权（combined instruments purchase right）** 继承 **购买权（purchase right）**
- 其余 43 条关系从略。

## 2. 类（Class）

| 类（Class） | 定义（Definition） |
|---|---|
| 公司权证（CompanyWarrant） | 由公司自身发行的权证，行权时通常涉及公司发行新股。 |
| 配股权（allotment right） | 授予现有证券持有人的特权，使其有权免费获得新证券。<br>privileges allotted to existing security holders, entitling them to receive new securities free of charge |
| 配股权公式（allotment right formula） | 用于计算配股权对应证券数量的规则，通常基于持有人所持该类工具的数量。<br>rule applied to calculate the number of securities for an allotment right, typically based on the number of these instruments that the holder holds |
| 基于障碍工具的迷你期货凭证（barrier instrument-based mini-future certificate） | 在产品存续期内障碍工具交易价格水平被突破时立即到期的迷你期货凭证。<br>mini-future certificate that immediately expires if the barrier instrument trading price level is breached during product lifetime |
| 标的障碍迷你期货凭证（barrier underlying mini-future certificate） | 在产品存续期内标的价格突破障碍水平时立即到期的迷你期货凭证。<br>mini-future certificate that immediately expires if the barrier underlying level is breached during product lifetime |
| 篮子权证（basket warrant） | 允许持有人在规定期间内按指定价格购买一揽子或一组资产的权证。<br>warrant that permits the holder to acquire a package or group of assets at a specified price during a specified period |
| 债券购买权（bond purchase right） | 赋予潜在被收购方债券持有人以大幅折价购买该公司或任何收购该公司者之债券的权利的反收购安排。<br>purchase right that gives a prospective acquiree's bondholders the right to buy bonds of the firm or bonds of anyone who acquires the firm at a deep discount to their fair market value |
| 债券认购权（bond subscription right） | 授予现有债券持有人以通常低于当时市价的价格认购新证券的认购权。<br>subscription right entitling existing bond holders to subscribe to new securities at a price normally lower than the prevailing market price |
| 认购认沽权证（call put warrant） | 未明确认购或认沽特征、或明确同时包含认购和认沽特征的权证。<br>warrant that either does not specify call or put features, or that explicitly includes both a call and put feature |
| 认购权证（call warrant） | 赋予买方（持有人）在规定期间内按指定价格购买特定标的资产的权利（而非义务）的权证。<br>warrant giving the buyer (holder) the right, but not the obligation, to acquire specific underlying assets during a specified period at a specified price |
| 组合工具购买权（combined instruments purchase right） | 赋予潜在被收购方多种证券持有人购买该公司或任何收购该公司者之证券的权利的反收购安排。<br>purchase right that gives a prospective acquiree's holders of multiple securities the right to buy securities of the firm or securities of anyone who acquires the firm at a deep discount to their fair market value |
| 组合工具认购权（combined instruments subscription right） | 授予现有多种证券持有人以通常低于当时市价的价格认购新证券的认购权。<br>subscription right entitling existing holders of multiple securities to subscribe to new securities at a price normally lower than the prevailing market price |
| 商品权证（commodity warrant） | 允许持有人在规定期间内按指定价格购买指定数量商品的权证。<br>warrant that permits the holder to acquire a specified amount of a commodity during a specified period at a specified price |
| 普通可转换股购买权（common convertible share purchase right） | 赋予潜在被收购方普通可转换股股东购买该公司或任何收购该公司者之普通可转换股的权利的购买权。<br>purchase right that gives a prospective acquiree's common, convertible shareholders the right to buy common, convertible shares of the firm or common, convertible shares of anyone who acquires the firm at a deep discount to their fair market value |
| 普通可转换股认购权（common convertible share subscription right） | 授予现有普通可转换股股东以通常低于当时市价的价格认购新证券的认购权。<br>subscription right entitling existing common convertible shareholders to subscribe to new securities at a price normally lower than the prevailing market price |
| 普通股购买权（common share purchase right） | 赋予潜在被收购方普通股股东购买该公司或任何收购该公司者之普通股的权利的购买权。<br>purchase right that gives a prospective acquiree's common shareholders the right to buy common shares of the firm or common shares of anyone who acquires the firm at a deep discount to their fair market value |
| 普通股认购权（common share subscription right） | 授予现有普通股股东以通常低于当时市价的价格认购新证券的认购权。<br>subscription right entitling existing common shareholders to subscribe to new securities at a price normally lower than the prevailing market price |
| 恒定杠杆凭证（constant leverage certificate） | 将开放式凭证结构与无固定期限的杠杆期权相结合、使杠杆在无期限条件下可用的权益凭证。<br>entitlement that combines the structure of an open-end certificate with a leverage option with no fixed term, making leverage available without a term restriction, without a knock-out barrier dependency |
| 备兑权证（covered warrant） | 赋予持有人按指定价格买入（认购权证）或卖出（认沽权证）标的资产的权利（而非义务）的权证，通常由第三方发行。<br>warrant that gives the holder the right, but not the obligation, to buy (call warrant) or to sell (put warrant) an underlying asset at a specified price (the strike or exercise price) by a predetermined date, issued without an accompanying security by a third party that holds as many securities as would be required if all the warrants are exercised |
| 货币权证（currency warrant） | 允许持有人在规定期间内按指定汇率购买指定金额某种货币的权证。<br>warrant that permits the holder to acquire a specified amount in a certain currency at a specified exchange rate during a specified period |
| 债务权证（debt warrant） | 允许持有人在规定期间内按指定价格购买指定数量债务工具或相关债务指标的权证。<br>warrant that permits the holder to acquire a specified amount of a debt instrument or related debt observable a specified period at a specified price |
| 股权权证（equity warrant） | 允许持有人在规定期间内按指定价格购买指定数量权益工具的权证。<br>warrant that permits the holder to acquire a specified amount of an equity instrument during a specified period at a specified price |
| 交易所交易权证（exchange-traded warrant） | 在证券交易所挂牌的权证。<br>warrant that is listed on a securities exchange |
| 奇异权证（exotic warrant） | 赋予持有人在非标准或复杂条件下买入（有时卖出）标的资产的权利（而非义务）的权证。<br>warrant that gives the holder the right (but not the obligation) to buy (or sometimes sell) an underlying asset under non-standard or complex conditions, often involving additional features not found in a plain vanilla (standard) warrant |
| 指数权证（index warrant） | 允许持有人在规定期间内按指定价格购买基于指数表现之指定金额的权证。<br>warrant that permits the holder to acquire a specified amount based on the performance of an index during a specified period at a specified price |
| 做多迷你期货凭证（long mini-future certificate） | 通常授予持有人在规定期间内按指定价格购买特定标的资产之权利的迷你期货凭证。<br>mini-future certificate that typically entitles the holder to acquire specific underlying assets during a specified period at a specified price |
| 迷你期货凭证（mini-future certificate） | 将开放式凭证结构与无固定期限的杠杆期权相结合、使杠杆在无期限条件下可用的权益凭证。<br>entitlement that combines the structure of an open-end certificate with a leverage option with no fixed term, making leverage available without a term restriction, and whose payoff depends on whether or not the underlying asset has reached or exceeded a predetermined price |
| 裸权证（naked warrant） | 赋予持有人按指定价格买入（认购权证）或卖出（认沽权证）标的资产的权利（而非义务）、但不伴随标的持有的权证。<br>warrant that gives the holder the right, but not the obligation, to buy (call warrant) or to sell (put warrant) an underlying asset at a specified price (the strike or exercise price) by a predetermined date, issued without an accompanying security by a third party that does not hold as many securities as would be required if all the warrants are exercised |
| 永续权证（perpetual warrant） | 无到期日的权证，赋予持有人按指定价格买入（认购权证）或卖出（认沽权证）标的资产的权利（而非义务）。<br>warrant without an expiration date, giving the holder the right, but not the obligation, to buy (call warrant) or to sell (put warrant) an underlying asset at a certain strike price |
| 优先可转换股购买权（preferred convertible share purchase right） | 赋予潜在被收购方优先可转换股股东购买该公司或任何收购该公司者之优先可转换股的权利的购买权。<br>purchase right that gives a prospective acquiree's preferred, convertible shareholders the right to buy preferred, convertible shares of the firm or preferred, convertible shares of anyone who acquires the firm at a deep discount to their fair market value |
| 优先可转换股认购权（preferred convertible share subscription right） | 授予现有优先可转换股股东以通常低于当时市价的价格认购新证券的认购权。<br>subscription right entitling existing preferred, convertible shareholders to subscribe to new securities at a price normally lower than the prevailing market price |
| 优先股购买权（preferred share purchase right） | 赋予潜在被收购方优先股股东购买该公司或任何收购该公司者之优先股的权利的购买权。<br>purchase right that gives a prospective acquiree's preferred shareholders the right to buy preferred shares of the firm or preferred shares of anyone who acquires the firm at a deep discount to their fair market value |
| 优先股认购权（preferred share subscription right） | 授予现有优先股股东以通常低于当时市价的价格认购新证券的认购权。<br>subscription right entitling existing preferred shareholders to subscribe to new securities at a price normally lower than the prevailing market price |
| 私募权证（private warrant） | 不可交易的权证。<br>warrant that is not tradable |
| 公募权证（public warrant） | 可在场外（OTC）或通过交易所交易的权证。<br>warrant that may be traded over the counter (OTC) or through an exchange |
| 购买权（purchase right） | 一种反收购安排：赋予潜在被收购方股东以折扣价购买该公司或任何收购该公司者之股份的权利。<br>anti-takeover device that gives a prospective acquiree's shareholders the right to buy shares of the firm or shares of anyone who acquires the firm at a deep discount to their fair market value |
| 认沽权证（put warrant） | 赋予买方（持有人）卖出指定资产（即以标的资产换取现金）的权利（而非义务）的权证。<br>warrant giving the buyer (holder) the right, but not the obligation, to sell the assets specified (i.e., acquire cash in exchange for the underlying assets, such as stock) back to the issuer at a fixed price or formula, on or before a specified date |
| 做空迷你期货凭证（short mini-future certificate） | 授予持有人以特定标的资产换取现金之权利的迷你期货凭证。<br>mini-future certificate that entitles the holder to acquire cash in exchange for specific underlying assets |
| 结构化权证（structured warrant） | 在交易所挂牌的权证，为投资者提供不直接购买标的资产即可参与其价格表现的途径。<br>warrant that is listed on an exchange, offering investors a way to participate in the price performance of an underlying asset without buying it directly |
| 认购权（subscription right） | 授予现有证券持有人的特权，使其有权以通常低于当时市价的价格认购新证券。<br>privileges allotted to existing security holders, entitling them to subscribe to new securities at a price normally lower than the prevailing market price |
| 传统权证（traditional warrant） | 赋予持有人按指定价格买入（认购权证）或卖出（认沽权证）标的资产的权利（而非义务）的权证。<br>warrant that gives the holder the right, but not the obligation, to buy (call warrant) or to sell (put warrant) an underlying asset at a specified price (the strike or exercise price) by a predetermined date, issued by the issuer of the underlying instrument |
| 权证（warrant） | 允许持有人在规定期间内按指定价格购买指定数量金融工具、商品、货币或其他资产的权益凭证。<br>entitlement that permits the holder to purchase a specified amount of a financial instrument, commodity, currency or other asset during a specified period at a specified price |

以下按类逐个展开：每个类给出继承关系、相关属性与公理约定；子类在父类之下降一级编号。

### 2.1 公司权证（CompanyWarrant）

定义：由公司自身发行的权证，行权时通常涉及公司发行新股。

### 2.2 配股权（allotment right）

定义：授予现有证券持有人的特权，使其有权免费获得新证券。

- 父类：**股票衍生品（EquityDerivative）**、**权益凭证（Entitlement）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有表达式（hasExpression）** | — | — |

公理：

- **具有表达式（hasExpression）**至少有一个取值，类型是**配股权公式（allotment right formula）**。

### 2.3 配股权公式（allotment right formula）

定义：用于计算配股权对应证券数量的规则，通常基于持有人所持该类工具的数量。

- 父类：**表达式（Expression）**

### 2.4 恒定杠杆凭证（constant leverage certificate）

定义：将开放式凭证结构与无固定期限的杠杆期权相结合、使杠杆在无期限条件下可用的权益凭证。

- 父类：**证券类衍生品（SecurityBasedDerivative）**、**权益凭证（Entitlement）**、**期权（Option）**

### 2.5 迷你期货凭证（mini-future certificate）

定义：将开放式凭证结构与无固定期限的杠杆期权相结合、使杠杆在无期限条件下可用的权益凭证。

- 父类：**障碍期权（BarrierOption）**、**证券类衍生品（SecurityBasedDerivative）**、**权益凭证（Entitlement）**
- 直接子类：**基于障碍工具的迷你期货凭证（barrier instrument-based mini-future certificate）**、**标的障碍迷你期货凭证（barrier underlying mini-future certificate）**、**做多迷你期货凭证（long mini-future certificate）**、**做空迷你期货凭证（short mini-future certificate）**

#### 2.5.1 基于障碍工具的迷你期货凭证（barrier instrument-based mini-future certificate）

定义：在产品存续期内障碍工具交易价格水平被突破时立即到期的迷你期货凭证。

- 父类：**迷你期货凭证（mini-future certificate）**

#### 2.5.2 标的障碍迷你期货凭证（barrier underlying mini-future certificate）

定义：在产品存续期内标的价格突破障碍水平时立即到期的迷你期货凭证。

- 父类：**迷你期货凭证（mini-future certificate）**

#### 2.5.3 做多迷你期货凭证（long mini-future certificate）

定义：通常授予持有人在规定期间内按指定价格购买特定标的资产之权利的迷你期货凭证。

- 父类：**迷你期货凭证（mini-future certificate）**

#### 2.5.4 做空迷你期货凭证（short mini-future certificate）

定义：授予持有人以特定标的资产换取现金之权利的迷你期货凭证。

- 父类：**迷你期货凭证（mini-future certificate）**

### 2.6 购买权（purchase right）

定义：一种反收购安排：赋予潜在被收购方股东以折扣价购买该公司或任何收购该公司者之股份的权利。

- 父类：**权益凭证（Entitlement）**
- 直接子类：**债券购买权（bond purchase right）**、**组合工具购买权（combined instruments purchase right）**、**普通可转换股购买权（common convertible share purchase right）**、**普通股购买权（common share purchase right）**、**优先可转换股购买权（preferred convertible share purchase right）**、**优先股购买权（preferred share purchase right）**

#### 2.6.1 债券购买权（bond purchase right）

定义：赋予潜在被收购方债券持有人以大幅折价购买该公司或任何收购该公司者之债券的权利的反收购安排。

- 父类：**购买权（purchase right）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有标的（hasUnderlier）** | — | — |

公理：

- **具有标的（hasUnderlier）**至少有一个取值，该取值满足：**由…扮演（is played by）**至少有一个取值，类型是**债券（Bond）**。

#### 2.6.2 组合工具购买权（combined instruments purchase right）

定义：赋予潜在被收购方多种证券持有人购买该公司或任何收购该公司者之证券的权利的反收购安排。

- 父类：**购买权（purchase right）**

#### 2.6.3 普通可转换股购买权（common convertible share purchase right）

定义：赋予潜在被收购方普通可转换股股东购买该公司或任何收购该公司者之普通可转换股的权利的购买权。

- 父类：**购买权（purchase right）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有标的（hasUnderlier）** | — | — |

公理：

- **具有标的（hasUnderlier）**至少有一个取值，该取值满足：**由…扮演（is played by）**至少有一个取值，类型是**可转换普通股（ConvertibleCommonShare）**。

#### 2.6.4 普通股购买权（common share purchase right）

定义：赋予潜在被收购方普通股股东购买该公司或任何收购该公司者之普通股的权利的购买权。

- 父类：**购买权（purchase right）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有标的（hasUnderlier）** | — | — |

公理：

- **具有标的（hasUnderlier）**至少有一个取值，该取值满足：**由…扮演（is played by）**至少有一个取值，类型是**普通股（CommonShare）**。

#### 2.6.5 优先可转换股购买权（preferred convertible share purchase right）

定义：赋予潜在被收购方优先可转换股股东购买该公司或任何收购该公司者之优先可转换股的权利的购买权。

- 父类：**购买权（purchase right）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有标的（hasUnderlier）** | — | — |

公理：

- **具有标的（hasUnderlier）**至少有一个取值，该取值满足：**由…扮演（is played by）**至少有一个取值，类型是**可转换优先股（ConvertiblePreferredShare）**。

#### 2.6.6 优先股购买权（preferred share purchase right）

定义：赋予潜在被收购方优先股股东购买该公司或任何收购该公司者之优先股的权利的购买权。

- 父类：**购买权（purchase right）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有标的（hasUnderlier）** | — | — |

公理：

- **具有标的（hasUnderlier）**至少有一个取值，该取值满足：**由…扮演（is played by）**至少有一个取值，类型是**优先股（PreferredShare）**。

### 2.7 认购权（subscription right）

定义：授予现有证券持有人的特权，使其有权以通常低于当时市价的价格认购新证券。

- 父类：**权益凭证（Entitlement）**
- 直接子类：**债券认购权（bond subscription right）**、**组合工具认购权（combined instruments subscription right）**、**普通可转换股认购权（common convertible share subscription right）**、**普通股认购权（common share subscription right）**、**优先可转换股认购权（preferred convertible share subscription right）**、**优先股认购权（preferred share subscription right）**

#### 2.7.1 债券认购权（bond subscription right）

定义：授予现有债券持有人以通常低于当时市价的价格认购新证券的认购权。

- 父类：**认购权（subscription right）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有标的（hasUnderlier）** | — | — |

公理：

- **具有标的（hasUnderlier）**至少有一个取值，该取值满足：**由…扮演（is played by）**至少有一个取值，类型是**债券（Bond）**。

#### 2.7.2 组合工具认购权（combined instruments subscription right）

定义：授予现有多种证券持有人以通常低于当时市价的价格认购新证券的认购权。

- 父类：**认购权（subscription right）**

#### 2.7.3 普通可转换股认购权（common convertible share subscription right）

定义：授予现有普通可转换股股东以通常低于当时市价的价格认购新证券的认购权。

- 父类：**认购权（subscription right）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有标的（hasUnderlier）** | — | — |

公理：

- **具有标的（hasUnderlier）**至少有一个取值，该取值满足：**由…扮演（is played by）**至少有一个取值，类型是**可转换普通股（ConvertibleCommonShare）**。

#### 2.7.4 普通股认购权（common share subscription right）

定义：授予现有普通股股东以通常低于当时市价的价格认购新证券的认购权。

- 父类：**认购权（subscription right）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有标的（hasUnderlier）** | — | — |

公理：

- **具有标的（hasUnderlier）**至少有一个取值，该取值满足：**由…扮演（is played by）**至少有一个取值，类型是**普通股（CommonShare）**。

#### 2.7.5 优先可转换股认购权（preferred convertible share subscription right）

定义：授予现有优先可转换股股东以通常低于当时市价的价格认购新证券的认购权。

- 父类：**认购权（subscription right）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有标的（hasUnderlier）** | — | — |

公理：

- **具有标的（hasUnderlier）**至少有一个取值，该取值满足：**由…扮演（is played by）**至少有一个取值，类型是**可转换优先股（ConvertiblePreferredShare）**。

#### 2.7.6 优先股认购权（preferred share subscription right）

定义：授予现有优先股股东以通常低于当时市价的价格认购新证券的认购权。

- 父类：**认购权（subscription right）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有标的（hasUnderlier）** | — | — |

公理：

- **具有标的（hasUnderlier）**至少有一个取值，该取值满足：**由…扮演（is played by）**至少有一个取值，类型是**优先股（PreferredShare）**。

### 2.8 权证（warrant）

定义：允许持有人在规定期间内按指定价格购买指定数量金融工具、商品、货币或其他资产的权益凭证。

- 父类：**权益凭证（Entitlement）**
- 直接子类：**篮子权证（basket warrant）**、**认购权证（call warrant）**、**商品权证（commodity warrant）**、**备兑权证（covered warrant）**、**货币权证（currency warrant）**、**债务权证（debt warrant）**、**奇异权证（exotic warrant）**、**指数权证（index warrant）**、**裸权证（naked warrant）**、**永续权证（perpetual warrant）**、**私募权证（private warrant）**、**公募权证（public warrant）**、**认沽权证（put warrant）**、**结构化权证（structured warrant）**、**传统权证（traditional warrant）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有行权条款（hasExerciseTerms）** | — | — |

公理：

- **具有行权条款（hasExerciseTerms）**至少有一个取值，类型是**行权条款（ExerciseTerms）**。

#### 2.8.1 篮子权证（basket warrant）

定义：允许持有人在规定期间内按指定价格购买一揽子或一组资产的权证。

- 父类：**权证（warrant）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有标的（hasUnderlier）** | — | — |

公理：

- **具有标的（hasUnderlier）**至少有一个取值，该取值满足：**由…扮演（is played by）**至少有一个取值，类型是**证券篮子（BasketOfSecurities）**。

#### 2.8.2 认购权证（call warrant）

定义：赋予买方（持有人）在规定期间内按指定价格购买特定标的资产的权利（而非义务）的权证。

- 父类：**权证（warrant）**
- 直接子类：**认购认沽权证（call put warrant）**、**股权权证（equity warrant）**

##### 2.8.2.1 认购认沽权证（call put warrant）

定义：未明确认购或认沽特征、或明确同时包含认购和认沽特征的权证。

- 父类：**认购权证（call warrant）**、**认沽权证（put warrant）**

##### 2.8.2.2 股权权证（equity warrant）

定义：允许持有人在规定期间内按指定价格购买指定数量权益工具的权证。

- 父类：**认购权证（call warrant）**、**传统权证（traditional warrant）**、**股票衍生品（EquityDerivative）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由……发行（isIssuedBy）** | — | — |

公理：

- **由……发行（isIssuedBy）**至少有一个取值，该取值满足：**由…扮演（is played by）**的所有取值只能是**股份公司（StockCorporation）**。

#### 2.8.3 商品权证（commodity warrant）

定义：允许持有人在规定期间内按指定价格购买指定数量商品的权证。

- 父类：**商品衍生品（CommodityDerivative）**、**权证（warrant）**

#### 2.8.4 备兑权证（covered warrant）

定义：赋予持有人按指定价格买入（认购权证）或卖出（认沽权证）标的资产的权利（而非义务）的权证，通常由第三方发行。

- 父类：**权证（warrant）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由……发行（isIssuedBy）** | — | — |

公理：

- **由……发行（isIssuedBy）**至少有一个取值，类型是**金融机构（FinancialInstitution）**。

#### 2.8.5 货币权证（currency warrant）

定义：允许持有人在规定期间内按指定汇率购买指定金额某种货币的权证。

- 父类：**货币衍生品（CurrencyDerivative）**、**权证（warrant）**

#### 2.8.6 债务权证（debt warrant）

定义：允许持有人在规定期间内按指定价格购买指定数量债务工具或相关债务指标的权证。

- 父类：**权证（warrant）**、**债务工具衍生品（DebtInstrumentDerivative）**

#### 2.8.7 奇异权证（exotic warrant）

定义：赋予持有人在非标准或复杂条件下买入（有时卖出）标的资产的权利（而非义务）的权证。

- 父类：**权证（warrant）**

#### 2.8.8 指数权证（index warrant）

定义：允许持有人在规定期间内按指定价格购买基于指数表现之指定金额的权证。

- 父类：**权证（warrant）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有标的（hasUnderlier）** | — | — |

公理：

- **具有标的（hasUnderlier）**至少有一个取值，该取值满足：**由…扮演（is played by）**可以有 0 个或多个**N353c645ea1b44464baa932e0a0d725b4**。

#### 2.8.9 裸权证（naked warrant）

定义：赋予持有人按指定价格买入（认购权证）或卖出（认沽权证）标的资产的权利（而非义务）、但不伴随标的持有的权证。

- 父类：**权证（warrant）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由……发行（isIssuedBy）** | — | — |

公理：

- **由……发行（isIssuedBy）**至少有一个取值，类型是**金融机构（FinancialInstitution）**。
- 与**备兑权证（covered warrant）**互斥：同一个体不能同时属于两者。

#### 2.8.10 永续权证（perpetual warrant）

定义：无到期日的权证，赋予持有人按指定价格买入（认购权证）或卖出（认沽权证）标的资产的权利（而非义务）。

- 父类：**权证（warrant）**

#### 2.8.11 私募权证（private warrant）

定义：不可交易的权证。

- 父类：**权证（warrant）**、**不可转让证券（NonNegotiableSecurity）**

#### 2.8.12 公募权证（public warrant）

定义：可在场外（OTC）或通过交易所交易的权证。

- 父类：**权证（warrant）**、**可转让证券（NegotiableSecurity）**
- 直接子类：**交易所交易权证（exchange-traded warrant）**

##### 2.8.12.1 交易所交易权证（exchange-traded warrant）

定义：在证券交易所挂牌的权证。

- 父类：**公募权证（public warrant）**、**上市证券（ListedSecurity）**

#### 2.8.13 认沽权证（put warrant）

定义：赋予买方（持有人）卖出指定资产（即以标的资产换取现金）的权利（而非义务）的权证。

- 父类：**权证（warrant）**
- 直接子类：**认购认沽权证（call put warrant）**

#### 2.8.14 结构化权证（structured warrant）

定义：在交易所挂牌的权证，为投资者提供不直接购买标的资产即可参与其价格表现的途径。

- 父类：**权证（warrant）**

#### 2.8.15 传统权证（traditional warrant）

定义：赋予持有人按指定价格买入（认购权证）或卖出（认沽权证）标的资产的权利（而非义务）的权证。

- 父类：**权证（warrant）**
- 直接子类：**股权权证（equity warrant）**

公理：

- 与**备兑权证（covered warrant）**互斥：同一个体不能同时属于两者。
- 与**裸权证（naked warrant）**互斥：同一个体不能同时属于两者。

## 3. 其他属性

以下属性未绑定到本体的具体类（定义域在外部本体或未声明）：

数据属性（Datatype Property）：

| 属性 | 定义 |
|---|---|
| **具有转换比率（has conversion ratio）** | 指明为买入或卖出特定数量证券或投资单位所需权证数量的换算系数。<br>indicates the factor used to determine the number of warrants needed in order to buy or sell a specific number of securities or investment units |
| **是否具有超额认购选择权（has oversubscribe option）** | 表明在其他权利持有人选择不认购时，该权利凭证持有人是否可以获得相应证券。<br>indicates whether the holders of the rights instrument may get securities in the event that other right holders choose not to subscribe |

## 4. 依赖（owl:imports，21 个）

本本体通过 `owl:imports` 引入以下本体，各项的中文名称与简介如下：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `BE/LegalEntities/CorporateBodies.rdf` | 法人团体本体（Corporate Bodies Ontology） | 定义依法设立、具有独立法律人格的法人团体（corporate body），是股份有限公司等具体法人类型的上位概念。 |
| `DER/DerivativesContracts/CommoditiesContracts.rdf` | 大宗商品合约本体（Commodities Contracts Ontology） | 定义以大宗商品（能源、金属、农产品等）为标的的衍生品合约。 |
| `DER/DerivativesContracts/CurrencyContracts.rdf` | 外汇合约本体（Currency Contracts Ontology） | 定义以外汇为标的的衍生品合约：外汇远期、货币互换等。 |
| `DER/DerivativesContracts/DerivativesBasics.rdf` | 衍生品基础本体（Derivatives Basics Ontology） | 定义衍生品合约（derivatives contract）的核心概念：标的资产、行权、到期等，是 DER 域的根基。 |
| `DER/DerivativesContracts/ExoticOptions.rdf` | 奇异期权本体（Exotic Options Ontology） | 定义障碍期权、亚式期权等非标准化（奇异）期权。 |
| `DER/SecurityBasedDerivatives/SecurityBasedDerivatives.rdf` | 证券类衍生品本体（Security-Based Derivatives Ontology） | 定义以单个证券或证券组合为标的的衍生品。 |
| `FBC/FinancialInstruments/FinancialInstruments.rdf` | 金融工具本体（Financial Instruments Ontology） | FIBO 核心本体之一，定义金融工具（financial instrument）的通用概念：可交易、代表某种权利义务的合同工具，是证券、衍生品等具体工具的共同基础。 |
| `FBC/FunctionalEntities/FinancialServicesEntities.rdf` | 金融服务实体本体（Financial Services Entities Ontology） | FBC 域核心本体，定义金融服务机构（银行、券商、保险公司、资管机构等）的功能分类体系。 |
| `FND/Relations/Relations.rdf` | 关系本体（Relations Ontology） | FIBO 最底层的基础本体，定义参考（reference）、分类（classify）等通用关系与抽象概念，全库普遍依赖。 |
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `IND/EconomicIndicators/EconomicIndicators.rdf` | 经济指标本体（Economic Indicators Ontology） | 定义宏观经济指标（GDP、CPI、失业率等）的通用结构：发布机构、发布频率与数值。 |
| `IND/MarketIndices/BasketIndices.rdf` | 篮子指数本体（Basket Indices Ontology） | 定义以一篮子成分为基础的指数：成分、权重与计算方法。 |
| `SEC/Debt/Bonds.rdf` | 债券本体（Bonds Ontology） | 定义债券（bond）：期限、票面利率、付息方式与偿还结构。 |
| `SEC/Debt/ExerciseConventions.rdf` | 行权惯例本体（Exercise Conventions Ontology） | 定义债务工具中嵌入期权的行权惯例：美式、欧式、百慕大式。 |
| `SEC/Equities/EquityInstruments.rdf` | 股权工具本体（Equity Instruments Ontology） | 定义股票等股权工具：普通股、优先股及其附带的权利。 |
| `SEC/Securities/Baskets.rdf` | 篮子本体（Baskets Ontology） | 定义证券篮子（basket）：作为整体交易或定价的一组证券。 |
| `SEC/Securities/SecuritiesIssuance.rdf` | 证券发行本体（Securities Issuance Ontology） | 定义证券发行（issuance）：发行人、发行条款与发行结果。 |
| `SEC/Securities/SecuritiesListings.rdf` | 证券上市本体（Securities Listings Ontology） | 定义证券在交易所上市（listing）及其上市状态。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |
| `https://www.omg.org/spec/Commons/QuantitiesAndUnits/` | OMG 通用量与单位本体（OMG Commons Quantities and Units） | Commons 库中的量与单位本体，定义数量、度量单位、量纲的通用概念，支撑金额、比率等数值表达。 |
| `https://www.omg.org/spec/Commons/RolesAndCompositions/` | OMG 通用角色与构成本体（OMG Commons Roles and Compositions） | Commons 库中的角色本体，定义角色及整体—部分构成关系的通用概念。 |

## 5. 文件

- 官方 RDF/XML：`RightsAndWarrants.rdf`
- 中文 Turtle：`RightsAndWarrants.ttl`
- 结构图：`RightsAndWarrants-structure.png` / `RightsAndWarrants-structure.svg`