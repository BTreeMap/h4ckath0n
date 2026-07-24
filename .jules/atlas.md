# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2024-07-24 - Missed FastAPI Routes in Drift Checks
**Learning:** In FastAPI (v0.138+), iterating `app.routes` misses endpoints from included sub-routers (`_IncludedRouter`), causing drift checks to falsely under-report total endpoints.
**Action:** To reliably extract all endpoints for route generation or drift checks, always parse the OpenAPI schema via `app.openapi()['paths']` instead of iterating `app.routes`.
