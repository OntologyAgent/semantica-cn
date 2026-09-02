# StockInsight 项目深读摘要（贯穿案例事实源）

> 来源：子代理深读 `projects/StockInsight/`（GUIDE.md、PLAN.md、scripts/、数据样例、_archive/）
> semantica 版本：0.6.7（.venv 实测）
> ⚠️ 现状：项目 2026-09-02 从 `projects/stock/` 重构为 `StockInsight/` 三级结构。GUIDE.md 里的路径（projects/stock/、output/、output_llm/）均为旧路径，产物已归档到 `_archive/`；`stocks/00100/std/` 为空——**std 契约目前只存在于 PLAN.md 定义，尚未落地**。

## A. 已验证流水线步骤表（API 逐字对照脚本代码）

| 步骤 | 模块 | 实际调用的 API（逐字） | 输入 | 输出产物 | 验证状态 |
|---|---|---|---|---|---|
| 1 摄取 | `semantica.ingest.FileIngestor` | `FileIngestor().ingest_file(report_path)` → `.path`（investment_pipeline.py L85） | 财报 PDF/TXT/HTM | sources 对象 | ✅ 真实 PDF 382KB/21 页 |
| 2 解析 | `semantica.parse.DocumentParser` | `DocumentParser().parse(sources.path)`，返回 dict 取 `parsed["text"]`（L89-90） | sources.path | 纯文本（14,197 字） | ✅ pdfplumber |
| 3 抽取(LLM) | `semantica.semantic_extract` | `NERExtractor(method="llm", provider="openai", model="glm-5.3-flash", base_url="https://open.bigmodel.cn/api/coding/paas/v4", api_key=api_key)`；`RelationExtractor(...)` 同参（L125-138）；`ner.extract(text)`、`rel.extract(text, entities=entities)`（L157-158） | 解析文本 | entities / relationships | ✅ 39 实体/43 关系 |
| 4 本体 | `semantica.ontology.OntologyEngine` | `OntologyEngine(base_uri="https://investment.example/ontology/")`；`engine.from_data({"entities": entities, "relationships": relationships})`（L164-167） | 抽取结果 | `investment_ontology.json` | ✅ 12 类本体 |
| 5 建图 | `semantica.kg.GraphBuilder` | `GraphBuilder(merge_entities=True)`；`builder.build({"entities": ..., "relationships": ...})`（L177-178） | 实体+关系 | graph dict → graph.json | ✅ 48 节点/66 边 |
| 6 溯源 | `semantica.provenance.ProvenanceManager` | `prov.track_entity(str(eid), sources.path, metadata={"confidence": 0.7})`（L185-189） | 实体+源路径 | PROV 记录 | ✅ |
| 7 导出 | `semantica.export` | `RDFExporter().export(graph, file_path=<out>/graph.ttl, format="turtle")`；`ParquetExporter().export(graph, file_path=<out>/graph.parquet)`（L197, L202） | graph | Turtle/Parquet/JSON/HTML | ✅ |
| 8 策略 | `semantica.context.AgentContext` | `AgentContext(vector_store=VectorStore(backend="faiss", dimension=384), knowledge_graph=ContextGraph(advanced_analytics=True), decision_tracking=True)`；`record_decision(category=, scenario=, reasoning=, outcome=, confidence=)`；`find_precedents("earnings growth", limit=3)`（L213-226） | graph+决策描述 | 决策记录 HOLD_AND_MONITOR | ✅ 0.72 |
| 冲突检测 | `semantica.conflicts` | `ConflictDetector()`；`detector.detect_conflicts(graph)`（build_full_graph.py L35-36） | 合并后 graph | 冲突列表（`.severity`/`.conflict_type.value`/`.entity_id`/`.property_name`） | ✅ GLW/NYSE 冲突自动标记 |
| 冲突消解 | `semantica.conflicts.ConflictResolver` | `resolver.resolve_conflicts(conflicts, strategy="highest_confidence")` → `.resolved`（L42-44） | 冲突列表 | 消解结果 | ✅ |
| 推理 A | `semantica.reasoning.Reasoner` | `engine.add_fact("revenue_growth(MiniMax, 283.1)")`；`Rule(rule_id=, name=, rule_type=RuleType.IMPLICATION, conditions=["revenue_growth(MiniMax, ?g)"], conclusion="high_growth_signal(MiniMax, ?g)", confidence=0.9)`；`engine.infer_with_results(facts, rules)`（investment_reasoning.py L21-44） | 事实字符串+规则 | 信号 0.80 | ✅ |
| 推理 B | `semantica.reasoning.DatalogReasoner` | `engine.add_rule("indirect_subsidiary(X, Y) :- subsidiary_of(X, Y).")`；`engine.query("indirect_subsidiary(X, Y)")`（L63-68） | Horn 子句字符串 | 传递闭包 3 条 | ✅ |
| 决策留痕 | `semantica.context.ContextGraph` | `cg.record_decision(category=, scenario=, reasoning=, outcome=, confidence=, decision_maker=)`（pipeline_v3_llm.py L179-184、process_docs.py L203-211） | 决策描述 | decision_id | ✅ |
| 图分析 | `semantica.kg.PathFinder / GraphAnalyzer` | `finder.find_shortest_path(G, source, target)`；`analyzer.calculate_centrality(G, method="degree")`（graph_analytics.py L39-49）。GraphBuilder.build() 返回 dict 需先转 networkx（L26-36 有标准转换） | networkx 图 | 路径/中心度/社区 | ✅ |
| LLM 直连 | `semantica.semantic_extract.providers.create_provider` | `create_provider("openai", model="glm-5.3-flash", base_url="https://open.bigmodel.cn/api/coding/paas/v4", api_key=os.getenv("ZHIPU_API_KEY"))` → `llm.generate(prompt)`（pipeline_v3_llm.py L20-23、L77）。源码签名 `create_provider(name, use_pool=True, **kwargs)`（providers.py L1576） | 提示词 | JSON 文本 | ✅ |
| 图存储 | FalkorDB | ① `redis.Redis(host, port)` + `r.execute_command("GRAPH.QUERY", GRAPH_NAME, cypher)`；② `falkordb.FalkorDB(host="localhost", port=6379)` + `db.select_graph(...)` + `graph.query(cypher)` | final/累计图 JSON | graph=investment / minimax_full | ✅ 59 节点/81 边 |

## B. 五个数据域（PLAN.md L91-118）

| 域 | 数据源（可信度） | 采制 | std 契约 | 状态 |
|---|---|---|---|---|
| 1 公告 | 披露易 HKEXnews ★★★ | announcements.json 索引 + PDF/HTM 下载 | `process_docs.py` LLM 抽取 → `std/announcements__<batch>.std.json` | raw 47 份就绪；process_docs.py 现写累计图，未输出 std |
| 2 新闻/社媒 | Reuters/SCMP/澎湃 ★★☆；社媒低可信 | 人工整理 `news_<date>_<slug>.md`（frontmatter+150~400 字），`related_announcements` 关联域1 | `process_news.py` → `news__<batch>.std.json`（待写） | raw 35 份事件+索引+schema 就绪 |
| 3 行情 | yfinance 00100.HK 日线 ★★☆ | `fetch_market.py` 拉 OHLCV | `raw/market_00100.parquet`（date,open,high,low,close,volume,amount,currency）→ 按月/事件窗口聚合 std；只出数据不出叙事 | ❌ 待建 |
| 4 基本面 | 公告 PDF 唯一权威 ★★★ | 不重复采——域1 加财务模板 | `raw/fundamentals_00100.parquet`（period,metric,value,unit,yoy,source_doc,confidence） | ❌ 待建 |
| 5 行业/宏观 | FRED ★★★、恒指/A股 yfinance、行业事件 ★★☆ | `fetch_macro.py` → 项目级 `macro/*.parquet` | 进图用 `MacroIndicator`/`MarketIndex` 实体 + `context_of` 关系，多股共享 | ❌ 待建（macro/ 为空） |

**std schema**（PLAN.md L122-136 逐字）：
```json
{
  "batch_id": "announcements__20260826",
  "stock": "00100",
  "domain": "announcements | news | market | fundamentals | macro",
  "source": {"type": "hkexnews|media|api", "url": "...", "retrieved_at": "..."},
  "entities": [{"id","text","label","confidence","metadata":{"source","domain","date"}}],
  "relationships": [{"source","target","type","confidence","metadata":{}}],
  "facts": [{"subject","predicate","object","value","unit","period","confidence"}]
}
```
硬性要求：每条必带 `metadata.source` + `domain`（PROV-O 溯源不可断）；事件日期入 `metadata.date`；命名 `<domain>__<batch>.std.json` 一文件一批次，**追加不覆盖**；时序域按月/事件窗口聚合。

## C. raw → std → final 三级契约（PLAN.md L6-49, L83-85, L138-147）

| 级 | 形态 | 命名 | 生产者 | 消费者 |
|---|---|---|---|---|
| raw/ | 原始数据 flat 平铺，前缀分域 | 公告保留披露易原文件名；新闻 `news_<YYYY-MM-DD>_<slug>.md`；行情/基本面 parquet | fetch_* / 人工 | process_* |
| std/ | `<domain>__<batch>.std.json` 七字段 schema | batch 为日期或文档号 | process_* | merge_std.py（待写） |
| final/ | `stocks/<code>/final_graph.json` 单文件 `{entities, relationships}` 每条带 metadata.source/domain/date | 单文件，**merge_std.py 全量重建（非增量拼接）** | merge_std.py | push_to_falkordb.py + export |

合并链路：各域 std → ConflictDetector（跨域实体名冲突）→ Deduplication → GraphBuilder(merge_entities=True) → final_graph.json → FalkorDB + export。冲突消解 `highest_confidence`，来源优先级 **公告 > 新闻 > 宏观推断**。跨域连接点：`related_announcements`（域2→域1）、`stock_code`（全域→00100.HK）、`period`（域4→域3）、`context_of`（域5→个股）。

铁律：每级只被上一级脚本生成，不越级写、不手工改；股票间零共享（共享仅 scripts/、macro/、.env）；废弃物进 `_archive/<原因>/` 只进不出。

**实际现状**：`final_graph.json`（509 实体/500 关系）实为 process_docs.py 风格的 LLM 累计抽取图（非 std 合并产物）；`to_explorer.py` 转成 `final_graph.explorer.json`（570 实体——补建 61 个悬空端点）供 Explorer 加载。

## D. 坑与踩坑记录

**LLM 接入**
1. 0.6.7 `NERExtractor(method="llm", llm_provider=...)` 实例参数不被识别，必须 `provider="openai"` 字符串 + OpenAI 兼容端点。
2. 智谱只有 `https://open.bigmodel.cn/api/coding/paas/v4` 可用；`api/paas/v4` 报余额不足，`api/v1` 报无权限。
3. 关系抽取方法名**无 `"rule"`**，合法值 pattern/regex/cooccurrence/similarity/dependency/ml/spacy/huggingface/llm；非法名触发 0.6.7 verbose_mode UnboundLocalError bug。
4. pattern 抽取质量差，投资场景必须 LLM。

**冲突与合并**
5. 冲突检测是特性：GLW/NYSE type/name 冲突自动标记，`resolve_conflicts(strategy="highest_confidence")` 消解。
6. 手动桥接兜底：`minimax` 与 `MiniMax Group Inc.` 人工合并后图谱才连通。
7. process_docs.py 自实现合并：实体按规范化名去重（术语表别名归一）；关系按 (source, predicate, target) 键去重，同键不同来源记冲突候选。

**reasoning**
8. `Reasoner` 规则条件须字符串 `"predicate(args)"` 格式。
9. `DatalogReasoner.add_rule` 接受 Horn 子句字符串；add_fact 只接受字符串/dict，参数小写开头。
10. Datalog 变量须为无 `?` 前缀的大写（X/Y）——官方文档写 `?X` 是文档偏差；无 evaluate()，query 自动触发推导。

**FalkorDB**
11. `FalkorDBStore.create_node` 用数字内部 ID，自定义字符串 id 不落库 → 纯 Cypher + `name` 属性为键；建边 MATCH+CREATE；返回 bytes 需 decode。

**图分析**
12. `GraphBuilder.build()` 返回 dict，PathFinder/GraphAnalyzer 要 networkx 图，先转换。

**工程/网络**
13. API key 存 `.env`（600），load_dotenv 读取。**当前 StockInsight/.env 只含 `DEEPSEEK_API_KEY`**。
14. 巨型文档：>20000 字截断抽样前 2 万、1200 字分块、每块最多 3 次重试（间隔 5 秒）、超 12000 字降级轻量三字段模板。
15. 重构遗留路径不一致：process_docs.py 基线路径指向 `../stock/output_v3/graph.json`（已归档）；graph_db.py / push_to_falkordb.py 读的文件不存在。复用脚本先对齐路径。

## E. LLM 配置

| 脚本 | 接入 | model | base_url | key |
|---|---|---|---|---|
| investment_pipeline.py | NERExtractor/RelationExtractor provider="openai" | glm-5.3-flash / moonshot-v1-128k | bigmodel coding/paas/v4 / api.moonshot.cn/v1 | ZHIPU_API_KEY / MOONSHOT_API_KEY（fallback：ZHIPU→MOONSHOT→OPENAI） |
| pipeline_v3_llm.py | create_provider("openai", ...) | glm-5.3-flash | bigmodel coding/paas/v4 | ZHIPU_API_KEY |
| process_docs.py | create_provider("openai", ...) | deepseek-v4-flash-vision-exp | https://api.deepseek.com | DEEPSEEK_API_KEY（当前 .env 唯一在册） |

provider→env 映射：moonshot→MOONSHOT_API_KEY、zai/zhipu→ZHIPU_API_KEY、openai→OPENAI_API_KEY、anthropic→ANTHROPIC_API_KEY、gemini→GEMINI_API_KEY、groq→GROQ_API_KEY。其他走 `semantica.llms.LiteLLM(model=..., api_key=...)`，`SEMANTICA_LLM_MODEL` 可覆盖。

## F. 投资本体

- v1（investment_pipeline.py L34-67）：9 类 Company/Stock/FinancialMetric/FinancialReport/Segment/Executive/Event/MarketData/Strategy；8 关系 reports、has_metric、operates_segment、employed_by、listed_as、affects、part_of_strategy、related_to；含规则约束（Stock: must_have_ticker 等）。
- v2（seed_holdings.py L12-43，当前生效）：12 类 = v1 + ETF、Product、Concept（Report 更名）；13 关系 = v1 + tracks、has_concept、holds、listed_on、ticker_of。
- v3（pipeline_v3_llm.py E 模板）：LLM 归纳 `{"name","base_uri","classes":[{name,label,comment,parent}],"properties":[...]}`，产物 `_archive/output_v3/ontology.json`（11 类/45 属性含 domain/range）。
- final_graph.json 实际分布（509 实体/500 关系）：CONCEPT 201、FinancialMetric 149（属性提升为一等节点）、PRODUCT 49、ORG 46、DATE 31、PERSON 27、GPE 6；关系：has_attribute 223、owl:equivalentClass 24、其余约 253 条为中文自由谓词（包括 17/包含 19/擔任 7/任職於 6/屬於 5/委任 4…长尾 150+ 种）——**无本体约束的 LLM 抽取实况样本，可作"为什么需要本体约束层"的反面案例**。
- 持仓（seed_holdings.py 硬编码 6 只）：MiniMax 0100.HK、希音 SHEIN-W、XL二南方海力士（2x ETF tracks SK Hynix）、梅卡曼德机器人-W、SpaceX（未上市）、康宁 GLW；挂 Strategy 节点 portfolio（holds 边）+ has_concept 连 8 主题概念。
- my_stocks.json 目前是 3 节点演示样例，真实持仓在 seed_holdings.py。

## 附：脚本与 _archive

- **scripts/**（9 个已有）：investment_pipeline.py、seed_holdings.py、build_full_graph.py、investment_reasoning.py、graph_analytics.py、graph_db.py、pipeline_v3_llm.py、process_docs.py、push_to_falkordb.py；根目录 to_explorer.py。
- **PLAN.md 规划未写**：fetch_announcements.py、fetch_market.py、fetch_macro.py、process_news.py、process_fundamentals.py、merge_std.py。
- **_archive/**：stock_v1_v2/（v1/v2 全部产物+3 份对比 md）、output_v3/（全 LLM v3 产物）、00100_output_v0/、00100_dup/、minimax-hkex/、data/corning_q3_sample.txt、MiniMax_完整闭环_最终.md（34 问审计）。
