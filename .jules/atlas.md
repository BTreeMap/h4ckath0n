# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
## $(date +%Y-%m-%d) - Environment Variable Doc Drift Prevention
**Learning:** Hardcoding environment variable default values and descriptions in the `README.md` leads to inevitable drift when variables are added, modified, or when defaults are empty/lists/booleans.
**Action:** When working with Pydantic `Settings`, migrate plain type hints to `Field(description=...)` and automate generating the documentation markdown directly from the `Settings` schema. This creates a mathematically precise single source of truth.
