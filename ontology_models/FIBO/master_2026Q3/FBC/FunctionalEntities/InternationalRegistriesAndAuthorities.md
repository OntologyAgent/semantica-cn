# 国际登记与主管机构本体（International Registries and Authorities Ontology）结构与公理说明

本文档对应 `InternationalRegistriesAndAuthorities.rdf` / `InternationalRegistriesAndAuthorities.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `InternationalRegistriesAndAuthorities-structure.png`（`InternationalRegistriesAndAuthorities-structure.svg` 为可缩放版本）。

![国际登记与主管机构本体（International Registries and Authorities Ontology）本体结构图](InternationalRegistriesAndAuthorities-structure.png)

## 1. 本体概述

收录国际性登记机构与主管当局的参考个体（如国际证券识别编码机构等跨国组织）。

**在体系中的位置**：FBC 功能实体模块的参考数据本体，覆盖不属于单一国家的机构。

**上下游关系**：上游依赖商业登记与监管机构概念；下游为跨境业务提供机构实例。

**与相近概念的差别**：与各国登记/监管机构本体的差别——收录范围是跨国与超国家机构，不是某国国内机构。

## 2. 类（Class）

| 类（Class） | 定义（Definition） |
|---|---|
| 商业标识代码数据记录（business identifier code data record） | 符合 ISO 9362 的登记册条目，用于管理 BIC 代码及相关注册信息。 |
| 市场标识代码登记册条目（market identifier code registry entry） | 符合 ISO 10383 的市场标识代码（MIC）登记册条目。 |

### 2.1 继承关系（Inheritance）

- 商业标识代码数据记录（business identifier code data record） ⊑ 商业登记册条目
- 市场标识代码登记册条目（market identifier code registry entry） ⊑ 注册簿条目

## 5. 公理约定（Axioms）

- 商业标识代码数据记录（business identifier code data record）：restriction
- 商业标识代码数据记录（business identifier code data record）：是否自行维护 some xsd:string
- 商业标识代码数据记录（business identifier code data record）：包含 some 商业标识代码
- 市场标识代码登记册条目（market identifier code registry entry）：restriction
- 市场标识代码登记册条目（market identifier code registry entry）：restriction
- 市场标识代码登记册条目（market identifier code registry entry）：具有市场标识代码状态 市场标识代码状态 =1
- 市场标识代码登记册条目（market identifier code registry entry）：restriction
- 市场标识代码登记册条目（market identifier code registry entry）：包含 some 市场标识符

## 6. 依赖（owl:imports，20 个）

本本体通过 `owl:imports` 引入以下本体，各项的中文名称与简介如下：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `BE/GovernmentEntities/GovernmentEntities.rdf` | 政府实体本体（Government Entities Ontology） | 定义政府、政体（polity）、法域（jurisdiction）及政府实体的核心概念，是各区域政府实体本体的共同基础。 |
| `BE/LegalEntities/FormalBusinessOrganizations.rdf` | 正式商业组织本体（Formal Business Organizations Ontology） | 定义以营利为目的、依法注册的正式商业组织，连接法律实体与其商业功能。 |
| `BE/LegalEntities/LEIEntities.rdf` | LEI 法人实体本体（Legal Entity Identifier Entities Ontology） | 定义持有全球法人识别编码（LEI）的法人实体，对接 ISO 17442 标准的 LEI 体系。 |
| `FBC/FunctionalEntities/BusinessRegistries.rdf` | 商业登记机构本体（Business Registries Ontology） | 定义商业登记机构（如公司注册处）及其登记职能。 |
| `FBC/FunctionalEntities/FinancialServicesEntities.rdf` | 金融服务实体本体（Financial Services Entities Ontology） | FBC 域核心本体，定义金融服务机构（银行、券商、保险公司、资管机构等）的功能分类体系。 |
| `FBC/FunctionalEntities/Markets.rdf` | 市场本体（Markets Ontology） | 定义金融市场（market）：交易所、场外市场及其功能。 |
| `FBC/ProductsAndServices/FinancialProductsAndServices.rdf` | 金融产品与服务本体（Financial Products and Services Ontology） | 定义金融产品（financial product）与金融服务（financial service）及其提供、购买关系。 |
| `FND/Places/Addresses.rdf` | 地址本体（Addresses Ontology） | 定义邮政地址及其组成部分，为机构注册地、通讯地址建模。 |
| `FND/Relations/Relations.rdf` | 关系本体（Relations Ontology） | FIBO 最底层的基础本体，定义参考（reference）、分类（classify）等通用关系与抽象概念，全库普遍依赖。 |
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |
| `https://www.omg.org/spec/Commons/Collections/` | OMG 通用集合本体（OMG Commons Collections） | Commons 库中的集合本体，定义集合、成员等通用概念。 |
| `https://www.omg.org/spec/Commons/DatesAndTimes/` | OMG 通用日期与时间本体（OMG Commons Dates and Times） | Commons 库中的日期时间本体，定义日期、期间、时间点等通用时间概念。 |
| `https://www.omg.org/spec/Commons/Designators/` | OMG 通用指称符本体（OMG Commons Designators） | Commons 库中的指称符本体，定义名称、标识符等「指代某物的符号」的通用概念。 |
| `https://www.omg.org/spec/Commons/Identifiers/` | OMG 通用标识符本体（OMG Commons Identifiers） | Commons 库中的标识符本体，定义标识符及其编码方案的通用概念。 |
| `https://www.omg.org/spec/Commons/Locations/` | OMG 通用位置本体（OMG Commons Locations） | Commons 库中的位置本体，定义地理位置、地点的通用概念。 |
| `https://www.omg.org/spec/Commons/Organizations/` | OMG 通用组织本体（OMG Commons Organizations） | Commons 库中的组织本体，定义组织、组织成员与组织结构的通用概念。 |
| `https://www.omg.org/spec/Commons/RegistrationAuthorities/` | OMG 通用登记主管机构本体（OMG Commons Registration Authorities） | Commons 库中的登记主管机构本体，定义负责登记注册的主管机构及其登记行为的通用概念。 |
| `https://www.omg.org/spec/Commons/RolesAndCompositions/` | OMG 通用角色与构成本体（OMG Commons Roles and Compositions） | Commons 库中的角色本体，定义角色及整体—部分构成关系的通用概念。 |
| `https://www.omg.org/spec/LCC/Countries/ISO3166-1-CountryCodes/` | LCC ISO 3166-1 国家代码（ISO 3166-1 Country Codes） | LCC 中 ISO 3166-1 标准的国家/地区代码个体集（如 CN、US、MX），供法域与地址建模引用。 |

## 7. 文件

- 官方 RDF/XML：`InternationalRegistriesAndAuthorities.rdf`
- 中文 Turtle：`InternationalRegistriesAndAuthorities.ttl`
- 结构图：`InternationalRegistriesAndAuthorities-structure.png` / `InternationalRegistriesAndAuthorities-structure.svg`