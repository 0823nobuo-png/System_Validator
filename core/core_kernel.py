"""
System Validator / Theaterverse Final
Core Kernel - Immutable Center Unit

This module represents the immutable kernel of the system. It provides the
bootstrap sequence, initializes the event bus, config loader, plugin registry,
and core API services. The kernel itself is **never modified**; all features are
extended via plugins.
"""

from .core_event_bus import EventBus
from .core_config_loader import ConfigLoader
from .core_plugin_registry import PluginRegistry
from .core_logging_config import configure_logging
from .core_error_handler import ErrorHandler


class CoreKernel:
    """Immutable system kernel"""

    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        self.event_bus = EventBus()
        self.config_loader = ConfigLoader(base_dir)
        self.plugin_registry = PluginRegistry(self.event_bus)
        self.error_handler = ErrorHandler()

    def bootstrap(self):
        """Perform system bootstrap sequence"""
        # Configure logging
        configure_logging()

        # Load core configuration
        config = self.config_loader.load()

        # Initialize plugin registry
        self.plugin_registry.load_all(config)

        # Emit kernel_ready event
        self.event_bus.emit("kernel_ready", {"base_dir": self.base_dir})

        return True


if __name__ == "__main__":
    import os

    base_dir = os.getenv(
        "SYSTEM_VALIDATOR_BASE_DIR",
        "/root/System_Validator/APP_DIR/theaterverse_final",
    )
    kernel = CoreKernel(base_dir)
    if kernel.bootstrap():
        print("[CoreKernel] Bootstrap complete.")

--- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/core/core_kernel.py
# /root/System_Validator/APP_DIR/theaterverse_final/core/core_kernel.py
# --- END OF STRUCTURE ---
