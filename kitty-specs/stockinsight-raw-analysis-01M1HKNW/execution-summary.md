# StockInsight 00100 全量原始数据分析 — 执行摘要

**Mission**: stockinsight-raw-analysis-01M1HKNW | 完成日期: 2026-09-03
**执行环境**: .venv (Python 3.11) + semantica 0.6.7 + DeepSeek (`deepseek-v4-flash-vision-exp` @ api.deepseek.com)
**分支**: feature/stockinsight-raw-analysis（projects/ 下产物不进 git，符合仓库纪律）

## 一、交付物（三个新脚本，零侵入既有文件）

| 脚本 | 职责 | 行数 |
|---|---|---|
| `projects/StockInsight/scripts/process_announcements_std.py` | 公告（PDF/HTM/HTML）→ std 批次；parse → 2 万字截断 → 1200 字分块 → LLM 抽取（12 类词表绑定、3 次重试） | ~340 |
| `projects/StockInsight/scripts/process_news_std.py` | 新闻/研究 MD → std 批次；frontmatter 解析（日期/标题/related_announcements 进 metadata），news 按日期聚批，narrative 按整理时间聚批（`source.type=research`） | ~350 |
| `projects/StockInsight/scripts/merge_std.py` | std 全量消费 → 九阶段合并重建 final（可信度注册 → 归一 → 冲突/消解 → 合并 → 建图/校验 → 重建 → 溯源 → 导出/SHACL → 决策 → 快照） | ~480 |

三脚本均 `--stock <code>` 参数化（默认 00100），相对项目根定位路径，`--limit`/`--file` 支持烟测与断点续跑；已存在批次文件自动跳过（幂等）。

## 二、执行数字

### A. 公告域（process_announcements_std.py）

| 项 | 值 |
|---|---|
| 输入 | 47 份（44 PDF + 2 HTM + 1 占位 HTML）|
| 成功 / 失败 | **47 / 0** |
| std 批次 | 47 个 `std/announcements__<文档号>.std.json` |
| 抽取累计 | 536 实体 / 488 关系 / 264 事实（跨块合并后，含续跑）|
| 耗时 | ~5,500s（首次全跑 12+12 块烟测与续跑两段合计）|

### B. 新闻/研究域（process_news_std.py）

| 项 | 值 |
|---|---|
| 输入 | 48 份（41 news + 7 narrative research）|
| 成功 / 失败 | **48 / 0** |
| std 批次 | 42 个（41 按日期聚批 + `news__undated_research` 兜底批；`news__20260601` 一日双事件、`news__20260901_research` 四份研究同批）|
| 抽取累计 | 572 实体 / 513 关系 / 300 事实 |
| 类型分布 | Company 160 / Product 139 / Event 125 / Concept 49 / Executive 39 / 其余 60 |
| 耗时 | 1839s（~31 分钟）|

### C. 合并重建（merge_std.py）

| 阶段 | 结果 |
|---|---|
| ① 可信度 | announcements=0.95 > news=0.70 > research=0.60 |
| ② 消费 | **89 个 std 批次**，实体记录 1808 / 关系记录 1517；别名归并命中 61（MiniMax Group Inc.、00100.HK、闫俊杰、M3、H3、海螺AI 等繁简/简称变体），剔除占位噪声实体 |
| ③ 冲突 | 检出 **77 条**（value=53、type=24），`credibility_weighted` 全部消解写回 77 条（跨域收入/市值/类型矛盾按公告优先裁决）|
| ④ 合并 | `merge_entities(keep_most_complete, threshold=0.9)` 283 次操作 → 976 实体（含孤立实体拼完整集）；关系端点同步重映射后悬挂仅 2 条被预过滤 |
| ⑤⑥ 建图 | `GraphBuilder(merge_entities=True).build` → **552 节点 / 1515 边**；`GraphValidator` 结构校验 **is_valid=True**（零 DANGLING_EDGE，无需修复轮）|
| ⑦ 重建 | 旧 final_graph.json（509 实体累计图）已归档 `_archive/final_v0/`；新 **`stocks/00100/final_graph.json`**（552 实体 / 1515 关系，text/label 同构格式）|
| ⑧ 溯源 | `provenance.db`（storage_path 持久化）**1808 条**，source=原始文件路径、按批次 source_location 留痕 |
| ⑨ 导出 | `final_graph.ttl`（`RDFExporter(include_provenance=True)`，473KB）+ `final_graph_entities.parquet` / `final_graph_relationships.parquet`（snappy）；**SHACL conforms=True，违例 0**（`std/_shacl_report.json` 留档）|
| ⑩ 决策 | `ContextGraph.record_decision` → **decision_id `103b7fc5-724b-4c44-8e1e-d18c44a35fb6`**（category=std_rebuild, outcome=final_graph_rebuilt, decision_maker=claude@example.com）|
| ⑪ 快照 | `TemporalVersionManager` → **`std-v1`**（versions.db，author=claude@example.com，"std 契约首版全量重建"）|

## 三、对账结论（详见 `stocks/00100/std/_reconciliation.md`）

- **内容文件 95 = 成功 95 + 显式失败 0**（47 公告 + 41 新闻 MD + 7 研究 MD），逐文件清单见对账文档第三/四节
- spec 的「35 新闻 + 14 研究 = 49」与磁盘实际「41 新闻 + 7 研究 = 48」有口径出入，以磁盘实际文件对账，总数闭合、无静默遗漏；`news_schema.md` 为 schema 元文档不抽取，2 份索引 JSON 由脚本消费，均不计入内容文件
- 行情/基本面/宏观三域无 raw 数据（PLAN.md 待建项），如实记录不计遗漏

## 四、烟测与质量验证

1. **烟测先行**：tc.html（占位页空批次路径）→ H1 中报（12 块实体/关系/事实全链路）→ 新闻 frontmatter 批 → narrative research 批 → `_smoke` 临时目录 merge 端到端（11 步全通、61 边零悬挂、SHACL 通过），通过后才放行全量
2. **std schema 逐字段核对**：七字段（batch_id/stock/domain/source/entities/relationships/facts）+ 每条 `metadata.source/domain/date` 与 PLAN.md L122-136 一致
3. **format 同构验证**：`to_explorer.py 00100` 在新 final 上跑通（552 实体/1515 关系，补建悬空端点 0），spec 假设 2 成立

## 五、执行中发现并修复的问题（脚本内已固化）

1. `semantica.parse` 对 HTML 返回 `HTMLData` 对象（`.text`），与 PDF 的 dict（`full_text`）不一致 → `parse_document` 双路径兼容
2. **关系 dict 字面量 `"source"` 键重复**（端点 id 被来源名覆盖，Python dict 后者胜）→ 删除重复键，来源名移入 `metadata.source_type`
3. `news` 脚本 `ensure_entity` 漏更新去重集合 → 补 `ent_ids.add(cid)`
4. `ConflictType` 枚举比较（`'VALUE'` ≠ `'value_conflict'`）导致消解不落盘 → 统一经 `conflict_kind()` 归一
5. `merge_entities` 内部 fuzzy 归并会改实体 id（毛利/毛利率、M3/H3 误并）→ `threshold=0.9` 收紧为仅同 id 合并 + 用 `source_entities` 构建 id 映射重映射全部关系端点

## 六、遗留与建议（超本使命范围）

- `detect_conflicts` 不支持期间（period）过滤：跨年度财务数值（如 2026H1 vs 2025H1 同指标）会被判为 value 冲突后消解为单值；完整期间序列在 `facts` 数组保留，后续可做 period-aware 冲突检测
- `merge_entities` 的 fuzzy 策略偶有过并（本次已用 threshold 收紧），语义层可引入本体 disjoint 约束二次把关
- 财报类大 PDF（17 块截断 2 万字）为抽样抽取，尾部章节未覆盖；如需全覆盖可改为按章节分段抽取
