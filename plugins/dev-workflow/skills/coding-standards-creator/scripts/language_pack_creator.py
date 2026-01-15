#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Language pack creator utilities for coding-standards skill.

Usage:
    python language_pack_creator.py create <language_key> --name "Display Name"
    python language_pack_creator.py validate <language_key>
    python language_pack_creator.py list-templates
"""

import argparse
import json
import os
import sys
import io
from datetime import datetime

# Windows UTF-8 support
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


# Template for 15 sections
SECTION_TEMPLATE = """# {display_name} コーディング規約

## 1. 命名規則

### 1.1 基本原則
- **英語を使用**し、略語は避ける
- **意味のある名前**を付ける
- **一貫性**を保つ

### 1.2 ケース規則

| 要素 | ケース | 例 |
|------|--------|-----|
| クラス | PascalCase | `UserService`, `OrderManager` |
| インターフェース | PascalCase (I接頭辞) | `IUserService`, `IRepository` |
| メソッド | PascalCase | `GetUser()`, `SaveOrder()` |
| プロパティ | PascalCase | `FirstName`, `IsActive` |
| フィールド (private) | _PascalCase | `_UserName`, `_IsInitialized` |
| 変数・パラメータ | camelCase | `userName`, `orderCount` |
| 定数 | SNAKE_CASE | `MAX_CONNECTION_COUNT` |

## 2. フォーマット・レイアウト

### 2.1 インデント
- **4スペース**を使用（タブは使用しない）

### 2.2 波括弧の配置
- 新しい行に配置

### 2.3 行の長さ
- **120文字**を上限とする

## 3. クラス設計

### 3.1 クラスの構成順序
1. イベント
2. フィールド (定数 → static → instance)
3. コンストラクタ
4. プロパティ
5. メソッド

### 3.2 アクセス修飾子
- **最小限の公開レベル**を使用
- 明示的にアクセス修飾子を記述

## 4. メソッド設計

### 4.1 メソッドの責任
- **単一責任の原則**に従う

### 4.2 パラメータ
- **4個以下**を推奨

## 5. 非同期プログラミング

### 5.1 非同期メソッドの命名
- Asyncサフィックスを使用

## 6. コメントとドキュメント

### 6.1 XMLドキュメントコメント
- publicメンバーには必ず記述

## 7. パフォーマンス

### 7.1 文字列操作
- StringBuilderを使用

## 8. varキーワード

### 8.1 var使用の原則
- 右辺から型が明確に判断できる場合のみ使用

## 9. 例外処理

### 9.1 例外の種類
- 適切な例外を使用

## 10. LINQとコレクション

### 10.1 LINQ の使用
- メソッド構文を推奨

## 11. 型システム

### 11.1 型アノテーション
- 明示的な型宣言を推奨

## 12. テスト

### 12.1 ユニットテスト
- Arrange-Act-Assert パターンを使用

## 13. セキュリティ

### 13.1 入力検証
- すべての外部入力を検証

## 14. ツール・設定

### 14.1 推奨ツール
- エディタ設定を統一

## 15. リソース

### 15.1 参考資料
- 公式ドキュメント

---

## 更新履歴

| バージョン | 日付 | 変更内容 |
|-----------|------|---------|
| 1.0.0 | {date} | 初版リリース |

*このコーディング規約は継続的に更新・改善していきます。*
"""

METADATA_TEMPLATE = {
    "language": "",
    "display_name": "",
    "version": "1.0.0",
    "frameworks": [],
    "detail_level": "enterprise",
    "keywords": [],
    "sections": [
        "naming", "format", "class", "method", "async",
        "comments", "performance", "var", "error-handling",
        "linq", "types", "testing", "security", "tools", "resources"
    ]
}


def get_references_path():
    """Get the path to references directory."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Navigate to coding-standards/references
    refs_path = os.path.join(script_dir, '..', '..', 'coding-standards', 'references')
    return os.path.normpath(refs_path)


def create_language_pack(language_key, display_name, keywords=None, frameworks=None):
    """Create a new language pack directory structure."""
    refs_path = get_references_path()
    pack_path = os.path.join(refs_path, language_key)

    if os.path.exists(pack_path):
        print(f"Error: Language pack '{language_key}' already exists at {pack_path}")
        return False

    # Create directories
    os.makedirs(pack_path)
    os.makedirs(os.path.join(pack_path, 'examples'))

    # Create metadata.json
    metadata = METADATA_TEMPLATE.copy()
    metadata['language'] = language_key
    metadata['display_name'] = display_name
    metadata['keywords'] = keywords or [language_key]
    metadata['frameworks'] = frameworks or []

    metadata_path = os.path.join(pack_path, 'metadata.json')
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    # Create standards.md
    today = datetime.now().strftime('%Y-%m-%d')
    standards_content = SECTION_TEMPLATE.format(
        display_name=display_name,
        date=today
    )

    standards_path = os.path.join(pack_path, 'standards.md')
    with open(standards_path, 'w', encoding='utf-8') as f:
        f.write(standards_content)

    # Create example placeholder
    example_path = os.path.join(pack_path, 'examples', 'good_example.cs')
    with open(example_path, 'w', encoding='utf-8') as f:
        f.write(f"// Good example for {display_name}\n// TODO: Add example code\n")

    print(f"Created language pack '{language_key}' at {pack_path}")
    print(f"  - metadata.json")
    print(f"  - standards.md")
    print(f"  - examples/good_example.cs")
    print(f"\nNext steps:")
    print(f"  1. Edit standards.md with your coding conventions")
    print(f"  2. Add code examples to examples/")
    print(f"  3. Register in config/language_packs.json")

    return True


def validate_language_pack(language_key):
    """Validate an existing language pack structure."""
    refs_path = get_references_path()
    pack_path = os.path.join(refs_path, language_key)

    errors = []
    warnings = []

    # Check directory exists
    if not os.path.exists(pack_path):
        errors.append(f"Language pack directory not found: {pack_path}")
        print_validation_result(language_key, errors, warnings)
        return False

    # Check metadata.json
    metadata_path = os.path.join(pack_path, 'metadata.json')
    if not os.path.exists(metadata_path):
        errors.append("metadata.json not found")
    else:
        try:
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)

            required_fields = ['language', 'display_name', 'version', 'keywords']
            for field in required_fields:
                if field not in metadata:
                    errors.append(f"Missing required field in metadata.json: {field}")
        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON in metadata.json: {e}")

    # Check standards.md
    standards_path = os.path.join(pack_path, 'standards.md')
    if not os.path.exists(standards_path):
        errors.append("standards.md not found")
    else:
        with open(standards_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for required sections
        expected_sections = [
            "命名規則", "フォーマット", "クラス設計", "メソッド設計",
            "非同期", "コメント", "パフォーマンス", "var", "例外処理",
            "LINQ", "型システム", "テスト", "セキュリティ", "ツール", "リソース"
        ]

        for section in expected_sections:
            if section not in content:
                warnings.append(f"Section may be missing or renamed: {section}")

    # Check examples directory
    examples_path = os.path.join(pack_path, 'examples')
    if not os.path.exists(examples_path):
        warnings.append("examples/ directory not found")
    elif not os.listdir(examples_path):
        warnings.append("examples/ directory is empty")

    print_validation_result(language_key, errors, warnings)
    return len(errors) == 0


def print_validation_result(language_key, errors, warnings):
    """Print validation results."""
    print(f"\n=== Validation Result for '{language_key}' ===\n")

    if not errors and not warnings:
        print("✓ All checks passed!")
        return

    if errors:
        print("Errors:")
        for error in errors:
            print(f"  ✗ {error}")

    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"  ⚠ {warning}")

    print(f"\nResult: {'FAILED' if errors else 'PASSED with warnings'}")


def list_templates():
    """List available templates."""
    print("Available Templates:")
    print("  - csharp: Standard C# conventions")
    print("  - unity: Unity-specific C# (no LINQ, no try-catch)")
    print("  - typescript: TypeScript with ESLint")
    print("  - python: PEP 8 compliant Python")


def main():
    parser = argparse.ArgumentParser(description='Language pack creator utilities')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Create command
    create_parser = subparsers.add_parser('create', help='Create new language pack')
    create_parser.add_argument('language_key', help='Language key (e.g., "unity")')
    create_parser.add_argument('--name', required=True, help='Display name')
    create_parser.add_argument('--keywords', nargs='+', help='Search keywords')
    create_parser.add_argument('--frameworks', nargs='+', help='Target frameworks')

    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate language pack')
    validate_parser.add_argument('language_key', help='Language key to validate')

    # List templates command
    subparsers.add_parser('list-templates', help='List available templates')

    args = parser.parse_args()

    if args.command == 'create':
        create_language_pack(
            args.language_key,
            args.name,
            keywords=args.keywords,
            frameworks=args.frameworks
        )
    elif args.command == 'validate':
        validate_language_pack(args.language_key)
    elif args.command == 'list-templates':
        list_templates()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
