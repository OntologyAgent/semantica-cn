---
work_package_id: WP02
title: LLM 别名消解
dependencies: []
requirement_refs:
- FR-002
tracker_refs: []
planning_base_branch: feature/llm-extractor-family
merge_target_branch: feature/llm-extractor-family
branch_strategy: Planning artifacts for this mission were generated on feature/llm-extractor-family. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feature/llm-extractor-family unless the human explicitly redirects the landing branch.
subtasks:
- T004
- T005
history: []
agent_profile: python-pedro
authoritative_surface: semantica/semantic_extract/coreference_resolver.py
create_intent:
- tests/semantic_extract/test_coref_llm.py
execution_mode: code_change
owned_files:
- semantica/semantic_extract/coreference_resolver.py
- tests/semantic_extract/test_coref_llm.py
role: implementer
tags: []
agent: "python-pedro"
shell_pid: "79740"
---

# WP02 — LLM 别名消解

## Purpose

CoreferenceResolver 新增 `resolve_aliases_llm(text, provider="openai", llm_model=None, api_key=None, min_confidence=0.85, prompt=None, **options)`。

## 实现要点（research R3 notebook 参考实现）

1. 默认中文指令：识别简称/别名/指代 → 规范全称（甲方乙方→公司名、公司简称→全称、政策简称→全称；不输出地点/日期/数字/规格），输出 `{"mappings":[{"alias","canonical","confidence"}]}`
2. `prompt` 参数整体替换默认指令（与 WP01 同语义）
3. 安全替换：按 alias 长度降序；`(?<![\u4e00-\u9fff])alias(?![\u4e00-\u9fff])` 独立出现判定；confidence<min_confidence 或 alias==canonical 或 len(alias)<2 → skipped 带原因
4. provider 经 create_provider + generate_structured；失败语义与既有 provider 一致
5. 返回 {resolved_text, mappings, skipped}（data-model Entity 2）

## 验收

```bash
uv run --frozen pytest tests/semantic_extract/test_coref_llm.py -q
```

## Activity Log

- 2026-10-02T04:05:30Z – python-pedro – shell_pid=79740 – Assigned agent via action command
- 2026-10-02T04:17:06Z – python-pedro – shell_pid=79740 – 7/7 green; protection semantics superior to notebook rule
