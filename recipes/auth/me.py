#!/usr/bin/env python3
"""Print the authenticated user (Bearer-token flow).

Endpoint: GET /api/auth/me
Auth:     Bearer API key from INTELSURF_API_KEY
"""
from __future__ import annotations

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
    if not api_key_from_env():
        print("set INTELSURF_API_KEY=sk-slimestack-... before running")
        return 2

    result = http_request(
        base_url=host_from_env(),
        path="/api/auth/me",
        headers=bearer_headers(),
    ).raise_for_status()

    print(json.dumps(result.json(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
