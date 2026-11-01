# Commons 标注词汇表（Commons Annotation Vocabulary）本体结构与公理说明

本文档对应 `AnnotationVocabulary.rdf` / `AnnotationVocabulary.ttl`，说明该本体的类、继承关系、属性和公理约定。结构图见 `AnnotationVocabulary-structure.png`（`AnnotationVocabulary-structure.svg` 为可缩放版本）。

![Commons 标注词汇表（Commons Annotation Vocabulary）本体结构图](AnnotationVocabulary-structure.png)

## 1. 本体概述

提供本体元数据标注用的词汇表：摘要、定义、版权、同义词、缩写、逻辑定义、使用说明等标注属性，并梳理 SKOS 与 Dublin Core 标注属性之间的关系。

**在体系中的位置**：Commons 全部 22 个模块都导入它——它是整个库的「元数据基础设施」，不含业务类。

**上下游关系**：上游仅依赖 Dublin Core、SKOS 等 W3C 词汇；下游被 Commons 所有模块及 FIBO 全库引用（FIBO 用自己的标注词汇表与它对接）。

**与相近概念的差别**：标注属性≠业务属性——标注属性描述「概念本身的文档信息」（如定义、出处），不参与推理；业务属性描述「现实对象之间的关系」。

## 2. 其他属性

以下属性未绑定到本体的具体类（定义域在外部本体或未声明）：

标注属性（Annotation Property）：

| 属性 | 定义 |
|---|---|
| **缩写（abbreviation）** | designation formed by omitting parts from the full form of a term that denotes the same concept |
| **首字母缩写（acronym）** | abbreviation that is made up of the initial letters of the components of the full form of a term or proper name or from syllables of the full form |
| **改编自（adaptedFrom）** | document or other source from which a given term (or its definition) was adapted (i.e., is compatible with but not quoted); the range for this annotation can be a string, URI, or citation |
| **版权（copyright）** | exclusive legal right, given to an originator or an assignee to print, publish, perform, film, or record literary, artistic, or musical material, and to authorize others to do the same |
| **直接来源（directSource）** | quoted reference for the subject resource; the range for this annotation can be a string, URI, or bibliographic citation |
| **解释性说明（explanatoryNote）** | note that provides additional explanatory material for a resource |
| **逻辑定义（logicalDefinition）** | definition in the form of a formal expression, such as the mathematical or logic representation, for the resource |
| **符号（symbol）** | abbreviation that is a design or mark, or other non-alpha-numeric character(s) conventionally used to represent something, such as a currency or mathematical sign or operator |
| **同义词（synonym）** | designation that can be substituted for the primary representation of something |
| **使用说明（usageNote）** | note that provides information about how a given resource is used or may be extended |

## 3. 文件

- 官方 RDF/XML：`AnnotationVocabulary.rdf`
- 中文 Turtle：`AnnotationVocabulary.ttl`
- 结构图：`AnnotationVocabulary-structure.png` / `AnnotationVocabulary-structure.svg`