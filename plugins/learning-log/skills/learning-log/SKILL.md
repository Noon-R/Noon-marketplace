---
name: learning-log
description: Automatically record learning notes and insights to a timestamped log file. Use this skill when the user's message contains keywords like "メモ:" (memo), "学習:" (learning), "気づき:" (insight), or "問題:" (problem). These keywords indicate the user wants to log their thoughts, learnings, or issues to docs/learning_log.md for later reference. Additionally, this skill can review logged entries and add AI-generated supplements with references.
---

# Learning Log

## Overview

Automatically capture and organize learning notes, insights, and observations during development work. When users prefix their messages with specific keywords, this skill logs the content to `docs/learning_log.md` with timestamps and categories.

## Quick Start

When you detect a message starting with one of these keywords:

- **メモ:** - General notes and observations
- **学習:** - Learning content and technical understanding
- **気づき:** - Insights and realizations
- **問題:** - Problems and questions encountered

Immediately execute these steps in sequence:

**Step 1 - Log the entry:**
```bash
python scripts/log_entry.py "<category>" "<message content>" --log-file "<current-project>/docs/learning_log.md"
```

**Step 2 - Perform web search for references:**
Use WebSearch tool to find relevant documentation or articles

**Step 3 - Add AI supplement with references:**
```bash
python scripts/review_and_supplement.py --supplement "<AI-generated context>" --reference "<references>" --log-file "<current-project>/docs/learning_log.md"
```

Where:
- `<category>` is one of: `メモ`, `学習`, `気づき`, `問題`
- `<current-project>` is the absolute path to the current project directory
- `<AI-generated context>` is your analysis with clarifications, best practices, or related concepts (2-3 sentences)
- **Reference materials (REQUIRED)**:
  - ALWAYS add `--reference "<ref>"` parameter
  - If specific web articles or documentation available: Include Markdown hyperlinks `[Title](URL)`
  - If no specific references available: Use `--reference "参照資料: 一般的な知識に基づく"`

## Workflow

1. **Detect keyword** in user message (メモ:, 学習:, 気づき:, 問題:)
2. **Extract category** from the keyword
3. **Extract message** (everything after the keyword)
4. **Execute log script** using `scripts/log_entry.py` with current project's absolute path
5. **Perform web search** to find relevant reference materials:
   - Use WebSearch tool with appropriate query based on the entry content
   - Look for official documentation, tutorials, or authoritative articles
   - Extract relevant URLs and titles from search results
6. **Analyze entry** and identify areas that need clarification or additional context
7. **Prepare AI supplement** with relevant technical context, best practices, or related concepts
8. **Prepare reference material** (REQUIRED):
   - If web search found relevant articles: Include as Markdown hyperlinks `[Title](URL)`
   - If no specific references found: Use "参照資料: 一般的な知識に基づく"
9. **Execute supplement script** using `scripts/review_and_supplement.py --supplement "<text>" --reference "<ref>"` (ALWAYS include --reference parameter)
10. **Confirm** briefly to the user (e.g., "✅ 記録しました（AI補足付き）")

## Categories

### メモ: (Memo)
General notes, observations, and quick thoughts that don't fit other categories.

**Example:**
```
User: メモ: DirectX 12のディスクリプタヒープは、リソースへのポインタのようなもの
→ Log to docs/learning_log.md under category "メモ"
```

### 学習: (Learning)
Technical learnings, understanding gained, and educational content.

**Example:**
```
User: 学習: コマンドリストは再利用可能で、コマンドアロケータはフレームごとに分ける必要がある
→ Log to docs/learning_log.md under category "学習"
```

### 気づき: (Insight)
Sudden realizations, aha moments, and important discoveries.

**Example:**
```
User: 気づき: リソースバリアはGPUの同期を制御するために必要
→ Log to docs/learning_log.md under category "気づき"
```

### 問題: (Problem)
Issues encountered, questions to investigate, or blockers.

**Example:**
```
User: 問題: デバイス作成時にD3D12CreateDeviceが失敗する
→ Log to docs/learning_log.md under category "問題"
```

## Script Usage

### log_entry.py

Adds a timestamped entry to the learning log.

**Parameters:**
- `category` (required): Entry category (メモ, 学習, 気づき, 問題)
- `message` (required): The content to log
- `--log-file` (optional): Path to log file (default: `docs/learning_log.md`)

**Example:**
```bash
python scripts/log_entry.py "メモ" "これはテストです" --log-file "docs/learning_log.md"
```

**Output format:**
```markdown
### 2026-01-04 15:09 - メモ
これはテストです
```

### review_and_supplement.py

Reviews the latest log entry and adds AI-generated supplements with optional references.

**Parameters:**
- `--log-file` (optional): Path to log file (default: `docs/learning_log.md`)
- `--supplement` (optional): AI supplement text to add
- `--reference` (optional): Temporary reference material
- `--review-only` (optional): Only display the latest entry without adding supplement

**Example - Review only:**
```bash
python scripts/review_and_supplement.py --review-only
```

**Example - Add supplement:**
```bash
python scripts/review_and_supplement.py --supplement "この手法は○○の場合に特に有効です" --reference "参照: 公式ドキュメント Section 3.2"
```

**Output format:**
```markdown
**🤖 AI補足 (15:30):**
この手法は○○の場合に特に有効です

> 📚 参照:
> [Article Title - Source Name](https://example.com/article-url)
```

**IMPORTANT**: When referencing web articles, ALWAYS use Markdown hyperlink format: `[Title](URL)`

## Implementation Notes

- **Current project path**: ALWAYS use the current project's absolute path for `--log-file` parameter
- **Web search for references**: ALWAYS perform web search before adding supplement
  - Use WebSearch tool with appropriate query based on entry content
  - Prioritize official documentation (Microsoft Docs, MDN, official API docs)
  - Look for recent and authoritative sources (2020+)
  - Extract 1-3 most relevant URLs with titles
- **Automatic AI supplement**: After logging an entry, ALWAYS add AI supplement with technical context
  - Provide clarifications, best practices, or related concepts
  - Keep supplement concise but informative (2-3 sentences)
- **Reference materials (REQUIRED)**: ALWAYS include --reference parameter
  - Use Markdown hyperlink format for web references: `[Title](URL)`
  - If web search found relevant articles, include them as hyperlinks
  - If no specific references found after search, use: `--reference "参照資料: 一般的な知識に基づく"`
  - **NEVER omit the --reference parameter**
- **Silent execution**: Run both scripts quietly without asking for confirmation
- **Brief confirmation**: After logging with supplement, give a concise confirmation (e.g., "✅ 記録しました（AI補足付き）")
- **Continue conversation**: Don't let logging interrupt the conversation flow
- **File creation**: The script automatically creates `docs/learning_log.md` if it doesn't exist
- **Encoding**: Always use UTF-8 encoding to handle Japanese text properly (Windows support included)

### AI Supplement Workflow

When a user requests review or supplement of a logged entry:

1. **Review**: Execute `review_and_supplement.py --review-only` to display the latest entry
2. **Analyze**: Read the entry and identify areas that need clarification or additional context
3. **Supplement**: If you have useful information to add:
   - Prepare supplement text explaining or clarifying the original entry
   - Include reference materials if applicable (documentation, code snippets, etc.)
   - Execute `review_and_supplement.py --supplement "<text>" --reference "<ref>"`
4. **Confirm**: Give brief confirmation with summary of what was added

**Example conversation:**
```
User: learning-logの利用時にメモ内容の確認をして補足したいことがあれば、記載してください

AI: 最新のエントリーを確認します。
[Executes: python scripts/review_and_supplement.py --review-only]

最新のメモは「DirectX 12のディスクリプタヒープは、リソースへのポインタのようなもの」ですね。

補足を追加します：
[Executes: python scripts/review_and_supplement.py --supplement "ディスクリプタヒープは、GPU側から見たリソースの配列と考えることができます。CPUのポインタと異なり、GPU側で直接インデックスアクセス可能な点が重要です。" --reference "参照: DirectX 12 Programming Guide - Descriptor Heaps (Microsoft Docs)"]

✅ AI補足を追加しました
```

**AI補足の識別:**
- すべてのAI生成補足は「🤖 AI補足」マーカーで明示
- タイムスタンプ付きで追加時刻を記録
- 参照資料は「📚 参照:」セクションに記載
- Web記事は必ずMarkdown形式のハイパーリンク（`[Title](URL)`）で記載
