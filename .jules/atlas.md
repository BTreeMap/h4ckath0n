# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-03-01 - Avoid hardcoded configuration lists in README

**Learning:** Environment variables and configuration options listed in READMEs frequently drift from the actual code definition (like `pydantic.BaseSettings`). In this repo, many properties were completely undocumented (like SMTP settings). Hardcoded lists are practically guaranteed to drift.

**Action:** Centralize config documentation directly on the code models (e.g. `pydantic.Field(description="...")`), generate the markdown table programmatically, and use HTML markers (`<!-- BEGIN CONFIG TABLE -->`) to inject it into the README. Add a check script hooked into CI to fail if the generated table drifts from the README.
