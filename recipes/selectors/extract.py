#!/usr/bin/env python3
"""Extract IntelSurf selectors from free-form text via the NLP endpoint.

Endpoint: POST /api/selectors/extract
Auth:     none (rate-limited 30/hour per IP)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _common.intelsurf_http import host_from_env, http_request


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompt", help="free-text input")
    args = parser.parse_args()

    result = http_request(
        base_url=host_from_env(),
        path="/api/selectors/extract",
        method="POST",
        json_body={"prompt": args.prompt},
    ).raise_for_status()

    print(json.dumps(result.json(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
