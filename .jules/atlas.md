# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-03-16 - Configuration docs drift when decoupled from source of truth

**Learning:** Manually listing configuration variables (e.g. env vars in README.md) inevitably drifts as the codebase evolves (e.g. Pydantic Settings models change). Using a programmatic drift check (e.g. reflecting over `Settings.model_fields.keys()`) against the docs string is an effective verification technique to catch missing variables.

**Action:** Whenever generating lists of configuration options, env vars, or similar attributes, write a drift check script that dynamically introspects the source of truth (e.g. the Pydantic model) and verifies each variable exists in the documentation string.
