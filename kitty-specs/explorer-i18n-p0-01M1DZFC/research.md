# Research: Explorer 中文界面 P0

**Mission**: explorer-i18n-p0-01M1DZFC · 2026-09-01 · 研究经官方文档/npm/源码核实（详见末尾来源）

## R1. 依赖版本与 React 19 兼容

- **Decision**: 锁定 `i18next@26.4.1` + `react-i18next@17.0.13`（当前 latest）。
- **Rationale**: react-i18next@17 的 peer 为 `react >= 16.8`、`i18next >= 26.2`；React Compiler 相关修复（rules-of-hooks 违规 #1863、`i18n.language` 在 memo 下不触发重渲染 PR #1884、"Maximum update depth" #1885）全部落在 **16.2.0–16.3.3**，17.0.13 天然包含 → 满足 C-003/C-006。
- **Alternatives considered**: react-i18next 16.x（需自行核对 i18next 配对，无增益）；自研 t()（用户已在决策记录中否决）。

## R2. TypeScript 键类型化与键同构（FR-006）

- **Decision**: 官方 `CustomTypeOptions` 模式 + `satisfies` 双向把关：
  ```ts
  // types.d.ts
  import type en from "./locales/en.json";
  declare module "i18next" {
    interface CustomTypeOptions {
      defaultNS: "translation";
      resources: { translation: typeof en.translation };
    }
  }
  // index.ts 组装资源
  export const resources = {
    en,
    zh: zh satisfies typeof en,   // zh 缺 en 的任何键 → 编译失败
  } as const;
  ```
- **Rationale**: `typeof en.translation` 使 `t()` 键全类型化（strict + resolveJsonRequired）；`satisfies` 拦 zh 缺键。
- **缺口与补法**：assignability 语义下 **zh 多出的键不报编译错** → 以 ui_zh_status.py 的 `extra_keys` 运行时把关（FR-008 已覆盖），并在 `zh.ts` 组装处加一个键集parity 的类型级断言（`keyof` 双向 extends，非真值则 never）作编译期兜底。
- **`__meta` 位置**：与 `translation` namespace 同级（`resources` 顶层键是语言码，`__meta` 被当作永不选中的语言，惰性无害；`CustomTypeOptions` 只引 `typeof en.translation`，meta 不污染键空间）。en.json 也保留空 `__meta` 对象以维持两文件结构同构、`satisfies` 可比。
- **Alternatives considered**: meta 放 translation 内（污染键类型）；meta 放独立 TS 模块（脚本读取需额外解析 TS，破坏"JSON 即真相"）。

## R3. 无插件初始化与语言解析（FR-002/FR-003）

- **Decision**: 应用代码内自解析语言（URL `?lang=` → localStorage → navigator.language → en），结果作 `lng` 传入 `init`；切换用 `changeLanguage`，持久化写 `i18n.resolvedLanguage`。
- **Rationale**: `lng` "overrides language detection"（无 detector 插件时的文档化路径）；init 直传 `lng` 是零闪烁路径（不传则首帧落 fallback 再闪变）；官方明确勿多次调 init。`interpolation.escapeValue: false`（React 已防 XSS）；`returnNull` 自 v21 默认 false，无需配置。`react: { useSuspense: false }` 显式关闭，避免 Suspense 边界要求。
- **Alternatives considered**: i18next-browser-languagedetector 插件（多一依赖，检测顺序自定义反而更绕）。

## R4. React Compiler 互操作（C-003）

- **Decision**: 组件内一律消费 `useTranslation()` 返回的 `t`；禁止在 memoized 回调/模块常量里直读 `i18n.language` 或缓存 `t` 的结果。
- **Rationale**: `useTranslation` 内部经 `use-sync-external-store` 订阅 `languageChanged`（17.0.13 源码核实），编译器记忆化下仍正确重渲染；手写依赖数组的旧模式正是 R1 所列 issue 的成因。模块级常量（`navItems` 等）改为渲染期经 `t()` 解析。

## R5. 体积预算（NFR-002）

- **Decision**: 采用 bundlephobia 实测口径：i18next 13.7 KB gzip + react-i18next 10.2 KB gzip + 小依赖（html-parse-stringify/use-sync-external-store）≈ **25 KB gzip**，占 50 KB 预算一半。
- **Rationale**: 两份 JSON 资源随 bundle 增量预计 5–10 KB gzip（P0 约 300 条）。合计远低于预算；build 后以实际产物复核。

## R6. e2e 英文预置（FR-009）

- **Decision**: e2e 经 `context.addInitScript` 预置 `localStorage["semantica.explorer.lang"]="en"`；检测契约（contracts/language-detection.md）保证其先于应用代码执行。
- **Rationale**: `addInitScript` 在每个导航前注入，URL `?lang=` 作为人工调试的补充路径；二者均已在检测顺序中排在最高优先级。

## 待观察项（不阻塞）

- react-i18next v15 "React 19-ready" 发布说明原文未取得（不影响选型，兼容性以 peer 范围与 16.3.3+ 修复为准）。
- `enableSelector` v26 默认值未核实（P0 不用 selector 语法，无影响）。
- 未查询的 namespace 无害结论属机制推断（meta 永不被查询，风险趋零）。

## 来源

npm registry（i18next@26.4.1、react-i18next@17.0.13 peer 数据）· [i18next TypeScript](https://www.i18next.com/overview/typescript) · [配置选项](https://www.i18next.com/overview/configuration-options) · [迁移指南](https://www.i18next.com/misc/migration-guide) · [react-i18next quick start](https://react.i18next.com/guides/quick-start) · [useTranslation](https://react.i18next.com/latest/usetranslation-hook) · react-i18next CHANGELOG（#1863、#1884、#1885）· bundlephobia API
