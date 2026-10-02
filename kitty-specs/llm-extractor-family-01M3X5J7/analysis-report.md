---
schema_version: 1
artifact_type: spec-kitty.analysis-report
command: /spec-kitty.analyze
mission_slug: llm-extractor-family-01M3X5J7
mission_id: 01M3X5J7RPB6JQG1Q86235NGNH
generated_at: '2026-10-02T12:05:15.182223+08:00'
analyzer_agent: python-pedro
input_artifacts:
  spec.md:
    path: kitty-specs/llm-extractor-family-01M3X5J7/spec.md
    sha256: e95fce1323e8d11ddce9d6d25376eb059a86ec2724c366c1f4de3c3547b55459
  plan.md:
    path: kitty-specs/llm-extractor-family-01M3X5J7/plan.md
    sha256: 773151352d123d2f66e34f1bf6ea8281a921a89f675e8958182bbc65e4d35243
  tasks.md:
    path: kitty-specs/llm-extractor-family-01M3X5J7/tasks.md
    sha256: 223947987ee0139550f9003e155eeff2b4a57aba42902c0f35a9a4a7438799e6
  charter:
    path: .kittify/charter/charter.md
    sha256: a5e01a009b82bb321c397f1f4d566511a1a4713370ab47480516eb838cffce67
verdict: ready
issue_counts:
  medium: 0
  low: 1
---

# Analysis Report: llm-extractor-family 实现前分析

**Mission**: llm-extractor-family-01M3X5J7 | **Date**: 2026-10-02 | **Analyst**: python-pedro（宿主执行）

## A1: 代码事实核实

1. **提示词构造点**（methods.py）：:1352 实体、:2122 关系、:2145 关系 temporal 分支、:2803 三元组——构造模式一致（指令体 f-string + 原文注入 → generate_typed(schema)），prompt 注入点明确
2. **透传断点**：ner_extractor.py:701 / relation_extractor.py:406 / triplet_extractor.py:456 的 llm 分支仅挑 provider/model/api_key——prompt 需显式加入 method_options
3. **EventDetector**（event_detector.py:88）默认 method="llm"，事件由 NER+Relation 组合派生——无独立提示词点，prompt 打通后自动受益（T003 用组合断言验证）
4. **缓存**：extract_*_llm 走 _result_cache.get(..., **cache_params)——prompt 必须进 cache_params，否则同文本不同 prompt 串缓存（关键正确性风险）
5. **CoreferenceResolver**：method 传底层 NER；自身 resolve_pronouns 为规则。resolve_aliases_llm 为全新方法，无既有行为回改面

## A2: 现有测试基线

tests/semantic_extract/ 现有用例（含 retry/pool/batch）构成回归保护；实现前全量跑一遍确认起点（上次门禁已绿）。LLM 相关既有测试全部 mock provider——新增测试沿用同模式，不打真实 API。

## A3: 冲突排查

- llm_extraction.py 的 enhance_* 是另一套「增强」路径（对已抽取结果加工），与 prompt 入口正交，不动
- providers.py 的 generate_typed/generate_structured 无需改动
- notebook 参考实现中的 API key 不入库（测试全 mock）

## A4: 验证策略

- WP01/WP02 mock provider：断言收到的 prompt 含用户指令 + 守卫尾；缓存键区分；默认路径 byte-identical
- 收口 run_gate.sh（基线 51 外零新增）

## 结论

ready，无阻塞。一处低危：守卫尾与用户 prompt 输出要求可能重复（无害，schema 兜底）。
