#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
List available coding standards and search by keywords.

Usage:
    python list_standards.py                    # List all standards
    python list_standards.py --search "unity"   # Search by keyword
    python list_standards.py --json             # Output as JSON
"""

import argparse
import json
import os
import sys
import io

# Windows UTF-8 support
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def get_config_path():
    """Get the path to language_packs.json config file."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Navigate up to skills/coding-standards, then to plugin root config
    config_path = os.path.join(script_dir, '..', '..', '..', 'config', 'language_packs.json')
    return os.path.normpath(config_path)


def load_language_packs():
    """Load language packs configuration."""
    config_path = get_config_path()

    if not os.path.exists(config_path):
        print(f"Warning: Config file not found at {config_path}", file=sys.stderr)
        return {}

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            return config.get('language_packs', {})
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in config file: {e}", file=sys.stderr)
        return {}
    except Exception as e:
        print(f"Error loading config: {e}", file=sys.stderr)
        return {}


def list_all_standards(as_json=False):
    """List all available coding standards."""
    packs = load_language_packs()

    if as_json:
        print(json.dumps(packs, ensure_ascii=False, indent=2))
        return

    if not packs:
        print("No language packs found.")
        return

    print("## Available Coding Standards\n")
    print("| Keywords | Language/Standard | File | Status |")
    print("|----------|------------------|------|--------|")

    for key, pack in sorted(packs.items(), key=lambda x: x[1].get('priority', 999)):
        keywords = "'" + "', '".join(pack.get('keywords', [])) + "'"
        display_name = pack.get('display_name', key)
        file_path = pack.get('file_path', 'N/A')
        status = pack.get('status', 'unknown')
        status_symbol = '✓' if status == 'available' else '○' if status == 'planned' else '✗'

        print(f"| {keywords} | {display_name} | [{file_path}]({file_path}) | {status_symbol} |")

    print("\n## Detail Levels")
    for key, pack in sorted(packs.items(), key=lambda x: x[1].get('priority', 999)):
        display_name = pack.get('display_name', key)
        keywords = "'" + "', '".join(pack.get('keywords', [])) + "'"
        detail_level = pack.get('detail_level', 'basic')
        print(f"- **{display_name}**: {keywords} (詳細度: {detail_level})")


def search_standards(keyword):
    """Search for standards matching a keyword."""
    packs = load_language_packs()
    keyword_lower = keyword.lower()

    matches = []
    for key, pack in packs.items():
        pack_keywords = [k.lower() for k in pack.get('keywords', [])]
        if keyword_lower in pack_keywords or keyword_lower in key.lower():
            matches.append({
                'key': key,
                'display_name': pack.get('display_name', key),
                'file_path': pack.get('file_path'),
                'status': pack.get('status', 'unknown'),
                'priority': pack.get('priority', 999),
                'detail_level': pack.get('detail_level', 'basic')
            })

    # Sort by priority
    matches.sort(key=lambda x: x['priority'])

    if not matches:
        print(f"No standards found matching '{keyword}'")
        return

    print(f"## Standards matching '{keyword}'\n")
    for match in matches:
        status_symbol = '✓' if match['status'] == 'available' else '○'
        print(f"- **{match['display_name']}** [{status_symbol}]")
        print(f"  - File: {match['file_path']}")
        print(f"  - Detail Level: {match['detail_level']}")


def main():
    parser = argparse.ArgumentParser(description='List and search coding standards')
    parser.add_argument('--search', '-s', type=str, help='Search by keyword')
    parser.add_argument('--json', '-j', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    if args.search:
        search_standards(args.search)
    else:
        list_all_standards(as_json=args.json)


if __name__ == '__main__':
    main()
