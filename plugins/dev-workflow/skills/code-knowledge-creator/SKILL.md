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

code-knowledgeスキル用のナレッジパック（コーディング規約・技術制約・模範サンプル）を作成・更新するスキル。**良いパックは「量」ではなく「ロード効率と遵守率」で決まる**。以下の設計原則（勘所）に必ず従って作成する。

---

## 設計原則（勘所）— パック作成前に必ず読む

### 原則1: 3層構造と分離基準

知識は「いつロードされるか」で3層に分ける。**全部入りの1ファイルを作ってはならない**（コンテキストを圧迫し、肝心の制約が埋もれて遵守率が下がる）。

| 層 | 内容 | サイズ予算 | ロードタイミング |
|----|------|-----------|----------------|
| **core.md** | 致命的制約 + 必須スタイル要点 | **~2KB厳守** | 常時（実装agentに注入） |
| **examples/** | ゴールデンサンプル | 1ファイル~100行 | 実装開始前 |
| **sections/** | トピック別詳細規約 | 各1-4KB | 疑問が生じたときだけ |

**分離の判断基準:**
- 「違反したら即リジェクト」レベルの制約 → core.md
- 「迷ったときに参照する」詳細・背景・パターン集 → sections/
- 「文章で説明するより見せたほうが早い」流儀 → examples/

### 原則2: LLMが言われなくても守ることは書かない

Claudeは「意味のある変数名を付ける」「単一責任にする」を指示なしでも概ね守る。そういう一般論はcore.mdに入れない。**書く価値があるのは、デフォルト挙動と違うことだけ**:

- ✅ 書く価値が高い: 「LINQ禁止」「try-catch禁止」「privateフィールドは`_PascalCase`」（Claudeのデフォルトは`_camelCase`）「enum値はSNAKE_CASE」
- ❌ 書く価値が低い: 「クラスはPascalCase」「メソッドは動詞で始める」「意味のある名前を付ける」

ユーザーへのヒアリングでも「一般的なC#/言語標準と**違うところはどこですか**」を最優先で聞く。

### 原則3: 禁止事項は必ず ❌/✅ 対訳にする

禁止形だけ示しても、代替手段がわからなければ破られる。core.mdの致命的制約には必ず**書き換え対**（5〜10行）を付ける:

```csharp
// ❌ var actives = users.Where(u => u.IsActive).ToList();
// ✅
List<User> actives = new List<User>();
foreach (User user in users)
{
    if (user.IsActive) { actives.Add(user); }
}
```

### 原則4: ゴールデンサンプルは「規約の交差点」として設計する

ルール別の細切れスニペットを大量に作るのではなく、**1ファイルで多数の規約を同時に体現する完成形コード**を作る。トークン効率が圧倒的に高く、LLMはルール散文よりコードの模倣に強く従う。

- **1ドメイン1ファイル**: コードの種類ごとに分ける（例: Unity = 一般クラス用 + MonoBehaviour用）
- **~100行以内**: 長いサンプルは読まれないし模倣の焦点がぼける
- **実コンパイル可能**: 疑似コードは禁止。質の低いサンプルはルール散文より害が大きい（悪い癖ごと模倣される）
- **冒頭コメントで体現規約を列挙**: 「このファイルが何の見本か」を明示する
- **設計時の確認**: 命名・構成順序・エラー処理・禁止事項の代替が1ファイルに全部現れているかをチェックリスト的に確認する

参照実装: `code-knowledge/references/unity/examples/golden_service.cs`

### 原則5: sections/は索引で引けるようにする

各セクションはmetadata.jsonの`sections`に**1行のdescription付き**で登録する。実装agentはdescriptionだけを見て「読むかどうか」を判断するため、descriptionには中身が推測できる具体語を入れる（「エラー処理の詳細」ではなく「try-catch禁止の詳細、Result<T>パターン、TryPattern、入力検証」）。

---

## Workflow: Create New Knowledge Pack

### Step 1: Gather Sample Code（推奨）

ユーザーの既存コード・プロジェクトがあれば読み、以下を抽出する:

- **デフォルトと違う規約**（原則2の観点で。これがcore.md候補）
- 命名・構成パターン（ゴールデンサンプルの素材）
- 禁止されているAPI・パターン（❌/✅対訳の素材）

サンプルがなければ言語標準（C#ならMicrosoftガイドライン等）を出発点に、「標準と変えたいところ」をヒアリングする。

### Step 2: Define Pack

- Pack key（例: "unity"）、display name、対象フレームワーク、検索keywords

### Step 3: Scaffold

```bash
python scripts/knowledge_pack_creator.py create <pack_key> --name "Display Name" --keywords kw1 kw2
```

`core.md` + `sections/`（雛形5種: naming, formatting, class-design, error-handling, testing）+ `examples/`（空）+ `metadata.json` が生成される。

### Step 4: Write core.md（最重要・原則2,3を適用）

1. 致命的制約を❌/✅対訳で記述（通常3〜6個。10個を超えるなら本当に致命的か見直す）
2. 必須スタイル要点を表形式で（デフォルトと違うものだけ）
3. **2KB以内に収める**。超えたら詳細をsections/へ移す

### Step 5: Create Golden Samples（原則4を適用）

1. コードドメインを特定（例: サービスクラス / UIコンポーネント / テスト）
2. ドメインごとに~100行の完成形コードを書く
3. ユーザーにレビューしてもらう（「このコードがそのまま増殖してよいか?」）
4. metadata.jsonの`examples`にdescription付きで登録

### Step 6: Write sections/（原則5を適用)

詳細規約をトピック別に記述。不要な雛形は削除。各セクションをmetadata.jsonに具体的なdescription付きで登録。

### Step 7: Register & Validate

1. `config/knowledge_packs.json` に登録（`"format": "structured"`）
2. 検証: `python scripts/knowledge_pack_creator.py validate <pack_key>`
   - core.mdのサイズ超過・❌/✅対訳の欠落・examples未登録を警告する
3. `code-knowledge/scripts/generate_skill_content.py update` でSKILL.mdの動的セクションを更新
4. code-knowledgeスキルで新パックが引けることを確認

---

## Workflow: Migrate Monolithic Pack to Structured

旧形式（standards.md一枚岩）のパックを3層構造に移行する:

1. standards.mdを読み、**致命的制約**（🔴 CRITICAL相当）を抽出 → core.mdへ（❌/✅対訳に整形）
2. 散在するコード例を**ゴールデンサンプルに統合・蒸留** → examples/へ
3. 残りの詳細をトピック別に分割 → sections/へ（関連する章は1ファイルにまとめてよい）
4. metadata.jsonを`"format": "structured"`に書き換え、sections索引とexamplesを登録
5. standards.mdを削除し、knowledge_packs.jsonを更新
6. validateと動的コンテンツ更新を実行

参照例: unityパックの移行（15章 → core.md + 2サンプル + 10セクション）

---

## Workflow: Update Existing Pack

1. **更新種別の特定**: 制約追加/緩和、セクション加筆、サンプル更新、誤り修正
2. **更新先の判断（原則1の分離基準で）**:
   - 新しい禁止事項 → core.md（対訳付き）+ 必要ならsections/に詳細
   - 詳細パターンの追加 → sections/のみ
   - 流儀の変更 → **ゴールデンサンプルも必ず更新**（サンプルと規約の矛盾は最悪の状態。LLMはサンプルに従う）
3. metadata.jsonの`version`と`last_updated`を更新
4. validate実行 → 動的コンテンツ更新

---

## Quality Checklist

パック完成時に確認:

- [ ] core.mdは2KB以内か
- [ ] 致命的制約すべてに❌/✅対訳があるか
- [ ] core.mdに「LLMが言われなくても守る一般論」が混ざっていないか
- [ ] ゴールデンサンプルはコンパイル可能か（可能ならビルドで確認）
- [ ] サンプルがcore.md・sections/の規約と矛盾していないか
- [ ] metadata.jsonのsections descriptionは具体的か（中身が推測できるか)
- [ ] knowledge_packs.jsonに登録され、動的コンテンツが更新されているか

## Implementation Details

- `scripts/knowledge_pack_creator.py`: scaffold生成・構造検証ユーティリティ（structured/monolithic両対応）
