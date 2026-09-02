# 现有《本体建模最佳实践.md》审计报告

> 来源：子代理全文审计 744 行文档，逐条对照重扫书稿、semantica 源码（含实测 import）、官方 docs/reference、StockInsight 脚本。
> 核心结论：**约八成代码示例实测不能直接跑通**；29 句话表与重扫书稿大面积不符（旧版扫描带偏的实锤）；术语"双模型协同"一词两义；多处内部矛盾。

## A. 章节地图

| 行号 | 标题 | 体量 | 类型 |
|---|---|---|---|
| 1–9 | 引言 | 9 | 方法论论述（含"原创声明"，与事实冲突见 F5） |
| 11–27 | 一、全局视图 | 17 | 九阶段↔模块映射表 |
| 31–85 | 二、输出契约 | 55 | 29 句话表（讹误重灾区 F1） |
| 89–488 | 三、逐步落地 | 400 | 九阶段代码（3.1 萃取13 / 3.2 标准化42 / 3.3 术语归一62 / 3.4 冲突去重13 / 3.5 本体建模55 / 3.6 推理审计85 / 3.7 可视化49 / 3.8 场景测试53 / 3.9 入库16） |
| 492–539 | 四、质量准入 | 48 | 四铁律 P1–P4 + 评审路径 |
| 543–585 | 五、校验与术语 | 43 | 属性四剑客 / 术语速查 / 易混点 |
| 589–621 | 六、提示词与双模型 | 33 | 方法论 + 对比表 |
| 625–673 | 七、不足与替代 | 49 | ODRL 五影子方案 + 兼容表 |
| 676–714 | 八、结语 | 39 | 本体→决策→回路 |
| 717–744 | 附录 | 28 | 最小可跑链路（含 T1/T12/T16 错误） |

## B. 来源推断

| 章节 | 来源 | 依据 |
|---|---|---|
| 一 | 作者自创综合 | 书稿是五环（预处理-建模-入库-平台-实施），九阶段流水线是把书稿映射到 Semantica 的再创作 |
| 二 | 书稿 6.1.1 图 6-1 改编 | "29 句话""7 类语义"是书稿原概念；表格讹误与旧扫描特征吻合 |
| 3.1/3.2 | Semantica 官方能力 | API 真实但用法多有错（见 C） |
| 3.3 | 混合 | SKOS 说法源自书稿 6.1.2；B 模板骨架仿 llm_generator._build_prompt 自创 |
| 3.4 | Semantica + 书稿"逻辑正确"工程化 | 先标记再合并对应书稿 6.1.3 |
| 3.5 | 书稿 6.2.1 + from_text/to_owl | 书稿要 Turtle 输出，文档改为"输出 dict、Turtle 由库生成"是有意纠正 |
| 3.6 | 书稿 6.2.2 双大模型 + Reasoner | 三步闭环与书稿表 6-3 一一对应 |
| 3.7 | 书稿 6.2.3 + kg | 四剑客直接取自书稿（书稿脚注引 Protégé 指南） |
| 3.8 | 书稿 6.2.4 + Reasoner | 黄金用例+AI 矩阵对应书稿两步法 |
| 3.9 | 作者补写 | 书稿"入库"环节在 6.3（未收录）；provenance/context/export 是真实 API |
| 四 | 书稿 6.1.3 几乎逐条对应 | P1–P4 = 描述清晰/逻辑正确/内容完备/极简表达 |
| 五 5.1 | 书稿 6.2.3 | 同 3.7（但嫁接到了 Semantica 上，见 T19） |
| 五 5.2/5.3 | 作者自创 | "双模型协同"定义与书稿原义冲突（F2） |
| 六 | 书稿 6.2.1/6.2.2 + 作者经验 | .replace 不用 .format 是实测心得 |
| 七 | 作者代码考古 + 书稿 ODRL 落空记录 | 五影子方案是上游勘察 |
| 八 | 作者提炼 + context 能力 | 本体-决策-回路为作者综合 |

## C. 待核验论断清单（✗=不成立 △=有偏差 ?=待核）

- **T1 ✗（最严重）** `from semantica.semantic_extract import extract_triplets_llm` 实测 ImportError；正确 `from semantica.semantic_extract.methods import extract_triplets_llm`（methods.py:2367 未进 _LAZY_EXPORTS）。官方只示范 TripletExtractor 类。
- T2 ✓ extract_triplets_llm 返回 List[Triplet]（subject/predicate/object/confidence/metadata）
- T3 △ Chunk 字段实为 start_index/end_index（非 start/end）
- T4 ? "回文本反查偏移"机制待核 match_entity
- T5 ✓ EventDetector(method="llm", provider=)/detect_events/Event 九字段一致
- **T6 ✗** `EntityCoreferenceDetector().resolve(doc, entities=)`——该类无 resolve（只有 detect_entity_coreferences(text, mentions)）；带 resolve 的是 CoreferenceResolver；返回 CoreferenceChain 列表非"规范名"
- **T7 ✗** `merge_entities(groups=..., strategy="prefer_prefLabel")`——实际签名 merge_entities(entities: List[Dict], method="keep_most_complete")；无 prefer_prefLabel、无 groups 参数
- **T8 ✗（结构性）** "B/E 模板输出的 classes/properties 字典 from_data 直接入库"——from_data→generate_ontology 只接受 entities/relationships，从数据推导本体，不吃现成类定义。注入版正确路径：仿 llm_generator._normalize_output 把 base_uri 规范成 uri 键后直接喂 to_owl（to_owl 读 ontology.get("uri")，owl_generator.py:179）。3.3/3.5 注入版需重设计。
- **T9 ✗** `OntologyEngine()` 默认构造 store=None，create_alignment 抛 ProcessingError（须配 TripletStore）
- **T10 ✗** `detect_conflicts(facts, rule="attribute_range_conflict")`——参数是 method，合法值 value/type/relationship/temporal/logical/entity，无 rule 参数
- T11 △ `resolve_conflicts(c, policy="expert_review")` 参数应为 method；expert_review 是合法值
- **T12 ✗** `dedup_triplets(facts)` 返回重复对列表（检测非清洗）；附录还把 Conflict 列表错喂给它
- T13 ✓/△ from_text/to_owl/to_shacl 存在；默认版链路成立、注入版不成立（T8）
- T14 ✓ CompetencyQuestionsManager.add_question/validate_ontology
- T15 △ validate_ontology 判定是关键词启发式（_can_ontology_answer），"逐句验收"表述偏强
- **T16 ✗** 附录 `validate_ontology(model)["questions"][0]["answerable"]`——返回 dict 无 questions 键（实际键 total_questions/answerable/unanswerable/by_category）；逐题状态在 manager.questions[i].answerable
- T17 ✓ Reasoner IF...AND...THEN/add_fact/forward_chain/backward_chain 属实；**另核实：_parse_rule_definition 对不匹配规则静默生成永不触发的空条件规则而非报错**（比文档 7.2 说的更隐蔽，修订要写明）
- **T18 ✗✗** `GraphBuilder().build(entities=..., relationships=...).to_kg_dict()`——build(sources) 不接受这两个关键字（正确传 {"entities": [...], "relationships": [...]}）；GraphBuilder 无 to_kg_dict 方法，build 本身返回 dict
- **T19 ✗✗** "OntologyEngine().validate_graph(gview) 校验属性四剑客"——(a) validate_graph(data_graph, shacl=None, ontology=None) 必须给其一否则 ValueError，官方用法 validate_graph(kg, ontology=ontology)；(b) data_graph 须 RDF 字符串或 rdflib.Graph，GraphBuilder dict 不是；(c) **代码库全文无 FunctionalProperty/InverseFunctionalProperty/TransitiveProperty/inverseOf 的任何处理，to_shacl 也不生成这四类约束——四剑客是书稿的 Protégé/OWL 推理机能力，被嫁接到 Semantica**
- T20 ✓ record_decision/track_entity 签名吻合
- **T21 ✗** CLI `semantica export --rdf /catalog.ttl`——实际 `semantica export --format turtle --output graph.ttl`，无 --rdf 选项
- T22 ✓ 7.1 五处影子方案全部核实（server.py:95 CORS、sparql.py:41、record_decision、add_rule、associative_class.py:206）
- T23 ✓/△ find_precedents、analyze_decision_influence 均存在
- **T24 ?** 术语表把 SWRL/OWL-S 列为"标准"——grep 全包无 SWRL、无 OWL-S、无 ODRL 实现；修订须显式区分"目标标准"与"实际实现"
- T25 ? 3.9"版本可回滚"无 API 支撑（上游有 version_manager/change_management 但正文零代码，应补或删）

## D. 阶段契约缺口（对照 输入/输出/前置/后续 四要素）

| 阶段 | 缺口 |
|---|---|
| 3.1 | 后续流向未明说（chunks 交给谁） |
| 3.2 | 对象 vs dict 未约定，而 3.4 要 List[Dict]，转换断档；events 流向无交代 |
| 3.3 | **缺口最大**：输入 objects 无来源定义；默认版/注入版产物性质不同未说明；输出去向未说 |
| 3.4 | 输入 facts 无来源定义；输出 clean 名不副实（T12） |
| 3.5 | 注入版 desc 如何由 A/B/C/D 合成完全没讲；glossary/prefix 来源无定义 |
| 3.6 | 规则清单来源未定义；审计不通过回路未写 |
| 3.7 | 输入用 ... 省略且 API 写错；校验不过处置流未写 |
| 3.8 | 前置依赖隐含；失败修复回路丢了（书稿 6.2.4 第三步有"结果回溯"） |
| 3.9 | entity_id 凭空出现；版本回滚无支撑；无"资产如何被消费"出口 |

共性：九阶段之间没有任何"上一阶段产物变量名→本阶段输入变量名"的数据流；四铁律与 3.1–3.9 的退回对应只给模块名没给阶段号。

## E. 领域绑定度

**写死荔枝植保（需整体换 StockInsight）**：pest_records.csv、荔枝蝽施药、蜂糖罂/白糖罂、霜疫霉病 500–1000 倍、Disease/tempHigh/humidityHigh 规则、:FrostBlight、农户权限、H/I 模板植保实参。
**已领域无关可保留**：A–I 模板正文、四铁律检查单、5.2/5.3 术语表、6 章方法论述、7.1 影子方案表、8 章全文。
**改造点**：规则→投资规则（毛利率连续下滑且亏损扩大→HOLD_AND_MONITOR）；权限→投资决策需复核；H 模板评审人→投资经理；溯源 source→财报 PDF 路径（StockInsight 有现成写法）。

## F. 可疑点

1. **29 句话表讹误重灾区**：重扫版 29 句 = 2+7+3+1+5+4+7；文档枚举 = 4+7+3+6+2(+4 缺)+4+7，既不足 29 也对不上类。文档 13 归类错；14 书稿无此句；22/23 重复；42–46 错归第 4 类（实为第 5 类）；51 语句不通；53–56 标"（原图裁切）"；72/76 语义错配（7.2 是"高效查"、7.6 是"查复杂"）。**修订必须以重扫书稿图 6-1 为准重排。**
2. "双模型协同"一词两义：5.2 定义"语义层+向量层双表示"，3.6/六/七指"生成者 LLM+审计者 LLM"（书稿原义）。内部矛盾。
3. I 模板与 7.1 矛盾：C 模板明令不要 ODRL，I 模板却允许 kind: "odrl" 用例；全库无 SWRL 实现，3.8"注入版"无执行引擎。
4. 五处"见第八章"实为第七章 7.1（第八章是结语）。
5. line 5"方法论为原创，不复制书籍原文"与事实冲突（四铁律/29 句话/评审路径/四剑客/双模型协同均取自书稿）——需重写为诚实引用。
6. line 3"反复验证"声明与 T1/T6/T7/T8/T9/T10/T12/T16/T18/T19/T21 实测不成立冲突；真正跑通的是 StockInsight 那套 API 组合。
7. 3.7 名实不符：标题"可视化把关（kg visualization）"，实际 visualization 模块全文未调用，"可视化"由 H 模板让 LLM 画 Mermaid——与确定性基础设施定位相悖。
8. 术语漂移：原文子串→类/属性 dict→IRI 三种标识形态并存，无说明在哪一步转换。
9. line 27"不是单向的流水线"自相矛盾（小瑕疵）。

## G. 拆分方案素材

**方案一（推荐）：契约—实现—协同—边界—参考 五篇**
1. 《方法总纲与知识契约》← 一、二、四、八
2. 《流水线逐步落地》← 三 + 附录（StockInsight 重写 + 四要素契约 + 变量流）
3. 《提示词与双模型协同》← 六 + A–I 模板集中管理 + 7.3 兼容表
4. 《能力边界与替代方案》← 七 + 5.1（目标标准 vs 实际实现）
5. 《术语速查与贯穿案例》← 5.2、5.3 + StockInsight 端到端

**方案二：读者旅程四篇**（实操篇约 480 行过厚）
**方案三：流水线纵深五篇**（贴合阶段契约但方法论/实现拆散，单篇叙事弱）

**前置工作（任何方案都需）**：①按 C 节清单逐条重验 API（约八成示例不能直接跑）；②29 句话表按重扫书稿重排。
