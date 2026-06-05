# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2025-06-05 - Environment Variable Docs Drift Check
**Learning:** The configuration table in README.md easily falls out of sync with `Settings` in `src/h4ckath0n/config.py` (e.g., Redis, email, storage settings were missing). Manual documentation updates are prone to omissions as the app's configuration grows.
**Action:** Created `scripts/check_doc_env_vars.py` and added it to the CI pipeline to enforce that every environment variable defined in Pydantic's `Settings.model_fields` is strictly matched within backticks in `README.md`. Handle exceptions like `OPENAI_API_KEY` explicitly.
