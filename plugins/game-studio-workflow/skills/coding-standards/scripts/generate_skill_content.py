#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate dynamic content for SKILL.md based on language_packs.json.

Usage:
    python generate_skill_content.py update    # Update SKILL.md dynamic content
    python generate_skill_content.py preview   # Preview generated content
"""

import argparse
import json
import os
import re
import sys
import io
from datetime import datetime

# Windows UTF-8 support
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def get_paths():
    """Get paths to config and SKILL.md files."""
    script_dir = os.path.dirname(os.path.abspath(__file__))

    config_path = os.path.join(script_dir, '..', '..', '..', 'config', 'language_packs.json')
    skill_path = os.path.join(script_dir, '..', 'SKILL.md')

    return {
        'config': os.path.normpath(config_path),
        'skill': os.path.normpath(skill_path)
    }


def load_language_packs():
    """Load language packs configuration."""
    paths = get_paths()
    config_path = paths['config']

    if not os.path.exists(config_path):
        print(f"Error: Config file not found at {config_path}", file=sys.stderr)
        return None

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config: {e}", file=sys.stderr)
        return None


def generate_dynamic_content(config):
    """Generate the dynamic content section."""
    packs = config.get('language_packs', {})
    version = config.get('version', '1.0.0')
    last_updated = config.get('last_updated', datetime.now().strftime('%Y-%m-%d'))

    lines = []
    lines.append(f"\n## 利用可能な言語パック\n")
    lines.append(f"以下の言語パックが利用可能です (最終更新: {last_updated}, version: {version})\n")
    lines.append("| キーワード | 言語/規約 | ファイル | 状態 |")
    lines.append("|-----------|----------|---------|------|")

    for key, pack in sorted(packs.items(), key=lambda x: x[1].get('priority', 999)):
        keywords = "'" + "', '".join(pack.get('keywords', [])) + "'"
        display_name = pack.get('display_name', key)
        file_path = pack.get('file_path', 'N/A')
        status = pack.get('status', 'unknown')
        status_text = 'OK' if status == 'available' else 'PLANNED' if status == 'planned' else 'N/A'

        lines.append(f"| {keywords} | {display_name} | [{file_path}]({file_path}) | {status_text} |")

    lines.append("\n## 利用可能な言語パック（詳細）\n")

    for key, pack in sorted(packs.items(), key=lambda x: x[1].get('priority', 999)):
        display_name = pack.get('display_name', key)
        keywords = "'" + "', '".join(pack.get('keywords', [])) + "'"
        detail_level = pack.get('detail_level', 'basic')

        # Add special notes for Unity
        if key == 'unity':
            lines.append(f"- **{display_name}**: {keywords} (詳細度: {detail_level})")
            lines.append(f"  - **重要な制約**: Linq禁止、try-catch例外処理禁止")
        else:
            lines.append(f"- **{display_name}**: {keywords} (詳細度: {detail_level})")

    lines.append("")

    return '\n'.join(lines)


def update_skill_md(preview_only=False):
    """Update SKILL.md with generated content."""
    paths = get_paths()
    config = load_language_packs()

    if config is None:
        return False

    dynamic_content = generate_dynamic_content(config)

    if preview_only:
        print("=== Preview of Dynamic Content ===")
        print(dynamic_content)
        return True

    # Read current SKILL.md
    skill_path = paths['skill']
    if not os.path.exists(skill_path):
        print(f"Error: SKILL.md not found at {skill_path}", file=sys.stderr)
        return False

    try:
        with open(skill_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading SKILL.md: {e}", file=sys.stderr)
        return False

    # Replace content between markers
    pattern = r'(<!-- DYNAMIC_CONTENT_START:.*?-->).*?(<!-- DYNAMIC_CONTENT_END -->)'
    replacement = r'\1' + dynamic_content + r'\2'

    new_content, count = re.subn(pattern, replacement, content, flags=re.DOTALL)

    if count == 0:
        print("Warning: Dynamic content markers not found in SKILL.md", file=sys.stderr)
        return False

    # Write updated content
    try:
        with open(skill_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Successfully updated {skill_path}")
        return True
    except Exception as e:
        print(f"Error writing SKILL.md: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description='Generate dynamic content for SKILL.md')
    parser.add_argument('action', choices=['update', 'preview'],
                       help='Action to perform: update SKILL.md or preview content')

    args = parser.parse_args()

    if args.action == 'preview':
        update_skill_md(preview_only=True)
    else:
        success = update_skill_md(preview_only=False)
        sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
