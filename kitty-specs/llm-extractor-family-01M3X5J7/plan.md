# Implementation Plan: LLM 抽取器家族（提示词入口）

**Branch**: `feature/llm-extractor-family` | **Date**: 2026-10-02 | **Spec**: [spec.md](./spec.md)
**Input**: kitty-specs/llm-extractor-family-01M3X5J7/spec.md（2026-10-02 澄清版：只留提示词入口）

## Summary

五类 LLM 抽取能力统一接受一个 `prompt` 参数：整体替换默认提示词指令体，抽取目的/方法/例子/主题方向/输出要求全由用户提示词承载；框架保留 schema 守卫尾与原文注入，输出解析路径不变。另为 CoreferenceResolver 增加 LLM 别名消解方法（notebook 参考实现），并补 MinerU 4.0.10 文档说明。

## Technical Context

**Language/Version**: Python 3.10–3.13（仓库 requires-python；零新依赖）
**Primary Dependencies**: 既有 `semantica/semantic_extract/`（providers.py 的 create_provider / generate_typed / generate_structured）
**Storage**: N/A
**Testing**: pytest；LLM 全 mock（fake provider 注入），不打真实 API；夜间门禁基线 51 外零新增
**Target Platform**: 跨平台
**Project Type**: single
**Performance Goals**: 无新增性能面（纯参数传递）
**Constraints**: 不改任何既有公共签名（prompt 为新增可选参数）；默认行为 byte-identical（未传 prompt 时）
**Scale/Scope**: methods.py 4 个提示词构造点 + 3 个 extractor 透传分支 + coref 新方法 + 2 个文档文件；测试约 30 个

## Charter Check

- 只用项目声明技术（标准库 + 既有 provider 层）✅
- 变更可预测：纯新增参数与新方法，默认行为零改动 ✅
- 质量门：run_gate.sh 基线比对 ✅

## Project Structure

```
semantica/semantic_extract/
├── methods.py                  # 扩展：extract_entities_llm / extract_relations_llm(×2 分支) / extract_triplets_llm 接受 prompt
├── ner_extractor.py            # 扩展：llm 分支透传 prompt（:701 附近）
├── relation_extractor.py       # 扩展：llm 分支透传 prompt（:406 附近）
├── triplet_extractor.py        # 扩展：llm 分支透传 prompt（:456 附近）
└── coreference_resolver.py     # 新增：resolve_aliases_llm（LLM 别名→规范名映射 + 安全替换）

tests/semantic_extract/
├── test_prompt_entry.py        # 新增：prompt 注入与透传（mock provider）
└── test_coref_llm.py           # 新增：LLM 别名消解（mock provider）

docs_zh/integrations/mineru.md  # 补 MinerU 4.0.10 支持说明
README.zh-CN.md                 # 同上（一段话）
```

**Structure Decision**: 全部落在既有模块内，单项目结构。

## Complexity Tracking

无 charter 违规。

## Implementation Concern Map

### IC-01 — prompt 参数语义与注入点
- **Purpose**: 定义 prompt 的替换边界（指令体整体替换、schema 守卫尾自动附加、原文注入不变）与缓存键纳入
- **Relevant requirements**: FR-001、FR-003、FR-004、FR-005（经 NER/Relation 组合受益）、FR-006
- **Affected surfaces**: methods.py、三个 extractor 的 llm 分支
- **Sequencing/depends-on**: none
- **Risks**: 用户 prompt 覆盖输出格式约束导致解析失败——守卫尾兜底；缓存键漏纳 prompt 会串结果

### IC-02 — LLM 别名消解（coref）
- **Purpose**: CoreferenceResolver 增加 resolve_aliases_llm：LLM 产出 alias→canonical 映射，安全替换（min_conf、独立出现判定防子串误伤）
- **Relevant requirements**: FR-002
- **Affected surfaces**: coreference_resolver.py
- **Sequencing/depends-on**: none
- **Risks**: 子串误替换（notebook 已有解法：前后非汉字 + 长度排序）；映射幻觉（min_conf 门槛 + 只替换文中实际出现者）

### IC-03 — 文档与收口
- **Purpose**: MinerU 4.0.10 说明 + 门禁 + quickstart 走查
- **Relevant requirements**: FR-007
- **Affected surfaces**: docs_zh/integrations/mineru.md、README.zh-CN.md
- **Sequencing/depends-on**: IC-01、IC-02
- **Risks**: 无
