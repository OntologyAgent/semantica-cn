"""
CJK Spacing Normalizer Module

This module provides text normalization for CJK (Chinese) typography: spacing
between CJK and Western (Latin letters / digits) runs, and fullwidth space
(U+3000) unification. It follows pangu-style semantics.

Algorithms Used:
    - Character Class Detection: Unicode block membership (CJK Unified
      Ideographs, CJK punctuation, fullwidth ASCII forms) decides which side
      of a "boundary" each character belongs to
    - Boundary Spacing: regex adjacency rules insert (policy "add") or remove
      (policy "remove") spaces at Western/CJK-ideograph boundaries; policy
      "preserve" only unifies U+3000
    - Idempotency: inserted spaces create no new adjacency, so repeated
      application is a fixed point; removal likewise

Design Constraints:
    - Pure standard library (re, unicodedata); no third-party dependencies
    - Text without any CJK ideograph or U+3000 is returned byte-identical
    - Fullwidth punctuation is NOT spaced against CJK ideographs, and by
      default not against Western characters either (matches pangu's default
      and avoids over-correction like "Semantica！" -> "Semantica ！")

Key Features:
    - Three policies: "add" (default), "remove", "preserve"
    - Detailed mode returning an adjustment count for provenance/auditing
    - Fullwidth space U+3000 always normalized to a halfwidth space

Main Classes:
    - CJKSpacingNormalizer: CJK/Western boundary spacing normalizer

Example Usage:
    >>> from semantica.normalize.cjk_spacing import CJKSpacingNormalizer
    >>> normalizer = CJKSpacingNormalizer()
    >>> normalizer.normalize("Semantica知识图谱")
    'Semantica 知识图谱'
    >>> normalizer.normalize("AI驱动决策")
    'AI 驱动决策'

Author: Semantica Contributors
License: MIT
"""

import re
from typing import Any, Dict

from ..utils.logging import get_logger

# CJK Unified Ideographs (common + Extension A + compatibility ideographs).
_CJK_IDEOGRAPH = (
    "\u3400-\u4dbf"  # Extension A
    "\u4e00-\u9fff"  # Unified Ideographs (common)
    "\uf900-\ufaff"  # Compatibility Ideographs
)

# Western side: ASCII letters/digits plus common symbols that cling to CJK
# in finance text ($5M、¥100、50%off) — spacing rules treat them as Western.
_WESTERN = "A-Za-z0-9$%\\u00a5\\u20ac\\u00a3+#&*=<>/"

# Patterns are compiled once per direction; each is a pair (pattern, template)
# applied in order. A boundary exists only where a Western char and a CJK
# ideograph are directly adjacent (no space between them).
_ADD_PATTERNS = (
    (re.compile(r"([%s])([%s])" % (_WESTERN, _CJK_IDEOGRAPH)), r"\1 \2"),
    (re.compile(r"([%s])([%s])" % (_CJK_IDEOGRAPH, _WESTERN)), r"\1 \2"),
)

# For removal, a boundary is a run of spaces separating the two classes —
# plus CJK-CJK runs: PDF extraction noise like "知 识" collapses to "知识"
# (the primary token-saving use case; mirrors the maintainer's pipeline).
_REMOVE_PATTERNS = (
    (re.compile(r"([%s]) +([%s])" % (_WESTERN, _CJK_IDEOGRAPH)), r"\1\2"),
    (re.compile(r"([%s]) +([%s])" % (_CJK_IDEOGRAPH, _WESTERN)), r"\1\2"),
    (re.compile(r"([%s]) +(?=[%s])" % (_CJK_IDEOGRAPH, _CJK_IDEOGRAPH)), r"\1"),
)

# Fast-path check: anything CJK-ish at all (ideographs or fullwidth space)?
_NEEDS_WORK = re.compile("[%s\u3000]" % _CJK_IDEOGRAPH)

_VALID_POLICIES = ("add", "remove", "preserve")


class CJKSpacingNormalizer:
    """Normalize spacing between CJK and Western character runs.

    Policies:
        - ``add`` (default): insert one space at each Western/CJK-ideograph
          boundary that has none
        - ``remove``: delete spaces at those boundaries and between
          adjacent CJK ideographs (PDF-extraction noise)
        - ``preserve``: leave boundaries untouched; only unify U+3000

    In all policies the fullwidth space U+3000 is normalized to a halfwidth
    space. Text containing no CJK ideograph and no U+3000 is returned
    unchanged (byte-identical).
    """

    def __init__(self, policy: str = "add", **config: Any) -> None:
        """Initialize with a spacing policy.

        Args:
            policy: One of "add", "remove", "preserve" (default "add").
            **config: Reserved for future options; unknown keys are ignored.

        Raises:
            ValueError: If the policy is not one of the valid values.
        """
        self.logger = get_logger("cjk_spacing_normalizer")
        if policy not in _VALID_POLICIES:
            raise ValueError(
                "policy must be one of %s, got %r" % (", ".join(_VALID_POLICIES), policy)
            )
        self.policy = policy
        self.config = config

    def normalize(self, text: str) -> str:
        """Return ``text`` with CJK/Western spacing normalized.

        Idempotent: ``normalize(normalize(x)) == normalize(x)``.
        """
        return self.normalize_detailed(text)["normalized"]

    def normalize_detailed(self, text: str) -> Dict[str, Any]:
        """Normalize and report how many boundaries were adjusted.

        Returns:
            dict with keys ``normalized`` (str), ``boundaries_adjusted`` (int,
            insertions + removals) and ``policy`` (str).
        """
        if not isinstance(text, str):
            raise ValueError("cjk_spacing expects str input, got %s" % type(text).__name__)

        if not text or not _NEEDS_WORK.search(text):
            return {"normalized": text, "boundaries_adjusted": 0, "policy": self.policy}

        # Fullwidth space unification happens in every policy first; it is
        # not counted as a boundary adjustment (it is a separate rule).
        working = text.replace("\u3000", " ")

        adjusted = 0
        if self.policy == "add":
            for pattern, template in _ADD_PATTERNS:
                adjusted += len(pattern.findall(working))
                working = pattern.sub(template, working)
        elif self.policy == "remove":
            for pattern, template in _REMOVE_PATTERNS:
                adjusted += len(pattern.findall(working))
                working = pattern.sub(template, working)

        return {"normalized": working, "boundaries_adjusted": adjusted, "policy": self.policy}
