# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
## 2025-04-03 - Generate env vars table to prevent doc drift
**Learning:** Hardcoded environment variables tables in markdown files are prone to drifting as the system settings schema evolves.
**Action:** Rely on a central config file (`src/h4ckath0n/config.py`) using `pydantic.Field` descriptions as a single source of truth, and generate/enforce parity in `README.md` through a drift-prevention script (`scripts/check_doc_env_vars.py`).
