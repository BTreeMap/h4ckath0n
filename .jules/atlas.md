# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
## 2026-03-01 - Replace hand-written API docs with OpenAPI generated tables
**Learning:** Hand-written API endpoints in documentation quickly fall out of sync or get hidden behind new FastAPI structures (e.g., `_IncludedRouter`). Testing them via regex search can result in false positives or masking.
**Action:** Replace manual endpoint lists with markdown markers (`<!-- BEGIN API ROUTES -->`) and dynamically generate API documentation tables directly from the `app.openapi()` schema. Ensure the drift check verifies table inclusion rather than just keyword presence.
