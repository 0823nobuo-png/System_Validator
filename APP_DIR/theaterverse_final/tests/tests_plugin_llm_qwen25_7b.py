"""
System Validator / Theaterverse Final
Tests: Plugin LLM Qwen2.5-7B

Smoke tests for Qwen2.5-7B plugin adapter routes.
"""

import pytest
import httpx
import os

BASE_URL = os.getenv("TEST_BASE_URL", "http://localhost:8080")


@pytest.mark.asyncio
async def test_qwen25_7b_generate():
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{BASE_URL}/llm/qwen25_7b/generate", params={"prompt": "Hello"})
        assert r.status_code == 200
        data = r.json()
        assert data["model"] == "qwen2.5-7b"
        assert "output" in data

--- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/tests/tests_plugin_llm_qwen25_7b.py
# /root/System_Validator/APP_DIR/theaterverse_final/tests/tests_plugin_llm_qwen25_7b.py
# --- END OF STRUCTURE ---
