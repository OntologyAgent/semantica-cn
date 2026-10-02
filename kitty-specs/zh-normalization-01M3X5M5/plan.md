# Implementation Plan: 中文规范化（CJK 空格与中文日期）

**Branch**: `feature/zh-normalization` | **Date**: 2026-10-02 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/kitty-specs/zh-normalization-01M3X5M5/spec.md`

## Summary

为 `semantica/normalize/` 补两类中文规范化能力：CJK 空格规范化（全角/半角统一、中英文边界加/去空格，策略可配置）与中文日期解析（`2026年10月2日`、无年份格式、相对日期）。技术路线为纯标准库实现（`re` + `unicodedata` + `datetime`），CJK 空格挂载到既有文本规范化链路，中文日期作为 `DateNormalizer` 的中文扩展并与现有 dateutil 路径并存回退。

## Technical Context

**Language/Version**: Python 3.10–3.13（仓库 requires-python；仅用标准库，不加新依赖）
**Primary Dependencies**: 标准库 `re`、`unicodedata`、`datetime`；既有 `dateutil`（date_normalizer.py 已依赖，中文路径不新增）
**Storage**: N/A（纯函数式规范化器）
**Testing**: 仓库既有 pytest 体系，`tests/normalize/` 下按模块建测试文件；mock 不需要（无外部服务）；夜间门禁基线 51 条已知失败外零新增
**Target Platform**: 跨平台（PyPI 分发，Linux/macOS/Windows）
**Project Type**: single（semantica 包内模块扩展）
**Performance Goals**: 常规文本（≤10k 字符）单次规范化 <10ms（纯正则，无回溯爆炸模式）
**Constraints**: 零新增第三方依赖；纯非中文文本 byte-identical（FR-001）
**Scale/Scope**: 2 个新模块 + date_normalizer 扩展 + 注册表接入，测试用例约 60–80 个

## Charter Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- 语言/框架：Python + 仓库既有 pytest ✅（charter: 只用项目声明技术）
- 变更可预测可评审：纯新增模块 + 明确扩展点，无行为回改 ✅
- 质量门：沿用 tools/nightly/run_gate.sh 基线比对 ✅

## Project Structure

### Documentation (this mission)

```
kitty-specs/zh-normalization-01M3X5M5/
├── plan.md              # 本文件
├── research.md          # Phase 0（中文格式清单与边界样例集）
├── data-model.md        # Phase 1（规范化结果结构）
├── quickstart.md        # Phase 1
├── contracts/           # Phase 1（公共 API 契约）
└── tasks.md             # Phase 2（/spec-kitty.tasks 产出）
```

### Source Code (repository root)

```
semantica/normalize/
├── cjk_spacing.py       # 新增：CJKSpacingNormalizer（FR-001）
├── zh_date_parser.py    # 新增：中文日期解析（FR-002/FR-004）
├── date_normalizer.py   # 扩展：中文探测入口 + 回退既有 dateutil 路径
├── registry.py          # 扩展：注册两个新规范化器
└── __init__.py          # 导出新 API

tests/normalize/
├── test_cjk_spacing.py  # 新增
└── test_zh_date_parser.py  # 新增（+ test_date_normalizer.py 补中文用例）
```

**Structure Decision**: 单项目结构，全部落在既有 `semantica/normalize/` 包内，不新建顶层目录。

## Complexity Tracking

*无 charter 违规需要豁免。*

## Implementation Concern Map

### IC-01 — CJK 边界判定与空格策略

- **Purpose**: 定义「中英文/数字边界」的字符类判定（CJK 表意文字、全角标点 vs 拉丁字母数字）与三种策略（add/remove/preserve）的幂等实现
- **Relevant requirements**: FR-001
- **Affected surfaces**: `semantica/normalize/cjk_spacing.py`、`text_normalizer.py`（可选接入点）
- **Sequencing/depends-on**: none
- **Risks**: 幂等性（二次运行不变形）；全角空格 U+3000 与 NBSP 的归类决策；纯英文零改动需逐字节验证

### IC-02 — 中文日期模式集与解析

- **Purpose**: 覆盖 `YYYY年M月D日`、`M月D日`、ISO/横线格式、相对日期（今天/明天/下周X/前天）的解析；无年份策略（默认当前年，可配严格拒绝）；不支持格式原样保留并计数（FR-004）
- **Relevant requirements**: FR-002、FR-004
- **Affected surfaces**: `semantica/normalize/zh_date_parser.py`、`date_normalizer.py`
- **Sequencing/depends-on**: none
- **Risks**: 与既有英文相对日期解析的职责边界（中文表达式优先走新路径，未命中回退 dateutil）；`2月30日` 等非法日期的错误语义（拒绝 vs 溢出规范化）

### IC-03 — 流水线接入与注册

- **Purpose**: 两个规范化器接入 `registry.py` 与组合调用（可单独调用、可进 normalize 流水线），输出类型与既有 normalizer 一致
- **Relevant requirements**: FR-003
- **Affected surfaces**: `registry.py`、`__init__.py`、`tests/normalize/test_integration.py`
- **Sequencing/depends-on**: IC-01、IC-02
- **Risks**: 注册顺序与既有 normalizer 的组合语义（文本规范化先于日期解析）
