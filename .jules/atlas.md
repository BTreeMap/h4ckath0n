# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-03-01 - Pydantic settings drift in README documentation
**Learning:** The configuration variables derived from `pydantic-settings` easily drift from `README.md` as new features (like Redis, Storage, and Email support) are added to the `Settings` class without corresponding documentation updates.
**Action:** Implement a configuration drift-check script (`check_doc_config.py`) that iterates over `Settings.model_fields` and ensures every expected environment variable (with prefix `H4CKATH0N_`) appears in the `README.md`.
