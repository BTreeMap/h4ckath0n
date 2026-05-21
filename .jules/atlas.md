# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2023-11-20 - Ensure environment variables are documented and synchronized in README.md

**Learning:** We discovered that a significant number of environment variables defined in `src/h4ckath0n/config.py` using `pydantic-settings` were not documented in the `README.md`. It's easy for the documentation of configuration values to drift from the actual code.
**Action:** Created `scripts/check_env_vars.py` to enforce parity between configuration fields defined in `Settings` and those documented in `README.md`. Also added it to the CI pipeline to prevent future regressions. We should always check for undocumented config options using similar scripts.
