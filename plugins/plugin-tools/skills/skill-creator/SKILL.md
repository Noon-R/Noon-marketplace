---
name: skill-creator
description: |
  プラグイン内に新規スキルのディレクトリ構造とSKILL.mdテンプレートを自動生成します。
  init_skill.pyを使ったスキル初期化、SKILL.mdテンプレート生成、ディレクトリ構造作成を支援。
  トリガー：「スキルを作成」「新しいスキル」「skill create」「create skill」「init skill」
---

# Skill Creator

プラグイン内に新規スキルを作成するワークフローを提供します。

## ワークフロー

### 1. スキル初期化

```bash
# 新規スキルを作成
python scripts/init_skill.py <skill-name> --path ./plugins/<plugin-name>/skills

# 説明を指定して作成
python scripts/init_skill.py <skill-name> --path ./plugins/<plugin-name>/skills --description "スキルの説明"
```

出力:
```
plugins/<plugin-name>/skills/<skill-name>/
├── SKILL.md       <- スキル定義（テンプレート生成済み）
├── scripts/       <- 実行スクリプト用（空）
├── references/    <- リファレンスドキュメント用（空）
└── assets/        <- リソースファイル用（空）
```

### 2. SKILL.md の編集

生成されたテンプレートを編集して、スキルの詳細を記述します：

```yaml
---
name: skill-name
description: |
  スキルの詳細な説明。
  Claude Codeが自動認識するためのトリガーキーワードを含める。
  トリガー：「キーワード1」「キーワード2」
---
```

### 3. バリデーション

```bash
# skill-updaterのvalidate_skill.pyを使用して構造を検証
python plugins/plugin-tools/skills/skill-updater/scripts/validate_skill.py <skill-path>
```

## スキル構造

```
<skill-name>/
├── SKILL.md       # スキル定義（必須）
├── scripts/       # 実行スクリプト（オプション）
├── references/    # 詳細ドキュメント（オプション）
└── assets/        # リソースファイル（オプション）
```

## SKILL.md 設計指針

### Frontmatter 必須フィールド

```yaml
---
name: skill-name          # ハイフン区切り、小文字
description: |
  スキルの説明（20文字以上）
  トリガーキーワードを含める
---
```

### Progressive Disclosure

- SKILL.md は 500 行以下を目標
- 詳細情報は `references/` に分離して SKILL.md からリンク
- スクリプトは `scripts/` に配置

### 命名規約

- **スキル名**: ハイフン区切り、小文字（例: `code-review`）
- **スクリプトファイル**: スネークケース（例: `run_analysis.py`）
- **バージョン**: セマンティックバージョニング

## 使用例

```bash
# dev-workflow プラグインに code-review スキルを追加
python plugins/plugin-tools/skills/skill-creator/scripts/init_skill.py \
  code-review \
  --path ./plugins/dev-workflow/skills \
  --description "コードレビューワークフローを提供します"
```
