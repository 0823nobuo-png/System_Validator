-- System Validator / Theaterverse Final
-- Plugin: PostgreSQL Storage Schema

BEGIN;

-- Example table for plugin-specific state
CREATE TABLE IF NOT EXISTS storage_plugin_state (
    id BIGSERIAL PRIMARY KEY,
    key TEXT UNIQUE NOT NULL,
    value JSONB,
    updated_at TIMESTAMP DEFAULT NOW()
);

COMMIT;

--- END OF STRUCTURE ---
-- /root/System_Validator/APP_DIR/theaterverse_final/plugins/plugin_storage_postgres/plugin_storage_postgres_schema.sql
# /root/System_Validator/APP_DIR/theaterverse_final/plugins/plugin_storage_postgres/plugin_storage_postgres_schema.sql
# --- END OF STRUCTURE ---
