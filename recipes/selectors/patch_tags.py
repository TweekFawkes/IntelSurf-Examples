#!/usr/bin/env python3
"""Add or remove tags on a selector.

Endpoint: PATCH /api/selectors/{selector_id}/tags
Auth:     Bearer API key
Body:     {"add": [...], "remove": [...]}  (both optional, both lists)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _common.intelsurf_http import (
    api_key_from_env,
    bearer_headers,
    host_from_env,
    http_request,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("selector_id", type=int)
    parser.add_argument("--add", action="append", default=[], help="tag(s) to add (repeatable)")
    parser.add_argument("--remove", action="append", default=[], help="tag(s) to remove (repeatable)")
    args = parser.parse_args()

    if not api_key_from_env():
        print("set INTELSURF_API_KEY=sk-slimestack-... before running")
        return 2
    if not args.add and not args.remove:
        print("supply at least one --add or --remove")
        return 2

    payload = {}
    if args.add:
        payload["add"] = args.add
    if args.remove:
        payload["remove"] = args.remove

    result = http_request(
        base_url=host_from_env(),
        path=f"/api/selectors/{args.selector_id}/tags",
        method="PATCH",
        headers=bearer_headers(),
        json_body=payload,
    ).raise_for_status()

    print(json.dumps(result.json(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
