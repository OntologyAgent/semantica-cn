---
title: CLI 配置
description: Semantica 的五个可执行文件：各自的作用、使用时机，以及如何确认它们正常工作。
source: cli-setup.md
source_version: c401eeeca7663e96dd3be5b50acb4b2f45f0b444
icon: "terminal"
---

安装基础包后，`PATH` 上会注册五个可执行文件，各有分工。本页介绍它们是什么、如何验证可用，以及每种场景该用哪一个。


## 已安装的命令

```bash
pip install semantica
```

安装后可用以下命令：

| 命令 | 入口点 | 作用 |
| :------- | :----------- | :------------ |
| `semantica` | `semantica.cli:main` | 通用 CLI：流水线运行、抽取、图操作 |
| `semantica-server` | `semantica.server:main` | FastAPI/uvicorn REST API 服务器，默认绑定 `127.0.0.1:8000`（设 `SEMANTICA_HOST` 可覆盖） |
| `semantica-worker` | `semantica.worker:main` | Semantica 部署的后台工作进程入口 |
| `semantica-explorer` | `semantica.explorer:main` | 交互式浏览器面板，用于知识图谱探索 |
| `semantica-mcp` | `semantica.mcp_server:main` | MCP 服务器（stdio），供 Claude Desktop、Cursor、Windsurf 等 MCP 客户端使用 |

<Note>
  `semantica-explorer` 需要 `pip install semantica[explorer]`。不带该 extra 运行会立即打印错误并退出。完整流程见 [Explorer 配置](./explorer-setup.md)。
</Note>


## 验证安装

确认每个命令可达并打印用法：

```bash
semantica --help
semantica-server --help
semantica-worker --help
semantica-explorer --help
semantica-mcp --help
```

确认包版本：

```bash
python -c "import semantica; print(semantica.__version__)"
```


## 各命令的使用时机

- **semantica** — 通用 CLI。适合在 shell 脚本或 CI 任务里做一次性流水线运行、实体抽取和图操作。
- **semantica-server** — 启动 REST API 服务器，默认绑定 `127.0.0.1:8000`（设 `SEMANTICA_HOST` 可覆盖）。当其他服务或应用需要经 HTTP 以编程方式访问 Semantica 时使用。
- **semantica-worker** — 后台任务处理器。当异步流水线执行需要脱离请求周期时，与 `semantica-server` 搭配运行。先启动服务器，再启动一个或多个指向同一后端的工作进程。
- **semantica-explorer** — 启动浏览器面板，需要 `pip install semantica[explorer]`。用于交互式探索已保存的知识图谱。见 [Explorer 配置](./explorer-setup.md)。
- **semantica-mcp** — 以 stdio 方式运行 MCP 服务器。在 MCP 客户端的设置文件里配置它，即可向 Claude Desktop、Cursor、Windsurf 或任何支持 MCP 的客户端暴露全部 12 个工具和 3 个资源。见 [MCP 服务器](../reference/mcp_server.md)。


## 使用示例

<Tabs>
  <Tab title="REST 服务器">
    ```bash
    # 在 127.0.0.1:8000 上启动 FastAPI + uvicorn（设 SEMANTICA_HOST 可更改）
    semantica-server
    ```

    启动后可用以下命令检查：

    ```bash
    curl http://localhost:8000/health
    # {"status": "ok"}

    curl http://localhost:8000/api/info
    # {"name": "Semantica API", "version": "...", "status": "active"}
    ```

    交互式 API 文档在 `http://localhost:8000/docs`。
  </Tab>
  <Tab title="Worker">
    ```bash
    semantica-worker
    ```

    收到 `SIGINT`（Ctrl-C）或 `SIGTERM` 时，worker 会干净退出。
  </Tab>
  <Tab title="MCP 客户端配置">
    加入 MCP 客户端的设置文件：

    ```json
    {
      "mcpServers": {
        "semantica": {
          "command": "semantica-mcp"
        }
      }
    }
    ```

    如果命令不在 `PATH` 上，可用 Python 模块形式：

    ```json
    {
      "mcpServers": {
        "semantica": {
          "command": "python",
          "args": ["-m", "semantica.mcp_server"]
        }
      }
    }
    ```

    配置客户端之前，先在 shell 里直接测试：

    ```bash
    echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' | semantica-mcp
    ```

    应收到 JSON-RPC 响应。完整的工具与资源清单见 [MCP 服务器](../reference/mcp_server.md)。
  </Tab>
  <Tab title="Explorer">
    ```bash
    pip install semantica[explorer]
    semantica-explorer --graph my_graph.json
    ```

    完整流程（包括如何构建并保存图文件）见 [Explorer 配置](./explorer-setup.md)。
  </Tab>
  <Tab title="Python 模块形式">
    每个命令也能以 Python 模块方式运行——当脚本目录不在 `PATH` 上时很有用：

    ```bash
    python -m semantica.mcp_server
    python -m semantica.explorer --graph my_graph.json
    ```
  </Tab>
</Tabs>


## 环境变量

`semantica-mcp` 读取两个环境变量：

| 变量 | 默认值 | 说明 |
| :-------- | :------- | :----------- |
| `SEMANTICA_KG_PATH` | *（无）* | 启动时加载的已保存图文件路径 |
| `SEMANTICA_LOG_LEVEL` | `WARNING` | 日志级别：`DEBUG`、`INFO`、`WARNING` |

`semantica-server` 读取一个：

| 变量 | 默认值 | 说明 |
| :-------- | :------- | :----------- |
| `SEMANTICA_CORS_ORIGINS` | `http://localhost:5173,http://127.0.0.1:5173` | 允许的 CORS 来源，逗号分隔 |

除上述变量外，这些命令不读取其他环境变量。


## 故障排查

<AccordionGroup>

<Accordion title="command not found" icon="terminal">

可执行文件位于当前 Python 环境的 `bin/`（Linux/Mac）或 `Scripts/`（Windows）目录。找不到命令，多半是这个目录不在 `PATH` 上。

先激活虚拟环境：

```bash
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
semantica --help
```

查找 pip 放置脚本的位置：

```bash
python -m site --user-scripts   # 用户级安装
pip show -f semantica           # 列出所有已安装文件
```

</Accordion>

<Accordion title="能找到命令，但导入时崩溃" icon="triangle-exclamation">

```bash
pip install --upgrade semantica
python -c "import semantica; print(semantica.__version__)"
```

如果有多个 Python 环境，装到 shell 实际解析的那个：

```bash
python -m pip install semantica
```

</Accordion>

<Accordion title="semantica-explorer: uvicorn is required" icon="map">

基础安装不含 Explorer 的依赖：

```bash
pip install semantica[explorer]
```

</Accordion>

<Accordion title="semantica-mcp 在 MCP 客户端里静默失败" icon="plug">

MCP 服务器经 stdio 通信。先在 shell 里直接测试：

```bash
echo '{"jsonrpc":"2.0","id":1,"method":"ping","params":{}}' | semantica-mcp
```

收到 `{"jsonrpc":"2.0","id":1,"result":{}}` 说明服务器工作正常。如果毫无输出，检查命令是否在 `PATH` 上、基础包是否已安装。

</Accordion>

<Accordion title="Windows：启动时 DLL 报错" icon="windows">

安装 [Microsoft Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)。这是 PyTorch 及相关包需要的 Windows 系统依赖，不是 Semantica 的缺陷。

</Accordion>

</AccordionGroup>


## 下一步

- [Explorer 配置](./explorer-setup.md) — 构建图、保存、启动浏览器面板。
- [MCP 服务器](../reference/mcp_server.md) — 经 MCP 协议暴露的全部 12 个工具和 3 个资源。
- [安装](./installation.md) — 虚拟环境、可选 extra 和平台相关说明。
- [快速开始](./quickstart.md) — 端到端流水线演练，附可运行代码。
