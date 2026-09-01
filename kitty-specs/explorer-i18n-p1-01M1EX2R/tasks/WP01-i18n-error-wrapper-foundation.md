---
work_package_id: WP01
title: i18n 错误包装基础与 e2e 锚定（Foundation）
dependencies: []
requirement_refs:
- FR-003
- FR-008
tracker_refs: []
planning_base_branch: feature/explorer-i18n-p1
merge_target_branch: feature/explorer-i18n-p1
branch_strategy: Planning artifacts for this mission were generated on feature/explorer-i18n-p1. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feature/explorer-i18n-p1 unless the human explicitly redirects the landing branch.
subtasks:
- T001
- T002
- T003
agent: claude
history:
- timestamp: '2026-09-02T00:00:00Z'
  action: created
  agent: claude
agent_profile: frontend-freddy
authoritative_surface: explorer/src/i18n/
create_intent:
- explorer/src/i18n/apiError.ts
- explorer/src/i18n/locales/en.json
- explorer/src/i18n/locales/zh.json
- explorer/tests/deterministicExplorerRendering.e2e.ts
execution_mode: code_change
owned_files:
- explorer/src/i18n/apiError.ts
- explorer/tests/deterministicExplorerRendering.e2e.ts
role: implementer
tags: []
---

## ⚡ Do This First: Load Agent Profile

Before reading anything else, load your assigned agent profile:

```
/ad-hoc-profile-load frontend-freddy
```

If that command is unavailable, proceed as a careful frontend implementer: TypeScript strict（`erasableSyntaxOnly` 禁 enum/namespace）、React 19 函数组件、零新增依赖（C-005）。

## Objective

为 P1 探索工作区国际化建立错误包装地基与 e2e 锚定：

1. 新增 `explorer/src/i18n/apiError.ts`——把 API 响应错误转成「中文包装提示 + 后端 detail 原文」的结构，供后续 WP（WP02/WP03）在错误渲染点接入。
2. 在 `locales/en.json` / `locales/zh.json` 增补 `graph.errors.*` 键段（包装文案的键空间入口）。
3. deterministic-e2e 的 `page.goto(BASE_URL)` 加 `?lang=en` 预置，显式锚定英文，防止后续抽取改变默认语言判断时锚点漂移。

完成后：`npm run build` 绿（键同构校验通过）、e2e 全绿、`apiError.ts` 可被后续 WP 直接 import。

## Context

- **P0 已就位的 i18n 设施**（勿改动其机制）：
  - `explorer/src/i18n/index.ts`——i18next 初始化、四级语言检测（`?lang=` → localStorage → navigator → en）、`fallbackLng: 'en'`、`languageChanged` 事件同步 `<html lang>` 与标题。
  - `locales/en.json` 是键基准（P0 期 107 键）；`zh.json` 经 `satisfies typeof en.translation` 同构校验（INV-1：任一侧缺键/多键在 `tsc` 报错）。
  - `zh.json` 顶层 `__meta.source_version` 记录翻译时的 en.json blob sha（i18next 忽略该键；本 WP **不刷新**它，收口归 WP05）。
- **401 现状**：后端设 `SEMANTICA_API_KEY` 后，保护路由全部返回 401，detail 为英文原文（如 `"Invalid or missing API key. Send it as the X-API-Key header."`，见 `semantica/explorer/dependencies.py`）。前端目前无任何认证/错误包装代码。
- **fetch 无集中层**：前端各 workspace 直接 `fetch()`。本 WP 只建纯函数模块，不接任何调用点（接入是 WP02/WP03 的事，且接入点文件归它们所有）。

## Implementation Guidance

### T001 — 新建 `explorer/src/i18n/apiError.ts`

纯函数模块，零 React 依赖（不 hook、不订阅），便于任意组件消费。

```ts
// 期望对外形状（可按实现微调，但必须覆盖以下语义）：
export interface ApiErrorView {
  /** 中文包装提示的 i18n 键（graph.errors.* 段） */
  wrapperKey: string;
  /** 后端 detail 原文；拿不到时为空串，消费侧据此决定是否渲染该段 */
  detail: string;
}
export function describeApiError(status: number | undefined, body: unknown): ApiErrorView
export async function describeResponseError(response: Response): Promise<ApiErrorView>
```

行为规格：

- **状态码 → wrapperKey 映射**（键名见 T002）：401 → `graph.errors.unauthorized`；403 → `graph.errors.forbidden`；404 → `graph.errors.notFound`；5xx → `graph.errors.serverError`；其余 4xx → `graph.errors.requestFailed`。
- **网络异常**（fetch reject / TypeError）由调用方传 `status: undefined` 表达 → `graph.errors.network`。
- **detail 提取**：`body` 为对象且 `detail` 为字符串时原样取用——**不截断、不改写、不翻译**（FR-003 硬约束）。body 非 JSON / detail 缺失 / detail 非字符串 → `detail: ""`，消费侧隐藏该段而不是显示空段。
- `describeResponseError` 内部 `response.json()` 必须 try/catch 包裹（空 body、HTML 错误页都不能抛）。解析失败按 `detail: ""` 处理。
- **不吞异常**：解析失败的静默降级仅限 detail 字段；包装函数本身不捕获调用方逻辑错误。

### T002 — locales 增补 `graph.errors.*` 键段

`en.json` 与 `zh.json` **同步**增补（同构校验要求两侧同时落键），命名空间挂 `graph.`（P1 工作区键段前缀，浅两级以内）：

| 键 | en | zh（术语基准 docs/zh/glossary.md） |
| --- | --- | --- |
| `graph.errors.unauthorized` | Authentication failed: the API key is invalid or missing. | 认证失败：API key 无效或缺失。 |
| `graph.errors.forbidden` | Access denied: this key lacks permission for the requested resource. | 没有访问权限：当前 API key 无权访问该资源。 |
| `graph.errors.notFound` | Resource not found. | 资源不存在。 |
| `graph.errors.serverError` | Server error: the backend failed to complete the request. | 服务错误：后端处理请求失败。 |
| `graph.errors.requestFailed` | Request failed. | 请求失败。 |
| `graph.errors.network` | Network error: the server could not be reached. | 网络错误：无法连接服务器。 |
| `graph.errors.detailPrefix` | Backend message | 后端返回 |

en 值即原文英文（英文用户所见与包装前语义一致）；zh 译文措辞可在实现时按中文习惯微调，但"认证失败"对应 401 的口径不变。

**Ownership rationale（out-of-map edit）**：本 WP `owned_files` 不含 locales（避免与 WP05 冲突）；此处增补属"键空间骨架先行"的必要编辑，在此记录一行 rationale。改动仅限新增键，不碰 P0 既有 107 键。

### T003 — e2e `?lang=en` 预置

`explorer/tests/deterministicExplorerRendering.e2e.ts` 仅改一行：

```ts
// before
await page.goto(BASE_URL);
// after
await page.goto(`${BASE_URL}?lang=en`);
```

- `?lang=` 是 P0 检测链第 1 优先级（`resolveInitialLanguage()`），显式锚定后默认语言判断再变也不影响锚点。
- **定位器不改**：`getByRole("button", { name: "Zoom In" })`（GraphWorkspace 工具栏）与 `/Open Semantica Explorer/`（App 层）在本 mission 中英文键值与原文一致，始终命中。
- 改完跑 `npm run test:deterministic-e2e` 验证全绿。
- 若后续 WP 报告该定位器失效，仅允许最小调整且必须在 WP 完成说明中显式记录（spec Assumptions）。

## Validation

- [ ] `cd explorer && npm run build` 绿——键同构校验通过（en/zh 两侧 graph.errors.* 齐全）
- [ ] `npm run test:deterministic-e2e` 全绿
- [ ] `npm run lint` 零增量（相对改造前 74 条存量，不新增）
- [ ] `apiError.ts` 无 React import、无副作用（import 该模块不触发任何 IO）
- [ ] P0 既有键零改动（`git diff explorer/src/i18n/locales/` 仅见新增行）

## Risks

- 后端 detail 形态多样（纯文本/JSON `{detail: ...}`/HTML 错误页）——T001 的防御性解析必须全覆盖，宁降级 detail 为空也不抛异常。
- e2e 是 Playwright 真浏览器测试，本机代理可能影响——失败时先确认是否网络环境问题再排查改动。
- 不要顺手"修"其他 i18n 文件或接入任何调用点——那是后续 WP 的 owned 范围（WP 隔离纪律）。

## Reviewer Guidance

- 核对 `apiError.ts`：状态码映射完整、detail 原样保留、解析失败不抛。
- 核对 locales diff：仅 graph.errors.* 新增键、两侧同构。
- 核对 e2e diff：仅 goto 一行变化。
