# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-03-02 - Pydantic Field metadata enables doc generation

**Learning:** When environment variables drift in READMEs, manually syncing them is error-prone. In projects using Pydantic `BaseSettings`, Pydantic's `Field(description=...)` can be used to add descriptions directly to the settings models without affecting runtime logic.
**Action:** Always prefer parsing Pydantic `model_fields` to extract config defaults and descriptions, using HTML comments as markers in the Markdown file, to automatically generate accurate documentation that cannot drift. Hook a check script into CI.
