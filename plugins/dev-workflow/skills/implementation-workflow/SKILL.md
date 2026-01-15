---
name: implementation-workflow
description: |
  Orchestrate the full implementation workflow from requirements to completion.
  Use when user wants to start a new implementation task with full workflow support, or manage an ongoing implementation.
  Triggers include "機能を作りたい", "新しい機能を作りたい", "implementation workflow", "ワークフロー開始", or explicit workflow management requests.
  Coordinates design-discussion, implementation, and behavior-verification skills with progress tracking and checkpoints.
---

Orchestrate the full implementation workflow. Manages progress through stages, coordinates between skills, and handles checkpoints with backups.

## Workflow Overview

This meta-skill coordinates 8 stages:

| Stage | Skill | Description |
|-------|-------|-------------|
| 1 | - | Receive implementation request |
| 2 | design-discussion | Design discussion and documentation |
| 3 | implementation | Code implementation |
| 4 | behavior-verification | Verification checklist and user testing |
| 4.5 | (user decision) | User confirms: proceed or revise |
| 5 | code-review | Code quality review (Phase 2) |
| 6 | code-commenting | Comment insertion (Phase 2) |
| 7 | logging-enhancement | Log embedding (Phase 2) |
| 8 | - | RELogVisualizer settings update (user) |

**Phase 1 scope:** Stages 1-4.5 (design → implementation → verification loop)

---

## Initialization

### Request Input

When user provides implementation request:

1. **Extract prefix** from request using simple logic:
   - Identify primary noun/concept
   - Convert to lowercase ASCII with underscores
   - Example: "ログイン機能の実装" → 'login'
   - Example: "Search API implementation" → 'search_api'

2. **Confirm prefix** with user:
   > プレフィックス「{prefix}」を使用します。この識別子でファイルを管理します。
   > 別のプレフィックスをご希望の場合はお知らせください。

3. **Create request directory**:

```
requests/{prefix}/
├── progress.md
├── {prefix}_design_output.md (created by design-discussion)
├── {prefix}_implementation_output.md (created by implementation)
├── {prefix}_verification_output.md (created by behavior-verification)
└── backup/
    └── {YYYYMMDD_HHMMSS}/
```

### Progress Document

Create `progress.md` with initial structure:

```markdown
# Implementation Progress: {Feature Name}

## Request
{Original request text}

## Prefix
{prefix}

## Current Stage
1 - Request Received

## Stage History

| Stage | Status | Timestamp | Notes |
|-------|--------|-----------|-------|
| 1 | ✓ Complete | {timestamp} | Request received |
| 2 | ○ Pending | | Design Discussion |
| 3 | ○ Pending | | Implementation |
| 4 | ○ Pending | | Behavior Verification |
| 5 | ○ Pending | | Code Review |
| 6 | ○ Pending | | Code Commenting |
| 7 | ○ Pending | | Logging Enhancement |

## Artifacts

| Stage | File | Status |
|-------|------|--------|
| Design | {prefix}_design_output.md | ○ |
| Implementation | {prefix}_implementation_output.md | ○ |
| Verification | {prefix}_verification_output.md | ○ |
| Code Review | {prefix}_code_review_output.md | ○ |
| Commented Code | {prefix}_commented_code_output.md | ○ |

## Checkpoints

| Checkpoint | Timestamp | Backup Path |
|------------|-----------|-------------|
| - | - | - |

## Issues Log
(Issues found during verification or review)
```

---

## Stage Transitions

### Stage 1 → 2: Start Design

After initialization:

1. Update progress.md: Stage 2 in progress
2. Invoke design-discussion skill with:
   - Request content
   - Output path: `requests/{prefix}/{prefix}_design_output.md`
3. After design complete, create checkpoint

### Stage 2 → 3: Start Implementation

After design complete:

1. **Create checkpoint**: Copy current artifacts to `backup/{timestamp}/`
2. Update progress.md: Stage 3 in progress
3. Invoke implementation skill with:
   - Design path: `requests/{prefix}/{prefix}_design_output.md`
   - Output path: `requests/{prefix}/{prefix}_implementation_output.md`
4. After implementation complete, create checkpoint

### Stage 3 → 4: Start Verification

After implementation complete:

1. **Create checkpoint**: Copy current artifacts to `backup/{timestamp}/`
2. Update progress.md: Stage 4 in progress
3. Invoke behavior-verification skill with:
   - Implementation path: `requests/{prefix}/{prefix}_implementation_output.md`
   - Output path: `requests/{prefix}/{prefix}_verification_output.md`
4. Wait for user response

### Stage 4.5: User Decision Point

Display decision prompt:

| 選択 | 説明 |
|------|------|
| **✓ 確認完了** | すべての項目が正常に動作しました。次の段階へ進みます。 |
| **✗ 修正が必要** | 問題が見つかりました。修正します。 |

**If "確認完了":**
1. Update progress.md: Stage 4 complete
2. Create checkpoint
3. Proceed to Stage 5 (code-review)

**If "修正が必要":**
1. Ask user to describe issues
2. Log issues in progress.md
3. Return to Stage 3 (implementation)
4. Pass issue context to implementation skill

### Stage 4.5 → 5: Start Code Review

After verification complete and user confirms:

1. **Create checkpoint**: Copy current artifacts to `backup/{timestamp}/`
2. Update progress.md: Stage 5 in progress
3. Invoke code-review skill with:
   - Implementation path: `requests/{prefix}/{prefix}_implementation_output.md`
   - Design path: `requests/{prefix}/{prefix}_design_output.md`
   - Output path: `requests/{prefix}/{prefix}_code_review_output.md`
4. Wait for review completion

### Stage 5.5: Review Decision Point

After code review, check review decision:

**If "Needs Revision" (Critical issues found):**
1. Display critical findings to user
2. Ask for confirmation to return to implementation
3. Log critical issues in progress.md
4. Return to Stage 3 (implementation)
5. Pass critical findings to implementation skill

**If "Approved with Comments" or "Approved":**
1. Update progress.md: Stage 5 complete
2. Create checkpoint
3. Proceed to Stage 6 (code-commenting)

### Stage 5 → 6: Start Code Commenting

After review approved:

1. **Create checkpoint**: Copy current artifacts to `backup/{timestamp}/`
2. Update progress.md: Stage 6 in progress
3. Invoke code-commenting skill with:
   - Implementation path: `requests/{prefix}/{prefix}_implementation_output.md`
   - Review path: `requests/{prefix}/{prefix}_code_review_output.md`
   - Output path: `requests/{prefix}/{prefix}_commented_code_output.md`
4. After commenting complete, create checkpoint
5. Proceed to Stage 7 (logging-enhancement) when ready

---

## Checkpoint Management

### Creating Checkpoints

At each stage completion:

1. Generate timestamp: `YYYYMMDD_HHMMSS`
2. Create backup directory: `backup/{timestamp}/`
3. Copy all artifact files to backup directory
4. Update progress.md checkpoint log

### Checkpoint Operations

```
# Create checkpoint
requests/{prefix}/backup/{timestamp}/
├── {prefix}_design_output.md
├── {prefix}_implementation_output.md
├── {prefix}_verification_output.md
├── {prefix}_code_review_output.md
└── {prefix}_commented_code_output.md
```

### Restoring from Checkpoint

If user requests restore:

1. List available checkpoints from progress.md
2. Ask user which checkpoint to restore
3. Copy files from backup to request directory
4. Update progress.md with restore note

---

## Stage Navigation

### Jump to Any Stage

User can request to jump to specific stage:

- "設計からやり直したい" → Go to Stage 2
- "実装を修正したい" → Go to Stage 3
- "検証をやり直したい" → Go to Stage 4

When jumping:

1. Create checkpoint of current state
2. Update progress.md
3. Invoke appropriate skill

### Resume Workflow

If workflow is interrupted:

1. Read progress.md to determine current stage
2. Resume from that stage
3. Report current status to user

---

## Progress Display

After each stage change, display status:

```
📋 Implementation Workflow: {Feature Name}

Current Stage: {stage number} - {stage name}

Progress:
[✓] 1. Request Received
[✓] 2. Design Discussion
[●] 3. Implementation
[ ] 4. Behavior Verification
[ ] 5. Code Review
[ ] 6. Code Commenting
[ ] 7. Logging Enhancement

📌 Last Checkpoint: {timestamp}
```

---

## Error Handling

### Skill Invocation Failure

If a skill fails to produce expected output:

1. Log error in progress.md
2. Ask user how to proceed:
   - Retry the stage
   - Skip to next stage
   - Abort workflow

### Missing Artifacts

If required artifact file is missing:

1. Check backup for recovery
2. If not in backup, ask user to provide or recreate

---

## Prefix Extraction Logic

Simple extraction algorithm:

1. Split request into words
2. Filter out common verbs and particles
3. Take first significant noun
4. Apply transformations:
   - Japanese: Romanize or use English equivalent
   - Spaces → underscores
   - Lowercase all
5. Truncate to 20 characters max

Examples:

| Request | Extracted Prefix |
|---------|------------------|
| ログイン機能の実装 | login |
| ユーザー検索API実装 | user_search |
| Dashboard component | dashboard |
| File upload handler | file_upload |

---

## Tips for Effective Workflow

- Review progress.md regularly for status
- Use checkpoints before major changes
- Keep request descriptions clear and specific
- Issues during verification help improve implementation
