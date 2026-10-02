# Tasks: 中文规范化（CJK 空格与中文日期）

**Mission**: zh-normalization-01M3X5M5
**Branch**: feature/zh-normalization
**Generated**: 2026-10-02

## Subtask Index

| ID | Description | WP | Parallel | Status |
|----|-------------|----|----------|--------|
| T001 | cjk_spacing.py：Unicode 字符类判定（CJK 表意/全角标点/西文）+ add/remove/preserve 三策略幂等实现 + U+3000 全角空格归一 | WP01 |  | pending |
| T002 | normalize_detailed 计数路径 + 纯西文 byte-identical 保障 | WP01 |  | pending |
| T003 | test_cjk_spacing.py：幂等性/三策略/R2 边界样例/全角标点不过度修正 | WP01 |  | pending |
| T004 | zh_date_parser.py：R3 格式家族正则集（full/no_year/with_time/han_numeral/relative）+ 汉字数字转换 | WP02 |  | pending |
| T005 | no_year_policy 配置（current_year/strict）+ 非法日期拒绝 + 不支持历法原样保留与计数 | WP02 |  | pending |
| T006 | DateNormalizer 路由扩展：中文模式独占，未命中回退 dateutil，既有行为零回改 | WP02 |  | pending |
| T007 | test_zh_date_parser.py + test_date_normalizer.py 中文与回退用例 | WP02 |  | pending |
| T008 | method_registry 注册（text/cjk_spacing、date/zh_date）+ __init__ 公共导出（契约对齐 contracts/public-api.md） | WP03 | [P] | pending |
| T009 | test_integration.py 扩展：空格→日期组合流水线语义 + 单独可调用 | WP03 | [P] | pending |
| T010 | 全量门禁 run_gate.sh（基线 51 外零新增）+ quickstart §3 走查收口 | WP03 |  | pending |

## WP01 — CJK 空格规范化器

**Prompt**: `tasks/WP01-cjk-spacing.md`
**Goal**: 交付 `CJKSpacingNormalizer`（契约见 contracts/public-api.md），三策略幂等、纯西文零改动
**Priority**: P0（串行第一棒）
**Independent test**: `uv run --frozen pytest tests/normalize/test_cjk_spacing.py -q` 全绿；`normalize(normalize(x)) == normalize(x)` 对全部测试样例成立
**Estimated prompt size**: ~150 lines

- [x] T001 cjk_spacing.py：Unicode 字符类判定 + 三策略幂等实现 + U+3000 归一 (WP01)
- [x] T002 normalize_detailed 计数路径 + 纯西文 byte-identical 保障 (WP01)
- [x] T003 test_cjk_spacing.py：幂等性/三策略/R2 边界样例/全角标点不过度修正 (WP01)

**Dependencies**: none
**Parallel opportunities**: 无（WP02 可并行开发但 WP03 依赖两者）
**Risks**: 幂等性与「过度修正」边界（全角标点默认不与西文加空格）；U+3000 归一在 remove 策略下与边界删除的交互顺序

## WP02 — 中文日期解析器

**Prompt**: `tasks/WP02-zh-date-parser.md`
**Goal**: 交付 `ZhDateParser` + `DateNormalizer` 中文路由，失败语义遵循 FR-004（不抛异常、原样保留计数）
**Priority**: P0（与 WP01 可并行）
**Independent test**: `uv run --frozen pytest tests/normalize/test_zh_date_parser.py tests/normalize/test_date_normalizer.py -q` 全绿；既有英文用例零回改
**Estimated prompt size**: ~180 lines

- [ ] T004 zh_date_parser.py：R3 格式家族正则集 + 汉字数字转换 (WP02)
- [ ] T005 no_year_policy 配置 + 非法日期拒绝 + 不支持历法保留计数 (WP02)
- [ ] T006 DateNormalizer 路由扩展：中文模式独占，未命中回退 (WP02)
- [ ] T007 test_zh_date_parser.py + test_date_normalizer.py 中文与回退用例 (WP02)

**Dependencies**: none（独立于 WP01）
**Parallel opportunities**: 与 WP01 并行
**Risks**: 与 dateutil 回退路径的互斥判定（含 `年/月/日` 汉字即独占）；`2月30日` 拒绝而非溢出；相对日期参考时间默认值

## WP03 — 注册与集成验收

**Prompt**: `tasks/WP03-registry-integration.md`
**Goal**: 注册表接入 + 组合语义 + 门禁收口（FR-003/FR-004 全量验证）
**Priority**: P1（依赖 WP01+WP02）
**Independent test**: `bash tools/nightly/run_gate.sh` exit 0；quickstart §3 走查通过
**Estimated prompt size**: ~120 lines

- [ ] T008 method_registry 注册 + __init__ 公共导出 (WP03)
- [ ] T009 test_integration.py 扩展：组合流水线 + 单独调用 (WP03)
- [ ] T010 全量门禁 + quickstart §3 走查收口 (WP03)

**Dependencies**: WP01、WP02
**Parallel opportunities**: T008 与 T009 可并行
**Risks**: 注册顺序语义（文本规范化先于日期解析的组合次序约定）

---

**spec 覆盖**：FR-001 → WP01；FR-002/FR-004 → WP02；FR-003 → WP03（T009 组合语义 + T008 注册）。
