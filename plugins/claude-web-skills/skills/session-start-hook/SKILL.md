---
name: session-start-hook
description: |
  Claude Code on Web 向けのリポジトリセットアップを行い、SessionStart フックを作成します。
  Webセッション開始時にテスト・リンターが自動実行されるよう .claude/settings.json を設定します。
  トリガー：「session-start-hook」「セッション開始フック」「SessionStart」「hook setup」「フックを設定」「web セットアップ」
---

# Session Start Hook

Claude Code on Web のリポジトリに `SessionStart` フックを設定・開発するスキルです。

## 概要

Claude Code on Web でセッションを開始したとき、自動的にテストやリンターを実行させたい場合に使用します。
`.claude/settings.json` に `SessionStart` フックを追加し、プロジェクトの品質チェックを自動化します。

## ワークフロー

### 1. 事前確認

- プロジェクトのテストコマンドを確認する（`npm test`, `pytest`, `go test` など）
- リンターコマンドを確認する（`eslint`, `flake8`, `golint` など）
- `.claude/` ディレクトリの存在を確認する

### 2. SessionStart フックの作成

`.claude/settings.json` に以下を追加・更新する：

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "<テストコマンド>"
          }
        ]
      }
    ]
  }
}
```

### 3. フックのカスタマイズ

プロジェクトの種類に応じて適切なコマンドを設定：

**Node.js / TypeScript**
```json
{ "command": "npm test -- --passWithNoTests" }
```

**Python**
```json
{ "command": "python -m pytest --tb=short -q 2>/dev/null || true" }
```

**複数コマンドの組み合わせ**
```json
{ "command": "npm run lint && npm test -- --passWithNoTests" }
```

### 4. 完了確認

- `.claude/settings.json` が正しい JSON 形式であることを確認する
- セッションを再起動してフックが実行されることを確認する

## 使用例

```
# リポジトリのセットアップを依頼する
session-start-hook を設定して

# 具体的なコマンドを指定する場合
pytest を実行する SessionStart フックを作成して
```

## 評価サマリー

| 項目 | 評価 |
|------|------|
| 目的の明確さ | ◎ 明確（Web セッション初期化） |
| トリガーの充実度 | ◎ 豊富なキーワード |
| 適用範囲 | ○ Claude Code on Web 限定（適切な制約） |
| 自動化レベル | ○ 設定ファイルの生成まで対応 |
| リスク | ○ 低リスク（設定ファイルの作成のみ） |

## 注意事項

- `SessionStart` フックはセッション開始ごとに毎回実行されます
- 重い処理（長時間テストなど）はセッション開始を遅延させる可能性があります
- フックコマンドが失敗してもセッションは継続されます（エラーは表示されます）

## 関連スキル

- `simplify`: セッション開始後のコードレビューと組み合わせて品質管理を強化
