# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-03-01 - OpenAPI schema for reliable route enumeration

**Learning:** Iterating `app.routes` in a FastAPI application only yields top-level routes and instances of `_IncludedRouter` or `Mount`; it does not flatten or expose nested routes. To reliably enumerate all fully evaluated API endpoints (e.g., for drift checks), query the OpenAPI schema (`app.openapi().get('paths', {})`) instead. Also, framework-provided paths (like `/openapi.json`, `/docs`, and `/redoc`) are automatically excluded, eliminating the need for manual filtering.

**Action:** Always use `app.openapi().get('paths', {})` to query for routes when building drift prevention scripts instead of iterating over `app.routes`.
