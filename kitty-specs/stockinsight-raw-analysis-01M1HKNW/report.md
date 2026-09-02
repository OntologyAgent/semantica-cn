# Mission Report: StockInsight 00100 全量原始数据分析

**Mission**: stockinsight-raw-analysis-01M1HKNW（software-dev）| **日期**: 2026-09-03
**状态**: ✅ 完成（主验收通过）| **执行详情**: [execution-summary.md](execution-summary.md)（实现代理完整记录）

## 成果对账（已由主代理独立复核）

| 指标 | 结果 |
|---|---|
| 内容文件覆盖 | **95/95，0 静默失败**（47 公告 + 48 新闻/研究；spec 预估 35+14=49 与磁盘实际 41+7=48 的口径出入已按磁盘对账并记录） |
| std 批次 | 89 个（公告 47 + 新闻 42），累计实体 1108 / 关系 1001 / 事实 585——**std 契约首次落地** |
| final 图谱重建 | 552 实体 / 1515 关系（旧 509 实体累计图已归档 `_archive/final_v0/`） |
| 冲突处理 | 检出 77（value 53 + type 24），credibility_weighted 全消解（公告>新闻>研究），顺序符合最佳实践 3.4 铁律 |
| 图质量 | GraphValidator is_valid=True 零悬挂边；SHACL conforms=True 违例 0 |
| 资产 | provenance.db（1808 条溯源）+ final_graph.ttl（含溯源）+ 双 parquet + versions.db 快照 std-v1 + 决策 `103b7fc5` |
| 复用性 | 三脚本 `--stock` 参数化；to_explorer.py 在新图上验证通过 |

## 交付物

- `projects/StockInsight/scripts/process_announcements_std.py` / `process_news_std.py` / `merge_std.py`（新增，零改动既有脚本）
- `projects/StockInsight/stocks/00100/std/`（89 批次 + `_reconciliation.md` 对账清单 + failures 机制）
- `projects/StockInsight/stocks/00100/final_graph.json` 及全套资产
- 执行中修复的 5 个问题（HTML 对象差异、关系 dict source 键覆盖端点、去重集合漏更新、枚举比较失效、fuzzy 误并致悬挂）已固化进脚本，详见 execution-summary

## 遗留（后续建议，不阻塞验收）

1. 跨年度财务数值的 period-aware 冲突检测（当前 value 法按属性名，不区分报告期）
2. 大 PDF 抽样抽取的全覆盖改造（>20000 字截断策略会丢尾部内容）
3. 行情/基本面/宏观三域数据采集（PLAN.md 待建项，本次无 raw 输入）

## 方法论验证闭环

本次执行即最佳实践文档集（同夜完成）的首次实战：九阶段顺序、std 契约、四要素变量流、冲突先于合并、溯源四元组、决策即一等对象——全部按文档落地，未发现文档与实战冲突的新偏差。

## 后续修复（2026-09-03 用户反馈驱动）

用户指出两个图谱质量问题，均已修复并重建（final 974 实体 / 1168 关系，决策 34ac8c8f）：

1. **裸指代实体**：「本公司/本集团」是港股公告自称（共挂 91 条边），已在 merge_std 的 ALIAS 表消解到 MiniMax Group Inc.——修复后主体挂边 499，成为图中枢。
2. **时态缺失**：std 层 96% 记录本来就有 metadata.date，但 to_explorer.py 转换时丢弃、Explorer 时态滑块按 properties.valid_from 过滤所以播放无效果。修复：merge_std 注入 valid_from（实体用跨批次**首次出现日**、关系用批次日期）+ to_explorer 透传。现覆盖实体 96% / 关系 96%，时间跨度 2025-09-16 → 2026-09-01。

**顺带修掉两个更深的合并 bug**（实战验证了最佳实践「先显式归一、去重后建图关二次合并」的必要性，已回写篇2/篇4）：
- merge_entities 相似度分组只把同 id 的 99 条主实体记录并组 2 条，其余 97 条被 merged_ids 静默丢弃 → 改为按规范 id 折叠（字段并集）
- GraphBuilder(merge_entities=True) 把 MiniMax Group Inc. 与上海稀宇科技有限公司（开曼主体 vs 境内 WFOE，不同实体）模糊并组顶掉规范名 → 干净输入传 False
