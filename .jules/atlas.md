# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
## 2026-03-02 - FastAPI nested routers obscure endpoint enumeration
**Learning:** In FastAPI 0.115+, iterating over `app.routes` directly misses endpoints nested inside `_IncludedRouter` objects, leading to false negatives during route drift checks. It also fails when trying to access `.path` or `.methods` on these objects directly.
**Action:** Always parse the OpenAPI schema directly via `app.openapi().get('paths', {})` to safely and comprehensively enumerate all registered application routes.
