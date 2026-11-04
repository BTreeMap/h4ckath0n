# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
## 2026-02-28 - FastAPI app.routes does not flatten nested routers
**Learning:** Iterating `app.routes` in FastAPI only yields top-level routes and `_IncludedRouter` / `Mount` instances, which misses all nested routes. The only reliable way to enumerate all fully evaluated API routes without framework paths (like `/docs`) is to query `app.openapi().get("paths", {})`.
**Action:** Always use the OpenAPI schema to extract API endpoints for drift checks instead of directly iterating `app.routes`.
