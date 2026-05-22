# Cursor / Aider / Continue.dev

Generic recipes for AI coding tools that don't have a deep, first-class
integration like Claude Code or Codex but can still shell out to the
`intelsurf` CLI. The pattern is the same in every case:

1. Install the `intelsurf` CLI on the host.
2. Put `INTELSURF_API_KEY` in your env (or `~/.config/intelsurf/config.toml`).
3. Tell the agent IntelSurf exists via the tool's system-prompt mechanism.

Pick the section for your tool below.

---

## Cursor

[Cursor](https://cursor.sh) is a VS-Code fork with built-in chat + agent
modes. It runs shell commands through the IDE's terminal pane.

### Setup

```bash
# Install IntelSurf CLI globally.
/bin/bash -c "$(curl -fsSL https://dev.intel.surf/install/intelsurf.sh)"

# Verify in any Cursor terminal:
intelsurf whoami
```

Put the API key in `~/.config/intelsurf/config.toml` so Cursor's shell tool
inherits it without you re-exporting per session.

### Rules

Cursor reads `.cursor/rules` in the project root. Add:

```
You have access to the IntelSurf CLI (`intelsurf`) for OSINT and
threat-intel context. Quick reference:

  intelsurf surf <target> --wait        # full scan + intel report
  intelsurf tool run <slug> <target>    # one microservice tool
  intelsurf api METHOD /api/path        # generic REST passthrough

Recipes: github.com/TweekFawkes/IntelSurf-Examples/tree/main/recipes
OpenAPI: github.com/TweekFawkes/IntelSurf-Examples/blob/main/openapi/openapi.json

Reports land under ./intelsurf-runs/<scan_job_id>/.
```

Cursor's agent mode will read this file and reach for `intelsurf` when the
context calls for it.

---

## Aider

[Aider](https://aider.chat) is a Git-aware coding agent that pairs with any
LLM API. It runs shell commands via `/run` in the chat.

### Setup

```bash
# Install both.
pipx install aider-chat
/bin/bash -c "$(curl -fsSL https://dev.intel.surf/install/intelsurf.sh)"
export PATH="$HOME/.local/bin:$PATH"

# Or, if you prefer Python recipes over the CLI:
git clone https://github.com/TweekFawkes/IntelSurf-Examples
```

### System prompt

Aider takes `--message` or `--instructions-file` flags. Drop the system block
from [`claude-code.md`](claude-code.md) into a file and pass it:

```bash
aider --instructions-file intelsurf-instructions.md
```

### Usage

Inside Aider:

```
> /run intelsurf surf example.com --wait
> what does the intel report say about TLS?
```

Aider sees the `/run` output and incorporates it into the next reply.

---

## Continue.dev

[Continue.dev](https://continue.dev) is an open-source VS-Code / JetBrains
plugin similar to Cursor. Same shape: install the CLI, drop a system prompt
into the project config.

### Setup

```bash
# Install IntelSurf CLI.
/bin/bash -c "$(curl -fsSL https://dev.intel.surf/install/intelsurf.sh)"
```

### Project config

Edit `.continue/config.json` (or the equivalent for your install) and add an
entry to `systemMessage`:

```json
{
  "systemMessage": "You have access to the IntelSurf CLI (`intelsurf`) and the IntelSurf REST API at https://dev.intel.surf. Use it for OSINT and threat-intel work. Recipes: github.com/TweekFawkes/IntelSurf-Examples"
}
```

Continue's tool-use loop will reach for the shell when scanning is relevant.

---

## All three: gotchas

- **Default to the CLI**, not raw HTTP, unless you specifically need to embed
  the response in code. The CLI handles auth, retries, and PyCrucible
  bootstrap; raw HTTP via curl/requests gives you none of that.
- **API key surface area.** All three tools log shell output by default. If
  you've ever pasted `intelsurf api GET /api/...` with `Authorization`
  visible, that line is in the transcript. The CLI never echoes the key — use
  it.
- **Sandboxing.** Some installs of these tools sandbox shell commands. If
  `intelsurf` can't reach the network, check the tool's sandbox docs — you may
  need to allow-list `dev.intel.surf`.
- **Recipe shortcut.** When you want the agent to do something complex, point
  it at a recipe instead of writing a long prompt:

  > "Use the surf_one_shot recipe at
  > github.com/TweekFawkes/IntelSurf-Examples/blob/main/recipes/scans/surf_one_shot.py
  > to scan example.com."

  Every recipe is ≤200 LOC and self-explanatory — the agent reads, runs,
  reports.

## When to upgrade

If you find yourself writing the same IntelSurf prompts over and over in
these tools, consider [Claude Code](claude-code.md) or
[Codex CLI](codex-cli.md) — both have richer agent loops and the official
one-paste install path is already tuned for them.
