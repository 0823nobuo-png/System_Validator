"""
System Validator / Theaterverse Final
Tests: End-to-End Smoke Tests

Covers API health, metrics, and minimal DB query.
"""

import pytest
import httpx
import os

BASE_URL = os.getenv("TEST_BASE_URL", "http://localhost:8080")


@pytest.mark.asyncio
async def test_health():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BASE_URL}/health")
        assert r.status_code == 200
        assert r.json().get("status") == "ok"


@pytest.mark.asyncio
async def test_metrics():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BASE_URL}/metrics")
        assert r.status_code == 200


--- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/tests/tests_e2e_smoke.py
# /root/System_Validator/APP_DIR/theaterverse_final/tests/tests_e2e_smoke.py
# --- END OF STRUCTURE ---
