"""Minimal stdlib HTTP client for the IntelSurf REST API.

Duplicates ``recipes/_common/intelsurf_http.py`` on purpose: a pip-installed
MCP server should not reach into a sibling ``recipes/`` directory at runtime.
The duplication is ~80 lines and keeps the install side-effect-free.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any

DEFAULT_HOST = "https://dev.intel.surf"


def host() -> str:
    return os.environ.get("INTELSURF_HOST", DEFAULT_HOST).rstrip("/")


def api_key() -> str:
    key = os.environ.get("INTELSURF_API_KEY")
    if not key:
        raise RuntimeError(
            "INTELSURF_API_KEY is not set. Mint a key at "
            "https://dev.intel.surf/app/account/api-keys and add it to your "
            "MCP client config."
        )
    return key


@dataclass(frozen=True)
class HttpResult:
    status: int
    body: str

    def json(self) -> Any:
        return json.loads(self.body)


class ApiError(RuntimeError):
    def __init__(self, status: int, body: str):
        super().__init__(f"IntelSurf API error  HTTP {status}\n{body[:1000]}")
        self.status = status
        self.body = body


def request(
    method: str,
    path: str,
    *,
    json_body: Any = None,
    timeout: float = 60.0,
) -> HttpResult:
    url = f"{host()}{path}"
    data = None if json_body is None else json.dumps(json_body).encode("utf-8")
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key()}",
    }
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method.upper())
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return HttpResult(int(resp.status), resp.read().decode("utf-8", errors="replace"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise ApiError(int(exc.code), body) from exc


def get(path: str, **kw: Any) -> Any:
    return request("GET", path, **kw).json()


def post(path: str, json_body: Any = None, **kw: Any) -> Any:
    return request("POST", path, json_body=json_body, **kw).json()


def get_text(path: str, **kw: Any) -> str:
    return request("GET", path, **kw).body
