---
work_package_id: WP08
title: 资源收口与全量验证（键同构 · source_version · 测试全绿 · 走查）
dependencies:
- WP07
requirement_refs:
- FR-006
- FR-007
- FR-008
- FR-009
- FR-011
- FR-012
- NFR-001
- NFR-002
- NFR-003
- NFR-004
tracker_refs: []
planning_base_branch: feature/explorer-i18n-p2
merge_target_branch: feature/explorer-i18n-p2
branch_strategy: Planning artifacts for this mission were generated on feature/explorer-i18n-p2. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feature/explorer-i18n-p2 unless the human explicitly redirects the landing branch.
subtasks:
- T031
- T032
- T033
- T034
agent: "claude"
shell_pid: "54069"
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

不可用时：按验证与质量审计模式实施——只做核对、修复资源文件层问题；组件级缺陷回退给对应 WP 记录。

## Objective

资源层收口与全量验证：`__meta.source_version` 刷新、键同构终检、四套测试全绿、lint/build 零增量、gzip 增量实测、残留终扫、术语核对、双语走查。本 WP 是 mission 的发布门（quickstart.md §1-§7 全部在此执行）。

## Context（实现前必读）

- 本 WP `owned_files` 是 `locales/{en,zh}.json`——全部抽取 WP 已完成，此二文件至此归本 WP 终检。**组件级发现的问题不直接改组件**（越 owned_files）：小问题（键值笔误、漏译键值）可修 locales 后记录；组件问题记入报告交回。
- P1 先例数据：gzip 增量 9.8KB/307 键；lint 基线 74（57 errors + 17 warnings）；四套测试命令见 quickstart §1。
- `zh.translation satisfies typeof en.translation` 构建期同构校验是 FR-008 的执行机制。
- 过期追踪：`python tools/i18n/ui_zh_status.py` 以 en.json 的 HEAD blob sha 对照 zh.json 的 `__meta.source_version`（FR-012）。

## Implementation Guidance

### T031 — source_version 刷新 + ui_zh_status fresh

```bash
# 取 en.json 当前 blob sha
git rev-parse HEAD:explorer/src/i18n/locales/en.json
# 写入 zh.json 顶层 __meta.source_version（保持 i18next 忽略该键的结构）
python tools/i18n/ui_zh_status.py            # 期望 fresh=1 stale=0 missing=0 extra=0
python tools/i18n/ui_zh_status.py --json
```

### T032 — 四套测试 + lint/build + gzip 实测

```bash
cd explorer
npm run build                                # 键同构终检（tsc strict）
npm run lint                                 # 74 基线零增量
npm run test:graph-workspace
npm run test:graph-store
npm run test:plugin-registry
npm run test:deterministic-e2e               # Playwright，锚点 Semantica Explorer / Zoom In
```

- gzip 实测（NFR-002）：构建产物中 locales 所在 chunk 的 gzip 体积相对 P2 基线（改造前同一构建方式）增量 ≤60KB。记录实测值；超限则评估键压缩（缩键名）策略并记录，不得静默放行。
- e2e 锚点若意外失败：**只允许最小定位器调整并显式记录**（C-001），不得改锚定语义。

### T033 — 残留终扫 + 术语核对

- 复跑 WP07 T030 的扫描命令于全工作区，期望：全部命中项在豁免清单（WP07 Execution Notes + 本 WP 复核）内，真实残留 0。
- 术语核对（quickstart §6）：zh.json 违禁词 0（知识探索器/工作台/工作空间/探索器单用）；标准名保留（SPARQL/SHACL/SKOS/OWL/PROV-O/Ontology Hub/Semantica）；抽查术语与 `docs/zh/glossary.md` 一致（推理/决策智能/实体消解/注册表/谱系/本体/溯源）。

### T034 — 双语走查（quickstart §2-§5）

- §2 中文全量走查六屏（分析/决策/增强/管理/Ontology Hub/词表）逐屏核对 0 英文框架残留。
- §3 语言切换：逐工作区 中↔EN 即时切换、`<html lang>` 与标签页标题同步、刷新保持。
- §4 英文回归：`?lang=en` 抽查每工作区主要界面与改造前逐字一致。
- §5 错误与空态：后端不可达/401 中文包装 + detail 英文可见；空数据态随语言切换。
- 走查结果记入 Execution Notes（逐屏 PASS/FAIL 与问题清单）。

### 键值修复权限边界

- locales 内的键值笔误、漏译、术语不一致 → 直接修（本 WP owned_files），修后复跑 T031/T032 受影响步骤。
- 组件抽取缺陷（漏抽、错键引用）→ 记入报告，标注来源 WP，不越界修改。

## Validation

- [ ] `ui_zh_status` fresh=1 stale=0 missing=0 extra=0
- [ ] `npm run build` + `npm run lint`（74 基线）零增量
- [ ] 四套测试全绿
- [ ] gzip 增量实测 ≤60KB（记录数值）
- [ ] 残留终扫真实残留 0（豁免清单完整）
- [ ] 违禁词 0、术语抽查通过
- [ ] 双语走查六屏 PASS，Execution Notes 完整

## Risks

- gzip 超限（估 27KB，余量大，但需实测背书）——超限不得静默放行，记录并提方案。
- 走查发现组件级缺陷——如实记录并回退，不越 owned_files 修补。

## Reviewer Guidance

- 核对 ui_zh_status 输出与 git 中 source_version 一致。
- 抽验 lint 基线数（74）与测试输出真伪（防"绿灯幻觉"——看原始输出）。
- 抽查走查记录的六屏覆盖完整性。

## Activity Log

- 2026-09-02T00:00:00Z – claude – created
- 2026-09-02T04:10:20Z – claude – shell_pid=48509 – Assigned agent via action command
- 2026-09-02T04:17:23Z – claude – shell_pid=48509 – Ready for review: all four gates green on first run, zero locales fixes needed (empty verification commit 45b6ac3a carries full Execution Notes). T031 ui_zh_status fresh=1 all-zero; T032 build+lint 73=baseline, 4 suites 82/82 pass incl. Playwright e2e with intact en anchors, gzip +14.3KB vs 60KB budget (measured vs P1 baseline c46fba9a); T033 final sweep real residue 0 (2 exempt Turtle options + 2 exempt example-URL placeholders), forbidden words 0, glossary spot-check pass; T034 automated walkthrough evidence complete, browser visual manual pass recorded as remaining human acceptance. owned_files locales untouched - HEAD resources already compliant.
- 2026-09-02T04:17:46Z – claude – shell_pid=54069 – Started review via action command
