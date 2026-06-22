# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
## 2024-05-18 - Enforce Environment Variable Parity with Settings.model_fields
**Learning:** Checking documentation drift for environment variables against Pydantic settings requires using `Settings.model_fields` (in Pydantic V2) instead of accessing `.keys()` or iterating on the class directly to avoid `PydanticDeprecatedSince211` warnings.
**Action:** Always parse the source of truth (e.g., `model_fields` in `h4ckath0n.config.Settings`) dynamically and verify it against markdown documentation iteratively to prevent silent drift of env var documentation.
