# cookbook + examples 实践模式摘要

> 来源：子代理读 cookbook 三子目录（41 notebook + 1 py）与 examples（4 py + ci/）
> 关键发现：advanced/13（手工本体+Snowflake 映射）与 advanced/14（Datalog）是仅有两篇带明确「最佳实践架构」论述的教程，是补充官方模块文档的最佳素材源。

## A. cookbook 教程地图（introduction 25 篇全读）

| # | 路径 | 主题 | 关键 API |
|---|---|---|---|
| 01 | introduction/01_Welcome | 三层架构+全模块+最小流水线 | `Semantica(config).build_knowledge_base(sources, embeddings, graph)`、`OntologyGenerator.generate_ontology` |
| 02 | 02_Data_Ingestion | 十类摄取器 | `FileIngestor`、`WebIngestor(delay, user_agent, respect_robots)`、`DBIngestor.export_table`、`MCPIngestor` |
| 03 | 03_Document_Parsing | 多格式解析 | `DocumentParser.extract_text/extract_metadata`、`CSVParser`、`StructuredDataParser.parse_data` |
| 04 | 04_Data_Normalization | 规范化 | `EntityNormalizer.normalize_entity(entity, entity_type=)`、`DateNormalizer`、`DataCleaner.clean_data(data, remove_duplicates=True)` |
| 05 | 05_Entity_Extraction | NER 五法对比 | `NERExtractor(method=)`、`NamedEntityRecognizer(methods, confidence_threshold, merge_overlapping)`、`EntityClassifier`、`EntityConfidenceScorer`、`CustomEntityDetector(patterns={regex})`、`ner.process_batch(docs)` |
| 06 | 06_Relation_Extraction | 关系抽取 | `RelationExtractor(relation_types, confidence_threshold, max_distance)`、`TripletExtractor(include_temporal, include_provenance)`、`RDFSerializer.serialize_to_rdf` |
| 07 | 07_Building_Knowledge_Graphs | span→建边、消解重映射 | `GraphBuilder.build({"entities","relationships"})`、`EntityResolver.resolve_entities`、`EntityMerger.merge_duplicates(strategy=MergeStrategy.KEEP_MOST_COMPLETE)` |
| 08 | 08_Your_First_KG | 五步端到端 | `FileIngestor.ingest_file`、`DocumentParser.parse_document`、`KGVisualizer.visualize_network(output="html")` |
| 09 | 09_Graph_Store | Neo4j/FalkorDB CRUD | `GraphStore(backend="neo4j")`、`create_node(s)`、`execute_query(sql, parameters=)`、`create_index(label, property_name)` |
| 10 | 10_Graph_Analytics | 中心性/社区/连通 | `GraphAnalyzer.compute_metrics`、`CentralityCalculator`、`CommunityDetector` |
| 11 | 11_Chunking | 15+ 分块法、KG-aware | `TextSplitter(method=)`、`EntityAwareChunker(ner_method)`、`RelationAwareChunker(preserve_triplets=True)`、`ProvenanceTracker.track_chunk` |
| 12 | 12_Embedding | 多 provider | `EmbeddingGenerator.generate_embeddings`、`TextEmbedder.set_model(method="fastembed")` |
| 13 | 13_Vector_Store | 索引/混合检索/namespace | `VectorStore(backend, dimension)`、`HybridSearch`、`MetadataFilter().eq().gt()` |
| 14 | **14_Ontology** | **本体生成主线** | `OntologyEngine(base_uri).from_data(data, name=)`、`ClassInferrer(min_occurrences)`、`PropertyGenerator.infer_properties(entities, relationships, classes)`、`OntologyOptimizer.optimize_ontology(o, remove_redundancy=True)`、`CompetencyQuestionsManager`、`VersionManager`、`ReuseManager`、`engine.export_owl` |
| 15 | 15_Export | 8 格式导出 | `RDFExporter.export(format="ttl")`、`CSVExporter.export_entities/export_relationships`、`OWLExporter`、`LPGExporter`、`MethodRegistry.register` |
| 16 | 16_Visualization | 四类可视化 | `KGVisualizer`、`OntologyVisualizer.visualize_hierarchy` |
| 17 | **17_Conflict** | **冲突主线** | `SourceTracker.register_source(source_id, source_type, credibility_score)`、`ConflictDetector(source_tracker=).detect_value_conflicts(records, "birth_date")`、`resolver.set_source_tracker` + `resolve_conflicts(conflicts, strategy="voting"/"credibility_weighted")`、`InvestigationGuideGenerator.generate_guide` |
| 18 | 18_Deduplication | 去重 | `SimilarityCalculator(string_weight, property_weight, relationship_weight)`、`DuplicateDetector(similarity_threshold).detect_duplicate_groups/incremental_detect`、`EntityMerger` |
| 19 | 19_Context_Module | 决策上下文 | `AgentContext.store/retrieve/conversation`、`ContextGraph.query/get_neighbors/stats`、`EntityLinker.link_entities`、`method_registry.register` |
| 20 | 20_Triplet_Store | RDF 存储 | `TripletStore(backend, endpoint)`、`add_triplet(s)`、`execute_query(SPARQL)` |
| 21 | 21_Neptune | IAM/OpenCypher | `GraphStore(backend="neptune", iam_auth=True)` |
| 22 | **22_Provenance** | **溯源主线** | `ProvenanceManager.track_entity(entity_id, source, confidence, source_location, source_quote)`、`track_relationship`、`get_lineage/revision_history/get_all_sources`、`invalidate(entity_id, agent_id, reason)`、`verify_checksum/verify_chain` |
| 23 | 23_Reasoning | 前向/后向/Datalog/解释 | `Reasoner.add_fact/add_rule/forward_chain/backward_chain/infer_facts`、`DatalogReasoner.derive_all/query`、`ExplanationGenerator` |
| 24 | 24_Change_Management | 版本快照+防篡改 | `ChangeLogEntry(timestamp, author=email, description)`、`InMemoryVersionStorage.save/save_tag/get`、`compute_checksum/verify_checksum`、`SQLiteVersionStorage` |
| 25 | 25_Seed_Data | 种子先行 | `SeedDataManager.register_source/load_source/create_foundation_graph/validate_quality` |

## advanced/（13 notebook + snowflake py）

| # | 主题 | 关键 API |
|---|---|---|
| 01 | 高级抽取：事件→共指→三元组→LLM 增强→校验 | `EventDetector`、`CoreferenceResolver`、`LLMEnhancer.enhance_extractions`、`ExtractionValidator.validate` |
| 02 | **KG 生产管线六阶段**（验证→去重冲突→建图→分析→时态→溯源）含 DANGLING_EDGE 自动修复 | `GraphValidator.validate(...).is_valid/issues/code`、`TemporalGraphQuery.query_at_time` |
| 03 | 可视化套件（弱相关） | — |
| 05 | 9 类导出器+报告 | `RDFSerializer.convert_kg_to_rdf`、`RDFValidator.validate_rdf_syntax`、`ReportGenerator` |
| 06 | **多源整合**：5 类源各带 source 键、离线降级、合并补占位端点 | `GraphBuilder(merge_entities=True, resolve_conflicts=True).build(sources=[...])`、`cg.build_from_entities_and_relationships`、`context.store(docs, extract_entities=False)`、`context.retrieve(query, use_graph=True, expand_graph=True)` |
| 08 | IF/THEN 规则推理 | `Reasoner`、`ExplanationGenerator` |
| 09 | 语义层：KG→本体→映射→RDF | `OntologyGenerator.generate_from_graph`、`RDFExporter.export(kg, "knowledge_graph.ttl", format="turtle")` |
| 10 | **时态 KG**：点事件 timestamp vs 区间 valid_from/valid_to、时点/演化查询、版本对比 | `GraphBuilder(enable_temporal=True, temporal_granularity="day")`、`TemporalGraphQuery`、`TemporalPatternDetector`、`TemporalVersionManager.create_version/compare_versions` |
| 11 | 生产级 Agent 记忆：FAISS+Neo4j、GraphRAG 配置（hops/alpha） | `AgentContext(retention_days, use_graph_expansion, max_expansion_hops, hybrid_alpha)` |
| 12 | **非结构化→本体双范式**（NLP 管线 vs LLM 管线） | `OntologyGenerator.generate_ontology({...}, name=)`、`LLMOntologyGenerator(provider="openai").generate_ontology_from_text` |
| **13** | **手工本体+显式映射（最佳实践核心）** | `AssociativeClassBuilder.create_associative_class(name, connects, temporal, properties)`、`OntologyEngine.validate/to_owl/to_shacl/export_owl/export_shacl`、`TripletStore.store(knowledge_graph, ontology)` |
| **14** | **Datalog 推理（RBAC 样板）** | `DatalogReasoner.add_fact(str 或 {source,target,type} dict)/add_rule/derive_all/query/load_from_graph/clear`、`ExplanationGenerator(detail_level)`、`dr._rules/_all_facts/_fact_index` 内省 |
| — | 向量检索进阶（间接） | `FAISSStore.create_index(index_type="hnsw", metric="L2", m=16)`、`SearchRanker(strategy="reciprocal_rank_fusion")` |
| — | snowflake_ingestion_examples.py：14 例（分页、增量水位线、key-pair、ETL） | `SnowflakeIngestor.ingest_table(table, limit, offset)`、`ingest_query(query, params=, batch_size=100)`、`get_table_schema` |

## integrations/（3 篇 Agno）

- agno_decision_intelligence：`AgentContext(decision_tracking=True).record_decision(...)`、`PolicyEngine(graph_store).check_compliance(data, rules)`、`find_precedents_advanced`
- agno_graphrag_context：`RelationExtractor(confidence_threshold=0.60)`、`GraphBuilder(merge_entities=True, temporal_support=True)`、`toolkit.add_to_graph/find_related(query, hops=2)`
- agno_multi_agent_shared_context：`AgnoSharedContext(vector_store, knowledge_graph).bind_agent(role)`、`trace_causal_chain(decision_id, depth=3)`

## B. examples 代码地图

| 路径 | 用途 | 关键 API |
|---|---|---|
| arrow_export_example.py | Arrow 列式导出+回读 | `ArrowExporter().export_entities/export_relationships/export_knowledge_graph` |
| parquet_export_example.py | Parquet 6 种压缩对比 | `ParquetExporter(compression="snappy")`、`export_knowledge_graph(kg, base_path)` |
| **capability_gap_context_graphs_example.py** | **单文件官方推荐编排样板**（全模块串联） | `OntologyEvaluator().evaluate_ontology(od, competency_questions=[...])`、`TextSplitter(method="recursive", chunk_size=1800, chunk_overlap=250).split_batch()`、`PipelineBuilder().add_step().connect_steps().build(name=)`、`NamedEntityRecognizer(method="pattern", confidence_threshold=0.2)`、`EntityResolver(strategy="fuzzy")`、`detect_conflicts([...], method="value", property_name=)`、`GraphBuilder(merge_entities=True, resolve_conflicts=True).build([...], extract=False)`、`PolicyEngine(context_graph).add_policy(policy)`、`multi_hop_query(context_graph, start_entity=, query=, max_hops=3)`、`VersionManager(base_uri=).create_version()`、`export_rdf(kg, path, format="turtle")` |
| explorer_deterministic_rendering_example.py | Explorer E2E 基线（无关） | — |
| ci/ | 三条 CI 模板 + composite action（无关） | — |

## C. 实践模式清单（27 条，含代码出处）

### 直接相关（进最佳实践）

- **C1 本体即代码**：Python dict 手写本体（类/属性/domain/range/required 显式），与代码一起版本化；schema 变化只改映射函数。原文："If Semantica inferred the ontology from your Snowflake schema, every schema migration would risk silently changing your semantic model."（advanced/13 Step 1、Best-Practice Architecture）
- **C2 显式映射层**：节点 ID 由业务键派生（`person:{EMPLOYEE_ID}`），事件 ID 含全部参与者+日期防重聘覆盖。（advanced/13 Step 4 map_rows_to_kg）
- **C3 N 元事实物化**：关联类（AssociativeClassBuilder，temporal=True 自动加 startDate/endDate）+ 快捷边双轨；SPARQL 无上下文走快捷边、要上下文走事件节点。（advanced/13 Step 2/4、SPARQL Query Patterns）
- **C4 属性/关系类型带完整 URI**：否则 TripletStore 落默认 `urn:property:<name>`，`PREFIX hr:` 查空。（advanced/13 Step 1/4 注释）
- **C5 物化节点属性过滤 None**：`{k: v for k, v in event_props.items() if v is not None}` 防字面量 "None" 入库。（advanced/13 Step 4）
- **C6 OWL+SHACL 双工件**：`engine.validate(ontology)` → `to_owl` + `to_shacl`，required 属性装载时强制。（advanced/13 Step 5）
- **C7 Competency Questions 验收前置**：`CompetencyQuestionsManager().add_question(...)` → `validate_ontology(ontology)`；同 capability_gap example L147-159。（introduction/14 Advanced Usage）
- **C8 数据驱动三件套**：`ClassInferrer(min_occurrences)`（滤噪声）+ `PropertyGenerator.infer_properties`（区分 object/data property、domain/range）+ `OntologyOptimizer(remove_redundancy=True)`。（introduction/14）
- **C9 版本管理+标准本体复用**：`VersionManager.create_version("1.0", ontology, changes=[...])`；`ReuseManager().research_ontology("http://xmlns.com/foaf/0.1/")` → imports 追加 URI。（introduction/14 Lifecycle）
- **C10 双范式建本体**：NLP（确定性、离线、受词表限制）vs LLM（概念化、非确定）；dataclass→dict 转换坑（优先 to_dict()，退化 getattr）。（advanced/12）
- **C11 span 映射建边**：`(start_char, end_char)` → graph_id，端点查映射表，查不到跳过打日志，不按位置猜。（introduction/07 Step 2）
- **C12 消解后端点重映射**：resolved 实体带 merged_from，构建 source_id→canonical_id 改写关系端点。（introduction/07 Step 3）
- **C13 去重完整集**：合并产物 + 未进 group 的孤立实体；策略 KEEP_MOST_COMPLETE。（introduction/07 Step 4、18 Section 6）
- **C14 入图前验证门禁**：`GraphValidator.validate` → DANGLING_EDGE 过滤坏边 → re-validate；种子数据 `validate_quality`。（advanced/02 Phase 1、introduction/25）
- **C15 冲突处理全家桶**：记录带 source/timestamp → SourceTracker 注册可信度（内部库>抓取>公共 API）→ detect_value_conflicts 逐字段 → voting / credibility_weighted 双策略 → InvestigationGuide 人工兜底 → ConflictAnalyzer 找系统性噪声源。（introduction/17 Step 2-6）
- **C16 审计级溯源**：证据四元组（source=DOI、source_location=Figure 2、source_quote=原句、confidence）；invalidate 存 prov:Invalidation 不删除；verify_chain 链式 SHA-256。track_relationship 端点按惯例写 metadata。（introduction/22 Step 1-6）
- **C21 种子先行**：SeedDataManager 注册可信源 → create_foundation_graph（confidence=1.0）→ 抽取结果有锚可链。（introduction/25）

### 间接相关（延伸阅读）

- C17 多源整合离线降级 + 每实体带 source 键 + 合并补占位端点（advanced/06 Phase 5）
- C18 时态建模：点事件 timestamp / 区间 valid_from-valid_to；`GraphBuilder(enable_temporal=True, temporal_granularity="day")`（advanced/10）
- C19 规则推理+审计解释：KG 关系 dict 直接 `dr.add_fact(rel)`；递归 Horn 推 RBAC；add_rule 自动去重 issue #732（advanced/14 Part 4、introduction/23）
- C20 变更管理：快照+tag+SHA-256 防篡改，改一字 verify_checksum 翻 False；SQLiteVersionStorage（introduction/24）
- C22 分批抽取+先共指后抽取+抽取器复用：`process_batch` 批量实体/三元组、关系逐条；"Cache extractors instead of recreating them"；实体只抽一次喂给关系和三元组（capability_gap L295-317、05/06）
- C23 置信度阈值前置：NER 0.7-0.8、关系 0.6-0.7；EntityConfidenceScorer 分桶定人工复核优先级（05 Step 6/9、06 Step 8）
- C24 Parquet/Arrow 导出供 pandas 生态（examples/parquet、arrow）
- C25 大表分页+增量水位线：`WHERE UPDATED_AT > %(last_load)s`（snowflake Example 6/13）
- C26 KG-aware 分块+chunk 溯源：EntityAwareChunker 不切断实体、RelationAwareChunker 保三元组；track_chunk 记来源（introduction/11）
- C27 GraphRAG 上下文：实体文本化描述批量入向量库（extract_entities=False）→ retrieve(use_graph=True, expand_graph=True)；手动 build_graph 注入业务关系（advanced/06 Phase 9、11 Section 5-6）

### 无关（不进本体文档）

纯可视化（advanced/03、introduction/16）、存储后端（09/13/20/21、Advanced_Vector_Store）、部署工具链（examples/ci、explorer）、Agno 集成三篇。

## 补充观察

1. `cookbook/use_cases/` 目录不存在，但 11_Chunking 和 capability_gap example 引用了它——文档引用路径时注意。
2. introduction 系列 = API 演示 + 章末 Best Practices；advanced/13、14 是仅有的两篇带完整「最佳实践架构」论述的教程。
