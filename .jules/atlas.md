# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-02-28 - Config Table drift prevention

**Learning:** Documentation for environment variable configurations is likely to drift from code. Simply keeping configurations in README.md will end up generating bugs.
**Action:** Extract descriptions from Pydantic `Field` and generate the Config table to prevent any out of date configurations. Add a CI test that calls `uv run --locked scripts/generate_doc_config.py --check` and fails the test if any changes are made.
