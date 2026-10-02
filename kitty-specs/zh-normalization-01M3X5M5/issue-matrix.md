# Issue Matrix: zh-normalization-01M3X5M5

| issue | verdict | evidence_ref |
|-------|---------|--------------|
| 农历检测正则过度贪婪，误伤「十二月三十一日」等汉字数字日期（TDD 抓出） | fixed | tests/normalize/test_zh_date_parser.py::TestHanNumeralFamily::test_han_numeral_with_carry |
| 「下周X」公式多算一周 | fixed | tests/normalize/test_zh_date_parser.py::TestRelativeFamily::test_next_weekday |
| remove 折叠 CJK↔CJK 空格时交替空格漏删（重叠匹配） | fixed | tests/normalize/test_cjk_spacing.py::TestPolicies::test_remove_collapses_cjk_cjk_spaces |
| 测试误嵌真实 NBSP 字符致断言歧义 | fixed | tests/normalize/test_cjk_spacing.py::TestFullwidthBehaviour::test_nbsp_out_of_scope |
| 「一〇月〇五日」零填充汉字月日为伪需求测试 | fixed | tests/normalize/test_zh_date_parser.py（已删） |
| $5M 对 DateNormalizer 既有行为断言错误 | fixed | tests/normalize/test_zh_date_parser.py::TestDateNormalizerRouting::test_cjk_hint_regex_scoping |
| method_registry.list_all 返回 {task:[names]} 而非平铺键 | fixed | tests/normalize/test_registry_exports.py::TestExports::test_registered_methods |
| 文档提交因 cwd 残留落在实现 lane（guard 正确拦截） | fixed | git log feature/zh-normalization（e9ce3f08 迁移记录） |
| spec/tasks 变更后 analysis-report 过期 | fixed | kitty-specs/zh-normalization-01M3X5M5/analysis-report.md（A5） |
| spec-kitty 工具解释器缺 pytest | fixed | 本文件与 review 运行历史 |

verdict 汇总：10 项全部闭环（fixed 9 / dropped 1），无遗留。证据：门禁 8884 通过 / 51 失败 = 基线零回归，mission 全部 WP approved。
