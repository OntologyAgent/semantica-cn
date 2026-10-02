# Research: LLM 抽取器家族（提示词入口）

**Mission**: llm-extractor-family-01M3X5J7 | **Date**: 2026-10-02

## R1: 提示词构造点（methods.py，代码事实）

| 位置 | 函数 | 分支 |
|------|------|------|
| :1352 | extract_entities_llm | 默认 |
| :2122 | extract_relations_llm | 默认 |
| :2145 | extract_relations_llm | temporal（带时间有效性） |
| :2803 | extract_triplets_llm | 默认 |

构造模式：`prompt = f"""<指令体（含 entity_types 等条件段）>"""` + 原文注入 → `llm.generate_typed(prompt, schema=XxxResponse)`。

## R2: 透传断点（extractor 类 → method 函数只挑三个 key）

- ner_extractor.py :701 `method_name == "llm"` 分支：只透传 provider/model/api_key
- relation_extractor.py :406 同款
- triplet_extractor.py :456 同款
- EventDetector（event_detector.py :88）默认 method="llm"，事件由 NER+Relation 组合派生 → prompt 入口打通后自动受益，无独立提示词点
- CoreferenceResolver :95 method 传给底层 NER；自身别名/代词逻辑为规则

## R3: 用户 notebook 参考实现（~/Downloads/main.md，2026-10-02 提供）

- 指代消解：DeepSeek generate_structured → {"mappings":[{alias,canonical,confidence}]} → 安全替换：按 alias 长度降序、confidence≥0.85、alias 与 canonical 非空且不等、`(?<!CJK)alias(?!CJK)` 独立出现判定（防「北京」误伤「华跃控股北京有限公司」）
- 中文事件检测：整段中文指令 + JSON 输出 → generate_structured
- 结论：两者本质都是「用户提示词替换默认指令」——正是本 mission 的统一入口；notebook 中的 API key 不得入库

## R4: provider 层事实

- create_provider(provider, model, **kwargs) → llm.generate_typed(prompt, schema) / generate_structured(prompt)
- 输出经 pydantic schema 校验（EntitiesResponse 等）→ 守卫天然存在；prompt 全替换后解析仍由 schema 兜底
- 缓存：_result_cache.get("entities", text, **cache_params) —— prompt 必须纳入 cache_params（R2 IC-01 风险）
