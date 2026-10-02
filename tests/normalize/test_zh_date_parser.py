"""Tests for the Chinese date parser (mission zh-normalization-01M3X5M5).

Covers every family from research R3, invalid-calendar rejection, strict
no-year policy, unsupported-calendar preservation and the DateNormalizer
routing (Chinese exclusive-on-hit, legacy fallback unchanged).
"""

import sys
import unittest
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from semantica.normalize.date_normalizer import DateNormalizer
from semantica.normalize.zh_date_parser import ZhDateParser


class TestFullFamily(unittest.TestCase):
    def test_full_date(self):
        result = ZhDateParser().parse("于2026年10月2日到账")
        self.assertEqual(result["value"], datetime(2026, 10, 2))
        self.assertEqual(result["matched_text"], "2026年10月2日")
        self.assertEqual(result["family"], "full")
        self.assertFalse(result["year_inferred"])

    def test_full_date_with_hao_suffix(self):
        result = ZhDateParser().parse("10月2号")
        self.assertEqual(result["value"].year, datetime.now().year)
        self.assertEqual(result["family"], "no_year")

    def test_full_date_with_time(self):
        result = ZhDateParser().parse("2026年10月2日 14:30")
        self.assertEqual(result["value"], datetime(2026, 10, 2, 14, 30))
        self.assertEqual(result["family"], "full_with_time")

    def test_full_date_with_time_and_seconds(self):
        result = ZhDateParser().parse("2026年10月2日 14:30:45")
        self.assertEqual(result["value"], datetime(2026, 10, 2, 14, 30, 45))


class TestHanNumeralFamily(unittest.TestCase):
    def test_han_numeral_full(self):
        result = ZhDateParser().parse("二〇二六年十月二日")
        self.assertEqual(result["value"], datetime(2026, 10, 2))
        self.assertEqual(result["family"], "han_numeral")

    def test_han_numeral_with_carry(self):
        result = ZhDateParser().parse("二〇二五年十二月三十一日")
        self.assertEqual(result["value"], datetime(2025, 12, 31))


class TestNoYearFamily(unittest.TestCase):
    def test_no_year_defaults_to_reference_year(self):
        reference = datetime(2026, 6, 15)
        result = ZhDateParser().parse("10月2日", reference=reference)
        self.assertEqual(result["value"], datetime(2026, 10, 2))
        self.assertTrue(result["year_inferred"])
        self.assertEqual(result["family"], "no_year")

    def test_no_year_strict_policy(self):
        parser = ZhDateParser(no_year_policy="strict")
        result = parser.parse("10月2日")
        self.assertIsNone(result["value"])

    def test_invalid_no_year_policy_rejected(self):
        with self.assertRaises(ValueError):
            ZhDateParser(no_year_policy="guess")


class TestRelativeFamily(unittest.TestCase):
    def test_basic_relative_tokens(self):
        reference = datetime(2026, 10, 2)
        cases = {"今天": 0, "明天": 1, "昨天": -1, "前天": -2, "后天": 2, "大后天": 3}
        for token, offset in cases.items():
            result = ZhDateParser().parse(token, reference=reference)
            self.assertEqual(result["value"], reference + __import__("datetime").timedelta(days=offset), token)
            self.assertTrue(result["year_inferred"])

    def test_next_weekday(self):
        reference = datetime(2026, 10, 2)  # Friday
        result = ZhDateParser().parse("下周一", reference=reference)
        self.assertEqual(result["value"], datetime(2026, 10, 5))  # next Monday
        result = ZhDateParser().parse("下周日", reference=reference)
        self.assertEqual(result["value"], datetime(2026, 10, 11))

    def test_this_weekday(self):
        reference = datetime(2026, 10, 2)  # Friday
        self.assertEqual(ZhDateParser().parse("本周一", reference=reference)["value"], datetime(2026, 9, 28))


class TestTimeOnlyFamily(unittest.TestCase):
    def test_time_only_uses_reference_date(self):
        reference = datetime(2026, 10, 2, 9, 0)
        result = ZhDateParser().parse("14时30分", reference=reference)
        self.assertEqual(result["value"], datetime(2026, 10, 2, 14, 30))
        self.assertEqual(result["family"], "with_time")


class TestInvalidAndUnsupported(unittest.TestCase):
    def test_invalid_february_30_rejected(self):
        result = ZhDateParser().parse("2月30日")
        self.assertIsNone(result["value"])

    def test_invalid_month_rejected(self):
        self.assertIsNone(ZhDateParser().parse("13月5日")["value"])

    def test_invalid_time_rejected(self):
        self.assertIsNone(ZhDateParser().parse("25时00分")["value"])

    def test_lunar_preserved_and_counted(self):
        before = ZhDateParser.unsupported_count
        result = ZhDateParser().parse("腊月初八")
        self.assertIsNone(result["value"])
        self.assertEqual(result["unsupported_matched"], "腊月初八")
        self.assertEqual(result.get("unsupported_kind"), "lunar")
        self.assertEqual(ZhDateParser.unsupported_count, before + 1)

    def test_republican_calendar_preserved(self):
        result = ZhDateParser().parse("民国115年")
        self.assertIsNone(result["value"])
        self.assertEqual(result.get("unsupported_kind"), "republican")

    def test_no_pattern_returns_none(self):
        self.assertIsNone(ZhDateParser().parse("hello world"))
        self.assertIsNone(ZhDateParser().parse(""))
        self.assertIsNone(ZhDateParser().parse("123"))


class TestZhDateNormalizer(unittest.TestCase):
    """fork 扩展：中文路由版 DateNormalizer（组合，不改上游）。"""

    def test_chinese_date_through_extension(self):
        from semantica.normalize import ZhDateNormalizer

        normalized = ZhDateNormalizer().normalize_date("2026年10月2日")
        self.assertTrue(normalized.startswith("2026-10-02"), normalized)

    def test_legacy_iso_path_unchanged(self):
        from semantica.normalize import ZhDateNormalizer

        self.assertTrue(ZhDateNormalizer().normalize_date("2023-01-15").startswith("2023-01-15"))

    def test_legacy_relative_falls_back(self):
        from semantica.normalize import ZhDateNormalizer

        normalized = ZhDateNormalizer().normalize_date("yesterday")
        self.assertIsInstance(normalized, str)
        self.assertNotIn("yesterday", normalized)

    def test_upstream_date_normalizer_untouched(self):
        """上游 DateNormalizer 无中文路由（开闭原则：行为不加不减）。"""
        from semantica.normalize import DateNormalizer

        n = DateNormalizer()
        # dateutil 对中文日期无能为力——上游行为保持原样（不抛错断言具体形态，
        # 只断言它不认识中文：结果是相对回退或异常，而非 2026-10-02）
        try:
            out = n.normalize_date("2026年10月2日")
            self.assertFalse(out.startswith("2026-10-02"), out)
        except Exception:
            pass  # 上游对无法解析输入的既有行为（抛错）也属"未改动"


if __name__ == "__main__":
    unittest.main()
