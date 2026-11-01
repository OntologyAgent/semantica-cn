# Commons 文本数据类型本体（Commons Text Datatype Ontology）结构与公理说明

本文档对应 `TextDatatype.rdf` / `TextDatatype.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `TextDatatype-structure.png`（`TextDatatype-structure.svg` 为可缩放版本）。

![Commons 文本数据类型本体（Commons Text Datatype Ontology）本体结构图](TextDatatype-structure.png)

## 1. 本体概述

定义文本相关的数据类型：带语言标记的字符串等基础文本格式。

**在体系中的位置**：Commons 最底层的类型模块，为名称、描述等文本属性提供数据类型定义。

**上下游关系**：上游仅依赖标注词汇表；下游被指称符、集合等基础模块引用。

**与相近概念的差别**：本模块不含任何类，只定义数据类型（datatype）——它管「文本值怎么表示」，不管「事物是什么」；与语言模块的差别——语言模块定义语言实体，本模块定义带语言标记的文本格式。

## 2. 其他属性

以下属性未绑定到本体的具体类（定义域在外部本体或未声明）：

数据属性（Datatype Property）：

| 属性 | 定义 |
|---|---|
| **具有文本值（has text value）** | 为某事物提供字符串值，可带或不带语言标签。<br>provides a string value for something, with or without a language tag |

## 3. 依赖（owl:imports，1 个）

本本体通过 `owl:imports` 引入以下本体，各项的中文名称与简介如下：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `AnnotationVocabulary/AnnotationVocabulary.rdf` | Commons 标注词汇表（Commons Annotation Vocabulary） | 提供文档标注常用的属性，如摘要、定义、解释、版权、同义词等，并梳理 SKOS 与 Dublin Core 标注属性之间的关系。 |

## 4. 文件

- 官方 RDF/XML：`TextDatatype.rdf`
- 中文 Turtle：`TextDatatype.ttl`
- 结构图：`TextDatatype-structure.png` / `TextDatatype-structure.svg`