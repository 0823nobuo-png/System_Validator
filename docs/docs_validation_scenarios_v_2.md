# 実行検証シナリオ v2（回帰チェック追記）

正式パス：/root/System_Validator/APP_DIR/theaterverse_final/docs/docs_validation_scenarios_v2.md

---

## 1. システム回帰フロー（順次実行）
1. **systemd 起動検証**
   - 配置：`systemd/system_validator.service` を `/etc/systemd/system/` へ
   - `sudo systemctl daemon-reload && sudo systemctl enable --now system_validator`
   - 期待：`active (running)` / ジャーナル警告なし
2. **Secrets 生成**
   - sops/Vault で `.env` または `EnvironmentFile` を生成
   - 期待：平文秘匿値のリポジトリ混入がない
3. **LLM 疎通**
   - `python core/core_adapter_llm.py` の `__main__` を実行
   - 期待：優先順に応答取得（vLLM → llama.cpp → OpenAI）
4. **OIDC/JWT 検証**
   - `core_auth_manager.verify_access_token` にテストトークンを渡す
   - 期待：`iss/aud/exp/nbf` 検証OK、scope/role適用OK
5. **DB/DR 演習**
   - `scripts/dr_restore_test.sh` を実行
   - 期待：`dr_restore_report.txt` 出力、エラー検出時は非0終了
6. **CI/CD（SBOM）**
   - `scripts/ci_sbom_generator.py` をCIで実行
   - 期待：`sbom.json` が artifacts として保存
7. **Observability**
   - `monitoring/grafana_dashboard_template.json` をインポート
   - 期待：メトリクス可視化（LLMレイテンシ、Auth失敗、DB接続、CPU%）
8. **Blue/Green**
   - `NEW_RELEASE=<dir> HEALTH_URL=http://127.0.0.1:8000/health python scripts/deploy_bluegreen.py`
   - 期待：成功時通知／失敗時ロールバック

## 2. 負荷・障害シナリオ（抜粋）
- **LLMタイムアウト**：意図的に応答遅延 → フェイルオーバ動作とOTELトレース確認
- **JWT kid不一致**：未知kidで拒否されること
- **DB接続断**：DR演習時のエラー報告が非0終了になること
- **リリース破損**：Blue/Green 事後ヘルス失敗で自動ロールバック

## 3. 合格基準
- すべてのステップが**自動／半自動で再現可能**
- 重大警告（セキュリティ/可用性）が残らない
- 監査ログ・SBOM・DRレポートが**追跡可能な形で保存**

---

--- END OF STRUCTURE ---
<!-- /root/System_Validator/APP_DIR/theaterverse_final/docs/docs_validation_scenarios_v2.md -->

/root/System_Validator/APP_DIR/theaterverse_final/docs/docs_validation_scenarios_v_2.md
--- END OF STRUCTURE ---
