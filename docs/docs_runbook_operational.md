# System Validator / Theaterverse Final
運用 Runbook（完全版）

---

## 1. 前提
- OS: Ubuntu 22.04 LTS ja-JP
- Python: 3.11+
- Node.js: 20+
- DB: PostgreSQL 15+（16 推奨）
- systemd 必須

## 2. セットアップ
```bash
./scripts/script_env_setup.sh
source .venv/bin/activate
pip install -r requirements.txt
./scripts/script_db_migrate.sh
psql "$SYSTEM_VALIDATOR_DSN" -f db/db_seeds_minimal.sql
```

## 3. ワンクリック起動
```bash
./scripts/script_oneclick_boot.sh
```
- 依存点検 → DB migration → UI build → API 起動

## 4. Blue/Green デプロイ
```bash
./scripts/script_deploy_bluegreen.sh B
```
- Slot 切替、ヘルスチェック、失敗時は即ロールバック

## 5. systemd 常駐
```bash
sudo cp systemd/systemd_service_api.service /etc/systemd/system/system_validator.service
sudo systemctl daemon-reload
sudo systemctl enable --now system_validator.service
```

バックアップ検証:
```bash
sudo cp systemd/systemd_service_backup_verify.service /etc/systemd/system/
sudo cp systemd/systemd_timer_backup_verify.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now systemd_timer_backup_verify.timer
```

## 6. テスト
```bash
pytest -q
```
- `tests/tests_e2e_smoke.py`: API ヘルス/メトリクス
- `tests/tests_perf_smoke.py`: レイテンシ
- `tests/tests_contracts_openapi.py`: OpenAPI 契約

## 7. バックアップ
```bash
./scripts/script_db_dump.sh
./scripts/script_db_restore.sh /var/backups/system_validator.dump
```

## 8. 観測性
- `/metrics/prometheus`: Prometheus 互換エンドポイント
- ログ: JSON Lines

## 9. トラブルシュート
- API 起動失敗: `.env` と DB 状況確認
- Blue/Green 切替失敗: `script_deploy_bluegreen.sh` のタイムアウト調整
- Backup 失敗: `plugins/plugin_backup_verifier/plugin_backup_verifier_job.py` ログ確認

---

## 10. ドキュメント連携
- `CHANGELOG_fusion_history.md`: 変更履歴
- `docs_change_log_fusion.md`: 融合差分記録
- `handover_fusion_plan.md`: 会話引き継ぎ資料

--- END OF STRUCTURE ---
<!-- /root/System_Validator/APP_DIR/theaterverse_final/docs/docs_runbook_operational.md -->

/root/System_Validator/APP_DIR/theaterverse_final/docs/docs_runbook_operational.md
--- END OF STRUCTURE ---
