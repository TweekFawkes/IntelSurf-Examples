#!/usr/bin/env bash
# Refresh openapi/openapi.json from the live IntelSurf deployment.
#
# Usage:
#   ./openapi/refresh.sh                      # uses https://dev.intel.surf
#   INTELSURF_HOST=https://intel.surf ./openapi/refresh.sh
#
# Run from the repo root. Commits are manual — review the diff first.
set -euo pipefail

HOST="${INTELSURF_HOST:-https://dev.intel.surf}"
OUT="$(dirname "$0")/openapi.json"

echo "[refresh] fetching ${HOST}/api/openapi.json"
curl -fsSL "${HOST}/api/openapi.json" | python3 -m json.tool > "${OUT}"

TITLE=$(python3 -c "import json; print(json.load(open('${OUT}'))['info']['title'])")
VERSION=$(python3 -c "import json; print(json.load(open('${OUT}'))['info'].get('version','?'))")
PATHS=$(python3 -c "import json; print(len(json.load(open('${OUT}'))['paths']))")

echo "[refresh] ${OUT}  title=${TITLE}  version=${VERSION}  paths=${PATHS}"
