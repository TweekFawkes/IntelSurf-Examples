# IntelSurf Examples

Working integration examples for the [IntelSurf](https://intel.surf) SaaS REST
API — raw HTTP recipes, AI-coding-agent setup guides, an OpenAPI mirror, and a
small Model Context Protocol (MCP) server.

The companion CLI is `intelsurf`, installable in one line — see
[`ai-tools/claude-code.md`](ai-tools/claude-code.md) or
[dev.intel.surf/app/account/cli](https://dev.intel.surf/app/account/cli).

## What's here

| Directory | What's in it |
| --- | --- |
| [`recipes/`](recipes) | curl + Python snippets for the public REST endpoints — auth, projects, selectors, scans, public feed |
| [`ai-tools/`](ai-tools) | one-paste setup guides for Claude Code CLI, Claude Cowork, OpenAI Codex CLI, Cursor/Aider/Continue |
| [`openapi/`](openapi) | checked-in snapshot of `https://dev.intel.surf/api/openapi.json` + a refresh script |
| [`mcp-server/`](mcp-server) | minimal Python MCP server that exposes IntelSurf scan/selector tools to Claude Desktop and Claude Code |

## Fastest path

1. Mint an API key on [dev.intel.surf/app/account/api-keys](https://dev.intel.surf/app/account/api-keys).
2. Export it:

   ```bash
   export INTELSURF_HOST="https://dev.intel.surf"
   export INTELSURF_API_KEY="sk-slimestack-..."
   ```

3. Run an unauthenticated recipe to confirm the host is reachable:

   ```bash
   python recipes/public_feed/list_public_scans.py
   ```

4. Then the headline workflow — scan a target, wait, fetch the intel report:

   ```bash
   python recipes/scans/surf_one_shot.py example.com
   ```

That's it. Each recipe is a single file. Open the source — there's no framework
in the way.

## Conventions

- Every recipe is **runnable standalone** with `bash foo.sh` or `python foo.py`.
- Python recipes are **stdlib-only** unless the file's header note says
  otherwise (only `recipes/scans/websocket_live_tail.py` needs a third-party
  dep at v1).
- Recipes share `recipes/_common/intelsurf_http.py` — a 150-line `urllib`
  wrapper. Lifted from the live test suite in the main IntelSurf repo so the
  shape is already known to work.
- Configuration is read from `INTELSURF_HOST` and `INTELSURF_API_KEY` env vars.

## AI coding agents

The repo is structured so an AI coding agent (Claude Code, Codex, etc.) can
read it cold and produce working IntelSurf-driven code without any further
context. Point your agent at:

- `recipes/` for endpoint usage patterns
- `openapi/openapi.json` for the full schema
- `ai-tools/<your-tool>.md` for setup

See [`ai-tools/README.md`](ai-tools/README.md) for the per-tool matrix.

## Rate limits

Anonymous and public-feed endpoints are IP-rate-limited (e.g. 5
`/api/scan-jobs/anonymous` per hour, 60 `/api/public/scans` per minute). If a
recipe starts returning HTTP 429, that's the limiter — not a bug. Wait or
authenticate.

## Issues + recipe requests

Open one via the templates at [`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE).
We triage roughly weekly.

## License

[MIT](LICENSE).
