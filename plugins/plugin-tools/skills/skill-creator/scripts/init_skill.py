#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill Initializer - Creates a new skill directory structure within a plugin.

Usage:
    python init_skill.py <skill-name> --path <plugin-skills-dir>
    python init_skill.py my-skill --path ./plugins/my-plugin/skills
    python init_skill.py my-skill --path ./plugins/my-plugin/skills --description "My skill description"
"""

import argparse
import os
import sys
import io

# Windows UTF-8 support
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


SKILL_MD_TEMPLATE = """\
---
name: {skill_name}
description: |
  {description}
  トリガー：「{skill_name}」「{trigger}」
---

# {skill_title}

{description}

## ワークフロー

### 1. 事前確認

<!-- 実行前に確認すべき事項を記載 -->

### 2. 実行手順

<!-- スキルの具体的な手順を記載 -->

### 3. 完了確認

<!-- 完了の確認方法を記載 -->

## 使用例

```
# 例: このスキルの使い方
```

## 注意事項

<!-- 注意すべき点があれば記載 -->
"""


def validate_skill_name(name):
    """Validate skill name format."""
    import re
    if not re.match(r'^[a-z][a-z0-9-]*$', name):
        return False, "Skill name must be lowercase, start with letter, use only letters, numbers, and hyphens"
    if len(name) > 40:
        return False, "Skill name must be 40 characters or less"
    if '--' in name:
        return False, "Skill name cannot contain consecutive hyphens"
    return True, None


def init_skill(skill_name, skills_path, description=None):
    """
    Initialize a new skill directory structure.

    Args:
        skill_name: Name of the skill
        skills_path: Path to the plugin's skills directory
        description: Optional skill description

    Returns:
        Path to created skill directory, or None if error
    """
    # Validate skill name
    is_valid, error = validate_skill_name(skill_name)
    if not is_valid:
        print(f"Error: {error}")
        return None

    # Determine skill directory path
    skill_dir = os.path.join(os.path.abspath(skills_path), skill_name)

    # Check if directory already exists
    if os.path.exists(skill_dir):
        print(f"Error: Skill directory already exists: {skill_dir}")
        return None

    # Check parent directory exists
    if not os.path.exists(skills_path):
        print(f"Error: Skills directory does not exist: {skills_path}")
        return None

    # Create directory structure
    try:
        os.makedirs(skill_dir)
        print(f"Created: {skill_dir}/")

        scripts_dir = os.path.join(skill_dir, 'scripts')
        os.makedirs(scripts_dir)
        print(f"Created: {scripts_dir}/")

        refs_dir = os.path.join(skill_dir, 'references')
        os.makedirs(refs_dir)
        print(f"Created: {refs_dir}/")

        assets_dir = os.path.join(skill_dir, 'assets')
        os.makedirs(assets_dir)
        print(f"Created: {assets_dir}/")

    except Exception as e:
        print(f"Error creating directories: {e}")
        return None

    # Create SKILL.md from template
    desc = description or f"{skill_name} skill"
    skill_title = ' '.join(w.capitalize() for w in skill_name.split('-'))
    trigger = skill_name.replace('-', ' ')

    skill_md_content = SKILL_MD_TEMPLATE.format(
        skill_name=skill_name,
        skill_title=skill_title,
        description=desc,
        trigger=trigger,
    )

    skill_md_path = os.path.join(skill_dir, 'SKILL.md')
    try:
        with open(skill_md_path, 'w', encoding='utf-8') as f:
            f.write(skill_md_content)
        print(f"Created: {skill_md_path}")
    except Exception as e:
        print(f"Error creating SKILL.md: {e}")
        return None

    # Print summary
    print(f"\n{'='*50}")
    print(f"Skill '{skill_name}' created successfully!")
    print(f"{'='*50}")
    print(f"\nLocation: {skill_dir}")
    print(f"\nStructure:")
    print(f"  {skill_name}/")
    print(f"  ├── SKILL.md       <- Edit this with skill details")
    print(f"  ├── scripts/       <- Add execution scripts here")
    print(f"  ├── references/    <- Add reference docs here")
    print(f"  └── assets/        <- Add resource files here")
    print(f"\nNext steps:")
    print(f"  1. Edit {skill_md_path}")
    print(f"     - Update description and trigger keywords")
    print(f"     - Fill in the workflow steps")
    print(f"  2. Add scripts to {scripts_dir}/")
    print(f"  3. Validate: python validate_skill.py {skill_dir}")

    return skill_dir


def main():
    parser = argparse.ArgumentParser(description='Initialize a new skill in a plugin')
    parser.add_argument('skill_name', help='Name of the skill (lowercase, hyphen-separated)')
    parser.add_argument('--path', required=True, help='Path to the plugin skills directory')
    parser.add_argument('--description', '-d', help='Skill description')

    args = parser.parse_args()

    print(f"Initializing skill: {args.skill_name}")
    print(f"Location: {args.path}")
    print()

    result = init_skill(args.skill_name, args.path, args.description)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
