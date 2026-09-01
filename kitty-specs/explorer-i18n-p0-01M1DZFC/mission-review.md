# Mission Review Report: explorer-i18n-p0-01M1DZFC

**Reviewer**: Claude Code（mission review skill，协调方复核模式）
**Date**: 2026-09-01
**Mission**: `explorer-i18n-p0-01M1DZFC` — Explorer 中文界面 P0
**Baseline commit**: `293a113b`（main 上 mission 开始前的 HEAD；meta.json 的 `baseline_merge_commit` 字段记录的是 merge 时的 accept 提交，非代码基线）
**HEAD at review**: `8d647214`（main，merge feature/explorer-i18n-p0）
**WPs reviewed**: WP01..WP04（全部 done，19/19 子任务）

---

## Gate Results

> 说明：Gate 1–3 为 spec-kitty CLI 仓库自身的回归套件（`tests/contract/`、`tests/architectural/`、跨仓 e2e），本 mission 位于 semantica 仓库，不存在该结构，按 N/A 记录而非套用。

### Gate 1 — Contract tests
- Result: **N/A**（semantica 仓库无 `tests/contract/` 套件）

### Gate 2 — Architectural tests
- Result: **N/A**（semantica 仓库无 `tests/architectural/` 套件）

### Gate 3 — Cross-repo E2E
- Result: **N/A**（无跨仓 e2e 依赖）

### Gate 4 — Issue Matrix
- File: `kitty-specs/<slug>/issue-matrix.md` — **不存在**
- Rows: 0；空/unknown verdict: 0；缺 follow-up handle 的 deferral: 0
- Result: **PASS**（本 mission 无关联 GitHub issues、事件史无 deferral 记录，空矩阵即真实状态）

## 流程审查（Step 1/4）

- 事件史 29 条：4 WP 全部走 `planned→claimed→in_progress→for_review→in_review→approved→done` 标准路径，**0 次 force、0 次 arbiter override、0 次 rejection cycle**（无 review-cycle-*.md——本 mission 采用协调方逐 WP 实测验收模式，验收记录见各 move-task note 与 acceptance-matrix.json）。
- `ReviewerSelfApproval`：无独立 reviewer 角色；验收由协调方（派发方）执行并附实测证据。此为本 mission 的流程特征，记录为已知局限而非发现。

## 约束核验（C-001…C-006）

| 约束 | 核验方式 | 结果 |
|---|---|---|
| C-001 零侵入白名单 | `git diff 293a113b..main --stat` 全清单比对 | **PASS**：上游文件改动仅 main.tsx(+1)、App.tsx、ErrorBoundary.tsx、package.json(+2)、package-lock.json、e2e 预置(+5)；其余全为新增文件（i18n/**、tools/i18n/ui_zh_status.py） |
| C-002 禁触区 | diff 中无 `semantica/explorer/**`、`index.html`、`vite.config.ts` | **PASS** |
| C-003 响应式传播 | 全部渲染文案经 `useTranslation()` 订阅；类组件 `i18n.t()` 直调（spec 认可瞬态 UI） | **PASS** |
| C-004 术语基准 | zh.json 对照 glossary：7 词全合规、禁用词（工作台/工作空间）零命中 | **PASS** |
| C-005 可扩展 | 资源按语言分文件 + `__meta`，新增语言=新增 JSON + types 扩展，无结构重构 | **PASS** |
| C-006 依赖白名单 | package.json 仅 +i18next@26.4.1 +react-i18next@17.0.13 | **PASS** |

## FR Coverage Matrix

| FR ID | Description (brief) | WP Owner | Evidence | Test Adequacy | Finding |
|-------|---------------------|----------|----------|---------------|---------|
| FR-001 | 切换即时无刷新 | WP02/WP04 | §3 走查 2（98ms、window 标记存活） | PARTIAL | RISK-1 |
| FR-002 | 偏好持久化 | WP01 | §3 走查 3 + try/catch 读写 | PARTIAL | RISK-1 |
| FR-003 | 首访四级检测 | WP01 | §3 走查 1/4/6 + `isSupportedLanguage` 白名单 | PARTIAL | RISK-1 |
| FR-004 | P0 全覆盖双语 | WP02 | 107 键同构脚本核验、残留清点表、走查 1 | ADEQUATE | — |
| FR-005 | 缺译回落英文 | WP01 | `fallbackLng:'en'`；键名显示路径被 FR-006 构建期封死 | PARTIAL | RISK-1 |
| FR-006 | 键同构构建期失败 | WP01 | `zh satisfies typeof en` + `tsc -b` exit 0 | ADEQUATE | — |
| FR-007 | html lang/title 同步 | WP01/WP02 | §3 走查 5 + languageChanged 监听 | PARTIAL | RISK-1 |
| FR-008 | 过期追踪脚本 | WP03 | 实跑 fresh/0/0/exit 0 双确认；降级演练 7 例退出码语义正确 | ADEQUATE | — |
| FR-009 | e2e 英文预置全绿 | WP04 | e2e 仅 +5 行、复跑 pass 1/fail 0 | ADEQUATE | — |

**PARTIAL 定性**：非 punt。spec 测试策略明确"不新增单测（spec 未要求）"，走查是 quickstart §3 认可的验收方式；但走查脚本为一次性（放 /tmp 用后删），这些行为无持久 CI 防护（见 RISK-1）。ADEQUATE 判据：键同构删除任一侧键 tsc 必失败（满足"删实现则验证失败"）；ui_zh_status 与 e2e 为常驻可重跑验证。

## 抽样比对（成功标准 3）

基线 `293a113b:explorer/src/App.tsx` 原文 vs en.json 键值：`Open Semantica Explorer`、`Run Reasoning`、`Backend Unreachable`、`System Online`、`Loading workspace…` 五串逐字一致；e2e 锚点实测命中。

## Drift Findings

### DRIFT-1: NFR-004 "lint 零错误"字面未达，验收按"零回归"口径解释

**Type**: NFR-MISS（措辞级）
**Severity**: LOW
**Spec reference**: NFR-004
**Evidence**: `npm run lint` = 74 problems（57 errors / 17 warnings），与 mission 前基线完全一致（同 74、同 18 个文件，均为存量 `no-explicit-any` 等，不在本 mission 改动文件内）；tsc 零错误属实。

**Analysis**: NFR-004 原文"lint 与类型检查零错误"与仓库现实（mission 前 lint 即红）冲突。实现团队在 WP04 验收表按"与基线持平、零增量"解释并留痕，属合理解释但偏离字面。非阻塞；建议后续 mission 的 NFR 措辞显式区分"零回归"与"清零"口径。

## Risk Findings

### RISK-1: 语言检测/切换行为无持久回归防护

**Type**: ERROR-PATH（验证缺口）
**Severity**: LOW
**Location**: `explorer/src/i18n/index.ts`（四级检测）、`syncDocumentLanguage`
**Trigger condition**: 未来重构 i18n 初始化或检测顺序时，无 CI 测试拦截。

**Analysis**: FR-002/003/005/007 的验证依赖一次性 Playwright 走查（脚本已删）。常驻的 deterministic-e2e 只护英文首屏与画布渲染锚点。P1 批次建议把 quickstart §3 七项走查固化为常驻 Playwright 测试（`explorer/tests/`）。

### Note: 成功标准 3 与语言开关的措辞张力

spec 成功标准 3 要求英文界面"与改造前完全一致（0 处差异）"，而 FR-004/主流程要求新增语言开关（英文模式下 rail 上也可见）。实现按"文案层逐字一致 + 新增开关组件"落地，是两条要求的唯一同时满足方式。spec 内在张力，非实现缺陷；记录供后续 spec 措辞参考。

## Silent Failure Candidates

无。`index.ts` 的三段 try/catch 是 spec 边界情况（禁用本地存储）明确要求的降级路径，带 fall-through 注释；`ui_zh_status.py` 坏 JSON 时 `raise LocaleDataError` → 退出码 1，非吞错。

## Security Notes

| 检查项 | 结果 |
|---|---|
| subprocess（ui_zh_status.py:64） | list 参数、无 shell=True、root 为脚本内计算值，无注入面 |
| `?lang=` 输入（index.ts:50） | 经 `isSupportedLanguage` 白名单（en/zh），非法值 fall through |
| localStorage | 读写均 try/catch，无私密数据（仅语言码） |
| 网络/凭据 | 本 mission 无涉及 |

## Final Verdict

**PASS WITH NOTES**

### Verdict rationale

九条 FR 全部有证据链（spec→WP→验证→代码），其中四条为常驻可重跑验证（键同构 tsc、ui_zh_status、deterministic-e2e、构建产物），五条依赖一次性走查但均为 spec 认可的验收方式且结果已留痕。六条约束全部核验通过，零侵入边界在 diff 全清单上成立。唯一 drift 为 NFR-004 的 lint 措辞口径（LOW，存量零增量、有留痕）。无 CRITICAL/HIGH 发现，无安全发现。

### Open items (non-blocking)

1. RISK-1：P1 批次把 §3 七项走查固化为常驻 Playwright 测试。
2. DRIFT-1：后续 mission NFR 措辞显式区分"零回归/清零"。
3. `welcome.titleLine2` 拆键等 4 处越界补键已在 tasks.md Execution Notes 集中留痕，P2+ 批次沿用该汇总模式。

## Retrospective Reminder

`retrospective.yaml` 已在 runtime terminus 自动 capture（`kitty-specs/explorer-i18n-p0-01M1DZFC/retrospective.yaml`，112 行，提交 4d035616），已验证存在。`spec-kitty retrospect summary` 当前聚合 mission_count=0（记录位于 mission 目录而非 `.kittify/missions/`，聚合器未覆盖旧路径——不影响本 mission）；`spec-kitty agent retrospect synthesize --mission explorer-i18n-p0-01M1DZFC` dry-run 结果 planned=0，无待应用提案。
