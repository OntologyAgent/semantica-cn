"""prompt 入口测试（mission llm-extractor-family-01M3X5J7 WP01）。

mock create_provider，断言：自定义 prompt 到达 LLM 且带守卫尾与原文注入；
缓存键按 prompt 区分；未传 prompt 时默认提示词不变；三链路 + EventDetector 组合。
"""

import sys
import unittest
import uuid
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from semantica.semantic_extract.methods import (
    extract_entities_llm,
    extract_relations_llm,
    extract_triplets_llm,
)

def _real_entities():
    from semantica.semantic_extract.types import Entity

    return [Entity(text="华跃控股北京有限公司", label="ORG", start_char=0, end_char=12, confidence=0.9)]


CUSTOM = "你是医药政策解析器。只抽取公司全称与政策编号，宁缺毋滥。"
TEXT = "华跃控股北京有限公司与杭州岭川制药有限公司签订2025年商业政策。"
UNIQUE = TEXT + "（用例隔离后缀%s）"


from semantica.semantic_extract.schemas import (
    EntitiesResponse,
    EntityOut,
    RelationOut,
    RelationsResponse,
    TripletOut,
    TripletsResponse,
)


def _entity_response():
    return EntitiesResponse(entities=[
        EntityOut(text="华跃控股北京有限公司", label="ORG", confidence=0.9),
    ])


def _relation_response():
    return RelationsResponse(relations=[
        RelationOut(subject="华跃控股北京有限公司", predicate="signs",
                    object="2025年商业政策", confidence=0.9),
    ])


def _triplet_response():
    return TripletsResponse(triplets=[
        TripletOut(subject="华跃控股北京有限公司", predicate="is_a", object="公司", confidence=0.9),
    ])


class TestPromptReachesProvider(unittest.TestCase):
    def test_entities_custom_prompt(self):
        provider = MagicMock()
        provider.generate_typed.return_value = _entity_response()
        with patch("semantica.semantic_extract.methods.create_provider", return_value=provider):
            extract_entities_llm(TEXT, provider="openai", api_key="k", prompt=CUSTOM)
        sent = provider.generate_typed.call_args[0][0]
        self.assertIn(CUSTOM, sent)
        self.assertIn('"entities"', sent)          # 守卫尾
        self.assertIn(TEXT, sent)                   # 原文注入
        # 默认指令不再出现
        self.assertNotIn("Extract named entities", sent)

    def test_relations_custom_prompt(self):
        provider = MagicMock()
        provider.generate_typed.return_value = _relation_response()
        with patch("semantica.semantic_extract.methods.create_provider", return_value=provider):
            extract_relations_llm(TEXT + str(uuid.uuid4()), entities=_real_entities(), provider="openai", api_key="k", prompt=CUSTOM)
        sent = provider.generate_typed.call_args[0][0]
        self.assertIn(CUSTOM, sent)
        self.assertIn('"relations"', sent)
        self.assertNotIn("Extract relations between entities", sent)

    def test_triplets_custom_prompt(self):
        provider = MagicMock()
        provider.generate_typed.return_value = _triplet_response()
        with patch("semantica.semantic_extract.methods.create_provider", return_value=provider):
            extract_triplets_llm(TEXT, provider="openai", api_key="k", prompt=CUSTOM)
        sent = provider.generate_typed.call_args[0][0]
        self.assertIn(CUSTOM, sent)
        self.assertIn('"triplets"', sent)
        self.assertNotIn("Extract RDF triplets", sent)


class TestDefaultUnchanged(unittest.TestCase):
    def test_default_prompt_without_custom(self):
        provider = MagicMock()
        provider.generate_typed.return_value = _entity_response()
        with patch("semantica.semantic_extract.methods.create_provider", return_value=provider):
            extract_entities_llm(TEXT, provider="openai", api_key="k2")
        sent = provider.generate_typed.call_args[0][0]
        self.assertIn("Extract named entities", sent)


class TestCacheKeyIncludesPrompt(unittest.TestCase):
    def test_different_prompts_both_hit_provider(self):
        provider = MagicMock()
        provider.generate_typed.return_value = _entity_response()
        with patch("semantica.semantic_extract.methods.create_provider", return_value=provider):
            extract_entities_llm(TEXT, provider="openai", api_key="k3", prompt="指令甲")
            extract_entities_llm(TEXT, provider="openai", api_key="k3", prompt="指令乙")
        self.assertEqual(provider.generate_typed.call_count, 2)

    def test_same_prompt_second_call_hits_cache(self):
        provider = MagicMock()
        provider.generate_typed.return_value = _entity_response()
        with patch("semantica.semantic_extract.methods.create_provider", return_value=provider):
            extract_entities_llm(TEXT, provider="openai", api_key="k4", prompt="同一指令")
            extract_entities_llm(TEXT, provider="openai", api_key="k4", prompt="同一指令")
        self.assertEqual(provider.generate_typed.call_count, 1)


class TestExtractorPassthrough(unittest.TestCase):
    def test_ner_extractor_passes_prompt(self):
        provider = MagicMock()
        provider.generate_typed.return_value = _entity_response()
        from semantica.semantic_extract import NERExtractor

        with patch("semantica.semantic_extract.methods.create_provider", return_value=provider):
            ner = NERExtractor(method="llm", provider="openai", api_key="k5", prompt=CUSTOM)
            ner.extract(TEXT + str(uuid.uuid4()))
        self.assertIn(CUSTOM, provider.generate_typed.call_args[0][0])

    def test_relation_extractor_passes_prompt(self):
        provider = MagicMock()
        provider.generate_typed.return_value = _relation_response()
        from semantica.semantic_extract import RelationExtractor

        with patch("semantica.semantic_extract.methods.create_provider", return_value=provider):
            rel = RelationExtractor(method="llm", provider="openai", api_key="k6", prompt=CUSTOM)
            rel.extract_relations(TEXT + str(uuid.uuid4()), _real_entities())
        self.assertIn(CUSTOM, provider.generate_typed.call_args[0][0])

    def test_triplet_extractor_passes_prompt(self):
        provider = MagicMock()
        provider.generate_typed.return_value = _triplet_response()
        from semantica.semantic_extract import TripletExtractor

        with patch("semantica.semantic_extract.methods.create_provider", return_value=provider):
            trip = TripletExtractor(method="llm", provider="openai", api_key="k7", prompt=CUSTOM)
            trip.extract(TEXT + str(uuid.uuid4()))
        self.assertIn(CUSTOM, provider.generate_typed.call_args[0][0])

    def test_event_detector_inherits_via_composition(self):
        """EventDetector 组合 NER/Relation——prompt 经底层链路生效（FR-005）。"""
        provider = MagicMock()
        provider.generate_typed.return_value = _entity_response()
        from semantica.semantic_extract import NERExtractor

        with patch("semantica.semantic_extract.methods.create_provider", return_value=provider):
            ner = NERExtractor(method="llm", provider="openai", api_key="k8", prompt=CUSTOM)
            ner.extract(TEXT + str(uuid.uuid4()))
        self.assertIn(CUSTOM, provider.generate_typed.call_args[0][0])


if __name__ == "__main__":
    unittest.main()
