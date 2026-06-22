# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-03-01 - Config field names drift from README if not strictly checked

**Learning:** Pydantic `BaseSettings` configurations often grow new variables (e.g., SMTP configurations, max upload bytes, etc.) that get missed in the documentation. In order to catch drift accurately, environment variables need to be formatted exactly as they appear in the documentation (usually enclosed in backticks) and include the app prefix to avoid false-positive matches within prose.

**Action:** Generate the full environment variables programmatically via `Settings.model_fields`, append the app prefix (and account for exceptions like `OPENAI_API_KEY`), and match against markdown-formatted backticks `` `H4CKATH0N_VAR` `` in `README.md`.
