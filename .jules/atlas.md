# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2024-03-24 - OpenAPI vs app.routes for FastAPI endpoint discovery
**Learning:** Iterating `app.routes` in a FastAPI application only yields top-level routes and `_IncludedRouter` instances, failing to expose nested endpoints.
**Action:** To reliably enumerate all fully evaluated API endpoints (e.g. for drift checks), always query the OpenAPI schema using `app.openapi().get('paths', {})`.
