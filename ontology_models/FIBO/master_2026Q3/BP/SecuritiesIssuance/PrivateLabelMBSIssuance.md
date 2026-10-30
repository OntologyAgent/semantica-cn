# 私人品牌 MBS 发行本体（Private Label MBS Issuance Ontology）结构与公理说明

本文档对应 `PrivateLabelMBSIssuance.rdf` / `PrivateLabelMBSIssuance.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `PrivateLabelMBSIssuance-structure.png`（`PrivateLabelMBSIssuance-structure.svg` 为可缩放版本）。

![私人品牌 MBS 发行本体（Private Label MBS Issuance Ontology）本体结构图](PrivateLabelMBSIssuance-structure.png)

## 1. 本体概述

定义私人品牌抵押贷款支持证券（private label MBS）的发行流程：由私人金融机构（非政府机构）组建贷款池并发行。

**在体系中的位置**：BP 证券发行模块中 MBS 发行的两个子类之一。

**上下游关系**：上游继承 MBS 发行本体；下游关联 SEC 抵押贷款支持证券与担保债务凭证本体。

**与相近概念的差别**：与机构 MBS 发行的差别——没有机构担保，需要依靠分层、超额抵押等信用增级手段，2008 年金融危机中出问题的主要是这类。

## 2. 类（Class）

| 类（Class） | 定义（Definition） |
|---|---|
| 池生命周期状态选择（PoolLifecycleStateSelection） | 对抵押贷款池生命周期状态的选择。 |
| 分配主标识符（allocate primary identifier） | 为证券分配主要标识符。 |
| 分配评级（allocate ratings） | 为各分层证券确定评级。 |
| 评估池的发行适用性（assess pool suitability for issuance） | 评估抵押贷款池是否适合用于发行。 |
| 评估评级（assess ratings） | 对分层证券可获得的评级进行评估。 |
| 经纪自营商（broker dealer） | 可能成为本次发行主要投资者的实体。 |
| 完成交易（close deal） | 完成本次发行交易。 |
| 定义票据参数（define notes parameters） | 定义票据的面额等参数。 |
| 定义池特征（define pool characteristics） | 确定抵押贷款池的特征。 |
| 起草分层票据参数（draft tranche notes parameters） | 起草定义某一分层票据细分（面额及可购金额）的信息集。 |
| 起草分层结构（draft tranche structure） | 起草定义分层发行中各分层及其相互关系的信息集。 |
| 起草分层条款清单（draft tranche termsheet） | 起草定义分层发行中某一分层的信息集，将成为该分层的条款清单。 |
| 拟定发行备忘录（draw up offering memorandum） | 拟定载明未来发行基本信息、供潜在投资者参考的发行备忘录。 |
| 拟定各分层条款清单（draw up tranche termsheets） | 拟定分层发行中各分层的条款清单。 |
| 定稿池内容（finalize pool content） | 最终确定抵押贷款池的构成内容。 |
| 定稿招募说明书（finalize prospectus） | 最终确定发行的招募说明书。 |
| 获得投资者承诺（get commitment from investors） | 取得投资者认购本次发行的承诺。 |
| 识别合格抵押贷款（identify conforming mortgage） | 识别符合该发行人总体要求的抵押贷款。 |
| 确定承销商（identify underwriter） | 确定本次发行的承销商。 |
| 组建中抵押贷款池（in assembly mortgage pool） | 尚在组建、内容未定的抵押贷款池。 |
| 发行中非机构抵押贷款池（in issuance non agency mortgage pool） | 正在发行过程中的非机构抵押贷款池。 |
| 各分层定义（individual tranche definitions） | 标识分层发行中单个分层之条款的信息类别（实际为一份条款清单中针对各分层的条款信息集）。 |
| 投资者（investor） | 通过投资拥有某组织一定份额的参与方。 |
| MBS 证券化结束（m b s securitization end） | MBS 证券化流程的结束节点。 |
| MBS 证券化开始（m b s securitization start） | MBS 证券化流程的起始节点。 |
| 使证券进入市场（make securities available in market） | 使所发行证券可在市场上获得（结构化融资市场较小，主要通过定向营销）。 |
| 向主要投资者营销发行（market issue to primary investors） | 面向主要投资者对本次发行进行营销。 |
| 非机构池创建结束（non agency pool creation end） | 非机构抵押贷款池创建流程的结束节点。 |
| 非机构池创建流程（non agency pool creation process） | 私募（非机构）抵押贷款池的创建过程。 |
| 非机构池创建开始（non agency pool creation start） | 非机构抵押贷款池创建流程的起始节点。 |
| 未发行非机构抵押贷款池（not yet issued non agency mortgage pool） | 已组建但尚未发行的非机构抵押贷款池。 |
| 编号机构（numbering agency） | 为证券提供主要证券标识符的机构。 |
| 池可发行（pool ready for issue） | 抵押贷款池已具备发行条件的状态。 |
| 池受托人（pool trustee） | 为资产池担任受托人的参与方。 |
| 潜在 MBS 投资者（potential m b s investor） | 可能成为 MBS 发行投资者的参与方。 |
| 潜在非机构 MBS 发行人（potential non agency m b s issuer） | 将成为分层 MBS 发行发行方的实体，是发行中大多数活动的主要行为体。 |
| 潜在分层发行承销商（potential tranched issue underwriter） | 将成为分层 MBS 发行承销商的实体。 |
| 主要投资者（primary investor） | 通过购买本次发行的部分分层而成为主要投资者的参与方。 |
| 购入抵押贷款入池（purchase mortgage into pool） | 购入抵押贷款并将其纳入资产池。 |
| 评级机构（ratings agency） | 为发行提供评级的机构。 |
| 评级适合发行（ratings suitable for issue） | 评级结果满足发行要求的状态。 |
| 注册证券（register security） | 交易完成后将证券在注册机构正式注册。 |
| 汇款报告（remittance report） | 包含关于本次交易的特定有限信息集的报告。 |
| 分层票据参数（tranche notes parameters） | 定义某一分层票据细分（面额及该分层中可购金额）的一组信息。 |
| 分层结构与条款清单（tranche structure and termsheet） | 定义 MBS 结构的一份清单。 |
| 分层招募说明书草案（tranched draft prospectus） | 发行实体在营销发行前确定的分层 MBS 发行招募说明书草案。 |
| 分层 MBS 交易结算（tranched m b s deal settlement） | 分层 MBS 交易的结算。 |
| 分层 MBS 交易（tranched m b s deal transaction） | 据以向主要投资者发行 MBS 的交易。 |
| 分层 MBS 发行招募说明书部分（tranched m b s issue prospectus part） | 分层 MBS 发行招募说明书的一个部分或章节。 |
| 分层 MBS 一级交易结算流程（tranched m b s primary deal transaction settlement process） | 一级交易完成结算的过程。 |
| 分层 MBS 招募说明书大纲（tranched m b s prospectus outline） | 分层招募说明书的大纲，提供可能分层及其特征的初步表示。 |
| 分层 MBS 证券化流程（tranched m b s securitization process） | 分层抵押贷款支持证券的证券化过程。 |
| 分层发行备忘录（tranched offering memorandum） | 发行备忘录，包含或附上构成本次发行的两个或多个分层的条款及分层结构。 |

### 2.1 继承关系（Inheritance）

- 池生命周期状态选择（PoolLifecycleStateSelection） ⊑ 生命周期阶段
- 分配主标识符（allocate primary identifier） ⊑ 发行流程活动
- 分配评级（allocate ratings） ⊑ 发行流程活动
- 评估池的发行适用性（assess pool suitability for issuance） ⊑ 发行流程活动
- 评估评级（assess ratings） ⊑ 发行流程活动
- 完成交易（close deal） ⊑ 发行流程活动
- 定义票据参数（define notes parameters） ⊑ 发行流程活动
- 定义池特征（define pool characteristics） ⊑ 发行流程活动
- 起草分层票据参数（draft tranche notes parameters） ⊑ 文件
- 起草分层结构（draft tranche structure） ⊑ 文件
- 起草分层条款清单（draft tranche termsheet） ⊑ 条款清单
- 拟定发行备忘录（draw up offering memorandum） ⊑ 发行流程活动
- 拟定各分层条款清单（draw up tranche termsheets） ⊑ 发行流程活动
- 定稿池内容（finalize pool content） ⊑ 发行流程活动
- 定稿招募说明书（finalize prospectus） ⊑ 发行流程活动
- 获得投资者承诺（get commitment from investors） ⊑ 发行流程活动
- 识别合格抵押贷款（identify conforming mortgage） ⊑ 发行流程活动
- 确定承销商（identify underwriter） ⊑ 发行流程活动
- 组建中抵押贷款池（in assembly mortgage pool） ⊑ 非机构抵押贷款池
- 发行中非机构抵押贷款池（in issuance non agency mortgage pool） ⊑ 非机构抵押贷款池
- 各分层定义（individual tranche definitions） ⊑ 分层 MBS 发行招募说明书部分（tranched m b s issue prospectus part）
- 各分层定义（individual tranche definitions） ⊑ 条款清单
- 使证券进入市场（make securities available in market） ⊑ 发行流程活动
- 向主要投资者营销发行（market issue to primary investors） ⊑ 发行流程活动
- 非机构池创建流程（non agency pool creation process） ⊑ 零售资产池创建流程
- 未发行非机构抵押贷款池（not yet issued non agency mortgage pool） ⊑ 非机构抵押贷款池
- 编号机构（numbering agency） ⊑ 证券发行流程参与者
- 池受托人（pool trustee） ⊑ 参与方角色（party role）
- 潜在非机构 MBS 发行人（potential non agency m b s issuer） ⊑ 池支持证券证券化流程参与者
- 潜在分层发行承销商（potential tranched issue underwriter） ⊑ 潜在承销商
- 购入抵押贷款入池（purchase mortgage into pool） ⊑ 发行流程活动
- 注册证券（register security） ⊑ 发行流程活动
- 汇款报告（remittance report） ⊑ 报告
- 分层票据参数（tranche notes parameters） ⊑ 分层 MBS 发行招募说明书部分（tranched m b s issue prospectus part）
- 分层结构与条款清单（tranche structure and termsheet） ⊑ 分层 MBS 发行招募说明书部分（tranched m b s issue prospectus part）
- 分层招募说明书草案（tranched draft prospectus） ⊑ 初步招募说明书
- 分层 MBS 交易（tranched m b s deal transaction） ⊑ 金融一级市场交易
- 分层 MBS 发行招募说明书部分（tranched m b s issue prospectus part） ⊑ 招募说明书部分
- 分层 MBS 一级交易结算流程（tranched m b s primary deal transaction settlement process） ⊑ 结算过程
- 分层 MBS 招募说明书大纲（tranched m b s prospectus outline） ⊑ 初步招募说明书
- 分层 MBS 证券化流程（tranched m b s securitization process） ⊑ MBS 证券化流程
- 分层发行备忘录（tranched offering memorandum） ⊑ 发行文件

## 3. 对象属性（Object Property）

| 属性（Property） | 中文（English） | 定义（Definition） | 说明 |
|---|---|---|---|
| fibo-bp-iss-pmbs:addsTo | 添加到（adds to） | 将某物添加到另一事物。 | 定义域（domain）：购入抵押贷款入池（purchase mortgage into pool）；值域（range）：组建中抵押贷款池（in assembly mortgage pool） |
| fibo-bp-iss-pmbs:allocatesIdentifier | 分配标识符（allocates identifier） | 为某事物分配标识符。 | 定义域（domain）：编号机构（numbering agency）；值域（range）：分配主标识符（allocate primary identifier） |
| fibo-bp-iss-pmbs:allocatesRatings | 分配评级（allocates ratings） | 为证券分配评级。 | 定义域（domain）：评级机构（ratings agency）；值域（range）：分配评级（allocate ratings） |
| fibo-bp-iss-pmbs:commitmentBasedOn | 基于……的承诺（commitment based on） | 标识承诺所依据的事物。 | 定义域（domain）：获得投资者承诺（get commitment from investors）；值域（range）：分层招募说明书草案（tranched draft prospectus） |
| fibo-bp-iss-pmbs:commitsTo | 承诺（commits to） | 对某事物作出承诺。 | 定义域（domain）：经纪自营商（broker dealer）；值域（range）：获得投资者承诺（get commitment from investors） |
| fibo-bp-iss-pmbs:decomposesInto | 分解为（decomposes into） | 将整体分解为若干部分。 | 定义域（domain）：分层 MBS 交易结算（tranched m b s deal settlement）；值域（range）：分层 MBS 一级交易结算流程（tranched m b s primary deal transaction settlement process） |
| fibo-bp-iss-pmbs:denominationIncrement | 面额增量（denomination increment） | 票据面额的增量。 | 定义域（domain）：分层票据参数（tranche notes parameters）；值域（range）：货币数量 |
| fibo-bp-iss-pmbs:finalizes.1 | 定稿（finalizes） | 最终确定某事物。 | 定义域（domain）：定稿池内容（finalize pool content）；值域（range）：发行中非机构抵押贷款池（in issuance non agency mortgage pool） |
| fibo-bp-iss-pmbs:flow | 流转（flow） | 流程中的流转关系。 | 定义域（domain）：非机构池创建结束（non agency pool creation end）；值域（range）：MBS 证券化开始（m b s securitization start） |
| fibo-bp-iss-pmbs:hasContent | 具有内容（has content） | 标识某事物所包含的内容。 | 定义域（domain）：分层 MBS 招募说明书大纲（tranched m b s prospectus outline）；值域（range）：起草分层结构（draft tranche structure）；子属性（subPropertyOf）：具有部分 |
| fibo-bp-iss-pmbs:hasContent.1 | 具有内容（has content） | 标识某事物所包含的内容。 | 定义域（domain）：分层 MBS 招募说明书大纲（tranched m b s prospectus outline）；值域（range）：起草分层条款清单（draft tranche termsheet）；子属性（subPropertyOf）：具有部分 |
| fibo-bp-iss-pmbs:hasCounterparty | 具有交易对手（has counterparty） | 标识合同的当事方，通常不是合同主当事方。 | 定义域（domain）：分层 MBS 交易（tranched m b s deal transaction）；值域（range）：主要投资者（primary investor） |
| fibo-bp-iss-pmbs:hasPrimaryHolder | 具有主要持有人（has primary holder） | 标识某事物的主要持有人。 | 定义域（domain）：分档型抵押支持证券工具；值域（range）：主要投资者（primary investor） |
| fibo-bp-iss-pmbs:hasPrincipalParty | 具有主当事方（has principal party） | 标识合同的主要或主当事方。 | 定义域（domain）：分层 MBS 交易（tranched m b s deal transaction）；值域（range）：非机构抵押支持证券发行人 |
| fibo-bp-iss-pmbs:hasResource | 具有资源（has resource） | 标识某过程或活动所使用的资源。 | 定义域（domain）：获得投资者承诺（get commitment from investors）；值域（range）：起草分层票据参数（draft tranche notes parameters） |
| fibo-bp-iss-pmbs:hasResource.1 | 具有资源（has resource） | 标识某过程或活动所使用的资源。 | 定义域（domain）：向主要投资者营销发行（market issue to primary investors）；值域（range）：分层发行备忘录（tranched offering memorandum） |
| fibo-bp-iss-pmbs:hasResource.2 | 具有资源（has resource） | 标识某过程或活动所使用的资源。 | 定义域（domain）：获得投资者承诺（get commitment from investors）；值域（range）：起草分层票据参数（draft tranche notes parameters） |
| fibo-bp-iss-pmbs:hasTrustee | 具有受托人（has trustee） | 将信托关联到具名受托人。 | 定义域（domain）：非机构抵押贷款池；值域（range）：池受托人（pool trustee） |
| fibo-bp-iss-pmbs:identifierIssuedBy | 标识符由……签发（identifier issued by） | 标识签发该标识符的机构。 | 定义域（domain）：分档型抵押支持证券工具；值域（range）：主标识符签发方 |
| fibo-bp-iss-pmbs:includesDetailsAbout | 包含……的细节（includes details about） | 标识某文件所包含细节所关涉的对象。 | 定义域（domain）：分层发行备忘录（tranched offering memorandum）；值域（range）：分层结构与条款清单（tranche structure and termsheet） |
| fibo-bp-iss-pmbs:includesDetailsAbout.1 | 包含……的细节（includes details about） | 标识某文件所包含细节所关涉的对象。 | 定义域（domain）：分层发行备忘录（tranched offering memorandum）；值域（range）：各分层定义（individual tranche definitions） |
| fibo-bp-iss-pmbs:isAssessmentOf | 是……的评估（is assessment of） | 标识评估所针对的对象。 | 定义域（domain）：评估池的发行适用性（assess pool suitability for issuance）；值域（range）：组建中抵押贷款池（in assembly mortgage pool） |
| fibo-bp-iss-pmbs:isIssueOf | 是……的发行（is issue of） | 标识发行所对应的证券或池。 | 定义域（domain）：使证券进入市场（make securities available in market）；值域（range）：分档型抵押支持证券交易 |
| fibo-bp-iss-pmbs:isPurchaseOf | 是……的购买（is purchase of） | 标识购买行为所针对的资产。 | 定义域（domain）：购入抵押贷款入池（purchase mortgage into pool）；值域（range）：房地产担保贷款 |
| fibo-bp-iss-pmbs:isDefiningOf | 是……的定义（isDefiningOf） | 标识该定义所针对的对象。 | 定义域（domain）：定义池特征（define pool characteristics）；值域（range）：未发行非机构抵押贷款池（not yet issued non agency mortgage pool） |
| fibo-bp-iss-pmbs:maximumAmount | 最大金额（maximum amount） | 允许的最大金额。 | 定义域（domain）：分层票据参数（tranche notes parameters）；值域（range）：货币数量 |
| fibo-bp-iss-pmbs:mayBecome | 可能成为（may become） | 标识某事物在流程中可能转变成的角色或状态。 | 定义域（domain）：池受托人（pool trustee）；值域（range）：证券承销商 |
| fibo-bp-iss-pmbs:mayIncludeDetailsAbout | 可能包含……的细节（may include details about） | 标识某文件可能包含细节所关涉的对象。 | 定义域（domain）：分层发行备忘录（tranched offering memorandum）；值域（range）：起草分层票据参数（draft tranche notes parameters） |
| fibo-bp-iss-pmbs:minimumDenomination | 最小面额（minimum denomination） | 允许的最小面额。 | 定义域（domain）：分层票据参数（tranche notes parameters）；值域（range）：货币数量 |
| fibo-bp-iss-pmbs:refersTo | 引用（refers to） | 将……作为信息或解释来源加以引用。 | 定义域（domain）：识别合格抵押贷款（identify conforming mortgage）；值域（range）：房地产担保贷款 |
| fibo-bp-iss-pmbs:requires | 要求（requires） | 标识某活动或状态所要求的前提。 | 定义域（domain）：拟定各分层条款清单（draw up tranche termsheets）；值域（range）：非机构抵押贷款池 |
| fibo-bp-iss-pmbs:requires.1 | 要求（requires） | 标识某活动或状态所要求的前提。 | 定义域（domain）：使证券进入市场（make securities available in market）；值域（range）：分档型抵押支持证券交易招募说明书 |
| fibo-bp-iss-pmbs:resultsIn | 导致（results in） | 产生某个结果。 | 定义域（domain）：完成交易（close deal）；值域（range）：分层 MBS 交易（tranched m b s deal transaction） |
| fibo-bp-iss-pmbs:resultsIn.1 | 导致（results in） | 产生某个结果。 | 定义域（domain）：定义票据参数（define notes parameters）；值域（range）：起草分层票据参数（draft tranche notes parameters） |
| fibo-bp-iss-pmbs:resultsIn.2 | 导致（results in） | 产生某个结果。 | 定义域（domain）：定稿招募说明书（finalize prospectus）；值域（range）：分档型抵押支持证券交易招募说明书 |
| fibo-bp-iss-pmbs:resultsInPublicationOf | 导致发布（results in publication of） | 其结果是某文件的发布。 | 定义域（domain）：完成交易（close deal）；值域（range）：汇款报告（remittance report） |

## 5. 公理约定（Axioms）

- 评估池的发行适用性（assess pool suitability for issuance）：是……的评估（is assessment of） some 组建中抵押贷款池（in assembly mortgage pool）
- 经纪自营商（broker dealer）：承诺（commits to） some 获得投资者承诺（get commitment from investors）
- 完成交易（close deal）：导致（results in） some 分层 MBS 交易（tranched m b s deal transaction）
- 完成交易（close deal）：导致发布（results in publication of） some 汇款报告（remittance report）
- 定义票据参数（define notes parameters）：导致（results in） some 起草分层票据参数（draft tranche notes parameters）
- 定义池特征（define pool characteristics）：是……的定义（isDefiningOf） some 未发行非机构抵押贷款池（not yet issued non agency mortgage pool）
- 拟定各分层条款清单（draw up tranche termsheets）：要求（requires） some 非机构抵押贷款池
- 定稿池内容（finalize pool content）：定稿（finalizes） some 发行中非机构抵押贷款池（in issuance non agency mortgage pool）
- 定稿招募说明书（finalize prospectus）：导致（results in） some 分档型抵押支持证券交易招募说明书
- 获得投资者承诺（get commitment from investors）：基于……的承诺（commitment based on） some 分层招募说明书草案（tranched draft prospectus）
- 获得投资者承诺（get commitment from investors）：具有资源（has resource） some 起草分层票据参数（draft tranche notes parameters）
- 获得投资者承诺（get commitment from investors）：具有资源（has resource） some 起草分层票据参数（draft tranche notes parameters）
- 识别合格抵押贷款（identify conforming mortgage）：引用（refers to） some 房地产担保贷款
- 确定承销商（identify underwriter）：导致 some 潜在分层发行承销商（potential tranched issue underwriter）
- 组建中抵押贷款池（in assembly mortgage pool）：具有阶段 some 组建中
- 发行中非机构抵押贷款池（in issuance non agency mortgage pool）：具有阶段 some 发行中
- 各分层定义（individual tranche definitions）：具有合同要素 some 债券摊销支付条款
- 各分层定义（individual tranche definitions）：具有合同要素 some 票息支付条款
- 使证券进入市场（make securities available in market）：是……的发行（is issue of） some 分档型抵押支持证券交易
- 使证券进入市场（make securities available in market）：要求（requires） some 分档型抵押支持证券交易招募说明书
- 向主要投资者营销发行（market issue to primary investors）：具有资源（has resource） some 分层发行备忘录（tranched offering memorandum）
- 非机构池创建结束（non agency pool creation end）：流转（flow） some MBS 证券化开始（m b s securitization start）
- 未发行非机构抵押贷款池（not yet issued non agency mortgage pool）：具有阶段 some 尚未发行
- 编号机构（numbering agency）：分配标识符 some 分配主标识符
- 编号机构（numbering agency）：分配标识符（allocates identifier） some 分配主标识符（allocate primary identifier）
- 池受托人（pool trustee）：可能成为（may become） some 证券承销商
- 潜在非机构 MBS 发行人（potential non agency m b s issuer）：评估 some 评估池的发行适用性（assess pool suitability for issuance）
- 潜在非机构 MBS 发行人（potential non agency m b s issuer）：评估 some 评估评级（assess ratings）
- 购入抵押贷款入池（purchase mortgage into pool）：添加到（adds to） some 组建中抵押贷款池（in assembly mortgage pool）
- 购入抵押贷款入池（purchase mortgage into pool）：是……的购买（is purchase of） some 房地产担保贷款
- 评级机构（ratings agency）：分配评级（allocates ratings） some 分配评级（allocate ratings）
- 分层票据参数（tranche notes parameters）：最大金额（maximum amount） 货币数量 ≤1
- 分层票据参数（tranche notes parameters）：关于 some 抵押支持证券分档票据
- 分层招募说明书草案（tranched draft prospectus）：先于 some 分档型抵押支持证券交易招募说明书
- 分层 MBS 交易结算（tranched m b s deal settlement）：分解为（decomposes into） some 分层 MBS 一级交易结算流程（tranched m b s primary deal transaction settlement process）
- 分层 MBS 交易（tranched m b s deal transaction）：具有交易对手（has counterparty） some 主要投资者（primary investor）
- 分层 MBS 交易（tranched m b s deal transaction）：遵循 some 分层 MBS 一级交易结算流程（tranched m b s primary deal transaction settlement process）
- 分层 MBS 招募说明书大纲（tranched m b s prospectus outline）：具有内容（has content） some 起草分层条款清单（draft tranche termsheet）
- 分层发行备忘录（tranched offering memorandum）：可能包含……的细节（may include details about） 起草分层票据参数（draft tranche notes parameters） ≤1
- 分层发行备忘录（tranched offering memorandum）：包含……的细节（includes details about） some 分层结构与条款清单（tranche structure and termsheet）
- 分层发行备忘录（tranched offering memorandum）：包含……的细节（includes details about） some 各分层定义（individual tranche definitions）

## 6. 依赖（owl:imports，26 个）

本本体通过 `owl:imports` 引入以下本体，各项的中文名称与简介如下：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `BP/SecuritiesIssuance/AgencyMBSIssuance.rdf` | 机构 MBS 发行本体（Agency MBS Issuance Ontology） | 定义机构抵押贷款支持证券（agency MBS，如房利美、房地美发行）的发行流程。 |
| `BP/SecuritiesIssuance/DebtIssuance.rdf` | 债务发行本体（Debt Issuance Ontology） | 定义债券等债务工具的发行流程与参与方。 |
| `BP/SecuritiesIssuance/IssuanceDocuments.rdf` | 发行文件本体（Issuance Documents Ontology） | 定义证券发行过程中使用的法律文件：募集说明书、条款清单等。 |
| `BP/SecuritiesIssuance/IssuanceProcess.rdf` | 发行流程本体（Issuance Process Ontology） | 定义证券发行的通用流程框架：从筹划、定价到配售的各阶段。 |
| `BP/SecuritiesIssuance/MBSIssuance.rdf` | MBS 发行本体（MBS Issuance Ontology） | 定义抵押贷款支持证券（MBS）发行的通用流程：资产池组建、分层与发售。 |
| `FND/Accounting/CurrencyAmount.rdf` | 货币金额本体（Currency Amount Ontology） | 定义「金额＋币种」的货币金额（currency amount）表示，是 FIBO 中表达价格、债务金额、付款额等一切带币种数值的基础构件。 |
| `FND/Agreements/Contracts.rdf` | 合同本体（Contracts Ontology） | 在协议之上定义具有法律约束力的合同（contract）：合同当事方、合同条款、义务与权利，是金融工具与交易合同建模的基石。 |
| `FND/Arrangements/Lifecycles.rdf` | 生命周期本体（Lifecycles Ontology） | 定义生命周期、生命周期阶段与状态转移，用于描述合同、金融工具、机构从创设到终止的演化过程。 |
| `FND/Arrangements/Reporting.rdf` | 报告本体（Reporting Ontology） | 定义报告、报告方与报告内容的关系，支撑监管报告、财务报告等报送场景。 |
| `FND/DatesAndTimes/FinancialDates.rdf` | 金融日期本体（Financial Dates Ontology） | 定义金融语境下的日期与期间概念：结算日、付息日、到期日、日计数基准等。 |
| `FND/Relations/Relations.rdf` | 关系本体（Relations Ontology） | FIBO 最底层的基础本体，定义参考（reference）、分类（classify）等通用关系与抽象概念，全库普遍依赖。 |
| `FND/TransactionsExt/REATransactions.rdf` | REA 交易本体（REA Transactions Ontology） | 基于资源—事件—代理（REA）会计模型定义交易的经济资源交换结构。 |
| `FND/TransactionsExt/SecuritiesTransactions.rdf` | 证券交易本体（Securities Transactions Ontology） | 定义证券买卖交易：订单、成交、结算指令等。 |
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `LOAN/LoansGeneral/Loans.rdf` | 贷款本体（Loans Ontology） | LOAN 域核心本体，定义贷款（loan）的通用结构：借款人、贷款人、本金、利率与还款安排。 |
| `LOAN/RealEstateLoans/Mortgages.rdf` | 抵押贷款本体（Mortgages Ontology） | 定义以不动产为抵押的贷款：抵押物、抵押登记与止赎。 |
| `SEC/Debt/Bonds.rdf` | 债券本体（Bonds Ontology） | 定义债券（bond）：期限、票面利率、付息方式与偿还结构。 |
| `SEC/Debt/CollateralizedDebtObligations.rdf` | 担保债务凭证本体（Collateralized Debt Obligations Ontology） | 定义担保债务凭证（CDO）：以债务资产池分层发行的证券。 |
| `SEC/Debt/MortgageBackedSecurities.rdf` | 抵押贷款支持证券本体（Mortgage-backed Securities Ontology） | 定义抵押贷款支持证券（MBS）：以抵押贷款池为支持的证券。 |
| `SEC/Debt/PoolBackedSecurities.rdf` | 池支持证券本体（Pool-backed Securities Ontology） | 定义以资产池为支持的证券的通用结构：资产池、分层（tranche）与过手安排。 |
| `SEC/Securities/SecuritiesIssuance.rdf` | 证券发行本体（Securities Issuance Ontology） | 定义证券发行（issuance）：发行人、发行条款与发行结果。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |
| `https://www.omg.org/spec/Commons/Collections/` | OMG 通用集合本体（OMG Commons Collections） | Commons 库中的集合本体，定义集合、成员等通用概念。 |
| `https://www.omg.org/spec/Commons/DatesAndTimes/` | OMG 通用日期与时间本体（OMG Commons Dates and Times） | Commons 库中的日期时间本体，定义日期、期间、时间点等通用时间概念。 |
| `https://www.omg.org/spec/Commons/Documents/` | OMG 通用文档本体（OMG Commons Documents） | Commons 库中的文档本体，定义文档及其组成部分的通用概念。 |
| `https://www.omg.org/spec/Commons/PartiesAndSituations/` | OMG 通用参与方与情境本体（OMG Commons Parties and Situations） | Commons 库中的参与方本体，定义独立主体、参与方及其角色扮演的通用概念，是 FIBO 参与方模型的上游。 |

## 7. 文件

- 官方 RDF/XML：`PrivateLabelMBSIssuance.rdf`
- 中文 Turtle：`PrivateLabelMBSIssuance.ttl`
- 结构图：`PrivateLabelMBSIssuance-structure.png` / `PrivateLabelMBSIssuance-structure.svg`