# 担保债务凭证本体（Collateralized Debt Obligations Ontology）结构与公理说明

本文档对应 `CollateralizedDebtObligations.rdf` / `CollateralizedDebtObligations.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `CollateralizedDebtObligations-structure.png`（`CollateralizedDebtObligations-structure.svg` 为可缩放版本）。

![担保债务凭证本体（Collateralized Debt Obligations Ontology）本体结构图](CollateralizedDebtObligations-structure.png)

## 1. 本体概述

定义担保债务凭证（CDO）：以债券、贷款份额等债务资产池为支持、按优先级/夹层/股权档分层发行的证券。

**在体系中的位置**：SEC 债务模块中证券化产品的品种之一。

**上下游关系**：上游继承池支持证券本体；下游被合成 CDO 本体扩展。

**与相近概念的差别**：与 ABS/MBS 的差别在底层资产（债务工具）与分层复杂度——CDO 的档级结构与瀑布式偿付规则（waterfall）更复杂；与合成 CDO 的差别——合成型不持有真实资产。

本本体中类与类的核心关系如下（完整细节见各类小节）：

- **资产支持证券担保债务凭证交易（ABS CDO deal）** 继承 **担保债务凭证交易（CDO deal）**
- **资产支持证券担保债务凭证工具（ABS CDO instrument）** 继承 **现金型担保债务凭证分档（cash CDO tranche）**
- **机构抵押担保债券（agency CMO）** 继承 **债务发行（DebtOffering）**
- **机构仅付息分档（agency IO tranche）** 继承 **机构抵押担保债券（agency CMO）**
- **机构跳转分档（agency jump tranche）** 继承 **机构抵押担保债券（agency CMO）**
- **机构跳转 Z 分档（agency jump Z tranche）** 继承 **机构跳转分档（agency jump tranche）**
- **机构跳转 Z 分档（agency jump Z tranche）** 继承 **机构 Z 分档（agency Z tranche）**
- **机构仅付本分档（agency PO tranche）** 继承 **机构抵押担保债券（agency CMO）**
- **机构常规跳转 Z 分档（agency regular jump Z）** 继承 **机构跳转 Z 分档（agency jump Z tranche）**
- **机构粘性跳转 Z 分档（agency sticky jump Z）** 继承 **机构跳转 Z 分档（agency jump Z tranche）**
- **机构 Z 分档（agency Z tranche）** 继承 **机构抵押担保债券（agency CMO）**
- **套利型担保债务凭证（arbitrage CDO）** 继承 **担保债务凭证交易（CDO deal）**
- 其余 99 条关系从略。

## 2. 类（Class）

| 类（Class） | 定义（Definition） |
|---|---|
| 担保债务凭证分档优先级选择（CDOTrancheSenioritySelection） | CDO 发行中某一档的优先级别。<br>The seniority of a tranche of a CDO issue. |
| 资产支持证券担保债务凭证交易（ABS CDO deal） | 资产支持证券担保债务凭证（ABS CDO）票据的一次发行。<br>An issue of Asset Backed Security CDO notes. |
| 资产支持证券担保债务凭证工具（ABS CDO instrument） | 标的资产池为资产支持证券（ABS）的担保债务凭证。<br>CDO where the underlying asset pool is ABS. |
| 机构抵押担保债券（agency CMO） | 由政府机构发行或担保的抵押担保债券（CMO）。 |
| 机构仅付息分档（agency IO tranche） | 机构产品中仅支付利息的分档（Interest Only）。 |
| 机构跳转分档（agency jump tranche） | 机构产品中的一种分档：当某种触发事件达成时，该分档持有人开始收到付款。<br>A tranche where if there is some sort of trigger event reached then the holders of the tranche will begin to receive payments. |
| 机构跳转 Z 分档（agency jump Z tranche） | 类似于 Z 分档，但当某种触发事件达成时，跳转 Z 分档持有人开始收到付款。<br>A Jump Z tranche is like a Z tranche but if there is some sort of trigger event reached then the holders of the Jump Z tranche will begin to receive payments. Regular non-Sticky Jump Z tranches maintain their changed status only while the trigger event is in effect, and revert to their old payment status once the trigger event has passed. |
| 机构仅付本分档（agency PO tranche） | 仅支付本金的分档（Principal Only）。<br>Principal Only tranche. This tranche will only pay principal. |
| 机构常规跳转 Z 分档（agency regular jump Z） | 常规（非粘性）跳转 Z 分档：仅在触发事件持续期间维持变更后的状态，触发事件解除后恢复原有付款状态。<br>Regular non-Sticky Jump Z tranches maintain their changed status only while the trigger event is in effect, and revert to their old payment status once the trigger event has passed. |
| 机构粘性跳转 Z 分档（agency sticky jump Z） | 「粘性」跳转 Z 分档：一旦触发即保持跳转 Z 分档的付款优先级，直至清偿完毕。<br>"Sticky" Jump Z tranches maintain the payment priority of a Jump Z tranche until they are retired. |
| 机构 Z 分档（agency Z tranche） | 在其他分档存续期间不接收付款的分档。<br>A tranche that does not receive payments while other tranches remain. |
| 套利型担保债务凭证（arbitrage CDO） | 套利型 CDO/CLO/CBO：由公司、管道机构或特殊目的载体（SPV）购入参考资产，旨在重新打包后出售。<br>Arbitrage CDO/CLO/CBO - the reference assets are bought by a firm or conduit or SPV (Special Purpose Vehicle) with a view to repackage them and sell them on as the structured product. |
| 套利型目标（arbitrage CDO objective） | 目标是套利：通过将资产重新打包为不同分档来增加价值。<br>The objective is arbitrage, whereby the motivation is to add value by repackaging assets into tranches. |
| 资产负债表型担保债务凭证（balance sheet CDO） | 资产负债表型 CDO/CLO/CBO：其组合的参考资产取自某一公司的资产负债表。<br>Balance Sheet CDO/CLO/CBO - the reference assets for the SDO portfolio are taken from a company/firm's balance sheet. |
| 资产负债表型目标（balance sheet CDO objective） | 目标是创建担保债务凭证以将资产移出发起人的资产负债表。<br>The objective is that the CDO is created to move assets off the originator balance sheet. |
| 担保债务凭证现金流处理结构（CDO cashflow treatment structure） | 担保债务凭证（CDO）中现金流的处理方式。<br>The way in which cash flows are handled in a CDO. |
| 担保债务凭证交易（CDO deal） | 作为面向市场发行的一部分、一组 CDO 分档的一次发行。<br>An Issue of a set of CDO tranches as part of an offering to the market. |
| 担保债务凭证管理风格（CDO management style） | CDO 存续期内参考资产的管理方式。<br>The manner in which reference assets are managed during the life of a CDO. |
| 担保债务凭证发起目标（CDO origination objective） | CDO 发行背后的缘起或动机。<br>The origin or motivation behind a CDO issue. |
| 担保债务凭证池（CDO pool） | 由 CDO 证券组成的池，双层 CDO（CDO Squared）的标的就是 CDO 工具池。<br>A pool of CDO securities. The underlying of the CDO Squared is a pool of CDO instruments. |
| 担保债务凭证组合（CDO portfolio） | 持有 CDO 参考资产的组合。<br>A portfolio in which the reference assets of the CDO are held. |
| 担保债务凭证组合管理人（CDO portfolio manager） | 管理型 CDO 或套利型 CDO 的组合管理人（亦称资产管理人）。<br>The portfolio manager for a managed CDO or arbitrage CDO (also called an asset manager). This assumes that the role is the same in both cases. |
| 双层担保债务凭证交易（CDO squared deal） | 双层 CDO（CDO Squared）票据的一次发行。<br>An issue of CDO Squared notes. |
| 双层担保债务凭证工具（CDO squared instrument） | 标的资产池为其他 CDO 的担保债务凭证。<br>CDOs where the underlying asset pool is CDOs. |
| 抵押担保债券交易（CMO deal） | 抵押担保债券（CMO）的一次发行。<br>An issue of Collateralized mortgaged Obligations. |
| 现金型资产支持证券池（cash ABS pool） | 由一组现金型 ABS 工具组成的池投资。<br>A pool investment consisting of a collection of cash ABS instruments. |
| 现金型担保债务凭证（cash CDO） | 标的资产组合由发行人实际持有的 CDO。<br>A CDO which has an uderlying portfolio of assets which are held by the issuer. |
| 现金型担保债务凭证分档（cash CDO tranche） | 现金型 CDO 的一个分档。 |
| 现金流型担保债务凭证（cashflow CDO） | 类似于 CMO：抵押品产生的现金流用于向投资者支付本金和利息；若现金流不足则按约定处理。<br>A cash-flow CDO is analogous to a CMO. Cash flows from collateral are used to pay principal and interest to investors. If such cash flows prove inadequate, principal and interest is paid to tranches according to seniority. At any point in time, all immediate obligations to a given tranch are met before any payments are made to less senior tranches. |
| 现金流结构（cashflow structure） | CDO 的资金来源为现金流，即抵押品产生的现金流用于向投资者支付本金和利息。<br>The source of funds for the CDO is cashflow. this means that cash flows from collateral are used to pay principal and interest to investors. |
| 担保债券凭证（collateralized bond obligation） | 以投资级债券为标的资产、由高收益或垃圾债券应收款支持的结构化债务证券。<br>structured debt security that has investment-grade bonds as its underlying assets backed by the receivables on high-yield or junk bonds |
| 担保债务凭证（collateralized debt obligation） | 由公司贷款和抵押支持证券等固定收益资产组合构建的结构化金融产品，由特殊目的载体发行。<br>structured finance constructed from a portfolio of fixed income assets including corporate loans and mortgage backed securities. A special purpose vehicle (SPV) issues notes to investors in order to raise funds that are invested in a portfolio of those fixed income assets, held by the SPV as collateral for the notes. Further notes: Collateralized Debt Obligation, for example, ABS CDO which consists of a portfolio of different ABS bonds, and the payments to the holders of these trust certificates are derived from the cash flows of the ABS bonds. This CDO instrument is part of a CDO issue, consisting of individual CDO instruments of a given seniority. Often referred to as tranches and slices (Investopedia). Investopedia: Similar in structure to a collateralized mortgage obligation (CMO) or collateralized bond obligation (CBO), CDOs are unique in that they represent different types of debt and credit risk. In the case of CDOs, these different types of debt are often referred to as 'tranches' or 'slices'. Each slice has a different maturity and risk associated with it. The higher the risk, the more the CDO pays. Further details: Collateralized Debt obligations are securitized interests in pools of - generally non-mortgage - assets. Assets - called collateral - usually comprise loans or debt instruments. A CDO may be called a collateralized loan obligation (CLO) or collateralized bond obligation (CBO) if it holds only loans or bonds, respectively. Investors bear the credit risk of the collateral. Multiple tranches of securities are issued by the CDO, offering investors various maturity and credit risk characteristics. |
| 担保贷款凭证发行（collateralized loan obligation offering） | 担保贷款凭证（CLO）的一次发行。 |
| 浮动分档（floater tranche） | 与某一指数加利差挂钩的分档。<br>A floater tranche is a tranche that is keyed to an index and a spread. |
| 混合型担保债务凭证（hybrid CDO） | 兼具现金型和合成型 CDO 特征的 CDO，即同时具有现金型分档和合成标的资产分档的 CDO。<br>A CDO which combines features both of the cash and synthetic CDO. This is a CDO with tranches of cash and tranches of synthetic underlying assets. Further notes: So for example an issiue of $550 million may have $500 million in an asset pool and an additional $50 million created via a synthetic asset. |
| 小仅付息分档（IOette） | 一种仅付息（IO）分档的变体。<br>REVIEW: Is this a kind of IO Tranche. |
| 反向浮动分档（inverse floater tranche） | 票息与参考利率反向变动的分档。 |
| 跳转 Z 触发事件（jump Z trigger event） | 触发跳转 Z 分档生效的事件。<br>The event which triggers the Jump Z |
| 跳转 Z 触发事件解除（jump z trigger event reversal） | 触发跳转 Z 分档之事件的解除。<br>The reversal of the event which triggers the Jump Z |
| 贷款池（loan pool） | 成分为贷款的债务池。<br>debt pool whose consituents are loans |
| 抵押支持证券工具切片（MBS instrument slice） | 对某一档中单独一片或数片的持有。<br>A holding of an individual slice or slices of a tranche. |
| 抵押支持证券分档票据（MBS tranche note） | 某一档中的单张票据。<br>An individual note of a tranche. |
| 管理型担保债务凭证（managed CDO） | 参考资产购入后（组合逐步建成），CDO 管理人可酌情调整组合的 CDO。<br>A CDO where the reference assets are bought (the portfolio is ramped up) and then the CDO manager may alter the portfolio as they see fit. |
| 管理型担保债务凭证组合（managed CDO portfolio） | 参考资产购入后（组合逐步建成），CDO 管理人可酌情调整的组合。<br>A portfolio where the reference assets of the CDO are bought (the portfolio is ramped up) and then the CDO manager may alter the portfolio as they see fit. |
| 管理型管理风格（managed management style） | 由管理人主动调整参考资产组合的管理方式。 |
| 市值型担保债务凭证（market value CDO） | 以偿付能力取决于抵押品市场价值（而非仅现金流）的 CDO。 |
| 市值结构（market value structure） | CDO 的资金来源为市值，即向投资者支付的本金和利息来自抵押品现金流及抵押品出售所得。 |
| 夹层担保债务凭证分档（mezzanine CDO tranche） | 介于优先档与次级档之间的分档，CDO 夹层档的评级通常为 B 至 BBB。<br>The tranche between senior and subordinated. Mezzanine tranches of a CDO issue are typically rated B to BBB. |
| 夹层抵押支持证券分档（mezzanine MBS tranche） | MBS 发行中优先级居中的夹层分档。<br>Specific kinds of tranche are modeled for example and investigation only and have been removed from the diagrams. These will be removed from the final model. |
| 非机构仅付息分档（non-agency IO tranche） | 仅支付利息的分档（Interest Only），即该分档只付息。<br>Interest Only tranche, meaning that this tranche will only pay interest. |
| 非机构跳转分档（non-agency jump tranche） | 当某种触发事件达成时，该分档持有人开始收到付款的分档。<br>A tranche where if there is some sort of trigger event reached then the holders of the tranche will begin to receive payments. |
| 非机构跳转 Z 分档（non-agency jump Z tranche） | 类似于 Z 分档，但当某种触发事件达成时，跳转 Z 分档持有人开始收到付款。<br>A Jump Z tranche is like a Z tranche but if there is some sort of trigger event reached then the holders of the Jump Z tranche will begin to receive payments. Regular non-Sticky Jump Z tranches maintain their changed status only while the trigger event is in effect, and revert to their old payment status once the trigger event has passed. |
| 非机构仅付本分档（non-agency PO tranche） | 仅支付本金的分档（Principal Only）。<br>Principal Only tranche. This tranche will only pay principal. |
| 非机构常规跳转 Z 分档（non-agency regular jump Z tranche） | 常规（非粘性）跳转 Z 分档：仅在触发事件持续期间维持变更后的状态，触发事件解除后恢复原有付款状态。<br>Regular non-Sticky Jump Z tranches maintain their changed status only while the trigger event is in effect, and revert to their old payment status once the trigger event has passed. |
| 非机构粘性跳转 Z 分档（non-agency sticky jump Z tranche） | 「粘性」跳转 Z 分档：一旦触发即保持跳转 Z 分档的付款优先级，直至清偿完毕。<br>"Sticky" Jump Z tranches maintain the payment priority of a Jump Z tranche until they are retired. |
| 非机构 Z 分档（non-agency Z tranche） | 在其他分档存续期间不接收付款的分档。<br>A tranche that does not receive payments while other tranches remain. |
| 计划摊销仅付本分档（PAC PO tranche） | 计划摊销档（PAC）中的仅付本金分档。<br>Planned Amortization Class principal only tranche. |
| 计划摊销档摊销计划表（PAC tranche amortization schedule） | 计划摊销档（PAC）分档的本金摊销计划表。 |
| 计划摊销 Z 分档（PAC-Z tranche） | 同时为 Z 分档的计划摊销档（PAC）分档。<br>Planned Amortization Class tranche which is also a Z tranche, that is Definition needed. |
| 计划摊销一档（PAC-1 class） | 计划摊销档（PAC）分档，PAC-1 是优先级最高的计划摊销档。<br>Planned Amortization Class tranche. PAC-1 is the most senior Planned Amortization Class tranche. |
| 计划摊销二档（PAC-2 class） | 计划摊销档（PAC）分档，PAC-2 指具有类似 PAC 债券之计划付款结构的支持档。<br>Planned Amortization Class tranche. PAC-2 refers to a support tranche that is given a scheduled payment structure like a PAC bond. |
| 计划摊销三档（PAC-3 class） | 计划摊销档（PAC）分档，具有计划付款的补充支持档。<br>Planned Amortization Class tranche. Additional support tranche with scheduled payments. |
| 计划摊销档债券（planned amortization class bond） | 本金支付必须遵循特定计划表的分档（PAC）。<br>Planned Amortization Class tranche.This is a tranche where the principal payment must follow a certain schedule. |
| 常规浮动分档（regular floater tranche） | 与某一指数加利差挂钩的分档，利差加在指数之上。<br>A floater tranche is a tranche that is keyed to an index and a spread. The spread is added to the index. |
| 剩余分档（residual tranche） | 收取其他分档受偿后剩余现金流的分档。<br>Unknown Further notes: Verify whether Residual Tranche and Support Tranche are meant to be in the same list of types as PAC etc. i.e. can a tranche not be PAC and Residual? this looks suspicioulsy like two semantics. |
| 优先担保债务凭证分档（senior CDO tranche） | CDO 发行中优先级最高的分档，评级通常为 A 至 AAA；若发生违约或抵押品表现不佳，计划付款优先保障该档。<br>The most senior tranche of the CDO issue. Typically rated A to AAA. If there are defaults or the CDO's collateral otherwise underperforms, scheduled payments to senior tranches take precedence over those of mezzanine tranches. |
| 优先抵押支持证券分档（senior MBS tranche） | MBS 发行中优先级最高的分档。<br>Specific kinds of tranche are modeled for example and investigation only and have been removed from the diagrams. These will be removed from the final model. |
| 静态担保债务凭证（static CDO） | 抵押品在 CDO 存续期内固定不变的 CDO：参考资产购入后，在产品期限内不再调整。<br>A CDO where collateral is fixed through the life of the CDO. The reference assets are bought and then are kept untouched for the term of the product. |
| 静态担保债务凭证组合（static CDO portfolio） | 抵押品在 CDO 存续期内固定不变的组合：参考资产购入后，在产品期限内保持不动。<br>A portfolio where collateral of the CDO is fixed through the life of the CDO. The reference assets are bought and then are kept untouched for the term of the product. |
| 静态管理风格（static management style） | 参考资产组合在存续期内保持固定的管理方式。 |
| 次级担保债务凭证权益档（subordinated CDO equity） | 次级（亦称权益）CDO 分档是 CDO 发行中最末尾的分档，违约或抵押品表现不佳时最先承担损失。<br>The subordinated (also known as equity) CDO tranche is the most junior tranche in the CDO issue. If there are defaults or the CDO's collateral otherwise underperforms, scheduled payments to senior and mezzanine tranches take precedence over those to subordinated/equity tranches. |
| 次级抵押支持证券分档（subordinated MBS tranche） | MBS 发行中优先级最低的分档。<br>Specific kinds of tranche are modeled for example and investigation only and have been removed from the diagrams. These will be removed from the final model. |
| 超级浮动分档（super floater tranche） | 票息杠杆放大浮动利率变动的分档。 |
| 超级仅付本分档（super PO tranche） | 仅支付本金的分档（Principal Only）的一种特殊形式。<br>Principal Only tranche. This tranche will only pay principal. Not clear how this is distinct from generic PO. |
| 超优先担保债务凭证分档（super senior CDO tranche） | 位于 CDO 发行最顶端的分档。<br>A tranche at the very top of a CDO Issue. |
| 支持分档（support tranche） | 为计划摊销档（PAC）分档提供付款支持的分档。<br>A tranche which provides payment support to a PAC Tranche. |
| 目标摊销档（TAC tranche） | 目标摊销档（TAC）：与 PAC 分档相关，具有针对特定提前偿付速度（称为定价速度）的付款计划表。<br>Targeted Amortization Class. This is related to a PAC tranche and has a payment schedule geared towards a specified prepayment speed (called the pricing speed). Agency CMO |
| 目标摊销档摊销计划表（TAC tranche amortization schedule） | 目标摊销档（TAC）分档的本金摊销计划表。 |
| 分档发行时评级（tranche rating at issue） | 证券某一档在发行时的评级。<br>The rating at issue of a tranche of a security. Note this is under review |
| 分档类型（tranche type） | 指明分档的类型。<br>the type of tranche in a tranched MBS security |
| 分档型抵押支持证券交易（tranched MBS deal） | 分档型 MBS 的一次发行。 |
| 分档型抵押支持证券交易招募说明书（tranched MBS deal prospectus） | 分档型 MBS 发行的招募说明书。 |
| 分档型抵押支持证券工具（tranched MBS instrument） | 分档型 MBS 的工具。 |
| 触发事件（trigger event） | 某一数值越过某一阈值的事件，或其他类型的业务事件。<br>Any event where some value passes some threashold. Or some other type of business event. This is not restricted to "trigger" in the sense of a value passing a threshold. Can also be an seen such as a CDO manager going into bankruptcy. |
| 真实出售目标（true sale objective） | 以实现资产真实出售为目的的发起目标。 |

以下按类逐个展开：每个类给出继承关系、相关属性与公理约定；子类在父类之下降一级编号。

### 2.1 担保债务凭证分档优先级选择（CDOTrancheSenioritySelection）

定义：CDO 发行中某一档的优先级别。

### 2.2 机构抵押担保债券（agency CMO）

定义：由政府机构发行或担保的抵押担保债券（CMO）。

- 父类：**债务发行（DebtOffering）**
- 直接子类：**机构仅付息分档（agency IO tranche）**、**机构跳转分档（agency jump tranche）**、**机构仅付本分档（agency PO tranche）**、**机构 Z 分档（agency Z tranche）**、**计划摊销档债券（planned amortization class bond）**、**目标摊销档（TAC tranche）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有分档类型（has tranche type）** | 指明分档的类型。 | 值域：分档类型（tranche type） |
| **提供提前偿付支持（provides prepayment support）** | 表明某分档吸收提前偿付变动以保护其他分档。 | 值域：机构抵押担保债券（agency CMO） |
| **包含（comprises）** | — | — |

公理：

- **具有分档类型（has tranche type）**至少有一个取值，类型是**分档类型（tranche type）**。
- **包含（comprises）**至少有一个取值，类型是**机构抵押支持证券池（AgencyMBSPool）**。
- **提供提前偿付支持（provides prepayment support）**至少有一个取值，类型是**机构抵押担保债券（agency CMO）**。

#### 2.2.1 机构仅付息分档（agency IO tranche）

定义：机构产品中仅支付利息的分档（Interest Only）。

- 父类：**机构抵押担保债券（agency CMO）**
- 直接子类：**小仅付息分档（IOette）**

公理：

- 与**机构仅付本分档（agency PO tranche）**互斥：同一个体不能同时属于两者。

##### 2.2.1.1 小仅付息分档（IOette）

定义：一种仅付息（IO）分档的变体。

- 父类：**机构仅付息分档（agency IO tranche）**

#### 2.2.2 机构跳转分档（agency jump tranche）

定义：机构产品中的一种分档：当某种触发事件达成时，该分档持有人开始收到付款。

- 父类：**机构抵押担保债券（agency CMO）**
- 直接子类：**机构跳转 Z 分档（agency jump Z tranche）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **规定触发（specifies trigger）** | 规定一旦发生时使跳转 Z 持有人开始接收付款的事件。<br>The event which, when it takes place, causes the Jump Z holders to begin receiving payments. | 值域：跳转 Z 触发事件（jump Z trigger event） |

公理：

- **规定触发（specifies trigger）**至少有一个取值，类型是**跳转 Z 触发事件（jump Z trigger event）**。

##### 2.2.2.1 机构跳转 Z 分档（agency jump Z tranche）

定义：类似于 Z 分档，但当某种触发事件达成时，跳转 Z 分档持有人开始收到付款。

- 父类：**机构跳转分档（agency jump tranche）**、**机构 Z 分档（agency Z tranche）**
- 直接子类：**机构常规跳转 Z 分档（agency regular jump Z）**、**机构粘性跳转 Z 分档（agency sticky jump Z）**

###### 2.2.2.1.1 机构常规跳转 Z 分档（agency regular jump Z）

定义：常规（非粘性）跳转 Z 分档：仅在触发事件持续期间维持变更后的状态，触发事件解除后恢复原有付款状态。

- 父类：**机构跳转 Z 分档（agency jump Z tranche）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **于……时恢复（reverts on）** | 指明使该分档恢复原有付款状态的事件。 | 值域：跳转 Z 触发事件解除（jump z trigger event reversal） |

公理：

- **于……时恢复（reverts on）**至少有一个取值，类型是**跳转 Z 触发事件解除（jump z trigger event reversal）**。

###### 2.2.2.1.2 机构粘性跳转 Z 分档（agency sticky jump Z）

定义：「粘性」跳转 Z 分档：一旦触发即保持跳转 Z 分档的付款优先级，直至清偿完毕。

- 父类：**机构跳转 Z 分档（agency jump Z tranche）**

#### 2.2.3 机构仅付本分档（agency PO tranche）

定义：仅支付本金的分档（Principal Only）。

- 父类：**机构抵押担保债券（agency CMO）**
- 直接子类：**计划摊销仅付本分档（PAC PO tranche）**、**超级仅付本分档（super PO tranche）**

##### 2.2.3.1 计划摊销仅付本分档（PAC PO tranche）

定义：计划摊销档（PAC）中的仅付本金分档。

- 父类：**机构仅付本分档（agency PO tranche）**、**计划摊销档债券（planned amortization class bond）**

##### 2.2.3.2 超级仅付本分档（super PO tranche）

定义：仅支付本金的分档（Principal Only）的一种特殊形式。

- 父类：**机构仅付本分档（agency PO tranche）**

#### 2.2.4 机构 Z 分档（agency Z tranche）

定义：在其他分档存续期间不接收付款的分档。

- 父类：**机构抵押担保债券（agency CMO）**
- 直接子类：**机构跳转 Z 分档（agency jump Z tranche）**、**计划摊销 Z 分档（PAC-Z tranche）**

##### 2.2.4.2 计划摊销 Z 分档（PAC-Z tranche）

定义：同时为 Z 分档的计划摊销档（PAC）分档。

- 父类：**机构 Z 分档（agency Z tranche）**、**计划摊销档债券（planned amortization class bond）**

#### 2.2.5 计划摊销档债券（planned amortization class bond）

定义：本金支付必须遵循特定计划表的分档（PAC）。

- 父类：**机构抵押担保债券（agency CMO）**
- 直接子类：**计划摊销仅付本分档（PAC PO tranche）**、**计划摊销 Z 分档（PAC-Z tranche）**、**计划摊销一档（PAC-1 class）**、**计划摊销二档（PAC-2 class）**、**计划摊销三档（PAC-3 class）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **为……提供提前偿付支持（provides prepayment support for）** | 表明某分档为另一特定分档吸收提前偿付变动。 | 值域：计划摊销档债券（planned amortization class bond）；逆属性：由……支持（supported by）；子属性：提供提前偿付支持（provides prepayment support） |
| **规定（specifies）** | 清晰而确定地提及、命名或陈述某事物。 | 值域：计划摊销档摊销计划表（PAC tranche amortization schedule） |
| **由……支持（supported by）** | 表明某分档由另一分档提供付款支持。 | 值域：计划摊销档债券（planned amortization class bond） |

公理：

- **为……提供提前偿付支持（provides prepayment support for）**的所有取值只能是**计划摊销档债券（planned amortization class bond）**。
- **由……支持（supported by）**的所有取值只能是**计划摊销档债券（planned amortization class bond）**。
- **规定（specifies）**至少有一个取值，类型是**计划摊销档摊销计划表（PAC tranche amortization schedule）**。

##### 2.2.5.3 计划摊销一档（PAC-1 class）

定义：计划摊销档（PAC）分档，PAC-1 是优先级最高的计划摊销档。

- 父类：**计划摊销档债券（planned amortization class bond）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **在……之后承担提前偿付（takes prepayment after）** | 表明某分档在另一分档之后承担提前偿付现金流。 | 值域：计划摊销二档（PAC-2 class）；子属性：由……支持（supported by） |

公理：

- **在……之后承担提前偿付（takes prepayment after）**的所有取值只能是**计划摊销二档（PAC-2 class）**。

##### 2.2.5.4 计划摊销二档（PAC-2 class）

定义：计划摊销档（PAC）分档，PAC-2 指具有类似 PAC 债券之计划付款结构的支持档。

- 父类：**计划摊销档债券（planned amortization class bond）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **在……之后承担提前偿付（takes prepayment after）** | 表明某分档在另一分档之后承担提前偿付现金流。 | 值域：计划摊销三档（PAC-3 class）；子属性：由……支持（supported by） |

公理：

- **在……之后承担提前偿付（takes prepayment after）**的所有取值只能是**计划摊销三档（PAC-3 class）**。

##### 2.2.5.5 计划摊销三档（PAC-3 class）

定义：计划摊销档（PAC）分档，具有计划付款的补充支持档。

- 父类：**计划摊销档债券（planned amortization class bond）**

#### 2.2.6 目标摊销档（TAC tranche）

定义：目标摊销档（TAC）：与 PAC 分档相关，具有针对特定提前偿付速度（称为定价速度）的付款计划表。

- 父类：**机构抵押担保债券（agency CMO）**、**分档型抵押支持证券工具（tranched MBS instrument）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **规定（specifies）** | 清晰而确定地提及、命名或陈述某事物。 | 值域：目标摊销档摊销计划表（TAC tranche amortization schedule） |

公理：

- **规定（specifies）**至少有一个取值，类型是**目标摊销档摊销计划表（TAC tranche amortization schedule）**。

### 2.3 担保债务凭证现金流处理结构（CDO cashflow treatment structure）

定义：担保债务凭证（CDO）中现金流的处理方式。

- 父类：**战略（Strategy）**
- 直接子类：**现金流结构（cashflow structure）**、**市值结构（market value structure）**

#### 2.3.1 现金流结构（cashflow structure）

定义：CDO 的资金来源为现金流，即抵押品产生的现金流用于向投资者支付本金和利息。

- 父类：**担保债务凭证现金流处理结构（CDO cashflow treatment structure）**

#### 2.3.2 市值结构（market value structure）

定义：CDO 的资金来源为市值，即向投资者支付的本金和利息来自抵押品现金流及抵押品出售所得。

- 父类：**担保债务凭证现金流处理结构（CDO cashflow treatment structure）**

### 2.4 担保债务凭证交易（CDO deal）

定义：作为面向市场发行的一部分、一组 CDO 分档的一次发行。

- 父类：**债务发行（DebtOffering）**
- 直接子类：**资产支持证券担保债务凭证交易（ABS CDO deal）**、**套利型担保债务凭证（arbitrage CDO）**、**资产负债表型担保债务凭证（balance sheet CDO）**、**双层担保债务凭证交易（CDO squared deal）**、**现金型担保债务凭证（cash CDO）**、**现金流型担保债务凭证（cashflow CDO）**、**混合型担保债务凭证（hybrid CDO）**、**管理型担保债务凭证（managed CDO）**、**市值型担保债务凭证（market value CDO）**、**静态担保债务凭证（static CDO）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有担保债务凭证发起目标（has CDO origination objective）** | 指明 CDO 发行的发起目标或动机。 | 值域：担保债务凭证发起目标（CDO origination objective） |
| **管理风格（management style）** | 参考资产购入后（组合逐步建成），CDO 管理人可酌情调整组合的管理方式。<br>A CDO where the reference assets are bought (the portfolio is ramped up) and then the CDO manager may alter the portfolio as they see fit. | 值域：担保债务凭证管理风格（CDO management style） |
| **结构（structure）** | CDO 的资金来源为市值，即向投资者支付的本金和利息来自抵押品现金流及抵押品出售所得。<br>The source of funds for the CDO is market value. This means that principal and interest payments to investors come from both collateral cash flows as well as sales of collateral. | 值域：担保债务凭证现金流处理结构（CDO cashflow treatment structure） |
| **具有成员（hasMember）** | — | — |
| **适用于（appliesTo）** | — | — |
| **由……管理（isManagedBy）** | — | — |

公理：

- **具有成员（hasMember）**至少有一个取值，类型是**优先担保债务凭证分档（senior CDO tranche）**。
- **具有成员（hasMember）**至少有一个取值，类型是**夹层担保债务凭证分档（mezzanine CDO tranche）**。
- **具有成员（hasMember）**至少有一个取值，类型是**担保债务凭证组合（CDO portfolio）**。
- **具有成员（hasMember）**至少有一个取值，类型是**次级担保债务凭证权益档（subordinated CDO equity）**。
- **具有成员（hasMember）**至少有一个取值，类型是**超优先担保债务凭证分档（super senior CDO tranche）**。
- **由……管理（isManagedBy）**至少有一个取值，类型是**担保债务凭证组合管理人（CDO portfolio manager）**。
- **适用于（appliesTo）**至少有一个取值，类型是**担保债务凭证（collateralized debt obligation）**。

#### 2.4.1 资产支持证券担保债务凭证交易（ABS CDO deal）

定义：资产支持证券担保债务凭证（ABS CDO）票据的一次发行。

- 父类：**担保债务凭证交易（CDO deal）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **包含（comprises）** | — | — |

公理：

- **包含（comprises）**至少有一个取值，该取值满足：该属性存在取值约束。

#### 2.4.2 套利型担保债务凭证（arbitrage CDO）

定义：套利型 CDO/CLO/CBO：由公司、管道机构或特殊目的载体（SPV）购入参考资产，旨在重新打包后出售。

- 父类：**担保债务凭证交易（CDO deal）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有担保债务凭证发起目标（has CDO origination objective）** | 指明 CDO 发行的发起目标或动机。 | 值域：担保债务凭证发起目标（CDO origination objective） |

公理：

- **具有担保债务凭证发起目标（has CDO origination objective）**至少有一个取值，类型是**套利型目标（arbitrage CDO objective）**。

#### 2.4.3 资产负债表型担保债务凭证（balance sheet CDO）

定义：资产负债表型 CDO/CLO/CBO：其组合的参考资产取自某一公司的资产负债表。

- 父类：**担保债务凭证交易（CDO deal）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有担保债务凭证发起目标（has CDO origination objective）** | 指明 CDO 发行的发起目标或动机。 | 值域：担保债务凭证发起目标（CDO origination objective） |

公理：

- **具有担保债务凭证发起目标（has CDO origination objective）**至少有一个取值，类型是**资产负债表型目标（balance sheet CDO objective）**。

#### 2.4.4 双层担保债务凭证交易（CDO squared deal）

定义：双层 CDO（CDO Squared）票据的一次发行。

- 父类：**担保债务凭证交易（CDO deal）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **包含（comprises）** | — | — |

公理：

- **包含（comprises）**至少有一个取值，类型是**担保债务凭证池（CDO pool）**。

#### 2.4.5 现金型担保债务凭证（cash CDO）

定义：标的资产组合由发行人实际持有的 CDO。

- 父类：**担保债务凭证交易（CDO deal）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **发行（issues）** | 正式使某事物可得。 | 值域：现金型担保债务凭证分档（cash CDO tranche） |

公理：

- **发行（issues）**至少有一个取值，类型是**现金型担保债务凭证分档（cash CDO tranche）**。
- 与**合成担保债务凭证（SyntheticCDO）**互斥：同一个体不能同时属于两者。

#### 2.4.6 现金流型担保债务凭证（cashflow CDO）

定义：类似于 CMO：抵押品产生的现金流用于向投资者支付本金和利息；若现金流不足则按约定处理。

- 父类：**担保债务凭证交易（CDO deal）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **结构（structure）** | CDO 的资金来源为市值，即向投资者支付的本金和利息来自抵押品现金流及抵押品出售所得。<br>The source of funds for the CDO is market value. This means that principal and interest payments to investors come from both collateral cash flows as well as sales of collateral. | 值域：担保债务凭证现金流处理结构（CDO cashflow treatment structure） |

公理：

- **结构（structure）**至少有一个取值，类型是**现金流结构（cashflow structure）**。
- 与**市值型担保债务凭证（market value CDO）**互斥：同一个体不能同时属于两者。

#### 2.4.7 混合型担保债务凭证（hybrid CDO）

定义：兼具现金型和合成型 CDO 特征的 CDO，即同时具有现金型分档和合成标的资产分档的 CDO。

- 父类：**担保债务凭证交易（CDO deal）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **适用于（appliesTo）** | — | — |

公理：

- **适用于（appliesTo）**的所有取值只能是**N24c8db0d1b0d4f44bdb6117094be6121**。

#### 2.4.8 管理型担保债务凭证（managed CDO）

定义：参考资产购入后（组合逐步建成），CDO 管理人可酌情调整组合的 CDO。

- 父类：**担保债务凭证交易（CDO deal）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **管理风格（management style）** | 参考资产购入后（组合逐步建成），CDO 管理人可酌情调整组合的管理方式。<br>A CDO where the reference assets are bought (the portfolio is ramped up) and then the CDO manager may alter the portfolio as they see fit. | 值域：担保债务凭证管理风格（CDO management style） |
| **具有成员（hasMember）** | — | — |

公理：

- **具有成员（hasMember）**至少有一个取值，类型是**抵押支持证券工具切片（MBS instrument slice）**。
- **具有成员（hasMember）**至少有一个取值，类型是**管理型担保债务凭证组合（managed CDO portfolio）**。
- **管理风格（management style）**至少有一个取值，类型是**管理型管理风格（managed management style）**。
- 与**静态担保债务凭证（static CDO）**互斥：同一个体不能同时属于两者。

#### 2.4.9 市值型担保债务凭证（market value CDO）

定义：以偿付能力取决于抵押品市场价值（而非仅现金流）的 CDO。

- 父类：**担保债务凭证交易（CDO deal）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **结构（structure）** | CDO 的资金来源为市值，即向投资者支付的本金和利息来自抵押品现金流及抵押品出售所得。<br>The source of funds for the CDO is market value. This means that principal and interest payments to investors come from both collateral cash flows as well as sales of collateral. | 值域：担保债务凭证现金流处理结构（CDO cashflow treatment structure） |

公理：

- **结构（structure）**至少有一个取值，类型是**市值结构（market value structure）**。

#### 2.4.10 静态担保债务凭证（static CDO）

定义：抵押品在 CDO 存续期内固定不变的 CDO：参考资产购入后，在产品期限内不再调整。

- 父类：**担保债务凭证交易（CDO deal）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **管理风格（management style）** | 参考资产购入后（组合逐步建成），CDO 管理人可酌情调整组合的管理方式。<br>A CDO where the reference assets are bought (the portfolio is ramped up) and then the CDO manager may alter the portfolio as they see fit. | 值域：担保债务凭证管理风格（CDO management style） |

公理：

- **管理风格（management style）**至少有一个取值，类型是**静态管理风格（static management style）**。

### 2.5 担保债务凭证管理风格（CDO management style）

定义：CDO 存续期内参考资产的管理方式。

- 父类：**战略（Strategy）**
- 直接子类：**管理型管理风格（managed management style）**、**静态管理风格（static management style）**

#### 2.5.1 管理型管理风格（managed management style）

定义：由管理人主动调整参考资产组合的管理方式。

- 父类：**担保债务凭证管理风格（CDO management style）**

#### 2.5.2 静态管理风格（static management style）

定义：参考资产组合在存续期内保持固定的管理方式。

- 父类：**担保债务凭证管理风格（CDO management style）**

### 2.6 担保债务凭证发起目标（CDO origination objective）

定义：CDO 发行背后的缘起或动机。

- 父类：**目标（Objective）**
- 直接子类：**套利型目标（arbitrage CDO objective）**、**资产负债表型目标（balance sheet CDO objective）**、**真实出售目标（true sale objective）**

#### 2.6.1 套利型目标（arbitrage CDO objective）

定义：目标是套利：通过将资产重新打包为不同分档来增加价值。

- 父类：**担保债务凭证发起目标（CDO origination objective）**

#### 2.6.2 资产负债表型目标（balance sheet CDO objective）

定义：目标是创建担保债务凭证以将资产移出发起人的资产负债表。

- 父类：**担保债务凭证发起目标（CDO origination objective）**

#### 2.6.3 真实出售目标（true sale objective）

定义：以实现资产真实出售为目的的发起目标。

- 父类：**担保债务凭证发起目标（CDO origination objective）**

### 2.7 担保债务凭证池（CDO pool）

定义：由 CDO 证券组成的池，双层 CDO（CDO Squared）的标的就是 CDO 工具池。

- 父类：**债务池（DebtPool）**

### 2.8 担保债务凭证组合（CDO portfolio）

定义：持有 CDO 参考资产的组合。

- 父类：**组合（Portfolio）**
- 直接子类：**管理型担保债务凭证组合（managed CDO portfolio）**、**静态担保债务凭证组合（static CDO portfolio）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有成员（hasMember）** | — | — |
| **由……管理（isManagedBy）** | — | — |

公理：

- **具有成员（hasMember）**至少有一个取值，类型是**抵押支持证券工具切片（MBS instrument slice）**。
- **由……管理（isManagedBy）**至少有一个取值，类型是**担保债务凭证组合管理人（CDO portfolio manager）**。

#### 2.8.1 管理型担保债务凭证组合（managed CDO portfolio）

定义：参考资产购入后（组合逐步建成），CDO 管理人可酌情调整的组合。

- 父类：**担保债务凭证组合（CDO portfolio）**

#### 2.8.2 静态担保债务凭证组合（static CDO portfolio）

定义：抵押品在 CDO 存续期内固定不变的组合：参考资产购入后，在产品期限内保持不动。

- 父类：**担保债务凭证组合（CDO portfolio）**

### 2.9 担保债务凭证组合管理人（CDO portfolio manager）

定义：管理型 CDO 或套利型 CDO 的组合管理人（亦称资产管理人）。

- 父类：**参与方角色（party role）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **管理（manages）** | — | — |

公理：

- **管理（manages）**至少有一个取值，类型是**担保债务凭证组合（CDO portfolio）**。

### 2.10 抵押担保债券交易（CMO deal）

定义：抵押担保债券（CMO）的一次发行。

- 父类：**债务发行（DebtOffering）**

### 2.11 现金型资产支持证券池（cash ABS pool）

定义：由一组现金型 ABS 工具组成的池投资。

- 父类：**债务池（DebtPool）**

### 2.12 担保债务凭证（collateralized debt obligation）

定义：由公司贷款和抵押支持证券等固定收益资产组合构建的结构化金融产品，由特殊目的载体发行。

- 父类：**结构化金融工具（StructuredFinanceInstrument）**
- 直接子类：**双层担保债务凭证工具（CDO squared instrument）**、**现金型担保债务凭证分档（cash CDO tranche）**、**夹层担保债务凭证分档（mezzanine CDO tranche）**、**优先担保债务凭证分档（senior CDO tranche）**、**超优先担保债务凭证分档（super senior CDO tranche）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **是否现金型（is cash）** | 表明 CDO 是否拥有真实资产的标的池：是则为现金型，否则为合成型标的池。<br>Whether the CDO has an underlying pool of real assets. If yes, the CDO has an underlying pool of real assets. If no, the CDO has a synthetic pool of underlying assets. | 值域：xsd:boolean |
| **具有交易管理风格（has deal management style）** | 表明 CDO 是静态还是管理型，即 CDO 管理人是否可在存续期内调整参考组合。<br>Whether the CDO is static or managed. This refers to whether or not the CDO manager may make changes to the reference portfolio during the life of the security. Further notes: If it is static, collateral is fixed through the life of the CDO. The reference assets are bought and then are kept untouched for the term of the product.If it is managed, the reference assets are bought (the portfolio is ramped up) and then the CDO manager may alter the portfolio as they see fit. | 值域：担保债务凭证管理风格（CDO management style） |
| **具有发起目标（has origination objective）** | 指明发行的发起目标或动机。 | 值域：担保债务凭证发起目标（CDO origination objective） |
| **优先级别（seniority）** | 界定该分档的优先级别，即计划付款的先后次序；分档通常分为优先、夹层和次级。<br>The seniority which defines this tranche. This is the precedence order for scheduled payments. Further notes: Tranches are categorized as senior, mezzanine, and subordinated/equity, according to their degree of credit risk. If there are defaults or the CDO's collateral otherwise underperforms, scheduled payments to senior tranches take precedence over those of mezzanine tranches, and scheduled payments to mezzanine tranches take precedence over those to subordinated/equity tranches. Senior and mezzanine tranches are typically rated, with the former receiving ratings of A to AAA and the latter receiving ratings of B to BBB. The ratings reflect both the credit quality of underlying collateral as well as how much protection a given tranch is afforded by tranches that are subordinate to it. | 值域：担保债务凭证分档优先级选择（CDOTrancheSenioritySelection） |
| **具有结构类型（has structure type）** | 指明 CDO 的资金来源类型，即现金流型或市值型。<br>The source of funds for the CDO. This is either cashflow or market value. | 值域：担保债务凭证现金流处理结构（CDO cashflow treatment structure） |
| **次于（isSubordinatedTo）** | — | — |

公理：

- **次于（isSubordinatedTo）**至多有 1 个**担保债务凭证（collateralized debt obligation）**。

#### 2.12.1 双层担保债务凭证工具（CDO squared instrument）

定义：标的资产池为其他 CDO 的担保债务凭证。

- 父类：**担保债务凭证（collateralized debt obligation）**

#### 2.12.2 现金型担保债务凭证分档（cash CDO tranche）

定义：现金型 CDO 的一个分档。

- 父类：**担保债务凭证（collateralized debt obligation）**、**分档（Tranche）**
- 直接子类：**资产支持证券担保债务凭证工具（ABS CDO instrument）**、**担保债券凭证（collateralized bond obligation）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **是否现金型（is cash）** | 表明 CDO 是否拥有真实资产的标的池：是则为现金型，否则为合成型标的池。<br>Whether the CDO has an underlying pool of real assets. This is yes: the CDO has an underlying pool of real assets, | 值域：xsd:boolean |
| **是……的部分（isPartOf）** | — | — |

公理：

- **是……的部分（isPartOf）**至少有一个取值，类型是**债务池（DebtPool）**。
- 与**资产支持证券（AssetBackedSecurity）**互斥：同一个体不能同时属于两者。
- 与**合成担保债务凭证分档（SyntheticCDOTranche）**互斥：同一个体不能同时属于两者。

##### 2.12.2.1 资产支持证券担保债务凭证工具（ABS CDO instrument）

定义：标的资产池为资产支持证券（ABS）的担保债务凭证。

- 父类：**现金型担保债务凭证分档（cash CDO tranche）**

##### 2.12.2.2 担保债券凭证（collateralized bond obligation）

定义：以投资级债券为标的资产、由高收益或垃圾债券应收款支持的结构化债务证券。

- 父类：**现金型担保债务凭证分档（cash CDO tranche）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **引用（refersTo）** | — | — |

公理：

- **引用（refersTo）**至少有一个取值，类型是**债券池（BondPool）**。
- 与**机构抵押担保债券（agency CMO）**互斥：同一个体不能同时属于两者。
- 与**担保贷款凭证发行（collateralized loan obligation offering）**互斥：同一个体不能同时属于两者。

#### 2.12.3 夹层担保债务凭证分档（mezzanine CDO tranche）

定义：介于优先档与次级档之间的分档，CDO 夹层档的评级通常为 B 至 BBB。

- 父类：**担保债务凭证（collateralized debt obligation）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **发行时评级（rated at issue）** | 分档在发行时所获得的评级。 | 值域：分档发行时评级（tranche rating at issue） |
| **优先级别（seniority）** | 界定该分档的优先级别，即计划付款的先后次序；分档通常分为优先、夹层和次级。<br>The seniority which defines this tranche. This is the precedence order for scheduled payments. This is Mezzanine, meaning the tranche between senior and subordinated. | — |

公理：

- **发行时评级（rated at issue）**至少有一个取值，类型是**分档发行时评级（tranche rating at issue）**。

#### 2.12.4 优先担保债务凭证分档（senior CDO tranche）

定义：CDO 发行中优先级最高的分档，评级通常为 A 至 AAA；若发生违约或抵押品表现不佳，计划付款优先保障该档。

- 父类：**担保债务凭证（collateralized debt obligation）**、**分档（Tranche）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **发行时评级（rated at issue）** | 分档在发行时所获得的评级。 | 值域：分档发行时评级（tranche rating at issue） |
| **优先级别（seniority）** | 界定该分档的优先级别，即计划付款的先后次序；分档通常分为优先、夹层和次级。<br>The seniority which defines this tranche. This is the precedence order for scheduled payments. This is defined as Senior, i.e. this is the most senior tranche of the CDO issue. | — |

公理：

- **发行时评级（rated at issue）**至少有一个取值，类型是**分档发行时评级（tranche rating at issue）**。

#### 2.12.5 超优先担保债务凭证分档（super senior CDO tranche）

定义：位于 CDO 发行最顶端的分档。

- 父类：**担保债务凭证（collateralized debt obligation）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **优先级别（seniority）** | 界定该分档的优先级别，即计划付款的先后次序；分档通常分为优先、夹层和次级。<br>The seniority which defines this tranche. This is the precedence order for scheduled payments. This is defined as Senior, i.e. this is the most senior tranche of the CDO issue. | — |

### 2.13 担保贷款凭证发行（collateralized loan obligation offering）

定义：担保贷款凭证（CLO）的一次发行。

- 父类：**债务发行（DebtOffering）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **引用（refersTo）** | — | — |

公理：

- **引用（refersTo）**至少有一个取值，类型是**贷款池（loan pool）**。
- 与**机构抵押担保债券（agency CMO）**互斥：同一个体不能同时属于两者。

### 2.14 贷款池（loan pool）

定义：成分为贷款的债务池。

- 父类：**债务池（DebtPool）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有成员（hasMember）** | — | — |

公理：

- **具有成员（hasMember）**至少有一个取值，类型是**贷款（Loan）**。

### 2.15 抵押支持证券工具切片（MBS instrument slice）

定义：对某一档中单独一片或数片的持有。

- 父类：**组合（Portfolio）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **引用（refersTo）** | — | — |

公理：

- **引用（refersTo）**至少有一个取值，该取值满足：该属性存在取值约束。

### 2.16 抵押支持证券分档票据（MBS tranche note）

定义：某一档中的单张票据。

- 父类：**本票（PromissoryNote）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **票面金额（denomination）** | 票据计价的货币金额，例如 500 美元面额的票据。<br>The currency amount in which the Note is denominated, for example $500 notes. | 值域：货币数量 |

### 2.17 计划摊销档摊销计划表（PAC tranche amortization schedule）

定义：计划摊销档（PAC）分档的本金摊销计划表。

- 父类：**赎回计划表（RedemptionSchedule）**

### 2.18 次级担保债务凭证权益档（subordinated CDO equity）

定义：次级（亦称权益）CDO 分档是 CDO 发行中最末尾的分档，违约或抵押品表现不佳时最先承担损失。

- 父类：**证券（Security）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **授予……的所有权（confers ownership of）** | 表明某凭证或分档授予对某一资产或现金流的权利。 | — |
| **优先级别（seniority）** | 界定该分档的优先级别，即计划付款的先后次序；分档通常分为优先、夹层和次级。<br>The seniority which defines this tranche. This is the precedence order for scheduled payments. This is subordinated (also known as equity) and is the most junior tranche in the CDO issue. | — |

### 2.19 支持分档（support tranche）

定义：为计划摊销档（PAC）分档提供付款支持的分档。

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由…扮演（is played by）** | — | — |

公理：

- **由…扮演（is played by）**至少有一个取值，类型是**计划摊销二档（PAC-2 class）**。

### 2.20 目标摊销档摊销计划表（TAC tranche amortization schedule）

定义：目标摊销档（TAC）分档的本金摊销计划表。

- 父类：**赎回计划表（RedemptionSchedule）**

### 2.21 分档发行时评级（tranche rating at issue）

定义：证券某一档在发行时的评级。

### 2.22 分档类型（tranche type）

定义：指明分档的类型。

### 2.23 分档型抵押支持证券交易（tranched MBS deal）

定义：分档型 MBS 的一次发行。

- 父类：**债务发行（DebtOffering）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **同时是（is also）** | 表明某分档同时属于另一类型。 | 值域：私募品牌抵押支持证券交易 |

公理：

- **同时是（is also）**至少有一个取值，类型是**私募品牌抵押支持证券交易（PrivateLabelMBSDeal）**。

### 2.24 分档型抵押支持证券交易招募说明书（tranched MBS deal prospectus）

定义：分档型 MBS 发行的招募说明书。

- 父类：**抵押支持证券发行招募说明书（MortgageBackedSecurityOfferingProspectus）**

### 2.25 分档型抵押支持证券工具（tranched MBS instrument）

定义：分档型 MBS 的工具。

- 父类：**抵押支持证券（MortgageBackedSecurity）**
- 直接子类：**浮动分档（floater tranche）**、**夹层抵押支持证券分档（mezzanine MBS tranche）**、**非机构仅付息分档（non-agency IO tranche）**、**非机构跳转分档（non-agency jump tranche）**、**非机构仅付本分档（non-agency PO tranche）**、**非机构 Z 分档（non-agency Z tranche）**、**剩余分档（residual tranche）**、**优先抵押支持证券分档（senior MBS tranche）**、**次级抵押支持证券分档（subordinated MBS tranche）**、**目标摊销档（TAC tranche）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **现金流优先顺序（cashflow precedence）** | 指明各分档获得现金流的先后次序。 | 值域：分档型抵押支持证券工具（tranched MBS instrument）；逆属性：为……提供信用支持（provides credit support to） |
| **为……提供信用支持（provides credit support to）** | 表明某分档为另一分档提供信用增进。 | 值域：分档型抵押支持证券工具（tranched MBS instrument）；子属性：次于 |
| **具有票据（hasNote）** | — | — |

公理：

- **为……提供信用支持（provides credit support to）**的所有取值只能是**分档型抵押支持证券工具（tranched MBS instrument）**。
- **具有票据（hasNote）**至少有一个取值，类型是**抵押支持证券分档票据（MBS tranche note）**。
- **现金流优先顺序（cashflow precedence）**的所有取值只能是**分档型抵押支持证券工具（tranched MBS instrument）**。

#### 2.25.1 浮动分档（floater tranche）

定义：与某一指数加利差挂钩的分档。

- 父类：**分档型抵押支持证券工具（tranched MBS instrument）**
- 直接子类：**反向浮动分档（inverse floater tranche）**、**常规浮动分档（regular floater tranche）**、**超级浮动分档（super floater tranche）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有重复区间（hasRecurrenceInterval）** | — | — |

公理：

- **具有重复区间（hasRecurrenceInterval）**至少有一个取值，类型是**月中日（DayOfMonth）**。

##### 2.25.1.1 反向浮动分档（inverse floater tranche）

定义：票息与参考利率反向变动的分档。

- 父类：**浮动分档（floater tranche）**

公理：

- 与**常规浮动分档（regular floater tranche）**互斥：同一个体不能同时属于两者。
- 与**超级浮动分档（super floater tranche）**互斥：同一个体不能同时属于两者。

##### 2.25.1.2 常规浮动分档（regular floater tranche）

定义：与某一指数加利差挂钩的分档，利差加在指数之上。

- 父类：**浮动分档（floater tranche）**

公理：

- 与**超级浮动分档（super floater tranche）**互斥：同一个体不能同时属于两者。

##### 2.25.1.3 超级浮动分档（super floater tranche）

定义：票息杠杆放大浮动利率变动的分档。

- 父类：**浮动分档（floater tranche）**

#### 2.25.2 夹层抵押支持证券分档（mezzanine MBS tranche）

定义：MBS 发行中优先级居中的夹层分档。

- 父类：**分档型抵押支持证券工具（tranched MBS instrument）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **优先于（senior to）** | 表明某一分档在受偿顺序上优先于另一分档。<br>Specific kinds of tranche are modeled for example and investigation only and have been removed from the diagrams. These will be removed from the final model. | 值域：夹层抵押支持证券分档（mezzanine MBS tranche）；子属性：现金流优先顺序（cashflow precedence） |

公理：

- **优先于（senior to）**至少有一个取值，类型是**次级抵押支持证券分档（subordinated MBS tranche）**。

#### 2.25.3 非机构仅付息分档（non-agency IO tranche）

定义：仅支付利息的分档（Interest Only），即该分档只付息。

- 父类：**分档型抵押支持证券工具（tranched MBS instrument）**

#### 2.25.4 非机构跳转分档（non-agency jump tranche）

定义：当某种触发事件达成时，该分档持有人开始收到付款的分档。

- 父类：**分档型抵押支持证券工具（tranched MBS instrument）**
- 直接子类：**非机构跳转 Z 分档（non-agency jump Z tranche）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **规定触发（specifies trigger）** | 规定一旦发生时使跳转 Z 持有人开始接收付款的事件。<br>The event which, when it takes place, causes the Jump Z holders to begin receiving payments. | 值域：跳转 Z 触发事件（jump Z trigger event） |

公理：

- **规定触发（specifies trigger）**至少有一个取值，类型是**跳转 Z 触发事件（jump Z trigger event）**。

##### 2.25.4.1 非机构跳转 Z 分档（non-agency jump Z tranche）

定义：类似于 Z 分档，但当某种触发事件达成时，跳转 Z 分档持有人开始收到付款。

- 父类：**非机构跳转分档（non-agency jump tranche）**、**非机构 Z 分档（non-agency Z tranche）**
- 直接子类：**非机构常规跳转 Z 分档（non-agency regular jump Z tranche）**、**非机构粘性跳转 Z 分档（non-agency sticky jump Z tranche）**

###### 2.25.4.1.1 非机构常规跳转 Z 分档（non-agency regular jump Z tranche）

定义：常规（非粘性）跳转 Z 分档：仅在触发事件持续期间维持变更后的状态，触发事件解除后恢复原有付款状态。

- 父类：**非机构跳转 Z 分档（non-agency jump Z tranche）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **恢复（reverts）** | 表明触发事件解除后该分档恢复原有付款状态。 | 值域：跳转 Z 触发事件解除（jump z trigger event reversal） |

公理：

- **恢复（reverts）**至少有一个取值，类型是**跳转 Z 触发事件解除（jump z trigger event reversal）**。

###### 2.25.4.1.2 非机构粘性跳转 Z 分档（non-agency sticky jump Z tranche）

定义：「粘性」跳转 Z 分档：一旦触发即保持跳转 Z 分档的付款优先级，直至清偿完毕。

- 父类：**非机构跳转 Z 分档（non-agency jump Z tranche）**

#### 2.25.5 非机构仅付本分档（non-agency PO tranche）

定义：仅支付本金的分档（Principal Only）。

- 父类：**分档型抵押支持证券工具（tranched MBS instrument）**

#### 2.25.6 非机构 Z 分档（non-agency Z tranche）

定义：在其他分档存续期间不接收付款的分档。

- 父类：**分档型抵押支持证券工具（tranched MBS instrument）**
- 直接子类：**非机构跳转 Z 分档（non-agency jump Z tranche）**

#### 2.25.7 剩余分档（residual tranche）

定义：收取其他分档受偿后剩余现金流的分档。

- 父类：**分档型抵押支持证券工具（tranched MBS instrument）**

#### 2.25.8 优先抵押支持证券分档（senior MBS tranche）

定义：MBS 发行中优先级最高的分档。

- 父类：**分档型抵押支持证券工具（tranched MBS instrument）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **优先于（senior to）** | 表明某一分档在受偿顺序上优先于另一分档。<br>Specific kinds of tranche are modeled for example and investigation only and have been removed from the diagrams. These will be removed from the final model. | 值域：夹层抵押支持证券分档（mezzanine MBS tranche）；子属性：现金流优先顺序（cashflow precedence） |

公理：

- **优先于（senior to）**至少有一个取值，类型是**夹层抵押支持证券分档（mezzanine MBS tranche）**。

#### 2.25.9 次级抵押支持证券分档（subordinated MBS tranche）

定义：MBS 发行中优先级最低的分档。

- 父类：**分档型抵押支持证券工具（tranched MBS instrument）**

### 2.26 触发事件（trigger event）

定义：某一数值越过某一阈值的事件，或其他类型的业务事件。

- 直接子类：**跳转 Z 触发事件（jump Z trigger event）**、**跳转 Z 触发事件解除（jump z trigger event reversal）**

#### 2.26.1 跳转 Z 触发事件（jump Z trigger event）

定义：触发跳转 Z 分档生效的事件。

- 父类：**触发事件（trigger event）**

#### 2.26.2 跳转 Z 触发事件解除（jump z trigger event reversal）

定义：触发跳转 Z 分档之事件的解除。

- 父类：**触发事件（trigger event）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **规定反向触发（specifies reverse trigger）** | 规定使分档恢复原有状态的反向触发事件。 | 值域：跳转 Z 触发事件（jump Z trigger event） |

公理：

- **规定反向触发（specifies reverse trigger）**至少有一个取值，类型是**跳转 Z 触发事件（jump Z trigger event）**。

## 3. 依赖（owl:imports，27 个）

本本体通过 `owl:imports` 引入以下本体，各项的中文名称与简介如下：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `BE/FunctionalEntities/FunctionalEntities.rdf` | 功能实体本体（Functional Entities Ontology） | 定义「功能实体」：按其在商业中承担的功能（而非法律形式）刻画的实体，是出版方、登记机构等功能性主体的基础。 |
| `DER/CreditDerivatives/CreditDefaultSwaps.rdf` | 信用违约互换本体（Credit Default Swaps Ontology） | 定义信用违约互换（CDS）：保护买方与卖方、参考实体、信用事件与结算方式。 |
| `FBC/FinancialInstruments/FinancialInstruments.rdf` | 金融工具本体（Financial Instruments Ontology） | FIBO 核心本体之一，定义金融工具（financial instrument）的通用概念：可交易、代表某种权利义务的合同工具，是证券、衍生品等具体工具的共同基础。 |
| `FBC/ProductsAndServices/FinancialProductsAndServices.rdf` | 金融产品与服务本体（Financial Products and Services Ontology） | 定义金融产品（financial product）与金融服务（financial service）及其提供、购买关系。 |
| `FND/Accounting/CurrencyAmount.rdf` | 货币金额本体（Currency Amount Ontology） | 定义「金额＋币种」的货币金额（currency amount）表示，是 FIBO 中表达价格、债务金额、付款额等一切带币种数值的基础构件。 |
| `FND/Agreements/Contracts.rdf` | 合同本体（Contracts Ontology） | 在协议之上定义具有法律约束力的合同（contract）：合同当事方、合同条款、义务与权利，是金融工具与交易合同建模的基石。 |
| `FND/DatesAndTimes/BusinessDates.rdf` | 营业日期本体（Business Dates Ontology） | 定义营业日、营业日历与日期调整规则（如顺延约定），支撑金融合同中的营业日计算。 |
| `FND/DatesAndTimes/FinancialDates.rdf` | 金融日期本体（Financial Dates Ontology） | 定义金融语境下的日期与期间概念：结算日、付息日、到期日、日计数基准等。 |
| `FND/GoalsAndObjectives/Objectives.rdf` | 目标本体（Objectives Ontology） | 定义目标（objective）及其与组织、计划的关系，用于表达机构的经营目标与投资目标。 |
| `FND/OwnershipAndControl/Ownership.rdf` | 所有权本体（Ownership Ontology） | 定义「拥有」关系：所有者、被拥有资产及所有权份额。 |
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `LOAN/LoansGeneral/Loans.rdf` | 贷款本体（Loans Ontology） | LOAN 域核心本体，定义贷款（loan）的通用结构：借款人、贷款人、本金、利率与还款安排。 |
| `SEC/Debt/AssetBackedSecurities.rdf` | 资产支持证券本体（Asset-backed Securities Ontology） | 定义以资产池（如贷款、应收账款）为支持的资产支持证券（ABS）。 |
| `SEC/Debt/Bonds.rdf` | 债券本体（Bonds Ontology） | 定义债券（bond）：期限、票面利率、付息方式与偿还结构。 |
| `SEC/Debt/DebtInstruments.rdf` | 债务工具本体（Debt Instruments Ontology） | 定义债务工具（debt instrument）的通用概念：可交易的债权凭证，是债券、票据等的上位模型。 |
| `SEC/Debt/MortgageBackedSecurities.rdf` | 抵押贷款支持证券本体（Mortgage-backed Securities Ontology） | 定义抵押贷款支持证券（MBS）：以抵押贷款池为支持的证券。 |
| `SEC/Debt/PoolBackedSecurities.rdf` | 池支持证券本体（Pool-backed Securities Ontology） | 定义以资产池为支持的证券的通用结构：资产池、分层（tranche）与过手安排。 |
| `SEC/Debt/SyntheticCDOs.rdf` | 合成 CDO 本体（Synthetic CDOs Ontology） | 定义以信用衍生品（而非实际债务资产）构建风险敞口的合成型担保债务凭证。 |
| `SEC/Funds/Funds.rdf` | 基金本体（Funds Ontology） | 定义投资基金（fund）：基金份额、净值与管理结构。 |
| `SEC/Securities/Pools.rdf` | 证券池本体（Securities Pools Ontology） | 定义证券池（pool）：归集起来作为证券化基础的一组资产。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |
| `https://www.omg.org/spec/Commons/Collections/` | OMG 通用集合本体（OMG Commons Collections） | Commons 库中的集合本体，定义集合、成员等通用概念。 |
| `https://www.omg.org/spec/Commons/ContextualDesignators/` | OMG 通用语境指称本体（OMG Commons Contextual Designators） | Commons 库中的语境指称本体，定义「在某个语境下指代某物的名称/符号」，是地址、账户号码等语境相关标识的基础。 |
| `https://www.omg.org/spec/Commons/Documents/` | OMG 通用文档本体（OMG Commons Documents） | Commons 库中的文档本体，定义文档及其组成部分的通用概念。 |
| `https://www.omg.org/spec/Commons/Organizations/` | OMG 通用组织本体（OMG Commons Organizations） | Commons 库中的组织本体，定义组织、组织成员与组织结构的通用概念。 |
| `https://www.omg.org/spec/Commons/PartiesAndSituations/` | OMG 通用参与方与情境本体（OMG Commons Parties and Situations） | Commons 库中的参与方本体，定义独立主体、参与方及其角色扮演的通用概念，是 FIBO 参与方模型的上游。 |
| `https://www.omg.org/spec/Commons/RolesAndCompositions/` | OMG 通用角色与构成本体（OMG Commons Roles and Compositions） | Commons 库中的角色本体，定义角色及整体—部分构成关系的通用概念。 |

## 4. 文件

- 官方 RDF/XML：`CollateralizedDebtObligations.rdf`
- 中文 Turtle：`CollateralizedDebtObligations.ttl`
- 结构图：`CollateralizedDebtObligations-structure.png` / `CollateralizedDebtObligations-structure.svg`