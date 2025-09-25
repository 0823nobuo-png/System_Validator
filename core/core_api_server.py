"""
System Validator / Theaterverse Final
Core API Server - FastAPI application with integrated kernel and plugins.

Provides lifecycle management and exposes HTTP endpoints.
"""

import logging
import os
from fastapi import FastAPI
import uvicorn

from .core_kernel import CoreKernel
from .core_router import CoreRouter

logger = logging.getLogger(__name__)


class CoreAPIServer:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        self.kernel = CoreKernel(base_dir)
        self.app = FastAPI(title="System Validator API")
        self.router = CoreRouter(self.app)

    def setup(self):
        # Bootstrap kernel
        self.kernel.bootstrap()

        # Add core routes
        self.router.add_health_route()
        self.router.add_metrics_route()

        # Integrate plugin routes
        self.router.integrate_plugin_routes(self.kernel.plugin_registry.plugins)

        logger.info("Core API Server setup complete.")
        return self.app

    def run(self):
        app = self.setup()
        host = os.getenv("API_BIND_HOST", "0.0.0.0")
        port = int(os.getenv("API_BIND_PORT", "8080"))
        uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    base_dir = os.getenv(
        "SYSTEM_VALIDATOR_BASE_DIR",
        "/root/System_Validator/APP_DIR/theaterverse_final",
    )
    server = CoreAPIServer(base_dir)
    server.run()

# --- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/core/core_api_server.py
# /root/System_Validator/APP_DIR/theaterverse_final/core/core_api_server.py
# --- END OF STRUCTURE ---
