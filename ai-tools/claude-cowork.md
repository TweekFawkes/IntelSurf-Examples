# Claude Cowork

[Claude Cowork](https://www.anthropic.com/claude) is Anthropic's hosted coding
agent — it runs in an Anthropic-managed sandbox you point at a Git repo.
Because Cowork is hosted, every "install IntelSurf" step has to happen inside
that sandbox; you can't pre-stage it on your laptop.

## Prereqs

- A Claude.ai account with Cowork access.
- A GitHub repo Cowork can clone (this one works; fork it if you want to add
  recipes).
- An IntelSurf API key.

## Configure the secret

Cowork environments inherit secrets you've added to your Claude account.
Add `INTELSURF_API_KEY` so the agent can use it without you pasting:

1. Go to your Cowork environment settings → **Secrets**.
2. Add `INTELSURF_API_KEY` with the `sk-slimestack-...` value minted at
   [`dev.intel.surf/app/account/api-keys`](https://dev.intel.surf/app/account/api-keys).
3. (Optional) Also add `INTELSURF_HOST=https://dev.intel.surf` if you want to
   target a non-default host.

Cowork redacts these in transcripts; the agent reads them at runtime.

## Paste-this-prompt — first message in a new Cowork environment

```
Clone https://github.com/TweekFawkes/IntelSurf-Examples and install the
IntelSurf CLI into the sandbox so I can drive scans from here.

Steps:
1. git clone https://github.com/TweekFawkes/IntelSurf-Examples /workspace/examples
2. /bin/bash -c "$(curl -fsSL https://dev.intel.surf/install/intelsurf.sh)"
3. export PATH="$HOME/.local/bin:$PATH"
4. The INTELSURF_API_KEY secret should already be in your env from my
   Cowork settings. Confirm by running `intelsurf whoami`.
5. Read /workspace/examples/README.md and /workspace/examples/recipes/README.md
   so you know what's available.

Then wait for my next instruction.
```

After that, every follow-up prompt can assume `intelsurf` is on `$PATH`.

## Worked example

```
> Look at the open Linear issues tagged "ip-investigation" and run an
> IntelSurf deep scan against every IP we don't have a recent report for.
> Summarize the high-risk ones (>40) in a Linear comment.

[Cowork agent]
  - Pulls the Linear issues via your Linear MCP / API.
  - For each IP, runs:
      intelsurf surf <ip> --wait
  - Reads ./intelsurf-runs/<id>/intel.md.
  - Filters to risk_score > 40.
  - Posts a Linear comment per high-risk IP with the report link.
```

## Why use Cowork over Claude Code CLI?

- **No laptop setup.** Recipes run in the sandbox, not on your machine.
- **Always-on agents.** Schedule recurring "triage all new public scans"
  loops directly in Cowork instead of running them locally.
- **Shareable transcripts.** Output is rendered in the Claude.ai web UI; easy
  to drop into a ticket or PR.

The flip side: every scan triggers a CLI download inside the sandbox the first
time the agent runs `intelsurf`. PyCrucible's ~10s bootstrap happens on every
fresh container, not just once.

## Gotchas

- **Sandbox PATH.** Cowork resets `$PATH` between commands in some setups.
  Either run the export at the top of every script, or symlink the binary into
  `/usr/local/bin` once during setup.
- **Long-running scans.** Deep scans can take several minutes. Cowork commands
  have a default timeout; either use `--scan-mode quick` or have the agent
  kick off the scan + return immediately, then poll the next turn.
- **Secret rotation.** Cowork caches the env from secret-set time. If you
  rotate `INTELSURF_API_KEY`, restart the environment so the new value loads.

## Cross-reference

- The exact CLI install steps Cowork follows live at
  [`https://dev.intel.surf/install/intelsurf.md`](https://dev.intel.surf/install/intelsurf.md).
- Once installed, the [Claude Code guide](claude-code.md) section on "system
  prompt" applies identically — drop the same `system` block in your Cowork
  project so Cowork knows the conventions.
