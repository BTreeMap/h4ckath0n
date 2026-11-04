# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-03-01 - OpenAPI vs app.routes for drift checks

**Learning:** Using `app.routes` in FastAPI 0.115+ to enumerate API routes for documentation drift checks can lead to severe false negatives. It fails to expose endpoints nested within `_IncludedRouter`, meaning a missing doc might silently pass CI since the drift script cannot even "see" the route.
**Action:** Always use `app.openapi().get('paths', {})` as the definitive, machine-readable source of truth for drift scripts verifying FastAPI routes.
