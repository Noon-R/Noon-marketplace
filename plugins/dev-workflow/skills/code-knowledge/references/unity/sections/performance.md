# Unity パフォーマンス（詳細）

## 文字列操作

```csharp
// ✅ 推奨: StringBuilderを使用
public string BuildMessage(List<string> items)
{
    StringBuilder builder = new StringBuilder();
    foreach (string item in items)
    {
        builder.AppendLine($"Item: {item}");
    }
    return builder.ToString();
}

// ✅ 推奨: string interpolation
string message = $"Hello, {name}! Today is {DateTime.Now:yyyy-MM-dd}";

// ❌ 避ける: ループ内の文字列連結
string result = "";
foreach (string item in items)
{
    result += item + "\n"; // 毎回新しい文字列を生成しGCを圧迫する
}
```

## コレクションの選択

```csharp
public class UserCache
{
    // 高速なキー検索が必要 → Dictionary
    private readonly Dictionary<int, User> _UserDictionary = new();

    // 順序付きで重複を許可しない → SortedSet
    private readonly SortedSet<string> _SortedUserNames = new();

    // シンプルな列挙 → List
    private readonly List<User> _UserList = new();
}
```

## Unity固有のパフォーマンス

```csharp
// ✅ 推奨: GetComponentのキャッシュ
private Transform _Transform;

private void Awake()
{
    _Transform = GetComponent<Transform>();
}

// ❌ 禁止: 毎フレームのGetComponent呼び出し
private void Update()
{
    GetComponent<Transform>().position = newPosition;
}
```

その他の指針:
- `Update`内でのアロケーション（`new`、文字列生成、クロージャ）を避ける
- 頻繁な生成・破棄はオブジェクトプールを検討する
- `Camera.main`もキャッシュする（内部でFindGameObjectWithTagが走る）
