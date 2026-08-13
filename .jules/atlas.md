# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-03-05 - FastAPI routing tree introspection misses nested endpoints
**Learning:** In newer FastAPI versions (v0.115+), nested routers are wrapped internally as `_IncludedRouter` objects which hide their `.path` and `.methods` properties, breaking simple `app.routes` iteration when verifying endpoints.
**Action:** When writing scripts to check endpoint drift or generate documentation, always parse the generated OpenAPI schema (`app.openapi().get('paths', {})`) instead of walking the routing tree manually.
