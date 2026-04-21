# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
## 2024-05-18 - Environment variable drift
**Learning:** In h4ckath0n, environment variables configured in `src/h4ckath0n/config.py` can easily drift from `README.md` documentation since they are not coupled. New env vars often lack documentation or have outdated default values.
**Action:** Added `scripts/generate_env_docs.py` which dynamically reads `Settings.model_fields` and generates the markdown table for `README.md`. Included a `--check` flag to prevent regressions in CI.
