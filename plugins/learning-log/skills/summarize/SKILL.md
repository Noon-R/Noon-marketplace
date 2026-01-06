---
name: summarize
description: Create structured summaries from learning log entries through interactive dialogue. Use this skill when the user wants to organize, summarize, or review their learning log (e.g., "ログをまとめて", "今週の学習を整理", "学んだことを振り返りたい"). Supports topic-based and chronological organization.
---

# Learning Log Summarize

## Overview

Interactive skill for creating structured summaries from learning log entries. Works collaboratively with the user through dialogue to organize entries by topic or timeline, creating polished documents for review and reference.

## Quick Start

When you detect messages like:
- "ログをまとめて" / "まとめを作成"
- "今週/今月の学習を整理したい"
- "学んだことを振り返りたい"
- "トピック別にまとめて"

Start the interactive summarization workflow:

1. **Parse the log**: Use `summarize.py --list` to load all entries
2. **Discuss scope**: Ask user about time range, categories, topics of interest
3. **Propose structure**: Suggest organization (topic-based or chronological)
4. **Iterate**: Refine structure based on user feedback
5. **Generate summary**: Create the final document
6. **Save**: Output to `docs/summaries/` directory

## Workflow

### Phase 1: Scope Definition (対話開始)

1. **Load entries**: Execute `python ../learning-log/scripts/summarize.py --log-file "<project>/docs/learning_log.md" --list`
2. **Present overview**: Show total entries, date range, categories
3. **Ask user**:
   - "どの期間のログをまとめますか？（全期間/今週/今月/カスタム）"
   - "特定のカテゴリに絞りますか？（メモ/学習/気づき/問題/全て）"
   - "キーワードで絞り込みますか？"

### Phase 2: Structure Proposal (構造提案)

1. **Analyze entries**: Identify common topics/themes
2. **Propose organization**:
   - **トピック別**: Group similar entries by subject
   - **時系列**: Organize chronologically with context
3. **Show example structure**: Present outline for user approval
4. **Gather feedback**: Adjust based on user preferences

### Phase 3: Content Generation (コンテンツ生成)

1. **Create sections**: Build content for each section
2. **Include references**: Preserve links from AI supplements
3. **Add insights**: Provide connections between topics
4. **Format document**: Apply chosen format (Markdown report, Q&A, etc.)

### Phase 4: Review & Save (確認と保存)

1. **Present draft**: Show generated summary
2. **Iterate if needed**: Make adjustments based on feedback
3. **Save document**: Write to `docs/summaries/<timestamp>_summary.md`
4. **Confirm**: Provide file path and summary stats

## Output Formats

### トピック別まとめ

```markdown
# 学習まとめ: [期間]

## [トピック1: 例 DirectX 12]

### 主な学習内容
- エントリー1の要約
- エントリー2の要約

### 重要なポイント
- ポイント1
- ポイント2

### 参考資料
- [リンク1](URL)
- [リンク2](URL)

## [トピック2: 例 COM プログラミング]
...
```

### 時系列レポート

```markdown
# 学習レポート: [期間]

## Week 1 (YYYY-MM-DD 〜 YYYY-MM-DD)

### 学んだこと
- トピック別のサマリー

### 気づき
- 重要な洞察

### 参考資料
- まとめたリンク

## Week 2 (YYYY-MM-DD 〜 YYYY-MM-DD)
...
```

## Script Usage

### summarize.py

**List all entries:**
```bash
python summarize.py --log-file "docs/learning_log.md" --list
```

**Group by category:**
```bash
python summarize.py --log-file "docs/learning_log.md" --by-category
```

**Group by time period:**
```bash
python summarize.py --log-file "docs/learning_log.md" --by-date week
```

Options: `day`, `week`, `month`

## Implementation Notes

- **Interactive approach**: ALWAYS engage in dialogue with user at each phase
  - Don't make assumptions about scope or structure
  - Present options and ask for preferences
  - Show examples before generating full content

- **Preserve references**: Maintain all reference links from original entries
  - Extract URLs from AI supplements
  - Group related references by topic

- **Use absolute paths**: ALWAYS use current project's absolute path for file operations

- **Output location**: Save summaries to `docs/summaries/` directory
  - Create directory if it doesn't exist
  - Use timestamp in filename: `YYYYMMDD_HHMM_summary.md`

- **Natural language triggers**: Recognize variations:
  - "ログをまとめて", "まとめを作成して"
  - "整理したい", "振り返りたい"
  - "サマリーを作って", "レビューしたい"

- **Bilingual support**: Handle both Japanese and English naturally

## Example Dialogue

```
User: 今週のログをまとめたい

AI: 今週の学習ログをまとめますね。まず現在のログを確認します。
[Executes: python summarize.py --log-file "d:/project/docs/learning_log.md" --list]

今週は3件のエントリーがあります：
1. [メモ] IID_PPV_ARGSについて
2. [学習] DirectX 12の基礎
3. [気づき] COMの理解が深まった

まとめ方について相談させてください：

**質問1**: どの形式がお好みですか？
A) トピック別（DirectX、COMなど技術ごと）
B) 時系列（学習の流れを重視）

User: トピック別で

AI: 了解しました。エントリーを分析したところ、以下のトピックに分類できそうです：

## 提案する構成

### 1. COM プログラミング
   - IID_PPV_ARGSマクロ
   - COMの理解

### 2. DirectX 12
   - 基礎概念
   - COM との関連

この構成でよろしいですか？調整が必要な部分があればお知らせください。

User: いいですね

AI: ありがとうございます！では詳細なまとめを作成します...
[Generates structured summary document]

完成しました！以下に保存しました：
📄 docs/summaries/20260106_0800_summary.md

**概要**:
- トピック数: 2
- 総エントリー: 3件
- 参考資料: 5個のリンクを含む

ご確認ください！
```