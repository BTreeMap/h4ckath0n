# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2024-11-09 - Iterating `app.routes` misses nested routes

**Learning:** When listing endpoints for documentation or drift checks in FastAPI, iterating through `app.routes` only yields top-level routes and `_IncludedRouter` instances. This approach completely misses sub-routes defined within those nested routers, leading to incomplete validation.
**Action:** Always fetch the evaluated endpoint list from the OpenAPI schema (e.g., `app.openapi().get('paths', {})`) rather than querying `app.routes` directly to guarantee that all fully instantiated endpoints are found.
