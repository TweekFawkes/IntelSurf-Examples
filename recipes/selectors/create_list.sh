#!/usr/bin/env bash
# Create a selector, then list selectors.
#
# Endpoints:
#   POST /api/selectors           body: {"value": "<target>", "selector_type"?}
#   GET  /api/selectors           query: project_id?, limit?
# Auth: Bearer API key
#
# Usage:
#   export INTELSURF_API_KEY=sk-slimestack-...
#   ./create_list.sh example.com
set -euo pipefail

HOST="${INTELSURF_HOST:-https://dev.intel.surf}"
: "${INTELSURF_API_KEY:?set INTELSURF_API_KEY=sk-slimestack-... before running}"
TARGET="${1:?usage: $0 <target-value>}"

echo "[create] POST /api/selectors"
curl --fail-with-body --silent --show-error \
  --header "Authorization: Bearer ${INTELSURF_API_KEY}" \
  --header "Content-Type: application/json" \
  --data "$(printf '{"value":"%s"}' "${TARGET}")" \
  "${HOST}/api/selectors" \
  | python3 -m json.tool

echo
echo "[list] GET /api/selectors?limit=5"
curl --fail-with-body --silent --show-error \
  --header "Authorization: Bearer ${INTELSURF_API_KEY}" \
  --header "Accept: application/json" \
  "${HOST}/api/selectors?limit=5" \
  | python3 -m json.tool
