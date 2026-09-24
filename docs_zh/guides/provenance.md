---
title: 溯源与审计轨迹
description: Semantica 如何用符合 W3C PROV-O 的记录追踪每个实体、关系、分块和属性的来源与血缘——带 SHA-256 完整性校验和与 SQLite 持久化，为国防、制药、银行和安全合规提供跨模块审计轨迹。
source: guides/provenance.md
source_version: ee460eeedc477bc34c63a132defdfa0e76c9c6d7
icon: "file-certificate"
---

## 什么是溯源？

溯源(Provenance)是指系统性地记录数据从哪里来、经历了怎样的变换、生命周期中每一步由谁负责。普通的图元数据只是描述实体，溯源则更进一步：它建立一条不可篡改的审计轨迹，追踪系统中每一条信息的完整历史。

**关键溯源概念：**

**血缘(Lineage)** 追踪从原始来源、经所有变换、到当前状态的监管链，精确呈现数据如何随时间演化。

**来源归属(Source attribution)** 记录产出每条数据的特定文档、数据库、API 调用或人工输入，支持精确引用与验证。

**完整性校验** 使用密码学校验和，检测溯源记录创建之后的任何未授权更改。

**审计轨迹(Audit trail)** 通过防篡改日志记录全部数据操作、变换和决策，满足监管合规要求。

溯源与简单元数据的区别在于：它创建法律上可辩护、密码学上可验证的记录，能回答这些关键问题——"它从哪来？""谁处理了它？""它何时变更？""它被篡改过吗？"

## 为什么使用溯源？

**满足监管要求。** 对接 FDA 21 CFR Part 11、ICH E6(R2) GCP、巴塞尔 III BCBS 239 以及国防情报共享协议——这些法规都强制要求数据全程可追溯和电子记录完整性。

**来源归属与引用。** 把每个实体、关系和属性值回溯到其确切的源文档、API 响应或人工输入，支撑科研可复现性与法律可辩护性。

**可审计与透明。** 让审计方、监管机构和利益相关方完整看到数据处理工作流：谁执行了每个操作、变更何时发生。

**冲突消解(Conflict Resolution)与数据质量。** 当多个来源对同一属性给出不同值时，溯源记录支持基于证据的冲突消解——比较来源可信度、时新性和置信度水平。

**篡改检测与取证。** 密码学完整性校验能发现对数据记录的未授权修改，支撑安全敏感环境中的事件响应与取证分析。

**数据血缘可追溯。** 回答关于数据世系的复杂问题，尤其是在多阶段处理流水线中——实体经历抽取、增强、融合和分析变换的场景。

## 适用与不适用场景

**适合启用溯源追踪：**
- 要求审计轨迹的受监管环境（医疗、金融、国防、制药）
- 需要基于证据消解信息冲突的多源数据融合
- 数据质量与来源可信度很重要的长期知识图谱(Knowledge Graph)
- 数据完整性与篡改检测至关重要的生产系统
- 实体经历多重变换的复杂处理流水线
- 基于抽取数据所做的决策需要法律可辩护性的场合

**溯源可能不必要：**
- 无合规要求的简单原型和概念验证演示
- 数据只处理一次、结果立即丢弃的临时工作流
- 跨会话不持久化数据的无状态应用
- 数据来自单一可信来源的内部研究项目
- 溯源开销影响性能的高频低延迟操作
- 所有数据都来自单一、高度可信且从不变更来源的场景

**以下情况可考虑更简单的替代方案：**
- 基础元数据（创建时间戳、源文件名）已提供足够的可追溯性
- 数据处理透明，仅靠版本控制即可复现
- 监管合规不要求密码学完整性校验

`ProvenanceManager` 为每个实体、关系、文档分块和属性值记录一条符合 W3C PROV-O 的条目——带 SHA-256 校验和用于篡改检测，并在每次 `track_entity()` 调用时自动做版本链接。当你需要回答监管问题——某个值从哪来、谁写入的、自首次摄取以来是否变更过——就用它。

<Info>
知识图谱流水线会对它抽取的所有内容自动调用 `track_entity()` 和 `track_relationship()`，因此经标准流水线进入的实体已被追踪。当你需要自定义审计集成、跨模块血缘链，或跨多来源的细粒度属性级归属时，再使用本指南介绍的手动 API。
</Info>

## 搭建溯源存储

`ProvenanceManager` 支持两种存储后端。内存存储零依赖，适合测试。SQLite 存储跨重启持久化、支持并发读，还能让合规团队直接用标准工具查询一个标准数据库。

```python
from semantica.provenance import ProvenanceManager

# In-memory — session only, no persistence
prov = ProvenanceManager()

# SQLite — persists to disk, free concurrent reads
prov = ProvenanceManager(storage_path="provenance.db")

# Custom backend — pass any ProvenanceStorage implementation
from semantica.provenance.storage import SQLiteStorage
prov = ProvenanceManager(storage=SQLiteStorage("audit.db"))
```

任何受监管部署——安全运营、临床数据、金融风险——都应使用 `storage_path`。SQLite 文件可以备份、版本化，并用标准工具查询，无需架设服务器。

<Note>
  `SQLiteStorage` 自动配置预写日志(Write-Ahead Logging, `WAL`)、`busy_timeout=5000` 和 `synchronous=NORMAL`；读-改-写操作（如 `track_entity()`）在原子立即事务（`BEGIN IMMEDIATE`）中执行，普通读取（`retrieve()`、`trace_lineage()`）走独立连接、不加显式写锁，因此不会串行排在写入者之后。此外，自定义存储后端只要覆写 `trace_lineage(self, entity_id)` 即可获得支持，`ProvenanceManager` 不要求其签名中含 `max_depth`。
</Note>

## 摄取数据时记录溯源

数据进入图谱的那一刻，就是必须记录溯源的那一刻。`track_entity()` 捕获源文档、时间戳、执行抽取的操作者或流水线、来源原文引句，以及置信度分数。它返回 `Optional[ProvenanceEntry]`（成功返回 `ProvenanceEntry`，全新实体的存储失败返回 `None`），SHA-256 校验和自动计算。

```python
# Ingesting CVE-2024-3400 from NVD and a commercial feed
# Both are tracked separately so the full multi-source picture is preserved.

entry_nvd = prov.track_entity(
    entity_id="cve-2024-3400",
    source="NVD_feed_2024-04-12",
    metadata={
        "cvss_score": 10.0,
        "vector": "AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H",
        "exploit_status": "unconfirmed",
    },
    confidence=0.98,
    entity_type="vulnerability",
    activity_id="nvd_feed_ingestion",
    source_location="CVE-2024-3400 JSON record",
    source_quote='{"cvssMetricV31":[{"cvssData":{"baseScore":10.0}}]}',
)

print(f"Entity tracked : {entry_nvd.entity_id}")
print(f"Source         : {entry_nvd.source_document}")
print(f"Timestamp      : {entry_nvd.timestamp}")
print(f"Checksum       : {entry_nvd.checksum}")       # SHA-256 hex digest
print(f"First seen     : {entry_nvd.first_seen}")     # set on first call only
```

```text
Entity tracked : cve-2024-3400
Source         : NVD_feed_2024-04-12
Timestamp      : 2024-04-12T14:22:07.881Z
Checksum       : 3f7a9c2d...                          # tamper-detectable
First seen     : 2024-04-12T14:22:07.881Z
```

一小时后，同一实体又从商业数据源到达。对同一个 `entity_id` 再次调用 `track_entity()`，NVD 条目会自动归档为历史记录，并创建一条经 `parent_entity_id` 链接到它的新当前条目：

```python
entry_commercial = prov.track_entity(
    entity_id="cve-2024-3400",
    source="commercial_feed_2024-04-12",
    metadata={
        "cvss_score": 9.8,
        "exploit_status": "in_wild",
        "observed_exploitation": True,
    },
    confidence=0.91,
    entity_type="vulnerability",
    activity_id="commercial_feed_ingestion",
)

# The NVD entry is now archived as cve-2024-3400:v:2024-04-12T14:22:07
# The commercial entry is the new current state
# entry_commercial.parent_entity_id == "cve-2024-3400:v:2024-04-12T14:22:07"
```

版本链接自动发生，你无需手动管理历史条目。

## 追踪多来源属性值

当同一属性在多个来源中出现且值不同——正是上面的 CVE 分数场景——用 `track_property_source()` 分别记录每一条归属。这些记录直接为下游的冲突检测(Conflict Detection)提供输入：冲突模块可以比较某属性的全部已追踪值，并连同完整来源元数据一起呈现分歧。

**SourceReference** 是一个结构化元数据容器，精确捕获一条信息在文档中的出处：文档标识符、具体位置（页码、章节、字节区间）、置信度水平，以及满足领域特定归属需求的自定义元数据字段。

```python
from semantica.provenance.schemas import SourceReference

nvd_ref = SourceReference(
    document="NVD_feed_2024-04-12",
    section="cvssMetricV31",
    confidence=0.98,
    metadata={"publisher": "NIST", "feed_type": "NVD"},
)

commercial_ref = SourceReference(
    document="commercial_feed_2024-04-12",
    section="cvss_assessment",
    confidence=0.91,
    metadata={"publisher": "ThreatFeed-Co", "observed": True},
)

# Track each source's value separately under the same entity + property key
prov.track_property_source("cve-2024-3400", "cvss_score", 10.0, nvd_ref)
prov.track_property_source("cve-2024-3400", "cvss_score", 9.8,  commercial_ref)

# Property sources are stored under "<entity_id>_<property_name>"
# Later: retrieve all sources for this property to answer "where did 9.8 come from?"
sources = prov.get_all_sources("cve-2024-3400_cvss_score")
for s in sources:
    print(f"{s['source']:<35}  confidence={s['confidence']:.2f}  loc={s['location'] or '—'}")
```

```text
NVD_feed_2024-04-12                   confidence=0.98  loc=cvssMetricV31
commercial_feed_2024-04-12            confidence=0.91  loc=cvss_assessment
```

当监管机构问"9.8 这个值从哪来？"，答案就在这里：`commercial_feed_2024-04-12`，章节 `cvss_assessment`，置信度 0.91，完整元数据表明它来自一家报告了在野利用情况的商业数据商。

## 追踪节点的血缘

一个实体有了多条溯源条目之后，就可以追踪它的完整历史，了解它如何随时间演化。摄取六个月后，跑一次血缘追踪：`get_lineage()` 返回完整版本链——实体经历过的每一个状态，从旧到新——外加汇总元数据：

```python
lineage = prov.get_lineage("cve-2024-3400")

print(f"Entity      : {lineage['entity_id']}")
print(f"First seen  : {lineage['first_seen']}")
print(f"Last updated: {lineage['last_updated']}")
print(f"History depth: {lineage['entity_count']} entries")
print(f"Sources seen : {lineage['source_documents']}")
print()
print("Full version chain (oldest → newest):")
for entry in lineage["lineage_chain"]:
    print(f"  [{entry['timestamp'][:19]}]  agent={entry['agent_id']}")
    print(f"    source={entry['source_document']}")
    print(f"    activity={entry['activity_id']}")
```

```text
Entity      : cve-2024-3400
First seen  : 2024-04-12T14:22:07.881Z
Last updated: 2024-10-08T09:11:44.302Z
History depth: 4 entries
Sources seen : ['NVD_feed_2024-04-12', 'commercial_feed_2024-04-12',
                'NVD_feed_2024-07-18', 'commercial_feed_2024-10-08']

Full version chain (oldest → newest):
  [2024-04-12T14:22:07]  agent=semantica
    source=NVD_feed_2024-04-12
    activity=nvd_feed_ingestion
  [2024-04-12T15:18:33]  agent=semantica
    source=commercial_feed_2024-04-12
    activity=commercial_feed_ingestion
  [2024-07-18T08:04:11]  agent=semantica
    source=NVD_feed_2024-07-18
    activity=nvd_feed_ingestion       # NVD updated their score
  [2024-10-08T09:11:44]  agent=semantica
    source=commercial_feed_2024-10-08
    activity=commercial_feed_ingestion
```

这条链回答了监管者的全部三个问题：9.8 来自 `commercial_feed_2024-04-12`；操作者是 `threat_ingest_pipeline_v2`；分数确实变更过——NVD 在 7 月 18 日更新了记录——链上精确显示了变更时间。

## 校验完整性

每条 `ProvenanceEntry` 都带写入时计算的 SHA-256 校验和。如果任何字段事后被修改——无论是配置错误的流水线、数据库迁移，还是蓄意篡改——重算的校验和都将无法匹配。

完整性校验对监管合规和取证分析至关重要。把完整性检查纳入每一次合规审计：

```python
from semantica.provenance.integrity import compute_checksum

raw_entries = prov.trace_lineage("cve-2024-3400")

print("Integrity check:")
for e in raw_entries:
    stored   = e.checksum
    computed = compute_checksum(e)
    status   = "OK" if stored == computed else "TAMPERED"
    print(f"  [{status}] {e.entity_id[:50]}  {(stored or '')[:16]}...")
```

```text
Integrity check:
  [OK] cve-2024-3400                                 3f7a9c2d...
  [OK] cve-2024-3400:v:2024-04-12T14:22:07           a1b2c3d4...
  [OK] cve-2024-3400:v:2024-04-12T15:18:33           e5f6a7b8...
  [OK] cve-2024-3400:v:2024-07-18T08:04:11           c9d0e1f2...
```

`TAMPERED` 状态意味着存储的哈希与按当前字段值重算的结果不一致——这是写入后遭修改的证据，在记录用于合规用途之前必须先调查清楚。

## 追踪文档分块及其子块

溯源不只面向实体。当文档为检索增强生成(RAG)或自然语言处理工作流被切分成块时，每个分块都需要自己的溯源记录，把它链接到源文件和字节区间。

递归切分产生的子分块经 `parent_chunk_id` 链接到父分块，对应 W3C PROV-O 标准中的 `prov:wasDerivedFrom`：

```python
# Track the parent chunk (a section of an advisory PDF)
prov.track_chunk(
    chunk_id="advisory_section_3",
    source_document="CISA_advisory_AA24-099A.pdf",
    source_path="/feeds/cisa/advisories/AA24-099A.pdf",
    start_index=4096,
    end_index=8192,
)

# Track a child chunk derived from recursive splitting
prov.track_chunk(
    chunk_id="advisory_section_3a",
    source_document="CISA_advisory_AA24-099A.pdf",
    source_path="/feeds/cisa/advisories/AA24-099A.pdf",
    start_index=4096,
    end_index=6144,
    parent_chunk_id="advisory_section_3",   # prov:wasDerivedFrom
)

# Retrieve the provenance record for a chunk
record = prov.get_provenance("advisory_section_3a")
if record:
    print(f"Source   : {record['source_document']}")
    print(f"Range    : bytes {record['start_index']}–{record['end_index']}")
    print(f"Parent   : {record['parent_entity_id']}")  # advisory_section_3
    print(f"Checksum : {record['checksum']}")
```

在 GDPR 数据主体删除请求的工作流中，每个分块溯源记录中的字节区间会精确告诉你：该删哪份文档的哪个部分。

## 溯源库的统计信息

大规模摄取运行结束后，`get_statistics()` 给出全部已追踪内容的汇总：

```python
stats = prov.get_statistics()

print(f"Total tracked    : {stats['total_entries']}")
print(f"By entity type   : {stats['entity_types']}")
print(f"Unique sources   : {stats['unique_sources']}")
```

```text
Total tracked    : 14,822
By entity type   : {'vulnerability': 3041, 'chunk': 8204, 'relationship': 2891,
                    'property': 686}
Unique sources   : 12
```

这份汇总是合规证明的起点：你可以据此陈述已追踪记录总数、不同数据来源数量，以及按记录类型的分布。

## 常见陷阱

**溯源不保证真实。** 溯源记录忠实追踪信息从哪来、如何被处理，但它无法验证原始来源本身是否准确。一条来自缺陷或恶意来源、记录得再完美的监管链，产出的仍是不可靠数据。

**复用泛化的来源标识符。** 使用"daily_feed"或"batch_001"这类无区分度的来源 ID，会让单条记录无法回溯到确切来源。来源文档名中务必带上时间戳、版本号或唯一批次标识。

**绕过溯源工作流。** 手工插入数据或运行跳过 `track_entity()` 调用的临时脚本，会在审计轨迹上留下缺口。所有数据入口——自动化流水线、人工修正、管理操作——都应记录相应的溯源。

**忽视血缘校验。** 在多阶段处理流水线中，溯源链会变得复杂。定期校验 `get_lineage()` 和 `trace_lineage()` 返回的链完整且逻辑连贯，没有缺失环节或循环引用。

**在低价值场景滥用溯源。** 为每个中间计算或临时变量记录溯源，只会增加存储开销而没有合规收益。把溯源追踪聚焦在有法律、监管或业务意义的实体、关系和属性上。

**忘记校验完整性校验和。** 密码学完整性校验只有在你真的去检查时才有效。把定期的 `compute_checksum()` 校验纳入审计工作流和事件响应流程。

**混用溯源粒度。** 有的实体在文档层级追踪、有的在句子层级追踪，会产生不一致的审计轨迹。为每类数据和每个处理工作流建立一致的粒度标准。

## 领域示例

<Tabs>

<Tab title="国防 — CTI/威胁情报">

信号情报融合小组追踪每个情报实体从原始采集、分析处理到成品的监管链。链上每一层——原始采集、NER 抽取、融合、成品情报——都必须单独记录，并附上相应的密级处理方式和操作者身份。溯源链就是监管链(chain of custody)：它证明成品情报产品的每一步都可追溯到经授权的采集和经授权的分析。

按 ITAR 和情报界共享协议的要求，溯源记录必须显示：原始数据由哪种采集方式产出、由哪位分析师处理、在实体进入成品之前由哪个融合活动与其他情报合并。`track_chunk()`、`track_entity()` 和 `track_relationship()` 各对应链上的一层。

```python
from semantica.provenance import ProvenanceManager
from semantica.provenance.schemas import SourceReference

prov = ProvenanceManager(storage_path="intel_provenance.db")

# Tier 1: Raw collection
prov.track_chunk(
    chunk_id="osint_collection_20260621_0442Z",
    source_document="COLLECTION_TASKING_TK-2026-0192",
    source_path="/osint/raw/20260621_0442Z.txt",
    start_index=0,
    end_index=2048,
    classification="UNCLASSIFIED//FOUO",
    collection_method="OSINT",
    collector_id="STATION_ECHO",
)

# Tier 2: Entity extracted from collection
prov.track_entity(
    entity_id="threat_actor_DELTA9",
    source="osint_collection_20260621_0442Z",
    metadata={"label": "THREAT_ACTOR", "confidence_level": "C2"},
    confidence=0.87,
    entity_type="threat_actor",
    activity_id="ner_extraction",
    source_location="paragraph_3",
)

# Tier 3: Campaign relationship from all-source fusion
prov.track_relationship(
    relationship_id="DELTA9_operates_CAMPAIGN_IRON",
    source="FUSION_REPORT_FP-2026-0447",
    metadata={"type": "operates", "confidence": 0.81},
    confidence=0.81,
    activity_id="all_source_fusion",
)

# Tier 4: Property from two independent INT sources
humint_src = SourceReference(
    document="HUMINT_REPORT_HR-2026-0821",
    confidence=0.91,
    metadata={"classification": "SECRET", "source_country": "PARTNER_5EYES"},
)
imint_src = SourceReference(
    document="IMINT_PRODUCT_IP-2026-1104",
    page=3,
    section="Ground Truth Assessment",
    confidence=0.87,
    metadata={"sensor": "OPIR", "resolution_m": 0.3},
)
prov.track_property_source("DELTA9", "location_country", "COUNTRY_X", humint_src)
prov.track_property_source("DELTA9", "location_country", "COUNTRY_X", imint_src)

# Finished product audit — full chain of custody
lineage = prov.get_lineage("threat_actor_DELTA9")
print("Chain of custody:")
for entry in lineage["lineage_chain"]:
    print(f"  [{entry['timestamp'][:19]}]  {entry['activity_id']}  agent={entry['agent_id']}")

# Corroborating INT sources for the location assessment
sources = prov.get_all_sources("DELTA9_location_country")
for s in sources:
    print(f"  INT source: {s['source']}  (conf={s['confidence']:.2f})")
```

</Tab>

<Tab title="安全 — SOC/事件响应">

SOC 威胁情报平台追踪每个 CVE 的完整历程：从首次 NVD 摄取，到增强运行、CVSS 更新和分析师标注。溯源链回答事件响应中最要紧的问题："这条漏洞记录是最新的吗？自我们上次检查以来，CVSS 分数被修订过吗？"

对同一个 `entity_id` 反复调用 `track_entity()` 形成的版本链，就是一份完整的更新历史。如果 NVD 在概念验证发布后把分数从 7.5 修订到 9.8，这条链会显示修订的精确时间戳，以及是哪条流水线写入了更新值。

```python
from semantica.provenance import ProvenanceManager
from semantica.provenance.schemas import SourceReference
from semantica.provenance.integrity import compute_checksum

prov = ProvenanceManager(storage_path="soc_provenance.db")

# Initial NVD ingestion
prov.track_entity(
    entity_id="cve-2023-44487",
    source="NVD_feed_2023-10-10",
    metadata={"cvss_score": 7.5, "description": "HTTP/2 Rapid Reset DDoS"},
    confidence=0.98,
    entity_type="vulnerability",
    activity_id="nvd_feed_ingestion",
)

# Six weeks later: NVD revised the score after PoC publication
prov.track_entity(
    entity_id="cve-2023-44487",
    source="NVD_feed_2023-11-22",
    metadata={"cvss_score": 7.5, "kev_added": True, "known_exploited": True},
    confidence=0.98,
    entity_type="vulnerability",
    activity_id="nvd_feed_update",
)

# Track CISA KEV addition as a separate property source
kev_ref = SourceReference(
    document="CISA_KEV_catalog_2023-11-22",
    section="Known Exploited Vulnerabilities",
    confidence=1.0,
    metadata={"publisher": "CISA", "mandatory_remediation": True},
)
prov.track_property_source("cve-2023-44487", "known_exploited", True, kev_ref)

# Incident response query: full history for this CVE
lineage = prov.get_lineage("cve-2023-44487")
print(f"CVE first seen  : {lineage['first_seen'][:10]}")
print(f"CVE last updated: {lineage['last_updated'][:10]}")
print(f"Update count    : {lineage['entity_count']} records")

# Integrity check before relying on the record for a patch decision
entries = prov.trace_lineage("cve-2023-44487")
for e in entries:
    ok = compute_checksum(e) == e.checksum
    print(f"  [{('OK' if ok else 'TAMPERED')}] {e.timestamp[:19]}  source={e.source_document}")
```

</Tab>

<Tab title="生命科学 — 临床/制药">

临床证据图谱追踪疗效数据从源文献、结构化抽取到监管申报的全过程。这条 W3C PROV-O 链满足 ICH E6(R2) GCP 对数据可追溯性的要求，也满足 21 CFR Part 11 对电子记录完整性的要求。申报材料中的每个实体都必须能追溯到源文档、抽取活动和操作者。

`track_property_source()` 在这里尤为重要：当两项独立研究对同一终点报告不同的疗效值时，每一条都必须连同完整引用元数据单独追踪。得到的多来源记录是荟萃分析的证据基础，这些溯源条目也成为监管申报档案中的支撑文件。

```python
from semantica.provenance import ProvenanceManager
from semantica.provenance.schemas import SourceReference
from semantica.provenance.integrity import compute_checksum

prov = ProvenanceManager(storage_path="clinical_provenance.db")

# Track the source document chunk (Phase III study report section)
prov.track_chunk(
    chunk_id="phase3_primary_endpoint_C4591001",
    source_document="STUDY_REPORT_BNT162b2_C4591001_MOD2",
    source_path="/submissions/EMA_rolling_review/mod2_clinical_overview.pdf",
    start_index=4096,
    end_index=6144,
    study_phase="Phase_III",
    ctgov="NCT04368728",
    sponsor="BioNTech_Pfizer",
)

# Track extracted efficacy entity with verbatim source quote
prov.track_entity(
    entity_id="VE_primary_BNT162b2_C4591001",
    source="phase3_primary_endpoint_C4591001",
    metadata={"value": "95.0%", "CI_95": "[90.3–97.6]", "label": "EFFICACY_MEASURE"},
    confidence=0.99,
    entity_type="clinical_endpoint",
    activity_id="structured_data_extraction",
    source_quote="Vaccine efficacy against COVID-19 was 95.0% (95% CI, 90.3–97.6)",
)

# Multi-study property tracking for meta-analysis
study1 = SourceReference(
    document="NEJM_doi_10.1056_NEJMoa2034577",
    page=9, section="Table 2",
    confidence=0.99,
    metadata={"study_id": "C4591001", "n_participants": 43448},
)
study2 = SourceReference(
    document="Lancet_doi_10.1016_S0140-6736_21_00448-7",
    page=6, section="Results",
    confidence=0.97,
    metadata={"study_id": "EXT_COHORT", "n_participants": 9119},
)
prov.track_property_source("BNT162b2", "vaccine_efficacy_symptomatic_covid19", "95.0", study1)
prov.track_property_source("BNT162b2", "vaccine_efficacy_symptomatic_covid19", "94.1", study2)

# Regulatory submission audit — evidence chain
lineage = prov.get_lineage("VE_primary_BNT162b2_C4591001")
print("Evidence chain for regulatory submission:")
for entry in lineage["lineage_chain"]:
    print(f"  {entry['timestamp'][:10]} | {entry['source_document'][:45]} | "
          f"agent={entry['agent_id']}")

# Integrity verification (21 CFR Part 11 requirement)
entries = prov.trace_lineage("VE_primary_BNT162b2_C4591001")
for e in entries:
    status = "OK" if compute_checksum(e) == e.checksum else "TAMPERED"
    print(f"  Integrity [{status}]: {e.entity_id}")

stats = prov.get_statistics()
print(f"\nTotal evidence records in dossier: {stats['total_entries']}")
```

</Tab>

<Tab title="银行业 — 风险/合规">

抵押贷款发放系统为每笔信贷决策记录完整溯源，满足 SR 11-7 模型风险管理指引和 EBA 模型文档要求。承保模型用到的每个特征——信用分、DTI 比率、房产估值——都必须能追溯到其源数据拉取、运行模型的操作者，以及决策时间戳。

房产估值经 `track_property_source()` 从两个来源追踪（RICS 评估和 AVM 自动估值），合规团队由此完整了解 LTV 如何计算、模型最终采信了哪种估值方法。

```python
from semantica.provenance import ProvenanceManager
from semantica.provenance.schemas import SourceReference

prov = ProvenanceManager(storage_path="credit_provenance.db")
app_id = "APP-2026-994421"

# Track the bureau data pull
prov.track_chunk(
    chunk_id=f"{app_id}_bureau_pull",
    source_document=f"EXPERIAN_CREDITEXPERT_{app_id}_2026-06-21",
    source_path=f"/bureau/experian/{app_id}/2026-06-21.json",
    start_index=0,
    end_index=4096,
    bureau="Experian",
    pull_timestamp="2026-06-21T09:14:32Z",
    consent_ref=f"CONSENT-{app_id}",
)

# Batch-track extracted credit features
features = [
    {"id": f"{app_id}_credit_score",         "confidence": 1.0, "value": 714},
    {"id": f"{app_id}_dti_ratio",             "confidence": 1.0, "value": 0.38},
    {"id": f"{app_id}_derogatory_count_7yr",  "confidence": 1.0, "value": 0},
]
prov.track_entities_batch(
    features,
    source=f"{app_id}_bureau_pull",
    entity_type="credit_feature",
    activity_id="bureau_parsing",
    agent_id="credit_data_service_v2",
)

# Track competing property valuations
rics_val = SourceReference(
    document=f"RICS_VALUATION_{app_id}_2026-06-18",
    page=3, section="Market Value Assessment",
    confidence=0.96,
    metadata={"valuer": "JLL_Residential", "method": "comparable_sales"},
)
avm_val = SourceReference(
    document=f"AVM_ESTIMATE_{app_id}_2026-06-21",
    confidence=0.84,
    metadata={"provider": "Hometrack_AVM", "model_version": "v8.3"},
)
prov.track_property_source(app_id, "property_value_GBP", "410000", rics_val)
prov.track_property_source(app_id, "property_value_GBP", "403500", avm_val)

# Track the underwriting decision itself
prov.track_entity(
    entity_id=f"DECISION_{app_id}",
    source=f"{app_id}_bureau_pull",
    metadata={"outcome": "approved_conditional_lmi", "model": "underwriting_model_v4"},
    confidence=0.89,
    entity_type="credit_decision",
    activity_id="automated_underwriting",
)

# SR 11-7 audit output
print("=== MODEL AUDIT TRAIL ===")
lineage = prov.get_lineage(f"DECISION_{app_id}")
for entry in lineage["lineage_chain"]:
    print(f"  [{entry['timestamp'][:19]}]  {entry['activity_id']}  agent={entry['agent_id']}")

print("\n=== PROPERTY VALUATION SOURCES ===")
for s in prov.get_all_sources(f"{app_id}_property_value_GBP"):
    print(f"  {s['source'][:55]}  conf={s['confidence']:.2f}")

stats = prov.get_statistics()
print(f"\nTotal audit records: {stats['total_entries']}  |  Sources: {stats['unique_sources']}")
```

</Tab>

</Tabs>

## W3C PROV-O 映射

每条 `ProvenanceEntry` 都直接映射到 W3C PROV-O 术语。如果你的合规团队或监管机构要求 PROV-O 导出，字段是一一对应的：

| PROV-O 术语 | `ProvenanceEntry` 字段 | 记录内容 |
| :--- | :--- | :--- |
| `prov:Entity` | `entity_id` | 被追踪对象——实体、分块、关系或属性 |
| `prov:Activity` | `activity_id` | 产出它的过程——`"ner_extraction"`、`"bureau_parsing"` |
| `prov:Agent` / `prov:Person` / `prov:SoftwareAgent` / `prov:Organization` | `agent_id`, `agent_type`, `is_automated` | 由谁——或什么——运行了该活动，以及是否有人直接担责 |
| `prov:qualifiedAssociation` + `prov:hadRole` | `role` | 执行者对该实体的具体角色——`"generator"`（默认）、`"approver"`、`"reviewer"`——用于签核/四眼工作流 |
| `prov:wasDerivedFrom` | `parent_entity_id`（旧版合并字段） | 此实体的先前版本或来源 |
| — | `previous_version_id` | 此条目修正/替换**同一**事实的先前版本 |
| `prov:wasDerivedFrom` | `derived_from_id` | 此条目派生自**另一个**来源实体 |
| `prov:used` | `used_entities` | 产出此条目所消耗的实体 ID |
| `prov:generatedAtTime` | `timestamp` | ISO 日期时间，写入时自动设为 `utc_now_iso()` |
| `prov:qualifiedInvalidation` | `invalidated`, `invalidated_at_time`, `invalidated_by`, `invalidation_reason` | 经 `ProvenanceManager.invalidate()` 以墓碑记录形式登记的撤回/更正，从不硬删除 |
| `prov:startedAtTime` / `prov:endedAtTime` | `activity_started_at_time`, `activity_ended_at_time` | 类型化 Activity 计时——经 `activity=` 关键字参数传入 `ActivityRecord`，可与 `activity_id` 一起设置 |
| `prov:qualifiedGeneration`/`Generation`, `qualifiedUsage`/`Usage`, `qualifiedDerivation`/`Derivation` | （由上述字段派生） | `wasGeneratedBy`/`used`/`wasDerivedFrom` 的附加限定形式，随普通三元组自动产出 |
| `prov:wasAssociatedWith` | （由 `agent_id` 派生） | Activity→Agent 直接链接，区别于 Entity→Agent 的 `wasAttributedTo` |
| `prov:actedOnBehalfOf` | `acted_on_behalf_of` | Agent→Agent 委托——例如自动化智能体代表授权它的人类/组织行事 |
| `prov:wasInformedBy` | `informed_by_activities`（经 `informed_by=[...]` 传入） | 把本条目的活动链接到它所依据的先前活动（例如流水线中的前一个阶段） |
| `prov:Bundle` + `prov:hadMember` | `bundle_id` | 按来源/数据集/摄取运行对条目分组（成员关系三元组，并非真正的 RDF 命名图分区） |
| — | `valid_from`, `valid_until`, `revision_type`, `supersedes` | 自弃用的 `kg.ProvenanceTracker` 合并而来的双时间维度字段——始终由调用方提供（从不自动计算），经 `ProvenanceManager.revision_history()` 呈现；未显式设置的条目回退为按时间戳推导 |

`previous_version_id` 和 `derived_from_id` 是在 `parent_entity_id` 之外新增的——读取 `parent_entity_id` 的现有代码行为不变，新代码则能用这两个关系消除歧义。

`checksum` 字段不属于 PROV-O 标准——它是 Semantica 的防篡改扩展。现在每条条目的 SHA-256 还会并入 `previous_checksum`（按 `sequence_id` 插入顺序取上一条目的校验和），把每条条目与其前一条链接起来。`ProvenanceManager.verify_chain()` 会走完整条链并报告任何断点——包括从底层表中硬删除的行，仅靠单行校验和是检测不到这种删除的。

注意：上面的银行示例向 `track_entities_batch()` 传入了 `agent_id="credit_data_service_v2"`——现在它确实会填充条目的 `agent_id` 字段（此前有个 bug：`agent_id`/`entity_type`/`activity_id` 这类批量级类型化关键字参数被静默吸进了不透明的 `metadata` 块里）。

`export_prov()` 在 `ProvenanceManager.DEFAULT_BASE_URI` 下铸造实体/智能体/活动 URI（默认为 `https://semantica.dev/ns#`——`RDFExporter` 的 `NamespaceManager` 为其 `"semantica"` 前缀使用的正是同一命名空间，因此同一 `entity_id` 的 KG 导出 URI 与 PROV 导出 URI 可以协同解析），除非通过 `export_prov(base_uri=...)` 或 CLI 的 `--base-uri` 选项另行覆盖。

## 延伸阅读

- [语义抽取](./semantic-extraction.md) — 自动为每个抽取出的实体生成溯源条目的 NER 与关系抽取流水线
- [冲突消解](./conflict-resolution.md) — 溯源属性来源直接汇入冲突检测；每个消解后的值都可追溯到其来源
- [去重](./deduplication.md) — 合并操作会记入合并历史；与溯源配合，可得从来源到规范实体的完整血缘
- [溯源参考](../reference/provenance.md) — 完整的存储后端 API、`InMemoryStorage`、`SQLiteStorage` 与 `ProvenanceEntry` 模式
