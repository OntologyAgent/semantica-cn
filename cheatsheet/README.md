# Semantic Web Cheatsheets · 语义网规范速查系列

一套统一设计的语义网规范速查卡:24 张卡覆盖从数据模型、本体语言到领域词表的完整技术栈。每张卡固定 **176 × 250 mm** 版面、「Measured Graph」视觉体系(暖纸 #F6F1E7 · 墨 #1C2430 · 朱红 #B23A26 · 蓝 #33506E),**总分结构**——第 01 节永远是这张卡自己的地图。

设计哲学见 [design-philosophy.md](design-philosophy.md)。

---

## 怎么读一张卡

每张卡都是同一个骨架:

- **§01 总览**——色带结构图 + 主线注记。先读它,后面所有细节都挂在图上
- **PART N 分部**——每节的右上角小字标明所属部分,从简单到复杂排列
- **深色代码块**——可直接抄的 Turtle / SPARQL 示例
- **实操坑清单**——每张卡的收尾,按踩坑频率排序
- **页脚 `SHEET NN · P.N/M`**——PL 编号即系列编号,卡片间互引用「引 PL.NN §NN」格式

配套深度笔记:[RDF 1.1 问答笔记](RDF%201.1/rdf-1.1-qa.md)(白话费曼式,其余卡片按需补)。

---

## 全系列目录

### 核心模型与语言

| 编号 | 卡片 | 页 | 一句话 |
|---|---|---|---|
| PL.01 | [RDF 1.1](RDF%201.1/rdf-1.1-cheatsheet.html) | 7 | 底座:三元组、图、IRI/字面量/bnode、六种语法、蕴含三档 |
| PL.02 | [RDFS 1.1](RDFS%201.1/rdfs-cheatsheet.html) | 5 | 词表与推理:subClassOf、domain/range、闭包规则 |
| PL.04 | [OWL 2](OWL%202/owl-cheatsheet.html) | 8 | 本体语言:类构造子、公理、三剖面、推理复杂度 |
| PL.05 | [SWRL](SWRL/swrl-cheatsheet.html) | 4 | OWL + Horn 规则:原子七类与可判定性代价 |
| PL.06 | [RDF 1.2](RDF%201.2/rdf-1.2-cheatsheet.html) | 4 | 演进版:三元词项、方向性语言标签、版本声明 |
| PL.10 | [SPARQL 1.1](SPARQL1.1/sparql-cheatsheet.html) | 5 | 查询与更新:图模式、属性路径、协议族 |

### 校验与策略

| 编号 | 卡片 | 页 | 一句话 |
|---|---|---|---|
| PL.07 | [SHACL 1.0](SHACL%201.0/shacl-cheatsheet.html) | 5 | 形状校验:约束组件、验证报告,闭世界合同 |
| PL.09 | [ODRL 2.2](ODRL%202.2/odrl-cheatsheet.html) | 4 | 许可政策:permission / duty / constraint 写成数据 |

### 通用基础设施词表

跨领域的基础构件——不绑定任何行业,任何知识图谱都可能用到。

| 编号 | 卡片 | 页 | 一句话 |
|---|---|---|---|
| PL.03 | [SKOS](SKOS/skos-cheatsheet.html) | 5 | 知识组织:概念方案、标签三约束、五种映射 |
| PL.11 | [PROV-O](PROV-O/prov-o-cheatsheet.html) | 3 | 溯源本体(旧版视觉,待重做) |
| PL.12 | [OWL-Time](OWL-Time/owl-time-cheatsheet.html) | 4 | 时间本体:时点/时段、Allen 15 关系 |
| PL.13 | [FOAF](FOAF/foaf-cheatsheet.html) | 3 | 人物词表:IFP 身份标识、档案文档 |
| PL.14 | [DCTERMS](DCTERMS/dcterms-cheatsheet.html) | 3 | 都柏林核心:15 老元素 + 细化词层级 |
| PL.15 | [QUDT](QUDT/qudt-cheatsheet.html) | 3 | 单位与量类:三件套模式、量纲向量、换算 |
| PL.22 | [DCAT 3](DCAT/dcat-cheatsheet.html) | 2 | 数据目录:Catalog → Dataset → Distribution、复用优先 |
| PL.23 | [SSN/SOSA](SSN-SOSA/ssn-sosa-cheatsheet.html) | 2 | 传感观测:观测五件套、SOSA 轻量核 + SSN 推理层 |
| PL.24 | [ORG](ORG/org-cheatsheet.html) | 2 | 组织本体:成员三机制、reportsTo、变更历史 |

### 行业与领域本体

| 编号 | 卡片 | 页 | 一句话 |
|---|---|---|---|
| PL.16 | [LKIF Core](LKIF/lkif-cheatsheet.html) | 3 | 法律:规范、霍菲尔德权利、法律渊源 |
| PL.17 | [FRAPO](FRAPO/frapo-cheatsheet.html) | 3 | 科研管理:资助、合同、预算(FRapo = Funding, Research Administration and Projects Ontology) |
| PL.18 | [FIBO](FIBO/fibo-cheatsheet.html) | 3 | 金融本体:11 域、证券衍生贷款、OMG 标准(MIT 许可) |
| PL.19 | [BIOMED](BIOMED/biomed-cheatsheet.html) | 3 | 生物医学全景:SNOMED CT、OBO 家族、LOINC / RxNorm 映射 |
| PL.20 | [EPCIS 2.0](EPCIS/epcis-cheatsheet.html) | 2 | 供应链事件:四维四类型、CBV 词表、JSON-LD |
| PL.21 | [GeoSPARQL 1.1](GeoSPARQL/geosparql-cheatsheet.html) | 2 | 地理空间:要素与几何分离、sf: 层级、拓扑函数 |

### 服务

| 编号 | 卡片 | 页 | 一句话 |
|---|---|---|---|
| PL.08 | [OWL-S 1.1](OWL-S%201.1/owl-s-cheatsheet.html) | 3 | 服务本体:Profile / ProcessModel / Grounding 三档案 |

---

## 依赖关系

全部词表和语言最终都落在同一块地基上。整图见 [assets/dependency-map.svg](assets/dependency-map.svg),ASCII 速览:

```text
          ┌─ 第 4 层 · 领域词表与应用 ────────────────────────┐
          │ SKOS  FOAF  DCTERMS  OWL-Time  QUDT  PROV-O      │
          │ LKIF  FRAPO  ODRL  OWL-S                         │
          └────┬─────────────────────────────┬───────────────┘
    形式公理    │                  直接写成三元组│
(OWL DL / SHACL)│                             │
┌─ 第 3 层 · 推理与查询 ─────────────────────┴────────────┐
│  OWL 2 ── SWRL      SPARQL 1.1(蕴含档位)   SHACL(闭世界) │
└──────┬──────────────┬───────────────────┬───────────────┘
       │表达力升级     │查询                │校验
┌─ 第 2 层 · 词表与语义 ──────────────────────────────────┐
│  RDFS 1.1 · subClassOf/subPropertyOf · domain/range     │
└──────┬──────────────────────────────────────────────────┘
       │词表写在图上
┌─ 第 1 层 · 数据模型 ────────────────────────────────────┐
│  RDF 1.1 · 三元组 · 图   ◀── RDF 1.2(向后兼容的演进)    │
└─────────────────────────────────────────────────────────┘
```

读图三句话:

1. **第 1 层只有一页纸的内容**——三元组、图、两种匿名节点。真正的底
2. **每一层用下一层的机制写成**——RDFS 是一份说了「subClassOf 是什么」的 RDF 文件;OWL、SKOS、FRAPO 全部同理,自举到底,没有新机器
3. **SHACL 与 OWL 分属两个世界**——闭世界校验对开世界推理,互补不互斥

---

## 学习路径

按目标选路线,编号即上面目录的 PL 号:

**路线 A · 模型与推理主线**(理解语义网在做什么)

```text
PL.01 RDF 1.1 ──▶ PL.02 RDFS ──▶ PL.10 SPARQL ──▶ PL.04 OWL 2 ──▶ PL.05 SWRL
   底座            词表+推理       查询             本体            加规则
```

**路线 B · 数据质量**(给数据上验收标准)

```text
PL.01 RDF 1.1 ──▶ PL.07 SHACL ──▶ PL.15 QUDT
   底座            形状校验         单位化数值
```

**路线 C · 词汇应用**(直接搭知识图谱)

```text
PL.01 → PL.02 → PL.13 FOAF(人)→ PL.14 DCTERMS(文档)→ PL.03 SKOS(概念)
                    ↘ PL.12 时间 / PL.15 单位 / PL.11 溯源,按需取用
```

**路线 D · 法律与合规**

```text
PL.16 LKIF(法律概念)──▶ PL.09 ODRL(许可政策)──▶ PL.17 FRAPO(合同与经费)
```

**路线 E · 服务与自动化**

```text
PL.04 OWL 2 ──▶ PL.08 OWL-S(服务描述)──▶ PL.09 ODRL(数据许可)
```

配套读法:每条路线跑完,回到对应卡的 §01 总览做一次「只看图复述」——能复述,才算过。

---

## 工程约定

- **产物三件套**:每卡 `<name>-cheatsheet.html` + `.pdf` + 每页一张 `-N.png`
- **页面规格**:176 × 250 mm,`@page` 直出 PDF;PNG 按 1040/665 缩放因子逐 sheet 截取
- **字体**:JetBrainsMono / BigShoulders / InstrumentSans,经 `file://` 引入(渲染机需要对应字体文件)
- **内容纪律**:官方状态与术语先核对再写;在途规范(如 RDF 1.2、OWL-Time CRD)标注检索日期;弃用术语保留但标明
- **重构规范**:节序调整后,正文交叉引用(`§NN`、`引 PL.NN §NN`)必须逐条按新旧映射校准
- **已知欠账**:PL.11 PROV-O 仍为旧版视觉体系,重做等于整卡重建,未排期

---

## 文件结构

```text
cheatsheet/
├── README.md                     ← 本文件
├── design-philosophy.md          ← 视觉设计宣言
├── assets/
│   └── dependency-map.svg        ← 依赖关系图(本页引用)
├── <规范名>/
│   ├── <name>-cheatsheet.html    ← 源(单文件,内嵌全部样式)
│   ├── <name>-cheatsheet.pdf     ← 打印版
│   ├── <name>-cheatsheet-N.png   ← 每页一张
│   └── <name>-qa.md              ← 学习笔记(目前 PL.01 有)
└── _archive/
    └── <规范名>/                  ← 重构前的历史版本
```
