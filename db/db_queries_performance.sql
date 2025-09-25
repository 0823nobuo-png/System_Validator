-- System Validator / Theaterverse Final
-- Performance-related queries and indexes

BEGIN;

-- Index for audit_logs created_at
CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON audit_logs(created_at);

-- Index for plugin_registry plugin_name
CREATE INDEX IF NOT EXISTS idx_plugin_registry_name ON plugin_registry(plugin_name);

-- Index for backup_verifications checked_at
CREATE INDEX IF NOT EXISTS idx_backup_verifications_checked_at ON backup_verifications(checked_at);

-- Query: Get last 100 audit logs
-- SELECT * FROM audit_logs ORDER BY created_at DESC LIMIT 100;

-- Query: Count active plugins
-- SELECT COUNT(*) FROM plugin_registry WHERE enabled = TRUE;

COMMIT;

--- END OF STRUCTURE ---
-- /root/System_Validator/APP_DIR/theaterverse_final/db/db_queries_performance.sql
# /root/System_Validator/APP_DIR/theaterverse_final/db/db_queries_performance.sql
# --- END OF STRUCTURE ---
