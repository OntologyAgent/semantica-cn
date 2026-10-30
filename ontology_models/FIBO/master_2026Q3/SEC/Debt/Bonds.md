# 债券本体（Bonds Ontology）结构与公理说明

本文档对应 `Bonds.rdf` / `Bonds.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `Bonds-structure.png`（`Bonds-structure.svg` 为可缩放版本）。

![债券本体（Bonds Ontology）本体结构图](Bonds-structure.png)

## 1. 本体概述

定义债券（bond）：期限、票面利率（coupon）、付息方式、到期偿还与赎回条款。

**在体系中的位置**：SEC 债务模块的核心，最典型的一类债务工具。

**上下游关系**：上游继承债务工具本体并依赖参数化计划表（摊还结构）；下游被各类具体债券（市政债、可转换债）引用。

**与相近概念的差别**：债券≠票据（note）——主要是期限划分（票据通常较短），本质相同；债券≠贷款——债券是标准化可交易的，有票面利率与市场价格的联动关系。

## 2. 类（Class）

| 类（Class） | 定义（Definition） |
|---|---|
| 建设美国债券（Build America Bond） | 依 2009 年《美国复苏与再投资法》（ARRA）于 2010 年 12 月 31 日前发行的应税市政债券。 |
| 英国政府证券（U.K. Government security） | 由英国财政部发行并在伦敦证券交易所挂牌的债务工具。 |
| 美国国债（U.S. Treasury security） | 由美国财政部发行、附有完全信用担保的债务工具。 |
| 摊销债券（amortizing bond） | 在债券存续期内随利息支出定期偿还债务本金（面值）的债券。 |
| 债券（bond） | 代表一笔贷款的可交易债务工具，发行人对持有人负有债务。 |
| 债券摊销支付条款（bond amortization payment terms） | 包含债券存续期内本金偿还计划的条款，通常按固定间隔等额支付。 |
| 债券子弹式本金偿还条款（bond bullet principal repayment terms） | 以一次性付款覆盖全部本金金额的债券本金偿还条款。 |
| 债券转换条款（bond conversion terms） | 指明可转换债券何时可转换为另一证券（通常为同一发行人发行的公开交易股票）的条款。 |
| 债券票息（bond coupon） | 发行人承诺在到期前向持有人支付的债务证券利率，以面值的年度百分比表示。 |
| 债券保险（bond insurance） | 债券发行人购买的保险单，在发行人违约时保证向债券持有人偿还本金及全部相关利息。 |
| 债券本金偿还条款（bond principal repayment terms） | 关于债券本金偿还的条款。 |
| 债券登记机构（bond registrar） | 代表发行人负责维护记名债券所有人记录的一方。 |
| 债券浮动票息（bond variable coupon） | 利率可变的债券票息。 |
| 可部分赎回债券（bond with partial call） | 具有发行人可自行决定金额部分赎回之特征的债券。 |
| 公布偿债基金债券（bond with published sinking fund） | 按已知且公开的偿债基金计划表进行摊销的债券。 |
| 附权证债券（bond with warrant） | 发行时附带一份或多份权证的债券，权证赋予持有人购买指定证券的权利。 |
| 子弹型债券（bullet bond） | 全部本金在到期日一次性支付、而非在存续期内摊销的债券。 |
| 可赎回债券（callable bond） | 包含允许发行人在赎回保护期后按赎回价回购并注销债券之条款的债券。 |
| 可赎回可转换债券（callable convertible bond） | 同时具有可赎回特征的可转换债券。 |
| 义务证书（certificate of obligation） | 在自然灾害等需要立即行动而无时间表决的紧急情况下供地方议会使用的市政证券。 |
| 参与证书（certificate of participation） | 证明对特定质押收入流（通常为发行人的租赁付款）享有按比例份额的债务工具。 |
| 常规金边债券（conventional gilt） | 由英国财政部发行的固定票息债券，保证每六个月向持有人支付固定现金（票息）直至到期。 |
| 可转换债券（convertible bond） | 当股票价格高于指定水平时，赋予持有人将债券转换为固定数量股份（转换比率）之权利的债券。 |
| 公司债券（corporate bond） | 公司为筹集资金而发行的债券。 |
| 票息支付条款（coupon payment terms） | 关于债券利息支付的条款。 |
| 股票挂钩债券（equity linked bond） | 基于股票随时间的回报（即价格与股息支付或总回报，类似于总回报互换）的债券。 |
| 特别赎回条款（extraordinary redemption provision） | 赋予债券发行人在发行说明书规定的异常一次性事件发生时赎回债券之权利的条款。 |
| 首个常规付息日（first regular coupon date） | 在任何非标准（长或短）首个票息期之后，常规重复票息期系列中首次常规票息支付的计划日期。 |
| 固定票息债券（fixed coupon bond） | 票息率和本金金额在发行或出售时确定、并在证券存续期内保持不变的债券。 |
| 固定票息条款（fixed coupon terms） | 关于按固定利率支付债券利息的条款。 |
| 浮动利率票据（floating rate note） | 以公开参考利率为基础的浮动利率债券。 |
| 完全信用担保债券（full faith credit bond） | 由另一实体无条件付款承诺担保的债券。 |
| 一般责任市政债券（general obligation municipal bond） | 由发行市政当局的完全信用、一般资源和一般征税权力支持的市政债券。 |
| 政府债券（government bond） | 政府为资助政府开支而发行的债务证券。 |
| 政府发行债务证券（government issued debt security） | 由某一政府代表某一政体发行的债务证券，包括主权债务和市政债务。 |
| 绿色债券（green bond） | 专门为气候或环境项目融资而发行的债券。 |
| 隐含完全信用债券（implicit full faith credit bond） | 由政府支持机构或公司（而非政府直接）发行的债券。 |
| 指数挂钩债券（index-linked bond） | 收益可能随时间变动的债券，因其票息率或本金金额与特定指数（如消费者价格指数）挂钩。 |
| 通胀挂钩债券（inflation-linked bond） | 与通胀挂钩的债券，其本金或利息支付随通胀率升降。 |
| 最后常规付息日（last regular coupon date） | 常规重复票息期系列中最后一次常规票息支付的计划日期。 |
| 上市债券（listed bond） | 可在交易所交易的债券。 |
| 补偿赎回（make whole call） | 允许发行人提前清偿剩余债务的赎回安排。 |
| 强制可转换债券（mandatory convertible bond） | 无论股票价格如何、到期时强制转换为股份的可转换债券。 |
| 中期票据（medium term note） | 在储架发行计划下分期发行的债券，各期可有不同票息，期限通常为一至十年。 |
| 市政债券（municipal bond） | 可由地方（而非国家）当局发行的政府债券。 |
| 市政债务资金用途（municipal debt funds usage） | 说明新发行市政证券所筹资金用途的正式声明。 |
| 市政债务再营销代理人（municipal debt remarketing agent） | 负责向投资者转售证券（如浮动利率即期债务和其他投标选择权债券）的市政证券交易商。 |
| 市政债务资金来源（municipal debt source of funds） | 指明新发行市政证券资金来源的正式声明。 |
| 市政票据（municipal note） | 在某一日期偿还指定本金及按约定利率计付利息的短期债务，通常以特定收入来源偿付。 |
| 市政证券（municipal security） | 由地方政府实体发行的债务凭证。 |
| 市政受托机构（municipal trustee） | 由发行人指定、依债券合同以受托人身份为债券持有人利益行事的具有信托权限的金融机构。 |
| 原始发行折价债券（original issue discount bond） | 以面值大幅折价发行的附息债券。 |
| 部分赎回（partial call） | 对债券发行的一部分进行赎回。 |
| 部分赎回特征（partial call feature） | 发行人可在预定日期按某规则或抽签方式选择部分债券进行赎回的赎回特征。 |
| 部分赎回分配惯例（partial redemption allocation convention） | 用于确定部分赎回如何在债券持有人之间分摊的惯例。 |
| 永续债券（perpetual bond） | 没有到期日、永久支付利息的债券。 |
| 利率基准惯例（rate basis convention） | 在规定债券赎回百分比金额时所用百分比报价利率的基准。 |
| 赎回付款（redemption payment） | 在到期或赎回时支付债券本金的偿还事件。 |
| 赎回计划表（redemption schedule） | 按规定日期赎回债券发行一定百分比的偿还计划表。 |
| 监管赎回（regulatory call） | 由某项监管特定规则触发的赎回。 |
| 可再营销债券（remarketable bond） | 未偿债券票息率通过拍卖程序定期重置的公司债券计划。 |
| 收益债券（revenue bond） | 由特定项目收入支持的市政债券。 |
| 有担保债券（secured bond） | 除一般付款承诺外，还以抵押品（如有形资产或收入流）为支持的债券。 |
| 偿债基金摊销条款（sinking fund amortization terms） | 偿债基金型摊销证券本金偿付的条款。 |
| 主权债券（sovereign bond） | 由国家政府发行的债券。 |
| 主权债务工具（sovereign debt instrument） | 由国家政府发行的债务证券。 |
| 特别摊派债券（special assessment bond） | 用于为开发项目融资、以受益社区的摊派（税收）收入偿付的市政债券。 |
| 特别责任债券（special obligation bond） | 以有限收入来源（如指定项目所得收入）为担保的债券。 |
| 特别税债券（special tax bond） | 以从价税以外的指定税收收入为担保的债券。 |
| 票息递增债券（step up bond） | 票息在存续期内递增的债券。 |
| 阶梯票息条款（stepped coupon terms） | 票息在债券存续期内递增的证券的票息支付条款。 |
| 拆息债券（strip bond） | 由债券的每笔利息支付和本金分别拆分为独立零息债券而形成的系列债券之一。 |
| 税收增额债券（tax allocation bond） | 以财产价值和其他经济活动增加所实现税收增量偿付的债券，通常用于特定开发区。 |
| 短期国库券（treasury bill） | 期限为一至十二个月的短期零息国库债务。 |
| 长期国债（treasury bond） | 以 20 年或 30 年期发行、每六个月付息一次直至到期的长期附息国库债务。 |
| 通胀保值国债（treasury inflation-protected security） | 本金与通胀或通缩挂钩、并在证券存续期内相应变动的可变收益债券。 |
| 中期国债（treasury note） | 原始期限为二至十年的中期附息国库债务。 |
| 非上市债券（unlisted bond） | 在场外交易（而非通过交易所或其他挂牌场所）的债券。 |
| 无担保债券（unsecured bond） | 仅以债券发行人的良好信用为支持的债券。 |
| 浮动票息债券（variable coupon bond） | 利率浮动的债券。 |
| 浮动票息条款（variable coupon terms） | 规定浮动票息债券利率计算方法的合同条款。 |
| 可变债务本金（variable debt principal） | 随某一变量定义、因而随时间变动的本金。 |
| 可变收益债券（variable income bond） | 收益可能随时间变动的债券，因其票息率或本金金额在存续期内随某指数或计划表变动。 |
| 可变利息计算公式（variable interest calculation formula） | 用于计算可变利息的公式。 |
| 可变利息表达式（variable interest expression） | 用于确定可变利息支付金额的表达式。 |
| 可变本金债券（variable principal bond） | 本金随指数变动而调整的债券。 |
| 零息债券（zero coupon bond） | 票息率为零、以面值大幅折价交易的债券。 |
| 零息条款（zero coupon terms） | 关于零息债券利息支付的条款。 |

### 2.1 继承关系（Inheritance）

- 建设美国债券（Build America Bond） ⊑ 市政债券（municipal bond）
- 英国政府证券（U.K. Government security） ⊑ 主权债务工具（sovereign debt instrument）
- 美国国债（U.S. Treasury security） ⊑ 主权债务工具（sovereign debt instrument）
- 摊销债券（amortizing bond） ⊑ 债券（bond）
- 债券（bond） ⊑ 到期偿还型信贷协议
- 债券（bond） ⊑ 可交易债务工具
- 债券摊销支付条款（bond amortization payment terms） ⊑ 债券本金偿还条款（bond principal repayment terms）
- 债券子弹式本金偿还条款（bond bullet principal repayment terms） ⊑ 债券本金偿还条款（bond principal repayment terms）
- 债券转换条款（bond conversion terms） ⊑ 转换条款
- 债券票息（bond coupon） ⊑ 利率
- 债券保险（bond insurance） ⊑ 保险单
- 债券本金偿还条款（bond principal repayment terms） ⊑ 本金偿还条款
- 债券登记机构（bond registrar） ⊑ 法定代理人
- 债券登记机构（bond registrar） ⊑ 注册员
- 债券浮动票息（bond variable coupon） ⊑ 可变利率
- 债券浮动票息（bond variable coupon） ⊑ 债券票息（bond coupon）
- 可部分赎回债券（bond with partial call） ⊑ 可赎回债券（callable bond）
- 公布偿债基金债券（bond with published sinking fund） ⊑ 摊销债券（amortizing bond）
- 附权证债券（bond with warrant） ⊑ 债券（bond）
- 子弹型债券（bullet bond） ⊑ 债券（bond）
- 可赎回债券（callable bond） ⊑ 债券（bond）
- 可赎回可转换债券（callable convertible bond） ⊑ 可赎回债券（callable bond）
- 可赎回可转换债券（callable convertible bond） ⊑ 可转换债券（convertible bond）
- 义务证书（certificate of obligation） ⊑ 市政证券（municipal security）
- 参与证书（certificate of participation） ⊑ 债务工具
- 常规金边债券（conventional gilt） ⊑ 固定票息债券（fixed coupon bond）
- 常规金边债券（conventional gilt） ⊑ 英国政府证券（U.K. Government security）
- 可转换债券（convertible bond） ⊑ 债券（bond）
- 可转换债券（convertible bond） ⊑ 可转换证券
- 公司债券（corporate bond） ⊑ 债券（bond）
- 票息支付条款（coupon payment terms） ⊑ 利息支付条款
- 股票挂钩债券（equity linked bond） ⊑ 浮动票息债券（variable coupon bond）
- 特别赎回条款（extraordinary redemption provision） ⊑ 赎回特征
- 首个常规付息日（first regular coupon date） ⊑ 显式日期
- 固定票息债券（fixed coupon bond） ⊑ 债券（bond）
- 固定票息债券（fixed coupon bond） ⊑ 固定收益证券
- 固定票息条款（fixed coupon terms） ⊑ 票息支付条款（coupon payment terms）
- 浮动利率票据（floating rate note） ⊑ 浮动票息债券（variable coupon bond）
- 完全信用担保债券（full faith credit bond） ⊑ 无担保债券（unsecured bond）
- 一般责任市政债券（general obligation municipal bond） ⊑ 完全信用担保债券（full faith credit bond）
- 一般责任市政债券（general obligation municipal bond） ⊑ 市政债券（municipal bond）
- 政府债券（government bond） ⊑ 债券（bond）
- 政府债券（government bond） ⊑ 政府发行债务证券（government issued debt security）
- 政府发行债务证券（government issued debt security） ⊑ 债务工具
- 绿色债券（green bond） ⊑ 债券（bond）
- 隐含完全信用债券（implicit full faith credit bond） ⊑ 无担保债券（unsecured bond）
- 指数挂钩债券（index-linked bond） ⊑ 可变收益债券（variable income bond）
- 通胀挂钩债券（inflation-linked bond） ⊑ 指数挂钩债券（index-linked bond）
- 最后常规付息日（last regular coupon date） ⊑ 显式日期
- 上市债券（listed bond） ⊑ 债券（bond）
- 上市债券（listed bond） ⊑ 上市证券
- 补偿赎回（make whole call） ⊑ 赎回事件
- 强制可转换债券（mandatory convertible bond） ⊑ 可转换债券（convertible bond）
- 中期票据（medium term note） ⊑ 债券（bond）
- 市政债券（municipal bond） ⊑ 政府债券（government bond）
- 市政债券（municipal bond） ⊑ 市政证券（municipal security）
- 市政债务资金用途（municipal debt funds usage） ⊑ 法律文件
- 市政债务再营销代理人（municipal debt remarketing agent） ⊑ 交易商
- 市政债务再营销代理人（municipal debt remarketing agent） ⊑ 合同第三方
- 市政债务资金来源（municipal debt source of funds） ⊑ 法律文件
- 市政票据（municipal note） ⊑ 市政证券（municipal security）
- 市政证券（municipal security） ⊑ 政府发行债务证券（government issued debt security）
- 市政受托机构（municipal trustee） ⊑ 受托人
- 市政受托机构（municipal trustee） ⊑ 金融机构
- 原始发行折价债券（original issue discount bond） ⊑ 债券（bond）
- 部分赎回（partial call） ⊑ 赎回事件
- 部分赎回特征（partial call feature） ⊑ 赎回特征
- 部分赎回分配惯例（partial redemption allocation convention） ⊑ 惯例
- 永续债券（perpetual bond） ⊑ 债券（bond）
- 利率基准惯例（rate basis convention） ⊑ 惯例
- 赎回付款（redemption payment） ⊑ 支付事件
- 赎回付款（redemption payment） ⊑ 兑付事件
- 赎回计划表（redemption schedule） ⊑ 支付进度表
- 监管赎回（regulatory call） ⊑ 赎回事件
- 可再营销债券（remarketable bond） ⊑ 公司债券（corporate bond）
- 可再营销债券（remarketable bond） ⊑ 浮动利率票据（floating rate note）
- 收益债券（revenue bond） ⊑ 市政债券（municipal bond）
- 收益债券（revenue bond） ⊑ 有担保债券（secured bond）
- 有担保债券（secured bond） ⊑ 债券（bond）
- 偿债基金摊销条款（sinking fund amortization terms） ⊑ 债券摊销支付条款（bond amortization payment terms）
- 主权债券（sovereign bond） ⊑ 政府债券（government bond）
- 主权债券（sovereign bond） ⊑ 主权债务工具（sovereign debt instrument）
- 主权债务工具（sovereign debt instrument） ⊑ 政府发行债务证券（government issued debt security）
- 特别摊派债券（special assessment bond） ⊑ 市政债券（municipal bond）
- 特别摊派债券（special assessment bond） ⊑ 有担保债券（secured bond）
- 特别责任债券（special obligation bond） ⊑ 市政债券（municipal bond）
- 特别税债券（special tax bond） ⊑ 市政债券（municipal bond）
- 特别税债券（special tax bond） ⊑ 有担保债券（secured bond）
- 票息递增债券（step up bond） ⊑ 债券（bond）
- 票息递增债券（step up bond） ⊑ 固定收益证券
- 阶梯票息条款（stepped coupon terms） ⊑ 票息支付条款（coupon payment terms）
- 拆息债券（strip bond） ⊑ 零息债券（zero coupon bond）
- 拆息债券（strip bond） ⊑ 拆条
- 税收增额债券（tax allocation bond） ⊑ 市政债券（municipal bond）
- 税收增额债券（tax allocation bond） ⊑ 有担保债券（secured bond）
- 短期国库券（treasury bill） ⊑ 美国国债（U.S. Treasury security）
- 短期国库券（treasury bill） ⊑ 货币市场工具
- 长期国债（treasury bond） ⊑ 主权债券（sovereign bond）
- 长期国债（treasury bond） ⊑ 美国国债（U.S. Treasury security）
- 通胀保值国债（treasury inflation-protected security） ⊑ 通胀挂钩债券（inflation-linked bond）
- 通胀保值国债（treasury inflation-protected security） ⊑ 美国国债（U.S. Treasury security）
- 通胀保值国债（treasury inflation-protected security） ⊑ 可变本金债券（variable principal bond）
- 中期国债（treasury note） ⊑ 中期票据（medium term note）
- 中期国债（treasury note） ⊑ 美国国债（U.S. Treasury security）
- 非上市债券（unlisted bond） ⊑ 债券（bond）
- 无担保债券（unsecured bond） ⊑ 债券（bond）
- 浮动票息债券（variable coupon bond） ⊑ 可变收益债券（variable income bond）
- 浮动票息条款（variable coupon terms） ⊑ 票息支付条款（coupon payment terms）
- 可变债务本金（variable debt principal） ⊑ 公开发行债务
- 可变收益债券（variable income bond） ⊑ 债券（bond）
- 可变收益债券（variable income bond） ⊑ 可变收益证券
- 可变利息计算公式（variable interest calculation formula） ⊑ 完全指数化利率
- 可变利息表达式（variable interest expression） ⊑ 表达式
- 可变本金债券（variable principal bond） ⊑ 可变收益债券（variable income bond）
- 零息债券（zero coupon bond） ⊑ 债券（bond）
- 零息债券（zero coupon bond） ⊑ 固定收益证券
- 零息条款（zero coupon terms） ⊑ 债券摊销支付条款（bond amortization payment terms）
- 零息条款（zero coupon terms） ⊑ 固定票息条款（fixed coupon terms）

## 3. 对象属性（Object Property）

| 属性（Property） | 中文（English） | 定义（Definition） | 说明 |
|---|---|---|---|
| fibo-sec-dbt-bnd:hasAwardDate | 具有配售日（has award date） | 规定协议承销中债券配售给牵头行或银团的日期，或竞争性承销中的投标日期。 | 定义域（domain）：市政债券（municipal bond）；值域（range）：显式日期；子属性（subPropertyOf）：具有显式日期 |
| fibo-sec-dbt-bnd:hasCallPrice | 具有赎回价格（has call price） | 指明指定赎回日的赎回金额，通常为面值加赎回溢价，按合约规定。 | 定义域（domain）：赎回特征；值域（range）：货币价格；子属性（subPropertyOf）：具有价格 |
| fibo-sec-dbt-bnd:hasCallRateBasis | 具有赎回利率基准（has call rate basis） | 对计划表中的每一赎回事件，指明该利率以面值百分比还是累计平均百分比表示。 | 定义域（domain）：赎回事件；值域（range）：利率基准惯例（rate basis convention） |
| fibo-sec-dbt-bnd:hasConvertibleDate | 具有转换日（has convertible date） | 债券可转换为指定权益证券的日期。 | 定义域（domain）：债券转换条款（bond conversion terms）；值域（range）：显式日期；子属性（subPropertyOf）：具有显式日期 |
| fibo-sec-dbt-bnd:hasExtraordinaryRedemptionProvision | 具有特别赎回条款（has extraordinary redemption provision） | 将债务工具的赎回条款与发行人在特定情况下可行使的一次性条款关联起来。 | 定义域（domain）：赎回条款；值域（range）：特别赎回条款（extraordinary redemption provision）；子属性（subPropertyOf）：具有合同要素 |
| fibo-sec-dbt-bnd:hasFinalMaturityDate | 具有最终到期日（has final maturity date） | 指明金融工具的最后付款日，届时本金（及全部剩余利息）到期应付。 | 定义域（domain）：赎回条款；值域（range）：显式日期；子属性（subPropertyOf）：具有显式日期 |
| fibo-sec-dbt-bnd:hasFirstCallPrice | 具有首次赎回价格（has first call price） | 指明赎回计划表规定的首个赎回日的赎回金额。 | 定义域（domain）：赎回特征；值域（range）：货币价格；子属性（subPropertyOf）：具有赎回价格（has call price） |
| fibo-sec-dbt-bnd:hasFirstCouponPaymentDate | 具有首次付息日（has first coupon payment date） | 规定发行人或其代理人预期或承诺支付首次票息的日期。 | 定义域（domain）：票息支付条款（coupon payment terms）；值域（range）：显式日期；子属性（subPropertyOf）：具有显式日期 |
| fibo-sec-dbt-bnd:hasFirstParCallDate | 具有首次平价赎回日（has first par call date） | 指明债券首次可按面值赎回的日期。 | 定义域（domain）：赎回特征；值域（range）：显式日期；子属性（subPropertyOf）：具有显式日期 |
| fibo-sec-dbt-bnd:hasFirstParCallPrice | 具有首次平价赎回价格（has first par call price） | 规定赎回计划表中首个平价赎回日的赎回金额。 | 定义域（domain）：赎回特征；值域（range）：货币价格；子属性（subPropertyOf）：具有首次赎回价格（has first call price） |
| fibo-sec-dbt-bnd:hasFirstPremiumCallDate | 具有首次溢价赎回日（has first premium call date） | 指明债券首次可按高于面值的价格赎回的日期。 | 定义域（domain）：赎回特征；值域（range）：显式日期；子属性（subPropertyOf）：具有显式日期 |
| fibo-sec-dbt-bnd:hasFirstPremiumCallPrice | 具有首次溢价赎回价格（has first premium call price） | 规定赎回计划表中首次可按高于面值价格赎回之日的赎回金额。 | 定义域（domain）：赎回特征；值域（range）：货币价格；子属性（subPropertyOf）：具有首次赎回价格（has first call price） |
| fibo-sec-dbt-bnd:hasFirstPutDate | 具有首次回售日（has first put date） | 指明持有人可在到期前将债券售回给发行人的首个日期。 | 定义域（domain）：回售特征；值域（range）：显式日期；子属性（subPropertyOf）：具有回售日（has put date） |
| fibo-sec-dbt-bnd:hasFirstPutPrice | 具有首次回售价格（has first put price） | 规定持有人可在到期前将债券售回给发行人的初始价格。 | 定义域（domain）：回售特征；值域（range）：货币价格；子属性（subPropertyOf）：具有价格 |
| fibo-sec-dbt-bnd:hasFundingSource | 具有资金来源（has funding source） | 指明新发行市政证券的资金来源。 | 定义域（domain）：市政证券（municipal security）；值域（range）：市政债务资金来源（municipal debt source of funds）；子属性（subPropertyOf）：具有数据来源 |
| fibo-sec-dbt-bnd:hasLastCouponPaymentDate | 具有最后付息日（has last coupon payment date） | 规定发行人预期支付最后一次票息的日期。 | 定义域（domain）：票息支付条款（coupon payment terms）；值域（range）：显式日期；子属性（subPropertyOf）：具有结束日期 |
| fibo-sec-dbt-bnd:hasLockoutPeriod | 具有锁定期（has lockout period） | 指明可赎回证券不可赎回、持有人仅收到利息票息支付的时间段。 | 定义域（domain）：赎回特征；值域（range）：日期区间；子属性（subPropertyOf）：具有日期区间 |
| fibo-sec-dbt-bnd:hasMunicipalTrustee | 具有市政受托机构（has municipal trustee） | 指明由发行人指定、依债券合同以受托人身份为债券持有人利益行事的具有信托权限的金融机构。 | 定义域（domain）：市政债券（municipal bond）；值域（range）：市政受托机构（municipal trustee）；子属性（subPropertyOf）：具有第三方 |
| fibo-sec-dbt-bnd:hasOriginalIssueDiscountAmount | 具有原始发行折价金额（has original issue discount amount） | 指明到期既定赎回价格与发行价格之间的差额。 | 定义域（domain）：债券（bond）；值域（range）：货币数量；子属性（subPropertyOf）：具有货币数量 |
| fibo-sec-dbt-bnd:hasPartialRedemptionAllocationConvention | 具有部分赎回分配惯例（has partial redemption allocation convention） | 指明用于确定赎回如何在债券持有人集合中分摊的惯例。 | 定义域（domain）：部分赎回特征（partial call feature）；值域（range）：部分赎回分配惯例（partial redemption allocation convention） |
| fibo-sec-dbt-bnd:hasPenultimateCouponPaymentDate | 具有到期前最后付息日（has penultimate coupon payment date） | 规定到期前的最后一次票息支付日期。 | 定义域（domain）：票息支付条款（coupon payment terms）；值域（range）：显式日期；子属性（subPropertyOf）：具有显式日期 |
| fibo-sec-dbt-bnd:hasPremiumAmount | 具有溢价金额（has premium amount） | 指明债券被赎回时支付给债券持有人的溢价。 | 定义域（domain）：赎回特征；值域（range）：货币数量；子属性（subPropertyOf）：具有货币数量 |
| fibo-sec-dbt-bnd:hasPutDate | 具有回售日（has put date） | 指明证券可由债券持有人要求赎回的日期。 | 定义域（domain）：回售特征；值域（range）：显式日期；子属性（subPropertyOf）：具有显式日期 |
| fibo-sec-dbt-bnd:hasPutFrequency | 具有回售频率（has put frequency） | 指明回售特征可行使的重复时间窗口。 | 定义域（domain）：回售特征；值域（range）：重复区间；子属性（subPropertyOf）：具有重复区间 |
| fibo-sec-dbt-bnd:hasRedemptionAmount | 具有赎回金额（has redemption amount） | 指明赎回付款中支付的本金金额。 | 定义域（domain）：赎回付款（redemption payment）；值域（range）：货币数量；子属性（subPropertyOf）：具有货币数量 |
| fibo-sec-dbt-bnd:hasRemarketingAgent | 具有再营销代理（has remarketing agent） | 标识再营销代理。 | 定义域（domain）：市政证券（municipal security）；值域（range）：市政债务再营销代理人（municipal debt remarketing agent）；子属性（subPropertyOf）：具有第三方 |
| fibo-sec-dbt-bnd:hasResetDateOffset | 具有重置日偏移（has reset date offset） | 指明相对于票息支付日进行利率重置的偏移量。 | 定义域（domain）：浮动票息条款（variable coupon terms）；值域（range）：相对日期；子属性（subPropertyOf）：具有日期 |
| fibo-sec-dbt-bnd:isLinkedToFallback | 关联后备债券（is linked to fallback） | 将指数挂钩工具与计算代理人可选定的政府债券关联起来。 | 定义域（domain）：金融工具；值域（range）：政府债券（government bond）；子属性（subPropertyOf）：引用 |

## 4. 数据属性（Datatype Property）

| 属性（Property） | 中文（English） | 定义（Definition） |
|---|---|---|
| fibo-sec-dbt-bnd:hasCeiling | 具有上限（has ceiling） | 指明可变利息支付金额的最大值。 |
| fibo-sec-dbt-bnd:hasFloor | 具有下限（has floor） | 指明可变利息支付金额的最小值。 |
| fibo-sec-dbt-bnd:isBankQualified | 银行合格（is bank qualified） | 发行人在合理预期其在该发行日历年内的发行不超过规定额度时，给予公共目的债券发行的指定。 |
| fibo-sec-dbt-bnd:isLegalOpinionAvailable | 是否有法律意见书（is legal opinion available） | 表明某一市政债券是否存在法律意见书。 |
| fibo-sec-dbt-bnd:isMandatory | 是否强制（is mandatory） | 表明某事物是否为必需。 |
| fibo-sec-dbt-bnd:isProRated | 是否按比例计算（is pro-rated） | 表明票息是否按付款期间实际天数与付款期数之比按比例计算。 |
| fibo-sec-dbt-bnd:isSuperSinker | 超级偿债债券（super sinker） | 表明该债券具有长期票息但潜在到期日较短。 |

## 5. 公理约定（Axioms）

- 美国国债（U.S. Treasury security）：restriction
- 摊销债券（amortizing bond）：具有偿还条款 some 债券摊销支付条款（bond amortization payment terms）
- 摊销债券（amortizing bond） 与 子弹型债券（bullet bond） 互斥（disjointWith）
- 债券（bond）：restriction
- 债券（bond）：具有利息支付条款 some 票息支付条款（coupon payment terms）
- 债券（bond）：具有偿还条款 some 债券本金偿还条款（bond principal repayment terms）
- 债券摊销支付条款（bond amortization payment terms）：具有进度表 some 摊销计划表
- 债券摊销支付条款（bond amortization payment terms） 与 债券子弹式本金偿还条款（bond bullet principal repayment terms） 互斥（disjointWith）
- 债券转换条款（bond conversion terms）：规定转换为 some 上市股份
- 债券本金偿还条款（bond principal repayment terms）：具有进度表 some 支付进度表
- 债券本金偿还条款（bond principal repayment terms） 与 赎回特征 互斥（disjointWith）
- 债券登记机构（bond registrar）：登记 some 债券（bond）
- 可部分赎回债券（bond with partial call）：具有赎回特征 some 部分赎回特征（partial call feature）
- 子弹型债券（bullet bond）：具有偿还条款 some 债券子弹式本金偿还条款（bond bullet principal repayment terms）
- 子弹型债券（bullet bond） 与 摊销债券（amortizing bond） 互斥（disjointWith）
- 子弹型债券（bullet bond） 与 可赎回债券（callable bond） 互斥（disjointWith）
- 可赎回债券（callable bond）：restriction
- 可赎回债券（callable bond）：具有特别赎回条款（has extraordinary redemption provision） 特别赎回条款（extraordinary redemption provision） ≤1
- 可赎回债券（callable bond）：具有赎回特征 some 赎回特征
- 可转换债券（convertible bond）：具有合同要素 债券转换条款（bond conversion terms） ≥0
- 公司债券（corporate bond）：由……发行 some（由…扮演（is played by） some 法律实体）
- 公司债券（corporate bond） 与 政府债券（government bond） 互斥（disjointWith）
- 公司债券（corporate bond） 与 市政债券（municipal bond） 互斥（disjointWith）
- 票息支付条款（coupon payment terms）：具有利率 some 债券票息（bond coupon）
- 票息支付条款（coupon payment terms）：具有货币 some 货币
- 票息支付条款（coupon payment terms）：具有进度表 some 利息支付计划表
- 固定票息债券（fixed coupon bond）：具有利息支付条款 some 固定票息条款（fixed coupon terms）
- 固定票息债券（fixed coupon bond） 与 浮动票息债券（variable coupon bond） 互斥（disjointWith）
- 固定票息条款（fixed coupon terms）：具有利率 some 固定利率
- 固定票息条款（fixed coupon terms） 与 浮动票息条款（variable coupon terms） 互斥（disjointWith）
- 浮动利率票据（floating rate note）：具有利率 some 参考利率
- 一般责任市政债券（general obligation municipal bond） 与 收益债券（revenue bond） 互斥（disjointWith）
- 政府发行债务证券（government issued debt security）：由……发行 some（由…扮演（is played by） some 政体）
- 指数挂钩债券（index-linked bond）：基于 some（restriction）
- 通胀挂钩债券（inflation-linked bond）：基于 some 通货膨胀率
- 上市债券（listed bond） 与 非上市债券（unlisted bond） 互斥（disjointWith）
- 强制可转换债券（mandatory convertible bond）：具有合同要素 some 债券转换条款（bond conversion terms）
- 市政证券（municipal security）：具有目标 some 市政债务资金用途（municipal debt funds usage）
- 市政证券（municipal security）：由……发行 some（由…扮演（is played by） some（restriction））
- 市政证券（municipal security）：具有资金来源（has funding source） some 市政债务资金来源（municipal debt source of funds）
- 市政证券（municipal security） 与 主权债务工具（sovereign debt instrument） 互斥（disjointWith）
- 原始发行折价债券（original issue discount bond）：restriction
- 原始发行折价债券（original issue discount bond）：具有原始发行折价金额（has original issue discount amount） 货币数量 ≥0
- 部分赎回特征（partial call feature）：具有部分赎回分配惯例（has partial redemption allocation convention） some 部分赎回分配惯例（partial redemption allocation convention）
- 部分赎回分配惯例（partial redemption allocation convention）：restriction
- 利率基准惯例（rate basis convention）：restriction
- 赎回计划表（redemption schedule）：包含 some 兑付事件
- 有担保债券（secured bond） 与 无担保债券（unsecured bond） 互斥（disjointWith）
- 偿债基金摊销条款（sinking fund amortization terms）：restriction
- 主权债券（sovereign bond） 与 市政债券（municipal bond） 互斥（disjointWith）
- 主权债务工具（sovereign debt instrument）：由……发行 some（由…扮演（is played by） some 主权国家）
- 票息递增债券（step up bond）：具有利息支付条款 some 阶梯票息条款（stepped coupon terms）
- 阶梯票息条款（stepped coupon terms）：具有进度表 some 阶梯计划表
- 拆息债券（strip bond）：基于 some 债券（bond）
- 短期国库券（treasury bill）：restriction
- 短期国库券（treasury bill）：restriction
- 短期国库券（treasury bill）：具有利率 some 参考利率
- 浮动票息债券（variable coupon bond）：具有利率 some 债券浮动票息（bond variable coupon）
- 浮动票息条款（variable coupon terms）：基于 some 市场利率
- 浮动票息条款（variable coupon terms）：具有表达式 some 可变利息计算公式（variable interest calculation formula）
- 可变债务本金（variable debt principal）：具有货币数量 some 货币数量
- 可变利息表达式（variable interest expression）：restriction
- 可变利息表达式（variable interest expression）：restriction
- 可变利息表达式（variable interest expression）：具有自变量 完全指数化利率 =1
- 可变本金债券（variable principal bond）：为……定义条款 some 可变债务本金（variable debt principal）
- 零息债券（zero coupon bond）：restriction
- 零息债券（zero coupon bond）：具有原始发行折价金额（has original issue discount amount） 货币数量 ≥0
- 零息债券（zero coupon bond）：具有利息支付条款 some 零息条款（zero coupon terms）
- 零息条款（zero coupon terms）：restriction

## 6. 依赖（owl:imports，37 个）

本本体通过 `owl:imports` 引入以下本体，各项的中文名称与简介如下：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `BE/FunctionalEntities/FunctionalEntities.rdf` | 功能实体本体（Functional Entities Ontology） | 定义「功能实体」：按其在商业中承担的功能（而非法律形式）刻画的实体，是出版方、登记机构等功能性主体的基础。 |
| `BE/GovernmentEntities/GovernmentEntities.rdf` | 政府实体本体（Government Entities Ontology） | 定义政府、政体（polity）、法域（jurisdiction）及政府实体的核心概念，是各区域政府实体本体的共同基础。 |
| `BE/LegalEntities/CorporateBodies.rdf` | 法人团体本体（Corporate Bodies Ontology） | 定义依法设立、具有独立法律人格的法人团体（corporate body），是股份有限公司等具体法人类型的上位概念。 |
| `BE/Trusts/Trusts.rdf` | 信托本体（Trusts Ontology） | 定义信托（trust）及委托人、受托人与受益人之间的信托关系。 |
| `FBC/DebtAndEquities/Debt.rdf` | 债务本体（Debt Ontology） | 定义债务（debt）与债权债务关系的核心概念：借款人、贷款人、本金与利息义务。 |
| `FBC/DebtAndEquities/Guaranty.rdf` | 担保本体（Guaranty Ontology） | 定义担保（guaranty）：担保人、被担保债务与担保范围。 |
| `FBC/FinancialInstruments/FinancialInstruments.rdf` | 金融工具本体（Financial Instruments Ontology） | FIBO 核心本体之一，定义金融工具（financial instrument）的通用概念：可交易、代表某种权利义务的合同工具，是证券、衍生品等具体工具的共同基础。 |
| `FBC/FunctionalEntities/FinancialServicesEntities.rdf` | 金融服务实体本体（Financial Services Entities Ontology） | FBC 域核心本体，定义金融服务机构（银行、券商、保险公司、资管机构等）的功能分类体系。 |
| `FBC/ProductsAndServices/FinancialProductsAndServices.rdf` | 金融产品与服务本体（Financial Products and Services Ontology） | 定义金融产品（financial product）与金融服务（financial service）及其提供、购买关系。 |
| `FND/Accounting/CurrencyAmount.rdf` | 货币金额本体（Currency Amount Ontology） | 定义「金额＋币种」的货币金额（currency amount）表示，是 FIBO 中表达价格、债务金额、付款额等一切带币种数值的基础构件。 |
| `FND/Accounting/ISO4217-CurrencyCodes.rdf` | ISO 4217 货币代码本体（ISO 4217-1 Currency Codes Ontology） | 收录 ISO 4217-1 标准的全部货币代码个体（如 USD、CNY、EUR），为货币金额提供标准化的币种取值。 |
| `FND/Agreements/Agreements.rdf` | 协议本体（Agreements Ontology） | 定义两个或以上参与方之间协议（agreement）的通用概念：协议的当事方、条款、生效与终止，是合同等一切契约性安排的上位模型。 |
| `FND/Agreements/Contracts.rdf` | 合同本体（Contracts Ontology） | 在协议之上定义具有法律约束力的合同（contract）：合同当事方、合同条款、义务与权利，是金融工具与交易合同建模的基石。 |
| `FND/DatesAndTimes/BusinessDates.rdf` | 营业日期本体（Business Dates Ontology） | 定义营业日、营业日历与日期调整规则（如顺延约定），支撑金融合同中的营业日计算。 |
| `FND/DatesAndTimes/FinancialDates.rdf` | 金融日期本体（Financial Dates Ontology） | 定义金融语境下的日期与期间概念：结算日、付息日、到期日、日计数基准等。 |
| `FND/DatesAndTimes/Occurrences.rdf` | 事件与发生本体（Occurrences Ontology） | 定义「发生」（occurrence）、事件与触发条件，用于表达企业行动、信用事件等「发生了什么」。 |
| `FND/GoalsAndObjectives/Objectives.rdf` | 目标本体（Objectives Ontology） | 定义目标（objective）及其与组织、计划的关系，用于表达机构的经营目标与投资目标。 |
| `FND/Parties/Parties.rdf` | 参与方本体（Parties Ontology） | 定义参与方（party）、独立主体（autonomous agent）与「角色扮演」（party in role），是 FIBO 全库使用最广的基础本体之一。 |
| `FND/ProductsAndServices/PaymentsAndSchedules.rdf` | 付款与计划表本体（Payments and Schedules Ontology） | 定义付款、付款计划表（payment schedule）及其日期与金额结构，是贷款还款、债券付息建模的基础。 |
| `FND/Relations/Relations.rdf` | 关系本体（Relations Ontology） | FIBO 最底层的基础本体，定义参考（reference）、分类（classify）等通用关系与抽象概念，全库普遍依赖。 |
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `IND/EconomicIndicators/EconomicIndicators.rdf` | 经济指标本体（Economic Indicators Ontology） | 定义宏观经济指标（GDP、CPI、失业率等）的通用结构：发布机构、发布频率与数值。 |
| `IND/Indicators/Indicators.rdf` | 指标本体（Indicators Ontology） | 定义「指标」（indicator）的通用概念：对某现象的可度量表示，是经济指标、利率等的上位模型。 |
| `IND/InterestRates/InterestRates.rdf` | 利率本体（Interest Rates Ontology） | 定义利率（interest rate）的结构：基准利率、利差、期限与重置机制。 |
| `SEC/Debt/DebtInstruments.rdf` | 债务工具本体（Debt Instruments Ontology） | 定义债务工具（debt instrument）的通用概念：可交易的债权凭证，是债券、票据等的上位模型。 |
| `SEC/Debt/TradedShortTermDebt.rdf` | 短期交易债务本体（Traded Short-Term Debt Ontology） | 定义货币市场工具等短期可交易债务：商业票据、国库券等。 |
| `SEC/Equities/EquityInstruments.rdf` | 股权工具本体（Equity Instruments Ontology） | 定义股票等股权工具：普通股、优先股及其附带的权利。 |
| `SEC/Securities/SecuritiesIssuance.rdf` | 证券发行本体（Securities Issuance Ontology） | 定义证券发行（issuance）：发行人、发行条款与发行结果。 |
| `SEC/Securities/SecuritiesListings.rdf` | 证券上市本体（Securities Listings Ontology） | 定义证券在交易所上市（listing）及其上市状态。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |
| `https://www.omg.org/spec/Commons/Collections/` | OMG 通用集合本体（OMG Commons Collections） | Commons 库中的集合本体，定义集合、成员等通用概念。 |
| `https://www.omg.org/spec/Commons/DatesAndTimes/` | OMG 通用日期与时间本体（OMG Commons Dates and Times） | Commons 库中的日期时间本体，定义日期、期间、时间点等通用时间概念。 |
| `https://www.omg.org/spec/Commons/Documents/` | OMG 通用文档本体（OMG Commons Documents） | Commons 库中的文档本体，定义文档及其组成部分的通用概念。 |
| `https://www.omg.org/spec/Commons/Organizations/` | OMG 通用组织本体（OMG Commons Organizations） | Commons 库中的组织本体，定义组织、组织成员与组织结构的通用概念。 |
| `https://www.omg.org/spec/Commons/QuantitiesAndUnits/` | OMG 通用量与单位本体（OMG Commons Quantities and Units） | Commons 库中的量与单位本体，定义数量、度量单位、量纲的通用概念，支撑金额、比率等数值表达。 |
| `https://www.omg.org/spec/Commons/RegistrationAuthorities/` | OMG 通用登记主管机构本体（OMG Commons Registration Authorities） | Commons 库中的登记主管机构本体，定义负责登记注册的主管机构及其登记行为的通用概念。 |
| `https://www.omg.org/spec/Commons/RolesAndCompositions/` | OMG 通用角色与构成本体（OMG Commons Roles and Compositions） | Commons 库中的角色本体，定义角色及整体—部分构成关系的通用概念。 |

## 7. 文件

- 官方 RDF/XML：`Bonds.rdf`
- 中文 Turtle：`Bonds.ttl`
- 结构图：`Bonds-structure.png` / `Bonds-structure.svg`