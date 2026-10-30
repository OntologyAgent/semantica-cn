# FBC 域欧洲与北美扩展合并入口（All FBC, European and North American Extension）聚合说明

本文档对应 `AllFBC-EuropeAndNorthAmerica.rdf` / `AllFBC-EuropeAndNorthAmerica.ttl`。

![FBC 域欧洲与北美扩展合并入口（All FBC, European and North American Extension）聚合结构图](AllFBC-EuropeAndNorthAmerica-structure.png)

## 1. 本文件是什么

同时引入 FBC 域的欧洲扩展与北美扩展，便于业务横跨两大法域的应用一次加载全部区域性内容。

从机制上说，这是一个聚合入口（load-all）文件：它本身不定义任何新的类或属性，只通过 `owl:imports` 把一组本体打包在一起。应用只要导入这一个文件，推理机就会把它列出的所有本体一次性加载进来，免去逐个声明的麻烦。因此它的价值不在「内容」，而在「组合」——组合方式本身就表达了发布方的意图（例如按域打包、按区域扩展打包、按是否含参考数据打包）。

## 2. 聚合的本地本体（2 个）

以下本体均可在本目录结构中找到同名 `.rdf` 文件及配套中文文档：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `FBC/AllFBC-Europe.rdf` | FBC 域欧洲扩展入口（All FBC, European Extension） | 聚合 FBC 域中欧洲法域的扩展本体（欧盟金融服务实体、欧盟监管机构、欧洲市场参考个体等），与 AllFBC 配合用于欧洲场景。 |
| `FBC/AllFBC-NorthAmerica.rdf` | FBC 域北美扩展入口（All FBC, North American Extension） | 聚合 FBC 域中北美法域的扩展本体（美国与加拿大的金融服务实体、监管机构及受控词汇等）。 |

## 3. 文件

- 官方 RDF/XML：`AllFBC-EuropeAndNorthAmerica.rdf`
- 中文 Turtle：`AllFBC-EuropeAndNorthAmerica.ttl`
- 结构图：`AllFBC-EuropeAndNorthAmerica-structure.png` / `AllFBC-EuropeAndNorthAmerica-structure.svg`