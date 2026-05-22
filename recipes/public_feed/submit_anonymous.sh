#!/usr/bin/env bash
# Submit an anonymous scan against IntelSurf and print the public slug.
#
# Endpoint: POST /api/scan-jobs/anonymous
# Auth:     none (rate-limited 5/hour, 20/day per IP)
# Body:     {"selector": "<target>", "scan_mode": "quick"|"deep"}
#
# Usage:
#   ./submit_anonymous.sh example.com
set -euo pipefail

HOST="${INTELSURF_HOST:-https://dev.intel.surf}"
TARGET="${1:?usage: $0 <target>}"

curl --fail-with-body --silent --show-error \
  --header "Content-Type: application/json" \
  --header "Accept: application/json" \
  --data "$(printf '{"selector":"%s","scan_mode":"quick"}' "${TARGET}")" \
  "${HOST}/api/scan-jobs/anonymous" \
  | python3 -m json.tool
