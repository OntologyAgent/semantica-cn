---
title: 本体管理
description: 从知识图谱生成 OWL 本体，校验类层级，推断属性，并导出为 Turtle、RDF/XML 或 JSON-LD。
source: guides/ontology.md
source_version: ef379e285ef28246dc515425038d8de0888fbe25
---

`OntologyGenerator` 直接从知识图谱中已有的实体和关系推导出正式的网络本体语言(OWL)本体(Ontology)——无需预先设计模式(Schema)。你可以用它为图谱的类(Class)和属性(Property)生成一份机器可读的契约，再导出为 Turtle、OWL/XML 或 JSON-LD，供 SHACL 校验、推理引擎和 STIX/TAXII 工具链使用。

## 什么是本体？

一句话点破：本体就是给你的知识图谱(Knowledge Graph)定下一套公认的词汇表——声明清楚存在哪些类型的事物、它们之间能有什么关系。正式地说，本体(Ontology)是对某个领域中概念与关系的形式化规范。它通过以下声明为知识图谱定义共享词汇：

**类(Class)** —— 你所在领域中的实体类型。例如网络安全领域的 `ThreatActor`、`Vulnerability` 或 `Software`。类描述世界上存在哪些种类的事物。

**对象属性(Object Properties)** —— 实体之间的关系。例如 `exploits`（威胁行为者利用漏洞）、`targets`（恶意软件攻击组织）、`uses`（行为者使用工具）。

**数据属性(Datatype Properties)** —— 带字面值的特征。例如 `name`（文本）、`severity_score`（小数）、`published_date`（日期）或 `ip_address`（字符串）。

本体指明哪些关系合法、每个属性能取什么类型的值、概念之间如何形成层级，从而让知识图谱变得机器可读。

## 为什么使用本体？

**一致性。** 没有本体时，同一个概念可能一个团队写成 "Threat_Actor"，另一个团队写成 "ThreatActor"。本体强制统一的命名约定。

**校验。** 本体让自动检查成为可能——这条关系合理吗？`Vulnerability` 的 CVSS 分数该存成文本还是数字？

**推理。** 导出为 OWL/Turtle 后，外部推理引擎（HermiT、Pellet、ELK）可以推断出新事实。如果 `Malware` 是 `Software` 的子类，而 HAMMERTOSS 属于 `Malware`，OWL 推理机就能得出结论：HAMMERTOSS 也属于 `Software`。Semantica 负责导出本体；推理本身在外部工具中运行。

**知识图谱质量。** 结构化的模式能尽早暴露错误，保证新数据与既有实体干净地整合。

## 适用与不适用场景

**适合使用本体的场景：**
- 实体关系复杂的正式知识图谱
- 跨团队或跨组织的数据整合
- 自动推理和基于规则的系统
- 需要长期保持一致性的知识库
- 与依赖 OWL/RDF 模式的外部工具集成

**不适合使用本体的场景：**
- 对文本文档做简单的语义检索
- 向量相似度已经够用的轻量级检索增强生成(RAG)
- 模式频繁变动的原型开发
- 一次性、不需要复用的数据分析
- 维护开销超过领域本身复杂度的情形

<Info>
Semantica 的本体模块直接从知识图谱中已有的实体和关系推导出正式的 OWL 本体——无需预先设计模式。一条 6 阶段流水线负责推断类、构建层级、映射 OWL 类型并序列化为 Turtle。整条流水线在内存中运行，你不需要一个在运行的三元组库(Triplet Store)。
</Info>

---

## 一个简单示例

先从一个熟悉的业务领域入手理解机制，再进入网络安全场景：

```python
from semantica.ontology import OntologyGenerator

# 直接构建一个简单的组织架构图
data = {
    "entities": [
        {"id": "e-1", "name": "Alice",            "type": "Person"},
        {"id": "e-2", "name": "Bob",              "type": "Person"},
        {"id": "e-3", "name": "Carol",            "type": "Person"},
        {"id": "e-4", "name": "Acme Corporation", "type": "Company"},
        {"id": "e-5", "name": "San Francisco",    "type": "Location"},
    ],
    "relationships": [
        {"source_id": "e-1", "target_id": "e-4", "type": "works_for"},
        {"source_id": "e-2", "target_id": "e-4", "type": "works_for"},
        {"source_id": "e-1", "target_id": "e-3", "type": "reports_to"},
        {"source_id": "e-4", "target_id": "e-5", "type": "headquartered_in"},
    ],
}

generator = OntologyGenerator(
    base_uri="https://company.example.org/ontology/",
    min_occurrences=1,
)

ontology = generator.generate_ontology(
    data,
    name="OrganizationOntology",
    build_hierarchy=True,
)

# 查看生成了什么
print(f"Classes: {len(ontology.get('classes', []))}")
# Classes: 3

print("Object Properties:")
for prop in ontology.get('properties', []):
    if prop.get('type') == 'object':
        domain = ', '.join(prop.get('domain', []))
        range_ = ', '.join(prop.get('range', []))
        print(f"  {prop['name']} ({domain} → {range_})")
# works_for (Person → Company)
# reports_to (Person → Person)
# headquartered_in (Company → Location)

print("Datatype Properties:")
for prop in ontology.get('properties', []):
    if prop.get('type') == 'data':
        print(f"  {prop['name']} ({prop.get('range')})")
# name (string)
```

**base_uri**（`https://company.example.org/ontology/`）会成为所有类和属性的命名空间前缀。在导出的资源描述框架(RDF)中，`Person` 会变成 `<https://company.example.org/ontology/Person>`。

**对象属性**把实体连接到其他实体（`works_for`、`reports_to`）；**数据属性**把实体连接到字面值（`name`）。

---

## 没有模式的图

有了模式的概念之后，往知识图谱里灌入网络威胁情报(CTI)数据，让流水线的运作机制看得见摸得着。

```python
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore

vs    = VectorStore(backend="faiss", dimension=768)
graph = ContextGraph()
ctx   = AgentContext(vector_store=vs, knowledge_graph=graph, graph_expansion=True)

ctx.store(
    [
        "CVE-2024-3400 is a critical vulnerability in PAN-OS exploited by APT29.",
        "APT29 is a Russian state-sponsored threat actor targeting NATO governments.",
        "PAN-OS is a network operating system developed by Palo Alto Networks.",
        "HAMMERTOSS is a backdoor malware used by APT29 for command-and-control.",
    ],
    extract_entities=True,
    extract_relationships=True,
)

# 此时我们已有约 8 个节点和若干条边，但还没有正式的模式。
# "APT29" 和一个假想的 "Lazarus Group" 都是 ThreatActor——
# 却没有任何机制强制二者都必须带有 attribution_confidence 属性。
print(f"Graph nodes: {len(graph.to_dict().get('nodes', []))}")
```

---

## 生成本体

`OntologyGenerator` 读取你的图字典，跑完 6 阶段流水线。

```python
from semantica.ontology import OntologyGenerator

generator = OntologyGenerator(
    base_uri="https://cti.example.org/ontology/",
    min_occurrences=1,   # 出现过至少一次的实体类型都会成为类
)

ontology = generator.generate_from_graph(
    graph.to_dict(),
    name="CyberThreatOntology",
    build_hierarchy=True,  # 推断父子类关系
)

# 流水线的产出：
print(f"Classes   : {len(ontology.get('classes', []))}")
# Classes   : 4  → ThreatActor, Vulnerability, Software, Malware

print(f"Properties: {len(ontology.get('properties', []))}")
# Properties: 3  → exploits (object), targets (object), name (datatype)

# 查看某个类：
for cls in ontology.get("classes", []):
    print(f"  {cls['name']}  parent={cls.get('parent')}")
# ThreatActor   parent=None
# Vulnerability parent=None
# Software      parent=None
# Malware       parent=Software   ← hierarchy inferred because HAMMERTOSS was linked to PAN-OS (Software)
```

`Malware` 的层级条目说明：流水线根据关系图中的共现模式，检测出恶意软件是软件的一个子类型。导出之前，你可以手动覆盖这些推断结果。

---

## 校验模式

导出之前先做结构校验。

```python
from semantica.ontology import validate_ontology

result = validate_ontology(ontology)

print(f"Valid: {result.get('valid', False)}")
# Valid: True

for w in result.get("warnings", []):
    print(f"  WARN : {w}")
# WARN : Class 'Malware' has no declared datatype properties

for e in result.get("errors", []):
    print(f"  ERROR: {e}")
# (none — the ontology is structurally sound)
```

这个阶段出现"缺少数据属性"的警告很常见。它的含义是：推断流水线在你的图中发现了这个类，但没有哪个节点带有显式的属性值。你可以在下一轮导出之前，用 `ClassInferrer` 和 `PropertyGenerator` 手动补充属性。

---

## 随新节点类型出现而生长本体

用 `ClassInferrer` 增量添加新的实体类型，不必重新生成整个本体。

```python
from semantica.ontology import ClassInferrer, PropertyGenerator

# 精细控制：从这批新实体推断类
new_entities = [
    {"id": "kev-001", "name": "KEV-CVE-2024-3400", "type": "KEVEntry",
     "due_date": "2024-04-19", "ransomware_use": "Known"},
    {"id": "kev-002", "name": "KEV-CVE-2023-4966", "type": "KEVEntry",
     "due_date": "2023-11-14", "ransomware_use": "Unknown"},
]

inferrer = ClassInferrer()
new_classes = inferrer.infer_classes(new_entities)
# [{"id": "KEVEntry", "name": "KEVEntry", "parent": None, ...}]

# 合并前手动把父类设为 Vulnerability
for cls in new_classes:
    if cls["name"] == "KEVEntry":
        cls["parent"] = "https://cti.example.org/ontology/Vulnerability"

# 查看层级
hierarchy = inferrer.build_class_hierarchy(new_classes)
print(hierarchy)
# {"KEVEntry": {"parent": "...Vulnerability", "children": []}}

# 合并进现有本体
ontology["classes"].extend(new_classes)

# 从新节点推断属性
prop_gen = PropertyGenerator()
# PropertyGenerator 读取实体属性和关系模式，
# 生成数据属性（due_date: xsd:date）和对象属性
```

这里的核心是增量式：对每批新数据运行 `infer_classes`，检查结果，把流水线猜错的父类改过来，然后合并。本体随图谱一起生长，而不是落在图谱后面。

---

## 从非结构化文本生成本体

`LLMOntologyGenerator` 用 LLM 从自然语言文本中抽取类和属性——还没有结构化图谱时，适合用它做冷启动。

```python
from semantica.ontology import LLMOntologyGenerator

llm_gen = LLMOntologyGenerator(provider="groq", model="llama-3.1-8b-instant")

ontology_from_text = llm_gen.generate_ontology_from_text(
    """
    APT29 (also known as Cozy Bear) is a Russian state-sponsored threat actor.
    They use spear-phishing emails to deliver HAMMERTOSS malware.
    HAMMERTOSS communicates over Twitter and GitHub to evade detection.
    The group has been observed exploiting CVE-2024-3400 in PAN-OS appliances.
    """
)

# LLM 识别出：ThreatActor, Malware, Vulnerability, Platform, CommunicationChannel
print(f"Classes extracted: {len(ontology_from_text.get('classes', []))}")

# 支持的提供商："groq", "openai", "anthropic", "novita"
```

<Info>
`LLMOntologyGenerator` 最适合还没有结构化图谱时给新领域做冷启动。一旦有了图，优先用 `OntologyGenerator.generate_from_graph()`——它结果确定、可复现，而且不会在每次运行时消耗 LLM token。
</Info>

---

## 为下游系统导出

按下游工具期望的格式导出。

```python
from semantica.export import export_owl, export_rdf

# OWL/XML——供 Protégé、OWL API、HermiT、Pellet 使用
export_owl(ontology, "cyber_threat.owl", format="owl-xml")

# Turtle——紧凑、人类可读；SHACL 工具链首选
export_rdf(ontology, "cyber_threat.ttl", format="turtle")

# JSON-LD——面向 Web API 和关联数据应用
export_rdf(ontology, "cyber_threat.jsonld", format="jsonld")

# N-Triples——用于向三元组库批量导入（GraphDB、Stardog、Oxigraph）
export_rdf(ontology, "cyber_threat.nt", format="ntriples")
```

导出的 Turtle 文件是 Semantica SHACL 校验流水线的输入。如何从该本体生成 SHACL 形状、再用实时图数据跑校验，见 [SHACL 校验](./shacl-validation.md)指南。

---

## 本体的草拟、评审与发布

修改一个在线运行的本体，比改图数据的影响更重。其他系统可能已经依赖那些类名和属性名，一次重命名会波及四方。探索(Explorer)功能通过 HTTP 暴露草稿/提案流程，让变更先暂存、先评审，再落到图谱上。

一旦编辑同一本体的不止一个人或智能体，这套流程的开销就值得。还在原型阶段时，重新生成本体通常比评审 diff 更省事。

**状态机**

| 状态 | 进入方式 | 后续可进行的操作 |
| :---- | :--------- | :------------------- |
| `draft` | `PATCH /api/ontology/draft` | 提交为提案 |
| `proposed` | `POST /api/ontology/propose` | 批准或驳回 |
| `approved` | `POST /api/ontology/proposals/{id}/approve` | 发布（只有此状态可以） |
| `rejected` | `POST /api/ontology/proposals/{id}/reject` | 修改成新草稿 |
| `published` | `POST /api/ontology/proposals/{id}/publish` | 终态 |

只要不是 `approved` 状态，`publish` 都会返回 `400`——没有显式批准，提案就进不了图谱。

**流程**

```bash
# 1. 暂存变更。这个端点是 PATCH，不是 POST。
curl -X PATCH http://localhost:8000/api/ontology/draft \
  -H "Content-Type: application/json" \
  -d '{
    "ontology_uri": "http://example.org/onto/security",
    "author": "analyst@example.org",
    "summary": "Add Platform class for infrastructure entities",
    "diff": {
      "added_classes": ["http://example.org/onto/security#Platform"],
      "added_properties": []
    }
  }'
# → {"draft_id": "draft_9f2c1a4b7e03", ...}
```

```bash
# 2. 提交提案。各项检查就是在这一步运行的。
curl -X POST http://localhost:8000/api/ontology/propose \
  -H "Content-Type: application/json" \
  -d '{
    "draft_id": "draft_9f2c1a4b7e03",
    "ontology_uri": "http://example.org/onto/security",
    "summary": "Add Platform class for infrastructure entities"
  }'
```

响应里有两个块：

- `impact_analysis` —— `VersionManager.diff_ontologies` 产出的结构化 diff，外加 `class_adds`、`class_removals`、`property_changes` 和 `restriction_changes` 计数。
- `shacl_validation` —— 用提案本体生成的形状去校验当前图数据的结果。会话未配置存储时显示 `{"status": "skipped", "reason": "No store configured"}`；校验本身失败时显示 `{"status": "error", ...}`。这两者都不会阻止提案创建，仅供参考。

```bash
# 3. 阅读提案，然后批准或驳回。`GET /api/ontology/proposals`
#    会列出所有提案，可用 ?ontology_uri= 和 ?state= 过滤。
curl http://localhost:8000/api/ontology/proposals/prop_4d8e01a9c3f2
curl -X POST http://localhost:8000/api/ontology/proposals/prop_4d8e01a9c3f2/approve

# 评审者还可以针对具体的元素 URI 留言。
curl -X POST http://localhost:8000/api/ontology/proposals/prop_4d8e01a9c3f2/comment \
  -H "Content-Type: application/json" \
  -d '{
    "element_uri": "http://example.org/onto/security#Platform",
    "text": "Should this inherit from Infrastructure rather than sit at the top level?",
    "author": "reviewer@example.org"
  }'
```

```bash
# 4. 发布。先创建版本记录，再写入图谱。
curl -X POST http://localhost:8000/api/ontology/proposals/prop_4d8e01a9c3f2/publish
# → {"status": "published", "version": "1.1.0", "nodes_added": 1, "edges_added": 0}
```

**publish 应用什么、按什么顺序**

publish 在触碰在线图谱之前，会先调用 `VersionManager.create_version()`。版本创建失败时，请求返回 `500`，图谱不会有任何变化。

publish 只应用新增内容。`added_classes` 和 `added_properties` 会变成 `owl:Class` 和 `owl:ObjectProperty` 节点；删除和修改只会记入版本历史，不会删除或改写图中已有的任何东西。

**版本历史与对比**

```bash
curl "http://localhost:8000/api/ontology/versions/http%3A%2F%2Fexample.org%2Fonto%2Fsecurity"

curl -X POST "http://localhost:8000/api/ontology/versions/http%3A%2F%2Fexample.org%2Fonto%2Fsecurity/compare" \
  -H "Content-Type: application/json" \
  -d '{"version1": "1.1.0", "version2": "1.2.0"}'
```

`compare` 把 `class_changes`、`property_changes`、`restriction_changes` 和 `axiom_changes` 分块返回——想知道改了什么，不必对整个本体做 diff。

---

## 常见陷阱

**过度建模。** 10 个类就够用，就别建 50 个。从简单开始，只有当推理或校验需要形式化的区分时才增加复杂度。给 `MaliciousEmail` 和 `PhishingEmail` 分别建类，只有当它们拥有不同的属性或关系时才有意义。

**本体漂移。** 图里冒出新实体类型时，本体若不重新生成或增量更新就会过时。建议建立监控，及时发现当前本体未覆盖的新实体类型。

**类命名不一致。** 选定一种约定（CamelCase、snake_case 或 kebab-case）并贯彻到底。同一个本体里混用 `ThreatActor`、`threat_actor` 和 `threat-actor`，既制造混乱，也会弄坏依赖一致命名模式的工具。

**状态只存内存。** 草拟/提案流程的状态保存在应用对象上而非存储里，重启会丢掉所有草稿、提案和版本记录，状态也不在多个 worker 进程间共享。凡是想保留的内容，都必须在进程重启前发布。

**路径段中未编码的 `#`。** `/api/ontology/drafts/{uri}` 和 `/api/ontology/versions/{uri}` 把本体 URI 放在路径段里，而 `#` 在 URL 中是片段起始符，服务器只能看到它之前的部分。请把它编码成 `%23`，就像上面的版本示例那样。OWL 本体的 URI 常以 `#` 结尾，而且这里的失败是静默的：端点返回 `200` 和一个空列表，不会报告 URI 被截断。不含 `#` 的 URI 不受影响。

---

## 领域示例

<Tabs>

<Tab title="国防——CTI/威胁情报">

某国防网络威胁情报(CTI)团队每天早晨摄取原始 OSINT 报告。本体必须与 STIX 2.1 和北约 MISP 分类法保持互操作，因此 IRI 采用美国国防部(DoD)命名空间，本体导出为 OWL/XML，供机构的安全信息与事件管理(SIEM)推理插件使用。

```python
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore
from semantica.ingest import ingest_file, ingest_web
from semantica.ontology import OntologyGenerator, validate_ontology
from semantica.export import export_owl, export_rdf

vs    = VectorStore(backend="faiss", dimension=768)
graph = ContextGraph()
ctx   = AgentContext(vector_store=vs, knowledge_graph=graph, graph_expansion=True)

# 摄取一份战役 PDF 和 NVD 公告页面
cti_report = ingest_file("apt29_cozycar_2024.pdf", method="file")
nvd_entry  = ingest_web("https://nvd.nist.gov/vuln/detail/CVE-2024-3400", method="url")

ctx.store(
    [cti_report.text, nvd_entry.text],
    extract_entities=True,
    extract_relationships=True,
)

generator = OntologyGenerator(
    base_uri="https://ontology.dod.mil/cyber/",
    min_occurrences=1,
)
ontology = generator.generate_from_graph(
    graph.to_dict(),
    name="CyberThreatOntology",
    build_hierarchy=True,
)

result = validate_ontology(ontology)
print(f"Ontology valid: {result.get('valid')}")
# Ontology valid: True

# OWL/XML 给 SIEM 推理插件；Turtle 给 SHACL 流水线
export_owl(ontology, "./ontologies/cyber_threat.owl", format="owl-xml")
export_rdf(ontology, "./ontologies/cyber_threat.ttl", format="turtle")

print(f"Classes    : {len(ontology.get('classes', []))}")
print(f"Properties : {len(ontology.get('properties', []))}")
# Classes    : 7  (ThreatActor, Vulnerability, Malware, Platform, Campaign, ...)
# Properties : 9  (exploits, targets, uses, name, cvss_score, ...)
```

</Tab>

<Tab title="安全——SOC/事件响应">

某安全运营中心(SOC)团队把零信任身份实体——用户、服务账号、资源和策略——建模为 OWL 本体，让策略评估引擎使用统一的形式化词汇，而不是硬编码的字符串。

```python
from semantica.ontology import OntologyGenerator, ClassInferrer
from semantica.export import export_owl

# 手工指定身份图谱——生产环境中这些数据来自你的 IAM 导出
data = {
    "entities": [
        {"id": "u-1",  "name": "alice",      "type": "User"},
        {"id": "u-2",  "name": "svc-scanner","type": "ServiceAccount"},
        {"id": "r-1",  "name": "kube-api",   "type": "Resource"},
        {"id": "r-2",  "name": "s3-prod",    "type": "Resource"},
        {"id": "p-1",  "name": "ReadOnly",   "type": "Policy"},
        {"id": "p-2",  "name": "AdminAccess","type": "Policy"},
    ],
    "relationships": [
        {"source_id": "u-1", "target_id": "p-1", "type": "BOUND_TO"},
        {"source_id": "u-2", "target_id": "p-2", "type": "BOUND_TO"},
        {"source_id": "p-1", "target_id": "r-1", "type": "ALLOWS_ACCESS"},
        {"source_id": "p-2", "target_id": "r-2", "type": "ALLOWS_ACCESS"},
    ],
}

generator = OntologyGenerator(
    base_uri="https://zerotrust.corp/ontology/",
    min_occurrences=1,
)
ontology = generator.generate_ontology(data, name="ZeroTrustOntology")

# 查看流水线推断出的内容
inferrer = ClassInferrer()
classes  = inferrer.infer_classes(data["entities"])
for cls in classes:
    print(f"  Class: {cls.get('name')}")
# Class: User
# Class: ServiceAccount
# Class: Resource
# Class: Policy

export_owl(ontology, "./ontologies/zero_trust.owl", format="owl-xml")
print("Ontology exported for policy evaluation engine")
```

</Tab>

<Tab title="生命科学——临床/制药">

某制药团队需要一个符合 OBO Foundry 约定（GO、CHEBI、HP）的本体，用来描述 II/III 期肿瘤试验方案。由于源数据放在 PostgreSQL 试验数据库里——而不是知识图谱——他们用 `LLMOntologyGenerator` 从文字描述做冷启动。

```python
from semantica.ontology import LLMOntologyGenerator, OntologyGenerator, validate_ontology
from semantica.export import export_owl, export_rdf
from semantica.ingest import DBIngestor

# 从临床数据库加载试验记录
db = DBIngestor()
trial_rows = db.execute_query(
    "postgresql://readonly@clindb:5432/trials",
    """
        SELECT compound, target_protein, disease_indication,
               mechanism_of_action, primary_endpoint
        FROM trial_protocols WHERE phase IN ('II','III')
    """,
)

# 为 LLM 构造自然语言摘要
protocol_text = "\n".join(
    f"Compound {r['compound']} targets {r['target_protein']} "
    f"in {r['disease_indication']} via {r['mechanism_of_action']}. "
    f"Primary endpoint: {r['primary_endpoint']}."
    for r in trial_rows
)

# LLM 抽取出的类：Compound, TargetProtein, DiseaseIndication,
#   MechanismOfAction, ClinicalEndpoint, ClinicalTrial
llm_gen  = LLMOntologyGenerator(provider="openai", model="gpt-4o")
ontology = llm_gen.generate_ontology_from_text(protocol_text)

result = validate_ontology(ontology)
print(f"Valid: {result.get('valid')}")
for w in result.get("warnings", []):
    print(f"  WARN: {w}")

# 按 OBO Foundry URI 约定导出
export_owl(ontology, "./ontologies/clinical_trial.owl", format="owl-xml")
export_rdf(ontology, "./ontologies/clinical_trial.ttl", format="turtle")
print("Ontology ready for Protégé review and OBO alignment check")
```

</Tab>

<Tab title="银行——风险/合规">

某风险团队把巴塞尔协议III(Basel III) / BCBS 239 的概念形式化为 OWL 本体，让自动化合规规则用统一词汇对信贷风险实体做推理——取代 Python 脚本里硬编码的字段名检查。

```python
from semantica.ontology import LLMOntologyGenerator, validate_ontology
from semantica.export import export_owl, export_rdf
from semantica.ingest import ingest_file

# 摄取监管源文件
regs = [
    ingest_file("basel3_cre20.pdf", method="file"),
    ingest_file("sr_11_7.pdf",      method="file"),
    ingest_file("bcbs239.pdf",      method="file"),
]

# 用 LLM 从监管文本中抽取概念模型
llm_gen  = LLMOntologyGenerator(provider="anthropic", model="claude-sonnet-5")
ontology = llm_gen.generate_ontology_from_text(
    "\n\n".join(r.text[:8000] for r in regs)  # 每份文档截取 token 安全的片段
)

result = validate_ontology(ontology)
if not result.get("valid"):
    for err in result.get("errors", []):
        print(f"ERROR: {err}")
    # 修复错误后再发布到合规规则引擎
else:
    print("Ontology valid — publishing to compliance registry")
    # Turtle 做 SHACL 形状；OWL/XML 给 HermiT 推理；JSON-LD 给 API
    export_owl(ontology, "./ontologies/regulatory.owl",    format="owl-xml")
    export_rdf(ontology, "./ontologies/regulatory.ttl",    format="turtle")
    export_rdf(ontology, "./ontologies/regulatory.jsonld", format="jsonld")
```

</Tab>

</Tabs>

---

## 相关指南

- [SHACL 校验](./shacl-validation.md) — 从你的本体生成 W3C SHACL 约束形状，并用实时图数据做校验
- [推理与规则](./reasoning.md) — 在本体上应用前向/后向链式规则，推导新事实
- [导出与序列化](./export.md) — 把图导出为 RDF、GraphML、CSV 和 Neo4j Cypher
- [语义抽取](./semantic-extraction.md) — 抽取实体和关系，为本体生成提供输入
- [上下文图](./context-graphs.md) — 本体生成所读取的那张知识图谱
