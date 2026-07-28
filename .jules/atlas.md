# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
## 2026-02-28 - Replacing manual API routes with generated markers
**Learning:** Hardcoded API route lists in README files drift quickly as the application evolves (e.g. password auth extra features). Using an automated generation script with HTML markers (`<!-- ROUTES:START -->`) paired with OpenAPI's robust schema representation provides a reliable, drift-proof documentation surface that can be validated in CI without complex regex matching logic.
**Action:** When documenting API surfaces in Python apps (like FastAPI), always rely on generated schemas (like OpenAPI `app.openapi()['paths']`) dynamically replacing documentation via markers instead of manually updating static markdown lists.
