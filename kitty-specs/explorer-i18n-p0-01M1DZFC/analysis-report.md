---
schema_version: 1
artifact_type: spec-kitty.analysis-report
command: /spec-kitty.analyze
mission_slug: explorer-i18n-p0-01M1DZFC
mission_id: 01M1DZFCYQQK6A5AZEDW3QAS5E
generated_at: '2026-09-01T10:26:40.977500+00:00'
analyzer_agent: unknown
input_artifacts:
  spec.md:
    path: /Users/luofisher/ToolsChain/semantica/kitty-specs/explorer-i18n-p0-01M1DZFC/spec.md
    sha256: 87aa6d831ad7eb4647971d8c072f5f9d99ec5c3d2b3e30e07bc1edc77820c188
  plan.md:
    path: /Users/luofisher/ToolsChain/semantica/kitty-specs/explorer-i18n-p0-01M1DZFC/plan.md
    sha256: 4f5b4b16700f19561c114d914e72761836ed676e3f7695efaf012d00c59b3eb3
  tasks.md:
    path: /Users/luofisher/ToolsChain/semantica/kitty-specs/explorer-i18n-p0-01M1DZFC/tasks.md
    sha256: 430a5786ffe7f6c74715d43f0197cd0bc744a905ced66e1787e0156bb9bc71f2
  charter:
    path: /Users/luofisher/ToolsChain/semantica/.kittify/charter/charter.md
    sha256: a5e01a009b82bb321c397f1f4d566511a1a4713370ab47480516eb838cffce67
verdict: blocked
issue_counts:
  critical: 0
  high: 1
  low: 3
  medium: 1
  info: 0
findings:
- id: A1
  severity: high
  category: coverage
  summary: zh.json __meta.source_version 的最终刷新无任务负责：WP02 会给 en.json 追加 error.* 键，使 WP01 记录的 sha 过期，WP03/WP04 的 fresh 门禁将按当前设计 false-fail。
- id: A2
  severity: medium
  category: coverage
  summary: quickstart §3 手动走查（7 项）与 §4 术语抽查未指派给任何工作包，而成功标准 1-3 依赖它们。
- id: L1
  severity: low
  category: ambiguity
  summary: NFR-001 的 1 秒切换阈值没有任何任务做度量，仅剩定性人工观察。
- id: L2
  severity: low
  category: inconsistency
  summary: spec/plan 估算 200-300 条文案 vs tasks 键清单约 95+5 键，计数口径未在工件中说明，评审易误读为覆盖不足。
- id: L3
  severity: low
  category: underspecification
  summary: T002 键清单之外有两处刻意补充键（WP01 的 language.toggle、WP02 的 error.*×5），属已声明的越界编辑但未在单一位置汇总，评审需自行拼图。
---

# Specification Analysis Report — explorer-i18n-p0-01M1DZFC

分析范围：`spec.md` / `plan.md` / `tasks.md` + 4 份 WP 提示文件 + contracts/ + quickstart.md；charter（2026-09-01 编译版）为基准。

## Findings

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| A1 | Coverage | HIGH | tasks.md WP02-T012 / WP03-T015 / WP04-T019; data-model.md StalenessRecord | `__meta.source_version` 生命周期断链：WP01-T002 记录 en.json 的 blob sha → WP02-T011 给 en.json/zh.json 追加 error.* 键 → en.json HEAD sha 变化，但没有任何任务刷新 zh.json 的 `source_version` → WP03-T015 与 WP04-T019 期望的 fresh 判定必然落空（stale），集成门 false-fail | 在 WP02-T012 增加一步：en.json 内容定稿后重算 `git hash-object explorer/src/i18n/locales/en.json` 并同步更新 zh.json `__meta.source_version`（WP01 拥有该文件，越界编辑已有规则通道）；WP04-T019 的复核即成为真实验证 |
| A2 | Coverage | MEDIUM | quickstart.md §3/§4; tasks.md WP04-T019 | 成功标准 1-3（逐屏走查 0 残留、切换保持、英文零差异）依赖手动走查，但 quickstart §3 的 7 项与 §4 术语抽查没有落进任何 WP 的任务清单，存在"人人以为对方会做"的风险 | 扩展 WP04-T019：明确追加 quickstart §3 七项走查与 §4 术语抽查，结果并入验收表（无法自动化者标注"人工执行"及执行人） |
| L1 | Ambiguity | LOW | spec.md NFR-001; tasks.md | NFR-001 的 "<1s 且不重载" 无度量任务；当前仅靠"点击后观察"定性验证 | 并入 A2 的走查项，加一条明确检查框"切换后文案更新无可感知延迟、无页面重载" |
| L2 | Inconsistency | LOW | spec.md Overview / plan.md Scale/Scope vs tasks.md T002 | spec/plan 写"约 200-300 条文案"，tasks 键清单约 95 键（+5 后补）。两者口径不同（键数 vs 含双语与重复渲染实例的字符串计数），未在工件中解释 | 在 tasks.md Execution Notes 补一行口径说明；或把 spec/plan 的估算改为"约 100 键"，消除评审歧义 |
| L3 | Underspecification | LOW | WP01-T005 (language.toggle)、WP02-T011 (error.*×5) | 两处刻意超出 T002 键清单的补键是设计内越界（所有权规则允许、须记录理由），但汇总位置分散在各 WP 内部 | 无需改任务；建议 mission review 时把两处越界补键列入检查单，核验 en/zh 成对与理由记录 |

## Coverage Summary

| Requirement Key | Has Task? | Task IDs | Notes |
|-----------------|-----------|----------|-------|
| FR-001 切换即时无刷新 | ✓ | T007, T009, T010 | WP02 挂载开关 + 渲染期取译 |
| FR-002 偏好持久化 | ✓ | T004, T005 | 读写均 try/catch |
| FR-003 首访语言检测 | ✓ | T004 | 四级检测顺序 |
| FR-004 P0 全覆盖双语 | ✓ | T002, T007–T011 | 键位契约流 WP01→WP02 |
| FR-005 缺译回落英文 | ✓ | T004 | fallbackLng: 'en' |
| FR-006 键同构构建期失败 | ✓ | T002, T003 | satisfies + tsc |
| FR-007 html lang 与标题同步 | ✓ | T004, T012 | languageChanged 监听 + WP02 验证 |
| FR-008 过期追踪脚本 | ✓ | T013–T015, T019 | WP03 实现 + WP04 复核 |
| FR-009 e2e 英文预置全绿 | ✓ | T016–T017 | 仅预置行增量 |
| NFR-001 切换 <1s | ✓(弱) | — | 无度量步骤，见 L1 |
| NFR-002 gzip ≤50KB | ✓ | T006(记录), T019(复核) | |
| NFR-003 术语一致率 100% | ✓ | T002(规则+校验), A2 建议 | 抽查落点待显式化 |
| NFR-004 既有测试零回归 | ✓ | T018 | 五条命令 + e2e |

## Charter Alignment Issues

无冲突。核对记录：测试方式用项目已声明者（npm scripts + Playwright）✓；质量门禁未新增强加于既有流程的门（ui_zh_status 是本期交付物自身的验收，非外加门禁）✓；评审政策（focused reviewer before merge）由 mission review 承接 ✓；部署约束 macOS/Linux 已入 plan Technical Context ✓；新增依赖属"项目显式声明工具"的扩展，已由 spec DIRECTIVE_003 + C-006 决策留痕 ✓；Directive 1（五阶段工件一致）——A1 即该指令下的缺口。

## Unmapped Tasks

无。19 个子任务均可溯源到 FR/NFR 或门禁职责（T012/T015/T019 为验证性任务，对应 NFR-004/FR-008/NFR-002）。

## Metrics

- Total Requirements: 13（FR 9 + NFR 4；约束 C-001…C-006 另计，全部映射到 WP 边界与提示文件的禁触清单）
- Total Tasks: 19（4 WP）
- Coverage %: 100%（13/13 有 ≥1 任务；NFR-001 为弱覆盖）
- Ambiguity Count: 1（L1）
- Duplication Count: 0
- Critical Issues Count: 0

## Next Actions

1. **A1（HIGH，阻塞级）**：先修再实现——在 WP02-T012 增加 source_version 刷新步骤（或改由 WP01 在 T006 预留说明、WP02 执行）。修复后 verdict 可翻绿。
2. **A2（MEDIUM）**：把 quickstart §3/§4 显式并入 WP04-T019 走查清单。
3. L1-L3：低危，可在同一轮编辑中顺带处理，也可留待 mission review 关注。
4. 处理完 A1/A2 后即可进入 `/spec-kitty.implement`（WP01 先行，WP02∥WP03，WP04 收尾）。
