# Contributing

## Goals

This repo optimizes for one thing: **a reader can clone it and have a working
IntelSurf integration running in under a minute.**

That goal beats elegance, abstraction, and breadth. Pull requests that make
recipes shorter, clearer, or more self-contained get merged faster than ones
that add new files.

## Layout rules

- `recipes/<area>/<name>.{sh,py}` — one file per recipe, per language. No
  subpackages, no shared base classes (beyond `recipes/_common/intelsurf_http.py`).
- `ai-tools/<tool>.md` — one markdown per AI coding tool. Each follows the
  same outline: prereqs → install → auth → paste-this-prompt → worked example
  → gotchas.
- `openapi/openapi.json` — single committed snapshot. Refresh via
  `openapi/refresh.sh` before tagging a release.
- `mcp-server/` — its own pip-installable package. Self-contained; does not
  import from `recipes/`.

## Style

- **Python recipes**: stdlib only. The only currently-allowed exception is
  `recipes/scans/websocket_live_tail.py`, which needs `pip install websockets`
  (called out in the file header).
- **Shell recipes**: `#!/usr/bin/env bash`, `set -euo pipefail`, prefer
  `curl --fail-with-body --silent --show-error` over plain `curl`.
- **No frameworks.** No Click, no Typer, no Pydantic in recipes. Argv parsing
  with stdlib `argparse` or shell positionals only.
- **Configuration**: `INTELSURF_HOST` (default `https://dev.intel.surf`) and
  `INTELSURF_API_KEY` env vars. Never hardcode keys.
- **Naming**: snake_case for files, lowercase for endpoint slugs.

## Adding a recipe

1. Pick an area (`auth`, `selectors`, `scans`, `public_feed`) and a name.
2. Write the `.sh` first — it's the most copy-pasteable form for AI agents.
3. Mirror the `.sh` as `.py` using the helpers in
   `recipes/_common/intelsurf_http.py`.
4. Update [`recipes/README.md`](recipes/README.md) with a one-line entry.

## Adding an AI tool guide

Use [`ai-tools/claude-code.md`](ai-tools/claude-code.md) as the template.
Keep the outline identical so readers can cross-compare.

## PR review

We aim to triage PRs weekly. CI (`.github/workflows/lint-and-smoke.yml`)
runs `py_compile`, `bash -n`, and markdownlint — get a green tick before
asking for review.

## Out of scope

- A polished Python SDK. The CLI (private repo) already covers that surface.
- Tutorials longer than a single file. If a worked example needs >1 file,
  it belongs in a blog post, not here.
