"""prompt 入口测试（fork 扩展：method="llm_prompt"，零侵入上游）。

mock create_provider，断言：自定义 prompt 到达 LLM 且带守卫尾与原文注入；
上游默认路径不受影响；缓存旁路（不同 prompt 不串结果）且事后恢复；
三链路 + EventDetector 组合；上游源码零改动守卫（开闭原则）。
"""

import sys
import subprocess
import unittest
import uuid
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from semantica.semantic_extract import methods
from semantica.semantic_extract.methods import (
    extract_entities_llm,
)
from semantica.semantic_extract.prompt_extraction import (
    extract_entities_llm_prompt,
    extract_relations_llm_prompt,
    extract_triplets_llm_prompt,
)

CUSTOM = "你是医药政策解析器。只抽取公司全称与政策编号，宁缺毋滥。"
TEXT = "华跃控股北京有限公司与杭州岭川制药有限公司签订2025年商业政策。"
REPO = str(Path(__file__).resolve().parents[2])


def _real_entities():
    from semantica.semantic_extract.types import Entity

    return [Entity(text="华跃控股北京有限公司", label="ORG", start_char=0, end_char=11, confidence=0.9)]


def _entity_response():
    from semantica.semantic_extract.schemas import EntitiesResponse, EntityOut

    return EntitiesResponse(entities=[
        EntityOut(text="华跃控股北京有限公司", label="ORG", confidence=0.9),
    ])


def _relation_response():
    from semantica.semantic_extract.schemas import RelationOut, RelationsResponse

    return RelationsResponse(relations=[
        RelationOut(subject="华跃控股北京有限公司", predicate="signs",
                    object="2025年商业政策", confidence=0.9),
    ])


def _triplet_response():
    from semantica.semantic_extract.schemas import TripletOut, TripletsResponse

    return TripletsResponse(triplets=[
        TripletOut(subject="华跃控股北京有限公司", predicate="is_a", object="公司", confidence=0.9),
    ])


class TestPromptReachesProvider(unittest.TestCase):
    def test_entities_custom_prompt(self):
        provider = MagicMock()
        provider.generate_typed.return_value = _entity_response()
        with patch("semantica.semantic_extract.methods.create_provider", return_value=provider):
            extract_entities_llm_prompt(TEXT + str(uuid.uuid4()), provider="openai",
                                        api_key="k", prompt=CUSTOM)
        sent = provider.generate_typed.call_args[0][0]
        self.assertIn(CUSTOM, sent)
        self.assertIn('"entities"', sent)                  # 守卫尾
        self.assertIn(TEXT, sent)                           # 原文注入
        self.assertNotIn("Extract named entities", sent)    # 默认指令被整体替换

    def test_relations_custom_prompt(self):
        provider = MagicMock()
        provider.generate_typed.return_value = _relation_response()
        with patch("semantica.semantic_extract.methods.create_provider", return_value=provider):
            extract_relations_llm_prompt(TEXT + str(uuid.uuid4()), entities=_real_entities(),
                                          provider="openai", api_key="k", prompt=CUSTOM)
        sent = provider.generate_typed.call_args[0][0]
        self.assertIn(CUSTOM, sent)
        self.assertIn('"relations"', sent)
        self.assertNotIn("Extract relations between entities", sent)

    def test_triplets_custom_prompt(self):
        provider = MagicMock()
        provider.generate_typed.return_value = _triplet_response()
        with patch("semantica.semantic_extract.methods.create_provider", return_value=provider):
            extract_triplets_llm_prompt(TEXT + str(uuid.uuid4()), provider="openai",
                                         api_key="k", prompt=CUSTOM)
        sent = provider.generate_typed.call_args[0][0]
        self.assertIn(CUSTOM, sent)
        self.assertIn('"triplets"', sent)
        self.assertNotIn("Extract RDF triplets", sent)


class TestUpstreamUntouched(unittest.TestCase):
    def test_default_llm_method_unchanged(self):
        """method='llm'（上游原生）行为与上游完全一致（默认提示词）。"""
        provider = MagicMock()
        provider.generate_typed.return_value = _entity_response()
        unique = TEXT + str(uuid.uuid4())
        with patch("semantica.semantic_extract.methods.create_provider", return_value=provider):
            result = extract_entities_llm(unique, provider="openai", api_key="k")
        sent = provider.generate_typed.call_args[0][0]
        self.assertIn("Extract named entities", sent)
        self.assertEqual(len(result), 1)

    def test_upstream_source_has_no_fork_edits(self):
        """开闭原则守卫：六个上游文件相对上游基线零改动。"""
        for rel in ("semantica/semantic_extract/methods.py",
                    "semantica/semantic_extract/ner_extractor.py",
                    "semantica/semantic_extract/relation_extractor.py",
                    "semantica/semantic_extract/triplet_extractor.py",
                    "semantica/semantic_extract/coreference_resolver.py",
                    "semantica/normalize/date_normalizer.py"):
            out = subprocess.run(
                ["git", "diff", "254e358f", "--", rel], cwd=REPO,
                capture_output=True, text=True).stdout
            self.assertEqual(out.strip(), "", f"{rel} 相对上游基线被改动：\n{out[:300]}")


class TestCacheBypass(unittest.TestCase):
    def test_different_prompts_no_cross_pollution(self):
        """上游缓存键不含 prompt——扩展必须旁路：同文本不同提示词各打各的。"""
        text = TEXT + str(uuid.uuid4())
        provider = MagicMock()
        provider.generate_typed.return_value = _entity_response()
        with patch("semantica.semantic_extract.methods.create_provider", return_value=provider):
            extract_entities_llm_prompt(text, provider="openai", api_key="k", prompt="指令甲")
            extract_entities_llm_prompt(text, provider="openai", api_key="k", prompt="指令乙")
        self.assertEqual(provider.generate_typed.call_count, 2)  # 缓存被旁路

    def test_upstream_internals_restored_after_call(self):
        """委托结束后上游缓存与 create_provider 原样恢复。"""
        provider = MagicMock()
        provider.generate_typed.return_value = _entity_response()
        original_cache = methods._result_cache
        original_create = methods.create_provider
        with patch("semantica.semantic_extract.methods.create_provider", return_value=provider):
            extract_entities_llm_prompt(TEXT + str(uuid.uuid4()), provider="openai",
                                         api_key="k", prompt=CUSTOM)
        self.assertIs(methods._result_cache, original_cache)
        self.assertEqual(methods.create_provider, original_create)


class TestExtractorViaRegistry(unittest.TestCase):
    def test_ner_extractor_llm_prompt(self):
        provider = MagicMock()
        provider.generate_typed.return_value = _entity_response()
        from semantica.semantic_extract import NERExtractor

        with patch("semantica.semantic_extract.methods.create_provider", return_value=provider):
            ner = NERExtractor(method="llm_prompt", provider="openai", api_key="k5", prompt=CUSTOM)
            ner.extract(TEXT + str(uuid.uuid4()))
        self.assertIn(CUSTOM, provider.generate_typed.call_args[0][0])

    def test_relation_extractor_llm_prompt(self):
        provider = MagicMock()
        provider.generate_typed.return_value = _relation_response()
        from semantica.semantic_extract import RelationExtractor

        with patch("semantica.semantic_extract.methods.create_provider", return_value=provider):
            rel = RelationExtractor(method="llm_prompt", provider="openai", api_key="k6", prompt=CUSTOM)
            rel.extract_relations(TEXT + str(uuid.uuid4()), _real_entities())
        self.assertIn(CUSTOM, provider.generate_typed.call_args[0][0])

    def test_triplet_extractor_llm_prompt(self):
        provider = MagicMock()
        provider.generate_typed.return_value = _triplet_response()
        from semantica.semantic_extract import TripletExtractor

        with patch("semantica.semantic_extract.methods.create_provider", return_value=provider):
            trip = TripletExtractor(method="llm_prompt", provider="openai", api_key="k7", prompt=CUSTOM)
            trip.extract(TEXT + str(uuid.uuid4()))
        self.assertIn(CUSTOM, provider.generate_typed.call_args[0][0])

    def test_event_detector_inherits_via_composition(self):
        """EventDetector 组合 NER/Relation——底层方法名换 llm_prompt 即生效。"""
        provider = MagicMock()
        provider.generate_typed.return_value = _entity_response()
        from semantica.semantic_extract import NERExtractor

        with patch("semantica.semantic_extract.methods.create_provider", return_value=provider):
            ner = NERExtractor(method="llm_prompt", provider="openai", api_key="k8", prompt=CUSTOM)
            ner.extract(TEXT + str(uuid.uuid4()))
        self.assertIn(CUSTOM, provider.generate_typed.call_args[0][0])


if __name__ == "__main__":
    unittest.main()
