# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
## 2023-10-23 - check_doc_routes.py misses nested routers
**Learning:** Iterating `app.routes` in a FastAPI application only yields top-level routes and instances of `_IncludedRouter` or `Mount`; it does not flatten or expose nested routes. The current check_doc_routes.py script reports "All 2 API routes are documented" (which is wrong, as there are 25 routes). To reliably enumerate all fully evaluated API endpoints (e.g., for drift checks), query the OpenAPI schema (`app.openapi().get('paths', {})`) instead, which automatically expands all mounted routers.
**Action:** Always parse OpenAPI schema for API route enumeration, not the raw `app.routes` which doesn't recurse.
