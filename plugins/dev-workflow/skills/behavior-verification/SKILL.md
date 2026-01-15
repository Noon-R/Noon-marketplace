---
name: behavior-verification
description: |
  Generate verification checklists for implemented code and guide user through testing.
  Use when user wants to verify implementation, test code behavior, or when proceeding from implementation stage.
  Triggers include "動作確認したい", "テストして", "verify this", "検証を実施して",
  or when implementation-workflow transitions to verification stage.
  Produces structured checklist and waits for user confirmation.
---

Generate verification checklists for implemented code. Guides user through testing and collects confirmation before proceeding.

## Workflow Overview

Three-stage process:

1. **Implementation Input**: Receive implementation summary
2. **Checklist Generation**: Create verification checklist
3. **User Confirmation**: Wait for user to complete verification

## Input Modes

This skill supports multiple input modes:

### Mode 1: File Reference

User provides path to implementation summary (e.g., `{prefix}_implementation_output.md`).
- Read the file and extract IMPLEMENTATION_OUTPUT section
- Analyze components and generate verification items

### Mode 2: Direct Input

User provides implementation details or code directly.
- Analyze the provided code/description
- Generate appropriate verification items

### Mode 3: Workflow Integration

When called from implementation-workflow, receive implementation path from workflow context.

---

## Stage 1: Implementation Input

**Goal:** Understand what was implemented to generate relevant verification items.

### Input Analysis

From the implementation summary, extract:

- Files created and their purposes
- Key components and their responsibilities
- Usage examples
- Dependencies added
- Integration points

### Context Gathering

If needed, ask:

1. How should the implementation be executed? (command, UI, API call)
2. Are there specific test scenarios to cover?
3. Any edge cases highlighted in design?
4. Access to test environment/data?

---

## Stage 2: Checklist Generation

**Goal:** Create comprehensive verification checklist.

### Checklist Structure

Generate checklist covering:

1. **Basic Functionality**
   - Core features work as expected
   - Input/output matches specification

2. **Error Handling**
   - Invalid input handling
   - Edge cases
   - Error messages are appropriate

3. **Integration**
   - Works with existing components
   - Dependencies load correctly

4. **Non-Functional** (if applicable)
   - Performance acceptable
   - Memory/resource usage reasonable

### Output Format

```markdown
<!-- VERIFICATION_CHECKLIST -->
# Verification: [Feature Name]

## Verification Environment
- Target: description of what to verify
- Prerequisites: required setup or dependencies

## Checklist

### Basic Functionality
- [ ] **[Test Item 1]**: Description of what to test
  - Expected: what should happen
  - How to test: steps to verify
- [ ] **[Test Item 2]**: ...

### Error Handling
- [ ] **[Error Case 1]**: Description
  - Input: what to provide
  - Expected: expected error behavior

### Integration
- [ ] **[Integration Point 1]**: Description
  - How to test: steps to verify

### Notes
- Any special considerations
- Known limitations to be aware of

## Verification Result
_To be filled by user after testing_

- [ ] All items verified
- [ ] Issues found (describe below)

### Issues Found
(List any issues discovered during verification)

<!-- /VERIFICATION_CHECKLIST -->
```

### File Output

**Standalone execution:**
Ask user where to save the checklist. Suggest filename:
- Format: `{prefix}_verification_output.md`
- Example: `login_verification_output.md`

**Workflow integration:**
Output to the path specified by implementation-workflow.

---

## Stage 3: User Confirmation

**Goal:** Wait for user to complete verification and collect result.

### Waiting for User

After generating checklist, display:

---

**動作確認を実施してください**

チェックリストに従って動作確認を行い、完了後に結果を教えてください。

確認が完了したら、以下のいずれかを選択してください：

| 選択 | 説明 |
|------|------|
| **✓ 確認完了** | すべての項目が正常に動作しました |
| **✗ 修正が必要** | 問題が見つかりました（詳細を教えてください） |

---

### Handling User Response

**If "確認完了" (Verification Complete):**
- Record verification as successful
- If in workflow mode, signal to proceed to next stage (code-review)

**If "修正が必要" (Needs Modification):**
- Ask user to describe the issues found
- Document the issues
- If in workflow mode, signal to return to implementation stage
- Pass issue details to implementation skill for correction

### Issue Documentation

When issues are reported, create structured issue list:

```markdown
## Issues from Verification

### Issue 1: [Title]
- **Symptom**: What happened
- **Expected**: What should have happened
- **Steps to reproduce**: How to trigger the issue
- **Severity**: High/Medium/Low

### Issue 2: ...
```

---

## Prefix Handling

Use the same prefix as the implementation document:
- If input is `login_implementation_output.md`, output `login_verification_output.md`
- If prefix unclear, ask user to specify

---

## Tips for Effective Verification

- Focus on user-observable behavior
- Prioritize critical paths over edge cases initially
- Keep checklist actionable and specific
- Include "how to test" for each item
- Make pass/fail criteria clear

## Reference

See [verification-checklist.md](references/verification-checklist.md) for detailed checklist templates and examples.
