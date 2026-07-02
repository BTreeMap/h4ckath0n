# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-05-28 - Env vars drift between config loaders and documentation

**Learning:** Environment variables defined in configuration loaders (like Pydantic's `Settings`) frequently drift from the documentation (e.g., `README.md`). New variables are added to the code but authors forget to document them in the configuration tables, leading to a frustrating onboarding experience.

**Action:** Implement a drift prevention check that reads the actual configuration keys (e.g., via `Settings.model_fields`) and asserts their explicit presence in the documentation. Add this check to the CI pipeline to prevent future regressions.
