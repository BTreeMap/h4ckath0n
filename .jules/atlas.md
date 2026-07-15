# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-02-28 - FastAPI route iteration misses nested sub-routes
**Learning:** In newer versions of FastAPI (>=0.115.0), routes added via `include_router` are encapsulated within `_IncludedRouter` objects rather than being flattened into `app.routes`. Iterating directly over `app.routes` will miss all sub-routes, causing drift checks to silently pass when they should fail.
**Action:** To accurately enumerate all flattened API paths (e.g. for drift checks), parse the generated OpenAPI schema via `app.openapi().get('paths', {})` instead of looping over `app.routes`.
