# テンプレート置き場

テンプレートは1ディレクトリ=1テンプレート。差し替え・追加はディレクトリを足すだけ。

```
templates/
  default/            # 組み込みデフォルト（template.pptx なし = python-pptx標準マスター）
    design.md         # デザインドキュメント
  my-company/         # 例: 自社テンプレート
    template.pptx     # スライドマスター・レイアウト定義済みの .pptx
    design.md         # このテンプレート用のデザインルール（任意だが推奨）
```

## 自社テンプレートの追加手順

1. PowerPointでスライドマスターを編集した .pptx を用意する
   （サンプルスライドが入っていてもよい。生成時にデフォルトで全削除される）
2. `templates/<名前>/template.pptx` として配置
3. `python scripts/inspect_template.py templates/<名前>/template.pptx` で
   レイアウト名とプレースホルダー構成を確認
4. `references/design-doc-template.md` をコピーして `design.md` を書く
   （レイアウトの使い分け・テキストルールなど）

## 注意

- レイアウト名はテンプレート作成時のPowerPointの言語に依存する
  （日本語版なら「タイトル スライド」等）。アウトラインJSONでは
  `inspect_template.py` が出力した名前をそのまま使うこと。
- `template.pptx` が存在しないテンプレートディレクトリ（default等）は
  python-pptx の組み込みマスターで生成される。
