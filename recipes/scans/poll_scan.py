#!/usr/bin/env python3
"""Poll a scan job until it reaches a terminal state.

Endpoint: GET /api/scan-jobs/{scan_job_id}
Auth:     Bearer API key
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _common.intelsurf_http import (
    api_key_from_env,
    bearer_headers,
    host_from_env,
    http_request,
)

TERMINAL = {"Complete", "Failed", "Cancelled", "complete", "failed", "cancelled"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scan_job_id", type=int)
    parser.add_argument("--interval", type=float, default=3.0)
    parser.add_argument("--timeout", type=float, default=300.0)
    args = parser.parse_args()

    if not api_key_from_env():
        print("set INTELSURF_API_KEY=sk-slimestack-... before running")
        return 2

    base = host_from_env()
    headers = bearer_headers()
    deadline = time.time() + args.timeout

    while time.time() < deadline:
        result = http_request(
            base_url=base,
            path=f"/api/scan-jobs/{args.scan_job_id}",
            headers=headers,
        )
        if result.status >= 400:
            print(f"HTTP {result.status}\n{result.body}")
            return 1
        scan = result.json()
        state = scan.get("status") or scan.get("state") or "?"
        print(f"  state={state}  risk={scan.get('risk_score', '?')}")
        if state in TERMINAL:
            print(json.dumps(scan, indent=2))
            return 0 if state.lower() == "complete" else 1
        time.sleep(args.interval)

    print(f"timed out after {args.timeout}s")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
