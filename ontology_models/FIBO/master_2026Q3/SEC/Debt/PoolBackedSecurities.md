# 池支持证券本体（Pool-backed Securities Ontology）结构与公理说明

本文档对应 `PoolBackedSecurities.rdf` / `PoolBackedSecurities.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `PoolBackedSecurities-structure.png`（`PoolBackedSecurities-structure.svg` 为可缩放版本）。

![池支持证券本体（Pool-backed Securities Ontology）本体结构图](PoolBackedSecurities-structure.png)

## 1. 本体概述

定义以资产池为支持的证券的通用结构：资产池、分层（tranche）、过手（pass-through）安排。

**在体系中的位置**：SEC 债务模块中资产证券化的框架本体，ABS、MBS、CDO 的共同上游。

**上下游关系**：上游继承债务工具并依赖证券池本体；下游被资产支持证券、抵押贷款支持证券、担保债务凭证特化。

**与相近概念的差别**：池支持证券≠普通债券——偿付来源是资产池现金流而非发行人信用；分层机制使不同档（tranche）承担不同风险，这是普通债券没有的结构。

## 2. 类（Class）

| 类（Class） | 定义（Definition） |
|---|---|
| 绝对提前偿付率（absolute prepayment rate） | 以原始资产池余额百分比表示的月度贷款提前偿付率。 |
| 资产支持证券（asset-backed security） | 由房地产贷款或抵押贷款以外应收款支持的债务工具。 |
| 附着点（attachment point） | 分档的下边界，以发行时或某一时点抵押品总池价值的百分比表示。 |
| 债务池统计度量（debt pool statistical measure） | 对一个或多个债务工具可能随时间变化之行为的某方面进行的限定性度量。 |
| 违约率（default rate） | 对池中债务工具持有人违约比率的限定性度量。 |
| 脱离点（detachment point） | 分档的上边界，以发行时或某一时点抵押品总池价值的百分比表示。 |
| 资产池支持证券（pool-backed security） | 现金流来源于标的抵押贷款池或其他应收款池的债务工具。 |
| 提前偿付速度（prepayment speed） | 对债务或部分债务提前清偿比率的估计。 |
| 保本票据（principal protected note） | 通过多种方式和不对称支付结构为投资者提供选定标的资产风险敞口的结构化金融产品。 |
| 单月清偿率（single monthly mortality） | 对抵押支持证券（MBS）池中每月将提前清偿之抵押贷款百分比的估计。 |
| 结构化金融工具（structured finance instrument） | 通过特定结构将资产池风险与发起机构风险相隔离的资产池支持证券。 |
| 无本金保护结构化金融产品（structured finance without principal protection） | 与标的资产挂钩、提供稳定收入流的短期票据类结构化金融产品。 |
| 分档（tranche） | 证券池（通常为债务工具）的一个部分。 |
| 加权平均票息（weighted average coupon） | 抵押支持证券（MBS）标的抵押贷款池按余额加权的平均总利率。 |
| 加权平均期限（weighted average life） | 本金偿还时间的加权平均值，按收取全部未来现金流的时间加权计算。 |
| 加权平均贷款账龄（weighted average loan age） | 衡量抵押转手证券或集合证券中各笔贷款账龄的金额加权平均值。 |
| 加权平均到期期限（weighted average maturity） | 抵押支持证券（MBS）中抵押贷款到期时间的加权平均值。 |
| 加权平均剩余期限（weighted average remaining term） | 资产支持证券（ABS）或抵押支持证券（MBS）组合的加权平均到期时间。 |

### 2.1 继承关系（Inheritance）

- 绝对提前偿付率（absolute prepayment rate） ⊑ 债务池统计度量（debt pool statistical measure）
- 资产支持证券（asset-backed security） ⊑ 资产池支持证券（pool-backed security）
- 附着点（attachment point） ⊑ 百分比货币数量
- 债务池统计度量（debt pool statistical measure） ⊑ 限定度量
- 违约率（default rate） ⊑ 债务池统计度量（debt pool statistical measure）
- 违约率（default rate） ⊑ 比率
- 脱离点（detachment point） ⊑ 百分比货币数量
- 资产池支持证券（pool-backed security） ⊑ 可交易债务工具
- 提前偿付速度（prepayment speed） ⊑ 债务池统计度量（debt pool statistical measure）
- 保本票据（principal protected note） ⊑ 结构化金融工具（structured finance instrument）
- 单月清偿率（single monthly mortality） ⊑ 债务池统计度量（debt pool statistical measure）
- 单月清偿率（single monthly mortality） ⊑ 百分比
- 结构化金融工具（structured finance instrument） ⊑ 资产池支持证券（pool-backed security）
- 无本金保护结构化金融产品（structured finance without principal protection） ⊑ 结构化金融工具（structured finance instrument）
- 分档（tranche） ⊑ 结构化金融工具（structured finance instrument）
- 加权平均票息（weighted average coupon） ⊑ 算术平均值
- 加权平均票息（weighted average coupon） ⊑ 债务池统计度量（debt pool statistical measure）
- 加权平均期限（weighted average life） ⊑ 算术平均值
- 加权平均期限（weighted average life） ⊑ 债务池统计度量（debt pool statistical measure）
- 加权平均贷款账龄（weighted average loan age） ⊑ 算术平均值
- 加权平均贷款账龄（weighted average loan age） ⊑ 债务池统计度量（debt pool statistical measure）
- 加权平均到期期限（weighted average maturity） ⊑ 算术平均值
- 加权平均到期期限（weighted average maturity） ⊑ 债务池统计度量（debt pool statistical measure）
- 加权平均剩余期限（weighted average remaining term） ⊑ 算术平均值
- 加权平均剩余期限（weighted average remaining term） ⊑ 债务池统计度量（debt pool statistical measure）

## 3. 对象属性（Object Property）

| 属性（Property） | 中文（English） | 定义（Definition） | 说明 |
|---|---|---|---|
| fibo-sec-dbt-pbs:hasAttachmentPoint | 具有附着点（has attachment point） | 指明标的抵押品总价值的下限（以发行时或某一时点计），达到该点时该分档开始承担损失。 | 值域（range）：附着点（attachment point）；子属性（subPropertyOf）：具有量值 |
| fibo-sec-dbt-pbs:hasDetachmentPoint | 具有脱离点（has detachment point） | 指明标的抵押品总价值的上限（以发行时或某一时点计），达到该点时该分档不再承担损失。 | 值域（range）：脱离点（detachment point）；子属性（subPropertyOf）：具有量值 |
| fibo-sec-dbt-pbs:hasEstimatedTotalCollateralValueAtIssuance | 是……的估计价值（is estimated value of） | 将评估价值关联到评估日所关注的资产。 | 值域（range）：截至日抵押品价值；子属性（subPropertyOf）：是……的估计价值 |

## 4. 数据属性（Datatype Property）

| 属性（Property） | 中文（English） | 定义（Definition） |
|---|---|---|
| fibo-sec-dbt-pbs:isPassThrough | 是否过手（is pass through） | 表明标的资产池的现金流是否通过赎回付款方式过手给投资者。 |

## 5. 公理约定（Axioms）

- 附着点（attachment point）：是……的估计价值 截至日抵押品价值 ≥0
- 债务池统计度量（debt pool statistical measure）：具有适用期间 日期区间 ≥0
- 债务池统计度量（debt pool statistical measure）：适用于 some 债务池
- 脱离点（detachment point）：是……的估计价值 截至日抵押品价值 ≥0
- 资产池支持证券（pool-backed security）：是……的估计价值（is estimated value of） 截至日抵押品价值 ≥0
- 资产池支持证券（pool-backed security）：以……为特征 债务池统计度量（debt pool statistical measure） ≥0
- 资产池支持证券（pool-backed security）：restriction
- 资产池支持证券（pool-backed security）：基于 some 工具池
- 结构化金融工具（structured finance instrument）：由……发行 some（由…扮演（is played by） some 特殊目的载体）
- 无本金保护结构化金融产品（structured finance without principal protection） 与 保本票据（principal protected note） 互斥（disjointWith）
- 分档（tranche）：是……的估计价值（is estimated value of） 截至日抵押品价值 ≥0
- 分档（tranche）：具有附着点（has attachment point） 附着点（attachment point） ≥0
- 分档（tranche）：具有脱离点（has detachment point） 脱离点（detachment point） ≥0
- 分档（tranche）：包含 some（是……的部分 some 工具池）
- 加权平均期限（weighted average life）：引用 提前偿付速度（prepayment speed） ≥0

## 6. 依赖（owl:imports，17 个）

本本体通过 `owl:imports` 引入以下本体，各项的中文名称与简介如下：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `BE/LegalEntities/LegalPersons.rdf` | 法律主体本体（Legal Persons Ontology） | 定义法律主体（legal person）与法定实体（legal entity）的核心概念：能持有权利义务、可起诉与被诉的主体。 |
| `FBC/DebtAndEquities/Debt.rdf` | 债务本体（Debt Ontology） | 定义债务（debt）与债权债务关系的核心概念：借款人、贷款人、本金与利息义务。 |
| `FND/Accounting/CurrencyAmount.rdf` | 货币金额本体（Currency Amount Ontology） | 定义「金额＋币种」的货币金额（currency amount）表示，是 FIBO 中表达价格、债务金额、付款额等一切带币种数值的基础构件。 |
| `FND/Arrangements/Assessments.rdf` | 评估本体（Assessments Ontology） | 定义评估活动、评估结果与评估方的通用结构，为信用评级、风险打分等判断性活动提供基础模型。 |
| `FND/Relations/Relations.rdf` | 关系本体（Relations Ontology） | FIBO 最底层的基础本体，定义参考（reference）、分类（classify）等通用关系与抽象概念，全库普遍依赖。 |
| `FND/Utilities/Analytics.rdf` | 分析本体（Analytics Ontology） | 定义分析工具、度量与比率的通用概念，支撑指标与模型的表达。 |
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `SEC/Debt/DebtInstruments.rdf` | 债务工具本体（Debt Instruments Ontology） | 定义债务工具（debt instrument）的通用概念：可交易的债权凭证，是债券、票据等的上位模型。 |
| `SEC/Securities/Pools.rdf` | 证券池本体（Securities Pools Ontology） | 定义证券池（pool）：归集起来作为证券化基础的一组资产。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |
| `https://www.omg.org/spec/Commons/Classifiers/` | OMG 通用分类器本体（OMG Commons Classifiers） | OMG 通用本体库（Commons）中的分类器本体，定义分类方案、类别与归类关系的通用概念，FIBO 的分类建模建立在其上。 |
| `https://www.omg.org/spec/Commons/Collections/` | OMG 通用集合本体（OMG Commons Collections） | Commons 库中的集合本体，定义集合、成员等通用概念。 |
| `https://www.omg.org/spec/Commons/ContextualDesignators/` | OMG 通用语境指称本体（OMG Commons Contextual Designators） | Commons 库中的语境指称本体，定义「在某个语境下指代某物的名称/符号」，是地址、账户号码等语境相关标识的基础。 |
| `https://www.omg.org/spec/Commons/DatesAndTimes/` | OMG 通用日期与时间本体（OMG Commons Dates and Times） | Commons 库中的日期时间本体，定义日期、期间、时间点等通用时间概念。 |
| `https://www.omg.org/spec/Commons/Documents/` | OMG 通用文档本体（OMG Commons Documents） | Commons 库中的文档本体，定义文档及其组成部分的通用概念。 |
| `https://www.omg.org/spec/Commons/QuantitiesAndUnits/` | OMG 通用量与单位本体（OMG Commons Quantities and Units） | Commons 库中的量与单位本体，定义数量、度量单位、量纲的通用概念，支撑金额、比率等数值表达。 |
| `https://www.omg.org/spec/Commons/RolesAndCompositions/` | OMG 通用角色与构成本体（OMG Commons Roles and Compositions） | Commons 库中的角色本体，定义角色及整体—部分构成关系的通用概念。 |

## 7. 文件

- 官方 RDF/XML：`PoolBackedSecurities.rdf`
- 中文 Turtle：`PoolBackedSecurities.ttl`
- 结构图：`PoolBackedSecurities-structure.png` / `PoolBackedSecurities-structure.svg`