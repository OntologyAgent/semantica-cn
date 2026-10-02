# Specification: 中文规范化（CJK 空格与中文日期）

**Mission**: `zh-normalization-01M3X5M5` · software-dev · single_branch
**Branch contract**: 规划与实现均在 `feature/zh-normalization`，mission merge 时回 `main`
**Date**: 2026-10-02
**Status**: backlog（specify 完成待启动 plan/tasks；本文为路线图待办的规格化记录）

## Overview

`semantica/normalize/` 已有数字、货币等规范化器（number_normalizer、currency_normalizer 等），但缺少中文文本特有两类规范化能力。本 mission 补齐：

1. **CJK 空格规范化**
   - 全角/半角空格统一处理（含 U+3000 全角空格、全角 ASCII 空白）
   - 中英文混排边界自动加空格（pangu 风格）：`Semantica知识图谱` ↔ `Semantica 知识图谱`
   - 可选策略：规范化为「加空格」/「去空格」/「不动」，默认加空格
2. **中文日期解析**
   - 公文/自然语言格式归一：`2026年10月2日`、`2026-10-02`、`十月二日`、`本周五`（相对日期按参考时间解析）
   - 输出对齐现有日期/时间表示（datetime 或既有时态区间结构）
   - 无年份上下文时的默认策略（取当前年 vs 拒绝）需可配置

落点：`semantica/normalize/`，参考现有 normalizer 的类结构与测试模式（`tests/normalize/`）。

## User Scenarios & Testing

### 主流程

用户对 `支付时间2026年10月2日，金额$5M` 运行规范化流水线 → 日期解析为 `2026-10-02`（datetime），金额走既有 currency_normalizer 得 5000000.0 USD → 混排文本 `AI驱动决策` 按策略输出 `AI 驱动决策`。

### 边界情况

- 纯英文文本：CJK 空格规则零改动（byte-identical）
- 罕见格式（民国纪年、农历）：本期不支持，原样保留并计数上报，不抛异常
- 相对日期（「下周一」）无参考时间：使用当前时间并标注推断来源

## Requirements

### Functional Requirements

| ID | Requirement | Status |
| --- | --- | --- |
| FR-001 | CJK 空格规范化器：全角/半角统一、中英文边界加/去空格，策略可配置，纯非中文文本零改动 | Clear |
| FR-002 | 中文日期解析：覆盖 `YYYY年M月D日`、`M月D日`（无年份可配策略）、ISO 及常见横线格式、相对日期（今天/明天/下周X） | Clear |
| FR-003 | 两项能力接入现有 normalize 流水线（可组合、可单独调用），输出类型与既有 normalizer 一致 | Clear |
| FR-004 | 不支持的日期格式原样保留并计数，不抛异常中断流水线 | Clear |

### Non-goals

- 农历、民国纪年等特殊历法（本期仅公历）
- 时区推断（沿用项目既有时区约定）

## Work Packages（草案，最终以 /spec-kitty.tasks 产出为准）

- WP01 CJK 空格规范化器（FR-001）
- WP02 中文日期解析器（FR-002、FR-004）
- WP03 流水线接入与组合测试（FR-003）

## 决策记录

- 2026-10-02 用户提出 7 项路线图待办（本 mission 覆盖其中 ②）
- 2026-10-02 用户提供 DeepSeek notebook 实测用例，FR-002 家族扩展：日期区间（…至/到…，返回 value+value_end）、仅年份、年度相对词（去年/明年等，锚定参考年 1 月 1 日）、数量偏移（前三个自然月，月按 30 天近似与 notebook 一致）。频率表达式（每季度→P3M）不入本 mission（非日期语义）
