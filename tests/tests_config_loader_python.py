"""
System Validator / Theaterverse Final
Tests: Config Loader (Python)

Validates that the Python ConfigLoader loads env and YAML properly.
"""

import os
import pytest
from core.core_config_loader import ConfigLoader

BASE_DIR = "/root/System_Validator/APP_DIR/theaterverse_final"


def test_config_loader_env_and_yaml(tmp_path, monkeypatch):
    # Prepare temp env file
    env_file = tmp_path / "config_env_template.env"
    env_file.write_text("SYSTEM_VALIDATOR_DSN=postgresql://u:p@localhost:5432/db\n")

    # Prepare temp yaml file
    yaml_file = tmp_path / "config_app_defaults.yaml"
    yaml_file.write_text("API_BIND_PORT: 1234\n")

    # Monkeypatch base_dir
    monkeypatch.setenv("SYSTEM_VALIDATOR_BASE_DIR", str(tmp_path))

    loader = ConfigLoader(str(tmp_path))
    cfg = loader.load()

    assert cfg["SYSTEM_VALIDATOR_DSN"].startswith("postgresql")
    assert cfg["API_BIND_PORT"] == 1234

# --- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/tests/tests_config_loader_python.py
# /root/System_Validator/APP_DIR/theaterverse_final/tests/tests_config_loader_python.py
# --- END OF STRUCTURE ---
