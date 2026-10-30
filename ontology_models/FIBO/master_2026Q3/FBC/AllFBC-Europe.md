# FBC 域欧洲扩展入口（All FBC, European Extension）聚合说明

本文档对应 `AllFBC-Europe.rdf` / `AllFBC-Europe.ttl`。

![FBC 域欧洲扩展入口（All FBC, European Extension）聚合结构图](AllFBC-Europe-structure.png)

## 1. 本文件是什么

聚合 FBC 域中欧洲法域的扩展本体（欧盟金融服务实体、欧盟监管机构、欧洲市场参考个体等），与 AllFBC 配合用于欧洲场景。

从机制上说，这是一个聚合入口（load-all）文件：它本身不定义任何新的类或属性，只通过 `owl:imports` 把一组本体打包在一起。应用只要导入这一个文件，推理机就会把它列出的所有本体一次性加载进来，免去逐个声明的麻烦。因此它的价值不在「内容」，而在「组合」——组合方式本身就表达了发布方的意图（例如按域打包、按区域扩展打包、按是否含参考数据打包）。

## 2. 聚合的本地本体（5 个）

以下本体均可在本目录结构中找到同名 `.rdf` 文件及配套中文文档：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `BE/AllBE-Europe.rdf` | BE 域欧洲扩展入口（All BE, European Extension） | 聚合 BE 域中欧洲法域的扩展本体（欧盟及欧洲各区域政府实体与法域个体），与 AllBE 配合用于欧洲场景。 |
| `FBC/AllFBC-ReferenceMarkets.rdf` | FBC 域参考市场入口（All FBC, Reference Markets） | 聚合全球主要金融市场的参考个体（市场、商业中心及其个体数据），用于需要市场主数据的场景。 |
| `FBC/FunctionalEntities/EuropeanEntities/EUFinancialServicesEntities.rdf` | 欧盟金融服务实体本体（EU Financial Services Entities Ontology） | 定义欧盟法域下的金融服务机构类型与个体。 |
| `FBC/FunctionalEntities/EuropeanEntities/EURegulatoryAgencies.rdf` | 欧盟监管机构本体（EU Regulatory Agencies Ontology） | 收录欧盟层面的金融监管机构个体（如欧洲央行、欧洲证券和市场管理局 ESMA）。 |
| `FBC/FunctionalEntities/EuropeanEntities/EuropeanFinancialServicesEntitiesIndividuals.rdf` | 欧洲金融服务实体个体本体（European Financial Services Entities Individuals Ontology） | 收录欧洲各国金融服务机构与市场的参考个体。 |

## 3. 文件

- 官方 RDF/XML：`AllFBC-Europe.rdf`
- 中文 Turtle：`AllFBC-Europe.ttl`
- 结构图：`AllFBC-Europe-structure.png` / `AllFBC-Europe-structure.svg`