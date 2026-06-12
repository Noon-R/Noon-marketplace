---
name: code-knowledge-creator
description: |
  Create and update knowledge packs (coding standards, technical constraints, golden samples) for the code-knowledge skill.
  Use when user wants to create new language/framework specific knowledge packs, update existing packs,
  migrate monolithic standards to the structured format, or extend the code-knowledge system.
  Generates structured packs: core constraints (with rewrite pairs), golden samples, and detail sections.
  Triggers: "規約を作成", "規約を更新", "新しいコーディング規約", "ナレッジパック作成", "create coding standard", "create knowledge pack"
---

## Overview

Creates and updates knowledge packs (coding standards, technical constraints, golden samples) for the code-knowledge skill. **A good pack is measured by load efficiency and compliance rate, not volume.** Always follow the design principles below. Communicate with the user in Japanese.

---

## Design Principles — read before creating any pack

### Principle 1: Three layers, separated by load timing

Split knowledge by **when it gets loaded**. Never create an all-in-one file (it bloats context and buries the critical constraints, lowering compliance).

| Layer | Content | Size budget | Load timing |
|-------|---------|-------------|-------------|
| **core.md** | Critical constraints + essential style table | **~2KB strict** | Always (injected into implementation agents) |
| **examples/** | Golden samples | ~100 lines per file | Before implementation |
| **sections/** | Per-topic detail rules | 1-4KB each | Only when a question arises |

**Separation criteria:**
- "Violation = immediate reject" constraints → core.md
- Details, background, pattern collections consulted when unsure → sections/
- Conventions faster to show than to explain → examples/

### Principle 2: Don't write what an LLM already does unprompted

Claude already uses meaningful names and single-responsibility design without being told. Generic advice does not belong in core.md. **Only write what differs from default behavior:**

- ✅ Worth writing: "No LINQ", "No try-catch", "private fields are `_PascalCase`" (Claude defaults to `_camelCase`), "enum values are SNAKE_CASE"
- ❌ Not worth writing: "Classes are PascalCase", "Methods start with verbs", "Use meaningful names"

When interviewing the user, the top question is: **"Where do your rules differ from the standard conventions of this language?"**

### Principle 3: Prohibitions always come as ❌/✅ rewrite pairs

A prohibition without an alternative gets violated. Every critical constraint in core.md must include a **rewrite pair** (5-10 lines):

```csharp
// ❌ var actives = users.Where(u => u.IsActive).ToList();
// ✅
List<User> actives = new List<User>();
foreach (User user in users)
{
    if (user.IsActive) { actives.Add(user); }
}
```

### Principle 4: Design golden samples as "intersections of rules"

Instead of many per-rule snippets, create **one complete code file that embodies many rules at once**. Token efficiency is far higher, and LLMs imitate code more reliably than they follow rule prose.

- **One file per code domain** (e.g., Unity = one for plain classes + one for MonoBehaviour)
- **~100 lines max**: longer samples don't get read and blur the imitation focus
- **Must actually compile**: no pseudocode. A low-quality sample is worse than rule prose (bad habits get imitated too)
- **Header comment lists the embodied rules**: make explicit what the file is a model of
- **Design check**: verify naming, member ordering, error handling, and prohibition alternatives all appear in the one file

Reference implementation: `code-knowledge/references/unity/examples/golden_service.cs`

### Principle 5: Make sections/ discoverable via the index

Register each section in metadata.json's `sections` with a **one-line description**. Implementation agents decide whether to read a section from the description alone, so use concrete terms that reveal the content (not "error handling details" but "no-try-catch details, Result<T> pattern, TryPattern, input validation").

---

## Workflow: Create New Knowledge Pack

### Step 1: Gather Sample Code (recommended)

If the user has existing code, read it and extract:

- **Rules that differ from defaults** (per Principle 2 — these are core.md candidates)
- Naming/structure patterns (material for golden samples)
- Prohibited APIs/patterns (material for ❌/✅ pairs)

Without samples, start from the language standard (e.g., Microsoft guidelines for C#) and interview for "where do you deviate from the standard".

### Step 2: Define Pack

- Pack key (e.g., "unity"), display name, target frameworks, search keywords

### Step 3: Scaffold

```bash
python scripts/knowledge_pack_creator.py create <pack_key> --name "Display Name" --keywords kw1 kw2
```

Generates `core.md` + `sections/` (5 starter files: naming, formatting, class-design, error-handling, testing) + `examples/` (empty) + `metadata.json`.

### Step 4: Write core.md (most important — apply Principles 2 & 3)

1. Write critical constraints as ❌/✅ pairs (usually 3-6; if over 10, reconsider whether they are truly critical)
2. Essential style table (only what differs from defaults)
3. **Keep under 2KB.** Move overflow to sections/

### Step 5: Create Golden Samples (apply Principle 4)

1. Identify code domains (e.g., service class / UI component / test)
2. Write one ~100-line complete file per domain
3. Have the user review it ("Is this code OK to multiply across the codebase as-is?")
4. Register in metadata.json `examples` with descriptions

### Step 6: Write sections/ (apply Principle 5)

Write detail rules per topic. Delete unused starter files. Register each section in metadata.json with a concrete description.

### Step 7: Register & Validate

1. Register in `config/knowledge_packs.json` (`"format": "structured"`)
2. Validate: `python scripts/knowledge_pack_creator.py validate <pack_key>`
   - Warns on core.md size overrun, missing ❌/✅ pairs, unregistered examples
3. Run `code-knowledge/scripts/generate_skill_content.py update` to refresh the dynamic SKILL.md section
4. Confirm the new pack resolves via the code-knowledge skill

---

## Workflow: Migrate Monolithic Pack to Structured

To migrate a legacy single-file pack (standards.md) to the 3-layer structure:

1. Read standards.md and extract **critical constraints** (🔴 CRITICAL level) → core.md (reformat as ❌/✅ pairs)
2. **Consolidate and distill** scattered code examples into golden samples → examples/
3. Split remaining detail by topic → sections/ (related chapters may share one file)
4. Rewrite metadata.json with `"format": "structured"`, the sections index, and examples
5. Delete standards.md and update knowledge_packs.json
6. Run validate and the dynamic content update

Reference example: the unity pack migration (15 chapters → core.md + 2 samples + 10 sections)

---

## Workflow: Update Existing Pack

1. **Identify update type**: constraint add/relax, section addition, sample update, error fix
2. **Decide the target layer (Principle 1 separation criteria):**
   - New prohibition → core.md (with rewrite pair) + sections/ detail if needed
   - Additional detail patterns → sections/ only
   - Convention change → **always update the golden samples too** (sample-vs-rule contradiction is the worst state; LLMs follow the sample)
3. Update metadata.json `version` and `last_updated`
4. Run validate → dynamic content update

---

## Quality Checklist

On pack completion, verify:

- [ ] core.md is under 2KB
- [ ] Every critical constraint has a ❌/✅ pair
- [ ] core.md contains no generic advice an LLM follows unprompted
- [ ] Golden samples compile (build to confirm if possible)
- [ ] Samples do not contradict core.md / sections/
- [ ] metadata.json section descriptions are concrete (content guessable)
- [ ] Registered in knowledge_packs.json and dynamic content refreshed

## Implementation Details

- `scripts/knowledge_pack_creator.py`: scaffold generation and structure validation (supports structured/monolithic)
