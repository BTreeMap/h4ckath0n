# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-02-28 - Env vars configuration drift
**Learning:** There was a documentation gap where configuration environment variables available via `pydantic-settings` were not documented in the README. We can introspect Pydantic V2 `BaseSettings` via `.model_fields` and extract all env vars.
**Action:** Add a drift-prevention script that parses `Settings.model_fields` to automatically detect missing env var docs and run it in CI to prevent regression.
