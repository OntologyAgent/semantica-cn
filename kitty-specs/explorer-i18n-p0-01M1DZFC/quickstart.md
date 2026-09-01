# Quickstart: Explorer 中文界面 P0 验证

**Mission**: explorer-i18n-p0-01M1DZFC

实现完成后的端到端验证路径。前置：`cd explorer && npm ci`（引入 i18next/react-i18next 后首次必须）。

## 1. 静态门禁（必须全绿）

```bash
cd explorer
npm run lint                    # ESLint 零错误
npm run build                   # tsc -b（键同构在此把关）+ vite build → ../semantica/static
npm run test:graph-store        # 既有单测
npm run test:graph-workspace    # 既有单测（含确定性渲染）
npm run test:plugin-registry
npm run test:deterministic-e2e  # Playwright：强制英文预置后必须全绿
```

## 2. 译文过期检查

```bash
python tools/i18n/ui_zh_status.py            # 期望: fresh=1（zh 相对 en 基准一致）
python tools/i18n/ui_zh_status.py --json     # 机器可读，summary.missing_keys=0 extra_keys=0
```

## 3. 手动端到端（浏览器）

```bash
# 方式 A：开发模式（两个终端）
semantica-explorer --graph <样例>.json --no-browser   # 终端 1，后端 :8000
cd explorer && npm run dev                            # 终端 2，前端 :5173

# 方式 B：整包模式
cd explorer && npm run build && semantica-explorer --graph <样例>.json
```

走查清单（对应 spec 成功标准）：

1. 浏览器语言设为中文 → 打开 `http://localhost:5173` → 主导航六项、首屏、页签、连接状态全中文。
2. 点头部语言开关切 EN → 文案即时变英文，页面不刷新。
3. 刷新 → 仍英文；切回中文并刷新 → 保持中文。
4. 地址栏加 `?lang=en` 强制 → 英文（无论存储偏好）。
5. `<html lang>` 与标签页标题随语言变化（DevTools 查看）。
6. 浏览器语言设为英文并清站点数据 → 界面与改造前完全一致（全英文）。
7. 断开后端 → 连接状态提示显示当前语言文案。

## 4. 术语一致性抽查

P0 范围中文文案对照 `docs/zh/glossary.md`：知识图谱、本体、本体中心（Ontology Hub 保留英文）、溯源、实体消解、决策智能、工作区（不用"工作台"）。
