# 证券相关企业行动本体（Security-related Corporate Actions Ontology）结构与公理说明

本文档对应 `SecurityRelatedCorporateActions.rdf` / `SecurityRelatedCorporateActions.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `SecurityRelatedCorporateActions-structure.png`（`SecurityRelatedCorporateActions-structure.svg` 为可缩放版本）。

![证券相关企业行动本体（Security-related Corporate Actions Ontology）本体结构图](SecurityRelatedCorporateActions-structure.png)

## 1. 本体概述

定义直接改变证券条款或数量的企业行动：拆股、并股、换股、权证行使、证券赎回等。

**在体系中的位置**：CAE 域中企业行动本体的子集特化。

**上下游关系**：上游继承企业行动本体；下游关联 SEC 证券与 DER 权证相关本体。

**与相近概念的差别**：是企业行动的一个子类——专指影响证券本身形态的行动，区别于纯分配类行动（如现金分红不改变证券条款）。

## 2. 类（Class）

| 类（Class） | 定义（Definition） |
|---|---|
| 债券违约事件（bond default event） | 表明发行人未能履行债券协议中定义为违约事件之义务、且未予补救的公司行动。 |
| 红股发行（bonus issue） | 发行人按持有比例向证券持有人免费赠予额外资产的公司行动。 |
| 红利认股权发行（bonus rights issue） | 将认股权免费授予相关股份持有人的配股发行。 |
| 红股计划分配（bonus share plan distribution） | 从公司股本溢价储备中发行股份、视为资本分配而非收益发放的事件。 |
| 对中介证券的催缴（call on intermediate securities） | 对未缴款证券或中介证券分配产生的中介证券进行催缴或行权的公司行动。 |
| 股份注销（cancellation of shares） | 股份的注销，仅适用于未公开发行的股份（即库存股）。 |
| 资本分配（capital distribution） | 从发行人资本账户向股东支付现金的公司行动。 |
| 资本利得分配（capital gains distribution） | 将出售公司资产所得利润分配给股东的公司行动。 |
| 现金股息行动（cash dividend action） | 按持股比例向股东分配现金的公司行动。 |
| 证券交易状态变更事件（change of security trading status event） | 可交易证券的交易状态发生变化的事件。 |
| 最小可交易单位变更（change to smallest negotiable unit） | 修改股份最小可交易单位以获得新的可交易单位（SWIFT：SMAL）。 |
| 转换行动（conversion action） | 将证券（通常为可转换债券或优先股）转换为另一形式证券（通常为普通股）的公司行动。 |
| 转换暂停行动（conversion suspension action） | 暂停证券转换，通常在会议召开前数周（SWIFT：SCOP）。 |
| 公司行动义务（corporate action obligation） | 与持有某证券相关的义务。 |
| 公司行动付款义务（corporate action payment obligation） | 公司行动情境中支付款项的义务。 |
| 公司行动证券交付义务（corporate action securities delivery obligation） | 公司行动情境中交付某证券的义务；现金对价与证券对价均可表示为合同义务。 |
| 公司状态变更事件（corporate change of status event） | 某证券状态的某种变更。 |
| 息票剥离（coupon strip） | 将未来付息日的利息息票与授予持有人本金权利的证券本金分离的过程。 |
| 减值行动（decrease in value action） | 导致股份面值或基金资产价值减少的公司行动。 |
| 股息选择权行动（dividend option action） | 向股东分配股息、股东可选择收取形式的公司行动。 |
| 股息再投资行动（dividend reinvestment action） | 持有人可保留现金或将现金再投资为发行公司额外股票的股息支付行动。 |
| 抽签赎回（drawing） | 在证券预定最终到期日前部分赎回。 |
| 荷兰式拍卖（dutch auction） | 由希望收购某证券的参与方发起的公司行动。 |
| 交换行动（exchange action） | 以持仓换取其他证券和/或现金的公司行动。 |
| 正式要约（formal offer） | 向持有人、潜在持有人或其他利益相关方发出的、达成对参与方具有或将具有法律约束力之交易的要约。 |
| 全额提前赎回行动（full call early redemption action） | 在到期前对某次发行的全部流通证券进行赎回的公司行动。 |
| 付息行动（interest payment action） | 向计息资产持有人分配定期利息的公司行动。 |
| 实物付息（interest payment in kind） | 以现金以外的任何形式向计息资产持有人分配的利息支付（SWIFT：PINK）。 |
| 附本金付息（interest payment with principal） | 除利息支付外，同时支付计息资产部分本金的付款（SWIFT：PRII）。 |
| 利率调整（interest rate adjustment） | 浮动或可调利率证券票面利率的预定调整。 |
| 中介证券分配（intermediate securities distribution） | 分配中介证券或赋予持有人参与未来事件之权利的特权的公司行动。 |
| 退市消息（listing status delisting message） | 证券不再符合交易所上市要求、被从正式报价板移除的消息。 |
| 零股要约（odd lot offer） | 发行人向零股持有人发出的要约：可按市价进行免佣交易、卖出零股或买入凑整。 |
| 同等权益行动（pari-passu action） | 不同特征的证券在各方面变得完全相同（同等权益）时发生的公司行动。 |
| 部分赎回并削减面值行动（partial redemption with reduction of nominal value action） | 在预定最终到期日前部分赎回证券并削减其面值的公司行动。 |
| 部分赎回不削减面值行动（partial redemption without reduction of nominal value action） | 在预定最终到期日前部分赎回证券但不削减面值的公司行动。 |
| 合并后证券交换（post-merger securities exchange） | 因两家或多家公司合并、由发行人发起的流通证券交换（可包括期权）。 |
| 回售赎回行动（put redemption action） | 持有人按发行条款选择提前赎回证券、不削减面值的公司行动。 |
| 到期赎回行动（redemption at maturity action） | 在最终到期日对某次发行的全部流通证券进行赎回的公司行动。 |
| 重新计值行动（redenomination action） | 重新表述证券计值单位（货币和/或面值）的公司行动。 |
| 回购要约（repurchase offer） | 发行公司向现有股东发出的回购股权或可转换为股权之其他证券的要约。 |
| 并股（reverse stock split） | 在不改变股东权益或总市值的情况下减少公司流通股数量的公司行动。 |
| 权利行权事件（rights exercise event） | 行使购买股份之权利的事件，属持有人一方的行动。 |
| 股本溢价股息行动（shares premium dividend action） | 从股本溢价储备中向股东支付现金的公司行动。 |
| 股票股息行动（stock dividend action） | 以发行公司股票形式向股东分配股息的公司行动。 |
| 拆股（stock split） | 在不改变股东权益或总市值的情况下增加公司流通股数量的公司行动。 |
| 要约收购（tender offer） | 通常由第三方向股东发出的、请求其出售（投标）或交换所持股票的要约。 |
| 交易状态活跃消息（trading status active message） | 证券交易已开始、或在暂停后恢复交易的消息。 |
| 交易状态消息（trading status message） | 关于交易状态的消息。 |
| 交易状态暂停消息（trading status suspended message） | 证券交易已被暂停的消息。 |
| 认股权证行权行动（warrant exercise action） | 向持有人提供按预定价格买入（认购权证）或卖出（认沽权证）特定数量股票、现金或商品之选择权的公司行动。 |
| 无价值证券行动（worthless security action） | 涉及将无价值证券核销的公司行动。 |

### 2.1 继承关系（Inheritance）

- 债券违约事件（bond default event） ⊑ 强制性公司行动
- 债券违约事件（bond default event） ⊑ 债务违约
- 红股发行（bonus issue） ⊑ 强制性公司行动
- 红利认股权发行（bonus rights issue） ⊑ 中介证券分配（intermediate securities distribution）
- 红股计划分配（bonus share plan distribution） ⊑ 资本分配（capital distribution）
- 对中介证券的催缴（call on intermediate securities） ⊑ 带选择的强制性公司行动
- 股份注销（cancellation of shares） ⊑ 公司行动
- 资本分配（capital distribution） ⊑ 自愿性公司行动
- 资本利得分配（capital gains distribution） ⊑ 自愿性公司行动
- 现金股息行动（cash dividend action） ⊑ 强制性公司行动
- 证券交易状态变更事件（change of security trading status event） ⊑ 公司状态变更事件（corporate change of status event）
- 最小可交易单位变更（change to smallest negotiable unit） ⊑ 公司行动
- 转换行动（conversion action） ⊑ 自愿性公司行动
- 转换暂停行动（conversion suspension action） ⊑ 公司行动
- 公司行动义务（corporate action obligation） ⊑ 公司行动
- 公司行动义务（corporate action obligation） ⊑ 责任
- 公司行动付款义务（corporate action payment obligation） ⊑ 公司行动义务（corporate action obligation）
- 公司行动证券交付义务（corporate action securities delivery obligation） ⊑ 公司行动义务（corporate action obligation）
- 公司状态变更事件（corporate change of status event） ⊑ 公司行动
- 公司状态变更事件（corporate change of status event） ⊑ 生命周期事件
- 息票剥离（coupon strip） ⊑ 公司行动
- 减值行动（decrease in value action） ⊑ 强制性公司行动
- 股息选择权行动（dividend option action） ⊑ 带选择的强制性公司行动
- 股息再投资行动（dividend reinvestment action） ⊑ 带选择的强制性公司行动
- 抽签赎回（drawing） ⊑ 强制性公司行动
- 荷兰式拍卖（dutch auction） ⊑ 自愿性公司行动
- 交换行动（exchange action） ⊑ 公司行动
- 正式要约（formal offer） ⊑ 自愿性公司行动
- 全额提前赎回行动（full call early redemption action） ⊑ 强制性公司行动
- 付息行动（interest payment action） ⊑ 强制性公司行动
- 实物付息（interest payment in kind） ⊑ 付息行动（interest payment action）
- 附本金付息（interest payment with principal） ⊑ 付息行动（interest payment action）
- 利率调整（interest rate adjustment） ⊑ 强制性公司行动
- 中介证券分配（intermediate securities distribution） ⊑ 强制性公司行动
- 退市消息（listing status delisting message） ⊑ 通知
- 零股要约（odd lot offer） ⊑ 自愿性公司行动
- 同等权益行动（pari-passu action） ⊑ 强制性公司行动
- 部分赎回并削减面值行动（partial redemption with reduction of nominal value action） ⊑ 公司行动
- 部分赎回不削减面值行动（partial redemption without reduction of nominal value action） ⊑ 公司行动
- 合并后证券交换（post-merger securities exchange） ⊑ 公司行动
- 回售赎回行动（put redemption action） ⊑ 自愿性公司行动
- 到期赎回行动（redemption at maturity action） ⊑ 强制性公司行动
- 重新计值行动（redenomination action） ⊑ 强制性公司行动
- 回购要约（repurchase offer） ⊑ 自愿性公司行动
- 并股（reverse stock split） ⊑ 强制性公司行动
- 权利行权事件（rights exercise event） ⊑ 公司行动
- 股本溢价股息行动（shares premium dividend action） ⊑ 带选择的强制性公司行动
- 股票股息行动（stock dividend action） ⊑ 强制性公司行动
- 拆股（stock split） ⊑ 强制性公司行动
- 要约收购（tender offer） ⊑ 自愿性公司行动
- 交易状态活跃消息（trading status active message） ⊑ 交易状态消息（trading status message）
- 交易状态消息（trading status message） ⊑ 通知
- 交易状态暂停消息（trading status suspended message） ⊑ 交易状态消息（trading status message）
- 认股权证行权行动（warrant exercise action） ⊑ 公司行动
- 无价值证券行动（worthless security action） ⊑ 强制性公司行动

## 3. 对象属性（Object Property）

| 属性（Property） | 中文（English） | 定义（Definition） | 说明 |
|---|---|---|---|
| fibo-cae-ce-srca:convertsFrom | 转换自（converts from） | 标识转换前的证券。 | 定义域（domain）：公司行动；值域（range）：证券 |
| fibo-cae-ce-srca:convertsTo | 转换为（converts to） | 标识转换后的证券。 | 定义域（domain）：公司行动；值域（range）：证券 |

## 5. 公理约定（Axioms）

- 债券违约事件（bond default event）：适用于 some 债券
- 证券交易状态变更事件（change of security trading status event）：适用于 some 证券交易状态
- 转换行动（conversion action）：转换自（converts from） some 证券
- 转换行动（conversion action）：转换为（converts to） some 证券
- 息票剥离（coupon strip）：适用于 some 债券
- 利率调整（interest rate adjustment）：适用于 some 浮动票息债券
- 合并后证券交换（post-merger securities exchange）：具有货币数量 货币数量 ≥0
- 合并后证券交换（post-merger securities exchange）：转换自（converts from） some 证券
- 合并后证券交换（post-merger securities exchange）：转换为（converts to） some 证券
- 并股（reverse stock split）：适用于 some 股份
- 并股（reverse stock split） 与 拆股（stock split） 互斥（disjointWith）
- 拆股（stock split）：适用于 some 股份
- 要约收购（tender offer）：适用于 some 股份
- 交易状态消息（trading status message）：关于 some 证券交易状态
- 交易状态消息（trading status message）：引用 some 证券

## 6. 依赖（owl:imports，13 个）

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

## 7. 文件

- 官方 RDF/XML：`SecurityRelatedCorporateActions.rdf`
- 中文 Turtle：`SecurityRelatedCorporateActions.ttl`
- 结构图：`SecurityRelatedCorporateActions-structure.png` / `SecurityRelatedCorporateActions-structure.svg`