---
name: pptx-create
description: |
  PowerPoint資料（.pptx）の作成スキル。テンプレート.pptxのスライドマスターを差し替え可能で、
  テンプレートごとのデザインドキュメント（design.md）に従って構成・文面を組み立てる。
  依存OSSは python-pptx のみ。
  トリガー：「パワポ」「PowerPoint」「pptx」「スライド作成」「プレゼン資料」「資料を作って」
---

# PowerPoint Deck Creation Skill

アウトラインJSON → `scripts/build_pptx.py` で .pptx を生成する。
スタイルはすべてテンプレートのスライドマスターに委ね、Claudeは「構成と文面」に集中する。

## ディレクトリ

```
scripts/inspect_template.py   テンプレートのレイアウト/プレースホルダー一覧
scripts/build_pptx.py         アウトラインJSONから.pptx生成
templates/<名前>/template.pptx  スライドマスター（差し替え可能、templates/README.md参照）
templates/<名前>/design.md      テンプレートごとのデザインドキュメント
references/outline-schema.md   アウトラインJSONの仕様
references/design-doc-template.md  design.mdのひな形
```

## 前提

`python-pptx` が必要（依存はこれ1つ）:
```bash
pip install python-pptx
```

## Workflow

### Step 1: ヒアリング

未指定の項目のみ質問する:

1. **テーマと目的**: 何の資料か、誰に見せるか
2. **テンプレート**: `ls` で `templates/` 配下を提示して選んでもらう。
   ユーザーが自前の .pptx を持っている場合はパスを聞く（その場で使うか、
   `templates/` に登録するかも確認）
3. **分量**: おおよその枚数
4. **素材**: 元になるドキュメント・データ・画像があるか

### Step 2: デザインドキュメントとテンプレート構造の確認

1. 選ばれたテンプレートの `design.md` を**必ず読む**。構成ルール・レイアウトの
   使い分け・テキストルールはこれに従う。`design.md` がない場合はその旨を伝え、
   `references/design-doc-template.md` から作ることを提案する（任意）
2. `template.pptx` がある場合はレイアウト構成を確認する:
   ```bash
   python scripts/inspect_template.py templates/<名前>/template.pptx
   ```
   出力されたレイアウト名・プレースホルダーidxを以降のアウトラインで使う。
   **名前を推測で書かない**こと

### Step 3: 構成案の合意

スライド一覧（タイトル + 要点1行）をテキストで提示し、ユーザーの同意を得る。
design.md の構成ルール（1スライド1メッセージ、枚数上限など）を反映する。

### Step 4: アウトラインJSON作成と生成

1. `references/outline-schema.md` の仕様でアウトラインJSONを作成する
2. 生成:
   ```bash
   python scripts/build_pptx.py outline.json -o <出力名>.pptx -t templates/<名前>/template.pptx
   ```
   テンプレートなし（default）の場合は `-t` を省略し、JSONに `"slide_size": "16:9"` を入れる
3. エラー（レイアウト名不一致など）が出たら inspect の出力と突き合わせて修正する

### Step 5: 完了確認

- 生成ファイルのパスと枚数を伝える
- 直したい箇所を聞き、アウトラインJSONを修正 → 再生成で反映する
  （JSONを残しておけば何度でも作り直せることを伝える）

## テンプレートの差し替え・追加

`templates/README.md` の手順に従う。要点:
- `templates/<名前>/template.pptx` を置くだけで差し替え可能
- 追加時は `inspect_template.py` で構造確認 → `design.md` 作成を促す
- 同じアウトラインJSONでも、レイアウト名がテンプレート間で異なれば
  `layout` / `placeholders` の指定は書き直しが必要

## Constraints

- 色・フォント・背景はスライドマスターに委ねる。アウトラインJSONで装飾を
  指定しない（`bold` / `size_pt` は例外的な強調のみ）
- design.md とユーザー指示が矛盾したらユーザー指示を優先し、design.md の
  更新を提案する
- 既存の .pptx を上書きする前に確認を取る
- アウトラインJSONは成果物と同じ場所に残す（再編集のため）
