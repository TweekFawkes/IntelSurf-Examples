#!/usr/bin/env python3
"""Create a selector, then list the most recent ones.

Endpoints:
  POST /api/selectors           body: {"value", "selector_type"?, "project_id"?}
  GET  /api/selectors           query: project_id?, limit?
Auth: Bearer API key
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
    parser.add_argument("target", help="selector value (domain, IP, URL, ...)")
    args = parser.parse_args()

    if not api_key_from_env():
        print("set INTELSURF_API_KEY=sk-slimestack-... before running")
        return 2

    base = host_from_env()
    headers = bearer_headers()

    print(f"[create] POST /api/selectors  value={args.target}")
    created = http_request(
        base_url=base,
        path="/api/selectors",
        method="POST",
        json_body={"value": args.target},
        headers=headers,
    ).raise_for_status()
    selector = created.json()
    print(json.dumps(selector, indent=2))

    print("\n[list] GET /api/selectors?limit=5")
    listed = http_request(
        base_url=base,
        path="/api/selectors?limit=5",
        headers=headers,
    ).raise_for_status()

    payload = listed.json()
    items = payload.get("items", payload) if isinstance(payload, dict) else payload
    for s in items[:5] if isinstance(items, list) else []:
        print(f"  id={s.get('id'):<6} {s.get('value', '?'):<30} type={s.get('selector_type', '?')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
