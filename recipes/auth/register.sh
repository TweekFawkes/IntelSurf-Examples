#!/usr/bin/env bash
# Register a new IntelSurf account.
#
# Endpoint: POST /api/auth/register
# Auth:     none (some deployments require an invite code)
# Body:     {"email", "password", "invite_code"?}
# Side effects: sets a session cookie (slimestack_session)
#
# Usage:
#   ./register.sh me@example.com hunter2 INVITE-CODE
set -euo pipefail

HOST="${INTELSURF_HOST:-https://dev.intel.surf}"
EMAIL="${1:?usage: $0 <email> <password> [invite_code]}"
PASSWORD="${2:?usage: $0 <email> <password> [invite_code]}"
INVITE="${3:-}"

BODY=$(python3 -c '
import json, sys
payload = {"email": sys.argv[1], "password": sys.argv[2]}
if sys.argv[3]:
    payload["invite_code"] = sys.argv[3]
print(json.dumps(payload))
' "${EMAIL}" "${PASSWORD}" "${INVITE}")

curl --fail-with-body --silent --show-error \
  --cookie-jar ./cookies.txt \
  --header "Content-Type: application/json" \
  --header "Accept: application/json" \
  --data "${BODY}" \
  "${HOST}/api/auth/register" \
  | python3 -m json.tool

echo "session cookie written to ./cookies.txt"
