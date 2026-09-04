# Implementation Plan: 本体建模最佳实践修订

**Branch**: `feature/ontology-modeling-bp-revision` | **Date**: 2026-09-03 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `kitty-specs/ontology-modeling-bp-revision-01M1HFWN/spec.md`
**Research**: `research/01-book-digest.md`（书稿方法论）、`02-stockinsight-digest.md`（贯穿案例）、`03-cookbook-examples-digest.md`（27 实践模式）、`04-docs-digest.md`（能力事实矩阵）、`05-current-doc-audit.md`（现有文档审计）

## Summary

把 744 行单文件《本体建模最佳实践.md》修订为 5 篇有序、相对独立、少互引的文档集。三条主线：

1. **纠偏**：29 句话表按重扫书稿图 6-1 重排（现表枚举 4+7+3+6+2+4+7，与书稿 2+7+3+1+5+4+7 不符，是旧版扫描带偏的实锤）；约八成代码示例实测跑不通（审计 T1/T6/T7/T8/T9/T10/T12/T16/T18/T19/T21），全部换成 StockInsight 已验证调用 + cookbook 已验证模式；"双模型协同"一词两义统一为书稿 6.2.2 原义。
2. **补强**：每个业务阶段补齐「输入约定/输出约定/前置依赖/后续流向」四要素契约，并给出贯穿九阶段的变量流；融入 cookbook 17 个直接相关实践模式（本体即代码、SHACL 双工件、CQ 验收前置、源可信度冲突消解、审计级溯源四元组、种子先行等）；能力边界篇显式区分"书稿目标标准 vs Semantica 实际实现"（SWRL/OWL-S/ODRL/四剑客无实现）。
3. **解耦**：荔枝植保示例整体替换为 StockInsight 投资案例，同时每阶段给出「换领域怎么适配」指引，方法论与领域解耦。

## Technical Context

**Language/Version**: 文档为中文 Markdown（Mintlify 兼容，GitHub 可渲染）；代码示例为 Python 3.11，目标库 semantica **0.6.7**（.venv 实测版本；注意官方 docs 标注 0.5.0 滞后于实装，凡文档与实测冲突以实测为准并在文中注明版本）
**Primary Dependencies**: semantica 0.6.7（已装 .venv，无新增依赖）；LLM 抽取走 OpenAI 兼容端点（StockInsight/.env 现有 DEEPSEEK_API_KEY，可选 ZHIPU/MOONSHOT）
**Storage**: 交付物为 `docs/best-practices/` 下 5 个 .md 文件；案例数据引用 `projects/StockInsight/`（只读参照，不修改）
**Testing**: ①篇2 附录「最小可跑链路」脚本在 .venv 实际执行通过（无 LLM key 的段落用 pattern 法或 mock 标注）；②引用链接校验：脚本扫描全部相对路径链接指向仓库内真实文件；③五路 research 摘要作为逐条核验对照表
**Target Platform**: Mintlify 文档站 + GitHub Markdown 双渲染
**Project Type**: 文档集（single docs package，无代码结构）
**Performance Goals**: N/A（文档交付；唯一执行约束：最小链路脚本 5 分钟内跑完）
**Constraints**: 总篇数 = 5（NFR-002 上限）；任何一篇对其他篇显式引用 ≤3 处；只新增/修改 `docs/best-practices/`；书稿 `book/` 只读
**Scale/Scope**: 5 篇合计约 1800–2400 行（原 744 行扩充：四要素契约、变量流、适配指引、引用链接为净增量；删减：模板正文集中后正文去重）

## Charter Check

- **Testing Standards** ✓：本使命测试方式为「最小可跑链路执行 + 引用链接存在性校验」，已在 Technical Context Testing 声明。
- **Quality Gates** ✓：合并前至少一名评审者批准——PR 评审覆盖（spec 成功标准 #2「纠得正、查得到」由评审抽查书稿引用一致性）。
- **Performance Benchmarks** ✓：不涉 CLI 性能；最小链路 5 分钟内约束已声明。
- **Branch Strategy** ✓：feature 分支 + PR 合回 main；macOS 本地开发，无部署约束冲突。
- **DIR-001** ✓：spec（12 FR）→ plan（本文件 IC-01~08 全覆盖）→ tasks → 实现逐层对应，映射见各 IC 的 Relevant requirements。

## Project Structure

### Documentation (this mission)

```
kitty-specs/ontology-modeling-bp-revision-01M1HFWN/
├── plan.md              # 本文件
├── research/            # 五路源材料摘要（核验对照表，01~05）
│   └── research-notes.md  # （汇总索引，可选）
└── tasks/               # /spec-kitty.tasks 产出（后续）

docs/best-practices/     # 交付物（5 篇，数字前缀即阅读顺序）
├── 本体建模最佳实践.md            # 篇1《总纲与知识契约》（保留原文件名作入口：文档集导览+方法论主线）
├── 本体建模-02-流水线落地.md      # 篇2《九阶段落地：以 StockInsight 为例》
├── 本体建模-03-提示词与双模型协同.md  # 篇3
├── 本体建模-04-能力边界与替代方案.md  # 篇4
└── 本体建模-05-术语速查与易混辨析.md  # 篇5
```

### Source Code (repository root)

不新增源码。代码只出现在文档代码块中，全部来源于已验证的三类：StockInsight scripts/ 实测调用（research/02 A 表）、cookbook/examples 模式（research/03 C 清单）、审计确认正确的部分（research/05 T 清单中 ✓ 项）。

**Structure Decision**: 单文档包结构；原文件名保留为篇1兼入口（老链接不断）；新增 4 篇用「本体建模-0N-主题」命名保证排序与可发现性。

## Complexity Tracking

无 Charter 违反项，不需要复杂度豁免。

## Implementation Concern Map

### IC-01 — 总纲重构与 29 句话重排

- **Purpose**: 篇1 的方法论主干以重扫书稿为准绳：29 句话表按图 6-1 逐句重排（2+7+3+1+5+4+7），五环联动与九阶段的映射关系讲清；改写引言的"原创声明"为诚实来源标注（四铁律/29 句话/评审路径均源自书稿并链接）。
- **Relevant requirements**: FR-001, FR-008
- **Affected surfaces**: 本体建模最佳实践.md（一、二、四、八 → 篇1 重组）；research/01 §A/§B、research/05 §F1 为对照依据
- **Sequencing/depends-on**: none（可与 IC-02 并行启动）
- **Risks**: 29 句逐句归类需人工比对书稿原文，不可机械照抄审计结论；书稿 7 处转写痕迹（research/01 §F）在引用时不扩散

### IC-02 — API 核验与代码重写

- **Purpose**: 文档中全部代码示例按「StockInsight 实测 > cookbook 验证 > 官方 reference」优先级重写；逐条消解审计 T1~T25（11 处 ✗ 全部修正，△ 调整表述，? 逐一核实或删除）；关键修正：extract_triplets_llm 导入路径、CoreferenceResolver 正名、merge_entities(entities, method=) 签名、from_data 只吃 entities/relationships（注入版走 to_owl + uri 键）、detect_conflicts(method=)、dedup_triplets 是检测非清洗、GraphBuilder.build(dict) 无 to_kg_dict、validate_graph(kg, ontology=) 需 RDF 字符串、CLI export 无 --rdf。
- **Relevant requirements**: FR-002, FR-005
- **Affected surfaces**: 篇2 全部代码块；篇3 模板调用方式；篇4 边界表述
- **Sequencing/depends-on**: none（T 清单已备好）
- **Risks**: docs 0.5.0 与实装 0.6.7 差异——每个 API 用法标注来源与版本；书稿要求但 Semantica 无实现的（四剑客）移入篇4 目标标准，不在篇2 假装有 API

### IC-03 — 阶段契约四要素与变量流

- **Purpose**: 九阶段每阶段写清「输入约定（含上一阶段产物变量名与数据形态）/ 输出约定（产物 schema、命名、存放、达标判据）/ 前置依赖 / 后续流向」；篇2 开篇给变量流总图（chunks → entities/relations/events → normalized → resolved+deduped → ontology dict → 推理信号 → validated graph → 决策记录），终结"九阶段靠校验点衔接、无数据流"的现状；补审计 D 节列出的各阶段缺口（3.3 objects 来源、3.4 facts 来源、3.6 审计回路、3.8 失败修复回路等）。
- **Relevant requirements**: FR-010, FR-011
- **Affected surfaces**: 篇2 全部九阶段小节 + 开篇总图
- **Sequencing/depends-on**: IC-02（契约围绕正确 API 写）
- **Risks**: 契约粒度要「具体到可执行」但不过度形式化——每阶段固定小节模板控制体量

### IC-04 — StockInsight 贯穿与领域适配指引

- **Purpose**: 荔枝植保示例整体替换为 StockInsight 投资案例（规则：毛利率连续下滑且亏损扩大→HOLD_AND_MONITOR；权限：投资决策需复核；溯源 source：财报 PDF 路径）；每阶段末尾加「换领域时怎么适配」短段（领域术语表怎么定、实体类型怎么抽象、规则模板怎么换），满足跨领域泛化；文档集开篇声明适用范围不限于金融。
- **Relevant requirements**: FR-004, FR-009
- **Affected surfaces**: 篇1 案例导语、篇2 各阶段示例与适配段、篇5 案例术语
- **Sequencing/depends-on**: IC-02（示例代码先正确再案例化）
- **Risks**: StockInsight 自身有遗留问题（脚本路径失配、std 未落地）——文档引用时只引已验证部分并注明；不把项目未完成的规划写成已完成事实

### IC-05 — cookbook/examples 实践模式融入

- **Purpose**: 17 个直接相关模式按阶段织入：3.2 抽取器复用/置信度阈值（C22/C23）、3.3 消解重映射（C12）、3.4 去重完整集+源可信度（C13/C15）、3.5 本体即代码+三件套+SHACL 双工件+CQ 前置（C1/C8/C6/C7）、3.7 入图前验证门禁（C14）、3.9 审计级溯源四元组+版本管理（C16/C9）；间接相关模式以「延伸阅读」链接 cookbook 原文。
- **Relevant requirements**: FR-003
- **Affected surfaces**: 篇2 各阶段、篇4 引用
- **Sequencing/depends-on**: IC-03（融入点由阶段结构决定）
- **Risks**: 避免堆砌——每个模式必须回答「解决本阶段什么问题」；cookbook 路径引用注意 use_cases/ 目录不存在的事实

### IC-06 — 能力边界校准与文档间不一致裁定

- **Purpose**: 篇4 显式区分「书稿目标标准 vs Semantica 实际实现」：SWRL/OWL-S/ODRL 无实现（grep 全包核实）、四剑客是 Protégé/OWL 推理机能力非 Semantica（T19c）、TEMPORAL/LOGICAL 冲突未实现于 ConflictDetector、provenance 默认不持久、推理在外部工具跑；给出每项的可行替代（Reasoner 规则代 SWRL、SHACL 事后校验代四剑客、PolicyEngine+人工流程代 ODRL）；收录 11 处官方文档间不一致裁定表（reference 为准）。
- **Relevant requirements**: FR-002（边界部分）, FR-001（书稿与工具冲突时以官方文档界定能力）
- **Affected surfaces**: 篇4 全文、篇5 术语表"标准"列
- **Sequencing/depends-on**: IC-02
- **Risks**: 边界结论须全部带证据（源码位置/文档路径），版本敏感结论注明 0.6.7

### IC-07 — 文档集结构、导航与引用链接

- **Purpose**: 篇1 开篇为文档集导览（5 篇地图 + 三条阅读路径：快速上手/完整工程/深度参考）；每篇开篇「本篇讲什么/建议前置」+ 篇末参考资料清单；正文引用处标注仓库相对路径链接（书稿/官方 docs/cookbook/examples/StockInsight）；互引 ≤3 处/篇；修复 F4 章节号错位。
- **Relevant requirements**: FR-006, FR-012, NFR-002, NFR-004
- **Affected surfaces**: 全部 5 篇
- **Sequencing/depends-on**: IC-01~06（成文后统一定稿）
- **Risks**: 链接校验脚本必须跑（Testing ②），防止死链

### IC-08 — 中文写作规范与术语统一

- **Purpose**: 全文符合中文表达习惯（短句、意合、段落自然过渡）；术语首次出现「中文(English)」格式、全文与篇5 术语表一致；统一"双模型协同"为书稿 6.2.2 原义（生成者+审计者），5.2 旧义的"语义层+向量层"改名"混合检索表示"；消除 F2/F8 术语漂移（实体标识三形态的转换点在文中显式说明）。
- **Relevant requirements**: FR-007, NFR-003
- **Affected surfaces**: 全部 5 篇 + 篇5 术语表
- **Sequencing/depends-on**: IC-01~07（终稿统一润色）
- **Risks**: 术语表先行（篇5 先立规范），各篇写作时对照

### 阶段契约骨架（篇2 内容大纲，IC-03 的执行模板）

| 阶段 | 输入（变量/形态） | 输出（变量/形态/判据） | 前置 | 后续 |
|---|---|---|---|---|
| 3.1 多源萃取 | raw 文档路径（StockInsight: stocks/00100/raw/） | `chunks: List[Chunk]`（text/start_index/end_index/metadata/id）；判据：全覆盖无丢块 | 确定业务意图与数据域清单 | 3.2 |
| 3.2 语义标准化 | chunks | `entities/relations/events: List[dict]`（统一 dict schema：Entity {text,type,confidence,start,end} 等）；判据：置信度阈值过滤后非空 | 3.1 + LLM 端点配置 | 3.3（events 另记流向） |
| 3.3 术语归一 | entities/relations | 规范化后的同名集合（EntityNormalizer alias_map + CoreferenceResolver + merge_entities(entities, method=)）；判据：同义异形合并、跨块指代消解 | 3.2 + 领域术语表 | 3.4 |
| 3.4 冲突去重 | 规范化 entities/relations | 冲突报告（detect_conflicts(method=)）→ 消解决策 → 去重完整集（MergeOperation+孤立实体）；判据：冲突清零或全部挂人工审查 | 3.3 | 3.5/3.7 |
| 3.5 本体建模 | 去重后 entities/relationships（数据驱动）或审核过的本体 dict（注入版） | ontology dict（classes/properties 含 domain/range）+ Turtle（to_owl，注入版先规范 uri 键）+ SHACL shapes；判据：validate 通过 + CQ 验收 | 3.4 + 29 句话产出（篇1） | 3.6/3.7 |
| 3.6 规则推理+审计 | 事实（字符串/dict）+ 规则清单（源自 29 句话第④类） | 推理信号 List[InferenceResult] + 审计报告（双模型协同）；判据：审计三维度通过；不通过→回退路径明确 | 3.5 | 3.7 |
| 3.7 建图与校验 | {"entities": [...], "relationships": [...]} + ontology | graph dict（GraphBuilder.build）→ GraphValidator 通过 → SHACL validate_graph(kg, ontology=)（RDF 字符串）通过；判据：is_valid 且 conforms | 3.4/3.5/3.6 | 3.8 |
| 3.8 场景测试 | graph + ontology + 黄金用例（CQ） | 测试报告（validate_ontology 正确键 + Reasoner 断言）；判据：核心用例全过；失败→归因三分类回退 | 3.7 + 专家黄金用例 | 3.9 |
| 3.9 资产入库 | graph + 溯源四元组 | PROV 记录（track_entity 四元组）+ 导出（export_rdf/parquet，CLI --format）+ 决策记录（record_decision）+ 版本快照；判据：决策可回溯、导出文件可加载 | 3.8 | 下游消费（Explorer/FalkorDB/Agent） |

（阶段名与划分在写作时按官方 pipeline 顺序微调，四要素模板不变。）

## 执行顺序与验证

1. **IC-08 术语表先行**（篇5 骨架）→ 2. **IC-01+IC-02 并行**（篇1 重排 + T 清单消解底稿）→ 3. **IC-03/04/05 织入篇2**（核心工程量）→ 4. **IC-06 篇4** → 5. **篇3 收拢模板** → 6. **IC-07+IC-08 终稿**（导航/链接/润色）→ 7. **验证**：最小链路执行 + 链接校验 + 对照 spec 成功标准逐条自查。

失败处理：任何阶段发现 research 摘要与实际源冲突，以实际源为准并回写 research 摘要（DIR-001 一致性）。
