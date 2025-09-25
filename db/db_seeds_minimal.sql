-- System Validator / Theaterverse Final
-- Minimal seed data for PostgreSQL

BEGIN;

-- Default admin user (password must be reset immediately)
INSERT INTO users (username, password_hash, role)
VALUES ('admin', '$2b$12$PLACEHOLDER_HASH', 'admin')
ON CONFLICT (username) DO NOTHING;

-- Default operator
INSERT INTO users (username, password_hash, role)
VALUES ('operator', '$2b$12$PLACEHOLDER_HASH', 'operator')
ON CONFLICT (username) DO NOTHING;

-- Default viewer
INSERT INTO users (username, password_hash, role)
VALUES ('viewer', '$2b$12$PLACEHOLDER_HASH', 'viewer')
ON CONFLICT (username) DO NOTHING;

COMMIT;

--- END OF STRUCTURE ---
-- /root/System_Validator/APP_DIR/theaterverse_final/db/db_seeds_minimal.sql
# /root/System_Validator/APP_DIR/theaterverse_final/db/db_seeds_minimal.sql
# --- END OF STRUCTURE ---
