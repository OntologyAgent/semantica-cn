# Execution Summary — quant-pack-event-impact-01M1KS3R

**日期**: 2026-09-03 | **分支**: `feature/quant-pack-event-impact` | **代理**: Claude（实现代理）
**目标**: hk-quant-qlib 数据包三域入图（行情/基本面/宏观）+ 事件研究法影响分析（零 LLM）。

## 一、交付物

| # | 交付 | 位置 |
|---|---|---|
| A | 数据包导入（CSV→契约 parquet，重跑逐字节一致） | `projects/StockInsight/scripts/import_quant_pack.py` |
| B | 三域确定性处理器（零 LLM） | `scripts/process_market_std.py` / `process_fundamentals_std.py` / `process_macro_std.py` |
| C | merge_std 两处扩展（CREDIBILITY 4 行 + META_KEEP.stock_code 透传，FR-003） | `scripts/merge_std.py` |
| D | 事件影响分析器（事件研究法，幂等写回） | `scripts/impact_analysis.py` |
| E | 影响报告 + record_decision 留档 | `stocks/00100/impact_report.md` |
| F | 文档同步 + 双验收 | `PLAN.md` / `PROCESSING_MANIFEST.md` / `scripts/check_quant_acceptance.py` |

数据产物：`stocks/00100/raw/market_00100.parquet`（160 日）、`raw/fundamentals_00100.parquet`
（678 行：8 期指标 + 三大报表科目 + 档案）、`macro/{fred,index_hk,hibor,lpr,pmi}.parquet`
（长表 date/series_id/value）+ `macro/_sources.json`（manifest 溯源旁车）。

## 二、final 新规模

| 指标 | 值 |
|---|---|
| std 批次 | 114 = 既有 91（公告 48 + 新闻 43）+ 新 23（market 9 + fundamentals 9 + macro 5） |
| merge final | 1098 实体 / 1724 关系（GraphValidator is_valid=True，SHACL conforms=True 违例 0） |
| 三域新实体 | MarketData 月度快照 9、FinancialMetric 期实体 8、MarketIndex 4、MacroIndicator 18 |
| 跨域连接 | context_of 边 22 条（宏观/指数 → 00100.HK）；全域实体 metadata.stock_code 100% 挂靠 |
| 冲突检测 | 74 条检出 / 74 条 credibility_weighted 消解（新批次未引入假冲突，同 id 分组口径） |
| 源头治理度量计 | 繁简折叠 1 组（≤10）、指代 ALIAS 0 条（≤5）——既有防线不受新批次影响 |
| merge 耗时 | 3.4s（NFR-003 端到端 < 10 分钟，实测全链 < 30s） |

注：merge_std.py 在本次执行期间有并行会话叠加的改动（通用市场别名/谓词归一，
D-20260903-02/03/04），已按磁盘现状兼容消费；上述数字为最终态重跑结果。

## 三、事件影响层（FR-004/FR-005）

- 事件 298 个 Event 实体：可定价 248、**no_price_data 50**（上市前公告/新闻 +
  2 个数据末端后的未来股东会预告，如实标注不伪造）
- impact_5d 覆盖 215（窗口完整口径）、impact_20d 覆盖 188（尾部事件窗口截断留痕
  `window_20d_incomplete`）；可定价事件 benchmark=HSCCI + event_type 覆盖 100%
- 口径（报告方法论节与脚本常量一一对应）：T+0 非交易日顺延下一交易日留痕
  （22 例）；impact_0d 相对前收；impact_k=close(T+k)/close(T0)−1；
  abnormal_k=个股−HSCCI 同窗口
- **impact 覆盖率**：可定价且窗口完整事件 100% 带 impact_*/abnormal_* 字段；
  幂等验证：重跑 `_impact_analysis.json` 逐字节一致、impact 字段 0 差异
- record_decision(category="impact_analysis") 已留档并并入 final（决策 44e90d62…）

### 报告要点摘录（T+5 超额，个股−HSCCI）

- `product_release`（18 例）：T+5 平均 **+23.06%**、中位 +35.19%、正比例 77% —— 发布事件是历史上最强的正向类别，但 T+20 回落至 +18.45%（冲高后回吐）。
- `announcement`（74 例）：T+0 +1.18% / T+5 +1.55%，反应温和；T+20 +9.83%。
- `board_change`（23 例）：T+5 −1.58%、T+20 **−31.30%**（正比例仅 5%）—— 董事会变动窗口内显著跑输。
- `financing`（7 例）：T+5 −13.66% 但 T+20 +21.30% —— 短空长多的分裂形态（样本小，慎读）。
- Top 正超额 T+5：2026-06-12 竞品发布日逆势 +63.4%、2026-02-11 董事会公告 +62.6%；Top 负超额：2026-06-04 M3 评测争议簇 −30.6%、2026-07-07 月报表 −32.1%。
- 聚类事件提示已写入方法论：同日多事件共享窗口，类型间差异含自相关，不作因果解读（C-004 免责声明落报告第四节）。

## 四、验收（FR-007）

**既有门禁（check_acceptance.py，exit=0）**：A1 裸指代 0 / A2a 繁简分裂 0 组 /
A3 GraphValidator / A4 SHACL conforms=True / A5 valid_from 覆盖 95.5% /
M1=1（≤10）/ M2=0（≤5）/ R1 对账 114 批次 + 0 显式失败。

**新增断言（check_quant_acceptance.py，exit=0 → `std/_acceptance_quant.md`）**：

| # | 断言 | 结果 |
|---|---|---|
| Q1 | 三域批次消费 market/fundamentals/macro = 9/9/5 | ✅ |
| Q2a | 可定价事件 benchmark+event_type 覆盖 100%（215/215） | ✅ |
| Q2b | no_price_data 50 个全部无价格可算（上市前/数据末端后） | ✅ |
| Q3 | 抽检 3 事件（2026-01-09 financing / 2026-05-19 other / 2026-08-06 announcement）独立 pandas 复算 T+5/T+20 超额一致（容差 5e-7） | ✅ |
| Q4 | 确定性明细留痕 `_impact_analysis.json`（sha256=b0177552ab9862f3） | ✅ |

**确定性（NFR-001）**：import_parquet 重跑哈希一致；全链（import→三处理器→merge→
to_explorer→impact）重跑通过；impact 重跑 impact 字段 0 差异。零 LLM 调用。

## 五、边界与遗留

- 现金流量表源数据缺 2026-06-30 期（东财未发布），如实缺批次。
- `Event` 的 event_type 在 final 的 metadata 被 META_KEEP 过滤（既有约定），影响层
  从 std events 段重建众数映射写回 properties——未改 META_KEEP 词表面。
- FalkorDB 推送（PLAN 第 10 步）不在本使命范围，final_graph.json 就绪即可推送。
- 纪律遵守：hk-quant-qlib 仓库零改动（C-002）；projects/ 未进 git（C-003）；
  既有 89 批次未动；merge_std 仅 CREDIBILITY + META_KEEP 两处扩展（C-001）。
