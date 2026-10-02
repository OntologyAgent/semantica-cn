# Tasks: LLM 抽取器家族（提示词入口）

**Mission**: llm-extractor-family-01M3X5J7
**Branch**: feature/llm-extractor-family
**Generated**: 2026-10-02

## Subtask Index

| ID | Description | WP | Parallel | Status |
|----|-------------|----|----------|--------|
| T001 | methods.py：extract_entities_llm / extract_relations_llm（默认+temporal）/ extract_triplets_llm 接受 prompt——指令体整体替换 + schema 守卫尾自动附加 + prompt 纳入缓存键 | WP01 |  | pending |
| T002 | 三个 extractor 类 llm 分支透传 prompt（ner:701 / relation:406 / triplet:456） | WP01 |  | pending |
| T003 | test_prompt_entry.py：mock provider 断言（prompt 到达 LLM、守卫尾存在、缓存键区分、未传时默认提示词不变、Entity/Relation/Triplet 三链路 + EventDetector 组合） | WP01 |  | pending |
| T004 | CoreferenceResolver.resolve_aliases_llm：默认中文映射指令 + generate_structured + 安全替换（长度降序/独立出现/门槛）+ prompt 可替换指令 | WP02 | [P] | pending |
| T005 | test_coref_llm.py：mock 映射替换正确性、子串误伤防护（北京 案例）、min_conf 拒绝、无映射返回原文、prompt 替换到达 | WP02 | [P] | pending |
| T006 | MinerU 4.0.10 支持说明：docs_zh/integrations/mineru.md 增补 + README.zh-CN 一段话 | WP03 |  | pending |
| T007 | 全量门禁 run_gate.sh（基线 51 外零新增）+ quickstart §3 走查 | WP03 |  | pending |

## WP01 — prompt 入口贯穿三链路

**Prompt**: `tasks/WP01-prompt-entry.md`
**Goal**: prompt 参数从 extractor 构造一路到 LLM 调用点；默认行为零变化
**Priority**: P0（串行第一棒）
**Independent test**: `uv run --frozen pytest tests/semantic_extract/test_prompt_entry.py -q` 全绿
**Estimated prompt size**: ~140 lines

- [x] T001 methods.py 四个提示词点 (WP01)
- [x] T002 三个 extractor 透传 (WP01)
- [x] T003 mock 测试 (WP01)

**Dependencies**: none
**Risks**: 缓存键漏纳 prompt；守卫尾与用户 prompt 的输出要求冲突

## WP02 — LLM 别名消解

**Prompt**: `tasks/WP02-coref-llm.md`
**Goal**: CoreferenceResolver.resolve_aliases_llm 按 notebook 参考实现落地
**Priority**: P1（与 WP01 可并行）
**Independent test**: `uv run --frozen pytest tests/semantic_extract/test_coref_llm.py -q` 全绿
**Estimated prompt size**: ~130 lines

- [ ] T004 resolve_aliases_llm 实现 (WP02)
- [ ] T005 mock 测试 (WP02)

**Dependencies**: none（独立于 WP01）
**Risks**: 子串误替换（独立出现判定兜底）；幻觉映射（门槛+skipped 记录）

## WP03 — 文档与收口

**Prompt**: `tasks/WP03-docs-gate.md`
**Goal**: MinerU 说明 + 门禁收口
**Priority**: P1（依赖 WP01+WP02）
**Independent test**: `bash tools/nightly/run_gate.sh` exit 0
**Estimated prompt size**: ~80 lines

- [ ] T006 MinerU 4.0.10 文档 (WP03)
- [ ] T007 门禁 + quickstart 走查 (WP03)

**Dependencies**: WP01、WP02
**Risks**: 无

---

**spec 覆盖**：FR-001 → WP01（T001 入口语义）；FR-003/FR-004/FR-006 → WP01（T002 透传即达）；FR-005 → WP01（EventDetector 组合派生，T003 含组合断言）；FR-002 → WP02；FR-007 → WP03。
