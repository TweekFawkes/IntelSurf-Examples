#!/usr/bin/env python3
"""Submit an anonymous scan and poll its public-feed entry until terminal.

Endpoint: POST /api/scan-jobs/anonymous     (submit)
          GET  /api/public/scans/{slug}     (poll)
Auth:     none (submit: 5/hour, 20/day per IP)
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _common.intelsurf_http import host_from_env, http_request

TERMINAL_STATES = {"complete", "failed", "cancelled"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", help="domain / IP / URL to scan")
    parser.add_argument("--poll-timeout", type=int, default=180)
    args = parser.parse_args()

    base = host_from_env()
    submit = http_request(
        base_url=base,
        path="/api/scan-jobs/anonymous",
        method="POST",
        json_body={"selector": args.target, "scan_mode": "quick"},
    ).raise_for_status()

    payload = submit.json()
    slug = payload.get("public_slug") or payload.get("slug")
    if not slug:
        print(f"submitted, but response has no slug: {payload}")
        return 1
    print(f"submitted  slug={slug}  state={payload.get('state', '?')}")

    deadline = time.time() + args.poll_timeout
    while time.time() < deadline:
        poll = http_request(base_url=base, path=f"/api/public/scans/{slug}")
        if poll.status != 200:
            print(f"poll  HTTP {poll.status}")
            time.sleep(3)
            continue
        scan = poll.json()
        state = scan.get("state", "?")
        print(f"poll  state={state}  risk={scan.get('risk_score', '?')}")
        if state in TERMINAL_STATES:
            print(f"\ndone  https://dev.intel.surf/scans/{slug}")
            return 0 if state == "complete" else 1
        time.sleep(3)

    print("timed out waiting for terminal state")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
