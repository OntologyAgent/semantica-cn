# 股权工具本体（Equity Instruments Ontology）结构与公理说明

本文档对应 `EquityInstruments.rdf` / `EquityInstruments.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `EquityInstruments-structure.png`（`EquityInstruments-structure.svg` 为可缩放版本）。

![股权工具本体（Equity Instruments Ontology）本体结构图](EquityInstruments-structure.png)

## 1. 本体概述

定义股权工具（equity instrument）：普通股、优先股及其附带的权利（表决权、分红权、剩余索取权）。

**在体系中的位置**：SEC 权益模块的核心，股票类证券的概念基础。

**上下游关系**：上游继承 FBC 金融工具并依赖 BE 公司所有权概念；下游被存托凭证、股指示例、股票 CFI 分类引用。

**与相近概念的差别**：股权≠债权——股权是所有权份额（无到期、无固定回报），债权是固定偿付承诺；普通股与优先股的差别在表决权与分红/清偿顺序的取舍。

## 2. 类（Class）

| 类（Class） | 定义（Definition） |
|---|---|
| 普通股（CommonShare） | 表示公司所有权单位、并代表对公司部分资产和收益的请求权的股份。 |
| 可变利益实体份额（VariableInterestEntityShare） | 证明持有对公司一定比例利润之合同权利所有权的份额。 |
| 可调整利率股息（adjustable rate dividend） | 随基准利率变动的股息。 |
| 拍卖利率股息（auction rate dividend） | 利率通过拍卖定期重置（通常每 7、14、28 或 35 天）的优先股股息。 |
| 可转换普通股（convertible common share） | 可转换为另一证券的普通股。 |
| 可转换优先股（convertible preferred share） | 包含持有人可在预定日期后将股份转换为固定数量普通股之选择权的优先股。 |
| 累积优先股（cumulative preferred share） | 股息如未按时支付则累积递延至日后支付的优先股。 |
| 托管人（custodian） | 为客户保管证券的金融机构。 |
| 股息（dividend） | 宣布按证券类别按比例向股东分配部分收益的承诺。 |
| 股息分配方式（dividend distribution method） | 向股东提供股息的惯例。 |
| 股息支付计划表（dividend schedule） | 指明股息到期应付日期的付款计划表。 |
| 增强表决权股（enhanced voting share） | 每股享有超过一票表决权的股份。 |
| 股权转换条款（equity conversion terms） | 规定股份转换为其他证券之细节的转换条款。 |
| 股票头寸（equity position） | 在权益工具中的头寸。 |
| 股权赎回条款（equity redemption provision） | 规定发行人或股东可赎回股份之条件的赎回条款。 |
| 赎回日可延长的股权赎回条款（equity redemption provision with extendable redemption date） | 允许将赎回日修改至原定日期之后的股权赎回条款。 |
| 可交换优先股（exchangeable preferred share） | 可交换为另一发行人证券的优先股。 |
| 可展期优先股（extendable preferred share） | 赎回日可由发行人或持有人选择延长的优先股。 |
| 固定利率股息（fixed rate dividend） | 按股份名义价值（及任何溢价）提供固定年度回报的股息。 |
| 缴足股（fully paid share） | 付款状态表明股东无需就股份价值再向公司缴付任何款项的股份。 |
| 硬回售优先股（hard retractable preferred share） | 回售价值必须以现金支付的可回售优先股。 |
| 有限合伙份额（limited partnership unit） | 有限合伙中的份额：除一名或多名普通合伙人（GP）外，还有一名或多名承担有限责任的有限合伙人（LP）。 |
| 上市股份（listed share） | 在至少一个平台挂牌的股份。 |
| 未缴股款股份（nil paid share） | 付款状态表明公司尚未收到股份任何市值款项的股份。 |
| 非累积优先股（non-cumulative preferred share） | 股息不予递延的优先股。 |
| 非参与优先股（non-participating preferred share） | 不属于参与优先股的优先股。 |
| 无表决权股（non-voting share） | 不享有表决权的股份。 |
| 普通股息（ordinary dividend） | 定期向股东支付的股息。 |
| 部分缴足股（partially paid share） | 付款状态表明公司仅收到股份部分市值款项的股份。 |
| 参与优先股（participating preferred share） | 除支付约定股息外，还赋予持有人与普通股股东分享额外收益之权利的优先股。 |
| 永续优先股（perpetual preferred share） | 无固定到期日的优先股。 |
| 优先受偿权（precedence right） | 使股东就特定预定股息支付优先于其他股东、并在公司清算时先行受偿的权利。 |
| 优先股息（preferred dividend） | 向股东分配部分收益的承诺，类似于股息，但通常金额和支付计划固定。 |
| 优先股（preferred share） | 按约定利率支付股息、并在股息支付和公司资产清算方面优先于普通股的股份。 |
| 可调整利率股息优先股（preferred share with adjustable rate dividend） | 股息率随某一基准利率变动的优先股。 |
| 拍卖利率股息优先股（preferred share with auction rate dividend） | 股息率通过拍卖（如荷兰式拍卖）定期重置的优先股。 |
| 固定到期日优先股（preferred share with fixed maturity date） | 到期日既定（通常按招募说明书条款确定）的优先股。 |
| 固定利率股息优先股（preferred share with fixed rate dividend） | 股息既定（通常按招募说明书条款确定）的优先股。 |
| 每股价格（price per share） | 某一证券在某一时点的单股价格。 |
| 私人持有股份（privately held share） | 代表对非公开交易实体之所有权的股份。 |
| 合资格股息（qualified dividend） | 适用低于普通（不合资格）股息所得税率的资本利得税率的股息。 |
| 可赎回优先股（redeemable preferred share） | 赋予发行人在规定条件下赎回股份之权利的优先股。 |
| 到期日可延长的可赎回优先股（redeemable preferred share with extendable maturity date） | 有固定到期日、且发行人可选择延长到期日的可赎回优先股。 |
| 赎回日可延长的可赎回优先股（redeemable preferred share with extendable redemption date） | 赎回日可以修改的可赎回优先股。 |
| 受限股份（restricted share） | 其所有权/转让/出售受特殊条件（包括特定国家限制）约束的股份。 |
| 受限表决权股（restricted voting share） | 每股享有不足一票表决权的股份。 |
| 可回售优先股（retractable preferred share） | 赋予所有人（股东）在规定条件下要求赎回股份之权利的优先股。 |
| 到期日可延长的可回售优先股（retractable preferred share with extendable maturity date） | 有固定到期日、且发行人和/或持有人可选择延长到期日的可回售优先股。 |
| 赎回日可延长的可回售优先股（retractable preferred share with extendable redemption date） | 赎回日可以修改的可回售优先股。 |
| 股份（share） | 表示公司股权所有权单位、共同基金所有权单位、或合伙中权益的金融工具。 |
| 股份发行人（share issuer） | 发行代表对某事物所有权权益之证券的发行人。 |
| 股份缴款状态（share payment status） | 规定已发行股份总体缴款状态的分类器。 |
| 股息率（share yield） | 每股年化股息除以每股（当前）价格的比率。 |
| 单一表决权股（single voting share） | 每股享有一票表决权的股份。 |
| 软回售优先股（soft retractable preferred share） | 回售价值可由发行人选择以现金或等值发行人普通股支付的可回售优先股。 |
| 特别股息（special dividend） | 一次性向股东支付的股息。 |
| 非受限股份（unrestricted share） | 其所有权/转让/出售不受特殊条件（包括特定国家限制）约束的股份。 |
| 表决权（voting right） | 规定股东表决权利（如选举董事、选举外部审计师、就公司事项表决）的合同权利。 |

### 2.1 继承关系（Inheritance）

- 普通股（CommonShare） ⊑ 股份（share）
- 可变利益实体份额（VariableInterestEntityShare） ⊑ 股份（share）
- 可调整利率股息（adjustable rate dividend） ⊑ 优先股息（preferred dividend）
- 拍卖利率股息（auction rate dividend） ⊑ 优先股息（preferred dividend）
- 可转换普通股（convertible common share） ⊑ 普通股（CommonShare）
- 可转换普通股（convertible common share） ⊑ 可转换证券
- 可转换优先股（convertible preferred share） ⊑ 优先股（preferred share）
- 可转换优先股（convertible preferred share） ⊑ 可转换证券
- 累积优先股（cumulative preferred share） ⊑ 优先股（preferred share）
- 托管人（custodian） ⊑ 金融机构
- 托管人（custodian） ⊑ 第三方代理人
- 股息（dividend） ⊑ 承诺
- 股息分配方式（dividend distribution method） ⊑ 惯例
- 股息分配方式（dividend distribution method） ⊑ 战略
- 股息支付计划表（dividend schedule） ⊑ 定期进度表
- 股息支付计划表（dividend schedule） ⊑ 支付进度表
- 增强表决权股（enhanced voting share） ⊑ 股份（share）
- 股权转换条款（equity conversion terms） ⊑ 转换条款
- 股票头寸（equity position） ⊑ 头寸
- 股权赎回条款（equity redemption provision） ⊑ 赎回条款
- 赎回日可延长的股权赎回条款（equity redemption provision with extendable redemption date） ⊑ 股权赎回条款（equity redemption provision）
- 可交换优先股（exchangeable preferred share） ⊑ 优先股（preferred share）
- 可展期优先股（extendable preferred share） ⊑ 优先股（preferred share）
- 固定利率股息（fixed rate dividend） ⊑ 优先股息（preferred dividend）
- 缴足股（fully paid share） ⊑ 股份（share）
- 硬回售优先股（hard retractable preferred share） ⊑ 可回售优先股（retractable preferred share）
- 有限合伙份额（limited partnership unit） ⊑ 股份（share）
- 上市股份（listed share） ⊑ 股份（share）
- 上市股份（listed share） ⊑ 上市证券
- 未缴股款股份（nil paid share） ⊑ 股份（share）
- 非累积优先股（non-cumulative preferred share） ⊑ 优先股（preferred share）
- 非参与优先股（non-participating preferred share） ⊑ 优先股（preferred share）
- 无表决权股（non-voting share） ⊑ 股份（share）
- 普通股息（ordinary dividend） ⊑ 股息（dividend）
- 部分缴足股（partially paid share） ⊑ 股份（share）
- 参与优先股（participating preferred share） ⊑ 优先股（preferred share）
- 永续优先股（perpetual preferred share） ⊑ 优先股（preferred share）
- 优先受偿权（precedence right） ⊑ 合同权利
- 优先股息（preferred dividend） ⊑ 股息（dividend）
- 优先股（preferred share） ⊑ 股份（share）
- 可调整利率股息优先股（preferred share with adjustable rate dividend） ⊑ 优先股（preferred share）
- 拍卖利率股息优先股（preferred share with auction rate dividend） ⊑ 优先股（preferred share）
- 固定到期日优先股（preferred share with fixed maturity date） ⊑ 优先股（preferred share）
- 固定利率股息优先股（preferred share with fixed rate dividend） ⊑ 优先股（preferred share）
- 每股价格（price per share） ⊑ 证券价格
- 每股价格（price per share） ⊑ 单价
- 私人持有股份（privately held share） ⊑ 股份（share）
- 合资格股息（qualified dividend） ⊑ 股息（dividend）
- 可赎回优先股（redeemable preferred share） ⊑ 优先股（preferred share）
- 到期日可延长的可赎回优先股（redeemable preferred share with extendable maturity date） ⊑ 固定到期日优先股（preferred share with fixed maturity date）
- 到期日可延长的可赎回优先股（redeemable preferred share with extendable maturity date） ⊑ 可赎回优先股（redeemable preferred share）
- 赎回日可延长的可赎回优先股（redeemable preferred share with extendable redemption date） ⊑ 可赎回优先股（redeemable preferred share）
- 受限股份（restricted share） ⊑ 股份（share）
- 受限表决权股（restricted voting share） ⊑ 股份（share）
- 可回售优先股（retractable preferred share） ⊑ 优先股（preferred share）
- 到期日可延长的可回售优先股（retractable preferred share with extendable maturity date） ⊑ 固定到期日优先股（preferred share with fixed maturity date）
- 到期日可延长的可回售优先股（retractable preferred share with extendable maturity date） ⊑ 可回售优先股（retractable preferred share）
- 赎回日可延长的可回售优先股（retractable preferred share with extendable redemption date） ⊑ 可回售优先股（retractable preferred share）
- 股份（share） ⊑ 权益工具
- 股份发行人（share issuer） ⊑ 发行人
- 股份缴款状态（share payment status） ⊑ 生命周期状态
- 股息率（share yield） ⊑ 收益率
- 单一表决权股（single voting share） ⊑ 股份（share）
- 软回售优先股（soft retractable preferred share） ⊑ 可回售优先股（retractable preferred share）
- 特别股息（special dividend） ⊑ 股息（dividend）
- 非受限股份（unrestricted share） ⊑ 可转让证券
- 非受限股份（unrestricted share） ⊑ 股份（share）
- 表决权（voting right） ⊑ 合同权利

## 3. 对象属性（Object Property）

| 属性（Property） | 中文（English） | 定义（Definition） | 说明 |
|---|---|---|---|
| fibo-sec-eq-eq:confersOwnershipOf | 授予……的所有权（confers ownership of） | 表明某凭证或分档授予对某一资产或现金流的权利。 | 定义域（domain）：合同；子属性（subPropertyOf）：授予 |
| fibo-sec-eq-eq:hasAdjustableDividendRate | 具有可调整股息率（has adjustable dividend rate） | 指明可变股息率，通常在招募说明书中规定为基于基准的公式或经拍卖确定。 | 定义域（domain）：优先股息（preferred dividend）；值域（range）：百分比货币数量；子属性（subPropertyOf）：具有量值 |
| fibo-sec-eq-eq:hasDividendDeclarationDate | 具有宣派日（has declaration date） | 指明机构宣布预期支付股息的日期，包括股息金额、除息日等信息。 | 定义域（domain）：股份（share）；值域（range）：显式日期；子属性（subPropertyOf）：具有显式日期 |
| fibo-sec-eq-eq:hasDistributionMethod | 具有分配方式（has distribution method） | 指明股息支付的分配方式。 | 定义域（domain）：股息（dividend）；值域（range）：股息分配方式（dividend distribution method）；子属性（subPropertyOf）：具有战略 |
| fibo-sec-eq-eq:hasDividend | 具有股息（has dividend） | 将股份与适用于该股份或该股份可能支付的股息关联起来。 | 定义域（domain）：股份（share）；值域（range）：股息（dividend）；子属性（subPropertyOf）：由……分类 |
| fibo-sec-eq-eq:hasDividendGracePeriod | 具有股息宽限期（has dividend grace period） | 指明股息到期应付后、发行人受罚之前的时间段。 | 定义域（domain）：优先股息（preferred dividend）；值域（range）：时长；子属性（subPropertyOf）：具有时长 |
| fibo-sec-eq-eq:hasEarliestRedemptionDate | 具有最早赎回日（has earliest redemption date） | 指明股份可赎回的最早日期或其后日期。 | 定义域（domain）：股权赎回条款（equity redemption provision）；值域（range）：显式日期；子属性（subPropertyOf）：具有显式日期 |
| fibo-sec-eq-eq:hasExDividendDate | 具有除息日（has ex-dividend date） | 指明股票「除息」的日期，通常在向登记股东支付股息前约三周。 | 定义域（domain）：股份（share）；值域（range）：显式日期；子属性（subPropertyOf）：具有显式日期 |
| fibo-sec-eq-eq:hasFixedDividendRate | 具有固定股息率（has fixed dividend rate） | 指明优先股的预定固定股息率，通常在招募说明书中规定。 | 定义域（domain）：优先股息（preferred dividend）；值域（range）：百分比货币数量；子属性（subPropertyOf）：具有量值 |
| fibo-sec-eq-eq:hasMinimumRedemptionPrice | 具有最低赎回价格（has minimum redemption price） | 指明股份可赎回的最低市场价格门槛。 | 定义域（domain）：股权赎回条款（equity redemption provision）；值域（range）：货币数量；子属性（subPropertyOf）：具有价格 |
| fibo-sec-eq-eq:hasRecordDate | 具有股权登记日（has record date） | 指明发行人核查某方是否在规定时点登记于公司股东名册的日期。 | 定义域（domain）：股份（share）；值域（range）：显式日期；子属性（subPropertyOf）：具有显式日期 |
| fibo-sec-eq-eq:hasRedemptionPremium | 具有赎回溢价（has redemption premium） | 指明为赎回股份须支付的超过市场价格的每股溢价（如有）。 | 定义域（domain）：股权赎回条款（equity redemption provision）；值域（range）：货币价格；子属性（subPropertyOf）：具有价格 |
| fibo-sec-eq-eq:hasSharePaymentStatus | 具有股份缴款状态（has share payment status） | 指明已发行股份的缴款状态。 | 定义域（domain）：股份（share）；值域（range）：股份缴款状态（share payment status）；子属性（subPropertyOf）：由……分类 |
| fibo-sec-eq-eq:isSeniorTo | 优先于（is senior to） | 表明给定股份（股类）优先级别高于相关股份，即持有人对公司资产和收益享有更高请求权。 | 定义域（domain）：股份（share）；值域（range）：股份（share） |
| fibo-sec-eq-eq:specifiesConversionDate | 规定转换日（specifies conversion date） | 指明可以发生转换的日期或其后日期。 | 定义域（domain）：股权转换条款（equity conversion terms）；值域（range）：日期 |

## 4. 数据属性（Datatype Property）

| 属性（Property） | 中文（English） | 定义（Definition） |
|---|---|---|
| fibo-sec-eq-eq:hasAvailableShares | 具有可交易股份数（has available shares） | 指明流通股数量减去受限股份后的数量，即可供交易的股份数。 |
| fibo-sec-eq-eq:hasExtendableMaturityDate | 是否具有可延长到期日（has extendable maturity date） | 表明有固定到期日的可赎回股份的发行人和/或持有人是否可选择延长到期日。 |
| fibo-sec-eq-eq:hasExtendableRedemptionDate | 是否具有可延长赎回日（has extendable redemption date） | 表明有指定赎回日的可赎回股份的发行人和/或持有人是否可选择延长该日期。 |
| fibo-sec-eq-eq:hasFloatingStock | 具有流通股数量（has floating stock） | 指明可供交易的股份数量，即流通股减去内部人持有股份后的数量。 |
| fibo-sec-eq-eq:hasShareClass | 具有股类（has share class） | 指明股份所属的类别，通常按表决权等特权区分。 |
| fibo-sec-eq-eq:hasSharesIssued | 具有已发行股份数（has shares issued） | 指明股东实际持有的股份（即流通股）加库存股的总数。 |
| fibo-sec-eq-eq:hasSharesOutstanding | 具有流通股数（has shares outstanding） | 指明当前由股东持有的股份数量，包括散户投资者、机构投资者和内部人持有的股份。 |
| fibo-sec-eq-eq:hasTreasuryShares | 具有库存股数（has treasury shares） | 指明已发行但未流通的股份数量，包括曾在市场上流通但已被公司回购的股份。 |
| fibo-sec-eq-eq:hasVotingRestriction | 具有表决权限制（has voting restriction） | 规定对表决权的限制（如有）。 |
| fibo-sec-eq-eq:isRedeemableAtIssuerOption | 发行人是否可赎回（is redeemable at issuer option） | 表明发行人是否有权发起回购，类似于赎回特征。 |
| fibo-sec-eq-eq:isRedeemableAtShareholderOption | 股东是否可回售（is redeemable at shareholder option） | 表明股东是否有权发起回售，类似于回售特征。 |
| fibo-sec-eq-eq:confersNumberOfVotesPerShare | 每股表决票数（number of votes per share） | 按每股基准授予股东表决权的票数。 |

## 5. 公理约定（Axioms）

- 普通股（CommonShare）：具有股息（has dividend） 普通股息（ordinary dividend） ≥0
- 普通股（CommonShare） 与 优先股（preferred share） 互斥（disjointWith）
- 可变利益实体份额（VariableInterestEntityShare）：由……发行 some（由…扮演（is played by） some 可变利益实体）
- 可调整利率股息（adjustable rate dividend）：具有量类 利率基准 ≥0
- 可调整利率股息（adjustable rate dividend）：restriction
- 可调整利率股息（adjustable rate dividend）：具有可调整股息率（has adjustable dividend rate） some 百分比货币数量
- 拍卖利率股息（auction rate dividend）：具有可调整股息率（has adjustable dividend rate） some 百分比货币数量
- 托管人（custodian）：持有 some 股份（share）
- 股息（dividend）：具有分配方式（has distribution method） 股息分配方式（dividend distribution method） ≤1
- 股息（dividend）：具有支付金额 货币数量 ≥0
- 股息（dividend）：具有进度表 股息支付计划表（dividend schedule） ≥0
- 增强表决权股（enhanced voting share）：每股表决票数（number of votes per share） some（restriction）
- 股权转换条款（equity conversion terms）：规定转换日（specifies conversion date） some 日期
- 股权转换条款（equity conversion terms）：规定转换为 some 证券
- 股票头寸（equity position）：具有所有方 股东 ≥0
- 股票头寸（equity position）：由……持有 N06a64b2c35c34ee0917df735dbeb020c =1
- 股票头寸（equity position）：具有自有资产 some 持股
- 股权赎回条款（equity redemption provision）：具有最低赎回价格（has minimum redemption price） 货币价格 ≥0
- 股权赎回条款（equity redemption provision）：具有赎回溢价（has redemption premium） 货币价格 ≥0
- 股权赎回条款（equity redemption provision）：具有最早赎回日（has earliest redemption date） 显式日期 ≥0
- 股权赎回条款（equity redemption provision）：restriction
- 股权赎回条款（equity redemption provision）：restriction
- 股权赎回条款（equity redemption provision）：restriction
- 赎回日可延长的股权赎回条款（equity redemption provision with extendable redemption date）：restriction
- 固定利率股息（fixed rate dividend）：具有固定股息率（has fixed dividend rate） some 百分比货币数量
- 缴足股（fully paid share）：restriction
- 硬回售优先股（hard retractable preferred share） 与 软回售优先股（soft retractable preferred share） 互斥（disjointWith）
- 有限合伙份额（limited partnership unit）：具有交易对手 some（由…扮演（is played by） some 有限合伙）
- 未缴股款股份（nil paid share）：restriction
- 非累积优先股（non-cumulative preferred share） 与 累积优先股（cumulative preferred share） 互斥（disjointWith）
- 非参与优先股（non-participating preferred share） 与 参与优先股（participating preferred share） 互斥（disjointWith）
- 无表决权股（non-voting share）：restriction
- 普通股息（ordinary dividend）：具有支付金额 货币数量 =1
- 部分缴足股（partially paid share）：restriction
- 参与优先股（participating preferred share）：具有股息（has dividend） 普通股息（ordinary dividend） ≥0
- 永续优先股（perpetual preferred share）：具有到期日 显式日期 ≤0
- 永续优先股（perpetual preferred share） 与 固定到期日优先股（preferred share with fixed maturity date） 互斥（disjointWith）
- 优先股息（preferred dividend）：具有固定股息率（has fixed dividend rate） 百分比货币数量 ≤1
- 优先股息（preferred dividend）：具有股息宽限期（has dividend grace period） 时长 ≤1
- 优先股（preferred share）：具有到期日 显式日期 ≥0
- 优先股（preferred share）：具有股息（has dividend） some（restriction）
- 优先股（preferred share）：优先于（is senior to） some 普通股（CommonShare）
- 可调整利率股息优先股（preferred share with adjustable rate dividend）：具有股息（has dividend） 可调整利率股息（adjustable rate dividend） ≥0
- 可调整利率股息优先股（preferred share with adjustable rate dividend） 与 固定利率股息优先股（preferred share with fixed rate dividend） 互斥（disjointWith）
- 拍卖利率股息优先股（preferred share with auction rate dividend）：具有股息（has dividend） 拍卖利率股息（auction rate dividend） ≥0
- 拍卖利率股息优先股（preferred share with auction rate dividend） 与 固定利率股息优先股（preferred share with fixed rate dividend） 互斥（disjointWith）
- 固定到期日优先股（preferred share with fixed maturity date）：具有到期日 显式日期 =1
- 固定利率股息优先股（preferred share with fixed rate dividend）：具有股息（has dividend） 固定利率股息（fixed rate dividend） ≥0
- 每股价格（price per share）：是……的价格 some 股份（share）
- 私人持有股份（privately held share） 与 上市股份（listed share） 互斥（disjointWith）
- 可赎回优先股（redeemable preferred share）：具有赎回条款 some 股权赎回条款（equity redemption provision）
- 到期日可延长的可赎回优先股（redeemable preferred share with extendable maturity date）：restriction
- 赎回日可延长的可赎回优先股（redeemable preferred share with extendable redemption date）：具有展期条款 some 赎回日可延长的股权赎回条款（equity redemption provision with extendable redemption date）
- 受限股份（restricted share） 与 非受限股份（unrestricted share） 互斥（disjointWith）
- 受限表决权股（restricted voting share）：每股表决票数（number of votes per share） some（restriction）
- 可回售优先股（retractable preferred share）：具有赎回条款 some 股权赎回条款（equity redemption provision）
- 到期日可延长的可回售优先股（retractable preferred share with extendable maturity date）：restriction
- 到期日可延长的可回售优先股（retractable preferred share with extendable maturity date）：restriction
- 到期日可延长的可回售优先股（retractable preferred share with extendable maturity date）：具有展期条款 some 展期条款
- 赎回日可延长的可回售优先股（retractable preferred share with extendable redemption date）：具有展期条款 some 赎回日可延长的股权赎回条款（equity redemption provision with extendable redemption date）
- 股份（share）：restriction
- 股份（share）：restriction
- 股份（share）：restriction
- 股份（share）：restriction
- 股份（share）：restriction
- 股份（share）：restriction
- 股份（share）：restriction
- 股份（share）：具有授权股份数 some xsd:nonNegativeInteger
- 股份（share）：每股表决票数（number of votes per share） some xsd:decimal
- 股份（share）：授予……的所有权（confers ownership of） some 股东权益
- 股份（share）：具有股份缴款状态（has share payment status） some 股份缴款状态（share payment status）
- 股份发行人（share issuer）：发行 some 股份（share）
- 股份缴款状态（share payment status）：分类 some 股份（share）
- 股息率（share yield）：具有自变量 some（restriction）
- 单一表决权股（single voting share）：restriction
- 表决权（voting right）：由……授予 some 书面合同

## 6. 依赖（owl:imports，29 个）

本本体通过 `owl:imports` 引入以下本体，各项的中文名称与简介如下：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `BE/LegalEntities/CorporateBodies.rdf` | 法人团体本体（Corporate Bodies Ontology） | 定义依法设立、具有独立法律人格的法人团体（corporate body），是股份有限公司等具体法人类型的上位概念。 |
| `BE/LegalEntities/LegalPersons.rdf` | 法律主体本体（Legal Persons Ontology） | 定义法律主体（legal person）与法定实体（legal entity）的核心概念：能持有权利义务、可起诉与被诉的主体。 |
| `BE/OwnershipAndControl/CorporateOwnership.rdf` | 公司所有权本体（Corporate Ownership Ontology） | 定义公司层面的所有权关系：股东、股份持有与受益所有权。 |
| `BE/Partnerships/Partnerships.rdf` | 合伙本体（Partnerships Ontology） | 定义合伙企业及普通合伙、有限合伙等形态，刻画合伙人之间的权利义务。 |
| `FBC/DebtAndEquities/Debt.rdf` | 债务本体（Debt Ontology） | 定义债务（debt）与债权债务关系的核心概念：借款人、贷款人、本金与利息义务。 |
| `FBC/FinancialInstruments/FinancialInstruments.rdf` | 金融工具本体（Financial Instruments Ontology） | FIBO 核心本体之一，定义金融工具（financial instrument）的通用概念：可交易、代表某种权利义务的合同工具，是证券、衍生品等具体工具的共同基础。 |
| `FBC/FinancialInstruments/InstrumentPricing.rdf` | 工具定价本体（Instrument Pricing Ontology） | 定义金融工具的价格、报价与估值概念。 |
| `FBC/FunctionalEntities/FinancialServicesEntities.rdf` | 金融服务实体本体（Financial Services Entities Ontology） | FBC 域核心本体，定义金融服务机构（银行、券商、保险公司、资管机构等）的功能分类体系。 |
| `FBC/ProductsAndServices/FinancialProductsAndServices.rdf` | 金融产品与服务本体（Financial Products and Services Ontology） | 定义金融产品（financial product）与金融服务（financial service）及其提供、购买关系。 |
| `FND/Accounting/CurrencyAmount.rdf` | 货币金额本体（Currency Amount Ontology） | 定义「金额＋币种」的货币金额（currency amount）表示，是 FIBO 中表达价格、债务金额、付款额等一切带币种数值的基础构件。 |
| `FND/Agreements/Agreements.rdf` | 协议本体（Agreements Ontology） | 定义两个或以上参与方之间协议（agreement）的通用概念：协议的当事方、条款、生效与终止，是合同等一切契约性安排的上位模型。 |
| `FND/Agreements/Contracts.rdf` | 合同本体（Contracts Ontology） | 在协议之上定义具有法律约束力的合同（contract）：合同当事方、合同条款、义务与权利，是金融工具与交易合同建模的基石。 |
| `FND/Arrangements/Lifecycles.rdf` | 生命周期本体（Lifecycles Ontology） | 定义生命周期、生命周期阶段与状态转移，用于描述合同、金融工具、机构从创设到终止的演化过程。 |
| `FND/DatesAndTimes/BusinessDates.rdf` | 营业日期本体（Business Dates Ontology） | 定义营业日、营业日历与日期调整规则（如顺延约定），支撑金融合同中的营业日计算。 |
| `FND/DatesAndTimes/FinancialDates.rdf` | 金融日期本体（Financial Dates Ontology） | 定义金融语境下的日期与期间概念：结算日、付息日、到期日、日计数基准等。 |
| `FND/Law/LegalCapacity.rdf` | 法律能力本体（Legal Capacity Ontology） | 定义法律能力、缔约能力、签章权等概念，刻画主体从事法律行为的资格。 |
| `FND/OwnershipAndControl/Ownership.rdf` | 所有权本体（Ownership Ontology） | 定义「拥有」关系：所有者、被拥有资产及所有权份额。 |
| `FND/ProductsAndServices/PaymentsAndSchedules.rdf` | 付款与计划表本体（Payments and Schedules Ontology） | 定义付款、付款计划表（payment schedule）及其日期与金额结构，是贷款还款、债券付息建模的基础。 |
| `FND/Relations/Relations.rdf` | 关系本体（Relations Ontology） | FIBO 最底层的基础本体，定义参考（reference）、分类（classify）等通用关系与抽象概念，全库普遍依赖。 |
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `IND/InterestRates/InterestRates.rdf` | 利率本体（Interest Rates Ontology） | 定义利率（interest rate）的结构：基准利率、利差、期限与重置机制。 |
| `SEC/Securities/SecuritiesIssuance.rdf` | 证券发行本体（Securities Issuance Ontology） | 定义证券发行（issuance）：发行人、发行条款与发行结果。 |
| `SEC/Securities/SecuritiesListings.rdf` | 证券上市本体（Securities Listings Ontology） | 定义证券在交易所上市（listing）及其上市状态。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |
| `https://www.omg.org/spec/Commons/Classifiers/` | OMG 通用分类器本体（OMG Commons Classifiers） | OMG 通用本体库（Commons）中的分类器本体，定义分类方案、类别与归类关系的通用概念，FIBO 的分类建模建立在其上。 |
| `https://www.omg.org/spec/Commons/DatesAndTimes/` | OMG 通用日期与时间本体（OMG Commons Dates and Times） | Commons 库中的日期时间本体，定义日期、期间、时间点等通用时间概念。 |
| `https://www.omg.org/spec/Commons/Documents/` | OMG 通用文档本体（OMG Commons Documents） | Commons 库中的文档本体，定义文档及其组成部分的通用概念。 |
| `https://www.omg.org/spec/Commons/QuantitiesAndUnits/` | OMG 通用量与单位本体（OMG Commons Quantities and Units） | Commons 库中的量与单位本体，定义数量、度量单位、量纲的通用概念，支撑金额、比率等数值表达。 |
| `https://www.omg.org/spec/Commons/RolesAndCompositions/` | OMG 通用角色与构成本体（OMG Commons Roles and Compositions） | Commons 库中的角色本体，定义角色及整体—部分构成关系的通用概念。 |

## 7. 文件

- 官方 RDF/XML：`EquityInstruments.rdf`
- 中文 Turtle：`EquityInstruments.ttl`
- 结构图：`EquityInstruments-structure.png` / `EquityInstruments-structure.svg`