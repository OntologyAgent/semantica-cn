# 所有权方本体（Ownership Parties Ontology）结构与公理说明

本文档对应 `OwnershipParties.rdf` / `OwnershipParties.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `OwnershipParties-structure.png`（`OwnershipParties-structure.svg` 为可缩放版本）。

![所有权方本体（Ownership Parties Ontology）本体结构图](OwnershipParties-structure.png)

## 1. 本体概述

定义所有权关系中的各方角色：所有者、受益所有人、名义持有人等。

**在体系中的位置**：BE 所有权与控制权模块中「所有权」线索的角色层，与控制方本体平行。

**上下游关系**：上游依赖 FND 所有权与参与方本体；下游被公司所有权本体扩展。

**与相近概念的差别**：受益所有人与名义持有人的区分是核心——名义持有人只是登记在册，受益所有人才享有实际经济利益；这套区分直接服务反洗钱与透明度监管。

## 2. 类（Class）

| 类（Class） | 定义（Definition） |
|---|---|
| 章程性所有者（constitutional owner） | 以股东权益形式持有该实体股权的实体所有者。 |
| 控制性股权（controlling equity） | 依法或在相应股权工具中明示、正式赋予对实体之控制权的股东权益。 |
| 直接合并（direct consolidation） | 以会计合并方式记录的对实体的直接所有权。 |
| 实体所有者（entity owner） | 拥有正式企业组织或持有其所有权权益的所有者（个人、群体或其他企业实体）。 |
| 实体所有权（entity ownership） | 某参与方对某非政府正式组织之权益的所有权。 |
| 外国分支所有权（foreign branch ownership） | 某参与方对作为外国关联方且在法律上属于拥有实体一部分的正式组织或组织子单位的所有权。 |
| 投资权益（investment equity） | 代表对某实体之所有权权益的权益，可能以股东权益形式存在，也可能不是。 |
| 投资者（investor） | 通过投资拥有某组织一定份额的参与方。 |
| 投资者合同（investor contract） | 规定投资者向实体投资之条款、并规定赋予该投资者之权利的合同。 |
| 最终所有权（ultimate ownership） | 以会计合并为证的、某参与方对另一法律实体的最高层（顶端、末端）祖先级所有权。 |

### 2.1 继承关系（Inheritance）

- 章程性所有者（constitutional owner） ⊑ 实体所有者（entity owner）
- 控制性股权（controlling equity） ⊑ 股东权益
- 直接合并（direct consolidation） ⊑ 实体所有权（entity ownership）
- 实体所有者（entity owner） ⊑ 所有者
- 实体所有权（entity ownership） ⊑ 所有权
- 外国分支所有权（foreign branch ownership） ⊑ 实体所有权（entity ownership）
- 投资权益（investment equity） ⊑ 所有者权益
- 投资者（investor） ⊑ 实体所有者（entity owner）
- 投资者（investor） ⊑ 合同当事方
- 投资者合同（investor contract） ⊑ 书面合同
- 最终所有权（ultimate ownership） ⊑ 实体所有权（entity ownership）

## 3. 对象属性（Object Property）

| 属性（Property） | 中文（English） | 定义（Definition） | 说明 |
|---|---|---|---|
| fibo-be-oac-opty:guarantees | 担保（guarantees） | 提供正式的保证或承诺，尤指与产品、服务或交易相关的某些条件将得到满足。 | — |
| fibo-be-oac-opty:hasDirectOwnership | 具有直接所有权（has direct ownership） | 将正式组织关联到其被另一实体直接拥有的情形。 | 定义域（domain）：Na94fc9576da34375aa2884bfacc319ae；值域（range）：实体所有权（entity ownership）；逆属性（inverseOf）：具有被拥有实体（has owned entity）；子属性（subPropertyOf）：经历（experiences） |
| fibo-be-oac-opty:hasDirectOwningEntity | 具有直接拥有实体（has direct owning entity） | 将正式组织关联到直接的法律主体/所有者。 | — |
| fibo-be-oac-opty:hasInvestmentEntity | 具有投资实体（has investment entity） | 将法律主体关联到其直接拥有的正式组织或子公司，视所有权百分比而定。 | — |
| fibo-be-oac-opty:hasInvestmentOwnership | 具有投资所有权（has investment ownership） | 将法律主体关联到其拥有正式组织的情境。 | 定义域（domain）：法律主体；值域（range）：实体所有权（entity ownership）；逆属性（inverseOf）：具有拥有实体（has owning entity）；子属性（subPropertyOf）：在…中扮演主动角色（plays active role in） |
| fibo-be-oac-opty:hasOwnedEntity | 具有被拥有实体（has owned entity） | 标识被法律主体拥有的正式组织，可能包括独资企业。 | 定义域（domain）：实体所有权（entity ownership）；值域（range）：N4feeb6e88b6544fb855524b9dc3122ab；子属性（subPropertyOf）：被…经历（is experienced by） |
| fibo-be-oac-opty:hasOwningEntity | 具有拥有实体（has owning entity） | 标识拥有正式组织的参与方。 | 定义域（domain）：实体所有权（entity ownership）；值域（range）：法律主体；子属性（subPropertyOf）：具有主动参与方（has active party） |

## 5. 公理约定（Axioms）

- 章程性所有者（constitutional owner）：持有 some 股东权益
- 控制性股权（controlling equity）：授予 only 法律控制
- 实体所有者（entity owner）：持有 some 所有者权益
- 实体所有权（entity ownership）：受……限定 关系限定符 ≥0
- 实体所有权（entity ownership）：由……授予 N5dc4f7469e874abc9f1e2b34df7a970d ≥0
- 实体所有权（entity ownership）：restriction
- 实体所有权（entity ownership）：由……分类 关系状态 =1
- 实体所有权（entity ownership）：具有被拥有实体（has owned entity） some（restriction）
- 实体所有权（entity ownership）：具有拥有实体（has owning entity） some 法律主体
- 投资权益（investment equity）：由……持有 some 投资者（investor）
- 投资者（investor）：持有 some 投资权益（investment equity）
- 投资者合同（investor contract）：为……定义条款 some 投资权益（investment equity）

## 6. 依赖（owl:imports，13 个）

本本体通过 `owl:imports` 引入以下本体，各项的中文名称与简介如下：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `BE/LegalEntities/FormalBusinessOrganizations.rdf` | 正式商业组织本体（Formal Business Organizations Ontology） | 定义以营利为目的、依法注册的正式商业组织，连接法律实体与其商业功能。 |
| `BE/LegalEntities/LEIEntities.rdf` | LEI 法人实体本体（Legal Entity Identifier Entities Ontology） | 定义持有全球法人识别编码（LEI）的法人实体，对接 ISO 17442 标准的 LEI 体系。 |
| `BE/LegalEntities/LegalPersons.rdf` | 法律主体本体（Legal Persons Ontology） | 定义法律主体（legal person）与法定实体（legal entity）的核心概念：能持有权利义务、可起诉与被诉的主体。 |
| `FND/Agreements/Contracts.rdf` | 合同本体（Contracts Ontology） | 在协议之上定义具有法律约束力的合同（contract）：合同当事方、合同条款、义务与权利，是金融工具与交易合同建模的基石。 |
| `FND/OwnershipAndControl/Control.rdf` | 控制本体（Control Ontology） | 定义「控制」关系：控制方、被控制方与控制程度，用于公司治理与合并报表判断。 |
| `FND/OwnershipAndControl/Ownership.rdf` | 所有权本体（Ownership Ontology） | 定义「拥有」关系：所有者、被拥有资产及所有权份额。 |
| `FND/Relations/Relations.rdf` | 关系本体（Relations Ontology） | FIBO 最底层的基础本体，定义参考（reference）、分类（classify）等通用关系与抽象概念，全库普遍依赖。 |
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |
| `https://www.omg.org/spec/Commons/Classifiers/` | OMG 通用分类器本体（OMG Commons Classifiers） | OMG 通用本体库（Commons）中的分类器本体，定义分类方案、类别与归类关系的通用概念，FIBO 的分类建模建立在其上。 |
| `https://www.omg.org/spec/Commons/Documents/` | OMG 通用文档本体（OMG Commons Documents） | Commons 库中的文档本体，定义文档及其组成部分的通用概念。 |
| `https://www.omg.org/spec/Commons/Organizations/` | OMG 通用组织本体（OMG Commons Organizations） | Commons 库中的组织本体，定义组织、组织成员与组织结构的通用概念。 |
| `https://www.omg.org/spec/Commons/PartiesAndSituations/` | OMG 通用参与方与情境本体（OMG Commons Parties and Situations） | Commons 库中的参与方本体，定义独立主体、参与方及其角色扮演的通用概念，是 FIBO 参与方模型的上游。 |

## 7. 文件

- 官方 RDF/XML：`OwnershipParties.rdf`
- 中文 Turtle：`OwnershipParties.ttl`
- 结构图：`OwnershipParties-structure.png` / `OwnershipParties-structure.svg`