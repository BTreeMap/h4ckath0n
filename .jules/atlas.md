# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-03-01 - Generated Tables for Env Vars
**Learning:** Handwritten tables for environment variables drift easily because new settings are added to the code but not the docs. Relying on manually syncing descriptions is error-prone.
**Action:** Add descriptions directly in Python code (e.g., using `pydantic.Field(description=...)`) and use a drift-prevention script to generate the markdown table between `<!-- GENERATED_ENV_VARS_START -->` and `<!-- GENERATED_ENV_VARS_END -->` markers. Add a `--check` flag to run in CI.
