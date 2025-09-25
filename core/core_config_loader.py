"""
System Validator / Theaterverse Final
Core Config Loader - Environment and YAML configuration management.

Loads configuration from .env and YAML defaults, merges into a single dict.
Ensures PostgreSQL-only DSN and validates schema.
"""

import os
import logging
import yaml
from dotenv import load_dotenv
from typing import Any, Dict

logger = logging.getLogger(__name__)


class ConfigLoader:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        self.env_file = os.path.join(base_dir, "config", "config_env_template.env")
        self.yaml_file = os.path.join(base_dir, "config", "config_app_defaults.yaml")

    def load(self) -> Dict[str, Any]:
        """Load environment variables and YAML defaults."""
        # Load environment
        if os.path.exists(self.env_file):
            load_dotenv(self.env_file, override=True)
            logger.debug("Loaded env from %s", self.env_file)

        # Load YAML defaults
        config: Dict[str, Any] = {}
        if os.path.exists(self.yaml_file):
            with open(self.yaml_file, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f) or {}
            logger.debug("Loaded defaults from %s", self.yaml_file)

        # Merge environment overrides
        for key, value in os.environ.items():
            if key.startswith("SYSTEM_VALIDATOR_") or key in [
                "API_BIND_HOST",
                "API_BIND_PORT",
                "UI_DIST_DIR",
                "LOG_LEVEL",
                "BLUEGREEN_SLOT",
            ]:
                config[key] = value

        # PostgreSQL DSN validation
        dsn = config.get("SYSTEM_VALIDATOR_DSN")
        if not dsn or not dsn.startswith("postgresql"):
            raise ValueError("SYSTEM_VALIDATOR_DSN must be a PostgreSQL DSN")

        return config


if __name__ == "__main__":
    base_dir = os.getenv(
        "SYSTEM_VALIDATOR_BASE_DIR",
        "/root/System_Validator/APP_DIR/theaterverse_final",
    )
    loader = ConfigLoader(base_dir)
    cfg = loader.load()
    print("Loaded config keys:", list(cfg.keys()))

# --- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/core/core_config_loader.py
# /root/System_Validator/APP_DIR/theaterverse_final/core/core_config_loader.py
# --- END OF STRUCTURE ---
