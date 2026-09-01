# Quickstart: Explorer 中文界面 P1 验证

前置：`cd explorer && npm ci`（依赖与 P0 相同，零新增）。

## 1. 构建与静态校验

```bash
cd explorer
npm run lint            # 零增量（不引入新错误）
npm run build           # tsc -b 含键同构校验（INV-1）；构建产物落 semantica/static/
```

## 2. 既有测试全绿（FR-008）

```bash
npm run test:graph-workspace
npm run test:graph-store
npm run test:plugin-registry
npm run test:deterministic-e2e     # Playwright；?lang=en 预置后 "Zoom In" 锚点不变
```

## 3. 译文过期追踪（FR-009）

```bash
python tools/i18n/ui_zh_status.py   # explorer UI 资源报告 fresh
```

## 4. 手动走查（中文场景）

```bash
python -m semantica.explorer --graph projects/stock/output_llm/graph.json --port 8000
# 浏览器 zh 语言环境打开 http://localhost:8000?lang=zh → 打开探索工作区
```

逐屏核对（数据值豁免：节点/边 label、ORG/PERSON/PRODUCT 等类型值保持原文）：

- [ ] 搜索栏：placeholder 与按钮中文
- [ ] 工具栏：CAMERA/LAYOUT/ANALYSIS/UTILITY 分组与按钮（Zoom In/Out、Effects、Neighbors、Temporal、Run 等）中文
- [ ] 图例：框架文案 + 固定枚举标签（Biomolecule/Condition/Compound/Process/Community/Other）中文
- [ ] 时间轴：标题、播放控制、刻度框架文案中文
- [ ] Inspector 面板中文
- [ ] 会话加载态/失败面板（标题、说明、重试按钮）中文

## 5. 语言切换即时性（FR-002/NFR-001）

点击头部语言开关 中/EN → 工作区全部文案即时切换、页面不刷新 → 刷新后保持目标语言；`<html lang>` 与标签页标题同步（`探索 · Semantica` / `Semantica Knowledge Explorer`）。

## 6. 401 包装（FR-003）

```bash
# 后端设 key 且关闭匿名（不放行匿名时）
SEMANTICA_API_KEY=test-key python -m semantica.explorer --graph <graph.json>
# 前端无 key 请求 → 界面出现中文包装提示（如"认证失败：API key 无效或缺失"），
# 且后端 detail 原文（"Invalid or missing API key. Send it as the X-API-Key header."）仍完整可见。
```

## 7. 英文回归（FR-006 口径）

`?lang=en` 打开 → 探索工作区可见文案与改造前逐字一致（数据值豁免同口径）。
