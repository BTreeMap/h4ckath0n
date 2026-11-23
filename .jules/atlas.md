# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-02-28 - FastAPI app.routes drift check limitation
**Learning:** Iterating `app.routes` in a FastAPI application only yields top-level routes and misses nested router paths, causing incomplete doc drift checks.
**Action:** Always query the OpenAPI schema (`app.openapi().get('paths', {})`) to enumerate all fully evaluated API endpoints for reliable drift prevention.
