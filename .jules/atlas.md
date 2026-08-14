# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2024-08-14 - OpenAPI generation required to discover endpoints in FastAPI v0.115+
**Learning:** In newer versions of FastAPI, paths defined inside routers are hidden inside `_IncludedRouter` entries in `app.routes`. Iterating over `app.routes` no longer reliably yields all API endpoints.
**Action:** Always parse the OpenAPI schema via `app.openapi().get('paths', {})` to reliably enumerate registered endpoints for docs-generation or drift checks.
