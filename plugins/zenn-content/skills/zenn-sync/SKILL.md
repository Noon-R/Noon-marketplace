---
name: zenn-sync
description: |
  外部プロジェクトにZennドキュメント構造をセットアップし、zenn-contentへの同期を支援。
  どのプロジェクトからでも実行可能。
  トリガー：「zenn-sync」「プロジェクトを同期」「Zenn構造を作成」「zenn-init」「zenn同期」
---

# Zenn Project Sync Skill

現在のプロジェクトにZennドキュメント構造をセットアップし、zenn-contentリポジトリへの同期を支援する。

## 設定

zenn-contentリポジトリのパス（環境に応じて変更）:
```
ZENN_CONTENT_DIR: d:/0_Data/Developer/zenn-content
```

## Workflow

### Step 1: 対象プロジェクトの確認

ユーザーに以下を確認:
1. **プロジェクトパス**: 現在の作業ディレクトリをデフォルトとして提案
2. **ドキュメントディレクトリ**: デフォルト `docs/zenn`（カスタム可）
3. **サンプル記事**: 作成するかどうか

### Step 2: プロジェクト側のセットアップ

対象プロジェクトに以下の構造を作成:

```
project/
├── docs/
│   └── zenn/
│       ├── .gitkeep
│       ├── books/
│       │   └── .gitkeep
│       └── images/
│           └── .gitkeep
└── .zenn-sync.yaml
```

#### .zenn-sync.yaml の生成
```yaml
# Zenn 同期設定
docs_dir: docs/zenn

project:
  name: <プロジェクト名>
  slug: <slug化したプロジェクト名>
```

### Step 3: 同期の実行

同期スクリプトを実行:
```bash
bash {ZENN_CONTENT_DIR}/scripts/sync-from-project.sh <プロジェクトパス>
```

または手動で案内:
```bash
cd {ZENN_CONTENT_DIR}
make sync PROJECT=<プロジェクトパス>
```

### Step 4: 記事作成の案内

同期元プロジェクトの `docs/zenn/` に記事を書く方法を案内:
- Front matterの書き方
- slugにプロジェクト名プレフィックスを付ける推奨（例: `myproject-setup`）
- `/zenn-article` スキルを使えば記事作成も支援可能

## Sync Details

sync-from-project.sh の動作:
- `docs/zenn/*.md` → `{ZENN_CONTENT_DIR}/articles/` にコピー
- `docs/zenn/books/*` → `{ZENN_CONTENT_DIR}/books/` にコピー
- `docs/zenn/images/*` → `{ZENN_CONTENT_DIR}/images/` にコピー
- `.zenn-sync.yaml` の `docs_dir` 設定を読み込む

## Notes

- Windows環境でもbashスクリプトは Git Bash 経由で実行可能
- 同期は上書きコピーのため、zenn-content側で直接編集した内容は同期元と乖離する可能性がある
- 同期後は `make preview` でプレビュー確認を推奨
