# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-03-01 - Enumerating FastAPI routes reliably for drift checks
**Learning:** In recent FastAPI versions (0.115+), iterating through `app.routes` directly obfuscates endpoints nested within `_IncludedRouter`s. This causes false negatives in drift checks, as the script misses most of the application's routes.
**Action:** Always use `app.openapi().get('paths', {})` to reliably retrieve all registered endpoints and their metadata.
