#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ディレクトリ内の全ドキュメントをスキャンして
ハイパーリンクを集約ファイルへ書き出すスクリプト。

Usage:
    python scan_directory.py [--dir <directory>] [--output <file>] [--reset]

Options:
    --dir     スキャン対象ディレクトリ (default: カレントディレクトリ)
    --output  集約ファイルのパス (default: <dir>/docs/hyperlinks.md)
    --reset   集約ファイルをリセットしてから書き出す
    --ext     対象拡張子 (カンマ区切り, default: .md,.markdown,.txt,.rst)
    --exclude 除外ディレクトリ名 (カンマ区切り, default: .git,node_modules,.venv,__pycache__)
"""

import argparse
import os
import sys
import io
from pathlib import Path

# Windows での UTF-8 対応
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# extract_hyperlinks モジュールへのパスを追加
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from extract_hyperlinks import (
    extract_links_from_file,
    append_links_to_aggregated_file,
    _ensure_aggregated_file,
)

DEFAULT_EXTENSIONS = {".md", ".markdown", ".txt", ".rst"}
DEFAULT_EXCLUDES = {".git", "node_modules", ".venv", "__pycache__", ".claude"}


def collect_files(
    root_dir: Path,
    extensions: set[str],
    exclude_dirs: set[str],
    output_file: Path,
) -> list[Path]:
    """再帰的にファイルを収集する（集約ファイル自体は除外）。"""
    result = []
    output_abs = output_file.resolve()
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # 除外ディレクトリをスキップ
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs]
        for fname in sorted(filenames):
            fpath = Path(dirpath) / fname
            if fpath.resolve() == output_abs:
                continue
            if fpath.suffix.lower() in extensions:
                result.append(fpath)
    return result


def reset_aggregated_file(output_file: Path):
    """集約ファイルをヘッダーのみにリセットする。"""
    header = (
        "# Hyperlinks Index\n\n"
        "このファイルはプロジェクト内のドキュメントから自動収集されたハイパーリンクの集約ファイルです。\n"
        "`aggregate-hyperlinks` プラグインにより生成・更新されます。\n\n"
        "---\n\n"
    )
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(header)


def main():
    parser = argparse.ArgumentParser(description="ディレクトリ内のドキュメントからハイパーリンクを集約する")
    parser.add_argument(
        "--dir", default=".",
        help="スキャン対象ディレクトリ (default: カレントディレクトリ)"
    )
    parser.add_argument(
        "--output", default=None,
        help="集約ファイルのパス (default: <dir>/docs/hyperlinks.md)"
    )
    parser.add_argument(
        "--reset", action="store_true",
        help="集約ファイルをリセットしてから書き出す"
    )
    parser.add_argument(
        "--ext", default=".md,.markdown,.txt,.rst",
        help="対象拡張子 (カンマ区切り)"
    )
    parser.add_argument(
        "--exclude", default=".git,node_modules,.venv,__pycache__,.claude",
        help="除外ディレクトリ名 (カンマ区切り)"
    )

    args = parser.parse_args()

    root_dir = Path(args.dir).resolve()
    if not root_dir.is_dir():
        print(f"❌ ディレクトリが見つかりません: {root_dir}", file=sys.stderr)
        sys.exit(1)

    output_file = (
        Path(args.output).resolve()
        if args.output
        else root_dir / "docs" / "hyperlinks.md"
    )

    extensions = {e.strip() for e in args.ext.split(",") if e.strip()}
    exclude_dirs = {d.strip() for d in args.exclude.split(",") if d.strip()}

    # リセット
    if args.reset:
        reset_aggregated_file(output_file)
        print(f"🔄 集約ファイルをリセットしました: {output_file}")

    # ファイル収集
    files = collect_files(root_dir, extensions, exclude_dirs, output_file)
    print(f"📂 スキャン対象: {len(files)} ファイル（ルート: {root_dir}）")

    total_files_with_links = 0
    total_links_added = 0

    for fpath in files:
        links = extract_links_from_file(str(fpath))
        if not links:
            continue
        added = append_links_to_aggregated_file(
            links=links,
            source_file=str(fpath),
            aggregated_file=str(output_file),
        )
        if added > 0:
            rel = fpath.relative_to(root_dir)
            print(f"  ✅ {rel}: {added} 件追加")
            total_files_with_links += 1
            total_links_added += added
        else:
            rel = fpath.relative_to(root_dir)
            print(f"  ⏭️  {rel}: 新規リンクなし（スキップ）")

    print(f"\n📋 完了: {total_files_with_links} ファイルから {total_links_added} 件のリンクを追加")
    print(f"   集約ファイル: {output_file}")


if __name__ == "__main__":
    main()
