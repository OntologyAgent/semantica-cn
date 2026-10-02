# Contract: CJKSpacingNormalizer / ZhDateParser 公共 API

**Mission**: zh-normalization-01M3X5M5

两个新公共面，实现与调用方（含测试、后续 LLM 抽取器流水线）以此为准。

## CJKSpacingNormalizer

```python
from semantica.normalize import CJKSpacingNormalizer

n = CJKSpacingNormalizer(policy="add")   # "add" | "remove" | "preserve"，默认 "add"
n.normalize("Semantica知识图谱")          # -> "Semantica 知识图谱"
n.normalize_detailed("AI驱动")            # -> {"normalized": "AI 驱动", "boundaries_adjusted": 1, "policy": "add"}
```

| 形态 | 语义 |
|------|------|
| `normalize(str) -> str` | 幂等；纯西文输入 byte-identical |
| `normalize_detailed(str) -> dict` | 附带调整计数（字段见 data-model.md） |

## ZhDateParser

```python
from semantica.normalize import ZhDateParser

p = ZhDateParser(no_year_policy="current_year")  # "current_year" | "strict"，默认 "current_year"
p.parse("2026年10月2日")            # -> {"value": datetime(2026,10,2), "matched_text": ..., "family": "full", "year_inferred": False}
p.parse("10月2日")                   # -> year_inferred=True, value=当年
p.parse("腊月初八")                   # -> {"value": None, "unsupported_matched": "腊月初八", ...}
p.parse("hello")                     # -> None
p.parse("2025年1月1日至2025年12月31日")  # -> {"value": datetime(2025,1,1), "value_end": datetime(2025,12,31), "family": "range", ...}
p.parse("2025年")                      # -> {"value": datetime(2025,1,1), "family": "year_only", ...}
p.parse("前三个自然月", reference=datetime(2025,1,1))  # -> 90 天前（relative_offset，月按 30 天近似）
```

## ZhDateNormalizer（组合扩展；2026-10-02 OCP 重构后形态）

```python
from semantica.normalize import ZhDateNormalizer

ZhDateNormalizer().normalize_date("2026年10月2日")  # 中文命中走 ZhDateParser，ISO 输出
ZhDateNormalizer().normalize_date("2026-10-02")     # 回退父类 dateutil，行为零回改
```

上游 `DateNormalizer` 源码零改动（中文直取一律用 ZhDateNormalizer 或 `method="cn_date"`）。

## 注册表

```python
# 包导入时已自动注册（semantica/normalize/__init__.py）：
#   method_registry.register("text", "cjk_spacing", _cjk_spacing_method)
#   method_registry.register("date", "cn_date", _cn_date_method)
# 分发用法：
methods.normalize_text("Semantica知识图谱", method="cjk_spacing")      # -> "Semantica 知识图谱"
methods.normalize_date("2026年10月2日", method="cn_date", format="date")  # -> "2026-10-02"
```

**兼容性约束**: 两个新类从 `semantica.normalize.__init__` 导出；不修改任何既有公共签名；失败语义遵循 FR-004（不抛异常中断流水线）。
