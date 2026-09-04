# Implementation Plan: StockInsight 流水线最佳实践对齐修订

**Branch**: `feature/stockinsight-pipeline-revision` | **Date**: 2026-09-03 | **Spec**: [spec.md](spec.md)
**基准方案**: [本体建模-03-提示词与双模型协同](../../../docs/best-practices/本体建模-03-提示词与双模型协同.md)（逐条落地，骨架不打折）
**前置事实**: merge 端兜底现状（OpenCC t2s / ALIAS 表 / 裸指代门禁 / id 折叠）已在上使命生效，本次保留为第二道防线并用作「源头治理生效」的度量计

## Summary

三个处理脚本按篇3 重建抽取层：四段式提示词（含自称替换与简体统一条款）+ 自定义 Pydantic schema 走 `generate_typed` 硬校验 + 新增 events 段与 `metadata.language`；新增 `audit_std.py` 做抽样双模型审计（四维、severity 分级、error 回滚重抽）；PLAN.md 升级为 schema v2 + 全流程约定；全量重跑 96 文件重建资产；交付逐环节「处理方式清单」。全程 LLM 管语义、代码管机械。

## Technical Context

**Language/Version**: Python 3.11（.venv）；semantica 0.6.7（只调用不改）
**Primary Dependencies**: semantica 0.6.7（`create_provider().generate_typed`、conflicts/dedup/kg/export 等）；`pydantic`（semantica 自带依赖，自定义抽取 schema 用）；`opencc-python-reimplemented 0.1.7`（已装）；`python-dotenv`
**LLM**: 生成模型 `deepseek-v4-flash-vision-exp` @ api.deepseek.com（key：.env `DEEPSEEK_API_KEY`）；审计模型优先 env `DEEPSEEK_AUDIT_MODEL`（如 deepseek-reasoner/deepseek-chat 不同型号），缺省同模型+独立审计 Prompt 并在产物标注「非异构」局限
**Storage**: std 批次 `stocks/00100/std/`（v2 schema，旧 89 批次归档 `_archive/std_v1/`）；审计产物 `std/_audit/`；清单 `projects/StockInsight/PROCESSING_MANIFEST.md`
**Testing**: ①烟测：每域 2–3 份文件跑通「抽取→硬校验→merge→门禁」全链；②源头治理度量：重跑后 merge 端兜底命中数（繁简折叠 ≤10 组、指代 ALIAS ≤5 条）；③门禁断言：指代 0 残留、繁简 0 组、GraphValidator + SHACL 通过、valid_from ≥95%；④对账：96 = 成功 + 显式失败
**Target Platform**: macOS 本地（.venv），脚本 `--stock` 参数化保持跨股票复用
**Project Type**: 数据处理脚本修订（projects/ 下，不进 git）
**Performance Goals**: 端到端（重跑+审计）< 2 小时；单文件抽取 ≤ 3 次重试
**Constraints**: 篇3 四件套（四段式/硬校验/三步闭环/四维审计）必须全部落地；确定性环节同输入重跑逐字节一致；LLM 参数（model/temperature）写入批次 metadata
**Scale/Scope**: 96 内容文件；三脚本改造 + 新增 audit_std.py + merge_std.py 适配 events 段 + to_explorer.py 透传 events + PLAN.md 修订 + 处理方式清单

## Charter Check

- Testing ✓（上节 Testing 四项，含可断言阈值）；Quality Gates ✓（PR 评审 + 处理方式清单用户确认）；Branch ✓（feature 分支）；DIR-001 ✓（spec 7 FR → 本 plan 6 IC → 任务逐层对应）。

## Project Structure

```
projects/StockInsight/
├── PLAN.md                        # 修订：schema v2、多语言/指代条款、门禁、审计流程
├── PROCESSING_MANIFEST.md         # 新增：处理方式清单（逐环节 LLM/确定性标注）
├── to_explorer.py                 # 透传 events 与 language
├── scripts/
│   ├── process_announcements_std.py   # 改造：四段式提示词+硬校验+events 段
│   ├── process_news_std.py            # 同上
│   ├── audit_std.py                   # 新增：抽样双模型审计器
│   └── merge_std.py                   # 适配：消费 events 段；度量计输出
└── stocks/00100/
    ├── std/                        # v2 批次（v1 归档 _archive/std_v1/）
    │   └── _audit/                 # 审计报告/回滚记录/仲裁留痕
    └── final_graph.*               # 重建资产
```

**Structure Decision**: 不改既有 merge 兜底结构（已验证），抽取层推倒重建为篇3 形态；审计器独立成脚本（职责单一，可单独重跑）。

## Complexity Tracking

无 Charter 违反项。

## Implementation Concern Map

### IC-01 提示词重建（篇3 模板 A 结构）

- **Purpose**: 两抽取脚本的 EXTRACT_PROMPT 改为四段式：【角色】→【词表与条款】（12 类词表 + **自称替换条款**：本公司/本集团/发行人/该公司/該公司等一律替换为发行主体全名；**简体统一条款**：全部实体名/谓语/事件描述输出简体中文）→【输出骨架】（严格 JSON，含 events 段）→【纪律】（只输出 JSON/不确定省略/数值带单位）。占位符 `.replace()`。
- **Relevant requirements**: FR-001, FR-003（源头）, FR-004（源头）
- **Affected surfaces**: process_announcements_std.py、process_news_std.py
- **Sequencing**: none（起点）
- **Risks**: 条款过长稀释注意力——条款放词表后、纪律前，烟测验证命中率

### IC-02 Pydantic 硬校验

- **Purpose**: 定义 `AnnouncementExtraction`/`NewsExtraction` Pydantic 模型（entities[{name,type,confidence?}]/relations[{subject,predicate,object}]/attributes 或 events[{text,event_type,date,participants}]，字段 Optional 带默认以容错可缺省项但**类型错即拒**）；`llm.generate_typed(prompt, schema=…)` 替换手工 `json.loads`；失败重试 3 次 → failures 记录。批次 metadata 记 model/temperature。
- **Relevant requirements**: FR-002, NFR-001
- **Affected surfaces**: 两抽取脚本公共校验模块（`scripts/_extract_core.py` 共享，避免两份拷贝）
- **Sequencing**: IC-01（骨架与 schema 字段对齐）
- **Risks**: `generate_typed` 对自定义 schema 的行为需烟测确认（0.6.7 实测过 EntitiesResponse，自定义 BaseModel 预期同路径）；若不支持则降级 `generate` + `Model.model_validate` 手动硬校验——同样满足「字段级校验」骨架

### IC-03 抽样双模型审计器

- **Purpose**: `audit_std.py`：①确定性抽样——每域按文件名排序取 10%（公告 5 份、新闻+研究 5 份，固定规则保证可复现）；②财务事实全审——全部批次的 attributes 段逐条对照原文（source_quote 定位）；③审计 Prompt 按篇3 四维（语法规范/逻辑一致/语义归一/业务落地）输出 {verdict, issues[{dimension,severity,location,description,suggestion}]}；④severity=error 的批次回滚（作废重抽→复审）；⑤三步闭环留痕：审计报告→生成者对 warning 级的响应（辩护或修订）→仲裁记录。产物全部落 `std/_audit/`。
- **Relevant requirements**: FR-003, NFR-002
- **Affected surfaces**: 新增 audit_std.py；两抽取脚本暴露 `--only <批次>` 重抽入口
- **Sequencing**: IC-01/02（审计对象是新抽取产物）
- **Risks**: 审计模型与生成模型同厂——缺省不同型号，不可得则同模型独立 Prompt + 产物标注局限（spec 边界条款）

### IC-04 schema v2 与 PLAN.md 修订

- **Purpose**: std 批次 `metadata` 增 `language: "zh-CN"`；新增 `events` 段（text/event_type/date/participants/confidence，日期来自文档日期或正文显式日期）；merge_std 消费 events（Event 类型实体 + participants 关系）；to_explorer 透传。PLAN.md 写入：多语言条款、指代条款、四道门禁、审计流程、schema v2 定义与 v1 归档说明。
- **Relevant requirements**: FR-004, FR-005（schema 部分）
- **Affected surfaces**: 两抽取脚本、merge_std.py、to_explorer.py、PLAN.md
- **Sequencing**: IC-01/02（schema 与抽取骨架同改）
- **Risks**: merge 消费 events 时事件实体与既有 Event 类实体（新闻标题类）可能重复——事件去重键（event_type+date+首 participant）

### IC-05 全量重跑与验收

- **Purpose**: 旧批次归档 → 96 文件全量重跑（新脚本）→ 抽样审计 → merge 重建 → 资产再生成 → 四项 Testing 断言全过 → 对账清单 v2。输出**度量计**：merge 端兜底命中数（繁简折叠组数、指代 ALIAS 命中数）对比 v1 基线（88 组 / 74 命中）。
- **Relevant requirements**: FR-005, NFR-003, NFR-004
- **Affected surfaces**: 全部产物
- **Sequencing**: IC-01~04 全部完成 + 烟测通过后
- **Risks**: LLM 输出质量波动导致某文件反复失败——failures 记录后人工介入清单，不阻塞整批

### IC-06 处理方式清单

- **Purpose**: `PROCESSING_MANIFEST.md`：从 raw 到 final 逐环节表——环节名 / 输入→输出 / 处理方式（LLM｜确定性代码） / 理由 / 提示词条款或代码位置。覆盖：摄取解析、分块、抽取（实体/关系/事实/事件）、指代消解（源头 LLM + 兜底代码）、繁简归一（源头 + 兜底）、冲突检测消解、id 折叠去重、建图校验、门禁、导出、审计。语义判断环节 100% 指向 LLM 条款。
- **Relevant requirements**: FR-006, C-004
- **Affected surfaces**: 新文件
- **Sequencing**: IC-05 后（清单反映真实运行态）
- **Risks**: 无（文档性交付，但需与代码逐条对照防失真）

### IC-07 篇3 回写（条件触发）

- **Purpose**: 落地中若发现篇3 缺陷（如 schema 适配、审计闭环粒度），修订篇3 对应章节并在此记录；落地形态适配不削弱骨架。
- **Relevant requirements**: FR-007
- **Sequencing**: 视 IC-01~05 发现而定

## 执行顺序

IC-01+IC-02+IC-04（抽取层重建，一批改完）→ **烟测**（每域 2–3 份，验证四件套与门禁）→ IC-03（审计器 + 烟测审计）→ IC-05（全量重跑 + 验收断言）→ IC-06（清单）→ IC-07（视情）。实现委托后台代理执行、主代理验收（沿用上使命模式）；关键验收点：烟测通过才放全量、度量计达标（≤10 组 / ≤5 条）才算源头治理生效。
