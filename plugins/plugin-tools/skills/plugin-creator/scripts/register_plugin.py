#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Register a plugin to marketplace.json.

Usage:
    python register_plugin.py <plugin-name> [--marketplace <path>]
    python register_plugin.py my-plugin --marketplace ./.claude-plugin/marketplace.json
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


def get_default_marketplace_path():
    """Get the default marketplace.json path."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Navigate up to project root
    root_path = os.path.join(script_dir, '..', '..', '..', '..', '..')
    marketplace_path = os.path.join(root_path, '.claude-plugin', 'marketplace.json')
    return os.path.normpath(marketplace_path)


def load_marketplace(marketplace_path):
    """Load marketplace.json."""
    if not os.path.exists(marketplace_path):
        return None, f"Marketplace file not found: {marketplace_path}"

    try:
        with open(marketplace_path, 'r', encoding='utf-8') as f:
            return json.load(f), None
    except json.JSONDecodeError as e:
        return None, f"Invalid JSON in marketplace file: {e}"
    except Exception as e:
        return None, f"Error reading marketplace file: {e}"


def save_marketplace(marketplace_path, data):
    """Save marketplace.json."""
    try:
        with open(marketplace_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True, None
    except Exception as e:
        return False, f"Error writing marketplace file: {e}"


def find_plugin_info(plugin_name, plugins_path):
    """Find plugin information from its plugin.json."""
    plugin_dir = os.path.join(plugins_path, plugin_name)

    if not os.path.exists(plugin_dir):
        return None, f"Plugin directory not found: {plugin_dir}"

    plugin_json_path = os.path.join(plugin_dir, '.claude-plugin', 'plugin.json')

    if not os.path.exists(plugin_json_path):
        return None, f"plugin.json not found: {plugin_json_path}"

    try:
        with open(plugin_json_path, 'r', encoding='utf-8') as f:
            plugin_info = json.load(f)
        return plugin_info, None
    except Exception as e:
        return None, f"Error reading plugin.json: {e}"


def register_plugin(plugin_name, marketplace_path, plugins_path=None):
    """
    Register a plugin to marketplace.json.

    Args:
        plugin_name: Name of the plugin to register
        marketplace_path: Path to marketplace.json
        plugins_path: Path to plugins directory (auto-detected if None)

    Returns:
        tuple: (success, message)
    """
    # Load marketplace
    marketplace, error = load_marketplace(marketplace_path)
    if error:
        return False, error

    # Auto-detect plugins path
    if plugins_path is None:
        marketplace_dir = os.path.dirname(os.path.dirname(marketplace_path))
        plugins_path = os.path.join(marketplace_dir, 'plugins')

    # Find plugin info
    plugin_info, error = find_plugin_info(plugin_name, plugins_path)
    if error:
        return False, error

    # Check if already registered
    plugins = marketplace.get('plugins', [])
    for existing in plugins:
        if existing.get('name') == plugin_name:
            return False, f"Plugin '{plugin_name}' is already registered"

    # Create plugin entry
    plugin_entry = {
        "name": plugin_name,
        "source": f"./plugins/{plugin_name}",
        "description": plugin_info.get('description', ''),
        "version": plugin_info.get('version', '1.0.0')
    }

    # Add to marketplace
    plugins.append(plugin_entry)
    marketplace['plugins'] = plugins

    # Save marketplace
    success, error = save_marketplace(marketplace_path, marketplace)
    if not success:
        return False, error

    return True, f"Plugin '{plugin_name}' registered successfully"


def unregister_plugin(plugin_name, marketplace_path):
    """
    Remove a plugin from marketplace.json.

    Args:
        plugin_name: Name of the plugin to remove
        marketplace_path: Path to marketplace.json

    Returns:
        tuple: (success, message)
    """
    # Load marketplace
    marketplace, error = load_marketplace(marketplace_path)
    if error:
        return False, error

    # Find and remove plugin
    plugins = marketplace.get('plugins', [])
    original_count = len(plugins)

    plugins = [p for p in plugins if p.get('name') != plugin_name]

    if len(plugins) == original_count:
        return False, f"Plugin '{plugin_name}' not found in marketplace"

    marketplace['plugins'] = plugins

    # Save marketplace
    success, error = save_marketplace(marketplace_path, marketplace)
    if not success:
        return False, error

    return True, f"Plugin '{plugin_name}' unregistered successfully"


def list_registered_plugins(marketplace_path):
    """List all registered plugins."""
    marketplace, error = load_marketplace(marketplace_path)
    if error:
        print(f"Error: {error}")
        return

    plugins = marketplace.get('plugins', [])

    if not plugins:
        print("No plugins registered.")
        return

    print("\n## Registered Plugins\n")
    print("| Name | Version | Description |")
    print("|------|---------|-------------|")

    for plugin in plugins:
        name = plugin.get('name', 'unknown')
        version = plugin.get('version', '-')
        desc = plugin.get('description', '')[:40]
        if len(plugin.get('description', '')) > 40:
            desc += '...'
        print(f"| {name} | {version} | {desc} |")

    print(f"\nTotal: {len(plugins)} plugin(s)")


def main():
    parser = argparse.ArgumentParser(description='Register/unregister plugins to marketplace')
    parser.add_argument('plugin_name', nargs='?', help='Name of the plugin')
    parser.add_argument('--marketplace', '-m', default=None,
                        help='Path to marketplace.json')
    parser.add_argument('--unregister', '-u', action='store_true',
                        help='Unregister the plugin instead of registering')
    parser.add_argument('--list', '-l', action='store_true',
                        help='List all registered plugins')

    args = parser.parse_args()

    marketplace_path = args.marketplace or get_default_marketplace_path()

    if args.list:
        list_registered_plugins(marketplace_path)
        return

    if not args.plugin_name:
        parser.print_help()
        return

    if args.unregister:
        success, message = unregister_plugin(args.plugin_name, marketplace_path)
    else:
        success, message = register_plugin(args.plugin_name, marketplace_path)

    if success:
        print(f"Success: {message}")
    else:
        print(f"Error: {message}")
        sys.exit(1)


if __name__ == '__main__':
    main()
