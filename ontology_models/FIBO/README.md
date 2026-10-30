# FIBO：金融行业业务本体参考样例

FIBO（Financial Industry Business Ontology，金融行业业务本体）是一套面向金融业务的正式本体。它把金融合同、商业实体、证券、衍生品、贷款、市场数据等概念，以及这些概念之间的关系，写成人和机器都能读取的标准化定义。

本目录是 FIBO 的中文导览和官方源码参考快照，不是对官方本体的翻译或改写。`master_2026Q3/` 保留官方仓库在该发布标签下的完整源码树，原始文件未作修改。

## 1. 快照信息

| 项目 | 内容 |
|---|---|
| 官方项目 | [edmcouncil/fibo](https://github.com/edmcouncil/fibo) |
| 本地版本 | `master_2026Q3`（2026 年第三季度正式发布） |
| 固定提交 | [`2d73435a4419b66b7c9f44cb9763e35fe8ac7890`](https://github.com/edmcouncil/fibo/commit/2d73435a4419b66b7c9f44cb9763e35fe8ac7890) |
| 官方发布说明 | [Q3 2026 Release](https://github.com/edmcouncil/fibo/releases/tag/master_2026Q3) |
| 本地快照 | [`master_2026Q3/`](master_2026Q3/) |
| 文件规模 | 468 个文件，其中 296 个为 RDF/XML 文件 |
| 官方文档 | [FIBO 官网](https://spec.edmcouncil.org/fibo/) · [FIBO Viewer](https://spec.edmcouncil.org/fibo/ontology) · [OMG 规范](https://www.omg.org/spec/EDMC-FIBO/) |
| 许可证 | MIT，见 [`master_2026Q3/LICENSE`](master_2026Q3/LICENSE) |

这里的“完整”是指该 GitHub 标签下的全部文件和全部 RDF，包括业务域、ACTUS、示例、测试数据、汇总入口、元数据、目录映射和许可证。FIBO 还会导入 OMG Commons 等仓库外的本体；这些远程导入不属于该 GitHub 仓库，因此不包含在本快照中。

项目内另有一份[三页 FIBO 速查卡](../../cheatsheet/FIBO/fibo-cheatsheet.html)，适合快速回顾；本 README 适合系统了解和查找原始文件。

## 2. 背景：为什么需要 FIBO

2008 年金融危机暴露了金融数据治理中的一个基础问题：不同机构、系统和监管报表使用不同术语和定义，同一概念难以对齐，跨系统汇总与风险分析因此变得困难。参与数据治理和管理的行业从业者由此推动统一金融术语的工作，FIBO 于 2014 年首次发布，之后持续扩展。

FIBO 由企业数据管理委员会（Enterprise Data Management Council，EDM Council）托管和赞助，并由对象管理组织（Object Management Group，OMG）标准化。其概念经过多年 EDMC 成员机构评审，目标是表达金融行业对公共概念的共识，而不是某一家机构的私有数据模型。

自 2020 年 1 月起，FIBO 采用开放社区流程开发。各领域团队持续修订 GitHub 内容，正式发布按季度进行。因此，引用 FIBO 时应同时注明季度版本，而不能只说“使用 FIBO”。

## 3. FIBO 解决什么问题

FIBO 的核心作用是提供一套独立于具体平台、机器可读且含义明确的金融公共词汇。典型用途包括：

- **跨系统数据整合**：让交易、客户、合同和参考数据系统对“机构”“发行人”“合约”等概念采用共同语义。
- **证券主数据管理**：区分证券本身、发行主体、发行条款、登记信息和市场价格，避免把不同层面的信息混成一张宽表。
- **监管报送**：使报表字段能够追溯到明确的业务概念，降低同一术语在不同报表中含义不一致的风险。
- **风险分析与管理**：明确合同义务、交易对手、担保、金融工具和事件之间的关系，为聚合与分析提供语义基础。
- **知识图谱与语义应用**：作为类、属性和约束的来源，支持实体对齐、关系建模、查询、推理和数据血缘说明。

FIBO 是概念本体，不是 FIX 那样的交易报文协议，也不是一套可直接查询的真实金融业务数据库。它主要回答“这些事物是什么、彼此有什么关系”，不规定线上消息格式，也不替代机构自己的业务数据。

## 4. 技术基础与建模方式

FIBO 使用万维网联盟（W3C）制定的网络本体语言（Web Ontology Language，OWL）编写，并以资源描述框架（Resource Description Framework，RDF）序列化。本仓库中的 `.rdf` 文件采用 RDF/XML 语法。

可以把它理解为三层配合：

- **RDF** 用三元组表达事实和关系，例如“某类工具——属于——证券”。
- **OWL** 在 RDF 之上定义类、属性、继承、等价、互斥和属性限制，使概念具有明确的形式语义。
- **描述逻辑（Description Logic）** 是 OWL 的逻辑基础，使推理工具能够检查概念关系并推出隐含结论。

FIBO 的模式层（TBox）描述类、属性和约束；断言层（ABox）包含具体个体。币种、国家、司法辖区、市场识别码等参照数据个体是 ABox 内容。只研究概念结构时通常选择 TBoxOnly；需要随本体使用参照数据时，则选择包含参照数据的入口。

OWL 的开放世界假设也不同于普通数据库校验：“没有记录”不等于“事实为假”。如果目标是检查必填字段、数据类型和取值范围，通常还需要 SHACL 等约束机制，不能只依赖 OWL。

## 5. 领域全景

### 5.1 十个传统金融业务域

以下按当前快照的实际目录列出。FND 是公共基础，其余域在其上构建；ACTUS 和 EXMP 在下一节单独说明。

| 域 | 中英文名称 | 主要内容 | RDF 数 |
|---|---|---|---:|
| [`FND`](master_2026Q3/FND/) | 基础（Foundations） | 人员、组织、地点、协议、合同、缔约方、条款、日期时间、数量、所有权等跨域公共概念 | 59 |
| [`BE`](master_2026Q3/BE/) | 商业实体（Business Entities） | 法人、公司、合伙、信托、政府实体、所有权与控制、法律实体标识及司法辖区 | 48 |
| [`BP`](master_2026Q3/BP/) | 业务流程（Business Process） | 证券发行与交易等金融流程，以及流程带来的时间维度 | 12 |
| [`CAE`](master_2026Q3/CAE/) | 公司行为与事件（Corporate Actions and Events） | 证券生命周期中的公司行为、相关事件和持有人可能需要响应的活动 | 7 |
| [`DER`](master_2026Q3/DER/) | 衍生品（Derivatives） | 期权、期货、远期、互换、信用衍生品、商品与货币合约、主协议 | 23 |
| [`FBC`](master_2026Q3/FBC/) | 金融业务与商业（Financial Business and Commerce） | 金融产品与服务、金融工具、中介、登记与监管机构、市场、结算、债务与担保 | 38 |
| [`IND`](master_2026Q3/IND/) | 指数与指标（Indices and Indicators） | 经济指标、外汇、利率、参考利率，以及股票、债券和信用指数 | 18 |
| [`LOAN`](master_2026Q3/LOAN/) | 贷款（Loan） | 商业、小微、汽车、教育、抵押贷款，以及合同义务、信用、风险和担保协议 | 20 |
| [`MD`](master_2026Q3/MD/) | 市场数据（Market Data） | 具有时间维度的价格、收益率、债务和资产池分析数据 | 11 |
| [`SEC`](master_2026Q3/SEC/) | 证券（Securities） | 证券分类、识别、发行、登记，以及股票、基金和债务工具 | 37 |

几个域之间的关系，可以用三个例子理解：

- 一份贷款合同会把 FND 的合同与缔约方、LOAN 的贷款条款，以及 FBC 的金融产品概念连接起来。
- 一只债券的发行定义主要落在 SEC 和 FND，其随时间变化的价格与收益率则落在 MD。
- 一份利率互换会组合 DER 的衍生品合同概念与 IND 的参考利率概念。

### 5.2 ACTUS、示例、测试与根目录文件

完整仓库不只包含上述业务域。

| 位置 | 内容 | RDF 数 |
|---|---|---:|
| [`ACTUS`](master_2026Q3/ACTUS/) | 算法合同类型统一标准（Algorithmic Contract Types Unified Standards）相关受控词表，包括 ACTUS 分类、合同术语、术语映射和域元数据 | 4 |
| [`EXMP`](master_2026Q3/EXMP/) | 法人、市场、股票、指数、利率互换等示例本体与示例个体 | 10 |
| [`etc`](master_2026Q3/etc/) | 不属于正式金融业务域的辅助内容；本版主要是 FND 组织、所有权和控制的测试数据 | 3 |
| 根目录 | 5 个 `AboutFIBO*.rdf` 汇总入口，加上 `MetadataFIBO.rdf` | 6 |

因此，当前版本可以按“10 个传统金融业务域 + ACTUS + 示例与辅助内容”理解。全部 296 个 RDF 的分布为：273 个在传统业务域，4 个在 ACTUS，10 个在 EXMP，3 个在 `etc`，6 个在根目录。

## 6. 2026Q3 版本要点

根据官方发布说明，本版的主要变化包括：

- 增加数字资产和数字代币标识符（Digital Token Identifier，DTI）相关概念，为对应 ISO 24165 的后续工作打基础。
- 发布 ACTUS 分类和 ACTUS 合同术语两个受控词表，并把与 FIBO 的映射拆到独立本体；映射仍处于 provisional（暂定）状态。
- 增加养老金计划和养老基金的支持，包括基于 OECD 分类的暂定本体。
- 按季度更新 ISO 市场识别码（MIC），并包含若干概念、元数据和一致性问题修复。

这些是本版变更摘要，不代表 FIBO 的全部能力；完整变更应以[官方发布说明](https://github.com/edmcouncil/fibo/releases/tag/master_2026Q3)为准。

## 7. 汇总入口怎么选

根目录的 `AboutFIBO*.rdf` 是导入清单，用来一次装载一组本体，不是把所有三元组物理合并到一个文件里。

| 文件 | 装载范围 | 适用场景 |
|---|---|---|
| [`AboutFIBOProd.rdf`](master_2026Q3/AboutFIBOProd.rdf) | 全部生产本体，包含参照数据和示例 | 需要完整生产内容的工具加载入口 |
| [`AboutFIBOProd-IncludingReferenceData.rdf`](master_2026Q3/AboutFIBOProd-IncludingReferenceData.rdf) | 生产本体和参照数据，但排除示例 | 需要币种、司法辖区、监管机构、MIC 等参照个体，不需要示例 |
| [`AboutFIBOProd-TBoxOnly.rdf`](master_2026Q3/AboutFIBOProd-TBoxOnly.rdf) | 生产本体，目标是排除参照数据和示例 | 主要研究类、属性和模式结构 |
| [`AboutFIBODev.rdf`](master_2026Q3/AboutFIBODev.rdf) | 已发布、暂定和参考性本体 | 跟踪或参与开发，接受尚未定稿的概念 |
| [`AboutFIBODev-TBoxOnly.rdf`](master_2026Q3/AboutFIBODev-TBoxOnly.rdf) | 开发范围，排除参照数据和示例 | 研究最新模式结构 |

TBoxOnly 的范围以官方入口说明为准；当前官方注释特别指出，SEC 的 `Bonds` 仍会带入部分参照个体，不能把文件名理解为对所有间接导入内容的绝对保证。

[`MetadataFIBO.rdf`](master_2026Q3/MetadataFIBO.rdf) 是描述 FIBO 及各域的顶层元数据词表，不是生产本体的全量装载入口。生产与开发内容不应混载；应用对外交换或固定依赖时，应明确记录季度版本。

## 8. 如何阅读和加载

推荐按以下顺序阅读：

1. 从 [`FND`](master_2026Q3/FND/) 开始，先理解人员、组织、地点、协议、合同、相关方和条款。
2. 再看 [`BE`](master_2026Q3/BE/) 与 [`FBC`](master_2026Q3/FBC/)，分清“主体是谁”“主体在金融业务中扮演什么角色”。
3. 按业务问题进入 SEC、DER、LOAN、IND、MD、CAE 或 BP，不必从头到尾逐文件阅读。
4. 使用 [FIBO Viewer](https://spec.edmcouncil.org/fibo/ontology) 查定义和继承关系，再回到本地 RDF 核对正式表达与版本。

可以使用 Protégé 等 RDF/OWL 工具打开汇总入口。[`catalog-v001.xml`](master_2026Q3/catalog-v001.xml) 用于把本体标识映射到本地文件；需要离线或严格复现本版本时，应让工具使用本地目录映射，避免直接按网络地址导入到其他时间的最新内容。

本快照只保证官方仓库文件完整，不保证所有外部 `owl:imports` 都已离线收集。Semantica 的 `OntologyIngestor` 可以解析其中的单个 RDF 文件，但单文件解析不会自动把全部间接导入展开成一个完整图谱。

## 9. 治理、扩展与许可证

FIBO 的价值来自行业共识。业务需要扩展时，通常应新建子类或本地扩展本体，而不是直接修改共识概念的定义。若希望回馈上游，应遵循官方[`贡献指南`](master_2026Q3/CONTRIBUTING.md)、[`本体建模指南`](master_2026Q3/ONTOLOGY_GUIDE.md)和开发者来源证书（Developer Certificate of Origin，DCO）要求。

本快照保留 MIT 许可证原文。使用、修改和再分发时，应保留适用的版权与许可声明；FIBO 名称本身也是 EDM Council 的商标，开源许可证不等于商标授权。

## 10. 主要资料来源

- [官方 GitHub 仓库](https://github.com/edmcouncil/fibo)及本快照中的[官方 README](master_2026Q3/README.md)
- [2026Q3 官方发布说明](https://github.com/edmcouncil/fibo/releases/tag/master_2026Q3)
- [FIBO 官方网站与 Viewer](https://spec.edmcouncil.org/fibo/)
- [OMG 的 FIBO 规范页](https://www.omg.org/spec/EDMC-FIBO/)
- 本地根目录各 `AboutFIBO*.rdf` 和 `MetadataFIBO.rdf` 中的官方说明
