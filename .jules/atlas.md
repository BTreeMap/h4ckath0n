# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
## 2024-07-28 - Generated Route Documentation
**Learning:** In FastAPI, iterating `app.routes` misses endpoints from included sub-routers. Manually maintained route lists in README drift easily.
**Action:** Use OpenAPI (`app.openapi()['paths']`) to extract reliable route data, and use `check_doc_routes.py` as a generator that enforces parity in CI.
