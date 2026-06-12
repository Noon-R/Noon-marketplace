---
name: implementation-workflow
description: |
  Orchestrate the full implementation workflow from requirements to completion.
  Use when user wants to start a new implementation task with full workflow support, or manage an ongoing implementation.
  Triggers include "機能を作りたい", "新しい機能を作りたい", "implementation workflow", "ワークフロー開始", or explicit workflow management requests.
  Design discussion runs interactively in the main thread; implementation, verification, and code review run as autonomous agents (implementer, verifier, reviewer) with file-based handoff.
---

Orchestrate the implementation workflow. **相談（設計）はメインスレッドで対話的に、作業（実装・検証・レビュー）は自律agentで実行**し、成果物ファイルで受け渡す。メインスレッドには進行管理とユーザー判断点だけを残し、コンテキストを小さく保つ。

## Stages

| Stage | 実行者 | 実行場所 | 成果物 |
|-------|--------|----------|--------|
| 1. Request | - | main | progress.md |
| 2. Design | design-discussion skill | **main（対話）** | {prefix}_design_output.md |
| 3. Implementation | **implementer agent** | subagent | {prefix}_implementation_output.md + コード |
| 4. Verification | **verifier agent** | subagent | {prefix}_verification_output.md |
| 4.5 User Decision | ユーザー | main | - |
| 5. Code Review | **reviewer agent** | subagent | {prefix}_code_review_output.md |
| 5.5 Review Decision | ユーザー | main | - |

## Initialization

1. **Prefix抽出**: リクエストの主要概念を小文字ASCII+アンダースコアに変換（"ログイン機能の実装" → `login`）。20文字以内。ユーザーに確認:
   > プレフィックス「{prefix}」を使用します。変更希望があればお知らせください。
2. **ディレクトリ作成**: `requests/{prefix}/` と `requests/{prefix}/backup/`
3. **progress.md作成**:

```markdown
# Implementation Progress: {Feature Name}

## Request
{original request}

## Prefix
{prefix}

## Knowledge Pack
{設計段階で決定。例: unity}

## Stage History
| Stage | Status | Timestamp | Notes |
|-------|--------|-----------|-------|

## Checkpoints
| Timestamp | Backup Path |

## Issues Log
```

## Stage Transitions

### Stage 2: Design（メインスレッド・対話）

design-discussionスキルを使い、ユーザーと対話しながら設計する。出力先: `requests/{prefix}/{prefix}_design_output.md`。設計書には**使用するナレッジパックのキーを必ず記録**する（implementer agentがロードするため）。完了後チェックポイント作成。

### Stage 3: Implementation（implementer agent）

Agentツールで **implementer** agentを起動する。プロンプトに含めるもの:

- 設計書パス: `requests/{prefix}/{prefix}_design_output.md`
- 出力パス: `requests/{prefix}/{prefix}_implementation_output.md`
- 実装先ディレクトリ
- 再実行時: Issues Logの該当問題リスト

agentの要約から **Open Questionsと設計乖離の有無を確認**し、あればユーザーに提示して判断を仰ぐ。完了後チェックポイント作成。

### Stage 4: Verification（verifier agent）

Agentツールで **verifier** agentを起動する。プロンプトに含めるもの:

- 実装報告書パス・設計書パス
- 出力パス: `requests/{prefix}/{prefix}_verification_output.md`

agentが自動検証（制約スキャン・ビルド・テスト）を実行し、手動チェックリストを生成する。**自動検証で問題が見つかった場合はStage 4.5を待たずユーザーに報告**する。

### Stage 4.5: User Decision

検証報告書の手動チェックリストをユーザーに提示し、実施を依頼:

| 選択 | アクション |
|------|-----------|
| ✓ 確認完了 | チェックポイント作成 → Stage 5へ |
| ✗ 修正が必要 | 問題をIssues Logに記録 → Stage 3へ差し戻し（問題リストをimplementerに渡す） |

### Stage 5: Code Review（reviewer agent）

Agentツールで **reviewer** agentを起動する。プロンプトに含めるもの:

- 実装報告書パス・設計書パス
- 出力パス: `requests/{prefix}/{prefix}_code_review_output.md`

### Stage 5.5: Review Decision

agentの判定に応じて:

- **Needs Revision**: Critical指摘をユーザーに提示 → 確認後Issues Logに記録しStage 3へ差し戻し
- **Approved / Approved with Comments**: チェックポイント作成 → ワークフロー完了。Should Fix項目は完了報告に添える

## Checkpoint Management

各ステージ完了時に `requests/{prefix}/backup/{YYYYMMDD_HHMMSS}/` へ全成果物をコピーし、progress.mdに記録する。復元要求時はチェックポイント一覧から選択させ、ファイルを書き戻す。

## Navigation & Resume

- **ジャンプ**: 「設計からやり直したい」→ チェックポイント作成後、該当ステージへ
- **再開**: progress.mdを読んで現在ステージを特定し、状況を報告して続行
- **agent失敗時**: progress.mdにエラーを記録し、リトライ/スキップ/中断をユーザーに確認

## Progress Display

ステージ変化のたびに表示:

```
📋 {Feature Name}  [✓設計 ●実装 ○検証 ○レビュー]  Last checkpoint: {timestamp}
```

## 運用原則

- 成果物の受け渡しは**必ずファイル経由**。agentの応答全文をメインスレッドに展開しない
- メインスレッドでコードを読み直さない（レビュー結果はreviewer agentの報告書で判断）
- ユーザーへの判断要求は Stage 4.5 / 5.5 と、agentが報告したOpen Questionsのみに絞る
