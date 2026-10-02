---
schema_version: 1
artifact_type: spec-kitty.analysis-report
command: /spec-kitty.analyze
mission_slug: zh-normalization-01M3X5M5
mission_id: 01M3X5M5MBTGRTS6PKBTEV86EC
generated_at: '2026-10-02T03:35:53.511659+00:00'
analyzer_agent: unknown
input_artifacts:
  spec.md:
    path: /Users/luofisher/ToolsChain/semantica-cn/kitty-specs/zh-normalization-01M3X5M5/spec.md
    sha256: fdcc917c8026fa549970708de0e9ca396f73eeef6343c32efa78d3e5cc36449b
  plan.md:
    path: /Users/luofisher/ToolsChain/semantica-cn/kitty-specs/zh-normalization-01M3X5M5/plan.md
    sha256: e1e9f195b9a91d05f2810628e8ab60a2843e9be8fc73f7f3a0498aa8f351db21
  tasks.md:
    path: /Users/luofisher/ToolsChain/semantica-cn/kitty-specs/zh-normalization-01M3X5M5/tasks.md
    sha256: 7ef9d6d6ad599a18f3fb475fc65c2a17b18a19f0708c00377c19d06b58e2730f
  charter:
    path: /Users/luofisher/ToolsChain/semantica-cn/.kittify/charter/charter.md
    sha256: a5e01a009b82bb321c397f1f4d566511a1a4713370ab47480516eb838cffce67
verdict: unknown
issue_counts:
  low:
  info:
  critical:
  medium:
  high:
findings: []
---

---
schema_version: 1
artifact_type: spec-kitty.analysis-report
command: /spec-kitty.analyze
mission_slug: zh-normalization-01M3X5M5
mission_id: 01M3X5M5MBTGRTS6PKBTEV86EC
generated_at: '2026-10-02T11:35:27.617346+08:00'
analyzer_agent: python-pedro
input_artifacts:
  spec.md:
    path: kitty-specs/zh-normalization-01M3X5M5/spec.md
    sha256: fdcc917c8026fa549970708de0e9ca396f73eeef6343c32efa78d3e5cc36449b
  plan.md:
    path: kitty-specs/zh-normalization-01M3X5M5/plan.md
    sha256: e1e9f195b9a91d05f2810628e8ab60a2843e9be8fc73f7f3a0498aa8f351db21
  tasks.md:
    path: kitty-specs/zh-normalization-01M3X5M5/tasks.md
    sha256: 1ad605e489526cf3d75150ac0880bc92fe89f74ddc3bd02c781cea694990380f
  charter:
    path: .kittify/charter/charter.md
    sha256: a5e01a009b82bb321c397f1f4d566511a1a4713370ab47480516eb838cffce67
verdict: ready
issue_counts:
  medium: 0
  low: 1
---



# Analysis Report: zh-normalization 实现前分析

**Mission**: zh-normalization-01M3X5M5 | **Date**: 2026-10-02 | **Analyst**: python-pedro（宿主执行）

## A1: 接入点核实（代码事实）

1. **DateNormalizer.normalize_date**（date_normalizer.py:102）
   - 签名：`(date_input, format="ISO8601", timezone="UTC", **options) -> str`——**返回 ISO 字符串而非 datetime**（contracts/public-api.md 的「返回类型一致」即指此：路由后仍走既有 timezone→format 管线）
   - 现路径：str → dateutil.parse → 失败则 RelativeDateProcessor（英文）→ 再失败抛 ValidationError
   - 中文路由插入点：`isinstance(date_input, str)` 分支内、dateutil.parse **之前**：含汉字日期模式 → `ZhDateParser.parse()` 取 value → 成功则以 datetime 进入既有 timezone/format 管线（naive datetime 的 UTC 处理与英文路径一致）；value=None/未命中 → 原 dateutil 路径不动
   - 风险修正：契约示例 `DateNormalizer().normalize_date("2026年10月2日")` 期望返回 ISO 字符串（不是 datetime）——实现与测试以此为准
2. **method_registry**（registry.py:60/88）：`register(task, name, method_func)` classmethod；`list_all(task)` 返回 `Dict[str, List[str]]`。注册无顺序副作用，组合次序由调用方决定
3. **__init__.py**：按模块 `from .X import ...` 集中导出；新增两行导入 + docstring 的 Main Classes 增补即可

## A2: 现有测试基线

- `tests/normalize/test_date_normalizer.py` 现有英文/dateutil 用例构成回退路径的回归保护；实现前先全量跑一遍确认起点全绿（`uv run --frozen pytest tests/normalize/ -q`）
- 无任何既有测试覆盖中文输入 → 新增用例无语义冲突

## A3: 与既有模块的冲突排查

- `text_normalizer.py`：空白归一（多空格→单空格、全角空格**未**处理）——CJKSpacingNormalizer 的 U+3000 归一与其无重叠（text_normalizer 只处理 \u0020 系）；不修改 text_normalizer（零回改边界）
- `language_detector.py`：langdetect 依赖已在 [all]（nlp-langdetect extra，上游 #1823）——与本次无关但确认无符号冲突
- `number_normalizer`/`currency_normalizer`：`$5M`、`10月2日` 中的数字不受本次改动影响（我们只在日期正则命中时消费子串）

## A4: 实现顺序与验证策略

- WP01（cjk_spacing）与 WP02（zh_date_parser + date_normalizer 路由）并行无共享文件；WP03 收口
- 每个 WP 完成即跑自身测试 + `tests/normalize/` 全量；最终 run_gate.sh（基线 51）
- 幂等性与 byte-identical 用参数化用例固化，防回归

## 结论

无阻塞性发现；一处契约澄清（normalize_date 返回 str）已并入 A1，实现按此执行。

## A5: 增量分析（2026-10-02 第二次，notebook 家族吸收后）

- WP01 增补：remove 策略折叠 CJK↔CJK 空格（lookahead 消除交替空格重叠），add/preserve 保持 pangu 语义
- WP02 家族扩展后 retainer：区间家族引入 value_end 字段；年度相对词锚定参考年 1 月 1 日；数量偏移月按 30 天近似（与 notebook 一致，契约已注明）
- WP03 注册名将采用 notebook 约定 "cn_date"（而非契约初稿的 zh_date），契约随 WP03 一并修正
- 结论：ready，无新增阻塞
