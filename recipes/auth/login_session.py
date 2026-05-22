#!/usr/bin/env python3
"""Log in to IntelSurf, capture the session cookie, then call /me.

Endpoint: POST /api/auth/login
Auth:     none (creates a slimestack_session cookie)
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _common.intelsurf_http import Session, host_from_env


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("email")
    parser.add_argument("password")
    args = parser.parse_args()

    session = Session(base_url=host_from_env())
    login = session.post(
        "/api/auth/login",
        json_body={"email": args.email, "password": args.password},
    )
    if login.status >= 400:
        print(f"login failed  HTTP {login.status}\n{login.body}")
        return 1
    print(f"logged in  cookies={[c.name for c in session.cookies]}")

    # Re-use the cookie jar for the next call.
    me = session.get("/api/auth/me").raise_for_status()
    user = me.json()
    print(f"  id={user.get('id')}  email={user.get('email')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
