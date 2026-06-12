# Unity LINQとコレクション（詳細） 🔴 CRITICAL

## ❌ LINQは禁止

UnityではLINQ（System.Linq）の使用を**禁止**する。foreach/forループで代替する。

```csharp
// ❌ 禁止: LINQの使用
using System.Linq; // このusingは禁止

List<string> activeUserNames = users
    .Where(u => u.IsActive)
    .OrderBy(u => u.Name)
    .Select(u => u.Name)
    .ToList();

// ✅ 推奨: foreach/forループで代替
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

## LINQの代替パターン集

```csharp
// Where の代替
List<User> FilterActiveUsers(List<User> users)
{
    List<User> result = new List<User>();
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

## コレクションの初期化

```csharp
// ✅ 推奨: コレクション初期化子
var list = new List<string> { "item1", "item2", "item3" };
var dict = new Dictionary<string, int>
{
    { "key1", 1 },
    { "key2", 2 }
};
```
