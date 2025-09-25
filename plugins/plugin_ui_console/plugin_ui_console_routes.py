"""
System Validator / Theaterverse Final
Plugin: UI Console Routes

Provides backend routes for UI Console plugin.
"""

import logging
from fastapi import APIRouter

logger = logging.getLogger(__name__)


def register(event_bus):
    logger.info("Registering plugin: plugin_ui_console")
    event_bus.subscribe("kernel_ready", _on_kernel_ready)


def _on_kernel_ready(payload):
    logger.info("plugin_ui_console: kernel ready: %s", payload)


def routes(app):
    router = APIRouter()

    @router.get("/ui/console/status")
    async def status():
        return {"status": "ok", "plugin": "ui_console"}

    app.include_router(router)


--- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/plugins/plugin_ui_console/plugin_ui_console_routes.py
# /root/System_Validator/APP_DIR/theaterverse_final/plugins/plugin_ui_console/plugin_ui_console_routes.py
# --- END OF STRUCTURE ---
