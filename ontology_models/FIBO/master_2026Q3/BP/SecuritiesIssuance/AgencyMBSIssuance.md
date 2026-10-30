# 机构 MBS 发行本体（Agency MBS Issuance Ontology）结构与公理说明

本文档对应 `AgencyMBSIssuance.rdf` / `AgencyMBSIssuance.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `AgencyMBSIssuance-structure.png`（`AgencyMBSIssuance-structure.svg` 为可缩放版本）。

![机构 MBS 发行本体（Agency MBS Issuance Ontology）本体结构图](AgencyMBSIssuance-structure.png)

## 1. 本体概述

定义机构抵押贷款支持证券（agency MBS）的发行流程：由政府支持机构（如房利美、房地美）收购贷款、组建资产池并发行。

**在体系中的位置**：BP 证券发行模块中 MBS 发行的两个子类之一。

**上下游关系**：上游继承 MBS 发行本体；下游关联 SEC 抵押贷款支持证券本体。

**与相近概念的差别**：与私人品牌 MBS 发行的差别——发行主体是政府支持机构，证券带有机构担保，信用风险结构完全不同；这是美国住房金融体系的特有分类。

## 2. 类（Class）

| 类（Class） | 定义（Definition） |
|---|---|
| 获取抵押贷款（acquire mortgage） | 购入或以其他方式取得抵押贷款，作为入池资产。 |
| 将抵押贷款加入池中（add mortgage to pool） | 把一笔抵押贷款加入抵押贷款池。 |
| 机构抵押贷款池创建流程（agency mortgage pool creation process） | 机构发行方为证券化而创建抵押贷款池的过程。 |
| 分配主标识符（allocate primary identifier） | 为证券分配主要标识符。 |
| 评估池的发行适用性（assess pool suitablility for issuance） | 评估抵押贷款池是否适合用于发行。 |
| 分类抵押贷款（classify mortgage） | 按类别对抵押贷款进行归类。 |
| 定义抵押贷款池（define mortgage pool） | 确定抵押贷款池的构成标准与内容。 |
| 起草过手证券条款清单（draft pass through termsheet） | 起草定义过手证券条款的信息集，最终将成为该工具的合同条款。 |
| 拟定发行备忘录（draw up offering memorandum） | 拟定载明未来发行基本信息、供潜在投资者参考的发行备忘录。 |
| 拟定条款清单（draw up termsheet） | 拟定载明发行条款的条款清单。 |
| 定稿池内容（finalize pool content） | 最终确定抵押贷款池的构成内容。 |
| 定稿招募说明书（finalize prospectus） | 最终确定发行的招募说明书。 |
| 识别合格抵押贷款（identify conforming mortgage） | 识别符合该发行人总体要求的抵押贷款。 |
| 确定承销商（identify underwriter） | 确定本次发行的承销商。 |
| 组建中机构抵押贷款池（in assembly agency mortgage pool） | 尚在组建、内容未定的机构抵押贷款池。 |
| 发行中机构抵押贷款池（in issuance agency mortgage pool） | 正在发行过程中的机构抵押贷款池。 |
| 使证券进入市场（make securities availabe in market） | 使所发行证券可在市场上获得。 |
| 营销发行（market issue） | 对本次发行进行市场营销。 |
| 未发行机构抵押贷款池（not yet issued agency mortgage pool） | 已组建但尚未发行的机构抵押贷款池。 |
| 过手发行招募说明书部分（pass through issue prospectus part） | 过手 MBS 发行招募说明书的一个部分或章节。 |
| 过手 MBS 招募说明书草案（pass through m b s draft prospectus） | 发行机构在营销发行前确定的过手抵押贷款支持证券发行招募说明书草案。 |
| 过手 MBS 最终招募说明书（pass through m b s final prospectus） | 过手 MBS 发行的最终招募说明书。 |
| 过手 MBS 最终条款清单（pass through m b s final termsheet） | 过手 MBS 发行的最终条款清单，定义 MBS 合同本身的条款。 |
| 过手 MBS 证券化流程（pass through m b s securitization process） | 过手型抵押贷款支持证券的证券化过程。 |
| 过手发行备忘录（pass through offering memorandum） | 过手 MBS 发行的发行备忘录，载明未来发行的基本信息，供潜在投资者参考。 |
| 池合格标准（pool conformance criteria） | 抵押贷款须满足方可入池的标准。 |
| 潜在机构 MBS 发行人（potential agency m b s issuer） | 将成为过手 MBS 发行发行方的实体，是发行中大多数活动的主要行为体。 |
| 潜在过手发行承销商（potential pass through issuance underwriter） | 将成为过手 MBS 发行承销商的实体。 |
| 注册证券（register security） | 交易完成后将证券在注册机构正式注册。 |
| 适合发行（suitable for issue） | 经评估适合用于发行的状态。 |
| 验证合格性（validate conformance） | 自动验证抵押贷款是否符合其拟入池的要求。 |

### 2.1 继承关系（Inheritance）

- 获取抵押贷款（acquire mortgage） ⊑ 发行流程活动
- 将抵押贷款加入池中（add mortgage to pool） ⊑ 发行流程活动
- 机构抵押贷款池创建流程（agency mortgage pool creation process） ⊑ 零售资产池创建流程
- 分配主标识符（allocate primary identifier） ⊑ 发行流程活动
- 评估池的发行适用性（assess pool suitablility for issuance） ⊑ 发行流程活动
- 分类抵押贷款（classify mortgage） ⊑ 发行流程活动
- 定义抵押贷款池（define mortgage pool） ⊑ 发行流程活动
- 起草过手证券条款清单（draft pass through termsheet） ⊑ 条款清单
- 拟定发行备忘录（draw up offering memorandum） ⊑ 发行流程活动
- 拟定条款清单（draw up termsheet） ⊑ 发行流程活动
- 定稿池内容（finalize pool content） ⊑ 发行流程活动
- 定稿招募说明书（finalize prospectus） ⊑ 发行流程活动
- 识别合格抵押贷款（identify conforming mortgage） ⊑ 发行流程活动
- 确定承销商（identify underwriter） ⊑ 发行流程活动
- 组建中机构抵押贷款池（in assembly agency mortgage pool） ⊑ 机构抵押贷款池
- 发行中机构抵押贷款池（in issuance agency mortgage pool） ⊑ 机构抵押贷款池
- 使证券进入市场（make securities availabe in market） ⊑ 发行流程活动
- 营销发行（market issue） ⊑ 发行流程活动
- 未发行机构抵押贷款池（not yet issued agency mortgage pool） ⊑ 机构抵押贷款池
- 过手发行招募说明书部分（pass through issue prospectus part） ⊑ 招募说明书部分
- 过手 MBS 招募说明书草案（pass through m b s draft prospectus） ⊑ 初步招募说明书
- 过手 MBS 最终招募说明书（pass through m b s final prospectus） ⊑ 抵押支持证券发行招募说明书
- 过手 MBS 最终条款清单（pass through m b s final termsheet） ⊑ 过手发行招募说明书部分（pass through issue prospectus part）
- 过手 MBS 最终条款清单（pass through m b s final termsheet） ⊑ 条款清单
- 过手 MBS 证券化流程（pass through m b s securitization process） ⊑ MBS 证券化流程
- 过手发行备忘录（pass through offering memorandum） ⊑ 发行文件
- 潜在机构 MBS 发行人（potential agency m b s issuer） ⊑ 池支持证券证券化流程参与者
- 潜在过手发行承销商（potential pass through issuance underwriter） ⊑ 潜在承销商
- 注册证券（register security） ⊑ 发行流程活动
- 验证合格性（validate conformance） ⊑ 发行流程活动

## 3. 对象属性（Object Property）

| 属性（Property） | 中文（English） | 定义（Definition） | 说明 |
|---|---|---|---|
| fibo-bp-iss-ambs:adds | 添加（adds） | 将某物加入另一事物。 | 定义域（domain）：潜在机构 MBS 发行人（potential agency m b s issuer）；值域（range）：将抵押贷款加入池中（add mortgage to pool） |
| fibo-bp-iss-ambs:addsToPool | 加入池中（adds to pool） | 将某资产加入资产池。 | 定义域（domain）：将抵押贷款加入池中（add mortgage to pool）；值域（range）：房地产担保贷款 |
| fibo-bp-iss-ambs:allocatesIdentifier | 分配标识符（allocates identifier） | 为某事物分配标识符。 | — |
| fibo-bp-iss-ambs:definesCriteriaFor | 为……定义标准（defines criteria for） | 为某事物定义标准。 | 定义域（domain）：池合格标准（pool conformance criteria）；值域（range）：未发行机构抵押贷款池（not yet issued agency mortgage pool） |
| fibo-bp-iss-ambs:finalizes | 定稿（finalizes） | 最终确定某事物。 | 定义域（domain）：潜在机构 MBS 发行人（potential agency m b s issuer）；值域（range）：定稿池内容（finalize pool content） |
| fibo-bp-iss-ambs:hasResource | 具有资源（has resource） | 标识某过程或活动所使用的资源。 | 定义域（domain）：营销发行（market issue）；值域（range）：过手 MBS 招募说明书草案（pass through m b s draft prospectus） |
| fibo-bp-iss-ambs:identifies | 标识（identifies） | 在某情境内识别或确立身份。 | 定义域（domain）：潜在机构 MBS 发行人（potential agency m b s issuer）；值域（range）：识别合格抵押贷款（identify conforming mortgage） |
| fibo-bp-iss-ambs:isAssessmentOf | 是……的评估（is assessment of） | 标识评估所针对的对象。 | 定义域（domain）：分类抵押贷款（classify mortgage）；值域（range）：房地产担保贷款 |
| fibo-bp-iss-ambs:isDefiningOf | 是……的定义（is defining of） | 标识该定义所针对的对象。 | 定义域（domain）：定义抵押贷款池（define mortgage pool）；值域（range）：未发行机构抵押贷款池（not yet issued agency mortgage pool） |
| fibo-bp-iss-ambs:maximumLoanBalance | 最大贷款余额（maximum loan balance） | 入池贷款允许的最大余额。 | 定义域（domain）：池合格标准（pool conformance criteria）；值域（range）：货币数量 |
| fibo-bp-iss-ambs:minimumRating | 最低评级（minimum rating） | 入池或发行所要求的最低评级。 | 定义域（domain）：池合格标准（pool conformance criteria）；值域（range）：投资信用评级 |
| fibo-bp-iss-ambs:purchase | 购买（purchase） | 购入某项资产。 | 定义域（domain）：获取抵押贷款（acquire mortgage）；值域（range）：房地产担保贷款 |
| fibo-bp-iss-ambs:purchases | 购入（purchases） | 购买某项资产。 | 定义域（domain）：潜在机构 MBS 发行人（potential agency m b s issuer）；值域（range）：获取抵押贷款（acquire mortgage） |
| fibo-bp-iss-ambs:resultsInAppointmentOf | 导致任命（results in appointment of） | 其结果是任命某参与方担任某角色。 | 定义域（domain）：确定承销商（identify underwriter）；值域（range）：潜在过手发行承销商（potential pass through issuance underwriter） |
| fibo-bp-iss-ambs:validates | 验证（validates） | 核验某事物是否符合要求。 | 定义域（domain）：潜在机构 MBS 发行人（potential agency m b s issuer）；值域（range）：验证合格性（validate conformance） |

## 5. 公理约定（Axioms）

- 获取抵押贷款（acquire mortgage）：购买（purchase） some 房地产担保贷款
- 将抵押贷款加入池中（add mortgage to pool）：加入池中（adds to pool） some 房地产担保贷款
- 机构抵押贷款池创建流程（agency mortgage pool creation process）：具有结束日期 some 日期
- 机构抵押贷款池创建流程（agency mortgage pool creation process）：具有起始日期 some 日期
- 机构抵押贷款池创建流程（agency mortgage pool creation process）：先于 some 过手 MBS 证券化流程（pass through m b s securitization process）
- 机构抵押贷款池创建流程（agency mortgage pool creation process） 与 非机构池创建流程 互斥（disjointWith）
- 分类抵押贷款（classify mortgage）：是……的评估（is assessment of） some 房地产担保贷款
- 定义抵押贷款池（define mortgage pool）：是……的定义（is defining of） some 未发行机构抵押贷款池（not yet issued agency mortgage pool）
- 识别合格抵押贷款（identify conforming mortgage）：引用 some 房地产担保贷款
- 确定承销商（identify underwriter）：导致任命（results in appointment of） some 潜在过手发行承销商（potential pass through issuance underwriter）
- 组建中机构抵押贷款池（in assembly agency mortgage pool）：具有阶段 some 组建中
- 发行中机构抵押贷款池（in issuance agency mortgage pool）：具有阶段 some 发行中
- 营销发行（market issue）：具有资源（has resource） some 过手 MBS 招募说明书草案（pass through m b s draft prospectus）
- 未发行机构抵押贷款池（not yet issued agency mortgage pool）：具有阶段 some 尚未发行
- 过手 MBS 招募说明书草案（pass through m b s draft prospectus）：先于 some 过手 MBS 最终招募说明书（pass through m b s final prospectus）
- 过手 MBS 最终条款清单（pass through m b s final termsheet）：具有合同要素 some 债券摊销支付条款
- 过手 MBS 最终条款清单（pass through m b s final termsheet）：具有合同要素 some 票息支付条款
- 过手 MBS 证券化流程（pass through m b s securitization process）：具有结束日期 some 日期
- 过手 MBS 证券化流程（pass through m b s securitization process）：具有起始日期 some 日期
- 过手 MBS 证券化流程（pass through m b s securitization process） 与 分层 MBS 证券化流程 互斥（disjointWith）
- 过手发行备忘录（pass through offering memorandum）：包含……的细节 some 过手 MBS 最终条款清单（pass through m b s final termsheet）
- 池合格标准（pool conformance criteria）：为……定义标准（defines criteria for） some 未发行机构抵押贷款池（not yet issued agency mortgage pool）
- 潜在机构 MBS 发行人（potential agency m b s issuer）：添加（adds） some 将抵押贷款加入池中（add mortgage to pool）
- 潜在机构 MBS 发行人（potential agency m b s issuer）：定稿（finalizes） some 定稿池内容（finalize pool content）
- 潜在机构 MBS 发行人（potential agency m b s issuer）：标识（identifies） some 识别合格抵押贷款（identify conforming mortgage）
- 潜在机构 MBS 发行人（potential agency m b s issuer）：购入（purchases） some 获取抵押贷款（acquire mortgage）
- 潜在机构 MBS 发行人（potential agency m b s issuer）：验证（validates） some 验证合格性（validate conformance）
- 潜在机构 MBS 发行人（potential agency m b s issuer）：评估 some 评估池的发行适用性（assess pool suitablility for issuance）
- 潜在机构 MBS 发行人（potential agency m b s issuer）：评估 some 分类抵押贷款（classify mortgage）
- 验证合格性（validate conformance）：引用 some 池合格标准（pool conformance criteria）

## 6. 依赖（owl:imports，20 个）

本本体通过 `owl:imports` 引入以下本体，各项的中文名称与简介如下：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `BP/SecuritiesIssuance/DebtIssuance.rdf` | 债务发行本体（Debt Issuance Ontology） | 定义债券等债务工具的发行流程与参与方。 |
| `BP/SecuritiesIssuance/IssuanceDocuments.rdf` | 发行文件本体（Issuance Documents Ontology） | 定义证券发行过程中使用的法律文件：募集说明书、条款清单等。 |
| `BP/SecuritiesIssuance/IssuanceProcess.rdf` | 发行流程本体（Issuance Process Ontology） | 定义证券发行的通用流程框架：从筹划、定价到配售的各阶段。 |
| `BP/SecuritiesIssuance/MBSIssuance.rdf` | MBS 发行本体（MBS Issuance Ontology） | 定义抵押贷款支持证券（MBS）发行的通用流程：资产池组建、分层与发售。 |
| `BP/SecuritiesIssuance/PrivateLabelMBSIssuance.rdf` | 私人品牌 MBS 发行本体（Private Label MBS Issuance Ontology） | 定义私人机构（非政府机构）发行抵押贷款支持证券的流程。 |
| `FBC/DebtAndEquities/CreditRatings.rdf` | 信用评级本体（Credit Ratings Ontology） | 定义信用评级、评级机构与评级结果，刻画债务人与债务工具的信用水平。 |
| `FND/Accounting/CurrencyAmount.rdf` | 货币金额本体（Currency Amount Ontology） | 定义「金额＋币种」的货币金额（currency amount）表示，是 FIBO 中表达价格、债务金额、付款额等一切带币种数值的基础构件。 |
| `FND/Agreements/Contracts.rdf` | 合同本体（Contracts Ontology） | 在协议之上定义具有法律约束力的合同（contract）：合同当事方、合同条款、义务与权利，是金融工具与交易合同建模的基石。 |
| `FND/Arrangements/Lifecycles.rdf` | 生命周期本体（Lifecycles Ontology） | 定义生命周期、生命周期阶段与状态转移，用于描述合同、金融工具、机构从创设到终止的演化过程。 |
| `FND/Parties/Parties.rdf` | 参与方本体（Parties Ontology） | 定义参与方（party）、独立主体（autonomous agent）与「角色扮演」（party in role），是 FIBO 全库使用最广的基础本体之一。 |
| `FND/Relations/Relations.rdf` | 关系本体（Relations Ontology） | FIBO 最底层的基础本体，定义参考（reference）、分类（classify）等通用关系与抽象概念，全库普遍依赖。 |
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `LOAN/RealEstateLoans/Mortgages.rdf` | 抵押贷款本体（Mortgages Ontology） | 定义以不动产为抵押的贷款：抵押物、抵押登记与止赎。 |
| `SEC/Debt/Bonds.rdf` | 债券本体（Bonds Ontology） | 定义债券（bond）：期限、票面利率、付息方式与偿还结构。 |
| `SEC/Debt/MortgageBackedSecurities.rdf` | 抵押贷款支持证券本体（Mortgage-backed Securities Ontology） | 定义抵押贷款支持证券（MBS）：以抵押贷款池为支持的证券。 |
| `SEC/Debt/PoolBackedSecurities.rdf` | 池支持证券本体（Pool-backed Securities Ontology） | 定义以资产池为支持的证券的通用结构：资产池、分层（tranche）与过手安排。 |
| `SEC/Securities/SecuritiesIssuance.rdf` | 证券发行本体（Securities Issuance Ontology） | 定义证券发行（issuance）：发行人、发行条款与发行结果。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |
| `https://www.omg.org/spec/Commons/DatesAndTimes/` | OMG 通用日期与时间本体（OMG Commons Dates and Times） | Commons 库中的日期时间本体，定义日期、期间、时间点等通用时间概念。 |
| `https://www.omg.org/spec/Commons/Documents/` | OMG 通用文档本体（OMG Commons Documents） | Commons 库中的文档本体，定义文档及其组成部分的通用概念。 |

## 7. 文件

- 官方 RDF/XML：`AgencyMBSIssuance.rdf`
- 中文 Turtle：`AgencyMBSIssuance.ttl`
- 结构图：`AgencyMBSIssuance-structure.png` / `AgencyMBSIssuance-structure.svg`