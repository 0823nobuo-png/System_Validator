# System Validator / Theaterverse Final
バックアップ & リカバリ手順

---

## バックアップ
- 日次ジョブ: `systemd/systemd_timer_backup_verify.timer`
- バックアップファイル: `/var/backups/system_validator.dump`
- 実行スクリプト: `scripts/script_db_dump.sh`

### 手動実行
```bash
./scripts/script_db_dump.sh
```

## リカバリ
- 実行スクリプト: `scripts/script_db_restore.sh`
- 使用ファイル: `/var/backups/system_validator.dump`

### 手動実行
```bash
./scripts/script_db_restore.sh /var/backups/system_validator.dump
```

## 検証
- プラグイン: `plugin_backup_verifier`
- エンドポイント: `/backup/verify`
- 成功: `{ status: "ok" }`
- 失敗: `{ status: "error" }` or `{ status: "missing" }`

## 運用上の注意
- バックアップは最低 7 世代保持。
- `audit_logs` に結果を保存。
- 定期的にリカバリ演習を実施。

--- END OF STRUCTURE ---
<!-- /root/System_Validator/APP_DIR/theaterverse_final/docs/docs_backup_and_recovery.md -->

/root/System_Validator/APP_DIR/theaterverse_final/docs/docs_backup_and_recovery.md
--- END OF STRUCTURE ---
