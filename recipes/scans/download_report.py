#!/usr/bin/env python3
"""Download the LLM-synthesized intel report for a completed scan.

Endpoint: GET /api/reports/{scan_job_id}/{kind}.{ext}
          kind = intel | summary | raw
          ext  = md | json | pdf
Auth:     Bearer API key
"""
from __future__ import annotations

import argparse
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
    parser.add_argument("scan_job_id", type=int)
    parser.add_argument("--kind", choices=["intel", "summary", "raw"], default="intel")
    parser.add_argument("--ext", choices=["md", "json", "pdf"], default="md")
    parser.add_argument("--out", type=Path, help="output path (default: stdout)")
    args = parser.parse_args()

    if not api_key_from_env():
        print("set INTELSURF_API_KEY=sk-slimestack-... before running")
        return 2

    result = http_request(
        base_url=host_from_env(),
        path=f"/api/reports/{args.scan_job_id}/{args.kind}.{args.ext}",
        headers=bearer_headers(),
    ).raise_for_status()

    if args.out:
        args.out.write_text(result.body)
        print(f"wrote {len(result.body)} bytes -> {args.out}")
    else:
        sys.stdout.write(result.body)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
