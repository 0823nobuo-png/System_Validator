# 完成度確認・最終チェックリスト（System Validator / Theaterverse Final）

正式パス：/root/System_Validator/APP_DIR/theaterverse_final/docs/final_completion_checklist.md

---

## 1. ガバナンス & 命名・構文
- [ ] すべての新旧ファイルが `<ユニット>_<機能>.<拡張子>` を満たす
- [ ] 同一プロジェクト内で**重複ファイル名なし**（階層をまたいでも一意）
- [ ] 全ファイル末尾に `--- END OF STRUCTURE ---` もしくは JSON の `__file_path__` / `__end_of_structure__` が存在
- [ ] `.json` は末尾コメント方式 or 厳密JSONの特別フィールド方式のどちらかで**統一**
- [ ] 正式パスの先頭は `/root/System_Validator/APP_DIR/` を使用（`/root/`は環境差を許容）

## 2. セキュリティ & 認証
- [ ] `config/auth_oidc_settings.yaml`：`issuer`/`aud`/`algorithms` が本番値で設定
- [ ] OIDC Discovery 到達性（`/.well-known/openid-configuration`）と JWKS 取得を確認
- [ ] `core/core_auth_manager.py`：テストトークンで `iss/aud/exp/nbf` 検証成功
- [ ] 役割・権限：`read:content`/`write:content`/`admin:ops` の付与ロジックを実環境で確認
- [ ] 監査ログ（PostgreSQL）にイベントが記録される
- [ ] `.env` の秘匿値は **sops/Vault** で管理。平文コミット禁止

## 3. LLM 接続
- [ ] `config/llm_connector_config.json`：`base_url` と `default_model` が実環境値
- [ ] vLLM / llama.cpp / OpenAI で少なくとも**1系統**は応答取得
- [ ] ネットワーク遮断時に**フェイルオーバ**が機能
- [ ] レート制御（TokenBucket）が高頻度呼び出しで正しく抑制
- [ ] タイムアウト・再試行（指数バックオフ）がログで確認可能

## 4. 可観測性
- [ ] OpenTelemetry：`service_name=theaterverse_final` でトレースが発火
- [ ] Prometheus → Grafana：`grafana_dashboard_template.json` をインポート済み
- [ ] 「LLMレイテンシ」「Auth失敗数」「DB接続」「CPU%」が描画

## 5. CI/CD・品質
- [ ] `ci/ci_pipeline.yaml` を既存パイプラインに登録
- [ ] `scripts/ci_sbom_generator.py` から `sbom.json` が生成され artifacts 化
- [ ] `pip-audit` / `npm audit` / `bandit` / `eslint` の最低限のしきい値合格（Fail条件は運用ポリシーで決定）
- [ ] 主要ブランチは **必須レビュー** と **CI パス必須** を設定

## 6. バックアップ & DR
- [ ] `scripts/dr_restore_test.sh` 実行で `dr_restore_report.txt` を出力
- [ ] DR検証用DBを隔離（プレフィックス/ネットワーク/権限）
- [ ] 週1実行の定期ジョブ化（CI または systemd timer）
- [ ] 復旧 RTO/RPO の目標と実測値の差分が許容範囲

## 7. 運用自動化（Blue/Green）
- [ ] `scripts/deploy_bluegreen.py`：`NEW_RELEASE` 指定で切替
- [ ] 切替後ヘルスチェック失敗時に**自動ロールバック**を実確認
- [ ] Slack/メール通知が到達
- [ ] 切替 Runbook とロールバック基準を `docs/` に明文化

## 8. systemd ハードニング
- [ ] `systemd/system_validator.service` を `/etc/systemd/system/` へ配置
- [ ] `User=validator` 作成済み、必要ディレクトリの権限付与
- [ ] `ProtectSystem=strict` 適用下での書込先は `ReadWritePaths` のみ
- [ ] 起動後ステータス：`active (running)`、ジャーナルに危険警告なし

## 9. データベース（PostgreSQL）
- [ ] 接続情報（`DATABASE_URL`）は `.env` 由来で暗号化保護
- [ ] マイグレーション計画とバージョニング（例：`alembic`）を用意
- [ ] 監査テーブル `auth_audit_logs` のローテーション設計

## 10. ドキュメント & インベントリ
- [ ] `handover_summary_and_next_steps_v2.md` の残タスク消込
- [ ] `docs_master_inventory_and_dependencies_v2.md` を現況に同期
- [ ] `docs_validation_scenarios_v2.md` を**実行ログのリンク**付きで更新

## 11. リスク & 対応（抜粋）
- **IdP障害**：トークン検証不可能 → **緩和**：短期のキャッシュ/JWKS TTL、運用連絡フロー
- **LLM遅延**：推論詰まり → **緩和**：タイムアウト短縮＋フェイルオーバ＋優先順調整
- **誤リリース**：不整合切替 → **緩和**：ステージング→事前ヘルス→アトミック切替
- **秘匿値漏えい**：平文残留 → **緩和**：sops/Vault運用・PRチェックスクリプト

## 12. サインオフ基準
- [ ] 本チェックリストが**全てチェック**（除外項目は備考に理由）
- [ ] 回帰シナリオ v2 を**1周完了**し、主要ログ/レポートを保存
- [ ] 重大/高リスクが**0件**
- [ ] オーナー承認（署名・日時）

---

--- END OF STRUCTURE ---
<!-- /root/System_Validator/APP_DIR/theaterverse_final/docs/final_completion_checklist.md -->

/root/System_Validator/APP_DIR/theaterverse_final/docs/final_completion_checklist.md
--- END OF STRUCTURE ---
