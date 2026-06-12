# Unity 非同期プログラミング（詳細）

## Unity非同期パターン

```csharp
// ✅ 正しい: コルーチンを使用（標準）
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

// ❌ 禁止: Task（Unityではスレッド・ライフサイクルの問題が発生する）
public async Task<User> GetUserTask(int userID)
{
    await Task.Delay(100);
    return new User();
}
```

## 使い分けの指針

| 状況 | 選択 |
|------|------|
| フレーム待機・時間待機・簡単な逐次処理 | コルーチン |
| 戻り値が必要な非同期処理 | UniTask（導入済みの場合） |
| UniTask未導入で戻り値が必要 | コールバック + コルーチン |

## 注意点
- コルーチンはGameObjectの破棄で停止する。破棄をまたぐ処理には使わない
- `StartCoroutine`の多重起動に注意。必要なら実行中フラグで抑止する
