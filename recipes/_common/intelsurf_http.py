"""Tiny stdlib-only HTTP helper used by every Python recipe in this repo.

Lifted (with light edits) from the IntelSurf live test suite. Stdlib-only on
purpose: every recipe should run with nothing but a Python 3.11+ interpreter.

Two public entry points:

* :func:`http_request` - synchronous, returns :class:`HttpResult`.
* :class:`Session` - convenience wrapper that holds a cookie jar so
  authenticated flows (login -> /me) stay terse.

Environment variables read by recipes (not by this module directly):

* ``INTELSURF_HOST`` - default ``https://dev.intel.surf``.
* ``INTELSURF_API_KEY`` - ``sk-slimestack-...`` token from
  https://dev.intel.surf/app/account/api-keys.
"""
from __future__ import annotations

import http.cookiejar
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from typing import Any

DEFAULT_HOST = "https://dev.intel.surf"


def host_from_env() -> str:
    return os.environ.get("INTELSURF_HOST", DEFAULT_HOST).rstrip("/")


def api_key_from_env() -> str | None:
    return os.environ.get("INTELSURF_API_KEY")


def bearer_headers() -> dict[str, str]:
    """Return ``Authorization: Bearer ...`` if INTELSURF_API_KEY is set."""
    key = api_key_from_env()
    return {"Authorization": f"Bearer {key}"} if key else {}


@dataclass(frozen=True)
class HttpResult:
    status: int
    headers: dict[str, str]
    body: str

    def json(self) -> Any:
        return json.loads(self.body)

    def raise_for_status(self) -> "HttpResult":
        if self.status >= 400:
            raise SystemExit(
                f"HTTP {self.status} from IntelSurf:\n{self.body[:1000]}"
            )
        return self


def http_request(
    *,
    base_url: str,
    path: str,
    method: str = "GET",
    json_body: Any = None,
    headers: dict[str, str] | None = None,
    timeout: float = 30.0,
    cookies: http.cookiejar.CookieJar | None = None,
) -> HttpResult:
    """Single live HTTP request.

    Returns :class:`HttpResult` even on non-2xx (raises only on network
    errors / timeouts). If ``cookies`` is provided, Set-Cookie headers in
    the response are merged into the jar so a follow-up request can carry
    the session.
    """
    url = f"{base_url}{path}"
    data = None if json_body is None else json.dumps(json_body).encode("utf-8")
    request_headers = {"Accept": "application/json"}
    if data is not None:
        request_headers["Content-Type"] = "application/json"
    if headers:
        request_headers.update(headers)

    req = urllib.request.Request(
        url, data=data, headers=request_headers, method=method.upper()
    )
    if cookies is not None:
        cookies.add_cookie_header(req)

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            result = HttpResult(
                status=int(resp.status),
                headers={k.lower(): v for k, v in resp.headers.items()},
                body=raw.decode("utf-8", errors="replace"),
            )
            if cookies is not None:
                cookies.extract_cookies(resp, req)
            return result
    except urllib.error.HTTPError as exc:
        raw = exc.read()
        result = HttpResult(
            status=int(exc.code),
            headers={k.lower(): v for k, v in exc.headers.items()},
            body=raw.decode("utf-8", errors="replace"),
        )
        if cookies is not None:
            cookies.extract_cookies(exc, req)
        return result


@dataclass
class Session:
    """Cookie-bearing client for cookie-authenticated flows.

    For Bearer-token (API key) flows, you don't need a Session - pass the
    headers from :func:`bearer_headers` to :func:`http_request` directly.
    """

    base_url: str = field(default_factory=host_from_env)
    timeout: float = 30.0
    cookies: http.cookiejar.CookieJar = field(
        default_factory=http.cookiejar.CookieJar
    )

    def get(self, path: str, **kwargs: Any) -> HttpResult:
        return self._request(path, method="GET", **kwargs)

    def post(self, path: str, **kwargs: Any) -> HttpResult:
        return self._request(path, method="POST", **kwargs)

    def patch(self, path: str, **kwargs: Any) -> HttpResult:
        return self._request(path, method="PATCH", **kwargs)

    def delete(self, path: str, **kwargs: Any) -> HttpResult:
        return self._request(path, method="DELETE", **kwargs)

    def _request(self, path: str, *, method: str, **kwargs: Any) -> HttpResult:
        return http_request(
            base_url=self.base_url,
            path=path,
            method=method,
            timeout=self.timeout,
            cookies=self.cookies,
            **kwargs,
        )
