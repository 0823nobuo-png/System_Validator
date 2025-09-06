#!/usr/bin/env bash
# System Validator / Theaterverse Final
# Environment setup script

set -euo pipefail

BASE_DIR="${SYSTEM_VALIDATOR_BASE_DIR:-/root/System_Validator/APP_DIR/theaterverse_final}"
ENV_FILE="$BASE_DIR/.env"
TEMPLATE="$BASE_DIR/config/config_env_template.env"

if [ -f "$ENV_FILE" ]; then
  echo "[EnvSetup] .env already exists at $ENV_FILE"
  exit 0
fi

cp "$TEMPLATE" "$ENV_FILE"
echo "[EnvSetup] Created .env from template. Please edit values as needed."

--- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/scripts/script_env_setup.sh
# /root/System_Validator/APP_DIR/theaterverse_final/scripts/script_env_setup.sh
# --- END OF STRUCTURE ---
