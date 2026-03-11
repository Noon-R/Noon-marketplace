# aggregate-hyperlinks フック設定ガイド

このプラグインは Claude Code の **PostToolUse フック** を使用して、
ドキュメント作成・編集時にハイパーリンクを自動集約します。

---

## セットアップ手順

### 1. フックスクリプトの絶対パスを確認

```bash
# このプラグインのインストール先を確認
ls /path/to/your/plugin/aggregate-hyperlinks/hooks/post_tool_use.py
```

### 2. `.claude/settings.json` にフックを登録

プロジェクトの `.claude/settings.json`（または `.claude/settings.local.json`）に
以下を追加してください。

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python /絶対パス/plugins/aggregate-hyperlinks/hooks/post_tool_use.py"
          }
        ]
      }
    ]
  }
}
```

**Windows の場合:**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python D:\\path\\to\\plugins\\aggregate-hyperlinks\\hooks\\post_tool_use.py"
          }
        ]
      }
    ]
  }
}
```

---

## 動作確認

フック登録後、任意の Markdown ファイルを作成または編集してみてください。

```bash
# テスト用ドキュメントを作成
# Claude Code で Write ツールを使ってリンク入りのファイルを作成すると...
# → 自動的に docs/hyperlinks.md が更新されます
```

---

## フックの動作フロー

```
ユーザーがドキュメントを作成/編集
        ↓
Claude Code が Write または Edit ツールを実行
        ↓
PostToolUse フックが post_tool_use.py を呼び出し
        ↓
stdin に JSON 形式でツール情報を渡す:
{
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/document.md",
    "content": "..."
  }
}
        ↓
post_tool_use.py がファイルの拡張子を確認
（.md, .markdown, .txt, .rst, .html, .htm のみ対象）
        ↓
extract_hyperlinks.py でリンクを抽出
        ↓
新規 URL のみを docs/hyperlinks.md に追記
        ↓
完了（stderr にログを出力）
```

---

## 集約ファイルの場所

集約ファイルは書き込まれたファイルから `.git` ディレクトリを探して
プロジェクトルートを自動検出し、そこの `docs/hyperlinks.md` に保存されます。

```
プロジェクトルート/
├── .git/
├── docs/
│   └── hyperlinks.md   ← ここに集約される
├── src/
│   └── document.md     ← リンクがあれば抽出される
└── ...
```

---

## 既存ドキュメントの一括スキャン

フック設定前に作成済みのドキュメントは手動スキャンで集約できます:

```bash
python plugins/aggregate-hyperlinks/skills/aggregate-hyperlinks/scripts/scan_directory.py \
  --dir "/path/to/project" \
  --output "/path/to/project/docs/hyperlinks.md"
```

または Claude Code で「ハイパーリンクを集約して」と指示することで
`aggregate-hyperlinks` スキルが実行されます。

---

## トラブルシューティング

| 症状 | 原因 | 対処 |
|------|------|------|
| `docs/hyperlinks.md` が更新されない | フックが未登録 | `.claude/settings.json` を確認 |
| スクリプトエラーが出る | Python のパスが違う | `python3` や絶対パスで試す |
| リンクが重複して登録される | 集約ファイルが壊れている | `--reset` オプションで再スキャン |
| 特定のファイルが対象外 | 拡張子が対応外 | `post_tool_use.py` の `TARGET_EXTENSIONS` を確認 |
