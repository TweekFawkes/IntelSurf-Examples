#!/usr/bin/env python3
"""List recent public scans from the IntelSurf homepage feed.

Endpoint: GET /api/public/scans
Auth:     none (public; rate-limited 60/min per IP)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _common.intelsurf_http import host_from_env, http_request


def main() -> int:
    result = http_request(
        base_url=host_from_env(),
        path="/api/public/scans?sort=recent&page_size=5",
    ).raise_for_status()

    payload = result.json()
    print(f"# {payload.get('total', '?')} total public scans  (showing 5)\n")
    for scan in payload.get("items", [])[:5]:
        print(
            f"{scan.get('public_slug', '?'):<20} "
            f"{scan.get('selector_value', '?'):<30} "
            f"risk={scan.get('risk_score', '?'):<3} "
            f"{scan.get('status', '?')}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
