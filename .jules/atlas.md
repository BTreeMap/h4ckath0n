# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
## 2025-03-01 - Fix doc drift prevention mechanisms
**Learning:** In FastAPI >= 0.115.0, `app.routes` no longer reliably exposes nested included routes. Pydantic `BaseSettings` configurations are also highly susceptible to drift, requiring an automated parser using `Settings.model_fields` and string matching against the docs.
**Action:** Use `app.openapi().get('paths', {})` instead of `app.routes` for authoritative API route enumeration. Enforce environment variable drift prevention by generating and checking all possible names against markdown docs in CI.
