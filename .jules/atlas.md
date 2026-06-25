# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
## 2024-06-25 - Settings documentation drift
**Learning:** README.md manually duplicates the `H4CKATH0N_` environment variables list from `src/h4ckath0n/config.py` but is missing variables like `H4CKATH0N_DEMO_MODE`, `H4CKATH0N_REDIS_URL`, `H4CKATH0N_STORAGE_DIR`, etc.
**Action:** Use Pydantic V2 `Field(description="...")` inline and build a drift-prevention script that parses `Settings.model_fields` to automatically generate the markdown table and inject it into README.md between marker tags.
