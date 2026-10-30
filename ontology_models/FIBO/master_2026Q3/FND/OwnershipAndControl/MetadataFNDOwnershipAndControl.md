# FND 所有权与控制模块元数据（Metadata for the FND Ownership and Control Module）说明

本文档对应 `MetadataFNDOwnershipAndControl.rdf` / `MetadataFNDOwnershipAndControl.ttl`。

![FND 所有权与控制模块元数据（Metadata for the FND Ownership and Control Module）结构图](MetadataFNDOwnershipAndControl-structure.png)

## 1. 本文件是什么

声明所有权与控制（Ownership and Control）模块由所有权、控制、所有权与控制三个本体构成，及版本信息。

从机制上说，这是一个元数据清单（metadata manifest）文件：它本身不定义任何类或属性，而是通过 `dct:hasPart` 声明一个域或模块由哪些本体构成，并携带版本 IRI、版权、许可与成熟度等发布管理信息。它回答的问题是「这个域/模块包含什么、当前是什么版本」，供发布工具和文档系统按模块组织内容；它的 `owl:imports` 只引入标注词汇表，不是用来加载业务本体的入口（加载入口是 `All*` 与 `About*` 聚合文件）。

## 2. 声明的构成（dct:hasPart，3 个）

| 构成项 | 中文名称 | 简介 |
|---|---|---|
| `FND/OwnershipAndControl/Control.rdf` | 控制本体（Control Ontology） | 定义「控制」关系：控制方、被控制方与控制程度，用于公司治理与合并报表判断。 |
| `FND/OwnershipAndControl/Ownership.rdf` | 所有权本体（Ownership Ontology） | 定义「拥有」关系：所有者、被拥有资产及所有权份额。 |
| `FND/OwnershipAndControl/OwnershipAndControl.rdf` | 所有权与控制本体（Ownership and Control Ontology） | 综合所有权与控制关系，刻画「谁拥有、谁控制」的基本格局。 |

## 3. 标注依赖（owl:imports，2 个）

以下导入仅用于支撑元数据标注本身（如成熟度等级、概念映射），不属于业务内容：

| 导入本体 | 中文名称 | 简介 |
|---|---|---|
| `FND/Utilities/AnnotationVocabulary.rdf` | FIBO 标注词汇表（FIBO Annotation Vocabulary） | 定义 FIBO 专用的标注属性（如释义来源、成熟度等级），用于本体自身的元数据标注。 |
| `https://www.omg.org/spec/Commons/AnnotationVocabulary/` | OMG 通用标注词汇表（OMG Commons Annotation Vocabulary） | OMG 通用本体库（Commons）中的标注词汇表，提供概念映射等标注属性，FIBO 用它标注术语与外部标准的对应关系。 |

## 4. 文件

- 官方 RDF/XML：`MetadataFNDOwnershipAndControl.rdf`
- 中文 Turtle：`MetadataFNDOwnershipAndControl.ttl`
- 结构图：`MetadataFNDOwnershipAndControl-structure.png` / `MetadataFNDOwnershipAndControl-structure.svg`