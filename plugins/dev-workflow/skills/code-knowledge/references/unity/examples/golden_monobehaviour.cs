// ゴールデンサンプル: MonoBehaviour
// 体現している規約: SerializeFieldの使い方 / Awakeでのコンポーネントキャッシュ /
//                  コルーチンによる非同期 / 例外を投げないエラー処理 / ライフサイクルの構成順
using System.Collections;
using UnityEngine;

namespace Game.Player
{
    /// <summary>
    /// プレイヤーの体力管理と被ダメージ演出を担当するコンポーネント。
    /// </summary>
    public class PlayerHealth : MonoBehaviour
    {
        // 2. フィールド（インスペクタ公開はSerializeField付きprivateを使用）
        public const int MAX_HEALTH = 100;

        [SerializeField] private float _InvincibleDuration = 1.5f;
        [SerializeField] private SpriteRenderer _BodyRenderer;

        private Transform _Transform;
        private int _CurrentHealth;
        private bool _IsInvincible;

        // 4. プロパティ
        public int CurrentHealth => _CurrentHealth;
        public bool IsDead => _CurrentHealth <= 0;

        // 5. Unityライフサイクル（Awake → OnEnable → Start → Update の順に記述）
        private void Awake()
        {
            // GetComponentはAwakeで一度だけ実行してキャッシュする
            _Transform = GetComponent<Transform>();
            _CurrentHealth = MAX_HEALTH;
        }

        private void Update()
        {
            // 毎フレームのGetComponent呼び出しは禁止。キャッシュ済み参照を使う
            if (_Transform.position.y < -10f && !IsDead)
            {
                ApplyDamage(MAX_HEALTH);
            }
        }

        // 6. publicメソッド

        /// <summary>
        /// ダメージを適用します。無敵中・死亡済みの場合は適用されません。
        /// </summary>
        /// <param name="amount">ダメージ量（1以上）</param>
        /// <returns>ダメージが適用された場合はtrue</returns>
        public bool ApplyDamage(int amount)
        {
            // 例外は投げず、適用可否をboolで返す
            if (amount <= 0 || _IsInvincible || IsDead)
            {
                return false;
            }

            _CurrentHealth = Mathf.Max(0, _CurrentHealth - amount);

            if (!IsDead)
            {
                StartCoroutine(InvincibleCoroutine());
            }

            return true;
        }

        // 7. privateメソッド・コルーチン
        private IEnumerator InvincibleCoroutine()
        {
            _IsInvincible = true;
            _BodyRenderer.color = new Color(1f, 1f, 1f, 0.5f);

            yield return new WaitForSeconds(_InvincibleDuration);

            _BodyRenderer.color = Color.white;
            _IsInvincible = false;
        }
    }
}
