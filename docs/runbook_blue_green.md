# Blue/Green 切替 Runbook

正式パス：/root/System_Validator/APP_DIR/theaterverse_final/docs/runbook_blue_green.md

---

## 前提
- `releases/` にビルド済みディレクトリがあり、`current` は稼働中リリースへのシンボリックリンク
- `systemd/system_validator.service` が稼働中

## 手順
1. 新リリースを配置：`releases/<NEW_RELEASE>`
2. 事前ヘルス（現行）：`curl http://127.0.0.1:8000/health`
3. 切替実行：
   ```bash
   NEW_RELEASE=<NEW_RELEASE> \
   HEALTH_URL=http://127.0.0.1:8000/health \
   python scripts/deploy_bluegreen.py
   ```
4. 監視：通知（Slack/メール）を確認
5. 失敗時：自動ロールバックを確認（`current` が旧リリースに戻る）

## 成功基準
- `/health` が 200 を継続
- ログにエラーがない

---

--- END OF STRUCTURE ---
<!-- /root/System_Validator/APP_DIR/theaterverse_final/docs/runbook_blue_green.md -->

/root/System_Validator/APP_DIR/theaterverse_final/docs/runbook_blue_green.md
--- END OF STRUCTURE ---
