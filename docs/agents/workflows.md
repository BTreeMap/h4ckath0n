# Workflows

Exact commands and numbered procedures. Backend commands run from the repo root and use
`uv`; never call `pip` or `python` directly. Frontend commands run from
`packages/create-h4ckath0n/templates/fullstack/web/`.

## Backend CI quality gate

Run before committing any backend change. Format first, then verify in locked mode:

1. `uv run --locked ruff format .`
2. `uv run --locked ruff format --check .`
3. `uv run --locked ruff check .`
4. `uv run --locked mypy src`
5. `uv run --locked pytest -v`

Do not commit code that fails any of these. CI uses `uv sync --locked --all-extras` first.

## Required test surface

`pytest` integration tests (SQLite) must cover:

- passkey registration and login flow state
- WebAuthn challenge TTL and single-use behavior
- ID generators (length, prefix, charset)
- the last-passkey invariant (cannot revoke the last active passkey)
- device registration and revocation
- token verification (kid lookup, signature verification, `aud` separation)
- protected endpoint access driven by server-side DB authorization
- password auth lifecycle (when the password extra is enabled)

## Changing the API surface

When backend routes or schemas change, regenerate both checked-in artifacts in order:

1. Regenerate `api/openapi.json` from the FastAPI app.
2. Regenerate `web/src/api/openapi.ts` from `openapi.json` using the pinned generator in
   the web template. From the web directory: `npm run gen`.
3. Ensure at least one non-test web file imports types from `src/api/openapi.ts` and that
   `npm run typecheck` passes against them.

Never hand-edit the generated artifacts. Do not call `npx` in Node source — use
`npm exec --no -- ...`. See [docs/openapi/index.md](../openapi/index.md) for details.

## Frontend template checks

When changing files under `templates/fullstack/web/`, run from that directory:

1. `npm ci`
2. `npm run lint`
3. `npm run typecheck`
4. `npm test`
5. `npm run build`

## E2E quality guard (CI-equivalent)

Required when touching auth, passkeys, device auth, scaffolding, or OpenAPI type
generation. Run locally in a CI-equivalent way from the web directory and ensure it passes
before submitting:

1. `npm ci`
2. `npm exec --no -- playwright install --with-deps chromium`
3. `npm exec --no -- playwright test`

E2E must cover passkey registration/login, device-signed requests, the passkey management
UI (including the last-passkey revoke block), and generated OpenAPI types being usable.

## Scaffold CLI checks

When changing `packages/create-h4ckath0n/bin/` or `packages/create-h4ckath0n/lib/`:

1. `node packages/create-h4ckath0n/bin/cli.js --help`
2. In a temp directory:
   `node packages/create-h4ckath0n/bin/cli.js test-project --no-install --no-git`
3. Confirm the scaffolded project passes the web and api checks plus E2E above.
