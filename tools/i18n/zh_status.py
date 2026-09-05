#!/usr/bin/env python3
"""zh_status — 检查 docs/zh/ 译文相对英文源的新鲜度。

对比每篇译文 frontmatter 记录的 source_version（翻译时英文源的 git blob
sha）与 HEAD 中该源文件当前的 blob sha，判定 fresh / stale / orphan：

- fresh:  记录的 sha 与 HEAD 一致，源文件未变。
- stale:  sha 不一致；或 source / source_version 缺失、非法
          （附原因 ``missing_source_version``）。
- orphan: 英文源文件已从 HEAD 删除（current_source_sha 为 null）。

判定基准是 HEAD 的 blob sha，不含工作区未提交改动（避免半成品误报）。
只读工具：不修改任何文件，不写缓存。

用法::

    python tools/i18n/zh_status.py [--json] [--root <repo>] [--verbose]

退出码::

    0  扫描完成（允许存在 stale/orphan，这是工具的正常产出）
    1  用法/环境错误（git 不可用、--root 非 git 仓库）
    2  docs/zh/ 不存在或无任何译文
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

ZH_DIR = "docs/zh"
SOURCE_DIR = "docs"
# 译文目录 pairs:每项 (译文目录, 英文源目录, 文件 glob, source_version 读取方式)。
# docs/zh 走 frontmatter;cookbook_zh 走 notebook metadata(自建约定,
# 见 docs/zh/README.md「cookbook 翻译」一节)。
DIR_PAIRS = [
    ("docs/zh", "docs", "*.md", "frontmatter"),
    ("cookbook_zh", "cookbook", "*.ipynb", "notebook"),
]
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?", re.DOTALL)


def run_git(root: Path, *args: str) -> Optional[str]:
    """运行一条 git 命令，失败返回 None。

    Args:
        root: 仓库根目录（作为 git -C 的目标）。
        *args: git 子命令与参数。

    Returns:
        成功时的 stdout 文本；git 缺失或命令失败时返回 None。
    """
    try:
        proc = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            text=True,
        )
    except OSError:
        return None
    if proc.returncode != 0:
        return None
    return proc.stdout


def parse_frontmatter(text: str) -> Dict[str, str]:
    """解析 Markdown 顶层 frontmatter 的简单 key: value 行。

    只取平铺标量字段（本工具只需要 source 与 source_version），
    嵌套结构与列表行一律跳过。

    Args:
        text: Markdown 文件全文。

    Returns:
        字段名到字符串值的映射；无 frontmatter 时返回空字典。
    """
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    meta: Dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line or line[0] in " \t#":
            continue
        key, sep, value = line.partition(":")
        if not sep:
            continue
        meta[key.strip()] = value.strip().strip("'\"")
    return meta


def head_blobs(root: Path) -> Dict[str, str]:
    """取回 HEAD 中全部英文源目录的 blob sha。

    对 DIR_PAIRS 里每个英文源目录跑一次 ``git ls-tree -r`` 并合并。

    Args:
        root: 仓库根目录。

    Returns:
        相对仓库根的路径到 blob sha 的映射；HEAD 不可读（如空仓库）
        时返回空映射。
    """
    blobs: Dict[str, str] = {}
    for _zh_dir, source_dir, _glob, _kind in DIR_PAIRS:
        out = run_git(root, "ls-tree", "-r", "HEAD", "--", source_dir + "/")
        if out is None:
            continue
        for line in out.splitlines():
            meta, _, path = line.partition("\t")
            parts = meta.split()
            if len(parts) == 3 and parts[1] == "blob":
                blobs[path] = parts[2]
    return blobs


def diff_stat(root: Path, old_sha: str, new_sha: str) -> str:
    """返回两个 blob 之间 ``git diff --stat`` 的摘要行。

    blob sha 不能作为 tree-ish 参与 ``git diff <sha> -- <path>``，
    因此直接做 blob 对 blob 的比较，语义等价于
    ``git diff <old_sha> -- <path>`` 的摘要。

    Args:
        root: 仓库根目录。
        old_sha: 译文记录的源 blob sha。
        new_sha: HEAD 中源文件当前的 blob sha。

    Returns:
        --stat 的最后一行（"n files changed, ..."）；命令失败时返回提示。
    """
    out = run_git(root, "diff", "--stat", old_sha, new_sha)
    if out is None:
        return "diff unavailable"
    lines = [ln for ln in out.splitlines() if ln.strip()]
    return lines[-1] if lines else "no diff"


def _meta_from_frontmatter(path: Path) -> Dict[str, str]:
    try:
        return parse_frontmatter(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError):
        return {}


def _meta_from_notebook(path: Path) -> Dict[str, str]:
    """从 notebook metadata.zh_translation 读 source/source_version。"""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        zh = (data.get("metadata") or {}).get("zh_translation") or {}
        return {
            "source": str(zh.get("source", "")),
            "source_version": str(zh.get("source_version", "")),
        }
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return {}


def scan(root: Path, verbose: bool) -> List[Dict[str, Any]]:
    """扫描全部译文目录(docs/zh、cookbook_zh)并逐篇判定状态。

    Args:
        root: 仓库根目录。
        verbose: 为 stale/orphan 条目附加 diff stat。

    Returns:
        条目字典列表，按路径排序。每个条目含 path/source/status/
        recorded_source_sha/current_source_sha，必要时附 reason 与 diff_stat。
    """
    blobs = head_blobs(root)
    entries: List[Dict[str, Any]] = []
    for zh_dir, source_dir, pattern, kind in DIR_PAIRS:
        reader = _meta_from_frontmatter if kind == "frontmatter" else _meta_from_notebook
        for zh_path in sorted((root / zh_dir).rglob(pattern)):
            rel = zh_path.relative_to(root).as_posix()
            meta = reader(zh_path)
            source = meta.get("source")
            recorded = meta.get("source_version")
            current = blobs.get(f"{source_dir}/{source}") if source else None
            entry: Dict[str, Any] = {
                "path": rel,
                "source": source,
                "status": "stale",
                "recorded_source_sha": recorded or None,
                "current_source_sha": current,
            }
            if not source or not recorded or not SHA_RE.match(recorded):
                entry["reason"] = "missing_source_version"
            elif current is None:
                entry["status"] = "orphan"
            elif current == recorded:
                entry["status"] = "fresh"
            if verbose and entry["status"] in ("stale", "orphan"):
                if entry["status"] == "orphan":
                    entry["diff_stat"] = "source deleted in HEAD"
                elif current and recorded and SHA_RE.match(recorded):
                    entry["diff_stat"] = diff_stat(root, recorded, current)
                else:
                    entry["diff_stat"] = "unavailable (no valid recorded sha)"
            entries.append(entry)
    return entries


def print_table(entries: List[Dict[str, Any]]) -> None:
    """按人类可读的表格打印扫描结果。"""
    print(f"Semantica 中文译文状态（基准: HEAD，共 {len(entries)} 篇）")
    print(f"{'路径':<44} {'状态':<8} {'记录 sha':<10} {'当前 sha':<10}")
    for e in entries:
        recorded = (e["recorded_source_sha"] or "-")[:8]
        current = (e["current_source_sha"] or "-")[:8]
        note = e.get("reason", "")
        print(
            f"{e['path']:<44} {e['status']:<8} {recorded:<10} {current:<10}"
            + (f"  {note}" if note else "")
        )
        if "diff_stat" in e:
            print(f"    ↳ {e['diff_stat']}")
    summary = summarize(entries)
    print(
        "汇总: fresh={} stale={} orphan={}".format(
            summary["fresh"], summary["stale"], summary["orphan"]
        )
    )


def summarize(entries: List[Dict[str, Any]]) -> Dict[str, int]:
    """统计各状态的条目数。"""
    counts = {"fresh": 0, "stale": 0, "orphan": 0}
    for e in entries:
        counts[e["status"]] = counts.get(e["status"], 0) + 1
    return counts


def main(argv: Optional[List[str]] = None) -> int:
    """CLI 入口。

    Args:
        argv: 命令行参数；缺省取 sys.argv[1:]。

    Returns:
        进程退出码：0 扫描完成，1 环境错误，2 docs/zh 缺失。
    """
    parser = argparse.ArgumentParser(
        description="检查 docs/zh/ 译文相对英文源的新鲜度（fresh/stale/orphan）"
    )
    parser.add_argument("--json", action="store_true", help="输出机器可读 JSON")
    parser.add_argument("--root", default="./", help="仓库根目录（默认 ./）")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="stale/orphan 条目附带 diff stat 摘要",
    )
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()

    # 环境检查：git 可用且 root 是 git 仓库。
    if run_git(root, "rev-parse", "--show-toplevel") is None:
        print(
            f"错误: git 不可用或 {root} 不是 git 仓库",
            file=sys.stderr,
        )
        return 1

    # 环境检查:至少一个译文目录存在且非空。
    existing = [
        (root / zh_dir)
        for zh_dir, _src, pattern, _kind in DIR_PAIRS
        if (root / zh_dir).is_dir() and any((root / zh_dir).rglob(pattern))
    ]
    if not existing:
        print("错误: 找不到任何译文目录(docs/zh、cookbook_zh)", file=sys.stderr)
        return 2

    entries = scan(root, verbose=args.verbose)
    if args.json:
        payload = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "summary": summarize(entries),
            "entries": entries,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print_table(entries)
    return 0


if __name__ == "__main__":
    sys.exit(main())
