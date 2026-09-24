---
title: "本体模块（Ontology）"
description: "自动化本体生成、SHACL 校验、OWL/RDF 导出、命名空间管理，以及基于 LLM 的本体生成。"
source: reference/ontology.md
source_version: 889559c3c2884a91e1a4f000ab2bc88da49c74a0
icon: "sitemap"
---

`semantica.ontology` 覆盖知识图谱(Knowledge Graph)模式的完整生命周期：

- 通过 5 阶段流水线从 KG 数据自动生成本体(Ontology)（语义网络 → YAML → 类型 → 层级 → TTL）
- 复杂领域可用 `LLMOntologyGenerator` 做基于大语言模型(LLM)的本体生成
- SHACL 校验：生成形状(Shape)、校验图、产出违规报告
- 支持导出网络本体语言(OWL)与资源描述框架(RDF)，可选 Turtle、RDF/XML 和 JSON-LD 三种格式
- `semantica.explorer` 提供本体中心(Ontology Hub)可视化编辑器（v0.5.0）


## 导出的类

| 类 | 职责 |
| :--- | :--- |
| `OntologyEngine` | 协调本体完整生命周期的统一门面 |
| `OntologyGenerator` | 从 KG 数据自动生成本体（5 阶段流水线） |
| `LLMOntologyGenerator` | 复杂领域的 LLM 驱动本体生成 |
| `SHACLGenerator` | 从本体或 KG 模式生成 SHACL 形状 |
| `OntologyValidator` | 用 SHACL 形状校验任意图：返回 `SHACLValidationReport` |
| `OntologyQualityGate` | 为 CI 运行确定性的本体/KG 质量检查 |
| `OWLGenerator` | 把本体序列化为 Turtle、RDF/XML、JSON-LD |
| `NamespaceManager` | IRI 生成、前缀管理与命名空间绑定 |
| `OntologyEvaluator` | 覆盖率、完整度与粒度质量指标 |
| `ClassInferrer` | 从实体类型模式推断类 |
| `PropertyGenerator` | 从实体属性和关系生成属性 |
| `AssociativeClassBuilder` | 把 N 元关系建模为中间 OWL 类 |


## 快速开始

**`OntologyEngine`** 是完整本体工作流的主入口：

```python
from semantica.ontology import OntologyEngine

# Initialize with base URI for your domain
engine = OntologyEngine(base_uri="https://example.org/ontology/")

# Generate ontology from your knowledge graph data
ontology = engine.from_data({"entities": entities, "relationships": relationships})

# Validate a graph against the generated SHACL shapes
report = engine.validate_graph(kg, ontology=ontology)
if not report.conforms:
    for v in report.violations:
        print(f"{v.severity}: {v.message} on {v.focus_node}")

# Export to OWL Turtle
engine.export_owl(ontology, "ontology.ttl", format="turtle")
```

## OntologyEngine（统一门面）

**`OntologyEngine`** 协调本体的完整生命周期，覆盖**生成、校验、导出与评估**四个环节：

```python
from semantica.ontology import OntologyEngine

engine = OntologyEngine(base_uri="https://example.org/ontology/")

# Generate ontology from KG data
ontology = engine.from_data({"entities": entities, "relationships": relationships})

# Validate a graph against the generated SHACL shapes
report = engine.validate_graph(kg, ontology=ontology)
if not report.conforms:
    for v in report.violations:
        print(f"{v.severity}: {v.message} on {v.focus_node}")

# Export to OWL Turtle
engine.export_owl(ontology, "ontology.ttl", format="turtle")
```

### OntologyEngine 方法

| 方法 | 说明 |
| :------ | :----------- |
| `from_data(data)` | 对实体/关系数据运行 5 阶段流水线 |
| `validate_graph(kg, ontology=...)` | 用生成的 SHACL 形状校验知识图谱 |
| `quality_check(ontology, graph_data=...)` | 返回确定性的质量报告与 CI 友好的通过/失败结果 |
| `export_owl(ontology, path, format)` | 序列化为 `"turtle"`、`"xml"` 或 `"json-ld"` |
| `evaluate(ontology, kg)` | 计算覆盖率、完整度与粒度指标 |

### 本体质量门(Quality Gate)

可以把质量门理解成部署前的体检：只查出问题，不替你改数据。具体来说，在导出或部署前用它捕捉结构性问题，而且不引入任何运行时依赖：

```python
from semantica.ontology import ontology_quality_check

report = ontology_quality_check(
    ontology,
    graph_data=kg,
    thresholds={"min_coverage": 0.8},
)

if not report.passed:
    for issue in report.issues:
        print(issue.code, issue.message)
```

报告检查类/属性的覆盖率、孤立的模式元素、定义域和值域引用，以及未解析的 KG 关系端点。它输出机器可读的问题代码、严重级别、计数、指标和阈值失败项。第一版只报告发现，不自动修数据。

### 阈值

`min_coverage`（默认 `0.0`）给 `coverage` 分数（类覆盖与属性覆盖的平均值，取值 `0.0` 到 `1.0`）设了下限；分数低于它，质量门就判失败。`max_errors`（默认 `0.0`）限制允许的 `error`/`critical` 级问题数量，超出即失败。`max_warnings`（默认 `None`）以同样方式限制 `warning` 级问题，`None` 表示仅 warning 永远不会让质量门失败。`fail_on_warnings` 是独立参数，不是 `thresholds` 键，要直接传给 `OntologyQualityGate(...)` 或 `.check(...)`。设为 `True` 时，无论 `max_warnings` 是多少，一条 warning 就足以让质量门失败。

## OntologyGenerator（5 阶段流水线）

**`OntologyGenerator`** 从知识图谱的实体和关系自动生成形式化本体：

```python
from semantica.ontology import OntologyGenerator

generator = OntologyGenerator(base_uri="https://example.org/ontology/")
ontology  = generator.generate_ontology({
    "entities":      entities,
    "relationships": relationships,
})
```

简单说，这条流水线就是把图数据里现成的实体类型和关系模式，一步步提炼成一份正式的本体。

<Steps>
  <Step title="语义网络解析">
    从源数据的实体类型和关系结构中抽取概念与模式。
  </Step>
  <Step title="YAML 转定义">
    把抽取到的模式转换为中间的类与属性定义。
  </Step>
  <Step title="定义转类型">
    把定义映射为 OWL 构件：`owl:Class`、`owl:ObjectProperty`、`owl:DatatypeProperty`。
  </Step>
  <Step title="层级生成">
    用传递闭包和环检测构建分类树：产出 `rdfs:subClassOf` 链。
  </Step>
  <Step title="TTL 生成">
    用 `rdflib` 把最终本体序列化为 Turtle 格式。另支持 RDF/XML 和 JSON-LD。
  </Step>
</Steps>

## SHACL 校验

从本体生成 SHACL 形状，再用它们校验任意图：

```python
from semantica.ontology import SHACLGenerator, OntologyValidator, SHACLValidationReport, SHACLViolation

# Generate shapes from ontology
generator  = SHACLGenerator()
shapes     = generator.generate(ontology)
shapes_ttl = shapes.serialize(format="turtle")

# Validate a graph against the shapes
validator = OntologyValidator()
report: SHACLValidationReport = validator.validate_graph(kg, ontology=ontology)

if not report.conforms:
    violation: SHACLViolation
    for violation in report.violations:
        print(f"{violation.severity}: {violation.message}")
        print(f"  Node: {violation.focus_node}")
        print(f"  Path: {violation.result_path}")
```

### 校验报告字段

| 字段 | 类型 | 说明 |
| :----- | :---- | :----------- |
| `conforms` | `bool` | 图通过全部 SHACL 约束时为 `True` |
| `violations` | `List[SHACLViolation]` | 详细的失败记录 |
| `focus_node` | `str` | 违规图节点的 IRI |
| `result_path` | `str` | 违规属性路径的 IRI |
| `severity` | `str` | `"Violation"`、`"Warning"` 或 `"Info"` |
| `message` | `str` | 人类可读的约束失败描述 |

## 基于 LLM 的本体生成

适用于模式难以统计推断的复杂或全新领域：

```python
from semantica.ontology import LLMOntologyGenerator

# Initialize with your preferred LLM provider
generator = LLMOntologyGenerator(provider="openai")  # or "anthropic", "groq", etc.
ontology  = generator.generate_ontology_from_text(
    text="A biomedical ontology for clinical trial protocols involving patients, trials, interventions, and outcomes."
)
```

## OWL / RDF 导出

```python
from semantica.ontology import OWLGenerator

generator = OWLGenerator()
generator.export_owl(ontology, path="ontology.ttl",  format="turtle")
generator.export_owl(ontology, path="ontology.owl",  format="xml")
generator.export_owl(ontology, path="ontology.json", format="json-ld")
```

## 命名空间管理

```python
from semantica.ontology import NamespaceManager

ns = NamespaceManager(base_uri="https://example.org/")
ns.register("ex",     "https://example.org/")
ns.register("schema", "https://schema.org/")
ns.register("owl",    "http://www.w3.org/2002/07/owl#")

# Generate IRIs for classes and properties
class_iri    = ns.generate_class_iri("Person")
property_iri = ns.generate_property_iri("worksFor")
```

## 本体评估

度量所生成本体的覆盖率、完整度与粒度：

```python
from semantica.ontology import OntologyEvaluator

evaluator = OntologyEvaluator()
result    = evaluator.evaluate_ontology(ontology, kg)

print(f"Class coverage:    {result.class_coverage:.2f}")
print(f"Property coverage: {result.property_coverage:.2f}")
print(f"Completeness:      {result.completeness:.2f}")
print(f"Granularity:       {result.granularity:.2f}")

for gap in result.gaps:
    print(f"Gap: {gap.description}")
```

## 常见工作流

<Tabs>
  <Tab title="快速上手">
    **三步生成并校验一个本体：**

    ```python
    from semantica.ontology import OntologyEngine

    # 1. Initialize engine
    engine = OntologyEngine(base_uri="https://yourcompany.com/ontology/")

    # 2. Generate from your data
    ontology = engine.from_data({"entities": entities, "relationships": relationships})

    # 3. Validate against a knowledge graph
    report = engine.validate_graph(kg, ontology=ontology)
    if report.conforms:
        print("✓ Graph conforms to ontology")
    else:
        print(f"✗ Found {len(report.violations)} violations")
    ```
  </Tab>
  <Tab title="LLM 驱动生成">
    **从文本描述生成本体：**

    ```python
    from semantica.ontology import LLMOntologyGenerator

    generator = LLMOntologyGenerator(provider="openai")
    ontology = generator.generate_ontology_from_text("""
        Create an e-commerce ontology with products, customers, orders, 
        categories, reviews, and payment methods.
    """)

    # Refine with additional constraints
    engine = OntologyEngine()
    validated = engine.validate(ontology)
    ```
  </Tab>
  <Tab title="导出与集成">
    **以多种格式导出本体：**

    ```python
    from semantica.ontology import OntologyEngine

    engine = OntologyEngine()

    # Export as OWL/Turtle for Protégé
    engine.export_owl(ontology, "schema.ttl", format="turtle")

    # Export as JSON-LD for web applications
    engine.export_owl(ontology, "schema.jsonld", format="json-ld")

    # Generate SHACL shapes for validation
    engine.export_shacl(ontology, "shapes.ttl")
    ```
  </Tab>
</Tabs>

## 摄取已有本体

加载并解析本体文件供下游使用：

```python
from semantica.ontology import ingest_ontology

ontology_data = ingest_ontology("schema.ttl")     # Turtle
ontology_data = ingest_ontology("schema.owl")     # OWL/XML
ontology_data = ingest_ontology("schema.jsonld")  # JSON-LD
```

<Note>
  本体版本管理（`VersionManager`、`OntologyVersion`）已迁移到 `semantica.change_management`。请从那里导入：`from semantica.change_management import VersionManager`。
</Note>

- [Reasoning](./reasoning.md) — 对本体公理应用推理规则。
- [Knowledge Graph](./kg.md) — 本体所建模的图。
- [Export](./export.md) — 以 RDF、OWL 或 JSON-LD 导出本体。
- [Conflicts](./conflicts.md) — 检测本体约束违规。
