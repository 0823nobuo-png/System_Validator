"""
deploy_bluegreen.py

目的（強化⑥ 運用自動化）：
- Blue/Green デプロイのリリース切替
- Gitタグ/リリースIDに紐付くリリースディレクトリをアトミックに切替
- 事前/事後ヘルスチェック
- 失敗時は自動ロールバック
- Slack/メール通知（任意・環境変数で有効化）

正式パス：/root/System_Validator/APP_DIR/theaterverse_final/scripts/deploy_bluegreen.py
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
RELEASES = APP_ROOT / "releases"            # 例：releases/2025-09-05_1234_gittag
CURRENT  = APP_ROOT / "current"              # 稼働中へのシンボリックリンク
HEALTH_URL = os.environ.get("HEALTH_URL", "http://127.0.0.1:8000/health")
NEW_RELEASE = os.environ.get("NEW_RELEASE")  # 必須：切替対象ディレクトリ名

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

    # 事前ヘルス
    if not check_health(HEALTH_URL, timeout=5.0):
        notify("Blue/Green Warning", "Pre-switch health check failed (current)")

    # 切替
    atomic_symlink(new_path, CURRENT)

    # 再起動（systemd 経由を推奨）
    try:
        subprocess.run(["systemctl", "restart", "system_validator.service"], check=True)
    except Exception:
        notify("Blue/Green Info", "systemctl restart failed; ensure unit file is installed")

    # 事後ヘルス（新リリース）
    for i in range(10):
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
