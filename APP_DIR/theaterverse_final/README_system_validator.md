# System Validator / Theaterverse Final

**センタユニット不変＋プラグイン拡張**を原理とする本番運用向けアーキテクチャの最終版 README。対象 OS は **Ubuntu 22.04 LTS (ja-JP)**、DB は **PostgreSQL のみ**、Python は **3.11+** を前提にしています。ファイル命名規約は `<ユニット>_<機能>.<拡張子>`、区切りは `_` のみ、**同一プロジェクト内でベース名の重複禁止**（階層差あっても不可）。全ファイル末尾に `--- END OF STRUCTURE ---` を付与します。

## 1. 概要
- **Center Unit（不変核）**: `core/` 配下。イベントバス、設定ローダ、プラグイン登録、API ルータ、ポリシ、例外処理、ログ構成。
- **Plugin Unit（拡張）**: `plugins/` 配下。LLM アダプタ、ストレージ、モデレーション、デバッグ、UI、バックアップ検証、観測など。
- **運用導線（本実装）**: ワンクリック起動 → Blue/Green 切替 → systemd 常駐 → 監査/バックアップ/観測 → E2E/性能スモーク → CI 制御。

## 2. システム要件
- OS: Ubuntu 22.04 LTS（日本語環境可）
- CPU/GPU: 任意（LLM ローカル推論の前提に応じて調整）
- Python: 3.11 以上
- Node.js: 20 以上（UI ビルドに使用）
- PostgreSQL: 15 以上（運用は 16 を推奨）
- その他: systemd, bash, curl, openssl, git, make（任意）

## 3. インストール
```bash
# 1) Python / Node / PostgreSQL を導入（例: Ubuntu）
sudo apt update -y
sudo apt install -y python3.11 python3.11-venv python3.11-dev nodejs npm postgresql postgresql-contrib \
  systemd git curl make

# 2) リポジトリ配置（基準パスに従う）
#   /root は実環境で可変。以後の説明は /root を例示。
mkdir -p /root/System_Validator/APP_DIR/
cd /root/System_Validator/APP_DIR/
# theaterverse_final ディレクトリ一式がここに存在する前提

# 3) Python 仮想環境と依存導入
cd theaterverse_final
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 4) UI ビルド（必要に応じて）
# UI は "ui/" 配下（TS/TSX）。Node 20+ を推奨。
cd ui
npm ci || npm install
npm run build
cd ..

# 5) 初期 DB セットアップ（スキーマ & シード）
#   scripts/script_db_migrate.sh は db/db_migrations_core.sql を適用
#   scripts/script_db_dump.sh, script_db_restore.sh も参照
./scripts/script_env_setup.sh
./scripts/script_db_migrate.sh
# 任意: 初期データ
psql "$SYSTEM_VALIDATOR_DSN" -f db/db_seeds_minimal.sql
```

## 4. 環境変数
`.env` は `config/config_env_template.env` をコピーして編集します。

主要な例:
```
SYSTEM_VALIDATOR_ENV=production
SYSTEM_VALIDATOR_BASE_DIR=/root/System_Validator/APP_DIR/theaterverse_final
SYSTEM_VALIDATOR_DSN=postgresql://validator:validator@localhost:5432/validator
API_BIND_HOST=0.0.0.0
API_BIND_PORT=8080
UI_DIST_DIR=/root/System_Validator/APP_DIR/theaterverse_final/ui/dist
LOG_LEVEL=INFO
METRICS_PORT=9000
BLUEGREEN_SLOT=A
```

## 5. ディレクトリ構成（抜粋：決定版）
- `core/` 核心（不変）
- `plugins/` 機能（追加/削除可能）
- `scripts/` 運用スクリプト
- `systemd/` 常駐ユニットとタイマ
- `contracts/` スキーマと OpenAPI 守護
- `tests/` E2E・性能・契約テスト
- `docs/` 運用 Runbook、変更履歴、仕様

> 完全なツリーは `docs_runbook_operational.md` にも記載。

## 6. ワンクリック起動（本実装）
- `scripts/script_oneclick_boot.sh` は以下を**順次**実施します:
  1. 依存点検（Python/Node/psql）
  2. 必須プラグインの存在検査 & 契約整合性検証（`contracts/`）
  3. UI ビルド成果物の存在確認（`ui/dist`）
  4. DB マイグレーション適用（必要時）
  5. API/Router 起動（`core/core_api_server.py`）
  6. ヘルスチェック & メトリクス有効化

### 実行
```bash
./scripts/script_oneclick_boot.sh
```

## 7. Blue/Green デプロイ
- `scripts/script_deploy_bluegreen.sh` は **スロット A/B** を交互に切替えます。
  - ヘルスチェック失敗時は即時ロールバック。
  - 起動確認は HTTP ヘルスエンドポイント & DB 接続試験で実施。

### 実行
```bash
./scripts/script_deploy_bluegreen.sh --slot B   # 例: A→B に切替
```

## 8. systemd 常駐
- `systemd/systemd_service_api.service` を使用して API を常駐化。
- `systemd/systemd_service_backup_verify.service` + `systemd/systemd_timer_backup_verify.timer` でバックアップ検証を定期実行。

### 登録/起動例
```bash
sudo cp systemd/systemd_service_api.service /etc/systemd/system/system_validator.service
sudo systemctl daemon-reload
sudo systemctl enable --now system_validator.service

sudo cp systemd/systemd_service_backup_verify.service /etc/systemd/system/
sudo cp systemd/systemd_timer_backup_verify.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now systemd_timer_backup_verify.timer
```

## 9. PostgreSQL
- スキーマは `db/db_migrations_core.sql` に集約。
- 接続はプール `db/db_connection_pool.py` を使用。
- バックアップ/復旧は `scripts/script_db_dump.sh` / `scripts/script_db_restore.sh`。

### 健全性チェック
```bash
psql "$SYSTEM_VALIDATOR_DSN" -c "SELECT 1;"
```

## 10. セキュリティ
- RBAC: `config/config_rbac_roles.yaml`
- ポリシ: `core/core_security_policy.py`
- 秘密情報は `.env` 管理（ファイル権限 600 を推奨）
- 監査ログは DB へ保存（トリガ & Retention 方針は `db/db_migrations_core.sql`）

## 11. 観測性
- メトリクス: `plugins/plugin_observability_metrics` が Prometheus 互換の `/metrics` を提供
- ログ: 構造化ログ（JSON Lines）を標準出力 & ローテート
- 追跡: 主要ハンドラで処理時間/エラー率をサンプリング（`tools/tool_perf_sampler.py`）

## 12. バックアップ & 復旧
- `plugins/plugin_backup_verifier` が **日次検証**（systemd timer）を実行
- 失敗時はアラートログ（DB/標準出力）を生成し、Runbook に沿って復旧

## 13. テスト
- E2E スモーク: `tests/tests_e2e_smoke.py`
- 性能スモーク: `tests/tests_perf_smoke.py`
- 契約テスト: `tests/tests_contracts_openapi.py` / `contracts/*`
- Type/Lint: `ci/ci_lint_typecheck.yaml`

## 14. CI
- `ci/ci_pipeline_main.yaml` を基点に Contracts → Lint/Type → Unit/E2E → アーティファクト → デプロイ承認の順

## 15. トラブルシュート（抜粋）
- **起動しない**: `.env` 誤設定、DB 起動未確認、`ui/dist` 不在 → `script_env_setup.sh` と UI ビルドを再確認
- **DB 接続失敗**: DSN が実 DB と不整合、権限不足 → ロール作成＆権限付与
- **Blue/Green 失敗**: ヘルスエンドポイントの応答遅延 → `script_deploy_bluegreen.sh` のタイムアウト値を見直し

## 16. ライセンス/著作
- プロジェクトライセンスに従う（未設定の場合は私的利用限定）

---
**Immutable Core** の原則により、コア変更はプラグイン API を介した拡張優先で判断します。変更は `docs/docs_change_log_fusion.md` に記録し、OpenAPI/Contracts を必ず更新してください。

--- END OF STRUCTURE ---
<!-- /root/System_Validator/APP_DIR/theaterverse_final/README_system_validator.md -->

/root/System_Validator/APP_DIR/theaterverse_final/README_system_validator.md
--- END OF STRUCTURE ---
