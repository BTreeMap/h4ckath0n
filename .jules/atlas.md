# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
## 2024-05-08 - Automated Env Vars Docs
**Learning:** Env vars configurations in `src/h4ckath0n/config.py` using `pydantic-settings` can easily get out of sync with manual `README.md` tables.
**Action:** Use a verification script (`scripts/generate_env_docs.py`) checked in CI to generate the markdown table from `pydantic.Field(description=...)` and ensure parity.
