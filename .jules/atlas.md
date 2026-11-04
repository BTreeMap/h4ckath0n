# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
## 2026-10-18 - Replacing handwritten ENV lists with a generated block is a massive win

**Learning:** Environment variables in documentation constantly drift. A handwritten list is almost guaranteed to be wrong, outdated, or incomplete.
**Action:** Always prefer to replace a hand-written environment variable markdown block with a script that generates the block (using `Field(..., description="...")` in Pydantic `Settings`) and inserts it via `<!-- ENV_START -->` / `<!-- ENV_END -->` markers. Add a CI test script to check that the current README and `.env.example` match the generated version.
