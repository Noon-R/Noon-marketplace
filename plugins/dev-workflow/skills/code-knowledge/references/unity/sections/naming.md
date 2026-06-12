# Unity 命名規則（詳細）

## 基本原則
- **英語を使用**し、略語は避ける
- **意味のある名前**を付ける
- **一貫性**を保つ

## ケース規則

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

## 特別な命名規則

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
