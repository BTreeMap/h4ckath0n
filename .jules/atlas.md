# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
## 2023-10-18 - [FastAPI Route Extraction Drift]
**Learning:** Extracting routes directly from `app.routes` in recent FastAPI versions (0.115+) misses endpoints nested within `_IncludedRouter` (which obfuscates sub-routers like `passkeys_router`, `jobs_router`, etc.). The verification script `scripts/check_doc_routes.py` silently passed because it only saw the root routes (`/` and `/health`).
**Action:** Always use `app.openapi().get('paths', {})` to reliably retrieve all registered endpoints and their metadata for documentation drift checks, rather than iterating through `app.routes`.
