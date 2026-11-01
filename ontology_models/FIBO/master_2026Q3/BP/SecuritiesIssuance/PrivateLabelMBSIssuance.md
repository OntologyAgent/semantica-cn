# 私人品牌 MBS 发行本体（Private Label MBS Issuance Ontology）结构与公理说明

本文档对应 `PrivateLabelMBSIssuance.rdf` / `PrivateLabelMBSIssuance.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `PrivateLabelMBSIssuance-structure.png`（`PrivateLabelMBSIssuance-structure.svg` 为可缩放版本）。

![私人品牌 MBS 发行本体（Private Label MBS Issuance Ontology）本体结构图](PrivateLabelMBSIssuance-structure.png)

## 1. 本体概述

定义私人品牌抵押贷款支持证券（private label MBS）的发行流程：由私人金融机构（非政府机构）组建贷款池并发行。

**在体系中的位置**：BP 证券发行模块中 MBS 发行的两个子类之一。

**上下游关系**：上游继承 MBS 发行本体；下游关联 SEC 抵押贷款支持证券与担保债务凭证本体。

**与相近概念的差别**：与机构 MBS 发行的差别——没有机构担保，需要依靠分层、超额抵押等信用增级手段，2008 年金融危机中出问题的主要是这类。

本本体中类与类的核心关系如下（完整细节见各类小节）：

- **池生命周期状态选择（PoolLifecycleStateSelection）** 继承 **生命周期阶段（LifecycleStage）**
- **分配主标识符（allocate primary identifier）** 继承 **发行流程活动（IssuanceProcessActivity）**
- **分配评级（allocate ratings）** 继承 **发行流程活动（IssuanceProcessActivity）**
- **评估池的发行适用性（assess pool suitability for issuance）** 继承 **发行流程活动（IssuanceProcessActivity）**
- **评估评级（assess ratings）** 继承 **发行流程活动（IssuanceProcessActivity）**
- **完成交易（close deal）** 继承 **发行流程活动（IssuanceProcessActivity）**
- **定义票据参数（define notes parameters）** 继承 **发行流程活动（IssuanceProcessActivity）**
- **定义池特征（define pool characteristics）** 继承 **发行流程活动（IssuanceProcessActivity）**
- **起草分层票据参数（draft tranche notes parameters）** 继承 **文件（Document）**
- **起草分层结构（draft tranche structure）** 继承 **文件（Document）**
- **起草分层条款清单（draft tranche termsheet）** 继承 **条款清单（TermSheet）**
- **拟定发行备忘录（draw up offering memorandum）** 继承 **发行流程活动（IssuanceProcessActivity）**
- 其余 52 条关系从略。

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

以下按类逐个展开：每个类给出继承关系、相关属性与公理约定；子类在父类之下降一级编号。

### 2.1 池生命周期状态选择（PoolLifecycleStateSelection）

定义：对抵押贷款池生命周期状态的选择。

- 父类：**生命周期阶段（LifecycleStage）**

### 2.2 分配主标识符（allocate primary identifier）

定义：为证券分配主要标识符。

- 父类：**发行流程活动（IssuanceProcessActivity）**

### 2.3 分配评级（allocate ratings）

定义：为各分层证券确定评级。

- 父类：**发行流程活动（IssuanceProcessActivity）**

### 2.4 评估池的发行适用性（assess pool suitability for issuance）

定义：评估抵押贷款池是否适合用于发行。

- 父类：**发行流程活动（IssuanceProcessActivity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **是……的评估（is assessment of）** | 标识评估所针对的对象。 | 值域：组建中抵押贷款池（in assembly mortgage pool） |

公理：

- **是……的评估（is assessment of）**至少有一个取值，类型是**组建中抵押贷款池（in assembly mortgage pool）**。

### 2.5 评估评级（assess ratings）

定义：对分层证券可获得的评级进行评估。

- 父类：**发行流程活动（IssuanceProcessActivity）**

### 2.6 经纪自营商（broker dealer）

定义：可能成为本次发行主要投资者的实体。

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **承诺（commits to）** | 对某事物作出承诺。 | 值域：获得投资者承诺（get commitment from investors） |

公理：

- **承诺（commits to）**至少有一个取值，类型是**获得投资者承诺（get commitment from investors）**。

### 2.7 完成交易（close deal）

定义：完成本次发行交易。

- 父类：**发行流程活动（IssuanceProcessActivity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **导致（results in）** | 产生某个结果。 | 值域：分层 MBS 交易（tranched m b s deal transaction） |
| **导致发布（results in publication of）** | 其结果是某文件的发布。 | 值域：汇款报告（remittance report） |

公理：

- **导致发布（results in publication of）**至少有一个取值，类型是**汇款报告（remittance report）**。
- **导致（results in）**至少有一个取值，类型是**分层 MBS 交易（tranched m b s deal transaction）**。

### 2.8 定义票据参数（define notes parameters）

定义：定义票据的面额等参数。

- 父类：**发行流程活动（IssuanceProcessActivity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **导致（results in）** | 产生某个结果。 | 值域：起草分层票据参数（draft tranche notes parameters） |

公理：

- **导致（results in）**至少有一个取值，类型是**起草分层票据参数（draft tranche notes parameters）**。

### 2.9 定义池特征（define pool characteristics）

定义：确定抵押贷款池的特征。

- 父类：**发行流程活动（IssuanceProcessActivity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **是……的定义（isDefiningOf）** | 标识该定义所针对的对象。 | 值域：未发行非机构抵押贷款池（not yet issued non agency mortgage pool） |

公理：

- **是……的定义（isDefiningOf）**至少有一个取值，类型是**未发行非机构抵押贷款池（not yet issued non agency mortgage pool）**。

### 2.10 起草分层票据参数（draft tranche notes parameters）

定义：起草定义某一分层票据细分（面额及可购金额）的信息集。

- 父类：**文件（Document）**

### 2.11 起草分层结构（draft tranche structure）

定义：起草定义分层发行中各分层及其相互关系的信息集。

- 父类：**文件（Document）**

### 2.12 起草分层条款清单（draft tranche termsheet）

定义：起草定义分层发行中某一分层的信息集，将成为该分层的条款清单。

- 父类：**条款清单（TermSheet）**

### 2.13 拟定发行备忘录（draw up offering memorandum）

定义：拟定载明未来发行基本信息、供潜在投资者参考的发行备忘录。

- 父类：**发行流程活动（IssuanceProcessActivity）**

### 2.14 拟定各分层条款清单（draw up tranche termsheets）

定义：拟定分层发行中各分层的条款清单。

- 父类：**发行流程活动（IssuanceProcessActivity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **要求（requires）** | 标识某活动或状态所要求的前提。 | 值域：非机构抵押贷款池 |

公理：

- **要求（requires）**至少有一个取值，类型是**非机构抵押贷款池（NonAgencyMortgagePool）**。

### 2.15 定稿池内容（finalize pool content）

定义：最终确定抵押贷款池的构成内容。

- 父类：**发行流程活动（IssuanceProcessActivity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **定稿（finalizes）** | 最终确定某事物。 | 值域：发行中非机构抵押贷款池（in issuance non agency mortgage pool） |

公理：

- **定稿（finalizes）**至少有一个取值，类型是**发行中非机构抵押贷款池（in issuance non agency mortgage pool）**。

### 2.16 定稿招募说明书（finalize prospectus）

定义：最终确定发行的招募说明书。

- 父类：**发行流程活动（IssuanceProcessActivity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **导致（results in）** | 产生某个结果。 | 值域：分档型抵押支持证券交易招募说明书 |

公理：

- **导致（results in）**至少有一个取值，类型是**分档型抵押支持证券交易招募说明书（TranchedMBSDealProspectus）**。

### 2.17 获得投资者承诺（get commitment from investors）

定义：取得投资者认购本次发行的承诺。

- 父类：**发行流程活动（IssuanceProcessActivity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **基于……的承诺（commitment based on）** | 标识承诺所依据的事物。 | 值域：分层招募说明书草案（tranched draft prospectus） |
| **具有资源（has resource）** | 标识某过程或活动所使用的资源。 | 值域：起草分层票据参数（draft tranche notes parameters） |
| **具有资源（has resource）** | 标识某过程或活动所使用的资源。 | 值域：起草分层票据参数（draft tranche notes parameters） |

公理：

- **具有资源（has resource）**至少有一个取值，类型是**起草分层票据参数（draft tranche notes parameters）**。
- **具有资源（has resource）**至少有一个取值，类型是**起草分层票据参数（draft tranche notes parameters）**。
- **基于……的承诺（commitment based on）**至少有一个取值，类型是**分层招募说明书草案（tranched draft prospectus）**。

### 2.18 识别合格抵押贷款（identify conforming mortgage）

定义：识别符合该发行人总体要求的抵押贷款。

- 父类：**发行流程活动（IssuanceProcessActivity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **引用（refers to）** | 将……作为信息或解释来源加以引用。 | 值域：房地产担保贷款 |

公理：

- **引用（refers to）**至少有一个取值，类型是**房地产担保贷款（LoanSecuredByRealEstate）**。

### 2.19 确定承销商（identify underwriter）

定义：确定本次发行的承销商。

- 父类：**发行流程活动（IssuanceProcessActivity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **导致（resultsIn）** | — | — |

公理：

- **导致（resultsIn）**至少有一个取值，类型是**潜在分层发行承销商（potential tranched issue underwriter）**。

### 2.20 组建中抵押贷款池（in assembly mortgage pool）

定义：尚在组建、内容未定的抵押贷款池。

- 父类：**非机构抵押贷款池（NonAgencyMortgagePool）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有阶段（hasStage）** | — | — |

公理：

- **具有阶段（hasStage）**至少有一个取值，类型是**组建中（InAssembly）**。

### 2.21 发行中非机构抵押贷款池（in issuance non agency mortgage pool）

定义：正在发行过程中的非机构抵押贷款池。

- 父类：**非机构抵押贷款池（NonAgencyMortgagePool）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有阶段（hasStage）** | — | — |

公理：

- **具有阶段（hasStage）**至少有一个取值，类型是**发行中（InIssuance）**。

### 2.22 投资者（investor）

定义：通过投资拥有某组织一定份额的参与方。

### 2.23 MBS 证券化结束（m b s securitization end）

定义：MBS 证券化流程的结束节点。

### 2.24 MBS 证券化开始（m b s securitization start）

定义：MBS 证券化流程的起始节点。

### 2.25 使证券进入市场（make securities available in market）

定义：使所发行证券可在市场上获得（结构化融资市场较小，主要通过定向营销）。

- 父类：**发行流程活动（IssuanceProcessActivity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **是……的发行（is issue of）** | 标识发行所对应的证券或池。 | 值域：分档型抵押支持证券交易 |
| **要求（requires）** | 标识某活动或状态所要求的前提。 | 值域：分档型抵押支持证券交易招募说明书 |

公理：

- **是……的发行（is issue of）**至少有一个取值，类型是**分档型抵押支持证券交易（TranchedMBSDeal）**。
- **要求（requires）**至少有一个取值，类型是**分档型抵押支持证券交易招募说明书（TranchedMBSDealProspectus）**。

### 2.26 向主要投资者营销发行（market issue to primary investors）

定义：面向主要投资者对本次发行进行营销。

- 父类：**发行流程活动（IssuanceProcessActivity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有资源（has resource）** | 标识某过程或活动所使用的资源。 | 值域：分层发行备忘录（tranched offering memorandum） |

公理：

- **具有资源（has resource）**至少有一个取值，类型是**分层发行备忘录（tranched offering memorandum）**。

### 2.27 非机构池创建结束（non agency pool creation end）

定义：非机构抵押贷款池创建流程的结束节点。

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **流转（flow）** | 流程中的流转关系。 | 值域：MBS 证券化开始（m b s securitization start） |

公理：

- **流转（flow）**至少有一个取值，类型是**MBS 证券化开始（m b s securitization start）**。

### 2.28 非机构池创建流程（non agency pool creation process）

定义：私募（非机构）抵押贷款池的创建过程。

- 父类：**零售资产池创建流程（RetailAssetPoolCreationProcess）**

### 2.29 非机构池创建开始（non agency pool creation start）

定义：非机构抵押贷款池创建流程的起始节点。

### 2.30 未发行非机构抵押贷款池（not yet issued non agency mortgage pool）

定义：已组建但尚未发行的非机构抵押贷款池。

- 父类：**非机构抵押贷款池（NonAgencyMortgagePool）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有阶段（hasStage）** | — | — |

公理：

- **具有阶段（hasStage）**至少有一个取值，类型是**尚未发行（NotYetIssued）**。

### 2.31 编号机构（numbering agency）

定义：为证券提供主要证券标识符的机构。

- 父类：**证券发行流程参与者（SecuritiesIssuanceProcessActor）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **分配标识符（allocatesIdentifier）** | — | — |
| **分配标识符（allocates identifier）** | 为某事物分配标识符。 | 值域：分配主标识符（allocate primary identifier） |

公理：

- **分配标识符（allocates identifier）**至少有一个取值，类型是**分配主标识符（allocate primary identifier）**。
- **分配标识符（allocatesIdentifier）**至少有一个取值，类型是**分配主标识符（AllocatePrimaryIdentifier）**。

### 2.32 池可发行（pool ready for issue）

定义：抵押贷款池已具备发行条件的状态。

### 2.33 池受托人（pool trustee）

定义：为资产池担任受托人的参与方。

- 父类：**参与方角色（party role）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **可能成为（may become）** | 标识某事物在流程中可能转变成的角色或状态。 | 值域：证券承销商 |

公理：

- **可能成为（may become）**至少有一个取值，类型是**证券承销商（SecurityUnderwriter）**。

### 2.34 潜在 MBS 投资者（potential m b s investor）

定义：可能成为 MBS 发行投资者的参与方。

### 2.35 潜在非机构 MBS 发行人（potential non agency m b s issuer）

定义：将成为分层 MBS 发行发行方的实体，是发行中大多数活动的主要行为体。

- 父类：**池支持证券证券化流程参与者（PoolBackedSecuritySecuritizationProcessActor）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **评估（evaluates）** | — | — |

公理：

- **评估（evaluates）**至少有一个取值，类型是**评估池的发行适用性（assess pool suitability for issuance）**。
- **评估（evaluates）**至少有一个取值，类型是**评估评级（assess ratings）**。

### 2.36 潜在分层发行承销商（potential tranched issue underwriter）

定义：将成为分层 MBS 发行承销商的实体。

- 父类：**潜在承销商（PotentialUnderwriter）**

### 2.37 主要投资者（primary investor）

定义：通过购买本次发行的部分分层而成为主要投资者的参与方。

### 2.38 购入抵押贷款入池（purchase mortgage into pool）

定义：购入抵押贷款并将其纳入资产池。

- 父类：**发行流程活动（IssuanceProcessActivity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **添加到（adds to）** | 将某物添加到另一事物。 | 值域：组建中抵押贷款池（in assembly mortgage pool） |
| **是……的购买（is purchase of）** | 标识购买行为所针对的资产。 | 值域：房地产担保贷款 |

公理：

- **是……的购买（is purchase of）**至少有一个取值，类型是**房地产担保贷款（LoanSecuredByRealEstate）**。
- **添加到（adds to）**至少有一个取值，类型是**组建中抵押贷款池（in assembly mortgage pool）**。

### 2.39 评级机构（ratings agency）

定义：为发行提供评级的机构。

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **分配评级（allocates ratings）** | 为证券分配评级。 | 值域：分配评级（allocate ratings） |

公理：

- **分配评级（allocates ratings）**至少有一个取值，类型是**分配评级（allocate ratings）**。

### 2.40 评级适合发行（ratings suitable for issue）

定义：评级结果满足发行要求的状态。

### 2.41 注册证券（register security）

定义：交易完成后将证券在注册机构正式注册。

- 父类：**发行流程活动（IssuanceProcessActivity）**

### 2.42 汇款报告（remittance report）

定义：包含关于本次交易的特定有限信息集的报告。

- 父类：**报告（Report）**

### 2.43 分层招募说明书草案（tranched draft prospectus）

定义：发行实体在营销发行前确定的分层 MBS 发行招募说明书草案。

- 父类：**初步招募说明书（PreliminaryProspectus）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **先于（precedes）** | — | — |

公理：

- **先于（precedes）**至少有一个取值，类型是**分档型抵押支持证券交易招募说明书（TranchedMBSDealProspectus）**。

### 2.44 分层 MBS 交易结算（tranched m b s deal settlement）

定义：分层 MBS 交易的结算。

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **分解为（decomposes into）** | 将整体分解为若干部分。 | 值域：分层 MBS 一级交易结算流程（tranched m b s primary deal transaction settlement process） |

公理：

- **分解为（decomposes into）**至少有一个取值，类型是**分层 MBS 一级交易结算流程（tranched m b s primary deal transaction settlement process）**。

### 2.45 分层 MBS 交易（tranched m b s deal transaction）

定义：据以向主要投资者发行 MBS 的交易。

- 父类：**金融一级市场交易（FinancialPrimaryMarketTransaction）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有交易对手（has counterparty）** | 标识合同的当事方，通常不是合同主当事方。 | 值域：主要投资者（primary investor） |
| **具有主当事方（has principal party）** | 标识合同的主要或主当事方。 | 值域：非机构抵押支持证券发行人 |
| **遵循（follows）** | — | — |

公理：

- **具有交易对手（has counterparty）**至少有一个取值，类型是**主要投资者（primary investor）**。
- **遵循（follows）**至少有一个取值，类型是**分层 MBS 一级交易结算流程（tranched m b s primary deal transaction settlement process）**。

### 2.46 分层 MBS 发行招募说明书部分（tranched m b s issue prospectus part）

定义：分层 MBS 发行招募说明书的一个部分或章节。

- 父类：**招募说明书部分（ProspectusPart）**
- 直接子类：**各分层定义（individual tranche definitions）**、**分层票据参数（tranche notes parameters）**、**分层结构与条款清单（tranche structure and termsheet）**

#### 2.46.1 各分层定义（individual tranche definitions）

定义：标识分层发行中单个分层之条款的信息类别（实际为一份条款清单中针对各分层的条款信息集）。

- 父类：**分层 MBS 发行招募说明书部分（tranched m b s issue prospectus part）**、**条款清单（TermSheet）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有合同要素（hasContractualElement）** | — | — |

公理：

- **具有合同要素（hasContractualElement）**至少有一个取值，类型是**债券摊销支付条款（BondAmortizationPaymentTerms）**。
- **具有合同要素（hasContractualElement）**至少有一个取值，类型是**票息支付条款（CouponPaymentTerms）**。

#### 2.46.2 分层票据参数（tranche notes parameters）

定义：定义某一分层票据细分（面额及该分层中可购金额）的一组信息。

- 父类：**分层 MBS 发行招募说明书部分（tranched m b s issue prospectus part）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **面额增量（denomination increment）** | 票据面额的增量。 | 值域：货币数量 |
| **最大金额（maximum amount）** | 允许的最大金额。 | 值域：货币数量 |
| **最小面额（minimum denomination）** | 允许的最小面额。 | 值域：货币数量 |
| **关于（isAbout）** | — | — |

公理：

- **关于（isAbout）**至少有一个取值，类型是**抵押支持证券分档票据（MBSTrancheNote）**。
- **最大金额（maximum amount）**至多有 1 个**货币数量（MonetaryAmount）**。

#### 2.46.3 分层结构与条款清单（tranche structure and termsheet）

定义：定义 MBS 结构的一份清单。

- 父类：**分层 MBS 发行招募说明书部分（tranched m b s issue prospectus part）**

### 2.47 分层 MBS 一级交易结算流程（tranched m b s primary deal transaction settlement process）

定义：一级交易完成结算的过程。

- 父类：**结算过程（SettlementProcess）**

### 2.48 分层 MBS 招募说明书大纲（tranched m b s prospectus outline）

定义：分层招募说明书的大纲，提供可能分层及其特征的初步表示。

- 父类：**初步招募说明书（PreliminaryProspectus）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有内容（has content）** | 标识某事物所包含的内容。 | 值域：起草分层结构（draft tranche structure）；子属性：具有部分 |
| **具有内容（has content）** | 标识某事物所包含的内容。 | 值域：起草分层条款清单（draft tranche termsheet）；子属性：具有部分 |

公理：

- **具有内容（has content）**至少有一个取值，类型是**起草分层条款清单（draft tranche termsheet）**。

### 2.49 分层 MBS 证券化流程（tranched m b s securitization process）

定义：分层抵押贷款支持证券的证券化过程。

- 父类：**MBS 证券化流程（MBSSecuritizationProcess）**

### 2.50 分层发行备忘录（tranched offering memorandum）

定义：发行备忘录，包含或附上构成本次发行的两个或多个分层的条款及分层结构。

- 父类：**发行文件（OfferingDocument）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **包含……的细节（includes details about）** | 标识某文件所包含细节所关涉的对象。 | 值域：分层结构与条款清单（tranche structure and termsheet） |
| **包含……的细节（includes details about）** | 标识某文件所包含细节所关涉的对象。 | 值域：各分层定义（individual tranche definitions） |
| **可能包含……的细节（may include details about）** | 标识某文件可能包含细节所关涉的对象。 | 值域：起草分层票据参数（draft tranche notes parameters） |

公理：

- **包含……的细节（includes details about）**至少有一个取值，类型是**分层结构与条款清单（tranche structure and termsheet）**。
- **包含……的细节（includes details about）**至少有一个取值，类型是**各分层定义（individual tranche definitions）**。
- **可能包含……的细节（may include details about）**至多有 1 个**起草分层票据参数（draft tranche notes parameters）**。

## 3. 其他属性

以下属性未绑定到本体的具体类（定义域在外部本体或未声明）：

对象属性（Object Property）：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有主要持有人（has primary holder）** | 标识某事物的主要持有人。 | 值域：主要投资者（primary investor） |
| **具有受托人（has trustee）** | 将信托关联到具名受托人。 | 值域：池受托人（pool trustee） |
| **标识符由……签发（identifier issued by）** | 标识签发该标识符的机构。 | 值域：主标识符签发方 |

## 4. 依赖（owl:imports，26 个）

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

## 5. 文件

- 官方 RDF/XML：`PrivateLabelMBSIssuance.rdf`
- 中文 Turtle：`PrivateLabelMBSIssuance.ttl`
- 结构图：`PrivateLabelMBSIssuance-structure.png` / `PrivateLabelMBSIssuance-structure.svg`