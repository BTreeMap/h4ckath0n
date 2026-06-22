# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2024-05-20 - Ensure Config and Env Vars Docs Drift Parity

**Learning:** Pydantic models (like `Settings`) are the source of truth for application configuration, but their corresponding environment variable forms often drift in documentation. Relying on manual updates or searching for the exact doc variable string can lead to missing properties.

**Action:** Add scripts that iterate over the Pydantic `Settings.model_fields` to programmatically generate the expected environment variable keys (e.g. `H4CKATH0N_` + field name), then verify their explicit existence inside `README.md` and include this drift-prevention script in CI.
