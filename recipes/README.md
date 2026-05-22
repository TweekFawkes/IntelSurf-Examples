# Recipes

One file per recipe, one recipe per endpoint or workflow. Each runs standalone
with `bash foo.sh` or `python foo.py`. Python recipes share
[`_common/intelsurf_http.py`](_common/intelsurf_http.py) — a 150-line `urllib`
wrapper. No third-party deps (except where called out in the file header).

## Configuration

```bash
export INTELSURF_HOST="https://dev.intel.surf"   # default; override for stage/prod
export INTELSURF_API_KEY="sk-slimestack-..."     # required for authenticated recipes
```

Mint an API key at
[dev.intel.surf/app/account/api-keys](https://dev.intel.surf/app/account/api-keys).

## Index

### Public (no auth)

| Recipe | Endpoint | Notes |
| --- | --- | --- |
| [`public_feed/list_public_scans`](public_feed/) | `GET /api/public/scans` | 60/min/IP |
| [`public_feed/submit_anonymous`](public_feed/) | `POST /api/scan-jobs/anonymous` + slug poll | 5/hour, 20/day/IP |
| [`selectors/extract`](selectors/) | `POST /api/selectors/extract` | NLP → selector candidates; 30/hour/IP |

### Authenticated (API key required)

| Recipe | Endpoint | Notes |
| --- | --- | --- |
| [`auth/register`](auth/) | `POST /api/auth/register` | invite code may be required |
| [`auth/login_session`](auth/) | `POST /api/auth/login` | cookie auth |
| [`auth/me`](auth/) | `GET /api/auth/me` | works with cookie or Bearer |
| [`selectors/create_list`](selectors/) | `POST /api/selectors` + `GET /api/selectors` | |
| [`selectors/patch_tags`](selectors/) | `PATCH /api/selectors/{id}/tags` | tag add/remove |
| [`scans/surf_one_shot`](scans/) | full workflow | mirror of `intelsurf surf` |
| [`scans/create_scan`](scans/) | `POST /api/scan-jobs` | |
| [`scans/poll_scan`](scans/) | `GET /api/scan-jobs/{id}` | poll loop |
| [`scans/download_report`](scans/) | `GET /api/reports/{id}/intel.{ext}` | md / json / pdf |
| [`scans/websocket_live_tail.py`](scans/) | `WS /api/scan-jobs/{id}/ws` | **needs `pip install websockets`** |

## Rate limits

- Anonymous scan submit: 5/hour, 20/day per IP.
- Public scan feed: 60/min per IP.
- Selector extraction: 30/hour per IP.

HTTP 429 = rate limit. The API isn't broken; wait or authenticate.

## Conventions

- All recipes read `INTELSURF_HOST` (default `https://dev.intel.surf`).
- All authenticated recipes read `INTELSURF_API_KEY`.
- Python recipes import the shared HTTP helper via:

  ```python
  sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
  from _common.intelsurf_http import host_from_env, http_request
  ```

  Three lines of boilerplate per recipe; keeps recipes self-contained while
  still sharing the cookie/SSL/error plumbing.

- Shell recipes use `curl --fail-with-body` so non-2xx bodies still print
  before the script exits non-zero.

See the [`openapi/`](../openapi) mirror for the full endpoint surface and
exact request/response schemas.
