#!/usr/bin/env python3
"""Register a new IntelSurf account and capture the session cookie.

Endpoint: POST /api/auth/register
Auth:     none (invite code may be required by the deployment)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _common.intelsurf_http import Session, host_from_env


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("email")
    parser.add_argument("password")
    parser.add_argument("--invite-code")
    args = parser.parse_args()

    payload = {"email": args.email, "password": args.password}
    if args.invite_code:
        payload["invite_code"] = args.invite_code

    session = Session(base_url=host_from_env())
    result = session.post("/api/auth/register", json_body=payload)
    if result.status >= 400:
        print(f"HTTP {result.status}\n{result.body}")
        return 1

    user = result.json()
    print(f"registered  id={user.get('id')}  email={user.get('email')}")
    print(f"cookies captured: {[c.name for c in session.cookies]}")
    # Cookie jar lives in session.cookies for follow-up requests.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
