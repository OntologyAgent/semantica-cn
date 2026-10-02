"""
Prompt-Driven LLM Extraction（fork 扩展，零侵入上游）

semantica-cn 的提示词入口扩展：不改上游任何存量代码，通过官方
``method_registry`` 扩展点注册新方法 ``"llm_prompt"``，并以 provider
包装的方式把自定义提示词注入 LLM 调用。

用法（与官方抽取器同构，仅 method 换名）：

    >>> from semantica.semantic_extract import NERExtractor
    >>> ner = NERExtractor(method="llm_prompt", provider="deepseek",
    ...                    llm_model="deepseek-flash", api_key=KEY,
    ...                    prompt="只抽取医药政策里的公司全称，宁缺毋滥")
    >>> entities = ner.extract(text)

别名消解（抽取前的指代归并）：

    >>> from semantica.semantic_extract.prompt_extraction import resolve_aliases_llm
    >>> result = resolve_aliases_llm(text, provider="deepseek", api_key=KEY)

设计约束（fork 约定）：
    - 不修改上游文件；全部能力在本模块与注册表扩展点内实现
    - 委托上游 ``extract_*_llm`` 时旁路其结果缓存——上游缓存键不含
      prompt，复用会串结果；本模块因此也不做缓存（重复调用会重打 LLM）
    - 输出仍经上游 generate_typed 的 schema 校验与解析路径

Author: semantica-cn Contributors
License: MIT
"""

import os
from typing import Any, Dict, List, Optional

from . import methods as _methods
from .registry import method_registry

__all__ = [
    "extract_entities_llm_prompt",
    "extract_relations_llm_prompt",
    "extract_triplets_llm_prompt",
    "resolve_aliases_llm",
]

# 与上游默认提示词一致的输出守卫（schema 提示行），追加在用户提示词之后。
_GUARDS = {
    "entities": 'Return ONLY a JSON object with an "entities" key: a flat list of entities, each with "text", "label" and "confidence".',
    "relations": 'Return ONLY a JSON object with a "relations" key: a list of relations, each with "subject", "predicate", "object" and optional "confidence".',
    "triplets": 'Return ONLY a JSON object with a "triplets" key: a list of triplets, each with "subject", "predicate", "object" and optional "confidence".',
}


class _NullResultCache:
    """委托期间的空缓存：get 永远未命中，set 丢弃。

    上游缓存键不含 prompt；同文本不同提示词会串结果，故旁路。
    """

    def get(self, *args, **kwargs):
        return None

    def set(self, *args, **kwargs):
        return None


class _PromptOverrideLLM:
    """包装 LLM provider：把上游构造的默认提示词整体替换为用户提示词。"""

    def __init__(self, base_llm, prompt: str):
        self._base = base_llm
        self._prompt = prompt

    def __getattr__(self, name):
        return getattr(self._base, name)

    def generate_typed(self, prompt, *args, **kwargs):
        return self._base.generate_typed(self._prompt, *args, **kwargs)

    def generate_structured(self, prompt, *args, **kwargs):
        return self._base.generate_structured(self._prompt, *args, **kwargs)


def _compose_prompt(custom_prompt: str, guard: str, text: str,
                    entities: Optional[List[Any]] = None) -> str:
    parts = [custom_prompt.strip(), guard, "Text to extract from:", text]
    if entities:
        parts.append("Entities found in text: " + str(list(entities)))
    return "\n\n".join(parts)


def _delegate_with_prompt(upstream_fn, text, kwargs, guard, entities=None):
    """在 provider 与缓存两个接缝上做作用域包装，然后委托上游函数。"""
    custom_prompt = kwargs.pop("prompt", None)
    if not custom_prompt:
        return upstream_fn(text, **kwargs)

    composed = _compose_prompt(custom_prompt, guard, text, entities)
    original_create = _methods.create_provider
    original_cache = _methods._result_cache

    def _patched_create(provider, **provider_kwargs):
        provider_kwargs.pop("prompt", None)
        return _PromptOverrideLLM(original_create(provider, **provider_kwargs), composed)

    _methods.create_provider = _patched_create
    _methods._result_cache = _NullResultCache()
    try:
        if entities is None:
            return upstream_fn(text, **kwargs)
        return upstream_fn(text, entities=entities, **kwargs)
    finally:
        _methods.create_provider = original_create
        _methods._result_cache = original_cache


def extract_entities_llm_prompt(text: str, **kwargs):
    """LLM 实体抽取，``prompt`` 整体替换默认指令体。其余参数同上游。"""
    return _delegate_with_prompt(
        _methods.extract_entities_llm, text, kwargs, _GUARDS["entities"])


def extract_relations_llm_prompt(text: str, entities=None, **kwargs):
    """LLM 关系抽取，``prompt`` 整体替换默认指令体。其余参数同上游。"""
    if entities is None:
        entities = []
    return _delegate_with_prompt(
        _methods.extract_relations_llm, text, kwargs,
        _GUARDS["relations"], entities=entities)


def extract_triplets_llm_prompt(text: str, **kwargs):
    """LLM 三元组抽取，``prompt`` 整体替换默认指令体。其余参数同上游。"""
    return _delegate_with_prompt(
        _methods.extract_triplets_llm, text, kwargs, _GUARDS["triplets"])


# -- 别名消解（LLM 指代归并） ----------------------------------------------

_DEFAULT_ALIAS_PROMPT = """找出下面文本里的「简称/别名/指代」及其规范全称。

只关注这几类：
- 甲方/乙方 -> 具体公司名
- 公司简称 -> 公司全称（如 岭川 -> 杭州岭川制药有限公司）
- 政策简称 -> 政策全称

不要输出：地点（北京/杭州/中国）、日期、数字、产品规格。

只输出 JSON：{"mappings": [{"alias": "岭川", "canonical": "杭州岭川制药有限公司", "confidence": 0.9}]}

原文：
"""


def resolve_aliases_llm(
    text: str,
    provider: str = "openai",
    llm_model=None,
    api_key=None,
    min_confidence: float = 0.85,
    prompt=None,
    **options,
) -> Dict[str, Any]:
    """LLM 别名消解：识别简称/别名/指代 → 规范全称，并安全替换。

    规范名区间保护：alias 出现位置落在任一 canonical 内部时跳过该次出现
    （防「北京」误伤「华跃控股北京有限公司」，同时不拦「岭川与…」类正常
    替换）；confidence 低于 min_confidence、alias==canonical 或
    len(alias)<2 的映射跳过并记入 skipped。

    Returns:
        {"resolved_text": str, "mappings": [...], "skipped": [...]}
    """
    from .providers import create_provider

    instruction = (prompt + "\n\n原文：\n" + text) if prompt else (_DEFAULT_ALIAS_PROMPT + text)

    provider_kwargs = dict(options)
    if api_key:
        provider_kwargs["api_key"] = api_key
    elif not provider_kwargs.get("api_key"):
        env_key = os.getenv(f"{provider.upper()}_API_KEY")
        if env_key:
            provider_kwargs["api_key"] = env_key
    if llm_model:
        provider_kwargs["model"] = llm_model

    llm = create_provider(provider, **provider_kwargs)
    data = llm.generate_structured(instruction)
    raw = data.get("mappings", []) if isinstance(data, dict) else []

    canonicals = sorted(
        {str(m.get("canonical", "")).strip() for m in raw if m.get("canonical")},
        key=len, reverse=True,
    )

    def _protected_spans(haystack):
        spans = []
        for name in canonicals:
            if not name:
                continue
            start = haystack.find(name)
            while start != -1:
                spans.append((start, start + len(name)))
                start = haystack.find(name, start + 1)
        return spans

    applied, skipped = [], []
    result = text
    for m in sorted(raw, key=lambda x: -len(str(x.get("alias", "")))):
        alias = str(m.get("alias", "")).strip()
        canonical = str(m.get("canonical", "")).strip()
        try:
            conf = float(m.get("confidence", 0) or 0)
        except (TypeError, ValueError):
            conf = 0.0
        if conf < min_confidence:
            skipped.append({"mapping": m, "reason": f"confidence {conf} < {min_confidence}"})
            continue
        if not alias or not canonical or alias == canonical or len(alias) < 2:
            skipped.append({"mapping": m, "reason": "empty/self/short alias"})
            continue
        if alias not in result:
            skipped.append({"mapping": m, "reason": "alias not present in text"})
            continue
        protected = _protected_spans(result)
        pieces, cursor, replaced_any = [], 0, False
        start = result.find(alias)
        while start != -1:
            end = start + len(alias)
            inside = any(ps < start and end < pe for ps, pe in protected)
            if not inside:
                pieces.append(result[cursor:start])
                pieces.append(canonical)
                cursor = end
                replaced_any = True
            start = result.find(alias, end)
        pieces.append(result[cursor:])
        if replaced_any:
            result = "".join(pieces)
            applied.append({"alias": alias, "canonical": canonical, "confidence": conf})
        else:
            skipped.append({"mapping": m, "reason": "only protected occurrences"})

    return {"resolved_text": result, "mappings": applied, "skipped": skipped}


# -- 注册扩展方法（registry 官方扩展点；get_*_method 优先查 registry） ------
for _kind, _fn in (
    ("entity", extract_entities_llm_prompt),
    ("relation", extract_relations_llm_prompt),
    ("triplet", extract_triplets_llm_prompt),
):
    if "llm_prompt" not in (method_registry.list_all(_kind).get(_kind) or []):
        method_registry.register(_kind, "llm_prompt", _fn)