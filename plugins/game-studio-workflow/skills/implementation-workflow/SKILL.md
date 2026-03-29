---
name: implementation-workflow
description: |
  Orchestrate the full implementation workflow from requirements to completion.
  Coordinates design-system, agent-based implementation, behavior-verification, and code-review
  with progress tracking, checkpoints, and session state integration.
  Triggers: "機能を作りたい", "新しい機能を作りたい", "implementation workflow", "ワークフロー開始"
argument-hint: "[feature description]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, AskUserQuestion, TodoWrite
---

Orchestrate the full implementation workflow. Manages progress through stages,
delegates to specialized agents, and handles checkpoints with backups.

## Workflow Overview

| Stage | Method | Description |
|-------|--------|-------------|
| 1 | - | Receive implementation request |
| 2 | `/design-system` | Design discussion and documentation |
| 3 | Agent delegation | Code implementation via specialist agents |
| 4 | `/behavior-verification` | Verification checklist and user testing |
| 4.5 | (user decision) | User confirms: proceed or revise |
| 5 | `/code-review` | Code quality review |
| 5.5 | (user decision) | User confirms: proceed or revise |
| 6 | - | Summary and next steps |

---

## Initialization

### Request Input

When user provides implementation request:

1. **Extract prefix** from request:
   - Identify primary noun/concept
   - Convert to lowercase ASCII with underscores
   - Examples: "ログイン機能の実装" → `login`, "Search API" → `search_api`
   - Max 20 characters

2. **Confirm prefix** with user:
   > プレフィックス「{prefix}」を使用します。この識別子でファイルを管理します。
   > 別のプレフィックスをご希望の場合はお知らせください。

3. **Create request directory**:

```
requests/{prefix}/
├── progress.md
├── {prefix}_design_output.md      (created by design-system)
├── {prefix}_verification_output.md (created by behavior-verification)
└── backup/
    └── {YYYYMMDD_HHMMSS}/
```

### Progress Document

Create `progress.md`:

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
| 2 | ○ Pending | | Design (design-system) |
| 3 | ○ Pending | | Implementation (agent delegation) |
| 4 | ○ Pending | | Behavior Verification |
| 5 | ○ Pending | | Code Review |
| 6 | ○ Pending | | Summary |

## Artifacts

| Stage | File | Status |
|-------|------|--------|
| Design | {prefix}_design_output.md | ○ |
| Verification | {prefix}_verification_output.md | ○ |

## Agent Delegation Log

| Agent | Task | Status | Timestamp |
|-------|------|--------|-----------|

## Checkpoints

| Checkpoint | Timestamp | Backup Path |
|------------|-----------|-------------|

## Issues Log
(Issues found during verification or review)
```

### Update Session State

After each stage transition, update `production/session-state/active.md`:

```markdown
<!-- STATUS -->
Epic: Implementation Workflow
Feature: {Feature Name}
Task: Stage {N} - {Stage Name}
<!-- /STATUS -->
```

---

## Stage Transitions

### Stage 1 → 2: Start Design

1. Update progress.md: Stage 2 in progress
2. **Determine design approach** via `AskUserQuestion`:

   - If the feature involves a **game system** (combat, inventory, AI, etc.):
     > "This appears to be a game system. Which design approach?"
     - Options:
       - "Full GDD (8-section design)" — invokes `/design-system` in GDD mode
       - "Quick design discussion" — invokes `/design-system` in general mode
       - "Use existing GDD" — skip design, reference existing `design/gdd/*.md`

   - If the feature is a **general implementation task**:
     → Invoke `/design-system` in general mode (no argument or feature description)

3. Pass output path: `requests/{prefix}/{prefix}_design_output.md`
4. After design complete, create checkpoint

### Stage 2 → 3: Start Implementation

After design is complete:

1. **Create checkpoint**: Copy artifacts to `backup/{timestamp}/`
2. Update progress.md: Stage 3 in progress
3. **Select implementation agent(s)** based on the design document:

#### Agent Routing Table

| System Category | Primary Agent | Supporting Agent(s) |
|----------------|---------------|---------------------|
| Gameplay mechanics | `gameplay-programmer` | `systems-designer` (formulas) |
| AI / pathfinding | `ai-programmer` | `gameplay-programmer` |
| UI / HUD / menus | `ui-programmer` | `ux-designer` |
| Networking / multiplayer | `network-programmer` | `security-engineer` |
| Engine / core systems | `engine-programmer` | `technical-director` |
| Tools / pipeline | `tools-programmer` | `devops-engineer` |
| Shaders / VFX | Engine-specific shader specialist | `technical-artist` |
| Multi-domain feature | Recommend `/team-*` skill | See below |

#### Multi-Domain Detection

If the design document references multiple categories (e.g., gameplay + AI + audio),
recommend using a `/team-*` skill instead of individual agent delegation:

> "This feature spans multiple domains. Consider using one of these team skills
> for coordinated implementation:"
> - `/team-combat` — combat features
> - `/team-narrative` — story content
> - `/team-ui` — UI features
> - `/team-level` — level/area creation
> - `/team-audio` — audio work
> - `/team-polish` — optimization and polish

Use `AskUserQuestion` to let the user choose between agent delegation and team skill.

#### Delegating to Agents

When delegating via the Task tool, provide the agent with:
- The design document path
- Coding standards (loaded via `/coding-standards` skill based on project language)
- Target directory for implementation
- Relevant existing code paths
- Constraints from the design document

**Load coding standards**:
```
Check available: /coding-standards
Load specific: /coding-standards <language-keyword>
```

Pass loaded standards as context to the implementation agent.

4. Log agent delegation in progress.md Agent Delegation Log
5. After implementation complete, create checkpoint

### Stage 3 → 4: Start Verification

After implementation complete:

1. **Create checkpoint**: Copy artifacts to `backup/{timestamp}/`
2. Update progress.md: Stage 4 in progress
3. Invoke `/behavior-verification` with:
   - Implementation details (files created, components, usage examples)
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
2. Log issues in progress.md Issues Log
3. Return to Stage 3 — re-delegate to the same agent with issue context
4. The agent receives: original design, previous implementation, and issue details

### Stage 4.5 → 5: Start Code Review

After verification passes:

1. **Create checkpoint**
2. Update progress.md: Stage 5 in progress
3. Invoke `/code-review` with:
   - Path to implemented file(s)
   - The code-review skill checks: coding standards compliance, architectural patterns,
     SOLID principles, game-specific concerns (delta time, data-driven values, etc.)

### Stage 5.5: Review Decision Point

After code review:

**If "CHANGES REQUIRED":**
1. Display critical findings to user
2. Ask for confirmation to return to implementation
3. Log findings in progress.md
4. Return to Stage 3 — re-delegate with review findings

**If "APPROVED" or "APPROVED WITH SUGGESTIONS":**
1. Update progress.md: Stage 5 complete
2. Create checkpoint
3. Proceed to Stage 6

### Stage 5 → 6: Summary and Next Steps

1. Update progress.md: All stages complete
2. Present completion summary:

```
## Implementation Complete: {Feature Name}

### Artifacts
- Design: requests/{prefix}/{prefix}_design_output.md
- Verification: requests/{prefix}/{prefix}_verification_output.md
- Code review: APPROVED

### Files Created/Modified
[List from implementation agent output]

### Agent Delegation History
[From progress.md log]
```

3. Suggest next steps via `AskUserQuestion`:
   - "Run `/gate-check` to validate project phase readiness"
   - "Start another implementation (`/implementation-workflow`)"
   - "Run `/balance-check` if this affects game balance"
   - "Done for this session"

---

## Checkpoint Management

### Creating Checkpoints

At each stage completion:

1. Generate timestamp: `YYYYMMDD_HHMMSS`
2. Create backup directory: `backup/{timestamp}/`
3. Copy all artifact files to backup directory
4. Update progress.md checkpoint log

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
- "コードレビューをやり直したい" → Go to Stage 5

When jumping:
1. Create checkpoint of current state
2. Update progress.md
3. Invoke appropriate skill or agent

### Resume Workflow

If workflow is interrupted:

1. Read progress.md to determine current stage
2. Read `production/session-state/active.md` for additional context
3. Resume from the current stage
4. Report status to user

---

## Progress Display

After each stage change, display status:

```
📋 Implementation Workflow: {Feature Name}

Current Stage: {stage number} - {stage name}

Progress:
[✓] 1. Request Received
[✓] 2. Design (design-system)
[●] 3. Implementation (gameplay-programmer)
[ ] 4. Behavior Verification
[ ] 5. Code Review
[ ] 6. Summary

📌 Last Checkpoint: {timestamp}
```

---

## Error Handling

### Agent Delegation Failure

If an agent fails to produce expected output:

1. Log error in progress.md
2. Ask user how to proceed:
   - Retry with same agent
   - Try a different agent
   - Skip to next stage
   - Abort workflow

### Missing Artifacts

If required artifact file is missing:

1. Check backup for recovery
2. If not in backup, ask user to provide or recreate

---

## Collaborative Protocol

This skill follows the collaborative design principle:

1. **User approves** every stage transition
2. **AskUserQuestion** at every decision point
3. **Checkpoints** before every major change
4. **Session state** updated at every transition
5. **Agent delegation** is transparent — user sees what agent is invoked and why
6. **No autonomous multi-stage execution** — each stage requires explicit user go-ahead
