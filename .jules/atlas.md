# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-03-01 - Configuration Drift Prevention

**Learning:** When ensuring configuration values (like Pydantic `Settings`) are properly documented in README.md, you must also be mindful of environment variable prefixes (`H4CKATH0N_`) and possible exceptions like `OPENAI_API_KEY`.
**Action:** When adding drift checks for configurations, parse the application's configuration models directly (e.g. `Settings.model_fields.keys()`), reconstruct the expected environment variable name, and grep for it in the documentation.
