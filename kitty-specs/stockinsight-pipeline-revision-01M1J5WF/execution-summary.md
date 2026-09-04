# Execution Summary: stockinsight-pipeline-revision-01M1J5WF

**分支**: feature/stockinsight-pipeline-revision | **完成**: 2026-09-03
**基准方案**: 篇3《本体建模-03-提示词与双模型协同》（四件套骨架全部落地，未打折）

## 一、各 IC 落地情况

| IC | 交付 | 状态 |
|---|---|---|
| IC-01 提示词重建 | 两抽取脚本 `EXTRACT_PROMPT_V2` 四段式（【角色】→【词表与条款】→【输出骨架】→【纪律】），含自称替换条款（条款2）、简体统一条款（条款3）、12 类实体词表（条款1）、中文谓语（条款4）、事件受控词表（条款5）；占位符 `.replace()` 填充 | ✅ |
| IC-02 Pydantic 硬校验 | `scripts/_extract_core.py`：`AnnouncementExtraction`/`NewsExtraction`（Optional 带默认、类型错即拒），走 `generate_typed(prompt, schema=…)`。**实际路径（烟测确认）**：本环境未装 instructor，0.6.7 走库内 manual repair loop——generate + `model_validate` 字段级校验 + 错误摘要回灌重试，与 instructor 路径同为硬校验（已在 `_extract_core.py` 模块注释与篇3 回写中注明）。重试 3 次/间隔 5 秒，失败记 failures 不静默；坏 JSON 拦截单元烟测 5 类坏输入全拦 | ✅ |
| IC-03 审计器 | `scripts/audit_std.py`：确定性抽样（每域文件名排序前 10%，ceil）、财务事实全审（facts 分片 ≤40 条/请求，附 source_quote 定位）、四维审计（syntax/consistency/normalization/business_grounding + severity 三级）、error 回滚（`--only` 重抽→复审一次→仍 error 留人工清单）、warning 辩护/修订（DEFENSE_PROMPT，三步闭环第二步）、仲裁留痕。产物齐：`std/_audit/`（audit_report.md / rerun_log.md / arbitration.md / audit_result.json）。中途按需要补了断点续跑（audit_partial.json 每批落盘） | ✅ |
| IC-04 schema v2 与 PLAN.md | 批次 `metadata`（schema_version=2 / language=zh-CN / model / temperature）；`events` 段（text/event_type/date/participants/confidence）；merge 消费 events（Event 实体 + 参与关系，去重键 event_type+date+首参与者的规范形）；facts 增 `source_quote`；to_explorer 透传 language（实测 100% 实体带 zh-CN）；PLAN.md 写入 v2 schema、源头治理条款、四道门禁、审计流程、v1 归档说明 | ✅ |
| IC-05 全量重跑与验收 | v1 旧 89 批次归档 `_archive/std_v1/`（92 文件含 merge 元数据）；95 内容文件全量重跑 89 批（42 新闻 + 47 公告），零 failures；抽样审计 → merge 重建 → to_explorer → 验收断言全过；对账清单 v2 闭合（95 = 95 + 0） | ✅ |
| IC-06 处理方式清单 | `PROCESSING_MANIFEST.md`：37 环节逐条标注（环节/输入输出/LLM 或确定性/理由/条款名或代码位置），9 个语义判断环节 100% 指向提示词条款，正则/字符串处理全部为机械规范化并逐条列出 | ✅ |
| IC-07 篇3 回写 | 2 处小步回写（见第四节），骨架未削弱 | ✅ |

## 二、度量计对比表（源头治理生效判据）

| 度量计 | v1 基线 | v2 实测 | 阈值 | 判定 |
|---|---|---|---|---|
| 繁简折叠组数（merge ④ 兜底命中） | 88 组 | **1 组** | ≤10 | ✅ 达标 |
| 指代 ALIAS 命中（merge ② 兜底命中） | 74 条 | **0 条** | ≤5 | ✅ 达标 |

源头条款生效的直接证据：自称替换条款使指代兜底命中归零；简体统一条款使繁简兜底折叠从 88 组降至 1 组（余 1 组为人名生僻字转换波动，见下）。

## 三、验收断言（std/_acceptance.md，check_acceptance.py 确定性生成）

| # | 断言 | 实测 | 结果 |
|---|---|---|---|
| A1 | 裸指代残留 = 0 | 0（merge ⑥½ 门禁同步通过） | ✅ |
| A2a | 繁简分裂残留组 = 0（图级：跨节点未归一的同形异写） | 0 组 | ✅ |
| A3 | GraphValidator | is_valid=True（修复 0 轮） | ✅ |
| A4 | SHACL | conforms=True，违例 0 | ✅ |
| A5 | 实体 valid_from 覆盖 ≥95% | 97.2%（1059/1089） | ✅ |
| M1/M2 | 度量计 | 1 组 / 0 条 | ✅ |
| R1 | 对账闭合 | 95 = 95（89 批） + 0 失败 | ✅ |
| A2b | 字符级繁体残留（加严检查，不计入总判定） | 1 条，留人工确认名单（见边缘案例） | ⚠ 留档 |

final 规模：1089 实体 / 1711 关系（事件物化 490 条原始事件 → 279+ 个 Event 实体 + 千余条参与关系）。

### 边缘案例专项判定（OpenCC/转换边界）

- **华为昇腾**：OpenCC t2s 把「昇」映射为「升」（异体字归一），实为品牌官方用字，非繁简分裂 → 豁免（`check_acceptance.py: VARIANT_CHARS_OK`，豁免仅限字符、不掩盖同句其他繁体字）。
- **姓氏「貟」**：公告原文姓氏用字，转「员」会改人名 → 豁免。
- **「禕」（1 条留档）**：事件描述中人名「貟烨禕/貟烨祎」在不同文本块转换波动（同批次逐块独立、重抽不收敛）；已由 ④ 折叠归一为同一节点（M1 计入的 1 组），图中无分裂节点。属人名生僻字转换边界，留人工确认名单。
- **「标準」**：年度业绩公告首抽出现 1 处（应为"标准"），`--only` 重抽后清除。

## 四、抽样审计发现与回滚记录（std/_audit/）

- 抽样 12 批（公告 5 + 新闻 5；抽样期另有 2 批为回滚重抽复审），规则固定可复现。
- **财务事实全审 104 条（9 次分片请求），mismatch = 0**——抽取端数字质量过硬。
- 四维问题 145 条：error 92 / warning 38 / info 15；维度分布 syntax 33 / consistency 26 / normalization 39 / business_grounding 47。
- **error 回滚**：多批次触发 `--only` 重抽并复审一次；复审仍 error 的批次（含 announcements__2025123100026_c——审计者判定"大量编造数据"）按设计留人工清单，**不静默放行**；部分批次随后经 warning 修订路径重抽成功。
- **审计提示词两轮修复**（重要教训，已固化进 AUDIT_PROMPT/DEFENSE_PROMPT）：
  1. 首轮审计把「繁体照转简体」「自称替换」「id 规范化」判成 error（56 issues）——审计者不知道抽取规范。修复：AUDIT_PROMPT 增加【抽取规范（审计依据）】段，明确这些是规范行为；issue 数 56→6。
  2. 生成者曾顺从错误审计选择"改回繁体"——修复：DEFENSE_PROMPT 声明"符合规范的行为必须 defend 而非 revise"，并要求 description 收敛（不要在字段内自我辩论）。
- 审计模型：deepseek-chat（探测可用，与生成模型 deepseek-v4-flash-vision-exp 不同型号 = **真异构**）。

## 五、篇3 回写说明（IC-07，2 处小步，骨架未动）

1. 第一节「0.6.7 实测要点」补两条：自定义 BaseModel 可直接传 `generate_typed(schema=…)`；环境无 instructor 时走库内 manual repair loop（generate + model_validate + 错误回灌），硬校验力度一致。
2. 模板 E 后新增工程注记：审计对象为抽取产物时，模板 E 的【标准化描述】/【术语表】输入位应换成生成侧提示词条款（抽取规范原文），否则审计者按一般直觉判级会把源头治理条款当缺陷——附 StockInsight 实测案例。

## 六、执行中断时间线（会话环境清理所致，非任务故障）

| 事件 | 位置 | 恢复方式 |
|---|---|---|
| 网络断连（APIConnectionError） | 烟测公告 1/2 块级抽取 | 3 次重试机制显式记 failures，网络恢复后 `--file` 重跑成功 |
| 后台跑批进程被环境清理 ×2 | 公告域全量（16/47、29/47） | 改分片续跑（--limit 8/片，缩短单进程寿命），5 片至 47 批齐 |
| 后台审计进程被环境清理 ×2 | 抽样审计中途 | audit_std.py 补断点续跑（audit_partial.json 每批落盘，mtime 失效判定），续跑复用已审批次 |
| 协调者兜底进程并发竞争 | std/ 写入 | 协调者 kill 兜底进程；31 批完整性抽检无损坏 |
| 审计回滚中断留下的 2 个缺失批次 | 2025123100004_c / 2026010800026_c | `--only` 补抽后重新 merge（89 批全量消费） |

## 七、产物清单

- 脚本：`scripts/_extract_core.py`（新）、`process_announcements_std.py`、`process_news_std.py`（改造）、`audit_std.py`（新）、`check_acceptance.py`（新）、`gen_reconciliation.py`（新）、`merge_std.py`（适配）、`to_explorer.py`（透传）
- 文档：`PLAN.md`（v2）、`PROCESSING_MANIFEST.md`（新）、篇3（2 处回写）
- 数据：`stocks/00100/std/` 89 个 v2 批次 + `_audit/` 四件产物 + `_acceptance.md` + `_reconciliation.md`；`final_graph.json/.explorer.json/.ttl/*.parquet`；归档 `_archive/std_v1/`、`_archive/smoke_v2/`
- 决策/溯源：ContextGraph 决策 `c0bf0327-4816-4e67-ab8e-55b2020b532c`，版本快照 `std-20260903-1647` 后随最终 merge 更新，溯源 1700 条
