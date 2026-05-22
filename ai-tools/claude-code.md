# Claude Code CLI

[Claude Code](https://docs.claude.com/en/docs/claude-code/overview) is
Anthropic's terminal-based coding agent. This guide gives Claude Code the
ability to drive IntelSurf — scan targets, run individual tools, fetch intel
reports — by installing the `intelsurf` CLI on your machine and pointing
Claude Code at it.

## Prereqs

- macOS on Apple Silicon (arm64), Linux x86_64, or Linux ARM64. Windows works
  via the binary download but isn't covered by the one-paste install below.
- [Claude Code](https://docs.claude.com/en/docs/claude-code/overview) installed
  and logged in.
- A free IntelSurf account.

## One-paste install (recommended)

Open Claude Code and paste this prompt verbatim. Claude Code will fetch the
full step-by-step instructions from dev.intel.surf and run them, asking only
for your API key when needed.

```
Please install and configure the IntelSurf CLI on this machine for me.

Fetch the full step-by-step instructions from the URL below and follow
them exactly. The document is written for you (an AI coding agent) - it
specifies which shell commands to run, when to ask me for input, and
how to verify the install worked.

  https://dev.intel.surf/install/intelsurf.md

Assumptions baked into the guide:
- This laptop is macOS on Apple Silicon (arm64).
- I want the CLI binary at ~/.local/bin/intelsurf.
- The CLI should authenticate against https://dev.intel.surf.

When you finish, run `intelsurf whoami` and show me the output so I know
it's wired up.
```

If you're on Linux, swap the assumption block; the install guide branches
on `uname -sm`.

The page Claude Code fetches walks through downloading the matching binary,
stripping macOS quarantine xattrs, putting `~/.local/bin` on `$PATH`, prompting
you for an API key, and writing `~/.config/intelsurf/config.toml` with
`chmod 600`. Total time: ~30 seconds plus however long minting an API key
takes.

## Mint an API key

When the install guide asks for an API key:

1. Open [`dev.intel.surf/app/account/api-keys`](https://dev.intel.surf/app/account/api-keys).
2. Click **New key**, give it a name, copy the `sk-slimestack-...` secret
   (shown exactly once).
3. Paste it back to Claude Code.

The key gets written to `~/.config/intelsurf/config.toml` with mode `600`. It
never leaves your machine.

## Verify

```bash
intelsurf health        # round-trips dev.intel.surf
intelsurf whoami        # prints your user
intelsurf tool list     # lists every microservice tool
```

## Paste-this-prompt — give Claude Code a system prompt for IntelSurf

After the install, paste this so Claude Code knows IntelSurf is available
in every future session in this project:

```
You have access to the IntelSurf CLI (`intelsurf`) and its companion REST
API at https://dev.intel.surf. Use them whenever you need OSINT or
infrastructure context on a target.

Hand-tuned typed flows (prefer these):
  intelsurf surf <target> --wait       # full scan + intel report
  intelsurf scan get <id>              # scan state
  intelsurf report get <id>            # download intel/summary/raw report
  intelsurf tool list                  # list available microservice tools
  intelsurf tool run <slug> <target>   # run a single tool

Generic escape hatches:
  intelsurf api GET  /api/projects
  intelsurf api POST /api/scan-jobs --body '{"selector_id":42}'
  intelsurf rest <tag> <op>            # auto-generated typed wrappers
  intelsurf openapi --summary          # discover everything

Worked examples live at https://github.com/TweekFawkes/IntelSurf-Examples
(recipes/ for HTTP, ai-tools/ for setup guides).

Conventions:
- The CLI reads INTELSURF_HOST and INTELSURF_API_KEY from
  ~/.config/intelsurf/config.toml. Don't echo the key.
- Reports land under ./intelsurf-runs/<scan_job_id>/ by default.
- Public scan feed and selector extraction work without an API key.
```

Or save it to `.claude/system.md` and Claude Code picks it up automatically.

## Worked example

```
> Triage example.com for me. Run a deep scan and summarize the intel report
> highlights in three bullets.

[Claude Code does]
  intelsurf surf example.com --wait
  # selector 142 ready (Domain: example.com)
  # scan_job_id=88
  # ...
  # wrote ./intelsurf-runs/88/intel.md
  # cat ./intelsurf-runs/88/intel.md
  # ...

[Claude Code replies]
- TLS chain valid, served by Cloudflare WAF, DNSSEC enabled.
- WHOIS shows IANA assignment (reserved documentation domain).
- Zero threat-intel hits across ten feeds; risk score 5/100.
```

## Gotchas

- **First run is slow.** PyCrucible bootstraps the embedded Python env on
  first launch (~5–15s). Subsequent runs are instant.
- **macOS quarantine.** The install guide strips `com.apple.quarantine` /
  `com.apple.provenance` xattrs. If `intelsurf` SIGKILLs on launch, those
  xattrs sneaked back; re-run `xattr -d com.apple.quarantine` on the binary.
- **HTTP 401 on `whoami`.** API key was rejected. Mint a new one and update
  `~/.config/intelsurf/config.toml`.
- **`rest` subgroup is empty.** The typed wrappers package wasn't regenerated
  since the last spec change. Run `intelsurf openapi --summary` to confirm
  endpoints are visible, then ask the IntelSurf team to redeploy.

## Now try a recipe

Once `intelsurf whoami` works, the [recipes](../recipes) in this repo are the
fastest way to learn what the API can do. Start with:

```bash
git clone https://github.com/TweekFawkes/IntelSurf-Examples
cd IntelSurf-Examples
python recipes/scans/surf_one_shot.py example.com
```
