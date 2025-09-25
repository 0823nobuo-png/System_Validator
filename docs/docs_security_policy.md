# System Validator / Theaterverse Final
セキュリティポリシー

---

## 1. 認証/認可
- 認証: DB 内ユーザテーブル (`users`) による。
- パスワードは bcrypt ハッシュ (`passlib[bcrypt]`)。
- 認可: `config/config_rbac_roles.yaml` に基づく RBAC。

## 2. ログ/監査
- すべてのエラー・警告は JSON Lines 形式で構造化ログに保存。
- 監査ログ (`audit_logs`) は DB に保存し、保持期間は 180 日。

## 3. ネットワーク
- API バインドは `0.0.0.0` に制限。
- 外部通信は最小限 (LLM 接続など)。
- DB はローカルネットワーク内のみアクセス許可。

## 4. バックアップ
- バックアップファイルは `/var/backups/` に保存。
- `plugin_backup_verifier` により日次で検証。
- 失敗時はアラートログを生成。

## 5. 秘密情報
- `.env` ファイルに格納。
- 権限は `chmod 600`。
- Git 管理対象外。

## 6. 脆弱性対応
- 依存ライブラリは週次で更新確認。
- CI で `pip-audit` / `npm audit` を実行。

## 7. 将来拡張
- OIDC 連携を検討。
- TLS 終端を systemd ではなくリバースプロキシ (nginx/caddy) で実装予定。

--- END OF STRUCTURE ---
<!-- /root/System_Validator/APP_DIR/theaterverse_final/docs/docs_security_policy.md -->

/root/System_Validator/APP_DIR/theaterverse_final/docs/docs_security_policy.md
--- END OF STRUCTURE ---
