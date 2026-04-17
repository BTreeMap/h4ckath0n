# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-03-19 - Configuration documentation drift prevention
**Learning:** Hard-coded configuration tables in READMEs quickly drift from the code's truth.
**Action:** Always generate configuration documentation directly from the code source of truth (e.g. `pydantic.Field` descriptions) and use HTML comment markers (`<!-- CONFIG_TABLE_START -->`) to inject the generated output into markdown documents. Pair this with a CI check (`--check`) to fail builds if the generated documentation is out-of-sync.
