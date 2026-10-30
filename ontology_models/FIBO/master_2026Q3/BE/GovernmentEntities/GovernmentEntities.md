# 政府实体本体（Government Entities Ontology）结构与公理说明

本文档对应 `GovernmentEntities.rdf` / `GovernmentEntities.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `GovernmentEntities-structure.png`（`GovernmentEntities-structure.svg` 为可缩放版本）。

![政府实体本体（Government Entities Ontology）本体结构图](GovernmentEntities-structure.png)

## 1. 本体概述

定义政府（government）、政体（polity）与法域（jurisdiction）的核心概念：政体是具有主权的政治实体，政府是其行政机关，法域是其法律效力的适用范围。

**在体系中的位置**：BE 政府实体模块的根基，全球 17 个区域政府实体与法域本体全部建立在它之上。

**上下游关系**：上游依赖 FND 的法律核心、正式组织、地点本体；下游是各区域政府实体个体本体，以及 FBC、LOAN 等需要表达监管法域、注册地的本体。

**与相近概念的差别**：政体、政府、法域三者常被混用但含义不同——国家是政体，国务院/政府内阁是政府，「适用中国法律」指的是法域；与 FND/Law/LegalCore 的法域概念衔接并落到具体国家。

## 2. 类（Class）

| 类（Class） | 定义（Definition） |
|---|---|
| 政府部门分支（branch of government） | 国家政府的分支，拥有相互独立、互不冲突的权力与职责范围。 |
| 权力下放政府（devolved government） | 治理次国家领土的政府及政客，其权力可能是临时的、可撤销的，最终归属于中央政府。 |
| 行政分支（executive branch） | 经授权负责政府日常行政管理的政府部门分支。 |
| 联邦政府（federal government） | 在中央政府之下联合的各州，中央政府有别于各成员州各自的政府。 |
| 联邦主权体（federated sovereignty） | 以中央（联邦）政府之下若干部分自治的州或地区的联合为特征的政体。 |
| 政府（government） | 控制国家或共同体的体系。 |
| 政府机构（government agency） | 政府机器中负责某领域监督与行政的永久或半永久组织，常为受任命的委员会。 |
| 政府任命官员（government appointee） | 由政府法令指定领导或以某种身份参与政府机构的个人。 |
| 政府机关（government body） | 作为超国家、国家、联邦、州或地方政府之机构、部属单位或其他机关的正式组织。 |
| 政府部门（government department） | 负责政府公共行政某个领域的专门组织。 |
| 政府部长（government minister） | 被任命或当选担任政府高级职务的行政官员。 |
| 政府官员（government official） | 经选举或任命管理政府某方面事务的人。 |
| 部属单位（instrumentality） | 服务公共目的、与政府关系密切但不是政府机构的组织。 |
| 司法分支（judiciary） | 由法院系统构成的政府部门分支，以超国家、国家、联邦或地区当局之名解释和适用法律。 |
| 立法机关（legislature） | 政治单位（通常为国家政府）的立法机构，有权制定、修改和废止公共政策。 |
| 市政实体（municipal entity） | 通常代表城市、镇区或其他行政区划的政体，具有法人地位和自治权力或管辖权。 |
| 市政府（municipal government） | 城市、镇区或其他行政区划的地区政府。 |
| 国家政府（national government） | 治理整个国家（相对于地方政府）的政府及政客。 |
| 政体（polity） | 作为超国家实体、王室、国家或下级民政当局（如省、县、市）的法律主体。 |
| 地区政府（regional government） | 地理区域（如县、小城镇或类似社区）的行政机构。 |
| 地区主权体（regional sovereignty） | 对应行政区划、行政单位、行政实体或国家行政区划的法律主体。 |
| 主权国家（sovereign state） | 由对一个地理区域拥有主权的单一中央政府所代表的非物理法人实体。 |
| 超国家实体（supranational entity） | 依国际法或条约建立、或在国际层面注册成立的政府或非政府实体。 |
| 部落地区（tribal area） | 由原住民群体而非主权国家或地区政府实体管辖的地理区域的指称。 |
| 部落实体（tribal entity） | 代表主权部落（原住民）政府基本单位的法律实体。 |
| 部落政府（tribal government） | 代表原住民群体、对该群体拥有合法治理权（包括立法权）的政府。 |

### 2.1 继承关系（Inheritance）

- 政府部门分支（branch of government） ⊑ 政府机关（government body）
- 权力下放政府（devolved government） ⊑ 政府（government）
- 行政分支（executive branch） ⊑ 政府部门分支（branch of government）
- 联邦政府（federal government） ⊑ 国家政府（national government）
- 联邦主权体（federated sovereignty） ⊑ 主权国家（sovereign state）
- 政府（government） ⊑ 功能实体
- 政府机构（government agency） ⊑ 政府机关（government body）
- 政府任命官员（government appointee） ⊑ 政府官员（government official）
- 政府任命官员（government appointee） ⊑ 高管
- 政府机关（government body） ⊑ 正式组织
- 政府部门（government department） ⊑ 政府机关（government body）
- 政府部长（government minister） ⊑ 政府官员（government official）
- 政府部长（government minister） ⊑ 高管
- 政府官员（government official） ⊑ 责任方
- 部属单位（instrumentality） ⊑ 政府机关（government body）
- 部属单位（instrumentality） ⊑ 法律实体
- 司法分支（judiciary） ⊑ 政府部门分支（branch of government）
- 立法机关（legislature） ⊑ 政府部门分支（branch of government）
- 市政实体（municipal entity） ⊑ 政体（polity）
- 市政府（municipal government） ⊑ 政府（government）
- 国家政府（national government） ⊑ 政府（government）
- 政体（polity） ⊑ 政府机关（government body）
- 政体（polity） ⊑ 法律主体
- 地区政府（regional government） ⊑ 政府（government）
- 地区主权体（regional sovereignty） ⊑ 政体（polity）
- 主权国家（sovereign state） ⊑ 政体（polity）
- 超国家实体（supranational entity） ⊑ 政体（polity）
- 部落地区（tribal area） ⊑ 地缘政治实体
- 部落实体（tribal entity） ⊑ 政体（polity）
- 部落政府（tribal government） ⊑ 政府（government）

## 3. 对象属性（Object Property）

| 属性（Property） | 中文（English） | 定义（Definition） | 说明 |
|---|---|---|---|
| fibo-be-ge-ge:hasFullSovereigntyOver | 对……拥有完全主权（has full sovereignty over） | 将政体关联到其拥有绝对、最高且不受他者约束之统治权的地缘政治实体。 | 子属性（subPropertyOf）：对……拥有主权（has sovereignty over） |
| fibo-be-ge-ge:hasSharedSovereigntyOver | 对……拥有共享主权（has shared sovereignty over） | 将政体关联到其与他者共享统治权的地缘政治实体。 | 子属性（subPropertyOf）：对……拥有主权（has sovereignty over） |
| fibo-be-ge-ge:hasSovereigntyOver | 对……拥有主权（has sovereignty over） | 将政体关联到其行使政治统治权的地缘政治实体。 | 定义域（domain）：政体（polity）；值域（range）：地缘政治实体；子属性（subPropertyOf）：管辖 |
| fibo-be-ge-ge:isInstrumentOf | 是……的部属单位（is an instrument of） | 将某政府的部属单位关联到它所支持的政府。 | 定义域（domain）：部属单位（instrumentality）；值域（range）：政府（government） |
| fibo-be-ge-ge:isElectedBy | 由……选举产生（is elected by） | 标识通过投票选出任职的官员或政府。 | 逆属性（inverseOf）：选举 |
| fibo-be-ge-ge:isRepresentedBy | 由……代表（is represented by） | 将治理体系关联到其选出的代表。 | — |

## 5. 公理约定（Axioms）

- 联邦政府（federal government）：restriction
- 联邦主权体（federated sovereignty）：restriction
- 联邦主权体（federated sovereignty）：restriction
- 政府（government）：具有成员 N5208a413ac0a4e3aacf74b77636bfa8e ≥0
- 政府（government）：管辖 some 地缘政治实体
- 政府（government） 与 部属单位（instrumentality） 互斥（disjointWith）
- 政府机构（government agency）：由……管理 政府任命官员（government appointee） ≥0
- 政府机构（government agency） 与 政府部门（government department） 互斥（disjointWith）
- 政府任命官员（government appointee）：由…扮演（is played by） N637d4687be584d58a1792db2cd71b51c ≥0
- 政府机关（government body）：具有目标 公共宗旨 ≥0
- 政府部门（government department）：由……管理 政府部长（government minister） ≥0
- 政府官员（government official）：由…扮演（is played by） 具有法律行为能力的自然人 =1
- 政府官员（government official）：由…扮演（is played by） some（是……的成员 政府机关（government body） ≥0）
- 部属单位（instrumentality）：由……授权要求 成文法 ≥0
- 部属单位（instrumentality）：是……的部属单位（is an instrument of） some 政府（government）
- 司法分支（judiciary）：具有部分 some 法院
- 市政实体（municipal entity）：对……拥有主权（has sovereignty over） some 市政区
- 市政实体（municipal entity）：由……代表（is represented by） some 市政府（municipal government）
- 市政府（municipal government）：管辖 some 市政区
- 国家政府（national government）：管辖 some 国家
- 政体（polity）：对……拥有主权（has sovereignty over） some 地缘政治实体
- 政体（polity）：由……代表（is represented by） some 政府（government）
- 地区政府（regional government）：管辖 some 地缘政治实体
- 地区主权体（regional sovereignty）：对……拥有共享主权（has shared sovereignty over） some 地缘政治实体
- 地区主权体（regional sovereignty）：由……代表（is represented by） some 地区政府（regional government）
- 主权国家（sovereign state）：对……拥有完全主权（has full sovereignty over） some 国家
- 主权国家（sovereign state）：由……代表（is represented by） some 国家政府（national government）
- 超国家实体（supranational entity）：对……拥有共享主权（has shared sovereignty over） some 国家
- 超国家实体（supranational entity）：由……代表（is represented by） some 政府机关（government body）
- 部落实体（tribal entity）：对……拥有共享主权（has shared sovereignty over） some 部落地区（tribal area）
- 部落实体（tribal entity）：由……代表（is represented by） some 部落政府（tribal government）
- 部落政府（tribal government）：管辖 some 部落地区（tribal area）

## 6. 依赖（owl:imports，15 个）

本本体通过 `owl:imports` 引入以下本体，各项的中文名称与简介如下：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `BE/FunctionalEntities/FunctionalEntities.rdf` | 功能实体本体（Functional Entities Ontology） | 定义「功能实体」：按其在商业中承担的功能（而非法律形式）刻画的实体，是出版方、登记机构等功能性主体的基础。 |
| `BE/LegalEntities/LegalPersons.rdf` | 法律主体本体（Legal Persons Ontology） | 定义法律主体（legal person）与法定实体（legal entity）的核心概念：能持有权利义务、可起诉与被诉的主体。 |
| `BE/OwnershipAndControl/Executives.rdf` | 高管本体（Executives Ontology） | 定义公司高管（executive）、董事会成员及其职务角色，刻画「谁在管理公司」。 |
| `FND/AgentsAndPeople/People.rdf` | 人员本体（People Ontology） | 定义自然人（person）的核心属性：姓名、出生日期、国籍、身份标识与联系方式，为雇员、客户、签署人等角色提供「人」的基础模型。 |
| `FND/GoalsAndObjectives/Objectives.rdf` | 目标本体（Objectives Ontology） | 定义目标（objective）及其与组织、计划的关系，用于表达机构的经营目标与投资目标。 |
| `FND/Law/LegalCore.rdf` | 法律核心本体（Legal Core Ontology） | 定义法域（jurisdiction）、法律、法规等核心法律概念，为监管主体与适用法律建模。 |
| `FND/Relations/Relations.rdf` | 关系本体（Relations Ontology） | FIBO 最底层的基础本体，定义参考（reference）、分类（classify）等通用关系与抽象概念，全库普遍依赖。 |
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |
| `https://www.omg.org/spec/Commons/BusinessAuthorizations/` | OMG 通用商业授权本体（OMG Commons Business Authorizations） | OMG 通用本体库（Commons）中的商业授权本体，定义授权、签章与代理权限的通用概念。 |
| `https://www.omg.org/spec/Commons/Collections/` | OMG 通用集合本体（OMG Commons Collections） | Commons 库中的集合本体，定义集合、成员等通用概念。 |
| `https://www.omg.org/spec/Commons/Locations/` | OMG 通用位置本体（OMG Commons Locations） | Commons 库中的位置本体，定义地理位置、地点的通用概念。 |
| `https://www.omg.org/spec/Commons/Organizations/` | OMG 通用组织本体（OMG Commons Organizations） | Commons 库中的组织本体，定义组织、组织成员与组织结构的通用概念。 |
| `https://www.omg.org/spec/Commons/RegulatoryAgencies/` | OMG 通用监管机构本体（OMG Commons Regulatory Agencies） | Commons 库中的监管机构本体，定义监管机构及其监管职权的通用概念。 |
| `https://www.omg.org/spec/Commons/RolesAndCompositions/` | OMG 通用角色与构成本体（OMG Commons Roles and Compositions） | Commons 库中的角色本体，定义角色及整体—部分构成关系的通用概念。 |

## 7. 文件

- 官方 RDF/XML：`GovernmentEntities.rdf`
- 中文 Turtle：`GovernmentEntities.ttl`
- 结构图：`GovernmentEntities-structure.png` / `GovernmentEntities-structure.svg`