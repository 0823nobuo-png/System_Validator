"""
System Validator / Theaterverse Final
Core Logging Config - Structured logging setup.

Configures application-wide structured JSON logging for consistency across
core and plugins.
"""

import logging
import os
import sys
import json
from typing import Any, Dict


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_record: Dict[str, Any] = {
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "time": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
        }
        if record.exc_info:
            log_record["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(log_record, ensure_ascii=False)


def configure_logging():
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.handlers.clear()
    root_logger.addHandler(handler)

    logging.getLogger("uvicorn").setLevel(log_level)
    logging.getLogger("uvicorn.error").setLevel(log_level)
    logging.getLogger("uvicorn.access").setLevel(log_level)

    logging.info("Logging configured with level %s", log_level)


--- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/core/core_logging_config.py
# /root/System_Validator/APP_DIR/theaterverse_final/core/core_logging_config.py
# --- END OF STRUCTURE ---
