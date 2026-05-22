#!/usr/bin/env bash
# Log in to IntelSurf with email/password and capture the session cookie.
#
# Endpoint: POST /api/auth/login
# Auth:     none (creates a slimestack_session cookie)
# Body:     {"email", "password"}
#
# Usage:
#   ./login_session.sh me@example.com hunter2
#   curl --cookie ./cookies.txt https://dev.intel.surf/api/auth/me
set -euo pipefail

HOST="${INTELSURF_HOST:-https://dev.intel.surf}"
EMAIL="${1:?usage: $0 <email> <password>}"
PASSWORD="${2:?usage: $0 <email> <password>}"

curl --fail-with-body --silent --show-error \
  --cookie-jar ./cookies.txt \
  --header "Content-Type: application/json" \
  --header "Accept: application/json" \
  --data "$(python3 -c 'import json,sys;print(json.dumps({"email":sys.argv[1],"password":sys.argv[2]}))' "${EMAIL}" "${PASSWORD}")" \
  "${HOST}/api/auth/login" \
  | python3 -m json.tool

echo "session cookie written to ./cookies.txt"
echo "follow-up: curl --cookie ./cookies.txt ${HOST}/api/auth/me"
