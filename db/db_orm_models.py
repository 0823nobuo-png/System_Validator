"""
System Validator / Theaterverse Final
DB ORM Models - SQLAlchemy models for PostgreSQL
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP, JSON
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    role = Column(String, nullable=False, default="viewer")
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)
    event_type = Column(String, nullable=False)
    details = Column(JSON)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class BackupVerification(Base):
    __tablename__ = "backup_verifications"

    id = Column(Integer, primary_key=True)
    status = Column(String, nullable=False)
    checked_at = Column(TIMESTAMP, default=datetime.utcnow)
    details = Column(JSON)


class PluginRegistry(Base):
    __tablename__ = "plugin_registry"

    id = Column(Integer, primary_key=True)
    plugin_name = Column(String, nullable=False)
    version = Column(String)
    enabled = Column(Boolean, default=True)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)


# --- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/db/db_orm_models.py
# /root/System_Validator/APP_DIR/theaterverse_final/db/db_orm_models.py
# --- END OF STRUCTURE ---
