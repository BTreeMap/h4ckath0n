# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-02-28 - Config to documentation drift

**Learning:** When using Pydantic settings, environment variables are often added or updated in the code but not properly reflected in `README.md`.
**Action:** Use Pydantic's `Field(description=...)` to generate the documentation from the source code, and use HTML comment markers (`<!-- CONFIG_TABLE_START -->`) to inject the generated table into the markdown. Verify this with a script in CI (`--check`) that compares the generated table against the existing `README.md` to prevent regressions.
