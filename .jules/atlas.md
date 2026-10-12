# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
## 2024-10-12 - Drift prevention blindspots due to nested FastAPI routers and env aliases
**Learning:** `app.routes` misses endpoints nested in `_IncludedRouter` (e.g., from `app.include_router()`), causing false positives in route drift checks. Also, config parsers that assume a uniform prefix miss env vars with custom prefixes or legacy aliases.
**Action:** When validating FastAPI route parity, always parse `app.openapi().get("paths", {})` instead of `app.routes`. When validating env vars, explicitly account for known custom overrides (like `OPENAI_API_KEY` vs `H4CKATH0N_OPENAI_API_KEY`).
