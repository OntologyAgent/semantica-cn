---
title: "MCP 服务器（MCP Server）"
description: "模型上下文协议(MCP)服务器：把 Semantica 的全部能力暴露给 Claude Desktop、VS Code、Cursor 及任何支持 MCP 的工具。"
source: reference/mcp_server.md
source_version: 954aff70b0077f18ec8d799dfc513083127e8991
icon: "plug"
---

**`semantica.mcp_server`** 把 Semantica 的知识图谱(Knowledge Graph)、决策智能、语义抽取和推理能力打包成一个 [MCP（模型上下文协议，Model Context Protocol）](https://modelcontextprotocol.io) **服务器**，经 stdio 对外暴露：

- 暴露 15 个 MCP 工具：抽取实体、查询图、记录决策、运行推理、导出结果
- 启动后无需写 Python 代码：配置一次，任何支持 MCP 的客户端都能用
- 兼容 Claude Desktop、Windsurf、Cline、Continue、VS Code、Roo Code、Cursor

## 服务器接口

```json
// Configure in your MCP client (Claude Desktop, Windsurf, Cursor, VS Code, etc.)
{
  "mcpServers": {
    "semantica": {
      "command": "semantica-mcp"
    }
  }
}
```

```bash
# Or run directly
semantica-mcp
# or
python -m semantica.mcp_server
```

<Tip>
  `semantica.mcp_server` 是一个 **stdio 服务器进程**，不是 Python 库。说白了，它就是个只在标准输入输出上"对话"的后台进程，不暴露任何可导入的类。也就是说，与它交互的唯一方式，是由已连接的 AI 客户端发起 MCP 工具调用。
</Tip>

<Warning>
  **服务器经 stdio 通信：不要往 stdout 打日志。** stdout 是 JSON-RPC 消息的专用通道，一旦混进日志，客户端就会把日志误当协议消息来解析，整个通信就乱了。因此，任何指向 stdout 的 `print()` 或日志输出都是禁区：所有日志只写 `stderr`，详细程度用 `SEMANTICA_LOG_LEVEL` 环境变量控制。
</Warning>

## 你能得到什么

- **15 个 MCP 工具** — 抽取实体、抽取关系、记录决策、查询决策、查找先例、追溯因果链、添加实体、添加关系、运行分析、总结图、运行推理、导出图、查询活动图、更新节点、归档节点。
- **3 个可读资源** — 实时图 JSON（`semantica://graph/summary`）、决策列表和 schema/版本信息：任何 MCP 客户端都可读取。
- **零基础设施** — 经 stdio 运行：无需服务器、无需端口、无需 Docker。在任何 MCP 客户端里一个配置块即可启用。
- **持久化图** — 把 `SEMANTICA_KG_PATH` 指向已保存的图文件，服务器每次启动自动重新加载。
- **决策智能** — 记录决策、经混合相似度搜索查找先例、跨智能体运行追溯因果链。
- **REST 替代方案** — 更偏好程序化访问的话，[Explorer](./explorer.md) 模块提供完整的 HTTP API 和浏览器面板。

## 安装

```bash
pip install semantica
```

MCP 服务器包含在基础安装中：无需任何 extra。

## 配置

<Steps>
  <Step title="找到你的 MCP 客户端设置文件">

    | 客户端 | 设置文件 |
    | :------ | :------------- |
    | Claude Desktop（macOS） | `~/Library/Application Support/Claude/claude_desktop_config.json` |
    | Claude Desktop（Windows） | `%APPDATA%\Claude\claude_desktop_config.json` |
    | Cursor | 项目内 `.cursor/mcp.json`，或全局 `~/.cursor/mcp.json` |
    | VS Code / Continue | `.vscode/mcp.json` 或用户设置 |
    | Windsurf / Cline / Roo Code | 应用专属设置 → MCP Servers |

  </Step>
  <Step title="添加 Semantica MCP 服务器配置">

    <CodeGroup>

    ```json Claude Desktop / Windsurf / Cline
    {
      "mcpServers": {
        "semantica": {
          "command": "semantica-mcp"
        }
      }
    }
    ```

    ```json Cursor
    {
      "mcpServers": {
        "semantica": {
          "command": "semantica-mcp",
          "env": {
            "SEMANTICA_KG_PATH": "/path/to/my_graph.json"
          }
        }
      }
    }
    ```

    ```json VS Code / Continue / Roo Code
    {
      "mcpServers": {
        "semantica": {
          "command": "python",
          "args": ["-m", "semantica.mcp_server"]
        }
      }
    }
    ```

    ```json With persistent graph
    {
      "mcpServers": {
        "semantica": {
          "command": "semantica-mcp",
          "env": {
            "SEMANTICA_KG_PATH": "/path/to/my_graph.json",
            "SEMANTICA_LOG_LEVEL": "INFO"
          }
        }
      }
    }
    ```

    </CodeGroup>

    <Warning>
      **MCP 客户端的 `command` 字段要配置精确。**`command` 必须指向可执行文件的准确路径（macOS/Linux 上用 `which semantica-mcp` 查找）。路径错了会静默失败：服务器就是不出现在工具列表里。先直接跑 `echo | semantica-mcp` 确认二进制可用。
    </Warning>

  </Step>
  <Step title="配置客户端前先本地测试">
    ```bash
    # Run the server directly (reads from stdin, writes to stdout)
    semantica-mcp

    # Or via Python module
    python -m semantica.mcp_server

    # Send a JSON-RPC initialize message to confirm it's working
    echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' | semantica-mcp
    ```
  </Step>
</Steps>

## 环境变量

| 变量 | 默认值 | 说明 |
| :-------- | :------- | :----------- |
| `SEMANTICA_KG_PATH` | *（无：内存图）* | 启动时加载的持久化图文件路径 |
| `SEMANTICA_LOG_LEVEL` | `WARNING` | 日志详细程度：`DEBUG`、`INFO`、`WARNING` |

<Warning>
  **不设置 `SEMANTICA_KG_PATH`，图就从空开始。** MCP 服务器在首次使用时创建全新的内存 `ContextGraph`。把 `SEMANTICA_KG_PATH` 指向之前保存的图文件，即可跨服务器重启恢复状态。不设置的话，进程退出时全部数据丢失。
</Warning>

<Tip>
  **排障时开启 DEBUG 日志。** 在 MCP 客户端的 `env` 块里设 `SEMANTICA_LOG_LEVEL=DEBUG`，或直接运行 `python -m semantica.mcp_server` 查看 stderr 输出。
</Tip>

## 工具

MCP 服务器暴露 15 个工具，任何已连接的 AI 助手都可以调用：

| 工具 | 类别 | 说明 |
| :---- | :-------- | :----------- |
| `extract_entities` | 抽取 | NER：找出人物、地点、组织、概念 |
| `extract_relations` | 抽取 | 类型化关系与三元组抽取 |
| `record_decision` | 决策智能 | 保存一条带推理过程和结果的决策 |
| `query_decisions` | 决策智能 | 按自然语言或类别搜索已记录的决策 |
| `find_precedents` | 决策智能 | 对历史决策做混合相似度搜索 |
| `get_causal_chain` | 决策智能 | 追溯上游/下游因果链 |
| `add_entity` | 图操作 | 向活动图添加节点 |
| `add_relationship` | 图操作 | 在两个节点之间添加有向边 |
| `get_graph_summary` | 图操作 | 节点数、决策数、图状态 |
| `get_graph_analytics` | 图操作 | PageRank 中心性与社区检测 |
| `query_graph` | 图操作 | 取单个节点、遍历邻居，或按关键词搜索节点 |
| `update_node` | 图操作 | 把属性合并进节点并持久化到 `SEMANTICA_KG_PATH` |
| `delete_node` | 图操作 | 软删除（归档）节点并持久化到 `SEMANTICA_KG_PATH` |
| `run_reasoning` | 推理 | 对事实前向链接 IF/THEN 规则 |
| `export_graph` | 推理与导出 | 序列化图（`turtle`/`ttl`：RDF Turtle 别名、`nt`、`xml`、`json-ld`、`json`） |

### 知识抽取

<AccordionGroup>

<Accordion title="extract_entities" icon="tag">

用 Semantica 的命名实体识别(NER)从文本中抽取命名实体（人物、地点、组织、概念）。

**输入：**

```json
{ "text": "Apple Inc. was founded by Steve Jobs in Cupertino in 1976." }
```

**输出：**

```json
{
  "entities": [
    { "label": "Apple Inc.", "type": "ORGANIZATION", "start": 0,  "end": 10,  "confidence": 0.98 },
    { "label": "Steve Jobs", "type": "PERSON",       "start": 26, "end": 36,  "confidence": 0.99 },
    { "label": "Cupertino",  "type": "LOCATION",     "start": 40, "end": 49,  "confidence": 0.97 },
    { "label": "1976",       "type": "DATE",          "start": 53, "end": 57,  "confidence": 0.95 }
  ],
  "count": 4
}
```

</Accordion>

<Accordion title="extract_relations" icon="arrows-left-right">

从文本中抽取类型化关系和 `(subject, predicate, object)` 三元组。

**输入：**

```json
{ "text": "Steve Jobs founded Apple Inc. and led it until 2011." }
```

**输出：**

```json
{
  "relations": [
    { "source": "Steve Jobs", "type": "founded", "target": "Apple Inc.", "confidence": 0.96 }
  ],
  "triplets": [
    { "subject": "Steve Jobs", "predicate": "founded", "object": "Apple Inc." }
  ],
  "relation_count": 1,
  "triplet_count": 1
}
```

</Accordion>

</AccordionGroup>

### 决策智能

<AccordionGroup>

<Accordion title="record_decision" icon="check-circle">

把一条带完整上下文、推理过程和元数据的决策记录进知识图谱。

**输入：**

```json
{
  "category": "model_selection",
  "scenario": "Choose LLM for production reasoning pipeline",
  "reasoning": "GPT-4 benchmark advantage justifies 3x cost increase",
  "outcome": "selected_gpt4",
  "confidence": 0.91,
  "decision_maker": "product_team",
  "valid_from": "2024-01-01",
  "valid_until": "2024-12-31"
}
```

必填字段：`category`、`scenario`、`reasoning`、`outcome`、`confidence`。
可选：`decision_maker`（默认 `"mcp_client"`）、`valid_from`、`valid_until`。

**输出：**

```json
{ "decision_id": "dec_a1b2c3", "status": "recorded" }
```

</Accordion>

<Accordion title="query_decisions" icon="magnifying-glass">

按自然语言或类别过滤查询已记录的决策。

**输入：**

```json
{ "query": "model selection", "category": "model_selection", "limit": 5 }
```

所有字段可选。`limit` 默认 `10`。提供 `query` 时用相似度搜索；省略时按 `category` 过滤。

</Accordion>

<Accordion title="find_precedents" icon="clock-rotate-left">

用混合相似度搜索找出与给定场景相似的历史决策。

**输入：**

```json
{ "scenario": "Choose cloud provider for HIPAA workload", "max_results": 5 }
```

`max_results` 默认 `5`，最大 `50`。

<Tip>
  **高风险决策前先用 `find_precedents`。** 该工具对全部已记录决策做混合相似度搜索。因此，任何重要决策路径开始时都值得调用它：可直接套用的历史推理会随之浮现，既减少重复劳动，也让智能体多次运行之间保持一致。
</Tip>

</Accordion>

<Accordion title="get_causal_chain" icon="diagram-project">

从某条决策向上游或下游追溯因果链。

**输入：**

```json
{ "decision_id": "dec_a1b2c3", "direction": "downstream", "max_depth": 5 }
```

`direction` 接受 `"upstream"` 或 `"downstream"`（默认 `"downstream"`）。
`max_depth` 默认 `5`，最大 `20`。

</Accordion>

</AccordionGroup>

### 图操作

<AccordionGroup>

<Accordion title="add_entity" icon="circle-plus">

向活动知识图谱添加节点/实体。

**输入：**

```json
{
  "id": "apple_inc",
  "label": "Apple Inc.",
  "type": "Organization",
  "metadata": { "founded": 1976, "hq": "Cupertino" }
}
```

只有 `id` 必填。`label` 默认取 `id` 值。`type` 默认 `"Entity"`。

</Accordion>

<Accordion title="add_relationship" icon="arrow-right">

在两个已有实体之间添加有向关系（边）。

**输入：**

```json
{
  "source": "steve_jobs",
  "target": "apple_inc",
  "type": "FOUNDED",
  "metadata": { "year": 1976 }
}
```

`source` 和 `target` 必填。`type` 默认 `"RELATED_TO"`。

</Accordion>

<Accordion title="get_graph_summary" icon="info-circle">

返回当前知识图谱的高层摘要。

**输出：**

```json
{
  "node_count": 42,
  "decision_count": 5,
  "graph_ready": true
}
```

不接受输入参数。

</Accordion>

<Accordion title="get_graph_analytics" icon="chart-bar">

对当前图计算 PageRank 中心性和社区检测。返回按 PageRank 排序的头部节点、社区数量和整体节点/边计数。

不接受输入参数。

</Accordion>

<Accordion title="query_graph" icon="magnifying-glass">

以三种模式之一读取活动图，由 `mode` 决定：

- `node` — 按 `node_id` 返回单个节点。
- `neighbors`（默认）— 从 `node_id` 向外向内遍历至多 `depth` 跳（限 1-5，默认 1）。可选 `relationship_types` 过滤边类型；可选 `limit` 限制结果数。
- `search` — 把 `query` 与每个节点的 id 和内容做关键词匹配。可选 `node_type` 限定扫描范围；`limit` 默认 50。

**输入：**

```json
{ "mode": "neighbors", "node_id": "apple_inc", "depth": 2 }
```

</Accordion>

<Accordion title="update_node" icon="pen">

把一组属性合并进已有节点。变更先应用到内存；配置了 `SEMANTICA_KG_PATH` 时还会写回该文件，因此重启后仍然保留。未配置路径时返回 `persisted: false`。

**输入：**

```json
{
  "node_id": "task_42",
  "properties": { "status": "done", "note": "shipped in v0.6.7" }
}
```

`node_id` 与非空 `properties` 对象必填。更新不存在的节点会报错。

</Accordion>

<Accordion title="delete_node" icon="box-archive">

软删除节点：节点仍保留在图中以供追溯历史，但会打上 `status: "archived"` 标记。配置了 `SEMANTICA_KG_PATH` 时会持久化。

**输入：**

```json
{ "node_id": "task_42" }
```

</Accordion>

</AccordionGroup>

### 推理

<AccordionGroup>

<Accordion title="run_reasoning" icon="brain">

对一组事实运行前向链接 IF/THEN 规则，推导新事实。

**输入：**

```json
{
  "facts": ["Employee(John)", "Manager(John)"],
  "rules": ["IF Manager(?x) THEN HasAuthority(?x)"]
}
```

**输出：**

```json
{ "derived_facts": ["HasAuthority(John)"] }
```

</Accordion>

</AccordionGroup>

### 导出

<AccordionGroup>

<Accordion title="export_graph" icon="file-export">

把当前知识图谱导出为某种序列化格式。

**输入：**

```json
{ "format": "json-ld" }
```

支持格式：`turtle`、`ttl`、`nt`、`xml`、`json-ld`、`json`。默认 `json-ld`。

</Accordion>

</AccordionGroup>

## 资源

MCP 服务器暴露三个可读资源：

| URI | 说明 |
| :--- | :----------- |
| `semantica://graph/summary` | 图的高层统计信息 |
| `semantica://decisions/list` | 全部已记录决策（最多 50 条） |
| `semantica://schema/info` | 服务器版本和可用工具 |

- [Context](./context.md) — MCP 服务器所操作的 ContextGraph。
- [Semantic Extract](./semantic_extract.md) — 为 MCP 工具提供支撑的 NER 与关系抽取。
- [Reasoning](./reasoning.md) — run_reasoning 背后的前向链接引擎。
- [Agno Integration](../integrations/agno.md) — 在 Agno 多智能体团队中使用 Semantica。
