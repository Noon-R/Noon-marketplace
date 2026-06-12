# Unity エラー処理（詳細） 🔴 CRITICAL

## ❌ try-catch例外処理は禁止

Unityではtry-catchによる例外処理を**禁止**する。エラーは戻り値で表現する。

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
```

## Result型パターン

```csharp
public readonly struct Result<T>
{
    public bool IsSuccess { get; }
    public T Value { get; }
    public string ErrorMessage { get; }

    private Result(bool isSuccess, T value, string errorMessage)
    {
        IsSuccess = isSuccess;
        Value = value;
        ErrorMessage = errorMessage;
    }

    public static Result<T> Success(T value) => new Result<T>(true, value, null);
    public static Result<T> Failure(string error) => new Result<T>(false, default, error);
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

## TryPattern

```csharp
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

## 入力検証

公開メソッドの入口で検証し、不正値はResult/falseで返す。

```csharp
public Result<User> CreateUser(string name, string email)
{
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

## 使い分けの指針

| 状況 | 選択 |
|------|------|
| 失敗理由をユーザー/ログに伝える必要がある | Result<T> |
| 単純な成否と値の取得 | TryPattern |
| 失敗があり得ない内部処理 | 通常の戻り値 + 事前条件チェック |
