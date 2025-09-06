#!/usr/bin/env bash
# System Validator / Theaterverse Final
# Database restore script

set -euo pipefail

if [ -z "${SYSTEM_VALIDATOR_DSN:-}" ]; then
  echo "[DBRestore] SYSTEM_VALIDATOR_DSN is not set"
  exit 1
fi

BACKUP_FILE="${1:-/var/backups/system_validator.dump}"
if [ ! -f "$BACKUP_FILE" ]; then
  echo "[DBRestore] Backup file not found: $BACKUP_FILE"
  exit 1
fi

psql "$SYSTEM_VALIDATOR_DSN" < "$BACKUP_FILE"
echo "[DBRestore] Database restored from $BACKUP_FILE"

--- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/scripts/script_db_restore.sh
# /root/System_Validator/APP_DIR/theaterverse_final/scripts/script_db_restore.sh
# --- END OF STRUCTURE ---
