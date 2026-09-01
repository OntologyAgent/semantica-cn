# Contract: zh_status.py CLI

**Mission**: docs-zh-translation-01M1D2MJ

`tools/i18n/zh_status.py` 是唯一的新工具面，本契约固定其 CLI 形态，实现与调用方（人、Skill、未来 workflow）以此为准。

## 调用形态

```
python tools/i18n/zh_status.py [--json] [--root <repo>] [--verbose]
```

| 参数 | 默认 | 语义 |
|------|------|------|
| `--json` | off | 机器可读输出（供 Skill/workflow 消费）；缺省为人类可读表格 |
| `--root` | `./` | 仓库根；用于从任意目录运行 |
| `--verbose` | off | stale/orphan 条目附带 diff stat（`git diff <old_sha> -- <path>` 摘要行数） |

## 退出码

| 码 | 语义 |
|----|------|
| 0 | 扫描完成；允许存在 stale/orphan（这是工具的正常产出，不是错误） |
| 1 | 用法/环境错误（git 不可用、`--root` 非 git 仓库） |
| 2 | `docs/zh/` 不存在或无任何译文（提示而非 traceback） |

## JSON 输出 schema

```json
{
  "generated_at": "ISO-8601",
  "summary": {"fresh": 0, "stale": 0, "orphan": 0},
  "entries": [
    {
      "path": "docs/zh/quickstart.md",
      "source": "quickstart.md",
      "status": "stale",
      "recorded_source_sha": "b0679d4f…",
      "current_source_sha": "f3c540cf…"
    }
  ]
}
```

## 行为规则

- 扫描对象：`docs/zh/**/*.md`，解析 frontmatter 的 `source` 与 `source_version`
- `source_version` 缺失或非法的译文按 `stale` 处理并在输出中标注原因（`missing_source_version`）
- 判定基准是 HEAD 的 blob sha，不含工作区未提交改动（避免半成品状态误报）
- 只读工具：不修改任何文件，不写缓存
- 性能预算：83 文件规模 ≤5s（逐文件 `git rev-parse` 的子进程开销可控；必要时合并为单次 `git ls-tree` 优化）
