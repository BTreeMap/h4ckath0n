# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2024-07-01 - Prevent configuration drift in docs
**Learning:** The `README.md` configuration section easily drifts from `src/h4ckath0n/config.py` because there was no programmatic check to enforce parity for environment variables.
**Action:** Added a `scripts/check_doc_config.py` script that iterates over `Settings.model_fields` and verifies that every config key is documented as `H4CKATH0N_<KEY>` in `README.md`. Also added this check to `ci.yml`.
