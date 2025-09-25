"""
System Validator / Theaterverse Final
Plugin: Backup Verifier Job

Provides a scheduled backup verification process.
"""

import logging
import os
import subprocess
from fastapi import APIRouter

logger = logging.getLogger(__name__)


def register(event_bus):
    logger.info("Registering plugin: plugin_backup_verifier")
    event_bus.subscribe("kernel_ready", _on_kernel_ready)


def _on_kernel_ready(payload):
    logger.info("plugin_backup_verifier: kernel ready: %s", payload)


def _verify_backup():
    backup_file = os.getenv("BACKUP_FILE", "/var/backups/system_validator.dump")
    if not os.path.exists(backup_file):
        return {"status": "missing", "file": backup_file}
    try:
        result = subprocess.run(
            ["file", backup_file], capture_output=True, text=True, check=True
        )
        return {"status": "ok", "file": backup_file, "details": result.stdout.strip()}
    except Exception as e:
        return {"status": "error", "file": backup_file, "error": str(e)}


def routes(app):
    router = APIRouter()

    @router.get("/backup/verify")
    async def verify():
        return _verify_backup()

    app.include_router(router)


# --- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/plugins/plugin_backup_verifier/plugin_backup_verifier_job.py
# /root/System_Validator/APP_DIR/theaterverse_final/plugins/plugin_backup_verifier/plugin_backup_verifier_job.py
# --- END OF STRUCTURE ---
