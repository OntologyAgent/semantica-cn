# 金融机构示例（Financial Institution Examples）说明

本文档对应 `FinancialInstitutionExamples.rdf` / `FinancialInstitutionExamples.ttl`。

## 1. 本文件是什么

收录典型金融机构的示例个体。

从机制上说，这是一个个体（individuals）文件：它本身不定义任何新的类或属性，装的全是命名个体（owl:NamedIndividual）——也就是一条条真实存在的实例数据（如具体的货币、市场、监管机构、法域）。它的 `owl:imports` 引入的是这些个体所属的类定义所在的本体。应用需要实例级参考数据时加载这类文件。

## 2. 个体构成（共 217 个）

按个体所属类型统计（类型名为中文（English）对照）：

| 类型（Class） | 个体数量 |
|---|---|
| 法人识别编码登记册条目（LegalEntityIdentifierRegistryEntry） | 26 |
| 显式日期（ExplicitDate） | 26 |
| 常规街道地址（ConventionalStreetAddress） | 25 |
| 物理地址（PhysicalAddress） | 18 |
| 注册标识符（RegistrationIdentifier） | 14 |
| 研究统计监管与贴现信贷标识符（ResearchStatisticsSupervisionDiscountIdentifier） | 14 |
| 经纪公司（BrokerageFirm） | 12 |
| 公司（Corporation） | 12 |
| 介绍经纪商（IntroducingBroker） | 11 |
| 互换交易商（SwapDealer） | 11 |
| 商品交易顾问（CommodityTradingAdvisor） | 11 |
| 商业银行（CommercialBank） | 8 |
| 金融控股公司（FinancialHoldingCompany） | 7 |
| 联邦存款保险公司证书编号（FDICCertificateNumber） | 6 |
| 路由号码（RoutingTransitNumber） | 6 |
| 投资银行（InvestmentBank） | 6 |
| 国民银行（NationalBank） | 5 |
| 股份公司（StockCorporation） | 5 |
| 商业标识代码（BusinessIdentifierCode） | 5 |
| 商业方前缀（BusinessPartyPrefix） | 5 |
| 商业方后缀（BusinessPartySuffix） | 5 |
| 营利公司（ForProfitCorporation） | 5 |
| 公众持股公司（PubliclyHeldCompany） | 5 |
| 直接合并（DirectConsolidation） | 5 |
| 保险公司（InsuranceCompany） | 4 |
| 有限责任公司（LimitedLiabilityCompany） | 4 |
| 企业实体（BusinessEntity） | 3 |
| 有限责任私人公司（PrivateCompanyWithLimitedLiability） | 3 |
| 金融公司（FinanceCompany） | 1 |
| 管理公司（ManagementCompany） | 1 |
| 联邦储备体系成员（FederalReserveSystemMember） | 1 |
| 州特许银行（StateCharteredBank） | 1 |
| 注册标识符（RegisteredIdentifier） | 1 |
| 政府颁发的许可证（GovernmentIssuedLicense） | 1 |
| 许可标识符（LicenseIdentifier） | 1 |
| 州成员银行（StateMemberBank） | 1 |
| 信托（Trust） | 1 |

个体数量较多，仅举前 10 个示例，完整清单见同名 `.ttl` 文件：

| 个体（示例） | 类型 |
|---|---|
| ABN AMRO Bank | 介绍经纪商（IntroducingBroker）、互换交易商（SwapDealer）、经纪公司（BrokerageFirm）、商业银行（CommercialBank）、商品交易顾问（CommodityTradingAdvisor）、保险公司（InsuranceCompany） |
| ABN AMRO Bank N.V. | 公司（Corporation） |
| ABN AMRO Bank N.V. headquarters address | 常规街道地址（ConventionalStreetAddress） |
| ABN AMRO Bank N.V. legal address | 常规街道地址（ConventionalStreetAddress） |
| ABN AMRO Bank N.V. legal entity identifier registry entry | 法人识别编码登记册条目（LegalEntityIdentifierRegistryEntry） |
| ABN AMRO Securities | 经纪公司（BrokerageFirm） |
| ABN AMRO Securities (USA) LLC | 有限责任公司（LimitedLiabilityCompany） |
| ABN AMRO Securities (USA) LLC headquarters address | 常规街道地址（ConventionalStreetAddress） |
| ABN AMRO Securities (USA) LLC legal address | 常规街道地址（ConventionalStreetAddress） |
| ABN AMRO Securities (USA) LLC legal entity identifier registry entry | 法人识别编码登记册条目（LegalEntityIdentifierRegistryEntry） |

## 3. 依赖的本体（owl:imports，43 个）

以下导入提供个体所属的类定义与相关参考数据：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `BE/GovernmentEntities/GovernmentEntities.rdf` | 政府实体本体（Government Entities Ontology） | 定义政府、政体（polity）、法域（jurisdiction）及政府实体的核心概念，是各区域政府实体本体的共同基础。 |
| `BE/GovernmentEntities/NorthAmericanJurisdiction/USGovernmentEntitiesAndJurisdictions.rdf` | 美国政府实体与法域本体（US Government Entities and Jurisdictions Ontology） | 收录美国的政体、联邦与各州政府、法域个体，是北美金融建模最常用的法域参考数据。 |
| `BE/LegalEntities/CorporateBodies.rdf` | 法人团体本体（Corporate Bodies Ontology） | 定义依法设立、具有独立法律人格的法人团体（corporate body），是股份有限公司等具体法人类型的上位概念。 |
| `BE/LegalEntities/FormalBusinessOrganizations.rdf` | 正式商业组织本体（Formal Business Organizations Ontology） | 定义以营利为目的、依法注册的正式商业组织，连接法律实体与其商业功能。 |
| `BE/LegalEntities/LEIEntities.rdf` | LEI 法人实体本体（Legal Entity Identifier Entities Ontology） | 定义持有全球法人识别编码（LEI）的法人实体，对接 ISO 17442 标准的 LEI 体系。 |
| `BE/LegalEntities/LegalPersons.rdf` | 法律主体本体（Legal Persons Ontology） | 定义法律主体（legal person）与法定实体（legal entity）的核心概念：能持有权利义务、可起诉与被诉的主体。 |
| `BE/OwnershipAndControl/ControlParties.rdf` | 控制方本体（Control Parties Ontology） | 定义处于控制关系中的各方角色：控制方、被控制方、实际控制人等。 |
| `BE/OwnershipAndControl/CorporateControl.rdf` | 公司控制本体（Corporate Control Ontology） | 定义公司层面的控制关系：控股股东、多数/少数控制、表决权控制等。 |
| `BE/OwnershipAndControl/OwnershipParties.rdf` | 所有权方本体（Ownership Parties Ontology） | 定义所有权关系中的各方角色：所有者、受益所有人、名义持有人等。 |
| `BE/PrivateLimitedCompanies/PrivateLimitedCompanies.rdf` | 私人有限公司本体（Private Limited Companies Ontology） | 定义私人有限公司（private limited company）这类不公开募股的有限责任公司形态。 |
| `BE/Trusts/Trusts.rdf` | 信托本体（Trusts Ontology） | 定义信托（trust）及委托人、受托人与受益人之间的信托关系。 |
| `DER/DerivativesContracts/DerivativesBasics.rdf` | 衍生品基础本体（Derivatives Basics Ontology） | 定义衍生品合约（derivatives contract）的核心概念：标的资产、行权、到期等，是 DER 域的根基。 |
| `DER/DerivativesContracts/Swaps.rdf` | 互换本体（Swaps Ontology） | 定义互换（swap）合约的通用结构：互换腿（swap leg）、现金流交换与名义本金。 |
| `EXMP/LegalEntities/DowJonesIndustrialAverageCompanies.rdf` | 道指成分公司示例（Dow Jones Industrial Average Companies） | 收录道琼斯工业平均指数成分股公司的示例个体，供演示与测试。 |
| `FBC/FunctionalEntities/BusinessCentersIndividuals.rdf` | 商业中心个体本体（Business Centers Individuals） | 收录全球主要商业中心（如纽约、伦敦、东京）的参考个体。 |
| `FBC/FunctionalEntities/BusinessRegistries.rdf` | 商业登记机构本体（Business Registries Ontology） | 定义商业登记机构（如公司注册处）及其登记职能。 |
| `FBC/FunctionalEntities/CommercialRegistrationAuthorities.rdf` | 商事登记主管机关本体（Commercial Registration Authorities Ontology） | 定义负责商事登记的主管机关及其维护的登记记录。 |
| `FBC/FunctionalEntities/EuropeanEntities/EURegulatoryAgencies.rdf` | 欧盟监管机构本体（EU Regulatory Agencies Ontology） | 收录欧盟层面的金融监管机构个体（如欧洲央行、欧洲证券和市场管理局 ESMA）。 |
| `FBC/FunctionalEntities/FinancialServicesEntities.rdf` | 金融服务实体本体（Financial Services Entities Ontology） | FBC 域核心本体，定义金融服务机构（银行、券商、保险公司、资管机构等）的功能分类体系。 |
| `FBC/FunctionalEntities/MarketsIndividuals.rdf` | 市场个体本体（Markets Individuals） | 收录全球主要金融市场的参考个体。 |
| `FBC/FunctionalEntities/NorthAmericanEntities/USFinancialServicesEntities.rdf` | 美国金融服务实体本体（US Financial Services Entities Ontology） | 定义美国法域下的金融服务机构类型与个体。 |
| `FBC/FunctionalEntities/NorthAmericanEntities/USRegulatoryAgencies.rdf` | 美国监管机构本体（US Regulatory Agencies Ontology） | 收录美国金融监管机构个体（如美联储、证监会 SEC、货币监理署 OCC）。 |
| `FBC/FunctionalEntities/RegulatoryAgencies.rdf` | 监管机构本体（Regulatory Agencies Ontology） | 定义金融监管机构（regulatory agency）及其监管职能的通用概念。 |
| `FBC/ProductsAndServices/FinancialProductsAndServices.rdf` | 金融产品与服务本体（Financial Products and Services Ontology） | 定义金融产品（financial product）与金融服务（financial service）及其提供、购买关系。 |
| `FND/Agreements/Contracts.rdf` | 合同本体（Contracts Ontology） | 在协议之上定义具有法律约束力的合同（contract）：合同当事方、合同条款、义务与权利，是金融工具与交易合同建模的基石。 |
| `FND/Law/LegalCapacity.rdf` | 法律能力本体（Legal Capacity Ontology） | 定义法律能力、缔约能力、签章权等概念，刻画主体从事法律行为的资格。 |
| `FND/Places/Addresses.rdf` | 地址本体（Addresses Ontology） | 定义邮政地址及其组成部分，为机构注册地、通讯地址建模。 |
| `FND/ProductsAndServices/ProductsAndServices.rdf` | 产品与服务本体（Products and Services Ontology） | 定义产品、服务及其提供者与客户的通用关系。 |
| `FND/Relations/Relations.rdf` | 关系本体（Relations Ontology） | FIBO 最底层的基础本体，定义参考（reference）、分类（classify）等通用关系与抽象概念，全库普遍依赖。 |
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |
| `https://www.omg.org/spec/Commons/Collections/` | OMG 通用集合本体（OMG Commons Collections） | Commons 库中的集合本体，定义集合、成员等通用概念。 |
| `https://www.omg.org/spec/Commons/ContextualDesignators/` | OMG 通用语境指称本体（OMG Commons Contextual Designators） | Commons 库中的语境指称本体，定义「在某个语境下指代某物的名称/符号」，是地址、账户号码等语境相关标识的基础。 |
| `https://www.omg.org/spec/Commons/DatesAndTimes/` | OMG 通用日期与时间本体（OMG Commons Dates and Times） | Commons 库中的日期时间本体，定义日期、期间、时间点等通用时间概念。 |
| `https://www.omg.org/spec/Commons/Designators/` | OMG 通用指称符本体（OMG Commons Designators） | Commons 库中的指称符本体，定义名称、标识符等「指代某物的符号」的通用概念。 |
| `https://www.omg.org/spec/Commons/Identifiers/` | OMG 通用标识符本体（OMG Commons Identifiers） | Commons 库中的标识符本体，定义标识符及其编码方案的通用概念。 |
| `https://www.omg.org/spec/Commons/Locations/` | OMG 通用位置本体（OMG Commons Locations） | Commons 库中的位置本体，定义地理位置、地点的通用概念。 |
| `https://www.omg.org/spec/Commons/Organizations/` | OMG 通用组织本体（OMG Commons Organizations） | Commons 库中的组织本体，定义组织、组织成员与组织结构的通用概念。 |
| `https://www.omg.org/spec/Commons/RegistrationAuthorities/` | OMG 通用登记主管机构本体（OMG Commons Registration Authorities） | Commons 库中的登记主管机构本体，定义负责登记注册的主管机构及其登记行为的通用概念。 |
| `https://www.omg.org/spec/Commons/RegulatoryAgencies/` | OMG 通用监管机构本体（OMG Commons Regulatory Agencies） | Commons 库中的监管机构本体，定义监管机构及其监管职权的通用概念。 |
| `https://www.omg.org/spec/Commons/RolesAndCompositions/` | OMG 通用角色与构成本体（OMG Commons Roles and Compositions） | Commons 库中的角色本体，定义角色及整体—部分构成关系的通用概念。 |
| `https://www.omg.org/spec/LCC/Countries/ISO3166-1-CountryCodes/` | LCC ISO 3166-1 国家代码（ISO 3166-1 Country Codes） | LCC 中 ISO 3166-1 标准的国家/地区代码个体集（如 CN、US、MX），供法域与地址建模引用。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-US/` | LCC ISO 3166-2 子分区代码·US（ISO 3166-2 Subdivision Codes for 美国） | LCC 中 ISO 3166-2 标准下美国的省/州级行政区代码个体集。 |

## 4. 文件

- 官方 RDF/XML：`FinancialInstitutionExamples.rdf`
- 中文 Turtle：`FinancialInstitutionExamples.ttl`