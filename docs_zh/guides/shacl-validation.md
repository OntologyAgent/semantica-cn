---
title: SHACL 校验
description: 从 OWL 本体生成 W3C SHACL 形状，用结构与语义约束校验 RDF 知识图谱，并输出结构化的违规报告。
source: guides/shacl-validation.md
source_version: 236b8994c7053e20109e632472419355566c8877
icon: "shield-check"
---

## 什么是 SHACL 校验？

SHACL（Shapes Constraint Language，形状约束语言）是一种面向图数据的标准校验语言。本体(Ontology)描述的是概念层面的*模式*（你的领域里"有什么"），SHACL 定义的则是结构层面的*规则与约束*（这些数据"该怎么组织"）。

在 Semantica 中，`SHACLGenerator` 依据你的本体生成约束规则，也就是 SHACL 形状(SHACL shapes)，公开的 `run_shacl_validation` 函数再用这些规则去检查你的实际数据。一旦某个节点违反规则（比如缺少必需属性、用错了数据类型），就会生成一份详细的违规报告。旧名称 `_run_pyshacl` 仍作为兼容别名保留。

## 为什么用 SHACL 校验？

在跑分析、导出数据或把数据喂给生产模型之前，数据校验都是关键一步。SHACL 扮演的是**数据质量门禁**(data quality gate)的角色，保证图数据在结构上是可靠的。可以用它拦住：
- 缺失的必需属性（比如客户没有邮箱地址）。
- 数据类型不匹配（比如期望数字却给了字符串）。
- 基数(cardinality)超限（比如一个人填了三个"主地址"）。

## 适用与不适用场景

- **适用场景**：你有一张复杂、高度互联的知识图谱(Knowledge Graph)，需要校验节点之间的*关系*和结构完整性。SHACL 擅长确保合并后的高连接数据符合你的业务规则。
- **不适用场景**：只是校验一个扁平的 JSON 载荷或单个 API 请求。对扁平数据或单条记录，用 Pydantic、JSONSchema 这类更简单、更快的库就好。

---

## 关键术语解释

动手之前，先认识几个会反复出现的概念：

- **资源描述框架(RDF)**：把数据表示成图的标准方式。它把信息看作相互连接的"三元组"（主语 → 谓语 → 宾语）。
- **网络本体语言(OWL)**：用来构建本体的语言，定义你的领域里存在哪些类和属性。
- **SHACL 形状**：真正的校验规则。一个"形状"瞄准数据中的某个特定类（比如 `Person`），并定义它必须满足的约束（比如"必须恰好有一个出生日期"）。
- **Turtle（.ttl）**：一种流行的、人类可读的文件格式，用来存储 RDF 图数据和 SHACL 形状。

---

## 典型工作流

一条典型的 SHACL 校验流水线遵循这样的生命周期：

1. **本体**：构建一个描述你领域的本体。
2. **SHACL 形状**：从该本体生成形状。
3. **数据图**：准备好你的知识图谱。
4. **校验**：用 SHACL 形状校验知识图谱。
5. **违规报告**：分析报告中的错误。
6. **修复**：修好数据或流水线，然后重新校验。

---

## 通用示例：员工与部门

来看一个简单直白的例子：确保每个 `Employee` 都属于某个 `Department`，并且都有 `employee_id`。

```python
from semantica.context import ContextGraph
from semantica.ontology import OntologyGenerator, SHACLGenerator, PropertyShape
from semantica.ontology import run_shacl_validation

# 1. Prepare your data graph
graph = ContextGraph()
graph.add_node("emp-1", "Employee", "Alice", employee_id="E001")
graph.add_node("emp-2", "Employee", "Bob") # Missing employee_id, will cause a violation!

# 2. Build the ontology
ontology = (
    OntologyGenerator(base_uri="https://company.example.com/ontology/", min_occurrences=1)
    .generate_from_graph(graph.to_dict(), name="CompanyOntology")
)

# 3. Generate SHACL Shapes
shacl_gen = SHACLGenerator(base_uri="https://company.example.com/shapes/", severity="Violation")
shacl_graph = shacl_gen.generate(ontology)

# Inject mandatory constraints
BASE = "https://company.example.com/ontology/"
for ns in shacl_graph.node_shapes:
    if "Employee" in ns.target_class:
        ns.property_shapes.append(
            PropertyShape(path=f"{BASE}employee_id", min_count=1, severity="Violation")
        )

# Serialize shapes to Turtle
shacl_ttl = shacl_gen.serialize(shacl_graph, format="turtle")

# 4. Prepare your RDF data graph
# (For validation, serialize your graph instances to RDF. Here we use a Turtle string.)
data_ttl = """
@prefix ex: <https://company.example.com/ontology/> .

<http://example.org/emp-1> a ex:Employee ;
    ex:employee_id "E001" .

<http://example.org/emp-2> a ex:Employee .
"""

# 5. Run Validation
report = run_shacl_validation(data_ttl, shacl_ttl)

# 6. Analyze the Report
print(f"Graph conforms: {report.conforms}")
if not report.conforms:
    report.explain_violations() # Populates human-readable explanations
    for v in report.violations:
        print(f"Violation: {v.explanation}")
```

---

下面把这条工作流逐一展开。

## 第 1 步——从合并后的图构建本体

SHACL 形状由本体推导而来。如果上一轮运行已经留下本体，直接跳过这一步。

```python
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore
from semantica.ontology import OntologyGenerator

graph = ContextGraph()
ctx   = AgentContext(
    vector_store=VectorStore(backend="faiss", dimension=768),
    knowledge_graph=graph,
    graph_expansion=True,
)

# Load the merged CTI data — in production this would be your full 12,000-node graph
ctx.store(
    [
        "APT29 is a Russian state-sponsored threat actor targeting NATO governments.",
        "CVE-2024-3400 is a critical vulnerability in PAN-OS exploited by APT29.",
        "HAMMERTOSS is a backdoor malware family used by APT29 for C2 over Twitter.",
        "PAN-OS is a network operating system developed by Palo Alto Networks.",
    ],
    extract_entities=True,
    extract_relationships=True,
)

ontology = (
    OntologyGenerator(base_uri="https://cti.example.org/ontology/", min_occurrences=1)
    .generate_from_graph(graph.to_dict(), name="CyberOntology")
)

print(f"Classes inferred: {len(ontology.get('classes', []))}")
# Classes inferred: 4  → ThreatActor, Vulnerability, Malware, Platform
```

---

## 第 2 步——从本体生成 SHACL 形状

`SHACLGenerator` 会生成一个 `SHACLGraph`，其中每个 OWL 类对应一个 `NodeShape`。

```python
from semantica.ontology import SHACLGenerator

shacl_gen = SHACLGenerator(
    base_uri="https://cti.example.org/shapes/",
    include_inherited=True,   # propagate parent-class constraints to sub-classes
    severity="Violation",     # default severity for all generated shapes
    quality_tier="standard",  # constraint strictness: "minimal" | "standard" | "strict"
)

shacl_graph = shacl_gen.generate(ontology)

print(f"Node shapes generated: {len(shacl_graph.node_shapes)}")
# Node shapes generated: 4  — one per class

for ns in shacl_graph.node_shapes:
    print(f"  {ns.target_class}  ({len(ns.property_shapes)} property constraints)")
# https://cti.example.org/ontology/ThreatActor   (2 property constraints)
# https://cti.example.org/ontology/Vulnerability  (3 property constraints)
# https://cti.example.org/ontology/Malware        (2 property constraints)
# https://cti.example.org/ontology/Platform       (1 property constraint)
```

生成的形状反映的是流水线**观察到了什么**，还不包含你的领域**要求什么**。下一节展示如何注入领域特有的强制约束。

---

## 第 3 步——注入领域约束

补充那些流水线无法只凭数据推断出来的 `PropertyShape` 强制约束。

```python
from semantica.ontology import PropertyShape

BASE = "https://cti.example.org/ontology/"

for node_shape in shacl_graph.node_shapes:

    if "Malware" in node_shape.target_class:
        # family is required — missing it causes a Violation
        node_shape.property_shapes.append(
            PropertyShape(
                path=f"{BASE}family",
                min_count=1,
                severity="Violation",
            )
        )
        # attribution_confidence is recommended — missing it causes a Warning
        node_shape.property_shapes.append(
            PropertyShape(
                path=f"{BASE}attribution_confidence",
                min_count=1,
                datatype="http://www.w3.org/2001/XMLSchema#float",
                severity="Warning",
            )
        )

    if "Vulnerability" in node_shape.target_class:
        # cvss_score is required by your detection rules
        node_shape.property_shapes.append(
            PropertyShape(
                path=f"{BASE}cvss_score",
                min_count=1,
                datatype="http://www.w3.org/2001/XMLSchema#float",
                severity="Violation",
            )
        )

    if "ThreatActor" in node_shape.target_class:
        # name is required; nation_state classification is recommended
        node_shape.property_shapes.append(
            PropertyShape(path=f"{BASE}name",         min_count=1, severity="Violation")
        )
        node_shape.property_shapes.append(
            PropertyShape(path=f"{BASE}nation_state",  min_count=1, severity="Warning")
        )

# Serialise the final shape graph to Turtle for reuse and version control
shacl_ttl = shacl_gen.serialize(shacl_graph, format="turtle")

with open("cti_shapes.ttl", "w") as f:
    f.write(shacl_ttl)

print("Shapes written to cti_shapes.ttl")
```

你也可以完全手工构建形状——当需要表达生成器永远推断不出的约束时（比如给 CVE ID 字段加正则模式），这很有用：

```python
from semantica.ontology import NodeShape, PropertyShape, SHACLGraph

# Require CVE IDs to match the canonical NIST format
cve_id_shape = NodeShape(
    target_class="https://cti.example.org/ontology/Vulnerability",
    name="VulnerabilityShape",
    closed=False,
    severity="Violation",
    property_shapes=[
        PropertyShape(
            path="https://cti.example.org/ontology/cve_id",
            min_count=1,
            pattern=r"^CVE-\d{4}-\d{4,}$",   # e.g. CVE-2024-3400
            severity="Violation",
        ),
    ],
)
# Inject into the existing shacl_graph or build a standalone SHACLGraph
```

---

## 第 4 步——运行校验并读取报告

先把图序列化成 RDF，再用 `run_shacl_validation` 对着形状跑校验。

```python
from semantica.ontology import run_shacl_validation

# Prepare your RDF data string (since export_rdf primarily exports structural metadata,
# you typically serialize your custom data graph to Turtle using rdflib or similar).
data_ttl = """
@prefix ex: <https://cti.example.org/ontology/> .

<http://example.org/malware-002> a ex:Malware .
<http://example.org/vuln-003> a ex:Vulnerability ;
    ex:cve_id "CVE24-3400" .
"""

# Run SHACL validation
report = run_shacl_validation(
    data_ttl,
    shacl_ttl,
    data_graph_format="turtle",
    shacl_format="turtle",
)

# High-level summary
print(f"Conforms   : {report.conforms}")
# Conforms   : False   ← at least one Violation found

print(f"Violations : {report.violation_count}")
# Violations : 3

print(f"Warnings   : {report.warning_count}")
# Warnings   : 2

print(report.summary())
# Graph does NOT conform: 3 violation(s).
```

汇总信息告诉你哪里出了问题，接下来深入细节。

---

## 第 5 步——理解违规项

每个 `SHACLViolation` 都会指明问题节点、属性路径和需要的修复。

```python
if not report.conforms:
    # Populate plain-English explanations for every violation
    report.explain_violations()
    
    # Iterate and print the explanations
    for v in report.violations:
        print(v.explanation)
    # Node <http://example.org/malware-002> is missing required property
    #   <https://cti.example.org/ontology/family>. At least 1 value(s) are required.
    # Node <http://example.org/vuln-003> is missing required property
    #   <https://cti.example.org/ontology/cvss_score>. At least 1 value(s) are required.
    # Node <http://example.org/vuln-003> has value 'CVE24-3400' for
    #   <https://cti.example.org/ontology/cve_id> which does not match the required pattern.

    # Iterate for programmatic triage
    for v in report.violations:
        print(f"VIOLATION  node={v.focus_node}")
        print(f"           path={v.result_path}")
        print(f"           rule={v.constraint}")
        print(f"           msg ={v.message}")
        if v.value:
            print(f"           val ={v.value}")
        if v.explanation:
            print(f"           fix ={v.explanation}")
        print()

    # Warnings are lower severity — review but do not block
    for w in report.warnings:
        print(f"WARNING  {w.focus_node}  {w.result_path}  {w.message}")
```

这些输出可以直接转成修复任务：`malware-002` 需要补上 `family` 属性；`vuln-003` 需要补 `cvss_score`，并把 `cve_id` 改成规范格式。

---

## 第 6 步——自动修复常见违规

标记或修补缺少必需属性的节点，然后重新校验确认。

```python
# Parse the report into a dict for programmatic processing
report_dict = report.to_dict()

# Collect nodes missing the 'family' property
missing_family = [
    v["focus_node"]
    for v in report_dict.get("violations", [])
    if "family" in (v.get("result_path") or "")
]

print(f"Malware nodes missing 'family': {len(missing_family)}")
# In production: queue these for analyst enrichment or apply a default
# e.g. graph.update_node(node_id, {"family": "UNKNOWN — requires triage"})

# After remediation, re-run validation to confirm the fix
# (re-export the patched graph to Turtle first, then call run_shacl_validation again)
report2 = run_shacl_validation(patched_data_ttl, shacl_ttl)
print(f"Violations after remediation: {report2.violation_count}")
# Violations after remediation: 0
```

---

## 常见陷阱

- **以为本体自动保证数据质量**：`SHACLGenerator` 只根据它在数据里观察到的东西生成形状。数据缺了某个字段，生成器并不知道它本该必填，除非你像第 3 步那样显式注入约束。
- **把 `ContextGraph` 直接传给 SHACL 校验器**：`run_shacl_validation` 接收的是 RDF 字符串（比如 Turtle 格式），不是原始 Python 字典或 `ContextGraph` 对象。
- **忘记做 RDF 序列化**：校验之前必须先把图序列化（通常用 `export_rdf` 写入临时文件）。
- **把校验当成一次性动作**：校验应该作为自动化步骤嵌入 CI/CD 流水线或数据摄取(Ingestion)流程，充当常态化的守门员，而不是跑一次就完的脚本。
- **无视校验报告**：不合规的图必须修复。不查看 `violation_count`、不处理问题，SHACL 校验就失去了意义。
- **在声明了 `rdfs:range` 的属性上、开着 RDFS 蕴含(entailment)去校验 `sh:class`/`sh:node`**：RDFS 是一条蕴含推理规则，不是约束。pyshacl 以 `inference="rdfs"` 运行时，会把值域类推断到该属性的每个对象上，于是针对该属性的类约束永远不会失败——数据明明不合规，报告却给出 `conforms: True`：

    ```python
    from pyshacl import validate
    from rdflib import Graph

    data = Graph()
    data.parse(
        data="""
        @prefix ex: <https://example.org/ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        ex:contains rdfs:domain ex:Container ; rdfs:range ex:Item .
        ex:box a ex:Container ; ex:contains ex:notAnItem .
        ex:notAnItem a ex:Fish .
        """,
        format="turtle",
    )

    shapes = Graph()
    shapes.parse(
        data="""
        @prefix ex: <https://example.org/ns#> .
        @prefix sh: <http://www.w3.org/ns/shacl#> .
        ex:ContainerShape a sh:NodeShape ;
            sh:targetClass ex:Container ;
            sh:property [ sh:path ex:contains ; sh:class ex:Item ] .
        """,
        format="turtle",
    )

    for inference in ("none", "rdfs"):
        conforms, _, _ = validate(data, shacl_graph=shapes, inference=inference)
        print(inference, conforms)
    # none  False   <- correct: notAnItem is a Fish, not an Item
    # rdfs  True    <- the entailment manufactured the type
    ```

    缓解办法：打算用 `sh:class` 约束的属性，尽量别声明 `rdfs:range`；当类归属本身就是要检验的对象时，关掉 RDFS 蕴含再跑（`inference="none"`）；或者把检查改写成蕴含无法自行满足的约束（比如字面量属性约束）。注意代价：关掉蕴含后，`sh:targetClass` 不再覆盖子类，子类层次需要显式标注类型，或者选用感知推理的 target 写法。Semantica 自己的 `run_shacl_validation` 包装已经以 `inference="none"` 调用 pyshacl，所以只有直接调用 `pyshacl.validate` 且开着蕴含时才会踩中这个坑。
- **不查推理模式就轻信 `conforms: True`**：开启推理的运行可能恰好把形状要抓的那些违规藏起来（见上条）。把每次校验使用的推理模式记录在结果旁边；对含 `sh:class`/`sh:node` 的形状集，先关掉蕴含重跑一遍，再把通过当作最终结论。

---

## 领域示例

<Tabs>

<Tab title="国防——CTI/威胁情报">

国防部的网络威胁情报(CTI)团队在向 ISAC 伙伴共享威胁图之前，先对其施加兼容 STIX 的约束：每个 `ThreatActor` 必须声明 `name`，每个 `Vulnerability` 必须带 `cvss_score`。这道校验门禁在每晚同步时自动运行。

```python
from semantica.context import AgentContext, ContextGraph
from semantica.vector_store import VectorStore
from semantica.ontology import OntologyGenerator, SHACLGenerator, PropertyShape
from semantica.ontology import run_shacl_validation

graph = ContextGraph()
ctx   = AgentContext(
    vector_store=VectorStore(backend="faiss", dimension=768),
    knowledge_graph=graph,
    graph_expansion=True,
)

ctx.store([
    "APT29 is a Russian state-sponsored threat actor targeting NATO governments.",
    "CVE-2024-3400 is a critical PAN-OS vulnerability with CVSS 10.0, exploited by APT29.",
    "HAMMERTOSS is a backdoor malware family used by APT29 for C2 over Twitter and GitHub.",
], extract_entities=True, extract_relationships=True)

ontology  = (
    OntologyGenerator(base_uri="https://cti.dod.mil/ontology/", min_occurrences=1)
    .generate_from_graph(graph.to_dict(), name="CTIOntology")
)

shacl_gen   = SHACLGenerator(
    base_uri="https://cti.dod.mil/shapes/",
    include_inherited=True,
    severity="Violation",
)
shacl_graph = shacl_gen.generate(ontology)

# STIX-aligned mandatory fields
for ns in shacl_graph.node_shapes:
    if "ThreatActor" in ns.target_class:
        ns.property_shapes.append(
            PropertyShape(path="https://cti.dod.mil/ontology/name",         min_count=1, severity="Violation")
        )
        ns.property_shapes.append(
            PropertyShape(path="https://cti.dod.mil/ontology/nation_state",  min_count=1, severity="Warning")
        )
    if "Vulnerability" in ns.target_class:
        ns.property_shapes.append(
            PropertyShape(path="https://cti.dod.mil/ontology/cvss_score",   min_count=1, severity="Violation")
        )

shacl_ttl = shacl_gen.serialize(shacl_graph, format="turtle")

# Prepare RDF data string
data_ttl = """
@prefix ex: <https://cti.dod.mil/ontology/> .

<http://example.org/apt29> a ex:ThreatActor .
<http://example.org/cve-2024-3400> a ex:Vulnerability .
<http://example.org/hammertoss> a ex:Malware .
"""

report = run_shacl_validation(data_ttl, shacl_ttl)
print(f"CTI graph conforms : {report.conforms}")
print(f"Violations         : {report.violation_count}")
print(f"Warnings           : {report.warning_count}")

if not report.conforms:
    report.explain_violations()
    for v in report.violations:
        print(v.explanation)
    # Blocks the nightly ISAC share until violations are resolved
```

</Tab>

<Tab title="安全——SOC/事件响应">

SOC 团队在把零信任策略节点发布到策略执行点之前先做校验：每个 `Policy` 节点必须带 `version`（semver 格式）和 `effective_date`。缺任何一个字段都是 Violation 级违规，发布即被拦截。

```python
from semantica.context import ContextGraph
from semantica.ontology import OntologyGenerator, SHACLGenerator, PropertyShape
from semantica.ontology import run_shacl_validation

graph = ContextGraph()
graph.add_node("policy-001", "Policy", "MFA Required for Tier-1 Resources",
               version="1.0.0", effective_date="2025-01-01", owner="security_team")
graph.add_node("policy-002", "Policy", "Admin Access Requires PAM Checkout")
# policy-002 has no version or effective_date — Violations expected

ontology = (
    OntologyGenerator(base_uri="https://zerotrust.corp/ontology/", min_occurrences=1)
    .generate_from_graph(graph.to_dict(), name="ZeroTrustOntology")
)

shacl_gen   = SHACLGenerator(base_uri="https://zerotrust.corp/shapes/", severity="Violation")
shacl_graph = shacl_gen.generate(ontology)

BASE = "https://zerotrust.corp/ontology/"
for ns in shacl_graph.node_shapes:
    if "Policy" in ns.target_class:
        ns.property_shapes += [
            PropertyShape(
                path=f"{BASE}version",
                min_count=1,
                pattern=r"^\d+\.\d+\.\d+$",   # semver
                severity="Violation",
            ),
            PropertyShape(
                path=f"{BASE}effective_date",
                min_count=1,
                datatype="http://www.w3.org/2001/XMLSchema#date",
                severity="Violation",
            ),
        ]

shacl_ttl = shacl_gen.serialize(shacl_graph, format="turtle")

# Prepare RDF data string
data_ttl = """
@prefix ex: <https://zerotrust.corp/ontology/> .

<http://example.org/policy-001> a ex:Policy ;
    ex:version "1.0.0" ;
    ex:effective_date "2025-01-01"^^<http://www.w3.org/2001/XMLSchema#date> .

<http://example.org/policy-002> a ex:Policy .
"""

report = run_shacl_validation(data_ttl, shacl_ttl)
print(f"Policy graph conforms: {report.conforms}")
# Policy graph conforms: False

for v in report.violations:
    print(f"  VIOLATION: {v.focus_node}  —  {v.result_path}  —  {v.message}")
# VIOLATION: ...policy-002 — ...version       — Less than 1 values on ...version
# VIOLATION: ...policy-002 — ...effective_date — Less than 1 values on ...effective_date
```

</Tab>

<Tab title="生命科学——临床/制药">

临床信息学团队在把试验本体节点装入试验登记系统之前先做校验：每个 `ClinicalTrial` 节点必须声明 `phase`（I–IV 期之一）、`primary_endpoint` 和 `principal_investigator`。缺任何一项都无法提交登记。

```python
from semantica.ontology import LLMOntologyGenerator, SHACLGenerator, PropertyShape
from semantica.ontology import run_shacl_validation
from semantica.export import export_rdf
import tempfile, os

llm_gen  = LLMOntologyGenerator(provider="openai", model="gpt-4o")
ontology = llm_gen.generate_ontology_from_text(
    """
    A phase II oncology trial studies the efficacy of Compound XR-401 in NSCLC patients.
    The trial is led by Principal Investigator Dr. Sarah Chen at Memorial Sloan Kettering.
    Primary endpoint: overall response rate at 24 weeks.
    Secondary endpoint: progression-free survival.
    """
)

shacl_gen   = SHACLGenerator(base_uri="https://purl.obolibrary.org/obo/TRIAL_shapes/")
shacl_graph = shacl_gen.generate(ontology)

TRIAL = "https://purl.obolibrary.org/obo/TRIAL_"
for ns in shacl_graph.node_shapes:
    if "ClinicalTrial" in ns.target_class or "Trial" in ns.target_class:
        ns.property_shapes += [
            PropertyShape(
                path=f"{TRIAL}phase",
                min_count=1,
                in_values=["Phase I", "Phase II", "Phase III", "Phase IV"],
                severity="Violation",
            ),
            PropertyShape(
                path=f"{TRIAL}primary_endpoint",
                min_count=1,
                severity="Violation",
            ),
            PropertyShape(
                path=f"{TRIAL}principal_investigator",
                min_count=1,
                severity="Warning",
            ),
        ]

shacl_ttl = shacl_gen.serialize(shacl_graph, format="turtle")
print(f"SHACL shapes generated — {len(shacl_graph.node_shapes)} node shapes")
# SHACL shapes generated — 5 node shapes

# Validate trial data
# Serialize the ontology as data to validate against the shapes
tmp = tempfile.NamedTemporaryFile(suffix=".ttl", delete=False)
tmp.close()
export_rdf(ontology, tmp.name, format="turtle")
with open(tmp.name) as f:
    data_ttl = f.read()
os.unlink(tmp.name)

report = run_shacl_validation(data_ttl, shacl_ttl)
print(f"Trial data conforms: {report.conforms}")
print(f"Warnings           : {report.warning_count}")
```

</Tab>

<Tab title="银行——风险/合规">

信贷风险团队在贷款申请进入信贷模型之前，按巴塞尔协议 III CRE20 的必填字段（`ltv`、`pd`、`lgd`、`asset_class`）校验每个 `LoanApplication` 节点。缺任何一个字段都是 Violation 级违规，该记录直接被拒。

```python
from semantica.context import ContextGraph
from semantica.ontology import OntologyGenerator, SHACLGenerator, PropertyShape
from semantica.ontology import run_shacl_validation

graph = ContextGraph()
graph.add_node("loan-001", "LoanApplication", "Prime mortgage APP-2025-88421",
               ltv=0.78, pd=0.023, lgd=0.45, asset_class="CRE")
graph.add_node("loan-002", "LoanApplication", "SME working capital facility",
               ltv=0.65)
# loan-002 is missing pd, lgd, asset_class — three Violations expected

ontology = (
    OntologyGenerator(base_uri="https://basel.eba.eu/ontology/", min_occurrences=1)
    .generate_from_graph(graph.to_dict(), name="BaselRiskOntology")
)

shacl_gen   = SHACLGenerator(base_uri="https://basel.eba.eu/shapes/", severity="Violation")
shacl_graph = shacl_gen.generate(ontology)

BASE = "https://basel.eba.eu/ontology/"
for ns in shacl_graph.node_shapes:
    if "LoanApplication" in ns.target_class:
        for field in ["ltv", "pd", "lgd", "asset_class"]:
            ns.property_shapes.append(
                PropertyShape(
                    path=f"{BASE}{field}",
                    min_count=1,
                    severity="Violation",
                )
            )

shacl_ttl = shacl_gen.serialize(shacl_graph, format="turtle")

# Prepare RDF data string
data_ttl = """
@prefix ex: <https://basel.eba.eu/ontology/> .

<http://example.org/loan-001> a ex:LoanApplication ;
    ex:ltv "0.78" ;
    ex:pd "0.023" ;
    ex:lgd "0.45" ;
    ex:asset_class "CRE" .

<http://example.org/loan-002> a ex:LoanApplication ;
    ex:ltv "0.65" .
"""

report = run_shacl_validation(data_ttl, shacl_ttl)
print(f"Loan portfolio conforms: {report.conforms}")
# Loan portfolio conforms: False

print(f"Violations             : {report.violation_count}")
# Violations             : 3

for v in report.violations:
    print(f"  [{v.severity}]  {v.focus_node.split('/')[-1]}  —  {v.result_path.split('/')[-1]}")
# [Violation]  loan-002 — pd
# [Violation]  loan-002 — lgd
# [Violation]  loan-002 — asset_class

# Export violation report for regulatory audit trail
report_dict = report.to_dict()
```

</Tab>

</Tabs>

---

## 资源限制

Explorer 内的实时 SHACL 校验设有四项资源限制，全部可以通过环境变量配置。触发限制时，报错信息会指明对应的环境变量。

| 环境变量 | 默认值 | 限制的对象 |
| --- | --- | --- |
| `SEMANTICA_MAX_SHACL_TURTLE_BYTES` | `262144`（256 KB） | 提交的 SHACL Turtle 大小 |
| `SEMANTICA_MAX_SHACL_TRIPLES` | `1000` | 解析后形状图的三元组数量 |
| `SEMANTICA_MAX_SHACL_TIMEOUT` | `15.0` | 校验超时时间（秒） |
| `SEMANTICA_MAX_SHACL_CONCURRENCY` | `4` | 每个进程的并发校验数 |

前三项超限时会在校验报错信息中体现；并发限制以信号量方式生效，不会出现在响应里。

## 把 SHACL 校验用作 CI/CD 门禁

把这个函数用作发布前门禁；退出码 1 会阻断流水线。

```python
import sys
from semantica.ontology import OntologyGenerator, SHACLGenerator
from semantica.ontology import run_shacl_validation

def validate_before_publish(data_graph_str: str, ontology: dict) -> None:
    shacl_gen   = SHACLGenerator(base_uri="https://example.org/shapes/")
    shacl_graph = shacl_gen.generate(ontology)
    shacl_ttl   = shacl_gen.serialize(shacl_graph, format="turtle")

    report = run_shacl_validation(data_graph_str, shacl_ttl)

    if not report.conforms:
        print(f"Graph validation FAILED — {report.violation_count} violation(s)")
        report.explain_violations()
        for v in report.violations:
            print(v.explanation)
        sys.exit(1)

    print(f"Graph validation PASSED ({report.warning_count} warning(s))")
```

---

## 相关指南

- [本体管理](./ontology.md) — 生成 SHACL 形状所源自的 OWL 本体
- [推理与规则](./reasoning.md) — 用逻辑推理规则补充 SHACL 的结构约束
- [导出与序列化](./export.md) — 把图数据序列化为 Turtle/RDF/XML，作为 `run_shacl_validation` 的输入
- [冲突消解](./conflict-resolution.md) — 在 SHACL 校验之前检测并消解数据冲突
- [变更管理](./change-management.md) — 让 SHACL 形状与本体版本一起做版本门禁
