---
work_package_id: WP01
title: prompt 入口贯穿三链路
dependencies: []
requirement_refs:
- FR-001
- FR-003
- FR-004
- FR-005
- FR-006
tracker_refs: []
planning_base_branch: feature/llm-extractor-family
merge_target_branch: feature/llm-extractor-family
branch_strategy: Planning artifacts for this mission were generated on feature/llm-extractor-family. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feature/llm-extractor-family unless the human explicitly redirects the landing branch.
subtasks:
- T001
- T002
- T003
history: []
agent_profile: python-pedro
authoritative_surface: semantica/semantic_extract/methods.py
create_intent:
- tests/semantic_extract/test_prompt_entry.py
execution_mode: code_change
owned_files:
- semantica/semantic_extract/methods.py
- semantica/semantic_extract/ner_extractor.py
- semantica/semantic_extract/relation_extractor.py
- semantica/semantic_extract/triplet_extractor.py
- tests/semantic_extract/test_prompt_entry.py
role: implementer
tags: []
agent: "python-pedro"
shell_pid: "79740"
---

# WP01 — prompt 入口贯穿三链路

## Purpose

`prompt` 参数（str，整体替换默认指令体）从 NER/Relation/Triplet 构造器直达 LLM 调用点；EventDetector 经组合自动受益。

## 实现要点

1. methods.py 四个提示词点（research R1 行号）：函数签名加 `prompt: Optional[str] = None`；非空时 `prompt = <用户 prompt> + "\n\n" + <守卫尾>`，守卫尾 = 一行「Only output JSON matching the required structure.」类提示（与各 schema 对应）；原文注入段保持既有结构
2. 缓存：cache_params 增加 `"prompt": prompt`
3. 三个 extractor llm 分支：`method_options["prompt"] = all_options.get("prompt")`
4. 未传 prompt：所有路径 byte-identical（先跑既有测试确认基线）

## 验收

```bash
uv run --frozen pytest tests/semantic_extract/ -q      # 既有+新增全绿
```

## Activity Log

- 2026-10-02T04:05:23Z – python-pedro – shell_pid=79740 – Assigned agent via action command
- 2026-10-02T04:14:56Z – python-pedro – shell_pid=79740 – 10/10 green + 373 existing unchanged
