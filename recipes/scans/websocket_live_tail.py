#!/usr/bin/env python3
"""Live-tail scan-job state via the WebSocket endpoint.

Endpoint: WS  /api/scan-jobs/{scan_job_id}/ws
Auth:     session cookie ONLY (no Bearer support).
          We log in with email/password to obtain it.

Requirements:
  pip install websockets

Why a third-party dep? Python stdlib has no WebSocket client, only a
server-side handler. ``websockets`` is the standard async client and is the
only non-stdlib dep across every recipe in this repo.

Usage:
  export INTELSURF_HOST=https://dev.intel.surf
  export INTELSURF_EMAIL=me@example.com
  export INTELSURF_PASSWORD=hunter2
  python websocket_live_tail.py <scan_job_id>
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from urllib.parse import urlparse

try:
    import websockets
except ImportError:
    print("error: websockets is not installed. Run: pip install websockets", file=sys.stderr)
    raise SystemExit(2)

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _common.intelsurf_http import Session, host_from_env

TERMINAL = {"Complete", "Failed", "Cancelled", "complete", "failed", "cancelled"}


def cookie_header_from_session(session: Session) -> str:
    """Format the cookie jar back into a Cookie: header for the WS handshake."""
    parts = [f"{c.name}={c.value}" for c in session.cookies]
    return "; ".join(parts)


def ws_url(host: str, scan_job_id: int) -> str:
    parsed = urlparse(host)
    scheme = "wss" if parsed.scheme == "https" else "ws"
    return f"{scheme}://{parsed.netloc}/api/scan-jobs/{scan_job_id}/ws"


async def run(host: str, email: str, password: str, scan_job_id: int) -> int:
    session = Session(base_url=host)
    login = session.post(
        "/api/auth/login", json_body={"email": email, "password": password}
    )
    if login.status >= 400:
        print(f"login failed  HTTP {login.status}\n{login.body}")
        return 1
    cookie_header = cookie_header_from_session(session)

    url = ws_url(host, scan_job_id)
    print(f"connecting  {url}")
    async with websockets.connect(
        url, additional_headers={"Cookie": cookie_header}
    ) as ws:
        while True:
            try:
                raw = await ws.recv()
            except websockets.ConnectionClosed:
                print("server closed the connection")
                return 0
            payload = json.loads(raw)
            state = payload.get("status") or payload.get("state") or "?"
            print(
                f"frame  state={state}  risk={payload.get('risk_score', '?')}  "
                f"tools={len(payload.get('tools', []))}"
            )
            if state in TERMINAL:
                print(f"terminal  exiting")
                return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scan_job_id", type=int)
    args = parser.parse_args()

    email = os.environ.get("INTELSURF_EMAIL")
    password = os.environ.get("INTELSURF_PASSWORD")
    if not email or not password:
        print("set INTELSURF_EMAIL and INTELSURF_PASSWORD before running", file=sys.stderr)
        return 2

    return asyncio.run(run(host_from_env(), email, password, args.scan_job_id))


if __name__ == "__main__":
    raise SystemExit(main())
