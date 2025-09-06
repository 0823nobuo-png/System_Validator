#!/usr/bin/env bash
set -euo pipefail
ROOT="${1:-.}"
BASELINE="${2:-}"

echo "[INFO] Running SystemValidator Verification Kit"
echo "[INFO] Project root: ${ROOT}"
if [[ -n "${BASELINE}" ]]; then
  echo "[INFO] Using baseline: ${BASELINE}"
else
  echo "[INFO] No baseline provided (diffs will be skipped unless given)"
fi

python3 "$(dirname "$0")/verificationkit_validator_scan.py" --root "${ROOT}" ${BASELINE:+--baseline "${BASELINE}"}

OUT_DIR="${ROOT}/_validator_outputs"
echo "[INFO] Done. Collected files:"
ls -lah "${OUT_DIR}" || true

echo ""
echo "Next steps:"
echo "1) Upload these files for review:"
echo "   - _validator_outputs/root_current.txt"
echo "   - _validator_outputs/manifest.json"
echo "   - _validator_outputs/lint_report.md"
echo "   - _validator_outputs/rule_violations.json"
echo "   - _validator_outputs/duplicates_report.txt"
echo "   - _validator_outputs/checksums.sha256"
echo "   - _validator_outputs/diffs/* (if baseline provided)"
echo ""
echo "[INFO] Completed."

# 近傍に正式パスヒントを記載：
# /root/System_Validator/APP_DIR/tools/VerificationKit/verificationkit_run_all.sh
--- END OF STRUCTURE ---
