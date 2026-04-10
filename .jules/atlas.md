# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
## 2024-04-10 - Config variable documentation drift
**Learning:** The repo had ~16 undocumented environment variables (e.g. storage, email, redis settings) because the README table was hand-written and easily forgotten when new fields were added to `Settings`.
**Action:** Used `pydantic.Field` descriptions on the `Settings` model as the single source of truth, and generated the markdown table in the README inside `<!-- BEGIN ENV VARS -->` markers using a drift-prevention script.
