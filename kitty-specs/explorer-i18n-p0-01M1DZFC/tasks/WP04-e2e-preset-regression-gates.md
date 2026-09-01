---
work_package_id: WP04
title: e2e 英文预置与全套门禁回归（收尾）
dependencies:
- WP01
- WP02
- WP03
requirement_refs:
- FR-009
- NFR-002
- NFR-004
tracker_refs: []
planning_base_branch: feature/explorer-i18n-p0
merge_target_branch: feature/explorer-i18n-p0
branch_strategy: Planning artifacts for this mission were generated on feature/explorer-i18n-p0. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feature/explorer-i18n-p0 unless the human explicitly redirects the landing branch.
subtasks:
- T016
- T017
- T018
- T019
agent: "claude"
shell_pid: "51589"
history:
- timestamp: '2026-09-01T09:51:16Z'
  action: created
  agent: claude
agent_profile: frontend-freddy
authoritative_surface: explorer/tests/
create_intent: []
execution_mode: code_change
owned_files:
- explorer/tests/deterministicExplorerRendering.e2e.ts
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile

Before reading anything else, load your assigned agent profile:

```
/ad-hoc-profile-load frontend-freddy
```

If that command is unavailable, proceed as a careful frontend implementer：测试驱动、最小 diff、门禁意识。

## Objective

让既有 Playwright e2e 在 i18n 改造后继续全绿（FR-009）：给测试加英文预置（对上游 e2e 文件的唯一允许改动，C-001），然后跑全套门禁（lint/build/四套测试/过期脚本）作为 mission 的集成验收（NFR-004），复核体积预算（NFR-002），并收口 quickstart §3 手动走查与 §4 术语抽查（成功标准 1-3、NFR-001/NFR-003 的验证位）。本 WP 最后执行——WP01/WP02/WP03 的改动在你之前合入 lane 基线。

## Context

- 仓库根：`/Users/luofisher/ToolsChain/semantica`（执行时在 lane worktree，结构相同）
- e2e 文件：`explorer/tests/deterministicExplorerRendering.e2e.ts`——按 `getByRole("button", { name: /Open Semantica Explorer/ })`、`"Zoom In"` 等英文文案定位。i18n 上线后：无预置时语言由浏览器环境决定（CI 的 Playwright Chromium 默认 en-US，但**不能赌环境**），必须显式固定英文
- 预置契约（`contracts/language-detection.md` §e2e 预置契约）：两种合法机制——导航 URL 带 `?lang=en`，或 `context.addInitScript` 预置 `localStorage["semantica.explorer.lang"]="en"`。**推荐后者**（addInitScript 天然先于应用代码执行，覆盖文件内所有导航）
- 零侵入边界：你只动 `explorer/tests/deterministicExplorerRendering.e2e.ts` 一个上游文件，且只加预置相关行（预计 ≤5 行）；**不许**改测试断言、选择器或流程。PR 描述需显式说明此测试改动（spec Assumptions 已声明）
- 门禁命令（全部在 `explorer/` 下）：`npm run lint`、`npm run build`、`npm run test:graph-store`、`npm run test:graph-workspace`、`npm run test:plugin-registry`、`npm run test:deterministic-e2e`；仓库根：`python tools/i18n/ui_zh_status.py`
- quickstart 验收清单：`kitty-specs/explorer-i18n-p0-01M1DZFC/quickstart.md` §1–§4（§3 手动走查与 §4 术语抽查由你收口，成功标准 1-3 在此验证）

## Subtask Guidance

### T016: e2e 英文预置

**Purpose**: 固定 e2e 运行语言为英文，隔离浏览器环境差异（FR-009）。

**Steps**:
1. 读 e2e 文件，找到创建 browser context 的位置（`browser.newContext(...)` 或 fixture）。
2. 在 context 创建后、首次导航前加：
   ```ts
   await context.addInitScript(() => {
     try { window.localStorage.setItem("semantica.explorer.lang", "en"); } catch { /* ignore */ }
   });
   ```
   （若文件里已有 addInitScript 调用，合并进既有脚本时保持 try/catch 语义。）
3. 注释一行说明意图：`// Pin UI language to English so role-name locators stay deterministic regardless of browser locale.`
4. 不动其他任何行。

**Files**: `explorer/tests/deterministicExplorerRendering.e2e.ts`

**Validation**:
- [ ] 预置行 ≤5 行且只在 context 初始化处
- [ ] `git diff` 除预置外零改动

### T017: deterministic-e2e 全绿

**Purpose**: 证明英文路径与改造前行为一致（回归防护核心）。

**Steps**:
1. `cd explorer && npm run test:deterministic-e2e`。
2. 全绿 = 通过。若有失败：
   - 失败在英文文案定位（如 `Open Semantica Explorer`）→ 说明 WP02 改动了锚点文案，属 WP02 回归——**修 e2e 是禁区**，把失败详情写进完成报告并标记阻塞，交协调方裁决（正确修法是恢复 en 键值，不是改选择器）
   - 失败在非文案断言（布局/时序）→ 同样记录，不私改
3. 本地无显示器的环境照常可跑（Playwright headless 默认）。

**Files**: 无新改动（验证性子任务）

**Validation**:
- [ ] `npm run test:deterministic-e2e` 退出码 0
- [ ] 失败（若有）已完整记录且未私改测试

### T018: 全套静态与单元门禁

**Purpose**: NFR-004：lint/类型/既有测试套件零回归。

**Steps**:
1. 依次执行并记录结果：
   ```bash
   cd explorer
   npm run lint
   npm run build            # tsc -b：键同构与 t() 键名的最终把关
   npm run test:graph-store
   npm run test:graph-workspace
   npm run test:plugin-registry
   ```
2. 全绿才继续；失败按"哪层回归就记哪层"原则写进报告（不跨 WP 私修源码——你只拥有 e2e 文件）。
3. `npm run build` 会把产物写入 `semantica/static/`——这是预期行为（wheel 分发），无需清理。

**Files**: 无新改动（验证性子任务）

**Validation**:
- [ ] 五条命令全部退出码 0，输出摘要记入完成报告

### T019: 体积预算、过期脚本、手动走查与术语复核（NFR-002/FR-008/NFR-001/NFR-003 验收 + 成功标准 1-3）

**Purpose**: 量化门禁收口；quickstart §3 手动走查与 §4 术语抽查在此收口（成功标准 1-3 的验证位）。

**Steps**:
1. 体积（NFR-002，预算 gzip 增量 ≤ 50KB）：`npm run build` 后记录 `semantica/static/assets/*.js` 的 gzip 总量，与改造前基线对比（基线可由 `git stash` 后 build 一次获得，或直接采用 vite 输出里 i18n 相关 chunk 的尺寸估算；报告口径写清楚）。i18next+react-i18next 预期 ~25KB gzip + 资源 ~5-10KB，预算内。
2. 过期脚本（FR-008）：仓库根 `python tools/i18n/ui_zh_status.py` 与 `--json`——期望 fresh、missing=0、extra=0、退出码 0。这是 A1 修复后 source_version 链路的真实集成验证（WP02-T012 刷新的 sha 在此被 HEAD 口径的脚本检验）。
3. **手动走查（quickstart §3，成功标准 1-3 的验证位）**：起服务（quickstart §3 的方式 A `npm run dev` + 后端，或方式 B 整包），逐项执行七项走查并记录结果：
   - 走查 1：浏览器语言 zh → 首屏全中文（导航/首屏/页签/连接状态）
   - 走查 2：开关切 EN → 即时变英文（NFR-001 度量位：文案更新无可感知延迟、无页面重载，记录定性结论）
   - 走查 3：刷新保持（EN 刷新仍英文、zh 刷新仍中文）
   - 走查 4：`?lang=en` 强制英文（优先于存储偏好）
   - 走查 5：`<html lang>` 与标签页标题随语言变化（DevTools）
   - 走查 6：浏览器语言 en + 清站点数据 → 与改造前完全一致
   - 走查 7：断开后端 → 连接状态显示当前语言文案
   执行方式：能开浏览器就人工走查；无显示环境用临时 Playwright 脚本驱动（脚本放 `/tmp`，**不落仓库**）。无法自动化的项标注"人工执行"并留待用户复核。
4. **术语抽查（quickstart §4，NFR-003 验证位）**：zh 文案对照 `docs/zh/glossary.md` 核对——知识图谱、本体、Ontology Hub（保留英文）、溯源、实体消解、决策智能、工作区（禁"工作台/工作空间"），结果记入验收表。
5. quickstart §1 静态门禁清单逐项打勾（就是 T017/T018 的命令，确认无遗漏）。
6. 汇总一份验收表（命令 + 走查项 + 术语抽查 → 结果 → 对应 FR/NFR）写进完成报告，供 mission review 直接引用。

**Files**: 无新改动（验证性子任务）

**Validation**:
- [ ] gzip 增量数字入报告且 ≤ 50KB
- [ ] ui_zh_status fresh 双确认（表格 + JSON）
- [ ] quickstart §3 七项走查逐项有结果记录；NFR-001（切换无感知延迟、无页面重载）有明确结论
- [ ] §4 术语抽查逐词核过且入验收表
- [ ] 验收表完整覆盖 FR-001…FR-009、NFR-001…NFR-004 的可测部分（自动化 + 走查）

## Test Strategy

本 WP 本身就是测试收口，不新增测试文件。唯一代码改动是 T016 的预置行。

## Definition of Done

- [ ] T016–T019 全部完成且 Validation 勾稽
- [ ] e2e 仅含语言预置增量
- [ ] 六条门禁命令全绿，结果入报告
- [ ] 体积预算与 fresh 检查通过并量化记录
- [ ] quickstart §3 七项走查与 §4 术语抽查逐项有结果、入验收表
- [ ] 零侵入边界未破（diff 只有 e2e 预置行）

## Risks

- **e2e 锚点回归**：若 WP02 动了英文锚点文案，本 WP 会暴露——处理方式是上报阻塞而不是改测试，这条纪律必须守住（改选择器会掩盖真实的英文一致性回归，违反成功标准 3）。
- **本机代理干扰**：e2e 若触网（SSRF 守护拒绝经代理请求），macOS 下需 `NO_PROXY='*' no_proxy='*'` 前缀（仓库 CLAUDE.md 已知坑）。
- **Playwright 浏览器未装**：`npx playwright install chromium` 按需补装（explorer/ 下）。

## Reviewer Guidance

核对：① e2e diff 仅预置行；② 六条门禁的真实输出（不要采信转述）；③ 验收表与 spec FR/NFR 对得上；④ 体积口径可信（gzip、同一构建配置）。

## Activity Log

- 2026-09-01T14:01:49Z – claude – shell_pid=51589 – Assigned agent via action command
- 2026-09-01T14:50:42Z – claude – shell_pid=51589 – Ready for review
- 2026-09-01T14:53:56Z – user – shell_pid=51589 – 验收通过：e2e diff 仅5行预置；deterministic-e2e 复跑 1/1；lint 74 存量零增量；build exit 0；ui_zh_status fresh 双确认（6e6cf42b）；体积 +21.1KB≤50KB；§3 七项走查 7/7；§4 术语 7 词合规禁用词零；commit a5ab28b4
