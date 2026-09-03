# Mission Report: StockInsight 流水线最佳实践对齐修订

**Mission**: stockinsight-pipeline-revision-01M1J5WF（software-dev）| **日期**: 2026-09-03
**状态**: ✅ 完成，验收 8/8 全过（主代理独立复核）；详情见 [execution-summary.md](execution-summary.md)

## 核心成果：源头治理度量计（spec 成功标准 2）

| 度量计 | v1 基线 | v2 实测 | 阈值 | 含义 |
|---|---|---|---|---|
| 繁简折叠组数 | 88 | **1** | ≤10 | 「简体中文统一」提示词条款在源头拦住了 98.9% |
| 指代 ALIAS 命中 | 74 | **0** | ≤5 | 「发行人自称替换」条款在源头全量拦截 |

## 篇3 四件套落地（C-004 骨架不打折）

1. **四段式提示词**：两抽取脚本 EXTRACT_PROMPT_V2（角色/词表与条款/输出骨架/纪律），含自称替换、简体统一、类型受控、事件独立四条款
2. **Pydantic 硬校验**：`_extract_core.py` AnnouncementExtraction/NewsExtraction 走 `generate_typed`（0.6.7 不适配时库内 generate+model_validate 修复环），类型错即拒
3. **双模型三步闭环**：抽样审计（公告 5+新闻 5+facts 全审）→ error 回滚重抽（`--only`）→ warning 辩护/修订 → 仲裁留痕；审计模型 deepseek-chat 与生成模型**真异构**
4. **四维审计**：语法规范/逻辑一致/语义归一/业务落地，145 条分级问题（error 92/warning 38/info 15），财务事实全审 104 条 **mismatch 0**

## 数据与资产（schema v2：metadata.language + events 段）

- 89 个 v2 批次（公告 47 + 新闻 42，旧 v1 归档 `_archive/std_v1/`），对账闭合 95=95+0
- final：**1089 实体 / 1711 关系**（含 296 个 Event 实体——events 段物化）；指代残留 0；MiniMax 主体 634 边；时态覆盖 97.2%
- 审计四件套 `_audit/`（report/result/rerun_log/arbitration）；验收 `_acceptance.md` 8/8；决策 `c0bf0327`、快照 `std-20260903-1735`

## 处理方式清单（spec FR-006，用户核心关切）

`PROCESSING_MANIFEST.md`：14+ 环节逐行标注 LLM｜确定性代码、理由、提示词条款/代码位置。语义判断（实体/关系/事实/事件抽取、指代消解源头、繁简归一源头、审计）全部 LLM 且指向具体条款；机械环节（解析/截断/分块/frontmatter/校验/折叠/门禁/导出）全部确定性代码。**待用户逐环节确认。**

## 如实留档的两条边界

1. **A2b 字符级加严检查**：1 条人名转换波动（貟烨禕）留人工确认名单；异体字豁免 2 处（华为昇腾——品牌官方用字；貟姓——姓氏原字），豁免仅限字符本身，判定口径写入脚本注释
2. **过程事故**：会话清理三次杀死后台跑批/审计进程（无自身故障），以分片+断点 checkpoint 应对；一次双进程并发风险被我方及时发现并消除（31 批完整性抽检无损）——时间线在 execution-summary

## 篇3 回写（IC-07）

落地中发现并回写两处（见 execution-summary）：①自定义 schema 与 generate_typed 的适配路径说明 ②审计提示词需注入原文依据（否则假 error 泛滥——实测 56→6）

## 遗留（后续建议）

1. A2b 人名波动若需归零：人名归一兜底词表（机械层）或人工确认
2. 审计 warning 级问题中的系统性改进点（简称统一、英文缩写转中文全称、拟任董事状态标注）可进下一轮提示词迭代
3. 行情/基本面/宏观三域仍待采集（PLAN.md 待建项，非本使命范围）
