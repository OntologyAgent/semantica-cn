# Quickstart: Explorer 中文界面 P2（剩余工作区全量）

验证场景与走查清单。实现完成后按 §1-§7 顺序执行并记录结果。

## §1 环境与构建

```bash
cd explorer
npm run lint                     # 74 基线零增量（57 errors + 17 warnings）
npm run build                    # tsc -b 严格模式 exit 0（INV-1 键同构门）
npm run test:graph-workspace && npm run test:graph-store \
  && npm run test:plugin-registry && npm run test:deterministic-e2e   # 四套全绿
```

构建产物体积核对（NFR-002）：locales 相对 P2 基线 gzip 增量 ≤ 60KB。

## §2 中文全量走查（默认 zh 或 ?lang=zh）

逐屏核对 0 处英文残留（数据值豁免）：

1. **分析**：推理引擎页（前向链标题、快捷模板、事实/规则编辑区、写入推断开关、Run Reasoning、结果面板空态 "Ready to reason" 同位文案）；SPARQL 页（编辑器框架、执行按钮、结果表、错误提示）。facts/rules 示例与 SPARQL 模板内容保持原样（数据豁免）。
2. **决策**：列表标题、过滤框占位、空态（"No decisions"/"No decision selected" 同位文案）、详情面板（决策链/因果上下文/先例匹配）。
3. **增强**：导入与导出（拖放区、格式说明、Upload to Graph、Export Graph Snapshot、Download Export、What's included、FORMAT）、差异与合并、实体消解、注册表四页签。
4. **管理**：PROV-O 谱系（Enter Node ID 占位、Trace、Export JSON/MD、谱系图空态）、KG 概览（统计卡 NODES/EDGES/DENSITY、类型分布标题、TOP CONNECTED NODES、Refresh）、本体概要。节点/边类型值（ORG/DATE/part_of）保持原样。
5. **Ontology Hub**：注册表（搜索占位、All/OWL/SKOS/INTERNAL/EXTERNAL 过滤、Entity Search、Load Ontology、空态）、Editor、Versions、Alignments、Health、SHACL 工作室、提案评审、SKOS 词表管理器全部页签。
6. **词表**（探索 → 词表页签）：ConceptTree/PropertyPanel/导入拖放区等。

## §3 语言切换

- 逐工作区切换 中 ↔ EN：全部文案即时切换、页面不刷新。
- `<html lang>` 与标签页标题同步（`探索 · Semantica` / `Semantica Knowledge Explorer`）。
- 刷新后语言保持；禁用 localStorage 后切换仍可用（回落自动检测）。

## §4 英文回归

- `?lang=en` 抽查每工作区主要界面与改造前逐字一致（FR-008 英文不变口径）。
- deterministic-e2e 绿（锚点 `Semantica Explorer`、`Zoom In` 不变）。

## §5 错误与空态

- 后端不可达/401：各工作区错误提示为中文包装 + detail 英文原文可见（apiError 通道）。
- 空数据态：决策空态、本体空态（"No ontologies loaded yet" 同位）、版本/对齐空态均随语言切换。

## §6 术语核对（NFR-003）

- `zh.json` 违禁词 0：知识探索器/工作台/工作空间/探索器（单用）。
- 标准名保留：SPARQL、SHACL、SKOS、OWL、PROV-O、Ontology Hub、Semantica。
- 抽查术语与 `docs/zh/glossary.md` 一致：推理/决策智能/实体消解/注册表/谱系/本体/溯源。

## §7 过期追踪（FR-012）

```bash
python tools/i18n/ui_zh_status.py          # fresh=1 stale=0 missing=0 extra=0
python tools/i18n/ui_zh_status.py --json   # 同 fresh
```
