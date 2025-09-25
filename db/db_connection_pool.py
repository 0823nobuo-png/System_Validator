"""
System Validator / Theaterverse Final
DB Connection Pool - Async SQLAlchemy engine and session management.
"""

import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


class DBPool:
    def __init__(self):
        dsn = os.getenv(
            "SYSTEM_VALIDATOR_DSN",
            "postgresql+asyncpg://validator:validator@localhost:5432/validator",
        )
        if not dsn.startswith("postgresql"):
            raise ValueError("Only PostgreSQL DSN is supported")
        self.engine = create_async_engine(dsn, pool_pre_ping=True, future=True)
        self.session_factory = async_sessionmaker(self.engine, expire_on_commit=False)

    async def get_session(self):
        async with self.session_factory() as session:
            yield session


--- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/db/db_connection_pool.py
# /root/System_Validator/APP_DIR/theaterverse_final/db/db_connection_pool.py
# --- END OF STRUCTURE ---
