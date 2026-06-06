# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-06-06 - Pydantic Settings drift check technique
**Learning:** Documenting Pydantic Settings environment variables is a common source of drift. Dynamically parsing `Settings.model_fields` and strictly matching the full variable name (prefixed with `H4CKATH0N_` and enclosed in backticks) reliably catches undocumented configs and avoids false-positive substring matches.
**Action:** Create a script that iterates over `Settings.model_fields` and asserts that each corresponding environment variable is enclosed in backticks within the configuration documentation. Integrate this script into CI.
