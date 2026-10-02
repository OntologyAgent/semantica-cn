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

# Markdown 防护（CommonMark 语义）：默认 preserve_markdown=True 时，
# 1) 围栏代码块（``` / ~~~）与缩进代码块（≥4 空格）整行原样；
# 2) 行内代码 span（`…`）内容原样；
# 3) 行首块级标记（#{1,6} 标题、> 引用、-/*/+/1. 列表）后的空格保留；
# 4) 强调与标记符号 * # > 视为非边界字符——add 不会把 **加粗** 改成
#    ** 加粗 **（破坏强调），remove 不会吃掉 ## 标题 / > 引用的空格。
#    行中同样的符号（如 "版本#号"）随之不参与 CJK 边界，属可接受代价。
_MD_BLOCK_MARKER = re.compile(r"^(\s{0,3}(?:#{1,6}|>+|-|\*|\+|\d+[.\)]))(\s+)")
_MD_FENCE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")
_MD_INDENTED_CODE = re.compile(r"^    \S")
_MD_INLINE_CODE = re.compile(r"(`+)(.+?)\1")
_MD_MASK = {"*": "\x00", "#": "\x01", ">": "\x02"}
_MD_UNMASK = {v: k for k, v in _MD_MASK.items()}

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

    def __init__(self, policy: str = "add", preserve_markdown: bool = True,
                 **config: Any) -> None:
        """Initialize with a spacing policy.

        Args:
            policy: One of "add", "remove", "preserve" (default "add").
            preserve_markdown: 若为 True（默认），行首块级标记（#{1,6} 标题、
              > 引用、-/*/+ 与 "1." 列表）后的空格不被 remove 吃掉，围栏代
              码块（``` / ~~~）内容整段原样。设为 False 恢复逐字符处理。
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
        self.preserve_markdown = preserve_markdown
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

        if self.preserve_markdown:
            working, adjusted = self._apply_markdown_aware(text)
        else:
            working, adjusted = self._apply_plain(text)

        return {"normalized": working, "boundaries_adjusted": adjusted, "policy": self.policy}

    def _apply_plain(self, text: str):
        """逐字符整体处理（preserve_markdown=False 的旧行为）。"""
        # 全角空格归一在任何策略下先执行（不计入边界数）。
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
        return working, adjusted

    def _apply_markdown_aware(self, text: str):
        """按行处理，完整保留 Markdown 语法（见 _MD_* 常量注释）。"""
        out_lines = []
        adjusted = 0
        in_fence = False
        for line in text.split("\n"):
            if _MD_FENCE.match(line):
                in_fence = not in_fence
                out_lines.append(line)
                continue
            if in_fence or _MD_INDENTED_CODE.match(line):
                out_lines.append(line)          # 代码内容不动（含 U+3000）
                continue
            line = line.replace("\u3000", " ")
            marker = _MD_BLOCK_MARKER.match(line)
            if marker:
                prefix, rest = line[:marker.end(1)], line[marker.end(1):]
                out_lines.append(prefix + self._process_prose(rest))
                adjusted += self._last_adjusted
            else:
                out_lines.append(self._process_prose(line))
                adjusted += self._last_adjusted
        return "\n".join(out_lines), adjusted

    def _process_prose(self, segment: str) -> str:
        """处理正文段：行内代码 span 原样，其余部分对 * # > 掩码后归一。"""
        parts = []
        cursor = 0
        self._last_adjusted = 0
        for m in _MD_INLINE_CODE.finditer(segment):
            head = segment[cursor:m.start()]
            parts.append(self._normalize_masked(head))
            parts.append(m.group(0))            # 行内代码原样
            cursor = m.end()
        parts.append(self._normalize_masked(segment[cursor:]))
        return "".join(parts)

    def _normalize_masked(self, prose: str) -> str:
        for char, sentinel in _MD_MASK.items():
            prose = prose.replace(char, sentinel)
        processed, n = self._apply_plain(prose)
        self._last_adjusted = (getattr(self, "_last_adjusted", 0)) + n
        for sentinel, char in _MD_UNMASK.items():
            processed = processed.replace(sentinel, char)
        return processed
