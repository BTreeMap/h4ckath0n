# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
## 2024-07-22 - Extract endpoints accurately from OpenAPI for generated doc routes
**Learning:** In FastAPI (v0.138+), iterating `app.routes` misses endpoints from included sub-routers (`_IncludedRouter`), causing drift-prevention checks to fail to verify all endpoints.
**Action:** To reliably extract all endpoints for route generation or drift checks, parse the OpenAPI schema via `app.openapi()['paths']` instead. Prefer generating endpoint docs from source and wrapping them in HTML comment markers rather than using regex parsing to verify manually maintained lists.
