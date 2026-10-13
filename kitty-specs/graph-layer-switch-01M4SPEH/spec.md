# Mission: graph-layer-switch

## Mission Header

- **Mission ID:** 01M4SPEHS52KH8BKTSQ8MQMVM2
- **Type:** software-dev / single_branch
- **Op:** spec-kitty invocation 01M4SPDZBD169S4MKEVEP5TFGF (frontend-freddy)
- **Origin:** sinopharm-rebate 单实例统一视图方案 P0-2（用户裁决 2026-10-13）

## Overview

GraphWorkspace（explorer 图谱工作区）增加「图层」切换：一个单实例图同时承载业务实例、本体模式与推理边，用户通过工具栏胶囊组在视图预设间切换，并用独立开关控制推理边可见性。过滤发生在 display graph 构建之后（组合扩展），不动 sigma 渲染器与上游 graphSceneState。

## Data Contract（数据侧已定，10g 全景导出段）

- 节点：`node.properties.layer ∈ {instance, class, property, rules}`
  - 实例·X→instance；本体类→class；本体属性→property；规则库→rules
- 边：`edge.properties.layer ∈ {business, schema, inferred}`
  - 业务谓词边→business；结构边（rdf:type/subClassOf/rdfs:domain/rdfs:range）→schema；推理边→inferred（与既有 inferred=true 标志双保险）

## Functional Requirements

| FR | 需求 | 验收 |
|---|---|---|
| FR-1 | 视图预设胶囊组：全部/业务/本体，样式复用词表 Sidebar 过滤胶囊（TypeFilterChip 风格） | 胶囊组渲染于 explore-workflow-bar（SegmentedModeControl 之后），激活态高亮 |
| FR-2 | 预设过滤语义 | 业务=instance 节点+business 边；本体=class/property 节点+schema 边；全部=有 layer 的节点都显示+business/schema 边 |
| FR-3 | 无 layer 节点默认隐藏（load 注入未合并的 owl:Class/skos:Concept/sh:* 等）——仅在图存在 layer 数据时生效 | 有 layer 数据的图中，无 layer 节点不出现在任一预设 |
| FR-4 | 推理边独立开关（全局语义）：开=inferred 边参与显示，关=任何预设下 inferred 边都隐藏 | 开关即时生效，display graph 重建 |
| FR-5 | 零回归保护：图无任何 layer 数据时，过滤整体禁用、胶囊组隐藏（仿词表 presentTypes 先例） | 其他场景（无 layer 数据的图）行为与现状完全一致 |
| FR-6 | 图层过滤仅在 viewMode=full 生效；grouped/focused 下胶囊组禁用置灰 | grouped/focused 视图不触发过滤 |

## Non-goals

- 不动 sigma 渲染器、graphSceneState.ts、SigmaSceneAdapter（上游文件零改动）
- 不做 rules 节点的独立预设（rules 仅在「全部」出现；需要时再加）
- 图例/搜索/时态面板不随图层变化做特殊适配（色图例自然反映过滤后节点）

## Implementation Shape

- `explorer/src/workspaces/GraphWorkspace/graphLayers.ts`（新文件，纯函数）：layer 值域、`graphHasLayerData`、`applyLayerFilter(graph, preset, inferredEdgesEnabled)`（graphology copy + dropNode/dropEdge，仿 createCollapsedNeighborhoodGraph 先例；无 layer 数据返回 null=直通）
- `GraphWorkspace.tsx`：layerPreset/inferredEdgesEnabled state；displayResult useMemo 内后置过滤（依赖数组加入两值）；胶囊组 UI（LayerFilterChip，样式照 TypeFilterChip）；预设切换时选中节点不在新图则清空（仿 grouped reset effect 先例）
- i18n：en.json/zh.json 加 `graph.layer.*` 键；en.json 变动同提交内刷新 zh.json `__meta.source_version`

## Test Plan（Test-First）

- `explorer/src/workspaces/GraphWorkspace/graphLayers.test.ts`：纯函数覆盖 FR-2/3/4/5（预设节点/边集、无 layer 隐藏与直通、开关全局语义、dropNode 连带边清除）
- 注册进 package.json `test:graph-workspace` 显式清单
- node:test + tsx，图构造用内存 graphology 实例

## Acceptance（用户验收口径）

单实例 2731 切「业务」≈ 旧 2730 业务图（16 节点 110 边）；切「本体」= 类树+签名边；推理边开关即时生效。
