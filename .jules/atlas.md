# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
## 2026-10-10 - Pydantic Field descriptions for drift prevention
**Learning:** Hardcoding environment variable documentation in markdown files leads to drift. By embedding descriptions directly in the Pydantic `Settings` model using `Field(default, description='...')`, we can write scripts to auto-generate both markdown documentation and `.env.example` files from the codebase, guaranteeing parity.
**Action:** Always embed configuration documentation directly into the Pydantic models and generate docs from the source of truth, rather than duplicating the knowledge.
