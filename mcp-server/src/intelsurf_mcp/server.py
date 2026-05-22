"""FastMCP server exposing IntelSurf tools over stdio.

Tools:
  * intelsurf_surf            - selector -> scan -> poll -> intel report
  * intelsurf_scan_get        - fetch one scan job
  * intelsurf_report_get      - fetch intel/summary/raw report
  * intelsurf_tool_list       - list available microservice tools
  * intelsurf_tool_run        - run a single microservice tool against a target
  * intelsurf_selector_list   - list recent selectors

Run: ``intelsurf-mcp`` (entry point from pyproject.toml) or
``python -m intelsurf_mcp.server``.
"""
from __future__ import annotations

import time
from typing import Any, Literal

from mcp.server.fastmcp import FastMCP

from . import client

TERMINAL = {"Complete", "Failed", "Cancelled", "complete", "failed", "cancelled"}

mcp = FastMCP("intelsurf")


@mcp.tool()
def intelsurf_surf(
    target: str,
    scan_mode: Literal["quick", "deep"] = "quick",
    poll_timeout_seconds: int = 600,
) -> dict[str, Any]:
    """Run the full IntelSurf workflow against a target.

    Creates a selector, kicks off a scan, polls until terminal, then returns
    the scan record with the rendered intel report attached. Equivalent to
    ``intelsurf surf <target> --wait``.

    Args:
        target: Domain, IP, URL, FQDN, or email headers to scan.
        scan_mode: ``quick`` (fast subset of tools) or ``deep`` (full run).
        poll_timeout_seconds: Maximum time to wait for the scan to finish.

    Returns:
        A dict with ``selector``, ``scan``, and ``intel_md`` keys.
    """
    selector = client.post("/api/selectors", json_body={"value": target})
    scan = client.post(
        "/api/scan-jobs",
        json_body={"selector_id": selector["id"], "scan_mode": scan_mode},
    )
    scan_id = scan["id"]

    deadline = time.time() + poll_timeout_seconds
    final = scan
    while time.time() < deadline:
        final = client.get(f"/api/scan-jobs/{scan_id}")
        if (final.get("status") or final.get("state") or "") in TERMINAL:
            break
        time.sleep(4)
    else:
        return {"selector": selector, "scan": final, "intel_md": "", "timed_out": True}

    intel_md = ""
    if (final.get("status") or "").lower() == "complete":
        intel_md = client.get_text(f"/api/reports/{scan_id}/intel.md")

    return {"selector": selector, "scan": final, "intel_md": intel_md}


@mcp.tool()
def intelsurf_scan_get(scan_job_id: int) -> dict[str, Any]:
    """Fetch the current state of a scan job.

    Args:
        scan_job_id: Integer id returned from a previous scan creation.
    """
    return client.get(f"/api/scan-jobs/{scan_job_id}")


@mcp.tool()
def intelsurf_report_get(
    scan_job_id: int,
    kind: Literal["intel", "summary", "raw"] = "intel",
    ext: Literal["md", "json"] = "md",
) -> str:
    """Download a report for a completed scan.

    Args:
        scan_job_id: Scan job id.
        kind: ``intel`` (LLM-synthesized), ``summary`` (short), ``raw`` (tool output).
        ext: ``md`` for markdown, ``json`` for structured.
    """
    return client.get_text(f"/api/reports/{scan_job_id}/{kind}.{ext}")


@mcp.tool()
def intelsurf_tool_list() -> list[dict[str, Any]]:
    """List every IntelSurf microservice tool you can invoke."""
    payload = client.get("/api/tools")
    return payload.get("items", payload) if isinstance(payload, dict) else payload


@mcp.tool()
def intelsurf_tool_run(
    tool_slug: str,
    target: str,
    timeout_seconds: float | None = None,
) -> dict[str, Any]:
    """Run a single IntelSurf microservice tool against a target.

    Args:
        tool_slug: Slug from ``intelsurf_tool_list`` (e.g. ``whois``, ``ssl_check``).
        target: Domain, IP, URL, etc. the tool understands.
        timeout_seconds: Optional override; server caps at 300.
    """
    body: dict[str, Any] = {"target": target}
    if timeout_seconds is not None:
        body["timeout"] = timeout_seconds
    return client.post(f"/api/tools/{tool_slug}/run", json_body=body)


@mcp.tool()
def intelsurf_selector_list(limit: int = 20) -> list[dict[str, Any]]:
    """List your recently-created selectors.

    Args:
        limit: How many to return (server cap applies).
    """
    payload = client.get(f"/api/selectors?limit={limit}")
    return payload.get("items", payload) if isinstance(payload, dict) else payload


def main() -> None:
    """Entry point — stdio transport."""
    mcp.run()


if __name__ == "__main__":
    main()
