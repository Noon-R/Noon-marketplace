#!/usr/bin/env python3
"""Zenn記事の一覧表示・検索スクリプト。

Usage:
    python list_articles.py [--dir ZENN_CONTENT_DIR] [--search KEYWORD] [--status published|draft|all]
"""

import argparse
import os
import re
import sys
from pathlib import Path


def parse_frontmatter(filepath: Path) -> dict:
    """Markdownファイルのfront matterを解析する。"""
    content = filepath.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}

    fm = {}
    for line in match.group(1).split("\n"):
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            fm[key] = value
    return fm


def list_articles(zenn_dir: str, search: str = "", status: str = "all"):
    """記事一覧を表示する。"""
    articles_dir = Path(zenn_dir) / "articles"
    if not articles_dir.exists():
        print(f"Error: articles directory not found: {articles_dir}", file=sys.stderr)
        sys.exit(1)

    articles = []
    for md_file in sorted(articles_dir.glob("*.md")):
        fm = parse_frontmatter(md_file)
        title = fm.get("title", "(no title)")
        published = fm.get("published", "false")
        emoji = fm.get("emoji", "")
        article_type = fm.get("type", "")
        topics = fm.get("topics", "[]")

        # ステータスフィルタ
        if status == "published" and published != "true":
            continue
        if status == "draft" and published != "false":
            continue

        # 検索フィルタ
        if search and search.lower() not in title.lower() and search.lower() not in md_file.stem.lower():
            continue

        is_published = "published" if published == "true" else "draft"
        articles.append({
            "slug": md_file.stem,
            "title": title,
            "emoji": emoji,
            "type": article_type,
            "status": is_published,
            "topics": topics,
        })

    if not articles:
        print("No articles found.")
        return

    print(f"{'Slug':<30} {'Status':<10} {'Type':<6} {'Title'}")
    print("-" * 80)
    for a in articles:
        print(f"{a['slug']:<30} {a['status']:<10} {a['type']:<6} {a['emoji']} {a['title']}")

    print(f"\nTotal: {len(articles)} article(s)")


def main():
    parser = argparse.ArgumentParser(description="List Zenn articles")
    parser.add_argument("--dir", default="d:/0_Data/Developer/zenn-content",
                        help="Path to zenn-content directory")
    parser.add_argument("--search", default="", help="Search keyword")
    parser.add_argument("--status", choices=["published", "draft", "all"],
                        default="all", help="Filter by status")
    args = parser.parse_args()

    list_articles(args.dir, args.search, args.status)


if __name__ == "__main__":
    main()
