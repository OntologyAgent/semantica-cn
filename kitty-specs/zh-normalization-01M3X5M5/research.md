# Research: 中文规范化（CJK 空格与中文日期）

**Mission**: zh-normalization-01M3X5M5 | **Date**: 2026-10-02

## R1: 既有代码事实（evidence: 仓库源码）

- `semantica/normalize/` 已有：`text_normalizer.py`（Unicode/空白/大小写，无 CJK 边界感知）、`date_normalizer.py`（`DateNormalizer.normalize_date` 走 dateutil + `RelativeDateProcessor` 处理英文相对日期）、`registry.py`（`method_registry.register(task, name, fn)` 七类：text/entity/date/number/clean/language/encoding）
- `DateNormalizer.__init__(config)`、`normalize_date(date_input, **options)` 为公共形态；中文扩展需保持返回类型一致（datetime/str 与现路径相同）
- 测试形态：`tests/normalize/test_<module>.py`，unittest.TestCase 风格（见 test_number_normalizer.py）
- 依赖约束：normalize 模块核心零第三方依赖（dateutil 为既有例外）；charter 要求只用项目声明技术

## R2: CJK 边界字符类（Unicode 区段事实）

| 类别 | 区段 | 处理 |
|------|------|------|
| CJK 表意文字 | U+4E00–U+9FFF、U+3400–U+4DBF（Ext A）、U+F900–U+FAFF（兼容） | 参与「中文侧」边界判定 |
| 中文标点 | U+3001–U+303F（、。〈〉《》）、U+FF01–U+FF5E（全角 ASCII！？，（）） | 全角标点属「中文侧」；全角空格 U+3000 单独归一 |
| 拉丁字母数字 | U+0041–U+005A、U+0061–U+007A、U+0030–U+0039 | 「西文侧」 |
- 边界规则（pangu 语义）：西文字符与 CJK 表意文字相邻处插/删空格；**全角标点与汉字之间不加**、全角标点与西文之间按策略处理（默认不加，避免 `Semantica！` → `Semantica ！` 的过度修正——与 pangu 默认一致）
- 幂等性约束：add 策略运行两次结果相同（插入后不产生新边界）

## R3: 中文日期格式清单（样例即测试集种子）

| 家族 | 样例 | 解析目标 |
|------|------|----------|
| 完整日期 | `2026年10月2日`、`2026年10月2号` | datetime(2026,10,2) |
| 无年份 | `10月2日`、`10月2号` | 策略：默认当前年 / 严格拒绝（可配） |
| 带时间 | `2026年10月2日 14:30`、`14时30分` | datetime 含时间 |
| 数字变体 | `二〇二六年十月二日`（汉字数字） | datetime（汉字数字转换） |
| 相对 | `今天/明天/昨天/前天/后天/下周X/大后天` | 相对参考时间 |
- 不支持（原样保留 + 计数）：农历（`腊月初八`）、民国纪年（`民国115年`）、节气

## R4: 边界与风险样例

- `支付$5M，于2026年10月2日到账` → 日期命中、货币走既有 currency_normalizer、CJK 空格规则不破坏数字与单位
- `Semantica知识图谱` ⇄ `Semantica 知识图谱`；`AI驱动` ⇄ `AI 驱动`
- 纯英文 `Hello world 123` → byte-identical（R2 类判定保证）
- `2月30日` → 非法日期：拒绝并计数（不做 3 月 2 日溢出归一）
- 与 dateutil 路径边界：输入含 `年/月/日` 汉字模式 → 走中文路径；否则原 dateutil 路径，行为零回改
