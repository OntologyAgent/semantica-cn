# 商业登记机构本体（Business Registries Ontology）结构与公理说明

本文档对应 `BusinessRegistries.rdf` / `BusinessRegistries.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `BusinessRegistries-structure.png`（`BusinessRegistries-structure.svg` 为可缩放版本）。

![商业登记机构本体（Business Registries Ontology）本体结构图](BusinessRegistries-structure.png)

## 1. 本体概述

定义商业登记机构（business registry）：负责企业注册登记的机构（如州务卿办公室、公司注册处）及其登记职能。

**在体系中的位置**：FBC 功能实体模块中处理「企业在哪里登记」的本体。

**上下游关系**：上游依赖 BE 功能实体与登记主管机构相关概念；下游配套商事登记主管机关本体及其个体数据。

**与相近概念的差别**：登记机构≠监管机构——登记机构负责「记录主体存在」（发照注册），监管机构负责「监督行为合规」；与 LEI 登记的差别——LEI 是身份编码登记，商业登记是法人设立登记。

## 2. 类（Class）

| 类（Class） | 定义（Definition） |
|---|---|
| 北美行业分类体系代码（North American Industry Classification System code） | 代表某一行业的北美行业分类体系（NAICS）代码。 |
| 北美行业分类体系方案（North American Industry Classification System scheme） | 定义北美行业分类体系（NAICS）代码的方案。 |
| 商业登记册标识符（business register identifier） | 唯一标识商业登记册的标识符，例如由全球法人识别编码基金会（GLEIF）登记册标识的登记册。 |
| 商业登记主管机构（business registration authority） | 负责维护商业实体登记册的登记主管机构。 |
| 商业登记册（business registry） | 用于登记和维护商业实体信息的登记册。 |
| 商业登记册条目（business registry entry） | 商业登记册中的一条记录。 |
| 实体终止原因（entity expiration reason） | 表示法律实体终止存在和/或终止运营原因的代码。 |
| 实体法律形式登记册（entity legal form registry） | 按照特定司法管辖区规定，登记和维护商业实体有效法律形式信息的登记册。 |
| 实体法律形式登记册条目（entity legal form registry entry） | 符合 ISO 20275 标准的实体法律形式登记册记录。 |
| 实体状态（entity status） | 表明实体运营和/或法律状态的生命周期阶段。 |
| 实体核验级别（entity validation level） | 表示全球法人识别编码基金会（GLEIF）或本地运营单位（LOU）对注册人提供的参考数据所执行核验级别的代码。 |
| 法人识别编码登记册（legal entity identifier registry） | 为特定司法管辖区登记和维护商业实体信息的登记册。 |
| 法人识别编码登记册条目（legal entity identifier registry entry） | 符合 ISO 17442 及全球法人识别编码基金会（GLEIF）通用数据格式（CDF）的登记册记录。 |
| 本地运营单位（local operating unit） | 经全球法人识别编码基金会授权、可签发法人识别编码（LEI）的注册机构。 |
| 登记主管机构代码（registration authority code） | 唯一标识商业登记册、并与登记主管机构和司法管辖区相关联的标识符，由全球法人识别编码基金会签发。 |
| 登记状态（registration status） | 表明某事物（如企业或法律实体）特定登记状态的生命周期阶段，由登记主管机构规定。 |
| 标准行业分类代码（standard industrial classification code） | 代表某一行业的标准行业分类（SIC）代码。 |
| 标准行业分类方案（standard industrial classification scheme） | 定义标准行业分类（SIC）代码表的方案。 |

### 2.1 继承关系（Inheritance）

- 北美行业分类体系代码（North American Industry Classification System code） ⊑ 行业部门分类器
- 北美行业分类体系代码（North American Industry Classification System code） ⊑ 代码元素
- 北美行业分类体系方案（North American Industry Classification System scheme） ⊑ 行业部门分类方案
- 北美行业分类体系方案（North American Industry Classification System scheme） ⊑ 代码集
- 商业登记册标识符（business register identifier） ⊑ 标识符
- 商业登记主管机构（business registration authority） ⊑ 注册员
- 商业登记主管机构（business registration authority） ⊑ 注册机构
- 商业登记册（business registry） ⊑ 注册簿
- 商业登记册条目（business registry entry） ⊑ 注册簿条目
- 实体终止原因（entity expiration reason） ⊑ 代码元素
- 实体法律形式登记册（entity legal form registry） ⊑ 注册簿
- 实体法律形式登记册条目（entity legal form registry entry） ⊑ 注册簿条目
- 实体状态（entity status） ⊑ 生命周期阶段
- 实体核验级别（entity validation level） ⊑ 代码元素
- 法人识别编码登记册（legal entity identifier registry） ⊑ 商业登记册（business registry）
- 法人识别编码登记册条目（legal entity identifier registry entry） ⊑ 商业登记册条目（business registry entry）
- 本地运营单位（local operating unit） ⊑ 注册员
- 登记主管机构代码（registration authority code） ⊑ 代码元素
- 登记主管机构代码（registration authority code） ⊑ 注册标识符
- 登记状态（registration status） ⊑ 生命周期阶段
- 标准行业分类代码（standard industrial classification code） ⊑ 行业部门分类器
- 标准行业分类代码（standard industrial classification code） ⊑ 代码元素
- 标准行业分类方案（standard industrial classification scheme） ⊑ 行业部门分类方案
- 标准行业分类方案（standard industrial classification scheme） ⊑ 代码集

## 3. 对象属性（Object Property）

| 属性（Property） | 中文（English） | 定义（Definition） | 说明 |
|---|---|---|---|
| fibo-fbc-fct-breg:hasEntityExpirationReason | 具有实体终止原因（has entity expiration reason） | 指明实体终止存在的原因（如解散、与其他实体合并等）。 | 值域（range）：实体终止原因（entity expiration reason）；子属性（subPropertyOf）：由……表示 |
| fibo-fbc-fct-breg:hasEntityStatus | 具有实体状态（has entity status） | 指明实体的状态（如存续、注销）。 | 值域（range）：实体状态（entity status）；子属性（subPropertyOf）：具有阶段 |
| fibo-fbc-fct-breg:hasManagingLocalOperatingUnit | 具有管理本地运营单位（has managing local operating unit） | 将法人识别记录与注册相关法人识别编码的本地运营单位标识符关联起来。 | — |
| fibo-fbc-fct-breg:hasRegistrationStatus | 具有登记状态（has registration status） | 指明特定登记（如标识符或许可证的登记）的状态。 | 值域（range）：登记状态（registration status）；子属性（subPropertyOf）：具有阶段 |
| fibo-fbc-fct-breg:hasValidationAuthority | 具有核验机构（has validation authority） | 标识法律实体的商业登记主管机构，本地运营单位（LOU）以其作为核验依据。 | 值域（range）：商业登记主管机构（business registration authority）；子属性（subPropertyOf）：具有参与方角色（has party role） |
| fibo-fbc-fct-breg:hasValidationLevel | 具有核验级别（has validation level） | 指明注册机构对法律实体执行的核验级别。 | 值域（range）：实体核验级别（entity validation level） |

## 4. 数据属性（Datatype Property）

| 属性（Property） | 中文（English） | 定义（Definition） |
|---|---|---|
| fibo-fbc-fct-breg:hasAlternativeLanguageLegalName | 具有替代语言法定名称（has alternative language legal name） | 表示实体在其注册司法管辖区所使用的替代语言的注册法定名称。 |
| fibo-fbc-fct-breg:hasAutomaticallyTransliteratedLegalName | 具有自动转写法定名称（has automatically transliterated legal name） | 表示实体法定名称的自动生成的 ASCII 转写形式。 |
| fibo-fbc-fct-breg:hasEntityExpirationDate | 具有实体终止日期（has entity expiration date） | 指明实体终止存在的日期。 |
| fibo-fbc-fct-breg:hasExpiryDate | 具有到期日（has expiry date） | 指明某事物终止存在的日期。 |
| fibo-fbc-fct-breg:hasInitialRegistrationDate | 具有初始登记日期（has initial registration date） | 指明标识符或其他登记项目创建和/或首次登记的日期。 |
| fibo-fbc-fct-breg:hasPreferredTransliteratedLegalName | 具有首选转写法定名称（has preferred transliterated legal name） | 表示实体法定名称的首选 ASCII 转写形式。 |
| fibo-fbc-fct-breg:hasPriorLegalName | 具有曾用法定名称（has prior legal name） | 表示实体此前使用过的主要法定名称。 |
| fibo-fbc-fct-breg:hasRegistrationRevisionDate | 具有登记状态修订日期（has registration status revision date） | 指明登记册中特定登记状态被修订的日期。 |
| fibo-fbc-fct-breg:hasRegistryName | 具有登记册名称（has registry name） | 表示登记册的名称，例如登记法律实体商业登记标识符的商业登记册。 |
| fibo-fbc-fct-breg:hasRenewalDate | 具有续展日期（has renewal date） | 指明登记册中特定登记须续展或更新的日期。 |
| fibo-fbc-fct-breg:hasTradingOrOperationalName | 具有经营名称（has trading or operational name） | 表示实体当前使用的「以……名义经营」「品牌名」等名称，该名称是对法定名称的补充而非替代。 |
| fibo-fbc-fct-breg:hasTransliteratedLegalName | 具有转写法定名称（has transliterated legal name） | 表示实体法定名称的可选 ASCII 转写（即拉丁化/罗马化）形式。 |
| fibo-fbc-fct-breg:hasValidationDate | 具有核验日期（has validation date） | 指明登记册中特定登记最近一次被审核和核验的日期。 |
| fibo-fbc-fct-breg:isSelfMaintained | 是否自行维护（is self-maintained） | 表明实体信息是由内部维护还是由第三方维护。 |

## 5. 公理约定（Axioms）

- 北美行业分类体系代码（North American Industry Classification System code）：定义于 北美行业分类体系方案（North American Industry Classification System scheme） =1
- 北美行业分类体系代码（North American Industry Classification System code）：restriction
- 北美行业分类体系代码（North American Industry Classification System code）：分类 some 正式组织
- 北美行业分类体系方案（North American Industry Classification System scheme）：定义 some 北美行业分类体系代码（North American Industry Classification System code）
- 商业登记册标识符（business register identifier）：标识 商业登记册（business registry） =1
- 商业登记册标识符（business register identifier）：由……注册 some 商业登记主管机构（business registration authority）
- 商业登记主管机构（business registration authority）：管理 some 商业登记册（business registry）
- 商业登记主管机构（business registration authority）：登记 some 注册标识符
- 商业登记册（business registry）：restriction
- 商业登记册（business registry）：由……管理 商业登记主管机构（business registration authority） =1
- 商业登记册（business registry）：包含 some 商业登记册条目（business registry entry）
- 商业登记册条目（business registry entry）：具有登记状态（has registration status） 登记状态（registration status） ≤1
- 商业登记册条目（business registry entry）：包含 some 注册标识符
- 商业登记册条目（business registry entry）：具有注册日期 some cmns-dt:CombinedDateTime
- 实体终止原因（entity expiration reason）：restriction
- 实体法律形式登记册（entity legal form registry）：包含 some 实体法律形式登记册条目（entity legal form registry entry）
- 实体法律形式登记册条目（entity legal form registry entry）：包含 some 实体法律形式标识符
- 实体核验级别（entity validation level）：restriction
- 法人识别编码登记册（legal entity identifier registry）：包含 some 法人识别编码登记册条目（legal entity identifier registry entry）
- 法人识别编码登记册条目（legal entity identifier registry entry）：具有管理本地运营单位（has managing local operating unit） only 法律实体标识符
- 法人识别编码登记册条目（legal entity identifier registry entry）：具有核验机构（has validation authority） 商业登记主管机构（business registration authority） ≥0
- 法人识别编码登记册条目（legal entity identifier registry entry）：具有登记状态（has registration status） some 登记状态（registration status）
- 法人识别编码登记册条目（legal entity identifier registry entry）：具有核验级别（has validation level） some 实体核验级别（entity validation level）
- 法人识别编码登记册条目（legal entity identifier registry entry）：包含 some 法律实体标识符
- 本地运营单位（local operating unit）：发行 some 法律实体标识符
- 本地运营单位（local operating unit）：登记 some 法律实体标识符
- 登记主管机构代码（registration authority code）：标识 商业登记册（business registry） =1
- 标准行业分类代码（standard industrial classification code）：定义于 标准行业分类方案（standard industrial classification scheme） =1
- 标准行业分类代码（standard industrial classification code）：restriction
- 标准行业分类代码（standard industrial classification code）：分类 some 正式组织
- 标准行业分类方案（standard industrial classification scheme）：定义 some 标准行业分类代码（standard industrial classification code）

## 6. 依赖（owl:imports，20 个）

本本体通过 `owl:imports` 引入以下本体，各项的中文名称与简介如下：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `BE/LegalEntities/CorporateBodies.rdf` | 法人团体本体（Corporate Bodies Ontology） | 定义依法设立、具有独立法律人格的法人团体（corporate body），是股份有限公司等具体法人类型的上位概念。 |
| `BE/LegalEntities/FormalBusinessOrganizations.rdf` | 正式商业组织本体（Formal Business Organizations Ontology） | 定义以营利为目的、依法注册的正式商业组织，连接法律实体与其商业功能。 |
| `BE/LegalEntities/LEIEntities.rdf` | LEI 法人实体本体（Legal Entity Identifier Entities Ontology） | 定义持有全球法人识别编码（LEI）的法人实体，对接 ISO 17442 标准的 LEI 体系。 |
| `FBC/FunctionalEntities/FinancialServicesEntities.rdf` | 金融服务实体本体（Financial Services Entities Ontology） | FBC 域核心本体，定义金融服务机构（银行、券商、保险公司、资管机构等）的功能分类体系。 |
| `FND/AgentsAndPeople/People.rdf` | 人员本体（People Ontology） | 定义自然人（person）的核心属性：姓名、出生日期、国籍、身份标识与联系方式，为雇员、客户、签署人等角色提供「人」的基础模型。 |
| `FND/Arrangements/ClassificationSchemes.rdf` | 分类方案本体（Classification Schemes Ontology） | 定义分类方案（classification scheme）、类别及「将事物归入类别」的关系，支撑证券分类、行业分类等具体分类体系。 |
| `FND/Places/Addresses.rdf` | 地址本体（Addresses Ontology） | 定义邮政地址及其组成部分，为机构注册地、通讯地址建模。 |
| `FND/Relations/Relations.rdf` | 关系本体（Relations Ontology） | FIBO 最底层的基础本体，定义参考（reference）、分类（classify）等通用关系与抽象概念，全库普遍依赖。 |
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |
| `https://www.omg.org/spec/Commons/Classifiers/` | OMG 通用分类器本体（OMG Commons Classifiers） | OMG 通用本体库（Commons）中的分类器本体，定义分类方案、类别与归类关系的通用概念，FIBO 的分类建模建立在其上。 |
| `https://www.omg.org/spec/Commons/CodesAndCodeSets/` | OMG 通用代码与代码集本体（OMG Commons Codes and Code Sets） | Commons 库中的代码本体，定义代码、代码集及其维护方的通用概念，是 ISO 4217、ISO 3166 等编码体系建模的基础。 |
| `https://www.omg.org/spec/Commons/Collections/` | OMG 通用集合本体（OMG Commons Collections） | Commons 库中的集合本体，定义集合、成员等通用概念。 |
| `https://www.omg.org/spec/Commons/DatesAndTimes/` | OMG 通用日期与时间本体（OMG Commons Dates and Times） | Commons 库中的日期时间本体，定义日期、期间、时间点等通用时间概念。 |
| `https://www.omg.org/spec/Commons/Designators/` | OMG 通用指称符本体（OMG Commons Designators） | Commons 库中的指称符本体，定义名称、标识符等「指代某物的符号」的通用概念。 |
| `https://www.omg.org/spec/Commons/Identifiers/` | OMG 通用标识符本体（OMG Commons Identifiers） | Commons 库中的标识符本体，定义标识符及其编码方案的通用概念。 |
| `https://www.omg.org/spec/Commons/Organizations/` | OMG 通用组织本体（OMG Commons Organizations） | Commons 库中的组织本体，定义组织、组织成员与组织结构的通用概念。 |
| `https://www.omg.org/spec/Commons/PartiesAndSituations/` | OMG 通用参与方与情境本体（OMG Commons Parties and Situations） | Commons 库中的参与方本体，定义独立主体、参与方及其角色扮演的通用概念，是 FIBO 参与方模型的上游。 |
| `https://www.omg.org/spec/Commons/RegistrationAuthorities/` | OMG 通用登记主管机构本体（OMG Commons Registration Authorities） | Commons 库中的登记主管机构本体，定义负责登记注册的主管机构及其登记行为的通用概念。 |
| `https://www.omg.org/spec/Commons/RolesAndCompositions/` | OMG 通用角色与构成本体（OMG Commons Roles and Compositions） | Commons 库中的角色本体，定义角色及整体—部分构成关系的通用概念。 |

## 7. 文件

- 官方 RDF/XML：`BusinessRegistries.rdf`
- 中文 Turtle：`BusinessRegistries.ttl`
- 结构图：`BusinessRegistries-structure.png` / `BusinessRegistries-structure.svg`