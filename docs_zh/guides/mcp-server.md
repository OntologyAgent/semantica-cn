---
title: "模型上下文协议(MCP)服务器"
description: "将 Semantica 的知识图谱、决策智能与推理能力接入 Claude Desktop、Windsurf、VS Code、Cline 及任何兼容 MCP 的 AI 客户端。"
source: guides/mcp-server.md
source_version: db22256acb7e9a0e01b6ea866d4003fae8bdb811
icon: "plug"
---

## 什么是模型上下文协议(MCP)？

MCP 是 Model Context Protocol（模型上下文协议）的缩写。作为一项开放标准，它允许外部 AI 助手（如 Claude Desktop、Cursor 或 Windsurf）安全地访问本地工具和数据源。

Semantica MCP 服务器把你的知识图谱(Knowledge Graph)暴露为 15 个可调用的工具。接入之后，任何兼容的 AI 客户端都能在对话过程中实时遍历图谱、记录决策、运行分析并导出结果，无需编写自定义工具封装。

<Info>
  Semantica MCP 服务器提供 15 个工具和 3 个只读资源。所有工具都接收并返回 JSON。除一个用于图持久化的可选环境变量外，无需任何其他配置。
</Info>

## 架构与通信

先弄清 MCP 的底层工作方式很重要。**Semantica MCP 服务器不是 REST API。** 它不开网络端口，没有 HTTP 端点，也不需要 API key。

它的做法是：AI 客户端把 `semantica-mcp` 作为子进程在本地启动，AI 与 Semantica 之间的全部通信都通过标准输入输出（`stdio`）安全完成。由于服务器以你的用户账户在本地运行，它天然拥有你的本地文件权限。

## 为什么在 Semantica 中使用 MCP？

- **零代码集成**：不用写胶水代码，就能把 Semantica 的图谱能力接入你的 AI IDE 或桌面聊天应用。
- **实时更新图谱**：与 AI 对话，从文档中抽取实体(Entity)并填充到实时运转的知识图谱里。
- **可审计的 AI**：让 AI 做决策，Semantica 的决策智能(Decision Intelligence)工具会自动把推理过程和因果链写入图谱。

## 适用与不适用场景

- **适用 MCP**：想让第三方 AI 界面（如 Claude Desktop 或 Windsurf）操作、查询本机上的 Semantica 知识图谱并对其进行推理时。
- **适用 `AgentContext`**：正在构建自主运行的 Python 脚本或后端服务时。要写 Python 代码搭建智能体(Agent)，请直接使用 `semantica.context.AgentContext`，不必另起 MCP 服务器。MCP 服务器不支持通过 HTTP/SSE 远程托管。

---

## 典型工作流

接入 AI 客户端遵循一套标准流程：

1. **安装**：在 Python 环境中安装 Semantica。
2. **配置客户端**：把 `semantica-mcp` 命令和图谱的绝对路径写进 AI 客户端的 JSON 配置。
3. **启动客户端**：启动 Claude Desktop 或 Windsurf，它们会自动拉起 MCP 服务器。
4. **工具调用**：用自然语言向 AI 提问，AI 会自主串联这 15 个可用工具。
5. **图谱更新**：AI 直接修改你的本地图谱，添加实体、边和决策。

---

## 启动服务器

先安装 Semantica，再配置客户端去启动 MCP 服务器。服务器使用 `stdio` 传输方式运行。

```bash
pip install semantica
```

```bash
# 通过 CLI 入口（推荐）
semantica-mcp

# 或直接通过 Python 模块
python -m semantica.mcp_server
```

默认情况下，服务器以 `WARNING` 级别记录日志，启动时不产生任何输出。把 `SEMANTICA_LOG_LEVEL` 设为 `INFO`（或 `DEBUG`），就能在 stderr 上看到启动信息。不设置 `SEMANTICA_KG_PATH` 时，服务器会初始化一张空的内存图谱——用来测试已经足够。要让图谱跨重启保留，请设置该路径：

```bash
SEMANTICA_KG_PATH=/data/threat_graph.json semantica-mcp
```

<Info>
  不设置 `SEMANTICA_KG_PATH` 时，服务器进程一退出，图谱就会重置。凡是数据需要跨重启保留的会话，务必用绝对文件路径设置该变量。
</Info>

### 通过 `semantica mcp start` 启动

`semantica` CLI 也提供 `semantica mcp start` 子命令。它在后台启动下文介绍的模块化 MCP 服务器，并记录进程 PID，之后可用 `semantica mcp stop` 停止。

```bash
semantica mcp start --transport stdio
semantica mcp stop
```

<Warning>
  `semantica mcp start` 只支持 `stdio` 传输方式（也是默认值）。传入 `--transport http` 时，命令会直接失败并报错 `HTTP transport is not supported (stdio only).`，不会启动任何服务器。`--port` 选项不起作用。
</Warning>

## 连接 Claude Desktop

编辑 Claude Desktop 的配置文件。macOS 上位于 `~/Library/Application Support/Claude/claude_desktop_config.json`，Windows 上位于 `%APPDATA%\Claude\claude_desktop_config.json`：

```json
{
  "mcpServers": {
    "semantica": {
      "command": "semantica-mcp",
      "env": {
        "SEMANTICA_KG_PATH": "/absolute/path/to/knowledge_graph.json",
        "SEMANTICA_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

保存后重启 Claude Desktop。Semantica 工具会自动出现在工具面板里，Claude 在任何对话中都能调用它们。

如果 `semantica-mcp` 不在系统 PATH 上（例如安装在虚拟环境中），请在 `"command"` 里写完整的二进制绝对路径：`"/path/to/venv/bin/semantica-mcp"`。

## 连接其他客户端

**Windsurf。** 在 Settings → MCP Servers → Add Server 中添加，或编辑 `~/.windsurf/mcp_servers.json`：

```json
{
  "semantica": {
    "command": "semantica-mcp",
    "env": { "SEMANTICA_KG_PATH": "/absolute/path/to/knowledge_graph.json" }
  }
}
```

**VS Code（Cline / Roo Code / Continue）。** 在项目根目录的 `.mcp.json` 中添加：

```json
{
  "servers": {
    "semantica": {
      "type": "stdio",
      "command": "semantica-mcp",
      "env": {
        "SEMANTICA_KG_PATH": "${workspaceFolder}/knowledge_graph.json",
        "SEMANTICA_LOG_LEVEL": "DEBUG"
      }
    }
  }
}
```

**Docker**：

```bash
docker run --rm -i \
  -e SEMANTICA_KG_PATH=/data/kg.json \
  -v /local/absolute/path:/data \
  ghcr.io/semantica-agi/semantica-mcp:latest
```

## 智体能做什么：15 个工具

接入之后，大语言模型(LLM)可以在对话中调用以下任意工具，智能体会自动串联调用顺序。你只需描述想要什么，不必亲自编排步骤。

**实体与关系抽取。** `extract_entities` 从自由文本中提取命名实体；`extract_relations` 抽取语义关系和资源描述框架(RDF)三元组。这两个工具不需要任何预处理，就能把一份原始的开源情报(OSINT)报告变成结构化的图谱输入。

**知识图谱操作。** `add_entity` 添加节点，`add_relationship` 添加有向边。抽取完成后，智能体调用这两个工具，把发现的内容持久化进实时图谱。

**图谱实时查询与编辑。** `query_graph` 无需导出即可读取图谱：获取单个节点、沿邻居遍历至多五跳，或按关键词搜索节点。`update_node` 把属性(Property)合并到已有节点上（比如把任务节点标记为 `done`）；`delete_node` 归档不再追踪的节点。设置了 `SEMANTICA_KG_PATH` 时，`update_node` 和 `delete_node` 会把修改写回该文件，重启后依然保留。

**决策智能。** `record_decision` 把决策写成带溯源(Provenance)的节点，附上置信度分数、推理过程和决策者身份。`query_decisions` 按查询或类别检索历史决策。`find_precedents` 用语义相似度找出最相似的历史决策。`get_causal_chain` 沿上游或下游追踪决策因果。

**推理。** `run_reasoning` 对一组事实应用前向链式 IF/THEN 规则，返回推导出的结论。

**分析与导出。** `get_graph_analytics` 计算 PageRank 中心性(Centrality)和社区发现(Community Detection)。`get_graph_summary` 返回节点数、决策数和服务器状态。`export_graph` 把当前图序列化为 Turtle（`"turtle"` / `"ttl"`）、RDF/XML（`"xml"`）、N-Triples（`"nt"`）、JSON-LD（`"json-ld"`）或纯 JSON（`"json"`）。

## 通用示例：员工名录

在进入复杂的领域示例之前，先看一个人人都能看懂的简单会话。一位 HR 经理在 Claude Desktop 里输入提示词：

> "从这段关于 Alice 调往工程部的会议记录中抽取实体，把它们加入图谱，并记录一条晋升决策。"

Claude 自动串联了四次工具调用：

```text
1. extract_entities(text="Alice is transferring to Engineering...")
   → { "entities": [{"label": "Alice", "type": "Employee"}, {"label": "Engineering", "type": "Department"}] }

2. add_entity(id="emp-alice", label="Alice", type="Employee")
   add_entity(id="dept-eng", label="Engineering", type="Department")

3. add_relationship(source="emp-alice", target="dept-eng", type="WORKS_IN")

4. record_decision(
       category="promotion",
       scenario="Alice transferring to Engineering",
       reasoning="Approved by Engineering Director",
       outcome="transfer_approved",
       confidence=1.0
   )
```

新的组织结构和一条完整可审计的决策轨迹随即写入图谱。

## 观摩一场真实的智能体会话

下面看看网络安全分析师在 Claude Desktop 输入提示词、图谱处于在线状态时会发生什么。提示词是：

> "从这份 OSINT 报告中抽取实体和关系，加入知识图谱，然后为 APT29 记录一条置信度 0.88 的归因决策，并把完整图谱导出为 Turtle。"

Claude 自动串联了六次工具调用：

```text
1. extract_entities(text="<report text>")
   → { "entities": [{"label": "APT29", "type": "ThreatActor"}, ...] }

2. extract_relations(text="<report text>")
   → { "relations": [{"source": "APT29", "type": "EXPLOITS", "target": "CVE-2024-3400"}] }

3. add_entity(id="apt29", label="APT29", type="ThreatActor", metadata={"alias": "NOBELIUM"})
   → { "status": "added", "id": "apt29" }
   （对每个抽取出的实体重复此步）

4. add_relationship(source="apt29", target="cve-2024-3400", type="EXPLOITS",
                    metadata={"confidence": 0.97})
   → { "status": "added" }
   （对每条抽取出的关系重复此步）

5. record_decision(
       category="threat_attribution",
       scenario="C2 beacon from 185.220.101.47, TTP T1566.001 observed",
       reasoning="IP overlaps APT29 infrastructure cluster; TTPs match NOBELIUM phishing playbook",
       outcome="attributed_to_apt29",
       confidence=0.88,
       decision_maker="analyst_zhang"
   )
   → { "decision_id": "dec_a3f2b1", "status": "recorded" }

6. export_graph(format="turtle")
   → { "format": "turtle", "data": "@prefix ... <apt29> a :ThreatActor ..." }
```

分析师只用自然语言问了一个问题，就有六次结构化工具调用作用在实时图谱数据上。一轮对话下来，你得到的是：一张填充好的图谱、一条带完整溯源且已记录在案的归因决策，以及一份随时可供 SPARQL 端点使用的 Turtle 导出文件。

## 三个只读资源

资源(Resource)无需调用工具即可暴露图谱状态，客户端可以在任意时刻读取：

| URI | 说明 |
| :-- | :---------- |
| `semantica://graph/summary` | 节点数、决策数、服务器状态 |
| `semantica://decisions/list` | 最多最近 50 条已记录决策 |
| `semantica://schema/info` | 服务器版本、能力、可用工具列表 |

## 模块化服务器：22 个工具与 4 个资源

Semantica 还附带一个模块化 MCP 服务器，由 `semantica mcp start` 启动（等价于 `python -m semantica_mcp.mcp.server`）。它同样只通过 `stdio` 通信，但提供更大的工具集：22 个工具和 4 个只读资源。

| 分组 | 工具 |
| :-- | :-- |
| 抽取 | `extract_entities`、`extract_relations`、`extract_all` |
| 决策智能 | `record_decision`、`query_decisions`、`find_precedents`、`get_causal_chain`、`analyze_decision_impact`、`link_decisions` |
| 知识图谱 | `add_entity`、`add_relationship`、`search_graph`、`get_graph_summary`、`get_graph_analytics` |
| 推理 | `run_reasoning`、`abductive_reasoning` |
| 导出与溯源 | `export_graph`、`get_provenance` |
| 语义检索 | `store_document`、`retrieve_context`、`update_document`、`remove_document` |

除上表三个资源外，模块化服务器还提供 `semantica://ontology/schema`，返回完整的本体(Ontology) schema。

**语义检索。** 需要让 AI 基于你自己的文档回答问题时，使用这组工具。

- `store_document` 把文档切分成块、生成嵌入并存入向量库。文档以 `(source, version)` 为键。重复存储内容相同的文档不会产生任何变化。
- `retrieve_context` 对自然语言查询生成嵌入，返回最相关的文本块及其分数和溯源信息，并附上知识图谱中的相关关系。`top_k` 默认为 5，最大为 10。
- `update_document` 替换由 `(source, version)` 标识的已存储文档内容。找不到匹配文档时返回 `not_found`。
- `remove_document` 从向量库中删除 `(source, version)` 下的全部文本块。

```text
1. store_document(content="<policy manual text>", source="policy_manual#page12", version="v2")
2. retrieve_context(query="员工出差报销上限是多少？", top_k=3)
3. update_document(content="<revised text>", source="policy_manual#page12", version="v2")
4. remove_document(source="policy_manual#page12", version="v2")
```

## 领域示例

<Tabs>

<Tab title="国防：CTI/威胁情报">

网络威胁情报(CTI)团队用 Claude Desktop 把新的 OSINT 报告与既有威胁图谱做关联、记录归因决策，并通过自然语言查询因果链——图谱全程实时更新。

**分析师提示词：**
> "从这份 Mandiant 关于 APT40 的报告中抽取实体，加入知识图谱，查找与 APT40 归因相关的历史决策，并记录一条置信度 0.84 的新归因决策。"

Claude 自动串联：

1. `extract_entities(text="Mandiant APT40 report text...")`
2. `add_entity(id="apt40", type="ThreatActor", label="APT40")`
3. `find_precedents(scenario="APT40 spear-phishing campaign attribution", max_results=3)`
4. `record_decision(category="attribution", scenario="APT40 campaign matches known TTPs", outcome="attributed_apt40", confidence=0.84, decision_maker="cti_lead_01")`
5. `export_graph(format="json-ld")`

归因决策在图谱中留下可审计的记录，与来源实体相互关联，随时可用于情报共享。

</Tab>

<Tab title="安全：SOC/事件响应">

事件处置进行中时，安全运营中心(SOC)用 Claude 对图谱做推理、应用零信任策略规则，并把遏制决策连同因果链一起记录下来，形成实时审计轨迹。

**SOC 分析师提示词：**
> "把 WKSTN-047 和 DC01 添加为主机，添加二者之间的横向移动关系，运行推理判定严重级别，并记录一条遏制决策。"

Claude 串联调用：

1. `add_entity(id="wkstn-047", type="Host", label="WKSTN-047")`
2. `add_entity(id="dc01", type="Host", label="DC01")`
3. `add_relationship(source="wkstn-047", target="dc01", type="lateral_movement")`
4. `run_reasoning(facts=["Host(WKSTN-047)", "LateralMove(WKSTN-047, DC01)", "DC(DC01)"], rules=["IF LateralMove(X, Y) AND DC(Y) THEN CriticalIncident(X)"])`
5. `record_decision(category="containment", scenario="Lateral movement to DC detected", outcome="isolate_wkstn047", confidence=0.95)`
6. `get_causal_chain(decision_id="...", direction="downstream", max_depth=3)`

遏制决策及其下游影响都被图谱捕获，供事后复盘使用。

</Tab>

<Tab title="生命科学：临床/制药">

临床 AI 助手借助 MCP 服务器记录带溯源的治疗决策、检索指南先例，并导出决策图，用于监管申报和多学科诊疗(MDT)审查。

**临床提示词：**
> "患者 eGFR 为 28，正在服用二甲双胍。查找肾功能重度减退时二甲双胍剂量调整的先例，然后记录一条治疗调整决策。"

Claude 依次调用：

1. `find_precedents(scenario="metformin with eGFR below 30", max_results=5)`
2. `record_decision(category="treatment_modification", scenario="eGFR 28, current metformin 1000mg BD", reasoning="eGFR 28 is below the 30 mL/min/1.73m2 absolute contraindication threshold per BNF and NICE NG28", outcome="discontinue_metformin_switch_to_gliclazide", confidence=0.97, decision_maker="clinical_ai_v2")`
3. `get_causal_chain(direction="upstream")` 会呈现出驱动该决策的指南节点
4. `export_graph(format="json-ld")` 生成供 MDT 审查使用的决策图

图谱完整记录了这条决策、它的指南依据和因果链，监管审计时均可检索。

</Tab>

<Tab title="银行：风险/合规">

信贷风险团队用 MCP 服务器记录每一笔信贷决策及其推理链、调取监管先例，并导出合规图谱，供巴塞尔协议III(Basel III)模型治理审查。

**信贷分析师提示词：**
> "为 APP-2025-994421（贷款价值比(LTV) 78%，偿债收入比(DSTI) 38%，信用分 714）记录一笔有条件按揭审批，找出最相似的三笔历史审批，并返回该决策的因果链。"

Claude 依次调用：

1. `record_decision(category="mortgage_origination", scenario="LTV 78%, DSTI 38%, credit score 714, first-time buyer", reasoning="LTV within 80% cap; DSTI 38% under stressed rate scenario breaches 35% guideline — conditional approval with LMI requirement", outcome="approved_conditional_lmi", confidence=0.89, decision_maker="credit_model_v3")`
2. `find_precedents(scenario="mortgage approval borderline DSTI stress test", max_results=3)`
3. `get_causal_chain(decision_id="...", direction="upstream", max_depth=5)`
4. `export_graph(format="turtle")` 为模型治理委员会生成决策溯源图

最终产出一条带先例链接、完全可审计的信贷决策轨迹，随时可用于 SR 11-7 模型风险治理审查。

</Tab>

</Tabs>

---

## 常见陷阱

- **把 MCP 当成 HTTP 服务器。** 不要试图 `curl` MCP 服务器，也别去找端口号。它通过 `stdin/stdout` 通信，等待父级 AI 客户端发来 JSON-RPC 消息。
- **给 `SEMANTICA_KG_PATH` 用相对路径。** AI 客户端以子进程方式启动服务器，工作目录难以预测。务必使用绝对路径（例如 `C:\Users\Name\graph.json` 或 `/Users/name/graph.json`），以免丢失数据。
- **虚拟环境的 PATH 问题。** 如果 Semantica 安装在 Python 虚拟环境中，Claude Desktop 在全局系统 PATH 上找不到 `semantica-mcp`。必须在 `"command"` 字段里写二进制的绝对路径。
- **指望远程托管。** 基于 stdio 的 MCP 服务器必须与 AI 客户端同在一台本机运行，不支持跨网络的远程执行。
- **混淆 MCP 集成与 `AgentContext`。** 如果你要自己写 Python 代码编排 LLM，就不要用 MCP 服务器，直接在代码里使用 `AgentContext` 类。

---

## 故障排查

**服务器没有出现在 Claude Desktop 里。** 编辑配置后要完全退出并重新打开 Claude Desktop（只关窗口不够）。确认二进制在 PATH 上：Unix 用 `which semantica-mcp`，Windows 用 `where semantica-mcp`。如果使用虚拟环境，`"command"` 里写二进制的绝对路径。把 `SEMANTICA_LOG_LEVEL` 设为 `DEBUG`，并检查 stderr 里的启动报错。

**图谱数据没有跨会话持久化。** 把 `SEMANTICA_KG_PATH` 设为绝对文件路径。不设置时图谱只存在于内存，服务器每次重启都会清空。

**工具调用返回空结果。** `get_graph_summary` 返回 `"node_count": 0` 说明图谱是空的。先用 `add_entity` 和 `add_relationship` 填充图谱，或先对文本运行 `extract_entities`，再对每个结果调用 `add_entity`。

**`SEMANTICA_KG_PATH` 权限错误。** 服务器进程需要对该文件及其父目录的读写权限。如果在 Docker 里运行，请检查卷挂载与文件属主。

## 相关指南

- [推理与规则](./reasoning.md)：`run_reasoning` 工具背后的引擎
- [决策智能](./decision-intelligence.md)：决策如何作为因果图节点存储
- [上下文图](./context-graphs.md)：`add_entity` 和 `add_relationship` 写入的那张图
- [导出与序列化](./export.md)：`export_graph` 支持的全部导出格式
- [本体管理(Ontology)](./ontology.md)：从经由 MCP 构建的图谱生成网络本体语言(OWL)本体
