"""
deploy_bluegreen.py

逶ｮ逧・ｼ亥ｼｷ蛹問則 驕狗畑閾ｪ蜍募喧・会ｼ・- Blue/Green 繝・・繝ｭ繧､縺ｮ繝ｪ繝ｪ繝ｼ繧ｹ蛻・崛
- Git繧ｿ繧ｰ/繝ｪ繝ｪ繝ｼ繧ｹID縺ｫ邏蝉ｻ倥￥繝ｪ繝ｪ繝ｼ繧ｹ繝・ぅ繝ｬ繧ｯ繝医Μ繧偵い繝医Α繝・け縺ｫ蛻・崛
- 莠句燕/莠句ｾ後・繝ｫ繧ｹ繝√ぉ繝・け
- 螟ｱ謨玲凾縺ｯ閾ｪ蜍輔Ο繝ｼ繝ｫ繝舌ャ繧ｯ
- Slack/繝｡繝ｼ繝ｫ騾夂衍・井ｻｻ諢上・迺ｰ蠅・､画焚縺ｧ譛牙柑蛹厄ｼ・
豁｣蠑上ヱ繧ｹ・・root/System_Validator/APP_DIR/theaterverse_final/scripts/deploy_bluegreen.py
"""
from __future__ import annotations

import os
import json
import time
import shutil
import socket
import subprocess
from pathlib import Path
from typing import Optional

APP_ROOT = Path(os.environ.get("APP_ROOT", "/root/System_Validator/APP_DIR/theaterverse_final"))
RELEASES = APP_ROOT / "releases"            # 萓具ｼ嗷eleases/2025-09-05_1234_gittag
CURRENT  = APP_ROOT / "current"              # 遞ｼ蜒堺ｸｭ縺ｸ縺ｮ繧ｷ繝ｳ繝懊Μ繝・け繝ｪ繝ｳ繧ｯ
HEALTH_URL = os.environ.get("HEALTH_URL", "http://127.0.0.1:8000/health")
NEW_RELEASE = os.environ.get("NEW_RELEASE")  # 蠢・茨ｼ壼・譖ｿ蟇ｾ雎｡繝・ぅ繝ｬ繧ｯ繝医Μ蜷・
SLACK_WEBHOOK = os.environ.get("SLACK_WEBHOOK")
MAIL_TO = os.environ.get("MAIL_TO")
MAIL_CMD = os.environ.get("MAIL_CMD", "mail")


def notify(title: str, message: str) -> None:
    payload = {"title": title, "message": message, "host": socket.gethostname(), "ts": int(time.time())}
    if SLACK_WEBHOOK:
        try:
            import urllib.request
            req = urllib.request.Request(SLACK_WEBHOOK, data=json.dumps({"text": f"[{title}] {message}"}).encode("utf-8"), headers={"Content-Type": "application/json"})
            urllib.request.urlopen(req, timeout=5).read()
        except Exception:
            pass
    if MAIL_TO:
        try:
            subprocess.run([MAIL_CMD, "-s", title, MAIL_TO], input=message.encode("utf-8"), check=False)
        except Exception:
            pass


def check_health(url: str, timeout: float = 5.0) -> bool:
    try:
        import urllib.request
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return 200 <= r.status < 300
    except Exception:
        return False


def atomic_symlink(target: Path, link: Path) -> None:
    tmp_link = link.with_suffix(".tmp")
    if tmp_link.exists() or tmp_link.is_symlink():
        tmp_link.unlink()
    tmp_link.symlink_to(target)
    tmp_link.replace(link)


def rollback(prev: Optional[Path]) -> None:
    if prev and prev.exists():
        atomic_symlink(prev, CURRENT)
        notify("Blue/Green Rollback", f"Rolled back to {prev}")


def main() -> None:
    if not NEW_RELEASE:
        raise SystemExit("NEW_RELEASE env is required (directory under releases)")
    new_path = RELEASES / NEW_RELEASE
    if not new_path.exists():
        raise SystemExit(f"release not found: {new_path}")

    prev_target = None
    if CURRENT.is_symlink():
        prev_target = CURRENT.resolve()

    notify("Blue/Green Start", f"Switching to {new_path}")

    # 莠句燕繝倥Ν繧ｹ
    if not check_health(HEALTH_URL, timeout=5.0):
        notify("Blue/Green Warning", "Pre-switch health check failed (current)")

    # 蛻・崛
    atomic_symlink(new_path, CURRENT)

    # 蜀崎ｵｷ蜍包ｼ・ystemd 邨檎罰繧呈耳螂ｨ・・    try:
        subprocess.run(["systemctl", "restart", "system_validator.service"], check=True)
    except Exception:
        notify("Blue/Green Info", "systemctl restart failed; ensure unit file is installed")

    # 莠句ｾ後・繝ｫ繧ｹ・域眠繝ｪ繝ｪ繝ｼ繧ｹ・・    for i in range(10):
        if check_health(HEALTH_URL, timeout=3.0):
            notify("Blue/Green Success", f"Now serving {new_path}")
            break
        time.sleep(1 + i * 0.5)
    else:
        notify("Blue/Green Failure", f"New release unhealthy: {new_path}; rolling back")
        rollback(prev_target)
        raise SystemExit(2)


if __name__ == "__main__":
    main()

# --- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/scripts/deploy_bluegreen.py
# /root/System_Validator/APP_DIR/theaterverse_final/scripts/deploy_bluegreen.py
# --- END OF STRUCTURE ---
