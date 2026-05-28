# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2024-03-14 - Pydantic settings are the source of truth for config docs

**Learning:** Generating the environment variable docs natively from the Pydantic `Settings` model using string representations of defaults is more reliable than extracting them with regex or using manual lists, which are prone to drift. This provides an executable specification for the environment variables configuration.

**Action:** Add an automated doc-generation check script that reads the `Settings` schema directly using `Settings.model_fields.items()` and ensure it is hooked into the `backend` CI validation step.
