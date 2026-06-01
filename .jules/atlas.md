# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2024-06-01 - Config Drift Prevented
**Learning:** This repo has a `Settings` class in `src/h4ckath0n/config.py` that specifies all config variables using `H4CKATH0N_` prefix but relies on manual README updates, leading to drift. Adding a script `scripts/check_env_vars.py` parsing `Settings.model_fields.keys()` verifies README drift.
**Action:** Always check Pydantic Settings classes to identify the source of truth for config variables, and add a drift check if it's missing.
