# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2024-04-15 - Config Environment Variables Drift

**Learning:** Configuration environment variables defined in Pydantic models (like `Settings`) frequently drift from the documentation (e.g., `README.md`) because there is no automated parity check. Adding fields to `config.py` doesn't enforce a documentation update.

**Action:** Implemented a drift-prevention script (`scripts/check_doc_env.py`) that extracts fields from `Settings.model_fields` and asserts their corresponding `H4CKATH0N_` environment variable is documented in the README. Added this check to CI.
