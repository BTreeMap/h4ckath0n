# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-02-28 - Config table manual maintenance leads to drift

**Learning:** Manually maintaining configuration variables in markdown tables leads to drift between the source of truth (`src/h4ckath0n/config.py` settings model) and the documentation.
**Action:** Use code-generated configuration tables directly from `pydantic.Field` descriptions and inject them using HTML comment markers. Always pair this with a `--check` CI flag to prevent future drift.
