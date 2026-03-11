#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PostToolUse Hook: aggregate-hyperlinks
========================================
Claude Code の PostToolUse フックとして実行されるスクリプト。
Write / Edit ツールが使用された後に自動的に呼ばれ、
作成・編集されたファイルからハイパーリンクを抽出して
集約ファイル (hyperlinks.md) に追記します。

フック入力（stdin）は Claude Code から JSON 形式で渡されます:
{
  "tool_name": "Write" | "Edit" | ...,
  "tool_input": {
    "file_path": "/path/to/file",
    ...
  }
}

使用方法（.claude/settings.json への登録）:
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python /absolute/path/to/post_tool_use.py"
          }
        ]
      }
    ]
  }
}
"""

import json
import os
import sys
import io
from pathlib import Path

# Windows での UTF-8 対応
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# このスクリプトの場所からプラグインのルートを求め、extract_hyperlinks をインポート
SCRIPT_DIR = Path(__file__).parent
PLUGIN_ROOT = SCRIPT_DIR.parent
SCRIPTS_DIR = PLUGIN_ROOT / "skills" / "aggregate-hyperlinks" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from extract_hyperlinks import extract_links_from_file, append_links_to_aggregated_file


# 対象とするファイル拡張子
TARGET_EXTENSIONS = {".md", ".markdown", ".txt", ".rst", ".html", ".htm"}

# 除外するファイルパターン（集約ファイル自体や一時ファイルなど）
EXCLUDE_PATTERNS = {"hyperlinks.md", "hyperlinks_index.md"}


def should_process_file(file_path: str) -> bool:
    """ファイルを処理対象とするか判定する。"""
    path = Path(file_path)
    if path.suffix.lower() not in TARGET_EXTENSIONS:
        return False
    if path.name in EXCLUDE_PATTERNS:
        return False
    return True


def find_aggregated_file(written_file_path: str) -> Path:
    """
    書き込まれたファイルのプロジェクトルートを推定し、
    集約ファイルのパスを返す。
    プロジェクトルートは git リポジトリのルートを探して決定する。
    """
    written_path = Path(written_file_path).resolve()

    # git のルートディレクトリを探す
    current = written_path.parent
    for _ in range(10):  # 最大 10 階層上まで探索
        if (current / ".git").exists():
            docs_dir = current / "docs"
            docs_dir.mkdir(parents=True, exist_ok=True)
            return docs_dir / "hyperlinks.md"
        parent = current.parent
        if parent == current:
            break
        current = parent

    # git ルートが見つからなければ書き込みファイルと同階層の docs/ に置く
    docs_dir = written_path.parent / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    return docs_dir / "hyperlinks.md"


def main():
    # stdin から Claude Code の JSON 入力を読み取る
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            sys.exit(0)
        data = json.loads(raw)
    except (json.JSONDecodeError, Exception) as e:
        # パース失敗はフックを静かに終了（Claude Code のフローを止めない）
        sys.exit(0)

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    # Write / Edit のみを対象とする
    if tool_name not in ("Write", "Edit"):
        sys.exit(0)

    file_path = tool_input.get("file_path", "")
    if not file_path:
        sys.exit(0)

    if not should_process_file(file_path):
        sys.exit(0)

    # ファイルが実際に存在するか確認
    if not Path(file_path).exists():
        sys.exit(0)

    # ハイパーリンクを抽出
    links = extract_links_from_file(file_path)
    if not links:
        sys.exit(0)

    # 集約ファイルへ追記
    aggregated_file = find_aggregated_file(file_path)
    added_count = append_links_to_aggregated_file(
        links=links,
        source_file=file_path,
        aggregated_file=str(aggregated_file)
    )

    if added_count > 0:
        print(f"🔗 {added_count} 件のリンクを {aggregated_file} に追加しました（ソース: {file_path}）",
              file=sys.stderr)


if __name__ == "__main__":
    main()
