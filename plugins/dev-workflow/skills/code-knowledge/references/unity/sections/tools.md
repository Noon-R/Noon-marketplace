# Unity ツール・設定・リソース（詳細）

## 推奨ツール
- **IDE**: Visual Studio, Rider
- **コード分析**: Roslyn Analyzers
- **バージョン管理**: Git

## EditorConfig

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

## Unity固有の設定

```csharp
// Assembly Definition を活用してコンパイル時間を短縮
// Editor スクリプトは Editor フォルダに配置
// プラットフォーム固有のコードは #if で分岐
#if UNITY_EDITOR
    // Editor専用コード
#endif
```

## 参考資料
- [Unity Documentation](https://docs.unity3d.com/)
- [Microsoft C# Coding Conventions](https://docs.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions)
- [Unity Best Practices](https://unity.com/how-to)
