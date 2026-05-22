#!/usr/bin/env bash
# Print the authenticated user (Bearer-token flow).
#
# Endpoint: GET /api/auth/me
# Auth:     Bearer API key OR slimestack_session cookie
#
# Usage:
#   export INTELSURF_API_KEY=sk-slimestack-...
#   ./me.sh
set -euo pipefail

HOST="${INTELSURF_HOST:-https://dev.intel.surf}"
: "${INTELSURF_API_KEY:?set INTELSURF_API_KEY=sk-slimestack-... before running}"

curl --fail-with-body --silent --show-error \
  --header "Accept: application/json" \
  --header "Authorization: Bearer ${INTELSURF_API_KEY}" \
  "${HOST}/api/auth/me" \
  | python3 -m json.tool
