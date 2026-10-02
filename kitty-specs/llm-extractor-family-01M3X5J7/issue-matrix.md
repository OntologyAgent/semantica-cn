# Issue Matrix: llm-extractor-family-01M3X5J7

| issue | verdict | evidence_ref |
|-------|---------|--------------|
| methods.py 多轮脚本编辑破坏缩进（cwd 重置导致 checkout 未作用于 lane） | fixed | git -C 固定路径重做；AST parse 校验后落盘 |
| prompt 替换分支缩进与 prompt 赋值层级不一致（try 内 8 空格 vs 函数级 4 空格各点不同） | fixed | insert_branch 按各赋值行实测缩进插入；AST 通过 |
| 测试 mock 用 MagicMock 属性致类级路径解析失败 | fixed | 改用真实 pydantic schema 对象（EntitiesResponse 等） |
| 类级测试与直调测试共享缓存键（api_key 被安全缓存排除、文本相同） | fixed | 测试文本改运行时 uuid 隔离 |
| extract_relations_llm 直调漏传必填 entities | fixed | 提供 _real_entities() |
| notebook 别名替换的「前后非汉字」规则过堵（默沙东与… 的正常替换被拦） | fixed | 改为规范名区间保护：alias 出现处落在任一 canonical 内才跳过 | tests/semantic_extract/test_coref_llm.py::TestResolveAliasesLLM::test_substring_protection |
| WP03 approved 前置校验要求 lane-c rebase 协调分支 | fixed | 按提示 rebase 后 move 成功 |
| merge squash 报 no changes（恢复中断态） | fixed | merge --abort 后以 --strategy merge 完成 |
| spec-kitty 工具解释器缺 pytest（沿 zh-normalization 遗留） | verified-already-fixed | 上 mission 已装入工具环境 |
