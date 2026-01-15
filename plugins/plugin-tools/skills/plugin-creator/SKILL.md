---
name: plugin-creator
description: |
  新規プラグインのディレクトリ構造とファイルを自動生成します。
  plugin.json作成、skillsディレクトリ初期化、marketplace.json登録を支援。
  トリガー：「プラグインを作成」「新しいプラグイン」「plugin create」「create plugin」
---

# Plugin Creator

Claude Code用の新規プラグインを作成するワークフローを提供します。

## ワークフロー

### 1. プラグイン初期化

```bash
# 新規プラグインを作成
python scripts/init_plugin.py <plugin-name> --path ./plugins

# 説明を指定して作成
python scripts/init_plugin.py <plugin-name> --path ./plugins --description "プラグインの説明"
```

出力:
```
plugins/<plugin-name>/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── (empty - ready for skills)
```

### 2. marketplace.jsonへの登録

```bash
# プラグインをマーケットプレイスに登録
python scripts/register_plugin.py <plugin-name> --marketplace ./.claude-plugin/marketplace.json
```

### 3. 初期スキルの追加（オプション）

プラグイン作成後、skill-creator または skill-updater を使用してスキルを追加します。

```bash
# skill-creatorのinit_skill.pyを使用
python path/to/init_skill.py <skill-name> --path plugins/<plugin-name>/skills
```

## プラグイン構造

詳細は [references/plugin-structure.md](references/plugin-structure.md) を参照。

```
plugins/<plugin-name>/
├── .claude-plugin/
│   └── plugin.json        # プラグインメタデータ
└── skills/
    └── <skill-name>/
        ├── SKILL.md       # スキル定義
        ├── scripts/       # 実行スクリプト
        ├── references/    # リファレンスドキュメント
        └── assets/        # リソースファイル
```

## plugin.json形式

```json
{
  "name": "plugin-name",
  "description": "プラグインの説明",
  "version": "1.0.0",
  "skills": "./skills/"
}
```

**注意**: `author`フィールドを追加する場合はオブジェクト形式を使用：
```json
{
  "author": {
    "name": "Author Name",
    "email": "email@example.com"
  }
}
```

## marketplace.json形式

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
      "description": "プラグインの説明",
      "version": "1.0.0"
    }
  ]
}
```

## 命名規約

- **プラグイン名**: ハイフン区切り、小文字（例: `my-plugin`）
- **スキル名**: ハイフン区切り、小文字（例: `data-processor`）
- **バージョン**: セマンティックバージョニング（例: `1.0.0`）
