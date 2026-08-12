# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
## 2026-02-28 - FastAPI v0.115+ nested router drift check trap
**Learning:** Checking `app.routes` misses API endpoints if they are mapped inside internal routers (via `_IncludedRouter`), leading to incomplete documentation drift prevention checks.
**Action:** When extracting full list of endpoints for verification or generation, always use `app.openapi().get('paths', {})` instead of `app.routes`.
