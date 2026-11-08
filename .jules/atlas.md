# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-02-28 - FastAPI app.routes fails to expose nested router endpoints

**Learning:** Iterating `app.routes` in a FastAPI application only yields top-level routes and `_IncludedRouter` instances. This fails to expose nested API endpoints, which breaks route enumeration for documentation drift checks.

**Action:** To reliably enumerate all fully evaluated API endpoints, always query the OpenAPI schema using `app.openapi().get('paths', {})` instead of `app.routes`.
