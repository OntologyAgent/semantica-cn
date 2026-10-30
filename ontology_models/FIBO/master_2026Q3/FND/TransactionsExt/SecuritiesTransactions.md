# 证券交易本体（Securities Transactions Ontology）结构与公理说明

本文档对应 `SecuritiesTransactions.rdf` / `SecuritiesTransactions.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `SecuritiesTransactions-structure.png`（`SecuritiesTransactions-structure.svg` 为可缩放版本）。

![证券交易本体（Securities Transactions Ontology）本体结构图](SecuritiesTransactions-structure.png)

## 1. 本体概述

定义证券买卖交易：订单、成交（execution）、结算指令及其参与方。

**在体系中的位置**：FND 交易扩展模块中专为证券领域特化的本体。

**上下游关系**：上游继承市场交易本体并引用 SEC 证券、FBC 结算概念；下游服务交易记录与清算建模。

**与相近概念的差别**：交易≠结算——交易是达成买卖，结算是履约交割（见 FBC 结算本体）；与市场交易的差别——增加了证券特有的订单与成交结构。

## 2. 类（Class）

| 类（Class） | 定义（Definition） |
|---|---|
| 金融一级市场交易（financial primary market transaction） | 在一级市场上进行的金融交易。 |
| 金融证券二级市场交易（financial securities secondary market transaction） | 以某种可流通证券换取某种对价的交易。 |
| 证券交易合同（securities transaction contract） | 治理二级市场证券交易的合同（书面或默示）。 |
| 证券交易对手方（securities transaction counterparty） | 证券交易中的对手方。 |
| 证券交易主当事方（securities transaction principal） | 证券交易中的主当事方。 |
| 结算过程（settlement process） | 完成交易交收的过程。 |
| 预发行交易（when issued transaction） | 在证券正式交易之前进行的证券买卖。 |

### 2.1 继承关系（Inheritance）

- 金融一级市场交易（financial primary market transaction） ⊑ 市场交易
- 金融一级市场交易（financial primary market transaction） ⊑ 合同性交易
- 金融证券二级市场交易（financial securities secondary market transaction） ⊑ 市场交易
- 金融证券二级市场交易（financial securities secondary market transaction） ⊑ 合同性交易
- 证券交易合同（securities transaction contract） ⊑ 经济合同
- 证券交易对手方（securities transaction counterparty） ⊑ 交易对手方
- 证券交易主当事方（securities transaction principal） ⊑ 交易委托方
- 预发行交易（when issued transaction） ⊑ 金融证券二级市场交易（financial securities secondary market transaction）

## 3. 对象属性（Object Property）

| 属性（Property） | 中文（English） | 定义（Definition） | 说明 |
|---|---|---|---|
| fibo-fnd-txn-sec:embodies | 体现（embodies） | 是……的表达，赋予……以具体形式。 | 定义域（domain）：金融证券二级市场交易（financial securities secondary market transaction）；值域（range）：证券交易合同（securities transaction contract）；子属性（subPropertyOf）：交易体现经济协议 |
| fibo-fnd-txn-sec:follows | 遵循（follows） | 按……进行。 | 定义域（domain）：金融一级市场交易（financial primary market transaction）；值域（range）：结算过程（settlement process）；子属性（subPropertyOf）：交易事件遵循业务流程 |
| fibo-fnd-txn-sec:governs | 管辖（governs） | 对……拥有并行使权力。 | 定义域（domain）：证券交易合同（securities transaction contract）；值域（range）：金融证券二级市场交易（financial securities secondary market transaction）；逆属性（inverseOf）：体现（embodies）；子属性（subPropertyOf）：管辖 |

## 4. 数据属性（Datatype Property）

| 属性（Property） | 中文（English） | 定义（Definition） |
|---|---|---|
| fibo-fnd-txn-sec:offsetForWIIssueDate | 预发行发行日偏移（offset for w i issue date） | 用于由给定预发行（WI）发行日计算实际结算日；若发行日未知，它确定自发行日起算的天数。 |

## 5. 公理约定（Axioms）

- 金融一级市场交易（financial primary market transaction）：遵循（follows） some 结算过程（settlement process）
- 金融证券二级市场交易（financial securities secondary market transaction）：具有交易对手 some 证券交易对手方（securities transaction counterparty）
- 金融证券二级市场交易（financial securities secondary market transaction）：具有主当事方 some 证券交易主当事方（securities transaction principal）
- 金融证券二级市场交易（financial securities secondary market transaction）：对价 some（restriction）
- 金融证券二级市场交易（financial securities secondary market transaction）：标的 some 证券
- 金融证券二级市场交易（financial securities secondary market transaction）：体现（embodies） some 证券交易合同（securities transaction contract）
- 证券交易合同（securities transaction contract）：管辖（governs） some 金融证券二级市场交易（financial securities secondary market transaction）

## 6. 依赖（owl:imports，7 个）

本本体通过 `owl:imports` 引入以下本体，各项的中文名称与简介如下：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `FND/Accounting/CurrencyAmount.rdf` | 货币金额本体（Currency Amount Ontology） | 定义「金额＋币种」的货币金额（currency amount）表示，是 FIBO 中表达价格、债务金额、付款额等一切带币种数值的基础构件。 |
| `FND/Agreements/Contracts.rdf` | 合同本体（Contracts Ontology） | 在协议之上定义具有法律约束力的合同（contract）：合同当事方、合同条款、义务与权利，是金融工具与交易合同建模的基石。 |
| `FND/TransactionsExt/MarketTransactions.rdf` | 市场交易本体（Market Transactions Ontology） | 定义市场上发生的交易（market transaction）：买卖双方、价格与数量。 |
| `FND/TransactionsExt/REATransactions.rdf` | REA 交易本体（REA Transactions Ontology） | 基于资源—事件—代理（REA）会计模型定义交易的经济资源交换结构。 |
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |
| `https://www.omg.org/spec/Commons/RegulatoryAgencies/` | OMG 通用监管机构本体（OMG Commons Regulatory Agencies） | Commons 库中的监管机构本体，定义监管机构及其监管职权的通用概念。 |

## 7. 文件

- 官方 RDF/XML：`SecuritiesTransactions.rdf`
- 中文 Turtle：`SecuritiesTransactions.ttl`
- 结构图：`SecuritiesTransactions-structure.png` / `SecuritiesTransactions-structure.svg`