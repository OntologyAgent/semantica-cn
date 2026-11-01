# 产品与服务本体（Products and Services Ontology）结构与公理说明

本文档对应 `ProductsAndServices.rdf` / `ProductsAndServices.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `ProductsAndServices-structure.png`（`ProductsAndServices-structure.svg` 为可缩放版本）。

![产品与服务本体（Products and Services Ontology）本体结构图](ProductsAndServices-structure.png)

## 1. 本体概述

定义产品（product）与服务（service）的通用概念：提供方、客户、产品特征与服务协议。

**在体系中的位置**：FND 产品与服务模块的基础本体，是 FBC 金融产品与服务的直接上游。

**上下游关系**：上游依赖参与方与协议本体；下游被 FBC 金融产品与服务本体特化到金融领域。

**与相近概念的差别**：产品≠服务——产品是可交付的标的（可以是一项安排），服务是持续提供的行为；本本体是领域无关的，金融特性在 FBC 层加入。

本本体中类与类的核心关系如下（完整细节见各类小节）：

- **买方（buyer）** 继承 **参与方角色（party role）**
- **客户（client）** 继承 **参与方角色（party role）**
- **客户标识符（client identifier）** 继承 **参与方角色标识符（PartyRoleIdentifier）**
- **商品（commodity）** 继承 **货物（good）**
- **消费者（consumer）** 继承 **参与方角色（party role）**
- **合同型产品（contractual product）** 继承 **产品（product）**
- **合同模板型产品（contractual template product）** 继承 **合同型产品（contractual product）**
- **合同模板型产品（contractual template product）** 继承 **现货产品（off-the-shelf product）**
- **定制产品（custom product）** 继承 **产品（product）**
- **顾客（customer）** 继承 **买方（buyer）**
- **顾客标识符（customer identifier）** 继承 **参与方角色标识符（PartyRoleIdentifier）**
- **可流通商品（negotiable commodity）** 继承 **商品（commodity）**
- 其余 16 条关系从略。

## 2. 类（Class）

| 类（Class） | 定义（Definition） |
|---|---|
| 买方（buyer） | 依销售合同以货币或其他对价购买某物的参与方。 |
| 客户（client） | 向另一参与方购买专业服务、或与其存在购买服务之正式关系的参与方。 |
| 客户标识符（client identifier） | 在某组织情境内唯一标识客户的字符序列。 |
| 商品（commodity） | 商业中使用的、可与同类型其他商品互换的物质资源。 |
| 消费者（consumer） | 使用经济货物或服务的参与方，通常用于个人、家庭或住户目的。 |
| 合同型产品（contractual product） | 以协议形式存在的产品。 |
| 合同模板型产品（contractual template product） | 通过为模板中定义的参数指定取值而定稿的合同型产品。 |
| 定制产品（custom product） | 按订单生产、依客户规格委托制作的产品。 |
| 顾客（customer） | 接收或消费产品（货物或服务）、并能在不同产品和供应商之间选择的参与方。 |
| 顾客标识符（customer identifier） | 在某组织情境内唯一标识顾客的字符序列。 |
| 货物（good） | 可确立所有权、且其所有权可通过交易在参与方之间转移的有形生产物品。 |
| 可流通商品（negotiable commodity） | 可在某市场买入或卖出的商品。 |
| 现货产品（off-the-shelf product） | 可直接从库存现货获得、或可快速按订单配置的产品，非专门设计或定制。 |
| 生产者（producer） | 某种产品或其他货物的种植者、制造者、加工者或生产商。 |
| 产品（product） | 商业化分销的货物：(1) 有形财产，(2) 加工、制造或生产过程的产出或结果，或 (3) 服务。 |
| 产品标识符（product identifier） | 在某情境中唯一标识产品的字符序列。 |
| 销售（sale） | 以货物或服务换取货币的交换。 |
| 卖方（seller） | 向实际或潜在买方作出、要约或订立销售合同的参与方。 |
| 服务协议（service agreement） | 客户与服务提供方之间的书面合同，服务提供方据此以时间、劳务和/或专业知识的形式提供某项服务。 |
| 供应商（supplier） | 提供某参与方所需货物或服务的参与方，尤指长期供应者。 |
| 交易确认书（transaction confirmation） | 卖方或服务提供方出具的、复述交易相关细节的书面通信。 |
| 交易事件（transaction event） | 交易的事件成分。 |

以下按类逐个展开：每个类给出继承关系、相关属性与公理约定；子类在父类之下降一级编号。

### 2.1 买方（buyer）

定义：依销售合同以货币或其他对价购买某物的参与方。

- 父类：**参与方角色（party role）**
- 直接子类：**顾客（customer）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **购买（buys）** | 将处于购买者角色的参与方关联到其已购买或计划购买的事物。 | 值域：产品（product） |
| **从……购买（buys from）** | 将处于购买者角色的参与方关联到其已购买或计划购买的对方参与方。 | 值域：卖方（seller）；子属性：受…影响（is affected by） |

公理：

- **购买（buys）**至少有一个取值，类型是**产品（product）**。

#### 2.1.1 顾客（customer）

定义：接收或消费产品（货物或服务）、并能在不同产品和供应商之间选择的参与方。

- 父类：**买方（buyer）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **从……购买（buys from）** | 将处于购买者角色的参与方关联到其已购买或计划购买的对方参与方。 | 值域：卖方（seller）；子属性：受…影响（is affected by） |

公理：

- **从……购买（buys from）**至少有一个取值，类型是**供应商（supplier）**。

### 2.2 客户（client）

定义：向另一参与方购买专业服务、或与其存在购买服务之正式关系的参与方。

- 父类：**参与方角色（party role）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由…扮演（is played by）** | — | — |

公理：

- **由…扮演（is played by）**至少有一个取值，该取值满足：**是…的参与方（is a party to）**至少有一个取值，类型是**服务协议（service agreement）**。

### 2.3 客户标识符（client identifier）

定义：在某组织情境内唯一标识客户的字符序列。

- 父类：**参与方角色标识符（PartyRoleIdentifier）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **标识（identifies）** | — | — |

公理：

- **标识（identifies）**恰好有 1 个**客户（client）**。

### 2.4 消费者（consumer）

定义：使用经济货物或服务的参与方，通常用于个人、家庭或住户目的。

- 父类：**参与方角色（party role）**

### 2.5 顾客标识符（customer identifier）

定义：在某组织情境内唯一标识顾客的字符序列。

- 父类：**参与方角色标识符（PartyRoleIdentifier）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **标识（identifies）** | — | — |

公理：

- **标识（identifies）**恰好有 1 个**顾客（customer）**。

### 2.6 货物（good）

定义：可确立所有权、且其所有权可通过交易在参与方之间转移的有形生产物品。

- 直接子类：**商品（commodity）**

公理：

- 与**货币金额（AmountOfMoney）**互斥：同一个体不能同时属于两者。
- 与**房地产（RealEstate）**互斥：同一个体不能同时属于两者。

#### 2.6.1 商品（commodity）

定义：商业中使用的、可与同类型其他商品互换的物质资源。

- 父类：**货物（good）**
- 直接子类：**可流通商品（negotiable commodity）**

##### 2.6.1.1 可流通商品（negotiable commodity）

定义：可在某市场买入或卖出的商品。

- 父类：**商品（commodity）**

### 2.7 生产者（producer）

定义：某种产品或其他货物的种植者、制造者、加工者或生产商。

- 父类：**参与方角色（party role）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **生产（produces）** | — | — |

公理：

- **生产（produces）**至少有一个取值，类型是**货物（good）**。

### 2.8 产品（product）

定义：商业化分销的货物：(1) 有形财产，(2) 加工、制造或生产过程的产出或结果，或 (3) 服务。

- 直接子类：**合同型产品（contractual product）**、**定制产品（custom product）**、**现货产品（off-the-shelf product）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由……供应（is supplied by）** | 标识使产品可获得的参与方（供应商、卖方、分销商等）。 | 值域：供应商（supplier）；逆属性：供应（supplies）；子属性：由……提供 |

公理：

- 该属性存在取值约束。

#### 2.8.1 合同型产品（contractual product）

定义：以协议形式存在的产品。

- 父类：**产品（product）**
- 直接子类：**合同模板型产品（contractual template product）**

##### 2.8.1.1 合同模板型产品（contractual template product）

定义：通过为模板中定义的参数指定取值而定稿的合同型产品。

- 父类：**合同型产品（contractual product）**、**现货产品（off-the-shelf product）**

#### 2.8.2 定制产品（custom product）

定义：按订单生产、依客户规格委托制作的产品。

- 父类：**产品（product）**

公理：

- 与**现货产品（off-the-shelf product）**互斥：同一个体不能同时属于两者。

#### 2.8.3 现货产品（off-the-shelf product）

定义：可直接从库存现货获得、或可快速按订单配置的产品，非专门设计或定制。

- 父类：**产品（product）**
- 直接子类：**合同模板型产品（contractual template product）**

### 2.9 产品标识符（product identifier）

定义：在某情境中唯一标识产品的字符序列。

- 父类：**标识符（Identifier）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **标识（identifies）** | — | — |

公理：

- **标识（identifies）**恰好有 1 个**产品（product）**。

### 2.10 卖方（seller）

定义：向实际或潜在买方作出、要约或订立销售合同的参与方。

- 父类：**参与方角色（party role）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **销售（sells）** | 将处于经纪人、交易商、卖方或经销商角色的参与方关联到其提供出售的事物。 | 值域：产品（product） |
| **销售给（sells to）** | 将处于经纪人、交易商、卖方或经销商角色的参与方关联到买方或潜在买方。 | 值域：买方（buyer）；逆属性：从……购买（buys from）；子属性：对…采取行动（acts on） |

公理：

- **销售（sells）**至少有一个取值，类型是**产品（product）**。

### 2.11 服务协议（service agreement）

定义：客户与服务提供方之间的书面合同，服务提供方据此以时间、劳务和/或专业知识的形式提供某项服务。

- 父类：**书面合同（WrittenContract）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有合同当事方（hasContractParty）** | — | — |
| **管辖（governs）** | — | — |

公理：

- **具有合同当事方（hasContractParty）**恰好有 1 个**服务提供方（ServiceProvider）**。
- **管辖（governs）**至少有一个取值，类型是**服务（Service）**。

### 2.12 供应商（supplier）

定义：提供某参与方所需货物或服务的参与方，尤指长期供应者。

- 父类：**参与方角色（party role）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **供应（supplies）** | 将处于装备商、供应商、分销商等角色的参与方关联到其提供的事物。 | 值域：产品（product）；子属性：提供 |

公理：

- **供应（supplies）**至少有一个取值，类型是**产品（product）**。

### 2.13 交易确认书（transaction confirmation）

定义：卖方或服务提供方出具的、复述交易相关细节的书面通信。

- 父类：**法律文件（LegalDocument）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **是……的证据（isEvidenceFor）** | — | — |

公理：

- **是……的证据（isEvidenceFor）**恰好有 1 个**交易事件（transaction event）**。

### 2.14 交易事件（transaction event）

定义：交易的事件成分。

- 父类：**发生类别（OccurrenceKind）**
- 直接子类：**销售（sale）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由……证明（isEvidencedBy）** | — | — |

公理：

- **由……证明（isEvidencedBy）**可以有 0 个或多个**交易确认书（transaction confirmation）**。

#### 2.14.1 销售（sale）

定义：以货物或服务换取货币的交换。

- 父类：**交易事件（transaction event）**、**情境（situation）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有价格（hasPrice）** | — | — |
| **具有买方（has buyer）** | 标识销售交易情境中的购买方。 | 值域：买方（buyer）；子属性：具有参与方角色（has party role） |
| **具有卖方（has seller）** | 标识销售交易情境中的卖方。 | 值域：卖方（seller）；子属性：具有行为者（has actor） |
| **适用于（appliesTo）** | — | — |

公理：

- **具有买方（has buyer）**至少有一个取值，类型是**买方（buyer）**。
- **具有价格（hasPrice）**至少有一个取值，类型是**货币数量（MonetaryAmount）**。
- **具有卖方（has seller）**至少有一个取值，类型是**卖方（seller）**。
- **适用于（appliesTo）**至少有一个取值，类型是**产品（product）**。

## 3. 其他属性

以下属性未绑定到本体的具体类（定义域在外部本体或未声明）：

对象属性（Object Property）：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由……配置提供（is provisioned by）** | 标识配置提供服务或设施的服务提供方。 | 值域：服务提供方；逆属性：配置提供（provisions）；子属性：由……提供 |
| **配置提供（provisions）** | 定制、提供或装备交付服务所需的事物。 | 子属性：提供 |

## 4. 依赖（owl:imports，17 个）

本本体通过 `owl:imports` 引入以下本体，各项的中文名称与简介如下：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `FND/Accounting/CurrencyAmount.rdf` | 货币金额本体（Currency Amount Ontology） | 定义「金额＋币种」的货币金额（currency amount）表示，是 FIBO 中表达价格、债务金额、付款额等一切带币种数值的基础构件。 |
| `FND/Agreements/Contracts.rdf` | 合同本体（Contracts Ontology） | 在协议之上定义具有法律约束力的合同（contract）：合同当事方、合同条款、义务与权利，是金融工具与交易合同建模的基石。 |
| `FND/DatesAndTimes/Occurrences.rdf` | 事件与发生本体（Occurrences Ontology） | 定义「发生」（occurrence）、事件与触发条件，用于表达企业行动、信用事件等「发生了什么」。 |
| `FND/Law/LegalCapacity.rdf` | 法律能力本体（Legal Capacity Ontology） | 定义法律能力、缔约能力、签章权等概念，刻画主体从事法律行为的资格。 |
| `FND/Parties/Parties.rdf` | 参与方本体（Parties Ontology） | 定义参与方（party）、独立主体（autonomous agent）与「角色扮演」（party in role），是 FIBO 全库使用最广的基础本体之一。 |
| `FND/Places/RealProperty.rdf` | 不动产本体（Real Property Ontology） | 定义不动产（real property）及其与地点、所有权的关系，支撑抵押贷款与房地产金融。 |
| `FND/Relations/Relations.rdf` | 关系本体（Relations Ontology） | FIBO 最底层的基础本体，定义参考（reference）、分类（classify）等通用关系与抽象概念，全库普遍依赖。 |
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |
| `https://www.omg.org/spec/Commons/ContextualDesignators/` | OMG 通用语境指称本体（OMG Commons Contextual Designators） | Commons 库中的语境指称本体，定义「在某个语境下指代某物的名称/符号」，是地址、账户号码等语境相关标识的基础。 |
| `https://www.omg.org/spec/Commons/Documents/` | OMG 通用文档本体（OMG Commons Documents） | Commons 库中的文档本体，定义文档及其组成部分的通用概念。 |
| `https://www.omg.org/spec/Commons/Identifiers/` | OMG 通用标识符本体（OMG Commons Identifiers） | Commons 库中的标识符本体，定义标识符及其编码方案的通用概念。 |
| `https://www.omg.org/spec/Commons/Organizations/` | OMG 通用组织本体（OMG Commons Organizations） | Commons 库中的组织本体，定义组织、组织成员与组织结构的通用概念。 |
| `https://www.omg.org/spec/Commons/PartiesAndSituations/` | OMG 通用参与方与情境本体（OMG Commons Parties and Situations） | Commons 库中的参与方本体，定义独立主体、参与方及其角色扮演的通用概念，是 FIBO 参与方模型的上游。 |
| `https://www.omg.org/spec/Commons/RegulatoryAgencies/` | OMG 通用监管机构本体（OMG Commons Regulatory Agencies） | Commons 库中的监管机构本体，定义监管机构及其监管职权的通用概念。 |
| `https://www.omg.org/spec/Commons/RolesAndCompositions/` | OMG 通用角色与构成本体（OMG Commons Roles and Compositions） | Commons 库中的角色本体，定义角色及整体—部分构成关系的通用概念。 |
| `https://www.omg.org/spec/Commons/SitesAndFacilities/` | OMG 通用场所与设施本体（OMG Commons Sites and Facilities） | Commons 库中的场所与设施本体，定义物理场所、设施及其位置的通用概念。 |

## 5. 文件

- 官方 RDF/XML：`ProductsAndServices.rdf`
- 中文 Turtle：`ProductsAndServices.ttl`
- 结构图：`ProductsAndServices-structure.png` / `ProductsAndServices-structure.svg`