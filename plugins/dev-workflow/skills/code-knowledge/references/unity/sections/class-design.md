# Unity クラス・メソッド設計（詳細）

## クラスの構成順序

メンバーは以下の順で記述する。各カテゴリ内はアクセスレベル順（public → internal → protected → private）。

```csharp
public class ExampleClass
{
    // 1. イベント
    public event EventHandler<EventArgs> SomethingHappened;

    // 2. フィールド (定数 → static → instance)
    public const int MAX_COUNT = 100;
    private const int MIN_COUNT = 1;

    public static readonly string DefaultName = "Default";
    private static readonly Logger _Logger = new Logger();

    private readonly string _Name;
    private bool _IsInitialized;

    // 3. コンストラクタ
    public ExampleClass(string name)
    {
        _Name = name;
    }

    // 4. プロパティ
    public string Name => _Name;
    public bool IsInitialized
    {
        get => _IsInitialized;
        private set => _IsInitialized = value;
    }

    // 5. メソッド
    public void Initialize() { }
    internal void InternalMethod() { }
    protected void ProtectedMethod() { }
    private void PrivateMethod() { }
}
```

## アクセス修飾子
- **最小限の公開レベル**を使用
- 明示的にアクセス修飾子を記述（省略しない）

## メソッド設計

### 責任
- **単一責任の原則**に従う
- メソッド名は動作を明確に表現

### パラメータ
- **4個以下**を推奨。多い場合はオブジェクトでグループ化

```csharp
// ✅ 推奨
public void CreateUser(CreateUserRequest request) { }

// ❌ 避ける
public void CreateUser(string name, string email, DateTime birthDate, string phoneNumber) { }
```

### 戻り値
- `null`の代わりにエラーを型で表現する（例外禁止のため）

```csharp
// ✅ 推奨
public bool TryGetUser(int userID, out User user)   // try pattern
public IEnumerable<User> GetUsers()                  // 空のコレクション返却
public Result<User> FindUser(int userID)            // Result型

// ❌ 避ける: nullを返す可能性が型で表現されていない
public User FindUser(int userID)
```

## 型システム

### Nullable参照型

```csharp
// nullを返す可能性がある場合は明示
public User? FindUser(int userID) { }
```

### ジェネリクス

```csharp
public class Repository<T> where T : class
{
    private readonly List<T> _Items = new List<T>();

    public T Find(Predicate<T> predicate)
    {
        foreach (T item in _Items)
        {
            if (predicate(item))
            {
                return item;
            }
        }
        return null;
    }
}
```
