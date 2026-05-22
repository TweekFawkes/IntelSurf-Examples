"""IntelSurf MCP server.

Exposes a handful of IntelSurf REST API operations as MCP tools, so AI agents
(Claude Desktop, Claude Code, anything else MCP-aware) can scan targets, fetch
intel reports, and run individual microservice tools through one stdio
transport.

Configuration is via environment variables:

* ``INTELSURF_HOST``     - default ``https://dev.intel.surf``
* ``INTELSURF_API_KEY``  - required; ``sk-slimestack-...``
"""
__version__ = "0.1.0"
