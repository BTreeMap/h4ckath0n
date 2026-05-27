# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-02-28 - Env var drift prevention

**Learning:** Environment variables documented in README configuration tables frequently drift from the actual Pydantic `Settings` model fields as new features (like redis, storage, emails) are added.

**Action:** Added a drift-prevention script `scripts/check_env_vars.py` that iterates over `Settings.model_fields` to verify each variable is present in `README.md`.
