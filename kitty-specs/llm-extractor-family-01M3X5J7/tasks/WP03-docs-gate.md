---
work_package_id: WP03
title: 文档与收口
dependencies:
- WP01
- WP02
requirement_refs:
- FR-007
tracker_refs: []
planning_base_branch: feature/llm-extractor-family
merge_target_branch: feature/llm-extractor-family
branch_strategy: Planning artifacts for this mission were generated on feature/llm-extractor-family. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feature/llm-extractor-family unless the human explicitly redirects the landing branch.
subtasks:
- T006
- T007
history: []
agent_profile: python-pedro
authoritative_surface: docs_zh/integrations/mineru.md
create_intent: []
execution_mode: code_change
owned_files:
- docs_zh/integrations/mineru.md
- README.zh-CN.md
role: implementer
tags: []
agent: "python-pedro"
shell_pid: "81050"
---

# WP03 — 文档与收口

## Purpose

MinerU 4.0.10 支持说明 + 全量门禁。

## 要点

1. docs_zh/integrations/mineru.md 顶部 Note：fork 支持 MinerU 4.x（当前 4.0.10）——双代 API 自动探测、`parse-mineru` extra 装 `mineru[torch]>=4.0,<5`、backend→tier 映射（pipeline→basic、vlm*→standard）；官方 semantica 钉 2.x。注意同步 frontmatter source_version（若英文源未变则不更新 sha）
2. README.zh-CN.md fork 声明段补一句 MinerU 4 支持
3. `bash tools/nightly/run_gate.sh` exit 0；quickstart §3 命令逐条实跑（mock 不打真实 API 的部分）

## 验收

```bash
bash tools/nightly/run_gate.sh && echo GATE-OK
```

## Activity Log

- 2026-10-02T04:17:36Z – python-pedro – shell_pid=81050 – Assigned agent via action command
- 2026-10-02T04:18:09Z – python-pedro – shell_pid=81050 – docs landed; gate next
