# 担保债务凭证本体（Collateralized Debt Obligations Ontology）结构与公理说明

本文档对应 `CollateralizedDebtObligations.rdf` / `CollateralizedDebtObligations.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `CollateralizedDebtObligations-structure.png`（`CollateralizedDebtObligations-structure.svg` 为可缩放版本）。

![担保债务凭证本体（Collateralized Debt Obligations Ontology）本体结构图](CollateralizedDebtObligations-structure.png)

## 1. 本体概述

定义担保债务凭证（CDO）：以债券、贷款份额等债务资产池为支持、按优先级/夹层/股权档分层发行的证券。

**在体系中的位置**：SEC 债务模块中证券化产品的品种之一。

**上下游关系**：上游继承池支持证券本体；下游被合成 CDO 本体扩展。

**与相近概念的差别**：与 ABS/MBS 的差别在底层资产（债务工具）与分层复杂度——CDO 的档级结构与瀑布式偿付规则（waterfall）更复杂；与合成 CDO 的差别——合成型不持有真实资产。

## 2. 类（Class）

| 类（Class） | 定义（Definition） |
|---|---|
| 担保债务凭证分档优先级选择（CDOTrancheSenioritySelection） | CDO 发行中某一档的优先级别。 |
| 资产支持证券担保债务凭证交易（ABS CDO deal） | 资产支持证券担保债务凭证（ABS CDO）票据的一次发行。 |
| 资产支持证券担保债务凭证工具（ABS CDO instrument） | 标的资产池为资产支持证券（ABS）的担保债务凭证。 |
| 机构抵押担保债券（agency CMO） | 由政府机构发行或担保的抵押担保债券（CMO）。 |
| 机构仅付息分档（agency IO tranche） | 机构产品中仅支付利息的分档（Interest Only）。 |
| 机构跳转分档（agency jump tranche） | 机构产品中的一种分档：当某种触发事件达成时，该分档持有人开始收到付款。 |
| 机构跳转 Z 分档（agency jump Z tranche） | 类似于 Z 分档，但当某种触发事件达成时，跳转 Z 分档持有人开始收到付款。 |
| 机构仅付本分档（agency PO tranche） | 仅支付本金的分档（Principal Only）。 |
| 机构常规跳转 Z 分档（agency regular jump Z） | 常规（非粘性）跳转 Z 分档：仅在触发事件持续期间维持变更后的状态，触发事件解除后恢复原有付款状态。 |
| 机构粘性跳转 Z 分档（agency sticky jump Z） | 「粘性」跳转 Z 分档：一旦触发即保持跳转 Z 分档的付款优先级，直至清偿完毕。 |
| 机构 Z 分档（agency Z tranche） | 在其他分档存续期间不接收付款的分档。 |
| 套利型担保债务凭证（arbitrage CDO） | 套利型 CDO/CLO/CBO：由公司、管道机构或特殊目的载体（SPV）购入参考资产，旨在重新打包后出售。 |
| 套利型目标（arbitrage CDO objective） | 目标是套利：通过将资产重新打包为不同分档来增加价值。 |
| 资产负债表型担保债务凭证（balance sheet CDO） | 资产负债表型 CDO/CLO/CBO：其组合的参考资产取自某一公司的资产负债表。 |
| 资产负债表型目标（balance sheet CDO objective） | 目标是创建担保债务凭证以将资产移出发起人的资产负债表。 |
| 担保债务凭证现金流处理结构（CDO cashflow treatment structure） | 担保债务凭证（CDO）中现金流的处理方式。 |
| 担保债务凭证交易（CDO deal） | 作为面向市场发行的一部分、一组 CDO 分档的一次发行。 |
| 担保债务凭证管理风格（CDO management style） | CDO 存续期内参考资产的管理方式。 |
| 担保债务凭证发起目标（CDO origination objective） | CDO 发行背后的缘起或动机。 |
| 担保债务凭证池（CDO pool） | 由 CDO 证券组成的池，双层 CDO（CDO Squared）的标的就是 CDO 工具池。 |
| 担保债务凭证组合（CDO portfolio） | 持有 CDO 参考资产的组合。 |
| 担保债务凭证组合管理人（CDO portfolio manager） | 管理型 CDO 或套利型 CDO 的组合管理人（亦称资产管理人）。 |
| 双层担保债务凭证交易（CDO squared deal） | 双层 CDO（CDO Squared）票据的一次发行。 |
| 双层担保债务凭证工具（CDO squared instrument） | 标的资产池为其他 CDO 的担保债务凭证。 |
| 抵押担保债券交易（CMO deal） | 抵押担保债券（CMO）的一次发行。 |
| 现金型资产支持证券池（cash ABS pool） | 由一组现金型 ABS 工具组成的池投资。 |
| 现金型担保债务凭证（cash CDO） | 标的资产组合由发行人实际持有的 CDO。 |
| 现金型担保债务凭证分档（cash CDO tranche） | 现金型 CDO 的一个分档。 |
| 现金流型担保债务凭证（cashflow CDO） | 类似于 CMO：抵押品产生的现金流用于向投资者支付本金和利息；若现金流不足则按约定处理。 |
| 现金流结构（cashflow structure） | CDO 的资金来源为现金流，即抵押品产生的现金流用于向投资者支付本金和利息。 |
| 担保债券凭证（collateralized bond obligation） | 以投资级债券为标的资产、由高收益或垃圾债券应收款支持的结构化债务证券。 |
| 担保债务凭证（collateralized debt obligation） | 由公司贷款和抵押支持证券等固定收益资产组合构建的结构化金融产品，由特殊目的载体发行。 |
| 担保贷款凭证发行（collateralized loan obligation offering） | 担保贷款凭证（CLO）的一次发行。 |
| 浮动分档（floater tranche） | 与某一指数加利差挂钩的分档。 |
| 混合型担保债务凭证（hybrid CDO） | 兼具现金型和合成型 CDO 特征的 CDO，即同时具有现金型分档和合成标的资产分档的 CDO。 |
| 小仅付息分档（IOette） | 一种仅付息（IO）分档的变体。 |
| 反向浮动分档（inverse floater tranche） | 票息与参考利率反向变动的分档。 |
| 跳转 Z 触发事件（jump Z trigger event） | 触发跳转 Z 分档生效的事件。 |
| 跳转 Z 触发事件解除（jump z trigger event reversal） | 触发跳转 Z 分档之事件的解除。 |
| 贷款池（loan pool） | 成分为贷款的债务池。 |
| 抵押支持证券工具切片（MBS instrument slice） | 对某一档中单独一片或数片的持有。 |
| 抵押支持证券分档票据（MBS tranche note） | 某一档中的单张票据。 |
| 管理型担保债务凭证（managed CDO） | 参考资产购入后（组合逐步建成），CDO 管理人可酌情调整组合的 CDO。 |
| 管理型担保债务凭证组合（managed CDO portfolio） | 参考资产购入后（组合逐步建成），CDO 管理人可酌情调整的组合。 |
| 管理型管理风格（managed management style） | 由管理人主动调整参考资产组合的管理方式。 |
| 市值型担保债务凭证（market value CDO） | 以偿付能力取决于抵押品市场价值（而非仅现金流）的 CDO。 |
| 市值结构（market value structure） | CDO 的资金来源为市值，即向投资者支付的本金和利息来自抵押品现金流及抵押品出售所得。 |
| 夹层担保债务凭证分档（mezzanine CDO tranche） | 介于优先档与次级档之间的分档，CDO 夹层档的评级通常为 B 至 BBB。 |
| 夹层抵押支持证券分档（mezzanine MBS tranche） | MBS 发行中优先级居中的夹层分档。 |
| 非机构仅付息分档（non-agency IO tranche） | 仅支付利息的分档（Interest Only），即该分档只付息。 |
| 非机构跳转分档（non-agency jump tranche） | 当某种触发事件达成时，该分档持有人开始收到付款的分档。 |
| 非机构跳转 Z 分档（non-agency jump Z tranche） | 类似于 Z 分档，但当某种触发事件达成时，跳转 Z 分档持有人开始收到付款。 |
| 非机构仅付本分档（non-agency PO tranche） | 仅支付本金的分档（Principal Only）。 |
| 非机构常规跳转 Z 分档（non-agency regular jump Z tranche） | 常规（非粘性）跳转 Z 分档：仅在触发事件持续期间维持变更后的状态，触发事件解除后恢复原有付款状态。 |
| 非机构粘性跳转 Z 分档（non-agency sticky jump Z tranche） | 「粘性」跳转 Z 分档：一旦触发即保持跳转 Z 分档的付款优先级，直至清偿完毕。 |
| 非机构 Z 分档（non-agency Z tranche） | 在其他分档存续期间不接收付款的分档。 |
| 计划摊销仅付本分档（PAC PO tranche） | 计划摊销档（PAC）中的仅付本金分档。 |
| 计划摊销档摊销计划表（PAC tranche amortization schedule） | 计划摊销档（PAC）分档的本金摊销计划表。 |
| 计划摊销 Z 分档（PAC-Z tranche） | 同时为 Z 分档的计划摊销档（PAC）分档。 |
| 计划摊销一档（PAC-1 class） | 计划摊销档（PAC）分档，PAC-1 是优先级最高的计划摊销档。 |
| 计划摊销二档（PAC-2 class） | 计划摊销档（PAC）分档，PAC-2 指具有类似 PAC 债券之计划付款结构的支持档。 |
| 计划摊销三档（PAC-3 class） | 计划摊销档（PAC）分档，具有计划付款的补充支持档。 |
| 计划摊销档债券（planned amortization class bond） | 本金支付必须遵循特定计划表的分档（PAC）。 |
| 常规浮动分档（regular floater tranche） | 与某一指数加利差挂钩的分档，利差加在指数之上。 |
| 剩余分档（residual tranche） | 收取其他分档受偿后剩余现金流的分档。 |
| 优先担保债务凭证分档（senior CDO tranche） | CDO 发行中优先级最高的分档，评级通常为 A 至 AAA；若发生违约或抵押品表现不佳，计划付款优先保障该档。 |
| 优先抵押支持证券分档（senior MBS tranche） | MBS 发行中优先级最高的分档。 |
| 静态担保债务凭证（static CDO） | 抵押品在 CDO 存续期内固定不变的 CDO：参考资产购入后，在产品期限内不再调整。 |
| 静态担保债务凭证组合（static CDO portfolio） | 抵押品在 CDO 存续期内固定不变的组合：参考资产购入后，在产品期限内保持不动。 |
| 静态管理风格（static management style） | 参考资产组合在存续期内保持固定的管理方式。 |
| 次级担保债务凭证权益档（subordinated CDO equity） | 次级（亦称权益）CDO 分档是 CDO 发行中最末尾的分档，违约或抵押品表现不佳时最先承担损失。 |
| 次级抵押支持证券分档（subordinated MBS tranche） | MBS 发行中优先级最低的分档。 |
| 超级浮动分档（super floater tranche） | 票息杠杆放大浮动利率变动的分档。 |
| 超级仅付本分档（super PO tranche） | 仅支付本金的分档（Principal Only）的一种特殊形式。 |
| 超优先担保债务凭证分档（super senior CDO tranche） | 位于 CDO 发行最顶端的分档。 |
| 支持分档（support tranche） | 为计划摊销档（PAC）分档提供付款支持的分档。 |
| 目标摊销档（TAC tranche） | 目标摊销档（TAC）：与 PAC 分档相关，具有针对特定提前偿付速度（称为定价速度）的付款计划表。 |
| 目标摊销档摊销计划表（TAC tranche amortization schedule） | 目标摊销档（TAC）分档的本金摊销计划表。 |
| 分档发行时评级（tranche rating at issue） | 证券某一档在发行时的评级。 |
| 分档类型（tranche type） | 指明分档的类型。 |
| 分档型抵押支持证券交易（tranched MBS deal） | 分档型 MBS 的一次发行。 |
| 分档型抵押支持证券交易招募说明书（tranched MBS deal prospectus） | 分档型 MBS 发行的招募说明书。 |
| 分档型抵押支持证券工具（tranched MBS instrument） | 分档型 MBS 的工具。 |
| 触发事件（trigger event） | 某一数值越过某一阈值的事件，或其他类型的业务事件。 |
| 真实出售目标（true sale objective） | 以实现资产真实出售为目的的发起目标。 |

### 2.1 继承关系（Inheritance）

- 资产支持证券担保债务凭证交易（ABS CDO deal） ⊑ 担保债务凭证交易（CDO deal）
- 资产支持证券担保债务凭证工具（ABS CDO instrument） ⊑ 现金型担保债务凭证分档（cash CDO tranche）
- 机构抵押担保债券（agency CMO） ⊑ 债务发行
- 机构仅付息分档（agency IO tranche） ⊑ 机构抵押担保债券（agency CMO）
- 机构跳转分档（agency jump tranche） ⊑ 机构抵押担保债券（agency CMO）
- 机构跳转 Z 分档（agency jump Z tranche） ⊑ 机构跳转分档（agency jump tranche）
- 机构跳转 Z 分档（agency jump Z tranche） ⊑ 机构 Z 分档（agency Z tranche）
- 机构仅付本分档（agency PO tranche） ⊑ 机构抵押担保债券（agency CMO）
- 机构常规跳转 Z 分档（agency regular jump Z） ⊑ 机构跳转 Z 分档（agency jump Z tranche）
- 机构粘性跳转 Z 分档（agency sticky jump Z） ⊑ 机构跳转 Z 分档（agency jump Z tranche）
- 机构 Z 分档（agency Z tranche） ⊑ 机构抵押担保债券（agency CMO）
- 套利型担保债务凭证（arbitrage CDO） ⊑ 担保债务凭证交易（CDO deal）
- 套利型目标（arbitrage CDO objective） ⊑ 担保债务凭证发起目标（CDO origination objective）
- 资产负债表型担保债务凭证（balance sheet CDO） ⊑ 担保债务凭证交易（CDO deal）
- 资产负债表型目标（balance sheet CDO objective） ⊑ 担保债务凭证发起目标（CDO origination objective）
- 担保债务凭证现金流处理结构（CDO cashflow treatment structure） ⊑ 战略
- 担保债务凭证交易（CDO deal） ⊑ 债务发行
- 担保债务凭证管理风格（CDO management style） ⊑ 战略
- 担保债务凭证发起目标（CDO origination objective） ⊑ 目标
- 担保债务凭证池（CDO pool） ⊑ 债务池
- 担保债务凭证组合（CDO portfolio） ⊑ 组合
- 担保债务凭证组合管理人（CDO portfolio manager） ⊑ 参与方角色（party role）
- 双层担保债务凭证交易（CDO squared deal） ⊑ 担保债务凭证交易（CDO deal）
- 双层担保债务凭证工具（CDO squared instrument） ⊑ 担保债务凭证（collateralized debt obligation）
- 抵押担保债券交易（CMO deal） ⊑ 债务发行
- 现金型资产支持证券池（cash ABS pool） ⊑ 债务池
- 现金型担保债务凭证（cash CDO） ⊑ 担保债务凭证交易（CDO deal）
- 现金型担保债务凭证分档（cash CDO tranche） ⊑ 担保债务凭证（collateralized debt obligation）
- 现金型担保债务凭证分档（cash CDO tranche） ⊑ 分档
- 现金流型担保债务凭证（cashflow CDO） ⊑ 担保债务凭证交易（CDO deal）
- 现金流结构（cashflow structure） ⊑ 担保债务凭证现金流处理结构（CDO cashflow treatment structure）
- 担保债券凭证（collateralized bond obligation） ⊑ 现金型担保债务凭证分档（cash CDO tranche）
- 担保债务凭证（collateralized debt obligation） ⊑ 结构化金融工具
- 担保贷款凭证发行（collateralized loan obligation offering） ⊑ 债务发行
- 浮动分档（floater tranche） ⊑ 分档型抵押支持证券工具（tranched MBS instrument）
- 混合型担保债务凭证（hybrid CDO） ⊑ 担保债务凭证交易（CDO deal）
- 小仅付息分档（IOette） ⊑ 机构仅付息分档（agency IO tranche）
- 反向浮动分档（inverse floater tranche） ⊑ 浮动分档（floater tranche）
- 跳转 Z 触发事件（jump Z trigger event） ⊑ 触发事件（trigger event）
- 跳转 Z 触发事件解除（jump z trigger event reversal） ⊑ 触发事件（trigger event）
- 贷款池（loan pool） ⊑ 债务池
- 抵押支持证券工具切片（MBS instrument slice） ⊑ 组合
- 抵押支持证券分档票据（MBS tranche note） ⊑ 本票
- 管理型担保债务凭证（managed CDO） ⊑ 担保债务凭证交易（CDO deal）
- 管理型担保债务凭证组合（managed CDO portfolio） ⊑ 担保债务凭证组合（CDO portfolio）
- 管理型管理风格（managed management style） ⊑ 担保债务凭证管理风格（CDO management style）
- 市值型担保债务凭证（market value CDO） ⊑ 担保债务凭证交易（CDO deal）
- 市值结构（market value structure） ⊑ 担保债务凭证现金流处理结构（CDO cashflow treatment structure）
- 夹层担保债务凭证分档（mezzanine CDO tranche） ⊑ 担保债务凭证（collateralized debt obligation）
- 夹层抵押支持证券分档（mezzanine MBS tranche） ⊑ 分档型抵押支持证券工具（tranched MBS instrument）
- 非机构仅付息分档（non-agency IO tranche） ⊑ 分档型抵押支持证券工具（tranched MBS instrument）
- 非机构跳转分档（non-agency jump tranche） ⊑ 分档型抵押支持证券工具（tranched MBS instrument）
- 非机构跳转 Z 分档（non-agency jump Z tranche） ⊑ 非机构跳转分档（non-agency jump tranche）
- 非机构跳转 Z 分档（non-agency jump Z tranche） ⊑ 非机构 Z 分档（non-agency Z tranche）
- 非机构仅付本分档（non-agency PO tranche） ⊑ 分档型抵押支持证券工具（tranched MBS instrument）
- 非机构常规跳转 Z 分档（non-agency regular jump Z tranche） ⊑ 非机构跳转 Z 分档（non-agency jump Z tranche）
- 非机构粘性跳转 Z 分档（non-agency sticky jump Z tranche） ⊑ 非机构跳转 Z 分档（non-agency jump Z tranche）
- 非机构 Z 分档（non-agency Z tranche） ⊑ 分档型抵押支持证券工具（tranched MBS instrument）
- 计划摊销仅付本分档（PAC PO tranche） ⊑ 机构仅付本分档（agency PO tranche）
- 计划摊销仅付本分档（PAC PO tranche） ⊑ 计划摊销档债券（planned amortization class bond）
- 计划摊销档摊销计划表（PAC tranche amortization schedule） ⊑ 赎回计划表
- 计划摊销 Z 分档（PAC-Z tranche） ⊑ 机构 Z 分档（agency Z tranche）
- 计划摊销 Z 分档（PAC-Z tranche） ⊑ 计划摊销档债券（planned amortization class bond）
- 计划摊销一档（PAC-1 class） ⊑ 计划摊销档债券（planned amortization class bond）
- 计划摊销二档（PAC-2 class） ⊑ 计划摊销档债券（planned amortization class bond）
- 计划摊销三档（PAC-3 class） ⊑ 计划摊销档债券（planned amortization class bond）
- 计划摊销档债券（planned amortization class bond） ⊑ 机构抵押担保债券（agency CMO）
- 常规浮动分档（regular floater tranche） ⊑ 浮动分档（floater tranche）
- 剩余分档（residual tranche） ⊑ 分档型抵押支持证券工具（tranched MBS instrument）
- 优先担保债务凭证分档（senior CDO tranche） ⊑ 担保债务凭证（collateralized debt obligation）
- 优先担保债务凭证分档（senior CDO tranche） ⊑ 分档
- 优先抵押支持证券分档（senior MBS tranche） ⊑ 分档型抵押支持证券工具（tranched MBS instrument）
- 静态担保债务凭证（static CDO） ⊑ 担保债务凭证交易（CDO deal）
- 静态担保债务凭证组合（static CDO portfolio） ⊑ 担保债务凭证组合（CDO portfolio）
- 静态管理风格（static management style） ⊑ 担保债务凭证管理风格（CDO management style）
- 次级担保债务凭证权益档（subordinated CDO equity） ⊑ 证券
- 次级抵押支持证券分档（subordinated MBS tranche） ⊑ 分档型抵押支持证券工具（tranched MBS instrument）
- 超级浮动分档（super floater tranche） ⊑ 浮动分档（floater tranche）
- 超级仅付本分档（super PO tranche） ⊑ 机构仅付本分档（agency PO tranche）
- 超优先担保债务凭证分档（super senior CDO tranche） ⊑ 担保债务凭证（collateralized debt obligation）
- 目标摊销档（TAC tranche） ⊑ 机构抵押担保债券（agency CMO）
- 目标摊销档（TAC tranche） ⊑ 分档型抵押支持证券工具（tranched MBS instrument）
- 目标摊销档摊销计划表（TAC tranche amortization schedule） ⊑ 赎回计划表
- 分档型抵押支持证券交易（tranched MBS deal） ⊑ 债务发行
- 分档型抵押支持证券交易招募说明书（tranched MBS deal prospectus） ⊑ 抵押支持证券发行招募说明书
- 分档型抵押支持证券工具（tranched MBS instrument） ⊑ 抵押支持证券
- 真实出售目标（true sale objective） ⊑ 担保债务凭证发起目标（CDO origination objective）

## 3. 对象属性（Object Property）

| 属性（Property） | 中文（English） | 定义（Definition） | 说明 |
|---|---|---|---|
| fibo-sec-dbt-cdo:cashflowPrecedence | 现金流优先顺序（cashflow precedence） | 指明各分档获得现金流的先后次序。 | 定义域（domain）：分档型抵押支持证券工具（tranched MBS instrument）；值域（range）：分档型抵押支持证券工具（tranched MBS instrument）；逆属性（inverseOf）：为……提供信用支持（provides credit support to） |
| fibo-sec-dbt-cdo:confersOwnershipOf | 授予……的所有权（confers ownership of） | 表明某凭证或分档授予对某一资产或现金流的权利。 | 定义域（domain）：次级担保债务凭证权益档（subordinated CDO equity） |
| fibo-sec-dbt-cdo:denomination | 票面金额（denomination） | 票据计价的货币金额，例如 500 美元面额的票据。 | 定义域（domain）：抵押支持证券分档票据（MBS tranche note）；值域（range）：货币数量 |
| fibo-sec-dbt-cdo:hasCDOOriginationObjective | 具有担保债务凭证发起目标（has CDO origination objective） | 指明 CDO 发行的发起目标或动机。 | 定义域（domain）：担保债务凭证交易（CDO deal）；值域（range）：担保债务凭证发起目标（CDO origination objective） |
| fibo-sec-dbt-cdo:managementStyle | 具有交易管理风格（has deal management style） | 表明 CDO 是静态还是管理型，即 CDO 管理人是否可在存续期内调整参考组合。 | 定义域（domain）：担保债务凭证（collateralized debt obligation）；值域（range）：担保债务凭证管理风格（CDO management style） |
| fibo-sec-dbt-cdo:origination.2 | 具有发起目标（has origination objective） | 指明发行的发起目标或动机。 | 定义域（domain）：担保债务凭证（collateralized debt obligation）；值域（range）：担保债务凭证发起目标（CDO origination objective） |
| fibo-sec-dbt-cdo:structure | 具有结构类型（has structure type） | 指明 CDO 的资金来源类型，即现金流型或市值型。 | 定义域（domain）：担保债务凭证（collateralized debt obligation）；值域（range）：担保债务凭证现金流处理结构（CDO cashflow treatment structure） |
| fibo-sec-dbt-cdo:hasTrancheType | 具有分档类型（has tranche type） | 指明分档的类型。 | 定义域（domain）：结构化金融工具；值域（range）：分档类型（tranche type） |
| fibo-sec-dbt-cdo:isAlso.1 | 同时是（is also） | 表明某分档同时属于另一类型。 | 定义域（domain）：分档型抵押支持证券交易（tranched MBS deal）；值域（range）：私募品牌抵押支持证券交易 |
| fibo-sec-dbt-cdo:issues | 发行（issues） | 正式使某事物可得。 | 定义域（domain）：现金型担保债务凭证（cash CDO）；值域（range）：现金型担保债务凭证分档（cash CDO tranche） |
| fibo-sec-dbt-cdo:managementStyle.1 | 管理风格（management style） | 参考资产购入后（组合逐步建成），CDO 管理人可酌情调整组合的管理方式。 | 定义域（domain）：担保债务凭证交易（CDO deal）；值域（range）：担保债务凭证管理风格（CDO management style） |
| fibo-sec-dbt-cdo:providesCreditSupportTo | 为……提供信用支持（provides credit support to） | 表明某分档为另一分档提供信用增进。 | 定义域（domain）：分档型抵押支持证券工具（tranched MBS instrument）；值域（range）：分档型抵押支持证券工具（tranched MBS instrument）；子属性（subPropertyOf）：次于 |
| fibo-sec-dbt-cdo:providesPrepaymentSupport | 提供提前偿付支持（provides prepayment support） | 表明某分档吸收提前偿付变动以保护其他分档。 | 定义域（domain）：机构抵押担保债券（agency CMO）；值域（range）：机构抵押担保债券（agency CMO） |
| fibo-sec-dbt-cdo:providesPrepaymentSupportFor | 为……提供提前偿付支持（provides prepayment support for） | 表明某分档为另一特定分档吸收提前偿付变动。 | 定义域（domain）：计划摊销档债券（planned amortization class bond）；值域（range）：计划摊销档债券（planned amortization class bond）；逆属性（inverseOf）：由……支持（supported by）；子属性（subPropertyOf）：提供提前偿付支持（provides prepayment support） |
| fibo-sec-dbt-cdo:ratedAtIssue | 发行时评级（rated at issue） | 分档在发行时所获得的评级。 | 定义域（domain）：夹层担保债务凭证分档（mezzanine CDO tranche）；值域（range）：分档发行时评级（tranche rating at issue） |
| fibo-sec-dbt-cdo:ratedAtIssue.1 | 发行时评级（rated at issue） | 分档在发行时所获得的评级。 | 定义域（domain）：优先担保债务凭证分档（senior CDO tranche）；值域（range）：分档发行时评级（tranche rating at issue） |
| fibo-sec-dbt-cdo:reverts | 恢复（reverts） | 表明触发事件解除后该分档恢复原有付款状态。 | 定义域（domain）：非机构常规跳转 Z 分档（non-agency regular jump Z tranche）；值域（range）：跳转 Z 触发事件解除（jump z trigger event reversal） |
| fibo-sec-dbt-cdo:revertsOn | 于……时恢复（reverts on） | 指明使该分档恢复原有付款状态的事件。 | 定义域（domain）：机构常规跳转 Z 分档（agency regular jump Z）；值域（range）：跳转 Z 触发事件解除（jump z trigger event reversal） |
| fibo-sec-dbt-cdo:seniorTo | 优先于（senior to） | 表明某一分档在受偿顺序上优先于另一分档。 | 定义域（domain）：夹层抵押支持证券分档（mezzanine MBS tranche）；值域（range）：夹层抵押支持证券分档（mezzanine MBS tranche）；子属性（subPropertyOf）：现金流优先顺序（cashflow precedence） |
| fibo-sec-dbt-cdo:seniority | 优先级别（seniority） | 界定该分档的优先级别，即计划付款的先后次序；分档通常分为优先、夹层和次级。 | 定义域（domain）：担保债务凭证（collateralized debt obligation）；值域（range）：担保债务凭证分档优先级选择（CDOTrancheSenioritySelection） |
| fibo-sec-dbt-cdo:specifies | 规定（specifies） | 清晰而确定地提及、命名或陈述某事物。 | 定义域（domain）：计划摊销档债券（planned amortization class bond）；值域（range）：计划摊销档摊销计划表（PAC tranche amortization schedule） |
| fibo-sec-dbt-cdo:specifies.1 | 规定（specifies） | 清晰而确定地提及、命名或陈述某事物。 | 定义域（domain）：目标摊销档（TAC tranche）；值域（range）：目标摊销档摊销计划表（TAC tranche amortization schedule） |
| fibo-sec-dbt-cdo:specifiesReverseTrigger | 规定反向触发（specifies reverse trigger） | 规定使分档恢复原有状态的反向触发事件。 | 定义域（domain）：跳转 Z 触发事件解除（jump z trigger event reversal）；值域（range）：跳转 Z 触发事件（jump Z trigger event） |
| fibo-sec-dbt-cdo:specifiesTrigger | 规定触发（specifies trigger） | 规定一旦发生时使跳转 Z 持有人开始接收付款的事件。 | 定义域（domain）：机构跳转分档（agency jump tranche）；值域（range）：跳转 Z 触发事件（jump Z trigger event） |
| fibo-sec-dbt-cdo:structure.2 | 结构（structure） | CDO 的资金来源为市值，即向投资者支付的本金和利息来自抵押品现金流及抵押品出售所得。 | 定义域（domain）：担保债务凭证交易（CDO deal）；值域（range）：担保债务凭证现金流处理结构（CDO cashflow treatment structure） |
| fibo-sec-dbt-cdo:supportedBy | 由……支持（supported by） | 表明某分档由另一分档提供付款支持。 | 定义域（domain）：计划摊销档债券（planned amortization class bond）；值域（range）：计划摊销档债券（planned amortization class bond） |
| fibo-sec-dbt-cdo:takesPrepaymentAfter | 在……之后承担提前偿付（takes prepayment after） | 表明某分档在另一分档之后承担提前偿付现金流。 | 定义域（domain）：计划摊销一档（PAC-1 class）；值域（range）：计划摊销二档（PAC-2 class）；子属性（subPropertyOf）：由……支持（supported by） |
| fibo-sec-dbt-cdo:takesPrepaymentAfter.1 | 在……之后承担提前偿付（takes prepayment after） | 表明某分档在另一分档之后承担提前偿付现金流。 | 定义域（domain）：计划摊销二档（PAC-2 class）；值域（range）：计划摊销三档（PAC-3 class）；子属性（subPropertyOf）：由……支持（supported by） |

## 4. 数据属性（Datatype Property）

| 属性（Property） | 中文（English） | 定义（Definition） |
|---|---|---|
| fibo-sec-dbt-cdo:isCash | 是否现金型（is cash） | 表明 CDO 是否拥有真实资产的标的池：是则为现金型，否则为合成型标的池。 |
| fibo-sec-dbt-cdo:isCash.1 | 是否现金型（is cash） | 表明 CDO 是否拥有真实资产的标的池：是则为现金型，否则为合成型标的池。 |
| fibo-sec-dbt-cdo:seniority.1 | 优先级别（seniority） | 界定该分档的优先级别，即计划付款的先后次序；分档通常分为优先、夹层和次级。 |
| fibo-sec-dbt-cdo:seniority.2 | 优先级别（seniority） | 界定该分档的优先级别，即计划付款的先后次序；分档通常分为优先、夹层和次级。 |
| fibo-sec-dbt-cdo:seniority.3 | 优先级别（seniority） | 界定该分档的优先级别，即计划付款的先后次序；分档通常分为优先、夹层和次级。 |
| fibo-sec-dbt-cdo:seniority.4 | 优先级别（seniority） | 界定该分档的优先级别，即计划付款的先后次序；分档通常分为优先、夹层和次级。 |

## 5. 公理约定（Axioms）

- 资产支持证券担保债务凭证交易（ABS CDO deal）：包含 some（restriction）
- 机构抵押担保债券（agency CMO）：具有分档类型（has tranche type） some 分档类型（tranche type）
- 机构抵押担保债券（agency CMO）：提供提前偿付支持（provides prepayment support） some 机构抵押担保债券（agency CMO）
- 机构抵押担保债券（agency CMO）：包含 some 机构抵押支持证券池
- 机构仅付息分档（agency IO tranche） 与 机构仅付本分档（agency PO tranche） 互斥（disjointWith）
- 机构跳转分档（agency jump tranche）：规定触发（specifies trigger） some 跳转 Z 触发事件（jump Z trigger event）
- 机构常规跳转 Z 分档（agency regular jump Z）：于……时恢复（reverts on） some 跳转 Z 触发事件解除（jump z trigger event reversal）
- 套利型担保债务凭证（arbitrage CDO）：具有担保债务凭证发起目标（has CDO origination objective） some 套利型目标（arbitrage CDO objective）
- 资产负债表型担保债务凭证（balance sheet CDO）：具有担保债务凭证发起目标（has CDO origination objective） some 资产负债表型目标（balance sheet CDO objective）
- 担保债务凭证交易（CDO deal）：具有成员 some 担保债务凭证组合（CDO portfolio）
- 担保债务凭证交易（CDO deal）：具有成员 some 夹层担保债务凭证分档（mezzanine CDO tranche）
- 担保债务凭证交易（CDO deal）：具有成员 some 优先担保债务凭证分档（senior CDO tranche）
- 担保债务凭证交易（CDO deal）：具有成员 some 次级担保债务凭证权益档（subordinated CDO equity）
- 担保债务凭证交易（CDO deal）：具有成员 some 超优先担保债务凭证分档（super senior CDO tranche）
- 担保债务凭证交易（CDO deal）：适用于 some 担保债务凭证（collateralized debt obligation）
- 担保债务凭证交易（CDO deal）：由……管理 some 担保债务凭证组合管理人（CDO portfolio manager）
- 担保债务凭证组合（CDO portfolio）：具有成员 some 抵押支持证券工具切片（MBS instrument slice）
- 担保债务凭证组合（CDO portfolio）：由……管理 some 担保债务凭证组合管理人（CDO portfolio manager）
- 担保债务凭证组合管理人（CDO portfolio manager）：管理 some 担保债务凭证组合（CDO portfolio）
- 双层担保债务凭证交易（CDO squared deal）：包含 some 担保债务凭证池（CDO pool）
- 现金型担保债务凭证（cash CDO）：发行（issues） some 现金型担保债务凭证分档（cash CDO tranche）
- 现金型担保债务凭证（cash CDO） 与 合成担保债务凭证 互斥（disjointWith）
- 现金型担保债务凭证分档（cash CDO tranche）：是……的部分 some 债务池
- 现金型担保债务凭证分档（cash CDO tranche） 与 资产支持证券 互斥（disjointWith）
- 现金型担保债务凭证分档（cash CDO tranche） 与 合成担保债务凭证分档 互斥（disjointWith）
- 现金流型担保债务凭证（cashflow CDO）：结构（structure） some 现金流结构（cashflow structure）
- 现金流型担保债务凭证（cashflow CDO） 与 市值型担保债务凭证（market value CDO） 互斥（disjointWith）
- 担保债券凭证（collateralized bond obligation）：引用 some 债券池
- 担保债券凭证（collateralized bond obligation） 与 机构抵押担保债券（agency CMO） 互斥（disjointWith）
- 担保债券凭证（collateralized bond obligation） 与 担保贷款凭证发行（collateralized loan obligation offering） 互斥（disjointWith）
- 担保债务凭证（collateralized debt obligation）：次于 担保债务凭证（collateralized debt obligation） ≤1
- 担保贷款凭证发行（collateralized loan obligation offering）：引用 some 贷款池（loan pool）
- 担保贷款凭证发行（collateralized loan obligation offering） 与 机构抵押担保债券（agency CMO） 互斥（disjointWith）
- 浮动分档（floater tranche）：具有重复区间 some 月中日
- 混合型担保债务凭证（hybrid CDO）：适用于 only N08f036e3f4af4fe3b5a3065f0c3d2461
- 反向浮动分档（inverse floater tranche） 与 常规浮动分档（regular floater tranche） 互斥（disjointWith）
- 反向浮动分档（inverse floater tranche） 与 超级浮动分档（super floater tranche） 互斥（disjointWith）
- 跳转 Z 触发事件解除（jump z trigger event reversal）：规定反向触发（specifies reverse trigger） some 跳转 Z 触发事件（jump Z trigger event）
- 贷款池（loan pool）：具有成员 some 贷款
- 抵押支持证券工具切片（MBS instrument slice）：引用 some（restriction）
- 管理型担保债务凭证（managed CDO）：管理风格（management style） some 管理型管理风格（managed management style）
- 管理型担保债务凭证（managed CDO）：具有成员 some 抵押支持证券工具切片（MBS instrument slice）
- 管理型担保债务凭证（managed CDO）：具有成员 some 管理型担保债务凭证组合（managed CDO portfolio）
- 管理型担保债务凭证（managed CDO） 与 静态担保债务凭证（static CDO） 互斥（disjointWith）
- 市值型担保债务凭证（market value CDO）：结构（structure） some 市值结构（market value structure）
- 夹层担保债务凭证分档（mezzanine CDO tranche）：发行时评级（rated at issue） some 分档发行时评级（tranche rating at issue）
- 夹层抵押支持证券分档（mezzanine MBS tranche）：优先于（senior to） some 次级抵押支持证券分档（subordinated MBS tranche）
- 非机构跳转分档（non-agency jump tranche）：规定触发（specifies trigger） some 跳转 Z 触发事件（jump Z trigger event）
- 非机构常规跳转 Z 分档（non-agency regular jump Z tranche）：恢复（reverts） some 跳转 Z 触发事件解除（jump z trigger event reversal）
- 计划摊销一档（PAC-1 class）：在……之后承担提前偿付（takes prepayment after） only 计划摊销二档（PAC-2 class）
- 计划摊销二档（PAC-2 class）：在……之后承担提前偿付（takes prepayment after） only 计划摊销三档（PAC-3 class）
- 计划摊销档债券（planned amortization class bond）：为……提供提前偿付支持（provides prepayment support for） only 计划摊销档债券（planned amortization class bond）
- 计划摊销档债券（planned amortization class bond）：由……支持（supported by） only 计划摊销档债券（planned amortization class bond）
- 计划摊销档债券（planned amortization class bond）：规定（specifies） some 计划摊销档摊销计划表（PAC tranche amortization schedule）
- 常规浮动分档（regular floater tranche） 与 超级浮动分档（super floater tranche） 互斥（disjointWith）
- 优先担保债务凭证分档（senior CDO tranche）：发行时评级（rated at issue） some 分档发行时评级（tranche rating at issue）
- 优先抵押支持证券分档（senior MBS tranche）：优先于（senior to） some 夹层抵押支持证券分档（mezzanine MBS tranche）
- 静态担保债务凭证（static CDO）：管理风格（management style） some 静态管理风格（static management style）
- 支持分档（support tranche）：由…扮演（is played by） some 计划摊销二档（PAC-2 class）
- 目标摊销档（TAC tranche）：规定（specifies） some 目标摊销档摊销计划表（TAC tranche amortization schedule）
- 分档型抵押支持证券交易（tranched MBS deal）：同时是（is also） some 私募品牌抵押支持证券交易
- 分档型抵押支持证券工具（tranched MBS instrument）：现金流优先顺序（cashflow precedence） only 分档型抵押支持证券工具（tranched MBS instrument）
- 分档型抵押支持证券工具（tranched MBS instrument）：为……提供信用支持（provides credit support to） only 分档型抵押支持证券工具（tranched MBS instrument）
- 分档型抵押支持证券工具（tranched MBS instrument）：具有票据 some 抵押支持证券分档票据（MBS tranche note）

## 6. 依赖（owl:imports，27 个）

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

## 7. 文件

- 官方 RDF/XML：`CollateralizedDebtObligations.rdf`
- 中文 Turtle：`CollateralizedDebtObligations.ttl`
- 结构图：`CollateralizedDebtObligations-structure.png` / `CollateralizedDebtObligations-structure.svg`