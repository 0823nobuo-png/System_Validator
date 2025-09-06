# Observability Runbook（監視・計測）

正式パス：/root/System_Validator/APP_DIR/theaterverse_final/docs/runbook_observability.md

---

## 目的
- OTELトレースとPrometheusメトリクスの最小構成セットアップ

## 手順
1. OTEL Collector を起動（HTTP/OTLP :4318）
2. アプリ設定：`config/app_settings.yaml` を確認（`otlp_endpoint`, `metrics_port`）
3. アプリ起動：`systemctl restart system_validator`
4. Grafanaに `monitoring/grafana_dashboard_template.json` をインポート

## 成功基準
- トレースが Collector → Grafana Tempo/Jaeger に流れる
- メトリクス（LLMレイテンシ/Auth失敗/DB接続/CPU%）が表示

---

--- END OF STRUCTURE ---
<!-- /root/System_Validator/APP_DIR/theaterverse_final/docs/runbook_observability.md -->

/root/System_Validator/APP_DIR/theaterverse_final/docs/runbook_observability.md
--- END OF STRUCTURE ---
