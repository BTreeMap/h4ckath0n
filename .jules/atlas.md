# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
## 2025-04-12 - Prevented README.md environment variables drift

**Learning:** The configuration table in README.md is hand-written, which frequently drifts when new `Settings` variables are added or changed in `src/h4ckath0n/config.py`.
**Action:** Wrote `scripts/check_doc_env_vars.py` to parse Pydantic `Settings` and generate a markdown table of environment variables, with automated validation to enforce parity between the README and configuration fields. Added to `.github/workflows/ci.yml` as a backend CI gate.
