#!/usr/bin/env bash
# Add and/or remove tags on a selector.
#
# Endpoint: PATCH /api/selectors/{selector_id}/tags
# Auth:     Bearer API key
# Body:     {"add": ["tag1", ...], "remove": ["tag2", ...]}  (both optional)
#
# Tags can be referenced by name (created on the fly) or id. See
# POST /api/tags to create one explicitly.
#
# Usage:
#   ./patch_tags.sh <selector_id> add tag-name
#   ./patch_tags.sh <selector_id> remove tag-name
set -euo pipefail

HOST="${INTELSURF_HOST:-https://dev.intel.surf}"
: "${INTELSURF_API_KEY:?set INTELSURF_API_KEY=sk-slimestack-... before running}"
SELECTOR_ID="${1:?usage: $0 <selector_id> <add|remove> <tag-name>}"
OP="${2:?usage: $0 <selector_id> <add|remove> <tag-name>}"
TAG="${3:?usage: $0 <selector_id> <add|remove> <tag-name>}"

case "${OP}" in
  add)    BODY=$(printf '{"add":["%s"]}' "${TAG}") ;;
  remove) BODY=$(printf '{"remove":["%s"]}' "${TAG}") ;;
  *) echo "op must be 'add' or 'remove'" >&2; exit 1 ;;
esac

curl --fail-with-body --silent --show-error \
  --request PATCH \
  --header "Authorization: Bearer ${INTELSURF_API_KEY}" \
  --header "Content-Type: application/json" \
  --data "${BODY}" \
  "${HOST}/api/selectors/${SELECTOR_ID}/tags" \
  | python3 -m json.tool
