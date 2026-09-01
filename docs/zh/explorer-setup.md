---
title: Explorer 配置
description: 安装 Explorer extra，把 ContextGraph 存成 JSON，然后启动交互式浏览器面板。
source: explorer-setup.md
source_version: 4d8caa1fdbe88b0746f0947ef329a2774b316359
icon: "map"
---

**`semantica-explorer`** 是一个用于知识图谱探索的**交互式浏览器面板**。你给它一个图文件，它启动本地服务器并打开浏览器标签页，你可以在里面搜索节点、寻找路径、查看溯源、运行分析：启动之后不需要写任何代码。

本页覆盖从零到跑通 Explorer 所需的全部内容。完整的 REST API 参考和端点目录见 [Explorer 参考](../reference/explorer.md)。


## 前置条件

Explorer 依赖 FastAPI 和 uvicorn，基础安装不包含它们：

```bash
pip install semantica[explorer]
```

<Note>
  仅 `pip install semantica` 是不够的。不带 `[explorer]` extra 运行 `semantica-explorer` 会立即打印错误并以退出码 1 结束。
</Note>

验证：

```bash
semantica-explorer --help
```

应该能看到带四个可用标志的用法信息。如果看到 `command not found`，先激活你的虚拟环境。PATH 问题见 [CLI 配置](./cli-setup.md#故障排查)。


## 最小端到端示例

以下四步就是让 Explorer 跑起来的全部内容：

```python
from semantica.context import ContextGraph

# 1. 创建图
graph = ContextGraph()

# 2. 添加节点
graph.add_node("python", "language", content="Python programming language")

# 3. 保存到磁盘
graph.save_to_file("my_graph.json")
```

```bash
# 4. 启动 Explorer
semantica-explorer --graph my_graph.json
```

浏览器会打开 `http://127.0.0.1:8000`。健康检查端点可确认服务器已就绪：

```bash
curl http://127.0.0.1:8000/api/health
# {"status": "ok"}
```


## 第 1 步：构建并保存 ContextGraph

Explorer 从磁盘上的 JSON 文件加载图。你需要先创建这个文件。

<Steps>
  <Step title="构建图">
    ```python
    from semantica.context import ContextGraph

    graph = ContextGraph()

    # add_node(node_id, node_type, content=None, **properties)
    graph.add_node("python",  "language",  content="Python programming language")
    graph.add_node("fastapi", "framework", content="FastAPI web framework")
    graph.add_node("guido",   "person",    content="Guido van Rossum")

    # add_edge(source_id, target_id, edge_type="related_to", weight=1.0, **properties)
    graph.add_edge("python",  "fastapi", "enables")
    graph.add_edge("guido",   "python",  "created")
    ```
  </Step>
  <Step title="保存为 JSON 文件">
    ```python
    graph.save_to_file("my_graph.json")
    ```

    `save_to_file` 会把含 `graph_id`、`nodes`、`edges` 和 `links` 的 JSON 对象写入指定路径。
  </Step>
  <Step title="验证文件可加载（可选的完整性检查）">
    ```python
    from semantica.context import ContextGraph

    check = ContextGraph()
    check.load_from_file("my_graph.json")
    print(check.stats())
    # {
    #   "node_count": 3,
    #   "edge_count": 2,
    #   "node_types": {"language": 1, "framework": 1, "person": 1},
    #   "edge_types": {"enables": 1, "created": 1},
    #   "density": ...
    # }
    ```

    这段能无错运行，Explorer 就能成功加载该文件。
  </Step>
</Steps>

<Tip>
  流水线已经产出图了？直接跳到第 2 步。唯一要求是文件经 `ContextGraph.save_to_file()` 保存。
</Tip>


## 第 2 步：启动 Explorer

```bash
semantica-explorer --graph my_graph.json
```

启动过程会打印：

```
✓ Graph loaded: 3 nodes, 2 edges
╭─ Semantica Explorer · http://127.0.0.1:8000 ─╮
│  API docs  http://127.0.0.1:8000/docs         │
│  Health    http://127.0.0.1:8000/api/health   │
╰───────────────────────────────────────────────╯
```

服务器启动后不久，浏览器会自动打开 `http://127.0.0.1:8000`。


## CLI 标志

`semantica-explorer` 只接受四个标志：

| 标志 | 短形式 | 默认值 | 说明 |
| :---- | :----- | :------- | :----------- |
| `--graph` | `-g` | *（**必填**）* | ContextGraph JSON 文件路径 |
| `--port` | `-p` | `8000` | 服务器绑定的端口 |
| `--host` | 无 | `127.0.0.1` | 服务器绑定的主机 |
| `--no-browser` | 无 | 关闭 | 不自动打开浏览器标签页 |

没有认证、日志级别或 TLS 相关的标志。CLI 未实现这些能力。

### 示例

```bash
# 最简：仅本机，端口 8000，浏览器自动打开
semantica-explorer --graph my_graph.json

# 短标志
semantica-explorer -g my_graph.json -p 8080

# 暴露到网络，让其他机器可以连接
semantica-explorer --graph my_graph.json --host 0.0.0.0 --port 8080

# 无头模式：跳过自动打开，手动访问
semantica-explorer --graph my_graph.json --no-browser
```

<Warning>
  `--host 0.0.0.0` 会让 Explorer 在所有网络接口上可达。自 v0.6.5 起，Explorer API 要求配置 `SEMANTICA_API_KEY`（以 `X-API-Key` 请求头发送），未配置时默认失败并返回 `503`；只有显式设置 `SEMANTICA_ALLOW_ANONYMOUS=true` 才可能匿名访问。请只在可信的私有网络上这样使用。
</Warning>


## 浏览器访问

服务器运行起来后：

| URL | 内容 |
| :--- | :------------ |
| `http://127.0.0.1:8000` | 交互式面板 |
| `http://127.0.0.1:8000/docs` | Swagger UI：全部 REST 端点，可交互 |
| `http://127.0.0.1:8000/api/health` | 健康检查：`{"status": "ok"}` |

启动后不久浏览器标签页会自动打开。如果没打开，手动访问该 URL，或加 `--no-browser` 后自行打开。


## 以 Python 模块方式运行

如果 `semantica-explorer` 不在 `PATH` 上，用模块形式：

```bash
python -m semantica.explorer --graph my_graph.json --port 8080
```


## 常见启动错误

<AccordionGroup>

<Accordion title="Error: graph file not found" icon="file-circle-xmark">

传给 `--graph` 的路径必须指向存在的文件。CLI 在加载前会用 `os.path.isfile()` 检查。

```bash
# 确认文件存在
ls my_graph.json                                          # Linux / Mac
dir my_graph.json                                         # Windows

# 需要时使用完整路径
semantica-explorer --graph /absolute/path/to/my_graph.json
```

</Accordion>

<Accordion title="Error: uvicorn is required" icon="triangle-exclamation">

基础包安装时没有装 `[explorer]` extra：

```bash
pip install semantica[explorer]
```

</Accordion>

<Accordion title="Explorer 启动了，但节点数为零" icon="circle-xmark">

文件加载了，但里面没有节点。用 Python 验证：

```python
from semantica.context import ContextGraph
g = ContextGraph()
g.load_from_file("my_graph.json")
print(g.stats())  # check node_count
```

`node_count` 为 `0` 说明图在添加任何节点之前就保存了。确认在 `save_to_file()` 之前调用过 `add_node()`。

</Accordion>

<Accordion title="从另一台机器连接被拒绝" icon="network-wired">

默认 `--host 127.0.0.1` 只接受本机连接。允许远程访问：

```bash
semantica-explorer --graph my_graph.json --host 0.0.0.0
```

</Accordion>

<Accordion title="浏览器标签页没有打开" icon="browser">

无头环境、SSH 和容器环境属正常现象。加 `--no-browser` 抑制警告，然后在能访问服务器网络的浏览器里打开 `http://127.0.0.1:8000`。

</Accordion>

</AccordionGroup>


## Explorer 提供什么

运行起来后，Explorer 提供 REST API 和面板，支持：

- **节点与边搜索**：按 ID、类型和内容对所有节点做索引搜索
- **邻域展开**：按可配置的跳数深度检查邻居
- **路径查找**：任意两节点间的 BFS 最短路径
- **图分析**：中心度、社区发现、连通性
- **决策与溯源**：查询已记录的决策及其因果链
- **导入/导出**：上传 JSON 或 CSV 扩展图；下载当前状态

完整端点目录见 `/docs` 的 Swagger UI 和下方参考页。

- [Explorer 参考](../reference/explorer.md) — 全部 REST 端点、WebSocket 事件、分析和所有支持的标志。
- [CLI 配置](./cli-setup.md) — Semantica 全部五个可执行文件及各自适用场景。
- [Context 模块](../reference/context.md) — ContextGraph 完整文档：构建、查询、保存和加载。
- [快速开始](./quickstart.md) — 端到端流水线：摄取 → 抽取 → 构建图 → 导出。
