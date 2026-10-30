# 权利与权证本体（Rights and Warrants Ontology）结构与公理说明

本文档对应 `RightsAndWarrants.rdf` / `RightsAndWarrants.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `RightsAndWarrants-structure.png`（`RightsAndWarrants-structure.svg` 为可缩放版本）。

![权利与权证本体（Rights and Warrants Ontology）本体结构图](RightsAndWarrants-structure.png)

## 1. 本体概述

定义认股权证（warrant）与配股权（rights）：赋予持有人按约定价格认购证券的权利的凭证。

**在体系中的位置**：衍生品合约模块的四大基础结构本体之一。

**上下游关系**：上游继承衍生品基础与期权本体；下游关联 SEC 股权工具（权证常依附于股票或债券发行）。

**与相近概念的差别**：与期权的差别——权证由公司或发行人发行、行权会稀释股本、期限长，期权多为交易所标准化合约、行权不涉及新股发行；配股权则是面向现有股东的短期认购权。

## 2. 类（Class）

| 类（Class） | 定义（Definition） |
|---|---|
| 公司权证（CompanyWarrant） | 由公司自身发行的权证，行权时通常涉及公司发行新股。 |
| 配股权（allotment right） | 授予现有证券持有人的特权，使其有权免费获得新证券。 |
| 配股权公式（allotment right formula） | 用于计算配股权对应证券数量的规则，通常基于持有人所持该类工具的数量。 |
| 基于障碍工具的迷你期货凭证（barrier instrument-based mini-future certificate） | 在产品存续期内障碍工具交易价格水平被突破时立即到期的迷你期货凭证。 |
| 标的障碍迷你期货凭证（barrier underlying mini-future certificate） | 在产品存续期内标的价格突破障碍水平时立即到期的迷你期货凭证。 |
| 篮子权证（basket warrant） | 允许持有人在规定期间内按指定价格购买一揽子或一组资产的权证。 |
| 债券购买权（bond purchase right） | 赋予潜在被收购方债券持有人以大幅折价购买该公司或任何收购该公司者之债券的权利的反收购安排。 |
| 债券认购权（bond subscription right） | 授予现有债券持有人以通常低于当时市价的价格认购新证券的认购权。 |
| 认购认沽权证（call put warrant） | 未明确认购或认沽特征、或明确同时包含认购和认沽特征的权证。 |
| 认购权证（call warrant） | 赋予买方（持有人）在规定期间内按指定价格购买特定标的资产的权利（而非义务）的权证。 |
| 组合工具购买权（combined instruments purchase right） | 赋予潜在被收购方多种证券持有人购买该公司或任何收购该公司者之证券的权利的反收购安排。 |
| 组合工具认购权（combined instruments subscription right） | 授予现有多种证券持有人以通常低于当时市价的价格认购新证券的认购权。 |
| 商品权证（commodity warrant） | 允许持有人在规定期间内按指定价格购买指定数量商品的权证。 |
| 普通可转换股购买权（common convertible share purchase right） | 赋予潜在被收购方普通可转换股股东购买该公司或任何收购该公司者之普通可转换股的权利的购买权。 |
| 普通可转换股认购权（common convertible share subscription right） | 授予现有普通可转换股股东以通常低于当时市价的价格认购新证券的认购权。 |
| 普通股购买权（common share purchase right） | 赋予潜在被收购方普通股股东购买该公司或任何收购该公司者之普通股的权利的购买权。 |
| 普通股认购权（common share subscription right） | 授予现有普通股股东以通常低于当时市价的价格认购新证券的认购权。 |
| 恒定杠杆凭证（constant leverage certificate） | 将开放式凭证结构与无固定期限的杠杆期权相结合、使杠杆在无期限条件下可用的权益凭证。 |
| 备兑权证（covered warrant） | 赋予持有人按指定价格买入（认购权证）或卖出（认沽权证）标的资产的权利（而非义务）的权证，通常由第三方发行。 |
| 货币权证（currency warrant） | 允许持有人在规定期间内按指定汇率购买指定金额某种货币的权证。 |
| 债务权证（debt warrant） | 允许持有人在规定期间内按指定价格购买指定数量债务工具或相关债务指标的权证。 |
| 股权权证（equity warrant） | 允许持有人在规定期间内按指定价格购买指定数量权益工具的权证。 |
| 交易所交易权证（exchange-traded warrant） | 在证券交易所挂牌的权证。 |
| 奇异权证（exotic warrant） | 赋予持有人在非标准或复杂条件下买入（有时卖出）标的资产的权利（而非义务）的权证。 |
| 指数权证（index warrant） | 允许持有人在规定期间内按指定价格购买基于指数表现之指定金额的权证。 |
| 做多迷你期货凭证（long mini-future certificate） | 通常授予持有人在规定期间内按指定价格购买特定标的资产之权利的迷你期货凭证。 |
| 迷你期货凭证（mini-future certificate） | 将开放式凭证结构与无固定期限的杠杆期权相结合、使杠杆在无期限条件下可用的权益凭证。 |
| 裸权证（naked warrant） | 赋予持有人按指定价格买入（认购权证）或卖出（认沽权证）标的资产的权利（而非义务）、但不伴随标的持有的权证。 |
| 永续权证（perpetual warrant） | 无到期日的权证，赋予持有人按指定价格买入（认购权证）或卖出（认沽权证）标的资产的权利（而非义务）。 |
| 优先可转换股购买权（preferred convertible share purchase right） | 赋予潜在被收购方优先可转换股股东购买该公司或任何收购该公司者之优先可转换股的权利的购买权。 |
| 优先可转换股认购权（preferred convertible share subscription right） | 授予现有优先可转换股股东以通常低于当时市价的价格认购新证券的认购权。 |
| 优先股购买权（preferred share purchase right） | 赋予潜在被收购方优先股股东购买该公司或任何收购该公司者之优先股的权利的购买权。 |
| 优先股认购权（preferred share subscription right） | 授予现有优先股股东以通常低于当时市价的价格认购新证券的认购权。 |
| 私募权证（private warrant） | 不可交易的权证。 |
| 公募权证（public warrant） | 可在场外（OTC）或通过交易所交易的权证。 |
| 购买权（purchase right） | 一种反收购安排：赋予潜在被收购方股东以折扣价购买该公司或任何收购该公司者之股份的权利。 |
| 认沽权证（put warrant） | 赋予买方（持有人）卖出指定资产（即以标的资产换取现金）的权利（而非义务）的权证。 |
| 做空迷你期货凭证（short mini-future certificate） | 授予持有人以特定标的资产换取现金之权利的迷你期货凭证。 |
| 结构化权证（structured warrant） | 在交易所挂牌的权证，为投资者提供不直接购买标的资产即可参与其价格表现的途径。 |
| 认购权（subscription right） | 授予现有证券持有人的特权，使其有权以通常低于当时市价的价格认购新证券。 |
| 传统权证（traditional warrant） | 赋予持有人按指定价格买入（认购权证）或卖出（认沽权证）标的资产的权利（而非义务）的权证。 |
| 权证（warrant） | 允许持有人在规定期间内按指定价格购买指定数量金融工具、商品、货币或其他资产的权益凭证。 |

### 2.1 继承关系（Inheritance）

- 配股权（allotment right） ⊑ 股票衍生品
- 配股权（allotment right） ⊑ 权益凭证
- 配股权公式（allotment right formula） ⊑ 表达式
- 基于障碍工具的迷你期货凭证（barrier instrument-based mini-future certificate） ⊑ 迷你期货凭证（mini-future certificate）
- 标的障碍迷你期货凭证（barrier underlying mini-future certificate） ⊑ 迷你期货凭证（mini-future certificate）
- 篮子权证（basket warrant） ⊑ 权证（warrant）
- 债券购买权（bond purchase right） ⊑ 购买权（purchase right）
- 债券认购权（bond subscription right） ⊑ 认购权（subscription right）
- 认购认沽权证（call put warrant） ⊑ 认购权证（call warrant）
- 认购认沽权证（call put warrant） ⊑ 认沽权证（put warrant）
- 认购权证（call warrant） ⊑ 权证（warrant）
- 组合工具购买权（combined instruments purchase right） ⊑ 购买权（purchase right）
- 组合工具认购权（combined instruments subscription right） ⊑ 认购权（subscription right）
- 商品权证（commodity warrant） ⊑ 商品衍生品
- 商品权证（commodity warrant） ⊑ 权证（warrant）
- 普通可转换股购买权（common convertible share purchase right） ⊑ 购买权（purchase right）
- 普通可转换股认购权（common convertible share subscription right） ⊑ 认购权（subscription right）
- 普通股购买权（common share purchase right） ⊑ 购买权（purchase right）
- 普通股认购权（common share subscription right） ⊑ 认购权（subscription right）
- 恒定杠杆凭证（constant leverage certificate） ⊑ 证券类衍生品
- 恒定杠杆凭证（constant leverage certificate） ⊑ 权益凭证
- 恒定杠杆凭证（constant leverage certificate） ⊑ 期权
- 备兑权证（covered warrant） ⊑ 权证（warrant）
- 货币权证（currency warrant） ⊑ 货币衍生品
- 货币权证（currency warrant） ⊑ 权证（warrant）
- 债务权证（debt warrant） ⊑ 权证（warrant）
- 债务权证（debt warrant） ⊑ 债务工具衍生品
- 股权权证（equity warrant） ⊑ 认购权证（call warrant）
- 股权权证（equity warrant） ⊑ 传统权证（traditional warrant）
- 股权权证（equity warrant） ⊑ 股票衍生品
- 交易所交易权证（exchange-traded warrant） ⊑ 公募权证（public warrant）
- 交易所交易权证（exchange-traded warrant） ⊑ 上市证券
- 奇异权证（exotic warrant） ⊑ 权证（warrant）
- 指数权证（index warrant） ⊑ 权证（warrant）
- 做多迷你期货凭证（long mini-future certificate） ⊑ 迷你期货凭证（mini-future certificate）
- 迷你期货凭证（mini-future certificate） ⊑ 障碍期权
- 迷你期货凭证（mini-future certificate） ⊑ 证券类衍生品
- 迷你期货凭证（mini-future certificate） ⊑ 权益凭证
- 裸权证（naked warrant） ⊑ 权证（warrant）
- 永续权证（perpetual warrant） ⊑ 权证（warrant）
- 优先可转换股购买权（preferred convertible share purchase right） ⊑ 购买权（purchase right）
- 优先可转换股认购权（preferred convertible share subscription right） ⊑ 认购权（subscription right）
- 优先股购买权（preferred share purchase right） ⊑ 购买权（purchase right）
- 优先股认购权（preferred share subscription right） ⊑ 认购权（subscription right）
- 私募权证（private warrant） ⊑ 权证（warrant）
- 私募权证（private warrant） ⊑ 不可转让证券
- 公募权证（public warrant） ⊑ 权证（warrant）
- 公募权证（public warrant） ⊑ 可转让证券
- 购买权（purchase right） ⊑ 权益凭证
- 认沽权证（put warrant） ⊑ 权证（warrant）
- 做空迷你期货凭证（short mini-future certificate） ⊑ 迷你期货凭证（mini-future certificate）
- 结构化权证（structured warrant） ⊑ 权证（warrant）
- 认购权（subscription right） ⊑ 权益凭证
- 传统权证（traditional warrant） ⊑ 权证（warrant）
- 权证（warrant） ⊑ 权益凭证

## 4. 数据属性（Datatype Property）

| 属性（Property） | 中文（English） | 定义（Definition） |
|---|---|---|
| fibo-der-drc-raw:hasConversionRatio | 具有转换比率（has conversion ratio） | 指明为买入或卖出特定数量证券或投资单位所需权证数量的换算系数。 |
| fibo-der-drc-raw:hasOversubscribeOption | 是否具有超额认购选择权（has oversubscribe option） | 表明在其他权利持有人选择不认购时，该权利凭证持有人是否可以获得相应证券。 |

## 5. 公理约定（Axioms）

- 配股权（allotment right）：具有表达式 some 配股权公式（allotment right formula）
- 篮子权证（basket warrant）：具有标的 some（由…扮演（is played by） some 证券篮子）
- 债券购买权（bond purchase right）：具有标的 some（由…扮演（is played by） some 债券）
- 债券认购权（bond subscription right）：具有标的 some（由…扮演（is played by） some 债券）
- 普通可转换股购买权（common convertible share purchase right）：具有标的 some（由…扮演（is played by） some 可转换普通股）
- 普通可转换股认购权（common convertible share subscription right）：具有标的 some（由…扮演（is played by） some 可转换普通股）
- 普通股购买权（common share purchase right）：具有标的 some（由…扮演（is played by） some 普通股）
- 普通股认购权（common share subscription right）：具有标的 some（由…扮演（is played by） some 普通股）
- 备兑权证（covered warrant）：由……发行 some 金融机构
- 股权权证（equity warrant）：由……发行 some（由…扮演（is played by） only 股份公司）
- 指数权证（index warrant）：具有标的 some（由…扮演（is played by） Nbac3ce0bca954591b9cee7d38aa5c1ff ≥0）
- 裸权证（naked warrant）：由……发行 some 金融机构
- 裸权证（naked warrant） 与 备兑权证（covered warrant） 互斥（disjointWith）
- 优先可转换股购买权（preferred convertible share purchase right）：具有标的 some（由…扮演（is played by） some 可转换优先股）
- 优先可转换股认购权（preferred convertible share subscription right）：具有标的 some（由…扮演（is played by） some 可转换优先股）
- 优先股购买权（preferred share purchase right）：具有标的 some（由…扮演（is played by） some 优先股）
- 优先股认购权（preferred share subscription right）：具有标的 some（由…扮演（is played by） some 优先股）
- 传统权证（traditional warrant） 与 备兑权证（covered warrant） 互斥（disjointWith）
- 传统权证（traditional warrant） 与 裸权证（naked warrant） 互斥（disjointWith）
- 权证（warrant）：具有行权条款 some 行权条款

## 6. 依赖（owl:imports，21 个）

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

## 7. 文件

- 官方 RDF/XML：`RightsAndWarrants.rdf`
- 中文 Turtle：`RightsAndWarrants.ttl`
- 结构图：`RightsAndWarrants-structure.png` / `RightsAndWarrants-structure.svg`