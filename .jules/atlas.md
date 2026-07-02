# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
## 2024-05-26 - Prevent Environment Variable Drift
**Learning:** Environment variables frequently diverge between the code (`src/h4ckath0n/config.py`) and documentation (`README.md`), leading to onboarding confusion and missing configurations.
**Action:** Always implement a dedicated drift-prevention check (like `scripts/check_env_vars.py`) that explicitly verifies documentation parity with the source of truth config structures (e.g. `Settings.model_fields` in pydantic-settings), and enforce it in CI alongside existing documentation checks.
