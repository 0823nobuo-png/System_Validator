# System Validator / Theaterverse Final
API リファレンス - OpenAPI

---

## 基本情報
- Title: System Validator API
- Version: 1.0.0
- Server: http://localhost:8080

## エンドポイント一覧

### Health
- **GET /health**
- Response: `{ "status": "ok" }`

### Metrics
- **GET /metrics**
- Response: Prometheus 互換メトリクス

### Qwen2.5-7B
- **POST /llm/qwen25_7b/generate**
- Params: `prompt: string`
- Response: `{ model: "qwen2.5-7b", output: string }`

### Mistral-7B
- **POST /llm/mistral7b/generate**
- Params: `prompt: string`
- Response: `{ model: "mistral-7b", output: string }`

### Storage Plugins
- **GET /storage/plugins**
- Response: `{ plugins: [ { name: string, enabled: boolean } ] }`

### Moderation
- **POST /moderation/check**
- Body: `{ content: string }`
- Response: `{ violations: [rule] }`

### Debug Inspector
- **GET /debug/inspect**
- Response: Debug info JSON

- **GET /debug/env**
- Response: Environment variables

- **GET /debug/sysinfo**
- Response: Python sys info

### UI Console
- **GET /ui/console/status**
- Response: `{ status: "ok", plugin: "ui_console" }`

### Backup Verifier
- **GET /backup/verify**
- Response: Backup verification status

--- END OF STRUCTURE ---
<!-- /root/System_Validator/APP_DIR/theaterverse_final/docs/docs_api_reference_openapi.md -->

/root/System_Validator/APP_DIR/theaterverse_final/docs/docs_api_reference_openapi.md
--- END OF STRUCTURE ---
