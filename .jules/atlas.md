# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2024-05-24 - Generated documentation prevents drift
**Learning:** Hand-written documentation of API endpoints is highly prone to drift. Replacing static lists scattered across README sections with a single, dynamically generated block using markers (like `<!-- BEGIN API ROUTES -->`) ensures complete parity between the code and docs.
**Action:** Instead of just checking if routes are mentioned, generate the authoritative documentation directly from the app (e.g. via OpenAPI schema) and insert it with a `--fix` script flag.
