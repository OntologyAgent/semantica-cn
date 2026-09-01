#!/usr/bin/env python3
"""ui_zh_status — 检查 explorer 界面中文资源相对英文基准的新鲜度。

对比 zh.json 顶层 ``__meta.source_version``（翻译时英文基准的 git blob
sha）与 HEAD 中 en.json 当前的 blob sha，判定 fresh / stale / orphan：

- fresh:  记录的 sha 与 HEAD 一致，基准未变。
- stale:  sha 不一致；或 source_version 缺失、非法
          （附原因 ``missing_source_version``）。
- orphan: 英文基准 en.json 已不在 HEAD（current_source_sha 为 null）。

无论 sha 是否一致都做键级比对：展平两文件 ``translation`` 命名空间下
的点号叶子键（``__meta`` 不计入键集合），en 有 zh 无记 missing_keys，
zh 有 en 无记 extra_keys——防止 sha 忘刷但键已漂移的静默漏报。

判定基准是 HEAD 的 blob sha，不含工作区未提交改动（避免半成品误报）。
只读工具：不修改任何文件，不写缓存。

用法::

    python tools/i18n/ui_zh_status.py [--json] [--root <repo>] [--verbose]

退出码::

    0  扫描完成（允许存在 stale/orphan，这是工具的正常产出）
    1  用法/环境错误（git 不可用、--root 非 git 仓库、JSON 解析失败）
    2  explorer/src/i18n/locales/ 不存在或缺 en.json/zh.json 任一
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

LOCALES_DIR = "explorer/src/i18n/locales"
SOURCE_NAME = "en.json"
TARGET_NAME = "zh.json"
SOURCE_PATH = f"{LOCALES_DIR}/{SOURCE_NAME}"
TARGET_PATH = f"{LOCALES_DIR}/{TARGET_NAME}"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


class LocaleDataError(Exception):
    """资源文件不可读或 JSON 结构非法。"""


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


def head_blobs(root: Path) -> Dict[str, str]:
    """单次 ls-tree 取回 HEAD 中 locales/ 下全部文件的 blob sha。

    Args:
        root: 仓库根目录。

    Returns:
        相对仓库根的路径到 blob sha 的映射；HEAD 不可读（如空仓库）
        时返回空映射。
    """
    out = run_git(root, "ls-tree", "-r", "HEAD", "--", LOCALES_DIR + "/")
    blobs: Dict[str, str] = {}
    if out is None:
        return blobs
    for line in out.splitlines():
        meta, _, path = line.partition("\t")
        parts = meta.split()
        if len(parts) == 3 and parts[1] == "blob":
            blobs[path] = parts[2]
    return blobs


def flatten(obj: Dict[str, Any], prefix: str = "") -> List[str]:
    """递归展平嵌套字典为点号叶子键列表。

    Args:
        obj: 待展平的字典（通常为 translation 命名空间）。
        prefix: 递归时已累积的父级键前缀。

    Returns:
        叶子键列表；字典值继续下钻，非字典值（str/list 等）视为叶子。
    """
    keys: List[str] = []
    for key, value in obj.items():
        flat = f"{prefix}{key}"
        if isinstance(value, dict):
            keys.extend(flatten(value, prefix=flat + "."))
        else:
            keys.append(flat)
    return keys


def load_locale(path: Path) -> Dict[str, Any]:
    """读取并解析一个 locale JSON，顶层必须是对象。

    Args:
        path: locale JSON 文件路径。

    Returns:
        解析后的顶层字典。

    Raises:
        LocaleDataError: 文件不可读、JSON 非法或顶层不是对象。
    """
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise LocaleDataError(f"{path}: {exc}") from exc
    if not isinstance(data, dict):
        raise LocaleDataError(f"{path}: 顶层必须是 JSON 对象")
    return data


def translation_keys(data: Dict[str, Any]) -> List[str]:
    """提取 translation 命名空间并展平为排序后的点号键。

    ``__meta`` 与 translation 同级，本就不在其内；若被误放进
    translation 内也在此剔除（防御）。

    Args:
        data: load_locale 返回的顶层字典。

    Returns:
        排序后的点号叶子键列表。

    Raises:
        LocaleDataError: translation 命名空间缺失或不是对象。
    """
    ns = data.get("translation")
    if not isinstance(ns, dict):
        raise LocaleDataError("translation 命名空间缺失或不是对象")
    return sorted(flatten({k: v for k, v in ns.items() if k != "__meta"}))


def recorded_source_version(data: Dict[str, Any]) -> Optional[str]:
    """读取顶层 ``__meta.source_version``，非法按 None 处理。

    Args:
        data: zh.json 解析后的顶层字典。

    Returns:
        40 位十六进制 blob sha；缺失或非法时返回 None。
    """
    meta = data.get("__meta")
    if not isinstance(meta, dict):
        return None
    version = meta.get("source_version")
    if not isinstance(version, str) or not SHA_RE.match(version):
        return None
    return version


def scan(root: Path, verbose: bool) -> List[Dict[str, Any]]:
    """对比 zh.json 与 HEAD 中 en.json，产出判定记录。

    Args:
        root: 仓库根目录。
        verbose: 为 stale/orphan 条目附加键级 diff 明细。

    Returns:
        条目字典列表（当前只有 zh.json ↔ en.json 一对）。

    Raises:
        LocaleDataError: 任一资源文件不可读或结构非法。
    """
    blobs = head_blobs(root)
    en_data = load_locale(root / SOURCE_PATH)
    zh_data = load_locale(root / TARGET_PATH)
    en_keys = set(translation_keys(en_data))
    zh_keys = set(translation_keys(zh_data))
    missing = sorted(en_keys - zh_keys)
    extra = sorted(zh_keys - en_keys)

    recorded = recorded_source_version(zh_data)
    current = blobs.get(SOURCE_PATH)
    entry: Dict[str, Any] = {
        "path": TARGET_PATH,
        "source": SOURCE_PATH,
        "status": "stale",
        "recorded_source_sha": recorded,
        "current_source_sha": current,
        "missing_keys": missing,
        "extra_keys": extra,
    }
    if recorded is None:
        entry["reason"] = "missing_source_version"
    elif current is None:
        entry["status"] = "orphan"
    elif current == recorded:
        entry["status"] = "fresh"
    if verbose and entry["status"] in ("stale", "orphan"):
        if entry["status"] == "orphan":
            entry["key_diff"] = "source deleted in HEAD"
        elif missing or extra:
            entry["key_diff"] = " | ".join(
                [
                    f"missing({len(missing)}): {', '.join(missing)}",
                    f"extra({len(extra)}): {', '.join(extra)}",
                ]
            )
        else:
            entry["key_diff"] = "键集无差异（仅 sha 漂移）"
    return [entry]


def summarize(entries: List[Dict[str, Any]]) -> Dict[str, int]:
    """统计各状态条目数与键级 diff 总数。"""
    counts: Dict[str, int] = {
        "fresh": 0,
        "stale": 0,
        "orphan": 0,
        "missing_keys": 0,
        "extra_keys": 0,
    }
    for e in entries:
        counts[e["status"]] = counts.get(e["status"], 0) + 1
        counts["missing_keys"] += len(e["missing_keys"])
        counts["extra_keys"] += len(e["extra_keys"])
    return counts


def print_table(entries: List[Dict[str, Any]]) -> None:
    """按人类可读的表格打印扫描结果。"""
    print(
        f"Semantica 界面译文状态"
        f"（基准: HEAD，{TARGET_NAME} ↔ {SOURCE_NAME}，共 {len(entries)} 对）"
    )
    print(
        f"{'路径':<44} {'状态':<8} {'记录 sha':<10} {'当前 sha':<10}"
        f" {'missing':<8} {'extra':<8}"
    )
    for e in entries:
        recorded = (e["recorded_source_sha"] or "-")[:8]
        current = (e["current_source_sha"] or "-")[:8]
        note = e.get("reason", "")
        row = (
            f"{e['path']:<44} {e['status']:<8} {recorded:<10} {current:<10}"
            f" {len(e['missing_keys']):<8} {len(e['extra_keys']):<8}"
        )
        print(row + (f"  {note}" if note else ""))
        if "key_diff" in e:
            print(f"    ↳ {e['key_diff']}")
    summary = summarize(entries)
    print(
        "汇总: fresh={} stale={} orphan={} missing_keys={} extra_keys={}".format(
            summary["fresh"],
            summary["stale"],
            summary["orphan"],
            summary["missing_keys"],
            summary["extra_keys"],
        )
    )


def main(argv: Optional[List[str]] = None) -> int:
    """CLI 入口。

    Args:
        argv: 命令行参数；缺省取 sys.argv[1:]。

    Returns:
        进程退出码：0 扫描完成，1 用法/环境错误，2 资源目录或文件缺失。
    """
    parser = argparse.ArgumentParser(
        description="检查 explorer 界面中文资源相对英文基准的新鲜度"
        "（fresh/stale/orphan）"
    )
    parser.add_argument("--json", action="store_true", help="输出机器可读 JSON")
    parser.add_argument("--root", default="./", help="仓库根目录（默认 ./）")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="stale/orphan 条目附带键级 diff 明细",
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

    locales_dir = root / LOCALES_DIR
    if not locales_dir.is_dir():
        print(f"错误: {locales_dir} 不存在", file=sys.stderr)
        return 2
    absent = [n for n in (SOURCE_NAME, TARGET_NAME) if not (locales_dir / n).is_file()]
    if absent:
        print(
            f"错误: {locales_dir} 缺少资源文件: {', '.join(absent)}",
            file=sys.stderr,
        )
        return 2

    try:
        entries = scan(root, verbose=args.verbose)
    except LocaleDataError as exc:
        print(f"错误: {exc}", file=sys.stderr)
        return 1

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
