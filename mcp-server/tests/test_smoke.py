"""Smoke tests for the MCP server module.

These don't hit the live IntelSurf API. They verify the package imports,
the FastMCP server registers the expected tool surface, and the client
module raises a sane error when INTELSURF_API_KEY is missing.
"""
from __future__ import annotations

import os
import pytest


def test_package_imports() -> None:
    import intelsurf_mcp
    import intelsurf_mcp.client
    import intelsurf_mcp.server

    assert intelsurf_mcp.__version__


def test_tools_registered() -> None:
    from intelsurf_mcp.server import mcp

    expected = {
        "intelsurf_surf",
        "intelsurf_scan_get",
        "intelsurf_report_get",
        "intelsurf_tool_list",
        "intelsurf_tool_run",
        "intelsurf_selector_list",
    }
    # FastMCP exposes registered tools via list_tools() (async) or its
    # internal registry. Use the introspection helper if present, else fall
    # back to the attribute that holds the manager.
    registered: set[str] = set()
    tool_mgr = getattr(mcp, "_tool_manager", None) or getattr(mcp, "tool_manager", None)
    if tool_mgr is not None:
        tools = getattr(tool_mgr, "_tools", None) or getattr(tool_mgr, "tools", None)
        if isinstance(tools, dict):
            registered = set(tools.keys())
    if not registered:
        pytest.skip("FastMCP internals changed; couldn't introspect tool list")

    assert expected.issubset(registered), f"missing tools: {expected - registered}"


def test_client_requires_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    from intelsurf_mcp import client

    monkeypatch.delenv("INTELSURF_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="INTELSURF_API_KEY"):
        client.api_key()


def test_host_default() -> None:
    from intelsurf_mcp import client

    os.environ.pop("INTELSURF_HOST", None)
    assert client.host() == "https://dev.intel.surf"
