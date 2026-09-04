# StockInsight 00100 全量原始数据分析

**Mission**: stockinsight-raw-analysis-01M1HKNW | **类型**: software-dev | **日期**: 2026-09-03
**授权**: 用户全权委托（睡眠期间自主执行）；方法论依据 = [本体建模最佳实践文档集](../../docs/best-practices/本体建模最佳实践.md)（同夜完成的 5 篇）

## 一、背景与目标

用户委托：按新最佳实践的九阶段契约，**全量（不遗漏）**处理 `projects/StockInsight/stocks/00100/raw/` 的 98 个原始文件，产出 PLAN.md 定义的 std 中间批次，合并重建 final 图谱并入资产库。这是 std 契约的**首次落地**（此前只有定义无实现）。

## 二、范围（对账口径）

| 数据 | 数量 | 处理域 | 方式 |
|---|---|---|---|
| 公告 PDF | 44 | announcements | LLM 抽取（deepseek，process_docs.py 的分块/截断/重试模式） |
| 公告 HTM/HTML | 3 | announcements | 同上 |
| 新闻事件 MD | 35 | news | frontmatter + 叙述，LLM 抽取 |
| 人工研究 MD | 14 | news（source.type=research） | 同上 |
| 索引 JSON | 2 | —（脚本消费，不单独抽取） | 元数据 |
| 行情/基本面/宏观 parquet | 0（数据未采集，PLAN.md 待建项） | — | 超范围，如实记录 |

对账公式：`输入内容文件数(96) = 成功处理数 + 显式失败记录数`，禁止静默跳过。

## 三、功能需求

| ID | 需求 | 状态 |
|---|---|---|
| FR-001 | 全量覆盖：96 个内容文件全部处理；产出对账清单（文件级：处理/失败/原因） | 已确认 |
| FR-002 | std 契约落地：每文件产出 `stocks/00100/std/<domain>__<batch>.std.json`，符合 PLAN.md 七字段 schema（batch_id/stock/domain/source/entities/relationships/facts）；每条带 `metadata.source`+`domain`；事件日期入 `metadata.date`；追加不覆盖 | 已确认 |
| FR-003 | 顺序铁律：冲突检测（SourceTracker 注册可信度 公告0.95>研究0.60>新闻0.70 修正为 公告>新闻>研究）→ 消解 → 去重 → 建图（最佳实践篇2 3.4/3.7） | 已确认 |
| FR-004 | final 全量重建：`merge_std.py` 从全部 std 重建 `stocks/00100/final_graph.json`；旧 final_graph.json（509 实体累计图）先归档 `_archive/final_v0/` | 已确认 |
| FR-005 | 资产入库：provenance 持久化（storage_path）+ RDF(Turtle 含溯源)/Parquet 导出 + 决策记录（record_decision） | 已确认 |
| FR-006 | 脚本股票无关：`--stock <code>` 参数化，放 `projects/StockInsight/scripts/`；不修改既有脚本（只新增） | 已确认 |

## 四、非功能需求

| ID | 需求 | 状态 |
|---|---|---|
| NFR-001 | 幂等重跑：重跑生成新 batch 不覆盖既有文件；失败文件记录 `<domain>__failures.jsonl` 可断点续跑 | 已确认 |
| NFR-002 | 图质量：GraphValidator 校验，悬挂边（DANGLING_EDGE）修复后复检；SHACL 校验（pyshacl 已装） conforms 或违例清单留档 | 已确认 |
| NFR-003 | 抽取目标受控：LLM 提示词绑定投资本体 v2 的 12 类实体类型词表（Company/Stock/ETF/FinancialMetric/Report/Segment/Executive/Event/MarketData/Product/Concept/Strategy），不让 LLM 自由发挥（篇2 3.2 契约） | 已确认 |

## 五、约束

- C-001 只新增脚本（process_announcements_std.py / process_news_std.py / merge_std.py），不改既有 9 个脚本
- C-002 `projects/` 不进 git（仓库纪律）；本使命 git 产物仅 kitty-specs
- C-003 LLM 用 `.env` 的 `DEEPSEEK_API_KEY`（deepseek-v4-flash-vision-exp @ api.deepseek.com，process_docs.py 已验证配置）
- C-004 代理网络注意：LLM 走 api.deepseek.com 需放行（StockInsight 坑 13/14 记录）

## 六、成功标准

1. 对账清单闭合：96 = 成功 + 显式失败，无静默遗漏
2. std 批次可被 merge_std 全量消费重建 final；重建图通过结构校验
3. 全链按最佳实践九阶段顺序执行，决策记录含本次分析结论
4. 脚本可对其他股票复用（--stock 参数化验证）

## 七、假设

- deepseek key 有效且余额充足（.env 在册）
- 旧 final_graph.json 归档后 to_explorer.py 仍可对新文件运行（格式同构）
- 行情/基本面/宏观域无数据，本次不处理（PLAN.md 待建项，如实记录不算遗漏）
