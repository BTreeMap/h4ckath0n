# Atlas Journal: Critical Learnings

## 2025-02-28 - Env var drift checks via pydantic-settings
**Learning:** Using `Settings.model_fields` to verify environment variables prevents hardcoded README drift and enforces single source of truth for config keys.
**Action:** When adding drift checks for environment variables using Pydantic Settings, dynamically parse `Settings.model_fields` and strictly match the variable name enclosed in backticks (e.g., `\`H4CKATH0N_ENV\``) to avoid false-positive substring matches.

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
