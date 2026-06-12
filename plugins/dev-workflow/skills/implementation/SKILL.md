---
name: implementation
description: |
  Execute implementation based on a design document, in the main thread.
  Use when user wants to implement code interactively based on a design. For autonomous workflow execution, implementation-workflow uses the implementer agent instead.
  Triggers include "実装して", "コードを書いて", "implement this", "この設計で実装".
  Reads design from file or direct input, loads the knowledge pack progressively, produces working code.
---

Execute implementation based on design documents, interactively in the main thread.

> **Note:** implementation-workflowから呼ばれる場合は、このスキルではなく**implementer agent**が使われる。このスキルはスタンドアロンで対話的に実装したいケース向け。

## Workflow Overview

1. **Design Input**: Receive and validate design document
2. **Implementation Execution**: Write code following design and knowledge pack
3. **Output Generation**: Produce implementation files and summary

## Input Modes

- **File Reference**: Path to design document (`{prefix}_design_output.md`) — extract DESIGN_OUTPUT section
- **Direct Input**: Design content in chat — parse and confirm understanding
- **Workflow Integration**: Design path from workflow context

---

## Stage 1: Design Input

### Design Validation

Check the design document contains: module/class structure, interface definitions, data flow, design decisions, knowledge pack specification. If missing critical information, ask clarifying questions before proceeding.

### Load Knowledge Pack（段階ロード）

設計書の「Knowledge Pack」セクションのパックキーを使い、code-knowledgeスキルの構造からロードする:

1. `references/{pack}/metadata.json` — ファイルパスとセクション索引
2. `references/{pack}/core.md` — **絶対遵守の制約**
3. 書くコードの種類に合うゴールデンサンプル（`examples/`）

詳細セクション（`sections/*.md`）は**実装中に疑問が生じたときだけ**読む。全文の先読みはしない。

パック指定が設計書にない場合: `scripts/list_knowledge.py` で一覧を提示し、ユーザーに選択を求める。該当なしなら一般的なベストプラクティスで進める。

### Pre-Implementation Checklist

Confirm with user: target directory / language・framework (if not in design) / knowledge pack / existing files to integrate with.

---

## Stage 2: Implementation Execution

1. **Start with structure**: File/folder structure first
2. **Core interfaces**: Public interfaces/APIs
3. **Internal logic**: Implementation details
4. **Error handling**: core.mdの流儀に従う（例: Unityなら例外でなく戻り値）
5. **Integration points**: Connect with existing code

迷ったらゴールデンサンプルの書き方に合わせる。設計との乖離は逐次記録する。

**General defaults**（パックがない場合）: clear naming, single responsibility, minimal comments, explicit error handling, idiomatic patterns for the target language.

---

## Stage 3: Output Generation

### Self-Verification

完了前に: core.md制約への違反をGrepで確認（例: `using System.Linq` / `catch`）。ビルド可能なら実行して確認。

### Implementation Summary

```markdown
<!-- IMPLEMENTATION_OUTPUT -->
# Implementation: {Feature Name}

## Applied Knowledge Pack
- Pack: {pack key} (core.md + {使用したサンプル/セクション})

## Files Created
| File | Purpose |
|------|---------|

## Implementation Summary
{description}

## Key Components
{location / purpose / key methods per component}

## Deviations from Design
| Item | Deviation | Reason |
（なければ "None - implemented as designed"）

## Self-Verification
- Constraint check: {結果}
- Build/Compile: {結果}

## Dependencies Added
（なければ "None"）

## Usage Example
{example code}

## Next Steps
- Verification items, integration tasks
<!-- /IMPLEMENTATION_OUTPUT -->
```

### File Output

- **Standalone**: Suggest `{prefix}_implementation_output.md`（設計書と同じprefix）
- **Workflow**: Output to the specified path

## Error Handling During Implementation

1. **Design ambiguity**: Ask user for clarification
2. **Technical constraint**: Propose alternative approach
3. **Scope creep**: Note as deviation and confirm with user
