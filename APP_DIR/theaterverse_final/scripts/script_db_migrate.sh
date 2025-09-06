#!/usr/bin/env bash
# System Validator / Theaterverse Final
# Database migration script

set -euo pipefail

BASE_DIR="${SYSTEM_VALIDATOR_BASE_DIR:-/root/System_Validator/APP_DIR/theaterverse_final}"
MIGRATIONS="$BASE_DIR/db/db_migrations_core.sql"

if [ -z "${SYSTEM_VALIDATOR_DSN:-}" ]; then
  echo "[DBMigrate] SYSTEM_VALIDATOR_DSN is not set"
  exit 1
fi

psql "$SYSTEM_VALIDATOR_DSN" -f "$MIGRATIONS"
echo "[DBMigrate] Migration applied successfully."

--- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/scripts/script_db_migrate.sh
# /root/System_Validator/APP_DIR/theaterverse_final/scripts/script_db_migrate.sh
# --- END OF STRUCTURE ---
