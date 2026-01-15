---
name: skill-updater
description: |
  既存スキルの更新・編集ワークフローを提供します。
  SKILL.mdのfrontmatter編集、description更新、ワークフロー追加、scripts/references管理を支援。
  トリガー：「スキルを更新」「skill update」「SKILL.mdを編集」「スキルの説明を変更」
---

# Skill Updater

既存スキルの更新・メンテナンスを効率化するワークフローを提供します。

## ワークフロー

### 1. 対象スキルの特定

```bash
# スキル一覧を表示
python scripts/update_skill.py list

# 特定のスキルを検索
python scripts/update_skill.py search <keyword>
```

### 2. 現在の構造確認

```bash
# スキルの構造と内容を確認
python scripts/update_skill.py info <skill-path>
```

出力例:
```
Skill: coding-standards
Description: コーディング規約を提供...
Files:
  - SKILL.md (125 lines)
  - scripts/generate_skill_content.py
  - references/unity/standards.md
```

### 3. バリデーション

```bash
# スキルの構造を検証
python scripts/validate_skill.py <skill-path>
```

検証項目:
- SKILL.md存在チェック
- YAML frontmatter形式（name, description必須）
- ディレクトリ構造
- 参照ファイルの存在

### 4. 更新実行

**SKILL.md更新の例**:

1. **description変更**: frontmatterのdescriptionを編集
2. **ワークフロー追加**: 新しいセクションを追加
3. **トリガーキーワード追加**: descriptionにキーワードを追加

**scripts更新**:
- 新しいスクリプトを `scripts/` に追加
- UTF-8エンコーディングを使用
- Windows互換性のため `sys.stdout` ラッパーを追加

**references更新**:
- 詳細ドキュメントを `references/` に追加
- SKILL.mdから参照リンクを記述

### 5. 更新後のバリデーション

```bash
python scripts/validate_skill.py <skill-path>
```

## 更新時の注意点

### YAML Frontmatter

```yaml
---
name: skill-name  # ハイフン区切り、小文字
description: |
  複数行の説明。
  トリガーキーワードを含める。
---
```

### Progressive Disclosure

- SKILL.mdは500行以下を目標
- 詳細情報は `references/` に分離
- SKILL.mdから明確にリンク

### スクリプト規約

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import io

# Windows UTF-8サポート
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
```
