#!/usr/bin/env bash
# Extract IntelSurf selectors from free-form text via the NLP endpoint.
#
# Endpoint: POST /api/selectors/extract
# Auth:     none (rate-limited 30/hour per IP; daily cap is host-configurable)
# Body:     {"prompt": "<free text>"}
#
# Usage:
#   ./extract.sh "find anything related to example.com and 1.2.3.4"
set -euo pipefail

HOST="${INTELSURF_HOST:-https://dev.intel.surf}"
PROMPT="${1:?usage: $0 \"<free-text prompt>\"}"

curl --fail-with-body --silent --show-error \
  --header "Content-Type: application/json" \
  --header "Accept: application/json" \
  --data "$(python3 -c 'import json,sys;print(json.dumps({"prompt": sys.argv[1]}))' "${PROMPT}")" \
  "${HOST}/api/selectors/extract" \
  | python3 -m json.tool
