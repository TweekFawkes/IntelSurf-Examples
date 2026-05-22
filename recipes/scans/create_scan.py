#!/usr/bin/env python3
"""Create a scan job against an existing selector.

Endpoint: POST /api/scan-jobs
Auth:     Bearer API key
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
    parser.add_argument("--scan-mode", choices=["quick", "deep"], default="deep")
    parser.add_argument("--is-public", action="store_true", help="include in the public feed")
    parser.add_argument("--tool", action="append", default=[], help="restrict to specific tools (repeatable)")
    args = parser.parse_args()

    if not api_key_from_env():
        print("set INTELSURF_API_KEY=sk-slimestack-... before running")
        return 2

    body = {
        "selector_id": args.selector_id,
        "scan_mode": args.scan_mode,
        "is_public": args.is_public,
    }
    if args.tool:
        body["tools"] = args.tool

    result = http_request(
        base_url=host_from_env(),
        path="/api/scan-jobs",
        method="POST",
        headers=bearer_headers(),
        json_body=body,
    ).raise_for_status()

    scan = result.json()
    print(json.dumps(scan, indent=2))
    print(f"\nscan_job_id={scan.get('id')}  poll with scans/poll_scan.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
