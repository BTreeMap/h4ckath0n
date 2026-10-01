# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-03-01 - Endpoints nested within _IncludedRouter obfuscate route drift checks in recent FastAPI versions

**Learning:** Since FastAPI 0.115+, traversing `app.routes` directly is no longer reliable because endpoints coming from `include_router` are encapsulated within `_IncludedRouter` blocks which do not expose `methods` and `path`. Scripts doing documentation-drift checking on routes need to leverage standard OpenAPI schemas.

**Action:** When programmatically enumerating routes for drift checks, always utilize `app.openapi().get("paths", {})` to retrieve the registered endpoints and their operational metadata reliably.
