---
title: "种子数据模块（Seed）"
description: "从经过验证的结构化来源引导知识图谱：分类体系、参考表、产品目录和领域锚点。"
source: reference/seed.md
source_version: 2e65b21e41be672567fe589c58086162747f41f5
icon: "database"
---

**`semantica.seed`** 给你的知识图谱一个**可靠、经过验证的起点**：

- 先装载经过验证的参考数据：ISO 代码、员工名册、产品目录、领域分类体系
- `SeedDataManager` 把新抽取的数据合并到基础节点上，不产生重复
- 支持 JSON、CSV 和以编程方式注册种子来源
- 从结构化种子数据生成确定性的测试图
- 把实体抽取锚定到已知实体上，减少幻觉和重复节点


## 导出的类

| 类 | 职责 |
| :--- | :--- |
| `SeedDataManager` | 协调器：`register_source`、`load_source`、`create_foundation_graph`、`integrate_with_extracted` |
| `SeedDataSource` | 配置 dataclass：`{name, format, location, entity_type, verified, version, metadata}` |
| `SeedData` | 容器 dataclass：`{entities, relationships, properties, metadata}` |

## 你能得到什么

- **SeedDataManager** — 注册来源、构建基础图、校验质量、与抽取数据合并。
- **SeedDataSource** — 类型化的来源定义：支持 CSV、JSON、SQL、API，带各格式专属配置。
- **基础图(Foundation Graph)** — 一次遍历全部已注册来源构建基础图，随时可与抽取数据合并。
- **合并策略** — `seed_first`、`extracted_first`、`merge`，带属性级冲突检测。
- **校验** — 装载前的必填字段检查、ID 唯一性、类型一致性、引用完整性和编码校验。
- **版本管理** — 跨流水线运行追踪种子数据版本，并对比版本间差异。

<Tip>
  **何时用种子数据模块：**用结构化参考数据做引导（分类体系、用户名单、产品目录）、装载抽取数据不应覆盖的不可变事实（ISO 国家代码、标准本体术语）、用确定性数据集保证测试可复现、用规范形式锚定实体消歧。
</Tip>

## 快速开始

<Steps>
  <Step title="注册种子来源">
    ```python
    from semantica.seed import SeedDataManager

    manager = SeedDataManager()

    manager.register_source("countries",  "csv",  "data/countries.csv")
    manager.register_source("taxonomy",   "json", "data/taxonomy.json")
    manager.register_source("employees",  "csv",  "data/employees.csv")
    ```

    <Tip>
      **调用 `create_foundation_graph()` 之前先注册全部来源。**`create_foundation_graph()` 一次遍历处理所有已注册来源。之后才注册的来源会被静默排除。在脚本开头注册全部来源，然后只调用一次 `create_foundation_graph()`。
    </Tip>
  </Step>
  <Step title="构建基础图">
    ```python
    foundation_kg = manager.create_foundation_graph()
    print(f"Foundation nodes: {len(foundation_kg['entities'])}")
    print(f"Foundation edges: {len(foundation_kg['relationships'])}")
    ```
  </Step>
  <Step title="装载前先校验">
    ```python
    # Note: validate_quality expects a graph dict, but load_source returns a list.
    # For demonstration, validate the foundation graph instead.
    report = manager.validate_quality(foundation_kg)
    if not report["valid"]:
        for error in report["errors"]:
            print(f"Error: {error}")
        for warning in report["warnings"]:
            print(f"Warning: {warning}")
    else:
        print(f"Validated {report['metrics']['entity_count']} entities: no issues found")
    ```

    <Warning>
      **装载前先校验。**`manager.validate_quality(seed_data)` 能在缺必填字段、类型不一致、ID 重复破坏你的图之前把它们捕获。装载之后才校验就意味着要回滚。校验很快：永远先校验。
    </Warning>
  </Step>
  <Step title="与抽取数据合并">
    ```python
    from semantica.semantic_extract import NERExtractor

    extractor = NERExtractor(method="ml")
    new_entities = extractor.extract("Apple Inc. partners with Microsoft Corp.")
    
    # Merge with seed data - note the correct parameter names
    final_kg = manager.integrate_with_extracted(
        seed_data=foundation_kg,
        extracted_data={"entities": new_entities, "relationships": []},
        merge_strategy="merge"
    )
    ```

    <Warning>
      **先装载种子数据，再装载抽取数据。**种子数据是你的地面真值(ground truth)：规范化、人工整理、已去重。先用 `create_foundation_graph()` 装载，再把抽取的实体合并上去。顺序反了，带噪的抽取数据就会覆盖可信的参考值。
    </Warning>
  </Step>
</Steps>

## SeedDataSource 类型

<Tabs>
  <Tab title="CSV">
    ```python
    from semantica.seed import SeedDataSource, SeedDataManager

    csv_source = SeedDataSource(
        name="employees",
        format="csv",
        location="data/employees.csv",
        entity_type="Person",
        verified=True,
        metadata={"description": "Company employee list with titles and departments"}
    )

    manager = SeedDataManager()
    manager.register_source(
        "employees", "csv", "data/employees.csv", entity_type="Person", verified=True
    )
    ```
  </Tab>
  <Tab title="JSON">
    ```python
    json_source = SeedDataSource(
        name="taxonomy",
        format="json",
        location="knowledge/taxonomy.json",
        entity_type="Concept",
        relationship_type="subclass_of",
        verified=True,
        metadata={"version": "2.1", "source": "domain_expert"}
    )

    manager.register_source(
        "taxonomy", "json", "knowledge/taxonomy.json",
        entity_type="Concept", relationship_type="subclass_of"
    )
    ```
  </Tab>
  <Tab title="数据库">
    ```python
    db_source = SeedDataSource(
        name="geographic",
        format="database",
        location="postgresql://user:pass@host/geonames",
        entity_type="Location",
        verified=False,  # needs validation
        metadata={"table": "countries", "last_sync": "2024-01-15"}
    )

    manager.register_source(
        "geographic", "database", "postgresql://user:pass@host/geonames",
        entity_type="Location", verified=False
    )
    ```
  </Tab>
  <Tab title="API">
    ```python
    api_source = SeedDataSource(
        name="wikidata",
        format="api",
        location="https://wikidata.org/sparql",
        entity_type="Entity",
        metadata={"auth_required": False, "rate_limit": 60}
    )

    manager.register_source(
        "wikidata", "api", "https://wikidata.org/sparql",
        entity_type="Entity"
    )
    ```
  </Tab>
</Tabs>

## SeedDataManager 参考

| 方法 | 说明 |
| :------ | :----------- |
| `register_source(name, format, location, **config)` | 向管理器添加新数据来源 |
| `load_source(source_name)` | 装载并返回已注册来源的原始数据 |
| `create_foundation_graph()` | 从全部已注册来源构建初始图 |
| `integrate_with_extracted(seed_data, extracted_data, merge_strategy)` | 把种子数据与新抽取的实体/关系合并 |
| `validate_quality(seed_data)` | 检查数据完整性并返回校验报告 |
| `export_seed_data(path, format)` | 把处理后的种子数据存到文件 |

`integrate_with_extracted()` 处理冲突的不同策略：

<Tabs>
  <Tab title="seed_first">
    **冲突时种子数据胜出**：优先保留人工整理的关系，而不是抽取的关系。

    ```python
    final_kg = manager.integrate_with_extracted(
        seed_data=foundation_kg,
        extracted_data=new_data,
        merge_strategy="seed_first"
    )
    ```

    种子数据可信度高、抽取只是探索性时用。
  </Tab>
  <Tab title="extracted_first">
    **冲突时抽取数据胜出**：用新鲜信息覆盖种子数据。

    ```python
    final_kg = manager.integrate_with_extracted(
        seed_data=foundation_kg,
        extracted_data=new_data,
        merge_strategy="extracted_first"
    )
    ```

    已知抽取质量好、需要快速原型时用。
  </Tab>
  <Tab title="merge">
    **智能冲突消解**：合并互补属性，实体去重。

    ```python
    final_kg = manager.integrate_with_extracted(
        seed_data=foundation_kg,
        extracted_data=new_data,
        merge_strategy="merge"
    )
    ```

    种子和抽取数据都有价值的生产流水线用。
  </Tab>
</Tabs>

<Tip>
  **参考数据用 `seed_first` 合并策略。**种子数据编码的是权威事实（公司官方名称、规范分类 ID、员工记录）时，`merge_strategy="seed_first"` 保证这些值胜过抽取值。只有抽取数据可能比种子更新时才用 `merge`。
</Tip>

## 完整流水线示例

```python
from semantica.seed import SeedDataManager
from semantica.parse import DocumentParser
from semantica.split import TextSplitter
from semantica.semantic_extract import NERExtractor, RelationExtractor

# Initialize components
manager   = SeedDataManager()
parser    = DocumentParser()
splitter  = TextSplitter(method="sentence", chunk_size=200)
ner       = NERExtractor(method="ml")
rel_ext   = RelationExtractor(method="ml")

# Register seed sources
manager.register_source("taxonomy", "json", "seeds/domain_taxonomy.json")
manager.register_source("entities", "csv",  "seeds/known_entities.csv")

# Create foundation
foundation_kg = manager.create_foundation_graph()
print(f"Foundation: {len(foundation_kg['entities'])} entities, {len(foundation_kg['relationships'])} relationships")

# Process new document
parsed = parser.parse("research_paper.pdf")
chunks = splitter.split(parsed["full_text"])

# Extract from each chunk
all_entities = []
all_relations = []
for chunk in chunks:
    entities = ner.extract(chunk.text)
    relations = rel_ext.extract(chunk.text)
    all_entities.extend(entities)
    all_relations.extend(relations)

# Merge with foundation
extracted_data = {"entities": all_entities, "relationships": all_relations}
final_kg = manager.integrate_with_extracted(
    seed_data=foundation_kg,
    extracted_data=extracted_data,
    merge_strategy="merge"
)

print(f"Final graph: {len(final_kg['entities'])} entities, {len(final_kg['relationships'])} relationships")

# Export for downstream use
manager.export_seed_data("output/enriched_kg.json", format="json")
```

## YAML 配置

生产部署在 YAML 里定义来源：切换环境不用改代码：

```yaml
seed:
  sources:
    - name: "employees"
      format: "csv"
      location: "./data/employees.csv"
      config:
        id_column: "employee_id"
        type: "Person"
    - name: "taxonomy"
      format: "json"
      location: "./data/taxonomy.json"
    - name: "products"
      format: "sql"
      location: "${DATABASE_URL}"
      config:
        query: "SELECT id, name, category FROM products WHERE active = true"
  merge:
    strategy: "merge"
  validation:
    strict: true
    required_fields: ["id", "type"]
```

环境变量覆盖：

```bash
export SEMANTICA_SEED_DATA_DIR=./data/seed
export SEMANTICA_SEED_MERGE_STRATEGY=seed_first
```

<Tip>
  **生产部署用 YAML 配置。**把来源路径硬编码进 Python 脚本，环境切换（dev → staging → prod）会很脆弱。在 `config.yaml` 的 `seed:` 键下声明来源，用 `SEMANTICA_SEED_DATA_DIR` 覆盖路径。这样同一份代码在每个环境都能跑。
</Tip>

- [Ingest](./ingest.md) — 在种子数据之外装载非结构化数据。
- [Knowledge Graph](./kg.md) — 种子数据要填充的目标图。
- [Deduplication](./deduplication.md) — 处理种子-抽取合并中的重复项。
- [Pipeline](../../reference/pipeline.md) — 把种子装载作为命名流水线步骤。
