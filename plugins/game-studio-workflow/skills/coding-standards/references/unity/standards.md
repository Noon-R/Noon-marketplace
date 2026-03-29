# Unity コーディング規約

> **重要な制約**
> - ❌ **LINQ禁止**: `using System.Linq;` を使用しない。foreach/forループで代替
> - ❌ **try-catch例外処理禁止**: 例外をスローせず、戻り値でエラーを表現

## 1. 命名規則

### 1.1 基本原則
- **英語を使用**し、略語は避ける
- **意味のある名前**を付ける
- **一貫性**を保つ

### 1.2 ケース規則

| 要素 | ケース | 例 |
|------|--------|-----|
| クラス | PascalCase | `UserService`, `OrderManager` |
| インターフェース | PascalCase (I接頭辞) | `IUserService`, `IRepository` |
| メソッド | PascalCase | `GetUser()`, `SaveOrder()` |
| プロパティ | PascalCase | `FirstName`, `IsActive` |
| フィールド (public) | PascalCase | `MaxRetryCount` |
| フィールド (private) | _PascalCase (_接頭辞) | `_UserName`, `_IsInitialized` |
| 変数・パラメータ | camelCase | `userName`, `orderCount` |
| 定数 | SNAKE_CASE | `MAX_CONNECTION_COUNT` |
| 列挙型 | SNAKE_CASE | `ORDER_STATUS` |
| 列挙値 | SNAKE_CASE | `ORDER_STATUS.PENDING` |

### 1.3 特別な命名規則
```csharp
// イベント: 動詞 + ed/ing
public event EventHandler<UserEventArgs> UserCreated;
public event EventHandler<UserEventArgs> UserCreating;

// Boolean: Is/Has/Can + 形容詞
public bool IsActive { get; set; }
public bool HasChildren { get; set; }
public bool CanEdit { get; set; }

// コレクション: 複数形
public List<User> Users { get; set; }
public Dictionary<string, Order> Orders { get; set; }

// ID の表記: I と D は同じケースにする
public int UserID { get; set; }     // PascalCaseの場合
public int userID;                  // camelCaseの場合
public int USER_ID;                 // SNAKE_CASEの場合
// ❌ 避ける: Id (大文字と小文字の混在)
```

## 2. フォーマット・レイアウト

### 2.1 インデント
- **4スペース**を使用（タブは使用しない）
- ネストレベルごとに4スペース追加

### 2.2 波括弧の配置
```csharp
// ✅ 正しい: 新しい行に配置
public class User
{
    public string Name { get; set; }

    public void DoSomething()
    {
        if (condition)
        {
            // 処理
        }
    }
}

// ❌ 間違い: 同じ行に配置
public class User {
    // ...
}
```

### 2.3 空白の使用
```csharp
// ✅ 正しい
public void Method(int param1, string param2)
{
    int result = param1 + 10;
    if (result > 0 && param2 != null)
    {
        // 処理
    }
}

// ❌ 間違い
public void Method(int param1,string param2)
{
    var result=param1+10;
    if(result>0&&param2!=null)
    {
        // 処理
    }
}
```

### 2.4 if文の書き方
```csharp
// ✅ 正しい: 1行でも必ずブロックで囲む
if (condition)
{
    DoSomething();
}

if (user != null)
{
    return user.Name;
}

// ❌ 間違い: ブロックなしの記述
if (condition)
    DoSomething();

if (user != null)
    return user.Name;
```

### 2.5 行の長さ
- **120文字**を上限とする
- 長い行は適切な位置で改行する

## 3. クラス設計

### 3.1 クラスの構成順序
```csharp
public class ExampleClass
{
    // 1. イベント
    // アクセスレベル順: public → internal → protected → private
    public event EventHandler<EventArgs> SomethingHappened;
    private event EventHandler<EventArgs> InternalEvent;

    // 2. フィールド (定数 → static → instance)
    // アクセスレベル順: public → internal → protected → private
    public const int MAX_COUNT = 100;
    private const int MIN_COUNT = 1;

    public static readonly string DefaultName = "Default";
    private static readonly Logger _Logger = new Logger();

    public readonly string PublicField;
    private readonly string _Name;
    private bool _IsInitialized;

    // 3. コンストラクタ
    // アクセスレベル順: public → internal → protected → private
    public ExampleClass(string name)
    {
        _Name = name;
    }

    private ExampleClass()
    {
        _Name = string.Empty;
    }

    // 4. プロパティ
    // アクセスレベル順: public → internal → protected → private
    public string Name => _Name;
    public bool IsInitialized
    {
        get => _IsInitialized;
        private set => _IsInitialized = value;
    }

    internal string InternalProperty { get; set; }
    protected string ProtectedProperty { get; set; }
    private string PrivateProperty { get; set; }

    // 5. メソッド
    // アクセスレベル順: public → internal → protected → private
    public void Initialize()
    {
        // 実装
    }

    internal void InternalMethod()
    {
        // 実装
    }

    protected void ProtectedMethod()
    {
        // 実装
    }

    private void PrivateMethod()
    {
        // 実装
    }
}
```

### 3.2 アクセス修飾子
- **最小限の公開レベル**を使用
- 明示的にアクセス修飾子を記述

```csharp
// ✅ 正しい
public class User
{
    private readonly string _ID;

    public string Name { get; private set; }

    internal void InternalMethod() { }

    private void PrivateMethod() { }
}
```

## 4. メソッド設計

### 4.1 メソッドの責任
- **単一責任の原則**に従う
- メソッド名は動作を明確に表現

### 4.2 パラメータ
- **4個以下**を推奨
- 多い場合はオブジェクトでグループ化

```csharp
// ✅ 推奨
public void CreateUser(CreateUserRequest request)
{
    // 実装
}

public class CreateUserRequest
{
    public string Name { get; set; }
    public string Email { get; set; }
    public DateTime BirthDate { get; set; }
    public string PhoneNumber { get; set; }
}

// ❌ 避ける
public void CreateUser(string name, string email, DateTime birthDate, string phoneNumber)
{
    // 実装
}
```

### 4.3 戻り値
- `null`の代わりに適切な型を使用

```csharp
// ✅ 推奨
public User FindUser(int userID, out bool found) // out パラメータでエラー表現
public IEnumerable<User> GetUsers() // 空のコレクション返却
public bool TryGetUser(int userID, out User user) // try pattern

// ❌ 避ける（Unityでは例外禁止のため）
public User FindUser(int userID) // nullを返す可能性があるが型で表現されていない
```

## 5. 非同期プログラミング

### 5.1 Unity非同期パターン
```csharp
// ✅ 正しい: コルーチンを使用
public IEnumerator LoadDataCoroutine()
{
    yield return new WaitForSeconds(1f);
    // 処理
}

// ✅ 正しい: UniTask（推奨ライブラリ）を使用
public async UniTask<User> GetUserAsync(int userID)
{
    await UniTask.Delay(100);
    return new User();
}

// ❌ 避ける: Task（Unity では問題が発生する可能性）
public async Task<User> GetUserTask(int userID)
{
    await Task.Delay(100);
    return new User();
}
```

## 6. コメントとドキュメント

### 6.1 XMLドキュメントコメント
```csharp
/// <summary>
/// 指定されたIDのユーザーを取得します。
/// </summary>
/// <param name="userID">取得するユーザーのID</param>
/// <param name="found">ユーザーが見つかったかどうか</param>
/// <returns>ユーザー情報。見つからない場合はnull</returns>
public User GetUser(int userID, out bool found)
{
    if (userID <= 0)
    {
        found = false;
        return null;
    }

    found = true;
    return _Repository.FindByID(userID);
}
```

### 6.2 インラインコメント
```csharp
public void ProcessOrder(Order order)
{
    // 在庫確認は外部サービスを呼び出すため時間がかかる可能性がある
    bool isAvailable = _InventoryService.CheckAvailability(order.ProductID);

    if (!isAvailable)
    {
        // 在庫切れの場合は処理を中断
        order.Status = ORDER_STATUS.OUT_OF_STOCK;
        return;
    }

    // 計算ロジックが複雑なため別メソッドに分離
    decimal totalAmount = CalculateOrderTotal(order);

    order.TotalAmount = totalAmount;
}
```

## 7. パフォーマンス考慮事項

### 7.1 文字列操作
```csharp
// ✅ 推奨: StringBuilderを使用
public string BuildMessage(List<string> items)
{
    var sb = new StringBuilder();
    foreach (string item in items)
    {
        sb.AppendLine($"Item: {item}");
    }
    return sb.ToString();
}

// ✅ 推奨: string interpolation
string message = $"Hello, {name}! Today is {DateTime.Now:yyyy-MM-dd}";

// ❌ 避ける: 大量の文字列連結
string result = "";
foreach (string item in items)
{
    result += item + "\n"; // パフォーマンスが悪い
}
```

### 7.2 コレクションの選択
```csharp
// 用途に応じた適切なコレクションを選択
public class UserCache
{
    // 高速な検索が必要
    private readonly Dictionary<int, User> _UserDictionary = new();

    // 順序付きで重複を許可しない
    private readonly SortedSet<string> _SortedUserNames = new();

    // シンプルなリスト
    private readonly List<User> _UserList = new();
}
```

### 7.3 Unity固有のパフォーマンス
```csharp
// ✅ 推奨: GetComponent のキャッシュ
private Transform _Transform;

private void Awake()
{
    _Transform = GetComponent<Transform>();
}

// ❌ 避ける: 毎フレームのGetComponent呼び出し
private void Update()
{
    GetComponent<Transform>().position = newPosition; // 毎フレーム呼び出しは重い
}
```

## 8. var キーワードの使用

### 8.1 var使用の原則
- **右辺から型が明確に判断できる場合のみ**使用する
- 可読性を優先し、型が不明確な場合は明示的に宣言

### 8.2 var使用が適切な場合
```csharp
// ✅ 適切: 右辺から型が明確
var user = new User();
var users = new List<User>();
var dictionary = new Dictionary<string, int>();
```

### 8.3 var使用を避けるべき場合
```csharp
// ❌ 避ける: 右辺から型が不明確
string name = GetName(); // 戻り値の型が不明確
int count = CalculateCount(); // 戻り値の型が不明確
bool isValid = ValidateInput(); // 戻り値の型が不明確

// ✅ 推奨: 明示的な型宣言
string name = GetName();
List<User> activeUsers = GetActiveUsers();
```

## 9. 例外処理 🔴 **CRITICAL: 禁止事項**

### 9.1 ❌ try-catch 例外処理は禁止

Unityでは try-catch による例外処理を**禁止**します。代わりに戻り値でエラーを表現してください。

```csharp
// ❌ 禁止: try-catchの使用
public User GetUser(int userID)
{
    try
    {
        return _Repository.FindByID(userID);
    }
    catch (Exception ex)
    {
        Debug.LogError(ex.Message);
        return null;
    }
}

// ✅ 推奨: 戻り値でエラー表現（Result型パターン）
public struct Result<T>
{
    public bool IsSuccess { get; }
    public T Value { get; }
    public string ErrorMessage { get; }

    public static Result<T> Success(T value) => new Result<T>(true, value, null);
    public static Result<T> Failure(string error) => new Result<T>(false, default, error);

    private Result(bool isSuccess, T value, string errorMessage)
    {
        IsSuccess = isSuccess;
        Value = value;
        ErrorMessage = errorMessage;
    }
}

public Result<User> GetUser(int userID)
{
    if (userID <= 0)
    {
        return Result<User>.Failure("IDは1以上である必要があります");
    }

    User user = _Repository.FindByID(userID);
    if (user == null)
    {
        return Result<User>.Failure($"ID {userID} のユーザーが見つかりません");
    }

    return Result<User>.Success(user);
}
```

### 9.2 TryPatternの使用
```csharp
// ✅ 推奨: TryPatternでエラーを処理
public bool TryGetUser(int userID, out User user)
{
    user = null;

    if (userID <= 0)
    {
        return false;
    }

    user = _Repository.FindByID(userID);
    return user != null;
}

// 使用例
if (TryGetUser(123, out User user))
{
    Debug.Log($"Found user: {user.Name}");
}
else
{
    Debug.LogWarning("User not found");
}
```

## 10. LINQ とコレクション 🔴 **CRITICAL: 禁止事項**

### 10.1 ❌ LINQ は禁止

Unityでは LINQ（System.Linq）の使用を**禁止**します。代わりに foreach/for ループを使用してください。

```csharp
// ❌ 禁止: LINQの使用
using System.Linq; // この using は禁止

List<string> activeUserNames = users
    .Where(u => u.IsActive)
    .OrderBy(u => u.Name)
    .Select(u => u.Name)
    .ToList();

// ✅ 推奨: foreach/for ループで代替
List<string> activeUserNames = new List<string>();
foreach (User user in users)
{
    if (user.IsActive)
    {
        activeUserNames.Add(user.Name);
    }
}
activeUserNames.Sort();
```

### 10.2 コレクションの初期化
```csharp
// ✅ 推奨
var list = new List<string> { "item1", "item2", "item3" };
var dict = new Dictionary<string, int>
{
    { "key1", 1 },
    { "key2", 2 }
};
```

### 10.3 LINQの代替パターン

```csharp
// Where の代替
List<User> FilterActiveUsers(List<User> users)
{
    var result = new List<User>();
    foreach (User user in users)
    {
        if (user.IsActive)
        {
            result.Add(user);
        }
    }
    return result;
}

// FirstOrDefault の代替
User FindFirstActiveUser(List<User> users)
{
    foreach (User user in users)
    {
        if (user.IsActive)
        {
            return user;
        }
    }
    return null;
}

// Any の代替
bool HasActiveUsers(List<User> users)
{
    foreach (User user in users)
    {
        if (user.IsActive)
        {
            return true;
        }
    }
    return false;
}

// Count の代替
int CountActiveUsers(List<User> users)
{
    int count = 0;
    foreach (User user in users)
    {
        if (user.IsActive)
        {
            count++;
        }
    }
    return count;
}
```

## 11. 型システム

### 11.1 型アノテーション
```csharp
// ✅ 推奨: 明示的な型宣言
string name = GetName();
List<User> activeUsers = GetActiveUsers();
Dictionary<int, string> mapping = new Dictionary<int, string>();
```

### 11.2 Nullable参照型
```csharp
// Nullable参照型を活用
public User? FindUser(int userID)
{
    // nullを返す可能性がある場合は明示
}

public string GetUserName(User user)
{
    // nullを返さない場合
}
```

### 11.3 ジェネリクス
```csharp
// 適切にジェネリクスを活用
public class Repository<T> where T : class
{
    private readonly List<T> _Items = new List<T>();

    public void Add(T item)
    {
        _Items.Add(item);
    }

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

## 12. テスト

### 12.1 ユニットテスト
```csharp
// Arrange-Act-Assert パターン
[Test]
public void GetUser_ValidID_ReturnsUser()
{
    // Arrange
    var repository = new UserRepository();
    repository.Add(new User { ID = 1, Name = "Test" });

    // Act
    bool found = repository.TryGetUser(1, out User result);

    // Assert
    Assert.IsTrue(found);
    Assert.AreEqual("Test", result.Name);
}
```

### 12.2 Unity Test Framework
```csharp
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;

public class PlayerTests
{
    [Test]
    public void Player_TakeDamage_ReducesHealth()
    {
        // Arrange
        var player = new Player { Health = 100 };

        // Act
        player.TakeDamage(30);

        // Assert
        Assert.AreEqual(70, player.Health);
    }
}
```

## 13. セキュリティ

### 13.1 入力検証
```csharp
public Result<User> CreateUser(string name, string email)
{
    // 入力検証
    if (string.IsNullOrWhiteSpace(name))
    {
        return Result<User>.Failure("名前は必須です");
    }

    if (name.Length > 100)
    {
        return Result<User>.Failure("名前は100文字以内にしてください");
    }

    if (!IsValidEmail(email))
    {
        return Result<User>.Failure("無効なメールアドレスです");
    }

    return Result<User>.Success(new User { Name = name, Email = email });
}
```

### 13.2 データ保護
```csharp
// 機密データの保護
public class SecureData
{
    private string _EncryptedPassword;

    public void SetPassword(string password)
    {
        _EncryptedPassword = Encrypt(password);
    }

    // パスワードを直接公開しない
    public bool ValidatePassword(string input)
    {
        return Encrypt(input) == _EncryptedPassword;
    }
}
```

## 14. ツール・設定

### 14.1 推奨ツール
- **IDE**: Visual Studio, Rider
- **コード分析**: Roslyn Analyzers
- **バージョン管理**: Git

### 14.2 EditorConfig
```ini
# .editorconfig
root = true

[*.cs]
indent_style = space
indent_size = 4
end_of_line = crlf
charset = utf-8-bom
trim_trailing_whitespace = true
insert_final_newline = true
```

### 14.3 Unity固有の設定
```csharp
// Assembly Definition を活用してコンパイル時間を短縮
// Editor スクリプトは Editor フォルダに配置
// プラットフォーム固有のコードは #if で分岐
#if UNITY_EDITOR
    // Editor専用コード
#endif
```

## 15. リソース

### 15.1 参考資料
- [Unity Documentation](https://docs.unity3d.com/)
- [Microsoft C# Coding Conventions](https://docs.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions)
- [Unity Best Practices](https://unity.com/how-to)

### 15.2 学習リソース
- Unity Learn
- C# Programming Guide

---

## 更新履歴

| バージョン | 日付 | 変更内容 |
|-----------|------|---------|
| 1.0.0 | 2026-01-14 | 初版リリース |

*このコーディング規約は継続的に更新・改善していきます。*
