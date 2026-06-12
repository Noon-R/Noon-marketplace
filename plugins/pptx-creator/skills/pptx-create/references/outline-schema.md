# Outline JSON スキーマ

`build_pptx.py` に渡すアウトラインJSONの仕様。

## トップレベル

```json
{
  "template": "path/to/template.pptx",
  "slide_size": "16:9",
  "keep_existing_slides": false,
  "slides": [ ... ]
}
```

| キー | 必須 | 説明 |
|---|---|---|
| `template` | - | テンプレート.pptxのパス。CLIの `-t` が優先される |
| `slide_size` | - | `"16:9"` 指定可。**テンプレート未使用時のみ**有効（デフォルトは4:3） |
| `keep_existing_slides` | - | `true` でテンプレート内の既存スライドを残す。デフォルト `false`（全削除して空の状態から生成） |
| `slides` | ✓ | スライド定義の配列 |

## スライド定義

```json
{
  "layout": "Title and Content",
  "title": "スライドタイトル",
  "body": [
    "第一階層の箇条書き",
    { "text": "第二階層", "level": 1 },
    { "text": "強調したい行", "bold": true, "size_pt": 20 }
  ],
  "placeholders": {
    "2": "idx=2 のプレースホルダーに入れるテキスト",
    "テキスト プレースホルダー 3": ["名前指定も可", "リストなら箇条書き"]
  },
  "images": [
    { "path": "logo.png", "placeholder": 13 },
    { "path": "chart.png", "left_cm": 2, "top_cm": 5, "width_cm": 14 }
  ],
  "tables": [
    { "placeholder": 14, "rows": [["項目", "値"], ["A", "100"]] },
    { "rows": [["..."]], "left_cm": 2, "top_cm": 5, "width_cm": 20, "height_cm": 6 }
  ],
  "notes": "発表者ノート",
  "prune_empty": true
}
```

| キー | 説明 |
|---|---|
| `layout` | レイアウト名（`inspect_template.py` の出力名と一致させる）または通し番号。省略時は `1` |
| `title` | タイトルプレースホルダーへのショートカット |
| `body` | 最初の本文プレースホルダーへのショートカット。文字列 or `{text, level, bold, size_pt}` の配列 |
| `placeholders` | idx（数値文字列）またはシェイプ名 → テキスト/箇条書き配列。複数カラムレイアウトはこちらで指定 |
| `images` | `placeholder` 指定で画像プレースホルダーに挿入、なければ cm 座標で配置 |
| `tables` | `rows` は二次元配列。`placeholder` 指定 or cm 座標 |
| `notes` | 発表者ノート |
| `prune_empty` | 未使用プレースホルダーの削除（デフォルト `true`。「テキストを入力」の枠が残らない） |

## 注意

- レイアウト名・プレースホルダーidxはテンプレートごとに異なる。**必ず先に `inspect_template.py` で確認**してから書くこと。
- フォント・色・背景はテンプレートのスライドマスターに従う。アウトライン側では原則指定しない（`bold` / `size_pt` は例外的な強調用）。
- 画像パスはスクリプト実行時のカレントディレクトリ基準。絶対パス推奨。
