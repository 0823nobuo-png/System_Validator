"""
System Validator / Theaterverse Final
Tests: Plugin Storage Postgres

Smoke tests for PostgreSQL storage plugin.
"""

import pytest
import httpx
import os

BASE_URL = os.getenv("TEST_BASE_URL", "http://localhost:8080")


@pytest.mark.asyncio
async def test_list_plugins():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BASE_URL}/storage/plugins")
        assert r.status_code == 200
        data = r.json()
        assert "plugins" in data
        assert isinstance(data["plugins"], list)

--- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/tests/tests_plugin_storage_postgres.py
# /root/System_Validator/APP_DIR/theaterverse_final/tests/tests_plugin_storage_postgres.py
# --- END OF STRUCTURE ---
