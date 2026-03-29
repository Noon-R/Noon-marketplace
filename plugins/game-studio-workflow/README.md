# Game Studio Workflow Plugin

ゲーム開発スタジオ統合ワークフロープラグイン for Claude Code.

## Overview

48の専門エージェントと41のスキルを統合した、インディーゲーム開発のためのClaude Codeプラグインです。
設計から実装、検証、リリースまでの全開発フェーズをカバーします。

## Features

- **48 Agents** — 3階層のスタジオ組織（Director → Lead → Specialist）
- **41 Skills** — 設計、制作、テスト、リリース、チームオーケストレーション
- **11 Rules** — パススコープ付きコーディング規約（自動適用）
- **8 Hooks** — セッション管理、バリデーション、監査
- **Dynamic Coding Standards** — 言語パックベースの動的コーディング規約
- **Implementation Workflow** — 進捗追跡・チェックポイント付き統合ワークフロー
- **Engine Support** — Godot 4 / Unity / Unreal Engine 5

## Installation

```bash
bash plugins/game-studio-workflow/setup.sh
```

This copies agents, hooks, rules, docs, and settings to `.claude/`.
Skills are served directly from the plugin directory.

## Quick Start

1. `bash plugins/game-studio-workflow/setup.sh` — Install
2. `/start` — Guided onboarding
3. `/setup-engine` — Configure your game engine
4. `/brainstorm` — Start ideation

## Skills (41)

### Design & Planning
| Command | Description |
|---------|-------------|
| `/start` | First-time onboarding |
| `/brainstorm` | Guided ideation (MDA, SDT, verb-first) |
| `/map-systems` | Decompose concept into systems |
| `/design-system` | GDD authoring + general design discussion |
| `/design-review` | Validate design document |
| `/architecture-decision` | Create ADR |

### Implementation
| Command | Description |
|---------|-------------|
| `/implementation-workflow` | Full workflow: design → implement → verify → review |
| `/coding-standards` | Load language-specific coding standards |
| `/coding-standards-creator` | Create new coding standards language pack |
| `/code-review` | Architectural and quality code review |
| `/behavior-verification` | Feature-level verification checklist |
| `/prototype` | Rapid prototyping |

### Production & Sprint
| Command | Description |
|---------|-------------|
| `/sprint-plan` | Sprint planning |
| `/estimate` | Effort estimation |
| `/scope-check` | Scope creep detection |
| `/milestone-review` | Milestone progress review |
| `/retrospective` | Sprint retrospective |
| `/gate-check` | Phase gate validation |

### Testing & Quality
| Command | Description |
|---------|-------------|
| `/balance-check` | Game balance analysis |
| `/playtest-report` | Playtest report template |
| `/perf-profile` | Performance profiling |
| `/tech-debt` | Tech debt tracking |
| `/asset-audit` | Asset compliance audit |

### Release
| Command | Description |
|---------|-------------|
| `/release-checklist` | Pre-release validation |
| `/launch-checklist` | Full launch readiness |
| `/changelog` | Auto-generate changelog |
| `/patch-notes` | Player-facing patch notes |
| `/hotfix` | Emergency fix workflow |

### Team Orchestration
| Command | Description |
|---------|-------------|
| `/team-combat` | Combat team (6 agents) |
| `/team-narrative` | Narrative team (4 agents) |
| `/team-ui` | UI team (3 agents) |
| `/team-release` | Release team (4 agents) |
| `/team-polish` | Polish team (4 agents) |
| `/team-audio` | Audio team (4 agents) |
| `/team-level` | Level design team (6 agents) |

## Agent Hierarchy

```
                creative-director / technical-director / producer
                                     |
      ---------------------------------------------------------------
      |            |           |           |          |        |
game-designer  lead-prog  art-dir  audio-dir  narr-dir  qa-lead  release-mgr
      |            |           |           |          |        |
 specialists  programmers  tech-art  snd-design  writer   qa-tester  devops
```

## Coding Standards System

Two-tier system:
- **Tier 1 (Automatic)**: `rules/` — path-scoped rules applied automatically on file edit
- **Tier 2 (On-demand)**: `/coding-standards` — detailed language packs loaded by skills

Available language packs: Unity, C# Project.
Create new packs with `/coding-standards-creator`.

## License

See LICENSE file in the repository root.
