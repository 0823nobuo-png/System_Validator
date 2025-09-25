"""
System Validator / Theaterverse Final
Core Error Handler - Centralized exception and error reporting.

Provides utilities for consistent error handling across kernel and plugins.
Integrates with logging for auditability.
"""

import logging
import traceback
from typing import Any, Dict

logger = logging.getLogger(__name__)


class ErrorHandler:
    def __init__(self):
        self.handlers = []

    def register(self, func):
        """Register a custom error handler function."""
        self.handlers.append(func)

    def handle(self, error: Exception, context: Dict[str, Any] = None):
        context = context or {}
        error_info = {
            "type": type(error).__name__,
            "message": str(error),
            "context": context,
            "trace": traceback.format_exc(),
        }

        logger.error("Error occurred: %s", error_info)

        for handler in self.handlers:
            try:
                handler(error_info)
            except Exception as e:
                logger.exception("Error in custom handler: %s", e)

        return error_info


# --- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/core/core_error_handler.py
# /root/System_Validator/APP_DIR/theaterverse_final/core/core_error_handler.py
# --- END OF STRUCTURE ---
