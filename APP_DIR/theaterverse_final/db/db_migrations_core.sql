-- System Validator / Theaterverse Final
-- Core PostgreSQL schema migrations

BEGIN;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'viewer',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Audit logs
CREATE TABLE IF NOT EXISTS audit_logs (
    id BIGSERIAL PRIMARY KEY,
    event_type TEXT NOT NULL,
    details JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Backup verification results
CREATE TABLE IF NOT EXISTS backup_verifications (
    id BIGSERIAL PRIMARY KEY,
    status TEXT NOT NULL,
    checked_at TIMESTAMP DEFAULT NOW(),
    details JSONB
);

-- Plugin registry state
CREATE TABLE IF NOT EXISTS plugin_registry (
    id BIGSERIAL PRIMARY KEY,
    plugin_name TEXT NOT NULL,
    version TEXT,
    enabled BOOLEAN DEFAULT TRUE,
    registered_at TIMESTAMP DEFAULT NOW()
);

COMMIT;

--- END OF STRUCTURE ---
-- /root/System_Validator/APP_DIR/theaterverse_final/db/db_migrations_core.sql
# /root/System_Validator/APP_DIR/theaterverse_final/db/db_migrations_core.sql
# --- END OF STRUCTURE ---
