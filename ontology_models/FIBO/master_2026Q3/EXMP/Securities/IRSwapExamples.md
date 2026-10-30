# 利率互换示例个体本体（Interest Rate Swap Example Individuals Ontology）说明

本文档对应 `IRSwapExamples.rdf` / `IRSwapExamples.ttl`。

![利率互换示例个体本体（Interest Rate Swap Example Individuals Ontology）结构图](IRSwapExamples-structure.png)

## 1. 本文件是什么

收录利率互换合约的示例个体。

从机制上说，这是一个个体（individuals）文件：它本身不定义任何新的类或属性，装的全是命名个体（owl:NamedIndividual）——也就是一条条真实存在的实例数据（如具体的货币、市场、监管机构、法域）。它的 `owl:imports` 引入的是这些个体所属的类定义所在的本体。应用需要实例级参考数据时加载这类文件。

## 2. 个体构成（共 24 个）

按个体所属类型统计（类型名为中文（English）对照）：

| 类型（Class） | 个体数量 |
|---|---|
| 显式日期（ExplicitDate） | 4 |
| 组合（Portfolio） | 4 |
| 利息支付条款（InterestPaymentTerms） | 2 |
| 货币数量（MonetaryAmount） | 2 |
| 互换方（SwapParty） | 2 |
| 单货币固定对浮动利率互换（FixedFloatSingleCurrencyInterestRateSwap） | 1 |
| 固定利率腿（FixedInterestRateLeg） | 1 |
| 固定利率（FixedInterestRate） | 1 |
| 浮动利率腿（FloatingInterestRateLeg） | 1 |
| 浮动利率（FloatingInterestRate） | 1 |
| 营业日惯例（BusinessDayConvention） | 1 |
| 国际证券识别码（InternationalSecuritiesIdentificationNumber） | 1 |
| 唯一互换标识符（UniqueSwapIdentifier） | 1 |
| 证券交易（SecuritiesTransaction） | 1 |
| 交易对手（Counterparty） | 1 |
| 交易员（Trader） | 1 |

个体数量较多，仅举前 10 个示例，完整清单见同名 `.ttl` 文件：

| 个体（示例） | 类型 |
|---|---|
| European Central Bank business day adjustment | 营业日惯例（BusinessDayConvention） |
| IY7VKEUR45886 | 唯一互换标识符（UniqueSwapIdentifier） |
| ZZ216659451 | 国际证券识别码（InternationalSecuritiesIdentificationNumber） |
| contract IY7VKEUR45886 | 单货币固定对浮动利率互换（FixedFloatSingleCurrencyInterestRateSwap） |
| contract leg 1 IY7VKEUR45886 | 固定利率腿（FixedInterestRateLeg） |
| contract leg 1 IY7VKEUR45886 effective date | 显式日期（ExplicitDate） |
| contract leg 1 IY7VKEUR45886 fixed interest rate | 固定利率（FixedInterestRate） |
| contract leg 1 IY7VKEUR45886 notional amount | 货币数量（MonetaryAmount） |
| contract leg 1 IY7VKEUR45886 termination date | 显式日期（ExplicitDate） |
| contract leg 1 interest payment terms IY7VKEUR45886 | 利息支付条款（InterestPaymentTerms） |

## 3. 依赖的本体（owl:imports，27 个）

以下导入提供个体所属的类定义与相关参考数据：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `DER/DerivativesContracts/Swaps.rdf` | 互换本体（Swaps Ontology） | 定义互换（swap）合约的通用结构：互换腿（swap leg）、现金流交换与名义本金。 |
| `DER/RateDerivatives/IRSwaps.rdf` | 利率互换本体（Interest Rate Swaps Ontology） | 定义利率互换（IRS）：固定利率与浮动利率现金流的交换结构。 |
| `FBC/DebtAndEquities/Debt.rdf` | 债务本体（Debt Ontology） | 定义债务（debt）与债权债务关系的核心概念：借款人、贷款人、本金与利息义务。 |
| `FBC/FinancialInstruments/FinancialInstruments.rdf` | 金融工具本体（Financial Instruments Ontology） | FIBO 核心本体之一，定义金融工具（financial instrument）的通用概念：可交易、代表某种权利义务的合同工具，是证券、衍生品等具体工具的共同基础。 |
| `FBC/FunctionalEntities/BusinessCentersIndividuals.rdf` | 商业中心个体本体（Business Centers Individuals） | 收录全球主要商业中心（如纽约、伦敦、东京）的参考个体。 |
| `FBC/ProductsAndServices/FinancialProductsAndServices.rdf` | 金融产品与服务本体（Financial Products and Services Ontology） | 定义金融产品（financial product）与金融服务（financial service）及其提供、购买关系。 |
| `FND/Accounting/CurrencyAmount.rdf` | 货币金额本体（Currency Amount Ontology） | 定义「金额＋币种」的货币金额（currency amount）表示，是 FIBO 中表达价格、债务金额、付款额等一切带币种数值的基础构件。 |
| `FND/Accounting/ISO4217-CurrencyCodes.rdf` | ISO 4217 货币代码本体（ISO 4217-1 Currency Codes Ontology） | 收录 ISO 4217-1 标准的全部货币代码个体（如 USD、CNY、EUR），为货币金额提供标准化的币种取值。 |
| `FND/Agreements/Contracts.rdf` | 合同本体（Contracts Ontology） | 在协议之上定义具有法律约束力的合同（contract）：合同当事方、合同条款、义务与权利，是金融工具与交易合同建模的基石。 |
| `FND/Arrangements/Documents.rdf` | 文档本体（Documents Ontology） | 定义文档、文档类型及文档与其所记载内容的关系，为合同文本、募集说明书等法律文书建模。 |
| `FND/DatesAndTimes/BusinessDates.rdf` | 营业日期本体（Business Dates Ontology） | 定义营业日、营业日历与日期调整规则（如顺延约定），支撑金融合同中的营业日计算。 |
| `FND/OwnershipAndControl/Ownership.rdf` | 所有权本体（Ownership Ontology） | 定义「拥有」关系：所有者、被拥有资产及所有权份额。 |
| `FND/ProductsAndServices/ProductsAndServices.rdf` | 产品与服务本体（Products and Services Ontology） | 定义产品、服务及其提供者与客户的通用关系。 |
| `FND/Relations/Relations.rdf` | 关系本体（Relations Ontology） | FIBO 最底层的基础本体，定义参考（reference）、分类（classify）等通用关系与抽象概念，全库普遍依赖。 |
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `IND/InterestRates/CommonInterestRates.rdf` | 常用利率本体（Common Interest Rates Ontology） | 收录市场常用参考利率个体（如各期限基准、政策利率）。 |
| `IND/InterestRates/InterestRates.rdf` | 利率本体（Interest Rates Ontology） | 定义利率（interest rate）的结构：基准利率、利差、期限与重置机制。 |
| `SEC/Debt/DebtInstruments.rdf` | 债务工具本体（Debt Instruments Ontology） | 定义债务工具（debt instrument）的通用概念：可交易的债权凭证，是债券、票据等的上位模型。 |
| `SEC/Securities/SecuritiesIdentification.rdf` | 证券识别本体（Securities Identification Ontology） | 定义证券标识符（ISIN、CUSIP、SEDOL 等）及其编码方案的结构。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |
| `https://www.omg.org/spec/Commons/Collections/` | OMG 通用集合本体（OMG Commons Collections） | Commons 库中的集合本体，定义集合、成员等通用概念。 |
| `https://www.omg.org/spec/Commons/ContextualDesignators/` | OMG 通用语境指称本体（OMG Commons Contextual Designators） | Commons 库中的语境指称本体，定义「在某个语境下指代某物的名称/符号」，是地址、账户号码等语境相关标识的基础。 |
| `https://www.omg.org/spec/Commons/DatesAndTimes/` | OMG 通用日期与时间本体（OMG Commons Dates and Times） | Commons 库中的日期时间本体，定义日期、期间、时间点等通用时间概念。 |
| `https://www.omg.org/spec/Commons/Designators/` | OMG 通用指称符本体（OMG Commons Designators） | Commons 库中的指称符本体，定义名称、标识符等「指代某物的符号」的通用概念。 |
| `https://www.omg.org/spec/Commons/Documents/` | OMG 通用文档本体（OMG Commons Documents） | Commons 库中的文档本体，定义文档及其组成部分的通用概念。 |
| `https://www.omg.org/spec/Commons/Identifiers/` | OMG 通用标识符本体（OMG Commons Identifiers） | Commons 库中的标识符本体，定义标识符及其编码方案的通用概念。 |
| `https://www.omg.org/spec/Commons/Locations/` | OMG 通用位置本体（OMG Commons Locations） | Commons 库中的位置本体，定义地理位置、地点的通用概念。 |

## 4. 文件

- 官方 RDF/XML：`IRSwapExamples.rdf`
- 中文 Turtle：`IRSwapExamples.ttl`
- 结构图：`IRSwapExamples-structure.png` / `IRSwapExamples-structure.svg`