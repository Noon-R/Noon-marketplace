---
name: implementation-workflow
description: |
  Orchestrate the full implementation workflow from requirements to completion.
  Use when user wants to start a new implementation task with full workflow support, or manage an ongoing implementation.
  Triggers include "機能を作りたい", "新しい機能を作りたい", "implementation workflow", "ワークフロー開始", or explicit workflow management requests.
  Design discussion runs interactively in the main thread; implementation, verification, and code review run as autonomous agents (implementer, verifier, reviewer) with file-based handoff.
---

Orchestrate the implementation workflow. **Consultation (design) runs interactively in the main thread; work (implementation, verification, review) runs in autonomous agents**, handing off artifacts via files. Keep only progress management and user decision points in the main thread to minimize context. Communicate with the user in Japanese.

## Stages

| Stage | Executor | Where | Artifact |
|-------|----------|-------|----------|
| 1. Request | - | main | progress.md |
| 2. Design | design-discussion skill | **main (interactive)** | {prefix}_design_output.md |
| 3. Implementation | **implementer agent** | subagent | {prefix}_implementation_output.md + code |
| 4. Verification | **verifier agent** | subagent | {prefix}_verification_output.md |
| 4.5 User Decision | user | main | - |
| 5. Code Review | **reviewer agent** | subagent | {prefix}_code_review_output.md |
| 5.5 Review Decision | user | main | - |

## Initialization

1. **Extract prefix**: convert the request's main concept to lowercase ASCII with underscores ("ログイン機能の実装" → `login`). Max 20 chars. Confirm with the user:
   > プレフィックス「{prefix}」を使用します。変更希望があればお知らせください。
2. **Create directories**: `requests/{prefix}/` and `requests/{prefix}/backup/`
3. **Create progress.md**:

```markdown
# Implementation Progress: {Feature Name}

## Request
{original request}

## Prefix
{prefix}

## Knowledge Pack
{decided during design. e.g., unity}

## Stage History
| Stage | Status | Timestamp | Notes |
|-------|--------|-----------|-------|

## Checkpoints
| Timestamp | Backup Path |

## Issues Log
```

## Stage Transitions

### Stage 2: Design (main thread, interactive)

Use the design-discussion skill to design interactively with the user. Output: `requests/{prefix}/{prefix}_design_output.md`. The design doc **must record the knowledge pack key** (the implementer agent loads it). Create a checkpoint when done.

### Stage 3: Implementation (implementer agent)

Launch the **implementer** agent via the Agent tool. Include in the prompt:

- Design doc path: `requests/{prefix}/{prefix}_design_output.md`
- Output path: `requests/{prefix}/{prefix}_implementation_output.md`
- Target directory
- On re-run: the relevant issue list from the Issues Log

From the agent's summary, **check for Open Questions and design deviations**; if any, present them to the user for judgment. Create a checkpoint when done.

### Stage 4: Verification (verifier agent)

Launch the **verifier** agent via the Agent tool. Include in the prompt:

- Implementation report path and design doc path
- Output path: `requests/{prefix}/{prefix}_verification_output.md`

The agent runs automated checks (constraint scan, build, tests) and generates a manual checklist. **If automated checks find problems, report them to the user immediately without waiting for Stage 4.5.**

### Stage 4.5: User Decision

Present the manual checklist from the verification report and ask the user to run it:

| Choice | Action |
|--------|--------|
| ✓ 確認完了 | Create checkpoint → Stage 5 |
| ✗ 修正が必要 | Record issues in Issues Log → back to Stage 3 (pass the issue list to implementer) |

### Stage 5: Code Review (reviewer agent)

Launch the **reviewer** agent via the Agent tool. Include in the prompt:

- Implementation report path and design doc path
- Output path: `requests/{prefix}/{prefix}_code_review_output.md`

### Stage 5.5: Review Decision

Based on the agent's decision:

- **Needs Revision**: present Critical findings to the user → after confirmation, record in Issues Log and return to Stage 3
- **Approved / Approved with Comments**: create checkpoint → workflow complete. Attach Should Fix items to the completion report

## Checkpoint Management

On each stage completion, copy all artifacts to `requests/{prefix}/backup/{YYYYMMDD_HHMMSS}/` and record in progress.md. On restore request, list checkpoints, let the user choose, and write files back.

## Navigation & Resume

- **Jump**: "設計からやり直したい" → create checkpoint, then go to that stage
- **Resume**: read progress.md to identify the current stage, report status, continue
- **Agent failure**: record the error in progress.md; ask the user to retry / skip / abort

## Progress Display

On every stage change, display:

```
📋 {Feature Name}  [✓設計 ●実装 ○検証 ○レビュー]  Last checkpoint: {timestamp}
```

## Operating Principles

- Artifact handoff is **always via files**. Never expand an agent's full response into the main thread
- Do not re-read code in the main thread (judge review results from the reviewer agent's report)
- Limit user decision requests to Stage 4.5 / 5.5 and Open Questions reported by agents
