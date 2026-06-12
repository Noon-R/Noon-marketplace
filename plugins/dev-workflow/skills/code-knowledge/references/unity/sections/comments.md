# Unity コメントとドキュメント（詳細）

## XMLドキュメントコメント

公開APIには`<summary>`を記述する。

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

## インラインコメント

「何をしているか」ではなく「なぜそうしているか」を書く。

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
