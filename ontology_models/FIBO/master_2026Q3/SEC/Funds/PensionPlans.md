# 养老金计划本体（Pension Plans Ontology）结构与公理说明

本文档对应 `PensionPlans.rdf` / `PensionPlans.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `PensionPlans-structure.png`（`PensionPlans-structure.svg` 为可缩放版本）。

![养老金计划本体（Pension Plans Ontology）本体结构图](PensionPlans-structure.png)

## 1. 本体概述

定义养老金计划（pension plan）：确定缴费型（DC）与确定给付型（DB）等形态，及其发起人、受托管理与受益规则。

**在体系中的位置**：SEC 基金模块的品种本体之一。

**上下游关系**：上游继承集合投资工具并依赖 BE 雇主雇员概念；下游服务养老金资产管理建模。

**与相近概念的差别**：DC 与 DB 的差别——DC 型（如 401(k)）缴费确定、收益不确定，风险在个人；DB 型承诺确定给付，风险在雇主；与普通基金的差别——养老金有税收优惠与领取限制。

本本体中类与类的核心关系如下（完整细节见各类小节）：

- **账面储备养老金计划（book reserved pension plan）** 继承 **养老金计划（pension plan）**
- **封闭型养老基金（closed pension fund）** 继承 **养老基金（PensionFund）**
- **待遇确定型职业养老金计划（defined benefit occupational pension plan）** 继承 **职业养老金计划（occupational pension plan）**
- **待遇确定型职业养老金计划分类器（defined benefit occupational pension plan classifier）** 继承 **分类符（Classifier）**
- **缴费确定型职业养老金计划（defined contribution occupational pension plan）** 继承 **职业养老金计划（occupational pension plan）**
- **基金制养老金计划（funded pension plan）** 继承 **养老金计划（pension plan）**
- **个人养老金账户（individual pension account）** 继承 **个人退休账户（individual retirement account）**
- **个人养老金账户（individual pension account）** 继承 **养老金账户（pension account）**
- **个人养老基金（individual pension fund）** 继承 **封闭型养老基金（closed pension fund）**
- **个人退休账户（individual retirement account）** 继承 **退休账户（retirement account）**
- **强制性职业养老金计划（mandatory occupational pension plan）** 继承 **职业养老金计划（occupational pension plan）**
- **强制性个人养老金计划（mandatory personal pension plan）** 继承 **个人养老金计划（personal pension plan）**
- 其余 19 条关系从略。

## 2. 类（Class）

| 类（Class） | 定义（Definition） |
|---|---|
| 账面储备养老金计划（book reserved pension plan） | 资产负债表反映计划发起人资产负债表中以储备或拨备形式入账之职业养老金计划金额的养老金计划。<br>pension plan whose balance sheet reflects sums entered in the balance sheet of the plan sponsor as reserves or provisions for occupational pension plan benefits |
| 封闭型养老基金（closed pension fund） | 成员资格限于特定人士或特定类别人士的养老基金。<br>pension fund whose membership is restricted to specified persons or categories of persons |
| 待遇确定型职业养老金计划（defined benefit occupational pension plan） | 按预定待遇公式预先确定退休待遇的职业养老金计划，由发起雇主承担给付责任。<br>occupational pension plan that provides retirement benefits determined in advance according to a prescribed benefit formula, with the sponsoring employer or plan sponsor bearing the primary responsibility for financing any shortfall required to provide the promised benefits |
| 待遇确定型职业养老金计划分类器（defined benefit occupational pension plan classifier） | 对按预定待遇公式预先确定退休待遇、并由发起雇主承担义务的职业计划进行分类的分类器。<br>classifier for occupational plans that provide retirement benefits determined in advance according to a prescribed benefit formula, and whose sponsoring employer or plan sponsor bears the primary responsibility for financing any shortfall required to provide the promised benefits |
| 缴费确定型职业养老金计划（defined contribution occupational pension plan） | 计划发起人支付固定缴费、且无法定或推定义务支付额外缴费的职业养老金计划。<br>occupational pension plan under which the plan sponsor pays fixed contributions and has no legal or constructive obligation to pay further contributions to an ongoing plan in the event of unfavourable plan experience |
| 基金制养老金计划（funded pension plan） | 积累专门资产以覆盖计划负债的养老金计划。<br>pension plan that accumulates dedicated assets to cover the plan's liabilities |
| 个人养老金账户（individual pension account） | 记录归属于个人之金额的养老金账户。<br>pension account in which amounts attributable to an individual are recorded |
| 个人养老基金（individual pension fund） | 支持一个或多个个人养老金计划、并按成员个人为基础维持资产和权益的封闭型养老基金。<br>closed pension fund that supports one or more individual pension plans and in which assets and entitlements are maintained on an individual-member basis |
| 个人退休账户（individual retirement account） | 记录归属于个人之金额的退休账户（IRA）。<br>retirement account in which amounts attributable to an individual are recorded |
| 强制性职业养老金计划（mandatory occupational pension plan） | 雇主必须参加的职业养老金计划。<br>occupational pension plan for which participation is mandatory for employers |
| 强制性个人养老金计划（mandatory personal pension plan） | 个人必须加入、或可接收强制性养老金缴费的个人养老金计划。<br>personal pension plan that individuals must join or that are eligible to receive mandatory pension contributions |
| 多雇主养老基金（multi-employer pension fund） | 汇集多个计划发起人所设养老金计划资产的养老基金。<br>pension fund that pools the assets of pension plans established by various plan sponsors |
| 职业养老金计划（occupational pension plan） | 与计划成员和设立计划的实体（计划发起人）之间雇佣或职业关系相关联的养老金计划。<br>pension plan linked to an employment or professional relationship between the plan member and the entity that establishes the plan (the plan sponsor) |
| 开放型养老基金（open pension fund） | 支持至少一个成员资格不受限制之计划的养老基金。<br>pension fund that supports at least one plan with no restriction on membership |
| 养老金账户（pension account） | 记录与养老金计划相关之金额的退休账户。<br>retirement account in which amounts associated with a pension plan are recorded |
| 养老金保险合同（pension insurance contract） | 规定养老金计划向保险企业缴费、以换取由保险企业支付养老金计划待遇的保险合同。<br>insurance contract that specifies pension plan contributions to an insurance undertaking in exchange for which the pension plan benefits will be paid when the members reach a specified retirement age or on earlier exit of members from the plan |
| 养老金计划（pension plan） | 具有明确退休目标的具有法律约束力的安排，或为满足税收相关条件或合同条款而设定受益安排的安排。<br>legally binding arrangement having an explicit retirement objective or - in order to satisfy tax related conditions or contract provisions - the benefits can not be paid at all or without a significant penalty unless the beneficiary is older than a legally defined retirement age |
| 个人养老金计划（personal pension plan） | 无须与雇佣或职业关系相关联的养老金计划。<br>pension plan that does not need to be linked to an employment or professional relationship |
| 私营养老基金（private pension fund） | 受私营部门法律监管的养老基金。<br>pension fund that is regulated under private sector law |
| 私营养老金计划（private pension plan） | 由一般政府以外机构管理的养老金计划。<br>pension plan administered by an institution other than general government |
| 公共养老基金（public pension fund） | 受公共部门法律监管的养老基金。<br>pension fund that is regulated under public sector law |
| 公共养老金计划（public pension plan） | 由一般政府（即中央、州和地方政府以及社会保障机构等其他公共部门机构）管理的养老金计划。<br>pension plan administered by the general government (that is central, state, and local governments, as well as other public sector bodies such as social security institutions) |
| 关联成员养老基金（related member pension fund） | 由数量有限的关联成员资产组成、且成员均为该养老基金管理机构成员的养老基金。<br>pension fund that comprises the assets of a limited number of related members who are all in the governing body of the pension fund |
| 退休账户（retirement account） | 记录旨在为退休期间提供收入或财务资源之金额的账户。<br>account in which amounts intended to provide income or financial resources during retirement are recorded |
| 退休安排（retirement arrangement） | 确立为退休积累或提供财务资源之条件的安排。<br>arrangement that establishes conditions for the accumulation or provision of financial resources for retirement |
| 单一雇主养老基金（single employer pension fund） | 汇集单一发起人所设养老金计划资产的养老基金。<br>pension fund that pools the assets of pension plans established by a single sponsor |
| 现收现付养老金计划（unfunded pension plan） | 直接以计划发起人或提供方和/或计划参与人的缴费支付的养老金计划。<br>pension plan that is financed directly from contributions from the plan sponsor or provider and/or the plan participant |
| 自愿性职业养老金计划（voluntary occupational pension plan） | 雇主自愿设立的职业养老金计划（包括作为雇佣安排一部分自动加入的情形）。<br>occupational pension plan for which establishment is voluntary for employers (including those in which there is automatic enrollment as part of an employment contract or where the law requires employees to join plans set up on a voluntary basis by their employers) |
| 自愿性个人养老金计划（voluntary personal pension plan） | 个人自愿参加的个人养老金计划。<br>personal pension plan in which participation is voluntary for individuals |

以下按类逐个展开：每个类给出继承关系、相关属性与公理约定；子类在父类之下降一级编号。

### 2.1 封闭型养老基金（closed pension fund）

定义：成员资格限于特定人士或特定类别人士的养老基金。

- 父类：**养老基金（PensionFund）**
- 直接子类：**个人养老基金（individual pension fund）**、**多雇主养老基金（multi-employer pension fund）**、**关联成员养老基金（related member pension fund）**、**单一雇主养老基金（single employer pension fund）**

#### 2.1.1 个人养老基金（individual pension fund）

定义：支持一个或多个个人养老金计划、并按成员个人为基础维持资产和权益的封闭型养老基金。

- 父类：**封闭型养老基金（closed pension fund）**

公理：

- 与**单一雇主养老基金（single employer pension fund）**互斥：同一个体不能同时属于两者。

#### 2.1.2 多雇主养老基金（multi-employer pension fund）

定义：汇集多个计划发起人所设养老金计划资产的养老基金。

- 父类：**封闭型养老基金（closed pension fund）**

公理：

- 与**个人养老基金（individual pension fund）**互斥：同一个体不能同时属于两者。
- 与**关联成员养老基金（related member pension fund）**互斥：同一个体不能同时属于两者。
- 与**单一雇主养老基金（single employer pension fund）**互斥：同一个体不能同时属于两者。

#### 2.1.3 关联成员养老基金（related member pension fund）

定义：由数量有限的关联成员资产组成、且成员均为该养老基金管理机构成员的养老基金。

- 父类：**封闭型养老基金（closed pension fund）**

公理：

- 与**个人养老基金（individual pension fund）**互斥：同一个体不能同时属于两者。
- 与**单一雇主养老基金（single employer pension fund）**互斥：同一个体不能同时属于两者。

#### 2.1.4 单一雇主养老基金（single employer pension fund）

定义：汇集单一发起人所设养老金计划资产的养老基金。

- 父类：**封闭型养老基金（closed pension fund）**

### 2.2 待遇确定型职业养老金计划分类器（defined benefit occupational pension plan classifier）

定义：对按预定待遇公式预先确定退休待遇、并由发起雇主承担义务的职业计划进行分类的分类器。

- 父类：**分类符（Classifier）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **分类（classifies）** | — | — |

公理：

- **分类（classifies）**至少有一个取值，类型是**待遇确定型职业养老金计划（defined benefit occupational pension plan）**。

### 2.3 开放型养老基金（open pension fund）

定义：支持至少一个成员资格不受限制之计划的养老基金。

- 父类：**养老基金（PensionFund）**

公理：

- 与**封闭型养老基金（closed pension fund）**互斥：同一个体不能同时属于两者。

### 2.4 养老金保险合同（pension insurance contract）

定义：规定养老金计划向保险企业缴费、以换取由保险企业支付养老金计划待遇的保险合同。

- 父类：**保险单（InsurancePolicy）**

### 2.5 私营养老基金（private pension fund）

定义：受私营部门法律监管的养老基金。

- 父类：**养老基金（PensionFund）**

公理：

- 与**公共养老基金（public pension fund）**互斥：同一个体不能同时属于两者。

### 2.6 公共养老基金（public pension fund）

定义：受公共部门法律监管的养老基金。

- 父类：**养老基金（PensionFund）**

### 2.7 退休账户（retirement account）

定义：记录旨在为退休期间提供收入或财务资源之金额的账户。

- 父类：**投资账户（InvestmentAccount）**
- 直接子类：**个人退休账户（individual retirement account）**、**养老金账户（pension account）**

#### 2.7.1 个人退休账户（individual retirement account）

定义：记录归属于个人之金额的退休账户（IRA）。

- 父类：**退休账户（retirement account）**
- 直接子类：**个人养老金账户（individual pension account）**

##### 2.7.1.1 个人养老金账户（individual pension account）

定义：记录归属于个人之金额的养老金账户。

- 父类：**个人退休账户（individual retirement account）**、**养老金账户（pension account）**

#### 2.7.2 养老金账户（pension account）

定义：记录与养老金计划相关之金额的退休账户。

- 父类：**退休账户（retirement account）**
- 直接子类：**个人养老金账户（individual pension account）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **规定于（isSpecifiedIn）** | — | — |

公理：

- **规定于（isSpecifiedIn）**至少有一个取值，类型是**养老金计划（pension plan）**。

### 2.8 退休安排（retirement arrangement）

定义：确立为退休积累或提供财务资源之条件的安排。

- 父类：**协议（Agreement）**
- 直接子类：**养老金计划（pension plan）**

#### 2.8.1 养老金计划（pension plan）

定义：具有明确退休目标的具有法律约束力的安排，或为满足税收相关条件或合同条款而设定受益安排的安排。

- 父类：**协议（Agreement）**、**退休安排（retirement arrangement）**
- 直接子类：**账面储备养老金计划（book reserved pension plan）**、**基金制养老金计划（funded pension plan）**、**职业养老金计划（occupational pension plan）**、**个人养老金计划（personal pension plan）**、**私营养老金计划（private pension plan）**、**公共养老金计划（public pension plan）**、**现收现付养老金计划（unfunded pension plan）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由……提供资金（is funded by）** | 将计划或基金与为其提供资金的协议或其他资金安排关联起来。<br>links a plan or fund to an agreement or other funding arrangement that funds it | 逆属性：为……提供资金（provides funding for）；子属性：由……提供 |
| **是否无保障（is unprotected）** | 若为真，表明养老金计划/基金本身或养老金提供方不提供任何投资回报或待遇保证。<br>indicates, if true, that the pension plan/fund itself or the pension provider does not offer any investment return or benefit guarantees or promises covering the whole plan/fund | 值域：xsd:boolean |
| **规定（specifies）** | — | — |

公理：

- **是否无保障（is unprotected）**存在取值约束。
- **由……提供资金（is funded by）**可以有 0 个或多个**Nabe0d3760c5b43c8a875bec007e97586**。
- **规定（specifies）**可以有 0 个或多个**养老金账户（pension account）**。

##### 2.8.1.1 账面储备养老金计划（book reserved pension plan）

定义：资产负债表反映计划发起人资产负债表中以储备或拨备形式入账之职业养老金计划金额的养老金计划。

- 父类：**养老金计划（pension plan）**

公理：

- 与**基金制养老金计划（funded pension plan）**互斥：同一个体不能同时属于两者。
- 与**现收现付养老金计划（unfunded pension plan）**互斥：同一个体不能同时属于两者。

##### 2.8.1.2 基金制养老金计划（funded pension plan）

定义：积累专门资产以覆盖计划负债的养老金计划。

- 父类：**养老金计划（pension plan）**

公理：

- 与**现收现付养老金计划（unfunded pension plan）**互斥：同一个体不能同时属于两者。

##### 2.8.1.3 职业养老金计划（occupational pension plan）

定义：与计划成员和设立计划的实体（计划发起人）之间雇佣或职业关系相关联的养老金计划。

- 父类：**养老金计划（pension plan）**
- 直接子类：**待遇确定型职业养老金计划（defined benefit occupational pension plan）**、**缴费确定型职业养老金计划（defined contribution occupational pension plan）**、**强制性职业养老金计划（mandatory occupational pension plan）**、**自愿性职业养老金计划（voluntary occupational pension plan）**

###### 2.8.1.3.1 待遇确定型职业养老金计划（defined benefit occupational pension plan）

定义：按预定待遇公式预先确定退休待遇的职业养老金计划，由发起雇主承担给付责任。

- 父类：**职业养老金计划（occupational pension plan）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由……分类（isClassifiedBy）** | — | — |

公理：

- **由……分类（isClassifiedBy）**至少有一个取值，类型是**待遇确定型职业养老金计划分类器（defined benefit occupational pension plan classifier）**。
- 与**缴费确定型职业养老金计划（defined contribution occupational pension plan）**互斥：同一个体不能同时属于两者。

###### 2.8.1.3.2 缴费确定型职业养老金计划（defined contribution occupational pension plan）

定义：计划发起人支付固定缴费、且无法定或推定义务支付额外缴费的职业养老金计划。

- 父类：**职业养老金计划（occupational pension plan）**

###### 2.8.1.3.3 强制性职业养老金计划（mandatory occupational pension plan）

定义：雇主必须参加的职业养老金计划。

- 父类：**职业养老金计划（occupational pension plan）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **是否强制（is mandatory）** | 表明某事物是否为必需。<br>indicates, if true, that something is required | 值域：xsd:boolean |

公理：

- **是否强制（is mandatory）**的取值固定为 true。

###### 2.8.1.3.4 自愿性职业养老金计划（voluntary occupational pension plan）

定义：雇主自愿设立的职业养老金计划（包括作为雇佣安排一部分自动加入的情形）。

- 父类：**职业养老金计划（occupational pension plan）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **是否强制（is mandatory）** | 表明某事物是否为必需。<br>indicates, if true, that something is required | 值域：xsd:boolean |

公理：

- **是否强制（is mandatory）**的取值固定为 false。
- 与**强制性职业养老金计划（mandatory occupational pension plan）**互斥：同一个体不能同时属于两者。

##### 2.8.1.4 个人养老金计划（personal pension plan）

定义：无须与雇佣或职业关系相关联的养老金计划。

- 父类：**养老金计划（pension plan）**
- 直接子类：**强制性个人养老金计划（mandatory personal pension plan）**、**自愿性个人养老金计划（voluntary personal pension plan）**

公理：

- 与**职业养老金计划（occupational pension plan）**互斥：同一个体不能同时属于两者。

###### 2.8.1.4.1 强制性个人养老金计划（mandatory personal pension plan）

定义：个人必须加入、或可接收强制性养老金缴费的个人养老金计划。

- 父类：**个人养老金计划（personal pension plan）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **是否强制（is mandatory）** | 表明某事物是否为必需。<br>indicates, if true, that something is required | 值域：xsd:boolean |

公理：

- **是否强制（is mandatory）**的取值固定为 true。

###### 2.8.1.4.2 自愿性个人养老金计划（voluntary personal pension plan）

定义：个人自愿参加的个人养老金计划。

- 父类：**个人养老金计划（personal pension plan）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **是否强制（is mandatory）** | 表明某事物是否为必需。<br>indicates, if true, that something is required | 值域：xsd:boolean |

公理：

- **是否强制（is mandatory）**的取值固定为 false。
- 与**强制性个人养老金计划（mandatory personal pension plan）**互斥：同一个体不能同时属于两者。

##### 2.8.1.5 私营养老金计划（private pension plan）

定义：由一般政府以外机构管理的养老金计划。

- 父类：**养老金计划（pension plan）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **是否强制（is mandatory）** | 表明某事物是否为必需。<br>indicates, if true, that something is required | 值域：xsd:boolean |

公理：

- **是否强制（is mandatory）**存在取值约束。
- 与**公共养老金计划（public pension plan）**互斥：同一个体不能同时属于两者。

##### 2.8.1.6 公共养老金计划（public pension plan）

定义：由一般政府（即中央、州和地方政府以及社会保障机构等其他公共部门机构）管理的养老金计划。

- 父类：**养老金计划（pension plan）**

##### 2.8.1.7 现收现付养老金计划（unfunded pension plan）

定义：直接以计划发起人或提供方和/或计划参与人的缴费支付的养老金计划。

- 父类：**养老金计划（pension plan）**

## 3. 其他属性

以下属性未绑定到本体的具体类（定义域在外部本体或未声明）：

对象属性（Object Property）：

| 属性 | 定义 | 说明 |
|---|---|---|
| **为……提供资金（provides funding for）** | 将协议或资金安排与其所资助的事物关联起来。<br>relates an agreement or funding arrangement to something that funds it | 逆属性：由……提供资金（is funded by）；子属性：提供 |

## 4. 依赖（owl:imports，12 个）

本本体通过 `owl:imports` 引入以下本体，各项的中文名称与简介如下：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `FBC/DebtAndEquities/Guaranty.rdf` | 担保本体（Guaranty Ontology） | 定义担保（guaranty）：担保人、被担保债务与担保范围。 |
| `FBC/ProductsAndServices/ClientsAndAccounts.rdf` | 客户与账户本体（Clients and Accounts Ontology） | 定义金融机构的客户、账户及账户持有关系。 |
| `FND/Agreements/Agreements.rdf` | 协议本体（Agreements Ontology） | 定义两个或以上参与方之间协议（agreement）的通用概念：协议的当事方、条款、生效与终止，是合同等一切契约性安排的上位模型。 |
| `FND/Agreements/Contracts.rdf` | 合同本体（Contracts Ontology） | 在协议之上定义具有法律约束力的合同（contract）：合同当事方、合同条款、义务与权利，是金融工具与交易合同建模的基石。 |
| `FND/GoalsAndObjectives/Objectives.rdf` | 目标本体（Objectives Ontology） | 定义目标（objective）及其与组织、计划的关系，用于表达机构的经营目标与投资目标。 |
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `SEC/Funds/Funds.rdf` | 基金本体（Funds Ontology） | 定义投资基金（fund）：基金份额、净值与管理结构。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |
| `https://www.omg.org/spec/Commons/Classifiers/` | OMG 通用分类器本体（OMG Commons Classifiers） | OMG 通用本体库（Commons）中的分类器本体，定义分类方案、类别与归类关系的通用概念，FIBO 的分类建模建立在其上。 |
| `https://www.omg.org/spec/Commons/Designators/` | OMG 通用指称符本体（OMG Commons Designators） | Commons 库中的指称符本体，定义名称、标识符等「指代某物的符号」的通用概念。 |
| `https://www.omg.org/spec/Commons/Documents/` | OMG 通用文档本体（OMG Commons Documents） | Commons 库中的文档本体，定义文档及其组成部分的通用概念。 |
| `https://www.omg.org/spec/Commons/Organizations/` | OMG 通用组织本体（OMG Commons Organizations） | Commons 库中的组织本体，定义组织、组织成员与组织结构的通用概念。 |

## 5. 文件

- 官方 RDF/XML：`PensionPlans.rdf`
- 中文 Turtle：`PensionPlans.ttl`
- 结构图：`PensionPlans-structure.png` / `PensionPlans-structure.svg`