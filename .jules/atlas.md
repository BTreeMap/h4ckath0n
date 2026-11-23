# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
## 2024-05-18 - Route Enumeration and Documentation Parity
**Learning:** Iterating `app.routes` in a FastAPI application only yields top-level routes and instances of `_IncludedRouter`. It does not expose nested routes. To reliably enumerate all fully evaluated API endpoints, querying the OpenAPI schema (`app.openapi().get('paths', {})`) is required.
**Action:** Use `app.openapi().get('paths', {})` instead of `app.routes` for checking documentation parity.
