#!/usr/bin/env python3
"""Headline workflow: selector -> scan -> poll -> intel report.

Mirrors ``intelsurf surf <target> --wait``. End-to-end exercise of:

  POST /api/selectors
  POST /api/scan-jobs
  GET  /api/scan-jobs/{id}             (poll loop)
  GET  /api/reports/{id}/intel.md

Auth: Bearer API key in INTELSURF_API_KEY.
"""
from __future__ import annotations

import argparse
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
    parser.add_argument("target", help="domain / IP / URL / email-headers to scan")
    parser.add_argument("--scan-mode", choices=["quick", "deep"], default="quick")
    parser.add_argument("--out-dir", type=Path, default=Path("./intelsurf-runs"))
    parser.add_argument("--poll-interval", type=float, default=4.0)
    parser.add_argument("--poll-timeout", type=float, default=600.0)
    args = parser.parse_args()

    if not api_key_from_env():
        print("set INTELSURF_API_KEY=sk-slimestack-... before running")
        return 2

    base = host_from_env()
    headers = bearer_headers()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[1/4] create selector  value={args.target}")
    selector = http_request(
        base_url=base,
        path="/api/selectors",
        method="POST",
        headers=headers,
        json_body={"value": args.target},
    ).raise_for_status().json()
    print(f"  selector_id={selector['id']}  type={selector.get('selector_type')}")

    print(f"[2/4] create scan job  scan_mode={args.scan_mode}")
    scan = http_request(
        base_url=base,
        path="/api/scan-jobs",
        method="POST",
        headers=headers,
        json_body={"selector_id": selector["id"], "scan_mode": args.scan_mode},
    ).raise_for_status().json()
    scan_id = scan["id"]
    print(f"  scan_job_id={scan_id}")

    print("[3/4] poll until terminal")
    deadline = time.time() + args.poll_timeout
    final = None
    while time.time() < deadline:
        poll = http_request(
            base_url=base,
            path=f"/api/scan-jobs/{scan_id}",
            headers=headers,
        ).raise_for_status().json()
        state = poll.get("status") or poll.get("state") or "?"
        print(f"  state={state}  risk={poll.get('risk_score', '?')}")
        if state in TERMINAL:
            final = poll
            break
        time.sleep(args.poll_interval)

    if not final:
        print(f"timed out after {args.poll_timeout}s")
        return 2
    if (final.get("status") or "").lower() != "complete":
        print(f"scan terminal but not complete: {final.get('status')}")
        return 1

    print("[4/4] download intel report")
    report = http_request(
        base_url=base,
        path=f"/api/reports/{scan_id}/intel.md",
        headers=headers,
    ).raise_for_status()
    out = args.out_dir / f"{scan_id}-intel.md"
    out.write_text(report.body)
    print(f"  wrote {len(report.body)} bytes -> {out}")
    print()
    print(report.body[:1500])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
