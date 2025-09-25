"""
System Validator / Theaterverse Final
Plugin: PostgreSQL Storage Adapter

Provides PostgreSQL storage operations for persistence. Exposes register()
method for plugin registry.
"""

import logging
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_connection_pool import DBPool

logger = logging.getLogger(__name__)

db_pool = DBPool()


def register(event_bus):
    logger.info("Registering plugin: plugin_storage_postgres")
    event_bus.subscribe("kernel_ready", _on_kernel_ready)


def _on_kernel_ready(payload):
    logger.info("plugin_storage_postgres: kernel ready: %s", payload)


def routes(app):
    router = APIRouter()

    async def get_session():
        async for session in db_pool.get_session():
            yield session

    @router.get("/storage/plugins")
    async def list_plugins(session: AsyncSession = Depends(get_session)):
        result = await session.execute("SELECT plugin_name, enabled FROM plugin_registry")
        rows = result.fetchall()
        return {"plugins": [{"name": r[0], "enabled": r[1]} for r in rows]}

    app.include_router(router)


# --- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/plugins/plugin_storage_postgres/plugin_storage_postgres_adapter.py
# /root/System_Validator/APP_DIR/theaterverse_final/plugins/plugin_storage_postgres/plugin_storage_postgres_adapter.py
# --- END OF STRUCTURE ---
