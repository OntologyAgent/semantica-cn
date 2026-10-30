# 正式组织本体（Formal Organizations Ontology）结构与公理说明

本文档对应 `FormalOrganizations.rdf` / `FormalOrganizations.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `FormalOrganizations-structure.png`（`FormalOrganizations-structure.svg` 为可缩放版本）。

![正式组织本体（Formal Organizations Ontology）本体结构图](FormalOrganizations-structure.png)

## 1. 本体概述

定义正式组织（formal organization）、组织成员与组织内部角色：有明确宗旨、结构和成员规则的团体。

**在体系中的位置**：FND 组织模块的核心，是 BE 公司、政府机构、FBC 金融服务机构等一切组织概念的上游。

**上下游关系**：上游依赖参与方与关系本体；下游被 BE、FBC 各组织类本体大量继承。

**与相近概念的差别**：正式组织≠法人——正式组织是社会学概念（有结构的团体），法人是法律概念（有独立人格）；一个非法人部门也可以是正式组织；组织≠参与方——组织只有进入业务关系才是参与方。

## 2. 类（Class）

| 类（Class） | 定义（Definition） |
|---|---|
| 雇员（employee） | 依任何明示或默示、口头或书面的雇佣合同为他人服务的人，雇主有权控制和指导其工作。 |
| 雇主（employer） | 以报酬（包括工资或薪金及潜在的其他福利）换取一人或多人工作的参与方。 |
| 雇佣关系（employment） | 表示被雇用状态的情形，即雇主与雇员之间在某段时期内存在的关系。 |
| 团体（group） | 被视为一个整体的代理（人、组织、软件代理等）集合。 |

### 2.1 继承关系（Inheritance）

- 雇员（employee） ⊑ 组织成员
- 雇主（employer） ⊑ 含成员组织
- 雇佣关系（employment） ⊑ 成员关系
- 团体（group） ⊑ 集合

## 3. 对象属性（Object Property）

| 属性（Property） | 中文（English） | 定义（Definition） | 说明 |
|---|---|---|---|
| fibo-fnd-org-fm:employs | 雇用（employs） | 标识被该法律主体雇用的人。 | 定义域（domain）：法律主体；值域（range）：个人；子属性（subPropertyOf）：扮演直接影响…的主动角色（plays active role that directly affects） |
| fibo-fnd-org-fm:hasEmployedParty | 具有被雇方（has employed party） | 标识雇佣情形中的雇员。 | 定义域（domain）：雇佣关系（employment）；值域（range）：雇员（employee）；逆属性（inverseOf）：受雇于情境（is employed in）；子属性（subPropertyOf）：具有组织成员 |
| fibo-fnd-org-fm:hasEmployee | 具有雇员（has employee） | 标识被雇主雇用的雇员。 | 定义域（domain）：雇主（employer）；值域（range）：雇员（employee）；逆属性（inverseOf）：是……的雇员（is employee of）；子属性（subPropertyOf）：对…采取行动（acts on） |
| fibo-fnd-org-fm:hasEmployingParty | 具有雇佣方（has employing party） | 标识雇佣情形中的雇主。 | 定义域（domain）：雇佣关系（employment）；值域（range）：雇主（employer）；逆属性（inverseOf）：是雇佣方（is employing party）；子属性（subPropertyOf）：具有成员关系 |
| fibo-fnd-org-fm:isEmployedBy | 受雇于（is employed by） | 标识雇用某人的参与方（法律主体或正式组织）。 | 定义域（domain）：个人；值域（range）：法律主体；子属性（subPropertyOf）：直接经历（experiences directly） |
| fibo-fnd-org-fm:isEmployedIn | 受雇于情境（is employed in） | 标识某人受雇所在的雇佣情境。 | 定义域（domain）：雇员（employee）；值域（range）：雇佣关系（employment）；子属性（subPropertyOf）：是组织成员 |
| fibo-fnd-org-fm:isEmployeeOf | 是……的雇员（is employee of） | 标识雇员为之工作的正式组织。 | 定义域（domain）：雇员（employee）；值域（range）：雇主（employer）；子属性（subPropertyOf）：受…影响（is affected by） |
| fibo-fnd-org-fm:isEmployingParty | 是雇佣方（is employing party） | 将处于雇主角色的参与方关联到雇佣情境。 | 定义域（domain）：雇主（employer）；值域（range）：雇佣关系（employment）；子属性（subPropertyOf）：在……中为成员方 |

## 5. 公理约定（Axioms）

- 雇员（employee）：受雇于情境（is employed in） some 雇佣关系（employment）
- 雇员（employee）：是……的雇员（is employee of） some 雇主（employer）
- 雇员（employee）：由…扮演（is played by） some 个人
- 雇主（employer）：具有雇员（has employee） some 雇员（employee）
- 雇主（employer）：是雇佣方（is employing party） some 雇佣关系（employment）
- 雇主（employer）：由…扮演（is played by） some 法律主体
- 雇佣关系（employment）：具有被雇方（has employed party） some 雇员（employee）
- 雇佣关系（employment）：具有雇佣方（has employing party） some 雇主（employer）
- 团体（group）：具有成员 only 智能体（agent）

## 6. 依赖（owl:imports，10 个）

本本体通过 `owl:imports` 引入以下本体，各项的中文名称与简介如下：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `FND/AgentsAndPeople/People.rdf` | 人员本体（People Ontology） | 定义自然人（person）的核心属性：姓名、出生日期、国籍、身份标识与联系方式，为雇员、客户、签署人等角色提供「人」的基础模型。 |
| `FND/GoalsAndObjectives/Objectives.rdf` | 目标本体（Objectives Ontology） | 定义目标（objective）及其与组织、计划的关系，用于表达机构的经营目标与投资目标。 |
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |
| `https://www.omg.org/spec/Commons/Collections/` | OMG 通用集合本体（OMG Commons Collections） | Commons 库中的集合本体，定义集合、成员等通用概念。 |
| `https://www.omg.org/spec/Commons/Designators/` | OMG 通用指称符本体（OMG Commons Designators） | Commons 库中的指称符本体，定义名称、标识符等「指代某物的符号」的通用概念。 |
| `https://www.omg.org/spec/Commons/Organizations/` | OMG 通用组织本体（OMG Commons Organizations） | Commons 库中的组织本体，定义组织、组织成员与组织结构的通用概念。 |
| `https://www.omg.org/spec/Commons/PartiesAndSituations/` | OMG 通用参与方与情境本体（OMG Commons Parties and Situations） | Commons 库中的参与方本体，定义独立主体、参与方及其角色扮演的通用概念，是 FIBO 参与方模型的上游。 |
| `https://www.omg.org/spec/Commons/RolesAndCompositions/` | OMG 通用角色与构成本体（OMG Commons Roles and Compositions） | Commons 库中的角色本体，定义角色及整体—部分构成关系的通用概念。 |
| `https://www.omg.org/spec/Commons/TextDatatype/` | OMG 通用文本数据类型（OMG Commons Text Datatype） | Commons 库中的文本数据类型定义，提供带语言标记的文本等基础数据类型。 |

## 7. 文件

- 官方 RDF/XML：`FormalOrganizations.rdf`
- 中文 Turtle：`FormalOrganizations.ttl`
- 结构图：`FormalOrganizations-structure.png` / `FormalOrganizations-structure.svg`