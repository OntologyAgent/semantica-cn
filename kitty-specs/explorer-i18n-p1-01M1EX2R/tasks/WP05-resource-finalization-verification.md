---
work_package_id: WP05
title: 资源收口与全量验证（键同构 · source_version · 测试全绿 · 走查）
dependencies:
- WP04
requirement_refs:
- FR-004
- FR-005
- FR-008
- FR-009
- NFR-002
- NFR-003
- NFR-004
tracker_refs: []
planning_base_branch: feature/explorer-i18n-p1
merge_target_branch: feature/explorer-i18n-p1
branch_strategy: Planning artifacts for this mission were generated on feature/explorer-i18n-p1. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feature/explorer-i18n-p1 unless the human explicitly redirects the landing branch.
subtasks:
- T016
- T017
- T018
- T019
agent: "claude"
shell_pid: "30510"
history:
- timestamp: '2026-09-02T00:00:00Z'
  action: created
  agent: claude
agent_profile: reviewer-renata
authoritative_surface: explorer/src/i18n/locales/
create_intent:
- explorer/src/i18n/locales/en.json
- explorer/src/i18n/locales/zh.json
execution_mode: code_change
owned_files:
- explorer/src/i18n/locales/en.json
- explorer/src/i18n/locales/zh.json
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile

```
/ad-hoc-profile-load reviewer-renata
```

不可用时：以细心前端审查者角色执行——先验证后修改，只动 locales 两个文件。

## Objective

P1 收口：确认全部抽取 WP 的键位与译文质量，刷新过期追踪基准，跑齐四套测试与 lint/build 零增量，完成双语走查与术语核对。本 WP 是 FR-004/005/008/009 与 NFR-002/003/004 的验收关。

## Context

- WP01-WP04 已合入：`graph.*` 键段由各 WP 增补完毕；`apiError.ts` 已接入错误渲染点。
- `zh.json` 的 `__meta.source_version` 仍是 P0 时的 en.json blob sha——本 WP 刷新为 P1 定稿后的 HEAD sha。
- `tools/i18n/ui_zh_status.py`：P0 交付的过期追踪脚本，源基准 = en.json HEAD blob sha，比对 `__meta.source_version` 输出 fresh/stale。**只运行，不改脚本**。
- 本 WP `owned_files` 仅 locales 两文件——发现组件层问题时**记入报告**交回对应 WP 修复，不自行改组件（WP 隔离）。

## Implementation Guidance

### T016 — 键同构复核与键位走查

- `cd explorer && npm run build`：tsc 通过即 INV-1（同构）成立。
- 键位走查：遍历 `graph.*` 段，逐键核对——① en 值与改造前原文一致（对照 git diff 中被替换的字面量）；② zh 值非空、非键名、非英文残留；③ 无孤儿键（键存在但无 `t()` 引用——tsc 不报孤儿键，需 grep 引用点）。
- 孤儿键清理或补引用；缺键（组件引用了但两侧缺）由 build 拦截，出现即回对应 WP。

### T017 — 刷新 `__meta.source_version` + ui_zh_status fresh

```bash
cd explorer
git add src/i18n/locales/en.json        # 先暂存定稿的 en.json
BLOB=$(git ls-files -s src/i18n/locales/en.json | awk '{print $2}')
```

- 把 `zh.json` 的 `__meta.source_version` 改为该 blob sha（注意：若暂存后 zh.json 再有改动，en.json 的 sha 不受影响——en 与 zh 的编辑互不干扰；但最终提交前重新取一次 sha 确认 en.json 未再变）。
- 运行 `python tools/i18n/ui_zh_status.py`（仓库根）确认 explorer UI 资源报告 **fresh**；`--json` 输出亦为 fresh。
- 若报告 stale/missing：说明 en.json 在取 sha 后又被改动——重取重刷。

### T018 — 测试全绿 + lint/build 零增量

```bash
cd explorer
npm run lint                       # 零增量：相对存量 74 条（57 errors），不新增
npm run build                      # 绿
npm run test:graph-workspace
npm run test:graph-store
npm run test:plugin-registry
npm run test:deterministic-e2e
```

- 任一失败：定位归属 WP（组件问题回 WP02-04 修复后复跑），不跳过不豁免。
- 构建产物体积核对（NFR-002）：`ls -l semantica/static/assets/*.js` 对照改造前，gzip 增量 ≤ 30KB（`gzip -k -9` 实测或按 bundle 大小粗估）。

### T019 — 双语走查与术语核对

按 `quickstart.md` §4-§7 执行并记录结果（结果可写入本 WP 完成说明）：

- zh 走查：搜索栏/工具栏/图例/时间轴/Inspector/加载与失败面板全中文；数据值（节点/边 label、ORG/PERSON/PRODUCT/DATE/CONCEPT）保持原文；0 处英文残留。
- 语言切换：中/EN 即时切换、不刷新页面、重开保持；`<html lang>` 与标题同步（`探索 · Semantica` / `Semantica Knowledge Explorer`）。
- 401 场景：中文包装提示出现、detail 英文原文完整可见。
- 术语核对（NFR-003）：zh.json 全量对照 `docs/zh/glossary.md`——"探索"定名（不得出现"知识探索器"）、工作区/检查器/时态/溯源等译名一致；"Semantica 探索"等组合词符合定名规则。
- 英文回归：`?lang=en` 抽查工作区主要界面与改造前逐字一致（FR-006 口径）。

## Validation

- [ ] `python tools/i18n/ui_zh_status.py` 输出 fresh（FR-009）
- [ ] 四套测试全绿（FR-008）
- [ ] lint/build 零增量（NFR-004）
- [ ] 键同构（FR-005）、无孤儿键、回落机制不变（FR-004）
- [ ] 术语一致率 100%（NFR-003）、体积增量达标（NFR-002）
- [ ] 走查记录完整（quickstart §4-7 全场景）

## Risks

- source_version 刷新时序：必须在 en.json 定稿后取 sha；提交前再验证一次 fresh，防收尾微调导致 stale。
- 走查发现组件层遗漏（如某插件残留英文）：不得越权改组件——记录清单交回对应 WP，修复后本 WP 复验收口。

## Reviewer Guidance

- 本 WP 自身即验收关：核对 T016-T019 每项证据（命令输出/走查记录）真实留存，不接受"应该没问题"。

## Activity Log

- 2026-09-01T18:40:35Z – claude – shell_pid=22827 – Implementation complete (commit 2fc7025f). T016: key parity 414=414, build INV-1, orphan-key triple scan 0. T017: source_version refreshed to 756a1b9a (staged en.json blob), ui_zh_status fresh (text+json, 0 missing/extra). T018: lint 74 baseline zero-delta, build green, 4 suites green (graph-workspace 73, plugin-registry 7, graph-store 1, deterministic-e2e 1), bundle gzip delta +9.8KB locales upper bound (NFR-002 ≤30KB). T019: zh full-text walkthrough clean, banned terms 0 (知识探索器/时序/探索器), glossary terms verified (探索/时态/距离带/距离智能/决策智能), data values untouched, en regression protected by deterministic-e2e; known limitation: panel/overlay titles via i18next.t() have a one-switch lag window (documented in WP04 review).
- 2026-09-01T18:40:40Z – claude – shell_pid=30510 – Started review via action command
- 2026-09-01T18:41:59Z – user – shell_pid=30510 – Review passed (8-item anti-pattern checklist): [1] Dead code N/A - WP05 adds no code, only zh.json value edits + source_version. [2] Synthetic-fixture N/A - no new tests; verification FRs evidenced by real command output. [3] Silent empty return N/A. [4] FR coverage PASS with live evidence: FR-009 ui_zh_status fresh (text+json, 0 missing/extra), FR-008 four suites green (73/7/1/1), FR-005 parity 414=414 + tsc INV-1, FR-004 fallbackLng:'en' untouched (index.ts:99) + error-wrapper tests green, NFR-002 gzip +9.8KB<=30KB, NFR-003 banned terms 0 (知识探索器/时序/探索器) + glossary verified, NFR-004 lint 74 baseline zero-delta. [5] Frozen surface PASS - commit 2fc7025f touches only owned zh.json; ui_zh_status.py 0 commits in mission branch. [6] Locked decision PASS - script run-not-modified honored; component-layer fixups routed through resources only. [7] Shared-file PASS with coordination note: locales co-edited by WP04 (lane-d) merged into lane-e BEFORE WP05 serial edits; no parallel writes. [8] Production fragility N/A. Orphan-key rescan: 0 across 307 graph.* keys (static+dynamic prefix scan). Known accepted limitation documented: panel/overlay title i18next.t() one-switch lag window.
