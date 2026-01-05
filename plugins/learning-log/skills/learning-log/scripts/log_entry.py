#!/usr/bin/env python3
"""
Log an entry to the learning log file.

Usage:
    python log_entry.py <category> <message> [--log-file <path>]

Categories:
    メモ, 学習, 気づき, 問題
"""

import argparse
from datetime import datetime
import os
import sys


def log_entry(category: str, message: str, log_file: str = "docs/learning_log.md"):
    """
    Add an entry to the learning log.

    Args:
        category: The category of the entry (メモ, 学習, 気づき, 問題)
        message: The message content
        log_file: Path to the learning log file (relative to project root)
    """
    # Get current timestamp
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M")

    # Format entry
    entry = f"\n### {date_str} {time_str} - {category}\n{message}\n"

    # Ensure the file exists
    if not os.path.exists(log_file):
        # Create directory if needed
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        # Create initial file
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write("# Learning Log\n\n## エントリー\n\n<!-- 以下に自動的にエントリーが追加されます -->\n")

    # Append entry
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(entry)

    print(f"✅ Logged to {log_file}")
    print(f"   Category: {category}")
    print(f"   Time: {date_str} {time_str}")


def main():
    parser = argparse.ArgumentParser(description="Log an entry to the learning log")
    parser.add_argument("category", help="Entry category (メモ, 学習, 気づき, 問題)")
    parser.add_argument("message", help="Entry message content")
    parser.add_argument("--log-file", default="docs/learning_log.md",
                        help="Path to learning log file (default: docs/learning_log.md)")

    args = parser.parse_args()

    # Validate category
    valid_categories = ["メモ", "学習", "気づき", "問題"]
    if args.category not in valid_categories:
        print(f"❌ Invalid category: {args.category}", file=sys.stderr)
        print(f"   Valid categories: {', '.join(valid_categories)}", file=sys.stderr)
        sys.exit(1)

    log_entry(args.category, args.message, args.log_file)


if __name__ == "__main__":
    main()
