# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-05-17 - Prevent Env Var Documentation Drift
**Learning:** Adding new fields to Pydantic Settings (config) without documenting them in the README Configuration section is a common drift pattern. This makes it difficult for users to know what configuration options are available.
**Action:** Created `scripts/check_env_vars.py` to introspect `Settings.model_fields` and verify that each `H4CKATH0N_{FIELD}` appears in `README.md`. Integrated this into CI so that any new configuration variable must be explicitly documented.
