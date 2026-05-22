#!/usr/bin/env bash
# Create a scan job against an existing selector.
#
# Endpoint: POST /api/scan-jobs
# Auth:     Bearer API key
# Body:     {"selector_id": <int>, "scan_mode": "quick"|"deep", "tools"?: [...], "is_public"?: false}
#
# Usage:
#   export INTELSURF_API_KEY=sk-slimestack-...
#   ./create_scan.sh <selector_id>
#   ./create_scan.sh <selector_id> quick
set -euo pipefail

HOST="${INTELSURF_HOST:-https://dev.intel.surf}"
: "${INTELSURF_API_KEY:?set INTELSURF_API_KEY=sk-slimestack-... before running}"
SELECTOR_ID="${1:?usage: $0 <selector_id> [scan_mode]}"
SCAN_MODE="${2:-deep}"

curl --fail-with-body --silent --show-error \
  --header "Authorization: Bearer ${INTELSURF_API_KEY}" \
  --header "Content-Type: application/json" \
  --data "$(printf '{"selector_id":%s,"scan_mode":"%s"}' "${SELECTOR_ID}" "${SCAN_MODE}")" \
  "${HOST}/api/scan-jobs" \
  | python3 -m json.tool
