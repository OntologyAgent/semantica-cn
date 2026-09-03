# 量化数据包接入与事件影响分析

**Mission**: quant-pack-event-impact-01M1KS3R | **类型**: software-dev | **日期**: 2026-09-03
**分支**: `feature/quant-pack-event-impact`
**用户目标**：**知道各类事件对股票价格的影响，为以后的分析和决策提供依据**（原话，2026-09-03 授权执行）

## 一、背景

前序使命已完成：公告/新闻全量抽取（89 批 std v2，296 个带日期 Event 实体）、best-practices 对齐（源头治理度量计 88→1 / 74→0）、final 1089 实体/1711 关系。PLAN.md 的域 3（行情）/域 4（基本面）/域 5（宏观）一直待建——用户现提供 [hk-quant-qlib 数据包](../../../../../Users/luofisher/hk-quant-qlib/data/minimax_stock/)（机器可读 manifest）补齐三域，并要求在此基础上建**事件影响分析**能力。

## 二、用户场景

**主场景（决策依据查询）**：投资者问「业绩公告这类事件，历史上对 00100 价格影响多大？」——打开影响报告或查图，得到按事件类型聚合的超额收益统计（如业绩类事件 T+5 平均超额 +X%，监管类 -Y%）与单事件明细；未来新事件发生时，Agent 按 `find_precedents` 检索同类事件及其历史价格反应，作为决策输入。

**场景二（可复现）**：新数据包到达 → 重跑导入与处理器 → merge → 影响分析，全链确定性、同输入逐字节一致，无 LLM 成本。

**边界**：上市日 2026-01-09 之前的事件（递表期公告/新闻）无价格数据——如实标注 `no_price_data`，不伪造。

## 三、功能需求

| ID | 需求 | 状态 |
|---|---|---|
| FR-001 | 数据包导入：`import_quant_pack.py --src <包路径> --stock 00100`，CSV → 契约 parquet（行情 raw/market_00100.parquet：date/open/high/low/close/volume/amount/currency+衍生列；基本面 raw/fundamentals_00100.parquet：period/metric/value/unit/source_doc/confidence+report_type；宏观 macro/{fred,index_hk,hibor,lpr,pmi}.parquet），manifest 来源信息入 metadata | 已确认 |
| FR-002 | 三域确定性处理器：`process_market_std.py` / `process_fundamentals_std.py` / `process_macro_std.py` → std 批次（schema v2 的 facts 段承载指标：subject/predicate/value/unit/period；entities 段放 MarketData/MarketIndex/MacroIndicator/FinancialMetric 实体；每条带 metadata.source+domain+date）；行情按月聚合批 + 明细留 parquet；「只出数据不出叙事」零 LLM | 已确认 |
| FR-003 | merge_std 扩展：可信度表加 tencent_quote=0.90 / eastmoney=0.85 / fred=0.95 / official_cn=0.95（公告 0.95 不变，东财财务与公告数字冲突时公告优先裁决留痕）；跨域连接：`context_of`（宏观/指数→00100.HK）、`period`（基本面期→行情窗口）、全域 `stock_code` 挂 00100.HK | 已确认 |
| FR-004 | **事件影响分析器** `impact_analysis.py`：事件研究法——每个带日期 Event 实体 × 日线 × 基准指数（HSCCI，缺则无基准模式），计算 T+0 当日收益、T+1~T+5 / T+1~T+20 累计收益与**超额收益**（个股-基准）；结果写回 final_graph 的事件实体 properties（impact_0d/5d/20d、abnormal_0d/5d/20d、benchmark、no_price_data 标注），幂等可重跑（merge 后重链） | 已确认 |
| FR-005 | 影响报告 `stocks/00100/impact_report.md`：按 event_type 聚合表（样本数/平均与中位超额 T+0/5/20）、Top 影响事件明细、方法论说明（窗口定义、基准选择、聚类事件提示、无价格期声明）；结论性 record_decision 留档 | 已确认 |
| FR-006 | 文档同步：PLAN.md 域 3/4/5 从待建改为已实现（含契约与来源）；PROCESSING_MANIFEST.md 补新环节行（全部确定性代码，理由列注明「结构化数值，语义在建模配置」） | 已确认 |
| FR-007 | 全链重建与验收：导入→三域 std→merge（消费 89+新批次）→to_explorer→impact_analysis→复验门禁（指代 0/繁简 0/双校验/时态覆盖不降）+ 新增断言（三域批次可消费、事件影响字段覆盖率、超额收益计算抽检） | 已确认 |

## 四、非功能需求

| ID | 需求 | 状态 |
|---|---|---|
| NFR-001 | 确定性：全链零 LLM 调用；同输入重跑逐字节一致 | 已确认 |
| NFR-002 | 可复算：影响分析的窗口/基准/公式写入报告方法论节与脚本常量 | 已确认 |
| NFR-003 | 端到端 < 10 分钟（数据量 160 日 × 8 期 × 宏观数千行，纯 pandas） | 已确认 |

## 五、约束

- C-001 只新增脚本（import/三处理器/impact_analysis），merge_std 仅做 FR-003 两处扩展，不动既有 89 批次
- C-002 数据包只读（源在 hk-quant-qlib 仓库，不修改）
- C-003 projects/ 不进 git；使命产物入 feature 分支
- C-004 影响分析只描述历史相关性，报告须声明「不构成因果推断与投资建议」

## 六、成功标准

1. 三域数据入图：final 含 MarketData/MarketIndex/MacroIndicator 实体与 context_of 边，财务事实与公告数字的冲突被检测并按可信度裁决
2. 事件影响可查：任一 Event 实体可读 impact_* 字段；报告按类型聚合可读；无价格期如实标注
3. 全链确定性重跑一致，门禁与既有断言全过
4. 决策回路接通：影响报告结论 record_decision 留档

## 七、假设

- HSCCI 指数日期与个股交易日对齐（同港交所日历）；不对齐日用可用最近基准日并留痕
- 事件日期（公告日/新闻日）即市场反应起始日 T+0（公告盘后发布等细节不建模，报告声明）
- data_manifest.json 的 data_sources 记录作为溯源来源串

## 八、非目标

- 不做因果推断/预测模型（只做历史事件研究统计）
- 不改 hk-quant-qlib 仓库任何内容
- 不做分时/盘口级分析（日频粒度）
