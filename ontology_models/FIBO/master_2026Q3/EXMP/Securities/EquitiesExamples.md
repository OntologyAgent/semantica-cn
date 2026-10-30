# 股票示例个体本体（Equities Example Individuals Ontology）说明

本文档对应 `EquitiesExamples.rdf` / `EquitiesExamples.ttl`。

![股票示例个体本体（Equities Example Individuals Ontology）结构图](EquitiesExamples-structure.png)

## 1. 本文件是什么

收录典型股票（上市公司普通股）的示例个体。

从机制上说，这是一个个体（individuals）文件：它本身不定义任何新的类或属性，装的全是命名个体（owl:NamedIndividual）——也就是一条条真实存在的实例数据（如具体的货币、市场、监管机构、法域）。它的 `owl:imports` 引入的是这些个体所属的类定义所在的本体。应用需要实例级参考数据时加载这类文件。

## 2. 个体构成（共 91 个）

按个体所属类型统计（类型名为中文（English）对照）：

| 类型（Class） | 个体数量 |
|---|---|
| 金融工具全球标识符（FinancialInstrumentGlobalIdentifier） | 21 |
| 行情代码（TickerSymbol） | 11 |
| 挂牌（Listing） | 11 |
| 上市股份（ListedShare） | 10 |
| 统一证券识别程序委员会号码（CommitteeOnUniformSecuritiesIdentificationProceduresNumber） | 10 |
| 国际证券识别码（InternationalSecuritiesIdentificationNumber） | 10 |
| 单一表决权、转让不受限、缴足普通股（CommonVotingUnrestrictedFullyPaidRegisteredShare） | 9 |
| 金融工具简称（FinancialInstrumentShortName） | 9 |
| 股份发行人（ShareIssuer） | 8 |
| 无表决权、转让不受限、缴足普通股（CommonNonVotingUnrestrictedFullyPaidRegisteredShare） | 1 |
| 证券交易所每日官方清单代码（StockExchangeDailyOfficialListCode） | 1 |

个体数量较多，仅举前 10 个示例，完整清单见同名 `.ttl` 文件：

| 个体（示例） | 类型 |
|---|---|
| 02079K107 | 统一证券识别程序委员会号码（CommitteeOnUniformSecuritiesIdentificationProceduresNumber） |
| 02079K305 | 统一证券识别程序委员会号码（CommitteeOnUniformSecuritiesIdentificationProceduresNumber） |
| 037833100 | 统一证券识别程序委员会号码（CommitteeOnUniformSecuritiesIdentificationProceduresNumber） |
| 172967424 | 统一证券识别程序委员会号码（CommitteeOnUniformSecuritiesIdentificationProceduresNumber） |
| 191216100 | 统一证券识别程序委员会号码（CommitteeOnUniformSecuritiesIdentificationProceduresNumber） |
| 437076102 | 统一证券识别程序委员会号码（CommitteeOnUniformSecuritiesIdentificationProceduresNumber） |
| 459200101 | 统一证券识别程序委员会号码（CommitteeOnUniformSecuritiesIdentificationProceduresNumber） |
| 46625H100 | 统一证券识别程序委员会号码（CommitteeOnUniformSecuritiesIdentificationProceduresNumber） |
| 742718109 | 统一证券识别程序委员会号码（CommitteeOnUniformSecuritiesIdentificationProceduresNumber） |
| 949746101 | 统一证券识别程序委员会号码（CommitteeOnUniformSecuritiesIdentificationProceduresNumber） |

## 3. 依赖的本体（owl:imports，23 个）

以下导入提供个体所属的类定义与相关参考数据：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `BE/GovernmentEntities/NorthAmericanJurisdiction/USGovernmentEntitiesAndJurisdictions.rdf` | 美国政府实体与法域本体（US Government Entities and Jurisdictions Ontology） | 收录美国的政体、联邦与各州政府、法域个体，是北美金融建模最常用的法域参考数据。 |
| `EXMP/LegalEntities/DowJonesIndustrialAverageCompanies.rdf` | 道指成分公司示例（Dow Jones Industrial Average Companies） | 收录道琼斯工业平均指数成分股公司的示例个体，供演示与测试。 |
| `EXMP/LegalEntities/FinancialInstitutionExamples.rdf` | 金融机构示例（Financial Institution Examples） | 收录典型金融机构的示例个体。 |
| `EXMP/LegalEntities/MarketsAndExchangesExamples.rdf` | 美国市场与交易所示例（US Markets and Exchanges Individuals） | 收录美国主要交易所与市场的示例个体。 |
| `FBC/FinancialInstruments/FinancialInstruments.rdf` | 金融工具本体（Financial Instruments Ontology） | FIBO 核心本体之一，定义金融工具（financial instrument）的通用概念：可交易、代表某种权利义务的合同工具，是证券、衍生品等具体工具的共同基础。 |
| `FBC/FunctionalEntities/MarketsIndividuals.rdf` | 市场个体本体（Markets Individuals） | 收录全球主要金融市场的参考个体。 |
| `FBC/FunctionalEntities/NorthAmericanEntities/USRegulatoryAgencies.rdf` | 美国监管机构本体（US Regulatory Agencies Ontology） | 收录美国金融监管机构个体（如美联储、证监会 SEC、货币监理署 OCC）。 |
| `FND/Accounting/CurrencyAmount.rdf` | 货币金额本体（Currency Amount Ontology） | 定义「金额＋币种」的货币金额（currency amount）表示，是 FIBO 中表达价格、债务金额、付款额等一切带币种数值的基础构件。 |
| `FND/Accounting/ISO4217-CurrencyCodes.rdf` | ISO 4217 货币代码本体（ISO 4217-1 Currency Codes Ontology） | 收录 ISO 4217-1 标准的全部货币代码个体（如 USD、CNY、EUR），为货币金额提供标准化的币种取值。 |
| `FND/Agreements/Contracts.rdf` | 合同本体（Contracts Ontology） | 在协议之上定义具有法律约束力的合同（contract）：合同当事方、合同条款、义务与权利，是金融工具与交易合同建模的基石。 |
| `FND/Relations/Relations.rdf` | 关系本体（Relations Ontology） | FIBO 最底层的基础本体，定义参考（reference）、分类（classify）等通用关系与抽象概念，全库普遍依赖。 |
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `SEC/Equities/EquityInstruments.rdf` | 股权工具本体（Equity Instruments Ontology） | 定义股票等股权工具：普通股、优先股及其附带的权利。 |
| `SEC/Securities/SecuritiesIdentification.rdf` | 证券识别本体（Securities Identification Ontology） | 定义证券标识符（ISIN、CUSIP、SEDOL 等）及其编码方案的结构。 |
| `SEC/Securities/SecuritiesIdentificationIndividuals.rdf` | 证券识别个体本体（Securities Identification Individuals Ontology） | 收录证券标识方案的参考个体（如 ISIN、CUSIP 编码方案本身）。 |
| `SEC/Securities/SecuritiesIssuance.rdf` | 证券发行本体（Securities Issuance Ontology） | 定义证券发行（issuance）：发行人、发行条款与发行结果。 |
| `SEC/Securities/SecuritiesListings.rdf` | 证券上市本体（Securities Listings Ontology） | 定义证券在交易所上市（listing）及其上市状态。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |
| `https://www.omg.org/spec/Commons/Classifiers/` | OMG 通用分类器本体（OMG Commons Classifiers） | OMG 通用本体库（Commons）中的分类器本体，定义分类方案、类别与归类关系的通用概念，FIBO 的分类建模建立在其上。 |
| `https://www.omg.org/spec/Commons/Designators/` | OMG 通用指称符本体（OMG Commons Designators） | Commons 库中的指称符本体，定义名称、标识符等「指代某物的符号」的通用概念。 |
| `https://www.omg.org/spec/Commons/Identifiers/` | OMG 通用标识符本体（OMG Commons Identifiers） | Commons 库中的标识符本体，定义标识符及其编码方案的通用概念。 |
| `https://www.omg.org/spec/Commons/RegistrationAuthorities/` | OMG 通用登记主管机构本体（OMG Commons Registration Authorities） | Commons 库中的登记主管机构本体，定义负责登记注册的主管机构及其登记行为的通用概念。 |
| `https://www.omg.org/spec/Commons/RolesAndCompositions/` | OMG 通用角色与构成本体（OMG Commons Roles and Compositions） | Commons 库中的角色本体，定义角色及整体—部分构成关系的通用概念。 |

## 4. 文件

- 官方 RDF/XML：`EquitiesExamples.rdf`
- 中文 Turtle：`EquitiesExamples.ttl`
- 结构图：`EquitiesExamples-structure.png` / `EquitiesExamples-structure.svg`