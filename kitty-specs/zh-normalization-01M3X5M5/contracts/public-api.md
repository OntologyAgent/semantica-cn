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
```

## DateNormalizer 路由（扩展点）

```python
DateNormalizer().normalize_date("2026年10月2日")   # 内部走 ZhDateParser，返回类型与既有路径一致
DateNormalizer().normalize_date("2026-10-02")      # 原 dateutil 路径，行为零回改
```

## 注册表

```python
method_registry.register("text", "cjk_spacing", CJKSpacingNormalizer().normalize)
method_registry.register("date", "zh_date", lambda s, **kw: (ZhDateParser().parse(s) or {}).get("value"))
```

**兼容性约束**: 两个新类从 `semantica.normalize.__init__` 导出；不修改任何既有公共签名；失败语义遵循 FR-004（不抛异常中断流水线）。
