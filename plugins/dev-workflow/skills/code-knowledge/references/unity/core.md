# Unity Core Constraints（常時適用・違反禁止）

> このファイルは実装agentのコンテキストに常時注入される。違反は即リジェクト対象。
> 詳細規約は `sections/`、模範コードは `examples/` を参照。

## 🔴 致命的制約（❌→✅ 書き換え対訳）

### 1. LINQ禁止（`using System.Linq;` を書かない）

```csharp
// ❌ var actives = users.Where(u => u.IsActive).ToList();
// ✅
List<User> actives = new List<User>();
foreach (User user in users)
{
    if (user.IsActive) { actives.Add(user); }
}
```

### 2. try-catch例外処理禁止（エラーは戻り値で表現）

```csharp
// ❌ try { return _Repository.FindByID(id); } catch (Exception ex) { return null; }
// ✅ TryPattern または Result<T>
public bool TryGetUser(int userID, out User user)
{
    user = userID > 0 ? _Repository.FindByID(userID) : null;
    return user != null;
}
```

### 3. Task禁止（非同期はコルーチンまたはUniTask）

```csharp
// ❌ public async Task<User> GetUserAsync(int id)
// ✅ public IEnumerator LoadDataCoroutine()        （標準）
// ✅ public async UniTask<User> GetUserAsync(int id) （UniTask導入時）
```

### 4. Update内でのGetComponent禁止（Awakeでキャッシュ）

```csharp
// ❌ void Update() { GetComponent<Transform>().position = pos; }
// ✅ void Awake() { _Transform = GetComponent<Transform>(); }
```

## 🔴 必須スタイル（要点のみ）

| 項目 | ルール |
|------|--------|
| privateフィールド | `_PascalCase`（`_UserName`） |
| 定数・enum型・enum値 | `SNAKE_CASE`（`MAX_COUNT`, `ORDER_STATUS.PENDING`） |
| ID表記 | `UserID` / `userID`（`Id` の混在ケース禁止） |
| if文 | 1行でも必ず `{ }` ブロック |
| 波括弧 | 新しい行に配置（Allman） |
| インデント | 4スペース、行長120文字まで |
| var | 右辺から型が自明な `new` のときのみ |
| クラス構成順 | イベント→フィールド→コンストラクタ→プロパティ→メソッド（各 public→private 順） |

実装前に `examples/golden_service.cs`（一般クラス）と `examples/golden_monobehaviour.cs`（MonoBehaviour）を読むこと。迷ったらサンプルの書き方に合わせる。
