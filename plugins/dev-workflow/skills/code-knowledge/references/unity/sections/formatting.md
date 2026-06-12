# Unity フォーマット・レイアウト（詳細）

## インデント
- **4スペース**を使用（タブは使用しない）
- ネストレベルごとに4スペース追加

## 波括弧の配置

```csharp
// ✅ 正しい: 新しい行に配置（Allman）
public class User
{
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

## 空白の使用

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

## if文の書き方

```csharp
// ✅ 正しい: 1行でも必ずブロックで囲む
if (condition)
{
    DoSomething();
}

// ❌ 間違い: ブロックなしの記述
if (condition)
    DoSomething();
```

## 行の長さ
- **120文字**を上限とする
- 長い行は適切な位置で改行する

## varキーワード

### 使用原則
- **右辺から型が明確に判断できる場合のみ**使用する
- 可読性を優先し、型が不明確な場合は明示的に宣言

```csharp
// ✅ 適切: 右辺から型が明確
var user = new User();
var users = new List<User>();
var dictionary = new Dictionary<string, int>();

// ❌ 避ける: 右辺から型が不明確
var name = GetName();        // 戻り値の型が不明確
var count = CalculateCount();

// ✅ 推奨: 明示的な型宣言
string name = GetName();
List<User> activeUsers = GetActiveUsers();
```
