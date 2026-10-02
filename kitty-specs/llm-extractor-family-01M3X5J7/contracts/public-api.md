# Contract: prompt 入口与 LLM 别名消解

**Mission**: llm-extractor-family-01M3X5J7

## prompt 参数（三类抽取器统一）

```python
from semantica.semantic_extract import NERExtractor, RelationExtractor, TripletExtractor

prompt = """你是医药商业政策解析器。只抽取：甲方/乙方公司全称、政策名称、产品通用名。
例子：输入「华跃控股北京有限公司（以下简称"华跃北京"）」→ 抽「华跃控股北京有限公司」（ORG）。
输出要求：宁缺毋滥，confidence 低于 0.7 的不要。"""

ner = NERExtractor(method="llm_prompt", provider="deepseek", llm_model="deepseek-flash",
                   api_key=..., prompt=prompt)
entities = ner.extract(text)                      # 指令体被整体替换
rel  = RelationExtractor(method="llm_prompt", provider="deepseek", api_key=..., prompt=...)
trip = TripletExtractor(method="llm_prompt", provider="deepseek", api_key=..., prompt=...)
```

**语义**:
- `prompt=None`（缺省）：退回官方默认（与现状完全一致）
- 非空：替换默认指令体（含 entity_types 条件段不再生效——类型约束改由提示词表达）；原文注入与 schema 守卫尾由扩展附加；**不共享上游结果缓存**（其键不含 prompt），重复调用重打 LLM
- 实现为零侵入扩展（method_registry 注册 "llm_prompt"），上游源码零改动
- EventDetector 经 NER/Relation 组合自动获得同能力

## resolve_aliases_llm（CoreferenceResolver 新方法）

```python
from semantica.semantic_extract import resolve_aliases_llm

result = resolve_aliases_llm(
    text, provider="deepseek", llm_model="deepseek-flash", api_key=...,
    min_confidence=0.85, prompt=None,   # prompt 可整体替换默认映射指令
)
result["resolved_text"]; result["mappings"]; result["skipped"]
```

**安全语义**: 独立出现判定防子串误替换；映射按 alias 长度降序应用；门槛外的进 skipped 并带原因。
