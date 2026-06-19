# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-02-28 - Env var docs drift
**Learning:** Manually updating environment variable docs in README.md inevitably leads to drift when new settings are added to Pydantic BaseSettings.
**Action:** Use Pydantic's `Field(description="...")` directly on the model, and use a script to automatically parse `model_fields` and generate the markdown table in the README between HTML comment delimiters. Run this script with a `--check` flag in CI.
