"""
core_observability.py

目的（強化④ 可観測性）:
- OpenTelemetry のトレーシング初期化（OTLP / stdout 簡易切替）
- Prometheus メトリクス（Counter/Histogram/Gauge）エクスポート
- LLM/認証/DB/アプリの汎用計測ヘルパ
- 依存最小: opentelemetry-sdk, opentelemetry-exporter-otlp, prometheus-client

正式パス：/root/System_Validator/APP_DIR/theaterverse_final/core/core_observability.py
"""
from __future__ import annotations

import os
import time
import logging
from contextlib import contextmanager
from typing import Optional, Dict, Any

# ------------------------------ Logging ---------------------------------- #
LOG = logging.getLogger("theaterverse_final.observability")
LOG.setLevel(logging.INFO)

# --------------------------- OpenTelemetry -------------------------------- #
try:
    from opentelemetry import trace
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    _OTEL_AVAILABLE = True
except Exception:  # pragma: no cover
    _OTEL_AVAILABLE = False
    trace = None  # type: ignore

# ------------------------- Prometheus Metrics ----------------------------- #
try:
    from prometheus_client import Counter, Histogram, Gauge, start_http_server
    _PROM_AVAILABLE = True
except Exception:  # pragma: no cover
    _PROM_AVAILABLE = False
    Counter = Histogram = Gauge = None  # type: ignore
    def start_http_server(*_args: Any, **_kwargs: Any) -> None:  # type: ignore
        pass

# ---------------------------- Global State -------------------------------- #
_TRACER = None
_METRICS: Dict[str, Any] = {}
_PROM_STARTED = False


def init_tracing(service_name: str = "theaterverse_final",
                 exporter: str = "otlp",
                 otlp_endpoint: Optional[str] = None) -> None:
    """Initialize OpenTelemetry tracing.
    exporter: "otlp" (default) or "stdout".
    If _OTEL_AVAILABLE is False, this is a no-op.
    """
    global _TRACER
    if not _OTEL_AVAILABLE:
        LOG.warning("OpenTelemetry not available; tracing disabled")
        return

    svc = service_name or os.environ.get("OTEL_SERVICE_NAME", "theaterverse_final")
    resource = Resource.create({"service.name": svc})
    provider = TracerProvider(resource=resource)

    if exporter == "stdout":
        # Lazy import to avoid hard dependency
        from opentelemetry.sdk.trace.export import ConsoleSpanExporter  # type: ignore
        processor = BatchSpanProcessor(ConsoleSpanExporter())
    else:
        endpoint = otlp_endpoint or os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT", "http://127.0.0.1:4318")
        processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint))

    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)
    _TRACER = trace.get_tracer("theaterverse_final.tracer")
    LOG.info("Tracing initialized (service=%s, exporter=%s)", svc, exporter)


def init_metrics(port: int = 9100) -> None:
    """Start Prometheus metrics server and register standard metrics."""
    global _PROM_STARTED
    if not _PROM_AVAILABLE:
        LOG.warning("prometheus_client not available; metrics disabled")
        return
    if not _PROM_STARTED:
        start_http_server(port)
        _PROM_STARTED = True
        LOG.info("Prometheus metrics server started on :%d", port)

    # Register metrics only once
    if not _METRICS:
        _METRICS.update({
            # LLM
            "llm_calls_total": Counter("llm_calls_total", "Number of LLM calls", ["provider", "result"]),
            "llm_latency_seconds": Histogram(
                "llm_latency_seconds", "Latency of LLM calls", ["provider"],
                buckets=(0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10)
            ),
            # Auth
            "auth_verify_failures_total": Counter("auth_verify_failures_total", "Number of auth verification failures", ["reason"]),
            # DB
            "db_connections": Gauge("db_connections", "Number of active DB connections"),
            # App
            "app_errors_total": Counter("app_errors_total", "Number of app errors", ["component", "kind"]),
        })


# ----------------------------- Helper APIs -------------------------------- #
@contextmanager
def traced_span(name: str, **attrs: Any):
    """Context manager to create a tracing span if tracing is available."""
    if _TRACER is None:
        yield None
        return
    with _TRACER.start_as_current_span(name) as span:
        for k, v in attrs.items():
            try:
                span.set_attribute(k, v)
            except Exception:
                pass
        yield span


@contextmanager
def observe_latency(histogram_name: str, **labels: str):
    """Measure latency for a code block and record it to a Histogram metric."""
    h = _METRICS.get(histogram_name)
    start = time.perf_counter()
    try:
        yield
    finally:
        if h is not None:
            try:
                h.labels(**labels).observe(time.perf_counter() - start)
            except Exception:
                pass


def record_counter(counter_name: str, **labels: str) -> None:
    c = _METRICS.get(counter_name)
    if c is not None:
        try:
            c.labels(**labels).inc()
        except Exception:
            pass


def set_gauge(gauge_name: str, value: float) -> None:
    g = _METRICS.get(gauge_name)
    if g is not None:
        try:
            g.set(value)
        except Exception:
            pass


# ------------------------- Domain-specific helpers ------------------------ #
def record_llm_call(provider: str, ok: bool) -> None:
    record_counter("llm_calls_total", provider=provider, result=("ok" if ok else "error"))


def time_llm_call(provider: str):
    return observe_latency("llm_latency_seconds", provider=provider)


def record_auth_failure(reason: str) -> None:
    record_counter("auth_verify_failures_total", reason=reason)


def set_db_connection_count(n: int) -> None:
    set_gauge("db_connections", float(n))


# ------------------------------ Bootstrap --------------------------------- #
def init_observability(service_name: str = "theaterverse_final",
                       otlp_endpoint: Optional[str] = None,
                       exporter: str = "otlp",
                       metrics_port: int = 9100) -> None:
    """Convenience initializer used by app entrypoint.
    - Initializes tracing and metrics in one call.
    """
    init_tracing(service_name=service_name, exporter=exporter, otlp_endpoint=otlp_endpoint)
    init_metrics(port=metrics_port)


# ------------------------------ Self test --------------------------------- #
if __name__ == "__main__":
    init_observability()
    with traced_span("demo-span", component="observability"):
        with time_llm_call("demo-provider"):
            time.sleep(0.123)
        record_llm_call("demo-provider", ok=True)
        record_auth_failure("invalid_token")
        set_db_connection_count(5)
    print("observability initialized")  # noqa: T201

# --- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/core/core_observability.py
# /root/System_Validator/APP_DIR/theaterverse_final/core/core_observability.py
# --- END OF STRUCTURE ---
