---
name: learning-log
description: Automatically record learning notes and insights to a timestamped log file. Use this skill when the user's message contains keywords like "メモ:" (memo), "学習:" (learning), "気づき:" (insight), or "問題:" (problem). These keywords indicate the user wants to log their thoughts, learnings, or issues to docs/learning_log.md for later reference.
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

Immediately execute:

```bash
python scripts/log_entry.py "<category>" "<message content>" --log-file "docs/learning_log.md"
```

Where `<category>` is one of: `メモ`, `学習`, `気づき`, `問題`

## Workflow

1. **Detect keyword** in user message (メモ:, 学習:, 気づき:, 問題:)
2. **Extract category** from the keyword
3. **Extract message** (everything after the keyword)
4. **Execute script** using `scripts/log_entry.py`
5. **Confirm** briefly to the user (e.g., "✅ 記録しました")

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

## Implementation Notes

- **Silent execution**: Run the script quietly without asking for confirmation
- **Brief confirmation**: After logging, give a concise confirmation (e.g., "✅ 記録しました")
- **Continue conversation**: Don't let logging interrupt the conversation flow
- **File creation**: The script automatically creates `docs/learning_log.md` if it doesn't exist
- **Encoding**: Always use UTF-8 encoding to handle Japanese text properly
