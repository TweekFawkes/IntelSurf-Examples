#!/usr/bin/env bash
# Headline workflow: create a selector, launch a scan, poll until complete,
# download the intel report. Mirrors `intelsurf surf <target> --wait`.
#
# Endpoints used:
#   POST /api/selectors
#   POST /api/scan-jobs
#   GET  /api/scan-jobs/{id}        (poll loop)
#   GET  /api/reports/{id}/intel.md
#
# Usage:
#   export INTELSURF_API_KEY=sk-slimestack-...
#   ./surf_one_shot.sh example.com
set -euo pipefail

HOST="${INTELSURF_HOST:-https://dev.intel.surf}"
: "${INTELSURF_API_KEY:?set INTELSURF_API_KEY=sk-slimestack-... before running}"
TARGET="${1:?usage: $0 <target>}"
SCAN_MODE="${SCAN_MODE:-quick}"
OUT_DIR="${OUT_DIR:-./intelsurf-runs}"

mkdir -p "${OUT_DIR}"

echo "[1/4] create selector  value=${TARGET}"
SELECTOR=$(curl --fail-with-body --silent --show-error \
  --header "Authorization: Bearer ${INTELSURF_API_KEY}" \
  --header "Content-Type: application/json" \
  --data "$(printf '{"value":"%s"}' "${TARGET}")" \
  "${HOST}/api/selectors")
SELECTOR_ID=$(printf '%s' "${SELECTOR}" | python3 -c 'import json,sys;print(json.load(sys.stdin)["id"])')
echo "  selector_id=${SELECTOR_ID}"

echo "[2/4] create scan job  scan_mode=${SCAN_MODE}"
SCAN=$(curl --fail-with-body --silent --show-error \
  --header "Authorization: Bearer ${INTELSURF_API_KEY}" \
  --header "Content-Type: application/json" \
  --data "$(printf '{"selector_id":%s,"scan_mode":"%s"}' "${SELECTOR_ID}" "${SCAN_MODE}")" \
  "${HOST}/api/scan-jobs")
SCAN_JOB_ID=$(printf '%s' "${SCAN}" | python3 -c 'import json,sys;print(json.load(sys.stdin)["id"])')
echo "  scan_job_id=${SCAN_JOB_ID}"

echo "[3/4] poll until terminal"
while :; do
  RESP=$(curl --fail-with-body --silent --show-error \
    --header "Authorization: Bearer ${INTELSURF_API_KEY}" \
    "${HOST}/api/scan-jobs/${SCAN_JOB_ID}")
  STATE=$(printf '%s' "${RESP}" | python3 -c 'import json,sys;print(json.load(sys.stdin).get("status","?"))')
  printf '  state=%s\n' "${STATE}"
  case "${STATE}" in
    Complete|complete)
      RISK=$(printf '%s' "${RESP}" | python3 -c 'import json,sys;print(json.load(sys.stdin).get("risk_score","?"))')
      echo "  risk_score=${RISK}"
      break
      ;;
    Failed|failed|Cancelled|cancelled)
      echo "  terminal but not complete; aborting"
      exit 1
      ;;
  esac
  sleep 4
done

echo "[4/4] download intel report"
REPORT_PATH="${OUT_DIR}/${SCAN_JOB_ID}-intel.md"
curl --fail-with-body --silent --show-error \
  --header "Authorization: Bearer ${INTELSURF_API_KEY}" \
  --output "${REPORT_PATH}" \
  "${HOST}/api/reports/${SCAN_JOB_ID}/intel.md"
echo "  wrote ${REPORT_PATH}"
echo
head -30 "${REPORT_PATH}"
