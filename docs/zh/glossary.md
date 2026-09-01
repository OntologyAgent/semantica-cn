---
title: 术语表
description: Semantica 中文文档术语对照表——全部译文的译名权威源
source: glossary.md
source_version: 271681c72c5c5395d328b1a64adb9de7ed8e8333
---

# 术语表

本页是 Semantica 中文文档的术语唯一权威源。翻译任何页面前先查本表；缺条目先补表再翻，拿不准的译名保留英文原词（不硬造）。

术语分两张表：**核心术语**已冻结译名，不得更改；**上游词条**随上游 `docs/glossary.md` 演进，本表逐条给出中文译法。

## 核心术语

以下 10 条译名已在规划阶段冻结，全部译文必须逐字采用。

| 英文原词 | 中文译名 | 备注 |
|---------|---------|------|
| Knowledge Graph | 知识图谱 | 简称 KG，首次出现标英文 |
| Context Graph | 上下文图 | `semantica.context` 的核心数据结构 |
| Decision Intelligence | 决策智能 | 决策作为一等对象的模块族 |
| Provenance | 溯源 | W3C PROV-O 兼容 |
| Ontology | 本体 | |
| Entity Resolution | 实体消解 | 又称 entity linking / deduplication |
| Triplet | 三元组 | (主语, 谓语, 宾语) |
| Ingestion | 摄取 | 流水线第一阶段 |
| Reasoning Engine | 推理引擎 | `semantica.reasoning` 的六类引擎 |
| Conflict Detection | 冲突检测 | 先检测后合并，禁止静默覆盖 |

## 上游词条翻译

对照上游 `docs/glossary.md` 的全部条目。"待定名"表示译名尚无把握，正文暂用英文原词。

| 英文原词 | 中文译名 | 备注 |
|---------|---------|------|
| Agent | 智能体 | |
| Context Graph | 上下文图 | 见核心术语 |
| Decision | 决策 | 一等对象，含因果链与溯源 |
| Entity | 实体 | |
| Knowledge Graph (KG) | 知识图谱 | 见核心术语 |
| Knowledge Explorer | 探索 | 产品功能名（2026-09 定名）：界面入口、标签页标题统一用"探索"，不再用"知识探索器" |
| Relationship | 关系 | 带类型、置信度与溯源 |
| Semantic | 语义 | |
| Chunking | 分块 | 七种策略：recursive、semantic、entity-aware 等 |
| Ingestion | 摄取 | 见核心术语 |
| Normalization | 规范化 | |
| Parsing | 解析 | |
| Abductive Reasoning | 溯因推理 | 六类推理引擎之一 |
| Datalog | Datalog | 声明式逻辑语言，保留英文 |
| GraphRAG | GraphRAG | 图增强 RAG，保留英文 |
| Inference | 推理 | |
| LLM | 大语言模型(LLM) | 首次出现标英文 |
| RAG | 检索增强生成(RAG) | 首次出现标英文 |
| Allen Interval Algebra | Allen 区间代数 | 13 种区间关系 |
| BiTemporalFact | BiTemporalFact | 代码类名，保留英文；指双时间维度事实 |
| Edge | 边 | |
| Node | 节点 | |
| Property | 属性 | |
| Temporal Graph | 时态图 | 区别于 UML 的时序图(sequence diagram) |
| Triplet | 三元组 | 见核心术语 |
| Coreference Resolution | 指代消解 | |
| Entity Resolution | 实体消解 | 见核心术语 |
| Event Detection | 事件检测 | |
| Named Entity Recognition (NER) | 命名实体识别(NER) | 首次出现标英文 |
| Relationship Extraction | 关系抽取 | |
| Axiom | 公理 | |
| Class | 类 | 本体中的类别 |
| Ontology | 本体 | 见核心术语 |
| Ontology Hub | 本体中心(Ontology Hub) | 产品功能名，首次出现标英文 |
| OWL | 网络本体语言(OWL) | W3C 标准 |
| SHACL | SHACL | 形状约束语言，标准名保留英文 |
| SKOS | SKOS | 简单知识组织系统，标准名保留英文 |
| Embedding | 嵌入 | 语义向量表示 |
| Graph Database | 图数据库 | |
| Hybrid Search | 混合检索 | 向量相似度 + 关键词过滤 |
| Triplet Store | 三元组库 | RDF 三元组专用存储 |
| Vector Store | 向量库 | 嵌入向量相似度检索 |
| Centrality | 中心性 | |
| Community Detection | 社区发现 | |
| Distance Band | 距离带 | near / mid / far 三档 |
| Distance Intelligence | 距离智能 | v0.5.0 特性 |
| PageRank | PageRank | 算法名，保留英文 |
| Cypher | Cypher | 图查询语言，保留英文 |
| RDF | 资源描述框架(RDF) | W3C 标准 |
| SPARQL | SPARQL | RDF 查询语言，保留英文 |
| Conflict Resolution | 冲突消解 | 注意区分"冲突检测" |
| Data Provenance | 数据溯源 | |
| Deduplication | 去重 | |
| W3C PROV-O | W3C PROV-O | 标准名保留英文 |
| SSRF | 服务端请求伪造(SSRF) | 安全术语 |
| XXE | XML 外部实体注入(XXE) | 安全术语 |

## 使用规则

1. 同一英文术语在全部译文中只用一个译名（以本表为准）。
2. 核心术语的译名已冻结；上游词条如有更好译名，先改本表、再全局替换。
3. 新术语翻译流程：查本表 → 无则补表 → 补不了的保留英文。
4. 本表对应英文源 `docs/glossary.md`，上游更新后需同步本表（追踪机制见 `tools/i18n/zh_status.py`）。

## 延伸阅读

- [翻译规范](./README.md) — 翻译流程与验收规则。
- 英文原页 [Glossary](../glossary.md)。
