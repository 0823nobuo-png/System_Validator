# System Validator / Theaterverse Final
実行検証シナリオ（OneClick → Blue/Green → systemd → E2E → Backup）

---

## 前提
- OS: Ubuntu 22.04 LTS
- 事前に `.env` 設置、PostgreSQL 起動、`requirements.txt` 導入済み

---

## 1) 命名/構成ゲート
```bash
python ./scripts/script_validator_naming_guard.py
python ./scripts/script_manifest_renamer.py
```
**判定**: どちらもエラー出力が無いこと。

---

## 2) スキーマ/契約検証
```bash
pytest tests/tests_contracts_openapi.py -q
```
**判定**: 0 failed。

---

## 3) DB マイグレーション & シード
```bash
./scripts/script_db_migrate.sh
psql "$SYSTEM_VALIDATOR_DSN" -f db/db_seeds_minimal.sql
```
**判定**: エラーなく終了。

---

## 4) One-Click 起動
```bash
./scripts/script_oneclick_boot.sh
```
**判定**:
```bash
curl -s http://localhost:8080/health | jq -r .status  # → ok
```

---

## 5) Blue/Green 切替
```bash
./scripts/script_deploy_bluegreen.sh B
```
**判定**: 切替後に `/health`=ok。失敗時に自動ロールバックが行われること。

---

## 6) systemd 常駐
```bash
sudo cp systemd/systemd_service_api.service /etc/systemd/system/system_validator.service
sudo systemctl daemon-reload
sudo systemctl enable --now system_validator.service
systemctl is-active system_validator   # → active
```
**判定**: active。

---

## 7) 観測/メトリクス
```bash
curl -I http://localhost:8080/metrics
curl -s http://localhost:8080/metrics/prometheus | head -n 5
```
**判定**: 200 応答、Prometheus フォーマットでメトリクス表示。

---

## 8) E2E/性能スモーク
```bash
pytest -q tests/tests_e2e_smoke.py
pytest -q tests/tests_perf_smoke.py
```
**判定**: 0 failed、ヘルス応答 < 1.0s。

---

## 9) バックアップ & 検証
```bash
./scripts/script_db_dump.sh
curl -s http://localhost:8080/backup/verify | jq
```
**判定**: `{ "status": "ok" }`。

---

## 10) CI 最小実行
```bash
pytest -q
```
**判定**: 0 failed。

---

## 付記: 代表的な失敗パターンと対処
- **`SYSTEM_VALIDATOR_DSN` 未設定**: `.env` を再確認、`script_env_setup.sh` 実行。
- **`/ui/dist` 不在**: `ui/` で `npm ci && npm run build`。
- **`/backup/verify` missing**: `/var/backups/system_validator.dump` を作成（`script_db_dump.sh`）後に再実行。
- **systemd 起動しない**: `journalctl -u system_validator -e`、ExecStart のパス整合性確認。

--- END OF STRUCTURE ---
<!-- /root/System_Validator/APP_DIR/theaterverse_final/docs/docs_validation_scenarios.md -->

/root/System_Validator/APP_DIR/theaterverse_final/docs/docs_validation_scenarios.md
--- END OF STRUCTURE ---
