# 金融服务实体本体（Financial Services Entities Ontology）结构与公理说明

本文档对应 `FinancialServicesEntities.rdf` / `FinancialServicesEntities.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `FinancialServicesEntities-structure.png`（`FinancialServicesEntities-structure.svg` 为可缩放版本）。

![金融服务实体本体（Financial Services Entities Ontology）本体结构图](FinancialServicesEntities-structure.png)

## 1. 本体概述

定义金融服务机构（financial services entity）的功能分类体系：银行、券商、保险公司、资管机构、清算所等，是 FBC 域的核心本体。

**在体系中的位置**：FBC 功能实体模块的中心，欧美各区域扩展本体（美国、加拿大、欧盟金融服务实体）都继承它。

**上下游关系**：上游依赖 BE 功能实体、FND 正式组织与产品服务本体；下游被金融产品与服务、客户与账户及全部区域扩展本体引用。

**与相近概念的差别**：按「功能」而非「法律形式」分类——同一家公司可以同时是银行和券商（功能叠加）；与 BE 法律实体的差别——法律实体回答「它是什么组织」，本本体回答「它干什么业务」。

## 2. 类（Class）

| 类（Class） | 定义（Definition） |
|---|---|
| 银行（bank） | 吸收存款、发放贷款、兑付支票并提供相关服务的存款性机构，通常为公司制，服务于个人客户和企业客户。 |
| 银行控股公司（bank holding company） | 拥有和/或直接或间接控制一家或多家银行的公司；银行控股公司还可以拥有经纪交易商等非银行子公司。 |
| 银行产品（banking product） | 由存款性机构向消费者和企业提供的产品。 |
| 银行服务（banking service） | 由存款性机构提供的金融服务。 |
| 经纪公司（brokerage firm） | 从事证券买卖业务的公司，视交易情况同时以经纪商和交易商身份运作。 |
| 商业标识代码（business identifier code） | 金融和非金融机构的国际标识符，用于促进金融服务信息的自动化处理。 |
| 商业标识代码方案（business identifier code scheme） | 规定用于标识金融和非金融机构的唯一商业标识代码（BIC）之构成要素的方案。 |
| 商业方前缀（business party prefix） | 为银行电讯目的与机构相关联的四位字符（4 位字母数字）代码。 |
| 商业方后缀（business party suffix） | 为银行电讯目的与机构相关联的两位字符（2 位字母数字）代码。 |
| 中央银行（central bank） | 作为一个国家（或国家集团）货币当局和主要监管银行的金融机构。 |
| 中央对手方清算所（central counterparty clearing house） | 帮助促进衍生品和股票市场交易的清算所。 |
| 中央证券存管机构（central securities depository） | 为金融工具（「证券」，如债券和股票）提供集中存管点的功能实体。 |
| 清算银行（clearing bank） | 为金融交易（如支票清算或促进买卖双方之间交易）的支付和结算提供便利的商业银行。 |
| 清算公司（clearing corporation） | 以公司形式组建的清算所。 |
| 清算所（clearing house） | 附属于交易所、提供清算服务（包括金融交易的确认、交割和结算）的金融服务提供商。 |
| 清算服务（clearing service） | 交易达成后由清算服务提供方代表机构市场参与者提供、完成证券和资金划转的服务。 |
| 商业银行（commercial bank） | 从事多种金融服务（如吸收存款和发放贷款）的存款性机构。 |
| 商业金融公司（commercial finance company） | 以应收账款、存货和设备为担保向制造商和批发商发放贷款的金融公司。 |
| 商品交易顾问（commodity trading advisor） | 直接或间接就买卖期货合约或期权的价值或可行性向他人提供建议的一方。 |
| 消费金融公司（consumer finance company） | 依据其经营所在司法管辖区的小额贷款法律向个人发放贷款的金融公司。 |
| 契约型储蓄机构（contractual savings institution） | 以受托（而非本人）方式为个人提供投资集合投资工具机会的金融机构。 |
| 信用合作社（credit union） | 为提倡节俭之目的而组织、发放个人贷款并提供其他消费金融服务的非营利性存款机构。 |
| 数据处理服务（data processing service） | 由主要从事托管或数据处理基础设施业务的实体提供的金融服务。 |
| 数据处理服务商（data processing servicer） | 主要从事托管或数据处理基础设施业务的金融服务提供商。 |
| 存款性机构（depository institution） | 从事从公众或其他机构吸收活期存款业务的任何金融机构。 |
| 开发银行（development bank） | 旨在为生产性投资提供中长期资本（通常附带技术援助）的国家或区域性金融机构。 |
| 电子资金转账服务（electronic funds transfer service） | 除纸质票据交易外，通过电子终端、电话、计算机或磁介质发起的资金转账服务。 |
| 面额证书公司（face amount certificate company） | 从事或拟从事发行分期型面额证书业务、或已从事该业务的投资公司。 |
| 金融公司（finance company） | 从事放贷业务、资金来源于银行、机构和其他货币市场渠道（而非公众存款）的金融中介。 |
| 金融机构（financial institution） | 被认定为政府机构或私营实体、从公众和其他机构归集资金的金融服务提供商。 |
| 金融服务提供商标识符（financial service provider identifier） | 基于金融服务提供商所提供职能正式分配给它的标识符，通常在某一司法管辖区内有效。 |
| 金融服务提供商标识符方案（financial service provider identifier scheme） | 依照签发注册机构或监管机构的规定定义金融服务提供商标识符的方案。 |
| 期货佣金商（futures commission merchant） | 从事以下两项业务的一方：（1）招揽或接受期货合约、期货期权、零售场外外汇等的买卖订单；（2）接受资金或其他资产作为保证金。 |
| 控股公司（holding company） | 为持有另一家公司股份而设立的商业实体，通常持有足够的表决权股份以对该公司的政策施加一定程度的控制。 |
| 保险公司（insurance company） | 主要且占主导地位的业务活动是承保保险或对保险公司承保的风险进行再保险的非存款性机构。 |
| 保险服务（insurance service） | 保险人承诺就特定潜在未来损失提供补偿、以换取定期付款（保费）的金融服务。 |
| 投资银行（investment bank） | 作为承销商或代理人、在证券发行人与投资公众之间充当中介的金融服务提供商。 |
| 投资公司（investment company） | 主要从事或自称主要从事、或拟主要从事投资、再投资或证券交易业务的任何发行人。 |
| 投资服务（investment service） | 旨在协助投资者运用资本创造更多资金的金融服务，可通过产生收入的工具或更具风险导向的工具实现。 |
| 管理公司（management company） | 除面额证书公司或单位投资信托外，出售并管理证券投资组合的投资公司。 |
| 商户服务（merchant service） | 金融机构向商户或其他企业提供的金融服务，包括但不限于通过多种支付渠道管理金融交易。 |
| 货币当局（monetary authority） | 控制某一国家或国家集团货币政策、监管和货币供应的监管机构。 |
| 货币服务业务（money services business） | 以下列任一身份开展业务的任何人（无论是否经常性地或以有组织的企业形式）：货币交易商或兑换商、支票兑现商、旅行支票或储值产品的发行/销售/赎回商、汇款商等。 |
| 抵押贷款公司（mortgage company） | 为住宅或商业物业发起和/或提供抵押贷款资金的金融服务提供商。 |
| 非存款性机构（non-depository institution） | 不具备完全银行牌照、通常不受国家或国际银行监管机构监管的金融机构。 |
| 支付服务（payment service） | 涉及通过信用卡、借记卡等银行支付方式等多种支付方式接受电子支付的金融服务。 |
| 薪资服务（payroll service） | 通常向规模不足以设立内部财务组织的小企业提供的、涉及薪资管理的金融服务。 |
| 主承销商（principal underwriter） | 以本人身份从投资公司购入证券、或依合同有权从该公司购入任何证券的承销商。 |
| 注册投资顾问（registered investment advisor） | 为高净值个人提供投资建议并管理其投资组合的注册代理人和金融服务提供商。 |
| 风险汇聚机构（risk pooling institution） | 在提供某项金融服务的同时分散该服务固有风险、以降低重大损失概率的金融机构。 |
| 销售金融公司（sales finance company） | 从汽车及其他消费品和商业商品经销商处购买零售和批发票据的金融公司。 |
| 储蓄协会（savings association） | 存款性机构，包括：（a）依《联邦存款保险法》第 1464 条特许的任何联邦储蓄银行或协会；（b）其他相关储蓄机构。 |
| 自律组织（self-regulating organization） | 有权在某国对某行业或职业创设并行施一定程度监管权的非政府组织。 |
| 信托公司（trust company） | 以受托人、信托受托机构或信托代理机构身份行事的金融机构。 |
| 承销商（underwriter） | 以佣金、保费、价差或利息等费用为代价，评估并承担他方风险的金融服务提供商。 |
| 承销安排（underwriting arrangement） | 承诺承销商承担风险的双方之间的书面合同。 |
| 单位投资信托（unit investment trust） | 依信托契约、托管或代理合同或类似文件组织、不设董事会的投资公司。 |
| 财富管理服务（wealth management service） | 为单一客户综合提供财务与投资建议、会计与税务服务、退休规划以及法律或遗产规划的金融服务。 |

### 2.1 继承关系（Inheritance）

- 银行（bank） ⊑ 存款性机构（depository institution）
- 银行控股公司（bank holding company） ⊑ 控股公司（holding company）
- 银行控股公司（bank holding company） ⊑ 金融服务提供商
- 银行产品（banking product） ⊑ 金融产品
- 银行服务（banking service） ⊑ 金融服务
- 经纪公司（brokerage firm） ⊑ 非存款性机构（non-depository institution）
- 经纪公司（brokerage firm） ⊑ 经纪交易商
- 商业标识代码（business identifier code） ⊑ 代码元素
- 商业标识代码（business identifier code） ⊑ 结构化标识符
- 商业标识代码（business identifier code） ⊑ 组织标识符
- 商业标识代码方案（business identifier code scheme） ⊑ 代码集
- 商业标识代码方案（business identifier code scheme） ⊑ 组织标识方案
- 商业方前缀（business party prefix） ⊑ 代码元素
- 商业方前缀（business party prefix） ⊑ 组织标识符
- 商业方后缀（business party suffix） ⊑ 代码元素
- 中央银行（central bank） ⊑ 银行（bank）
- 中央银行（central bank） ⊑ 货币当局（monetary authority）
- 中央对手方清算所（central counterparty clearing house） ⊑ 清算所（clearing house）
- 中央证券存管机构（central securities depository） ⊑ 金融服务提供商
- 清算银行（clearing bank） ⊑ 清算所（clearing house）
- 清算银行（clearing bank） ⊑ 商业银行（commercial bank）
- 清算公司（clearing corporation） ⊑ 清算所（clearing house）
- 清算所（clearing house） ⊑ 金融服务提供商
- 清算服务（clearing service） ⊑ 金融服务
- 商业银行（commercial bank） ⊑ 银行（bank）
- 商业金融公司（commercial finance company） ⊑ 金融公司（finance company）
- 商品交易顾问（commodity trading advisor） ⊑ 非存款性机构（non-depository institution）
- 消费金融公司（consumer finance company） ⊑ 金融公司（finance company）
- 契约型储蓄机构（contractual savings institution） ⊑ 投资者
- 契约型储蓄机构（contractual savings institution） ⊑ 非存款性机构（non-depository institution）
- 信用合作社（credit union） ⊑ 合作社
- 信用合作社（credit union） ⊑ 存款性机构（depository institution）
- 数据处理服务（data processing service） ⊑ 金融服务
- 数据处理服务商（data processing servicer） ⊑ 金融服务提供商
- 存款性机构（depository institution） ⊑ 金融机构（financial institution）
- 开发银行（development bank） ⊑ 金融机构（financial institution）
- 电子资金转账服务（electronic funds transfer service） ⊑ 金融服务
- 面额证书公司（face amount certificate company） ⊑ 投资公司（investment company）
- 金融公司（finance company） ⊑ 非存款性机构（non-depository institution）
- 金融机构（financial institution） ⊑ 金融服务提供商
- 金融服务提供商标识符（financial service provider identifier） ⊑ 参与方角色标识符
- 金融服务提供商标识符方案（financial service provider identifier scheme） ⊑ 标识方案
- 期货佣金商（futures commission merchant） ⊑ 非存款性机构（non-depository institution）
- 控股公司（holding company） ⊑ 功能型企业实体
- 保险公司（insurance company） ⊑ 风险汇聚机构（risk pooling institution）
- 保险服务（insurance service） ⊑ 金融服务
- 投资银行（investment bank） ⊑ 金融机构（financial institution）
- 投资公司（investment company） ⊑ 非存款性机构（non-depository institution）
- 投资服务（investment service） ⊑ 金融服务
- 管理公司（management company） ⊑ 投资公司（investment company）
- 商户服务（merchant service） ⊑ 金融服务
- 货币当局（monetary authority） ⊑ 监管机构
- 货币服务业务（money services business） ⊑ 非存款性机构（non-depository institution）
- 抵押贷款公司（mortgage company） ⊑ 金融服务提供商
- 非存款性机构（non-depository institution） ⊑ 金融机构（financial institution）
- 支付服务（payment service） ⊑ 商户服务（merchant service）
- 薪资服务（payroll service） ⊑ 金融服务
- 主承销商（principal underwriter） ⊑ 承销商（underwriter）
- 注册投资顾问（registered investment advisor） ⊑ 金融服务提供商
- 注册投资顾问（registered investment advisor） ⊑ 注册代理人
- 风险汇聚机构（risk pooling institution） ⊑ 非存款性机构（non-depository institution）
- 销售金融公司（sales finance company） ⊑ 金融公司（finance company）
- 储蓄协会（savings association） ⊑ 存款性机构（depository institution）
- 自律组织（self-regulating organization） ⊑ 监管机构
- 信托公司（trust company） ⊑ 金融机构（financial institution）
- 承销商（underwriter） ⊑ 金融服务提供商
- 承销安排（underwriting arrangement） ⊑ 书面合同
- 单位投资信托（unit investment trust） ⊑ 投资公司（investment company）
- 财富管理服务（wealth management service） ⊑ 金融服务

## 3. 对象属性（Object Property）

| 属性（Property） | 中文（English） | 定义（Definition） | 说明 |
|---|---|---|---|
| fibo-fbc-fct-fse:hasDateEstablished | 具有设立日期（has date established） | 金融服务提供商正式设立的日期。 | 值域（range）：显式日期；子属性（subPropertyOf）：具有显式日期 |
| fibo-fbc-fct-fse:hasDateEstablishmentTerminated | 具有终止日期（has date establishment terminated） | 实体存续的最后一个完整日。 | 值域（range）：显式日期；子属性（subPropertyOf）：具有到期日 |
| fibo-fbc-fct-fse:hasDateInsured | 具有投保生效日（has date insured） | 保险开始生效的日期。 | 值域（range）：显式日期；子属性（subPropertyOf）：具有显式日期 |
| fibo-fbc-fct-fse:hasPortfolioCompany | 具有被投公司（has portfolio company） | 指明风险投资机构、并购基金或控股公司所投资的一方。 | 定义域（domain）：控制方；值域（range）：受控方；逆属性（inverseOf）：是……的被投公司（is portfolio company of）；子属性（subPropertyOf）：是控制方 |
| fibo-fbc-fct-fse:isPortfolioCompanyOf | 是……的被投公司（is portfolio company of） | 指明作为该方财务投资人（即投资方）的风险投资机构、并购基金或控股公司。 | 定义域（domain）：受控方；值域（range）：控制方；子属性（subPropertyOf）：具有控制方 |
| fibo-fbc-fct-fse:regulatesSupplyOf | 监管……的供应（regulates supply of） | 将监管机构与其通过规章制度在某市场上控制或监督其供应的事物关联起来。 | 定义域（domain）：监管机构；子属性（subPropertyOf）：管辖 |

## 5. 公理约定（Axioms）

- 银行控股公司（bank holding company）：由…扮演（is played by） 公司 =1
- 银行产品（banking product）：由……提供 some 存款性机构（depository institution）
- 银行服务（banking service）：由……提供 some 存款性机构（depository institution）
- 商业标识代码（business identifier code）：包含 组织子单位标识符 ≥0
- 商业标识代码（business identifier code）：包含 商业方前缀（business party prefix） =1
- 商业标识代码（business identifier code）：包含 商业方后缀（business party suffix） =1
- 商业标识代码（business identifier code）：指代 正式组织 =1
- 商业标识代码（business identifier code）：包含 lcc-cr:Alpha2Code =1
- 商业标识代码（business identifier code）：是……的成员 some 商业标识代码方案（business identifier code scheme）
- 商业标识代码方案（business identifier code scheme）：具有成员 some 商业标识代码（business identifier code）
- 商业方前缀（business party prefix）：被包含于 商业标识代码（business identifier code） ≤1
- 商业方前缀（business party prefix）：定义于 some 商业标识代码方案（business identifier code scheme）
- 商业方后缀（business party suffix）：被包含于 some 商业标识代码（business identifier code）
- 商业方后缀（business party suffix）：定义于 some 商业标识代码方案（business identifier code scheme）
- 中央银行（central bank）：由…扮演（is played by） only 部属单位
- 清算公司（clearing corporation）：由…扮演（is played by） 公司 =1
- 清算所（clearing house）：提供 some 清算服务（clearing service）
- 商业银行（commercial bank）：由…扮演（is played by） 公司 =1
- 契约型储蓄机构（contractual savings institution）：由…扮演（is played by） N198e2cf8ae3c4102b7d3496999f1e58d ≥0
- 信用合作社（credit union）：由…扮演（is played by） 非营利组织 =1
- 数据处理服务（data processing service）：由……提供 some 数据处理服务商（data processing servicer）
- 面额证书公司（face amount certificate company） 与 管理公司（management company） 互斥（disjointWith）
- 金融机构（financial institution）：提供 some 金融服务
- 金融机构（financial institution）：受……监管 some 监管机构
- 金融服务提供商标识符（financial service provider identifier）：受……管辖 管辖权 ≥0
- 金融服务提供商标识符（financial service provider identifier）：是……的成员 金融服务提供商标识符方案（financial service provider identifier scheme） =1
- 金融服务提供商标识符（financial service provider identifier）：标识 金融服务提供商 =1
- 金融服务提供商标识符方案（financial service provider identifier scheme）：具有成员 some 金融服务提供商标识符（financial service provider identifier）
- 控股公司（holding company）：具有被投公司（has portfolio company） 受控方 ≥0
- 投资银行（investment bank）：restriction
- 管理公司（management company） 与 单位投资信托（unit investment trust） 互斥（disjointWith）
- 货币当局（monetary authority）：监管……的供应（regulates supply of） some 货币
- 支付服务（payment service）：涉及 some 支付义务
- 注册投资顾问（registered investment advisor）：提供咨询 some 受控方
- 注册投资顾问（registered investment advisor）：由……注册 some（restriction）
- 自律组织（self-regulating organization）：由…扮演（is played by） some 非政府组织
- 信托公司（trust company）：由…扮演（is played by） 公司 =1
- 承销商（underwriter）：由…扮演（is played by） some（是…的参与方（is a party to） some 承销安排（underwriting arrangement））
- 承销安排（underwriting arrangement）：具有参与方角色（has party role） some 承销商（underwriter）

## 6. 依赖（owl:imports，31 个）

本本体通过 `owl:imports` 引入以下本体，各项的中文名称与简介如下：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `BE/FunctionalEntities/FunctionalEntities.rdf` | 功能实体本体（Functional Entities Ontology） | 定义「功能实体」：按其在商业中承担的功能（而非法律形式）刻画的实体，是出版方、登记机构等功能性主体的基础。 |
| `BE/GovernmentEntities/GovernmentEntities.rdf` | 政府实体本体（Government Entities Ontology） | 定义政府、政体（polity）、法域（jurisdiction）及政府实体的核心概念，是各区域政府实体本体的共同基础。 |
| `BE/LegalEntities/CorporateBodies.rdf` | 法人团体本体（Corporate Bodies Ontology） | 定义依法设立、具有独立法律人格的法人团体（corporate body），是股份有限公司等具体法人类型的上位概念。 |
| `BE/LegalEntities/FormalBusinessOrganizations.rdf` | 正式商业组织本体（Formal Business Organizations Ontology） | 定义以营利为目的、依法注册的正式商业组织，连接法律实体与其商业功能。 |
| `BE/LegalEntities/LegalPersons.rdf` | 法律主体本体（Legal Persons Ontology） | 定义法律主体（legal person）与法定实体（legal entity）的核心概念：能持有权利义务、可起诉与被诉的主体。 |
| `BE/OwnershipAndControl/ControlParties.rdf` | 控制方本体（Control Parties Ontology） | 定义处于控制关系中的各方角色：控制方、被控制方、实际控制人等。 |
| `BE/OwnershipAndControl/OwnershipParties.rdf` | 所有权方本体（Ownership Parties Ontology） | 定义所有权关系中的各方角色：所有者、受益所有人、名义持有人等。 |
| `BE/Partnerships/Partnerships.rdf` | 合伙本体（Partnerships Ontology） | 定义合伙企业及普通合伙、有限合伙等形态，刻画合伙人之间的权利义务。 |
| `BE/PrivateLimitedCompanies/PrivateLimitedCompanies.rdf` | 私人有限公司本体（Private Limited Companies Ontology） | 定义私人有限公司（private limited company）这类不公开募股的有限责任公司形态。 |
| `FBC/ProductsAndServices/FinancialProductsAndServices.rdf` | 金融产品与服务本体（Financial Products and Services Ontology） | 定义金融产品（financial product）与金融服务（financial service）及其提供、购买关系。 |
| `FND/Accounting/CurrencyAmount.rdf` | 货币金额本体（Currency Amount Ontology） | 定义「金额＋币种」的货币金额（currency amount）表示，是 FIBO 中表达价格、债务金额、付款额等一切带币种数值的基础构件。 |
| `FND/Agreements/Contracts.rdf` | 合同本体（Contracts Ontology） | 在协议之上定义具有法律约束力的合同（contract）：合同当事方、合同条款、义务与权利，是金融工具与交易合同建模的基石。 |
| `FND/Arrangements/Documents.rdf` | 文档本体（Documents Ontology） | 定义文档、文档类型及文档与其所记载内容的关系，为合同文本、募集说明书等法律文书建模。 |
| `FND/OwnershipAndControl/Control.rdf` | 控制本体（Control Ontology） | 定义「控制」关系：控制方、被控制方与控制程度，用于公司治理与合并报表判断。 |
| `FND/Parties/Parties.rdf` | 参与方本体（Parties Ontology） | 定义参与方（party）、独立主体（autonomous agent）与「角色扮演」（party in role），是 FIBO 全库使用最广的基础本体之一。 |
| `FND/ProductsAndServices/PaymentsAndSchedules.rdf` | 付款与计划表本体（Payments and Schedules Ontology） | 定义付款、付款计划表（payment schedule）及其日期与金额结构，是贷款还款、债券付息建模的基础。 |
| `FND/Relations/Relations.rdf` | 关系本体（Relations Ontology） | FIBO 最底层的基础本体，定义参考（reference）、分类（classify）等通用关系与抽象概念，全库普遍依赖。 |
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |
| `https://www.omg.org/spec/Commons/CodesAndCodeSets/` | OMG 通用代码与代码集本体（OMG Commons Codes and Code Sets） | Commons 库中的代码本体，定义代码、代码集及其维护方的通用概念，是 ISO 4217、ISO 3166 等编码体系建模的基础。 |
| `https://www.omg.org/spec/Commons/Collections/` | OMG 通用集合本体（OMG Commons Collections） | Commons 库中的集合本体，定义集合、成员等通用概念。 |
| `https://www.omg.org/spec/Commons/ContextualIdentifiers/` | OMG 通用语境标识符本体（OMG Commons Contextual Identifiers） | Commons 库中的语境标识符本体，定义在特定语境下唯一标识事物的标识符结构，是地址、账户类标识的基础。 |
| `https://www.omg.org/spec/Commons/DatesAndTimes/` | OMG 通用日期与时间本体（OMG Commons Dates and Times） | Commons 库中的日期时间本体，定义日期、期间、时间点等通用时间概念。 |
| `https://www.omg.org/spec/Commons/Designators/` | OMG 通用指称符本体（OMG Commons Designators） | Commons 库中的指称符本体，定义名称、标识符等「指代某物的符号」的通用概念。 |
| `https://www.omg.org/spec/Commons/Identifiers/` | OMG 通用标识符本体（OMG Commons Identifiers） | Commons 库中的标识符本体，定义标识符及其编码方案的通用概念。 |
| `https://www.omg.org/spec/Commons/Organizations/` | OMG 通用组织本体（OMG Commons Organizations） | Commons 库中的组织本体，定义组织、组织成员与组织结构的通用概念。 |
| `https://www.omg.org/spec/Commons/PartiesAndSituations/` | OMG 通用参与方与情境本体（OMG Commons Parties and Situations） | Commons 库中的参与方本体，定义独立主体、参与方及其角色扮演的通用概念，是 FIBO 参与方模型的上游。 |
| `https://www.omg.org/spec/Commons/RegistrationAuthorities/` | OMG 通用登记主管机构本体（OMG Commons Registration Authorities） | Commons 库中的登记主管机构本体，定义负责登记注册的主管机构及其登记行为的通用概念。 |
| `https://www.omg.org/spec/Commons/RegulatoryAgencies/` | OMG 通用监管机构本体（OMG Commons Regulatory Agencies） | Commons 库中的监管机构本体，定义监管机构及其监管职权的通用概念。 |
| `https://www.omg.org/spec/Commons/RolesAndCompositions/` | OMG 通用角色与构成本体（OMG Commons Roles and Compositions） | Commons 库中的角色本体，定义角色及整体—部分构成关系的通用概念。 |
| `https://www.omg.org/spec/LCC/Countries/CountryRepresentation/` | LCC 国家表示本体（LCC Country Representation） | OMG 国家语言代码库（LCC）中的国家表示本体，定义国家、国家标识等概念，是 ISO 3166 各国代码个体的类定义来源。 |

## 7. 文件

- 官方 RDF/XML：`FinancialServicesEntities.rdf`
- 中文 Turtle：`FinancialServicesEntities.ttl`
- 结构图：`FinancialServicesEntities-structure.png` / `FinancialServicesEntities-structure.svg`