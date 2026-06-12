---
name: implementation
description: |
  Execute implementation based on a design document, in the main thread.
  Use when user wants to implement code interactively based on a design. For autonomous workflow execution, implementation-workflow uses the implementer agent instead.
  Triggers include "実装して", "コードを書いて", "implement this", "この設計で実装".
  Reads design from file or direct input, loads the knowledge pack progressively, produces working code.
---

Execute implementation based on design documents, interactively in the main thread. Communicate with the user in Japanese.

> **Note:** When called from implementation-workflow, the **implementer agent** is used instead of this skill. This skill is for standalone, interactive implementation.

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

### Load Knowledge Pack (progressive)

Using the pack key from the design doc's "Knowledge Pack" section, load from the code-knowledge skill structure:

1. `references/{pack}/metadata.json` — file paths and section index
2. `references/{pack}/core.md` — **non-negotiable constraints**
3. The golden sample matching the code type (`examples/`)

Read detail sections (`sections/*.md`) **only when a question arises during implementation**. Never preload everything.

If the design doc specifies no pack: list packs via `scripts/list_knowledge.py` and ask the user to choose. If none fits, proceed with general best practices.

### Pre-Implementation Checklist

Confirm with user: target directory / language & framework (if not in design) / knowledge pack / existing files to integrate with.

---

## Stage 2: Implementation Execution

1. **Start with structure**: File/folder structure first
2. **Core interfaces**: Public interfaces/APIs
3. **Internal logic**: Implementation details
4. **Error handling**: Follow core.md conventions (e.g., return values instead of exceptions for Unity)
5. **Integration points**: Connect with existing code

When in doubt, imitate the golden sample. Record design deviations as you go.

**General defaults** (no pack): clear naming, single responsibility, minimal comments, explicit error handling, idiomatic patterns for the target language.

---

## Stage 3: Output Generation

### Self-Verification

Before finishing: Grep the code for core.md constraint violations (e.g., `using System.Linq` / `catch`). Build and confirm if possible.

### Implementation Summary

Headers in English; write prose content in Japanese:

```markdown
<!-- IMPLEMENTATION_OUTPUT -->
# Implementation: {Feature Name}

## Applied Knowledge Pack
- Pack: {pack key} (core.md + {samples/sections used})

## Files Created
| File | Purpose |
|------|---------|

## Implementation Summary
{description}

## Key Components
{location / purpose / key methods per component}

## Deviations from Design
| Item | Deviation | Reason |
(If none: "None - implemented as designed")

## Self-Verification
- Constraint check: {result}
- Build/Compile: {result}

## Dependencies Added
(If none: "None")

## Usage Example
{example code}

## Next Steps
- Verification items, integration tasks
<!-- /IMPLEMENTATION_OUTPUT -->
```

### File Output

- **Standalone**: Suggest `{prefix}_implementation_output.md` (same prefix as the design doc)
- **Workflow**: Output to the specified path

## Error Handling During Implementation

1. **Design ambiguity**: Ask user for clarification
2. **Technical constraint**: Propose alternative approach
3. **Scope creep**: Note as deviation and confirm with user
