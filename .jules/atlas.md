# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-02-28 - Env vars table in README drifts from Pydantic Settings

**Learning:** The `README.md` hand-written environment variable table gets out of sync with `src/h4ckath0n/config.py` (e.g. missing Redis, Storage, and Email settings).
**Action:** Replaced the hand-written table with a generated section using `scripts/generate_env_docs.py` and `Pydantic` field descriptions. Added a CI step to enforce `--check`.
