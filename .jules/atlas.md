# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2024-05-30 - Environment variables drift silently
**Learning:** Pydantic `Settings` models can easily fall out of sync with README.md tables because there is no built-in linkage. Without explicit checks, default values and new features introduced in `config.py` are frequently undocumented in configuration guides.
**Action:** Always implement a dynamic schema-reflection script (e.g., `scripts/check_env_vars.py`) that loops through Pydantic fields, formats them with their environment variable prefix, and `grep`s the README, running this script as a mandatory CI step.
