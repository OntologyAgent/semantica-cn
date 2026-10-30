# 市政债发行本体（Municipal Issuance Ontology）结构与公理说明

本文档对应 `MuniIssuance.rdf` / `MuniIssuance.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `MuniIssuance-structure.png`（`MuniIssuance-structure.svg` 为可缩放版本）。

![市政债发行本体（Municipal Issuance Ontology）本体结构图](MuniIssuance-structure.png)

## 1. 本体概述

定义美国市政债券（municipal bond）的发行流程：州或地方政府为公共项目融资的发行安排。

**在体系中的位置**：BP 证券发行模块的品种特化本体之一。

**上下游关系**：上游继承发行流程本体与债务发行本体；下游关联 SEC 债务工具与 BE 政府实体本体。

**与相近概念的差别**：与公司债发行的差别——发行人是政府实体，债券通常享受免税待遇，且分为一般责任债（GO）与收入债（revenue bond）两种信用结构。

## 2. 类（Class）

| 类（Class） | 定义（Definition） |
|---|---|
| 公告证券发行（announce securities issue） | 对证券发行进行公告。 |
| 债券律师（bond counsel） | 就债券发行的法律问题提供意见的律师事务所。 |
| 代理行（correspondent） | 不是 DTC 直接成员的银行、券商或其他金融机构，依靠 DTC 直接参与者履行其 DTC 职能。 |
| DTCC 成员（d t c c member） | 作为 DTCC 成员的公司，可在发行模型中扮演多种角色。 |
| 债务拍卖流程（debt auction process） | 以拍卖方式发行债务证券的过程。 |
| 债务发行超额配售条款（debt issue over allotment terms） | 债务证券发行数量变更的条款。 |
| 债务承销收尾（debt underwriting closing） | 债务承销发行的收尾环节。 |
| 债务承销发行流程（debt underwriting issuance process） | 以承销方式发行债务证券的流程。 |
| 信息分发（dissemination） | 将发行相关信息向市场分发的活动。 |
| 信息分发承销商（dissemination underwriter） | 负责信息分发的承销商。 |
| 股权去互助化流程（equity demutualization process） | 互助组织转变为股份制公司的过程。 |
| 股票 IPO 流程（equity i p o process） | 股票首次公开发行的流程。 |
| 股票承销发行流程（equity underwriting issuance process） | 以承销方式发行股票的流程。 |
| 发行代理（issuance agent） | 在发行过程中担任代理的参与方。 |
| 发行收尾（issuance closing） | 在结算日向 DTC 参与者账户贷记新发行头寸的过程，整体收尾过程还包括其他步骤。 |
| 发行贷记参与者（issuance crediting participant） | 在发行收尾中被贷记头寸的参与者。 |
| 发行财务顾问（issuance financial advisor） | 为发行提供财务顾问服务的参与方。 |
| 发行印刷商（issuance printer） | 负责印制发行文件的参与方。 |
| 发行流程参与者（issuance process participant） | 发行流程中的参与者。 |
| 发行结算（issuance settlement） | 发行交易的资金与证券交收。 |
| 发行超额配售条款（issue over allotment terms） | 发行数量变更条款：承销协议中允许承销团成员额外购买证券的条款。 |
| 发行人律师（issuer counsel） | 为发行人提供法律意见的律师事务所。 |
| 市政债发行（muni debt offering） | 将市政债务证券提供发行的流程步骤。 |
| 市政发行流程参与者（muni issuance process participant） | 市政债发行流程中的参与者。 |
| 义务人（obligor） | 根据法律或协议有义务偿还债务、付款、做某事或不做某事的参与方。 |
| 付款代理（paying agent） | 代表发行人向证券持有人付款的代理机构。 |
| 潜在市政债承销商（potential muni underwriter） | 证券发行人与投资公众之间的中介，可为 DTC 参与者或代理行。 |
| 私募配售（private placement） | 向特定投资者非公开销售证券的发行方式。 |
| 流程参与者（process participant） | 业务流程中的参与者。 |
| 注册制证券发行流程（registered security issuance process） | 以注册方式发行证券的流程。 |
| 注册（registration） | 向监管机构办理发行注册的行为。 |
| 再营销代理（remarketing agent） | 负责将回售证券重新销售的代理机构。 |
| 证券发行情境（securities issuance context） | 证券发行活动发生的情境。 |
| 证券承销发行（securities underwriting issuance） | 作为证券发行方式的承销。 |
| 证券承销发行流程（securities underwriting issuance process） | 由承销辛迪加将债务工具承销并推向市场的过程。 |
| 服务机构（servicer） | 为资产池提供收款、管理等服务的机构。 |
| 过户代理（transfer agent） | 负责证券登记与过户的代理机构。 |
| 受托人（trustee） | 为他人利益持有并管理资产的参与方。 |
| 承销发行收尾（underwriting issuance closing） | 承销发行的收尾环节。 |
| 承销发行请求方（underwriting issuance requestor） | 发起承销发行请求的参与方。 |
| 承销流程活动（underwriting process activity） | 承销流程中的一项活动。 |
| 承销流程参与者（underwriting process actor） | DTCC 承销流程或任何其他承销流程中的参与者。 |

### 2.1 继承关系（Inheritance）

- 债券律师（bond counsel） ⊑ 合同第三方
- 代理行（correspondent） ⊑ 市政发行流程参与者（muni issuance process participant）
- 代理行（correspondent） ⊑ 合同第三方
- DTCC 成员（d t c c member） ⊑ 市政发行流程参与者（muni issuance process participant）
- 债务拍卖流程（debt auction process） ⊑ 证券发行流程
- 债务发行超额配售条款（debt issue over allotment terms） ⊑ 发行超额配售条款（issue over allotment terms）
- 债务承销收尾（debt underwriting closing） ⊑ 承销发行收尾（underwriting issuance closing）
- 债务承销发行流程（debt underwriting issuance process） ⊑ 证券承销发行流程（securities underwriting issuance process）
- 信息分发（dissemination） ⊑ 承销流程活动（underwriting process activity）
- 信息分发承销商（dissemination underwriter） ⊑ 潜在市政债承销商（potential muni underwriter）
- 股权去互助化流程（equity demutualization process） ⊑ 证券发行流程
- 股票 IPO 流程（equity i p o process） ⊑ 注册制证券发行流程（registered security issuance process）
- 股票承销发行流程（equity underwriting issuance process） ⊑ 注册制证券发行流程（registered security issuance process）
- 发行收尾（issuance closing） ⊑ 发行流程活动
- 发行流程参与者（issuance process participant） ⊑ 流程参与者（process participant）
- 发行结算（issuance settlement） ⊑ 发行流程活动
- 发行超额配售条款（issue over allotment terms） ⊑ 发行文件条款
- 市政债发行（muni debt offering） ⊑ 债务发行
- 市政发行流程参与者（muni issuance process participant） ⊑ 发行流程参与者（issuance process participant）
- 付款代理（paying agent） ⊑ 发行代理（issuance agent）
- 潜在市政债承销商（potential muni underwriter） ⊑ 潜在承销商
- 私募配售（private placement） ⊑ 证券发行流程
- 流程参与者（process participant） ⊑ 参与方角色（party role）
- 注册制证券发行流程（registered security issuance process） ⊑ 证券发行流程
- 注册（registration） ⊑ 发行流程活动
- 证券发行情境（securities issuance context） ⊑ 一级市场
- 证券承销发行（securities underwriting issuance） ⊑ 证券发行情境（securities issuance context）
- 证券承销发行流程（securities underwriting issuance process） ⊑ 证券发行流程
- 过户代理（transfer agent） ⊑ 发行代理（issuance agent）
- 承销发行收尾（underwriting issuance closing） ⊑ 发行收尾（issuance closing）
- 承销发行请求方（underwriting issuance requestor） ⊑ 潜在发行人
- 承销流程活动（underwriting process activity） ⊑ 发行流程活动
- 承销流程参与者（underwriting process actor） ⊑ 参与方角色（party role）

## 3. 对象属性（Object Property）

| 属性（Property） | 中文（English） | 定义（Definition） | 说明 |
|---|---|---|---|
| fibo-bp-iss-muni:actualClosingDate | 实际截止日（actual closing date） | 证券承销商完成收尾的日期。 | 定义域（domain）：发行收尾（issuance closing）；值域（range）：日期 |
| fibo-bp-iss-muni:advises | 提供咨询（advises） | 向……提供建议或指导。 | 定义域（domain）：发行财务顾问（issuance financial advisor）；值域（range）：证券承销发行流程（securities underwriting issuance process） |
| fibo-bp-iss-muni:announcesIssueOf | 公告……的发行（announces issue of） | 公告某证券的发行。 | 定义域（domain）：公告证券发行（announce securities issue）；值域（range）：证券 |
| fibo-bp-iss-muni:disseminationDecisionDateAndTime | 信息分发决定日期时间（dissemination decision date and time） | 信息分发承销商作出信息分发决定的日期时间。 | 定义域（domain）：信息分发（dissemination）；值域（range）：日期时间 |
| fibo-bp-iss-muni:facililtatesRemarketing | 促成再营销（facililtates remarketing） | 为证券的再营销提供便利。 | 定义域（domain）：再营销代理（remarketing agent）；值域（range）：证券承销发行流程（securities underwriting issuance process） |
| fibo-bp-iss-muni:facilitatesPayment | 促成付款（facilitates payment） | 为付款提供便利。 | 定义域（domain）：付款代理（paying agent）；值域（range）：证券承销发行流程（securities underwriting issuance process） |
| fibo-bp-iss-muni:facilitatesTransfer | 促成过户（facilitates transfer） | 为证券过户提供便利。 | 定义域（domain）：过户代理（transfer agent）；值域（range）：证券承销发行流程（securities underwriting issuance process） |
| fibo-bp-iss-muni:formalAwardDateAndTime | 正式授标日期时间（formal award date and time） | 发行人正式接受竞标（竞争性发行）或签署债券购买协议（协议发行）的日期时间。 | 定义域（domain）：债务发行；值域（range）：日期时间 |
| fibo-bp-iss-muni:givesRiseTo | 引起（gives rise to） | 导致某事物的产生。 | — |
| fibo-bp-iss-muni:hasAgent | 具有代理（has agent） | 标识担任代理的参与方。 | 定义域（domain）：证券承销发行流程（securities underwriting issuance process）；值域（range）：发行代理（issuance agent） |
| fibo-bp-iss-muni:hasBondCounsel | 具有债券律师（has bond counsel） | 标识担任债券律师的参与方。 | 定义域（domain）：债务承销发行流程（debt underwriting issuance process）；值域（range）：债券律师（bond counsel） |
| fibo-bp-iss-muni:hasFinancialAdvisor | 具有财务顾问（has financial advisor） | 标识担任财务顾问的参与方。 | 定义域（domain）：证券承销发行流程（securities underwriting issuance process）；值域（range）：发行财务顾问（issuance financial advisor） |
| fibo-bp-iss-muni:hasIssuanceGuarantor | 具有发行担保人（has issuance guarantor） | 标识发行担保人。 | — |
| fibo-bp-iss-muni:hasIssuerCounsel | 具有发行人律师（has issuer counsel） | 标识发行人律师。 | 定义域（domain）：证券承销发行流程（securities underwriting issuance process）；值域（range）：发行人律师（issuer counsel） |
| fibo-bp-iss-muni:hasObligor | 具有义务人（has obligor） | 标识承担偿付义务的参与方。 | 定义域（domain）：证券承销发行流程（securities underwriting issuance process）；值域（range）：义务人（obligor） |
| fibo-bp-iss-muni:hasPayingAgent | 具有付款代理（has paying agent） | 标识付款代理。 | 定义域（domain）：证券承销发行流程（securities underwriting issuance process）；值域（range）：付款代理（paying agent） |
| fibo-bp-iss-muni:hasPotentialIssuer | 具有潜在发行人（has potential issuer） | 标识潜在的发行人。 | — |
| fibo-bp-iss-muni:hasPrinter | 具有印刷商（has printer） | 标识负责印制的参与方。 | 定义域（domain）：证券承销发行流程（securities underwriting issuance process）；值域（range）：发行印刷商（issuance printer） |
| fibo-bp-iss-muni:hasRemarketingAgent | 具有再营销代理（has remarketing agent） | 标识再营销代理。 | 定义域（domain）：证券承销发行流程（securities underwriting issuance process）；值域（range）：再营销代理（remarketing agent） |
| fibo-bp-iss-muni:hasServicer | 具有服务机构（has servicer） | 标识服务机构。 | 定义域（domain）：证券承销发行流程（securities underwriting issuance process）；值域（range）：服务机构（servicer） |
| fibo-bp-iss-muni:hasSubscriber | 具有认购人（has subscriber） | 标识认购人。 | 定义域（domain）：证券承销发行流程（securities underwriting issuance process）；值域（range）：认购人 |
| fibo-bp-iss-muni:hasTransferAgent | 具有过户代理（has transfer agent） | 标识过户代理。 | 定义域（domain）：证券承销发行流程（securities underwriting issuance process）；值域（range）：过户代理（transfer agent） |
| fibo-bp-iss-muni:hasTrustee | 具有受托人（has trustee） | 将信托关联到具名受托人。 | 定义域（domain）：证券承销发行流程（securities underwriting issuance process）；值域（range）：受托人（trustee） |
| fibo-bp-iss-muni:includesStep | 包含步骤（includes step） | 标识流程所包含的步骤。 | 定义域（domain）：注册制证券发行流程（registered security issuance process）；值域（range）：注册（registration） |
| fibo-bp-iss-muni:isAgentIn | 是……中的代理（is agent in） | 标识某参与方担任代理的情境。 | 定义域（domain）：发行代理（issuance agent）；值域（range）：证券承销发行流程（securities underwriting issuance process） |
| fibo-bp-iss-muni:isBondCounsel | 是债券律师（is bond counsel） | 标识担任债券律师的参与方。 | 定义域（domain）：债券律师（bond counsel）；值域（range）：债务承销发行流程（debt underwriting issuance process） |
| fibo-bp-iss-muni:isCreditingParticipant | 是贷记参与者（is crediting participant） | 标识被贷记头寸的参与者。 | 定义域（domain）：发行贷记参与者（issuance crediting participant）；值域（range）：证券承销发行流程（securities underwriting issuance process） |
| fibo-bp-iss-muni:isIssuerCounsel | 是发行人律师（is issuer counsel） | 标识发行人律师。 | 定义域（domain）：发行人律师（issuer counsel）；值域（range）：证券承销发行流程（securities underwriting issuance process） |
| fibo-bp-iss-muni:isTrustee | 是受托人（is trustee） | 标识担任受托人的参与方。 | 定义域（domain）：受托人（trustee）；值域（range）：证券承销发行流程（securities underwriting issuance process） |
| fibo-bp-iss-muni:issuanceSettlementDate | 发行结算日（issuance settlement date） | 初始发行交易的结算日。 | 定义域（domain）：发行结算（issuance settlement）；值域（range）：日期 |
| fibo-bp-iss-muni:makesDecisionOn | 就……作出决定（makes decision on） | 标识决定所针对的事项。 | 定义域（domain）：信息分发承销商（dissemination underwriter）；值域（range）：信息分发（dissemination） |
| fibo-bp-iss-muni:maximumOverAllotmentAmount | 最大超额配售金额（maximum over allotment amount） | 超额配售选择权可用的最大金额。 | 定义域（domain）：债务发行超额配售条款（debt issue over allotment terms）；值域（range）：货币数量 |
| fibo-bp-iss-muni:maximumOverAllotmentPercentage | 最大超额配售百分比（maximum over allotment percentage） | 超额配售选择权可用的百分比。 | 定义域（domain）：发行超额配售条款（issue over allotment terms）；值域（range）：百分比 |
| fibo-bp-iss-muni:obligorTo | 对……负有义务（obligor to） | 标识义务所指向的参与方。 | 定义域（domain）：义务人（obligor）；值域（range）：证券承销发行流程（securities underwriting issuance process） |
| fibo-bp-iss-muni:offeringRequestor | 发行请求方（offering requestor） | 发起发行请求的参与方。 | — |
| fibo-bp-iss-muni:participatesIn | 参与（participates in） | 标识参与某流程或活动。 | 定义域（domain）：市政发行流程参与者（muni issuance process participant）；值域（range）：证券承销发行流程（securities underwriting issuance process） |
| fibo-bp-iss-muni:prints | 印制（prints） | 印制发行文件。 | 定义域（domain）：发行印刷商（issuance printer）；值域（range）：证券承销发行流程（securities underwriting issuance process） |
| fibo-bp-iss-muni:produces | 生产（produces） | 通过加工、制造或生产过程创造。 | 定义域（domain）：证券承销发行流程（securities underwriting issuance process）；值域（range）：承销流程细节 |
| fibo-bp-iss-muni:refersTo | 引用（refers to） | 将……作为信息或解释来源加以引用。 | 定义域（domain）：承销发行收尾（underwriting issuance closing）；值域（range）：承销商承销量 |
| fibo-bp-iss-muni:registeredUnder | 注册于（registered under） | 标识注册所依据的法规或机构。 | 定义域（domain）：注册（registration）；值域（range）：管辖权 |
| fibo-bp-iss-muni:requestedBy | 由……请求（requested by） | 标识发起请求的参与方。 | 定义域（domain）：证券承销发行流程（securities underwriting issuance process）；值域（range）：承销发行请求方（underwriting issuance requestor） |
| fibo-bp-iss-muni:requests | 请求（requests） | 索要某事物。 | 定义域（domain）：承销发行请求方（underwriting issuance requestor）；值域（range）：证券承销发行流程（securities underwriting issuance process） |
| fibo-bp-iss-muni:services | 服务（services） | 为某资产或池提供服务。 | 定义域（domain）：服务机构（servicer）；值域（range）：证券承销发行流程（securities underwriting issuance process） |
| fibo-bp-iss-muni:step | 步骤（step） | 流程中的一个步骤。 | 定义域（domain）：债务承销发行流程（debt underwriting issuance process）；值域（range）：债务发行 |
| fibo-bp-iss-muni:subscriber.1 | 认购人（subscriber） | 认购发行证券的参与方。 | — |
| fibo-bp-iss-muni:subscribesTo | 认购（subscribes to） | 认购人响应营销/招募说明书草案，表达兴趣并获配股份或债务单位。 | 定义域（domain）：认购人；值域（range）：证券承销发行流程（securities underwriting issuance process） |
| fibo-bp-iss-muni:subscribesTo.1 | 认购（subscribes to） | 认购人响应营销/招募说明书草案，表达兴趣并获配股份或债务单位。 | 定义域（domain）：认购人；值域（range）：证券发行流程 |
| fibo-bp-iss-muni:underwrites | 承销（underwrites） | 对发行进行承销。 | 定义域（domain）：潜在市政债承销商（potential muni underwriter）；值域（range）：证券承销发行流程（securities underwriting issuance process） |
| fibo-bp-iss-muni:underwrittenBy | 由……承销（underwritten by） | 标识承销该发行的承销商。 | 定义域（domain）：证券承销发行流程（securities underwriting issuance process）；值域（range）：潜在市政债承销商（potential muni underwriter） |

## 4. 数据属性（Datatype Property）

| 属性（Property） | 中文（English） | 定义（Definition） |
|---|---|---|
| fibo-bp-iss-muni:announcementComments | 公告备注（announcement comments） | 对发行目的、资金来源等的自由文本描述。 |
| fibo-bp-iss-muni:maximumOverAllotmentShares | 最大超额配售股数（maximum over allotment shares） | 超额配售选择权可用的最大股数。 |
| fibo-bp-iss-muni:overAllotmentAvailable | 可超额配售（over allotment available） | 该证券是否提供超额配售选择权。 |
| fibo-bp-iss-muni:overAllotmentExpiryPeriodDays | 超额配售到期天数（over allotment expiry period days） | 初始发行截止后超额配售选择权到期的日历天数。 |
| fibo-bp-iss-muni:saleMethod | 销售方式（sale method） | 证券的销售方式。 |

## 5. 公理约定（Axioms）

- 公告证券发行（announce securities issue）：公告 some 证券发行
- 公告证券发行（announce securities issue）：公告……的发行（announces issue of） some 证券
- 债券律师（bond counsel）：是债券律师（is bond counsel） some 债务承销发行流程（debt underwriting issuance process）
- 代理行（correspondent）：参与（participates in） some 证券承销发行流程（securities underwriting issuance process）
- DTCC 成员（d t c c member）：参与（participates in） some 证券承销发行流程（securities underwriting issuance process）
- 债务拍卖流程（debt auction process） 与 证券承销发行流程（securities underwriting issuance process） 互斥（disjointWith）
- 债务承销收尾（debt underwriting closing）：引用（refers to） some 承销商承销量
- 债务承销发行流程（debt underwriting issuance process）：具有债券律师（has bond counsel） some 债券律师（bond counsel）
- 债务承销发行流程（debt underwriting issuance process）：步骤（step） some 债务发行
- 债务承销发行流程（debt underwriting issuance process） 与 股票承销发行流程（equity underwriting issuance process） 互斥（disjointWith）
- 信息分发承销商（dissemination underwriter）：就……作出决定（makes decision on） some 信息分发（dissemination）
- 发行代理（issuance agent）：是……中的代理（is agent in） some 证券承销发行流程（securities underwriting issuance process）
- 发行贷记参与者（issuance crediting participant）：是贷记参与者（is crediting participant） some 证券承销发行流程（securities underwriting issuance process）
- 发行财务顾问（issuance financial advisor）：提供咨询（advises） some 证券承销发行流程（securities underwriting issuance process）
- 发行印刷商（issuance printer）：印制（prints） some 证券承销发行流程（securities underwriting issuance process）
- 发行超额配售条款（issue over allotment terms）：最大超额配售金额（maximum over allotment amount） 货币数量 ≤1
- 发行人律师（issuer counsel）：是发行人律师（is issuer counsel） some 证券承销发行流程（securities underwriting issuance process）
- 义务人（obligor）：对……负有义务（obligor to） some 证券承销发行流程（securities underwriting issuance process）
- 付款代理（paying agent）：促成付款（facilitates payment） some 证券承销发行流程（securities underwriting issuance process）
- 潜在市政债承销商（potential muni underwriter）：承销（underwrites） some 证券承销发行流程（securities underwriting issuance process）
- 注册制证券发行流程（registered security issuance process）：包含步骤（includes step） some 注册（registration）
- 注册（registration）：注册于（registered under） some 管辖权
- 再营销代理（remarketing agent）：促成再营销（facililtates remarketing） some 证券承销发行流程（securities underwriting issuance process）
- 证券发行情境（securities issuance context）：引用 some 证券
- 证券承销发行（securities underwriting issuance）：引用 some 证券
- 证券承销发行流程（securities underwriting issuance process）：具有代理（has agent） some 发行代理（issuance agent）
- 证券承销发行流程（securities underwriting issuance process）：具有财务顾问（has financial advisor） some 发行财务顾问（issuance financial advisor）
- 证券承销发行流程（securities underwriting issuance process）：具有发行人律师（has issuer counsel） some 发行人律师（issuer counsel）
- 证券承销发行流程（securities underwriting issuance process）：具有义务人（has obligor） some 义务人（obligor）
- 证券承销发行流程（securities underwriting issuance process）：具有付款代理（has paying agent） some 付款代理（paying agent）
- 证券承销发行流程（securities underwriting issuance process）：具有印刷商（has printer） some 发行印刷商（issuance printer）
- 证券承销发行流程（securities underwriting issuance process）：具有再营销代理（has remarketing agent） some 再营销代理（remarketing agent）
- 证券承销发行流程（securities underwriting issuance process）：具有服务机构（has servicer） some 服务机构（servicer）
- 证券承销发行流程（securities underwriting issuance process）：具有认购人（has subscriber） some 认购人
- 证券承销发行流程（securities underwriting issuance process）：具有过户代理（has transfer agent） some 过户代理（transfer agent）
- 证券承销发行流程（securities underwriting issuance process）：具有受托人（has trustee） some 受托人（trustee）
- 证券承销发行流程（securities underwriting issuance process）：生产（produces） some 承销流程细节
- 证券承销发行流程（securities underwriting issuance process）：由……请求（requested by） some 承销发行请求方（underwriting issuance requestor）
- 证券承销发行流程（securities underwriting issuance process）：由……承销（underwritten by） some 潜在市政债承销商（potential muni underwriter）
- 服务机构（servicer）：服务（services） some 证券承销发行流程（securities underwriting issuance process）
- 过户代理（transfer agent）：促成过户（facilitates transfer） some 证券承销发行流程（securities underwriting issuance process）
- 受托人（trustee）：是受托人（is trustee） some 证券承销发行流程（securities underwriting issuance process）
- 承销发行收尾（underwriting issuance closing）：引用（refers to） some 承销商承销量
- 承销发行请求方（underwriting issuance requestor）：请求（requests） some 证券承销发行流程（securities underwriting issuance process）
- 承销流程参与者（underwriting process actor）：restriction

## 6. 依赖（owl:imports，19 个）

本本体通过 `owl:imports` 引入以下本体，各项的中文名称与简介如下：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `BP/Process/FinancialContextAndProcess.rdf` | 金融语境与流程本体（Financial Context and Process Ontology） | 定义金融业务语境下的流程、阶段与参与者，是证券发行等具体业务流程本体的基础。 |
| `BP/SecuritiesIssuance/DebtIssuance.rdf` | 债务发行本体（Debt Issuance Ontology） | 定义债券等债务工具的发行流程与参与方。 |
| `BP/SecuritiesIssuance/IssuanceDocuments.rdf` | 发行文件本体（Issuance Documents Ontology） | 定义证券发行过程中使用的法律文件：募集说明书、条款清单等。 |
| `BP/SecuritiesIssuance/IssuanceProcess.rdf` | 发行流程本体（Issuance Process Ontology） | 定义证券发行的通用流程框架：从筹划、定价到配售的各阶段。 |
| `FBC/FinancialInstruments/FinancialInstruments.rdf` | 金融工具本体（Financial Instruments Ontology） | FIBO 核心本体之一，定义金融工具（financial instrument）的通用概念：可交易、代表某种权利义务的合同工具，是证券、衍生品等具体工具的共同基础。 |
| `FBC/ProductsAndServices/FinancialProductsAndServices.rdf` | 金融产品与服务本体（Financial Products and Services Ontology） | 定义金融产品（financial product）与金融服务（financial service）及其提供、购买关系。 |
| `FND/Accounting/CurrencyAmount.rdf` | 货币金额本体（Currency Amount Ontology） | 定义「金额＋币种」的货币金额（currency amount）表示，是 FIBO 中表达价格、债务金额、付款额等一切带币种数值的基础构件。 |
| `FND/Agreements/Agreements.rdf` | 协议本体（Agreements Ontology） | 定义两个或以上参与方之间协议（agreement）的通用概念：协议的当事方、条款、生效与终止，是合同等一切契约性安排的上位模型。 |
| `FND/Agreements/Contracts.rdf` | 合同本体（Contracts Ontology） | 在协议之上定义具有法律约束力的合同（contract）：合同当事方、合同条款、义务与权利，是金融工具与交易合同建模的基石。 |
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `SEC/Debt/DebtInstruments.rdf` | 债务工具本体（Debt Instruments Ontology） | 定义债务工具（debt instrument）的通用概念：可交易的债权凭证，是债券、票据等的上位模型。 |
| `SEC/Securities/SecuritiesIssuance.rdf` | 证券发行本体（Securities Issuance Ontology） | 定义证券发行（issuance）：发行人、发行条款与发行结果。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |
| `https://www.omg.org/spec/Commons/DatesAndTimes/` | OMG 通用日期与时间本体（OMG Commons Dates and Times） | Commons 库中的日期时间本体，定义日期、期间、时间点等通用时间概念。 |
| `https://www.omg.org/spec/Commons/Documents/` | OMG 通用文档本体（OMG Commons Documents） | Commons 库中的文档本体，定义文档及其组成部分的通用概念。 |
| `https://www.omg.org/spec/Commons/PartiesAndSituations/` | OMG 通用参与方与情境本体（OMG Commons Parties and Situations） | Commons 库中的参与方本体，定义独立主体、参与方及其角色扮演的通用概念，是 FIBO 参与方模型的上游。 |
| `https://www.omg.org/spec/Commons/QuantitiesAndUnits/` | OMG 通用量与单位本体（OMG Commons Quantities and Units） | Commons 库中的量与单位本体，定义数量、度量单位、量纲的通用概念，支撑金额、比率等数值表达。 |
| `https://www.omg.org/spec/Commons/RegulatoryAgencies/` | OMG 通用监管机构本体（OMG Commons Regulatory Agencies） | Commons 库中的监管机构本体，定义监管机构及其监管职权的通用概念。 |
| `https://www.omg.org/spec/Commons/RolesAndCompositions/` | OMG 通用角色与构成本体（OMG Commons Roles and Compositions） | Commons 库中的角色本体，定义角色及整体—部分构成关系的通用概念。 |

## 7. 文件

- 官方 RDF/XML：`MuniIssuance.rdf`
- 中文 Turtle：`MuniIssuance.ttl`
- 结构图：`MuniIssuance-structure.png` / `MuniIssuance-structure.svg`