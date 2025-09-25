#!/usr/bin/env bash
# create_validator_user.sh
# 正式パス：/root/System_Validator/APP_DIR/theaterverse_final/scripts/create_validator_user.sh
# 目的：systemd unit 用の実行ユーザ/権限を準備

set -euo pipefail
user=validator
group=validator
app_root=/root/System_Validator/APP_DIR/theaterverse_final
writable_dir="$app_root/current/var"

if ! getent group "$group" >/dev/null; then
  sudo groupadd --system "$group"
fi
if ! id -u "$user" >/dev/null 2>&1; then
  sudo useradd --system --no-create-home --shell /usr/sbin/nologin -g "$group" "$user"
fi

sudo mkdir -p "$writable_dir"
sudo chown -R "$user":"$group" "$writable_dir"
sudo chmod 750 "$writable_dir"

echo "validator user prepared."

# --- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/scripts/create_validator_user.sh
# /root/System_Validator/APP_DIR/theaterverse_final/scripts/create_validator_user.sh
# --- END OF STRUCTURE ---
