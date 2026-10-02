"""Registry/exports integration tests (mission zh-normalization-01M3X5M5).

非 integration 标记（门禁内跑）：注册分发、导出面、与既有 normalize 组合。
"""

import sys
import unittest
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from semantica.normalize import (
    CJKSpacingNormalizer,
    ZhDateParser,
    method_registry,
    methods,
)


class TestExports(unittest.TestCase):
    def test_public_exports(self):
        import semantica.normalize as pkg

        for name in ("CJKSpacingNormalizer", "ZhDateParser"):
            self.assertTrue(hasattr(pkg, name), name)
            self.assertIn(name, pkg.__all__)

    def test_registered_methods(self):
        self.assertIn("cjk_spacing", method_registry.list_all("text")["text"])
        self.assertIn("cn_date", method_registry.list_all("date")["date"])


class TestMethodDispatch(unittest.TestCase):
    def test_cjk_spacing_via_normalize_text(self):
        self.assertEqual(
            methods.normalize_text("Semantica知识图谱", method="cjk_spacing"),
            "Semantica 知识图谱",
        )

    def test_cjk_spacing_policy_passthrough(self):
        self.assertEqual(
            methods.normalize_text("知识 图谱", method="cjk_spacing", policy="remove"),
            "知识图谱",
        )

    def test_cn_date_via_normalize_date(self):
        self.assertEqual(
            methods.normalize_date("2026年10月2日", method="cn_date", format="date"),
            "2026-10-02",
        )

    def test_cn_date_range(self):
        result = methods.normalize_date(
            "2025年1月1日至2025年12月31日", method="cn_date", format="date")
        self.assertEqual(result, "2025-01-01")

    def test_cn_date_no_match_raises(self):
        with self.assertRaises(ValueError):
            methods.normalize_date("hello", method="cn_date")


class TestPipelineComposition(unittest.TestCase):
    def test_spacing_then_date(self):
        """notebook 流水线：去空格不破坏日期命中。"""
        raw = "支付 $5M ，于 2026年10月2日 到账"
        cleaned = CJKSpacingNormalizer(policy="remove").normalize(raw)
        result = ZhDateParser().parse(cleaned)
        self.assertEqual(result["value"], datetime(2026, 10, 2))

    def test_chinese_date_entry_points(self):
        # OCP：默认路径=上游 dateutil（无中文路由，中文输入回落相对处理器）。
        # 中文入口是 method="cn_date" 或 ZhDateNormalizer 扩展类。
        self.assertEqual(
            methods.normalize_date("2026年10月2日", method="cn_date", format="date"),
            "2026-10-02",
        )
        from semantica.normalize import ZhDateNormalizer

        self.assertTrue(ZhDateNormalizer().normalize_date("2026年10月2日").startswith("2026-10-02"))

    def test_default_text_unchanged(self):
        # 默认文本路径不受注册影响
        self.assertEqual(methods.normalize_text("Hello   World"), "Hello World")


if __name__ == "__main__":
    unittest.main()
