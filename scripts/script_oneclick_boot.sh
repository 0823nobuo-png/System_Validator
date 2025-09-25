#!/usr/bin/env bash
# System Validator / Theaterverse Final
# One-click boot script

set -euo pipefail

BASE_DIR="${SYSTEM_VALIDATOR_BASE_DIR:-/root/System_Validator/APP_DIR/theaterverse_final}"
VENV="$BASE_DIR/.venv"

# 1. Ensure Python virtualenv
if [ ! -d "$VENV" ]; then
  echo "[OneClick] Creating virtual environment..."
  python3.11 -m venv "$VENV"
fi
source "$VENV/bin/activate"
pip install --upgrade pip

# 2. Install dependencies
pip install -r "$BASE_DIR/requirements.txt"

# 3. Run DB migrations
"$BASE_DIR/scripts/script_db_migrate.sh"

# 4. Build UI (if not built)
if [ ! -d "$BASE_DIR/ui/dist" ]; then
  echo "[OneClick] Building UI..."
  pushd "$BASE_DIR/ui"
  npm ci || npm install
  npm run build
  popd
fi

# 5. Start API server
python "$BASE_DIR/core/core_api_server.py"

--- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/scripts/script_oneclick_boot.sh
# /root/System_Validator/APP_DIR/theaterverse_final/scripts/script_oneclick_boot.sh
# --- END OF STRUCTURE ---
