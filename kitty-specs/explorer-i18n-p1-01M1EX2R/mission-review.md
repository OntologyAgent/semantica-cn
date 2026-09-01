# Mission Review: explorer-i18n-p1-01M1EX2R

**审计问题**：合并代码是否如实、完整地实现了 spec？是否存在实现方未披露的风险？

**结论：通过（PASS）**。合并代码与 spec 无保真缺口；9 项 FR、4 项 NFR、6 项约束全部有可追溯证据链；跨 WP 集成无缺口；未发现实现方未披露的重大风险。三项已披露的限制与遗留见 §5。

审计时间：2026-09-02。审计基线：`eb6aa4b5`（planning tip）→ `c46fba9a`（squash merge of mission），main 落地点 `7cd757aa`。

## 1. 状态与历史

- 5/5 WP 全部 `approved`，0 个 rejection cycle（status.events.jsonl）。
- 事件日志无 forced approval、无 arbiter override、无 ReviewerSelfApproval。
- 验收矩阵（acceptance-matrix.json）19 条 criteria 全 pass，证据均为实测命令输出，无"应该没问题"式断言。

## 2. FR 追溯（spec → 代码 → 测试）

| FR | 证据链 | 裁决 |
|----|--------|------|
| FR-001 工作区文案双语 | 键同构 414=414（graph.* 307 键）；tsc -b exit 0；孤儿键静态+动态前缀双扫描 0；zh 全文走查 | 闭合 |
| FR-002 切换即时 | 面板 content/overlay 为 useTranslation 订阅组件；e2e 渲染管线绿；title 滞后窗口已披露 | 闭合 |
| FR-003 401 中文包装 | apiError.ts 映射 + detailPrefix 拼接 detail 原文；GraphWorkspace.tsx:27 生产 import、:1311 消费；套件断言 | 闭合 |
| FR-004 回落英文 | index.ts:99 `fallbackLng:'en'` 本 mission 零改动；satisfies 约束构建期挡缺译 | 闭合 |
| FR-005 键同构 | types.d.ts + zh satisfies typeof en；独立脚本双向 diff 为空 | 闭合 |
| FR-006 lang/title 同步 | P0 languageChanged 机制未动；e2e 预置 en 通过 | 闭合 |
| FR-007 数据值不译 | 枚举原值通道零改动；distance_band 经 BAND_LABEL_KEYS 键映射（GraphInspectorPanel.tsx:14,104-105）；entityShapes label 死字符串豁免有记录 | 闭合 |
| FR-008 四套测试 | 73/7/1/1 全绿（lane-e 与 main 双重复跑）；e2e 英文预置行保持 | 闭合 |
| FR-009 追踪 fresh | ui_zh_status fresh=1 stale=0 missing=0 extra=0（文本+JSON）；脚本 0 改动 | 闭合 |

NFR-001（订阅通道同步重渲染，P0 实测 98ms 量级架构未变）、NFR-002（locales gzip +9846 B ≤ 30720 B 上限）、NFR-003（违禁词 0 + glossary 对表）、NFR-004（lint 74 基线零增量 + tsc 绿）均闭合，证据见 acceptance-matrix.json。

## 3. Drift 与缺口

- **Non-goal 侵入：无**。mission 代码改动共 16 文件（`git diff eb6aa4b5..c46fba9a --name-only`），全部落在 C-001 允许集：GraphWorkspace/**（12）、i18n/**（3）、tests（2 的最小增量：e2e 锚点 4 行、markdown 测试 i18n 种子 14 行）。零触碰 semantica/、index.html、vite.config.ts、其他工作区、认证流程（C-002）。
- **Locked decision 违反：无**。零新增依赖（C-005，package.json 依赖区零改动）；数据值不入资源（C-006）；术语以 glossary 为准（C-004）；语言状态经响应式订阅传播（C-003）。
- **Punted FR：无**。9 项 FR 全部有测试断言或实测命令证据承载，无只挂 frontmatter 的空映射。
- **跨 WP 集成**：locales 两文件由 WP02-04 串行增键（lane-b→c→d→e 链式 merge，非并行写），最终 parity 双向 diff 为空；apiError.ts（WP01）与其消费点（WP02）经套件断言联通；WP05 术语修正全部落在资源值层，无组件联动需求。

## 4. 反模式复核（跨 WP 层面）

1. **Synthetic fixture**：错误包装断言走 apiError.ts 真实映射函数，非构造字面量比对；BAND 键映射断言经真实组件渲染路径。未发现假测试。
2. **死代码**：apiError.ts 有生产消费点（GraphWorkspace.tsx:27）；新增 PanelContent 组件均被宿主 plugin 定义消费；无孤儿模块。
3. **静默空返回**：i18n 路径无 `except: return 空` 模式；localStorage 读写 try/catch 为 P0 披露的容错语义（miss ≠ 静默失败）。
4. **共享文件所有权**：locales 多 WP 共写已确认为串行链，无并行冲突；协调说明记录于 WP05 approved note。

## 5. 风险与遗留（均已披露，不阻塞）

1. **面板 title 滞后窗口**：已开面板 + 切换语言 + 无后续状态变化时，`i18next.t()` 直调的 title/chip 有一个切换周期的滞后；开面板即刷新。memo 冻结架构下的接受限制（WP03/WP04/WP05 review note 三处记录）。
2. **registryStore.logEvent summary 英文**：spec Non-goal（数据而非 chrome），P3 批次口径。
3. **RISK-1**：双语走查依赖一次性人工/脚本核验，未固化为 Playwright 常驻测试——低优先级后续。

## 6. 流程观察（供后续 mission 参考）

1. **dossier sync 覆盖验收矩阵**：`spec-kitty merge` 的 dossier 同步把已提交的实质矩阵（19 条实测证据）重写为模板骨架（"Verify FR-xxx is satisfied"）。已在 `71ce470a` 恢复。后续 mission 在 merge 后应核对 acceptance-matrix.json 是否被模板覆写。
2. **P0 代码此前未进 main**：P0 mission 的代码一直停留在 `feature/explorer-i18n-p1` 分支（main 无 i18n 基础设施）。本次 merge 把 P0+P1 一并落地 main（`7cd757aa`）。因此 `293a113b..main` 的 diff 含 P0 文件（如 i18n/index.ts 显示为 new file）——这是历史遗留的分支状态，非本次 mission 的改动。
3. **accept 命令的 path convention**：software-dev 模板期望仓库根 `src/`、`contracts/`，与本仓库布局（前端在 `explorer/`）不匹配，产生固定误报。验收实质由矩阵承载，未按误报创建空目录。
