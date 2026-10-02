---
title: 中文规范化
description: CJK 空格与中文日期——semantica-cn fork 的中文增强规范化器。
source: reference/zh-normalization.md
source_version: cfd0097029a9647615dc5e67eb6c29d6cbac5ef3
icon: "languages"
---

# 中文规范化（fork 增强）

> 本页是 **semantica-cn fork 原生能力**（上游 semantica 无此模块），覆盖两块：CJK 空格规范化与中文日期解析。均为纯标准库实现，零新增依赖。

## CJK 空格规范化 `CJKSpacingNormalizer`

三种策略，幂等设计（跑两遍结果不变）：

```python
from semantica.normalize import CJKSpacingNormalizer

n = CJKSpacingNormalizer()                      # policy="add"（默认，pangu 风格）
n.normalize("Semantica知识图谱")                 # -> "Semantica 知识图谱"

r = CJKSpacingNormalizer(policy="remove")       # 删空格（省 token 主用途）
r.normalize("知 识 图 谱，AI 驱动")              # -> "知识图谱，AI驱动"

p = CJKSpacingNormalizer(policy="preserve")     # 只归一 U+3000 全角空格
```

**remove 策略**在中文边界和 CJK 相邻空格上都删除——PDF 抽取噪声（NFKC 之后残留的中文字间空格）一次清干净：

```python
t = unicodedata.normalize("NFKC", raw_text)
t = CJKSpacingNormalizer(policy="remove").normalize(t)
```

细节：`normalize_detailed(text)` 返回 `{normalized, boundaries_adjusted, policy}`；纯西文输入 byte-identical；全角标点默认不与西文加空格（避免 `Semantica！` 的过度修正）；NBSP 透传。

**Markdown 语法完整保留**（`preserve_markdown=True` 默认开，按 CommonMark 语义）：

- 围栏代码块（``` / ~~~）与缩进代码块（≥4 空格）内容整段原样
- 行内代码 span（\`…\`）内容原样
- 行首块级标记（`#{1,6}` 标题、`>` 引用、`-`/`*`/`+`/`1.` 列表）后的空格保留——`## 折扣政策` 不会被吃成 `##折扣政策`，`split_by_heading` / `find("## N. …")` 不受影响
- 强调标记与内容之间不插/删空格：add 不会把 `**加粗**` 改成 `** 加粗 **`（会破坏渲染）；`**加粗 术语**` 的标记结构原样、内容照常归一
- 链接 `[文本](url)` 不受影响
- `*` `#` `>` 在 Markdown 语境下不参与 CJK 边界判定（行中如 `版本#号` 随之不动，属可接受代价）
- `preserve_markdown=False` 恢复逐字符处理（旧行为）

## 中文日期解析 `ZhDateParser`

```python
from semantica.normalize import ZhDateParser
from datetime import datetime

p = ZhDateParser()                               # no_year_policy="current_year"
p.parse("2026年10月2日")                         # {"value": datetime(2026,10,2), "family": "full", ...}
p.parse("2026年10月2日 14:30")                   # family="full_with_time"
p.parse("二〇二六年十月二日")                     # family="han_numeral"（汉字数字）
p.parse("10月2日")                               # year_inferred=True
p.parse("2025年1月1日至2025年12月31日")          # {"value": start, "value_end": end, "family": "range"}
p.parse("2025年")                                # family="year_only" -> datetime(2025,1,1)
p.parse("去年", reference=datetime(2026,10,2))   # -> datetime(2025,1,1)
p.parse("前三个自然月", reference=datetime(2025,1,1))  # -> 90 天前（月按 30 天近似）
p.parse("下周Monday".replace("Monday","一"))      # 周一锚定的下周X
```

失败语义（不抛内容异常）：

- 非法日期（`2月30日`）→ `value=None`，**不做溢出归一**
- 不支持历法（`腊月初八`、`民国115年`）→ 原样保留，`unsupported_matched` 携带子串，类计数器递增
- 无任何中文日期模式 → 返回 `None`

`no_year_policy="strict"` 时无年份表达式直接拒绝（value=None）。

## 方法分发入口

包导入时已注册到 `method_registry`，无需手动注册：

```python
from semantica.normalize import methods

methods.normalize_text("Semantica知识图谱", method="cjk_spacing")            # add
methods.normalize_text("知 识", method="cjk_spacing", policy="remove")       # remove
methods.normalize_date("2026年10月2日", method="cn_date", format="date")      # "2026-10-02"
```

`cn_date` 无可解析模式时抛 `ValueError`（不静默返回原文）。

需要 `DateNormalizer` 直取中文时用 fork 扩展类 `ZhDateNormalizer`（组合实现，上游 `DateNormalizer` 源码零改动）——输入含汉字日期特征时先走中文解析，未命中回退父类 dateutil 路径：

```python
from semantica.normalize import ZhDateNormalizer

ZhDateNormalizer().normalize_date("2026年10月2日")   # -> "2026-10-02T00:00:00+00:00"
ZhDateNormalizer().normalize_date("2023-01-15")      # 回退父类，行为不变
```

## 边界速查

| 场景 | 行为 |
|------|------|
| 纯英文/纯数字文本 | 零改动（byte-identical） |
| `2月30日` | value=None，拒绝 |
| 农历/民国纪年 | 原样保留 + 计数 |
| 频率表达式（每季度→P3M） | 不在范围（非日期语义） |
| 时区 | 沿用项目既有时区约定（naive 与 dateutil 路径同待遇） |

## 相关链接

- Cookbook：Cookbook 示例：cookbook_zh/introduction/15_Chinese_Normalization.ipynb
- 上游规范化参考：[Normalization](./normalize.md)
