#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ファイルからハイパーリンクを抽出し、集約ファイルへ追記するコアモジュール。

対応フォーマット:
  - Markdown リンク: [テキスト](URL)
  - 参照スタイル Markdown: [テキスト][id] + [id]: URL
  - 裸の URL: https?://...
  - HTML アンカー: <a href="URL">
"""

import re
import os
import sys
import io
from datetime import datetime
from pathlib import Path
from typing import NamedTuple

# Windows での UTF-8 対応
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class LinkEntry(NamedTuple):
    url: str
    text: str       # リンクテキスト（空の場合は URL そのもの）
    line_no: int    # 元ファイルの行番号


# --- 正規表現パターン ---

# [テキスト](URL) 形式の Markdown リンク
_RE_MD_INLINE = re.compile(
    r'\[([^\]]*)\]\((https?://[^\s\)]+)\)',
    re.IGNORECASE
)

# [id]: URL 形式の参照スタイル定義
_RE_MD_REF_DEF = re.compile(
    r'^\s*\[([^\]]+)\]:\s*(https?://\S+)',
    re.IGNORECASE | re.MULTILINE
)

# 裸の URL (http/https で始まる、前後が非 URL 文字)
_RE_BARE_URL = re.compile(
    r'(?<!\()\b(https?://[^\s\)\]\>\"\']+)',
    re.IGNORECASE
)

# HTML アンカータグ
_RE_HTML_HREF = re.compile(
    r'<a\s[^>]*href=["\']?(https?://[^\s"\'>\)]+)["\']?',
    re.IGNORECASE
)


def extract_links_from_text(text: str) -> list[LinkEntry]:
    """
    テキスト文字列からハイパーリンクを抽出して LinkEntry リストを返す。
    重複 URL は除外し、最初に現れた行番号を保持する。
    """
    seen_urls: dict[str, LinkEntry] = {}
    lines = text.splitlines()

    def add(url: str, text_label: str, line_no: int):
        url = url.rstrip('.,;:!?)')  # 末尾の句読点を除去
        if url and url not in seen_urls:
            seen_urls[url] = LinkEntry(url=url, text=text_label or url, line_no=line_no)

    # --- 行ごとに処理 ---
    for i, line in enumerate(lines, start=1):
        # Markdown インラインリンク
        for m in _RE_MD_INLINE.finditer(line):
            add(m.group(2), m.group(1), i)

        # HTML href
        for m in _RE_HTML_HREF.finditer(line):
            add(m.group(1), "", i)

    # --- 全文で参照スタイル定義を収集 ---
    for m in _RE_MD_REF_DEF.finditer(text):
        # 行番号を計算
        line_no = text[:m.start()].count('\n') + 1
        add(m.group(2), m.group(1), line_no)

    # --- 裸 URL（既に登録済みの URL は追加しない） ---
    for i, line in enumerate(lines, start=1):
        # 既に Markdown リンク内にある URL は除外するため、
        # Markdown リンクの URL 部分を空白に置換してから検索
        clean_line = _RE_MD_INLINE.sub(lambda m: ' ' * len(m.group(0)), line)
        clean_line = _RE_HTML_HREF.sub(lambda m: ' ' * len(m.group(0)), clean_line)
        for m in _RE_BARE_URL.finditer(clean_line):
            add(m.group(1), "", i)

    # 行番号順にソートして返す
    return sorted(seen_urls.values(), key=lambda e: e.line_no)


def extract_links_from_file(file_path: str) -> list[LinkEntry]:
    """ファイルを読み込んでハイパーリンクを抽出する。"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            text = f.read()
        return extract_links_from_text(text)
    except OSError:
        return []


def _load_existing_urls(aggregated_file: str) -> set[str]:
    """集約ファイルに既に記録されている URL セットを返す。"""
    existing: set[str] = set()
    if not os.path.exists(aggregated_file):
        return existing
    try:
        with open(aggregated_file, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        # 集約ファイル内の URL をすべて拾う
        for m in _RE_MD_INLINE.finditer(content):
            existing.add(m.group(2).rstrip('.,;:!?)'))
        for m in _RE_BARE_URL.finditer(content):
            existing.add(m.group(1).rstrip('.,;:!?)'))
    except OSError:
        pass
    return existing


def _ensure_aggregated_file(aggregated_file: str):
    """集約ファイルが存在しない場合、ヘッダー付きで新規作成する。"""
    if os.path.exists(aggregated_file):
        return
    os.makedirs(os.path.dirname(os.path.abspath(aggregated_file)), exist_ok=True)
    header = (
        "# Hyperlinks Index\n\n"
        "このファイルはプロジェクト内のドキュメントから自動収集されたハイパーリンクの集約ファイルです。\n"
        "`aggregate-hyperlinks` プラグインの PostToolUse フックにより自動生成・更新されます。\n\n"
        "---\n\n"
    )
    with open(aggregated_file, 'w', encoding='utf-8') as f:
        f.write(header)


def append_links_to_aggregated_file(
    links: list[LinkEntry],
    source_file: str,
    aggregated_file: str
) -> int:
    """
    新規リンクのみを集約ファイルへ追記する。

    Returns:
        追記した新規リンク件数
    """
    _ensure_aggregated_file(aggregated_file)
    existing_urls = _load_existing_urls(aggregated_file)

    new_links = [lnk for lnk in links if lnk.url not in existing_urls]
    if not new_links:
        return 0

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    # ソースファイルのパスを相対パスに変換（可能な場合）
    try:
        rel_source = os.path.relpath(
            source_file,
            os.path.dirname(os.path.abspath(aggregated_file))
        )
    except ValueError:
        rel_source = source_file

    block = f"\n## {rel_source}  _{now}_\n\n"
    for lnk in new_links:
        if lnk.text and lnk.text != lnk.url:
            block += f"- [{lnk.text}]({lnk.url})\n"
        else:
            block += f"- <{lnk.url}>\n"

    with open(aggregated_file, 'a', encoding='utf-8') as f:
        f.write(block)

    return len(new_links)
