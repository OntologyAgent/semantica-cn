"""LLM 别名消解测试（mission llm-extractor-family-01M3X5J7 WP02）。

mock create_provider → generate_structured；断言：替换正确、子串误伤防护、
min_confidence 拒绝、无映射返回原文、prompt 替换到达 LLM。
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from semantica.semantic_extract.coreference_resolver import CoreferenceResolver

TEXT = "岭川与华跃控股北京有限公司签订2025年商业政策，华跃北京负责北京地区分销。"
MAPPINGS = {
    "mappings": [
        {"alias": "岭川", "canonical": "杭州岭川制药有限公司", "confidence": 0.95},
        {"alias": "华跃北京", "canonical": "华跃控股北京有限公司", "confidence": 0.9},
        {"alias": "跃控股", "canonical": "某控股集团", "confidence": 0.99},  # 规范名子串，应被保护
    ]
}


def _provider(return_value=None):
    p = MagicMock()
    p.generate_structured.return_value = return_value if return_value is not None else MAPPINGS
    return p


class TestResolveAliasesLLM(unittest.TestCase):
    def test_basic_replacement(self):
        with patch("semantica.semantic_extract.providers.create_provider", return_value=_provider()):
            result = CoreferenceResolver().resolve_aliases_llm(TEXT, provider="deepseek", api_key="k")
        self.assertIn("杭州岭川制药有限公司", result["resolved_text"])
        self.assertIn("华跃控股北京有限公司", result["resolved_text"])
        self.assertNotIn("岭川与", result["resolved_text"])

    def test_substring_protection(self):
        """「跃控股」是规范名「华跃控股北京有限公司」的子串——出现处全被保护，不替换。"""
        with patch("semantica.semantic_extract.providers.create_provider", return_value=_provider()):
            result = CoreferenceResolver().resolve_aliases_llm(TEXT, provider="deepseek", api_key="k")
        self.assertNotIn("某控股集团", result["resolved_text"])
        self.assertTrue(any(s["mapping"]["alias"] == "跃控股" and "protected" in s["reason"]
                            for s in result["skipped"]))
        # 被保护后原文完整保留该规范名
        self.assertIn("华跃控股北京有限公司", result["resolved_text"])

    def test_min_confidence_rejection(self):
        low = {"mappings": [{"alias": "岭川", "canonical": "X公司", "confidence": 0.5}]}
        with patch("semantica.semantic_extract.providers.create_provider", return_value=_provider(low)):
            result = CoreferenceResolver().resolve_aliases_llm(TEXT, provider="deepseek", api_key="k")
        self.assertEqual(result["resolved_text"], TEXT)
        self.assertTrue(any("confidence" in s["reason"] for s in result["skipped"]))

    def test_no_mappings_returns_original(self):
        with patch("semantica.semantic_extract.providers.create_provider", return_value=_provider({"mappings": []})):
            result = CoreferenceResolver().resolve_aliases_llm(TEXT, provider="deepseek", api_key="k")
        self.assertEqual(result["resolved_text"], TEXT)
        self.assertEqual(result["mappings"], [])

    def test_custom_prompt_reaches_llm(self):
        custom = "只映射政策简称，别的都不要。"
        provider = _provider()
        with patch("semantica.semantic_extract.providers.create_provider", return_value=provider):
            CoreferenceResolver().resolve_aliases_llm(
                TEXT, provider="deepseek", api_key="k", prompt=custom)
        sent = provider.generate_structured.call_args[0][0]
        self.assertIn(custom, sent)
        self.assertNotIn("找出下面文本里的", sent)

    def test_default_prompt_contains_text(self):
        provider = _provider()
        with patch("semantica.semantic_extract.providers.create_provider", return_value=provider):
            CoreferenceResolver().resolve_aliases_llm(TEXT, provider="deepseek", api_key="k")
        sent = provider.generate_structured.call_args[0][0]
        self.assertIn(TEXT, sent)
        self.assertIn("找出下面文本里的", sent)

    def test_alias_not_present_skipped(self):
        absent = {"mappings": [{"alias": "不存在的别名", "canonical": "某公司", "confidence": 0.99}]}
        with patch("semantica.semantic_extract.providers.create_provider", return_value=_provider(absent)):
            result = CoreferenceResolver().resolve_aliases_llm(TEXT, provider="deepseek", api_key="k")
        self.assertEqual(result["resolved_text"], TEXT)
        self.assertTrue(any("not present" in s["reason"] for s in result["skipped"]))


if __name__ == "__main__":
    unittest.main()
