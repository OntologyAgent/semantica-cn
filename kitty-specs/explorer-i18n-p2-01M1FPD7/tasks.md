# Tasks: Explorer 中文界面 P2（剩余工作区全量）

**Mission**: `explorer-i18n-p2-01M1FPD7` · Branch: `feature/explorer-i18n-p2` · Generated: 2026-09-02

**执行模型说明**：WP01→WP08 为串行依赖链（单 lane）。原因与 P1 相同：`t()` 经 P0 `CustomTypeOptions` 全类型化，组件抽取与 locales 键增补必须同步（缺键 = tsc 报错），而 `locales/{en,zh}.json` 是所有 WP 的共享汇聚点——串行执行避免并行 merge 冲突。各抽取 WP 对 locales 的增补相对其 `owned_files` 是"well-justified out-of-map edit"，已逐 WP 在 Execution Notes 记录 rationale；locales 的 `owned_files` 归属 WP08（资源收口），由其做终检与 `source_version` 刷新。

## Subtask Index

| ID | Description | WP | Parallel |
| --- | --- | --- | --- |
| T001 | 推理引擎页抽取：标题/快捷模板/事实规则编辑区/写入推断开关/运行按钮/结果面板与空态 → `reasoning.*` | WP01 | |
| T002 | SPARQL 页抽取：编辑器框架/执行按钮/结果表/错误提示 → `sparql.*`（模板内容不译） | WP01 | |
| T003 | 决策页抽取：列表/过滤框/空态/详情面板 → `decision.*` | WP01 | |
| T004 | WP01 键段写入 en/zh + `npm run build` 键同构校验 | WP01 | |
| T005 | 导入导出抽取：拖放区/格式说明/上传下载按钮/What's included → `importExport.*` | WP02 | |
| T006 | 差异与合并抽取 → `diffMerge.*` | WP02 | |
| T007 | 实体消解抽取 → `entityResolution.*` | WP02 | |
| T008 | 注册表抽取 → `registry.*`（审计 summary 为数据串按 Non-goal 豁免并记录） | WP02 | |
| T009 | WP02 键段写入 en/zh + 键同构校验 | WP02 | |
| T010 | PROV-O 谱系抽取：输入框/Trace/导出/空态 → `lineage.*` | WP03 | |
| T011 | KG 概览抽取：统计卡/类型分布/高度连接节点/刷新 → `kgOverview.*`（ORG/DATE 等数据值不译） | WP03 | |
| T012 | 本体概要抽取 → `ontologySummary.*` | WP03 | |
| T013 | WP03 键段写入 en/zh + 键同构校验 | WP03 | |
| T014 | Hub 壳层与 index 抽取 → `ontologyHub.shell.*` | WP04 | |
| T015 | OntologyManager（注册表主面板）抽取 → `ontologyHub.manager.*` | WP04 | |
| T016 | OntologyLoader 抽取 → `ontologyHub.loader.*` | WP04 | |
| T017 | OntologySearch 抽取 → `ontologyHub.search.*` | WP04 | |
| T018 | WP04 键段写入 en/zh + 键同构校验 | WP04 | |
| T019 | OntologyEditor 抽取 → `ontologyHub.editor.*` | WP05 | |
| T020 | AlignmentsTab 抽取 → `ontologyHub.alignments.*` | WP05 | |
| T021 | VersionsTab 抽取 → `ontologyHub.versions.*` | WP05 | |
| T022 | HealthTab 抽取 → `ontologyHub.health.*` | WP05 | |
| T023 | WP05 键段写入 en/zh + 键同构校验 | WP05 | |
| T024 | ShaclStudio 抽取 → `ontologyHub.shacl.*` | WP06 | |
| T025 | ProposalReview 抽取 → `ontologyHub.proposal.*` | WP06 | |
| T026 | SKOSVocabularyManager 抽取 → `ontologyHub.skos.*` | WP06 | |
| T027 | WP06 键段写入 en/zh + 键同构校验 | WP06 | |
| T028 | VocabularyWorkspace 五文件抽取 → `vocabulary.*` | WP07 | |
| T029 | `ui/primitives.tsx` 用户可见英文默认值清扫（仅文案默认值） | WP07 | |
| T030 | 全局残留英文扫描（workspaces 全目录 + 非组件层），结果记入 Execution Notes | WP07 | |
| T031 | 刷新 `__meta.source_version` + `ui_zh_status` fresh 验证 | WP08 | |
| T032 | 四套测试全绿 + lint/build 零增量 + gzip 增量实测（NFR-002） | WP08 | |
| T033 | 残留终扫零命中 + 术语表一致率核对（违禁词 0） | WP08 | |
| T034 | 双语走查（quickstart §2-§5）+ 语言切换/lang-title/回落验证，结果记入 Execution Notes | WP08 | |

## Work Packages

### WP01 — 分析工作区抽取（推理引擎 · SPARQL · 决策）

**Goal**: 三个分析页（约 793 行）文案全量抽取为 `reasoning.*` / `sparql.*` / `decision.*` 键段，覆盖用户高频分析路径。
**Priority**: High（链首） · **Independent test**: `npm run build`（键同构）+ 分析页 `?lang=zh` 无英文框架残留
**Prompt**: `tasks/WP01-analysis-workspaces-extraction.md` · ~300 lines

- [ ] T001 推理引擎页抽取（WP01）
- [ ] T002 SPARQL 页抽取（WP01）
- [ ] T003 决策页抽取（WP01）
- [ ] T004 WP01 键段写入 en/zh + 键同构校验（WP01）

Dependencies: none。Risks: facts/rules 语法示例与 SPARQL 模板内容属数据/代码不译（FR-010），仅框架文案入键。

### WP02 — 增强工作区四页签抽取（导入导出 · 差异合并 · 实体消解 · 注册表）

**Goal**: 增强工作区四个页签（约 1055 行）文案抽取为 `importExport.*` / `diffMerge.*` / `entityResolution.*` / `registry.*`。
**Priority**: High · **Independent test**: `npm run build` + 增强页四页签 `?lang=zh` 走查
**Prompt**: `tasks/WP02-enhance-workspaces-extraction.md` · ~300 lines

- [ ] T005 导入导出抽取（WP02）
- [ ] T006 差异与合并抽取（WP02）
- [ ] T007 实体消解抽取（WP02）
- [ ] T008 注册表抽取（WP02）
- [ ] T009 WP02 键段写入 en/zh + 键同构校验（WP02）

Dependencies: WP01。Risks: JSON/CSV 切换按钮属界面文案；拖放区支持格式（.json/.csv）为数据值；注册表审计 summary 按既定豁免并记录。

### WP03 — 管理工作区三页签抽取（谱系 · KG 概览 · 本体概要）

**Goal**: 管理工作区三个页签（约 1105 行）文案抽取为 `lineage.*` / `kgOverview.*` / `ontologySummary.*`。
**Priority**: High · **Independent test**: `npm run build` + 管理页三页签 `?lang=zh` 走查
**Prompt**: `tasks/WP03-manage-workspaces-extraction.md` · ~280 lines

- [ ] T010 PROV-O 谱系抽取（WP03）
- [ ] T011 KG 概览抽取（WP03）
- [ ] T012 本体概要抽取（WP03）
- [ ] T013 WP03 键段写入 en/zh + 键同构校验（WP03）

Dependencies: WP02。Risks: 节点/边类型枚举值（ORG/DATE/part_of）来自数据不译；PROV-O/Ontology Hub 标准名保留英文。

### WP04 — Ontology Hub 主体抽取（index · Manager · Loader · Search）

**Goal**: Hub 四个主体文件（约 2552 行）文案抽取为 `ontologyHub.shell/manager/loader/search.*` 键段，本期体量最大 WP。
**Priority**: High · **Independent test**: `npm run build` + Hub 打开态 `?lang=zh` 走查
**Prompt**: `tasks/WP04-ontology-hub-core-extraction.md` · ~340 lines

- [ ] T014 Hub 壳层与 index 抽取（WP04）
- [ ] T015 OntologyManager 抽取（WP04）
- [ ] T016 OntologyLoader 抽取（WP04）
- [ ] T017 OntologySearch 抽取（WP04）
- [ ] T018 WP04 键段写入 en/zh + 键同构校验（WP04）

Dependencies: WP03。Risks: 文件大（Manager 930 行、Loader 913 行），逐区块抽取防漏项；本体 URI/类别过滤值（OWL/SKOS/INTERNAL/EXTERNAL 枚举值本身）不译。

### WP05 — Ontology Hub 治理页签抽取（Editor · Alignments · Versions · Health）

**Goal**: Hub 四个治理页签（约 1695 行）文案抽取为 `ontologyHub.editor/alignments/versions/health.*`。
**Priority**: High · **Independent test**: `npm run build` + 对应页签 `?lang=zh` 走查
**Prompt**: `tasks/WP05-ontology-hub-governance-extraction.md` · ~300 lines

- [ ] T019 OntologyEditor 抽取（WP05）
- [ ] T020 AlignmentsTab 抽取（WP05）
- [ ] T021 VersionsTab 抽取（WP05）
- [ ] T022 HealthTab 抽取（WP05）
- [ ] T023 WP05 键段写入 en/zh + 键同构校验（WP05）

Dependencies: WP04。Risks: 表单校验错误提示量大且重复，优先共用键；OWL/SHACL 术语保留。

### WP06 — Ontology Hub 工作室与评审抽取（SHACL · Proposal · SKOS Manager）

**Goal**: Hub 剩余三个文件（约 1488 行）文案抽取为 `ontologyHub.shacl/proposal/skos.*`。
**Priority**: High · **Independent test**: `npm run build` + 对应页签 `?lang=zh` 走查
**Prompt**: `tasks/WP06-ontology-hub-studio-extraction.md` · ~300 lines

- [ ] T024 ShaclStudio 抽取（WP06）
- [ ] T025 ProposalReview 抽取（WP06）
- [ ] T026 SKOSVocabularyManager 抽取（WP06）
- [ ] T027 WP06 键段写入 en/zh + 键同构校验（WP06）

Dependencies: WP05。Risks: SHACL 约束示例与 shapes 数据不译；提案 diff 内容属数据值。

### WP07 — 词表工作区与全局清扫

**Goal**: SKOS 词表五个文件（约 487 行）抽取为 `vocabulary.*`；`ui/primitives.tsx` 文案默认值清扫；全站残留英文兜底扫描。
**Priority**: Medium（收口清扫，须在其余抽取完成后执行） · **Independent test**: `npm run build` + 残留扫描结果记录
**Prompt**: `tasks/WP07-vocabulary-sweep.md` · ~240 lines

- [ ] T028 VocabularyWorkspace 五文件抽取（WP07）
- [ ] T029 primitives 文案默认值清扫（WP07）
- [ ] T030 全局残留英文扫描（WP07）

Dependencies: WP06。Risks: 若扫描发现 GraphWorkspace 内遗漏，属 P1 回归，修复须单独记录并保持最小改动（IC-05 风险条款）。

### WP08 — 资源收口与全量验证

**Goal**: `source_version` 刷新、键同构终检、四套测试、lint/build 零增量、gzip 实测、残留终扫、术语核对、双语走查。
**Priority**: High（发布门） · **Independent test**: quickstart §1-§7 全部通过
**Prompt**: `tasks/WP08-resource-finalization-verification.md` · ~300 lines

- [ ] T031 source_version 刷新 + ui_zh_status fresh（WP08）
- [ ] T032 四套测试 + lint/build + gzip 实测（WP08）
- [ ] T033 残留终扫 + 术语核对（WP08）
- [ ] T034 双语走查 + 切换/回落验证（WP08）

Dependencies: WP07。Risks: gzip 增量须实测确认 ≤60KB（NFR-002）；如超限需评估键压缩策略并记录。

## Requirement Coverage

| FR/NFR | WPs |
| --- | --- |
| FR-001 | WP01 |
| FR-002 | WP01 |
| FR-003 | WP02 |
| FR-004 | WP03 |
| FR-005 | WP04, WP05, WP06 |
| FR-006 | WP01, WP02, WP03, WP04, WP05, WP06, WP07, WP08 |
| FR-007 | WP08 |
| FR-008 | WP01, WP02, WP03, WP04, WP05, WP06, WP08 |
| FR-009 | WP08 |
| FR-010 | WP01, WP02, WP03, WP04, WP05, WP06, WP07 |
| FR-011 | WP08 |
| FR-012 | WP08 |
| NFR-001 | WP08 |
| NFR-002 | WP08 |
| NFR-003 | WP08 |
| NFR-004 | WP08 |
