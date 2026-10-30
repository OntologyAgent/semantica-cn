# FIBO 生产版总入口·含参考数据（About FIBO Production, Including Reference Data）聚合说明

本文档对应 `AboutFIBOProd-IncludingReferenceData.rdf` / `AboutFIBOProd-IncludingReferenceData.ttl`。

## 1. 本文件是什么

在生产版基础上额外包含全部参考数据个体（国家代码、市场个体、监管机构等），是内容最全、加载最重的入口。

从机制上说，这是一个聚合入口（load-all）文件：它本身不定义任何新的类或属性，只通过 `owl:imports` 把一组本体打包在一起。应用只要导入这一个文件，推理机就会把它列出的所有本体一次性加载进来，免去逐个声明的麻烦。因此它的价值不在「内容」，而在「组合」——组合方式本身就表达了发布方的意图（例如按域打包、按区域扩展打包、按是否含参考数据打包）。

## 2. 聚合的本地本体（148 个）

以下本体均可在本目录结构中找到同名 `.rdf` 文件及配套中文文档：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `ACTUS/ACTUSTaxonomy.rdf` | ACTUS 受控词汇本体（ACTUS Controlled Vocabulary） | 收录 ACTUS 标准合约类型（如本金摊还型年金合约 PAM、到期一次偿还合约 NAM）的受控词汇。 |
| `ACTUS/ACTUSContractTerms.rdf` | ACTUS 合约条款本体（ACTUS Contract Terms Ontology） | 定义 ACTUS（算法合约类型统一标准）中的合约条款要素。 |
| `BE/FunctionalEntities/FunctionalEntities.rdf` | 功能实体本体（Functional Entities Ontology） | 定义「功能实体」：按其在商业中承担的功能（而非法律形式）刻画的实体，是出版方、登记机构等功能性主体的基础。 |
| `BE/FunctionalEntities/Publishers.rdf` | 出版方本体（Publishers Ontology） | 定义出版方及其出版物，用于标识金融信息与文档的发布来源。 |
| `BE/GovernmentEntities/AsianJurisdiction/CentralAsiaGovernmentEntitiesAndJurisdictions.rdf` | 中亚政府实体与法域本体（Central Asia Government Entities and Jurisdictions Ontology） | 收录中亚地区各国（如哈萨克斯坦等）的政体、政府与法域个体，用于确定实体注册或监管所属的法域。 |
| `BE/GovernmentEntities/AsianJurisdiction/EasternAsiaGovernmentEntitiesAndJurisdictions.rdf` | 东亚政府实体与法域本体（Eastern Asia Government Entities and Jurisdictions Ontology） | 收录东亚地区各国（中国、日本、韩国等）的政体、政府与法域个体。 |
| `BE/GovernmentEntities/AsianJurisdiction/SoutheasternAsiaGovernmentEntitiesAndJurisdictions.rdf` | 东南亚政府实体与法域本体（Southeastern Asia Government Entities and Jurisdictions Ontology） | 收录东南亚地区各国（新加坡、马来西亚、泰国等）的政体、政府与法域个体。 |
| `BE/GovernmentEntities/AsianJurisdiction/SouthernAsiaGovernmentEntitiesAndJurisdictions.rdf` | 南亚政府实体与法域本体（Southern Asia Government Entities and Jurisdictions Ontology） | 收录南亚地区各国（印度、巴基斯坦等）的政体、政府与法域个体。 |
| `BE/GovernmentEntities/AsianJurisdiction/WesternAsiaGovernmentEntitiesAndJurisdictions.rdf` | 西亚政府实体与法域本体（Western Asia Government Entities and Jurisdictions Ontology） | 收录西亚地区各国（沙特阿拉伯、阿联酋等）的政体、政府与法域个体。 |
| `BE/GovernmentEntities/EuropeanJurisdiction/EUGovernmentEntitiesAndJurisdictions.rdf` | 欧盟政府实体与法域本体（EU Government Entities and Jurisdictions Ontology） | 收录欧盟层面的政体、机构与法域个体（欧盟本身及其超国家机构）。 |
| `BE/GovernmentEntities/EuropeanJurisdiction/EasternEuropeGovernmentEntitiesAndJurisdictions.rdf` | 东欧政府实体与法域本体（Eastern Europe Government Entities and Jurisdictions Ontology） | 收录东欧各国（波兰、捷克、匈牙利等）的政体、政府与法域个体。 |
| `BE/GovernmentEntities/EuropeanJurisdiction/NorthernEuropeGovernmentEntitiesAndJurisdictions.rdf` | 北欧政府实体与法域本体（Northern Europe Government Entities and Jurisdictions Ontology） | 收录北欧各国（瑞典、挪威、丹麦等）的政体、政府与法域个体。 |
| `BE/GovernmentEntities/EuropeanJurisdiction/SouthernEuropeGovernmentEntitiesAndJurisdictions.rdf` | 南欧政府实体与法域本体（Southern Europe Government Entities and Jurisdictions Ontology） | 收录南欧各国（意大利、西班牙、希腊等）的政体、政府与法域个体。 |
| `BE/GovernmentEntities/EuropeanJurisdiction/UKGovernmentEntitiesAndJurisdictions.rdf` | 英国政府实体与法域本体（UK Government Entities and Jurisdictions Ontology） | 收录大不列颠及北爱尔兰联合王国的政体、政府与法域个体（英格兰、苏格兰、威尔士、北爱尔兰）。 |
| `BE/GovernmentEntities/EuropeanJurisdiction/WesternEuropeGovernmentEntitiesAndJurisdictions.rdf` | 西欧政府实体与法域本体（Western Europe Government Entities and Jurisdictions Ontology） | 收录西欧各国（法国、德国、荷兰等）的政体、政府与法域个体。 |
| `BE/GovernmentEntities/GovernmentEntities.rdf` | 政府实体本体（Government Entities Ontology） | 定义政府、政体（polity）、法域（jurisdiction）及政府实体的核心概念，是各区域政府实体本体的共同基础。 |
| `BE/GovernmentEntities/LatinAmericanJurisdiction/CentralAmericanGovernmentEntitiesAndJurisdictions.rdf` | 中美洲政府实体与法域本体（Central American Government Entities and Jurisdictions Ontology） | 收录中美洲各国（巴拿马、哥斯达黎加等）的政体、政府与法域个体。 |
| `BE/GovernmentEntities/LatinAmericanJurisdiction/SouthAmericanGovernmentEntitiesAndJurisdictions.rdf` | 南美洲政府实体与法域本体（South American Government Entities and Jurisdictions Ontology） | 收录南美洲各国（巴西、阿根廷等）的政体、政府与法域个体。 |
| `BE/GovernmentEntities/NorthAmericanJurisdiction/CAGovernmentEntitiesAndJurisdictions.rdf` | 加拿大政府实体与法域本体（Canadian Government Entities and Jurisdictions Ontology） | 收录加拿大的政体、联邦与省政府、法域个体。 |
| `BE/GovernmentEntities/NorthAmericanJurisdiction/CaribbeanGovernmentEntitiesAndJurisdictions.rdf` | 加勒比政府实体与法域本体（Caribbean Government Entities and Jurisdictions Ontology） | 收录加勒比地区各国与属地（开曼群岛、百慕大等）的政体、政府与法域个体。 |
| `BE/GovernmentEntities/NorthAmericanJurisdiction/MXGovernmentEntitiesAndJurisdictions.rdf` | 墨西哥政府实体与法域本体（Mexican Government Entities and Jurisdictions Ontology） | 收录墨西哥的政体、政府与法域个体。 |
| `BE/GovernmentEntities/NorthAmericanJurisdiction/USGovernmentEntitiesAndJurisdictions.rdf` | 美国政府实体与法域本体（US Government Entities and Jurisdictions Ontology） | 收录美国的政体、联邦与各州政府、法域个体，是北美金融建模最常用的法域参考数据。 |
| `BE/LegalEntities/CorporateBodies.rdf` | 法人团体本体（Corporate Bodies Ontology） | 定义依法设立、具有独立法律人格的法人团体（corporate body），是股份有限公司等具体法人类型的上位概念。 |
| `BE/LegalEntities/FormalBusinessOrganizations.rdf` | 正式商业组织本体（Formal Business Organizations Ontology） | 定义以营利为目的、依法注册的正式商业组织，连接法律实体与其商业功能。 |
| `BE/LegalEntities/LEIEntities.rdf` | LEI 法人实体本体（Legal Entity Identifier Entities Ontology） | 定义持有全球法人识别编码（LEI）的法人实体，对接 ISO 17442 标准的 LEI 体系。 |
| `BE/LegalEntities/LegalPersons.rdf` | 法律主体本体（Legal Persons Ontology） | 定义法律主体（legal person）与法定实体（legal entity）的核心概念：能持有权利义务、可起诉与被诉的主体。 |
| `BE/OwnershipAndControl/ControlParties.rdf` | 控制方本体（Control Parties Ontology） | 定义处于控制关系中的各方角色：控制方、被控制方、实际控制人等。 |
| `BE/OwnershipAndControl/CorporateControl.rdf` | 公司控制本体（Corporate Control Ontology） | 定义公司层面的控制关系：控股股东、多数/少数控制、表决权控制等。 |
| `BE/OwnershipAndControl/CorporateOwnership.rdf` | 公司所有权本体（Corporate Ownership Ontology） | 定义公司层面的所有权关系：股东、股份持有与受益所有权。 |
| `BE/OwnershipAndControl/Executives.rdf` | 高管本体（Executives Ontology） | 定义公司高管（executive）、董事会成员及其职务角色，刻画「谁在管理公司」。 |
| `BE/OwnershipAndControl/OwnershipParties.rdf` | 所有权方本体（Ownership Parties Ontology） | 定义所有权关系中的各方角色：所有者、受益所有人、名义持有人等。 |
| `BE/Partnerships/Partnerships.rdf` | 合伙本体（Partnerships Ontology） | 定义合伙企业及普通合伙、有限合伙等形态，刻画合伙人之间的权利义务。 |
| `BE/PrivateLimitedCompanies/PrivateLimitedCompanies.rdf` | 私人有限公司本体（Private Limited Companies Ontology） | 定义私人有限公司（private limited company）这类不公开募股的有限责任公司形态。 |
| `BE/SoleProprietorships/SoleProprietorships.rdf` | 独资经营本体（Sole Proprietorships Ontology） | 定义由单一自然人拥有和经营的独资企业形态。 |
| `BE/Trusts/Trusts.rdf` | 信托本体（Trusts Ontology） | 定义信托（trust）及委托人、受托人与受益人之间的信托关系。 |
| `CAE/CorporateEvents/CorporateActions.rdf` | 企业行动本体（Corporate Actions Ontology） | 定义企业行动（corporate action）：上市公司发起的、影响股东或证券的事件，如分红、拆股、并购。 |
| `DER/CreditDerivatives/CreditDefaultSwaps.rdf` | 信用违约互换本体（Credit Default Swaps Ontology） | 定义信用违约互换（CDS）：保护买方与卖方、参考实体、信用事件与结算方式。 |
| `DER/DerivativesContracts/CommoditiesContracts.rdf` | 大宗商品合约本体（Commodities Contracts Ontology） | 定义以大宗商品（能源、金属、农产品等）为标的的衍生品合约。 |
| `DER/DerivativesContracts/CurrencyContracts.rdf` | 外汇合约本体（Currency Contracts Ontology） | 定义以外汇为标的的衍生品合约：外汇远期、货币互换等。 |
| `DER/DerivativesContracts/DerivativesBasics.rdf` | 衍生品基础本体（Derivatives Basics Ontology） | 定义衍生品合约（derivatives contract）的核心概念：标的资产、行权、到期等，是 DER 域的根基。 |
| `DER/DerivativesContracts/DerivativesMasterAgreements.rdf` | 衍生品主协议本体（Derivatives Master Agreements Ontology） | 定义 ISDA 主协议等场外衍生品主协议（master agreement）及其条款结构。 |
| `DER/DerivativesContracts/ExoticOptions.rdf` | 奇异期权本体（Exotic Options Ontology） | 定义障碍期权、亚式期权等非标准化（奇异）期权。 |
| `DER/DerivativesContracts/FuturesAndForwards.rdf` | 期货与远期本体（Futures and Forwards Ontology） | 定义期货（futures）与远期（forwards）合约：标准化与非标准化的远期交割安排。 |
| `DER/DerivativesContracts/Options.rdf` | 期权本体（Options Ontology） | 定义期权（option）：买方权利、行权价、到期日、看涨与看跌等核心结构。 |
| `DER/DerivativesContracts/RightsAndWarrants.rdf` | 权利与权证本体（Rights and Warrants Ontology） | 定义认股权证（warrant）、配股权（rights）等赋予持有人购买权利的证券。 |
| `DER/DerivativesContracts/StructuredInstruments.rdf` | 结构化工具本体（Structured Instruments Ontology） | 定义结构化金融工具：由多个成分组合而成、现金流结构定制的工具。 |
| `DER/DerivativesContracts/Swaps.rdf` | 互换本体（Swaps Ontology） | 定义互换（swap）合约的通用结构：互换腿（swap leg）、现金流交换与名义本金。 |
| `DER/DerivativesContracts/SwapsIndividuals.rdf` | 互换个体本体（Swaps Individuals Ontology） | 收录标准化互换合约的参考个体（如标准利率互换的市场约定）。 |
| `DER/RateDerivatives/IRSwaps.rdf` | 利率互换本体（Interest Rate Swaps Ontology） | 定义利率互换（IRS）：固定利率与浮动利率现金流的交换结构。 |
| `DER/RateDerivatives/RateDerivatives.rdf` | 利率衍生品本体（Rate Derivatives Ontology） | 定义以利率为标的的衍生品的通用概念。 |
| `DER/SecurityBasedDerivatives/SecurityBasedDerivatives.rdf` | 证券类衍生品本体（Security-Based Derivatives Ontology） | 定义以单个证券或证券组合为标的的衍生品。 |
| `DER/SecurityBasedDerivatives/EquitySwaps.rdf` | 股权互换本体（Equity Swaps Ontology） | 定义股权互换（equity swap）：以股票或股指收益与利率现金流交换的合约。 |
| `FBC/DebtAndEquities/CreditEvents.rdf` | 信用事件本体（Credit Events Ontology） | 定义信用事件（credit event）：破产、拒付、重组等会触发信用衍生品结算的事件类型。 |
| `FBC/DebtAndEquities/Debt.rdf` | 债务本体（Debt Ontology） | 定义债务（debt）与债权债务关系的核心概念：借款人、贷款人、本金与利息义务。 |
| `FBC/DebtAndEquities/Guaranty.rdf` | 担保本体（Guaranty Ontology） | 定义担保（guaranty）：担保人、被担保债务与担保范围。 |
| `FBC/FinancialInstruments/FinancialInstruments.rdf` | 金融工具本体（Financial Instruments Ontology） | FIBO 核心本体之一，定义金融工具（financial instrument）的通用概念：可交易、代表某种权利义务的合同工具，是证券、衍生品等具体工具的共同基础。 |
| `FBC/FinancialInstruments/InstrumentPricing.rdf` | 工具定价本体（Instrument Pricing Ontology） | 定义金融工具的价格、报价与估值概念。 |
| `FBC/FinancialInstruments/Settlement.rdf` | 结算本体（Settlement Ontology） | 定义交易结算（settlement）：券款对付、结算日期与结算方式。 |
| `FBC/FunctionalEntities/BusinessCenters.rdf` | 商业中心本体（Business Centers Ontology） | 定义金融中心、商业中心等功能性地点概念，用于确定市场所在地与营业日历。 |
| `FBC/FunctionalEntities/BusinessCentersIndividuals.rdf` | 商业中心个体本体（Business Centers Individuals） | 收录全球主要商业中心（如纽约、伦敦、东京）的参考个体。 |
| `FBC/FunctionalEntities/BusinessRegistries.rdf` | 商业登记机构本体（Business Registries Ontology） | 定义商业登记机构（如公司注册处）及其登记职能。 |
| `FBC/FunctionalEntities/CommercialRegistrationAuthorities.rdf` | 商事登记主管机关本体（Commercial Registration Authorities Ontology） | 定义负责商事登记的主管机关及其维护的登记记录。 |
| `FBC/FunctionalEntities/EuropeanEntities/EUFinancialServicesEntities.rdf` | 欧盟金融服务实体本体（EU Financial Services Entities Ontology） | 定义欧盟法域下的金融服务机构类型与个体。 |
| `FBC/FunctionalEntities/EuropeanEntities/EURegulatoryAgencies.rdf` | 欧盟监管机构本体（EU Regulatory Agencies Ontology） | 收录欧盟层面的金融监管机构个体（如欧洲央行、欧洲证券和市场管理局 ESMA）。 |
| `FBC/FunctionalEntities/EuropeanEntities/EuropeanFinancialServicesEntitiesIndividuals.rdf` | 欧洲金融服务实体个体本体（European Financial Services Entities Individuals Ontology） | 收录欧洲各国金融服务机构与市场的参考个体。 |
| `FBC/FunctionalEntities/FinancialServicesEntities.rdf` | 金融服务实体本体（Financial Services Entities Ontology） | FBC 域核心本体，定义金融服务机构（银行、券商、保险公司、资管机构等）的功能分类体系。 |
| `FBC/FunctionalEntities/InternationalRegistriesAndAuthorities.rdf` | 国际登记与主管机构本体（International Registries and Authorities Ontology） | 收录国际性登记机构与主管当局的参考个体。 |
| `FBC/FunctionalEntities/Markets.rdf` | 市场本体（Markets Ontology） | 定义金融市场（market）：交易所、场外市场及其功能。 |
| `FBC/FunctionalEntities/MarketsIndividuals.rdf` | 市场个体本体（Markets Individuals） | 收录全球主要金融市场的参考个体。 |
| `FBC/FunctionalEntities/NorthAmericanEntities/CAFinancialServicesEntities.rdf` | 加拿大金融服务实体本体（Canadian Financial Services Entities Ontology） | 定义加拿大法域下的金融服务机构类型与个体。 |
| `FBC/FunctionalEntities/NorthAmericanEntities/CARegulatoryAgencies.rdf` | 加拿大监管机构本体（Canadian Regulatory Agencies Ontology） | 收录加拿大金融监管机构个体（如加拿大金融机构监管署 OSFI）。 |
| `FBC/FunctionalEntities/NorthAmericanEntities/USFinancialServicesEntities.rdf` | 美国金融服务实体本体（US Financial Services Entities Ontology） | 定义美国法域下的金融服务机构类型与个体。 |
| `FBC/FunctionalEntities/NorthAmericanEntities/USRegulatoryAgencies.rdf` | 美国监管机构本体（US Regulatory Agencies Ontology） | 收录美国金融监管机构个体（如美联储、证监会 SEC、货币监理署 OCC）。 |
| `FBC/FunctionalEntities/RegulatoryAgencies.rdf` | 监管机构本体（Regulatory Agencies Ontology） | 定义金融监管机构（regulatory agency）及其监管职能的通用概念。 |
| `FBC/ProductsAndServices/ClientsAndAccounts.rdf` | 客户与账户本体（Clients and Accounts Ontology） | 定义金融机构的客户、账户及账户持有关系。 |
| `FBC/ProductsAndServices/FinancialProductsAndServices.rdf` | 金融产品与服务本体（Financial Products and Services Ontology） | 定义金融产品（financial product）与金融服务（financial service）及其提供、购买关系。 |
| `FND/Accounting/CurrencyAmount.rdf` | 货币金额本体（Currency Amount Ontology） | 定义「金额＋币种」的货币金额（currency amount）表示，是 FIBO 中表达价格、债务金额、付款额等一切带币种数值的基础构件。 |
| `FND/Accounting/ISO4217-CurrencyCodes.rdf` | ISO 4217 货币代码本体（ISO 4217-1 Currency Codes Ontology） | 收录 ISO 4217-1 标准的全部货币代码个体（如 USD、CNY、EUR），为货币金额提供标准化的币种取值。 |
| `FND/AgentsAndPeople/People.rdf` | 人员本体（People Ontology） | 定义自然人（person）的核心属性：姓名、出生日期、国籍、身份标识与联系方式，为雇员、客户、签署人等角色提供「人」的基础模型。 |
| `FND/Agreements/Agreements.rdf` | 协议本体（Agreements Ontology） | 定义两个或以上参与方之间协议（agreement）的通用概念：协议的当事方、条款、生效与终止，是合同等一切契约性安排的上位模型。 |
| `FND/Agreements/Contracts.rdf` | 合同本体（Contracts Ontology） | 在协议之上定义具有法律约束力的合同（contract）：合同当事方、合同条款、义务与权利，是金融工具与交易合同建模的基石。 |
| `FND/Arrangements/Arrangements.rdf` | 安排本体（Arrangements Ontology） | 定义「安排」（arrangement）这一抽象概念：把若干事物按某种结构组织起来的方式，是分类方案、标识方案、生命周期等概念的上位基础。 |
| `FND/Arrangements/Assessments.rdf` | 评估本体（Assessments Ontology） | 定义评估活动、评估结果与评估方的通用结构，为信用评级、风险打分等判断性活动提供基础模型。 |
| `FND/Arrangements/ClassificationSchemes.rdf` | 分类方案本体（Classification Schemes Ontology） | 定义分类方案（classification scheme）、类别及「将事物归入类别」的关系，支撑证券分类、行业分类等具体分类体系。 |
| `FND/Arrangements/Documents.rdf` | 文档本体（Documents Ontology） | 定义文档、文档类型及文档与其所记载内容的关系，为合同文本、募集说明书等法律文书建模。 |
| `FND/Arrangements/IdentifiersAndIndices.rdf` | 标识符与索引本体（Identifiers and Indices Ontology） | 定义标识符（identifier）、标识方案与索引（index）的基本结构，是 ISIN、LEI、CUSIP 等编码体系建模的基础。 |
| `FND/Arrangements/Lifecycles.rdf` | 生命周期本体（Lifecycles Ontology） | 定义生命周期、生命周期阶段与状态转移，用于描述合同、金融工具、机构从创设到终止的演化过程。 |
| `FND/Arrangements/Ratings.rdf` | 评级本体（Ratings Ontology） | 定义评级（rating）、评级量表与评级方的通用结构，是信用评级等具体评级体系的基础。 |
| `FND/Arrangements/Reporting.rdf` | 报告本体（Reporting Ontology） | 定义报告、报告方与报告内容的关系，支撑监管报告、财务报告等报送场景。 |
| `FND/DatesAndTimes/BusinessDates.rdf` | 营业日期本体（Business Dates Ontology） | 定义营业日、营业日历与日期调整规则（如顺延约定），支撑金融合同中的营业日计算。 |
| `FND/DatesAndTimes/FinancialDates.rdf` | 金融日期本体（Financial Dates Ontology） | 定义金融语境下的日期与期间概念：结算日、付息日、到期日、日计数基准等。 |
| `FND/DatesAndTimes/Occurrences.rdf` | 事件与发生本体（Occurrences Ontology） | 定义「发生」（occurrence）、事件与触发条件，用于表达企业行动、信用事件等「发生了什么」。 |
| `FND/GoalsAndObjectives/Objectives.rdf` | 目标本体（Objectives Ontology） | 定义目标（objective）及其与组织、计划的关系，用于表达机构的经营目标与投资目标。 |
| `FND/Law/LegalCapacity.rdf` | 法律能力本体（Legal Capacity Ontology） | 定义法律能力、缔约能力、签章权等概念，刻画主体从事法律行为的资格。 |
| `FND/Law/LegalCore.rdf` | 法律核心本体（Legal Core Ontology） | 定义法域（jurisdiction）、法律、法规等核心法律概念，为监管主体与适用法律建模。 |
| `FND/Organizations/FormalOrganizations.rdf` | 正式组织本体（Formal Organizations Ontology） | 定义正式组织、组织成员与组织内部角色，是公司、政府机构等组织形态建模的基础。 |
| `FND/OwnershipAndControl/Control.rdf` | 控制本体（Control Ontology） | 定义「控制」关系：控制方、被控制方与控制程度，用于公司治理与合并报表判断。 |
| `FND/OwnershipAndControl/Ownership.rdf` | 所有权本体（Ownership Ontology） | 定义「拥有」关系：所有者、被拥有资产及所有权份额。 |
| `FND/OwnershipAndControl/OwnershipAndControl.rdf` | 所有权与控制本体（Ownership and Control Ontology） | 综合所有权与控制关系，刻画「谁拥有、谁控制」的基本格局。 |
| `FND/Parties/Parties.rdf` | 参与方本体（Parties Ontology） | 定义参与方（party）、独立主体（autonomous agent）与「角色扮演」（party in role），是 FIBO 全库使用最广的基础本体之一。 |
| `FND/Places/Addresses.rdf` | 地址本体（Addresses Ontology） | 定义邮政地址及其组成部分，为机构注册地、通讯地址建模。 |
| `FND/Places/RealProperty.rdf` | 不动产本体（Real Property Ontology） | 定义不动产（real property）及其与地点、所有权的关系，支撑抵押贷款与房地产金融。 |
| `FND/Places/VirtualPlaces.rdf` | 虚拟地点本体（Virtual Places Ontology） | 定义网站、电子邮箱等虚拟地点概念，补充物理地点之外的「场所」表达。 |
| `FND/Places/NorthAmerica/USPostalServiceAddresses.rdf` | 美国邮政地址本体（U.S. Postal Service Addresses Ontology） | 定义符合美国邮政服务（USPS）规范的地址结构：街道、城市、州与邮编。 |
| `FND/Places/NorthAmerica/USPostalServiceAddressesIndividuals.rdf` | 美国邮政地址个体本体（U.S. Postal Service Addresses Individuals Ontology） | 收录美国州、地区等地址参考数据个体，供美国地址建模时引用。 |
| `FND/ProductsAndServices/PaymentsAndSchedules.rdf` | 付款与计划表本体（Payments and Schedules Ontology） | 定义付款、付款计划表（payment schedule）及其日期与金额结构，是贷款还款、债券付息建模的基础。 |
| `FND/ProductsAndServices/ProductsAndServices.rdf` | 产品与服务本体（Products and Services Ontology） | 定义产品、服务及其提供者与客户的通用关系。 |
| `FND/Relations/Relations.rdf` | 关系本体（Relations Ontology） | FIBO 最底层的基础本体，定义参考（reference）、分类（classify）等通用关系与抽象概念，全库普遍依赖。 |
| `FND/Utilities/Analytics.rdf` | 分析本体（Analytics Ontology） | 定义分析工具、度量与比率的通用概念，支撑指标与模型的表达。 |
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `IND/EconomicIndicators/EconomicIndicators.rdf` | 经济指标本体（Economic Indicators Ontology） | 定义宏观经济指标（GDP、CPI、失业率等）的通用结构：发布机构、发布频率与数值。 |
| `IND/EconomicIndicators/NorthAmericanIndicators/CAEconomicIndicators.rdf` | 加拿大经济指标本体（Canadian Economic Indicators Ontology） | 收录加拿大官方发布的经济指标个体。 |
| `IND/EconomicIndicators/NorthAmericanIndicators/USEconomicIndicators.rdf` | 美国经济指标本体（US Economic Indicators Ontology） | 收录美国官方发布的经济指标个体（如非农就业、CPI、GDP 系列）。 |
| `IND/ForeignExchange/ForeignExchange.rdf` | 外汇本体（Foreign Exchange Ontology） | 定义外汇、汇率（exchange rate）与货币对的概念。 |
| `IND/Indicators/Indicators.rdf` | 指标本体（Indicators Ontology） | 定义「指标」（indicator）的通用概念：对某现象的可度量表示，是经济指标、利率等的上位模型。 |
| `IND/InterestRates/InterestRates.rdf` | 利率本体（Interest Rates Ontology） | 定义利率（interest rate）的结构：基准利率、利差、期限与重置机制。 |
| `IND/InterestRates/CommonInterestRates.rdf` | 常用利率本体（Common Interest Rates Ontology） | 收录市场常用参考利率个体（如各期限基准、政策利率）。 |
| `IND/InterestRates/MarketDataProviders.rdf` | 市场数据提供商本体（Market Data Providers Ontology） | 定义市场数据提供商（交易所、资讯商等）及其发布的数据。 |
| `IND/MarketIndices/BasketIndices.rdf` | 篮子指数本体（Basket Indices Ontology） | 定义以一篮子成分为基础的指数：成分、权重与计算方法。 |
| `LOAN/LoansGeneral/Loans.rdf` | 贷款本体（Loans Ontology） | LOAN 域核心本体，定义贷款（loan）的通用结构：借款人、贷款人、本金、利率与还款安排。 |
| `LOAN/LoansSpecific/CardAccounts.rdf` | 卡账户本体（Card Accounts Ontology） | 定义信用卡、借记卡账户及其信贷特征。 |
| `LOAN/LoansSpecific/CommercialLoans.rdf` | 商业贷款本体（Commercial Loans Ontology） | 定义面向企业的商业贷款。 |
| `LOAN/LoansSpecific/ConsumerLoans.rdf` | 消费贷款本体（Consumer Loans Ontology） | 定义面向个人消费者的贷款。 |
| `LOAN/LoansSpecific/GreenLoans.rdf` | 绿色贷款本体（Green Loans Ontology） | 定义符合绿色融资原则（资金投向环保项目）的绿色贷款。 |
| `LOAN/LoansSpecific/StudentLoans.rdf` | 学生贷款本体（Student Loans Ontology） | 定义用于教育支出的学生贷款。 |
| `LOAN/RealEstateLoans/Mortgages.rdf` | 抵押贷款本体（Mortgages Ontology） | 定义以不动产为抵押的贷款：抵押物、抵押登记与止赎。 |
| `SEC/Debt/AssetBackedSecurities.rdf` | 资产支持证券本体（Asset-backed Securities Ontology） | 定义以资产池（如贷款、应收账款）为支持的资产支持证券（ABS）。 |
| `SEC/Debt/Bonds.rdf` | 债券本体（Bonds Ontology） | 定义债券（bond）：期限、票面利率、付息方式与偿还结构。 |
| `SEC/Debt/DebtInstruments.rdf` | 债务工具本体（Debt Instruments Ontology） | 定义债务工具（debt instrument）的通用概念：可交易的债权凭证，是债券、票据等的上位模型。 |
| `SEC/Debt/DistributedLoans.rdf` | 分销贷款本体（Distributed Loans Ontology） | 定义银团贷款等被分销给多个持有人持有的贷款。 |
| `SEC/Debt/ExerciseConventions.rdf` | 行权惯例本体（Exercise Conventions Ontology） | 定义债务工具中嵌入期权的行权惯例：美式、欧式、百慕大式。 |
| `SEC/Debt/PoolBackedSecurities.rdf` | 池支持证券本体（Pool-backed Securities Ontology） | 定义以资产池为支持的证券的通用结构：资产池、分层（tranche）与过手安排。 |
| `SEC/Debt/TradedShortTermDebt.rdf` | 短期交易债务本体（Traded Short-Term Debt Ontology） | 定义货币市场工具等短期可交易债务：商业票据、国库券等。 |
| `SEC/Equities/DepositaryReceipts.rdf` | 存托凭证本体（Depositary Receipts Ontology） | 定义存托凭证（DR，如 ADR、GDR）：代表境外公司股票的可交易凭证。 |
| `SEC/Equities/EquityCFIClassificationIndividuals.rdf` | 股票 CFI 分类个体本体（Equities CFI Classification Individuals Ontology） | 收录 ISO 10962 金融工具分类（CFI）中股票类别的参考个体（普通股、优先股等类别代码）。 |
| `SEC/Equities/EquityInstruments.rdf` | 股权工具本体（Equity Instruments Ontology） | 定义股票等股权工具：普通股、优先股及其附带的权利。 |
| `SEC/Funds/Funds.rdf` | 基金本体（Funds Ontology） | 定义投资基金（fund）：基金份额、净值与管理结构。 |
| `SEC/Securities/EuropeanSecurities/EUSecuritiesRestrictions.rdf` | 欧盟证券限制本体（EU Securities Restrictions Ontology） | 定义欧盟法域下的证券发行与交易限制。 |
| `SEC/Securities/NorthAmericanSecurities/USSecuritiesRestrictions.rdf` | 美国证券限制本体（US Securities Restrictions Ontology） | 定义美国证券法下的发行与转售限制（如 Rule 144、Regulation S）。 |
| `SEC/Securities/Baskets.rdf` | 篮子本体（Baskets Ontology） | 定义证券篮子（basket）：作为整体交易或定价的一组证券。 |
| `SEC/Securities/ParametricSchedules.rdf` | 参数化计划表本体（Parametric Schedules Ontology） | 定义由参数驱动的日期与金额计划表（如分期偿还表、付息表）。 |
| `SEC/Securities/Pools.rdf` | 证券池本体（Securities Pools Ontology） | 定义证券池（pool）：归集起来作为证券化基础的一组资产。 |
| `SEC/Securities/SecuritiesClassification.rdf` | 证券分类本体（Securities Classification Ontology） | 定义证券分类方案：按 CFI 代码、按资产类别等对证券归类。 |
| `SEC/Securities/SecuritiesIdentification.rdf` | 证券识别本体（Securities Identification Ontology） | 定义证券标识符（ISIN、CUSIP、SEDOL 等）及其编码方案的结构。 |
| `SEC/Securities/SecuritiesIdentificationIndividuals.rdf` | 证券识别个体本体（Securities Identification Individuals Ontology） | 收录证券标识方案的参考个体（如 ISIN、CUSIP 编码方案本身）。 |
| `SEC/Securities/SecuritiesIssuance.rdf` | 证券发行本体（Securities Issuance Ontology） | 定义证券发行（issuance）：发行人、发行条款与发行结果。 |
| `SEC/Securities/SecuritiesListings.rdf` | 证券上市本体（Securities Listings Ontology） | 定义证券在交易所上市（listing）及其上市状态。 |
| `SEC/Securities/SecuritiesRestrictions.rdf` | 证券限制本体（Securities Restrictions Ontology） | 定义证券发行与转让限制的通用概念，是各法域具体限制本体的基础。 |

## 3. 外部依赖（81 个，不在 FIBO 仓库内）

以下导入来自 OMG 的外部本体库，不在 FIBO 仓库中，加载时需从 spec.edmcouncil.org / omg.org 获取：

| 外部本体 | 中文名称 | 简介 |
|---|---|---|
| `https://www.omg.org/spec/LCC/Countries/ISO3166-2-SubdivisionCodes/` | LCC ISO 3166-2 子分区代码总集（ISO 3166-2 Subdivision Codes） | OMG 国家语言代码库（LCC）中 ISO 3166-2 国家/地区子分区代码的总集本体，按国家拆分为各子文件。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-AD/` | LCC ISO 3166-2 子分区代码·AD（ISO 3166-2 Subdivision Codes for 安道尔） | LCC 中 ISO 3166-2 标准下安道尔的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-AL/` | LCC ISO 3166-2 子分区代码·AL（ISO 3166-2 Subdivision Codes for 阿尔巴尼亚） | LCC 中 ISO 3166-2 标准下阿尔巴尼亚的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-AT/` | LCC ISO 3166-2 子分区代码·AT（ISO 3166-2 Subdivision Codes for 奥地利） | LCC 中 ISO 3166-2 标准下奥地利的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-BA/` | LCC ISO 3166-2 子分区代码·BA（ISO 3166-2 Subdivision Codes for 波斯尼亚和黑塞哥维那） | LCC 中 ISO 3166-2 标准下波斯尼亚和黑塞哥维那的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-BE/` | LCC ISO 3166-2 子分区代码·BE（ISO 3166-2 Subdivision Codes for 比利时） | LCC 中 ISO 3166-2 标准下比利时的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-BG/` | LCC ISO 3166-2 子分区代码·BG（ISO 3166-2 Subdivision Codes for 保加利亚） | LCC 中 ISO 3166-2 标准下保加利亚的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-BY/` | LCC ISO 3166-2 子分区代码·BY（ISO 3166-2 Subdivision Codes for 白俄罗斯） | LCC 中 ISO 3166-2 标准下白俄罗斯的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-CH/` | LCC ISO 3166-2 子分区代码·CH（ISO 3166-2 Subdivision Codes for 瑞士） | LCC 中 ISO 3166-2 标准下瑞士的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-CZ/` | LCC ISO 3166-2 子分区代码·CZ（ISO 3166-2 Subdivision Codes for 捷克） | LCC 中 ISO 3166-2 标准下捷克的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-DE/` | LCC ISO 3166-2 子分区代码·DE（ISO 3166-2 Subdivision Codes for 德国） | LCC 中 ISO 3166-2 标准下德国的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-DK/` | LCC ISO 3166-2 子分区代码·DK（ISO 3166-2 Subdivision Codes for 丹麦） | LCC 中 ISO 3166-2 标准下丹麦的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-EE/` | LCC ISO 3166-2 子分区代码·EE（ISO 3166-2 Subdivision Codes for 爱沙尼亚） | LCC 中 ISO 3166-2 标准下爱沙尼亚的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-ES/` | LCC ISO 3166-2 子分区代码·ES（ISO 3166-2 Subdivision Codes for 西班牙） | LCC 中 ISO 3166-2 标准下西班牙的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-FI/` | LCC ISO 3166-2 子分区代码·FI（ISO 3166-2 Subdivision Codes for 芬兰） | LCC 中 ISO 3166-2 标准下芬兰的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-FR/` | LCC ISO 3166-2 子分区代码·FR（ISO 3166-2 Subdivision Codes for 法国） | LCC 中 ISO 3166-2 标准下法国的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-GB/` | LCC ISO 3166-2 子分区代码·GB（ISO 3166-2 Subdivision Codes for 英国） | LCC 中 ISO 3166-2 标准下英国的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-GG/` | LCC ISO 3166-2 子分区代码·GG（ISO 3166-2 Subdivision Codes for 根西岛） | LCC 中 ISO 3166-2 标准下根西岛的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-GR/` | LCC ISO 3166-2 子分区代码·GR（ISO 3166-2 Subdivision Codes for 希腊） | LCC 中 ISO 3166-2 标准下希腊的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-HR/` | LCC ISO 3166-2 子分区代码·HR（ISO 3166-2 Subdivision Codes for 克罗地亚） | LCC 中 ISO 3166-2 标准下克罗地亚的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-HU/` | LCC ISO 3166-2 子分区代码·HU（ISO 3166-2 Subdivision Codes for 匈牙利） | LCC 中 ISO 3166-2 标准下匈牙利的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-IE/` | LCC ISO 3166-2 子分区代码·IE（ISO 3166-2 Subdivision Codes for 爱尔兰） | LCC 中 ISO 3166-2 标准下爱尔兰的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-IS/` | LCC ISO 3166-2 子分区代码·IS（ISO 3166-2 Subdivision Codes for 冰岛） | LCC 中 ISO 3166-2 标准下冰岛的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-IT/` | LCC ISO 3166-2 子分区代码·IT（ISO 3166-2 Subdivision Codes for 意大利） | LCC 中 ISO 3166-2 标准下意大利的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-LI/` | LCC ISO 3166-2 子分区代码·LI（ISO 3166-2 Subdivision Codes for 列支敦士登） | LCC 中 ISO 3166-2 标准下列支敦士登的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-LT/` | LCC ISO 3166-2 子分区代码·LT（ISO 3166-2 Subdivision Codes for 立陶宛） | LCC 中 ISO 3166-2 标准下立陶宛的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-LU/` | LCC ISO 3166-2 子分区代码·LU（ISO 3166-2 Subdivision Codes for 卢森堡） | LCC 中 ISO 3166-2 标准下卢森堡的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-LV/` | LCC ISO 3166-2 子分区代码·LV（ISO 3166-2 Subdivision Codes for 拉脱维亚） | LCC 中 ISO 3166-2 标准下拉脱维亚的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-MC/` | LCC ISO 3166-2 子分区代码·MC（ISO 3166-2 Subdivision Codes for 摩纳哥） | LCC 中 ISO 3166-2 标准下摩纳哥的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-MD/` | LCC ISO 3166-2 子分区代码·MD（ISO 3166-2 Subdivision Codes for 摩尔多瓦） | LCC 中 ISO 3166-2 标准下摩尔多瓦的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-ME/` | LCC ISO 3166-2 子分区代码·ME（ISO 3166-2 Subdivision Codes for 黑山） | LCC 中 ISO 3166-2 标准下黑山的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-MK/` | LCC ISO 3166-2 子分区代码·MK（ISO 3166-2 Subdivision Codes for 北马其顿） | LCC 中 ISO 3166-2 标准下北马其顿的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-MT/` | LCC ISO 3166-2 子分区代码·MT（ISO 3166-2 Subdivision Codes for 马耳他） | LCC 中 ISO 3166-2 标准下马耳他的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-NL/` | LCC ISO 3166-2 子分区代码·NL（ISO 3166-2 Subdivision Codes for 荷兰） | LCC 中 ISO 3166-2 标准下荷兰的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-NO/` | LCC ISO 3166-2 子分区代码·NO（ISO 3166-2 Subdivision Codes for 挪威） | LCC 中 ISO 3166-2 标准下挪威的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-PL/` | LCC ISO 3166-2 子分区代码·PL（ISO 3166-2 Subdivision Codes for 波兰） | LCC 中 ISO 3166-2 标准下波兰的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-PT/` | LCC ISO 3166-2 子分区代码·PT（ISO 3166-2 Subdivision Codes for 葡萄牙） | LCC 中 ISO 3166-2 标准下葡萄牙的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-RO/` | LCC ISO 3166-2 子分区代码·RO（ISO 3166-2 Subdivision Codes for 罗马尼亚） | LCC 中 ISO 3166-2 标准下罗马尼亚的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-RS/` | LCC ISO 3166-2 子分区代码·RS（ISO 3166-2 Subdivision Codes for 塞尔维亚） | LCC 中 ISO 3166-2 标准下塞尔维亚的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-RU/` | LCC ISO 3166-2 子分区代码·RU（ISO 3166-2 Subdivision Codes for 俄罗斯） | LCC 中 ISO 3166-2 标准下俄罗斯的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-SE/` | LCC ISO 3166-2 子分区代码·SE（ISO 3166-2 Subdivision Codes for 瑞典） | LCC 中 ISO 3166-2 标准下瑞典的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-SI/` | LCC ISO 3166-2 子分区代码·SI（ISO 3166-2 Subdivision Codes for 斯洛文尼亚） | LCC 中 ISO 3166-2 标准下斯洛文尼亚的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-SJ/` | LCC ISO 3166-2 子分区代码·SJ（ISO 3166-2 Subdivision Codes for 斯瓦尔巴和扬马延） | LCC 中 ISO 3166-2 标准下斯瓦尔巴和扬马延的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-SK/` | LCC ISO 3166-2 子分区代码·SK（ISO 3166-2 Subdivision Codes for 斯洛伐克） | LCC 中 ISO 3166-2 标准下斯洛伐克的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-SM/` | LCC ISO 3166-2 子分区代码·SM（ISO 3166-2 Subdivision Codes for 圣马力诺） | LCC 中 ISO 3166-2 标准下圣马力诺的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-UA/` | LCC ISO 3166-2 子分区代码·UA（ISO 3166-2 Subdivision Codes for 乌克兰） | LCC 中 ISO 3166-2 标准下乌克兰的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-AG/` | LCC ISO 3166-2 子分区代码·AG（ISO 3166-2 Subdivision Codes for 安提瓜和巴布达） | LCC 中 ISO 3166-2 标准下安提瓜和巴布达的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-AS/` | LCC ISO 3166-2 子分区代码·AS（ISO 3166-2 Subdivision Codes for 美属萨摩亚） | LCC 中 ISO 3166-2 标准下美属萨摩亚的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-BB/` | LCC ISO 3166-2 子分区代码·BB（ISO 3166-2 Subdivision Codes for 巴巴多斯） | LCC 中 ISO 3166-2 标准下巴巴多斯的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-BQ/` | LCC ISO 3166-2 子分区代码·BQ（ISO 3166-2 Subdivision Codes for 荷兰加勒比区） | LCC 中 ISO 3166-2 标准下荷兰加勒比区的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-BS/` | LCC ISO 3166-2 子分区代码·BS（ISO 3166-2 Subdivision Codes for 巴哈马） | LCC 中 ISO 3166-2 标准下巴哈马的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-BZ/` | LCC ISO 3166-2 子分区代码·BZ（ISO 3166-2 Subdivision Codes for 伯利兹） | LCC 中 ISO 3166-2 标准下伯利兹的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-CA/` | LCC ISO 3166-2 子分区代码·CA（ISO 3166-2 Subdivision Codes for 加拿大） | LCC 中 ISO 3166-2 标准下加拿大的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-CR/` | LCC ISO 3166-2 子分区代码·CR（ISO 3166-2 Subdivision Codes for 哥斯达黎加） | LCC 中 ISO 3166-2 标准下哥斯达黎加的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-CU/` | LCC ISO 3166-2 子分区代码·CU（ISO 3166-2 Subdivision Codes for 古巴） | LCC 中 ISO 3166-2 标准下古巴的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-DM/` | LCC ISO 3166-2 子分区代码·DM（ISO 3166-2 Subdivision Codes for 多米尼克） | LCC 中 ISO 3166-2 标准下多米尼克的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-DO/` | LCC ISO 3166-2 子分区代码·DO（ISO 3166-2 Subdivision Codes for 多米尼加共和国） | LCC 中 ISO 3166-2 标准下多米尼加共和国的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-GD/` | LCC ISO 3166-2 子分区代码·GD（ISO 3166-2 Subdivision Codes for 格林纳达） | LCC 中 ISO 3166-2 标准下格林纳达的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-GL/` | LCC ISO 3166-2 子分区代码·GL（ISO 3166-2 Subdivision Codes for 格陵兰） | LCC 中 ISO 3166-2 标准下格陵兰的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-GP/` | LCC ISO 3166-2 子分区代码·GP（ISO 3166-2 Subdivision Codes for 瓜德罗普） | LCC 中 ISO 3166-2 标准下瓜德罗普的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-GT/` | LCC ISO 3166-2 子分区代码·GT（ISO 3166-2 Subdivision Codes for 危地马拉） | LCC 中 ISO 3166-2 标准下危地马拉的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-HN/` | LCC ISO 3166-2 子分区代码·HN（ISO 3166-2 Subdivision Codes for 洪都拉斯） | LCC 中 ISO 3166-2 标准下洪都拉斯的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-HT/` | LCC ISO 3166-2 子分区代码·HT（ISO 3166-2 Subdivision Codes for 海地） | LCC 中 ISO 3166-2 标准下海地的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-KN/` | LCC ISO 3166-2 子分区代码·KN（ISO 3166-2 Subdivision Codes for 圣基茨和尼维斯） | LCC 中 ISO 3166-2 标准下圣基茨和尼维斯的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-KY/` | LCC ISO 3166-2 子分区代码·KY（ISO 3166-2 Subdivision Codes for 开曼群岛） | LCC 中 ISO 3166-2 标准下开曼群岛的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-LC/` | LCC ISO 3166-2 子分区代码·LC（ISO 3166-2 Subdivision Codes for 圣卢西亚） | LCC 中 ISO 3166-2 标准下圣卢西亚的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-MF/` | LCC ISO 3166-2 子分区代码·MF（ISO 3166-2 Subdivision Codes for 法属圣马丁） | LCC 中 ISO 3166-2 标准下法属圣马丁的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-MP/` | LCC ISO 3166-2 子分区代码·MP（ISO 3166-2 Subdivision Codes for 北马里亚纳群岛） | LCC 中 ISO 3166-2 标准下北马里亚纳群岛的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-MX/` | LCC ISO 3166-2 子分区代码·MX（ISO 3166-2 Subdivision Codes for 墨西哥） | LCC 中 ISO 3166-2 标准下墨西哥的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-NI/` | LCC ISO 3166-2 子分区代码·NI（ISO 3166-2 Subdivision Codes for 尼加拉瓜） | LCC 中 ISO 3166-2 标准下尼加拉瓜的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-PA/` | LCC ISO 3166-2 子分区代码·PA（ISO 3166-2 Subdivision Codes for 巴拿马） | LCC 中 ISO 3166-2 标准下巴拿马的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-PM/` | LCC ISO 3166-2 子分区代码·PM（ISO 3166-2 Subdivision Codes for 圣皮埃尔和密克隆） | LCC 中 ISO 3166-2 标准下圣皮埃尔和密克隆的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-SV/` | LCC ISO 3166-2 子分区代码·SV（ISO 3166-2 Subdivision Codes for 萨尔瓦多） | LCC 中 ISO 3166-2 标准下萨尔瓦多的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-TC/` | LCC ISO 3166-2 子分区代码·TC（ISO 3166-2 Subdivision Codes for 特克斯和凯科斯群岛） | LCC 中 ISO 3166-2 标准下特克斯和凯科斯群岛的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-TT/` | LCC ISO 3166-2 子分区代码·TT（ISO 3166-2 Subdivision Codes for 特立尼达和多巴哥） | LCC 中 ISO 3166-2 标准下特立尼达和多巴哥的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-UM/` | LCC ISO 3166-2 子分区代码·UM（ISO 3166-2 Subdivision Codes for 美国本土外小岛屿） | LCC 中 ISO 3166-2 标准下美国本土外小岛屿的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-US/` | LCC ISO 3166-2 子分区代码·US（ISO 3166-2 Subdivision Codes for 美国） | LCC 中 ISO 3166-2 标准下美国的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-VC/` | LCC ISO 3166-2 子分区代码·VC（ISO 3166-2 Subdivision Codes for 圣文森特和格林纳丁斯） | LCC 中 ISO 3166-2 标准下圣文森特和格林纳丁斯的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-VG/` | LCC ISO 3166-2 子分区代码·VG（ISO 3166-2 Subdivision Codes for 英属维尔京群岛） | LCC 中 ISO 3166-2 标准下英属维尔京群岛的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/Regions/ISO3166-2-SubdivisionCodes-VI/` | LCC ISO 3166-2 子分区代码·VI（ISO 3166-2 Subdivision Codes for 美属维尔京群岛） | LCC 中 ISO 3166-2 标准下美属维尔京群岛的省/州级行政区代码个体集。 |
| `https://www.omg.org/spec/LCC/Countries/UN-M49-RegionCodes/` | LCC 联合国 M49 区域代码（UN-M49 Region Codes） | LCC 中联合国 M49 标准的地理区域代码个体（如东亚、西欧等区域编码）。 |

## 4. 文件

- 官方 RDF/XML：`AboutFIBOProd-IncludingReferenceData.rdf`
- 中文 Turtle：`AboutFIBOProd-IncludingReferenceData.ttl`