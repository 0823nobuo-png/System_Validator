#!/usr/bin/env bash
# System Validator / Theaterverse Final
# Blue/Green deployment script

set -euo pipefail

BASE_DIR="${SYSTEM_VALIDATOR_BASE_DIR:-/root/System_Validator/APP_DIR/theaterverse_final}"
SLOT="${1:-B}" # Default to B if not specified

CURRENT_SLOT="${BLUEGREEN_SLOT:-A}"
NEW_SLOT="$SLOT"

if [ "$CURRENT_SLOT" == "$NEW_SLOT" ]; then
  echo "[BlueGreen] Already on slot $CURRENT_SLOT"
  exit 0
fi

echo "[BlueGreen] Deploying slot $NEW_SLOT..."

# Export new slot to env
echo "BLUEGREEN_SLOT=$NEW_SLOT" > "$BASE_DIR/.bluegreen_env"

# Restart API with new slot
systemctl --user restart system_validator.service || true

# Health check
sleep 5
STATUS=$(curl -s http://localhost:8080/health || echo fail)
if [[ "$STATUS" != *"ok"* ]]; then
  echo "[BlueGreen] Health check failed, rolling back to $CURRENT_SLOT"
  echo "BLUEGREEN_SLOT=$CURRENT_SLOT" > "$BASE_DIR/.bluegreen_env"
  systemctl --user restart system_validator.service || true
  exit 1
fi

echo "[BlueGreen] Switched to slot $NEW_SLOT successfully."

--- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/scripts/script_deploy_bluegreen.sh
# /root/System_Validator/APP_DIR/theaterverse_final/scripts/script_deploy_bluegreen.sh
# --- END OF STRUCTURE ---
