---
title: 图存储后端与特性矩阵
description: Semantica 支持的 LPG/RDF 图存储后端清单、各后端特性矩阵和最小连接示例。
source: storage-backends.md
source_version: dc211ef062e0f499f6fc7e3ced47edf43f11af1c
icon: "database"
---

# 图存储后端与特性矩阵

Semantica 把图建模与物理存储解耦：LPG 后端经 `graph_store` 适配器访问，RDF 后端经 `triplet_store` 适配器访问。

本页刻意保持保守：它区分"适配器存在"、"该模型下特性普遍可用"和"后端需要用户自行接线"三种状态。

## 状态标签

- `built-in`：适配器实现在 Semantica 核心中。
- `tested`：有自动化集成夹具或测试覆盖。
- `example-only`：有可用示例，但集成测试不承诺支持。
- `interface/BYO`：存在接口或集成点；后端接线由用户自备。

## 适配器清单

| 后端 | 模型 | 适配器 | 状态 | 参考材料 |
| --- | --- | --- | --- | --- |
| Neo4j | LPG | `semantica.graph_store.Neo4jStore` | built-in | `cookbook/introduction/09_Graph_Store.ipynb` |
| FalkorDB | LPG | `semantica.graph_store.FalkorDBStore` | built-in | `docs/reference/graph_store.md` |
| Amazon Neptune | LPG | `semantica.graph_store.AmazonNeptuneStore` | built-in | `cookbook/introduction/21_Amazon_Neptune_Store.ipynb` |
| Apache AGE | LPG | `semantica.graph_store.ApacheAgeStore` | built-in | `docs/graph_stores/apache_age.md` |
| RDF4J | RDF | `semantica.triplet_store.RDF4JStore` | built-in | `cookbook/introduction/20_Triplet_Store.ipynb` |
| Apache Jena | RDF | `semantica.triplet_store.JenaStore` | built-in | `cookbook/introduction/20_Triplet_Store.ipynb` |
| Blazegraph | RDF | `semantica.triplet_store.BlazegraphStore` | built-in | `cookbook/introduction/20_Triplet_Store.ipynb` |
| Anzo | RDF | `semantica.triplet_store.AnzoStore` | built-in | `cookbook/introduction/20_Triplet_Store.ipynb` |
| Oxigraph | RDF | `semantica.triplet_store.OxigraphStore` | built-in | `docs/reference/triplet_store.md` |

## 特性矩阵

`Yes` 表示该能力预期可与该适配器及图模型配合工作。`Partial` 表示该能力可用，但受模型相关约束。`BYO` 表示用户必须为该后端自行提供或验证接线。

| 后端 | 模型 | 摄取 | 上下文图构建 | 推理/分析 | 溯源 | 已知限制 |
| --- | --- | --- | --- | --- | --- | --- |
| Neo4j | LPG | Yes | Yes | Yes | Partial | 溯源与上下文元数据存为节点/边属性；需要关系属性和稳定的节点标识符。 |
| FalkorDB | LPG | Yes | Yes | Partial | Partial | 基于 Redis；溯源依赖节点/边属性，多图隔离取决于所选图名。 |
| Amazon Neptune | LPG | Yes | Yes | Partial | Partial | 使用属性图端点；AWS 认证、VPC 和端点配置可能影响本地测试。溯源依赖节点/边属性。 |
| Apache AGE | LPG | Yes | Yes | Partial | Partial | 经 PostgreSQL/AGE 运行；Cypher 兼容性和属性处理可能与独立 LPG 引擎不同。 |
| RDF4J | RDF | Yes | Partial | Partial | Partial | 上下文分离依赖命名图；三元组级溯源可能需要具体化(reification)或图级元数据。 |
| Apache Jena | RDF | Yes | Partial | Partial | Partial | 上下文分离需要命名图；后端配置与事务行为很重要。 |
| Blazegraph | RDF | Yes | Partial | Partial | Partial | 用 quads/命名图承载上下文；IRI 稳定性和图命名影响溯源。 |
| Anzo | RDF | Yes | Partial | Partial | Partial | Anzo 部署因环境而异；需验证 `dataset_uri`/graphmart 命名、命名图支持和溯源映射。 |
| Oxigraph | RDF | Yes | Partial | Partial | Partial | 嵌入式单进程存储（内存或磁盘）；支持命名图，但没有可独立扩展的独立服务进程。 |

## RDF 与 LPG 的差异

- LPG 后端把上下文和溯源存为图元素及属性。若后端不支持关系属性，部分溯源模式可能降级。
- RDF 后端依赖 IRI、命名图和可选的具体化。存储支持命名图/quads 时，上下文图和溯源最容易保留。
- 摄取在两种模型上都可用，但物理表示不同：LPG 直接存节点/边，RDF 存主语-谓语-宾语语句。
- 推理与分析应以适配器的查询能力为准，尤其是路径遍历、属性过滤和命名图查询。

## 最小连接示例

可运行的配置请优先参考所引笔记本的单元格。以下示例只展示各适配器的入口写法，不是通用连接 DSL。

### Neo4j

```python
import os
from semantica.graph_store import Neo4jStore

store = Neo4jStore(
    uri='bolt://localhost:7687',
    user='neo4j',
    password=os.environ['NEO4J_PASSWORD']
)
```

### FalkorDB

```python
from semantica.graph_store import FalkorDBStore

store = FalkorDBStore(
    host='localhost',
    port=6379,
    graph_name='semantica'
)
```

### Amazon Neptune

```python
from semantica.graph_store import AmazonNeptuneStore

store = AmazonNeptuneStore(
    endpoint='your-neptune-cluster-endpoint',
    port=8182,
    region='us-east-1'
)
```

### Apache AGE

```python
from semantica.graph_store import ApacheAgeStore

store = ApacheAgeStore(
    connection_string='host=localhost dbname=agedb user=postgres password=postgres',
    graph_name='semantica'
)
```

### RDF4J

```python
from semantica.triplet_store import RDF4JStore

store = RDF4JStore(
    endpoint='http://localhost:8080/rdf4j-server',
    repository_id='semantica'
)
```

### Apache Jena

```python
from semantica.triplet_store import JenaStore

store = JenaStore(
    endpoint='http://localhost:3030/ds'
)
```

### Blazegraph

```python
from semantica.triplet_store import BlazegraphStore

store = BlazegraphStore(
    endpoint='http://localhost:9999/blazegraph/sparql'
)
```

### Anzo

```python
from semantica.triplet_store import AnzoStore

store = AnzoStore(
    endpoint='http://anzo-host:8080',
    dataset_uri='http://cambridgesemantics.com/Graphmart/your-graphmart-id'
)
```

### Oxigraph

```python
from semantica.triplet_store import OxigraphStore

# 内存存储省略 `path`；磁盘持久化传入一个目录。
store = OxigraphStore(path='./semantica-oxigraph-data')
```

请把主机名、端口、仓库、图和凭证替换为你环境中的实际值。受监管或自托管部署应把凭证放在环境变量或密钥存储里，不要写进源代码。
