#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill management utilities - list, search, and inspect skills.

Usage:
    python update_skill.py list [--path <plugins-dir>]
    python update_skill.py search <keyword> [--path <plugins-dir>]
    python update_skill.py info <skill-path>
"""

import argparse
import os
import sys
import io
import re
import json

# Windows UTF-8 support
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def get_default_plugins_path():
    """Get the default plugins path relative to script location."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Navigate up from skills/skill-updater/scripts to plugins/
    plugins_path = os.path.join(script_dir, '..', '..', '..', '..')
    return os.path.normpath(plugins_path)


def parse_frontmatter(content):
    """Parse YAML frontmatter from SKILL.md content."""
    pattern = r'^---\s*\n(.*?)\n---\s*\n'
    match = re.match(pattern, content, re.DOTALL)
    if not match:
        return None

    frontmatter = {}
    lines = match.group(1).strip().split('\n')
    current_key = None
    current_value = []

    for line in lines:
        if line.startswith('  ') and current_key:
            current_value.append(line.strip())
        elif ':' in line:
            if current_key:
                frontmatter[current_key] = '\n'.join(current_value).strip()
            key, _, value = line.partition(':')
            current_key = key.strip()
            value = value.strip()
            if value == '|':
                current_value = []
            else:
                current_value = [value] if value else []
        else:
            if current_key:
                current_value.append(line.strip())

    if current_key:
        frontmatter[current_key] = '\n'.join(current_value).strip()

    return frontmatter


def find_skills(plugins_path):
    """Find all skills in the plugins directory."""
    skills = []

    if not os.path.exists(plugins_path):
        return skills

    # Look for plugins
    plugins_dir = os.path.join(plugins_path, 'plugins')
    if not os.path.exists(plugins_dir):
        plugins_dir = plugins_path

    for plugin_name in os.listdir(plugins_dir):
        plugin_path = os.path.join(plugins_dir, plugin_name)
        if not os.path.isdir(plugin_path):
            continue

        skills_dir = os.path.join(plugin_path, 'skills')
        if not os.path.exists(skills_dir):
            continue

        for skill_name in os.listdir(skills_dir):
            skill_path = os.path.join(skills_dir, skill_name)
            skill_md = os.path.join(skill_path, 'SKILL.md')

            if os.path.exists(skill_md):
                try:
                    with open(skill_md, 'r', encoding='utf-8') as f:
                        content = f.read()
                    frontmatter = parse_frontmatter(content)
                    skills.append({
                        'name': skill_name,
                        'plugin': plugin_name,
                        'path': skill_path,
                        'frontmatter': frontmatter,
                        'lines': len(content.split('\n'))
                    })
                except Exception:
                    skills.append({
                        'name': skill_name,
                        'plugin': plugin_name,
                        'path': skill_path,
                        'frontmatter': None,
                        'lines': 0
                    })

    return skills


def list_skills(plugins_path):
    """List all skills."""
    skills = find_skills(plugins_path)

    if not skills:
        print("No skills found.")
        return

    print("\n## Available Skills\n")
    print("| Plugin | Skill | Description | Lines |")
    print("|--------|-------|-------------|-------|")

    for skill in sorted(skills, key=lambda x: (x['plugin'], x['name'])):
        plugin = skill['plugin']
        name = skill['name']
        lines = skill['lines']

        desc = ''
        if skill['frontmatter'] and 'description' in skill['frontmatter']:
            desc = skill['frontmatter']['description'][:50]
            if len(skill['frontmatter']['description']) > 50:
                desc += '...'

        print(f"| {plugin} | {name} | {desc} | {lines} |")

    print(f"\nTotal: {len(skills)} skills")


def search_skills(keyword, plugins_path):
    """Search skills by keyword."""
    skills = find_skills(plugins_path)
    keyword_lower = keyword.lower()

    matches = []
    for skill in skills:
        # Search in name
        if keyword_lower in skill['name'].lower():
            matches.append(skill)
            continue

        # Search in description
        if skill['frontmatter'] and 'description' in skill['frontmatter']:
            if keyword_lower in skill['frontmatter']['description'].lower():
                matches.append(skill)

    if not matches:
        print(f"No skills found matching '{keyword}'")
        return

    print(f"\n## Skills matching '{keyword}'\n")
    for skill in matches:
        print(f"**{skill['plugin']}/{skill['name']}**")
        print(f"  Path: {skill['path']}")
        if skill['frontmatter'] and 'description' in skill['frontmatter']:
            desc = skill['frontmatter']['description'][:100]
            print(f"  Description: {desc}...")
        print()


def show_skill_info(skill_path):
    """Show detailed information about a skill."""
    if not os.path.exists(skill_path):
        print(f"Error: Path not found: {skill_path}")
        return

    skill_md = os.path.join(skill_path, 'SKILL.md')
    if not os.path.exists(skill_md):
        print(f"Error: SKILL.md not found in {skill_path}")
        return

    skill_name = os.path.basename(skill_path)

    try:
        with open(skill_md, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading SKILL.md: {e}")
        return

    frontmatter = parse_frontmatter(content)
    lines = len(content.split('\n'))

    print(f"\n{'='*50}")
    print(f"Skill: {skill_name}")
    print(f"{'='*50}\n")

    if frontmatter:
        if 'name' in frontmatter:
            print(f"Name: {frontmatter['name']}")
        if 'description' in frontmatter:
            print(f"Description:\n  {frontmatter['description'][:200]}")
            if len(frontmatter['description']) > 200:
                print("  ...")
    else:
        print("Warning: No valid frontmatter found")

    print(f"\nSKILL.md: {lines} lines")

    # List files
    print("\nFiles:")
    for root, dirs, files in os.walk(skill_path):
        rel_root = os.path.relpath(root, skill_path)
        if rel_root == '.':
            rel_root = ''

        for f in files:
            if rel_root:
                print(f"  {rel_root}/{f}")
            else:
                print(f"  {f}")

    # Count by type
    scripts_path = os.path.join(skill_path, 'scripts')
    refs_path = os.path.join(skill_path, 'references')
    assets_path = os.path.join(skill_path, 'assets')

    print("\nResource counts:")
    if os.path.exists(scripts_path):
        count = len([f for f in os.listdir(scripts_path) if os.path.isfile(os.path.join(scripts_path, f))])
        print(f"  scripts/: {count} file(s)")
    if os.path.exists(refs_path):
        count = len([f for f in os.listdir(refs_path) if os.path.isfile(os.path.join(refs_path, f))])
        print(f"  references/: {count} file(s)")
    if os.path.exists(assets_path):
        count = len([f for f in os.listdir(assets_path) if os.path.isfile(os.path.join(assets_path, f))])
        print(f"  assets/: {count} file(s)")


def main():
    parser = argparse.ArgumentParser(description='Skill management utilities')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # List command
    list_parser = subparsers.add_parser('list', help='List all skills')
    list_parser.add_argument('--path', default=None, help='Plugins directory path')

    # Search command
    search_parser = subparsers.add_parser('search', help='Search skills by keyword')
    search_parser.add_argument('keyword', help='Keyword to search for')
    search_parser.add_argument('--path', default=None, help='Plugins directory path')

    # Info command
    info_parser = subparsers.add_parser('info', help='Show skill information')
    info_parser.add_argument('skill_path', help='Path to skill directory')

    args = parser.parse_args()

    if args.command == 'list':
        path = args.path or get_default_plugins_path()
        list_skills(path)
    elif args.command == 'search':
        path = args.path or get_default_plugins_path()
        search_skills(args.keyword, path)
    elif args.command == 'info':
        show_skill_info(args.skill_path)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
