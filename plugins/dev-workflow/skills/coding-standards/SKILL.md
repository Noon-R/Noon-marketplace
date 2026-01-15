---
name: coding-standards
description: |
  Provide coding standards and conventions based on project/language keywords.
  Triggered by 'coding-standards', language names (unity, csharp, c#), or requests for coding conventions.
  Uses dynamic external reference system with Python scripts for automatic language pack recognition.
  Keywords: "コーディング規約", "規約を教えて", "coding-standards"
---

This skill provides appropriate coding standards and conventions based on project and language keywords.

The external reference system enables automatic recognition when new language packs are added.

<!-- DYNAMIC_CONTENT_START: 内容はPythonスクリプトにより自動更新されます -->

## 利用可能な言語パック

以下の言語パックが利用可能です (最終更新: 2026-01-14, version: 1.0.0)

| キーワード | 言語/規約 | ファイル | 状態 |
|-----------|----------|---------|------|
| 'unity', 'unity3d', 'game', 'gamedev' | Unity | [references/unity/standards.md](references/unity/standards.md) | OK |
| 'csharp', 'c#', 'dotnet', '.net', 'cs' | C# Project | [references/csharp-project/standards.md](references/csharp-project/standards.md) | OK |

## 利用可能な言語パック（詳細）

- **Unity**: 'unity', 'unity3d', 'game', 'gamedev' (詳細度: enterprise)
  - **重要な制約**: Linq禁止、try-catch例外処理禁止
- **C# Project**: 'csharp', 'c#', 'dotnet', '.net', 'cs' (詳細度: enterprise)

<!-- DYNAMIC_CONTENT_END -->

## Usage

### Trigger Keywords

This skill is activated by the following keywords:

- 'coding-standards'
- 'コーディング規約' (Japanese: coding conventions)
- '規約を教えて' (Japanese: tell me the standards)
- Language or framework names (e.g., unity, csharp, c#)

### Basic Usage

When you make a request containing keywords, the corresponding standards will be provided:

**Examples:**
- "Tell me Unity standards" → Display Unity conventions
- "What are the C# coding standards?" → Display C# conventions
- "Show available standards" → List all available standards

## Execution Details

When this skill is activated, the following processes are executed:

1. **Retrieve Language List via Python Script**
   Execute `scripts/list_standards.py` to get available language packs

2. **Keyword Matching**
   - Extract keywords from user request
   - Match against language pack configuration
   - Select optimal standard by priority order

3. **Provide Standard Content**
   - Read corresponding standards.md
   - Provide formatted content

## Technical Details

### Component Structure

- `config/language_packs.json`: Language pack metadata (at plugin root)
- `scripts/list_standards.py`: Standard listing and search logic
- `references/*/standards.md`: Standards documentation for each language
- `scripts/generate_skill_content.py`: Dynamic SKILL.md generation

### Language Pack Structure

Each language pack is defined in the following format:

```json
{
  "language_key": {
    "display_name": "Display Name",
    "keywords": ["search", "keywords"],
    "file_path": "references/language/standards.md",
    "metadata_path": "references/language/metadata.json",
    "status": "available|planned|deprecated",
    "priority": 1,
    "detail_level": "basic|detailed|enterprise"
  }
}
```

### Error Handling

- Python script execution failure: Infer basic information from language pack names
- Config file load failure: Provide fallback information
- Standards file missing: Display recovery guidance

## Updating the Skill

After adding new language packs or updating existing standards, update the dynamic content section with:

```bash
python scripts/generate_skill_content.py update
```

This will update only the table and list between `<!-- DYNAMIC_CONTENT_START -->` and `<!-- DYNAMIC_CONTENT_END -->` markers, preserving manual edits to the rest of the file.

*The dynamic content section in this SKILL.md is automatically updated by the external reference system.*
*Manual edits to other sections are preserved. Update language_packs.json and run the script to refresh tables.*
