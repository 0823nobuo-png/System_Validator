"""
System Validator / Theaterverse Final
Core Plugin Registry - dynamic plugin loading and lifecycle management.

Responsible for scanning plugin directories, loading manifests and adapters,
and registering them to the event bus.
"""

import importlib.util
import json
import logging
import os
from typing import Any, Dict

from .core_event_bus import EventBus

logger = logging.getLogger(__name__)


class PluginRegistry:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.plugins: Dict[str, Any] = {}

    def load_all(self, config: Dict[str, Any]):
        base_dir = config.get(
            "SYSTEM_VALIDATOR_BASE_DIR",
            "/root/System_Validator/APP_DIR/theaterverse_final",
        )
        plugin_dir = os.path.join(base_dir, "plugins")

        for entry in os.scandir(plugin_dir):
            if entry.is_dir() and entry.name.startswith("plugin_"):
                self._load_plugin(entry.path)

    def _load_plugin(self, path: str):
        manifest_file = None
        for f in os.listdir(path):
            if f.endswith("_manifest.json"):
                manifest_file = os.path.join(path, f)
                break

        if not manifest_file:
            logger.warning("No manifest found in %s", path)
            return

        with open(manifest_file, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        plugin_name = manifest.get("name") or os.path.basename(path)
        adapter_file = manifest.get("adapter")
        if not adapter_file:
            logger.warning("No adapter specified in manifest for %s", plugin_name)
            return

        adapter_path = os.path.join(path, adapter_file)
        if not os.path.exists(adapter_path):
            logger.warning("Adapter file missing: %s", adapter_path)
            return

        spec = importlib.util.spec_from_file_location(plugin_name, adapter_path)
        if not spec or not spec.loader:
            logger.error("Failed to create spec for %s", adapter_path)
            return

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, "register"):
            module.register(self.event_bus)
            self.plugins[plugin_name] = module
            logger.info("Loaded plugin: %s", plugin_name)
        else:
            logger.warning("Plugin %s has no register() function", plugin_name)


# --- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/core/core_plugin_registry.py
# /root/System_Validator/APP_DIR/theaterverse_final/core/core_plugin_registry.py
# --- END OF STRUCTURE ---
