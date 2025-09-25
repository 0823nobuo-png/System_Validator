"""
System Validator / Theaterverse Final
Tests: OpenAPI Contract Validation

Validates API endpoints against OpenAPI configuration.
"""

import pytest
import httpx
import os
import yaml

BASE_URL = os.getenv("TEST_BASE_URL", "http://localhost:8080")
OPENAPI_FILE = os.getenv(
    "OPENAPI_FILE",
    "/root/System_Validator/APP_DIR/theaterverse_final/config/config_routes_openapi.yaml",
)


@pytest.mark.asyncio
async def test_openapi_contracts():
    with open(OPENAPI_FILE, "r", encoding="utf-8") as f:
        spec = yaml.safe_load(f)

    async with httpx.AsyncClient() as client:
        for path in spec.get("openapi", {}).get("paths", {}):
            for method in spec["openapi"]["paths"][path].keys():
                url = f"{BASE_URL}{path}"
                response = await client.request(method.upper(), url)
                assert response.status_code == 200, f"{method.upper()} {url} failed"


# --- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/tests/tests_contracts_openapi.py
# /root/System_Validator/APP_DIR/theaterverse_final/tests/tests_contracts_openapi.py
# --- END OF STRUCTURE ---
