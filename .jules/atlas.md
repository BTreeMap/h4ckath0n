# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2024-05-29 - Config Env Var Drift
**Learning:** Configuration environment variables drift easily between the pydantic Settings model and the README documentation.
**Action:** Created a script `scripts/check_env_vars.py` that parses `Settings.model_fields` and verifies each corresponding `H4CKATH0N_VAR` is documented in `README.md` and added it to CI.
