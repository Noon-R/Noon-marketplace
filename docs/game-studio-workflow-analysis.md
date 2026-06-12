# game-studio-workflow 解析・改善案・dev-workflowとの二重管理回避策

- 作成日: 2026-06-12
- 対象: `plugins/game-studio-workflow` v1.0.0
- 関連: `plugins/dev-workflow` v2.0.0（agent化・code-knowledge 3層構造への再設計済み、commit `b0ee7c9`）

---

## 1. 現状の構造

### 1.1 規模

| ディレクトリ | サイズ | 内容 |
|------------|--------|------|
| agents/ | 456KB | 48エージェント（平均~9.5KB） |
| skills/ | 362KB | 41スキル |
| engine-reference/ | 352KB | Godot/Unity/Unreal のAPI知識（modules, deprecated-apis, breaking-changes等） |
| docs/ | 313KB | テンプレート（192KB）、リファレンス類 |
| hooks/ | 40KB | bashフック8本 |
| rules/ | 39KB | ドメイン別ルール11ファイル（gameplay-code, shader-code等） |

### 1.2 配布モデル: 「プラグイン」と「コピーインストーラー」のハイブリッド

2つの配布経路が混在している（上流 claude-code-game-studios 由来の設計）:

1. **プラグインネイティブ**: skills（41個）と agents（48個）はプラグイン機構で自動認識される
2. **setup.shコピー方式**: hooks / rules / docs / settings / statusline は `setup.sh` で対象プロジェクトの `.claude/` へコピーして初めて機能する

---

## 2. 発見した問題（重要度順）

### ① マーケットプレイス経由では半分しか動かない

`plugin.json` には `"skills"` しか登録されていない。フック（コミット検証、セッション開始コンテキスト、PreCompact退避など）は `settings/settings.json` が `.claude/hooks/*.sh` を参照する前提のため、**setup.sh を実行しない限り一切発火しない**。プラグインとしてインストールしただけのユーザーには、品質ゲートが静かに全部無効になる。

### ② agentの知識参照パスが壊れている

godot-specialist 等は `docs/engine-reference/godot/VERSION.md` という相対パスを参照するが、プラグイン実体では `engine-reference/` はプラグインルート直下にある。setup.shコピー後または上流リポジトリのレイアウト前提のパスであり、**プラグインとして動かすと352KBのエンジン知識にagentが到達できない**。

### ③ agentの二重登録リスク

setup.sh は agents も `.claude/agents/` へコピーする。プラグイン機構が既に agents を認識しているため、setup.sh を実行すると**同名agentが二重登録**される。

### ④ 常時コンテキストコストが大きい

48のagent descriptionと41のskill descriptionは、サブエージェント起動の有無にかかわらず**毎セッション常時ロード**される（推定4〜5Kトークン）。Unityプロジェクトの利用者にもGodot系5体・Unreal系5体のspecialistが常駐する構造。

### ⑤ 重複スキルが既に乖離している（二重管理の実害）

dev-workflowとの重複: `coding-standards` / `coding-standards-creator` / `implementation-workflow` / `behavior-verification`（加えて `design-system` ⊃ design-discussion、`code-review` ≒ reviewer agent）。

- game側 `coding-standards` はdev-workflowの**旧v1のコピー**（monolithic standards.md + language_packs.json）。さらに `config/language_packs.json` が**コミット漏れ**（untracked）で、クローン環境では壊れている
- 一方 `implementation-workflow` はgame側が**進化版**（Stage 3でspecialist agentに委譲、design-system連携）

つまり「dev側が進んだ機能」と「game側が進んだ機能」が既に枝分かれしており、典型的な二重管理の症状が出ている。

---

## 3. 改善案

| # | 改善 | 効果 |
|---|------|------|
| 1 | フックを `hooks/hooks.json` としてプラグインに正式登録し、パスを `${CLAUDE_PLUGIN_ROOT}` 参照に変更。setup.shのフック/agentコピーを廃止 | マーケットプレイスインストールだけで完全動作。二重登録解消 |
| 2 | agent内の `docs/engine-reference/...` 参照を `${CLAUDE_PLUGIN_ROOT}/engine-reference/...` に統一 | エンジン知識への到達性回復 |
| 3 | エンジン別specialistを分割プラグイン化（`game-studio-godot` / `-unity` / `-unreal`）し、コアは横断ロールのみに | 常時コンテキストを約1/3削減。使うエンジンのagentだけ常駐 |
| 4 | `claude-code-game-studios-main/`（上流ソースのコピー、リポジトリ直下にuntracked）を .gitignore または削除 | リポジトリ衛生 |

※ ①②は動作不全に近いバグであり、優先着手を推奨。

---

## 4. 二重管理の回避策

### 4.1 選択肢の比較

| 案 | 内容 | 評価 |
|----|------|------|
| **A. dev-workflowをコンパニオン（共通基盤）化** | 重複をdev側に一本化し、game側はゲーム専門知識に特化 | **推奨** |
| B. 共通部分を第3のプラグインに抽出 | dev-core的なプラグインを新設 | プラグイン3つの整合管理になり、個人マーケットプレイスには過剰 |
| C. 同期スクリプトでコピーを自動追随 | dev→gameへ定期コピー | 二重管理を自動化するだけで根治しない |

### 4.2 A案の具体設計

役割を「**汎用ワークフロー = dev-workflow**」「**ゲーム専門知識 = game-studio-workflow**」で完全分離する。

#### (1) game側から重複4スキルを削除

`coding-standards` / `coding-standards-creator` / `behavior-verification` / `implementation-workflow` を削除し、dev-workflow側（code-knowledge体系 + implementer/verifier/reviewer agents）に一本化する。

- game側READMEとsession-startフックで「dev-workflow必須」を明示・検出する
- 削除により untracked の `config/language_packs.json` 問題も消滅する

#### (2) game側の進化分はdev側に吸収: 実装agent選択制

game版implementation-workflowの「specialist agent委譲」は価値があるため、dev-workflowのStage 3を**実装agent選択制**にする:

- 設計書に `Implementer: game-studio-workflow:gameplay-programmer` のように実装担当agentを記録
- オーケストレーターは指定agentに**成果物プロトコル（implementation_output.md形式）をプロンプトで渡して**起動
- 未指定なら従来どおり汎用 `implementer` agent

これでgame版workflowは削除可能になり、ゲーム以外のプロジェクトでも専門agent差し替えが使えるようになる。

#### (3) 知識システムをcode-knowledgeに統一: パック発見機構の拡張

`list_knowledge.py` に**マルチルート探索**を追加し、以下もスキャンする:

- 他プラグインの規約ディレクトリ: `plugins/*/knowledge-packs/*/metadata.json`
- プロジェクトローカル: `.claude/knowledge-packs/`

効果:

- game側は `rules/`（11ファイル）と `engine-reference/` を **game-studio-workflow内のknowledge packとして提供**でき、ロード機構はdev-workflowの1つだけになる
- パックの中身は各プラグインが所有（ゲーム知識はgame側、汎用はdev側）し、**機構とコンテンツの所有を分離**できる
- エンジン知識はgodot/unreal用のstructuredパック（core.md + examples + sections）へ段階的に移行。unityはdev側パックと統合

#### (4) game側に残すもの

- 48 agents（エンジン分割は改善③として任意）
- ゲーム特化スキル: design-systemのGDDモード、team-*、sprint-plan、playtest-report、balance-check 等
- hooks、production管理（sprints / milestones / session-state）
- `design-system` の汎用設計モードと `code-review` のゲーム固有チェックリストは、それぞれdev側スキル / reviewer agentへの**薄い委譲 + ゲーム固有差分のみ**に縮小

---

## 5. 推奨実施順

1. **改善①②**: フックのプラグイン登録・パス修正（動作不全の解消）
2. **回避策(1)(2)**: 重複スキル削除 + dev-workflow Stage 3のagent選択制
3. **回避策(3)**: code-knowledgeマルチルート探索 + rules/engine-referenceのパック化
4. **改善③**: エンジン別プラグイン分割（任意・効果はコンテキスト削減）

---

## 付録: dev-workflow v2.0.0 の前提（参照）

- 相談（design-discussion）はメインスレッド、作業（実装・検証・レビュー）は自律agent（implementer / verifier / reviewer）。成果物は `requests/{prefix}/` のファイル経由で受け渡し
- code-knowledge（旧coding-standards）はナレッジパック3層構造: core.md（致命的制約 + ❌/✅対訳、~2KB、常時注入）/ examples（ゴールデンサンプル）/ sections（詳細、オンデマンド）
- パック作成の勘所は `code-knowledge-creator/SKILL.md` に明文化済み
