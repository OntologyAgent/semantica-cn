# 官方文档能力事实矩阵（核验基准）

> 来源：子代理聚焦阅读 docs/（全局 4 篇 + 主线 guides/reference 10 篇 + 上游 4 篇简读 + 7 篇抽查）
> 注意：本仓库 quickstart 标注当前版本 **0.5.0**，而 StockInsight 实测 .venv 是 **0.6.7**——文档版本滞后于实装，API 以实际验证为准、文档为核验参照。

## A. 模块能力矩阵

### A1. ontology（主线核心）
- 统一入口 `OntologyEngine(base_uri=...)`："Unified facade orchestrating the full ontology lifecycle"（reference/ontology.md）
- 方法：`from_data(data)`（跑 5 阶段管线）、`validate_graph(kg, ontology=...)`、`export_owl(ontology, path, format)`（turtle/xml/json-ld）、`evaluate(ontology, kg)`、`validate(ontology)`、`export_shacl(ontology, "shapes.ttl")`
- `OntologyGenerator(base_uri=..., min_occurrences=...)`：`generate_ontology({entities, relationships})` 与 `generate_from_graph(graph.to_dict(), name=..., build_hierarchy=True)` 两个名字都在文档中
- **生成方向是「图→本体」**："derives a formal OWL ontology directly from the entities and relationships already in your knowledge graph — no schema design upfront"；有图后用确定性 `generate_from_graph`，LLM 生成只做 bootstrap
- 生成结果：`ontology.get('classes', [])`（name/parent）、`ontology.get('properties', [])`（type: object|data、name、domain、range）
- 独立函数 `validate_ontology(ontology)` → {valid, warnings, errors}
- 增量：`ClassInferrer().infer_classes(entities)`、`build_class_hierarchy(classes)`、`PropertyGenerator`、`AssociativeClassBuilder`（"Model N-ary relationships as intermediate OWL classes"）
- LLM：`LLMOntologyGenerator(provider="groq"|"openai"|"anthropic"|"novita", model=...)`，`generate_ontology_from_text(text)`
- SHACL：`SHACLGenerator().generate(ontology)`；`OntologyValidator().validate_graph(kg, ontology=)` → SHACLValidationReport（conforms/violations/focus_node/result_path/severity/message）
- 评估：`OntologyEvaluator().evaluate_ontology(ontology, kg)` → class_coverage/property_coverage/completeness/granularity/gaps
- 命名空间：`NamespaceManager(base_uri=)`：register/generate_class_iri/generate_property_iri
- 导入：`ingest_ontology("schema.ttl"|"schema.owl"|"schema.jsonld")`；ingest 侧 `OntologyIngestor().ingest_ontology(path, format="turtle")`
- 推理边界："Semantica exports the ontology; reasoning itself runs in the external tool"（HermiT/Pellet/ELK）
- Ontology Hub（v0.5.0，semantica.explorer）：可视化编辑器、SHACL Studio、alignment、health dashboard
- VersionManager/OntologyVersion 已移到 semantica.change_management
- 常见陷阱（guides/ontology.md）：over-modeling、ontology drift、类命名约定不一致

### A2. kg（GraphBuilder）
- `GraphBuilder(merge_entities=True)`；**merge_entities 默认 False**；`build(sources)` → dict（dict/列表/对象均可）；`build_single_source(data)`；quickstart 也展示 `build(entities=..., relationships=...)`
- 持久化：`GraphBuilder(..., graph_store=store)` 边建边写 Neo4j/FalkorDB
- `GraphBuilderWithProvenance(provenance_manager=...)`
- `GraphValidator().validate(kg)`（接受 build() 产物 dict）→ is_valid/issues；strict=True 把 warning 当 error；**可传 schema dict（entity_types/relationship_types）验证类型词汇表——文档中唯一「schema 进 KG 构建」的显式通道**
- 时态：关系带 valid_from/valid_until（无 until → TemporalBound.OPEN）；TemporalGraphQuery.query_at_time/reconstruct_at_time/query_time_range；BiTemporalFact（recorded_at/superseded_at）；TemporalVersionManager（create_snapshot/list_versions/compare_versions/verify_checksum）
- 分析：CentralityCalculator（5 种）、CommunityDetector（Louvain/Leiden/Label Propagation/K-Clique）、PathFinder（Dijkstra/A*/BFS/K-Shortest）、LinkPredictor、NodeEmbedder(node2vec)、GraphAnalyzer（一键）、ConnectivityAnalyzer
- 配置 YAML：kg.resolution.threshold/strategy、kg.temporal.*

### A3. semantic_extract
- 抽取器：NERExtractor、NamedEntityRecognizer（高层协调+阈值+重叠合并）、RelationExtractor、TripletExtractor、EventDetector、CoreferenceResolver、SemanticAnalyzer、SemanticNetworkExtractor
- 方法：reference 正文 pattern/huggingface/llm 三模式；对比表另有 ml；RelationExtractor 另有 dependency/cooccurrence；TripletExtractor 另有 rules；EventDetector 仅 pattern+llm
- 回退链：`NERExtractor(method=["llm", "pattern"])` "guarantees non-empty results"
- 参数：`llm_provider=llm`、`max_retries=3`、`custom_entities={"DRUG": [...]}`（pattern 字典）
- 输入：extract(text) 单/批量自动检测；批量可传 `[{"id": "doc_1", "content": "..."}]`（加溯源 metadata）
- 输出：Entity `{text, type, confidence, start, end}`；Relation `{subject, predicate, object, confidence}`；Event `{type, participants, temporal, location, confidence}`
- 关系抽取签名：`rel.extract(text, entities=entities)`（所有文档一致）
- 安装边界：pattern 零依赖；huggingface 需 extra；llm 需 extra + key

### A4. conflicts
- ConflictType 五种：VALUE/TYPE/TEMPORAL/LOGICAL/RELATIONSHIP
- **检测器仅 4 方法**：detect_value_conflicts(entities, property_name, entity_type=)、detect_type_conflicts(entities)、detect_relationship_conflicts(relationships)、detect_entity_conflicts(entities, entity_type=)、get_conflict_report()
- **Warning："TEMPORAL and LOGICAL conflict detection is not implemented on ConflictDetector directly"**
- `ConflictResolver(source_tracker=tracker)`；7 策略：VOTING/CREDIBILITY_WEIGHTED/MOST_RECENT/FIRST_SEEN/HIGHEST_CONFIDENCE/MANUAL_REVIEW/EXPERT_REVIEW
- `SourceTracker().set_source_credibility(name, score)`；**credibility 默认 0.50，不显式设置则 CREDIBILITY_WEIGHTED 等同 VOTING**
- ConflictAnalyzer.analyze_conflicts（patterns/by_severity/by_source）、analyze_trends
- InvestigationGuideGenerator.generate_guide(conflict)（title 是 @property）
- **顺序铁律："Detect before you merge, not after."** 冲突检测在 dedup 与构图之前，图里合并后 source attribution 会丢

### A5. deduplication
- `DuplicateDetector(similarity_threshold=0.7, confidence_threshold=0.6, max_results=100, top_k_per_entity=3, min_similarity=0.75, sort_by="confidence")`
- `detect_duplicates(entities)` → List[DuplicateCandidate]（字段 **entity1/entity2**/similarity_score/confidence/reasons）
- `detect_duplicate_groups(entities)` → union-find 传递聚类
- `EntityMerger.merge_duplicates(entities, strategy="keep_most_complete")` → **List[MergeOperation]，不是实体列表**（文档明确 Warning）；策略 keep_first/keep_last/keep_most_complete/keep_highest_confidence/merge_all
- 便捷函数：detect_duplicates(entities, method="pairwise"|"batch"|"incremental"|"group", ...)、merge_entities(entities, method=)、calculate_similarity(a, b, method="multi_factor")
- v2 策略 blocking_v2/hybrid_v2/semantic_v2 快 7×；concepts：v1=Jaro-Winkler
- "All workflows operate on plain Python dicts: no ORM or schema required"；先 Normalize 再匹配
- 自定义相似度：method_registry.register("similarity", "drug_name", fn)

### A6. reasoning
- 引擎：Reasoner（forward/backward）、GraphReasoner（LLM 问答）、ReteEngine、SPARQLReasoner、DatalogReasoner、TemporalReasoningEngine、ExplanationGenerator
- Reasoner：add_fact("Manager(Alice)")（字符串/实体 dict/关系 dict）、add_rule("IF ... THEN ...") 或 Rule 对象、forward_chain()（**max_iterations 默认 50，深递归静默提前停**）、backward_chain(goal, max_depth=10)、infer_facts(facts, rules)
- RuleType.IMPLICATION|EQUIVALENCE|CONSTRAINT|TRANSFORMATION；字段 rule_id/name/conditions/conclusion/rule_type/confidence/priority
- Datalog：add_fact（常量小写开头）、add_rule("ancestor(X, Y) :- parent(X, Y).")、derive_all()、query("ancestor(alice, ?Z)")、load_from_graph(graph)（ContextGraph nodes/edges 转 facts，**谓词与参数被小写化**）、clear()；"Termination is guaranteed"（semi-naive fixpoint）
- GraphReasoner：provider 初始化失败**返回 error 字符串而非抛异常**
- SPARQLReasoner：无 triplet_store 时 execute_query 返回空 bindings
- ExplanationGenerator()（无位置参数）：generate_explanation(result)、show_reasoning_path(result)、justify_conclusion(conclusion, path)

### A7. provenance
- `ProvenanceManager(storage=None, storage_path=None)`；默认 InMemoryStorage **不跨进程存活**；storage_path → SQLiteStorage
- track_entity(entity_id, source, source_location=, source_quote=, confidence=, entity_type=, metadata=)、track_relationship、track_chunk、track_property_source、track_entities_batch(entities, source)（batch_size=1000）
- 检索：get_lineage(id) → 聚合 dict（source_documents/first_seen/last_updated/lineage_chain/metadata）；trace_lineage(id) → List[ProvenanceEntry]；get_all_sources/get_provenance/get_statistics/clear
- 防篡改：每次 track 自动 SHA-256；verify_checksum(entry)；checksum 覆盖 entity_id/entity_type/activity_id/source_document/timestamp/confidence
- PROV-O compliant；**"ProvenanceManager does not include built-in Turtle or JSON-LD serialization"**——RDF 输出走 RDFExporter(include_provenance=True)
- `NERExtractor(method="ml", provenance=True)` 只在实体对象嵌 metadata，**不自动调 track_entity**

### A8. context
- `AgentContext(vector_store=..., knowledge_graph=ContextGraph(...), decision_tracking=False, retention_days=30, max_memories=10000, graph_expansion=True, max_expansion_hops=2, hybrid_alpha=0.5)`
- **decision_tracking=True 必须同时给 knowledge_graph，否则 record_decision 抛 RuntimeError**
- store(content, metadata=, conversation_id=, user_id=)（str→ID；list→stats）；retrieve(query, max_results=5, ...)（**参数是 max_results 不是 top_k**）；save(path)/load(path)
- **VectorStore 的 index_path= 是 no-op，持久化必须走 context.save()**
- 决策：record_decision(category, scenario, reasoning, outcome, confidence, entities, decision_maker, valid_from, valid_until) → str；find_precedents(scenario, category, limit, use_hybrid_search, max_hops, as_of)；query_decisions；get_causal_chain(decision_id, direction="upstream"|"downstream", max_depth)；trace_decision_explainability；get_policy_engine()
- GraphRAG：context.load_graph("company_kg.json")；query_with_reasoning(query, llm_provider=, max_hops=2, max_results=10)；retrieve(query, use_graph=True)
- ContextGraph 独立可用：add_node/add_edge（bulk add_nodes/add_edges）、get_neighbors(node_id, hops, min_weight=)、record_decision、find_precedents_by_scenario、query()（全文检索）、stats()、density()、save_to_file/load_from_file、build_from_conversations、purge_node()；**to_dict() 产物可直接喂 OntologyGenerator 与 YAML exporter**
- 其他：AgentMemory（Markdown 往返 export/import_data）、EntityLinker(similarity_threshold=0.8)（link_entities(entity1_id, entity2_id, link_type, confidence) 是两个 ID）、PolicyEngine(graph_store=).add_policy/check_compliance、CausalChainAnalyzer、ErasureCoordinator（GDPR 级联，FAISS/Milvus/Weaviate 无删除接口报 unsupported）

### A9. export
- RDFExporter.export_to_rdf(graph, format=) → 字符串；export(graph, file_path, format=) → 写文件；格式 turtle/ttl、jsonld/json-ld、ntriples/nt、rdfxml/xml/rdf；include_temporal=True, time_axis="valid"|"transaction"|"both"（OWL-Time）；include_provenance=True
- ParquetExporter(compression="snappy")：export_entities/export_relationships/export_knowledge_graph → <base>-entities.parquet + <base>-relationships.parquet
- LPGExporter（Cypher CREATE）、ArangoAQLExporter、GraphExporter（graphml/gexf/dot）、OWLExporter、CSVExporter、VectorExporter、ArrowExporter、DistanceExporter(graph)（构造必须传 graph）、ReportGenerator
- 便捷函数：export_rdf/json/parquet/csv/lpg/arango/graph/owl/vector/arrow/yaml、generate_report
- 陷阱：ArangoAQL/LPG export() 写文件返回 None；**pyarrow 缺失时 Parquet/Arrow 是 no-op stub**；YAML/LPG/AQL 接受 entities/relationships/triplets（nodes/edges 为别名），空映射抛 ValidationError

### A10. 上游阶段（边界）
- ingest：路径/URL/DB → typed object（FileObject/WebContent/TableData）；`ingest(path)` → dict 分发；FileIngestor().ingest_file/ingest_directory(recursive=True)；15+ ingestor；DuckDB/Elastic/GDrive/HuggingFace/Mongo/Pandas 未从顶层 re-export
- parse：文件 → dict {full_text, metadata, pages, tables, images, total_pages, export_format}；DocumentParser() 零依赖；DoclingParser(export_format="markdown", enable_ocr=) 需 docling；parse_batch(sources, continue_on_error=True)
- normalize：TextNormalizer.normalize_text(text, unicode_form="NFC", case=)；EntityNormalizer(alias_map={...})（**无内置公司后缀展开**）；DateNormalizer(format="ISO8601", timezone="UTC")；NumberNormalizer("$1.2B")→1200000000.0；顺序：编码→文本→实体→日期/数字→语言；**NER 前勿 lowercase**
- split：TextSplitter(method=, chunk_size=1000, chunk_overlap=200)；方法 recursive/semantic_transformer/entity_aware/relation_aware/structural/sliding_window/sentence/paragraph/token/word/character/embedding_semantic/hierarchical；→ List[Chunk]（text/start_index/end_index/metadata/id）；**KG 管道推荐 relation_aware（三元组不跨块）**

## B. 流水线衔接事实（architecture.md / modules.md Common Module Chains / quickstart.md）

1. Ingest→Parse：ingestor 产物直接 `parser.parse(source)`
2. Parse→Extract：`ner.extract(parsed)` 或取 full_text 分块抽取
3. Extract→关系抽取：`rel.extract(text, entities=entities)`（NER 结果为显式入参）
4. Extract→GraphBuilder：`{"entities": [...], "relationships": [...]}` 传 build()；多文档先累加再一次性 build（增量）
5. **QA 顺序**：pipeline 模板 kg_construction = Ingest → Extract Entities → Extract Relations → **Dedup → Resolve** → Build Graph（"saving you from common mistakes like deduplicating before normalizing"）；conflicts.md 要求冲突检测在 merge/构图**之前**
6. KG→持久化：GraphBuilder(graph_store=store) 边建边写
7. KG→Ontology：GraphBuilder 产物 dict / ContextGraph.to_dict() → OntologyGenerator.generate_from_graph / OntologyEngine.from_data；**文档未提及 GraphBuilder 直接接受 ontology 参数**——本体进 KG 侧只有三条路：GraphValidator(schema=) 类型词汇校验、SHACL 事后验证 validate_graph(kg, ontology=)、KGEvaluator().evaluate(kg, ontology=)
8. KG/本体→Export：graph dict → RDFExporter.export(..., format="turtle")；ontology dict → export_owl/export_rdf
9. KG→Context：context.load_graph("company_kg.json")
10. KG→Reasoning：DatalogReasoner.load_from_graph(graph)
11. 模板：PipelineTemplateManager.create_pipeline_from_template("ontology_generation") = Extract Concepts → Infer Classes → Infer Properties → Generate OWL → Validate

## C. 文档间不一致清单（核验中文文档论断时的对照表）

| # | 写法 A | 写法 B | 裁定 |
|---|---|---|---|
| 1 | OntologyGenerator 6-stage（guides/concepts） | 5-stage（reference） | 以 reference 为准表述或回避具体阶段数 |
| 2 | RuleType.FORWARD_CHAIN（concepts） | RuleType.IMPLICATION 等 4 值（reference/guides） | reference 为准 |
| 3 | DatalogEngine()、apply_transitivity/apply_symmetry/infer()（modules） | DatalogReasoner、forward_chain/backward_chain/infer_facts（reference） | reference 为准 |
| 4 | prov.get_entity_lineage（concepts/quickstart） | get_lineage/trace_lineage（reference） | reference 为准 |
| 5 | detector.detect_conflicts(kg) + detector.resolve（modules） | ConflictDetector.detect_* + ConflictResolver.resolve_conflicts（reference） | reference 为准 |
| 6 | context.analyze_decision_influence(id)、context.query(mode="graphrag")（concepts/quickstart/modules） | trace_decision_explainability、retrieve/query_with_reasoning（reference） | reference 为准 |
| 7 | DocumentParser(ocr=True)（quickstart） | OCR 走 DoclingParser(enable_ocr=True)（reference） | reference 为准 |
| 8 | 抽取方法 "ml"（concepts/modules/split） | "huggingface"（reference 正文） | 并存，以 StockInsight 实测（method="llm", provider="openai"）为准 |
| 9 | LLM provider 9 个（concepts）vs 8 个（modules） | guides/llm-integrations: Groq/OpenAI/Anthropic/HuggingFace/Novita + LiteLLM 100+ | guides 为准 |
| 10 | merge_duplicates 返回实体列表（concepts 暗示） | List[MergeOperation]（reference 明确 Warning） | reference 为准 |
| 11 | merge_entities=True 语义（quickstart: semantic similarity 自动去重；reference: enable entity deduplication，机制由 kg.resolution 配置） | — | 按 reference + 实测 |

## D. 已知能力边界（文档明说）

- conflicts：TEMPORAL/LOGICAL 未实现在 ConflictDetector；credibility 默认 0.50
- reasoning：GraphReasoner 失败返回 error 字符串；forward_chain 深递归静默停（用 DatalogReasoner）；SPARQLReasoner 无 store 空返回
- provenance：默认内存不持久；无内置 Turtle 序列化；provenance=True 不自动 track
- context：decision_tracking 必须配 knowledge_graph；index_path 是 no-op；FAISS/Milvus/Weaviate 无删除接口
- export：pyarrow 缺失 Parquet/Arrow no-op；部分导出器返回 None
- parse：DoclingParser 需 docling；DocumentParser 始终可用
- normalize：EntityNormalizer 无内置后缀展开
- ontology：LLM 生成非确定耗 token；推理在外部工具跑

## E. 版本注意

- v0.4.0：Datalog、temporal（Allen/OWL-Time）；v0.5.0：Ontology Hub、Distance Intelligence、Parquet/XML ingest
- **quickstart 标注 0.5.0；StockInsight 实测 0.6.7**——文档滞后，凡冲突以 StockInsight 已验证调用为准并在最佳实践里注明

## F. 文档路径索引（实际读过）

全局：docs/concepts.md、architecture.md、quickstart.md、modules.md
主线：docs/guides/ontology.md、docs/reference/{ontology,kg,semantic_extract,conflicts,deduplication,reasoning,provenance,context,export}.md
上游简读：docs/reference/{ingest,parse,normalize,split}.md
抽查：docs/reference/pipeline.md（kg_construction/ontology_generation 模板）、docs/guides/{reasoning,semantic-extraction,conflict-resolution,deduplication,llm-integrations}.md、docs/reference/graph_store.md
未整篇读（需逐句核对时补充）：docs/guides/{graph-analytics,graphrag,shacl-validation,context-graphs,decision-intelligence,export,provenance,distance-intelligence}.md
