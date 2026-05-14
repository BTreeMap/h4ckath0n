# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-02-28 - Env var documentation drifts from Config schema

**Learning:** Environment variables in `README.md` easily drift from `Settings` in `src/h4ckath0n/config.py`. Using Pydantic's `Field(description="...")` allows the `Settings` class to act as the single source of truth for generating docs.

**Action:** Whenever a configuration drift is identified, generate a markdown table from the source configuration class (`pydantic.Settings`) and use a check script (`generate_env_docs.py --check`) in CI to enforce parity.
