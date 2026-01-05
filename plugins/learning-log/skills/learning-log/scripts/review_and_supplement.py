#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Review a log entry and add AI-generated supplements with temporary references.

This script reads the latest entry from the learning log, displays it for review,
and allows appending AI-generated supplements marked with 🤖 AI補足:.

Usage:
    python review_and_supplement.py [--log-file <path>] [--supplement <text>] [--reference <text>]
"""

import argparse
from datetime import datetime
import os
import sys
import re
import io

# Force UTF-8 encoding for stdout/stderr on Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def get_latest_entry(log_file: str):
    """
    Get the latest entry from the learning log.

    Args:
        log_file: Path to the learning log file

    Returns:
        Tuple of (category, content, timestamp) or None if no entries
    """
    if not os.path.exists(log_file):
        return None

    with open(log_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all entries (format: ### YYYY-MM-DD HH:MM - Category)
    pattern = r'### (\d{4}-\d{2}-\d{2} \d{2}:\d{2}) - (.+?)\n(.*?)(?=\n### |\Z)'
    matches = list(re.finditer(pattern, content, re.DOTALL))

    if not matches:
        return None

    # Get the latest entry (last match)
    latest = matches[-1]
    timestamp = latest.group(1)
    category = latest.group(2).strip()
    entry_content = latest.group(3).strip()

    return category, entry_content, timestamp


def add_supplement(log_file: str, supplement: str, reference: str = None):
    """
    Add an AI supplement to the latest entry.

    Args:
        log_file: Path to the learning log file
        supplement: The supplement content to add
        reference: Optional temporary reference material
    """
    if not os.path.exists(log_file):
        print("❌ Log file not found", file=sys.stderr)
        sys.exit(1)

    # Format supplement
    now = datetime.now()
    time_str = now.strftime("%H:%M")

    supplement_text = f"\n**🤖 AI補足 ({time_str}):**\n{supplement}\n"

    if reference:
        supplement_text += f"\n> 📚 参照:\n> {reference.replace(chr(10), chr(10) + '> ')}\n"

    # Append supplement
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(supplement_text)

    print(f"✅ AI補足を追加しました")
    print(f"   Time: {time_str}")


def display_entry(category: str, content: str, timestamp: str):
    """
    Display an entry for review.

    Args:
        category: Entry category
        content: Entry content
        timestamp: Entry timestamp
    """
    print("\n" + "="*60)
    print(f"📝 最新のエントリー")
    print("="*60)
    print(f"カテゴリ: {category}")
    print(f"時刻: {timestamp}")
    print("-"*60)
    print(content)
    print("="*60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Review and add AI supplements to learning log entries"
    )
    parser.add_argument(
        "--log-file",
        default="docs/learning_log.md",
        help="Path to learning log file (default: docs/learning_log.md)"
    )
    parser.add_argument(
        "--supplement",
        help="AI supplement text to add"
    )
    parser.add_argument(
        "--reference",
        help="Temporary reference material"
    )
    parser.add_argument(
        "--review-only",
        action="store_true",
        help="Only display the latest entry without adding supplement"
    )

    args = parser.parse_args()

    # Get latest entry
    result = get_latest_entry(args.log_file)

    if result is None:
        print("❌ No entries found in log file", file=sys.stderr)
        sys.exit(1)

    category, content, timestamp = result

    # Display entry
    display_entry(category, content, timestamp)

    # If review only, exit
    if args.review_only:
        print("ℹ️  レビューモード: 補足は追加されませんでした")
        return

    # Add supplement if provided
    if args.supplement:
        add_supplement(args.log_file, args.supplement, args.reference)
    else:
        print("ℹ️  補足が指定されていません。--supplement オプションを使用してください。")


if __name__ == "__main__":
    main()
