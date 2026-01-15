---
name: implementation
description: |
  Execute implementation based on a design document.
  Use when user wants to implement code based on a design, or when proceeding from design-discussion.
  Triggers include "実装して", "コードを書いて", "implement this", "この設計で実装",
  or when implementation-workflow transitions to implementation stage.
  Reads design from file or direct input, produces working code following project conventions.
---

Execute implementation based on design documents. Produces working code following project conventions and best practices.

## Workflow Overview

Three-stage process:

1. **Design Input**: Receive and validate design document
2. **Implementation Execution**: Write code following design and conventions
3. **Output Generation**: Produce implementation files and summary

## Input Modes

This skill supports multiple input modes:

### Mode 1: File Reference

User provides path to design document (e.g., `{prefix}_design_output.md`).
- Read the file and extract DESIGN_OUTPUT section
- Validate design completeness
- Ask clarifying questions if needed

### Mode 2: Direct Input

User provides design content directly in chat.
- Parse the design structure
- Confirm understanding before implementing

### Mode 3: Workflow Integration

When called from implementation-workflow, receive design path from workflow context.

---

## Stage 1: Design Input

**Goal:** Understand the design and prepare for implementation.

### Design Validation

Check the design document contains:

- [ ] Clear module/class structure
- [ ] Interface definitions
- [ ] Data flow description
- [ ] Design decisions with rationale
- [ ] Coding standards specification

If missing critical information, ask clarifying questions before proceeding.

### Load Coding Standards

From the design document, extract specified coding standards:

1. **Read standards reference**: Check "Coding Standards" section in design document
2. **Load from coding-standards skill**: Read referenced standards from `coding-standards/references/`
3. **Apply standards**: Use loaded standards during implementation

If standards not specified in design:
- Ask user which standards to apply
- List available standards from coding-standards skill
- Allow custom standards input

### Pre-Implementation Checklist

Confirm with user:

1. Target directory for implementation
2. Language/framework if not specified in design
3. Coding standards confirmed (from design or user selection)
4. Existing files to integrate with (if any)

---

## Stage 2: Implementation Execution

**Goal:** Write code following design and conventions.

### Implementation Approach

1. **Start with structure**: Create file/folder structure first
2. **Core interfaces**: Implement public interfaces/APIs
3. **Internal logic**: Fill in implementation details
4. **Error handling**: Add error handling per design
5. **Integration points**: Connect with existing code if applicable

### Coding Conventions

**Load from coding-standards skill:**

Retrieve coding standards specified in the design document:

```
# Call coding-standards skill
Check available standards: coding-standards
Get specific standards: coding-standards <keywords>

# Examples:
coding-standards unity       # Get Unity standards
coding-standards csharp      # Get C# Project standards
```

**Apply standards:**

- Call coding-standards with language/framework keywords specified in design document
- Proceed with implementation based on retrieved standards
- Apply general coding principles if standards not found

**Fallback handling:**

- Standards unavailable: Apply language-specific best practices
- System error: Continue with basic coding principles

**General defaults** (when no specific standard applies):

- Clear, descriptive naming
- Single responsibility per function/class
- Minimal comments (code should be self-documenting)
- Handle errors explicitly

**Language-specific:**

Apply idiomatic patterns for the target language, combined with project-specific standards.

### Progress Updates

During implementation, provide periodic updates:

- Components completed
- Next steps

---

## Stage 3: Output Generation

**Goal:** Produce implementation files and summary.

### Implementation Files

Create actual code files in the target directory.

### Implementation Summary

Generate a summary document:

```markdown
<!-- IMPLEMENTATION_OUTPUT -->
# Implementation: {Feature Name}

## Applied Coding Standards
- Standards used: {list of applied standards}
- Reference: {link to coding-standards skill or specific reference files}

## Files Created

| File | Purpose |
|------|---------|
| path/to/file.ext | Description |
| ... | ... |

## Implementation Summary
Brief description of what was implemented.

## Key Components

### Component 1
- Location: path/to/file
- Purpose: what it does
- Key methods/functions

### Component 2
...

## Deviations from Design

| Item | Deviation | Reason |
|------|-----------|--------|
| ... | ... | ... |

(If no deviations, state "None - implemented as designed")

## Dependencies Added
- dependency1: purpose
- dependency2: purpose

(If no dependencies, state "None")

## Usage Example

```language
// Example code showing how to use the implementation
```

## Next Steps
- Verification items
- Integration tasks
- Potential improvements

<!-- /IMPLEMENTATION_OUTPUT -->
```

### File Output

**Standalone execution:**
Ask user where to save the summary. Suggest filename:
- Format: `{prefix}_implementation_output.md`
- Example: `login_implementation_output.md`

**Workflow integration:**
Output to the path specified by implementation-workflow.

---

## Prefix Handling

Use the same prefix as the design document:
- If input is `login_design_output.md`, output `login_implementation_output.md`
- If prefix unclear, ask user to specify

---

## Error Handling During Implementation

If encountering issues:

1. **Design ambiguity**: Ask user for clarification
2. **Technical constraint**: Propose alternative approach
3. **Scope creep**: Note as deviation and confirm with user

---

## Tips for Effective Implementation

- Implement incrementally, validate each step
- Keep implementations simple initially, refactor if needed
- Match design structure in code organization
- Document deviations immediately
- Consider testability from the start
