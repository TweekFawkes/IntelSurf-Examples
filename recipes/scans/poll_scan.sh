#!/usr/bin/env bash
# Poll a scan job until it reaches a terminal state.
#
# Endpoint: GET /api/scan-jobs/{scan_job_id}
# Auth:     Bearer API key
# Terminal states: complete, failed, cancelled
#
# Usage:
#   export INTELSURF_API_KEY=sk-slimestack-...
#   ./poll_scan.sh <scan_job_id>
set -euo pipefail

HOST="${INTELSURF_HOST:-https://dev.intel.surf}"
: "${INTELSURF_API_KEY:?set INTELSURF_API_KEY=sk-slimestack-... before running}"
SCAN_JOB_ID="${1:?usage: $0 <scan_job_id>}"
INTERVAL="${INTERVAL:-3}"
TIMEOUT="${TIMEOUT:-300}"

deadline=$(($(date +%s) + TIMEOUT))
while [[ $(date +%s) -lt ${deadline} ]]; do
  RESP=$(curl --fail-with-body --silent --show-error \
    --header "Authorization: Bearer ${INTELSURF_API_KEY}" \
    --header "Accept: application/json" \
    "${HOST}/api/scan-jobs/${SCAN_JOB_ID}")
  STATE=$(printf '%s' "${RESP}" | python3 -c 'import json,sys;d=json.load(sys.stdin);print(d.get("status") or d.get("state") or "?")' 2>/dev/null || echo "?")
  printf 'state=%-12s ' "${STATE}"
  date +%H:%M:%S
  case "${STATE}" in
    Complete|Failed|Cancelled|complete|failed|cancelled)
      printf '%s\n' "${RESP}" | python3 -m json.tool
      exit 0
      ;;
  esac
  sleep "${INTERVAL}"
done

echo "timed out after ${TIMEOUT}s" >&2
exit 2
