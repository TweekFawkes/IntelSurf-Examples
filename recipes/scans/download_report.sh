#!/usr/bin/env bash
# Download the LLM-synthesized intel report for a completed scan.
#
# Endpoint: GET /api/reports/{scan_job_id}/intel.{ext}    ext = md | json | pdf
# Auth:     Bearer API key
# Also:     /api/reports/{scan_job_id}/summary.{ext}
#           /api/reports/{scan_job_id}/raw.{ext}
#
# Usage:
#   export INTELSURF_API_KEY=sk-slimestack-...
#   ./download_report.sh <scan_job_id>           # intel.md to stdout
#   ./download_report.sh <scan_job_id> json      # intel.json to stdout
#   ./download_report.sh <scan_job_id> md ./report.md
set -euo pipefail

HOST="${INTELSURF_HOST:-https://dev.intel.surf}"
: "${INTELSURF_API_KEY:?set INTELSURF_API_KEY=sk-slimestack-... before running}"
SCAN_JOB_ID="${1:?usage: $0 <scan_job_id> [ext] [out-path]}"
EXT="${2:-md}"
OUT="${3:--}"

curl --fail-with-body --silent --show-error \
  --header "Authorization: Bearer ${INTELSURF_API_KEY}" \
  --output "${OUT}" \
  "${HOST}/api/reports/${SCAN_JOB_ID}/intel.${EXT}"

if [[ "${OUT}" != "-" ]]; then
  echo "wrote ${OUT}"
fi
