"""Tests for the CJK spacing normalizer (mission zh-normalization-01M3X5M5).

Covers: three policies, idempotency, round-trip add->remove, byte-identical
Western-only input, fullwidth punctuation behaviour and U+3000 unification.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from semantica.normalize.cjk_spacing import CJKSpacingNormalizer


SAMPLES = [
    "Semantica知识图谱",
    "AI驱动决策",
    "2026年10月2日",
    "支付$5M到账",
    "中文English混排text",
    "版本v2.5发布",
    "知识图谱(Knowledge Graph)是基础设施",
]


class TestPolicies(unittest.TestCase):
    def test_add_policy_inserts_spaces(self):
        n = CJKSpacingNormalizer()
        self.assertEqual(n.normalize("Semantica知识图谱"), "Semantica 知识图谱")
        self.assertEqual(n.normalize("AI驱动"), "AI 驱动")
        self.assertEqual(n.normalize("图谱AI"), "图谱 AI")

    def test_remove_policy_strips_boundary_spaces(self):
        n = CJKSpacingNormalizer(policy="remove")
        self.assertEqual(n.normalize("Semantica 知识图谱"), "Semantica知识图谱")
        self.assertEqual(n.normalize("图谱  AI"), "图谱AI")
        # Multiple spaces at the boundary collapse too.
        self.assertEqual(n.normalize("AI   驱动"), "AI驱动")

    def test_preserve_policy_only_unifies_u3000(self):
        n = CJKSpacingNormalizer(policy="preserve")
        self.assertEqual(n.normalize("Semantica 知识图谱"), "Semantica 知识图谱")
        self.assertEqual(n.normalize("Semantica知识图谱"), "Semantica知识图谱")
        self.assertEqual(n.normalize("全角\u3000空格"), "全角 空格")

    def test_invalid_policy_rejected(self):
        with self.assertRaises(ValueError):
            CJKSpacingNormalizer(policy="explode")

    def test_remove_collapses_cjk_cjk_spaces(self):
        # notebook 用例：NFKC 后 CJK 之间的噪声空格
        n = CJKSpacingNormalizer(policy="remove")
        self.assertEqual(n.normalize("知 识 图 谱"), "知识图谱")
        self.assertEqual(n.normalize("杭 州默沙东"), "杭州默沙东")

    def test_add_does_not_touch_cjk_cjk(self):
        n = CJKSpacingNormalizer()
        self.assertEqual(n.normalize("知 识"), "知 识")

    def test_round_trip_add_then_remove(self):
        add = CJKSpacingNormalizer()
        remove = CJKSpacingNormalizer(policy="remove")
        for sample in SAMPLES:
            spaced = add.normalize(sample)
            self.assertEqual(remove.normalize(spaced), sample)


class TestIdempotency(unittest.TestCase):
    def test_add_is_idempotent(self):
        n = CJKSpacingNormalizer()
        for sample in SAMPLES:
            once = n.normalize(sample)
            self.assertEqual(n.normalize(once), once)

    def test_remove_is_idempotent(self):
        n = CJKSpacingNormalizer(policy="remove")
        for sample in SAMPLES:
            once = n.normalize(sample)
            self.assertEqual(n.normalize(once), once)


class TestWesternOnlySafety(unittest.TestCase):
    def test_pure_western_byte_identical(self):
        n = CJKSpacingNormalizer()
        for text in ("Hello world 123", "2026-10-02 14:30:00", "", "   \t\n"):
            self.assertEqual(n.normalize(text), text)
            self.assertEqual(n.normalize(text).encode("utf-8"), text.encode("utf-8"))

    def test_western_with_punctuation_untouched(self):
        n = CJKSpacingNormalizer()
        self.assertEqual(n.normalize("Hello, world! (v2)"), "Hello, world! (v2)")


class TestFullwidthBehaviour(unittest.TestCase):
    def test_fullwidth_space_normalized_in_all_policies(self):
        for policy in ("add", "remove", "preserve"):
            n = CJKSpacingNormalizer(policy=policy)
            self.assertEqual(n.normalize("中文\u3000English"), "中文 English" if policy == "add" else ("中文English" if policy == "remove" else "中文 English"))

    def test_fullwidth_punctuation_not_spaced_against_cjk(self):
        n = CJKSpacingNormalizer()
        self.assertEqual(n.normalize("知识图谱。"), "知识图谱。")
        self.assertEqual(n.normalize("（注释）内容"), "（注释）内容")

    def test_fullwidth_punctuation_not_spaced_against_western_by_default(self):
        # pangu default: avoid over-correction such as "Semantica！" -> "Semantica ！"
        n = CJKSpacingNormalizer()
        self.assertEqual(n.normalize("发布Semantica！"), "发布 Semantica！")

    def test_nbsp_out_of_scope(self):
        # NBSP (U+00A0) is not a boundary space for any policy: it passes
        # through unchanged (research R2 scope decision).
        n = CJKSpacingNormalizer()
        self.assertEqual(n.normalize("中文\xa0English"), "中文\xa0English")
        remove = CJKSpacingNormalizer(policy="remove")
        self.assertEqual(remove.normalize("中文\xa0English"), "中文\xa0English")


class TestDetailedOutput(unittest.TestCase):
    def test_detailed_counts_boundaries(self):
        n = CJKSpacingNormalizer()
        result = n.normalize_detailed("AI驱动")
        self.assertEqual(result["normalized"], "AI 驱动")
        self.assertEqual(result["boundaries_adjusted"], 1)
        self.assertEqual(result["policy"], "add")

    def test_detailed_counts_both_directions(self):
        result = CJKSpacingNormalizer().normalize_detailed("图谱AI驱动")
        self.assertEqual(result["normalized"], "图谱 AI 驱动")
        self.assertEqual(result["boundaries_adjusted"], 2)

    def test_detailed_zero_for_western_only(self):
        result = CJKSpacingNormalizer().normalize_detailed("Hello world")
        self.assertEqual(result["boundaries_adjusted"], 0)

    def test_non_string_input_rejected(self):
        with self.assertRaises(ValueError):
            CJKSpacingNormalizer().normalize(123)


if __name__ == "__main__":
    unittest.main()
