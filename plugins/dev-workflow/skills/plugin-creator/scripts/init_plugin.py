#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plugin Initializer - Creates a new plugin directory structure.

Usage:
    python init_plugin.py <plugin-name> --path <plugins-dir>
    python init_plugin.py my-plugin --path ./plugins
    python init_plugin.py my-plugin --path ./plugins --description "My plugin description"
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


PLUGIN_JSON_TEMPLATE = {
    "name": "",
    "description": "",
    "version": "1.0.0",
    "skills": "./skills/"
}


def validate_plugin_name(name):
    """Validate plugin name format."""
    import re
    if not re.match(r'^[a-z][a-z0-9-]*$', name):
        return False, "Plugin name must be lowercase, start with letter, use only letters, numbers, and hyphens"
    if len(name) > 40:
        return False, "Plugin name must be 40 characters or less"
    if '--' in name:
        return False, "Plugin name cannot contain consecutive hyphens"
    return True, None


def init_plugin(plugin_name, plugins_path, description=None):
    """
    Initialize a new plugin directory structure.

    Args:
        plugin_name: Name of the plugin
        plugins_path: Path to the plugins directory
        description: Optional plugin description

    Returns:
        Path to created plugin directory, or None if error
    """
    # Validate plugin name
    is_valid, error = validate_plugin_name(plugin_name)
    if not is_valid:
        print(f"Error: {error}")
        return None

    # Determine plugin directory path
    plugin_dir = os.path.join(os.path.abspath(plugins_path), plugin_name)

    # Check if directory already exists
    if os.path.exists(plugin_dir):
        print(f"Error: Plugin directory already exists: {plugin_dir}")
        return None

    # Create directory structure
    try:
        # Main plugin directory
        os.makedirs(plugin_dir)
        print(f"Created: {plugin_dir}/")

        # .claude-plugin directory
        claude_plugin_dir = os.path.join(plugin_dir, '.claude-plugin')
        os.makedirs(claude_plugin_dir)
        print(f"Created: {claude_plugin_dir}/")

        # skills directory
        skills_dir = os.path.join(plugin_dir, 'skills')
        os.makedirs(skills_dir)
        print(f"Created: {skills_dir}/")

    except Exception as e:
        print(f"Error creating directories: {e}")
        return None

    # Create plugin.json
    plugin_json = PLUGIN_JSON_TEMPLATE.copy()
    plugin_json['name'] = plugin_name
    plugin_json['description'] = description or f"{plugin_name} plugin"

    plugin_json_path = os.path.join(claude_plugin_dir, 'plugin.json')
    try:
        with open(plugin_json_path, 'w', encoding='utf-8') as f:
            json.dump(plugin_json, f, ensure_ascii=False, indent=2)
        print(f"Created: {plugin_json_path}")
    except Exception as e:
        print(f"Error creating plugin.json: {e}")
        return None

    # Print summary
    print(f"\n{'='*50}")
    print(f"Plugin '{plugin_name}' created successfully!")
    print(f"{'='*50}")
    print(f"\nLocation: {plugin_dir}")
    print(f"\nStructure:")
    print(f"  {plugin_name}/")
    print(f"  ├── .claude-plugin/")
    print(f"  │   └── plugin.json")
    print(f"  └── skills/")

    print(f"\nNext steps:")
    print(f"  1. Add skills to {skills_dir}/")
    print(f"  2. Register in marketplace.json:")
    print(f"     python scripts/register_plugin.py {plugin_name}")
    print(f"  3. Install plugin: /plugin in Claude Code")

    return plugin_dir


def main():
    parser = argparse.ArgumentParser(description='Initialize a new plugin')
    parser.add_argument('plugin_name', help='Name of the plugin (lowercase, hyphen-separated)')
    parser.add_argument('--path', required=True, help='Path to plugins directory')
    parser.add_argument('--description', '-d', help='Plugin description')

    args = parser.parse_args()

    print(f"Initializing plugin: {args.plugin_name}")
    print(f"Location: {args.path}")
    print()

    result = init_plugin(args.plugin_name, args.path, args.description)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
