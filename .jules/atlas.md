# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
## 2026-05-25 - Prevent Environment Variable Documentation Drift
**Learning:** In a fast-moving repo with centralized configuration via pydantic-settings (`src/h4ckath0n/config.py`), new configuration fields are frequently added (e.g. email, storage, redis, demo mode) but the README.md documentation drifts out of sync.
**Action:** Created `scripts/check_env_vars.py` to introspect `Settings.model_fields` and assert that every configuration variable exists in `README.md`. Will add this script to the CI quality gates.
