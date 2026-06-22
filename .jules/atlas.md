# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-02-28 - Env var documentation parity

**Learning:** Environment variables frequently drift between config definitions and documentation, especially when using auto-populating config mechanisms like Pydantic settings. Adding a check script that compares `Settings.model_fields` against the `README.md` documentation reliably catches this drift.

**Action:** Add drift prevention checks that map config variables generated from the source code directly to the documentation (e.g., using a custom script like `check_env_vars.py`) and wire them into CI.
