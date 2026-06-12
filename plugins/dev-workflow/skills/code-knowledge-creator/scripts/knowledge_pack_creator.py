#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Knowledge pack creator utilities for the code-knowledge skill.

Usage:
    python knowledge_pack_creator.py create <pack_key> --name "Display Name"
    python knowledge_pack_creator.py validate <pack_key>
    python knowledge_pack_creator.py list-templates
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


CORE_TEMPLATE = """# {display_name} Core Constraints（常時適用・違反禁止）

> このファイルは実装agentのコンテキストに常時注入される。サイズ予算: ~2KB。
> 詳細規約は `sections/`、模範コードは `examples/` を参照。

## 🔴 致命的制約（❌→✅ 書き換え対訳）

<!-- 「絶対に違反してはならない制約」だけをここに書く。
     各制約には必ず ❌（禁止形）と ✅（代替手段）の対訳コードを付ける。 -->

### 1. {{制約名}}

```
// ❌ {{禁止されるコード}}
// ✅ {{代替コード}}
```

## 🔴 必須スタイル（要点のみ）

| 項目 | ルール |
|------|--------|
| {{項目}} | {{ルール}} |

実装前に `examples/` のゴールデンサンプルを読むこと。迷ったらサンプルの書き方に合わせる。
"""

SECTION_TEMPLATE = """# {display_name} {section_title}（詳細）

<!-- このセクションはオンデマンドでロードされる詳細リファレンス。
     core.mdにある制約の背景・詳細パターン・コード例をここに書く。 -->
"""

DEFAULT_SECTIONS = {
    'naming': '命名規則',
    'formatting': 'フォーマット・レイアウト',
    'class-design': 'クラス・メソッド設計',
    'error-handling': 'エラー処理',
    'testing': 'テスト',
}


def get_references_path():
    """Get the path to code-knowledge references directory."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    refs_path = os.path.join(script_dir, '..', '..', 'code-knowledge', 'references')
    return os.path.normpath(refs_path)


def create_knowledge_pack(pack_key, display_name, keywords=None, frameworks=None):
    """Create a new structured knowledge pack scaffold."""
    refs_path = get_references_path()
    pack_path = os.path.join(refs_path, pack_key)

    if os.path.exists(pack_path):
        print(f"Error: Knowledge pack '{pack_key}' already exists at {pack_path}")
        return False

    os.makedirs(os.path.join(pack_path, 'examples'))
    os.makedirs(os.path.join(pack_path, 'sections'))

    # metadata.json
    sections_meta = {}
    for key, title in DEFAULT_SECTIONS.items():
        sections_meta[key] = {
            'path': f'references/{pack_key}/sections/{key}.md',
            'description': f'{title}の詳細'
        }

    metadata = {
        'language': pack_key,
        'display_name': display_name,
        'version': '1.0.0',
        'frameworks': frameworks or [],
        'detail_level': 'detailed',
        'format': 'structured',
        'keywords': keywords or [pack_key],
        'core_path': f'references/{pack_key}/core.md',
        'examples': [],
        'sections': sections_meta,
        'constraints': {},
        'last_updated': datetime.now().strftime('%Y-%m-%d')
    }

    with open(os.path.join(pack_path, 'metadata.json'), 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    # core.md
    with open(os.path.join(pack_path, 'core.md'), 'w', encoding='utf-8') as f:
        f.write(CORE_TEMPLATE.format(display_name=display_name))

    # section scaffolds
    for key, title in DEFAULT_SECTIONS.items():
        section_path = os.path.join(pack_path, 'sections', f'{key}.md')
        with open(section_path, 'w', encoding='utf-8') as f:
            f.write(SECTION_TEMPLATE.format(display_name=display_name, section_title=title))

    print(f"Created knowledge pack scaffold '{pack_key}' at {pack_path}")
    print("  - metadata.json")
    print("  - core.md (要編集: 致命的制約とスタイル要点)")
    print(f"  - sections/ ({', '.join(DEFAULT_SECTIONS.keys())})")
    print("  - examples/ (空: ゴールデンサンプルを追加すること)")
    print("\nNext steps:")
    print("  1. core.md に致命的制約を ❌/✅ 対訳形式で記述")
    print("  2. examples/ にゴールデンサンプル（コンパイル可能・~100行）を追加し、metadata.jsonのexamplesに登録")
    print("  3. sections/ の各ファイルに詳細規約を記述（不要なセクションは削除）")
    print("  4. config/knowledge_packs.json に登録")
    print("  5. code-knowledge/scripts/generate_skill_content.py update を実行")

    return True


def validate_knowledge_pack(pack_key):
    """Validate an existing knowledge pack structure (structured or monolithic)."""
    refs_path = get_references_path()
    pack_path = os.path.join(refs_path, pack_key)

    errors = []
    warnings = []

    if not os.path.exists(pack_path):
        errors.append(f"Knowledge pack directory not found: {pack_path}")
        print_validation_result(pack_key, errors, warnings)
        return False

    # metadata.json
    metadata = {}
    metadata_path = os.path.join(pack_path, 'metadata.json')
    if not os.path.exists(metadata_path):
        errors.append("metadata.json not found")
    else:
        try:
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            for field in ['language', 'display_name', 'version', 'keywords']:
                if field not in metadata:
                    errors.append(f"Missing required field in metadata.json: {field}")
        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON in metadata.json: {e}")

    pack_format = metadata.get('format', 'monolithic')

    if pack_format == 'structured':
        # core.md
        core_path = os.path.join(pack_path, 'core.md')
        if not os.path.exists(core_path):
            errors.append("core.md not found (required for structured packs)")
        else:
            size = os.path.getsize(core_path)
            if size > 4096:
                warnings.append(f"core.md is {size} bytes (budget: ~2KB). 詳細はsections/へ移すこと")
            with open(core_path, 'r', encoding='utf-8') as f:
                core_content = f.read()
            if '❌' not in core_content or '✅' not in core_content:
                warnings.append("core.md に ❌/✅ 対訳が見つからない。禁止事項には代替手段を必ず示すこと")

        # examples
        examples_path = os.path.join(pack_path, 'examples')
        if not os.path.exists(examples_path) or not os.listdir(examples_path):
            warnings.append("examples/ が空。ゴールデンサンプルは規約遵守率に最も効く要素")
        else:
            registered = {os.path.basename(e.get('path', '')) for e in metadata.get('examples', [])}
            actual = set(os.listdir(examples_path))
            for missing in actual - registered:
                warnings.append(f"example '{missing}' が metadata.json の examples に未登録")

        # sections
        sections_path = os.path.join(pack_path, 'sections')
        if not os.path.exists(sections_path):
            warnings.append("sections/ directory not found")
        else:
            for key, section in metadata.get('sections', {}).items():
                section_file = os.path.join(pack_path, 'sections', os.path.basename(section.get('path', '')))
                if not os.path.exists(section_file):
                    errors.append(f"Section file missing: {section.get('path')}")
    else:
        # monolithic
        standards_path = os.path.join(pack_path, 'standards.md')
        if not os.path.exists(standards_path):
            errors.append("standards.md not found (required for monolithic packs)")
        else:
            size = os.path.getsize(standards_path)
            if size > 8192:
                warnings.append(
                    f"standards.md is {size} bytes — コンテキスト圧迫の懸念。"
                    "structured形式（core/examples/sections）への移行を推奨"
                )

    print_validation_result(pack_key, errors, warnings)
    return len(errors) == 0


def print_validation_result(pack_key, errors, warnings):
    """Print validation results."""
    print(f"\n=== Validation Result for '{pack_key}' ===\n")

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
    print("  - unity: Unity-specific C# (no LINQ, no try-catch) — see references/unity as the reference implementation")
    print("  - typescript: TypeScript with ESLint")
    print("  - python: PEP 8 compliant Python")


def main():
    parser = argparse.ArgumentParser(description='Knowledge pack creator utilities')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    create_parser = subparsers.add_parser('create', help='Create new knowledge pack scaffold')
    create_parser.add_argument('pack_key', help='Pack key (e.g., "unity")')
    create_parser.add_argument('--name', required=True, help='Display name')
    create_parser.add_argument('--keywords', nargs='+', help='Search keywords')
    create_parser.add_argument('--frameworks', nargs='+', help='Target frameworks')

    validate_parser = subparsers.add_parser('validate', help='Validate knowledge pack')
    validate_parser.add_argument('pack_key', help='Pack key to validate')

    subparsers.add_parser('list-templates', help='List available templates')

    args = parser.parse_args()

    if args.command == 'create':
        create_knowledge_pack(
            args.pack_key,
            args.name,
            keywords=args.keywords,
            frameworks=args.frameworks
        )
    elif args.command == 'validate':
        validate_knowledge_pack(args.pack_key)
    elif args.command == 'list-templates':
        list_templates()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
