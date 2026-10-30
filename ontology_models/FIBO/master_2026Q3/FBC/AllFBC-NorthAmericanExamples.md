# FBC 域北美示例入口（All FBC, North American Examples）聚合说明

本文档对应 `AllFBC-NorthAmericanExamples.rdf` / `AllFBC-NorthAmericanExamples.ttl`。

![FBC 域北美示例入口（All FBC, North American Examples）聚合结构图](AllFBC-NorthAmericanExamples-structure.png)

## 1. 本文件是什么

聚合面向北美市场的示例个体本体（如美国市场与交易所示例），供演示、教学与测试使用，不属于生产参考数据。

从机制上说，这是一个聚合入口（load-all）文件：它本身不定义任何新的类或属性，只通过 `owl:imports` 把一组本体打包在一起。应用只要导入这一个文件，推理机就会把它列出的所有本体一次性加载进来，免去逐个声明的麻烦。因此它的价值不在「内容」，而在「组合」——组合方式本身就表达了发布方的意图（例如按域打包、按区域扩展打包、按是否含参考数据打包）。

## 2. 聚合的本地本体（2 个）

以下本体均可在本目录结构中找到同名 `.rdf` 文件及配套中文文档：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `EXMP/LegalEntities/FinancialInstitutionExamples.rdf` | 金融机构示例（Financial Institution Examples） | 收录典型金融机构的示例个体。 |
| `FBC/AllFBC-NorthAmerica.rdf` | FBC 域北美扩展入口（All FBC, North American Extension） | 聚合 FBC 域中北美法域的扩展本体（美国与加拿大的金融服务实体、监管机构及受控词汇等）。 |

## 3. 上游缺失引用（1 个）

- `BE/AllBE-NorthAmericanExamples`：BE 域北美示例入口（All BE, North American Examples） —— FIBO 上游在聚合文件中引用了该本体（BE 域北美示例个体的入口），但当前版本仓库中并未包含对应文件，属于上游已声明、尚未随本版本发布的内容。

## 4. 文件

- 官方 RDF/XML：`AllFBC-NorthAmericanExamples.rdf`
- 中文 Turtle：`AllFBC-NorthAmericanExamples.ttl`
- 结构图：`AllFBC-NorthAmericanExamples-structure.png` / `AllFBC-NorthAmericanExamples-structure.svg`