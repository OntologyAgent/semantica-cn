# 美国金融服务实体本体（US Financial Services Entities Ontology）结构与公理说明

本文档对应 `USFinancialServicesEntities.rdf` / `USFinancialServicesEntities.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `USFinancialServicesEntities-structure.png`（`USFinancialServicesEntities-structure.svg` 为可缩放版本）。

![美国金融服务实体本体（US Financial Services Entities Ontology）本体结构图](USFinancialServicesEntities-structure.png)

## 1. 本体概述

定义美国法域下的金融服务机构类型与个体（国民银行、州立银行、注册投资顾问等）。

**在体系中的位置**：FBC 功能实体模块的北美扩展，美国体系的核心参考。

**上下游关系**：上游继承金融服务实体本体并依赖 BE 美国法域个体；下游被美国监管与 NIC 受控词汇配套使用。

**与相近概念的差别**：与欧盟体系的差别——美国实行双轨银行制度（联邦/州立）与功能监管，机构类型按注册与监管关系划分，颗粒度比欧盟牌照体系更细。

## 2. 类（Class）

| 类（Class） | 定义（Definition） |
|---|---|
| 纽约州第十二条投资公司（New York Article XII investment company） | 依纽约州银行法第十二条设立、拥有广泛借贷权限并可投资股票和债券的专业非存款性贷款机构。 |
| 美国银行（U.S. bank） | 获准在美国开展业务的银行。 |
| 美国银行控股公司（U.S. bank holding company） | 获准在美国开展业务、并依相关法律受联邦储备监管和监督的银行控股公司。 |
| 美国信用合作社（U.S. credit union） | 为促进会员节俭、并为勤俭或生产性目的创造信贷来源而组织的合作协会。 |
| 外国银行机构代理处（agency of a foreign banking organization） | 外国银行设于美国任何州的营业场所，在该场所维持贷方余额、兑付支票、发放贷款，或在法律允许范围内从事其他业务。 |
| 协议公司（agreement corporation） | 由州特许从事国际银行业务的公司，因该公司与联邦储备委员会订立「协议」而得名。 |
| 协议公司——银行类（agreement corporation - banking） | 章程允许其从事国际银行业务的协议公司。 |
| 协议公司——投资类（agreement corporation - investment） | 章程允许其从事国际投资银行业务的协议公司。 |
| 银行家银行（bankers' bank） | 除法律要求的董事资格股外，完全由其他存款性机构或存款性机构控股公司拥有的商业银行。 |
| 受准备金要求约束的银行家银行（bankers' bank subject to reserve requirements） | 其活动受联邦储备特定要求限制的银行家银行。 |
| 不受准备金要求约束的银行家银行（bankers' bank that is not subject to reserve requirements） | 其活动不受联邦储备特定要求限制的银行家银行。 |
| 存款性机构分支机构（branch of a depository institution） | 位于美国任何州、吸收存款的任何办事处或营业场所。 |
| 商业贷款公司（commercial lending company） | 依《联邦储备法》第 25 条以外的法律组建、从事商业贷款业务的机构（银行或依该法第 25 条运营的组织除外）。 |
| 合作银行（cooperative bank） | 依照其特许或组建所在州的法律组织和运营的州特许储蓄协会。 |
| 外国银行的境内分行（domestic branch of a foreign bank） | 外国银行设于美国任何州、吸收存款的营业场所，且不属于法规定义的代理处。 |
| 境内银行的境内分行（domestic branch of domestic bank） | 位于美国境内、其母行也位于美国境内的分行。 |
| 境内实体（domestic entity） | 在美国注册成立并以美国为住所地的金融服务提供商。 |
| 其他境内实体（domestic entity other） | 通常在美国从事与银行业务相关活动的境内机构。 |
| 境内实体的境内非银行子公司（domestic non-bank subsidiary of a domestic entity） | 总部位于美国、其 25% 或以上表决权股份由境内实体拥有或控制的非银行金融服务提供商。 |
| 埃奇公司（edge corporation） | 由联邦储备特许、从事国际银行和金融业务的股份公司，得名于《埃奇法》。 |
| 埃奇公司——银行类（edge corporation - banking） | 章程允许其从事国际银行业务的埃奇公司。 |
| 埃奇公司——境内分行（edge corporation - domestic branch） | 位于美国境内的埃奇公司分行。 |
| 埃奇公司——投资类（edge corporation - investment） | 章程允许其从事国际投资银行业务的埃奇公司。 |
| 农业信贷体系机构（farm credit system institution） | 由农业信贷管理局监督、检查和监管、并依相关法案运营的联邦特许金融机构。 |
| 外国银行机构的联邦代理处（federal agency of foreign banking organization） | 依《联邦法规汇编》第 12 编第 3102 节及 1978 年《国际银行法》第 4 节设立并运营的外国银行代理处。 |
| 外国银行机构的联邦分行（federal branch of foreign banking organization） | 依《联邦法规汇编》第 12 编第 3102 节及 1978 年《国际银行法》第 4 节设立并运营的外国银行分行。 |
| 联邦信用合作社（federal credit union） | 具有联邦隶属关系的信用合作社。 |
| 联邦储蓄银行（federal savings bank） | 具有联邦隶属关系的储蓄银行。 |
| 金融控股公司（financial holding company） | 依 1999 年《格雷姆-里奇-比利雷法》获准从事广泛银行相关业务的金融实体。 |
| 外国银行（foreign bank） | 依外国、美国属地、波多黎各、关岛、美属萨摩亚或维尔京群岛法律组建的金融机构。 |
| 外国银行机构（foreign banking organization） | 总部设在美国境外、可收购或设立独立银行或银行控股公司的金融服务提供商。 |
| 作为银行控股公司的外国银行机构（foreign banking organization as a bank holding company） | 在美国境内属于银行控股公司的外国银行机构。 |
| 银行控股公司旗下的外国银行机构（foreign banking organization of a bank holding company） | 由银行控股公司拥有或控制的外国银行机构。 |
| 美国银行的境外分行（foreign branch of US bank） | 位于美国境外、但其母行位于美国境内的分行。 |
| 外国银行的境外分行（foreign branch of foreign bank） | 位于美国境外、其母行也位于美国境外的分行。 |
| 由美国机构管理的外国银行境外分行（foreign branch of foreign bank managed by US office） | 位于美国境外、母行也在美国境外、但由该行的美国分行或代理处管理的分行。 |
| 其他境外实体（foreign entity other） | 通常在其所在国家从事与银行业务相关活动的境外机构。 |
| 工业银行（industrial bank） | 通过出售称为「投资股份」的凭证和吸收存款来筹集资金的有限服务金融机构。 |
| 外国银行机构的参保联邦分行（insured federal branch of foreign banking organization） | 外国银行设于美国任何州、吸收存款、依联邦法律设立并运营且受联邦存款保险公司承保的办事处或营业场所。 |
| 外国银行机构的参保州分行（insured state branch of foreign banking organization） | 外国银行设于美国任何州、吸收存款、依州法律设立并运营且受联邦存款保险公司承保的办事处或营业场所。 |
| 中间控股公司（intermediate holding company） | 外国银行机构依联邦储备委员会 YY 条例（12 CFR）O 分部分设立或指定的银行控股公司。 |
| 美国存款机构、埃奇公司或信托公司旗下的国际银行（international bank of US depositary, edge, trust company） | 由美国存款性机构、埃奇法公司或信托公司拥有或控制的银行。 |
| 境内实体的境外非银行子公司（international non-bank subsidiary of a domestic entity） | 总部位于美国境外、其 25% 或以上表决权股份由境内实体拥有或控制的非银行金融服务提供商。 |
| 外国银行的有限分行（limited branch of a foreign bank） | 仅吸收依《联邦储备法》第 25A 条组建的公司所允许吸收之存款的外国银行分行。 |
| 互助储蓄银行（mutual savings bank） | 主要从个人吸收存款、并将大部分资金投放于抵押贷款的金融机构。 |
| 国民银行（national bank） | 章程由货币监理署（OCC）而非州银行监管机构批准的商业银行。 |
| 境内实体的非银行子公司（non-bank subsidiary of a domestic entity） | 其 25% 或以上表决权股份由总部位于美国的实体拥有或控制的非银行实体。 |
| 非存款性信托公司（non-depository trust company） | 接受并执行信托但不发行货币的信托公司；可以是联邦储备成员或非成员。 |
| 外国银行办事机构（office of a foreign bank） | 外国银行在美国的任何分行、代理处、代表处或商业贷款公司子公司等设施。 |
| 外国银行区域行政办事处（regional administrative office of a foreign bank） | 由在美国运营两个或以上分行、代理处、商业贷款公司或银行的外国银行设立的代表处，承担区域管理职能。 |
| 外国银行代表处（representative office of a foreign bank） | 外国银行设于美国任何州、且不属于联邦分行、联邦代理处、州分行、州代理处或商业贷款公司的办事机构。 |
| 储蓄银行（savings bank） | 为吸收储蓄存款并对储蓄存款支付利息而组建的银行机构。 |
| 储蓄贷款协会（savings loan association） | 主要从个人吸收存款、并将资金主要投向住宅抵押贷款的金融机构。 |
| 储蓄贷款控股公司（savings loan holding company） | 直接或间接控制储蓄协会或相关控股公司的公司，明确排除同时属于银行控股公司的公司。 |
| 外国银行机构的州代理处（state agency of foreign banking organization） | 依美国任何州（含哥伦比亚特区）法律设立并运营的外国银行代理处。 |
| 外国银行机构的州分行（state branch of foreign banking organization） | 外国银行设于美国任何州、吸收存款、依该州法律设立并运营的分行。 |
| 州信用合作社（state credit union） | 具有州隶属关系的信用合作社。 |
| 州储蓄银行（state savings bank） | 具有州隶属关系的储蓄银行。 |
| 州特许银行（state-chartered bank） | 章程由州银行监管机构批准的商业银行。 |
| 境内实体的子公司（subsidiary of a domestic entity） | 其 25% 或以上表决权股份由总部位于美国的实体拥有或控制、或其实质多数股权受其控制的实体。 |
| 节俭机构（thrift institution） | 主要吸收储蓄账户存款并将大部分资金投资于抵押贷款的储蓄协会。 |
| 外国银行机构的未参保联邦代理处（uninsured federal agency of foreign banking organization） | 依《联邦法规汇编》第 12 编第 3102 节及 1978 年《国际银行法》第 4 节设立并运营、但不受联邦存款保险公司承保的外国银行代理处。 |
| 外国银行机构的未参保联邦分行（uninsured federal branch of foreign banking organization） | 外国银行设于美国任何州、吸收存款、依联邦法律设立并运营、但不受联邦存款保险公司承保的办事处或营业场所。 |
| 外国银行机构的未参保州代理处（uninsured state agency of foreign banking organization） | 依美国任何州法律设立并运营、不受联邦存款保险公司承保或监管的外国银行代理处。 |
| 外国银行机构的未参保州分行（uninsured state branch of foreign banking organization） | 外国银行设于美国任何州、吸收存款、依州法律设立并运营、但不受联邦存款保险公司承保的办事处或营业场所。 |

### 2.1 继承关系（Inheritance）

- 纽约州第十二条投资公司（New York Article XII investment company） ⊑ 非存款性机构
- 美国银行（U.S. bank） ⊑ 银行
- 美国银行（U.S. bank） ⊑ 境内实体（domestic entity）
- 美国银行控股公司（U.S. bank holding company） ⊑ 银行控股公司
- 美国银行控股公司（U.S. bank holding company） ⊑ 境内实体（domestic entity）
- 美国信用合作社（U.S. credit union） ⊑ 信用合作社
- 美国信用合作社（U.S. credit union） ⊑ 节俭机构（thrift institution）
- 外国银行机构代理处（agency of a foreign banking organization） ⊑ 金融机构
- 协议公司（agreement corporation） ⊑ 金融机构
- 协议公司——银行类（agreement corporation - banking） ⊑ 存款性机构
- 协议公司——银行类（agreement corporation - banking） ⊑ 协议公司（agreement corporation）
- 协议公司——投资类（agreement corporation - investment） ⊑ 投资银行
- 协议公司——投资类（agreement corporation - investment） ⊑ 协议公司（agreement corporation）
- 银行家银行（bankers' bank） ⊑ 商业银行
- 银行家银行（bankers' bank） ⊑ 美国银行（U.S. bank）
- 受准备金要求约束的银行家银行（bankers' bank subject to reserve requirements） ⊑ 银行家银行（bankers' bank）
- 不受准备金要求约束的银行家银行（bankers' bank that is not subject to reserve requirements） ⊑ 银行家银行（bankers' bank）
- 存款性机构分支机构（branch of a depository institution） ⊑ 分支机构
- 商业贷款公司（commercial lending company） ⊑ 非存款性机构
- 合作银行（cooperative bank） ⊑ 节俭机构（thrift institution）
- 外国银行的境内分行（domestic branch of a foreign bank） ⊑ 存款性机构分支机构（branch of a depository institution）
- 外国银行的境内分行（domestic branch of a foreign bank） ⊑ 外国银行办事机构（office of a foreign bank）
- 境内银行的境内分行（domestic branch of domestic bank） ⊑ 存款性机构分支机构（branch of a depository institution）
- 境内实体（domestic entity） ⊑ 金融服务提供商
- 其他境内实体（domestic entity other） ⊑ 境内实体（domestic entity）
- 境内实体的境内非银行子公司（domestic non-bank subsidiary of a domestic entity） ⊑ 境内实体（domestic entity）
- 境内实体的境内非银行子公司（domestic non-bank subsidiary of a domestic entity） ⊑ 境内实体的非银行子公司（non-bank subsidiary of a domestic entity）
- 埃奇公司（edge corporation） ⊑ 金融机构
- 埃奇公司——银行类（edge corporation - banking） ⊑ 存款性机构
- 埃奇公司——银行类（edge corporation - banking） ⊑ 埃奇公司（edge corporation）
- 埃奇公司——境内分行（edge corporation - domestic branch） ⊑ 分支机构
- 埃奇公司——投资类（edge corporation - investment） ⊑ 投资银行
- 埃奇公司——投资类（edge corporation - investment） ⊑ 埃奇公司（edge corporation）
- 农业信贷体系机构（farm credit system institution） ⊑ 金融机构
- 农业信贷体系机构（farm credit system institution） ⊑ 境内实体（domestic entity）
- 外国银行机构的联邦代理处（federal agency of foreign banking organization） ⊑ 外国银行机构代理处（agency of a foreign banking organization）
- 外国银行机构的联邦分行（federal branch of foreign banking organization） ⊑ 外国银行的境内分行（domestic branch of a foreign bank）
- 联邦信用合作社（federal credit union） ⊑ 美国信用合作社（U.S. credit union）
- 联邦储蓄银行（federal savings bank） ⊑ 储蓄银行（savings bank）
- 金融控股公司（financial holding company） ⊑ 银行控股公司
- 外国银行（foreign bank） ⊑ 银行
- 外国银行机构（foreign banking organization） ⊑ 金融服务提供商
- 作为银行控股公司的外国银行机构（foreign banking organization as a bank holding company） ⊑ 银行控股公司
- 作为银行控股公司的外国银行机构（foreign banking organization as a bank holding company） ⊑ 外国银行机构（foreign banking organization）
- 银行控股公司旗下的外国银行机构（foreign banking organization of a bank holding company） ⊑ 外国银行机构（foreign banking organization）
- 美国银行的境外分行（foreign branch of US bank） ⊑ 存款性机构分支机构（branch of a depository institution）
- 外国银行的境外分行（foreign branch of foreign bank） ⊑ 存款性机构分支机构（branch of a depository institution）
- 由美国机构管理的外国银行境外分行（foreign branch of foreign bank managed by US office） ⊑ 外国银行的境外分行（foreign branch of foreign bank）
- 其他境外实体（foreign entity other） ⊑ 金融机构
- 工业银行（industrial bank） ⊑ 银行
- 外国银行机构的参保联邦分行（insured federal branch of foreign banking organization） ⊑ 外国银行机构的联邦分行（federal branch of foreign banking organization）
- 外国银行机构的参保州分行（insured state branch of foreign banking organization） ⊑ 外国银行机构的州分行（state branch of foreign banking organization）
- 中间控股公司（intermediate holding company） ⊑ 银行控股公司
- 美国存款机构、埃奇公司或信托公司旗下的国际银行（international bank of US depositary, edge, trust company） ⊑ 银行
- 境内实体的境外非银行子公司（international non-bank subsidiary of a domestic entity） ⊑ 境内实体的非银行子公司（non-bank subsidiary of a domestic entity）
- 外国银行的有限分行（limited branch of a foreign bank） ⊑ 外国银行的境内分行（domestic branch of a foreign bank）
- 互助储蓄银行（mutual savings bank） ⊑ 储蓄银行（savings bank）
- 国民银行（national bank） ⊑ 商业银行
- 国民银行（national bank） ⊑ 美国银行（U.S. bank）
- 境内实体的非银行子公司（non-bank subsidiary of a domestic entity） ⊑ 境内实体的子公司（subsidiary of a domestic entity）
- 非存款性信托公司（non-depository trust company） ⊑ 非存款性机构
- 非存款性信托公司（non-depository trust company） ⊑ 信托公司
- 外国银行办事机构（office of a foreign bank） ⊑ 设施
- 外国银行区域行政办事处（regional administrative office of a foreign bank） ⊑ 外国银行代表处（representative office of a foreign bank）
- 外国银行代表处（representative office of a foreign bank） ⊑ 外国银行办事机构（office of a foreign bank）
- 储蓄银行（savings bank） ⊑ 节俭机构（thrift institution）
- 储蓄贷款协会（savings loan association） ⊑ 节俭机构（thrift institution）
- 储蓄贷款控股公司（savings loan holding company） ⊑ 控股公司
- 储蓄贷款控股公司（savings loan holding company） ⊑ 金融服务提供商
- 外国银行机构的州代理处（state agency of foreign banking organization） ⊑ 外国银行机构代理处（agency of a foreign banking organization）
- 外国银行机构的州分行（state branch of foreign banking organization） ⊑ 外国银行的境内分行（domestic branch of a foreign bank）
- 州信用合作社（state credit union） ⊑ 美国信用合作社（U.S. credit union）
- 州储蓄银行（state savings bank） ⊑ 储蓄银行（savings bank）
- 州特许银行（state-chartered bank） ⊑ 商业银行
- 州特许银行（state-chartered bank） ⊑ 美国银行（U.S. bank）
- 境内实体的子公司（subsidiary of a domestic entity） ⊑ 子公司
- 节俭机构（thrift institution） ⊑ 储蓄协会
- 节俭机构（thrift institution） ⊑ 境内实体（domestic entity）
- 外国银行机构的未参保联邦代理处（uninsured federal agency of foreign banking organization） ⊑ 外国银行机构的联邦代理处（federal agency of foreign banking organization）
- 外国银行机构的未参保联邦分行（uninsured federal branch of foreign banking organization） ⊑ 外国银行机构的联邦分行（federal branch of foreign banking organization）
- 外国银行机构的未参保州代理处（uninsured state agency of foreign banking organization） ⊑ 外国银行机构的州代理处（state agency of foreign banking organization）
- 外国银行机构的未参保州分行（uninsured state branch of foreign banking organization） ⊑ 外国银行机构的州分行（state branch of foreign banking organization）

## 3. 对象属性（Object Property）

| 属性（Property） | 中文（English） | 定义（Definition） | 说明 |
|---|---|---|---|
| fibo-fbc-fct-usfse:hasHomeCountry | 具有母国（has home country） | 就外国银行而言，指明该外国银行获得特许或注册成立的国家。 | 定义域（domain）：金融服务提供商；值域（range）：国家；子属性（subPropertyOf）：具有国家 |
| fibo-fbc-fct-usfse:hasHomeCountrySupervisor | 具有母国监管机构（has home country supervisor） | 就外国银行而言，指明其母国负有监管职责的政府实体。 | 定义域（domain）：金融服务提供商；值域（range）：监管机构；子属性（subPropertyOf）：受……监管 |

## 4. 数据属性（Datatype Property）

| 属性（Property） | 中文（English） | 定义（Definition） |
|---|---|---|
| fibo-fbc-fct-usfse:isSubjectToReserveRequirements | 是否受准备金要求约束（is subject to reserve requirements） | 表明金融服务提供商的某项能力是否以符合联邦储备特定政策、法规或要求为条件。 |

## 5. 公理约定（Axioms）

- 纽约州第十二条投资公司（New York Article XII investment company） 与 投资公司 互斥（disjointWith）
- 美国银行控股公司（U.S. bank holding company）：具有被投公司 some 美国银行（U.S. bank）
- 美国信用合作社（U.S. credit union）：由…扮演（is played by） 非营利公司 =1
- 外国银行机构代理处（agency of a foreign banking organization）：是……的受控方 some 外国银行（foreign bank）
- 外国银行机构代理处（agency of a foreign banking organization）：是自有资产 some 外国银行（foreign bank）
- 外国银行机构代理处（agency of a foreign banking organization）：由…扮演（is played by） some 外国银行办事机构（office of a foreign bank）
- 外国银行机构代理处（agency of a foreign banking organization）：由…扮演（is played by） some（restriction）
- 协议公司（agreement corporation）：由…扮演（is played by） 公司 =1
- 银行家银行（bankers' bank）：restriction
- 受准备金要求约束的银行家银行（bankers' bank subject to reserve requirements）：restriction
- 不受准备金要求约束的银行家银行（bankers' bank that is not subject to reserve requirements）：restriction
- 存款性机构分支机构（branch of a depository institution）：是……的部分 some（扮演角色（plays role） some 存款性机构）
- 外国银行的境内分行（domestic branch of a foreign bank）：restriction
- 外国银行的境内分行（domestic branch of a foreign bank）：是……的部分 some（扮演角色（plays role） some 外国银行（foreign bank））
- 境内银行的境内分行（domestic branch of domestic bank）：restriction
- 境内银行的境内分行（domestic branch of domestic bank）：是……的部分 some（扮演角色（plays role） some 美国银行（U.S. bank））
- 境内实体（domestic entity）：由…扮演（is played by） some（restriction）
- 埃奇公司（edge corporation）：由…扮演（is played by） 公司 =1
- 埃奇公司——境内分行（edge corporation - domestic branch）：restriction
- 埃奇公司——境内分行（edge corporation - domestic branch）：是……的部分 some（扮演角色（plays role） some 埃奇公司（edge corporation））
- 外国银行（foreign bank）：具有母国监管机构（has home country supervisor） 监管机构 ≥0
- 外国银行（foreign bank）：具有母国（has home country） some 国家
- 外国银行（foreign bank） 与 中央银行 互斥（disjointWith）
- 外国银行（foreign bank） 与 美国银行（U.S. bank） 互斥（disjointWith）
- 外国银行机构（foreign banking organization）：具有母国监管机构（has home country supervisor） 监管机构 ≥0
- 外国银行机构（foreign banking organization）：具有母国（has home country） some 国家
- 作为银行控股公司的外国银行机构（foreign banking organization as a bank holding company）：由…扮演（is played by） some（restriction）
- 美国银行的境外分行（foreign branch of US bank）：是……的部分 some（扮演角色（plays role） some 美国银行（U.S. bank））
- 美国银行的境外分行（foreign branch of US bank） 与 境内银行的境内分行（domestic branch of domestic bank） 互斥（disjointWith）
- 外国银行的境外分行（foreign branch of foreign bank）：是……的部分 some（扮演角色（plays role） some 外国银行（foreign bank））
- 外国银行的境外分行（foreign branch of foreign bank） 与 境内银行的境内分行（domestic branch of domestic bank） 互斥（disjointWith）
- 外国银行的境外分行（foreign branch of foreign bank） 与 美国银行的境外分行（foreign branch of US bank） 互斥（disjointWith）
- 由美国机构管理的外国银行境外分行（foreign branch of foreign bank managed by US office）：由……管理 some（restriction）
- 其他境外实体（foreign entity other） 与 境内实体（domestic entity） 互斥（disjointWith）
- 美国存款机构、埃奇公司或信托公司旗下的国际银行（international bank of US depositary, edge, trust company）：是……的部分 some（扮演角色（plays role） some（restriction））
- 境内实体的境外非银行子公司（international non-bank subsidiary of a domestic entity） 与 境内实体的境内非银行子公司（domestic non-bank subsidiary of a domestic entity） 互斥（disjointWith）
- 境内实体的非银行子公司（non-bank subsidiary of a domestic entity）：是……的子公司 some（由…扮演（is played by） some 金融机构）
- 境内实体的非银行子公司（non-bank subsidiary of a domestic entity） 与 银行 互斥（disjointWith）
- 外国银行代表处（representative office of a foreign bank） 与 外国银行的境内分行（domestic branch of a foreign bank） 互斥（disjointWith）
- 储蓄贷款控股公司（savings loan holding company）：具有被投公司 some（restriction）
- 储蓄贷款控股公司（savings loan holding company） 与 银行控股公司 互斥（disjointWith）
- 外国银行机构的州分行（state branch of foreign banking organization） 与 外国银行机构的联邦分行（federal branch of foreign banking organization） 互斥（disjointWith）
- 州储蓄银行（state savings bank） 与 联邦储蓄银行（federal savings bank） 互斥（disjointWith）
- 境内实体的子公司（subsidiary of a domestic entity）：是……的子公司 some（由…扮演（is played by） some 境内实体（domestic entity））
- 外国银行机构的未参保联邦分行（uninsured federal branch of foreign banking organization） 与 外国银行机构的参保联邦分行（insured federal branch of foreign banking organization） 互斥（disjointWith）
- 外国银行机构的未参保州分行（uninsured state branch of foreign banking organization） 与 外国银行机构的参保州分行（insured state branch of foreign banking organization） 互斥（disjointWith）

## 6. 依赖（owl:imports，17 个）

本本体通过 `owl:imports` 引入以下本体，各项的中文名称与简介如下：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `BE/GovernmentEntities/NorthAmericanJurisdiction/USGovernmentEntitiesAndJurisdictions.rdf` | 美国政府实体与法域本体（US Government Entities and Jurisdictions Ontology） | 收录美国的政体、联邦与各州政府、法域个体，是北美金融建模最常用的法域参考数据。 |
| `BE/LegalEntities/CorporateBodies.rdf` | 法人团体本体（Corporate Bodies Ontology） | 定义依法设立、具有独立法律人格的法人团体（corporate body），是股份有限公司等具体法人类型的上位概念。 |
| `BE/LegalEntities/FormalBusinessOrganizations.rdf` | 正式商业组织本体（Formal Business Organizations Ontology） | 定义以营利为目的、依法注册的正式商业组织，连接法律实体与其商业功能。 |
| `BE/OwnershipAndControl/CorporateControl.rdf` | 公司控制本体（Corporate Control Ontology） | 定义公司层面的控制关系：控股股东、多数/少数控制、表决权控制等。 |
| `FBC/FunctionalEntities/FinancialServicesEntities.rdf` | 金融服务实体本体（Financial Services Entities Ontology） | FBC 域核心本体，定义金融服务机构（银行、券商、保险公司、资管机构等）的功能分类体系。 |
| `FBC/ProductsAndServices/FinancialProductsAndServices.rdf` | 金融产品与服务本体（Financial Products and Services Ontology） | 定义金融产品（financial product）与金融服务（financial service）及其提供、购买关系。 |
| `FND/OwnershipAndControl/Control.rdf` | 控制本体（Control Ontology） | 定义「控制」关系：控制方、被控制方与控制程度，用于公司治理与合并报表判断。 |
| `FND/OwnershipAndControl/Ownership.rdf` | 所有权本体（Ownership Ontology） | 定义「拥有」关系：所有者、被拥有资产及所有权份额。 |
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |
| `https://www.omg.org/spec/Commons/Collections/` | OMG 通用集合本体（OMG Commons Collections） | Commons 库中的集合本体，定义集合、成员等通用概念。 |
| `https://www.omg.org/spec/Commons/Locations/` | OMG 通用位置本体（OMG Commons Locations） | Commons 库中的位置本体，定义地理位置、地点的通用概念。 |
| `https://www.omg.org/spec/Commons/Organizations/` | OMG 通用组织本体（OMG Commons Organizations） | Commons 库中的组织本体，定义组织、组织成员与组织结构的通用概念。 |
| `https://www.omg.org/spec/Commons/RegulatoryAgencies/` | OMG 通用监管机构本体（OMG Commons Regulatory Agencies） | Commons 库中的监管机构本体，定义监管机构及其监管职权的通用概念。 |
| `https://www.omg.org/spec/Commons/RolesAndCompositions/` | OMG 通用角色与构成本体（OMG Commons Roles and Compositions） | Commons 库中的角色本体，定义角色及整体—部分构成关系的通用概念。 |
| `https://www.omg.org/spec/Commons/SitesAndFacilities/` | OMG 通用场所与设施本体（OMG Commons Sites and Facilities） | Commons 库中的场所与设施本体，定义物理场所、设施及其位置的通用概念。 |
| `https://www.omg.org/spec/LCC/Countries/ISO3166-1-CountryCodes/` | LCC ISO 3166-1 国家代码（ISO 3166-1 Country Codes） | LCC 中 ISO 3166-1 标准的国家/地区代码个体集（如 CN、US、MX），供法域与地址建模引用。 |

## 7. 文件

- 官方 RDF/XML：`USFinancialServicesEntities.rdf`
- 中文 Turtle：`USFinancialServicesEntities.ttl`
- 结构图：`USFinancialServicesEntities-structure.png` / `USFinancialServicesEntities-structure.svg`