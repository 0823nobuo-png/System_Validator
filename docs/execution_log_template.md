# 実行ログ雛形（記入テンプレート）

正式パス：/root/System_Validator/APP_DIR/theaterverse_final/docs/execution_log_template.md

---

## 0. メタ情報
- 実行日: YYYY-MM-DD
- 実行者: （氏名/ID）
- 環境: dev / staging / prod
- リリースID: releases/2025-09-06_xxx
- 参照チェックリスト: `docs/final_completion_checklist.md`

---

## 1. systemd 起動検証
- コマンド:
  ```bash
  sudo systemctl status system_validator --no-pager
  journalctl -u system_validator -n 200 --no-pager
  ```
- 結果: ✅ / ❌
- 主要ログ抜粋:
  -
- 課題/対処:
  -

---

## 2. Secrets 生成（sops/Vault）
- 生成手順/コマンド:
  ```bash
  # 例: sops -d secrets.enc.env > .env
  ```
- リポジトリに平文秘匿値なし（確認方法）: ✅ / ❌
- 課題/対処:
  -

---

## 3. LLM 疎通
- コマンド/手順:
  ```bash
  python -m core.core_adapter_llm
  curl -s http://127.0.0.1:8000/v1/chat -X POST -H 'Content-Type: application/json' -d '{"messages":[{"role":"user","content":"ping"}]}'
  ```
- 応答（要約）:
  -
- フェイルオーバ試験（片系停止時）: ✅ / ❌  概要:
- レート制御/再試行の確認: ✅ / ❌  概要:
- 課題/対処:
  -

---

## 4. OIDC/JWT 検証
- 手順:
  ```bash
  # Discovery/JWKS 取得
  curl -s https://<issuer>/.well-known/openid-configuration | jq .jwks_uri
  # アクセストークン検証（テストトークン）
  ```
- 検証結果: ✅ / ❌  詳細:
- スコープ/ロール適用テスト: ✅ / ❌  詳細:
- 監査ログ記録（auth_audit_logs）: ✅ / ❌
- 課題/対処:
  -

---

## 5. DB/DR 演習
- 実行:
  ```bash
  bash scripts/dr_restore_test.sh
  ```
- レポート: `dr_restore_report.txt` （保存場所リンク）
- 結果: ✅ / ❌  概要:
- RTO/RPO（実測）: RTO=__ / RPO=__
- 課題/対処:
  -

---

## 6. CI/CD（SBOM・SAST・Audit）
- 実行ログ（CIリンク）:
- SBOM生成: ✅ / ❌  ファイル: `sbom.json`
- pip-audit / npm audit / bandit / eslint: 主要警告と対応:
  -

---

## 7. 可観測性（OTEL & Prometheus）
- Collector接続/エンドポイント:
- トレース確認（URL/スクショ）:
- メトリクス確認（ダッシュボードURL/スクショ）:
- 課題/対処:
  -

---

## 8. Blue/Green 切替
- 実行:
  ```bash
  NEW_RELEASE=<dir> HEALTH_URL=http://127.0.0.1:8000/health python scripts/deploy_bluegreen.py
  ```
- 結果: ✅ / ❌  概要:
- ロールバック試験: ✅ / ❌  概要:
- 通知（Slack/メール）: 到達/未達

---

## 9. セキュリティ・ハードニング確認
- `validator` ユーザ作成と権限: ✅ / ❌
- ReadOnlyPaths/ReadWritePaths の妥当性: ✅ / ❌
- ジャーナルに危険警告なし: ✅ / ❌

---

## 10. サインオフ
- 重大/高リスク: 0 / N 件
- 総合判定: ✅ リリース可 / ❌ 要修正
- 承認者サイン: ________  日時: ________

---

--- END OF STRUCTURE ---
<!-- /root/System_Validator/APP_DIR/theaterverse_final/docs/execution_log_template.md -->

/root/System_Validator/APP_DIR/theaterverse_final/docs/execution_log_template.md
--- END OF STRUCTURE ---
