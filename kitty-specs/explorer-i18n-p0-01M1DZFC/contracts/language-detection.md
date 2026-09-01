# Contract: 语言检测、持久化与切换

**Mission**: explorer-i18n-p0-01M1DZFC

前端语言解析与切换的对外可见行为契约。实现于 `explorer/src/i18n/index.ts` 与 `LanguageToggle.tsx`。

## 检测顺序（应用启动时解析一次，取先命中者）

1. URL 查询参数 `?lang=`，合法值 `en|zh`（供 e2e 与深链强制语言）
2. `localStorage["semantica.explorer.lang"]`，合法值 `en|zh`
3. `navigator.language` 前缀 `zh`（zh / zh-CN / zh-TW…）→ `zh`
4. 兜底 `en`

任一步读取抛异常（隐私模式、禁用存储）视为该步未命中，继续下一步。解析结果作为 `lng` 传入 i18next 初始化。

## 切换行为（语言开关）

| 步骤 | 行为 |
| --- | --- |
| 1 | 调用 i18n 运行时切换语言（不刷新页面、不重挂应用根） |
| 2 | 尝试写 `localStorage["semantica.explorer.lang"]`；失败静默（切换仅本次会话生效） |
| 3 | 同步 `document.documentElement.lang`（`zh → "zh-CN"`，`en → "en"`） |
| 4 | 同步 `document.title`（`zh → "知识探索器 · Semantica"`，`en → "Semantica Knowledge Explorer"`） |

步骤 3/4 由 i18n 运行时的语言变更事件驱动（含 `?lang=`/localStorage 初始化命中的场景），不依赖开关组件。

## 取译行为

- 缺失键、加载失败一律回落英文原文（`fallbackLng: 'en'`）；UI 层永不出现键名或空白（FR-005）。
- 语言切换在 1 秒内完成 P0 范围文案重渲染（NFR-001）；切换经订阅机制传播（C-003），禁止可变全局变量。

## e2e 预置契约

自动化端到端测试以步骤 1/2 任一机制固定英文：导航 URL 带 `?lang=en`，或测试上下文 `addInitScript` 预置 localStorage。二者必须先于应用代码执行（`addInitScript` 天然满足；URL 参数在初始化解析时消费）。该预置是对上游 e2e 文件的唯一允许改动（C-001）。

## 存储键（对外可见面）

| 键 | 值域 | 写入方 |
| --- | --- | --- |
| `semantica.explorer.lang` | `en` \| `zh` | 语言开关（用户显式选择时） |

命名空间 `semantica.explorer` 与后端 API key 环境变量（`SEMANTICA_API_KEY`）无关联，仅浏览器本地。
