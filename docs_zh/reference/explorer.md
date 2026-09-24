---
title: "Explorer 模块（Explorer）"
description: "交互式 FastAPI 面板：知识图谱探索、本体管理与图分析。"
source: reference/explorer.md
source_version: eb56c545245181890623b2ba8d9802248031df8b
icon: "map"
---

**`semantica.explorer`** 是一个**浏览器面板**，用于探索知识图谱、管理本体和运行可视化分析：

- 索引化搜索：11.8 万节点上 0.004ms：不做全量扫描
- 本体中心(Ontology Hub)：可视化编辑器、SHACL Studio、对齐编写和健康面板
- 任意两个节点之间的双向路径查找
- WebSocket 进度流，实时监控流水线
- 启动后无需写代码：在浏览器里完成全部图探索


## 快速开始

安装、把图导出为 JSON、启动：

```bash
pip install "semantica[explorer]"
```

```python
# 1. Export your graph to a JSON file
import json
from semantica.context import ContextGraph

graph = ContextGraph()
graph.add_node("Python",  "language",  properties={"paradigm": "multi-paradigm"})
graph.add_node("FastAPI", "framework", properties={"language": "Python"})
graph.add_edge("Python", "FastAPI", "enables")
graph.save_to_file("my_graph.json")
```

```bash
# 2. Launch the Explorer
semantica-explorer --graph my_graph.json
# → Loading graph...
# → Graph loaded: 2 nodes, 1 edges
# → Semantica Explorer · http://127.0.0.1:8000
#     API docs  http://127.0.0.1:8000/docs
#     Health    http://127.0.0.1:8000/api/health
```

浏览器会自动打开 `http://127.0.0.1:8000`。交互式 API 文档在 `/docs`。

<Tip>
  `semantica.explorer` 是一个**服务器进程**，不是可导入的 Python 库。用 CLI 或 `python -m semantica.explorer` 启动。`app.py` 模块提供模块级 `app` 实例，供 uvicorn 或 Docker 直接使用。
</Tip>

## 启动

<Steps>
  <Step title="保存图并启动 Explorer">
    ```python
    from semantica.context import ContextGraph

    graph = ContextGraph()
    graph.load_from_file("my_graph.json")   # verify graph loads
    ```

    ```bash
    semantica-explorer --graph my_graph.json
    # Serves at http://127.0.0.1:8000
    ```
  </Step>
  <Step title="自定义主机和端口">
    ```bash
    # Expose on the network
    semantica-explorer --graph my_graph.json --host 0.0.0.0 --port 8080

    # Skip auto-opening the browser
    semantica-explorer --graph my_graph.json --no-browser
    ```
  </Step>
  <Step title="不重启就导入新数据">
    ```bash
    # Import a JSON or CSV file into the running session
    curl -X POST http://localhost:8000/api/import \
      -F "file=@updated_graph.json"
    ```
  </Step>
  <Step title="经 Python 模块使用">
    ```bash
    python -m semantica.explorer --graph my_graph.json --port 8080
    ```
  </Step>
</Steps>

## CLI 参考

`semantica-explorer` 命令只接受四个旗标：

| 旗标 | 短选项 | 默认值 | 说明 |
| :---- | :----- | :------- | :----------- |
| `--graph` | `-g` | *（**必填**）* | 要加载的 ContextGraph JSON 文件路径 |
| `--port` | `-p` | `8000` | 服务器绑定端口 |
| `--host` | | `127.0.0.1` | 服务器绑定主机：对外暴露用 `0.0.0.0` |
| `--no-browser` | | 关闭 | 跳过自动打开浏览器标签页 |

<Note>
  CLI 没有认证、CORS 或日志级别旗标。CORS 允许的来源经 `EXPLORER_CORS_ORIGINS` 环境变量配置（逗号分隔，默认 `http://localhost:5173,http://127.0.0.1:5173`）。
</Note>

<Tip>
  **CORS 来源经环境变量配置。** 启动前把 `EXPLORER_CORS_ORIGINS` 设为逗号分隔的允许来源列表（如 `EXPLORER_CORS_ORIGINS="http://myapp.example.com"`）。
</Tip>

```bash
# Full example
EXPLORER_CORS_ORIGINS="http://myapp.example.com" \
  semantica-explorer --graph my_graph.json --host 0.0.0.0 --port 8080 --no-browser
```

## 你能得到什么

- **Graph Explorer** — 交互式节点/边搜索、路径查找和邻域扩展。11.8 万节点图上索引化搜索 0.004ms。
- **Ontology Hub** — SKOS 词表管理、SHACL shape 生成与校验、本体对齐、健康面板和版本管理。
- **分析** — 度中心性、社区检测、连通性分析、图校验和距离矩阵。
- **REST API** — 全部功能都有 REST API：`/docs` 有完整文档。
- **WebSocket 更新** — 实时图变更事件经 WebSocket 推送，地址 `/ws/graph-updates`。
- **CLI 启动器** — `semantica-explorer --graph my_graph.json` 一条命令本地启动。

## 功能

<Tabs>
  <Tab title="Graph Explorer">
    浏览知识图谱的核心面板：

    - **索引化搜索**：POST 到 `/api/graph/search`，带查询；11.8 万节点图上 0.004ms
    - **路径查找**：任意两节点之间 BFS 或 Dijkstra，走 `GET /api/graph/path?source=&target=`
    - **邻域扩展**：`GET /api/graph/node/{id}/neighbors?depth=2`
    - **按实体类型过滤**：`GET /api/graph/nodes?type=Person`
    - **语义邻域**：`GET /api/graph/semantic-neighborhood?node_id=&top_k=20`
    - **距离矩阵**：`POST /api/graph/distance-matrix`

    <Warning>
      **保存为 JSON 前先过滤大图。** CLI 会把整个 JSON 文件读进内存。超过 1 万节点的图，导出前先过滤出相关子图：力导向布局在超大图上会变得不可用。
    </Warning>
  </Tab>
  <Tab title="Ontology Hub">
    在浏览器里管理本体生命周期：

    - **注册表**：`GET /api/ontology/registry`：列出已加载的本体
    - **SKOS 词表**：`GET /api/ontology/skos/schemes`、`GET /api/ontology/skos/concept/{uri}`
    - **SHACL**：`POST /api/ontology/shacl/generate`、`POST /api/ontology/shacl/validate`
    - **对齐**：`GET/POST /api/ontology/alignments`、`POST /api/ontology/suggest-alignments`
    - **提案与版本**：`POST /api/ontology/propose`、`GET /api/ontology/versions/{uri}`
    - **健康**：`GET /api/ontology/health`
  </Tab>
  <Tab title="分析">
    对已加载的图运行图指标：

    - **组合指标**：`GET /api/analytics?metrics=centrality,community,connectivity`
    - **图校验**：`GET /api/analytics/validation`
    - **增强：链接预测**：`POST /api/enrich/links`
    - **增强：去重**：`POST /api/enrich/dedup`
    - **增强：实体抽取**：`POST /api/enrich/extract`
    - **时态**：`GET /api/temporal/snapshot`、`GET /api/temporal/diff`、`GET /api/temporal/bounds`

    <Tip>
      **用 `/api/analytics/validation` 检查图质量。** 校验器能在把图交给下游流水线之前，检测出孤立节点、缺失类型和其他结构问题。
    </Tip>
  </Tab>
  <Tab title="决策与溯源">
    决策跟踪与溯源查询：

    - **决策**：`GET /api/decisions`、`GET /api/decisions/{id}`、`GET /api/decisions/{id}/chain`
    - **先例**：`GET /api/decisions/{id}/precedents`
    - **因果距离**：`GET /api/decisions/causal-distance?source=&target=`
    - **合规**：`GET /api/decisions/{id}/compliance`
    - **溯源**：`GET /api/provenance?node_id=`、`GET /api/provenance/report?node_id=`
    - **注释**：`GET/POST /api/annotations`、`DELETE /api/annotations/{id}`

    <Tip>
      **自动化用 REST API，探索用 Explorer 界面。** Explorer 的 REST 端点是稳定的程序化 API：接进脚本即可自动化批量注释、SPARQL 查询或导出。
    </Tip>
  </Tab>
</Tabs>

## API 端点

完整交互式文档在 `http://localhost:8000/docs`。所有端点收发 JSON。

<AccordionGroup>
  <Accordion title="图端点">

    | 端点 | 方法 | 说明 |
    | :-------- | :------ | :----------- |
    | `/api/graph/stats` | `GET` | 节点数、边数、实体类型分布 |
    | `/api/graph/nodes` | `GET` | 列出节点：`?type=&search=&skip=&limit=&cursor=&bbox=` |
    | `/api/graph/node/{id}` | `GET` | 取单个节点及其全部属性 |
    | `/api/graph/node/{id}/neighbors` | `GET` | 节点邻居：`?depth=1`（1–5） |
    | `/api/graph/edges` | `GET` | 列出边：`?type=&source=&target=&skip=&limit=&cursor=` |
    | `/api/graph/path` | `GET` | 最短路径：`?source=&target=&algorithm=bfs&directed=true` |
    | `/api/graph/search` | `POST` | 索引化搜索：body：`{query, limit, filters, anchor_node}` |
    | `/api/graph/distance-matrix` | `POST` | 两两距离：body：`{node_ids, metric}`（最多 50 节点） |
    | `/api/graph/semantic-neighborhood` | `GET` | 语义邻居：`?node_id=&top_k=20&min_similarity=0.0` |

  </Accordion>
  <Accordion title="分析、增强与时态">

    **分析：**

    | 端点 | 方法 | 说明 |
    | :-------- | :------ | :----------- |
    | `/api/analytics` | `GET` | 图指标：`?metrics=centrality,community,connectivity` |
    | `/api/analytics/validation` | `GET` | 图校验报告 |

    **增强：**

    | 端点 | 方法 | 说明 |
    | :-------- | :------ | :----------- |
    | `/api/enrich/extract` | `POST` | 从文本抽取实体 |
    | `/api/enrich/links` | `POST` | 节点链接预测 |
    | `/api/enrich/dedup` | `POST` | 重复检测 |
    | `/api/enrich/merge` | `POST` | 合并重复节点 |
    | `/api/reason` | `POST` | 对图运行推理 |

    **时态：**

    | 端点 | 方法 | 说明 |
    | :-------- | :------ | :----------- |
    | `/api/temporal/snapshot` | `GET` | `?at=ISO8601` 时刻的图快照（默认当前） |
    | `/api/temporal/diff` | `GET` | 两个时刻之间的差异：`?from_time=&to_time=` |
    | `/api/temporal/patterns` | `GET` | 时态活动模式 |
    | `/api/temporal/bounds` | `GET` | 图中最早和最晚的时态边界 |
    | `/api/temporal/distance-history` | `GET` | 距离历史：`?source=&target=` |

  </Accordion>
  <Accordion title="本体、词表与 SPARQL">

    **本体：**

    | 端点 | 方法 | 说明 |
    | :-------- | :------ | :----------- |
    | `/api/ontology/registry` | `GET` | 列出已加载的本体 |
    | `/api/ontology/load` | `POST` | 从 URL 或内容加载本体 |
    | `/api/ontology/create` | `POST` | 创建新本体 |
    | `/api/ontology/search` | `GET` | 搜索本体实体：`?q=term` |
    | `/api/ontology/health` | `GET` | 本体健康度与覆盖率指标 |
    | `/api/ontology/alignments` | `GET/POST` | 列出或创建本体对齐 |
    | `/api/ontology/suggest-alignments` | `POST` | AI 建议的对齐 |
    | `/api/ontology/shacl/generate` | `POST` | 生成 SHACL shape |
    | `/api/ontology/shacl/validate` | `POST` | 用 SHACL 校验 RDF |
    | `/api/ontology/skos/schemes` | `GET` | 列出 SKOS 概念方案 |
    | `/api/ontology/skos/concept/{uri}` | `GET` | 获取 SKOS 概念 |
    | `/api/ontology/proposals` | `GET` | 列出或读取本体变更提案 |
    | `/api/ontology/propose` | `POST` | 将草稿提交为提案 |
    | `/api/ontology/versions/{uri}` | `GET` | 版本历史 |

    **词表：**

    | 端点 | 方法 | 说明 |
    | :-------- | :------ | :----------- |
    | `/api/vocabulary/schemes` | `GET` | 经 TripletStore 获取 SKOS 方案 |
    | `/api/vocabulary/concepts` | `GET` | 方案中的概念：`?scheme=URI` |
    | `/api/vocabulary/hierarchy` | `GET` | 概念层级树 |
    | `/api/vocabulary/import` | `POST` | 导入 SKOS/RDF 词表文件 |

    SKOS 层级写入在 `skos:broader` 和 `skos:narrower` 两个方向上都拒绝环。词表导入会先校验整批数据，再添加节点；直接经图/会话写边时，同样的不变量也在图存储边界强制执行。

    **SPARQL：**

    | 端点 | 方法 | 说明 |
    | :-------- | :------ | :----------- |
    | `/api/sparql` | `POST` | 执行只读 SPARQL 查询（`SELECT`、`ASK`、`CONSTRUCT` 或 `DESCRIBE`）；`CONSTRUCT`/`DESCRIBE` 以 `subject`、`predicate`、`object` 列返回三元组，`ASK` 返回 `result` 布尔列 |

  </Accordion>
  <Accordion title="决策、溯源、注释与导出">

    **决策：**

    | 端点 | 方法 | 说明 |
    | :-------- | :------ | :----------- |
    | `/api/decisions` | `GET` | 已记录决策的分页列表 |
    | `/api/decisions/{id}` | `GET` | 单条决策详情 |
    | `/api/decisions/{id}/chain` | `GET` | 某条决策的因果链 |
    | `/api/decisions/{id}/precedents` | `GET` | 相似的历史决策 |
    | `/api/decisions/{id}/compliance` | `GET` | 政策合规检查 |
    | `/api/decisions/causal-distance` | `GET` | 因果距离：`?source=&target=` |

    **溯源：**

    | 端点 | 方法 | 说明 |
    | :-------- | :------ | :----------- |
    | `/api/provenance` | `GET` | 实体溯源血缘：`?node_id=` |
    | `/api/provenance/report` | `GET` | 溯源导出报告：`?node_id=` |

    **注释：**

    | 端点 | 方法 | 说明 |
    | :-------- | :------ | :----------- |
    | `/api/annotations` | `GET` | 列出注释：`?node_id=`（可选） |
    | `/api/annotations` | `POST` | 创建注释（返回 201） |
    | `/api/annotations/{id}` | `DELETE` | 删除注释（返回 204） |

    **导出/导入：**

    | 端点 | 方法 | 说明 |
    | :-------- | :------ | :----------- |
    | `/api/export` | `POST` | 把图导出为 JSON 或 CSV：body：`{format, node_ids}` |
    | `/api/export/distance-enriched` | `POST` | 把两两距离导出为 CSV 或 JSONL |
    | `/api/import` | `POST` | 从 `.json` 或 `.csv` 文件导入节点/边（最大 50 MB） |

  </Accordion>
  <Accordion title="健康与信息">

    | 端点 | 方法 | 说明 |
    | :-------- | :------ | :----------- |
    | `/api/health` | `GET` | 返回 `{"status": "ok"}` |
    | `/api/info` | `GET` | 服务器名称、版本、状态 |
    | `/docs` | `GET` | 交互式 Swagger UI：全部端点 |

  </Accordion>
</AccordionGroup>

## WebSocket 图更新

实时图变更事件经 WebSocket 在 `ws://localhost:8000/ws/graph-updates` 推送。WebSocket 是一条保持打开的长连接：图一有变更，服务器就主动把事件推给客户端，无需轮询：

```python
import asyncio
import json
import websockets

async def watch_updates():
    async with websockets.connect("ws://localhost:8000/ws/graph-updates") as ws:
        # Server sends an ack on connect
        ack = json.loads(await ws.recv())
        print("Connected:", ack)

        # Send a ping to verify the connection is alive
        await ws.send("ping")

        async for message in ws:
            event = json.loads(message)
            print("[{}] {}".format(event["event"], event.get("data")))

asyncio.run(watch_updates())
```

WebSocket 消息 schema：

```json
{
  "event":     "graph_mutation",
  "data": {
    "event_type":  "ADD_NODE",
    "entity_id":   "node_123",
    "payload":     {}
  },
  "timestamp": "2024-01-15T10:30:00+00:00"
}
```

WebSocket 广播的事件类型包括：`connection_ack`、`pong` 和 `graph_mutation`（经导入或增强添加/更新/删除节点或边时触发）。发送文本 `"ping"` 即可收到 `pong` 响应。

<Warning>
  **服务器重启后会话状态丢失。** 没有自动保存。关停前先调 `POST /api/export`（body 为 `{"format": "json"}`）下载当前状态。
</Warning>

## 性能

| 场景 | 延迟 |
| :-------- | :------- |
| 节点搜索（11.8 万节点，索引化） | 0.004ms |
| 邻域扩展（深度 2） | < 5ms |
| BFS 路径（11.8 万节点） | < 50ms |
| SPARQL SELECT（简单模式） | < 20ms |
| 距离矩阵（50 节点，语义） | ~2s（带嵌入缓存） |

节点搜索索引在启动时构建。图超过 50 万节点时，连接前预留额外启动时间。

距离矩阵每次请求最多 50 对节点。语义距离要求节点属性里存有嵌入(Embedding)。

## 排障

**浏览器标签页没有打开**
浏览器在服务器启动 1.5 秒后打开。自动打开失败时，用 `--no-browser` 手动访问 `http://127.0.0.1:8000`。

**`Error: graph file not found`**
`--graph` 路径必须是已存在的文件。启动前检查路径、确认文件存在。

**`Error: uvicorn is required`**
安装 explorer extra：`pip install "semantica[explorer]"`。

**API 调用 `Connection refused`**
服务器默认只绑定 `127.0.0.1`。要从其他机器或容器访问 Explorer，用 `--host 0.0.0.0` 启动。

**导入后图是空的**
导入端点（`/api/import`）只解析 `.json` 和 `.csv` 文件。其他格式返回 HTTP 422。JSON 文件必须包含顶层 `entities`/`nodes` 数组或 `relationships`/`edges` 数组。

**`/api/graph/path` 报 `PathFinder not available`**
路径查找需要 `semantica[kg]` extra。用 `pip install "semantica[all]"` 安装。

**语义邻域返回 503**
语义邻域要求节点属性里存有嵌入（键为 `embedding`、`vector` 或 `node2vec_embedding`）。没有嵌入的图返回 503。

**重启后会话状态丢失**
会话状态只在内存里。关停前用 `POST /api/export` 保存 JSON 快照。

- [Context](./context.md) — 构建并保存 Explorer 加载的 ContextGraph。
- [Ontology](./ontology.md) — 程序化的本体管理与 SHACL 生成。
- [Visualization](./visualization.md) — 不经 Explorer 服务器的程序化图渲染。
- [Export](./export.md) — 不启动服务器，直接导出 RDF、Parquet 等格式。
