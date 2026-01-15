# Plugin Structure Reference

Claude Codeプラグインの構造とファイル形式の詳細リファレンス。

## ディレクトリ構造

```
Noon-marketplace/
├── .claude-plugin/
│   └── marketplace.json       # マーケットプレイス定義
└── plugins/
    └── <plugin-name>/
        ├── .claude-plugin/
        │   └── plugin.json    # プラグインメタデータ
        └── skills/
            └── <skill-name>/
                ├── SKILL.md       # スキル定義（必須）
                ├── scripts/       # 実行スクリプト
                ├── references/    # リファレンスドキュメント
                └── assets/        # リソースファイル
```

## marketplace.json

マーケットプレイス全体の定義ファイル。

```json
{
  "name": "marketplace-name",
  "owner": {
    "name": "Owner Name",
    "email": "email@example.com"
  },
  "plugins": [
    {
      "name": "plugin-name",
      "source": "./plugins/plugin-name",
      "description": "プラグインの説明文",
      "version": "1.0.0"
    }
  ]
}
```

### フィールド

| フィールド | 必須 | 説明 |
|-----------|------|------|
| name | Yes | マーケットプレイス名 |
| owner | Yes | オーナー情報（オブジェクト形式） |
| owner.name | Yes | オーナー名 |
| owner.email | No | 連絡先メール |
| plugins | Yes | プラグイン配列 |

### plugins配列

| フィールド | 必須 | 説明 |
|-----------|------|------|
| name | Yes | プラグイン名 |
| source | Yes | プラグインへの相対パス |
| description | Yes | プラグインの説明 |
| version | Yes | セマンティックバージョン |

## plugin.json

個別プラグインのメタデータファイル。

```json
{
  "name": "plugin-name",
  "description": "プラグインの説明",
  "version": "1.0.0",
  "skills": "./skills/"
}
```

### フィールド

| フィールド | 必須 | 説明 |
|-----------|------|------|
| name | Yes | プラグイン名（ディレクトリ名と一致） |
| description | Yes | プラグインの説明 |
| version | Yes | セマンティックバージョン |
| skills | Yes | skillsディレクトリへの相対パス |

### author（オプション）

authorフィールドを追加する場合は**オブジェクト形式**を使用：

```json
{
  "name": "plugin-name",
  "description": "...",
  "version": "1.0.0",
  "author": {
    "name": "Author Name",
    "email": "email@example.com"
  },
  "skills": "./skills/"
}
```

**注意**: 文字列形式（`"author": "Name"`）は無効です。

## SKILL.md

スキル定義ファイル。YAML frontmatterとMarkdownボディで構成。

```markdown
---
name: skill-name
description: |
  スキルの説明。複数行可。
  トリガーキーワードを含める。
---

# Skill Title

## Overview
...

## Workflow
...
```

### Frontmatter（必須）

| フィールド | 必須 | 説明 |
|-----------|------|------|
| name | Yes | スキル名（ディレクトリ名と一致） |
| description | Yes | スキルの説明とトリガーキーワード |

### 推奨セクション

1. **Overview** - スキルの概要
2. **Workflow** - 使用手順
3. **Resources** - バンドルリソースの説明

## 命名規約

### プラグイン名

- 小文字のみ
- ハイフン区切り
- 文字で開始
- 40文字以下
- 例: `my-plugin`, `data-processor`, `learning-log`

### スキル名

- 小文字のみ
- ハイフン区切り
- 文字で開始
- 例: `skill-creator`, `coding-standards`

### バージョン

セマンティックバージョニングを使用:
- MAJOR.MINOR.PATCH
- 例: `1.0.0`, `2.1.3`

## ベストプラクティス

1. **SKILL.mdは500行以下**を目標
2. **詳細情報はreferences/へ分離**
3. **スクリプトはUTF-8エンコーディング**を使用
4. **Windowsと互換性のあるパス**を使用
5. **descriptionにトリガーキーワード**を含める
