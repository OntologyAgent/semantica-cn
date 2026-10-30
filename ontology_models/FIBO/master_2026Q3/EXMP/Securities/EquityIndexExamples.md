# 股指示例个体本体（Equity Index Example Individuals Ontology）说明

本文档对应 `EquityIndexExamples.rdf` / `EquityIndexExamples.ttl`。

![股指示例个体本体（Equity Index Example Individuals Ontology）结构图](EquityIndexExamples-structure.png)

## 1. 本文件是什么

收录股票指数（如道琼斯工业平均指数）的示例个体。

从机制上说，这是一个个体（individuals）文件：它本身不定义任何新的类或属性，装的全是命名个体（owl:NamedIndividual）——也就是一条条真实存在的实例数据（如具体的货币、市场、监管机构、法域）。它的 `owl:imports` 引入的是这些个体所属的类定义所在的本体。应用需要实例级参考数据时加载这类文件。

## 2. 个体构成（共 17 个）

按个体所属类型统计（类型名为中文（English）对照）：

| 类型（Class） | 个体数量 |
|---|---|
| 证券篮子成分（SecuritiesBasketConstituent） | 5 |
| 显式日期（ExplicitDate） | 5 |
| 股票指数（EquityIndex） | 2 |
| 股票篮子（BasketOfEquities） | 2 |
| 数值指数值（NumericIndexValue） | 1 |
| 市场数据提供商（MarketDataProvider） | 1 |
| 金融服务提供商（FinancialServiceProvider） | 1 |
| 有限责任私人公司（PrivateCompanyWithLimitedLiability） | 1 |

个体数量较少，全部列出：

| 个体 | 类型 |
|---|---|
| Dow Jones Industrial Average | 股票指数（EquityIndex） |
| Dow Jones Industrial Average basket | 股票篮子（BasketOfEquities） |
| Dow Jones Industrial Average basket - Apple Inc. common stock constituent | 证券篮子成分（SecuritiesBasketConstituent） |
| Dow Jones Industrial Average basket - Apple Inc. common stock date added | 显式日期（ExplicitDate） |
| Dow Jones Industrial Average basket - IBM common stock constituent | 证券篮子成分（SecuritiesBasketConstituent） |
| Dow Jones Industrial Average basket - IBM common stock date added | 显式日期（ExplicitDate） |
| Dow Jones Industrial Average basket - The Coca-Cola Company common stock constituent | 证券篮子成分（SecuritiesBasketConstituent） |
| Dow Jones Industrial Average basket - The Coca-Cola Company common stock date added | 显式日期（ExplicitDate） |
| Dow Jones Industrial Average basket - The Home Depot, Inc. common stock constituent | 证券篮子成分（SecuritiesBasketConstituent） |
| Dow Jones Industrial Average basket - The Home Depot, Inc. common stock date added | 显式日期（ExplicitDate） |
| Dow Jones Industrial Average basket - The Proctor & Gamble Company common stock constituent | 证券篮子成分（SecuritiesBasketConstituent） |
| Dow Jones Industrial Average basket - The Proctor & Gamble Company common stock date added | 显式日期（ExplicitDate） |
| Dow Jones Industrial Average value as of Mar 6, 2020 | 数值指数值（NumericIndexValue） |
| S & P Dow Jones Indices | 市场数据提供商（MarketDataProvider）、金融服务提供商（FinancialServiceProvider） |
| S & P Dow Jones Indices LLC US-DE | 有限责任私人公司（PrivateCompanyWithLimitedLiability） |
| Standard & Poor's Composite Index | 股票指数（EquityIndex） |
| Standard & Poor's Composite Index basket | 股票篮子（BasketOfEquities） |

## 3. 依赖的本体（owl:imports，26 个）

以下导入提供个体所属的类定义与相关参考数据：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `BE/FunctionalEntities/Publishers.rdf` | 出版方本体（Publishers Ontology） | 定义出版方及其出版物，用于标识金融信息与文档的发布来源。 |
| `BE/LegalEntities/FormalBusinessOrganizations.rdf` | 正式商业组织本体（Formal Business Organizations Ontology） | 定义以营利为目的、依法注册的正式商业组织，连接法律实体与其商业功能。 |
| `BE/OwnershipAndControl/ControlParties.rdf` | 控制方本体（Control Parties Ontology） | 定义处于控制关系中的各方角色：控制方、被控制方、实际控制人等。 |
| `BE/PrivateLimitedCompanies/PrivateLimitedCompanies.rdf` | 私人有限公司本体（Private Limited Companies Ontology） | 定义私人有限公司（private limited company）这类不公开募股的有限责任公司形态。 |
| `EXMP/Securities/EquitiesExamples.rdf` | 股票示例个体本体（Equities Example Individuals Ontology） | 收录典型股票（上市公司普通股）的示例个体。 |
| `FBC/DebtAndEquities/Debt.rdf` | 债务本体（Debt Ontology） | 定义债务（debt）与债权债务关系的核心概念：借款人、贷款人、本金与利息义务。 |
| `FBC/FinancialInstruments/FinancialInstruments.rdf` | 金融工具本体（Financial Instruments Ontology） | FIBO 核心本体之一，定义金融工具（financial instrument）的通用概念：可交易、代表某种权利义务的合同工具，是证券、衍生品等具体工具的共同基础。 |
| `FBC/FunctionalEntities/BusinessRegistries.rdf` | 商业登记机构本体（Business Registries Ontology） | 定义商业登记机构（如公司注册处）及其登记职能。 |
| `FBC/FunctionalEntities/CommercialRegistrationAuthorities.rdf` | 商事登记主管机关本体（Commercial Registration Authorities Ontology） | 定义负责商事登记的主管机关及其维护的登记记录。 |
| `FBC/FunctionalEntities/NorthAmericanEntities/USRegulatoryAgencies.rdf` | 美国监管机构本体（US Regulatory Agencies Ontology） | 收录美国金融监管机构个体（如美联储、证监会 SEC、货币监理署 OCC）。 |
| `FBC/ProductsAndServices/FinancialProductsAndServices.rdf` | 金融产品与服务本体（Financial Products and Services Ontology） | 定义金融产品（financial product）与金融服务（financial service）及其提供、购买关系。 |
| `FND/Accounting/CurrencyAmount.rdf` | 货币金额本体（Currency Amount Ontology） | 定义「金额＋币种」的货币金额（currency amount）表示，是 FIBO 中表达价格、债务金额、付款额等一切带币种数值的基础构件。 |
| `FND/DatesAndTimes/FinancialDates.rdf` | 金融日期本体（Financial Dates Ontology） | 定义金融语境下的日期与期间概念：结算日、付息日、到期日、日计数基准等。 |
| `FND/Relations/Relations.rdf` | 关系本体（Relations Ontology） | FIBO 最底层的基础本体，定义参考（reference）、分类（classify）等通用关系与抽象概念，全库普遍依赖。 |
| `FND/Utilities/Analytics.rdf` | 分析本体（Analytics Ontology） | 定义分析工具、度量与比率的通用概念，支撑指标与模型的表达。 |
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `IND/Indicators/Indicators.rdf` | 指标本体（Indicators Ontology） | 定义「指标」（indicator）的通用概念：对某现象的可度量表示，是经济指标、利率等的上位模型。 |
| `IND/MarketIndices/BasketIndices.rdf` | 篮子指数本体（Basket Indices Ontology） | 定义以一篮子成分为基础的指数：成分、权重与计算方法。 |
| `SEC/Securities/Baskets.rdf` | 篮子本体（Baskets Ontology） | 定义证券篮子（basket）：作为整体交易或定价的一组证券。 |
| `SEC/Securities/SecuritiesClassification.rdf` | 证券分类本体（Securities Classification Ontology） | 定义证券分类方案：按 CFI 代码、按资产类别等对证券归类。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |
| `https://www.omg.org/spec/Commons/Collections/` | OMG 通用集合本体（OMG Commons Collections） | Commons 库中的集合本体，定义集合、成员等通用概念。 |
| `https://www.omg.org/spec/Commons/DatesAndTimes/` | OMG 通用日期与时间本体（OMG Commons Dates and Times） | Commons 库中的日期时间本体，定义日期、期间、时间点等通用时间概念。 |
| `https://www.omg.org/spec/Commons/Organizations/` | OMG 通用组织本体（OMG Commons Organizations） | Commons 库中的组织本体，定义组织、组织成员与组织结构的通用概念。 |
| `https://www.omg.org/spec/Commons/QuantitiesAndUnits/` | OMG 通用量与单位本体（OMG Commons Quantities and Units） | Commons 库中的量与单位本体，定义数量、度量单位、量纲的通用概念，支撑金额、比率等数值表达。 |
| `https://www.omg.org/spec/Commons/RolesAndCompositions/` | OMG 通用角色与构成本体（OMG Commons Roles and Compositions） | Commons 库中的角色本体，定义角色及整体—部分构成关系的通用概念。 |

## 4. 文件

- 官方 RDF/XML：`EquityIndexExamples.rdf`
- 中文 Turtle：`EquityIndexExamples.ttl`
- 结构图：`EquityIndexExamples-structure.png` / `EquityIndexExamples-structure.svg`