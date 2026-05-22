# OpenAPI mirror

A checked-in snapshot of [`https://dev.intel.surf/api/openapi.json`](https://dev.intel.surf/api/openapi.json)
so you can browse the full IntelSurf REST surface — request schemas, response
schemas, operation IDs — without booting the app or hitting the live host.

## Files

- [`openapi.json`](openapi.json) — the spec itself, pretty-printed.
- [`refresh.sh`](refresh.sh) — re-fetch from `INTELSURF_HOST`
  (default `https://dev.intel.surf`) and overwrite `openapi.json`.

## Drift

The snapshot **goes stale** every time the live API adds, removes, or changes
an endpoint. There's no automated drift check in CI (yet). The convention is:

- Re-run [`refresh.sh`](refresh.sh) before tagging a release of this repo.
- If you notice a recipe that contradicts the spec, refresh first, then fix the
  recipe.

## Reading the spec

The spec ships in raw JSON. To browse it interactively, the easiest paths are:

- **Live Swagger UI** at [`dev.intel.surf/api/docs`](https://dev.intel.surf/api/docs).
- **Redoc** at [`dev.intel.surf/api/redoc`](https://dev.intel.surf/api/redoc).
- **Generate a client** with [`openapi-generator`](https://openapi-generator.tech/)
  or [`openapi-python-client`](https://github.com/openapi-generators/openapi-python-client)
  against `openapi.json`. The `intelsurf` CLI itself uses this approach — see
  the `intelsurf rest` subcommands in the CLI docs.

## Refreshing

```bash
./openapi/refresh.sh
git diff openapi/openapi.json   # eyeball the changes
git commit -am "openapi: refresh mirror (<short summary>)"
```

If you're pointing at a non-default host (e.g. local dev), set
`INTELSURF_HOST` first.
