# 虚拟地点本体（Virtual Places Ontology）结构与公理说明

本文档对应 `VirtualPlaces.rdf` / `VirtualPlaces.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `VirtualPlaces-structure.png`（`VirtualPlaces-structure.svg` 为可缩放版本）。

![虚拟地点本体（Virtual Places Ontology）本体结构图](VirtualPlaces-structure.png)

## 1. 本体概述

本本体为描述虚拟位置概念提供脚手架。

## 2. 类（Class）

| 类（Class） | 定义（Definition） |
|---|---|
| 电子邮件地址（electronic mail address） | 定义电子邮件消息可投递到的电子消息端点的虚拟地址，通常通过基于简单邮件传输协议（SMTP）的通信系统投递。 |
| 网络位置（network location） | 可由网络地址（节点或接口的标识符）标识的虚拟位置。 |
| 概念性地点（notional place） | 一种抽象地点，是“国内”“欧元区”等众多常见概念之一。 |
| 电话号码（telephone number） | 可分配给固定电话用户台、无线电子电话设备或其他通过公共交换电话网传输数据的设备的虚拟地址。 |

### 2.1 继承关系（Inheritance）

- 电子邮件地址（electronic mail address） ⊑ 虚拟地址
- 网络位置（network location） ⊑ 虚拟位置
- 概念性地点（notional place） ⊑ 位置
- 电话号码（telephone number） ⊑ 虚拟地址

## 3. 对象属性（Object Property）

| 属性（Property） | 中文（English） | 定义（Definition） | 说明 |
|---|---|---|---|
| fibo-fnd-plc-vrt:hasElectronicMailAddress | 具有电子邮件地址（has electronic mail address） | 指定某实体可被定位、联系或接收信件的电子消息端点。 | 值域（range）：电子邮件地址（electronic mail address）；子属性（subPropertyOf）：具有地址 |
| fibo-fnd-plc-vrt:hasTelephoneNumber | 具有电话号码（has telephone number） | 指示由数字和符号序列组成的虚拟地址，可分配给固定电话用户台或无线电子电话设备等。 | 值域（range）：电话号码（telephone number）；子属性（subPropertyOf）：具有地址 |

## 5. 公理约定（Axioms）

- 网络位置（network location）：由……标识 地址 =1

## 6. 依赖（owl:imports，6 个）

本本体通过 `owl:imports` 引入以下本体，各项的中文名称与简介如下：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `FND/Places/Addresses.rdf` | 地址本体（Addresses Ontology） | 定义邮政地址及其组成部分，为机构注册地、通讯地址建模。 |
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |
| `https://www.omg.org/spec/Commons/Identifiers/` | OMG 通用标识符本体（OMG Commons Identifiers） | Commons 库中的标识符本体，定义标识符及其编码方案的通用概念。 |
| `https://www.omg.org/spec/Commons/Locations/` | OMG 通用位置本体（OMG Commons Locations） | Commons 库中的位置本体，定义地理位置、地点的通用概念。 |
| `https://www.omg.org/spec/Commons/Organizations/` | OMG 通用组织本体（OMG Commons Organizations） | Commons 库中的组织本体，定义组织、组织成员与组织结构的通用概念。 |

## 7. 文件

- 官方 RDF/XML：`VirtualPlaces.rdf`
- 中文 Turtle：`VirtualPlaces.ttl`
- 结构图：`VirtualPlaces-structure.png` / `VirtualPlaces-structure.svg`