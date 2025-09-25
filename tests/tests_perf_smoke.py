"""
System Validator / Theaterverse Final
Tests: Performance Smoke Tests

Ensures API endpoints respond within acceptable latency.
"""

import pytest
import httpx
import os
import time

BASE_URL = os.getenv("TEST_BASE_URL", "http://localhost:8080")
MAX_LATENCY = float(os.getenv("TEST_MAX_LATENCY", "1.0"))  # seconds


@pytest.mark.asyncio
async def test_health_latency():
    async with httpx.AsyncClient() as client:
        start = time.perf_counter()
        r = await client.get(f"{BASE_URL}/health")
        elapsed = time.perf_counter() - start
        assert r.status_code == 200
        assert elapsed < MAX_LATENCY, f"Health endpoint too slow: {elapsed:.2f}s"


# --- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/tests/tests_perf_smoke.py
# /root/System_Validator/APP_DIR/theaterverse_final/tests/tests_perf_smoke.py
# --- END OF STRUCTURE ---
