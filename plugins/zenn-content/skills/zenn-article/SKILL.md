---
name: zenn-article
description: |
  Zenn記事の作成を対話的に支援。どのプロジェクトからでもzenn-contentリポジトリに記事を追加・更新可能。
  トリガー：「zenn-article」「記事を書きたい」「新しい記事」「Zenn記事を作成」「zenn記事」
---

# Zenn Article Creation Skill

どのプロジェクトからでもZenn記事を作成・更新できるスキル。

## 設定

zenn-contentリポジトリのパス（環境に応じて変更）:
```
ZENN_CONTENT_DIR: d:/0_Data/Developer/zenn-content
```

## Workflow

### Step 1: ヒアリング

ユーザーに以下を質問する（未指定の場合のみ）:

1. **テーマ**: 何について書くか
2. **タイプ**: `tech`（技術記事）or `idea`（アイデア記事）- デフォルト: tech
3. **slug**: URL用の識別子（小文字英数字+ハイフン）- 提案してもよい
4. **topics**: 関連タグ（5つまで、小文字）
5. **emoji**: アイキャッチ絵文字

### Step 2: 記事ファイル生成

zenn-contentリポジトリの `articles/<slug>.md` に記事を作成する。

**パス**: `{ZENN_CONTENT_DIR}/articles/<slug>.md`

テンプレートは [references/](references/) を参照:
- tech記事: `references/article-tech.md`
- idea記事: `references/article-idea.md`

Front matter を正しく埋める:
```yaml
---
title: "<ユーザー指定のタイトル>"
emoji: "<選択した絵文字>"
type: "<tech or idea>"
topics: ["topic1", "topic2"]
published: false
---
```

### Step 3: 本文の構成提案

テーマに基づいて記事の構成（見出し構成）を提案し、ユーザーの同意を得てから本文のドラフトを作成する。

現在のプロジェクトに関連する記事の場合、プロジェクトのコードや構成を参照して内容を充実させる。

### Step 4: 既存記事の更新（該当する場合）

ユーザーが既存記事の更新を希望する場合:
1. `{ZENN_CONTENT_DIR}/articles/` から対象記事を検索
2. 内容を読み込んで編集
3. 変更箇所をユーザーに確認

### Step 5: 完了案内

以下を伝える:
- 作成/更新されたファイルパス
- zenn-contentディレクトリで `make preview` を実行するとプレビュー確認できること
- `published: true` に変更して `make publish` で公開できること
- 現在のプロジェクトから記事を書いた場合、`/zenn-sync` で同期セットアップも検討を提案

## Constraints

- slugは `^[a-z0-9][a-z0-9-]*[a-z0-9]$` に準拠（1文字の場合は `^[a-z0-9]$`）
- topicsは最大5つ
- titleは60文字以内推奨
- 必ず `published: false` で作成（下書き状態）
- Zenn記法を活用する:
  - `:::message` / `:::message alert` - メッセージボックス
  - `:::details タイトル` - 折りたたみ
  - 数式: `$$` ブロック
  - diff付きコードブロック

## 記事一覧の確認

既存記事を確認するには:
```bash
ls {ZENN_CONTENT_DIR}/articles/
```
