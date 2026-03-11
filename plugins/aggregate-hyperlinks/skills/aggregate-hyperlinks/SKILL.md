---
name: aggregate-hyperlinks
description: ドキュメント内のハイパーリンクを集約ファイルに集めるスキル。ユーザーが「リンクをまとめて」「ハイパーリンクを集約して」「hyperlinks をスキャンして」「リンク一覧を作って」などと言ったとき、または既存ドキュメントのリンクを一括収集したいときに使用する。PostToolUse フックと連携して自動集約も行う。
---

# Aggregate Hyperlinks

## Overview

プロジェクト内のドキュメント（Markdown、テキストなど）に含まれるハイパーリンクを
自動的に抽出し、`docs/hyperlinks.md` へ集約するスキル。

**2つの動作モード:**

| モード | 説明 |
|--------|------|
| **自動モード（フック）** | `Write`/`Edit` ツール使用後に自動実行。新しく書かれたリンクを即時集約 |
| **手動モード（スキル）** | ユーザーの指示で既存ドキュメントを一括スキャン |

---

## Quick Start（手動モード）

ユーザーから「リンクをまとめて」「ハイパーリンクを集約して」などと言われたら：

**Step 1 - ディレクトリ全体をスキャン:**
```bash
python scripts/scan_directory.py --dir "<project-root>" --output "<project-root>/docs/hyperlinks.md"
```

**Step 2 - 結果を報告:**
実行後、追加されたリンク件数と `docs/hyperlinks.md` の場所をユーザーに伝える。

---

## Workflow（手動モード）

1. **ユーザーの意図を確認**: リセットして再スキャンするか、追記スキャンするかを確認
2. **スクリプトを実行**: `scan_directory.py` でプロジェクト全体をスキャン
3. **結果を報告**: 何件のリンクを何ファイルから収集したかを簡潔に伝える

---

## Script Usage

### scan_directory.py

既存ドキュメントを一括スキャンして集約ファイルへ書き出す。

**基本的な使用方法:**
```bash
# カレントディレクトリをスキャン（出力: ./docs/hyperlinks.md）
python scripts/scan_directory.py

# ディレクトリを指定
python scripts/scan_directory.py --dir "/path/to/project"

# 出力先を指定
python scripts/scan_directory.py --dir "/path/to/project" --output "/path/to/hyperlinks.md"

# リセットしてから再スキャン（全リンクを書き直し）
python scripts/scan_directory.py --dir "/path/to/project" --reset

# 対象拡張子を追加
python scripts/scan_directory.py --ext ".md,.txt,.rst,.html"
```

**オプション一覧:**

| オプション | デフォルト | 説明 |
|-----------|-----------|------|
| `--dir`   | `.` | スキャン対象ディレクトリ |
| `--output` | `<dir>/docs/hyperlinks.md` | 集約ファイルのパス |
| `--reset` | false | 集約ファイルをリセットしてから書き出す |
| `--ext`   | `.md,.markdown,.txt,.rst` | 対象拡張子（カンマ区切り） |
| `--exclude` | `.git,node_modules,.venv,__pycache__,.claude` | 除外ディレクトリ |

---

### extract_hyperlinks.py（コアライブラリ）

対応するリンクフォーマット:

| フォーマット | 例 |
|-------------|-----|
| Markdown インライン | `[Claude Code](https://claude.ai/code)` |
| Markdown 参照スタイル | `[id]: https://example.com` |
| 裸の URL | `https://example.com` |
| HTML アンカー | `<a href="https://example.com">` |

---

## Hook Mode（自動モード）

`PostToolUse` フックにより、`Write` または `Edit` ツールが使用されるたびに
`hooks/post_tool_use.py` が自動実行されます。

**フックの動作:**
1. 書き込まれたファイルの拡張子を確認（`.md`, `.markdown`, `.txt`, `.rst`, `.html`, `.htm`）
2. ファイルからハイパーリンクを抽出
3. 新規 URL のみを `docs/hyperlinks.md` へ追記（重複スキップ）

**フック設定については `HOOKS_SETUP.md` を参照してください。**

---

## Output Format（集約ファイルの形式）

`docs/hyperlinks.md` の形式:

```markdown
# Hyperlinks Index

このファイルはプロジェクト内のドキュメントから自動収集されたハイパーリンクの集約ファイルです。

---

## docs/design.md  _2026-03-11 14:30_

- [Claude Code 公式サイト](https://claude.ai/code)
- [Anthropic API ドキュメント](https://docs.anthropic.com)
- <https://github.com/anthropics/anthropic-sdk-python>

## docs/references.md  _2026-03-11 15:00_

- [MDN Web Docs](https://developer.mozilla.org)
```

---

## Implementation Notes

- **重複排除**: 同じ URL は集約ファイルに一度だけ記録される
- **差分追記**: フックは新規 URL のみを追加し、既存エントリを変更しない
- **文字コード**: UTF-8 で処理（Windows でも動作）
- **エラー耐性**: フックはエラーで Claude Code のフローを中断しない（静かに終了）
- **プロジェクトルート検出**: `.git` ディレクトリを探してプロジェクトルートを自動検出
