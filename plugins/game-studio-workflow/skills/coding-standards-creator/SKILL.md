---
name: coding-standards-creator
description: |
  Create and update detailed coding standards language packs for the coding-standards skill.
  Use when user wants to create new language/framework specific standards, update existing standards,
  generate templates based on existing standards, or extend the coding standards system.
  Generates structured language packs with metadata, detailed standards documents, and code examples.
  Triggers: "規約を作成", "規約を更新", "新しいコーディング規約", "create coding standard"
---

## Overview

This skill provides a comprehensive toolset for creating and updating language packs (coding standards) for the coding-standards skill. It offers enterprise-level template generation, interactive customization through guided questions, automatic validation and integration, and support for incremental updates to existing standards.

## When to Use

- Create coding standards for new languages or frameworks
- **Update existing coding standards** (add rules, modify sections, fix errors)
- Standardize and document existing project conventions
- Generate detailed standards for major languages (C#, Unity, TypeScript, Python, etc.)
- Create enterprise-level standards with 15 sections
- Extend the coding-standards system
- Refine and improve existing language packs based on feedback or project evolution

## Key Features

1. **Sample Code Analysis** - Extract conventions from existing codebase or sample files
2. **Interactive Language Pack Generation** - Question-based standard creation wizard
3. **Automatic Template Generation** - Complete structure: metadata.json + standards.md + examples/
4. **Detail Level Support** - Three levels: basic/detailed/enterprise
5. **Automatic Integration System** - Registration, validation, and updates to coding-standards
6. **Comprehensive Validation** - Structure checks, content validation, and functional testing

## Workflow: Create New Language Pack

### Step 1: Gather Sample Code (Optional but Recommended)

Before starting the creation process, ask users if they have sample code or project folders that represent their desired coding standards.

**User Prompt:**

Do you have sample source code or project folders that demonstrate your coding style?
- If yes: Please provide file paths or paste sample code
- If no: We'll start from language-specific best practices

**If code is provided:** Read and analyze the code manually to identify:
- Naming conventions (camelCase, snake_case, PascalCase, etc.)
- Indentation style and size
- Line length preferences
- Import/module organization patterns
- Common patterns and structures
- Any anti-patterns to avoid

**If no samples:** Start with standard language conventions (Microsoft guidelines for C#, etc.)

### Step 2: Define Language and Framework

Gather basic information about the target language:

- Language name (e.g., "unity", "csharp-project")
- Display name (e.g., "Unity", "C# Project")
- Target frameworks (e.g., ["Unity 2022+"] or [".NET 6+"])
- Detail level: basic/detailed/enterprise

### Step 3: Create Directory Structure

Create the language pack directory structure:

```
coding-standards/references/<language>/
├── metadata.json
├── standards.md
└── examples/
    ├── good_example.cs
    └── anti_patterns.cs
```

### Step 4: Create metadata.json

Create `metadata.json` with basic information:

```json
{
  "language": "unity",
  "display_name": "Unity",
  "version": "1.0.0",
  "frameworks": ["Unity 2022+"],
  "detail_level": "enterprise",
  "keywords": ["unity", "unity3d", "game", "gamedev"],
  "sections": [
    "naming", "format", "class", "method", "async",
    "comments", "performance", "var", "error-handling",
    "linq", "types", "testing", "security", "tools", "resources"
  ]
}
```

### Step 5: Write standards.md

Create `standards.md` following the 15-section template:

| # | セクション | 内容 |
|---|-----------|------|
| 1 | 命名規則 | ケース規則、特殊命名 |
| 2 | フォーマット・レイアウト | インデント、波括弧、空白 |
| 3 | クラス設計 | 構成順序、アクセス修飾子 |
| 4 | メソッド設計 | 責任、パラメータ、戻り値 |
| 5 | 非同期プログラミング | async/await、ConfigureAwait |
| 6 | コメントとドキュメント | XMLコメント、インライン |
| 7 | パフォーマンス | 文字列操作、コレクション選択 |
| 8 | varキーワード | 使用原則、適切/不適切な場面 |
| 9 | 例外処理 | 例外の種類、処理パターン |
| 10 | LINQとコレクション | LINQ使用、初期化 |
| 11 | 型システム | 型アノテーション、generics |
| 12 | テスト | ユニットテスト、統合テスト |
| 13 | セキュリティ | 脆弱性対策、入力検証 |
| 14 | ツール・設定 | linter、formatter、IDE設定 |
| 15 | リソース | 学習資料、リファレンス |

For each section, include:
- Priority level (🔴 CRITICAL / 🟡 RECOMMENDED / ⭐ GOLD)
- Rules and guidelines
- Code examples (good vs bad)

### Step 6: Create Code Examples

Create example files in the `examples/` directory:

- `good_example.{ext}` - Demonstrates best practices
- `anti_patterns.{ext}` - Shows what to avoid with comments

Base examples on sample code if provided, or create representative examples.

### Step 7: Validate Structure

Ensure all required files are created:

- ✓ `metadata.json` - Valid JSON with required fields
- ✓ `standards.md` - All 15 sections present
- ✓ `examples/` - At least one good example file

### Step 8: Register in coding-standards

Update `config/language_packs.json` to include the new language:

```json
{
  "language_packs": {
    "new-language": {
      "display_name": "New Language",
      "keywords": ["new", "language"],
      "file_path": "references/new-language/standards.md",
      "metadata_path": "references/new-language/metadata.json",
      "status": "available",
      "priority": 10,
      "detail_level": "enterprise"
    }
  }
}
```

Test by requesting standards for the new language from the coding-standards skill.

---

## Workflow: Update Existing Standards

When users want to update existing coding standards, follow this workflow:

### Step 1: Identify Update Type

Determine what kind of update is needed:

**Update Types:**
1. **Rule Addition** - Add new coding rules or guidelines
2. **Rule Modification** - Change existing rules (relax/tighten restrictions)
3. **Section Addition** - Add entirely new sections
4. **Section Removal** - Remove obsolete sections
5. **Example Update** - Add/modify code examples
6. **Metadata Update** - Update version, frameworks, keywords
7. **Error Correction** - Fix typos, incorrect examples, or broken links

**User Prompt:**

What would you like to update in the [language] standards?
- Add new rules/guidelines
- Modify existing rules
- Add/remove sections
- Update code examples
- Update metadata (version, frameworks)
- Fix errors or typos

### Step 2: Locate Existing Files

Identify the language pack location:

```
coding-standards/references/<language>/
├── metadata.json
├── standards.md
└── examples/
```

### Step 3: Read Current Content

Read the relevant files to understand current state:

1. **For rule/section changes**: Read `standards.md`
2. **For metadata changes**: Read `metadata.json`
3. **For example changes**: Read files in `examples/`

### Step 4: Apply Updates

Make the necessary edits to the files.

### Step 5: Update Metadata

When making significant changes, update `metadata.json`:

```json
{
  "version": "1.1.0",
  "last_updated": "2026-01-14"
}
```

### Step 6: Update Changelog

Add update history to the end of `standards.md`:

```markdown
## 更新履歴

| バージョン | 日付 | 変更内容 |
|-----------|------|---------|
| 1.1.0 | 2026-01-14 | 新規ルールの追加、セクション構成の変更 |
| 1.0.0 | 2026-01-14 | 初版リリース |
```

### Step 7: Validate Changes

1. **Structure Check**: Ensure all sections are properly formatted
2. **Link Check**: Verify internal references still work
3. **Example Validation**: Check code examples are still valid
4. **Metadata Sync**: Confirm metadata reflects the changes

### Step 8: Test Integration

Verify the updated standards work correctly:
1. Request standards from coding-standards skill
2. Check that new rules appear in output
3. Verify section numbering is correct
4. Confirm examples are accessible

---

## Advanced Features

### Sample Code Analysis

When users provide sample code, analyze it to identify:

**Naming Patterns:**
- Variables: camelCase, snake_case, etc.
- Functions: verb-noun patterns, naming length
- Classes: PascalCase, suffixes (Manager, Service, etc.)
- Constants: UPPER_CASE, prefixes

**Code Structure:**
- Indentation: spaces vs tabs, size
- Line length: max characters per line
- Import organization: absolute vs relative, grouping
- File structure: class-per-file, exports

**Common Patterns:**
- Type annotations usage
- Documentation style
- Error handling approaches
- Testing patterns

### Language-Specific Templates

Pre-defined templates for major languages:

- **C#**: Microsoft Style Guide compliant, LINQ and async/await patterns
- **Unity**: C# based with Unity-specific constraints (no LINQ, no try-catch)
- **TypeScript**: ESLint configuration, type system best practices
- **Python**: PEP 8 compliant, type hints

### Customizable Elements

1. **Section Structure**: Add, remove, or reorder the 15 standard sections
2. **Priority Levels**: Adjust CRITICAL/RECOMMENDED/GOLD assignments
3. **Tool Configuration**: Specify linters, formatters, and build tools
4. **Framework Support**: Add framework-specific patterns and constraints
5. **Code Examples**: Include actual project examples and anti-pattern collections

### Quality Assurance

1. **Structure Validation**: Check required and recommended fields in metadata.json
2. **Content Validation**: Verify section completeness in standards.md
3. **Code Validation**: Check syntax and executability of examples/
4. **Integration Validation**: Verify operation with coding-standards
5. **Reference Validation**: Test access from other skills

---

## Implementation Details

This skill uses the following components:

- `scripts/language_pack_creator.py`: Helper utilities for language pack creation

## Resources

### scripts/

Helper utilities:
- `language_pack_creator.py` - Utility functions for language pack creation

### references/

Documentation and reference material:
- `language_templates/` - Pre-defined templates for major languages
