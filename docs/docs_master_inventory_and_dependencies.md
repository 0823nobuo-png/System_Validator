# System Validator / Theaterverse Final
マスターインベントリ & 依存関係マップ（決定版）

---

## 1. ファイル全一覧（最終統合）
```
/root/System_Validator/APP_DIR/theaterverse_final/
├─ README_system_validator.md
├─ CHANGELOG_fusion_history.md
├─ requirements.txt
│
├─ core/
│  ├─ core_kernel.py
│  ├─ core_event_bus.py
│  ├─ core_config_loader.py
│  ├─ core_plugin_registry.py
│  ├─ core_api_server.py
│  ├─ core_router.py
│  ├─ core_security_policy.py
│  ├─ core_error_handler.py
│  └─ core_logging_config.py
│
├─ config/
│  ├─ config_app_defaults.yaml
│  ├─ config_routes_openapi.yaml
│  ├─ config_env_template.env
│  ├─ config_rbac_roles.yaml
│  └─ config_ui_settings.yaml
│
├─ db/
│  ├─ db_migrations_core.sql
│  ├─ db_seeds_minimal.sql
│  ├─ db_queries_performance.sql
│  ├─ db_orm_models.py
│  └─ db_connection_pool.py
│
├─ plugins/
│  ├─ plugin_llm_qwen25_7b/
│  │  ├─ plugin_llm_qwen25_7b_manifest.json
│  │  ├─ plugin_llm_qwen25_7b_adapter.py
│  │  ├─ plugin_llm_qwen25_7b_config.yaml
│  │  └─ plugin_llm_qwen25_7b_tokenizer.json
│  │
│  ├─ plugin_llm_mistral7b/
│  │  ├─ plugin_llm_mistral7b_manifest.json
│  │  ├─ plugin_llm_mistral7b_adapter.py
│  │  └─ plugin_llm_mistral7b_config.yaml
│  │
│  ├─ plugin_storage_postgres/
│  │  ├─ plugin_storage_postgres_manifest.json
│  │  ├─ plugin_storage_postgres_adapter.py
│  │  ├─ plugin_storage_postgres_schema.sql
│  │  └─ plugin_storage_postgres_config.yaml
│  │
│  ├─ plugin_moderation_guard/
│  │  ├─ plugin_moderation_guard_manifest.json
│  │  ├─ plugin_moderation_guard_adapter.py
│  │  └─ plugin_moderation_guard_rules.yaml
│  │
│  ├─ plugin_observability_metrics/
│  │  ├─ plugin_observability_metrics_manifest.json
│  │  ├─ plugin_observability_metrics_exporter.py
│  │  └─ plugin_observability_metrics_config.yaml
│  │
│  ├─ plugin_debug_inspector/
│  │  ├─ plugin_debug_inspector_manifest.json
│  │  ├─ plugin_debug_inspector_panel.py
│  │  └─ plugin_debug_inspector_routes.py
│  │
│  ├─ plugin_ui_console/
│  │  ├─ plugin_ui_console_manifest.json
│  │  ├─ plugin_ui_console_panel.tsx
│  │  ├─ plugin_ui_console_routes.py
│  │  └─ plugin_ui_console_assets.json
│  │
│  └─ plugin_backup_verifier/
│     ├─ plugin_backup_verifier_manifest.json
│     ├─ plugin_backup_verifier_job.py
│     └─ plugin_backup_verifier_config.yaml
│
├─ scripts/
│  ├─ script_oneclick_boot.sh
│  ├─ script_deploy_bluegreen.sh
│  ├─ script_env_setup.sh
│  ├─ script_db_migrate.sh
│  ├─ script_db_dump.sh
│  ├─ script_db_restore.sh
│  ├─ script_generate_systemd.py
│  ├─ script_validator_naming_guard.py
│  └─ script_manifest_renamer.py
│
├─ systemd/
│  ├─ systemd_service_unit.yaml
│  ├─ systemd_service_api.service
│  ├─ systemd_service_backup_verify.service
│  └─ systemd_timer_backup_verify.timer
│
├─ ci/
│  ├─ ci_pipeline_main.yaml
│  ├─ ci_tests_contracts.yaml
│  └─ ci_lint_typecheck.yaml
│
├─ tests/
│  ├─ tests_e2e_smoke.py
│  ├─ tests_perf_smoke.py
│  ├─ tests_contracts_openapi.py
│  ├─ tests_config_loader_python.py
│  ├─ tests_config_loader_typescript.ts
│  ├─ tests_plugin_llm_qwen25_7b.py
│  └─ tests_plugin_storage_postgres.py
│
├─ tools/
│  ├─ tool_json_loader_python.py
│  ├─ tool_json_loader_typescript.ts
│  ├─ tool_yaml_schema_validator.py
│  ├─ tool_openapi_diff.py
│  └─ tool_perf_sampler.py
│
├─ ui/
│  ├─ ui_main.tsx
│  ├─ ui_router.ts
│  ├─ ui_theme_tokens.ts
│  ├─ ui_components_card.tsx
│  └─ ui_components_button.tsx
│
├─ contracts/
│  ├─ contracts_schema_registry.yaml
│  └─ contracts_openapi_guard.yaml
│
├─ docs/
│  ├─ docs_runbook_operational.md
│  ├─ docs_change_log_fusion.md
│  ├─ docs_spec_mistral7b_shared.md
│  ├─ docs_api_reference_openapi.md
│  ├─ docs_security_policy.md
│  ├─ docs_backup_and_recovery.md
│  └─ handover_fusion_plan.md
│
└─ assets/
   ├─ assets_ui_logo.svg
   └─ assets_ui_favicon.ico
```

---

## 2. 依存関係マップ（主要）
- **core/core_api_server.py** → `core_kernel`（構成）＋ `core_router`（ルート統合）
- **core/core_kernel.py** → `core_event_bus`（イベント）＋ `core_config_loader`（設定）＋ `core_plugin_registry`（プラグイン）＋ `core_error_handler`（例外）＋ `core_logging_config`（ログ）
- **plugins/** 各アダプタ → `core_event_bus` 経由で起動通知を受領（`kernel_ready`）
- **plugin_storage_postgres** → `db/db_connection_pool.py`（Async SQLAlchemy）
- **ui/** → `plugins/plugin_ui_console`（/storage/plugins 等のAPI）
- **scripts/** → `db/*.sql`、`systemd/*.service|*.timer`、`requirements.txt`
- **tests/** → API（FastAPI）・OpenAPI定義・DB状態

---

## 3. 実行順（本番導線）と各ゲートの合否判定
1) **Naming Guard**: `scripts/script_validator_naming_guard.py` で重複ベース名ゼロ → **PASS 条件**: 0件
2) **Manifest Renamer**: `scripts/script_manifest_renamer.py` 実行後、`*_manifest.json` のみ → **PASS**: すべて改名済
3) **Schema/Contracts**: `contracts/*` と `config/*` の検証 → **PASS**: `pytest tests/tests_contracts_openapi.py` 成功
4) **DB Migration**: `scripts/script_db_migrate.sh` → **PASS**: エラーなし
5) **OneClick 起動**: `scripts/script_oneclick_boot.sh` → **PASS**: `/health`=ok
6) **Blue/Green 切替**: `scripts/script_deploy_bluegreen.sh B` → **PASS**: 切替後 `/health`=ok、失敗時ロールバック
7) **systemd 常駐**: `.service` 配備 & 起動 → **PASS**: `systemctl is-active system_validator`=active
8) **Backup 検証**: `/backup/verify` → **PASS**: status=ok
9) **観測性**: `/metrics/prometheus` 応答 → **PASS**: 200
10) **性能スモーク**: `tests/tests_perf_smoke.py` → **PASS**: < 1.0s

---

## 4. 変更影響範囲
- コアは不変（PEP420/プラグイン優先）。
- 追加/削除は `plugins/` で閉じる設計。
- DB スキーマは `db/db_migrations_core.sql` のみを正典とする。

---

## 5. リスク・対応
- **LLM 実体未接続**: アダプタはダミー応答 → 実接続時はプロバイダ設定の追加が必要。
- **systemd ユーザ/システム単位**: 本番では system 単位を推奨、ユニット権限を確認。
- **バックアップ先の容量**: `/var/backups` 残量監視を別途導入推奨。

--- END OF STRUCTURE ---
<!-- /root/System_Validator/APP_DIR/theaterverse_final/docs/docs_master_inventory_and_dependencies.md -->

/root/System_Validator/APP_DIR/theaterverse_final/docs/docs_master_inventory_and_dependencies.md
--- END OF STRUCTURE ---
