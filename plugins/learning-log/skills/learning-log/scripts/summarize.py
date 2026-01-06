#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Summarize learning log entries into structured documents.

This script reads entries from the learning log and provides utilities
for creating summaries by topic, time period, or custom criteria.

Usage:
    python summarize.py [--log-file <path>] [--output <path>] [--format <format>]
"""

import argparse
from datetime import datetime
import os
import sys
import re
import io
from collections import defaultdict

# Force UTF-8 encoding for stdout/stderr on Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class LogEntry:
    """Represents a single learning log entry."""

    def __init__(self, timestamp, category, content, supplement=None, references=None):
        self.timestamp = timestamp
        self.category = category
        self.content = content
        self.supplement = supplement
        self.references = references


def parse_log_file(log_file: str):
    """
    Parse the learning log file and extract entries.

    Args:
        log_file: Path to the learning log file

    Returns:
        List of LogEntry objects
    """
    if not os.path.exists(log_file):
        return []

    entries = []
    current_entry = None

    with open(log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].rstrip()

        # Match entry header: ### YYYY-MM-DD HH:MM - カテゴリ
        header_match = re.match(r'^### (\d{4}-\d{2}-\d{2} \d{2}:\d{2}) - (.+)$', line)
        if header_match:
            # Save previous entry if exists
            if current_entry:
                entries.append(current_entry)

            timestamp_str = header_match.group(1)
            category = header_match.group(2)
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M")

            # Get content (next line)
            i += 1
            content = lines[i].rstrip() if i < len(lines) else ""

            current_entry = {
                'timestamp': timestamp,
                'category': category,
                'content': content,
                'supplement': None,
                'references': None
            }

        # Match AI supplement
        elif line.startswith('**🤖 AI補足'):
            i += 1
            supplement_lines = []
            while i < len(lines) and not lines[i].startswith('>') and not lines[i].startswith('###'):
                supplement_lines.append(lines[i].rstrip())
                i += 1
            if current_entry:
                current_entry['supplement'] = '\n'.join(supplement_lines).strip()
            i -= 1  # Back up one line

        # Match references
        elif line.startswith('> 📚 参照:'):
            i += 1
            ref_lines = []
            while i < len(lines) and lines[i].startswith('>'):
                ref_lines.append(lines[i].lstrip('> ').rstrip())
                i += 1
            if current_entry:
                current_entry['references'] = '\n'.join(ref_lines).strip()
            i -= 1  # Back up one line

        i += 1

    # Add last entry
    if current_entry:
        entries.append(current_entry)

    return [LogEntry(**e) for e in entries]


def display_entries(entries, title="📝 ログエントリー"):
    """
    Display entries in a formatted way.

    Args:
        entries: List of LogEntry objects
        title: Display title
    """
    print(f"\n{'='*60}")
    print(f"{title} ({len(entries)}件)")
    print(f"{'='*60}\n")

    for i, entry in enumerate(entries, 1):
        print(f"{i}. [{entry.category}] {entry.timestamp.strftime('%Y-%m-%d %H:%M')}")
        print(f"   {entry.content}")
        if entry.supplement:
            print(f"   💡 補足: {entry.supplement[:100]}...")
        print()


def group_by_category(entries):
    """Group entries by category."""
    groups = defaultdict(list)
    for entry in entries:
        groups[entry.category].append(entry)
    return dict(groups)


def group_by_date(entries, granularity='day'):
    """
    Group entries by time period.

    Args:
        entries: List of LogEntry objects
        granularity: 'day', 'week', or 'month'
    """
    groups = defaultdict(list)

    for entry in entries:
        if granularity == 'day':
            key = entry.timestamp.strftime('%Y-%m-%d')
        elif granularity == 'week':
            key = entry.timestamp.strftime('%Y-W%W')
        elif granularity == 'month':
            key = entry.timestamp.strftime('%Y-%m')
        else:
            key = entry.timestamp.strftime('%Y-%m-%d')

        groups[key].append(entry)

    return dict(groups)


def main():
    parser = argparse.ArgumentParser(description="Summarize learning log entries")
    parser.add_argument("--log-file", default="docs/learning_log.md",
                        help="Path to learning log file (default: docs/learning_log.md)")
    parser.add_argument("--list", action="store_true",
                        help="List all entries")
    parser.add_argument("--by-category", action="store_true",
                        help="Group by category")
    parser.add_argument("--by-date", choices=['day', 'week', 'month'],
                        help="Group by time period")

    args = parser.parse_args()

    # Parse log file
    entries = parse_log_file(args.log_file)

    if not entries:
        print("❌ ログエントリーが見つかりませんでした")
        return

    if args.list:
        display_entries(entries)
    elif args.by_category:
        groups = group_by_category(entries)
        for category, cat_entries in groups.items():
            display_entries(cat_entries, f"📂 {category}")
    elif args.by_date:
        groups = group_by_date(entries, args.by_date)
        for period, period_entries in sorted(groups.items()):
            display_entries(period_entries, f"📅 {period}")
    else:
        # Default: show summary stats
        print(f"\n📊 学習ログサマリー")
        print(f"{'='*60}")
        print(f"総エントリー数: {len(entries)}")
        print(f"期間: {entries[0].timestamp.strftime('%Y-%m-%d')} 〜 {entries[-1].timestamp.strftime('%Y-%m-%d')}")
        print(f"\nカテゴリ別:")
        groups = group_by_category(entries)
        for category, cat_entries in groups.items():
            print(f"  {category}: {len(cat_entries)}件")


if __name__ == "__main__":
    main()
