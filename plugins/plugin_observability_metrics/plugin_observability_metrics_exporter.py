"""
System Validator / Theaterverse Final
Plugin: Observability Metrics Exporter

Provides Prometheus-compatible metrics endpoint.
"""

import logging
from fastapi import APIRouter, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter

logger = logging.getLogger(__name__)

REQUEST_COUNT = Counter("system_validator_requests_total", "Total requests")


def register(event_bus):
    logger.info("Registering plugin: plugin_observability_metrics")
    event_bus.subscribe("kernel_ready", _on_kernel_ready)


def _on_kernel_ready(payload):
    logger.info("plugin_observability_metrics: kernel ready: %s", payload)


def routes(app):
    router = APIRouter()

    @router.get("/metrics/prometheus")
    async def prometheus_metrics():
        REQUEST_COUNT.inc()
        data = generate_latest()
        return Response(content=data, media_type=CONTENT_TYPE_LATEST)

    app.include_router(router)


# --- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/plugins/plugin_observability_metrics/plugin_observability_metrics_exporter.py
# /root/System_Validator/APP_DIR/theaterverse_final/plugins/plugin_observability_metrics/plugin_observability_metrics_exporter.py
# --- END OF STRUCTURE ---
