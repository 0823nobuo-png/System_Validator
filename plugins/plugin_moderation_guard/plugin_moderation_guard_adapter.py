"""
System Validator / Theaterverse Final
Plugin: Moderation Guard Adapter

Provides content moderation checks based on predefined rules.
Exposes register() and routes().
"""

import logging
from fastapi import APIRouter
import yaml
import os

logger = logging.getLogger(__name__)

RULES = []


def register(event_bus):
    logger.info("Registering plugin: plugin_moderation_guard")
    event_bus.subscribe("kernel_ready", _on_kernel_ready)


def _on_kernel_ready(payload):
    logger.info("plugin_moderation_guard: kernel ready: %s", payload)
    _load_rules(payload.get("base_dir"))


def _load_rules(base_dir: str):
    global RULES
    rules_file = os.path.join(base_dir, "plugins", "plugin_moderation_guard", "plugin_moderation_guard_rules.yaml")
    if not os.path.exists(rules_file):
        logger.warning("Moderation rules file not found: %s", rules_file)
        return
    with open(rules_file, "r", encoding="utf-8") as f:
        RULES = yaml.safe_load(f) or []
    logger.info("Loaded moderation rules: %d", len(RULES))


def routes(app):
    router = APIRouter()

    @router.post("/moderation/check")
    async def check(content: str):
        violations = []
        for rule in RULES:
            if rule.get("pattern") in content:
                violations.append(rule)
        return {"violations": violations}

    app.include_router(router)


# --- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/plugins/plugin_moderation_guard/plugin_moderation_guard_adapter.py
# /root/System_Validator/APP_DIR/theaterverse_final/plugins/plugin_moderation_guard/plugin_moderation_guard_adapter.py
# --- END OF STRUCTURE ---
