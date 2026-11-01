# 市政债发行本体（Municipal Issuance Ontology）结构与公理说明

本文档对应 `MuniIssuance.rdf` / `MuniIssuance.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `MuniIssuance-structure.png`（`MuniIssuance-structure.svg` 为可缩放版本）。

![市政债发行本体（Municipal Issuance Ontology）本体结构图](MuniIssuance-structure.png)

## 1. 本体概述

定义美国市政债券（municipal bond）的发行流程：州或地方政府为公共项目融资的发行安排。

**在体系中的位置**：BP 证券发行模块的品种特化本体之一。

**上下游关系**：上游继承发行流程本体与债务发行本体；下游关联 SEC 债务工具与 BE 政府实体本体。

**与相近概念的差别**：与公司债发行的差别——发行人是政府实体，债券通常享受免税待遇，且分为一般责任债（GO）与收入债（revenue bond）两种信用结构。

本本体中类与类的核心关系如下（完整细节见各类小节）：

- **债券律师（bond counsel）** 继承 **合同第三方（ContractThirdParty）**
- **代理行（correspondent）** 继承 **市政发行流程参与者（muni issuance process participant）**
- **代理行（correspondent）** 继承 **合同第三方（ContractThirdParty）**
- **DTCC 成员（d t c c member）** 继承 **市政发行流程参与者（muni issuance process participant）**
- **债务拍卖流程（debt auction process）** 继承 **证券发行流程（SecuritiesIssuanceProcess）**
- **债务发行超额配售条款（debt issue over allotment terms）** 继承 **发行超额配售条款（issue over allotment terms）**
- **债务承销收尾（debt underwriting closing）** 继承 **承销发行收尾（underwriting issuance closing）**
- **债务承销发行流程（debt underwriting issuance process）** 继承 **证券承销发行流程（securities underwriting issuance process）**
- **信息分发（dissemination）** 继承 **承销流程活动（underwriting process activity）**
- **信息分发承销商（dissemination underwriter）** 继承 **潜在市政债承销商（potential muni underwriter）**
- **股权去互助化流程（equity demutualization process）** 继承 **证券发行流程（SecuritiesIssuanceProcess）**
- **股票 IPO 流程（equity i p o process）** 继承 **注册制证券发行流程（registered security issuance process）**
- 其余 51 条关系从略。

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

以下按类逐个展开：每个类给出继承关系、相关属性与公理约定；子类在父类之下降一级编号。

### 2.1 公告证券发行（announce securities issue）

定义：对证券发行进行公告。

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **公告（announces）** | — | — |
| **公告备注（announcement comments）** | 对发行目的、资金来源等的自由文本描述。 | 值域：xsd:string |
| **公告……的发行（announces issue of）** | 公告某证券的发行。 | 值域：证券 |

公理：

- **公告……的发行（announces issue of）**至少有一个取值，类型是**证券（Security）**。
- **公告（announces）**至少有一个取值，类型是**证券发行（SecuritiesOffering）**。

### 2.2 债券律师（bond counsel）

定义：就债券发行的法律问题提供意见的律师事务所。

- 父类：**合同第三方（ContractThirdParty）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **是债券律师（is bond counsel）** | 标识担任债券律师的参与方。 | 值域：债务承销发行流程（debt underwriting issuance process） |

公理：

- **是债券律师（is bond counsel）**至少有一个取值，类型是**债务承销发行流程（debt underwriting issuance process）**。

### 2.3 债务拍卖流程（debt auction process）

定义：以拍卖方式发行债务证券的过程。

- 父类：**证券发行流程（SecuritiesIssuanceProcess）**

公理：

- 与**证券承销发行流程（securities underwriting issuance process）**互斥：同一个体不能同时属于两者。

### 2.4 股权去互助化流程（equity demutualization process）

定义：互助组织转变为股份制公司的过程。

- 父类：**证券发行流程（SecuritiesIssuanceProcess）**

### 2.5 发行代理（issuance agent）

定义：在发行过程中担任代理的参与方。

- 直接子类：**付款代理（paying agent）**、**过户代理（transfer agent）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **是……中的代理（is agent in）** | 标识某参与方担任代理的情境。 | 值域：证券承销发行流程（securities underwriting issuance process） |

公理：

- **是……中的代理（is agent in）**至少有一个取值，类型是**证券承销发行流程（securities underwriting issuance process）**。

#### 2.5.1 付款代理（paying agent）

定义：代表发行人向证券持有人付款的代理机构。

- 父类：**发行代理（issuance agent）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **促成付款（facilitates payment）** | 为付款提供便利。 | 值域：证券承销发行流程（securities underwriting issuance process） |

公理：

- **促成付款（facilitates payment）**至少有一个取值，类型是**证券承销发行流程（securities underwriting issuance process）**。

#### 2.5.2 过户代理（transfer agent）

定义：负责证券登记与过户的代理机构。

- 父类：**发行代理（issuance agent）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **促成过户（facilitates transfer）** | 为证券过户提供便利。 | 值域：证券承销发行流程（securities underwriting issuance process） |

公理：

- **促成过户（facilitates transfer）**至少有一个取值，类型是**证券承销发行流程（securities underwriting issuance process）**。

### 2.6 发行收尾（issuance closing）

定义：在结算日向 DTC 参与者账户贷记新发行头寸的过程，整体收尾过程还包括其他步骤。

- 父类：**发行流程活动（IssuanceProcessActivity）**
- 直接子类：**承销发行收尾（underwriting issuance closing）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **实际截止日（actual closing date）** | 证券承销商完成收尾的日期。 | 值域：日期 |

#### 2.6.1 承销发行收尾（underwriting issuance closing）

定义：承销发行的收尾环节。

- 父类：**发行收尾（issuance closing）**
- 直接子类：**债务承销收尾（debt underwriting closing）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **引用（refers to）** | 将……作为信息或解释来源加以引用。 | 值域：承销商承销量 |

公理：

- **引用（refers to）**至少有一个取值，类型是**承销商承销量（UnderwriterTakedown）**。

##### 2.6.1.1 债务承销收尾（debt underwriting closing）

定义：债务承销发行的收尾环节。

- 父类：**承销发行收尾（underwriting issuance closing）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **引用（refers to）** | 将……作为信息或解释来源加以引用。 | 值域：承销商承销量 |

公理：

- **引用（refers to）**至少有一个取值，类型是**承销商承销量（UnderwriterTakedownForDebt）**。

### 2.7 发行贷记参与者（issuance crediting participant）

定义：在发行收尾中被贷记头寸的参与者。

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **是贷记参与者（is crediting participant）** | 标识被贷记头寸的参与者。 | 值域：证券承销发行流程（securities underwriting issuance process） |

公理：

- **是贷记参与者（is crediting participant）**至少有一个取值，类型是**证券承销发行流程（securities underwriting issuance process）**。

### 2.8 发行财务顾问（issuance financial advisor）

定义：为发行提供财务顾问服务的参与方。

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **提供咨询（advises）** | 向……提供建议或指导。 | 值域：证券承销发行流程（securities underwriting issuance process） |

公理：

- **提供咨询（advises）**至少有一个取值，类型是**证券承销发行流程（securities underwriting issuance process）**。

### 2.9 发行印刷商（issuance printer）

定义：负责印制发行文件的参与方。

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **印制（prints）** | 印制发行文件。 | 值域：证券承销发行流程（securities underwriting issuance process） |

公理：

- **印制（prints）**至少有一个取值，类型是**证券承销发行流程（securities underwriting issuance process）**。

### 2.10 发行结算（issuance settlement）

定义：发行交易的资金与证券交收。

- 父类：**发行流程活动（IssuanceProcessActivity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **发行结算日（issuance settlement date）** | 初始发行交易的结算日。 | 值域：日期 |

### 2.11 发行超额配售条款（issue over allotment terms）

定义：发行数量变更条款：承销协议中允许承销团成员额外购买证券的条款。

- 父类：**发行文件条款（OfferingDocumentTerms）**
- 直接子类：**债务发行超额配售条款（debt issue over allotment terms）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **最大超额配售金额（maximum over allotment amount）** | 超额配售选择权可用的最大金额。 | 值域：货币数量 |
| **最大超额配售百分比（maximum over allotment percentage）** | 超额配售选择权可用的百分比。 | 值域：百分比 |
| **最大超额配售股数（maximum over allotment shares）** | 超额配售选择权可用的最大股数。 | 值域：xsd:integer |
| **可超额配售（over allotment available）** | 该证券是否提供超额配售选择权。 | 值域：xsd:boolean |
| **超额配售到期天数（over allotment expiry period days）** | 初始发行截止后超额配售选择权到期的日历天数。 | 值域：xsd:integer |

公理：

- **最大超额配售金额（maximum over allotment amount）**至多有 1 个**货币数量（MonetaryAmount）**。

#### 2.11.1 债务发行超额配售条款（debt issue over allotment terms）

定义：债务证券发行数量变更的条款。

- 父类：**发行超额配售条款（issue over allotment terms）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **最大超额配售金额（maximum over allotment amount）** | 超额配售选择权可用的最大金额。 | 值域：货币数量 |

### 2.12 发行人律师（issuer counsel）

定义：为发行人提供法律意见的律师事务所。

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **是发行人律师（is issuer counsel）** | 标识发行人律师。 | 值域：证券承销发行流程（securities underwriting issuance process） |

公理：

- **是发行人律师（is issuer counsel）**至少有一个取值，类型是**证券承销发行流程（securities underwriting issuance process）**。

### 2.13 市政债发行（muni debt offering）

定义：将市政债务证券提供发行的流程步骤。

- 父类：**债务发行（DebtOffering）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **销售方式（sale method）** | 证券的销售方式。 | 值域：xsd:string |

### 2.14 义务人（obligor）

定义：根据法律或协议有义务偿还债务、付款、做某事或不做某事的参与方。

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **对……负有义务（obligor to）** | 标识义务所指向的参与方。 | 值域：证券承销发行流程（securities underwriting issuance process） |

公理：

- **对……负有义务（obligor to）**至少有一个取值，类型是**证券承销发行流程（securities underwriting issuance process）**。

### 2.15 潜在市政债承销商（potential muni underwriter）

定义：证券发行人与投资公众之间的中介，可为 DTC 参与者或代理行。

- 父类：**潜在承销商（PotentialUnderwriter）**
- 直接子类：**信息分发承销商（dissemination underwriter）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **承销（underwrites）** | 对发行进行承销。 | 值域：证券承销发行流程（securities underwriting issuance process） |

公理：

- **承销（underwrites）**至少有一个取值，类型是**证券承销发行流程（securities underwriting issuance process）**。

#### 2.15.1 信息分发承销商（dissemination underwriter）

定义：负责信息分发的承销商。

- 父类：**潜在市政债承销商（potential muni underwriter）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **就……作出决定（makes decision on）** | 标识决定所针对的事项。 | 值域：信息分发（dissemination） |

公理：

- **就……作出决定（makes decision on）**至少有一个取值，类型是**信息分发（dissemination）**。

### 2.16 私募配售（private placement）

定义：向特定投资者非公开销售证券的发行方式。

- 父类：**证券发行流程（SecuritiesIssuanceProcess）**

### 2.17 流程参与者（process participant）

定义：业务流程中的参与者。

- 父类：**参与方角色（party role）**
- 直接子类：**发行流程参与者（issuance process participant）**

#### 2.17.1 发行流程参与者（issuance process participant）

定义：发行流程中的参与者。

- 父类：**流程参与者（process participant）**
- 直接子类：**市政发行流程参与者（muni issuance process participant）**

##### 2.17.1.1 市政发行流程参与者（muni issuance process participant）

定义：市政债发行流程中的参与者。

- 父类：**发行流程参与者（issuance process participant）**
- 直接子类：**代理行（correspondent）**、**DTCC 成员（d t c c member）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **参与（participates in）** | 标识参与某流程或活动。 | 值域：证券承销发行流程（securities underwriting issuance process） |

###### 2.17.1.1.1 代理行（correspondent）

定义：不是 DTC 直接成员的银行、券商或其他金融机构，依靠 DTC 直接参与者履行其 DTC 职能。

- 父类：**市政发行流程参与者（muni issuance process participant）**、**合同第三方（ContractThirdParty）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **参与（participates in）** | 标识参与某流程或活动。 | 值域：证券承销发行流程（securities underwriting issuance process） |

公理：

- **参与（participates in）**至少有一个取值，类型是**证券承销发行流程（securities underwriting issuance process）**。

###### 2.17.1.1.2 DTCC 成员（d t c c member）

定义：作为 DTCC 成员的公司，可在发行模型中扮演多种角色。

- 父类：**市政发行流程参与者（muni issuance process participant）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **参与（participates in）** | 标识参与某流程或活动。 | 值域：证券承销发行流程（securities underwriting issuance process） |

公理：

- **参与（participates in）**至少有一个取值，类型是**证券承销发行流程（securities underwriting issuance process）**。

### 2.18 注册制证券发行流程（registered security issuance process）

定义：以注册方式发行证券的流程。

- 父类：**证券发行流程（SecuritiesIssuanceProcess）**
- 直接子类：**股票 IPO 流程（equity i p o process）**、**股票承销发行流程（equity underwriting issuance process）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **包含步骤（includes step）** | 标识流程所包含的步骤。 | 值域：注册（registration） |

公理：

- **包含步骤（includes step）**至少有一个取值，类型是**注册（registration）**。

#### 2.18.1 股票 IPO 流程（equity i p o process）

定义：股票首次公开发行的流程。

- 父类：**注册制证券发行流程（registered security issuance process）**

#### 2.18.2 股票承销发行流程（equity underwriting issuance process）

定义：以承销方式发行股票的流程。

- 父类：**注册制证券发行流程（registered security issuance process）**

### 2.19 注册（registration）

定义：向监管机构办理发行注册的行为。

- 父类：**发行流程活动（IssuanceProcessActivity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **注册于（registered under）** | 标识注册所依据的法规或机构。 | 值域：管辖权 |

公理：

- **注册于（registered under）**至少有一个取值，类型是**管辖权（Jurisdiction）**。

### 2.20 再营销代理（remarketing agent）

定义：负责将回售证券重新销售的代理机构。

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **促成再营销（facililtates remarketing）** | 为证券的再营销提供便利。 | 值域：证券承销发行流程（securities underwriting issuance process） |

公理：

- **促成再营销（facililtates remarketing）**至少有一个取值，类型是**证券承销发行流程（securities underwriting issuance process）**。

### 2.21 证券发行情境（securities issuance context）

定义：证券发行活动发生的情境。

- 父类：**一级市场（PrimaryMarket）**
- 直接子类：**证券承销发行（securities underwriting issuance）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **引用（refersTo）** | — | — |

公理：

- **引用（refersTo）**至少有一个取值，类型是**证券（Security）**。

#### 2.21.1 证券承销发行（securities underwriting issuance）

定义：作为证券发行方式的承销。

- 父类：**证券发行情境（securities issuance context）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **引用（refersTo）** | — | — |

公理：

- **引用（refersTo）**至少有一个取值，类型是**证券（Security）**。

### 2.22 证券承销发行流程（securities underwriting issuance process）

定义：由承销辛迪加将债务工具承销并推向市场的过程。

- 父类：**证券发行流程（SecuritiesIssuanceProcess）**
- 直接子类：**债务承销发行流程（debt underwriting issuance process）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有代理（has agent）** | 标识担任代理的参与方。 | 值域：发行代理（issuance agent） |
| **具有财务顾问（has financial advisor）** | 标识担任财务顾问的参与方。 | 值域：发行财务顾问（issuance financial advisor） |
| **具有发行人律师（has issuer counsel）** | 标识发行人律师。 | 值域：发行人律师（issuer counsel） |
| **具有义务人（has obligor）** | 标识承担偿付义务的参与方。 | 值域：义务人（obligor） |
| **具有付款代理（has paying agent）** | 标识付款代理。 | 值域：付款代理（paying agent） |
| **具有印刷商（has printer）** | 标识负责印制的参与方。 | 值域：发行印刷商（issuance printer） |
| **具有再营销代理（has remarketing agent）** | 标识再营销代理。 | 值域：再营销代理（remarketing agent） |
| **具有服务机构（has servicer）** | 标识服务机构。 | 值域：服务机构（servicer） |
| **具有认购人（has subscriber）** | 标识认购人。 | 值域：认购人 |
| **具有过户代理（has transfer agent）** | 标识过户代理。 | 值域：过户代理（transfer agent） |
| **具有受托人（has trustee）** | 将信托关联到具名受托人。 | 值域：受托人（trustee） |
| **生产（produces）** | 通过加工、制造或生产过程创造。 | 值域：承销流程细节 |
| **由……请求（requested by）** | 标识发起请求的参与方。 | 值域：承销发行请求方（underwriting issuance requestor） |
| **由……承销（underwritten by）** | 标识承销该发行的承销商。 | 值域：潜在市政债承销商（potential muni underwriter） |

公理：

- **具有义务人（has obligor）**至少有一个取值，类型是**义务人（obligor）**。
- **具有付款代理（has paying agent）**至少有一个取值，类型是**付款代理（paying agent）**。
- **具有代理（has agent）**至少有一个取值，类型是**发行代理（issuance agent）**。
- **具有再营销代理（has remarketing agent）**至少有一个取值，类型是**再营销代理（remarketing agent）**。
- **具有印刷商（has printer）**至少有一个取值，类型是**发行印刷商（issuance printer）**。
- **具有发行人律师（has issuer counsel）**至少有一个取值，类型是**发行人律师（issuer counsel）**。
- **具有受托人（has trustee）**至少有一个取值，类型是**受托人（trustee）**。
- **具有服务机构（has servicer）**至少有一个取值，类型是**服务机构（servicer）**。
- **具有认购人（has subscriber）**至少有一个取值，类型是**认购人（Subscriber）**。
- **具有财务顾问（has financial advisor）**至少有一个取值，类型是**发行财务顾问（issuance financial advisor）**。
- **具有过户代理（has transfer agent）**至少有一个取值，类型是**过户代理（transfer agent）**。
- **生产（produces）**至少有一个取值，类型是**承销流程细节（UnderwritingProcessDetails）**。
- **由……承销（underwritten by）**至少有一个取值，类型是**潜在市政债承销商（potential muni underwriter）**。
- **由……请求（requested by）**至少有一个取值，类型是**承销发行请求方（underwriting issuance requestor）**。

#### 2.22.1 债务承销发行流程（debt underwriting issuance process）

定义：以承销方式发行债务证券的流程。

- 父类：**证券承销发行流程（securities underwriting issuance process）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有债券律师（has bond counsel）** | 标识担任债券律师的参与方。 | 值域：债券律师（bond counsel） |
| **步骤（step）** | 流程中的一个步骤。 | 值域：债务发行 |

公理：

- **具有债券律师（has bond counsel）**至少有一个取值，类型是**债券律师（bond counsel）**。
- **步骤（step）**至少有一个取值，类型是**债务发行（DebtOffering）**。
- 与**股票承销发行流程（equity underwriting issuance process）**互斥：同一个体不能同时属于两者。

### 2.23 服务机构（servicer）

定义：为资产池提供收款、管理等服务的机构。

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **服务（services）** | 为某资产或池提供服务。 | 值域：证券承销发行流程（securities underwriting issuance process） |

公理：

- **服务（services）**至少有一个取值，类型是**证券承销发行流程（securities underwriting issuance process）**。

### 2.24 受托人（trustee）

定义：为他人利益持有并管理资产的参与方。

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **是受托人（is trustee）** | 标识担任受托人的参与方。 | 值域：证券承销发行流程（securities underwriting issuance process） |

公理：

- **是受托人（is trustee）**至少有一个取值，类型是**证券承销发行流程（securities underwriting issuance process）**。

### 2.25 承销发行请求方（underwriting issuance requestor）

定义：发起承销发行请求的参与方。

- 父类：**潜在发行人（PotentialIssuer）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **请求（requests）** | 索要某事物。 | 值域：证券承销发行流程（securities underwriting issuance process） |

公理：

- **请求（requests）**至少有一个取值，类型是**证券承销发行流程（securities underwriting issuance process）**。

### 2.26 承销流程活动（underwriting process activity）

定义：承销流程中的一项活动。

- 父类：**发行流程活动（IssuanceProcessActivity）**
- 直接子类：**信息分发（dissemination）**

#### 2.26.1 信息分发（dissemination）

定义：将发行相关信息向市场分发的活动。

- 父类：**承销流程活动（underwriting process activity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **信息分发决定日期时间（dissemination decision date and time）** | 信息分发承销商作出信息分发决定的日期时间。 | 值域：日期时间 |

### 2.27 承销流程参与者（underwriting process actor）

定义：DTCC 承销流程或任何其他承销流程中的参与者。

- 父类：**参与方角色（party role）**

公理：

- 该属性存在取值约束。

## 3. 其他属性

以下属性未绑定到本体的具体类（定义域在外部本体或未声明）：

对象属性（Object Property）：

| 属性 | 定义 | 说明 |
|---|---|---|
| **正式授标日期时间（formal award date and time）** | 发行人正式接受竞标（竞争性发行）或签署债券购买协议（协议发行）的日期时间。 | 值域：日期时间 |
| **引起（gives rise to）** | 导致某事物的产生。 | — |
| **具有发行担保人（has issuance guarantor）** | 标识发行担保人。 | — |
| **具有潜在发行人（has potential issuer）** | 标识潜在的发行人。 | — |
| **发行请求方（offering requestor）** | 发起发行请求的参与方。 | — |
| **认购人（subscriber）** | 认购发行证券的参与方。 | — |
| **认购（subscribes to）** | 认购人响应营销/招募说明书草案，表达兴趣并获配股份或债务单位。 | 值域：证券承销发行流程（securities underwriting issuance process） |
| **认购（subscribes to）** | 认购人响应营销/招募说明书草案，表达兴趣并获配股份或债务单位。 | 值域：证券发行流程 |

## 4. 依赖（owl:imports，19 个）

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

## 5. 文件

- 官方 RDF/XML：`MuniIssuance.rdf`
- 中文 Turtle：`MuniIssuance.ttl`
- 结构图：`MuniIssuance-structure.png` / `MuniIssuance-structure.svg`