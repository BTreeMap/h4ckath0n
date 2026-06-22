# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-02-28 - Env var docs drift and generation

**Learning:** When using Pydantic Settings, environment variables often drift from the documentation because there's no native link between the model and the markdown file. I used a custom script (`check_env_vars.py`) to reflect on the `Settings` model fields and check if the resulting env vars exist in the README.
**Action:** When adding or modifying environment variables in Pydantic `Settings`, ensure to also document them in the `README.md` Configuration table. Create and run automated checks (like `scripts/check_env_vars.py`) on CI to ensure the parity between code and documentation is strictly maintained.
