# セキュリティポリシー（強化⑦）

正式パス：/root/System_Validator/APP_DIR/theaterverse_final/docs/security_policies.md

---

## 1. systemd ハードニング方針
- **Least Privilege**: `User=validator`, `Group=validator` を使用し root 常駐を禁止。
- **FS保護**: `ProtectSystem=strict`, `ProtectHome=true`, `ReadOnlyPaths`/`ReadWritePaths` を明示。
- **権限縮小**: `NoNewPrivileges=true`, `CapabilityBoundingSet=` を空に。
- **ランタイム隔離**: `PrivateTmp=true`, `LockPersonality=true`, `MemoryDenyWriteExecute=true`。
- **シスコール制限**: `SystemCallFilter` で必要最小限のセットに限定。

## 2. シークレット管理（sops/Vault）
- `.env` の平文秘匿値を廃止し、**sops** で暗号化した `secrets.enc.env` を管理。
- もしくは **HashiCorp Vault** を使用し、起動時に `EnvironmentFile` を生成。
- 監査観点：復号処理は systemd `ExecStartPre` で行い、**標準出力に出さない**。

## 3. OIDC/JWT 構成の安全基準
- `auth_oidc_settings.yaml` の `require_https: true` を維持。
- `algorithms` は `RS256/ES256` 等の非対称鍵を使用。
- `clock_skew_seconds` は 60 秒以下を推奨。
- スコープは最小権限で設計し、`admin:ops` は限定ロールのみ。

## 4. 監査ログ
- 監査テーブル `auth_audit_logs` を使用し、**ユーザID・リクエストID**（可能なら）を付与。
- 監査ログは **改ざん検知**のため WORM ストレージまたは外部転送を検討。

## 5. Blue/Green とロールバック
- `deploy_bluegreen.py` で **アトミック切替**（シンボリックリンク）を採用。
- 失敗時は直前の `current` を自動復帰。

## 6. 運用手順（抜粋）
1. `validator` ユーザ作成と権限設定。
2. `system_validator.service` を `/etc/systemd/system/` に配置し `daemon-reload`。
3. `EnvironmentFile` の秘匿値を sops/Vault から生成。
4. `systemctl enable --now system_validator.service`。
5. Grafana/Prometheus 接続を確認しダッシュボードをインポート。

---

--- END OF STRUCTURE ---
<!-- /root/System_Validator/APP_DIR/theaterverse_final/docs/security_policies.md -->

/root/System_Validator/APP_DIR/theaterverse_final/docs/security_policies.md
--- END OF STRUCTURE ---
