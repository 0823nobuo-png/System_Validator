# DR演習 Runbook（バックアップ検証）

正式パス：/root/System_Validator/APP_DIR/theaterverse_final/docs/runbook_dr.md

---

## 目的
- 直近バックアップのリストア可否と整合性を自動検証し、RTO/RPO を可視化

## 手順
1. 変数確認：`BACKUP_DIR`, `PG*` などを環境に設定
2. 実行：
   ```bash
   bash scripts/dr_restore_test.sh
   ```
3. レポート確認：`dr_restore_report.txt`
4. エラーの場合：CIを非0で終了 → 原因切り分け（権限/スキーマ/ダンプ形式）

## 成功基準
- DR用DBへのリストアが成功
- 主要テーブルのサンプル参照が成功

---

--- END OF STRUCTURE ---
<!-- /root/System_Validator/APP_DIR/theaterverse_final/docs/runbook_dr.md -->

/root/System_Validator/APP_DIR/theaterverse_final/docs/runbook_dr.md
--- END OF STRUCTURE ---
