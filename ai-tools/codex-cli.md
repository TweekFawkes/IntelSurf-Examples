# OpenAI Codex CLI

The [OpenAI Codex CLI](https://github.com/openai/codex) is OpenAI's
terminal-based coding agent. Setup mirrors Claude Code — install the
`intelsurf` CLI locally, give Codex a system prompt that knows about it,
done.

## Prereqs

- Node.js 18+ (for `npm i -g @openai/codex`).
- An OpenAI API key in `OPENAI_API_KEY`.
- An IntelSurf API key in `INTELSURF_API_KEY`.

## Install both CLIs

```bash
# OpenAI Codex
npm i -g @openai/codex
codex --version

# IntelSurf
/bin/bash -c "$(curl -fsSL https://dev.intel.surf/install/intelsurf.sh)"
export PATH="$HOME/.local/bin:$PATH"
intelsurf health
```

Persist both PATH entries in your shell rc file
(`~/.zshrc` or `~/.bashrc`).

## Auth

Mint API keys for each side:

```bash
# OpenAI
export OPENAI_API_KEY="sk-..."

# IntelSurf
export INTELSURF_HOST="https://dev.intel.surf"
export INTELSURF_API_KEY="sk-slimestack-..."     # dev.intel.surf/app/account/api-keys
```

Or write the IntelSurf key to `~/.config/intelsurf/config.toml`:

```toml
host = "https://dev.intel.surf"
api_key = "sk-slimestack-..."
```

`chmod 600` after writing.

## Paste-this-prompt — Codex system prompt

Codex reads `~/.codex/system.md` (or a project-local override). Drop this:

```
You have the IntelSurf CLI (`intelsurf`) and its companion REST API at
https://dev.intel.surf available in this shell. Use them whenever you need
OSINT, threat-intel, or infrastructure context on a target.

Quick reference:
  intelsurf surf <target> --wait       # full scan + intel report
  intelsurf scan get <id>              # scan state
  intelsurf report get <id>            # download report (md/json/pdf)
  intelsurf tool list                  # list microservice tools
  intelsurf tool run <slug> <target>   # run one tool

Escape hatches:
  intelsurf api GET /api/projects
  intelsurf rest <tag> <op>            # auto-generated wrappers
  intelsurf openapi --summary          # discover endpoints

Recipes: https://github.com/TweekFawkes/IntelSurf-Examples/tree/main/recipes
OpenAPI:  https://github.com/TweekFawkes/IntelSurf-Examples/blob/main/openapi/openapi.json

Conventions:
- The CLI auto-loads INTELSURF_HOST and INTELSURF_API_KEY from
  ~/.config/intelsurf/config.toml. Don't echo the key.
- Reports land under ./intelsurf-runs/<scan_job_id>/.
- Public-feed and selector-extract endpoints work without an API key.
```

## Worked example

```
$ codex
> scan example.com with intelsurf and summarize the highlights
[codex] running: intelsurf surf example.com --wait
[codex] # selector 142 ready (Domain: example.com)
[codex] # scan_job_id=88
[codex] # state=complete  risk_score=5
[codex] # wrote ./intelsurf-runs/88/intel.md
[codex] # cat ./intelsurf-runs/88/intel.md | head -50
[codex] ...
[codex] Summary:
  - Cloudflare-fronted, valid TLS, DNSSEC enabled.
  - IANA documentation reservation; zero threat hits.
  - Risk 5/100. Safe.
```

## Worked example — Python recipe (no CLI)

If you want Codex to use HTTP directly (e.g. to integrate into a script):

```
> use the recipe at recipes/scans/surf_one_shot.py from
> github.com/TweekFawkes/IntelSurf-Examples to scan example.com.
> i've already set INTELSURF_API_KEY in my env.

[codex] git clone https://github.com/TweekFawkes/IntelSurf-Examples /tmp/examples
[codex] python /tmp/examples/recipes/scans/surf_one_shot.py example.com
[codex] ...
```

## Gotchas

- **Two API keys.** Codex needs `OPENAI_API_KEY`; IntelSurf needs
  `INTELSURF_API_KEY`. Don't confuse them — both start with `sk-`.
- **PATH after install.** The `intelsurf.sh` installer writes to
  `~/.local/bin/intelsurf`. Make sure that's on `$PATH` before Codex runs,
  or call it by absolute path in your system prompt.
- **Codex sandboxing.** Recent Codex builds run commands in a restricted
  sandbox by default. If `intelsurf` can't see your env, either start Codex
  with `--no-sandbox` (when you trust the project) or pre-bake the key into
  `~/.config/intelsurf/config.toml`.
- **Long-running scans.** `--wait` blocks until terminal. For multi-minute
  deep scans, prefer `intelsurf scan start <target>` + `intelsurf scan wait
  <id>` so Codex can do other work in between.
