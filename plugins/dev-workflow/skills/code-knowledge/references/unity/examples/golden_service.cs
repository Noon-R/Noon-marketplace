// ゴールデンサンプル: 一般クラス（非MonoBehaviour）
// 体現している規約: クラス構成順序 / 命名規則 / Result<T>・TryPatternによるエラー表現 /
//                  LINQ非使用（foreach代替） / XMLドキュメントコメント / 入力検証
using System;
using System.Collections.Generic;
using System.Text;

namespace Game.Core
{
    public enum USER_STATUS
    {
        ACTIVE,
        SUSPENDED,
        WITHDRAWN
    }

    /// <summary>
    /// 処理結果を成功/失敗の戻り値で表現する構造体。例外の代替として使用する。
    /// </summary>
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

    /// <summary>
    /// ユーザー情報の検索と表示名整形を担当するサービス。
    /// </summary>
    public class UserService
    {
        // 1. イベント
        public event EventHandler<EventArgs> UserRegistered;

        // 2. フィールド（定数 → static → instance、各 public → private 順）
        public const int MAX_NAME_LENGTH = 100;
        private const int MIN_USER_ID = 1;

        private readonly Dictionary<int, User> _UserCache = new Dictionary<int, User>();
        private bool _IsInitialized;

        // 3. コンストラクタ
        public UserService()
        {
            _IsInitialized = true;
        }

        // 4. プロパティ
        public bool IsInitialized => _IsInitialized;
        public int CachedUserCount => _UserCache.Count;

        // 5. メソッド（public → private 順）

        /// <summary>
        /// 指定されたIDのユーザーを取得します。
        /// </summary>
        /// <param name="userID">取得するユーザーのID</param>
        /// <param name="user">見つかったユーザー。見つからない場合はnull</param>
        /// <returns>ユーザーが見つかった場合はtrue</returns>
        public bool TryGetUser(int userID, out User user)
        {
            user = null;

            if (userID < MIN_USER_ID)
            {
                return false;
            }

            return _UserCache.TryGetValue(userID, out user);
        }

        /// <summary>
        /// ユーザーを登録します。検証エラーはResult型で返します。
        /// </summary>
        public Result<User> RegisterUser(int userID, string name)
        {
            if (userID < MIN_USER_ID)
            {
                return Result<User>.Failure($"IDは{MIN_USER_ID}以上である必要があります");
            }

            if (string.IsNullOrWhiteSpace(name) || name.Length > MAX_NAME_LENGTH)
            {
                return Result<User>.Failure($"名前は1〜{MAX_NAME_LENGTH}文字で指定してください");
            }

            User user = new User(userID, name, USER_STATUS.ACTIVE);
            _UserCache[userID] = user;
            UserRegistered?.Invoke(this, EventArgs.Empty);

            return Result<User>.Success(user);
        }

        /// <summary>
        /// アクティブなユーザー名の一覧を取得します。
        /// </summary>
        public List<string> GetActiveUserNames()
        {
            // LINQのWhere/Selectは使用せず、foreachで抽出する
            List<string> activeNames = new List<string>();
            foreach (User user in _UserCache.Values)
            {
                if (user.Status == USER_STATUS.ACTIVE)
                {
                    activeNames.Add(user.Name);
                }
            }
            activeNames.Sort();
            return activeNames;
        }

        /// <summary>
        /// ユーザー一覧の表示用テキストを構築します。
        /// </summary>
        public string BuildUserListText(List<string> userNames)
        {
            // 繰り返しの文字列連結はStringBuilderを使用する
            StringBuilder builder = new StringBuilder();
            foreach (string userName in userNames)
            {
                builder.AppendLine($"User: {userName}");
            }
            return builder.ToString();
        }
    }

    public class User
    {
        private readonly int _UserID;

        public User(int userID, string name, USER_STATUS status)
        {
            _UserID = userID;
            Name = name;
            Status = status;
        }

        public int UserID => _UserID;
        public string Name { get; private set; }
        public USER_STATUS Status { get; private set; }
    }
}
