"""
System Validator / Theaterverse Final
Plugin: Debug Inspector Routes

Provides additional routes for debugging (stack traces, env, etc.).
"""

import logging
import os
import sys
from fastapi import APIRouter

logger = logging.getLogger(__name__)


def register(event_bus):
    logger.info("Registering plugin: plugin_debug_inspector (routes)")
    event_bus.subscribe("kernel_ready", _on_kernel_ready)


def _on_kernel_ready(payload):
    logger.info("plugin_debug_inspector (routes): kernel ready: %s", payload)


def routes(app):
    router = APIRouter()

    @router.get("/debug/env")
    async def get_env():
        return dict(os.environ)

    @router.get("/debug/sysinfo")
    async def sys_info():
        return {
            "version": sys.version,
            "argv": sys.argv,
            "platform": sys.platform,
        }

    app.include_router(router)


--- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/plugins/plugin_debug_inspector/plugin_debug_inspector_routes.py
# /root/System_Validator/APP_DIR/theaterverse_final/plugins/plugin_debug_inspector/plugin_debug_inspector_routes.py
# --- END OF STRUCTURE ---
