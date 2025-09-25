"""
System Validator / Theaterverse Final
Core Router - FastAPI router configuration.

Defines core routes and integrates plugin routes dynamically.
"""

from fastapi import FastAPI
import logging

logger = logging.getLogger(__name__)


class CoreRouter:
    def __init__(self, app: FastAPI):
        self.app = app

    def add_health_route(self):
        @self.app.get("/health")
        async def health():
            return {"status": "ok"}

    def add_metrics_route(self):
        @self.app.get("/metrics")
        async def metrics():
            # Prometheus metrics should be exported by plugin_observability_metrics
            return {"metrics": "provided by plugin_observability_metrics"}

    def integrate_plugin_routes(self, plugins):
        for name, module in plugins.items():
            if hasattr(module, "routes"):
                try:
                    module.routes(self.app)
                    logger.info("Integrated routes from plugin: %s", name)
                except Exception as e:
                    logger.exception("Failed to integrate routes for %s: %s", name, e)


--- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/core/core_router.py
# /root/System_Validator/APP_DIR/theaterverse_final/core/core_router.py
# --- END OF STRUCTURE ---
