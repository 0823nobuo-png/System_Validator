"""
app_main.py

目的：
- Systemd から起動されるアプリ実体（`python -m app.main` を想定）
- FastAPI による HTTP エンドポイント提供
  - GET /health … ヘルスチェック
  - POST /v1/chat … OpenAI互換の chat/completions 風IF（最小）
- Observability 初期化（OTel + Prometheus）
- OIDC 検証（任意）

正式パス：/root/System_Validator/APP_DIR/theaterverse_final/app/main.py
"""
from __future__ import annotations

import os
import uvicorn  # type: ignore
from fastapi import FastAPI, Request, HTTPException, Depends
from pydantic import BaseModel
from typing import Any, Dict, List, Optional

from core.core_observability import init_observability, traced_span, time_llm_call, record_llm_call
from core.core_adapter_llm import LLMAdapter
from core.core_auth_manager import CoreAuthManager


# -------------------------- Settings loader -------------------------- #
import yaml  # type: ignore

APP_SETTINGS_PATH = os.environ.get(
    "APP_SETTINGS_PATH",
    "/root/System_Validator/APP_DIR/theaterverse_final/config/app_settings.yaml",
)


def load_settings() -> Dict[str, Any]:
    try:
        with open(APP_SETTINGS_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        return {}


SETTINGS = load_settings()
SERVICE_NAME = SETTINGS.get("service_name", "theaterverse_final")
METRICS_PORT = int(SETTINGS.get("metrics_port", 9100))
OTLP_ENDPOINT = SETTINGS.get("otlp_endpoint")
USE_AUTH = bool(SETTINGS.get("auth", {}).get("enabled", False))

# --------------------------- Bootstrap -------------------------------- #
init_observability(service_name=SERVICE_NAME, otlp_endpoint=OTLP_ENDPOINT, metrics_port=METRICS_PORT)
adapter = LLMAdapter()
auth_mgr: Optional[CoreAuthManager] = CoreAuthManager() if USE_AUTH else None

app = FastAPI(title="System Validator API", version="1.0.0")


# --------------------------- Models ------------------------------------ #
class ChatRequest(BaseModel):
    model: Optional[str] = None
    messages: List[Dict[str, str]]
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None


# --------------------------- Auth Dep ---------------------------------- #
async def token_required(request: Request) -> Optional[Dict[str, Any]]:
    if not USE_AUTH:
        return None
    if not auth_mgr:
        raise HTTPException(status_code=500, detail="auth manager not initialized")
    auth = request.headers.get("authorization") or request.headers.get("Authorization")
    if not auth or not auth.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="missing bearer token")
    token = auth.split(" ", 1)[1]
    try:
        claims = auth_mgr.verify_access_token(token)
        return claims
    except Exception as e:  # noqa: BLE001
        from core.core_observability import record_auth_failure
        record_auth_failure("verify_failed")
        raise HTTPException(status_code=401, detail=str(e))


# --------------------------- Routes ------------------------------------ #
@app.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/chat")
async def v1_chat(req: ChatRequest, _claims: Optional[Dict[str, Any]] = Depends(token_required)) -> Dict[str, Any]:
    with traced_span("api.v1_chat", model=req.model or "default"):
        with time_llm_call("primary"):
            try:
                resp = adapter.chat(
                    messages=req.messages,
                    model=req.model,
                    temperature=req.temperature,
                    max_tokens=req.max_tokens,
                )
                record_llm_call("primary", ok=True)
                return resp
            except Exception as e:  # noqa: BLE001
                record_llm_call("primary", ok=False)
                raise HTTPException(status_code=500, detail=str(e))


# --------------------------- Entrypoint -------------------------------- #
if __name__ == "__main__":
    host = os.environ.get("APP_HOST", "0.0.0.0")
    port = int(os.environ.get("APP_PORT", "8000"))
    uvicorn.run("app.main:app", host=host, port=port, reload=False)

# --- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/app/main.py
# /root/System_Validator/APP_DIR/theaterverse_final/app/app_main.py
# --- END OF STRUCTURE ---
