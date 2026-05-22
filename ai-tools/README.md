# AI coding tool integrations

One-paste setup guides for using IntelSurf from the major AI coding agents.
Every guide follows the same outline so you can cross-compare:

1. Prereqs
2. Install
3. Auth (API key)
4. Paste-this-prompt
5. Worked example
6. Gotchas

## Tool matrix

| Tool | Where it runs | Install ergonomics | IntelSurf surface | Guide |
| --- | --- | --- | --- | --- |
| [Claude Code CLI](claude-code.md) | local terminal | one-paste prompt | `intelsurf` CLI + recipes | **recommended starting point** |
| [Claude Cowork](claude-cowork.md) | Anthropic-hosted | secret + repo link | `intelsurf` CLI inside the sandbox | hosted convenience |
| [OpenAI Codex CLI](codex-cli.md) | local terminal | `npm i -g @openai/codex` | `intelsurf` CLI + recipes | parity with Claude Code |
| [Cursor / Aider / Continue.dev](cursor-aider-continue.md) | local IDE | tool-specific | `intelsurf` CLI as a shell tool | generic recipes |

## Pattern

Every integration boils down to the same three pieces:

1. **An `intelsurf` CLI** on the host the agent can shell out to. Install from
   [`dev.intel.surf/install/intelsurf.sh`](https://dev.intel.surf/install/intelsurf.sh).
2. **An API key** in the env (`INTELSURF_API_KEY=sk-slimestack-...`). Mint at
   [`dev.intel.surf/app/account/api-keys`](https://dev.intel.surf/app/account/api-keys).
3. **A system prompt or rules file** that tells the agent IntelSurf is
   available and where to find the recipes.

If you understand those three, every guide below is just the local dialect.

## What if my tool isn't listed?

The integration almost certainly works — every modern AI coding agent has a
shell tool. Read [`claude-code.md`](claude-code.md) for the canonical setup;
the only tool-specific piece is *how* you give the agent the IntelSurf system
prompt.

Open a [recipe request](../.github/ISSUE_TEMPLATE/recipe-request.md) if you
want a first-class guide for your tool.
