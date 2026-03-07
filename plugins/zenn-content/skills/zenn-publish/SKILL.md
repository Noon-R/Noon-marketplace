---
name: zenn-publish
description: |
  Zenn記事の公開・デプロイを支援。git add/commit/pushでZennに反映。
  トリガー：「zenn-publish」「記事を公開」「Zennにデプロイ」「zenn push」「記事をpush」「zennを更新」
---

# Zenn Publish Skill

zenn-contentリポジトリの変更をgit push してZennに反映するスキル。

## 設定

```
ZENN_CONTENT_DIR: d:/0_Data/Developer/zenn-content
```

## Workflow

### Step 1: 変更内容の確認

zenn-contentリポジトリの状態を確認する:

```bash
cd {ZENN_CONTENT_DIR} && git status
```

変更があるファイルをユーザーに一覧表示し、内容を確認する。
変更がない場合はその旨を伝えて終了。

### Step 2: 公開設定の確認

変更された記事ファイルの `published` フラグを確認:
- `published: false` の記事 → 公開するか確認（trueに変更するか聞く）
- `published: true` の記事 → そのまま更新として反映

ユーザーが公開を希望する場合、`published: true` に変更する。

### Step 3: コミット＆プッシュ

ユーザーの確認を得てから実行:

```bash
cd {ZENN_CONTENT_DIR}
git add .
git commit -m "<コミットメッセージ>"
git push origin main
```

コミットメッセージはユーザーに提案する。例:
- `docs: add article <slug>` （新規記事）
- `docs: update article <slug>` （記事更新）
- `docs: publish article <slug>` （下書き→公開）

### Step 4: 完了案内

以下を伝える:
- pushが完了したこと
- Zennのダッシュボードでデプロイ状況を確認できること（https://zenn.dev/dashboard）
- 反映まで数分かかる場合があること

## Constraints

- git push前に必ずユーザーの確認を取ること（共有リソースへの操作）
- publishedフラグの変更も確認を取ること
- pushする前に変更差分を表示して内容を確認させること
