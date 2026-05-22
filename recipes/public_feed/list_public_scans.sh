#!/usr/bin/env bash
# List recent public scans from the IntelSurf homepage feed.
#
# Endpoint: GET /api/public/scans
# Auth:     none (public; rate-limited 60/min per IP)
# Query:    page (default 1), page_size (default 20), sort (recent|risk)
set -euo pipefail

HOST="${INTELSURF_HOST:-https://dev.intel.surf}"
SORT="${SORT:-recent}"
PAGE_SIZE="${PAGE_SIZE:-5}"

curl --fail-with-body --silent --show-error \
  --header "Accept: application/json" \
  "${HOST}/api/public/scans?sort=${SORT}&page_size=${PAGE_SIZE}" \
  | python3 -m json.tool
