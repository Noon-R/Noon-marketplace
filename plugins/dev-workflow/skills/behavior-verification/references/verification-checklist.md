# Verification Checklist Guide

## Checklist Structure

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

## Output Format

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

## File Output

**Standalone execution:**
Ask user where to save the checklist. Suggest filename:
- Format: `[prefix]_verification_output.md`
- Example: `login_verification_output.md`

**Workflow integration:**
Output to the path specified by implementation-workflow.

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
| **確認完了** | すべての項目が正常に動作しました |
| **修正が必要** | 問題が見つかりました（詳細を教えてください） |

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

## Prefix Handling

Use the same prefix as the implementation document:
- If input is `login_implementation_output.md`, output `login_verification_output.md`
- If prefix unclear, ask user to specify

## Tips for Effective Verification

- Focus on user-observable behavior
- Prioritize critical paths over edge cases initially
- Keep checklist actionable and specific
- Include "how to test" for each item
- Make pass/fail criteria clear
