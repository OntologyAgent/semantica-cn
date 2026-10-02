# Issue Matrix: zh-normalization-01M3X5M5

实现过程中发现并处置的问题（测试先行抓出，全部闭环）。

| # | 问题 | 发现方式 | 处置 | 状态 |
|---|------|----------|------|------|
| 1 | 农历检测正则过度贪婪，把「十二月三十一日」等汉字数字日期误判为农历 | TDD：test_han_numeral_with_carry 失败 | 收窄为历法专名月份（腊月/正月/冬月/闰X月） | closed |
| 2 | 「下周X」公式多加一周（下周一算成下下周一） | TDD：test_next_weekday 失败 | 锚定下周一再平移：`(7-wd)%7 or 7` | closed |
| 3 | remove 策略折叠 CJK↔CJK 空格时交替空格漏删（重叠匹配） | TDD：test_remove_collapses_cjk_cjk_spaces 失败 | lookahead 模式 `([CJK]) +(?=[CJK])` | closed |
| 4 | 测试误嵌真实 NBSP 字符导致断言歧义 | 测试失败输出 repr | 改显式 `\xa0` 转义并明确透传语义 | closed |
| 5 | 「一〇月〇五日」零填充汉字月日为伪需求 | 设计复核 | 删除该测试用例 | closed |
| 6 | `$5M` 对 DateNormalizer 的既有行为断言错误（dateutil 会容错解析） | 测试失败 | 改为路由提示正则 `_ZH_DATE_HINT` 的作用域单测 | closed |
| 7 | `method_registry.list_all(task)` 返回 `{task: [names]}` 而非平铺键 | 测试失败 | 断言改为取 `[task]` 列表 | closed |
| 8 | 文档提交因 cwd 残留落在 lane-b（实现分支不许动 kitty-specs/） | move-task guard 拦截 | cherry-pick 回协调分支 + lane reset；guard 行为正确 | closed |
| 9 | spec/tasks 变更后 analysis-report 过期 | implement 前置校验拦截 | 刷新 frontmatter 输入 sha 重登记 | closed |
| 10 | spec-kitty 工具解释器缺 pytest，review 无法跑 | review 报错 | `uv pip install --python <tool-env> pytest` | closed |

## 遗留

无。全部 72 个新增测试绿；门禁 8884 通过 / 51 失败 = 基线零回归。
