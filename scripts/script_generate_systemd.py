"""
System Validator / Theaterverse Final
Script: Generate systemd unit files

Generates systemd service and timer files for deployment.
"""

import os

BASE_DIR = os.getenv("SYSTEM_VALIDATOR_BASE_DIR", "/root/System_Validator/APP_DIR/theaterverse_final")
SYSTEMD_DIR = os.path.join(BASE_DIR, "systemd")


def generate_api_service():
    service = f"""[Unit]
Description=System Validator API Service
After=network.target

[Service]
ExecStart={BASE_DIR}/.venv/bin/python {BASE_DIR}/core/core_api_server.py
WorkingDirectory={BASE_DIR}
Restart=always
EnvironmentFile={BASE_DIR}/.env

[Install]
WantedBy=multi-user.target
"""
    path = os.path.join(SYSTEMD_DIR, "systemd_service_api.service")
    with open(path, "w", encoding="utf-8") as f:
        f.write(service)
    print(f"Generated {path}")


def generate_backup_service():
    service = f"""[Unit]
Description=System Validator Backup Verify
After=network.target

[Service]
ExecStart={BASE_DIR}/.venv/bin/python {BASE_DIR}/plugins/plugin_backup_verifier/plugin_backup_verifier_job.py
WorkingDirectory={BASE_DIR}
Restart=on-failure

[Install]
WantedBy=multi-user.target
"""
    path = os.path.join(SYSTEMD_DIR, "systemd_service_backup_verify.service")
    with open(path, "w", encoding="utf-8") as f:
        f.write(service)
    print(f"Generated {path}")


def generate_backup_timer():
    timer = """[Unit]
Description=Daily backup verification timer

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
"""
    path = os.path.join(SYSTEMD_DIR, "systemd_timer_backup_verify.timer")
    with open(path, "w", encoding="utf-8") as f:
        f.write(timer)
    print(f"Generated {path}")


if __name__ == "__main__":
    os.makedirs(SYSTEMD_DIR, exist_ok=True)
    generate_api_service()
    generate_backup_service()
    generate_backup_timer()

# --- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/scripts/script_generate_systemd.py
# /root/System_Validator/APP_DIR/theaterverse_final/scripts/script_generate_systemd.py
# --- END OF STRUCTURE ---
