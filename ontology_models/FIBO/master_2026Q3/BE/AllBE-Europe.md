# BE 域欧洲扩展入口（All BE, European Extension）聚合说明

本文档对应 `AllBE-Europe.rdf` / `AllBE-Europe.ttl`。

![BE 域欧洲扩展入口（All BE, European Extension）聚合结构图](AllBE-Europe-structure.png)

## 1. 本文件是什么

聚合 BE 域中欧洲法域的扩展本体（欧盟及欧洲各区域政府实体与法域个体），与 AllBE 配合用于欧洲场景。

从机制上说，这是一个聚合入口（load-all）文件：它本身不定义任何新的类或属性，只通过 `owl:imports` 把一组本体打包在一起。应用只要导入这一个文件，推理机就会把它列出的所有本体一次性加载进来，免去逐个声明的麻烦。因此它的价值不在「内容」，而在「组合」——组合方式本身就表达了发布方的意图（例如按域打包、按区域扩展打包、按是否含参考数据打包）。

## 2. 聚合的本地本体（7 个）

以下本体均可在本目录结构中找到同名 `.rdf` 文件及配套中文文档：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `BE/AllBE.rdf` | BE 域总入口（All Business Entities Domain） | 聚合商业实体（Business Entities，BE）域的全部生产本体：法律实体、公司、合伙、信托、所有权与控制权、政府实体等，一次导入即获得 BE 域完整模型。 |
| `BE/GovernmentEntities/EuropeanJurisdiction/EUGovernmentEntitiesAndJurisdictions.rdf` | 欧盟政府实体与法域本体（EU Government Entities and Jurisdictions Ontology） | 收录欧盟层面的政体、机构与法域个体（欧盟本身及其超国家机构）。 |
| `BE/GovernmentEntities/EuropeanJurisdiction/EasternEuropeGovernmentEntitiesAndJurisdictions.rdf` | 东欧政府实体与法域本体（Eastern Europe Government Entities and Jurisdictions Ontology） | 收录东欧各国（波兰、捷克、匈牙利等）的政体、政府与法域个体。 |
| `BE/GovernmentEntities/EuropeanJurisdiction/NorthernEuropeGovernmentEntitiesAndJurisdictions.rdf` | 北欧政府实体与法域本体（Northern Europe Government Entities and Jurisdictions Ontology） | 收录北欧各国（瑞典、挪威、丹麦等）的政体、政府与法域个体。 |
| `BE/GovernmentEntities/EuropeanJurisdiction/SouthernEuropeGovernmentEntitiesAndJurisdictions.rdf` | 南欧政府实体与法域本体（Southern Europe Government Entities and Jurisdictions Ontology） | 收录南欧各国（意大利、西班牙、希腊等）的政体、政府与法域个体。 |
| `BE/GovernmentEntities/EuropeanJurisdiction/UKGovernmentEntitiesAndJurisdictions.rdf` | 英国政府实体与法域本体（UK Government Entities and Jurisdictions Ontology） | 收录大不列颠及北爱尔兰联合王国的政体、政府与法域个体（英格兰、苏格兰、威尔士、北爱尔兰）。 |
| `BE/GovernmentEntities/EuropeanJurisdiction/WesternEuropeGovernmentEntitiesAndJurisdictions.rdf` | 西欧政府实体与法域本体（Western Europe Government Entities and Jurisdictions Ontology） | 收录西欧各国（法国、德国、荷兰等）的政体、政府与法域个体。 |

## 3. 文件

- 官方 RDF/XML：`AllBE-Europe.rdf`
- 中文 Turtle：`AllBE-Europe.ttl`
- 结构图：`AllBE-Europe-structure.png` / `AllBE-Europe-structure.svg`