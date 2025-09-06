#!/usr/bin/env bash
# System Validator / Theaterverse Final
# Database dump script

set -euo pipefail

if [ -z "${SYSTEM_VALIDATOR_DSN:-}" ]; then
  echo "[DBDump] SYSTEM_VALIDATOR_DSN is not set"
  exit 1
fi

BACKUP_DIR="/var/backups"
mkdir -p "$BACKUP_DIR"
BACKUP_FILE="$BACKUP_DIR/system_validator.dump"

pg_dump "$SYSTEM_VALIDATOR_DSN" > "$BACKUP_FILE"
echo "[DBDump] Backup created at $BACKUP_FILE"

--- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/scripts/script_db_dump.sh
# /root/System_Validator/APP_DIR/theaterverse_final/scripts/script_db_dump.sh
# --- END OF STRUCTURE ---
