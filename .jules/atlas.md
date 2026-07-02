# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-03-01 - Config drift prevention using Pydantic Settings

**Learning:** Documentation for environment variables often drifts from the source of truth, especially when new features or optional integrations (like Redis or SMTP) are added. The best way to prevent this in a FastAPI app using `pydantic-settings` is to dynamically parse `Settings.model_fields.keys()` and verify that each key exists in the documentation (usually prefixed with the app's env prefix, e.g. `H4CKATH0N_`). Exceptions to the prefix rule (like `OPENAI_API_KEY`) need to be handled explicitly.

**Action:** When adding config drift checks, import the settings model, iterate through `model_fields.keys()`, convert keys to upper case, and search the documentation for exact matches (e.g., using `re.search(rf"\`{env_var}\`", readme_text)`). Integrate this check into the CI pipeline to enforce parity permanently.
