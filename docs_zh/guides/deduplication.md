---
title: "去重与实体合并"
description: "用多因子相似度检测重复实体，用可配置策略合并它们，让知识图谱在规模化之下保持干净。"
source: guides/deduplication.md
source_version: 841a72783fb59d8f69de1b4bcac498741c53cbee
---

## 什么是去重？

去重(Deduplication)是识别那些指向同一个真实世界对象、却在数据里各占一条记录的实体，并把它们合并为单一规范表示的过程。数据来自多个来源时，别名、拼写变体和格式差异在所难免，这一过程正是为了消解它们。

**去重的关键概念：**

**规范实体(Canonical Entity)** 是合并所有重复记录后，某个真实世界对象的唯一权威表示。知识图谱里所有关系都指向这个规范实体节点。

**别名(Alias)** 是同一实体的其他名称或标识符。例如 "APT29"、"Cozy Bear"、"Midnight Blizzard" 指向的都是同一个威胁行为者。

**实体消解(Entity Resolution)** 是更宏观的过程：判定不同记录是否指向同一实体，涵盖相似度计算、重复检测和合并等步骤。

**相似度算法：**
- **Jaro-Winkler** 度量字符串相似度，对共享前缀给更高分，适合开头部分相同的名称
- **Levenshtein** 距离统计把一个字符串变成另一个所需的字符编辑次数，擅长发现错字和变体

**聚类(Clustering)** 用并查集(Union-Find)等算法把相互关联的重复项归为一组：只要 A 匹配 B、B 匹配 C，即使 A 和 C 不直接匹配，三者也会归入同一组。

## 为什么要用去重？

**数据质量与一致性。** 消除重复节点——它们割裂关系，还让同一实体因名称不同而给出不一致的查询结果。

**准确的分析与指标。** 实体不再因命名变体散落在多个节点上，计数、中心性(centrality)和关系分析才能准确。

**关系归并。** 把散落的关系合并到单一规范实体上，完整分析连接与模式——数据碎片化时这些模式就会漏掉。

**多源集成。** 把来自多个源、系统和数据库的数据无缝合并——同一实体在其中往往以不同标识符和命名约定出现。

**图效率。** 消除冗余节点以缩小图规模、提升查询性能，同时靠恰当的合并策略保住全部信息。

**溯源(Provenance)保留。** 维护完整审计轨迹，记录最终规范实体的每一条信息来自哪个源。

## 适用与不适用场景

**去重适用于：**
- 多源数据集成，实体在不同源里名称或标识符不同
- 易出现别名和变体的实体类型（组织、人物、产品、地理位置）
- 关系准确性依赖实体归并的知识图谱
- 需要规范实体管理的数据质量工作流
- 需要准确实体计数和关系指标的分析
- 同一真实世界对象出现在多个系统或数据库中的场景

**以下情况不要用去重：**
- 标识符和命名约定一致的单源数据
- 去重延迟不可接受的高吞吐流式场景
- 有可靠主键、设计上就不可能有重复的数据
- 需要把实体变体保留为独立节点的情况（不同产品版本、按时间区分的实体状态）
- 基本数据库约束就能保证唯一性的简单精确匹配场景

**以下情况要谨慎：**
- 大数据集，O(n²) 两两比较计算开销大
- 已有确定性主键（LEI、CVE-ID、ISIN）时仍用模糊匹配
- 过低的相似度阈值，可能把真正不同的实体合并掉

## 典型工作流

去重工作流从检测到合并遵循一套系统化流程：

**1. 检测** → 用 `detect_duplicates()` 或 `DuplicateDetector` 以多因子相似度(multi-factor similarity)评分找出潜在匹配

**2. 分组** → 用聚类算法把传递相关的重复项收进组（A 匹配 B，B 匹配 C → A、B、C 成组）

**3. 选定规范实体** → 依据完整度、来源权威性或置信度分数，为每组选出代表实体

**4. 合并** → 用 `keep_most_complete` 或 `merge_all` 等策略合并重复实体，同时保留溯源

**5. 校验** → 检查合并结果，依据精确率/召回率分析调整阈值或策略

**6. 更新图** → 用规范实体替换重复节点，并转移全部关系

这条流水线把碎片化的多源数据变成干净、归并的知识图谱，可直接用于分析与推理。

## API 模式：函数式与类式

Semantica 为不同用例同时提供简单函数包装器和完备的类 API：

**简单工作流用函数包装器：**
- `detect_duplicates()` — 一次调用完成重复检测，配置最少
- `calculate_similarity()` — 比较两个实体，给出详细的相似度分解
- `merge_entities()` — `merge_duplicates()` 的便捷包装，用于快速合并

**复杂工作流用类 API：**
- `DuplicateDetector` — 可配置的重复检测，支持聚类、增量处理和高级相似度选项
- `EntityMerger` — 精细合并，多种策略、溯源追踪与合并历史

**使用准则：**
- 手头是原始实体集合、需要自动重复检测时，用 `merge_duplicates()`
- 已经知道哪些实体是重复项、只需合并既定分组时，用 `merge_entity_group()`
- 不要在同一工作流里混用函数包装器和类 API——选定一种方式，贯彻到底

去重模块用六种互补的相似度算法——精确匹配、Levenshtein、Jaro-Winkler、余弦、属性比较和向量嵌入(Embedding)——检测多源知识图谱中的重复实体，然后把它们合并为单一规范实体，同时保留完整溯源。在跑图分析或冲突消解(Conflict Resolution)之前，先用它把别名簇（如 "APT29"、"Cozy Bear"、"Midnight Blizzard"）折叠起来。

<Info>
在摄取之后、冲突消解之前运行去重。去重把重复节点折叠为一个规范实体；冲突消解随后再调和该规范实体上相互矛盾的属性值。流水线顺序很重要：先去重，再消解冲突，最后用 SHACL 校验。
</Info>

## 第一次扫描：找到重复项

小数据集上做直接的重复检测，从 `detect_duplicates()` 开始。把实体交给它，两两比较算法会用多重相似度信号比较每一对。

**规模提示：** 几千个节点的数据集，几秒就能跑完。O(n²) 两两比较的成本要到一万个实体以上才成为问题——更大的集合见下文聚类一节。

```python
from semantica.deduplication import detect_duplicates

# 从四个不同 CTI 源摄取的威胁行为者——同一批行为者，名字各异
threat_actors = [
    {"id": "ta-nvd-001",  "name": "APT29",            "type": "ThreatActor",
     "country": "Russia",  "source": "MISP"},
    {"id": "ta-of-002",   "name": "APT-29",            "type": "ThreatActor",
     "country": "Russia",  "source": "OpenCTI"},
    {"id": "ta-rf-003",   "name": "Cozy Bear",         "type": "ThreatActor",
     "aliases": ["APT29"], "country": "Russia", "source": "RecordedFuture"},
    {"id": "ta-sx-004",   "name": "The Dukes",         "type": "ThreatActor",
     "aliases": ["APT29", "Cozy Bear"], "country": "Russia", "source": "STIX-partner"},
    {"id": "ta-ms-005",   "name": "Midnight Blizzard", "type": "ThreatActor",
     "aliases": ["NOBELIUM", "APT29"], "country": "Russia", "source": "Microsoft"},
    {"id": "ta-ap-006",   "name": "APT28",             "type": "ThreatActor",
     "country": "Russia",  "source": "MISP"},  # 不同的行为者——不应匹配
]

candidates = detect_duplicates(
    threat_actors,
    method="pairwise",          # 两两比较
    similarity_threshold=0.6,   # 判为候选的最低分
    confidence_threshold=0.5,   # 匹配置信度的下限
)

for c in candidates:
    print(f"{c.entity1['name']!r}  ~  {c.entity2['name']!r}")
    print(f"  similarity={c.similarity_score:.2f}  confidence={c.confidence:.2f}")
    print(f"  signals: {c.reasons}")
    print()
```

```text
'APT29'  ~  'APT-29'
  similarity=0.89  confidence=0.81
  signals: ['levenshtein', 'jaro_winkler']

'APT29'  ~  'Cozy Bear'
  similarity=0.63  confidence=0.71
  signals: ['property', 'relationship']   # alias field matched

'Cozy Bear'  ~  'The Dukes'
  similarity=0.61  confidence=0.68
  signals: ['property']                   # shared alias "APT29"

'APT29'  ~  'Midnight Blizzard'
  similarity=0.65  confidence=0.73
  signals: ['property']                   # alias "APT29" in Midnight Blizzard record
```

这些分数讲了个清楚的故事。"APT29" 和 "APT-29" 得分 0.89——只差一个连字符，字符串相似度信号很强。"Cozy Bear" 和 "The Dukes" 得分较低（0.61），因为名字完全不同，但属性信号触发了——两条记录的别名列表里都带着 `"APT29"`。"APT28" 从未出现在结果里，因为它只共享国家字段——不足以越过 0.6 的阈值。

## 理解候选对象

每个 `DuplicateCandidate` 携带两个实体、它们的相似度得分，以及一份详细分解：哪些相似度算法对这次匹配做出了贡献。审计和阈值调优因此有据可查：

```python
from semantica.deduplication import calculate_similarity

# 在提交合并之前，详细检查单对实体
e1 = threat_actors[0]   # APT29
e2 = threat_actors[2]   # Cozy Bear

result = calculate_similarity(e1, e2, method="multi_factor")

print(f"Overall score : {result.score:.2f}")
print(f"Method        : {result.method}")
print(f"Components    :")
for algo, score in result.components.items():
    print(f"  {algo:<20} {score:.2f}")
```

```text
Overall score : 0.63
Method        : multi_factor
Components    :
  exact                0.00   # names are completely different strings
  levenshtein          0.12   # high edit distance between "APT29" and "Cozy Bear"
  jaro_winkler         0.21   # no shared prefix
  property             0.94   # alias match is nearly definitive
  relationship         0.71   # share relationships to overlapping malware families
  embedding            0.78   # semantic vectors land in the same cluster
```

这里的分数大头来自属性分量（0.94）。"Cozy Bear" 的记录带着 `aliases: ["APT29"]`，这几乎确凿地表明两个实体指向同一个威胁行为者。看到这种模式——名字相似度弱但属性匹配强——通常面对的就是真正的别名关系，而不是误报。

## 合并前先分组

小数据集可以直接合并候选对。更大的图里，同一实体可能以六个名字散布在十二个源中，这时要用并查集聚类做重复分组。这样能保证：只要 A 匹配 B、B 匹配 C，即使 A 和 C 不直接达到相似度阈值，三个实体也会归为一组：

```python
from semantica.deduplication import DuplicateDetector, EntityMerger

detector = DuplicateDetector(
    similarity_threshold=0.6,
    confidence_threshold=0.5,
    use_clustering=True,      # 启用并查集分组
)

groups = detector.detect_duplicate_groups(threat_actors)

print(f"Found {len(groups)} duplicate groups:")
for group in groups:
    names = [e["name"] for e in group.entities]
    print(f"  Group (confidence={group.confidence:.2f}): {names}")
    if group.representative:
        print(f"  Representative: {group.representative['name']!r}")
```

```text
Found 2 duplicate groups:
  Group (confidence=0.74): ['APT29', 'APT-29', 'Cozy Bear', 'The Dukes', 'Midnight Blizzard']
  Representative: 'APT29'   # highest completeness score in the group

  Group (confidence=0.81): ['APT28', 'Fancy Bear']
  Representative: 'APT28'
```

分组结果把归并展示得清清楚楚：五个独立节点本该是一个规范实体。`representative` 字段标出合并器将用作基准的实体——通常是属性集最完整的那个，这里就是来自 MISP 源的 "APT29"。

## 合并：折叠分组而不丢数据

识别出重复分组后，合并过程把它们归并为规范实体。`keep_most_complete` 策略选属性数最多的实体作为规范节点，并用其他源补齐缺失字段：

```python
merger = EntityMerger(preserve_provenance=True)

for group in groups:
    if len(group.entities) < 2:
        continue

    # merge_entity_group() 会跳过重复检测，因为 group.entities
    # 已经是 detect_duplicate_groups() 确认过的分组
    op = merger.merge_entity_group(group.entities, strategy="keep_most_complete")

    canonical = op.merged_entity
    source_ids = [e["id"] for e in op.source_entities]
    print(f"Merged {len(op.source_entities)} entities → canonical: {canonical['name']!r}")
    print(f"  Source IDs retired : {source_ids}")
    print(f"  Merge strategy     : {op.merge_result.metadata.get('strategy')}")
```

```text
Merged 5 entities → canonical: 'APT29'
  Source IDs retired : ['ta-nvd-001', 'ta-of-002', 'ta-rf-003', 'ta-sx-004', 'ta-ms-005']
  Merge strategy     : keep_most_complete
```

五个源实体被一个规范表示取代。这五个节点承载的所有关系——指向战役、恶意软件家族、TTP、基础设施——现在都挂在规范节点 "APT29" 上。合并操作在消除冗余的同时保住了全部信息，溯源记录则精确显示每个属性来自哪个源。

## 审计：复查合并历史

批量合并之后，可以取回完整历史，逐条复查每个合并决定。这条审计轨迹对理解合并决策、向利益相关方解释必不可少：

```python
history = merger.get_merge_history()

print(f"Total merge operations: {len(history)}")
for op in history:
    print(f"  {op.merged_entity['name']!r} ← {len(op.source_entities)} sources")
    print(f"    strategy: {op.merge_result.metadata.get('strategy')}")
```

这段历史让合并决策完全透明。当某个源的数据负责人问"我的实体为什么并进了另一个实体"，你手里有成文的证据和理由。

## 流式摄取：增量去重

流水线处理持续数据流——比如每小时都有新威胁情报到达——时，你不会想对每个批次都把整张图重新做两两比较。用增量检测，只把新实体与既有规范集合比较：

```python
# 既有图实体（已去重）
existing_actors = [
    {"id": "ta-nvd-001", "name": "APT29", "type": "ThreatActor", "country": "Russia"},
]

# 新源到达的一批数据
new_batch = [
    {"id": "ta-new-007", "name": "NOBELIUM",      "type": "ThreatActor",
     "aliases": ["APT29"], "country": "Russia", "source": "MSTIC-2026-06"},
    {"id": "ta-new-008", "name": "Scattered Spider", "type": "ThreatActor",
     "country": "Unknown",  "source": "CrowdStrike"},
]

incremental = detector.incremental_detect(new_batch, existing_actors)

print(f"New duplicates found in this batch: {len(incremental)}")
for c in incremental:
    print(f"  {c.entity1['name']!r} matches existing {c.entity2['name']!r}")
    print(f"  score={c.similarity_score:.2f}")
```

```text
New duplicates found in this batch: 1
  'NOBELIUM' matches existing 'APT29'
  score=0.67        # alias field carries "APT29" — property signal fires
```

NOBELIUM 会被排入队列，与既有的 APT29 规范实体合并。Scattered Spider 对所有既有行为者的得分都低于阈值，于是作为新的唯一节点加入图。

## 扩展到大规模实体集

节点数超过一万后，两两比较因 O(n²) 复杂度变得计算昂贵。用 `build_clusters()` 跑更高效的向量化批量比较，再对每个聚类分别合并：

**性能警告：** 务必先在有代表性的数据规模上剖析相似度操作。1,000 个实体时可行的做法，到 10,000 个以上若无相应的扩展策略，可能慢得无法接受。

```python
from semantica.deduplication import build_clusters

# 来自 NVD、Vulhub 和厂商源的 1 万个 CVE 实体
# （未展示——假设 all_vulns 是 1 万多条 dict 组成的列表）

cluster_result = build_clusters(
    all_vulns,
    method="graph_based",        # 相似度图上跑并查集
    similarity_threshold=0.75,
)

print(f"Clusters found   : {len(cluster_result.clusters)}")
print(f"Unclustered      : {len(cluster_result.unclustered)}")
print(f"Quality metrics  : {cluster_result.quality_metrics}")

# 逐簇合并
merger = EntityMerger(preserve_provenance=True)
for cluster in cluster_result.clusters:
    if len(cluster.entities) > 1:
        # 用 merge_entity_group()，聚类已判定它们是重复项
        merger.merge_entity_group(cluster.entities, strategy="keep_most_complete")
```

更大的集合换 `method="hierarchical"`：凝聚式自底向上聚类，可扩展到几十万实体，代价是损失一些精度。

## 简单示例：客户去重

在进入领域专属案例之前，先走一个直白的客户去重场景。某公司 CRM 系统里积累了来自网页注册、销售录入和支持工单的重复客户记录：

```python
from semantica.deduplication import detect_duplicates, merge_entities

customers = [
    {"id": "cust-001", "name": "John Smith", "email": "john.smith@email.com", 
     "company": "Acme Corp", "source": "web_signup"},
    {"id": "cust-002", "name": "J. Smith", "email": "john.smith@email.com",
     "company": "Acme Corporation", "source": "sales_team"},
    {"id": "cust-003", "name": "John Smith", "phone": "+1-555-0123",
     "company": "Acme Corp", "source": "support_ticket"},
    {"id": "cust-004", "name": "Jane Doe", "email": "jane.doe@email.com",
     "company": "Beta Inc", "source": "web_signup"},
]

# 第一步：找出潜在重复
candidates = detect_duplicates(
    customers,
    method="pairwise",
    similarity_threshold=0.6,  # 要求 60% 相似度
    confidence_threshold=0.5,
)

print("Potential duplicates found:")
for c in candidates:
    print(f"  {c.entity1['name']} ~ {c.entity2['name']} (score: {c.similarity_score:.2f})")
    print(f"    Matching signals: {c.reasons}")

# Expected output:
# John Smith ~ J. Smith (score: 0.82)
#   Matching signals: ['exact', 'property']  # same email
# John Smith ~ John Smith (score: 0.78)  
#   Matching signals: ['exact', 'property']  # same name and company

# 第二步：合并重复项
john_smith_records = [customers[0], customers[1], customers[2]]  # John Smith 的全部变体
merged_ops = merge_entities(john_smith_records, method="keep_most_complete")

for op in merged_ops:
    canonical = op.merged_entity
    print(f"\nCanonical customer: {canonical['name']}")
    print(f"  Email: {canonical.get('email', 'N/A')}")
    print(f"  Phone: {canonical.get('phone', 'N/A')}")
    print(f"  Company: {canonical['company']}")
    print(f"  Merged from {len(op.source_entities)} records")
    
# 结果：一条 John Smith 记录，带有来自全部三条原始记录的
# 邮箱、电话和公司信息，并带完整溯源追踪
```

这个示例演示了核心概念：相似度检测找出相关记录，合并把它们归并为保留全部可用信息的规范实体。

## 常见陷阱

**调阈值不做验证。** 阈值设得太低，会把真正不同的实体错误合并。大规模合并之前，务必人工抽查一部分检出结果。

**两两比较的扩展问题。** 逐一比较每对实体的 O(n²) 成本在实体过万后难以承受。大数据集改用聚类方法（`build_clusters`）或向量化相似度。

**有主键还用模糊匹配。** 实体有可靠唯一标识（LEI 代码、CVE ID、ISBN 号）时，直接在这些字段上做精确匹配，不要用计算昂贵的相似度算法。

**函数式与类式 API 混用。** 不要调了 `detect_duplicates()` 又手动实例化 `EntityMerger`——函数式或类式二选一，整个工作流保持一致。

**忽视合并策略的影响。**`keep_first` 会完全覆盖后来的记录，`merge_all` 可能引入冲突值，`keep_most_complete` 可能不尊重来源权威。按你的数据质量要求选策略。

**跳过溯源追踪。** 没有 `preserve_provenance=True`，就看不到规范实体每个字段来自哪个源，审计轨迹无从谈起。

**相似度算法选择不当。** 纯字符串相似度对付别名关系会失效（"APT29" 对 "Cozy Bear"），而属性匹配对"共享属性但身份不同"的实体可能过于激进。

## 领域示例

<Tabs>

<Tab title="国防 — 威胁情报">

威胁情报平台从 Mandiant、CrowdStrike、MITRE ATT&CK 和合作 ISAC 源摄取行为者档案。同一批行为者以各厂商的叫法出现："Cozy Bear"（CrowdStrike）、"APT29"（MITRE）、"Midnight Blizzard"（Microsoft）、"The Dukes"（F-Secure）。任何分析师查询跑起来之前，这些别名必须先折叠为单一规范节点，让关系——使用过的恶意软件、运营过的基础设施、归因过的战役——都挂到一处。

别名字段是这里的关键信号。只要任何记录的 `aliases` 列表带有规范名称，基于属性的相似度就会强烈触发。设一个适中阈值（0.6），能抓住单靠名字相似度会漏掉的别名匹配。

```python
from semantica.deduplication import DuplicateDetector, EntityMerger

actors = [
    {"id": "ta-cs-001",  "name": "Cozy Bear",         "type": "ThreatActor",
     "aliases": ["APT29", "The Dukes"],  "country": "Russia", "source": "CrowdStrike"},
    {"id": "ta-mt-002",  "name": "APT29",              "type": "ThreatActor",
     "aliases": [],                       "country": "Russia", "source": "MITRE"},
    {"id": "ta-ms-003",  "name": "Midnight Blizzard",  "type": "ThreatActor",
     "aliases": ["NOBELIUM", "APT29"],   "country": "Russia", "source": "Microsoft"},
    {"id": "ta-fs-004",  "name": "The Dukes",          "type": "ThreatActor",
     "aliases": ["APT29", "Cozy Bear"],  "country": "Russia", "source": "F-Secure"},
    {"id": "ta-mt-005",  "name": "APT28",              "type": "ThreatActor",
     "aliases": ["Fancy Bear"],           "country": "Russia", "source": "MITRE"},
]

detector = DuplicateDetector(similarity_threshold=0.6, confidence_threshold=0.5)
groups = detector.detect_duplicate_groups(actors)

merger = EntityMerger(preserve_provenance=True)
for group in groups:
    if len(group.entities) < 2:
        continue
    ops = merger.merge_duplicates(group.entities, strategy="keep_most_complete")
    for op in ops:
        feeds = [e["source"] for e in op.source_entities]
        print(f"Canonical: {op.merged_entity['name']!r}  (merged from: {feeds})")
        # Canonical: 'APT29'  (merged from: ['CrowdStrike', 'MITRE', 'Microsoft', 'F-Secure'])
        # All four actor nodes collapse to one — every relationship they held now
        # attaches to the canonical APT29 node.
```

</Tab>

<Tab title="安全 — SOC/事件响应">

SOC 漏洞管理数据库从 NVD、Vulhub、CISA KEV 和厂商通告摄取 CVE。同一条 CVE 常常以 "CVE-2024-3400"（NVD）、"PAN-OS GlobalProtect RCE"（Tenable 插件）、"Critical PAN-OS 0day"（博客聚合）三种面目到达。光靠名字相似度匹配不上——`cve_id` 字段里的 CVE ID 才是决定性信号。

```python
from semantica.deduplication import detect_duplicates, merge_entities

vulns = [
    {"id": "v-nvd-001",  "name": "CVE-2024-3400",
     "description": "PAN-OS GlobalProtect command injection RCE",
     "cvss": 10.0, "source": "NVD",      "type": "Vulnerability"},
    {"id": "v-cisa-002", "name": "CVE-2024-3400",
     "description": "Critical PAN-OS vulnerability in active exploitation",
     "cvss": 10.0, "source": "CISA-KEV", "type": "Vulnerability"},
    {"id": "v-ten-003",  "name": "PAN-OS GlobalProtect RCE",
     "cve_id": "CVE-2024-3400",
     "cvss": 10.0, "source": "Tenable",  "type": "Vulnerability"},
    {"id": "v-nvd-004",  "name": "CVE-2023-44487",
     "description": "HTTP/2 Rapid Reset DDoS amplification",
     "cvss": 7.5,  "source": "NVD",      "type": "Vulnerability"},
]

# 阈值设低，因为 "CVE-2024-3400" 与
# "PAN-OS GlobalProtect RCE" 的名字相似度接近零——需要属性信号来补
candidates = detect_duplicates(
    vulns,
    method="pairwise",
    similarity_threshold=0.5,
    confidence_threshold=0.4,
)

for c in candidates:
    print(f"{c.entity1['name']!r}  ~  {c.entity2['name']!r}")
    print(f"  score={c.similarity_score:.2f}  signals={c.reasons}")
    # 'CVE-2024-3400'  ~  'PAN-OS GlobalProtect RCE'
    #   score=0.61  signals=['property', 'exact']   # cve_id field match

# 合并三个 CVE-2024-3400 变体
cve_group = [v for v in vulns if "3400" in v["name"] or v.get("cve_id") == "CVE-2024-3400"]
ops = merge_entities(cve_group, method="keep_most_complete", preserve_provenance=True)
for op in ops:
    print(f"Canonical CVE: {op.merged_entity['name']}  CVSS={op.merged_entity.get('cvss')}")
    # Canonical CVE: CVE-2024-3400  CVSS=10.0
    # One node now carries all three source records' provenance.
```

</Tab>

<Tab title="生命科学 — 临床/制药">

临床试验知识图谱从 WHO INN 目录、PubChem、商品名数据库和试验注册库摄取药物实体。华法林以 "warfarin"（INN）、"Coumadin"（商品名，百时美施贵宝）、"warfarin sodium"（PubChem 化学形式）和 "81-81-2"（CAS 号）出现。CAS 号是金标准——两条记录共享 CAS 号，无论叫什么名字都是同一化合物。

```python
from semantica.deduplication import DuplicateDetector, EntityMerger, calculate_similarity

compounds = [
    {"id": "c-inn-001", "name": "warfarin",         "type": "Drug",
     "cas": "81-81-2",   "source": "WHO-INN"},
    {"id": "c-bms-002", "name": "Coumadin",         "type": "Drug",
     "cas": "81-81-2",   "source": "BMS-brand"},
    {"id": "c-pc-003",  "name": "warfarin sodium",  "type": "Drug",
     "source": "PubChem"},                            # 无 CAS——记录不够完整
    {"id": "c-inn-004", "name": "metoprolol",       "type": "Drug",
     "cas": "37350-58-6","source": "WHO-INN"},
    {"id": "c-nov-005", "name": "Lopressor",        "type": "Drug",
     "cas": "37350-58-6","source": "Novartis-brand"},
]

# property 方法给 CAS 号匹配打出极高的分数
sim = calculate_similarity(compounds[0], compounds[1], method="property")
print(f"warfarin vs Coumadin: {sim.score:.2f}")
# warfarin vs Coumadin: 0.91  — CAS match dominates

detector = DuplicateDetector(similarity_threshold=0.6, confidence_threshold=0.5)
groups = detector.detect_duplicate_groups(compounds)

merger = EntityMerger(preserve_provenance=True)
for group in groups:
    if len(group.entities) < 2:
        continue
    ops = merger.merge_duplicates(group.entities, strategy="keep_most_complete")
    for op in ops:
        print(f"Canonical: {op.merged_entity['name']!r}  CAS={op.merged_entity.get('cas')}")
        print(f"  Sources: {[e['source'] for e in op.source_entities]}")
        # Canonical: 'warfarin'  CAS=81-81-2
        #   Sources: ['WHO-INN', 'BMS-brand', 'PubChem']
        # All three warfarin records merge; WHO-INN record wins as most complete.
```

</Tab>

<Tab title="银行 — 风控/合规">

风控系统在构建交易对手敞口图之前，先跨 CRM、KYC 和交易系统归并企业客户。法定实体标识符(Legal Entity Identifier，LEI)是决定性标识——一个 20 字符的 ISO 17442 代码，全球唯一标识每个法人实体。两条记录共享 LEI，无论名字怎么写都是同一法人。

三条 BlackRock 记录——"BlackRock Inc."（CRM）、"BlackRock, Inc."（KYC，带逗号）、"Blackrock"（交易系统，小写 b）——必须在信贷敞口汇总之前折叠为一个规范交易对手。属性相似度方法给 LEI 匹配打出接近 1.0 的分数，即使名字相似度一般也能处理。

```python
from semantica.deduplication import build_clusters, EntityMerger

clients = [
    {"id": "crm-001", "name": "BlackRock Inc.",           "type": "Client",
     "lei": "549300HLPTRASHS0E726", "source": "CRM"},
    {"id": "kyc-001", "name": "BlackRock, Inc.",          "type": "Client",
     "lei": "549300HLPTRASHS0E726", "source": "KYC"},
    {"id": "trd-001", "name": "Blackrock",                "type": "Client",
     "lei": "549300HLPTRASHS0E726", "source": "TradeOps"},
    {"id": "crm-002", "name": "Vanguard Group",           "type": "Client",
     "lei": "549300IH7BVXP9VN3J07", "source": "CRM"},
    {"id": "kyc-002", "name": "The Vanguard Group, Inc.", "type": "Client",
     "lei": "549300IH7BVXP9VN3J07", "source": "KYC"},
]

cluster_result = build_clusters(
    clients,
    method="graph_based",
    similarity_threshold=0.65,   # 仅 LEI 匹配的得分就高于此值
)

merger = EntityMerger(preserve_provenance=True)
for cluster in cluster_result.clusters:
    if len(cluster.entities) < 2:
        continue
    ops = merger.merge_duplicates(cluster.entities, strategy="keep_most_complete")
    for op in ops:
        sources = [e["source"] for e in op.source_entities]
        print(f"Canonical: {op.merged_entity['name']!r}  (from {sources})")
        # Canonical: 'BlackRock Inc.'  (from ['CRM', 'KYC', 'TradeOps'])
        # Canonical: 'Vanguard Group'  (from ['CRM', 'KYC'])

print(f"\nBefore: {len(clients)} client records")
print(f"After : {len(cluster_result.clusters)} canonical counterparties")
print(f"Quality: {cluster_result.quality_metrics}")
```

</Tab>

</Tabs>

## 选择合适的阈值

相似度阈值控制灵敏度。从 0.7 起步，先看误报再调整：

- **0.95 及以上** — 只匹配近乎相同的字符串。用于代码和 ID（LEI、CAS、CVE-ID），前提是名字格式在各源之间一致。
- **0.80–0.95** — 能抓住排版变体："Apple Inc." 对 "Apple, Inc."、"BlackRock" 对 "BlackRock Inc."
- **0.65–0.80** — 能抓住缩写和简称。组织名在各源里长短形式并存时必需。
- **0.50–0.65** — 语义相似度区间。需要属性或嵌入信号弥补名字相似度的不足。别名匹配用这个区间：名字完全不同、指向同一实体的字符串。

## 选择合并策略

| 策略 | 适用场景 |
| :--- | :--- |
| `keep_most_complete` | 没有指定的权威源；最大化信息密度。默认选择。 |
| `keep_first` | 第一个源是黄金记录(golden record)系统（MDM、LEI 注册库），其数据绝不能被覆盖。 |
| `keep_highest_confidence` | 实体自带显式置信度分数，且你信任它作为质量信号。 |
| `merge_all` | 想要所有属性的超集；只要之后会跑冲突消解来调和分歧，就可以接受。 |

## 相关指南

- [摄取一切](./ingest.md) — 多源摄取制造了本模块要解决的重复项
- [上下文图](./context-graphs.md) — 把去重后的实体直接存入知识图谱
- [冲突消解](./conflict-resolution.md) — 合并之后，调和规范实体上相互矛盾的属性值
- [溯源](./provenance.md) — 追踪合并血缘，让每个规范实体都能回溯到原始来源
- [流水线](./pipeline.md) — 把摄取、去重和存储串成 `PipelineBuilder` 工作流
