# Data Model: LLM 抽取器家族（提示词入口）

**Mission**: llm-extractor-family-01M3X5J7 | **Date**: 2026-10-02

## Entity 1: prompt 参数（贯穿契约）

**表示**: `prompt: Optional[str]`，extractor 构造参数与 `extract_*_llm` 关键字参数

| 字段 | 类型 | 约束 |
|------|------|------|
| prompt | str \| None | None=默认提示词（行为与现状 byte-identical）；非空=整体替换指令体 |

**不变量**:
- 替换仅覆盖指令体；原文注入段与 schema 守卫尾（一行 JSON 结构提示）由框架自动附加
- prompt 纳入结果缓存键；同文本不同 prompt 不得串缓存
- 输出仍经 generate_typed 的 schema 校验，解析失败路径与现状一致

## Entity 2: 别名消解映射（CoreferenceMapping）

**表示**: `CoreferenceResolver.resolve_aliases_llm(text, ...) -> dict`

| 字段 | 类型 | 约束 |
|------|------|------|
| resolved_text | str | 安全替换后的文本；无可用映射时等于原文 |
| mappings | list[dict] | 每项 {alias, canonical, confidence}；仅含实际应用于替换者 |
| skipped | list[dict] | 被门槛拒掉的映射（含原因） |

**不变量**:
- 只替换独立出现的 alias（前后非 CJK 汉字），按 alias 长度降序执行
- confidence < min_confidence（默认 0.85）、alias==canonical、alias 长度 <2 一律跳过
- LLM 调用失败 → 抛异常路径与既有 provider 语义一致，不静默返回半成品
