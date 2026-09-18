# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
## 2024-09-18 - Route Extraction Drift
**Learning:** In recent FastAPI versions, iterating through `app.routes` directly obfuscates endpoints nested within `_IncludedRouter`. This caused the documentation drift check to miss over a dozen routes and falsely report success.
**Action:** Always use `app.openapi().get('paths', {})` to reliably retrieve all registered endpoints and their metadata for drift-prevention checks.
