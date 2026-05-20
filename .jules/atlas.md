# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2024-03-24 - Env Var Doc Drift Prevention
**Learning:** Environment variables in `README.md` can easily drift from the definitions in `src/h4ckath0n/config.py`.
**Action:** Implement a verification script `scripts/check_doc_env_vars.py` that dynamically generates the env var table from `Settings` and compares it to the table in `README.md` to catch drift. Use `pydantic.Field` descriptions for the generated table.
