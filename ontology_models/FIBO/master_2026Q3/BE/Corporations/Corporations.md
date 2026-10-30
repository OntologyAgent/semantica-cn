# 公司本体（Corporations Ontology）结构与公理说明

本文档对应 `Corporations.rdf` / `Corporations.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `Corporations-structure.png`（`Corporations-structure.svg` 为可缩放版本）。

![公司本体（Corporations Ontology）本体结构图](Corporations-structure.png)

## 1. 本体概述

定义公司（corporation）这一法律实体形态：股份制、依法注册、具有独立法人资格的商业组织，及其注册与股份结构相关概念。

**在体系中的位置**：BE（商业实体）域公司模块的核心本体，处于「法律实体」层。

**上下游关系**：上游继承 BE/LegalEntities 的法人团体、正式商业组织以及 FND 的组织、法律本体；下游被 BE 所有权与控制权各本体以及 FBC、SEC 引用（发行人、上市公司通常就是公司）。

**与相近概念的差别**：与私人有限公司、合伙、信托并列，是股份制且可公开募资的法人形态；与正式商业组织的差别在于后者泛指一切以营利为目的的注册组织，公司只是其中一类。

## 2. 类（Class）

| 类（Class） | 定义（Definition） |
|---|---|
| 董事会协议（BoardAgreement） | 组织董事会成员之间正式的、具有法律约束力的协议。 |
| 合股公司（JointStockCompany） | 营利性、非法人企业，兼有公司与合伙的特征，所有权权益以股份表示。 |
| 私人持股公司（PrivatelyHeldCompany） | 已发行股份全部由家族或少数投资者团体持有、公众无法购买的公司。 |
| 公众持股公司（PubliclyHeldCompany） | 股份公开交易并持有的公司。 |
| 注册标识符（RegistrationIdentifier） | 组织注册时（通常在其组建所在管辖区）官方分配的标识符。 |
| 注册标识符方案（RegistrationIdentifierScheme） | 按签发注册机构规定注册标识符的方案。 |
| 宗教公司（ReligiousCorporation） | 目标特定于某套基本信仰与实践的非营利公司。 |

### 2.1 继承关系（Inheritance）


## 3. 对象属性（Object Property）

| 属性（Property） | 中文（English） | 定义（Definition） | 说明 |
|---|---|---|---|
| fibo-be-corp-corp:hasDateOfIncorporation | 具有注册成立日期（hasDateOfIncorporation） | 标识申报文件中所载的正式注册成立日期。 | — |
| fibo-be-corp-corp:hasDateOfRegistration | 具有登记日期（hasDateOfRegistration） | 标识公司为监管和/或税务目的在某管辖区登记的日期。 | — |
| fibo-be-corp-corp:hasIssuedCapital | 具有已发行资本（hasIssuedCapital） | 标识股东所持全部股份的总价值。 | — |

## 4. 数据属性（Datatype Property）

| 属性（Property） | 中文（English） | 定义（Definition） |
|---|---|---|
| fibo-be-corp-corp:hasSharesAuthorized | 具有授权股份数（hasSharesAuthorized） | 标识董事会确定的可发行股份的最大数量。 |

## 6. 依赖（owl:imports，12 个）

本本体通过 `owl:imports` 引入以下本体，各项的中文名称与简介如下：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `BE/LegalEntities/CorporateBodies.rdf` | 法人团体本体（Corporate Bodies Ontology） | 定义依法设立、具有独立法律人格的法人团体（corporate body），是股份有限公司等具体法人类型的上位概念。 |
| `BE/LegalEntities/FormalBusinessOrganizations.rdf` | 正式商业组织本体（Formal Business Organizations Ontology） | 定义以营利为目的、依法注册的正式商业组织，连接法律实体与其商业功能。 |
| `BE/LegalEntities/LegalPersons.rdf` | 法律主体本体（Legal Persons Ontology） | 定义法律主体（legal person）与法定实体（legal entity）的核心概念：能持有权利义务、可起诉与被诉的主体。 |
| `FND/Accounting/CurrencyAmount.rdf` | 货币金额本体（Currency Amount Ontology） | 定义「金额＋币种」的货币金额（currency amount）表示，是 FIBO 中表达价格、债务金额、付款额等一切带币种数值的基础构件。 |
| `FND/GoalsAndObjectives/Objectives.rdf` | 目标本体（Objectives Ontology） | 定义目标（objective）及其与组织、计划的关系，用于表达机构的经营目标与投资目标。 |
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |
| `https://www.omg.org/spec/Commons/DatesAndTimes/` | OMG 通用日期与时间本体（OMG Commons Dates and Times） | Commons 库中的日期时间本体，定义日期、期间、时间点等通用时间概念。 |
| `https://www.omg.org/spec/Commons/Designators/` | OMG 通用指称符本体（OMG Commons Designators） | Commons 库中的指称符本体，定义名称、标识符等「指代某物的符号」的通用概念。 |
| `https://www.omg.org/spec/Commons/Identifiers/` | OMG 通用标识符本体（OMG Commons Identifiers） | Commons 库中的标识符本体，定义标识符及其编码方案的通用概念。 |
| `https://www.omg.org/spec/Commons/Organizations/` | OMG 通用组织本体（OMG Commons Organizations） | Commons 库中的组织本体，定义组织、组织成员与组织结构的通用概念。 |
| `https://www.omg.org/spec/Commons/RegulatoryAgencies/` | OMG 通用监管机构本体（OMG Commons Regulatory Agencies） | Commons 库中的监管机构本体，定义监管机构及其监管职权的通用概念。 |

## 7. 文件

- 官方 RDF/XML：`Corporations.rdf`
- 中文 Turtle：`Corporations.ttl`
- 结构图：`Corporations-structure.png` / `Corporations-structure.svg`