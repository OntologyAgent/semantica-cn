---
title: 提示词驱动的抽取
description: 一个 prompt 参数控制五类 LLM 抽取——目的、方法、例子、输出要求全由提示词承载。
source: guides/prompt-driven-extraction.md
source_version: 6430bda76ee40df375e07427c56c2b3d31b97dc5
icon: "sparkles"
---

# 提示词驱动的抽取（fork 增强）

> 本页是 **semantica-cn fork 原生能力**：所有 LLM 抽取器接受一个 `prompt` 参数，整体替换默认提示词。抽取目的、方法、few-shot 例子、主题方向、类型约束、输出要求——全部写在你的提示词里，框架不拆分、不额外建模。

## 三链路统一入口

```python
from semantica.semantic_extract import NERExtractor, RelationExtractor, TripletExtractor

prompt = """你是医药商业政策解析器。只抽取：
- 甲方/乙方公司全称（ORG）
- 政策编号与政策名称（POLICY）

例子：「华跃控股北京有限公司（以下简称"华跃北京"）」→ 抽「华跃控股北京有限公司」

输出要求：宁缺毋滥，confidence 低于 0.7 的不要。"""

common = dict(method="llm_prompt", provider="deepseek", llm_model="deepseek-flash",
              api_key=KEY, prompt=prompt)   # method 换名即启用，官方 "llm" 行为零变化

ner  = NERExtractor(**common)
rel  = RelationExtractor(**common)
trip = TripletExtractor(**common)

entities    = ner.extract(text)
relations   = rel.extract_relations(text, entities)
triplets    = trip.extract(text, entities=entities, relations=relations)
```

> **零侵入设计**：本能力是 fork 扩展模块（`semantica/semantic_extract/prompt_extraction.py`），
> 通过官方 `method_registry` 注册新方法名 `"llm_prompt"` 实现——上游 `extract_*_llm`、
> 三个 Extractor 类与 `CoreferenceResolver` 源码零改动。代价：prompt 模式不共享上游
> 结果缓存（上游缓存键不含 prompt，复用会串结果），重复调用会重打 LLM。

**语义**：

- `prompt=None`（缺省）＝退回官方默认行为，**零变化**
- 非空时替换默认指令体；框架自动附加两样东西——schema 守卫尾（一行输出结构提示）与原文注入。输出仍走 pydantic schema 校验，解析失败路径与默认一致
- 相同文本不同 prompt **不共享缓存**
- `EventDetector` 由 NER/Relation 组合派生，prompt 经底层链路自动生效

## 别名消解（抽取前的指代归并）

中文政策文本里「岭川」「华跃北京」这类简称会让抽取和建图碎片化。`resolve_aliases_llm` 在抽取前把别名归并成规范全称：

```python
from semantica.semantic_extract import resolve_aliases_llm

result = resolve_aliases_llm(
    text, provider="deepseek", api_key=KEY,
    min_confidence=0.85,          # 映射置信度门槛，防幻觉
    # prompt=...,                 # 可整体替换默认映射指令
)
resolved_text = result["resolved_text"]
result["mappings"]   # [{"alias": "岭川", "canonical": "杭州岭川制药有限公司", ...}]
result["skipped"]    # 被门槛拒掉的映射与原因
```

**子串保护**：alias 出现位置落在任一规范名内部时跳过该次出现——「北京」不会误替换进「华跃控股北京有限公司」，而「岭川与…」这类独立出现正常替换。

## 推荐流水线

```python
# 1. 规范化（NFKC + 删 CJK 噪声空格）      见「中文规范化」参考页
# 2. 别名消解                                resolve_aliases_llm
# 3. 提示词驱动的抽取                        prompt=...
# 4. 建图                                    GraphBuilder
from semantica.kg import GraphBuilder

graph = GraphBuilder(merge_entities=True).build(
    {"entities": entities, "relationships": relations})
```

## 相关链接

- Cookbook：Cookbook 示例：cookbook_zh/introduction/16_Prompt_Driven_Extraction.ipynb
- 参考页：[中文规范化](../reference/zh-normalization.md)
- 上游抽取参考：[Semantic Extraction](../reference/semantic_extract.md)
