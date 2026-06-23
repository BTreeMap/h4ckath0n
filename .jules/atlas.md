# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-03-01 - Configuration environment variables are highly prone to drift
**Learning:** Hardcoded environment variable lists in READMEs routinely drift out of sync with actual configuration models (like Pydantic `BaseSettings`), leaving users unaware of valid config options.
**Action:** Implement drift-prevention checks that dynamically parse the application's configuration schema (e.g., `Settings.model_fields`) and verify that every accepted environment variable is explicitly documented.
