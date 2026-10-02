# Data Model: 中文规范化

**Mission**: zh-normalization-01M3X5M5 | **Date**: 2026-10-02

无数据库实体；数据模型为两个规范化器的输入/输出契约。

## Entity 1: CJK 空格规范化结果（CJKSpacingResult）

**表示**: `CJKSpacingNormalizer.normalize(text) -> str`（简单路径）与 `normalize_detailed(text) -> dict`

| 字段 | 类型 | 约束 |
|------|------|------|
| normalized | str | 必填；幂等（normalize(normalize(x)) == normalize(x)） |
| boundaries_adjusted | int | 必填 ≥0；本次插入+删除的边界数 |
| policy | str | "add" \| "remove" \| "preserve"（默认 add） |

**不变量**:
- text 不含 CJK 表意文字与全角字符时，normalized 与输入 byte-identical
- U+3000 全角空格始终归一为半角空格（三种策略下都执行）

## Entity 2: 中文日期解析结果（ZhDateResult）

**表示**: `ZhDateParser.parse(text, reference=None) -> dict | None`

| 字段 | 类型 | 约束 |
|------|------|------|
| value | datetime \| None | 命中时必填；非法日期（如 2月30日）为 None |
| matched_text | str | 命中时必填；原文命中的日期子串 |
| family | str | "full" \| "no_year" \| "with_time" \| "han_numeral" \| "relative" |
| year_inferred | bool | 无年份且按策略补当前年时为 True |
| unsupported_matched | str | 不支持历法命中时携带原文子串（value 为 None）

**不变量**:
- parse 返回 None 且 unsupported_matched 为空 ⇔ 文本无中文日期模式
- 非法日历值（月>12、日溢出）一律 value=None，不做溢出归一
- 与 dateutil 路径互斥：含汉字年月日模式由本解析器独占，未命中回退

## 关系

- `DateNormalizer.normalize_date` 内部路由：中文模式 → ZhDateParser；否则原 dateutil 路径（行为零回改）
- 两规范化器经 `method_registry.register("text"|"date", "cjk_spacing"|"zh_date", fn)` 进入注册表
