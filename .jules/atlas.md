# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-06-09 - Pydantic V2 dynamic model extraction for environment variable parity

**Learning:** Environment variables frequently drift because developers add fields to Pydantic Settings models but forget to document them. `BaseSettings` auto-generates env var names based on an `env_prefix` and field names, meaning hardcoding env vars in drift checks is brittle. Furthermore, multiple settings models (`Settings`, `ObservabilitySettings`) can exist with different prefix logic.
**Action:** When validating environment variable documentation, dynamically extract fields from Pydantic `model_fields`, prepend the correct app-specific prefix (handling exceptions like `OPENAI_API_KEY`), and match exact variables enclosed in backticks (e.g. `` `H4CKATH0N_ENV` ``) to avoid substring matches.
