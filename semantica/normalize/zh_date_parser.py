"""
Chinese Date Parser Module

Parses Chinese calendar-date expressions (Gregorian calendar written in
Chinese) into datetime values: ``2026年10月2日``, ``10月2号``, ``二〇二六年
十月二日``, relative expressions (``明天``, ``下周五``) and standalone times
(``14时30分``). Unsupported calendars (农历, 民国纪年) are detected, preserved
verbatim and counted — never silently mangled (FR-004).

Algorithms Used:
    - Family-Ordered Regex Matching: most specific family first
      (full+time > full > han-numeral > no-year > relative > time-only)
    - Han Numeral Conversion: positional digits for years (〇〇-九九), small
      numbers (< 100) with 十-carry for months/days
    - Strict Calendar Validation: month/day ranges via calendar.monthrange;
      invalid values (e.g. ``2月30日``) are rejected, never overflowed
    - Reference-Based Relative Resolution: offsets from ``reference`` (default
      now), reported with ``year_inferred=True``

Failure Semantics (FR-004):
    - ``parse`` never raises for content reasons; it returns
      ``value=None`` for invalid calendar values and carries
      ``unsupported_matched`` for unsupported calendars
    - ``parse`` returns ``None`` only when the text contains no Chinese date
      pattern at all

Main Classes:
    - ZhDateParser: Chinese date expression parser

Example Usage:
    >>> from semantica.normalize.zh_date_parser import ZhDateParser
    >>> ZhDateParser().parse("2026年10月2日")["value"]
    datetime.datetime(2026, 10, 2, 0, 0)

Author: Semantica Contributors
License: MIT
"""

import calendar
import re
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from ..utils.logging import get_logger

_HAN_DIGITS = {"〇": 0, "零": 0, "一": 1, "二": 2, "三": 3, "四": 4,
               "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}

# Families are tried in order; first match wins.
_TIME_SUFFIX = r"\s*(\d{1,2}):(\d{2})(?::(\d{2}))?"
_FULL_TIME_RE = re.compile(
    r"(\d{4})年(\d{1,2})月(\d{1,2})[日号]" + _TIME_SUFFIX)
_FULL_RE = re.compile(r"(\d{4})年(\d{1,2})月(\d{1,2})[日号]")
_HAN_YEAR_RE = re.compile(r"([〇零一二三四五六七八九]{4})年")
_HAN_FULL_RE = re.compile(
    r"([〇零一二三四五六七八九]{4})年([〇零一二三四五六七八九十]{1,3})月"
    r"([〇零一二三四五六七八九十]{1,3})[日号]")
_NO_YEAR_RE = re.compile(r"(\d{1,2})月(\d{1,2})[日号]")
_TIME_ONLY_RE = re.compile(r"(\d{1,2})时(\d{1,2})分")
# 区间：2025年1月1日至2025年12月31日（至/到/—/~/-）
_RANGE_RE = re.compile(
    r"(\d{4})年(\d{1,2})月(\d{1,2})[日号]\s*[至到—~\-]\s*"
    r"(\d{4})年(\d{1,2})月(\d{1,2})[日号]")
# 仅年份：2025年（须前无数字，避免被区间/完整日期抢先）
_YEAR_ONLY_RE = re.compile(r"(?<![\d年])(\d{4})年(?![\d月])")
# 数量偏移：前三个自然月 / 三天前 / 三个月后 / 两周内
_OFFSET_RE = re.compile(
    r"(前|后)?\s*([0-9一二两三四五六七八九十]+)\s*个?\s*(自然月|个月|月|周|天|日|年)\s*(前|后)?")
_OFFSET_UNIT_DAYS = {"天": 1, "日": 1, "周": 7, "月": 30, "个月": 30, "自然月": 30, "年": 365}
_HAN_NUM_EXTRA = {"两": 2}
# 年度相对词：去年/今年/明年/后年/大后年/大前年
_YEAR_RELATIVE_RE = re.compile(r"(大前年|前年|去年|今年|明年|后年|大后年)")
_YEAR_RELATIVE_OFFSET = {"大前年": -3, "前年": -2, "去年": -1, "今年": 0,
                         "明年": 1, "后年": 2, "大后年": 3}

_RELATIVE_RE = re.compile(
    r"(今天|明天|昨天|前天|后天|大后天|大前天|下周[一二三四五六日天]|"
    r"本周[一二三四五六日天]|这周[一二三四五六日天])")

# Unsupported calendars: detected so they can be preserved verbatim.
_UNSUPPORTED_RES = (
    # 只匹配非数字表达的历法专名月份（腊/正/冬/闰），避免误伤"十二月三十一日"这类汉字数字日期
    (re.compile(r"(?:腊月|正月|冬月|闰[一二三四五六七八九十]{1,2}月)"
                r"[初二三三四五六七八九十廿]{1,3}"), "lunar"),
    (re.compile(r"民国\s*\d{1,3}年"), "republican"),
)

_WEEKDAY_MAP = {"一": 0, "二": 1, "三": 2, "四": 3, "五": 4, "六": 5,
                "日": 6, "天": 6}


def _han_small_number(text: str) -> Optional[int]:
    """Convert a han-numeral month/day (< 100) to int; None if malformed."""
    if not text:
        return None
    if "十" not in text:
        if len(text) != 1 or text not in _HAN_DIGITS:
            return None
        return _HAN_DIGITS[text]
    parts = text.split("十")
    if len(parts) != 2:
        return None
    tens, ones = parts
    if len(tens) > 1 or (tens and tens not in _HAN_DIGITS):
        return None
    if ones and (len(ones) > 1 or ones not in _HAN_DIGITS):
        return None
    return (10 if not tens else _HAN_DIGITS[tens] * 10) + (0 if not ones else _HAN_DIGITS[ones])


def _han_year(text: str) -> Optional[int]:
    """Convert a 4-char positional han year (二〇二六) to int."""
    if len(text) != 4:
        return None
    value = 0
    for char in text:
        if char not in _HAN_DIGITS:
            return None
        value = value * 10 + _HAN_DIGITS[char]
    return value


def _valid_date(year: int, month: int, day: int) -> bool:
    if not (1 <= month <= 12):
        return False
    return 1 <= day <= calendar.monthrange(year, month)[1]


def _valid_time(hour: int, minute: int, second: int = 0) -> bool:
    return 0 <= hour <= 23 and 0 <= minute <= 59 and 0 <= second <= 59


class ZhDateParser:
    """Parse Chinese Gregorian date expressions into datetime values.

    Args:
        no_year_policy: ``"current_year"`` (default) completes year-less
          expressions with the reference year and reports
          ``year_inferred=True``; ``"strict"`` returns ``value=None`` for
          them.
    """

    unsupported_count = 0
    rejected_count = 0

    def __init__(self, no_year_policy: str = "current_year", **config: Any) -> None:
        if no_year_policy not in ("current_year", "strict"):
            raise ValueError(
                "no_year_policy must be 'current_year' or 'strict', got %r" % no_year_policy)
        self.no_year_policy = no_year_policy
        self.config = config
        self.logger = get_logger("zh_date_parser")

    def parse(self, text: str, reference: Optional[datetime] = None) -> Optional[Dict[str, Any]]:
        """Parse the first Chinese date expression in ``text``.

        Returns a dict (fields per data-model.md) or ``None`` when the text
        carries no Chinese date pattern at all. Never raises on content.
        """
        if not isinstance(text, str) or not text:
            return None
        reference = reference or datetime.now()

        for pattern, label in _UNSUPPORTED_RES:
            match = pattern.search(text)
            if match:
                ZhDateParser.unsupported_count += 1
                return {
                    "value": None,
                    "matched_text": match.group(0),
                    "family": "unsupported",
                    "year_inferred": False,
                    "unsupported_matched": match.group(0),
                    "unsupported_kind": label,
                }

        for matcher, family in self._iter_family_matchers(reference):
            result = matcher(text, reference)
            if result is not None:
                result["family"] = family
                return result
        return None

    # -- family matchers, first-match-wins -------------------------------

    def _iter_family_matchers(self, reference):
        yield self._match_range, "range"
        yield self._match_full_time, "full_with_time"
        yield self._match_full, "full"
        yield self._match_han_full, "han_numeral"
        yield self._match_no_year, "no_year"
        yield self._match_year_only, "year_only"
        yield self._match_year_relative, "relative_year"
        yield self._match_relative, "relative"
        yield self._match_offset, "relative_offset"
        yield self._match_time_only, "with_time"

    def _match_range(self, text, reference):
        match = _RANGE_RE.search(text)
        if not match:
            return None
        y1, m1, d1, y2, m2, d2 = (int(g) for g in match.groups())
        base = {"matched_text": match.group(0), "year_inferred": False}
        if not (_valid_date(y1, m1, d1) and _valid_date(y2, m2, d2)):
            ZhDateParser.rejected_count += 1
            return dict(base, value=None)
        start = datetime(y1, m1, d1)
        end = datetime(y2, m2, d2)
        if end < start:
            ZhDateParser.rejected_count += 1
            return dict(base, value=None)
        return dict(base, value=start, value_end=end)

    def _match_year_only(self, text, reference):
        match = _YEAR_ONLY_RE.search(text)
        if not match:
            return None
        return {"matched_text": match.group(0), "year_inferred": False,
                "value": datetime(int(match.group(1)), 1, 1)}

    def _match_year_relative(self, text, reference):
        match = _YEAR_RELATIVE_RE.search(text)
        if not match:
            return None
        offset = _YEAR_RELATIVE_OFFSET[match.group(0)]
        return {"matched_text": match.group(0), "year_inferred": True,
                "value": datetime(reference.year + offset, 1, 1)}

    def _match_offset(self, text, reference):
        match = _OFFSET_RE.search(text)
        if not match:
            return None
        lead, number, unit, tail = match.groups()
        value = None
        if number.isdigit():
            count = int(number)
        elif number in _HAN_DIGITS:
            count = _HAN_DIGITS[number]
        elif number in _HAN_NUM_EXTRA:
            count = _HAN_NUM_EXTRA[number]
        else:
            count = _han_small_number(number)
        base = {"matched_text": match.group(0)}
        if count is None:
            ZhDateParser.rejected_count += 1
            return dict(base, value=None, year_inferred=False)
        direction = tail or lead or "前"
        days = _OFFSET_UNIT_DAYS[unit] * count
        signed = -days if direction == "前" else days
        return dict(base, value=reference + timedelta(days=signed), year_inferred=True)

    def _match_full_time(self, text, reference):
        match = _FULL_TIME_RE.search(text)
        if not match:
            return None
        year, month, day = int(match.group(1)), int(match.group(2)), int(match.group(3))
        hour, minute = int(match.group(4)), int(match.group(5))
        second = int(match.group(6) or 0)
        base = {"matched_text": match.group(0), "year_inferred": False}
        if not (_valid_date(year, month, day) and _valid_time(hour, minute, second)):
            ZhDateParser.rejected_count += 1
            return dict(base, value=None)
        return dict(base, value=datetime(year, month, day, hour, minute, second))

    def _match_full(self, text, reference):
        match = _FULL_RE.search(text)
        if not match:
            return None
        year, month, day = int(match.group(1)), int(match.group(2)), int(match.group(3))
        base = {"matched_text": match.group(0), "year_inferred": False}
        if not _valid_date(year, month, day):
            ZhDateParser.rejected_count += 1
            return dict(base, value=None)
        return dict(base, value=datetime(year, month, day))

    def _match_han_full(self, text, reference):
        match = _HAN_FULL_RE.search(text)
        if not match:
            return None
        year = _han_year(match.group(1))
        month = _han_small_number(match.group(2))
        day = _han_small_number(match.group(3))
        base = {"matched_text": match.group(0), "year_inferred": False}
        if year is None or month is None or day is None or not _valid_date(year, month, day):
            ZhDateParser.rejected_count += 1
            return dict(base, value=None)
        return dict(base, value=datetime(year, month, day))

    def _match_no_year(self, text, reference):
        match = _NO_YEAR_RE.search(text)
        if not match:
            return None
        month, day = int(match.group(1)), int(match.group(2))
        base = {"matched_text": match.group(0)}
        if self.no_year_policy == "strict":
            return dict(base, value=None, year_inferred=False)
        if not _valid_date(reference.year, month, day):
            ZhDateParser.rejected_count += 1
            return dict(base, value=None, year_inferred=False)
        return dict(base, value=datetime(reference.year, month, day), year_inferred=True)

    def _match_relative(self, text, reference):
        match = _RELATIVE_RE.search(text)
        if not match:
            return None
        token = match.group(0)
        base = {"matched_text": token, "year_inferred": True}
        offsets = {"今天": 0, "明天": 1, "昨天": -1, "前天": -2, "大前天": -3,
                   "后天": 2, "大后天": 3}
        if token in offsets:
            return dict(base, value=reference + timedelta(days=offsets[token]))
        # 下周X / 本周X / 这周X — Monday-based weekday
        weekday = _WEEKDAY_MAP[token[-1]]
        if token.startswith("下"):
            days_to_next_monday = (7 - reference.weekday()) % 7 or 7
            next_monday = reference + timedelta(days=days_to_next_monday)
            target = next_monday + timedelta(days=weekday)
        else:
            target = reference - timedelta(days=reference.weekday())  # this week's Monday
            target += timedelta(days=weekday)
        return dict(base, value=target)

    def _match_time_only(self, text, reference):
        match = _TIME_ONLY_RE.search(text)
        if not match:
            return None
        hour, minute = int(match.group(1)), int(match.group(2))
        base = {"matched_text": match.group(0), "year_inferred": True}
        if not _valid_time(hour, minute):
            ZhDateParser.rejected_count += 1
            return dict(base, value=None)
        return dict(base, value=reference.replace(hour=hour, minute=minute, second=0, microsecond=0))


# -- fork 扩展：中文路由的 DateNormalizer（继承，不改上游） -------------------

_ZH_HINT = re.compile(r"[年月日号时]|今天|明天|昨天|前天|后天|大前天|大后天|下周")


class ZhDateNormalizer:
    """带中文路由的日期规范化器（组合扩展，零侵入上游 DateNormalizer）。

    输入含汉字日期提示时先走 :class:`ZhDateParser`；未命中或无提示回退
    上游 :class:`~semantica.normalize.date_normalizer.DateNormalizer`
    （dateutil 路径，英文行为零变化）。输出形态与父类一致（ISO 字符串）。
    """

    def __init__(self, no_year_policy: str = "current_year", **config):
        from .date_normalizer import DateNormalizer

        self._fallback = DateNormalizer(**config)
        self._parser = ZhDateParser(no_year_policy=no_year_policy)

    def normalize_date(self, date_input, format: str = "ISO8601", timezone: str = "UTC", **options):
        value = None
        if isinstance(date_input, str) and _ZH_HINT.search(date_input):
            result = self._parser.parse(date_input)
            if result is not None and result.get("value") is not None:
                value = result["value"]
        if value is None:
            return self._fallback.normalize_date(
                date_input, format=format, timezone=timezone, **options)
        dt = value
        if timezone != "UTC":
            dt = self._fallback.timezone_normalizer.normalize_timezone(dt, timezone)
        else:
            dt = self._fallback.timezone_normalizer.convert_to_utc(dt)
        if format == "ISO8601":
            return dt.isoformat()
        if format == "date":
            return dt.date().isoformat()
        return dt.strftime(format)
