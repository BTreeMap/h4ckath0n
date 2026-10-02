# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
## 2026-02-28 - OpenAPI path extraction in FastAPI 0.115+
**Learning:** Checking `app.routes` directly is unreliable in recent FastAPI versions (0.115+) because it obscures routes nested in `_IncludedRouter`. This leads to false positives/negatives in drift checks that iterate over routes directly.
**Action:** Always extract the definitive API surface by accessing `app.openapi().get("paths", {})` and iterating through paths and methods from the generated OpenAPI schema.
