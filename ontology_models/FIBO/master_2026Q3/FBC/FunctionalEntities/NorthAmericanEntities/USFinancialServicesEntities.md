# 美国金融服务实体本体（US Financial Services Entities Ontology）结构与公理说明

本文档对应 `USFinancialServicesEntities.rdf` / `USFinancialServicesEntities.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `USFinancialServicesEntities-structure.png`（`USFinancialServicesEntities-structure.svg` 为可缩放版本）。

![美国金融服务实体本体（US Financial Services Entities Ontology）本体结构图](USFinancialServicesEntities-structure.png)

## 1. 本体概述

定义美国法域下的金融服务机构类型与个体（国民银行、州立银行、注册投资顾问等）。

**在体系中的位置**：FBC 功能实体模块的北美扩展，美国体系的核心参考。

**上下游关系**：上游继承金融服务实体本体并依赖 BE 美国法域个体；下游被美国监管与 NIC 受控词汇配套使用。

**与相近概念的差别**：与欧盟体系的差别——美国实行双轨银行制度（联邦/州立）与功能监管，机构类型按注册与监管关系划分，颗粒度比欧盟牌照体系更细。

本本体中类与类的核心关系如下（完整细节见各类小节）：

- **纽约州第十二条投资公司（New York Article XII investment company）** 继承 **非存款性机构（NonDepositoryInstitution）**
- **美国银行（U.S. bank）** 继承 **银行（Bank）**
- **美国银行（U.S. bank）** 继承 **境内实体（domestic entity）**
- **美国银行控股公司（U.S. bank holding company）** 继承 **银行控股公司（BankHoldingCompany）**
- **美国银行控股公司（U.S. bank holding company）** 继承 **境内实体（domestic entity）**
- **美国信用合作社（U.S. credit union）** 继承 **信用合作社（CreditUnion）**
- **美国信用合作社（U.S. credit union）** 继承 **节俭机构（thrift institution）**
- **外国银行机构代理处（agency of a foreign banking organization）** 继承 **金融机构（FinancialInstitution）**
- **协议公司（agreement corporation）** 继承 **金融机构（FinancialInstitution）**
- **协议公司——银行类（agreement corporation - banking）** 继承 **存款性机构（DepositoryInstitution）**
- **协议公司——银行类（agreement corporation - banking）** 继承 **协议公司（agreement corporation）**
- **协议公司——投资类（agreement corporation - investment）** 继承 **投资银行（InvestmentBank）**
- 其余 70 条关系从略。

## 2. 类（Class）

| 类（Class） | 定义（Definition） |
|---|---|
| 纽约州第十二条投资公司（New York Article XII investment company） | 依纽约州银行法第十二条设立、拥有广泛借贷权限并可投资股票和债券的专业非存款性贷款机构。<br>specialized non-depository lending institution that has broad borrowing and lending powers and may invest in stocks and bonds |
| 美国银行（U.S. bank） | 获准在美国开展业务的银行。<br>bank that is licensed to conduct business in the United States |
| 美国银行控股公司（U.S. bank holding company） | 获准在美国开展业务、并依相关法律受联邦储备监管和监督的银行控股公司。<br>bank holding company that is licensed to conduct business in the United States and is regulated and supervised by the Federal Reserve in accordance with the Bank Holding Company Act of 1956 |
| 美国信用合作社（U.S. credit union） | 为促进会员节俭、并为勤俭或生产性目的创造信贷来源而组织的合作协会。<br>cooperative association organized for the purpose of promoting thrift among its members and creating a source of credit for provident or productive purposes |
| 外国银行机构代理处（agency of a foreign banking organization） | 外国银行设于美国任何州的营业场所，在该场所维持贷方余额、兑付支票、发放贷款，或在法律允许范围内从事其他业务。<br>place of business of a foreign bank, located in any state, at which credit balances are maintained, checks are paid, money is lent, or, to the extent not prohibited by state or federal law, deposits are accepted from a person or entity that is not a citizen or resident of the United States |
| 协议公司（agreement corporation） | 由州特许从事国际银行业务的公司，因该公司与联邦储备委员会订立「协议」而得名。<br>corporation chartered by a state to engage in international banking, so named because the corporation enters into an 'agreement' with the Fed's Board of Governors that it will limit its activities to those permitted |
| 协议公司——银行类（agreement corporation - banking） | 章程允许其从事国际银行业务的协议公司。<br>agreement corporation whose charter allows the corporation to engage in international banking |
| 协议公司——投资类（agreement corporation - investment） | 章程允许其从事国际投资银行业务的协议公司。<br>agreement corporation whose charter allows the corporation to engage in international investment banking |
| 银行家银行（bankers' bank） | 除法律要求的董事资格股外，完全由其他存款性机构或存款性机构控股公司拥有的商业银行。<br>commercial bank owned exclusively (except to the extent directors' qualifying shares are required by law) by other depository institutions or depository institution holding companies, the activities of which are limited by its articles of association exclusively to providing services to or for other depository institutions, their holding companies, and the officers, directors, and employees of such institutions and companies, and to providing correspondent banking services at the request of other depository institutions or their holding companies |
| 受准备金要求约束的银行家银行（bankers' bank subject to reserve requirements） | 其活动受联邦储备特定要求限制的银行家银行。<br>bankers' bank whose activities are limited by specific requirements of the Federal Reserve |
| 不受准备金要求约束的银行家银行（bankers' bank that is not subject to reserve requirements） | 其活动不受联邦储备特定要求限制的银行家银行。<br>bankers' bank whose activities are not limited by specific requirements of the Federal Reserve |
| 存款性机构分支机构（branch of a depository institution） | 位于美国任何州、吸收存款的任何办事处或营业场所。<br>any office or any place of business located in any State of the United States at which deposits are received |
| 商业贷款公司（commercial lending company） | 依《联邦储备法》第 25 条以外的法律组建、从事商业贷款业务的机构（银行或依该法第 25 条运营的组织除外）。<br>any institution, other than a bank or an organization operating under section 25 of the Federal Reserve Act [12 U.S.C. 601 et seq.], organized under the laws of any State of the United States, or the District of Columbia which maintains credit balances incidental to or arising out of the exercise of banking powers and engages in the business of making commercial loans |
| 合作银行（cooperative bank） | 依照其特许或组建所在州的法律组织和运营的州特许储蓄协会。<br>state-chartered savings association that is organized and operates according to the laws of the state in which it is chartered or organized, including Massachusetts, New Hampshire, Rhode Island or Vermont |
| 外国银行的境内分行（domestic branch of a foreign bank） | 外国银行设于美国任何州、吸收存款的营业场所，且不属于法规定义的代理处。<br>place of business of a foreign bank, located in any state, at which deposits are received, and that is not an agency as defined in https://www.ecfr.gov/current/title-12/chapter-II/subchapter-A/part-211/subpart-B/section-211.21 |
| 境内银行的境内分行（domestic branch of domestic bank） | 位于美国境内、其母行也位于美国境内的分行。<br>branch that resides in the United States, and whose parent is also located in the United States |
| 境内实体（domestic entity） | 在美国注册成立并以美国为住所地的金融服务提供商。<br>financial service provider that is incorporated and domiciled in the United States |
| 其他境内实体（domestic entity other） | 通常在美国从事与银行业务相关活动的境内机构。<br>domestic institution that engages in banking activities usually in connection with the business of banking in the United States |
| 境内实体的境内非银行子公司（domestic non-bank subsidiary of a domestic entity） | 总部位于美国、其 25% 或以上表决权股份由境内实体拥有或控制的非银行金融服务提供商。<br>non-bank financial service provider based in the United States of which 25 percent or more of whose voting shares are owned or controlled by an entity that is also based in the United States, or of which a majority of its directors are controlled by such domestic entity, or of which 25 percent or more of whose voting shares are held by trustees for the benefit of the shareholders or members of such domestic entity |
| 埃奇公司（edge corporation） | 由联邦储备特许、从事国际银行和金融业务的股份公司，得名于《埃奇法》。<br>corporation chartered by the Federal Reserve to engage in international banking and financial operations |
| 埃奇公司——银行类（edge corporation - banking） | 章程允许其从事国际银行业务的埃奇公司。<br>edge corporation whose charter allows the corporation to engage in international banking |
| 埃奇公司——境内分行（edge corporation - domestic branch） | 位于美国境内的埃奇公司分行。<br>branch of an edge corporation that is located in the United States |
| 埃奇公司——投资类（edge corporation - investment） | 章程允许其从事国际投资银行业务的埃奇公司。<br>edge corporation whose charter allows the corporation to engage in international investment banking |
| 农业信贷体系机构（farm credit system institution） | 由农业信贷管理局监督、检查和监管、并依相关法案运营的联邦特许金融机构。<br>federally-chartered financial institution that is supervised, examined, and regulated by the Farm Credit Administration and operates in accordance with the Farm Credit Act of 1971, as amended, 12 U.S.C. 2001 et seq |
| 外国银行机构的联邦代理处（federal agency of foreign banking organization） | 依《联邦法规汇编》第 12 编第 3102 节及 1978 年《国际银行法》第 4 节设立并运营的外国银行代理处。<br>agency of a foreign bank established and operating under section 3102 of CFR Title 12, Chapter 32 and section 4 of the International Banking Act of 1978 |
| 外国银行机构的联邦分行（federal branch of foreign banking organization） | 依《联邦法规汇编》第 12 编第 3102 节及 1978 年《国际银行法》第 4 节设立并运营的外国银行分行。<br>branch of a foreign bank established and operating under section 3102 of CFR Title 12, Chapter 32 and section 4 of the International Banking Act of 1978 |
| 联邦信用合作社（federal credit union） | 具有联邦隶属关系的信用合作社。<br>credit union that has a federal affiliation |
| 联邦储蓄银行（federal savings bank） | 具有联邦隶属关系的储蓄银行。<br>savings bank that has a federal affiliation |
| 金融控股公司（financial holding company） | 依 1999 年《格雷姆-里奇-比利雷法》获准从事广泛银行相关业务的金融实体。<br>financial entity engaged in a broad range of banking-related activities as permitted under the Gramm-Leach-Bliley Act of 1999 |
| 外国银行（foreign bank） | 依外国、美国属地、波多黎各、关岛、美属萨摩亚或维尔京群岛法律组建的金融机构。<br>financial institution organized under the laws of a foreign country, a territory of the United States, Puerto Rico, Guam, American Samoa, or the Virgin Islands, which engages in the business of banking, or any subsidiary or affiliate, organized under such laws, of any such institution |
| 外国银行机构（foreign banking organization） | 总部设在美国境外、可收购或设立独立银行或银行控股公司的金融服务提供商。<br>financial service provider that is headquartered outside the United States and that can acquire or establish freestanding banks or bank holding companies in the United States |
| 作为银行控股公司的外国银行机构（foreign banking organization as a bank holding company） | 在美国境内属于银行控股公司的外国银行机构。<br>foreign banking organization that is a bank holding company in the United States |
| 银行控股公司旗下的外国银行机构（foreign banking organization of a bank holding company） | 由银行控股公司拥有或控制的外国银行机构。<br>foreign banking organization that is owned or controlled by a bank holding company |
| 美国银行的境外分行（foreign branch of US bank） | 位于美国境外、但其母行位于美国境内的分行。<br>branch that resides outside of the United States, but has a parent that is located in the United States |
| 外国银行的境外分行（foreign branch of foreign bank） | 位于美国境外、其母行也位于美国境外的分行。<br>branch that resides outside of the United States whose parent is located outside of the United States |
| 由美国机构管理的外国银行境外分行（foreign branch of foreign bank managed by US office） | 位于美国境外、母行也在美国境外、但由该行的美国分行或代理处管理的分行。<br>branch that resides outside of the United States whose parent is located outside of the United States that is managed by a US branch or agency of the foreign bank |
| 其他境外实体（foreign entity other） | 通常在其所在国家从事与银行业务相关活动的境外机构。<br>foreign institution that engages in banking activities usually in connection with the business of banking in the countries where such foreign institutions are organized or operating |
| 工业银行（industrial bank） | 通过出售称为「投资股份」的凭证和吸收存款来筹集资金的有限服务金融机构。<br>limited service financial institution that raises funds by selling certificates called 'investment shares' and by accepting deposits |
| 外国银行机构的参保联邦分行（insured federal branch of foreign banking organization） | 外国银行设于美国任何州、吸收存款、依联邦法律设立并运营且受联邦存款保险公司承保的办事处或营业场所。<br>any office or any place of business of a foreign bank located in any State of the United States at which deposits are received established and operating under section 4 of the International Banking Act of 1978 that is insured and regulated by the Federal Deposit Insurance Corporation (FDIC) |
| 外国银行机构的参保州分行（insured state branch of foreign banking organization） | 外国银行设于美国任何州、吸收存款、依州法律设立并运营且受联邦存款保险公司承保的办事处或营业场所。<br>any office or any place of business of a foreign bank located in any State of the United States at which deposits are received, established and operating under the laws of that State that is insured and regulated by the Federal Deposit Insurance Corporation (FDIC) |
| 中间控股公司（intermediate holding company） | 外国银行机构依联邦储备委员会 YY 条例（12 CFR）O 分部分设立或指定的银行控股公司。<br>bank holding company established or designated by a foreign banking organization under subpart O of the Federal Reserve Board's Regulation YY (12 CFR part 252) |
| 美国存款机构、埃奇公司或信托公司旗下的国际银行（international bank of US depositary, edge, trust company） | 由美国存款性机构、埃奇法公司或信托公司拥有或控制的银行。<br>bank that is owned or controlled by a US depository institution, Edge Act corporation or trust company |
| 境内实体的境外非银行子公司（international non-bank subsidiary of a domestic entity） | 总部位于美国境外、其 25% 或以上表决权股份由境内实体拥有或控制的非银行金融服务提供商。<br>non-bank financial service provider based outside of the United States of which 25 percent or more of whose voting shares are owned or controlled by an entity that is based in the United States, or of which a majority of its directors are controlled by such domestic entity, or of which 25 percent or more of whose voting shares are held by trustees for the benefit of the shareholders or members of such domestic entity |
| 外国银行的有限分行（limited branch of a foreign bank） | 仅吸收依《联邦储备法》第 25A 条组建的公司所允许吸收之存款的外国银行分行。<br>branch of a foreign bank that receives only such deposits as would be permitted for a corporation organized under section 25A of the Federal Reserve Act (12 U.S.C. 611-631) |
| 互助储蓄银行（mutual savings bank） | 主要从个人吸收存款、并将大部分资金投放于抵押贷款的金融机构。<br>financial institution that accepts deposits primarily from individuals and places a large portion of its funds into mortgage loans |
| 国民银行（national bank） | 章程由货币监理署（OCC）而非州银行监管机构批准的商业银行。<br>commercial bank whose charter is approved by the Office of the Comptroller of the Currency (OCC) rather than by a state banking agency |
| 境内实体的非银行子公司（non-bank subsidiary of a domestic entity） | 其 25% 或以上表决权股份由总部位于美国的实体拥有或控制的非银行实体。<br>non-bank entity of which 25 percent or more of whose voting shares are owned or controlled by an entity that is based in the United States, or of which a majority of its directors are controlled by such domestic entity, or of which 25 percent or more of whose voting shares are held by trustees for the benefit of the shareholders or members of such domestic entity |
| 非存款性信托公司（non-depository trust company） | 接受并执行信托但不发行货币的信托公司；可以是联邦储备成员或非成员。<br>trust company that accepts and executes trusts, but does not issue currency; non-depository trust companies can either be Federal Reserve Members or Federal Reserve Non-members |
| 外国银行办事机构（office of a foreign bank） | 外国银行在美国的任何分行、代理处、代表处或商业贷款公司子公司等设施。<br>facility that is any branch, agency, representative office, or commercial lending company subsidiary of a foreign bank in the United States |
| 外国银行区域行政办事处（regional administrative office of a foreign bank） | 由在美国运营两个或以上分行、代理处、商业贷款公司或银行的外国银行设立的代表处，承担区域管理职能。<br>representative office that 
(1) Is established by a foreign bank that operates two or more branches, agencies, commercial lending companies, or banks in the United States; 
(2) Is located in the same city as one or more of the foreign bank's branches, agencies, commercial lending companies, or banks in the United States; 
(3) Manages, supervises, or coordinates the operations of the foreign bank or its affiliates, if any, in a particular geographic area that includes the United States or a region thereof, including by exercising credit approval authority in that area pursuant to written standards, credit policies, and procedures established by the foreign bank; and 
(4) Does not solicit business from actual or potential customers of the foreign bank or its affiliates. |
| 外国银行代表处（representative office of a foreign bank） | 外国银行设于美国任何州、且不属于联邦分行、联邦代理处、州分行、州代理处或商业贷款公司的办事机构。<br>office of a foreign bank which is located in any state and is not a federal branch, federal agency, state branch, state agency, or commercial lending company subsidiary |
| 储蓄银行（savings bank） | 为吸收储蓄存款并对储蓄存款支付利息而组建的银行机构。<br>banking institution organized to accept savings deposits and pay interest on those savings deposits |
| 储蓄贷款协会（savings loan association） | 主要从个人吸收存款、并将资金主要投向住宅抵押贷款的金融机构。<br>financial institution that accepts deposits primarily from individuals and channels its funds primarily into residential mortgage loans |
| 储蓄贷款控股公司（savings loan holding company） | 直接或间接控制储蓄协会或相关控股公司的公司，明确排除同时属于银行控股公司的公司。<br>company that directly or indirectly controls a savings association or related holding company, and explicitly excludes any company that is also a bank holding company |
| 外国银行机构的州代理处（state agency of foreign banking organization） | 依美国任何州（含哥伦比亚特区）法律设立并运营的外国银行代理处。<br>agency of a foreign bank established and operating under the laws of any state, where state means any State of the United States or the District of Columbia |
| 外国银行机构的州分行（state branch of foreign banking organization） | 外国银行设于美国任何州、吸收存款、依该州法律设立并运营的分行。<br>branch of a foreign bank located in any State of the United States at which deposits are received, established and operating under the laws of that State, where state means any State of the United States or the District of Columbia |
| 州信用合作社（state credit union） | 具有州隶属关系的信用合作社。<br>credit union that has a state affiliation |
| 州储蓄银行（state savings bank） | 具有州隶属关系的储蓄银行。<br>savings bank that has a state affiliation |
| 州特许银行（state-chartered bank） | 章程由州银行监管机构批准的商业银行。<br>commercial bank whose charter is approved by a state banking regulator |
| 境内实体的子公司（subsidiary of a domestic entity） | 其 25% 或以上表决权股份由总部位于美国的实体拥有或控制、或其实质多数股权受其控制的实体。<br>entity of which 25 percent or more of whose voting shares are owned or controlled by an entity that is based in the United States, or of which a majority of its directors are controlled by such domestic entity, or of which 25 percent or more of whose voting shares are held by trustees for the benefit of the shareholders or members of such domestic entity |
| 节俭机构（thrift institution） | 主要吸收储蓄账户存款并将大部分资金投资于抵押贷款的储蓄协会。<br>savings association that primarily accepts savings account deposits and invests most of the proceeds in mortgages |
| 外国银行机构的未参保联邦代理处（uninsured federal agency of foreign banking organization） | 依《联邦法规汇编》第 12 编第 3102 节及 1978 年《国际银行法》第 4 节设立并运营、但不受联邦存款保险公司承保的外国银行代理处。<br>agency of a foreign bank established and operating under section 3102 of CFR Title 12, Chapter 32 and section 4 of the International Banking Act of 1978 that is not insured or regulated by the Federal Deposit Insurance Corporation (FDIC) |
| 外国银行机构的未参保联邦分行（uninsured federal branch of foreign banking organization） | 外国银行设于美国任何州、吸收存款、依联邦法律设立并运营、但不受联邦存款保险公司承保的办事处或营业场所。<br>any office or any place of business of a foreign bank located in any State of the United States at which deposits are received established and operating under section 4 of the International Banking Act of 1978 that is not insured or regulated by the Federal Deposit Insurance Corporation (FDIC) |
| 外国银行机构的未参保州代理处（uninsured state agency of foreign banking organization） | 依美国任何州法律设立并运营、不受联邦存款保险公司承保或监管的外国银行代理处。<br>agency of a foreign bank established and operating under the laws of any state that is not insured or regulated by the Federal Deposit Insurance Corporation (FDIC) |
| 外国银行机构的未参保州分行（uninsured state branch of foreign banking organization） | 外国银行设于美国任何州、吸收存款、依州法律设立并运营、但不受联邦存款保险公司承保的办事处或营业场所。<br>any office or any place of business of a foreign bank located in any State of the United States at which deposits are received, established and operating under the laws of that State that is not insured or regulated by the Federal Deposit Insurance Corporation (FDIC) |

以下按类逐个展开：每个类给出继承关系、相关属性与公理约定；子类在父类之下降一级编号。

### 2.1 纽约州第十二条投资公司（New York Article XII investment company）

定义：依纽约州银行法第十二条设立、拥有广泛借贷权限并可投资股票和债券的专业非存款性贷款机构。

- 父类：**非存款性机构（NonDepositoryInstitution）**

公理：

- 与**投资公司（InvestmentCompany）**互斥：同一个体不能同时属于两者。

### 2.2 外国银行机构代理处（agency of a foreign banking organization）

定义：外国银行设于美国任何州的营业场所，在该场所维持贷方余额、兑付支票、发放贷款，或在法律允许范围内从事其他业务。

- 父类：**金融机构（FinancialInstitution）**
- 直接子类：**外国银行机构的联邦代理处（federal agency of foreign banking organization）**、**外国银行机构的州代理处（state agency of foreign banking organization）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **是……的受控方（isControlledPartyOf）** | — | — |
| **是自有资产（isOwnedAsset）** | — | — |
| **由…扮演（is played by）** | — | — |

公理：

- **是……的受控方（isControlledPartyOf）**至少有一个取值，类型是**外国银行（foreign bank）**。
- **是自有资产（isOwnedAsset）**至少有一个取值，类型是**外国银行（foreign bank）**。
- **由…扮演（is played by）**至少有一个取值，类型是**外国银行办事机构（office of a foreign bank）**。
- **由…扮演（is played by）**至少有一个取值，该取值满足：**注册于（isDomiciledIn）**的取值固定为 UnitedStatesOfAmerica。

#### 2.2.1 外国银行机构的联邦代理处（federal agency of foreign banking organization）

定义：依《联邦法规汇编》第 12 编第 3102 节及 1978 年《国际银行法》第 4 节设立并运营的外国银行代理处。

- 父类：**外国银行机构代理处（agency of a foreign banking organization）**
- 直接子类：**外国银行机构的未参保联邦代理处（uninsured federal agency of foreign banking organization）**

##### 2.2.1.1 外国银行机构的未参保联邦代理处（uninsured federal agency of foreign banking organization）

定义：依《联邦法规汇编》第 12 编第 3102 节及 1978 年《国际银行法》第 4 节设立并运营、但不受联邦存款保险公司承保的外国银行代理处。

- 父类：**外国银行机构的联邦代理处（federal agency of foreign banking organization）**

#### 2.2.2 外国银行机构的州代理处（state agency of foreign banking organization）

定义：依美国任何州（含哥伦比亚特区）法律设立并运营的外国银行代理处。

- 父类：**外国银行机构代理处（agency of a foreign banking organization）**
- 直接子类：**外国银行机构的未参保州代理处（uninsured state agency of foreign banking organization）**

##### 2.2.2.1 外国银行机构的未参保州代理处（uninsured state agency of foreign banking organization）

定义：依美国任何州法律设立并运营、不受联邦存款保险公司承保或监管的外国银行代理处。

- 父类：**外国银行机构的州代理处（state agency of foreign banking organization）**

### 2.3 协议公司（agreement corporation）

定义：由州特许从事国际银行业务的公司，因该公司与联邦储备委员会订立「协议」而得名。

- 父类：**金融机构（FinancialInstitution）**
- 直接子类：**协议公司——银行类（agreement corporation - banking）**、**协议公司——投资类（agreement corporation - investment）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由…扮演（is played by）** | — | — |

公理：

- **由…扮演（is played by）**恰好有 1 个**公司（Corporation）**。

#### 2.3.1 协议公司——银行类（agreement corporation - banking）

定义：章程允许其从事国际银行业务的协议公司。

- 父类：**存款性机构（DepositoryInstitution）**、**协议公司（agreement corporation）**

#### 2.3.2 协议公司——投资类（agreement corporation - investment）

定义：章程允许其从事国际投资银行业务的协议公司。

- 父类：**投资银行（InvestmentBank）**、**协议公司（agreement corporation）**

### 2.4 存款性机构分支机构（branch of a depository institution）

定义：位于美国任何州、吸收存款的任何办事处或营业场所。

- 父类：**分支机构（Branch）**
- 直接子类：**外国银行的境内分行（domestic branch of a foreign bank）**、**境内银行的境内分行（domestic branch of domestic bank）**、**美国银行的境外分行（foreign branch of US bank）**、**外国银行的境外分行（foreign branch of foreign bank）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **是……的部分（isPartOf）** | — | — |

公理：

- **是……的部分（isPartOf）**至少有一个取值，该取值满足：**扮演角色（plays role）**至少有一个取值，类型是**存款性机构（DepositoryInstitution）**。

#### 2.4.1 外国银行的境内分行（domestic branch of a foreign bank）

定义：外国银行设于美国任何州、吸收存款的营业场所，且不属于法规定义的代理处。

- 父类：**存款性机构分支机构（branch of a depository institution）**、**外国银行办事机构（office of a foreign bank）**
- 直接子类：**外国银行机构的联邦分行（federal branch of foreign banking organization）**、**外国银行的有限分行（limited branch of a foreign bank）**、**外国银行机构的州分行（state branch of foreign banking organization）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **是……的部分（isPartOf）** | — | — |
| **注册于（isDomiciledIn）** | — | — |

公理：

- **是……的部分（isPartOf）**至少有一个取值，该取值满足：**扮演角色（plays role）**至少有一个取值，类型是**外国银行（foreign bank）**。
- **注册于（isDomiciledIn）**的取值固定为 UnitedStatesOfAmerica。

##### 2.4.1.1 外国银行机构的联邦分行（federal branch of foreign banking organization）

定义：依《联邦法规汇编》第 12 编第 3102 节及 1978 年《国际银行法》第 4 节设立并运营的外国银行分行。

- 父类：**外国银行的境内分行（domestic branch of a foreign bank）**
- 直接子类：**外国银行机构的参保联邦分行（insured federal branch of foreign banking organization）**、**外国银行机构的未参保联邦分行（uninsured federal branch of foreign banking organization）**

###### 2.4.1.1.1 外国银行机构的参保联邦分行（insured federal branch of foreign banking organization）

定义：外国银行设于美国任何州、吸收存款、依联邦法律设立并运营且受联邦存款保险公司承保的办事处或营业场所。

- 父类：**外国银行机构的联邦分行（federal branch of foreign banking organization）**

###### 2.4.1.1.2 外国银行机构的未参保联邦分行（uninsured federal branch of foreign banking organization）

定义：外国银行设于美国任何州、吸收存款、依联邦法律设立并运营、但不受联邦存款保险公司承保的办事处或营业场所。

- 父类：**外国银行机构的联邦分行（federal branch of foreign banking organization）**

公理：

- 与**外国银行机构的参保联邦分行（insured federal branch of foreign banking organization）**互斥：同一个体不能同时属于两者。

##### 2.4.1.2 外国银行的有限分行（limited branch of a foreign bank）

定义：仅吸收依《联邦储备法》第 25A 条组建的公司所允许吸收之存款的外国银行分行。

- 父类：**外国银行的境内分行（domestic branch of a foreign bank）**

##### 2.4.1.3 外国银行机构的州分行（state branch of foreign banking organization）

定义：外国银行设于美国任何州、吸收存款、依该州法律设立并运营的分行。

- 父类：**外国银行的境内分行（domestic branch of a foreign bank）**
- 直接子类：**外国银行机构的参保州分行（insured state branch of foreign banking organization）**、**外国银行机构的未参保州分行（uninsured state branch of foreign banking organization）**

公理：

- 与**外国银行机构的联邦分行（federal branch of foreign banking organization）**互斥：同一个体不能同时属于两者。

###### 2.4.1.3.1 外国银行机构的参保州分行（insured state branch of foreign banking organization）

定义：外国银行设于美国任何州、吸收存款、依州法律设立并运营且受联邦存款保险公司承保的办事处或营业场所。

- 父类：**外国银行机构的州分行（state branch of foreign banking organization）**

###### 2.4.1.3.2 外国银行机构的未参保州分行（uninsured state branch of foreign banking organization）

定义：外国银行设于美国任何州、吸收存款、依州法律设立并运营、但不受联邦存款保险公司承保的办事处或营业场所。

- 父类：**外国银行机构的州分行（state branch of foreign banking organization）**

公理：

- 与**外国银行机构的参保州分行（insured state branch of foreign banking organization）**互斥：同一个体不能同时属于两者。

#### 2.4.2 境内银行的境内分行（domestic branch of domestic bank）

定义：位于美国境内、其母行也位于美国境内的分行。

- 父类：**存款性机构分支机构（branch of a depository institution）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **是……的部分（isPartOf）** | — | — |
| **注册于（isDomiciledIn）** | — | — |

公理：

- **是……的部分（isPartOf）**至少有一个取值，该取值满足：**扮演角色（plays role）**至少有一个取值，类型是**美国银行（U.S. bank）**。
- **注册于（isDomiciledIn）**的取值固定为 UnitedStatesOfAmerica。

#### 2.4.3 美国银行的境外分行（foreign branch of US bank）

定义：位于美国境外、但其母行位于美国境内的分行。

- 父类：**存款性机构分支机构（branch of a depository institution）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **是……的部分（isPartOf）** | — | — |

公理：

- **是……的部分（isPartOf）**至少有一个取值，该取值满足：**扮演角色（plays role）**至少有一个取值，类型是**美国银行（U.S. bank）**。
- 与**境内银行的境内分行（domestic branch of domestic bank）**互斥：同一个体不能同时属于两者。

#### 2.4.4 外国银行的境外分行（foreign branch of foreign bank）

定义：位于美国境外、其母行也位于美国境外的分行。

- 父类：**存款性机构分支机构（branch of a depository institution）**
- 直接子类：**由美国机构管理的外国银行境外分行（foreign branch of foreign bank managed by US office）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **是……的部分（isPartOf）** | — | — |

公理：

- **是……的部分（isPartOf）**至少有一个取值，该取值满足：**扮演角色（plays role）**至少有一个取值，类型是**外国银行（foreign bank）**。
- 与**境内银行的境内分行（domestic branch of domestic bank）**互斥：同一个体不能同时属于两者。
- 与**美国银行的境外分行（foreign branch of US bank）**互斥：同一个体不能同时属于两者。

##### 2.4.4.1 由美国机构管理的外国银行境外分行（foreign branch of foreign bank managed by US office）

定义：位于美国境外、母行也在美国境外、但由该行的美国分行或代理处管理的分行。

- 父类：**外国银行的境外分行（foreign branch of foreign bank）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由……管理（isManagedBy）** | — | — |

公理：

- **由……管理（isManagedBy）**至少有一个取值，该取值满足：该属性存在取值约束。

### 2.5 商业贷款公司（commercial lending company）

定义：依《联邦储备法》第 25 条以外的法律组建、从事商业贷款业务的机构（银行或依该法第 25 条运营的组织除外）。

- 父类：**非存款性机构（NonDepositoryInstitution）**

### 2.6 境内实体（domestic entity）

定义：在美国注册成立并以美国为住所地的金融服务提供商。

- 父类：**金融服务提供商（FinancialServiceProvider）**
- 直接子类：**美国银行（U.S. bank）**、**美国银行控股公司（U.S. bank holding company）**、**其他境内实体（domestic entity other）**、**境内实体的境内非银行子公司（domestic non-bank subsidiary of a domestic entity）**、**农业信贷体系机构（farm credit system institution）**、**节俭机构（thrift institution）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由…扮演（is played by）** | — | — |

公理：

- **由…扮演（is played by）**至少有一个取值，该取值满足：该属性存在取值约束。

#### 2.6.1 美国银行（U.S. bank）

定义：获准在美国开展业务的银行。

- 父类：**银行（Bank）**、**境内实体（domestic entity）**
- 直接子类：**银行家银行（bankers' bank）**、**国民银行（national bank）**、**州特许银行（state-chartered bank）**

##### 2.6.1.1 银行家银行（bankers' bank）

定义：除法律要求的董事资格股外，完全由其他存款性机构或存款性机构控股公司拥有的商业银行。

- 父类：**商业银行（CommercialBank）**、**美国银行（U.S. bank）**
- 直接子类：**受准备金要求约束的银行家银行（bankers' bank subject to reserve requirements）**、**不受准备金要求约束的银行家银行（bankers' bank that is not subject to reserve requirements）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **是否受准备金要求约束（is subject to reserve requirements）** | 表明金融服务提供商的某项能力是否以符合联邦储备特定政策、法规或要求为条件。<br>indicates whether some capability of a financial service provider is contingent on conformance with certain Federal Reserve policies, regulations, or other requirements | 值域：xsd:boolean |

公理：

- **是否受准备金要求约束（is subject to reserve requirements）**存在取值约束。

###### 2.6.1.1.1 受准备金要求约束的银行家银行（bankers' bank subject to reserve requirements）

定义：其活动受联邦储备特定要求限制的银行家银行。

- 父类：**银行家银行（bankers' bank）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **是否受准备金要求约束（is subject to reserve requirements）** | 表明金融服务提供商的某项能力是否以符合联邦储备特定政策、法规或要求为条件。<br>indicates whether some capability of a financial service provider is contingent on conformance with certain Federal Reserve policies, regulations, or other requirements | 值域：xsd:boolean |

公理：

- **是否受准备金要求约束（is subject to reserve requirements）**的取值固定为 true。

###### 2.6.1.1.2 不受准备金要求约束的银行家银行（bankers' bank that is not subject to reserve requirements）

定义：其活动不受联邦储备特定要求限制的银行家银行。

- 父类：**银行家银行（bankers' bank）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **是否受准备金要求约束（is subject to reserve requirements）** | 表明金融服务提供商的某项能力是否以符合联邦储备特定政策、法规或要求为条件。<br>indicates whether some capability of a financial service provider is contingent on conformance with certain Federal Reserve policies, regulations, or other requirements | 值域：xsd:boolean |

公理：

- **是否受准备金要求约束（is subject to reserve requirements）**的取值固定为 false。

##### 2.6.1.2 国民银行（national bank）

定义：章程由货币监理署（OCC）而非州银行监管机构批准的商业银行。

- 父类：**商业银行（CommercialBank）**、**美国银行（U.S. bank）**

##### 2.6.1.3 州特许银行（state-chartered bank）

定义：章程由州银行监管机构批准的商业银行。

- 父类：**商业银行（CommercialBank）**、**美国银行（U.S. bank）**

#### 2.6.2 美国银行控股公司（U.S. bank holding company）

定义：获准在美国开展业务、并依相关法律受联邦储备监管和监督的银行控股公司。

- 父类：**银行控股公司（BankHoldingCompany）**、**境内实体（domestic entity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有被投公司（hasPortfolioCompany）** | — | — |

公理：

- **具有被投公司（hasPortfolioCompany）**至少有一个取值，类型是**美国银行（U.S. bank）**。

#### 2.6.3 其他境内实体（domestic entity other）

定义：通常在美国从事与银行业务相关活动的境内机构。

- 父类：**境内实体（domestic entity）**

#### 2.6.4 境内实体的境内非银行子公司（domestic non-bank subsidiary of a domestic entity）

定义：总部位于美国、其 25% 或以上表决权股份由境内实体拥有或控制的非银行金融服务提供商。

- 父类：**境内实体（domestic entity）**、**境内实体的非银行子公司（non-bank subsidiary of a domestic entity）**

#### 2.6.5 农业信贷体系机构（farm credit system institution）

定义：由农业信贷管理局监督、检查和监管、并依相关法案运营的联邦特许金融机构。

- 父类：**金融机构（FinancialInstitution）**、**境内实体（domestic entity）**

#### 2.6.6 节俭机构（thrift institution）

定义：主要吸收储蓄账户存款并将大部分资金投资于抵押贷款的储蓄协会。

- 父类：**储蓄协会（SavingsAssociation）**、**境内实体（domestic entity）**
- 直接子类：**美国信用合作社（U.S. credit union）**、**合作银行（cooperative bank）**、**储蓄银行（savings bank）**、**储蓄贷款协会（savings loan association）**

##### 2.6.6.1 美国信用合作社（U.S. credit union）

定义：为促进会员节俭、并为勤俭或生产性目的创造信贷来源而组织的合作协会。

- 父类：**信用合作社（CreditUnion）**、**节俭机构（thrift institution）**
- 直接子类：**联邦信用合作社（federal credit union）**、**州信用合作社（state credit union）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由…扮演（is played by）** | — | — |

公理：

- **由…扮演（is played by）**恰好有 1 个**非营利公司（NotForProfitCorporation）**。

###### 2.6.6.1.1 联邦信用合作社（federal credit union）

定义：具有联邦隶属关系的信用合作社。

- 父类：**美国信用合作社（U.S. credit union）**

###### 2.6.6.1.2 州信用合作社（state credit union）

定义：具有州隶属关系的信用合作社。

- 父类：**美国信用合作社（U.S. credit union）**

##### 2.6.6.2 合作银行（cooperative bank）

定义：依照其特许或组建所在州的法律组织和运营的州特许储蓄协会。

- 父类：**节俭机构（thrift institution）**

##### 2.6.6.3 储蓄银行（savings bank）

定义：为吸收储蓄存款并对储蓄存款支付利息而组建的银行机构。

- 父类：**节俭机构（thrift institution）**
- 直接子类：**联邦储蓄银行（federal savings bank）**、**互助储蓄银行（mutual savings bank）**、**州储蓄银行（state savings bank）**

###### 2.6.6.3.1 联邦储蓄银行（federal savings bank）

定义：具有联邦隶属关系的储蓄银行。

- 父类：**储蓄银行（savings bank）**

###### 2.6.6.3.2 互助储蓄银行（mutual savings bank）

定义：主要从个人吸收存款、并将大部分资金投放于抵押贷款的金融机构。

- 父类：**储蓄银行（savings bank）**

###### 2.6.6.3.3 州储蓄银行（state savings bank）

定义：具有州隶属关系的储蓄银行。

- 父类：**储蓄银行（savings bank）**

公理：

- 与**联邦储蓄银行（federal savings bank）**互斥：同一个体不能同时属于两者。

##### 2.6.6.4 储蓄贷款协会（savings loan association）

定义：主要从个人吸收存款、并将资金主要投向住宅抵押贷款的金融机构。

- 父类：**节俭机构（thrift institution）**

### 2.7 埃奇公司（edge corporation）

定义：由联邦储备特许、从事国际银行和金融业务的股份公司，得名于《埃奇法》。

- 父类：**金融机构（FinancialInstitution）**
- 直接子类：**埃奇公司——银行类（edge corporation - banking）**、**埃奇公司——投资类（edge corporation - investment）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由…扮演（is played by）** | — | — |

公理：

- **由…扮演（is played by）**恰好有 1 个**公司（Corporation）**。

#### 2.7.1 埃奇公司——银行类（edge corporation - banking）

定义：章程允许其从事国际银行业务的埃奇公司。

- 父类：**存款性机构（DepositoryInstitution）**、**埃奇公司（edge corporation）**

#### 2.7.2 埃奇公司——投资类（edge corporation - investment）

定义：章程允许其从事国际投资银行业务的埃奇公司。

- 父类：**投资银行（InvestmentBank）**、**埃奇公司（edge corporation）**

### 2.8 埃奇公司——境内分行（edge corporation - domestic branch）

定义：位于美国境内的埃奇公司分行。

- 父类：**分支机构（Branch）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **是……的部分（isPartOf）** | — | — |
| **注册于（isDomiciledIn）** | — | — |

公理：

- **是……的部分（isPartOf）**至少有一个取值，该取值满足：**扮演角色（plays role）**至少有一个取值，类型是**埃奇公司（edge corporation）**。
- **注册于（isDomiciledIn）**的取值固定为 UnitedStatesOfAmerica。

### 2.9 金融控股公司（financial holding company）

定义：依 1999 年《格雷姆-里奇-比利雷法》获准从事广泛银行相关业务的金融实体。

- 父类：**银行控股公司（BankHoldingCompany）**

### 2.10 外国银行（foreign bank）

定义：依外国、美国属地、波多黎各、关岛、美属萨摩亚或维尔京群岛法律组建的金融机构。

- 父类：**银行（Bank）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有母国（has home country）** | 就外国银行而言，指明该外国银行获得特许或注册成立的国家。<br>indicates, with respect to a foreign bank, the country in which the foreign bank is chartered or incorporated | 值域：国家；子属性：具有国家 |
| **具有母国监管机构（has home country supervisor）** | 就外国银行而言，指明其母国负有监管职责的政府实体。<br>indicates, with respect to a foreign bank, the governmental entity or entities in the foreign bank's home country with responsibility for the supervision and regulation of the foreign bank | 值域：监管机构；子属性：受……监管 |

公理：

- **具有母国监管机构（has home country supervisor）**可以有 0 个或多个**监管机构（RegulatoryAgency）**。
- **具有母国（has home country）**至少有一个取值，类型是**国家（Country）**。
- 与**中央银行（CentralBank）**互斥：同一个体不能同时属于两者。
- 与**美国银行（U.S. bank）**互斥：同一个体不能同时属于两者。

### 2.11 外国银行机构（foreign banking organization）

定义：总部设在美国境外、可收购或设立独立银行或银行控股公司的金融服务提供商。

- 父类：**金融服务提供商（FinancialServiceProvider）**
- 直接子类：**作为银行控股公司的外国银行机构（foreign banking organization as a bank holding company）**、**银行控股公司旗下的外国银行机构（foreign banking organization of a bank holding company）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有母国（has home country）** | 就外国银行而言，指明该外国银行获得特许或注册成立的国家。<br>indicates, with respect to a foreign bank, the country in which the foreign bank is chartered or incorporated | 值域：国家；子属性：具有国家 |
| **具有母国监管机构（has home country supervisor）** | 就外国银行而言，指明其母国负有监管职责的政府实体。<br>indicates, with respect to a foreign bank, the governmental entity or entities in the foreign bank's home country with responsibility for the supervision and regulation of the foreign bank | 值域：监管机构；子属性：受……监管 |

公理：

- **具有母国监管机构（has home country supervisor）**可以有 0 个或多个**监管机构（RegulatoryAgency）**。
- **具有母国（has home country）**至少有一个取值，类型是**国家（Country）**。

#### 2.11.1 作为银行控股公司的外国银行机构（foreign banking organization as a bank holding company）

定义：在美国境内属于银行控股公司的外国银行机构。

- 父类：**银行控股公司（BankHoldingCompany）**、**外国银行机构（foreign banking organization）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **由…扮演（is played by）** | — | — |

公理：

- **由…扮演（is played by）**至少有一个取值，该取值满足：**注册于（isDomiciledIn）**的取值固定为 UnitedStatesOfAmerica。

#### 2.11.2 银行控股公司旗下的外国银行机构（foreign banking organization of a bank holding company）

定义：由银行控股公司拥有或控制的外国银行机构。

- 父类：**外国银行机构（foreign banking organization）**

### 2.12 其他境外实体（foreign entity other）

定义：通常在其所在国家从事与银行业务相关活动的境外机构。

- 父类：**金融机构（FinancialInstitution）**

公理：

- 与**境内实体（domestic entity）**互斥：同一个体不能同时属于两者。

### 2.13 工业银行（industrial bank）

定义：通过出售称为「投资股份」的凭证和吸收存款来筹集资金的有限服务金融机构。

- 父类：**银行（Bank）**

### 2.14 中间控股公司（intermediate holding company）

定义：外国银行机构依联邦储备委员会 YY 条例（12 CFR）O 分部分设立或指定的银行控股公司。

- 父类：**银行控股公司（BankHoldingCompany）**

### 2.15 美国存款机构、埃奇公司或信托公司旗下的国际银行（international bank of US depositary, edge, trust company）

定义：由美国存款性机构、埃奇法公司或信托公司拥有或控制的银行。

- 父类：**银行（Bank）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **是……的部分（isPartOf）** | — | — |

公理：

- **是……的部分（isPartOf）**至少有一个取值，该取值满足：**扮演角色（plays role）**至少有一个取值，该取值满足：该属性存在取值约束。

### 2.16 非存款性信托公司（non-depository trust company）

定义：接受并执行信托但不发行货币的信托公司；可以是联邦储备成员或非成员。

- 父类：**非存款性机构（NonDepositoryInstitution）**、**信托公司（TrustCompany）**

### 2.17 外国银行办事机构（office of a foreign bank）

定义：外国银行在美国的任何分行、代理处、代表处或商业贷款公司子公司等设施。

- 父类：**设施（Facility）**
- 直接子类：**外国银行的境内分行（domestic branch of a foreign bank）**、**外国银行代表处（representative office of a foreign bank）**

#### 2.17.2 外国银行代表处（representative office of a foreign bank）

定义：外国银行设于美国任何州、且不属于联邦分行、联邦代理处、州分行、州代理处或商业贷款公司的办事机构。

- 父类：**外国银行办事机构（office of a foreign bank）**
- 直接子类：**外国银行区域行政办事处（regional administrative office of a foreign bank）**

公理：

- 与**外国银行的境内分行（domestic branch of a foreign bank）**互斥：同一个体不能同时属于两者。

##### 2.17.2.1 外国银行区域行政办事处（regional administrative office of a foreign bank）

定义：由在美国运营两个或以上分行、代理处、商业贷款公司或银行的外国银行设立的代表处，承担区域管理职能。

- 父类：**外国银行代表处（representative office of a foreign bank）**

### 2.18 储蓄贷款控股公司（savings loan holding company）

定义：直接或间接控制储蓄协会或相关控股公司的公司，明确排除同时属于银行控股公司的公司。

- 父类：**控股公司（HoldingCompany）**、**金融服务提供商（FinancialServiceProvider）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **具有被投公司（hasPortfolioCompany）** | — | — |

公理：

- **具有被投公司（hasPortfolioCompany）**至少有一个取值，该取值满足：该属性存在取值约束。
- 与**银行控股公司（BankHoldingCompany）**互斥：同一个体不能同时属于两者。

### 2.19 境内实体的子公司（subsidiary of a domestic entity）

定义：其 25% 或以上表决权股份由总部位于美国的实体拥有或控制、或其实质多数股权受其控制的实体。

- 父类：**子公司（Subsidiary）**
- 直接子类：**境内实体的非银行子公司（non-bank subsidiary of a domestic entity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **是……的子公司（isSubsidiaryOf）** | — | — |

公理：

- **是……的子公司（isSubsidiaryOf）**至少有一个取值，该取值满足：**由…扮演（is played by）**至少有一个取值，类型是**境内实体（domestic entity）**。

#### 2.19.1 境内实体的非银行子公司（non-bank subsidiary of a domestic entity）

定义：其 25% 或以上表决权股份由总部位于美国的实体拥有或控制的非银行实体。

- 父类：**境内实体的子公司（subsidiary of a domestic entity）**
- 直接子类：**境内实体的境内非银行子公司（domestic non-bank subsidiary of a domestic entity）**、**境内实体的境外非银行子公司（international non-bank subsidiary of a domestic entity）**

属性：

| 属性 | 定义 | 说明 |
|---|---|---|
| **是……的子公司（isSubsidiaryOf）** | — | — |

公理：

- **是……的子公司（isSubsidiaryOf）**至少有一个取值，该取值满足：**由…扮演（is played by）**至少有一个取值，类型是**金融机构（FinancialInstitution）**。
- 与**银行（Bank）**互斥：同一个体不能同时属于两者。

##### 2.19.1.2 境内实体的境外非银行子公司（international non-bank subsidiary of a domestic entity）

定义：总部位于美国境外、其 25% 或以上表决权股份由境内实体拥有或控制的非银行金融服务提供商。

- 父类：**境内实体的非银行子公司（non-bank subsidiary of a domestic entity）**

公理：

- 与**境内实体的境内非银行子公司（domestic non-bank subsidiary of a domestic entity）**互斥：同一个体不能同时属于两者。

## 3. 依赖（owl:imports，17 个）

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

## 4. 文件

- 官方 RDF/XML：`USFinancialServicesEntities.rdf`
- 中文 Turtle：`USFinancialServicesEntities.ttl`
- 结构图：`USFinancialServicesEntities-structure.png` / `USFinancialServicesEntities-structure.svg`