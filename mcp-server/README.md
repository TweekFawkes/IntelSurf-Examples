# intelsurf-mcp

A minimal [Model Context Protocol](https://modelcontextprotocol.io) server
that exposes IntelSurf scan/selector tools to MCP-aware clients (Claude
Desktop, Claude Code, etc.) via stdio.

## What it gives the agent

Six tools, all backed by the public IntelSurf REST API:

| MCP tool | What it does |
| --- | --- |
| `intelsurf_surf` | selector → scan → poll → intel report (the headline workflow) |
| `intelsurf_scan_get` | fetch one scan job by id |
| `intelsurf_report_get` | fetch the intel/summary/raw report for a scan |
| `intelsurf_tool_list` | list available microservice tools |
| `intelsurf_tool_run` | run one microservice tool against a target |
| `intelsurf_selector_list` | list your recent selectors |

## Install

```bash
git clone https://github.com/TweekFawkes/IntelSurf-Examples
cd IntelSurf-Examples/mcp-server
pip install -e .
intelsurf-mcp --help        # nothing to print; the server is stdio-driven
```

Or, once a release is cut, `pip install intelsurf-mcp` (TBD).

## Configure your MCP client

### Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)
or `%APPDATA%/Claude/claude_desktop_config.json` (Windows). Add:

```json
{
  "mcpServers": {
    "intelsurf": {
      "command": "intelsurf-mcp",
      "env": {
        "INTELSURF_HOST": "https://dev.intel.surf",
        "INTELSURF_API_KEY": "sk-slimestack-..."
      }
    }
  }
}
```

Restart Claude Desktop. Open a conversation and ask:

> Use IntelSurf to scan example.com and summarize the result.

Claude will pick `intelsurf_surf`, wait for the scan, and write the summary.

### Claude Code CLI

Claude Code reads MCP servers from `~/.config/claude-code/mcp.json` (or the
project-local equivalent):

```json
{
  "mcpServers": {
    "intelsurf": {
      "command": "intelsurf-mcp",
      "env": {
        "INTELSURF_API_KEY": "sk-slimestack-..."
      }
    }
  }
}
```

### Other clients

Any client that supports MCP stdio servers can use this. The shape is the
same: a `command` to launch and `env` with `INTELSURF_API_KEY` (and
optionally `INTELSURF_HOST`).

## Configuration

| Env var | Default | Required |
| --- | --- | --- |
| `INTELSURF_HOST` | `https://dev.intel.surf` | no |
| `INTELSURF_API_KEY` | — | **yes** |

Mint an API key at
[`dev.intel.surf/app/account/api-keys`](https://dev.intel.surf/app/account/api-keys).

## Why duplicate the HTTP client?

The MCP server ships its own ~80-line `client.py` rather than importing the
recipe helper. Rationale: a pip-installable MCP server should be
runnable in isolation. Reaching into a sibling `recipes/` directory at
runtime would break that. The duplication is small and intentional.

## Tests

```bash
pip install -e ".[dev]"
pytest
```

Tests are import-only smoke checks — they don't hit the live API.

## Versioning

`0.1.0` is the initial cut. The MCP Python SDK (`mcp` on PyPI) is still
evolving; this server pins to `>=1.0,<2.0`. If a 2.x breaks compatibility, the
server will need a follow-up release.

## Trouble

- **`INTELSURF_API_KEY is not set`** — the env block in your MCP client
  config didn't reach the server. On macOS Claude Desktop, the config file
  format is strict JSON — no comments, no trailing commas.
- **`HTTP 401`** — key was rejected. Mint a fresh one.
- **`Tool not found`** — your MCP client cached the tool list from before the
  server was restarted. Restart the client.
