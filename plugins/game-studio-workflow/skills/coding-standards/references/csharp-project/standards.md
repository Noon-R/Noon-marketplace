# C# Project コーディング規約

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
public User? FindUser(int userID) // nullable reference type
public IEnumerable<User> GetUsers() // 空のコレクション返却
public bool TryGetUser(int userID, out User user) // try pattern

// ❌ 避ける
public User FindUser(int userID) // nullを返す可能性があるが型で表現されていない
```

## 5. 非同期プログラミング

### 5.1 非同期メソッドの命名
```csharp
// ✅ 正しい
public async Task<User> GetUserAsync(int userID)
public async Task SaveUserAsync(User user)
public async Task DeleteUserAsync(int userID)

// ❌ 間違い
public async Task<User> GetUser(int userID) // Asyncサフィックスなし
```

### 5.2 ConfigureAwait の使用
```csharp
// ライブラリコードでは ConfigureAwait(false) を使用
public async Task<string> GetDataAsync()
{
    HttpResponseMessage response = await _HttpClient.GetAsync(url).ConfigureAwait(false);
    string content = await response.Content.ReadAsStringAsync().ConfigureAwait(false);
    return content;
}
```

## 6. コメントとドキュメント

### 6.1 XMLドキュメントコメント
```csharp
/// <summary>
/// 指定されたIDのユーザーを取得します。
/// </summary>
/// <param name="userID">取得するユーザーのID</param>
/// <returns>ユーザー情報。見つからない場合はnull</returns>
/// <exception cref="ArgumentException">userIDが0以下の場合</exception>
public async Task<User?> GetUserAsync(int userID)
{
    if (userID <= 0)
    {
        throw new ArgumentException("IDは1以上である必要があります", nameof(userID));
    }

    return await _Repository.FindByIDAsync(userID);
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
        // TODO: 在庫切れの通知機能を実装
        throw new InvalidOperationException("商品が在庫切れです");
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
public string BuildMessage(IEnumerable<string> items)
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

## 8. var キーワードの使用

### 8.1 var使用の原則
- **右辺から型が明確に判断できる場合のみ**使用する
- 可読性を優先し、型が不明確な場合は明示的に宣言

### 8.2 var使用が適切な場合
```csharp
// ✅ 適切: 右辺から型が明確
var user = new User();
var users = new List<User>();
var result = _UserService.GetUserAsync(userID);
var dictionary = new Dictionary<string, int>();

// LINQ結果の匿名型
var userInfo = users.Select(u => new { u.Name, u.Email });

// 型推論が複雑な場合
var query = from u in users
            join o in orders on u.ID equals o.UserID
            select new { u.Name, o.Total };
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
Task<User> userTask = GetUserAsync(userID);
```

## 9. 例外処理

### 9.1 例外の種類
```csharp
// ✅ 適切な例外を使用
public void ValidateAge(int age)
{
    if (age < 0)
    {
        throw new ArgumentOutOfRangeException(nameof(age), "年齢は0以上である必要があります");
    }

    if (age > 150)
    {
        throw new ArgumentOutOfRangeException(nameof(age), "年齢は150以下である必要があります");
    }
}

public async Task<User> GetUserAsync(int userID)
{
    User? user = await _Repository.FindByIDAsync(userID);
    if (user == null)
    {
        throw new NotFoundException($"ID {userID} のユーザーが見つかりません");
    }

    return user;
}
```

### 9.2 例外処理のパターン
```csharp
// ✅ 正しい例外処理
try
{
    await ProcessDataAsync();
}
catch (SpecificException ex)
{
    _Logger.LogError(ex, "データ処理中にエラーが発生しました");
    throw; // 再スロー
}
catch (Exception ex)
{
    _Logger.LogError(ex, "予期しないエラーが発生しました");
    throw new ApplicationException("データ処理に失敗しました", ex);
}
```

## 10. LINQ とコレクション

### 10.1 LINQ の使用
```csharp
// ✅ 推奨: メソッド構文
List<string> activeUserNames = users
    .Where(u => u.IsActive)
    .OrderBy(u => u.Name)
    .Select(u => u.Name)
    .ToList();

// ✅ 複雑な場合はクエリ構文も可
var result = from user in users
             join order in orders on user.ID equals order.UserID
             where user.IsActive && order.Status == ORDER_STATUS.COMPLETED
             select new { user.Name, order.Total };
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

// C# 12以降のコレクション式
string[] array = ["item1", "item2", "item3"];
List<string> list = ["item1", "item2", "item3"];
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
// Nullable参照型を活用 (.NET 6+)
#nullable enable

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

    public T? Find(Func<T, bool> predicate)
    {
        return _Items.FirstOrDefault(predicate);
    }
}
```

### 11.4 Record型
```csharp
// 不変のデータ転送オブジェクトにRecord型を使用
public record UserDto(string Name, string Email, DateTime CreatedAt);

// With式で新しいインスタンスを作成
var updatedUser = user with { Email = "new@email.com" };
```

## 12. テスト

### 12.1 ユニットテスト
```csharp
// Arrange-Act-Assert パターン
[Fact]
public async Task GetUserAsync_ValidID_ReturnsUser()
{
    // Arrange
    var mockRepository = new Mock<IUserRepository>();
    mockRepository.Setup(r => r.FindByIDAsync(1))
                  .ReturnsAsync(new User { ID = 1, Name = "Test" });
    var service = new UserService(mockRepository.Object);

    // Act
    var result = await service.GetUserAsync(1);

    // Assert
    Assert.NotNull(result);
    Assert.Equal("Test", result.Name);
}
```

### 12.2 統合テスト
```csharp
public class UserApiTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _Client;

    public UserApiTests(WebApplicationFactory<Program> factory)
    {
        _Client = factory.CreateClient();
    }

    [Fact]
    public async Task GetUser_ReturnsSuccess()
    {
        // Act
        var response = await _Client.GetAsync("/api/users/1");

        // Assert
        response.EnsureSuccessStatusCode();
    }
}
```

## 13. セキュリティ

### 13.1 入力検証
```csharp
public async Task<User> CreateUserAsync(CreateUserRequest request)
{
    // 入力検証
    if (string.IsNullOrWhiteSpace(request.Name))
    {
        throw new ArgumentException("名前は必須です", nameof(request.Name));
    }

    if (request.Name.Length > 100)
    {
        throw new ArgumentException("名前は100文字以内にしてください", nameof(request.Name));
    }

    if (!IsValidEmail(request.Email))
    {
        throw new ArgumentException("無効なメールアドレスです", nameof(request.Email));
    }

    return await _Repository.CreateAsync(request);
}
```

### 13.2 SQLインジェクション対策
```csharp
// ✅ 正しい: パラメータ化クエリ
public async Task<User?> FindByNameAsync(string name)
{
    using var connection = new SqlConnection(_ConnectionString);
    return await connection.QueryFirstOrDefaultAsync<User>(
        "SELECT * FROM Users WHERE Name = @Name",
        new { Name = name }
    );
}

// ❌ 危険: 文字列連結
public async Task<User?> FindByNameAsync_Unsafe(string name)
{
    var sql = $"SELECT * FROM Users WHERE Name = '{name}'"; // SQLインジェクションの脆弱性
    // ...
}
```

### 13.3 機密データの保護
```csharp
// 機密データをログに出力しない
public void ProcessPayment(PaymentRequest request)
{
    _Logger.LogInformation("Processing payment for order {OrderID}", request.OrderID);
    // ❌ _Logger.LogInformation("Card number: {CardNumber}", request.CardNumber);
}
```

## 14. ツール・設定

### 14.1 推奨ツール
- **IDE**: Visual Studio, Visual Studio Code, Rider
- **Linter**: Roslyn Analyzers, StyleCop
- **Formatter**: dotnet format
- **テスト**: xUnit, NUnit, MSTest
- **モック**: Moq, NSubstitute
- **CI/CD**: GitHub Actions, Azure DevOps

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

# C# specific
csharp_new_line_before_open_brace = all
csharp_indent_case_contents = true
csharp_indent_switch_labels = true
```

### 14.3 Directory.Build.props
```xml
<Project>
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
  </PropertyGroup>
</Project>
```

## 15. リソース

### 15.1 参考資料
- [Microsoft C# Coding Conventions](https://docs.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions)
- [.NET API Design Guidelines](https://docs.microsoft.com/en-us/dotnet/standard/design-guidelines/)
- [C# Language Reference](https://docs.microsoft.com/en-us/dotnet/csharp/language-reference/)

### 15.2 学習リソース
- [Microsoft Learn - C#](https://docs.microsoft.com/en-us/learn/paths/csharp-first-steps/)
- [C# Programming Guide](https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/)

---

## 更新履歴

| バージョン | 日付 | 変更内容 |
|-----------|------|---------|
| 1.0.0 | 2026-01-14 | 初版リリース |

*このコーディング規約は継続的に更新・改善していきます。*
