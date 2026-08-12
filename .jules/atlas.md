# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-02-28 - Generating markdown docs from OpenAPI

**Learning:** When generating markdown docs from OpenAPI, do not destroy context. Pulling `summary` and `description` from the OpenAPI schema and rendering them into the documentation preserves usability and ensures no regression in "time-to-understanding". Always match the expected markdown format of the repo's original drift check scripts.

**Action:** When replacing hand-written route lists with dynamically generated ones, extract `summary` and `description` from `app.openapi().get("paths")` and format them to match the pre-existing structure (e.g. `- \`METHOD /path\` — summary. description.`).
