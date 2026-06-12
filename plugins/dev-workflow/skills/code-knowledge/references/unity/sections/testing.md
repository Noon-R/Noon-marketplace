# Unity テストとセキュリティ（詳細）

## ユニットテスト

Arrange-Act-Assertパターンで記述する。テスト名は `対象_条件_期待結果`。

```csharp
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

## Unity Test Framework

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

## セキュリティ

### 入力検証

外部入力（ユーザー入力、ファイル、ネットワーク）は必ず検証し、不正値はResultで返す。

```csharp
public Result<User> CreateUser(string name, string email)
{
    if (string.IsNullOrWhiteSpace(name))
    {
        return Result<User>.Failure("名前は必須です");
    }

    if (!IsValidEmail(email))
    {
        return Result<User>.Failure("無効なメールアドレスです");
    }

    return Result<User>.Success(new User { Name = name, Email = email });
}
```

### データ保護

```csharp
// 機密データは平文で保持・公開しない
public class SecureData
{
    private string _EncryptedPassword;

    public void SetPassword(string password)
    {
        _EncryptedPassword = Encrypt(password);
    }

    public bool ValidatePassword(string input)
    {
        return Encrypt(input) == _EncryptedPassword;
    }
}
```
