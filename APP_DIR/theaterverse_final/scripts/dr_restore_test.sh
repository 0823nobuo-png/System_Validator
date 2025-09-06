#!/usr/bin/env bash
# dr_restore_test.sh
# 目的：強化⑤ バックアップ戦略の高度化（隔離環境でのDRテスト自動化）
# - 直近バックアップの整合性確認
# - 隔離用一時DBへリストア
# - 検証クエリ実行＆結果レポート化
# - 成功/失敗コードでCIに連携
#
# 正式パス：/root/System_Validator/APP_DIR/theaterverse_final/scripts/dr_restore_test.sh

set -Eeuo pipefail
IFS=$'\n\t'

# ------- 設定（環境変数で上書き可能） ------- #
: "${PG_BIN:=/usr/bin}"
: "${PGHOST:=127.0.0.1}"
: "${PGPORT:=5432}"
: "${PGUSER:=postgres}"
: "${PGPASSWORD:=postgres}"
: "${TARGET_DB:=system_validator}"              # 本番系の論理名
: "${DR_DB:=system_validator_drtest}"           # DR検証用一時DB名
: "${BACKUP_DIR:=/var/backups/system_validator}" # pg_dump 出力格納想定
: "${LATEST_PATTERN:=backup_*.sql.gz}"          # 例：backup_2025-09-01T00-00-00.sql.gz
: "${REPORT:=dr_restore_report.txt}"

export PGPASSWORD

log() { printf "[%%s] %s\n" "$(date '+%Y-%m-%dT%H:%M:%S%z')" "$*" ; }
fail() { log "ERROR: $*" ; exit 1 ; }

need_bin() {
  command -v "$1" >/dev/null 2>&1 || fail "required binary not found: $1"
}

# 必要コマンド確認
need_bin "$PG_BIN/psql"
need_bin "$PG_BIN/dropdb"
need_bin "$PG_BIN/createdb"
need_bin "$PG_BIN/pg_restore" || true # .sql.gz の場合は未使用
need_bin gunzip
need_bin grep

# 最新バックアップ検出
log "searching backup in: $BACKUP_DIR ($LATEST_PATTERN)"
LATEST_FILE=$(ls -1t "$BACKUP_DIR"/$LATEST_PATTERN 2>/dev/null | head -n1 || true)
[[ -n "$LATEST_FILE" ]] || fail "no backup file found"
log "found backup: $LATEST_FILE"

# DR用DB作り直し
log "dropping DR database if exists: $DR_DB"
"$PG_BIN/psql" -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d postgres -v ON_ERROR_STOP=1 -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='$DR_DB';" || true
"$PG_BIN/dropdb" -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" "$DR_DB" || true
log "creating DR database: $DR_DB"
"$PG_BIN/createdb" -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" "$DR_DB"

# リストア（.sql.gz を想定）
TMP_SQL=$(mktemp)
trap 'rm -f "$TMP_SQL"' EXIT
log "decompressing backup..."
gunzip -c "$LATEST_FILE" > "$TMP_SQL"
log "restoring into $DR_DB ..."
"$PG_BIN/psql" -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$DR_DB" -v ON_ERROR_STOP=1 -f "$TMP_SQL"

# 整合性検証クエリ（必要に応じて拡張）
log "running validation queries..."
{
  echo "# DR Restore Report"
  echo "timestamp: $(date -u +%FT%TZ)"
  echo "backup_file: $LATEST_FILE"
  echo "host: $PGHOST port: $PGPORT user: $PGUSER db: $DR_DB"
  echo
  echo "## basic checks"
  "$PG_BIN/psql" -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$DR_DB" -A -F $'\t' -v ON_ERROR_STOP=1 -c "SELECT current_database(), NOW();"
  echo
  echo "## relation counts"
  "$PG_BIN/psql" -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$DR_DB" -A -F $'\t' -v ON_ERROR_STOP=1 -c "SELECT schemaname, relkind, count(*) FROM pg_catalog.pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace GROUP BY 1,2 ORDER BY 1,2;"
  echo
  echo "## table row samples"
  for t in auth_audit_logs llm_call_logs system_events; do
    echo "### $t (top 5)"
    "$PG_BIN/psql" -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$DR_DB" -A -F $'\t' -v ON_ERROR_STOP=1 -c "SELECT * FROM $t LIMIT 5;" || echo "(table not found)"
    echo
  done
} > "$REPORT"

# エラーパターン（簡易）検出
if grep -E "ERROR|FATAL|permission denied" -i "$REPORT" >/dev/null 2>&1; then
  log "validation detected errors; see $REPORT"
  exit 2
fi

log "DR test success; report saved: $REPORT"
exit 0

# --- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/scripts/dr_restore_test.sh
# /root/System_Validator/APP_DIR/theaterverse_final/scripts/dr_restore_test.sh
# --- END OF STRUCTURE ---
