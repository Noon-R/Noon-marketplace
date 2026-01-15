# Learning Log

## エントリー

<!-- 以下に自動的にエントリーが追加されます -->

### 2026-01-06 07:56 - メモ
IID_PPV_ARGSは安全にキャストするための仕組み

**🤖 AI補足 (07:57):**
IID_PPV_ARGSマクロは、COMインターフェースポインタ取得時に__uuidof()でIIDを自動抽出し、型チェックをコンパイル時に行うことで、IIDとポインタ型の不一致を防ぎます。QueryInterfaceやCoCreateInstanceで広く使用され、DirectXでも頻繁に見られます。

> 📚 参照:
> [IID_PPV_ARGS macro - Microsoft Learn](https://learn.microsoft.com/en-us/windows/win32/api/combaseapi/nf-combaseapi-iid_ppv_args), [COM Coding Practices - Microsoft Learn](https://learn.microsoft.com/en-us/windows/win32/learnwin32/com-coding-practices)
