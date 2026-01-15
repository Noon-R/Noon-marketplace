#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validate a skill's structure and contents.

Usage:
    python validate_skill.py <skill-path>
    python validate_skill.py plugins/dev-workflow/skills/coding-standards
"""

import argparse
import os
import sys
import io
import re

# Windows UTF-8 support
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


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
            # Continuation of multiline value
            current_value.append(line.strip())
        elif ':' in line:
            # Save previous key-value
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

    # Save last key-value
    if current_key:
        frontmatter[current_key] = '\n'.join(current_value).strip()

    return frontmatter


def validate_skill(skill_path):
    """
    Validate a skill directory structure.

    Returns:
        tuple: (is_valid, errors, warnings)
    """
    errors = []
    warnings = []

    # Check if path exists
    if not os.path.exists(skill_path):
        errors.append(f"Skill path does not exist: {skill_path}")
        return False, errors, warnings

    if not os.path.isdir(skill_path):
        errors.append(f"Path is not a directory: {skill_path}")
        return False, errors, warnings

    # Check SKILL.md exists
    skill_md_path = os.path.join(skill_path, 'SKILL.md')
    if not os.path.exists(skill_md_path):
        errors.append("SKILL.md not found")
        return False, errors, warnings

    # Read and parse SKILL.md
    try:
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        errors.append(f"Failed to read SKILL.md: {e}")
        return False, errors, warnings

    # Validate frontmatter
    frontmatter = parse_frontmatter(content)
    if frontmatter is None:
        errors.append("SKILL.md missing YAML frontmatter (must start with ---)")
    else:
        # Check required fields
        if 'name' not in frontmatter:
            errors.append("Frontmatter missing required field: name")
        elif not frontmatter['name']:
            errors.append("Frontmatter 'name' is empty")

        if 'description' not in frontmatter:
            errors.append("Frontmatter missing required field: description")
        elif not frontmatter['description']:
            errors.append("Frontmatter 'description' is empty")
        elif len(frontmatter['description']) < 20:
            warnings.append("Description is very short (< 20 chars). Consider adding more detail and trigger keywords.")

    # Check line count
    line_count = len(content.split('\n'))
    if line_count > 500:
        warnings.append(f"SKILL.md has {line_count} lines (recommended: < 500). Consider moving content to references/")

    # Check optional directories
    scripts_path = os.path.join(skill_path, 'scripts')
    if os.path.exists(scripts_path):
        if not os.listdir(scripts_path):
            warnings.append("scripts/ directory is empty")
        else:
            # Check Python files for UTF-8 encoding
            for f in os.listdir(scripts_path):
                if f.endswith('.py'):
                    py_path = os.path.join(scripts_path, f)
                    try:
                        with open(py_path, 'r', encoding='utf-8') as pf:
                            py_content = pf.read()
                        if 'encoding' not in py_content and 'utf-8' not in py_content.lower():
                            warnings.append(f"scripts/{f}: Consider adding UTF-8 encoding declaration")
                    except Exception:
                        pass

    refs_path = os.path.join(skill_path, 'references')
    if os.path.exists(refs_path) and not os.listdir(refs_path):
        warnings.append("references/ directory is empty")

    assets_path = os.path.join(skill_path, 'assets')
    if os.path.exists(assets_path) and not os.listdir(assets_path):
        warnings.append("assets/ directory is empty")

    is_valid = len(errors) == 0
    return is_valid, errors, warnings


def print_result(skill_path, is_valid, errors, warnings):
    """Print validation results."""
    skill_name = os.path.basename(skill_path)
    print(f"\n{'='*50}")
    print(f"Validation: {skill_name}")
    print(f"{'='*50}\n")

    if errors:
        print("Errors:")
        for error in errors:
            print(f"  ✗ {error}")
        print()

    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"  ⚠ {warning}")
        print()

    if is_valid:
        if warnings:
            print(f"✓ Validation PASSED with {len(warnings)} warning(s)")
        else:
            print("✓ Validation PASSED")
    else:
        print(f"✗ Validation FAILED with {len(errors)} error(s)")

    return is_valid


def main():
    parser = argparse.ArgumentParser(description='Validate a skill structure')
    parser.add_argument('skill_path', help='Path to the skill directory')

    args = parser.parse_args()

    is_valid, errors, warnings = validate_skill(args.skill_path)
    print_result(args.skill_path, is_valid, errors, warnings)

    sys.exit(0 if is_valid else 1)


if __name__ == '__main__':
    main()
