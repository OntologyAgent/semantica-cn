# Contract: ui_zh_status.py CLI

**Mission**: explorer-i18n-p0-01M1DZFC

`tools/i18n/ui_zh_status.py` 是本 mission 唯一新增工具面，契约固定其 CLI 形态。机制镜像 `tools/i18n/zh_status.py`（见 `kitty-specs/docs-zh-translation-01M1D2MJ/contracts/zh-status-cli.md`），把"文档对文档"换成"键资源对键资源"。

## 调用形态

```
python tools/i18n/ui_zh_status.py [--json] [--root <repo>] [--verbose]
```

| 参数 | 默认 | 语义 |
|------|------|------|
| `--json` | off | 机器可读输出；缺省为人类可读表格 |
| `--root` | `./` | 仓库根；用于从任意目录运行 |
| `--verbose` | off | stale 时附键级 diff 统计（missing/extra 计数） |

## 退出码

| 码 | 语义 |
|----|------|
| 0 | 扫描完成；允许存在 stale/orphan（正常产出，非错误） |
| 1 | 用法/环境错误（git 不可用、`--root` 非 git 仓库） |
| 2 | `explorer/src/i18n/locales/` 不存在或缺 en.json/zh.json 任一（提示而非 traceback） |

## JSON 输出 schema

```json
{
  "generated_at": "ISO-8601",
  "summary": {"fresh": 0, "stale": 0, "orphan": 0, "missing_keys": 0, "extra_keys": 0},
  "entries": [
    {
      "path": "explorer/src/i18n/locales/zh.json",
      "source": "explorer/src/i18n/locales/en.json",
      "status": "stale",
      "recorded_source_sha": "b0679d4f…",
      "current_source_sha": "f3c540cf…",
      "missing_keys": ["nav.analyze.label"],
      "extra_keys": []
    }
  ]
}
```

## 行为规则

- 源基准：HEAD 中 `explorer/src/i18n/locales/en.json` 的 blob sha（单次 `git ls-tree` 取回）。
- 版本钉：读 zh.json 顶层 `__meta.source_version`（40 位 hex；缺失/非法按 `stale`，原因 `missing_source_version`）。
- 判定基准是 HEAD，不含工作区未提交改动（与 zh_status.py 同哲学）。
- 键级比对：`translation` namespace 下收集全部叶子键（flat 点号键）；`en 有 zh 无` 记 `missing_keys`，`zh 有 en 无` 记 `extra_keys`；sha 一致时仍做键比对（防 sha 忘刷但键已漂移）。
- `__meta` 本身不计入键集合。
- 只读工具：不修改任何文件，不写缓存。
- 性能预算：单文件对单文件 + 一次 ls-tree，<1s。
